#!/usr/bin/env python3
"""Спортлото «5 из 36» (5 из 36 + 1 из 4): архив тиражей, проверка случайности и выбор момента для игры
на главные призы.

Запуск без аргументов: обновить архив и выдать комбинации на следующий тираж.
Подробности: python gosloto536.py --help
"""
import argparse
import csv
import datetime
import json
import math
import os
import random
import re
import sys
import threading
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(HERE, "draws_5x36.csv")
META_FILE = os.path.join(HERE, "draws_5x36.meta.json")

GAME = "5x36plus"
API = "https://www.stoloto.ru/p/api/mobile/api/v35/service/draws/archive"
# Public client key that stoloto.ru's own pages send with every archive request.
PARTNER = "bXMjXFRXZ3coWXh6R3s1NTdUX3dnWlBMLUxmdg"

N, K, NB = 36, 5, 4  # 5 numbers out of 36 and one bonus number out of 4
CATS = ("51", "5", "4", "3", "2")  # 5+1 (superprize 1), 5 (superprize 2), then 4, 3, 2 numbers
FIELDS = (["number", "date", "n1", "n2", "n3", "n4", "n5", "bonus", "columns", "players", "ticket_price", "sp1", "sp2"]
          + [f"w{c}" for c in CATS] + [f"d{c}" for c in CATS])

# ----------------------------------------------------------------------------- archive

UA = "Mozilla/5.0 (gosloto536 archive reader)"
_partner = [PARTNER]
_lock = threading.Lock()


def _discover_partner():
    """If stoloto.ru rotates its public client key, read the new one from the site's own scripts."""
    try:
        req = urllib.request.Request("https://www.stoloto.ru/5x36plus/archive", headers={"User-Agent": UA})
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
        for u in re.findall(r'src="(https://static\.stoloto\.ru/[^"]+\.js)"', html):
            js = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30).read().decode("utf-8", "ignore")
            m = re.search(r'GOSLOTO_PARTNER_T\(\)\{return\(0,[\w$.]+\)\("([^"]+)"', js)
            if m:
                return m.group(1)
    except Exception:
        return None
    return None


def _get(params, tries=6):
    url = API + "?" + urllib.parse.urlencode(dict({"game": GAME, "count": 50}, **params))
    rediscovered = False
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json",
                                                   "Gosloto-Partner": _partner[0]})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read().decode("utf-8"))
            if data.get("requestStatus") == "success":
                return data
            raise RuntimeError(data.get("errors"))
        except Exception as e:  # network hiccup or a new client key: retry
            if not rediscovered and getattr(e, "code", None) in (400, 401, 403):
                rediscovered = True
                key = _discover_partner()
                if key and key != _partner[0]:
                    _partner[0] = key
                    continue
            if attempt == tries - 1:
                raise RuntimeError(f"{params}: {e}")
            time.sleep(2 ** attempt)


def _parse(d):
    """One API draw -> flat record, or None if the draw is not finished yet."""
    if d.get("status") != "COMPLETED":
        return None
    balls = (d.get("combination") or {}).get("structured") or []
    if len(balls) != K + 1:
        return None
    jp = d.get("jackpots") or []
    rec = {"number": int(d["number"]), "date": d.get("date", "")[:16].replace("T", " "),
           "columns": int(d.get("betsCount") or 0), "players": int(d.get("ticketCount") or 0),
           "ticket_price": int(d.get("ticketPrice") or 0),
           "sp1": int(jp[0]) if len(jp) > 0 else int(d.get("superPrize") or 0),
           "sp2": int(jp[1]) if len(jp) > 1 else ""}
    for i, b in enumerate(balls[:K], 1):
        rec[f"n{i}"] = int(b)
    rec["bonus"] = int(balls[K])
    for c in CATS:
        rec[f"w{c}"] = ""
        rec[f"d{c}"] = ""
    info = {}
    wc = d.get("winningCategories")
    if isinstance(wc, str) and wc.strip():
        try:
            info = json.loads(wc)
        except ValueError:
            info = {}
    if info.get("columns"):
        rec["columns"] = int(info["columns"])
    if info.get("players"):
        rec["players"] = int(info["players"])
    names = {"СУПЕР №1": "51", "СУПЕР №2": "5"}
    for cat in info.get("categories", []):
        desc = cat.get("description", "")
        c = names.get(desc)
        if c is None:
            m = re.match(r"(\d)", desc)
            c = m.group(1) if m and m.group(1) in ("2", "3", "4") else None
        if c:
            rec[f"w{c}"] = int(cat.get("win_columns_number") or 0)
            rec[f"d{c}"] = round((cat.get("dividend_per_column") or 0) / 100, 2)
    return rec


def load_draws():
    if not os.path.exists(DATA_FILE):
        return []
    out = []
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rec = {"number": int(r["number"]), "date": r["date"],
                   "balls": [int(r[f"n{i}"]) for i in range(1, 6)], "bonus": int(r["bonus"])}
            for key in ("columns", "players", "ticket_price", "sp1"):
                rec[key] = int(float(r[key] or 0))
            rec["sp2"] = int(float(r["sp2"])) if r["sp2"] != "" else None
            for c in CATS:
                rec[f"w{c}"] = int(r[f"w{c}"]) if r[f"w{c}"] != "" else None
                rec[f"d{c}"] = float(r[f"d{c}"]) if r[f"d{c}"] != "" else None
            out.append(rec)
    out.sort(key=lambda x: x["number"])
    return out


def _save(known, complete, nxt=None):
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for n in sorted(known):
            w.writerow({k: known[n].get(k, "") for k in FIELDS})
    os.replace(tmp, DATA_FILE)
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump({"complete": complete, "next": nxt} if nxt else {"complete": complete}, f, ensure_ascii=False)


def _no_winners(r):
    return all(r.get(f"w{c}") in ("", None) for c in CATS)


def _range(lo, hi):
    """All finished draws with numbers lo..hi (the archive pages at most 25 000 draws deep, so walk in ranges)."""
    out, page = [], 1
    while True:
        data = _get({"page": page, "number_from": lo, "number_to": hi})
        draws = data.get("draws") or []
        out += [r for r in (_parse(d) for d in draws) if r]
        if not data.get("hasMore") or not draws:
            return out
        page += 1


def update(verbose=True, workers=6):
    """Download finished draws. The first run walks the whole archive (≈3 500 requests, 10–20 min);
    later runs stop as soon as they reach draws that are already stored."""
    known = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                known[int(r["number"])] = r
    complete = False
    if os.path.exists(META_FILE):
        try:
            complete = bool(json.load(open(META_FILE, encoding="utf-8")).get("complete"))
        except ValueError:
            complete = False
    added = 0
    if not complete:
        latest = max(int(d["number"]) for d in _get({"page": 1})["draws"])
        step = 2500
        ranges = [(lo, min(lo + step - 1, latest)) for lo in range(1, latest + 1, step)]
        done = [0]

        def job(r):
            recs = _range(*r)
            with _lock:
                done[0] += 1
                fresh = 0
                for rec in recs:
                    if rec["number"] not in known:
                        known[rec["number"]] = rec
                        fresh += 1
                if verbose:
                    print(f"  тиражи {r[0]}–{r[1]}: {len(recs)} (частей готово {done[0]} из {len(ranges)})", flush=True)
                if done[0] % 10 == 0:
                    _save(known, False)
                return fresh

        with ThreadPoolExecutor(workers) as ex:
            added = sum(ex.map(job, ranges))
        complete = True
    newest = max(known) if known else 0
    nxt = None
    page = 1
    while True:  # fresh draws on top of the archive
        data = _get({"page": page})
        draws = data.get("draws") or []
        fresh = 0
        for d in draws:
            rec = _parse(d)
            if not rec:
                jp = d.get("jackpots") or []
                if page == 1 and len(jp) >= 2 and (nxt is None or int(d["number"]) < nxt["number"]):
                    # the upcoming draw: its superprizes are already known
                    nxt = {"number": int(d["number"]), "date": d.get("date", "")[:16].replace("T", " "),
                           "sp1": int(jp[0]), "sp2": int(jp[1]), "ticket_price": int(d.get("ticketPrice") or 0)}
                continue
            old = known.get(rec["number"])
            late = (old is not None and rec["number"] > newest - 200
                    and _no_winners(old) and not _no_winners(rec))
            if old is None or late:
                known[rec["number"]] = rec
                fresh += 1
        added += fresh
        if not data.get("hasMore") or not draws or (fresh == 0 and page > 1):
            break
        page += 1
        time.sleep(0.25)
    _save(known, complete, nxt)
    if verbose:
        print(f"Архив: {len(known)} тиражей (новых: {added}). Файл: {DATA_FILE}")
    return added


# ----------------------------------------------------------------------------- math helpers

TOTAL = math.comb(N, K)  # 376 992 sets of five numbers
# P(exactly k of the 5 drawn numbers are on one ticket)
H = {k: math.comb(K, k) * math.comb(N - K, K - k) / TOTAL for k in range(K + 1)}
P51 = H[5] / NB             # 5 + bonus: superprize 1
P5 = H[5] * (NB - 1) / NB   # 5 without the bonus: superprize 2


def chi2_sf(x, k):
    """Upper tail of the chi-square distribution (regularized incomplete gamma)."""
    a, x = k / 2.0, x / 2.0
    if x <= 0:
        return 1.0
    lg = math.lgamma(a)
    if x < a + 1:
        s = t = 1.0 / a
        n = a
        for _ in range(5000):
            n += 1
            t *= x / n
            s += t
            if abs(t) < 1e-15 * s:
                break
        return max(0.0, 1.0 - s * math.exp(-x + a * math.log(x) - lg))
    b, c, d = x + 1 - a, 1e300, 1.0 / (x + 1 - a)
    h = d
    for i in range(1, 5000):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        d = 1.0 / d if d else 1e300
        c = b + an / c
        h *= d * c
        if abs(d * c - 1) < 1e-15:
            break
    return math.exp(-x + a * math.log(x) - lg) * h


def solve(A, b):
    """Gaussian elimination with partial pivoting."""
    n = len(b)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        if abs(piv) < 1e-12:
            continue
        for r in range(c + 1, n):
            f = M[r][c] / piv
            if f:
                row, top = M[r], M[c]
                for j in range(c, n + 1):
                    row[j] -= f * top[j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = s / M[i][i] if abs(M[i][i]) > 1e-12 else 0.0
    return x


# ----------------------------------------------------------------------------- 1. are the draws random?

def _chi_uniform(counts, expected, fpc=1.0):
    return sum((c - expected) ** 2 / expected for c in counts) / fpc


def randomness_report(draws):
    """Every check that could reveal a usable bias of the random number generator."""
    T = len(draws)
    fpc = (N - K) / (N - 1)  # five numbers are drawn without replacement
    out = {"draws": T}
    cnt = [0] * (N + 1)
    for d in draws:
        for x in d["balls"]:
            cnt[x] += 1
    E = T * K / N
    out["freq_p"] = chi2_sf(_chi_uniform(cnt[1:], E, fpc), N - 1)
    out["min_count"], out["max_count"], out["expected"] = min(cnt[1:]), max(cnt[1:]), E
    out["pos_p"] = []
    for pos in range(K):
        c = [0] * (N + 1)
        for d in draws:
            c[d["balls"][pos]] += 1
        out["pos_p"].append(chi2_sf(_chi_uniform(c[1:], T / N), N - 1))
    pc = {}
    for d in draws:
        for p in combinations(sorted(d["balls"]), 2):
            pc[p] = pc.get(p, 0) + 1
    ep = T * (K * (K - 1)) / (N * (N - 1))
    out["pairs_p"] = chi2_sf(sum((pc.get(p, 0) - ep) ** 2 / ep for p in combinations(range(1, N + 1), 2)),
                             N * (N - 1) // 2 - 1)
    ov = [len(set(draws[i]["balls"]) & set(draws[i - 1]["balls"])) for i in range(1, T)]
    m = sum(ov) / len(ov)
    sd = math.sqrt(sum((o - m) ** 2 for o in ov) / len(ov))
    out["overlap_mean"], out["overlap_expected"] = m, K * K / N
    out["overlap_z"] = (m - K * K / N) / (sd / math.sqrt(len(ov)))
    bc = [0] * (NB + 1)
    for d in draws:
        bc[d["bonus"]] += 1
    out["bonus_counts"] = bc[1:]
    out["bonus_p"] = chi2_sf(_chi_uniform(bc[1:], T / NB), NB - 1)
    rep = sum(1 for i in range(1, T) if draws[i]["bonus"] == draws[i - 1]["bonus"]) / (T - 1)
    out["bonus_repeat"] = rep
    out["bonus_repeat_z"] = (rep - 1 / NB) / math.sqrt((1 / NB) * (1 - 1 / NB) / (T - 1))
    # does the generator drift with the time of day or over the years?
    for key, part in (("hour_p", lambda d: d["date"][11:13]), ("year_p", lambda d: d["date"][:4])):
        groups = {}
        for d in draws:
            g = groups.setdefault(part(d), [0] * (N + 1))
            g[0] += 1
            for x in d["balls"]:
                g[x] += 1
        chi = sum(_chi_uniform(g[1:], g[0] * K / N, fpc) for g in groups.values() if g[0] >= 50)
        df = (N - 1) * sum(1 for g in groups.values() if g[0] >= 50)
        out[key] = chi2_sf(chi, df)
    return out


def _prequential(draws, values, pick, priors, half_lives, start=500):
    """Score frequency forecasts made only from earlier draws: sum of log(values * p) over drawn values.
    For truly random draws every score drifts below zero."""
    table, best = [], None
    for hl in half_lives:
        dec = 0.5 ** (1.0 / hl) if hl else 1.0
        for a in priors:
            c = [0.0] * (values + 1)
            n = 0.0
            g = 1.0  # weight of the current draw; earlier draws keep their smaller weights
            score = 0.0
            for t, d in enumerate(draws):
                xs = pick(d)
                if t >= start:
                    base = n / g
                    for x in xs:
                        score += math.log(values * (c[x] / g + a / values) / (base + a))
                g /= dec
                if g > 1e100:
                    c = [v / g for v in c]
                    n /= g
                    g = 1.0
                for x in xs:
                    c[x] += g
                n += g * len(xs)
            p = [0.0] + [(c[i] / g + a / values) / (n / g + a) for i in range(1, values + 1)]
            table.append((hl, a, score))
            if best is None or score > best[2]:
                best = (hl, a, score, p)
    return table, best


def bias_model(draws, gate=10.0):
    """Prequential check of frequency forecasts for the five numbers and for the bonus number.
    Returns probabilities to use (uniform unless a forecast beats chance by a clear margin)."""
    tm, bm = _prequential(draws, N, lambda d: d["balls"], (360.0, 3600.0), (2000, 10000, 40000, None))
    tb, bb = _prequential(draws, NB, lambda d: (d["bonus"],), (40.0, 400.0), (2000, 10000, 40000, None))
    p_main = bm[3] if bm[2] > gate else [0.0] + [1.0 / N] * N
    p_bonus = bb[3] if bb[2] > gate else [0.0] + [1.0 / NB] * NB
    return {"p_main": p_main, "p_bonus": p_bonus, "main": bm[:3], "bonus": bb[:3], "table_main": tm, "table_bonus": tb,
            "passed": bm[2] > gate or bb[2] > gate}


# ----------------------------------------------------------------------------- 2. what does the crowd play?

# a drawn number shifts log(winners of k) by about (k/5 - (5-k)/31) times how much more it is played
LEVER = {k: k / K - (K - k) / (N - K) for k in (2, 3)}


def crowd_model(draws, half_life=20000.0, ridge=30.0):
    """Fixed prizes make winner counts a direct poll of the crowd: when popular numbers are drawn, more
    people match 2 or 3 of them. Weighted ridge regression of log(winners / expected) on the drawn numbers."""
    dec = 0.5 ** (1.0 / half_life)
    beta = {}
    T = len(draws)
    dup = duplicated(draws)
    for k in (2, 3):
        A = [[0.0] * (N + 1) for _ in range(N + 1)]
        b = [0.0] * (N + 1)
        for t, d in enumerate(draws):
            w_k = d.get(f"w{k}")
            cols = d["columns"]
            if w_k is None or cols < 20 or d["number"] in dup:
                continue
            e = cols * H[k]
            y = math.log((w_k + 0.5) / (e + 0.5))
            wt = dec ** (T - 1 - t) / (1.0 / e + (0.002 if k == 2 else 0.01))  # Poisson noise plus a floor
            idx = [x - 1 for x in d["balls"]] + [N]
            for i in idx:
                b[i] += wt * y
                Ai = A[i]
                for j in idx:
                    Ai[j] += wt
        for i in range(N):
            A[i][i] += ridge
        sol = solve(A, b)
        mu = sol[N]
        bb = sol[:N]
        m = sum(bb) / N
        beta[k] = [v - m for v in bb]
    delta = [(beta[2][i] / LEVER[2] + beta[3][i] / LEVER[3]) / 2 for i in range(N)]
    return {"beta": beta, "delta": delta}


class Crowd:
    def __init__(self, model, n_norm=20000, seed=5):
        self.q = [1.0] + [math.exp(v) for v in model["delta"]]
        rng = random.Random(seed)
        self.norm = sum(self.raw(rng.sample(range(1, N + 1), K)) for _ in range(n_norm)) / n_norm

    def raw(self, C):
        v = 1.0
        for x in C:
            v *= self.q[x]
        return v

    def pop_rel(self, C):
        """How many times more (or less) often than an average ticket the crowd plays these five numbers."""
        return self.raw(C) / self.norm


# ----------------------------------------------------------------------------- 3. what the main prizes are worth

def _share(lam):
    """E[1 / (1 + other winners)] when other winners ~ Poisson(lam)."""
    return (1.0 - math.exp(-lam)) / lam if lam > 1e-12 else 1.0


def duplicated(draws):
    """Numbers of draws whose winner data is a copy of a neighbour's (an archive artifact, mostly in 2017–2021)."""
    key = lambda d: (d["columns"], d["w51"], d["w5"], d["w4"], d["w3"], d["w2"])
    out = set()
    for a, b in zip(draws, draws[1:]):
        if key(a) == key(b):
            out.add(a["number"])
            out.add(b["number"])
    return out


MULT = {4: 100, 3: 10, 2: 1}  # usual fixed prizes in bets


def _segments(draws):
    """Split the archive into periods with the same prize rules: the bet price, which small categories exist,
    and whether 3 numbers pays its usual 10 bets (promotions change it)."""
    segs = []
    usual3 = True
    for i, d in enumerate(draws):
        if d["w3"] and d["d3"]:
            usual3 = abs(d["d3"] - MULT[3] * d["ticket_price"]) < 0.01
        sig = (d["ticket_price"], d["w4"] is not None, d["w3"] is not None, d["w2"] is not None, usual3)
        if not segs or segs[-1][0] != sig:
            segs.append([sig, i, i])
        segs[-1][2] = i
    return segs


def _fit_tier(ds, k):
    """One small prize category within a period: fixed (one prize value) or shared (fund = a + b * bets)."""
    vals = [d[f"d{k}"] for d in ds if d[f"w{k}"] and d[f"d{k}"]]
    if not vals:
        return {"shared": False, "prize": ds[-1]["ticket_price"] * MULT[k] if ds[-1][f"w{k}"] is not None else 0.0}
    distinct = len(set(vals)) / len(vals)
    vals.sort()
    if distinct < 0.2 or len(vals) < 8:
        return {"shared": False, "prize": vals[len(vals) // 2]}
    xs = [d["columns"] for d in ds if d["columns"] > 0]
    ys = [(d[f"w{k}"] or 0) * (d[f"d{k}"] or 0) for d in ds if d["columns"] > 0]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx else 0.0
    a = my - b * mx
    if a < 0 or b < 0:
        a, b = 0.0, sum(ys) / sum(xs)
    return {"shared": True, "a": a, "b": b}


def _tier_value(t, cols):
    """Expected payout per bet of one category in a draw with `cols` bets."""
    if not t["shared"]:
        return None
    return (t["a"] + t["b"] * cols) / cols if cols > 0 else t["b"]


def prize_periods(draws):
    """For every draw: the expected payout per bet of the 4, 3 and 2 number prizes, and the period's rules."""
    small = [0.0] * len(draws)
    periods = []
    for sig, i0, i1 in _segments(draws):
        ds = draws[i0:i1 + 1]
        tiers = {k: _fit_tier(ds, k) for k in (4, 3, 2)}
        for j in range(i0, i1 + 1):
            cols = draws[j]["columns"] + 1  # with our own bet
            v = 0.0
            for k, t in tiers.items():
                tv = _tier_value(t, cols)
                v += H[k] * t["prize"] if tv is None else tv
            small[j] = v
        kind = ("shared" if any(t["shared"] for t in tiers.values())
                else "usual" if sig[3] and sig[4] else "promo")
        periods.append({"from": draws[i0]["number"], "to": draws[i1]["number"], "start": draws[i0]["date"],
                         "end": draws[i1]["date"], "price": sig[0], "kind": kind, "tiers": tiers, "draws": i1 - i0 + 1})
    return small, periods


def small_value(period, cols):
    v = 0.0
    for k, t in period["tiers"].items():
        tv = _tier_value(t, cols)
        v += H[k] * t["prize"] if tv is None else tv
    return v


def returns(draws, small=None):
    """Average return per ruble of a bet in every past draw: small prizes plus both superprizes."""
    small = small or prize_periods(draws)[0]
    return [(s + P51 * d["sp1"] + P5 * (d["sp2"] or 0)) / (d["ticket_price"] or 1) for d, s in zip(draws, small)]


def main_values(draws):
    """What both superprizes add to the return of one ruble in every past draw."""
    return [(P51 * d["sp1"] + P5 * (d["sp2"] or 0)) / (d["ticket_price"] or 1) for d in draws]


def prize_rules(draws):
    small, periods = prize_periods(draws)
    cur = periods[-1]
    ds = draws[-cur["draws"]:][-2000:]
    cols = sorted(d["columns"] for d in draws[-300:])
    slots = {}
    for d in ds:
        slots.setdefault(d["date"][11:16], []).append(d["columns"])
    return {"price": cur["price"], "start_number": cur["from"], "start": cur["start"], "kind": cur["kind"],
            "period": cur, "ev_small": small_value(cur, cols[len(cols) // 2] if cols else 300),
            "columns": cols[len(cols) // 2] if cols else 0,
            "slots": {s: _median(v[-10:]) for s, v in sorted(slots.items())},
            "prev_usual": next((p for p in reversed(periods[:-1]) if p["kind"] == "usual"), None)}


def ticket_return(rules, sp1, sp2, columns=None, pop_rel=1.0, price=None):
    """Expected payout per ruble of one bet in a draw with `columns` bets: small prizes for the current rules
    plus both superprizes (shared if several bets win)."""
    cols = rules["columns"] if columns is None else columns
    price = price or rules["price"]
    small = small_value(rules["period"], cols)
    main = P51 * sp1 * _share(cols * P51 * pop_rel) + P5 * sp2 * _share(cols * P5 * pop_rel)
    return (small + main) / price, main / price


def _day(d):
    return datetime.date(int(d["date"][:4]), int(d["date"][5:7]), int(d["date"][8:10]))


def _median(v):
    v = sorted(v)
    return v[len(v) // 2] if v else 0


def jackpot_history(draws, mains=None):
    """How the superprizes behave: what they add to a ruble, how fast they grow and how often they are won."""
    mains = mains or main_values(draws)
    t = _day(draws[-1])
    idx = [i for i, d in enumerate(draws) if (t - _day(d)).days <= 365]
    year = [draws[i] for i in idx]
    ms = sorted(mains[i] for i in idx)
    q = lambda f: ms[min(len(ms) - 1, int(f * len(ms)))]
    out = {"year_draws": len(year), "m_median": q(0.5), "m_q90": q(0.9), "m_max_year": ms[-1], "m_max_ever": max(mains)}
    for k in ("sp1", "sp2"):
        vals = [d[k] or 0 for d in year]
        out[k + "_min"], out[k + "_max"], out[k + "_median"] = min(vals), max(vals), _median(vals)
        out[k + "_max_ever"] = max(d[k] or 0 for d in draws)
    # growth per draw while the prize is not won (the median ignores rare top-ups by the organiser)
    for k, w in (("sp1", "w51"), ("sp2", "w5")):
        steps = [b[k] - a[k] for a, b in zip(year, year[1:]) if a[k] and b[k] and not a[w] and b[k] >= a[k]]
        out[k + "_step"] = _median(steps)
        out[k + "_step_mean"] = sum(steps) / len(steps) if steps else 0
    out["wins5_year"] = sum(1 for d in year if d["w5"])
    out["wins51_year"] = sum(1 for d in year if d["w51"])
    # main prizes won since 2023 against theory (earlier winner data has copied records)
    recent = [d for d in draws if d["date"] >= "2023"]
    dup = duplicated(recent)
    clean = [d for d in recent if d["number"] not in dup]
    out["check_from"] = clean[0]["date"][:10] if clean else ""
    out["check_bets"] = sum(d["columns"] for d in clean)
    out["check_exp"] = out["check_bets"] * H[5]
    out["check_obs"] = sum((d["w51"] or 0) + (d["w5"] or 0) for d in clean)
    return out


def timing_check(draws, rets=None, years=3, per_year=17520):
    """Walk-forward check of the timing rule: play only when the superprizes' share of the return reaches the
    90th percentile of the previous year of draws, compared with playing every draw."""
    import bisect
    rets = rets or main_values(draws)
    t_end = _day(draws[-1])
    test = [i for i, d in enumerate(draws) if (t_end - _day(d)).days <= 365 * years]
    j0 = test[0]
    lo = max(0, j0 - per_year)
    hist = sorted(rets[lo:j0])
    every, chosen = [], []
    for i in test:
        thr = hist[int(0.9 * (len(hist) - 1))] if hist else 0.0
        every.append(rets[i])
        if rets[i] >= thr:
            chosen.append(rets[i])
        bisect.insort(hist, rets[i])
        if i + 1 - lo > per_year:
            k = bisect.bisect_left(hist, rets[lo])
            if k < len(hist):
                hist.pop(k)
            lo += 1
    return {"draws": len(every), "every": sum(every) / len(every), "chosen": sum(chosen) / max(1, len(chosen)),
            "share": len(chosen) / len(every), "above1": sum(1 for r in chosen if r >= 1)}


# ----------------------------------------------------------------------------- 4. choosing tickets

def acceptable(C, recent):
    """Skip shapes that people fill in by hand: if such a ticket wins, the prize is shared more often."""
    s = sorted(C)
    run = best = 1
    for a, b in zip(s, s[1:]):
        run = run + 1 if b - a == 1 else 1
        best = max(best, run)
    if best >= 3:
        return False
    tens = [0] * 4
    for x in s:
        tens[x // 10] += 1
    if max(tens) >= 4:
        return False
    for w in (6, 7, 9):
        cols = [0] * w
        for x in s:
            cols[(x - 1) % w] += 1
        if max(cols) >= 4:
            return False
    ss = set(s)
    for i, a in enumerate(s):
        for b in s[i + 1:]:
            if a + 2 * (b - a) in ss and a + 3 * (b - a) in ss:
                return False
    for r in recent:
        if len(ss & r) >= 4:
            return False
    return True


def pick_tickets(score, n, recent, rng, restarts=4, max_shared=2):
    """Local search over five-number tickets maximizing `score`; tickets share at most `max_shared` numbers."""
    chosen = []
    for _ in range(n):
        best_c, best_s = None, -1e18
        for _r in range(restarts):
            for _try in range(500):
                C = sorted(rng.sample(range(1, N + 1), K))
                if acceptable(C, recent) and all(len(set(C) & set(o)) <= max_shared for o in chosen):
                    break
            else:
                continue
            cur = score(C)
            improved = True
            while improved:
                improved = False
                cand_best, cand_c = cur, None
                for i in range(K):
                    rest = C[:i] + C[i + 1:]
                    for x in range(1, N + 1):
                        if x in C:
                            continue
                        C2 = sorted(rest + [x])
                        if not acceptable(C2, recent) or any(len(set(C2) & set(o)) > max_shared for o in chosen):
                            continue
                        s = score(C2)
                        if s > cand_best + 1e-12:
                            cand_best, cand_c = s, C2
                if cand_c:
                    C, cur, improved = cand_c, cand_best, True
            if cur > best_s:
                best_c, best_s = C, cur
        if best_c:
            chosen.append(best_c)
    return chosen


def ticket_objective(crowd, bias):
    """Main prizes: a higher chance to draw the set (only if the generator showed a real bias) and,
    for equal chances, the set the fewest other people play, so a won superprize is less likely shared."""
    p = bias["p_main"]

    def f(C):
        return sum(math.log(N * p[x]) for x in C) - 0.01 * math.log(crowd.pop_rel(C))
    return f


def bonus_numbers(bias, n):
    """Bonus numbers for n tickets: the likeliest one if the generator favours it, otherwise all four in turn."""
    pb = bias["p_bonus"]
    if bias["bonus"][2] > 10.0:
        top = max(range(1, NB + 1), key=lambda i: pb[i])
        return [top] * n
    return [i % NB + 1 for i in range(n)]


# ----------------------------------------------------------------------------- commands

def num(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def rub(x, d=0):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def fmt_p(p):
    return "< 0,0001" if p < 1e-4 else num(p, 3)


def cmd_analyze(draws):
    r = randomness_report(draws)
    b = bias_model(draws)
    print(f"\n1. Случайность тиражей: {r['draws']} тиражей, №{draws[0]['number']}–№{draws[-1]['number']}")
    print(f"   частоты 36 чисел: p = {fmt_p(r['freq_p'])} (от {r['min_count']} до {r['max_count']} при ожидании {r['expected']:.0f})")
    print(f"   частоты по порядку выпадения: p = {'; '.join(fmt_p(p) for p in r['pos_p'])}")
    print(f"   частоты 630 пар: p = {fmt_p(r['pairs_p'])}")
    print(f"   совпадение с прошлым тиражом: {num(r['overlap_mean'], 3)} при теории {num(r['overlap_expected'], 3)} (z = {num(r['overlap_z'])})")
    print(f"   доп. число 1–4: {', '.join(map(str, r['bonus_counts']))}, p = {fmt_p(r['bonus_p'])}; "
          f"повтор доп. числа подряд {num(r['bonus_repeat'] * 100, 2)}% при теории 25% (z = {num(r['bonus_repeat_z'])})")
    print(f"   зависимость от часа тиража: p = {fmt_p(r['hour_p'])}; от года: p = {fmt_p(r['year_p'])}")
    print(f"   лучший прогноз частот, проверенный тираж за тиражом: числа {num(b['main'][2], 1)} нат, "
          f"доп. число {num(b['bonus'][2], 1)} нат против равных шансов")
    if b["passed"]:
        print("   → найдено устойчивое смещение, оно учтено при выборе чисел")
    else:
        print("   → генератор честный: ни один прогноз по частотам не угадывал лучше случая")
    return r, b


def cmd_predict(draws, n_tickets=4, bets=1, seed=None, nxt=None):
    last = draws[-1]
    print(f"Архив: {len(draws)} тиражей, последний №{last['number']} ({last['date']}): "
          f"{' '.join(map(str, sorted(last['balls'])))} + {last['bonus']}")
    _r, bias = cmd_analyze(draws)
    crowd = Crowd(crowd_model(draws))
    order = sorted(range(1, N + 1), key=lambda i: crowd.q[i])
    print("\n2. Выбор других игроков (по числу победителей за 2 и 3 числа):")
    print("   реже всего ставят: " + ", ".join(map(str, order[:10])))
    print("   чаще всего ставят: " + ", ".join(map(str, order[::-1][:10])))

    rules = prize_rules(draws)
    mains = main_values(draws)
    hist = jackpot_history(draws, mains)
    price = rules["price"]
    if nxt and nxt.get("number", 0) > last["number"]:
        sp1, sp2, label = nxt["sp1"], nxt["sp2"], f"в тираже №{nxt['number']} ({nxt['date']})"
        price = nxt.get("ticket_price") or price
    else:
        sp1, sp2, label = last["sp1"], last["sp2"] or 0, f"после тиража №{last['number']}"
    r_now, r_main = ticket_return(rules, sp1, sp2, rules["columns"] + bets, price=price)
    print(f"\n3. Главные призы {label}: 5+1 — {rub(sp1)} ₽, 5 — {rub(sp2)} ₽; ставка {price} ₽")
    print(f"   шанс на одну ставку: 5+1 — 1 к {rub(1 / P51)}, 5 без доп. числа — 1 к {rub(1 / P5)}")
    per = rules["period"]
    desc = []
    for k in (4, 3, 2):
        tt = per["tiers"][k]
        if tt["shared"]:
            desc.append(f"{k} — делится между победителями (фонд ≈ {rub(tt['a'])} ₽ + {num(tt['b'])} ₽ с каждой ставки)")
        elif tt["prize"]:
            desc.append(f"{k} — {rub(tt['prize'])} ₽")
        else:
            desc.append(f"{k} — не выплачивается")
    kind = {"usual": "обычные правила", "promo": "акция", "shared": "акция с делимым призом"}[per["kind"]]
    print(f"   призы сейчас ({kind}, с {per['start'][:16]}): " + "; ".join(desc))
    print(f"   ставка возвращает в среднем {num(r_now)} ₽ на 1 ₽, из них суперпризы — {num(r_main)} ₽")
    need2 = (price - rules["ev_small"] - P51 * sp1) / P5
    need1 = (price - rules["ev_small"] - P5 * sp2) / P51
    print(f"   окупаться ставка начнёт при суперпризе за 5 чисел от {rub(need2)} ₽ (при нынешнем 5+1)"
          f" или при суперпризе 5+1 от {rub(need1)} ₽ (при нынешнем за 5)")
    print(f"   суперпризы дают с рубля: сейчас {num(r_main)} ₽; за последний год обычно {num(hist['m_median'])},"
          f" у 10% лучших тиражей от {num(hist['m_q90'])}, максимум {num(hist['m_max_year'])}; за всю историю до {num(hist['m_max_ever'])}")
    if r_now >= 1:
        print("   → ставка сейчас в среднем окупается")
    elif r_main >= hist["m_q90"]:
        print("   → сейчас один из 10% лучших моментов года для игры на главные призы")
    else:
        grow = P51 * hist["sp1_step_mean"] + P5 * hist["sp2_step_mean"]  # rubles of expected value per draw
        steps = (hist["m_q90"] - r_main) * price / grow if grow > 0 else float("inf")
        print(f"   → лучше подождать: до 10% лучших моментов года суперпризам нужно вырасти"
              + (f", это ≈{steps:.0f} тиражей (≈{steps / 48:.0f} дн.), если их не выиграют раньше" if steps < 1e6 else ""))

    if per["kind"] == "shared":
        print("\n   Сейчас приз делится, поэтому выгоднее тиражи, где мало ставок: на 1 ₽ ставки по времени тиража")
        rows = []
        for slot, cols in rules["slots"].items():
            r_s, _m = ticket_return(rules, sp1, sp2, cols + bets, price=price)
            rows.append((r_s, slot, cols))
        rows.sort(reverse=True)
        for r_s, slot, cols in rows[:8]:
            print(f"   {slot}  ставок ≈{cols:6d}   {num(r_s)}" + ("  ← окупается" if r_s >= 1 else ""))
    rng = random.Random(seed)
    recent = [set(d["balls"]) for d in draws[-100:]]
    tickets = pick_tickets(ticket_objective(crowd, bias), n_tickets, recent, rng,
                           restarts=2 if n_tickets > 10 else 4, max_shared=3 if n_tickets > 30 else 2)
    bonus = bonus_numbers(bias, len(tickets))
    print("\n4. Комбинации на следующий тираж (5 чисел + доп. число):")
    for C, b in zip(tickets, bonus):
        print("   " + " ".join(f"{x:2d}" for x in C) + f"  + {b}"
              f"   эту пятёрку ставят в {num(1 / crowd.pop_rel(C), 1)} раза реже среднего")
    print("\n5. Шанс выиграть главный приз хотя бы одной ставкой (разные пятёрки):")
    print("   ставок   стоимость        5+1          5 без доп.   любой из двух")
    for n in (1, 10, 100, 1000, 10000):
        print(f"   {n:6d}  {rub(n * price):>10} ₽   1 к {rub(1 / (n * P51)):>9}   1 к {rub(1 / (n * P5)):>9}"
              f"   1 к {rub(1 / (n * H[5])):>9}")
    print(f"\n   За тираж без выигрыша суперприз 5+1 растёт в среднем на {rub(hist['sp1_step_mean'])} ₽,"
          f" за 5 чисел — на {rub(hist['sp2_step_mean'])} ₽. За год их выигрывали {hist['wins51_year']} и {hist['wins5_year']} раз.")
    return tickets


def cmd_history(draws):
    mains = main_values(draws)
    hist = jackpot_history(draws, mains)
    tc = timing_check(draws, mains)
    print(f"\nСуперпризы за последний год ({hist['year_draws']} тиражей):")
    print(f"   5+1: от {rub(hist['sp1_min'])} до {rub(hist['sp1_max'])} ₽, обычно {rub(hist['sp1_median'])} ₽;"
          f" максимум за всю историю {rub(hist['sp1_max_ever'])} ₽")
    print(f"   5: от {rub(hist['sp2_min'])} до {rub(hist['sp2_max'])} ₽, обычно {rub(hist['sp2_median'])} ₽;"
          f" максимум за всю историю {rub(hist['sp2_max_ever'])} ₽")
    print(f"   рост за тираж без выигрыша: 5+1 — в среднем {rub(hist['sp1_step_mean'])} ₽, 5 — {rub(hist['sp2_step_mean'])} ₽")
    print(f"   выигрывали за год: 5+1 — в {hist['wins51_year']} тиражах, 5 — в {hist['wins5_year']}")
    print(f"   с {hist['check_from']}: выигрышных ставок 5+1 и 5 — {hist['check_obs']} при ожидании {num(hist['check_exp'], 1)}"
          f" (ставок {rub(hist['check_bets'])})")
    print(f"   суперпризы дают с рубля ставки: обычно {num(hist['m_median'])}, 10% лучших от {num(hist['m_q90'])},"
          f" максимум за год {num(hist['m_max_year'])}, за всю историю {num(hist['m_max_ever'])} ₽")
    print(f"\nПроверка правила «играть только в 10% лучших моментов» на {tc['draws']} тиражах за 3 года")
    print("(порог каждый раз по предыдущему году; сколько дают суперпризы с рубля ставки):")
    print(f"   в каждом тираже: {num(tc['every'], 3)} ₽")
    print(f"   только по правилу ({num(tc['share'] * 100, 1)}% тиражей): {num(tc['chosen'], 3)} ₽ — в {num(tc['chosen'] / tc['every'], 2)} раза больше")
    return hist, tc


def main():
    try:  # old Windows consoles cannot print the rouble sign
        sys.stdout.reconfigure(errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="«5 из 36»: архив, проверка случайности, игра на главные призы.")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("update", help="скачать новые тиражи")
    pr = sub.add_parser("predict", help="комбинации на следующий тираж (по умолчанию)")
    pr.add_argument("-n", "--tickets", type=int, default=4, help="сколько комбинаций (по умолчанию 4)")
    pr.add_argument("--bets", type=int, default=1, help="сколько ставок вы покупаете в один тираж")
    pr.add_argument("--offline", action="store_true", help="не обновлять архив")
    sub.add_parser("analyze", help="только проверка случайности")
    sub.add_parser("history", help="как ведут себя суперпризы и когда выгоднее играть")
    a = ap.parse_args()
    cmd = a.cmd or "predict"
    if cmd == "update" or (cmd == "predict" and not getattr(a, "offline", False)):
        print("Обновляю архив тиражей…")
        try:
            update()
        except Exception as e:
            if cmd == "update":
                sys.exit(f"Не удалось обновить архив: {e}")
            print(f"Не удалось обновить архив ({e}); считаю по сохранённому.")
        if cmd == "update":
            return
    draws = load_draws()
    if len(draws) < 1000:
        sys.exit("Архив пуст: запустите `python gosloto536.py update` с доступом к интернету.")
    nxt = None
    try:
        nxt = json.load(open(META_FILE, encoding="utf-8")).get("next")
    except (OSError, ValueError):
        nxt = None
    if cmd == "predict":
        cmd_predict(draws, getattr(a, "tickets", 4), getattr(a, "bets", 1), nxt=nxt)
    elif cmd == "analyze":
        cmd_analyze(draws)
    elif cmd == "history":
        cmd_history(draws)


if __name__ == "__main__":
    main()
