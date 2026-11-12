#!/usr/bin/env python3
"""«Рапидо 2.0» (8 чисел из 20 + 1 из 4): архив тиражей, поиск закономерностей и игра на суперприз.

Запуск без аргументов: обновить архив и выдать комбинации на следующий тираж.
Подробности: python rapido2.py --help
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
DATA_FILE = os.path.join(HERE, "draws_rapido2.csv")
META_FILE = os.path.join(HERE, "draws_rapido2.meta.json")

GAME = "rapido2"
API = "https://www.stoloto.ru/p/api/mobile/api/v35/service/draws/archive"
# Public client key that stoloto.ru's own pages send with every archive request.
PARTNER = "bXMjXFRXZ3coWXh6R3s1NTdUX3dnWlBMLUxmdg"

N, K, NB = 20, 8, 4  # 8 numbers out of 20 and one bonus number out of 4
CATS = tuple(range(1, 17))  # prize categories of the API: 1 = 8+1 (superprize), 2 = 8, 3 = 7+1, 4 = 7, ...
FIELDS = (["number", "date"] + [f"n{i}" for i in range(1, 9)] + ["bonus", "columns", "ticket_price", "sp"]
          + [f"w{c}" for c in CATS] + [f"a{c}" for c in CATS])

# ----------------------------------------------------------------------------- archive

UA = "Mozilla/5.0 (rapido2 archive reader)"
_partner = [PARTNER]
_lock = threading.Lock()


def _discover_partner():
    """If stoloto.ru rotates its public client key, read the new one from the site's own scripts."""
    try:
        req = urllib.request.Request("https://www.stoloto.ru/rapido2/archive", headers={"User-Agent": UA})
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
    comb = (d.get("combination") or {}).get("structured") or {}
    balls = comb.get("played") if isinstance(comb, dict) else comb
    if not balls or len(balls) != K + 1:
        return None
    rec = {"number": int(d["number"]), "date": d.get("date", "")[:16].replace("T", " "),
           "columns": int(d.get("betsCount") or 0), "ticket_price": int(d.get("ticketPrice") or 0),
           "sp": int(d.get("superPrize") or 0)}
    for i, b in enumerate(balls[:K], 1):
        rec[f"n{i}"] = int(b)
    rec["bonus"] = int(balls[K])
    for c in CATS:
        rec[f"w{c}"] = ""
        rec[f"a{c}"] = ""
    info = {}
    wc = d.get("winningCategories")
    if isinstance(wc, str) and wc.strip():
        try:
            info = json.loads(wc)
        except ValueError:
            info = {}
    for cat in info.get("main") or []:
        c = cat.get("winCat")
        if c in CATS:
            rec[f"w{c}"] = int(cat.get("countWins") or 0)
            rec[f"a{c}"] = cat.get("amount") or 0
    return rec


def load_draws():
    if not os.path.exists(DATA_FILE):
        return []
    out = []
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rec = {"number": int(r["number"]), "date": r["date"],
                   "balls": [int(r[f"n{i}"]) for i in range(1, K + 1)], "bonus": int(r["bonus"])}
            for key in ("columns", "ticket_price", "sp"):
                rec[key] = int(float(r[key] or 0))
            for c in CATS:
                rec[f"w{c}"] = int(r[f"w{c}"]) if r[f"w{c}"] != "" else None
                rec[f"a{c}"] = float(r[f"a{c}"]) if r[f"a{c}"] != "" else None
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


def update(verbose=True, workers=8):
    """Download finished draws. The first run walks the whole archive (≈3 800 requests, 20–40 min);
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
                if page == 1 and d.get("superPrize") and (nxt is None or int(d["number"]) < nxt["number"]):
                    # the upcoming draw: its superprizes are already known
                    nxt = {"number": int(d["number"]), "date": d.get("date", "")[:16].replace("T", " "),
                           "sp": int(d["superPrize"]), "ticket_price": int(d.get("ticketPrice") or 0)}
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

TOTAL = math.comb(N, K)  # 125 970 sets of eight numbers
# P(exactly k of the 8 drawn numbers are in a given set of 8): matches on a ticket, repeats from the last draw
H = {k: math.comb(K, k) * math.comb(N - K, K - k) / TOTAL for k in range(K + 1)}
P_SUPER = 1.0 / (TOTAL * NB)  # 8 numbers and the bonus number
# category of the API -> (matched numbers, bonus matched)
CAT = {1: (8, True), 2: (8, False), 3: (7, True), 4: (7, False), 5: (6, True), 6: (6, False),
       7: (5, True), 8: (5, False), 9: (4, True)}
P_CAT = {c: H[k] * (1 if b else NB - 1) / NB for c, (k, b) in CAT.items()}


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


def _median(v):
    v = sorted(v)
    return v[len(v) // 2] if v else 0


def _day(d):
    return datetime.date(int(d["date"][:4]), int(d["date"][5:7]), int(d["date"][8:10]))


# ----------------------------------------------------------------------------- 1. patterns in the draws

def _chi(counts, expected):
    return sum((c - e) ** 2 / e for c, e in zip(counts, expected) if e > 0)


def repeats(draws, lag=1):
    """How many of the eight numbers of a draw were also in the draw `lag` steps earlier: counts for 0..8."""
    cnt = [0] * (K + 1)
    sets = [set(d["balls"]) for d in draws]
    for i in range(lag, len(sets)):
        cnt[len(sets[i] & sets[i - lag])] += 1
    return cnt


def repeat_table(cnt):
    """Observed share of each repeat count against theory, and the chance of one exact set of eight
    that shares j numbers with the previous draw (if draws are fair it is 1 in 125 970 for every j)."""
    T = sum(cnt)
    rows = []
    for j in range(K + 1):
        exp = T * H[j]
        lift = cnt[j] / exp if exp else 0.0
        sd = math.sqrt((1 - H[j]) / exp) if exp else 0.0  # relative standard error of the share
        rows.append({"j": j, "count": cnt[j], "share": cnt[j] / T, "theory": H[j], "lift": lift, "sd": sd,
                     "z": (lift - 1) / sd if sd else 0.0})
    # chi-square with the rare ends merged
    obs = [cnt[0] + cnt[1]] + cnt[2:6] + [sum(cnt[6:])]
    exp = [T * (H[0] + H[1])] + [T * H[j] for j in range(2, 6)] + [T * sum(H[j] for j in range(6, K + 1))]
    mean = sum(j * c for j, c in enumerate(cnt)) / T
    var = K * (K / N) * (1 - K / N) * (N - K) / (N - 1)
    return {"rows": rows, "mean": mean, "expected": K * K / N, "z": (mean - K * K / N) / math.sqrt(var / T),
            "p": chi2_sf(_chi(obs, exp), len(obs) - 1), "draws": T}


def patterns_report(draws):
    """Every check that could reveal a usable regularity of the random number generator."""
    T = len(draws)
    fpc = (N - K) / (N - 1)  # eight numbers are drawn without replacement
    out = {"draws": T}
    cnt = [0] * (N + 1)
    for d in draws:
        for x in d["balls"]:
            cnt[x] += 1
    E = T * K / N
    out["freq_p"] = chi2_sf(_chi(cnt[1:], [E] * N) / fpc, N - 1)
    out["counts"] = cnt[1:]
    out["min_count"], out["max_count"], out["expected"] = min(cnt[1:]), max(cnt[1:]), E
    out["pos_p"] = []
    for pos in range(K):
        c = [0] * (N + 1)
        for d in draws:
            c[d["balls"][pos]] += 1
        out["pos_p"].append(chi2_sf(_chi(c[1:], [T / N] * N), N - 1))
    pc = {}
    for d in draws:
        for p in combinations(sorted(d["balls"]), 2):
            pc[p] = pc.get(p, 0) + 1
    pi = K * (K - 1) / (N * (N - 1))
    ep = T * pi
    # Pair counts partly repeat the single-number frequencies. Remove that part and test what is left:
    # the residual lives in a space of N(N-3)/2 dimensions with one common variance.
    p1 = pi * (K - 2) / (N - 2)                 # two pairs sharing a number are both drawn
    p2 = p1 * (K - 3) / (N - 3)                 # two disjoint pairs are both drawn
    lam = pi * (1 - pi) - 2 * (p1 - pi * pi) + (p2 - pi * pi)
    g = [0.0] + [(K - 1) * (cnt[i] - E) / (N - 2) for i in range(1, N + 1)]
    resid = sum((pc.get((i, j), 0) - ep - g[i] - g[j]) ** 2 for i, j in combinations(range(1, N + 1), 2))
    out["pairs_p"] = chi2_sf(resid / (T * lam), N * (N - 3) // 2)
    best = max(pc.items(), key=lambda kv: kv[1])
    worst = min(pc.items(), key=lambda kv: kv[1])
    out["pair_max"], out["pair_min"], out["pair_expected"] = [list(best[0]), best[1]], [list(worst[0]), worst[1]], ep
    # repeats from draw to draw
    out["repeat"] = repeat_table(repeats(draws, 1))
    out["repeat_lag"] = {lag: repeat_table(repeats(draws, lag))["mean"] for lag in (2, 3, 5, 10)}
    # per number: how often it comes again right after it was drawn
    rep = [0] * (N + 1)
    was = [0] * (N + 1)
    prev = set(draws[0]["balls"])
    for d in draws[1:]:
        cur = set(d["balls"])
        for x in prev:
            was[x] += 1
            if x in cur:
                rep[x] += 1
        prev = cur
    rates = [rep[i] / was[i] for i in range(1, N + 1)]
    out["repeat_rate"] = sum(rep) / sum(was)
    out["repeat_rate_min"], out["repeat_rate_max"] = min(rates), max(rates)
    out["repeat_number_p"] = chi2_sf(sum((rep[i] - was[i] * K / N) ** 2 / (was[i] * K / N * (1 - K / N))
                                         for i in range(1, N + 1)), N)
    # streaks: a number drawn in the last two draws, or absent from the last five
    hot = [0, 0]
    cold = [0, 0]
    sets = [set(d["balls"]) for d in draws]
    for i in range(5, T):
        both = sets[i - 1] & sets[i - 2]
        hot[0] += len(both)
        hot[1] += len(both & sets[i])
        absent = set(range(1, N + 1)) - sets[i - 1] - sets[i - 2] - sets[i - 3] - sets[i - 4] - sets[i - 5]
        cold[0] += len(absent)
        cold[1] += len(absent & sets[i])
    out["hot_rate"] = hot[1] / hot[0] if hot[0] else 0.0
    out["hot_z"] = (hot[1] - hot[0] * K / N) / math.sqrt(hot[0] * K / N * (1 - K / N)) if hot[0] else 0.0
    out["cold_rate"] = cold[1] / cold[0] if cold[0] else 0.0
    out["cold_z"] = (cold[1] - cold[0] * K / N) / math.sqrt(cold[0] * K / N * (1 - K / N)) if cold[0] else 0.0
    # even numbers among the eight (10 of 20 are even)
    ev = [0] * (K + 1)
    for d in draws:
        ev[sum(1 for x in d["balls"] if x % 2 == 0)] += 1
    pe = [math.comb(10, k) * math.comb(10, K - k) / TOTAL for k in range(K + 1)]
    obs = [ev[0] + ev[1] + ev[2]] + ev[3:6] + [ev[6] + ev[7] + ev[8]]
    exp = [T * sum(pe[:3])] + [T * pe[k] for k in (3, 4, 5)] + [T * sum(pe[6:])]
    out["even_p"] = chi2_sf(_chi(obs, exp), len(obs) - 1)
    out["even_counts"], out["even_theory"] = ev, pe
    # low numbers 1..10, the sum and neighbours
    low = sum(sum(1 for x in d["balls"] if x <= 10) for d in draws) / T
    var_h = K * 0.5 * 0.5 * (N - K) / (N - 1)
    out["low_mean"], out["low_z"] = low, (low - K / 2) / math.sqrt(var_h / T)
    sm = [sum(d["balls"]) for d in draws]
    m = sum(sm) / T
    var_s = K * ((N * N - 1) / 12.0) * (N - K) / (N - 1)
    out["sum_mean"], out["sum_expected"], out["sum_z"] = m, K * (N + 1) / 2, (m - K * (N + 1) / 2) / math.sqrt(var_s / T)
    out["sum_sd"], out["sum_sd_theory"] = math.sqrt(sum((s - m) ** 2 for s in sm) / T), math.sqrt(var_s)
    adj = 0
    for d in draws:
        s = set(d["balls"])
        adj += sum(1 for x in s if x + 1 in s)
    out["adjacent_mean"], out["adjacent_expected"] = adj / T, (N - 1) * K * (K - 1) / (N * (N - 1))
    # bonus number
    bc = [0] * (NB + 1)
    for d in draws:
        bc[d["bonus"]] += 1
    out["bonus_counts"] = bc[1:]
    out["bonus_p"] = chi2_sf(_chi(bc[1:], [T / NB] * NB), NB - 1)
    rb = sum(1 for i in range(1, T) if draws[i]["bonus"] == draws[i - 1]["bonus"]) / (T - 1)
    out["bonus_repeat"] = rb
    out["bonus_repeat_z"] = (rb - 1 / NB) / math.sqrt((1 / NB) * (1 - 1 / NB) / (T - 1))
    inb = sum(1 for d in draws if d["bonus"] in d["balls"]) / T  # is the bonus tied to the eight numbers?
    out["bonus_in_main"], out["bonus_in_main_z"] = inb, (inb - K / N) / math.sqrt(K / N * (1 - K / N) / T)
    # drift with the time of day or over the years
    for key, part in (("hour_p", lambda d: d["date"][11:13]), ("year_p", lambda d: d["date"][:4])):
        groups = {}
        for d in draws:
            g = groups.setdefault(part(d), [0] * (N + 1))
            g[0] += 1
            for x in d["balls"]:
                g[x] += 1
        big = [g for g in groups.values() if g[0] >= 100]
        chi = sum(_chi(g[1:], [g[0] * K / N] * N) / fpc for g in big)
        out[key] = chi2_sf(chi, (N - 1) * len(big))
    # the same eight numbers drawn twice in the whole history
    seen = {}
    dup = 0
    for d in draws:
        key = tuple(sorted(d["balls"]))
        dup += seen.get(key, 0)
        seen[key] = seen.get(key, 0) + 1
    out["same_set_pairs"], out["same_set_expected"] = dup, T * (T - 1) / 2 / TOTAL
    return out


def _score(p, drawn):
    """Log-likelihood ratio of inclusion probabilities p[1..N] against equal chances for one draw."""
    s = 0.0
    q0, q1 = K / N, 1 - K / N
    for i in range(1, N + 1):
        s += math.log(p[i] / q0) if i in drawn else math.log((1 - p[i]) / q1)
    return s


def forecast_models(draws, gate=15.0, start=2000):
    """Walk-forward test of every forecast built from the past only. Each one gives the chance of every number
    to be among the eight; the score is its log-likelihood against equal chances, summed over all later draws.
    For fair draws every score drifts below zero; a clearly positive one would be a real, usable regularity."""
    T = len(draws)
    sets = [set(d["balls"]) for d in draws]
    q = K / N
    res = {}
    # a) frequencies with different memory
    best = None
    for hl in (2000, 20000, None):
        dec = 0.5 ** (1.0 / hl) if hl else 1.0
        for a in (2000.0,):
            c = [0.0] * (N + 1)
            n = 0.0
            score = 0.0
            for t in range(T):
                if t >= start:
                    score += _score([0.0] + [min(0.9, K * (c[i] + a / N) / (n + a)) for i in range(1, N + 1)], sets[t])
                if dec != 1.0:
                    c = [v * dec for v in c]
                    n *= dec
                for x in sets[t]:
                    c[x] += 1.0
                n += K
            p = [0.0] + [min(0.9, K * (c[i] + a / N) / (n + a)) for i in range(1, N + 1)]
            if best is None or score > best[0]:
                best = (score, p, hl)
    res["freq"] = {"score": best[0], "p": best[1], "half_life": best[2]}
    # b) repeats: a number of the last draw comes again with the rate seen so far
    for name, lag in (("repeat", 1), ("repeat2", 2)):
        rep = was = 0.0
        score = 0.0
        for t in range(lag, T):
            prev = sets[t - lag]
            r = (rep + 400.0 * q) / (was + 400.0)
            p_in, p_out = r, (K - K * r) / (N - K)
            if t >= start:
                score += _score([0.0] + [p_in if i in prev else p_out for i in range(1, N + 1)], sets[t])
            was += K
            rep += len(prev & sets[t])
        res[name] = {"score": score, "rate": (rep + 400.0 * q) / (was + 400.0)}
    # c) every number has its own repeat rate
    rep_i = [0.0] * (N + 1)
    was_i = [0.0] * (N + 1)
    score = 0.0
    for t in range(1, T):
        prev = sets[t - 1]
        p = [0.0] * (N + 1)
        tot_in = 0.0
        for i in prev:
            p[i] = (rep_i[i] + 400.0 * q) / (was_i[i] + 400.0)
            tot_in += p[i]
        for i in range(1, N + 1):
            if i not in prev:
                p[i] = (K - tot_in) / (N - K)
        if t >= start:
            score += _score(p, sets[t])
        for i in prev:
            was_i[i] += 1
            if i in sets[t]:
                rep_i[i] += 1
    res["repeat_number"] = {"score": score}
    # d) how long a number has been absent (gap since it was last drawn)
    G = 12
    hit = [0.0] * (G + 1)
    tot = [0.0] * (G + 1)
    gap = [0] * (N + 1)
    score = 0.0
    for t in range(T):
        raw = [0.0] + [(hit[min(gap[i], G)] + 400.0 * q) / (tot[min(gap[i], G)] + 400.0) for i in range(1, N + 1)]
        z = K / sum(raw[1:])
        p = [min(0.95, v * z) for v in raw]
        if t >= start:
            score += _score(p, sets[t])
        for i in range(1, N + 1):
            g = min(gap[i], G)
            tot[g] += 1
            if i in sets[t]:
                hit[g] += 1
                gap[i] = 0
            else:
                gap[i] += 1
    res["gap"] = {"score": score, "rates": [(hit[g] + 400.0 * q) / (tot[g] + 400.0) for g in range(G + 1)]}
    # e) bonus number frequencies
    c = [0.0] * (NB + 1)
    score = 0.0
    for t, d in enumerate(draws):
        if t >= start:
            score += math.log(NB * (c[d["bonus"]] + 100.0) / (t + 400.0))
        c[d["bonus"]] += 1
    res["bonus"] = {"score": score, "p": [0.0] + [(c[i] + 100.0) / (T + 400.0) for i in range(1, NB + 1)]}
    res["gate"] = gate
    res["passed"] = [k for k in ("freq", "repeat", "repeat2", "repeat_number", "gap", "bonus") if res[k]["score"] > gate]
    return res


def number_bias(draws, block=5000, start=20000):
    """Numbers that come up more often than the rest. Each number's excess is shrunk by how much the twenty
    excesses vary beyond chance (empirical Bayes). The walk-forward part names the leader from past draws
    only and counts how often it was then drawn."""
    T = len(draws)
    q = K / N
    cnt = [0] * (N + 1)
    for d in draws:
        for x in d["balls"]:
            cnt[x] += 1
    sd = math.sqrt(T * q * (1 - q))
    z = [0.0] + [(cnt[i] - T * q) / sd for i in range(1, N + 1)]
    ss = sum(v * v for v in z)
    B = max(0.0, 1.0 - (N - 1) / ss) if ss else 0.0
    lift = [1.0] + [1.0 + B * (cnt[i] / (T * q) - 1.0) for i in range(1, N + 1)]
    run = [0] * (N + 1)
    for d in draws[:start]:
        for x in d["balls"]:
            run[x] += 1
    hits = n = 0
    leaders = []
    for b0 in range(start, T, block):
        lead = max(range(1, N + 1), key=lambda i: run[i])
        leaders.append(lead)
        for d in draws[b0:b0 + block]:
            n += 1
            if lead in d["balls"]:
                hits += 1
            for x in d["balls"]:
                run[x] += 1
    top = max(range(1, N + 1), key=lambda i: cnt[i])
    years = {}
    for d in draws:
        y = years.setdefault(d["date"][:4], [0, 0])
        y[0] += 1
        y[1] += 1 if top in d["balls"] else 0
    return {"z": z, "lift": lift, "shrink": B, "top": top, "top_rate": cnt[top] / T, "top_z": z[top],
            "top_p": min(1.0, N * math.erfc(abs(z[top]) / math.sqrt(2))),  # corrected for picking the best of twenty
            "walk_rate": hits / n if n else q, "walk_z": (hits - n * q) / math.sqrt(n * q * (1 - q)) if n else 0.0,
            "walk_draws": n, "walk_leaders": leaders,
            "years": {y: v[1] / v[0] for y, v in sorted(years.items())},
            "anchors": [i for i in range(1, N + 1) if lift[i] > 1.003]}


def repeat_choice(draws, block=5000, start=20000, prior=20000.0):
    """How many numbers of the last draw to keep. For every count j the past shows how often exactly j numbers
    repeated; divided by theory it is the lift of one exact set with j repeats. The choice is the count with
    the highest lift so far (shrunk towards 1). The walk-forward part repeats this choice with past data only
    and reports what lift it then got on the following draws."""
    sets = [set(d["balls"]) for d in draws]
    ov = [len(sets[i] & sets[i - 1]) for i in range(1, len(sets))]

    def choose(cnt):
        T = sum(cnt)
        best, bl = 3, -1.0
        lifts = []
        for j in range(K + 1):
            e = T * H[j]  # rare counts are pulled towards 1: a few hundred draws prove little
            l = 1.0 + (cnt[j] / e - 1.0) * e / (e + prior) if e else 1.0
            lifts.append(l)
            if l > bl:
                best, bl = j, l
        return best, lifts

    cnt = [0] * (K + 1)
    for o in ov[:start]:
        cnt[o] += 1
    got = total = 0.0
    picks = []
    for b0 in range(start, len(ov), block):
        j, _l = choose(cnt)
        seg = ov[b0:b0 + block]
        picks.append(j)
        got += sum(1 for o in seg if o == j) / H[j]  # in units of "expected wins of an average set"
        total += len(seg)
        for o in seg:
            cnt[o] += 1
    j, lifts = choose(cnt)
    return {"repeats": j, "lifts": lifts, "walk_lift": got / total if total else 1.0, "walk_draws": int(total),
            "walk_picks": picks, "most_common": max(range(K + 1), key=lambda k: cnt[k])}


# ----------------------------------------------------------------------------- 2. what does the crowd play?

def duplicated(draws):
    """Numbers of draws whose winner data is a copy of a neighbour's (an archive artifact)."""
    key = lambda d: (d["columns"],) + tuple(d[f"w{c}"] for c in range(1, 10))
    out = set()
    for a, b in zip(draws, draws[1:]):
        if key(a) == key(b) and a["columns"] > 50:
            out.add(a["number"])
            out.add(b["number"])
    return out


def crowd_model(draws, half_life=40000.0, ridge=30.0):
    """Prizes are fixed, so winner counts are a direct poll of the crowd: when popular numbers are drawn, more
    bets match 5 of them. Weighted ridge regression of log(winners of 5 / expected) on the drawn numbers;
    a drawn number shifts it by about (5/8 - 3/12) of how much more often it is played."""
    dec = 0.5 ** (1.0 / half_life)
    T = len(draws)
    dup = duplicated(draws)
    A = [[0.0] * (N + 1) for _ in range(N + 1)]
    b = [0.0] * (N + 1)
    used = 0
    for t, d in enumerate(draws):
        if d["w7"] is None or d["w8"] is None or d["columns"] < 50 or d["number"] in dup:
            continue
        e = d["columns"] * H[5]
        y = math.log((d["w7"] + d["w8"] + 0.5) / (e + 0.5))
        wt = dec ** (T - 1 - t) / (1.0 / e + 0.01)
        idx = [x - 1 for x in d["balls"]] + [N]
        for i in idx:
            b[i] += wt * y
            Ai = A[i]
            for j in idx:
                Ai[j] += wt
        used += 1
    for i in range(N):
        A[i][i] += ridge
    sol = solve(A, b)
    m = sum(sol[:N]) / N
    lever = 5 / K - 3 / (N - K)
    delta = [(v - m) / lever for v in sol[:N]]
    return {"delta": delta, "used": used, "mu": sol[N] + K * m}


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
        """How many times more (or less) often than an average ticket the crowd plays these eight numbers."""
        return self.raw(C) / self.norm


# ----------------------------------------------------------------------------- 3. what the superprize is worth

def small_value(draws, i, memory):
    """Expected payout per bet of the fixed prizes (categories 2..9) in draw i. A category nobody won keeps
    the last prize paid at the same bet price."""
    d = draws[i]
    price = d["ticket_price"]
    v = 0.0
    for c in range(2, 10):
        w, a = d.get(f"w{c}"), d.get(f"a{c}")
        if w is None:
            continue
        if w and a:
            memory[(c, price)] = a
        v += P_CAT[c] * memory.get((c, price), 0.0)
    return v


def values(draws):
    """For every draw: what the superprize and the fixed prizes return per ruble of a bet."""
    memory = {}
    main, small = [], []
    for i, d in enumerate(draws):
        price = d["ticket_price"] or 1
        small.append(small_value(draws, i, memory) / price)
        main.append(P_SUPER * d["sp"] / price)
    return main, small, memory


def prize_rules(draws, memory=None):
    if memory is None:
        memory = values(draws)[2]
    last = draws[-1]
    price = last["ticket_price"]
    prizes = {c: memory.get((c, price), 0.0) for c in range(2, 10) if last.get(f"w{c}") is not None}
    cols = [d["columns"] for d in draws[-300:]]
    by_price = {}
    for d in draws[-2000:]:
        by_price[d["ticket_price"]] = by_price.get(d["ticket_price"], 0) + 1
    slots = {}
    for d in draws[-1500:]:
        slots.setdefault(d["date"][11:16], []).append(d["ticket_price"])
    return {"price": price, "prizes": prizes, "ev_small": sum(P_CAT[c] * a for c, a in prizes.items()),
            "columns": _median(cols), "prices": dict(sorted(by_price.items())),
            "slot_price": {s: _median(v[-10:]) for s, v in sorted(slots.items())}}


def jackpot_history(draws, main=None):
    """How the superprize behaves: what it adds to a ruble, how fast it grows and how often it is won."""
    main = main or values(draws)[0]
    t = _day(draws[-1])
    idx = [i for i, d in enumerate(draws) if (t - _day(d)).days <= 365]
    year = [draws[i] for i in idx]
    ms = sorted(main[i] for i in idx)
    q = lambda f: ms[min(len(ms) - 1, int(f * len(ms)))]
    out = {"year_draws": len(year), "m_median": q(0.5), "m_q90": q(0.9), "m_max_year": ms[-1], "m_max_ever": max(main)}
    sp = [d["sp"] for d in year]
    out["sp_min"], out["sp_max"], out["sp_median"] = min(sp), max(sp), _median(sp)
    out["sp_max_ever"] = max(d["sp"] for d in draws)
    steps = [b["sp"] - a["sp"] for a, b in zip(year, year[1:]) if not a["w1"] and b["sp"] >= a["sp"]]
    out["sp_step"], out["sp_step_mean"] = _median(steps), (sum(steps) / len(steps) if steps else 0)
    wins = [d for d in draws if d["w1"]]
    out["wins_year"] = sum(1 for d in year if d["w1"])
    out["wins_all"] = len(wins)
    out["wins"] = [[d["number"], d["date"], d["sp"], d["w1"], d["a1"], d["columns"]] for d in wins[-60:]]
    dup = duplicated(draws)
    clean = [d for d in draws if d["number"] not in dup]
    out["check_bets"] = sum(d["columns"] for d in clean)
    out["check_exp"] = out["check_bets"] * P_SUPER
    out["check_obs"] = sum(d["w1"] or 0 for d in clean)
    out["check8_exp"] = out["check_bets"] * H[8]
    out["check8_obs"] = sum((d["w1"] or 0) + (d["w2"] or 0) for d in clean)
    return out


def timing_check(draws, main=None, years=3):
    """Walk-forward check of the timing rule: play only when the superprize's share of the return reaches the
    90th percentile of the previous year of draws, compared with playing every draw."""
    import bisect
    main = main or values(draws)[0]
    t_end = _day(draws[-1])
    test = [i for i, d in enumerate(draws) if (t_end - _day(d)).days <= 365 * years]
    per_year = max(1000, len(test) // years)
    j0 = test[0]
    lo = max(0, j0 - per_year)
    hist = sorted(main[lo:j0])
    every, chosen = [], []
    for i in test:
        thr = hist[int(0.9 * (len(hist) - 1))] if hist else 0.0
        every.append(main[i])
        if main[i] >= thr:
            chosen.append(main[i])
        bisect.insort(hist, main[i])
        if i + 1 - lo > per_year:
            k = bisect.bisect_left(hist, main[lo])
            if k < len(hist):
                hist.pop(k)
            lo += 1
    return {"draws": len(every), "every": sum(every) / len(every), "chosen": sum(chosen) / max(1, len(chosen)),
            "share": len(chosen) / len(every)}


# ----------------------------------------------------------------------------- 4. choosing tickets

def number_scores(nb, crowd):
    """A score per number: numbers that are drawn measurably more often always go into a ticket (a large score),
    the rest differ only by how rarely other people play them."""
    return [0.0] + [(10.0 if i in nb["anchors"] else 0.0) + math.log(nb["lift"][i]) - 0.02 * math.log(crowd.q[i])
                    for i in range(1, N + 1)]


def pick_tickets(last, repeats, n, scores, rng, max_shared=6):
    """Tickets with exactly `repeats` numbers of the last draw and the rest from the other twelve.
    Numbers with a higher score are preferred, with enough randomness to make the tickets different."""
    inside = sorted(last)
    outside = [x for x in range(1, N + 1) if x not in last]
    chosen = []
    for _ in range(n):
        best = None
        for _try in range(400):
            def draw(pool, k):
                keyed = sorted(pool, key=lambda x: scores[x] + rng.gauss(0.0, 0.05), reverse=True)
                return keyed[:k]
            C = sorted(draw(inside, repeats) + draw(outside, K - repeats))
            if any(len(set(C) & set(o)) > max_shared for o in chosen) and _try < 399:
                continue
            best = C
            break
        if best and best not in chosen:
            chosen.append(best)
    return chosen


def bonus_numbers(fc, n):
    """Bonus numbers for n tickets: the likeliest one if the generator favours it, otherwise all four in turn."""
    if "bonus" in fc["passed"]:
        pb = fc["bonus"]["p"]
        return [max(range(1, NB + 1), key=lambda i: pb[i])] * n
    return [i % NB + 1 for i in range(n)]


# ----------------------------------------------------------------------------- commands

def num(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def rub(x, d=0):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def fmt_p(p):
    return "< 0,0001" if p < 1e-4 else num(p, 3)


FORECASTS = (("freq", "частоты чисел"), ("repeat", "повторы из прошлого тиража"), ("repeat2", "повторы через тираж"),
             ("repeat_number", "свой процент повторов у каждого числа"), ("gap", "сколько тиражей число не выпадало"),
             ("bonus", "частоты доп. числа"))


def cmd_analyze(draws):
    r = patterns_report(draws)
    fc = forecast_models(draws)
    rp = r["repeat"]
    print(f"\n1. Закономерности: {r['draws']} тиражей, №{draws[0]['number']}–№{draws[-1]['number']}")
    print(f"   Повторы от тиража к тиражу: в среднем {num(rp['mean'], 3)} числа из 8 (теория {num(rp['expected'], 3)}), p = {fmt_p(rp['p'])}")
    print("   повторов   доля тиражей   теория    отношение")
    for row in rp["rows"]:
        print(f"      {row['j']}        {num(row['share'] * 100, 2):>6}%      {num(row['theory'] * 100, 2):>6}%    ×{num(row['lift'], 3)}"
              + ("" if abs(row["z"]) < 3 else "  !"))
    print(f"   через 2, 3, 5 и 10 тиражей: " + ", ".join(num(r["repeat_lag"][k], 3) for k in (2, 3, 5, 10)))
    print(f"   число выпадает снова сразу после выпадения в {num(r['repeat_rate'] * 100, 2)}% случаев (теория 40%);"
          f" у отдельных чисел от {num(r['repeat_rate_min'] * 100, 1)} до {num(r['repeat_rate_max'] * 100, 1)}%, p = {fmt_p(r['repeat_number_p'])}")
    print(f"   «горячие» (были в двух последних тиражах): {num(r['hot_rate'] * 100, 2)}% (z = {num(r['hot_z'])});"
          f" «холодные» (не было в пяти): {num(r['cold_rate'] * 100, 2)}% (z = {num(r['cold_z'])})")
    print(f"   частоты 20 чисел: p = {fmt_p(r['freq_p'])} (от {r['min_count']} до {r['max_count']} при ожидании {r['expected']:.0f})")
    print(f"   частоты по порядку выпадения: p от {fmt_p(min(r['pos_p']))} до {fmt_p(max(r['pos_p']))}")
    print(f"   пары чисел: p = {fmt_p(r['pairs_p'])}; чётных среди восьми: p = {fmt_p(r['even_p'])}")
    print(f"   сумма чисел: {num(r['sum_mean'], 2)} (теория {num(r['sum_expected'], 0)}, z = {num(r['sum_z'])});"
          f" соседних пар: {num(r['adjacent_mean'], 3)} (теория {num(r['adjacent_expected'], 3)})")
    print(f"   доп. число 1–4: {', '.join(map(str, r['bonus_counts']))}, p = {fmt_p(r['bonus_p'])};"
          f" повтор подряд {num(r['bonus_repeat'] * 100, 2)}% (теория 25%, z = {num(r['bonus_repeat_z'])})")
    print(f"   зависимость от часа: p = {fmt_p(r['hour_p'])}; от года: p = {fmt_p(r['year_p'])}")
    print(f"   одна и та же восьмёрка выпадала дважды: {r['same_set_pairs']} раз (теория {num(r['same_set_expected'], 0)})")
    nb = number_bias(draws)
    t = nb["top"]
    print(f"   чаще всех выпадает {t}: в {num(nb['top_rate'] * 100, 2)}% тиражей при теории 40% (z = {num(nb['top_z'], 1)},"
          f" p = {num(nb['top_p'], 4)} с поправкой на выбор из 20); по годам: "
          + ", ".join(num(v * 100, 1) for v in nb["years"].values()))
    print(f"   проверка вперёд на {nb['walk_draws']} тиражах: лидер по прошлым данным выпадал в {num(nb['walk_rate'] * 100, 2)}% (z = {num(nb['walk_z'], 1)})")
    print("   Прогнозы, проверенные тираж за тиражом (выше нуля — лучше равных шансов):")
    for key, name in FORECASTS:
        print(f"      {name}: {num(fc[key]['score'], 1)} нат")
    if fc["passed"]:
        print("   → найдена устойчивая закономерность: " + ", ".join(n for k, n in FORECASTS if k in fc["passed"]) + "; она учтена")
    else:
        print("   → ни одна закономерность не угадывала лучше равных шансов: тиражи независимы")
    return r, fc, nb


def cmd_predict(draws, n_tickets=4, repeats=None, seed=None, nxt=None):
    last = draws[-1]
    print(f"Архив: {len(draws)} тиражей, последний №{last['number']} ({last['date']}): "
          f"{' '.join(map(str, sorted(last['balls'])))} + {last['bonus']}")
    _r, fc, nb = cmd_analyze(draws)
    rc = repeat_choice(draws)
    crowd = Crowd(crowd_model(draws))
    main, small, memory = values(draws)
    rules = prize_rules(draws, memory)
    hist = jackpot_history(draws, main)
    price = rules["price"]
    sp = last["sp"]
    label = f"после тиража №{last['number']}"
    if nxt and nxt.get("number", 0) > last["number"]:
        sp, label = nxt["sp"], f"в тираже №{nxt['number']} ({nxt['date']})"
        price = nxt.get("ticket_price") or price
    m_now = P_SUPER * sp / price
    print(f"\n2. Суперприз {label}: {rub(sp)} ₽, ставка {price} ₽")
    print(f"   шанс на одну ставку: 8 чисел + доп. число — 1 к {rub(1 / P_SUPER)}; 8 чисел — 1 к {rub(TOTAL)}")
    print(f"   суперприз даёт {num(m_now)} ₽ с рубля ставки, остальные призы — {num(rules['ev_small'] / rules['price'])} ₽")
    print(f"   за последний год: обычно {num(hist['m_median'])}, у 10% лучших тиражей от {num(hist['m_q90'])},"
          f" максимум {num(hist['m_max_year'])}; суперприз от {rub(hist['sp_min'])} до {rub(hist['sp_max'])} ₽")
    need = (price - rules["ev_small"] * price / rules["price"]) / P_SUPER
    print(f"   ставка окупится при суперпризе от {rub(need)} ₽; за всю историю он доходил до {rub(hist['sp_max_ever'])} ₽")
    if m_now >= hist["m_q90"]:
        print("   → сейчас один из 10% лучших моментов года для игры на суперприз")
    else:
        grow = hist["sp_step_mean"]
        steps = (hist["m_q90"] * price / P_SUPER - sp) / grow if grow > 0 else float("inf")
        print("   → лучше подождать: суперприз ниже 10% лучших моментов года"
              + (f", до них ≈{steps:.0f} тиражей (≈{steps / 48:.0f} дн.), если его не выиграют" if steps < 1e6 else ""))
    j = rc["repeats"] if repeats is None else max(0, min(K, repeats))
    rng = random.Random(seed)
    tickets = pick_tickets(set(last["balls"]), j, n_tickets, number_scores(nb, crowd), rng)
    bonus = bonus_numbers(fc, len(tickets))
    print(f"\n3. Комбинации на следующий тираж: {j} числа из прошлого тиража и {K - j} новых")
    print(f"   (за всю историю комбинации с {j} повторами выпадали в ×{num(rc['lifts'][j], 3)} раза чаще теории;"
          f" чаще всего повторяется {rc['most_common']} числа)")
    was = set(last["balls"])
    for C, b in zip(tickets, bonus):
        print("   " + " ".join((f"{x:2d}*" if x in was else f"{x:2d} ") for x in C) + f" + {b}")
    print("   * — число из прошлого тиража")
    if nb["anchors"]:
        a = nb["anchors"]
        print(f"   В каждой комбинации есть {', '.join(map(str, a))}: оно выпадает чаще остальных,"
              f" с ним шанс комбинации выше примерно на {num((nb['lift'][a[0]] - 1) * 100, 1)}–{num((nb['top_rate'] / (K / N) - 1) * 100, 1)}%.")
    print(f"\n   Проверка выбора числа повторов на {rc['walk_draws']} тиражах (выбор только по прошлым данным):"
          f" такие комбинации выпадали в ×{num(rc['walk_lift'], 3)} раза чаще средней.")
    print("\n4. Шанс суперприза хотя бы одной ставкой (разные восьмёрки):")
    for n in (1, 10, 100, 1000):
        print(f"   {n:5d} ставок, {rub(n * price):>7} ₽:  1 к {rub(1 / (n * P_SUPER))}")
    return tickets


def cmd_history(draws):
    main, _small, _m = values(draws)
    hist = jackpot_history(draws, main)
    tc = timing_check(draws, main)
    print(f"\nСуперприз за последний год ({hist['year_draws']} тиражей): от {rub(hist['sp_min'])} до {rub(hist['sp_max'])} ₽,"
          f" обычно {rub(hist['sp_median'])} ₽; максимум за всю историю {rub(hist['sp_max_ever'])} ₽")
    print(f"   растёт в среднем на {rub(hist['sp_step_mean'])} ₽ за тираж; выигрывали {hist['wins_year']} раз за год,"
          f" {hist['wins_all']} раз за всю историю")
    print(f"   выигрышных ставок 8+1: {hist['check_obs']} при ожидании {num(hist['check_exp'], 1)};"
          f" 8 чисел всего: {hist['check8_obs']} при ожидании {num(hist['check8_exp'], 1)} (ставок {rub(hist['check_bets'])})")
    print(f"   суперприз даёт с рубля ставки: обычно {num(hist['m_median'])}, 10% лучших от {num(hist['m_q90'])},"
          f" максимум за год {num(hist['m_max_year'])}, за всю историю {num(hist['m_max_ever'])} ₽")
    print(f"\nПравило «играть только в 10% лучших моментов» на {tc['draws']} тиражах за 3 года (порог по предыдущему году):")
    print(f"   в каждом тираже суперприз давал {num(tc['every'], 3)} ₽ с рубля,"
          f" по правилу ({num(tc['share'] * 100, 1)}% тиражей) — {num(tc['chosen'], 3)} ₽, в {num(tc['chosen'] / tc['every'], 2)} раза больше")
    return hist, tc


def main():
    try:  # old Windows consoles cannot print the rouble sign
        sys.stdout.reconfigure(errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="«Рапидо 2.0»: архив, закономерности, игра на суперприз.")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("update", help="скачать новые тиражи")
    pr = sub.add_parser("predict", help="комбинации на следующий тираж (по умолчанию)")
    pr.add_argument("-n", "--tickets", type=int, default=4, help="сколько комбинаций (по умолчанию 4)")
    pr.add_argument("--repeats", type=int, default=None, help="сколько чисел взять из прошлого тиража (по умолчанию — по истории)")
    pr.add_argument("--offline", action="store_true", help="не обновлять архив")
    sub.add_parser("analyze", help="только закономерности")
    sub.add_parser("history", help="как ведёт себя суперприз и когда выгоднее играть")
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
    if len(draws) < 3000:
        sys.exit("Архив пуст: запустите `python rapido2.py update` с доступом к интернету.")
    nxt = None
    try:
        nxt = json.load(open(META_FILE, encoding="utf-8")).get("next")
    except (OSError, ValueError):
        nxt = None
    if cmd == "predict":
        cmd_predict(draws, getattr(a, "tickets", 4), getattr(a, "repeats", None), nxt=nxt)
    elif cmd == "analyze":
        cmd_analyze(draws)
    elif cmd == "history":
        cmd_history(draws)


if __name__ == "__main__":
    main()
