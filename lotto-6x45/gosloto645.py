#!/usr/bin/env python3
"""Гослото «6 из 45»: архив тиражей, проверка случайности, подбор комбинации и тест на истории.

Запуск без аргументов: обновить архив и выдать комбинацию на следующий тираж.
Подробности: python gosloto645.py --help
"""
import argparse
import csv
import json
import math
import os
import random
import re
import sys
import time
import urllib.parse
import urllib.request
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(HERE, "draws_6x45.csv")

API = "https://www.stoloto.ru/p/api/mobile/api/v35/service/draws/archive"
# Public client key that stoloto.ru's own pages send with every archive request.
PARTNER = "bXMjXFRXZ3coWXh6R3s1NTdUX3dnWlBMLUxmdg"

N_BALLS, PICK = 45, 6
TIERS = (2, 3, 4, 5, 6)
FIELDS = (["number", "date", "b1", "b2", "b3", "b4", "b5", "b6", "columns", "players", "ticket_price", "superprize"]
          + [f"w{k}" for k in TIERS] + [f"d{k}" for k in TIERS])


# ----------------------------------------------------------------------------- archive

UA = "Mozilla/5.0 (gosloto645 archive reader)"
_partner = [PARTNER]


def _discover_partner():
    """If stoloto.ru rotates its public client key, read the new one from the site's own scripts."""
    try:
        req = urllib.request.Request("https://www.stoloto.ru/6x45/archive", headers={"User-Agent": UA})
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
        for u in re.findall(r'src="(https://static\.stoloto\.ru/[^"]+\.js)"', html):
            js = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30).read().decode("utf-8", "ignore")
            m = re.search(r'GOSLOTO_PARTNER_T\(\)\{return\(0,[\w$.]+\)\("([^"]+)"', js)
            if m:
                return m.group(1)
    except Exception:
        return None
    return None


def _get(page, count=50, tries=5):
    url = API + "?" + urllib.parse.urlencode({"game": "6x45", "count": count, "page": page})
    rediscovered = False
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json",
                                                   "Gosloto-Partner": _partner[0]})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
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
                raise RuntimeError(f"страница {page}: {e}")
            time.sleep(2 ** attempt)


def _parse(d):
    """One API draw -> flat record, or None if the draw is not finished yet."""
    if d.get("status") != "COMPLETED":
        return None
    balls = (d.get("combination") or {}).get("structured") or []
    if len(balls) != PICK:
        return None
    rec = {"number": int(d["number"]), "date": d.get("date", "")[:16].replace("T", " "),
           "columns": 0, "players": int(d.get("ticketCount") or 0),
           "ticket_price": int(d.get("ticketPrice") or 0), "superprize": int(d.get("superPrize") or 0)}
    for i, b in enumerate(balls, 1):
        rec[f"b{i}"] = int(b)
    for k in TIERS:
        rec[f"w{k}"] = ""
        rec[f"d{k}"] = ""
    wc = d.get("winningCategories")
    info = {}
    if isinstance(wc, str) and wc.strip():
        try:
            info = json.loads(wc)
        except ValueError:
            info = {}
    rec["columns"] = int(info.get("columns") or d.get("betsCount") or 0)
    if info.get("players"):
        rec["players"] = int(info["players"])
    for c in info.get("categories", []):
        desc = c.get("description", "")
        if desc.startswith("Совпало "):
            try:
                k = int(desc.split()[1])
            except (IndexError, ValueError):
                continue
            if k in TIERS:
                rec[f"w{k}"] = int(c.get("win_columns_number") or 0)
                rec[f"d{k}"] = round((c.get("dividend_per_column") or 0) / 100, 2)
    return rec


def load_draws():
    if not os.path.exists(DATA_FILE):
        return []
    out = []
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rec = {"number": int(r["number"]), "date": r["date"]}
            rec["balls"] = [int(r[f"b{i}"]) for i in range(1, 7)]
            for key in ("columns", "players", "ticket_price", "superprize"):
                rec[key] = int(float(r[key] or 0))
            for k in TIERS:
                rec[f"w{k}"] = int(r[f"w{k}"]) if r[f"w{k}"] != "" else None
                rec[f"d{k}"] = float(r[f"d{k}"]) if r[f"d{k}"] != "" else None
            out.append(rec)
    out.sort(key=lambda x: x["number"])
    return out


META_FILE = os.path.join(HERE, "draws_6x45.meta.json")


def _save(known, complete):
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for n in sorted(known):
            w.writerow({k: known[n].get(k, "") for k in FIELDS})
    os.replace(tmp, DATA_FILE)
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump({"complete": complete, "updated": time.strftime("%Y-%m-%d %H:%M")}, f)


def update(verbose=True):
    """Download finished draws. The first run walks the whole archive (≈390 requests, 2–3 min);
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
    page, added = 1, 0
    while True:
        data = _get(page)
        draws = data.get("draws", [])
        fresh = 0
        for d in draws:
            rec = _parse(d)
            if rec and rec["number"] not in known:
                known[rec["number"]] = rec
                fresh += 1
        added += fresh
        if verbose and (page == 1 or page % 25 == 0):
            last = draws[-1]["number"] if draws else "?"
            print(f"  страница {page}: дошли до тиража {last}, новых {added}", flush=True)
        if not data.get("hasMore") or not draws:
            complete = True
            break
        if complete and fresh == 0 and page > 1:
            break  # caught up with the stored archive
        if page % 50 == 0:
            _save(known, False if not complete else True)
        page += 1
        time.sleep(0.25)
    _save(known, complete)
    if verbose:
        print(f"Архив: {len(known)} тиражей (новых: {added}). Файл: {DATA_FILE}")
    return added


# ----------------------------------------------------------------------------- math helpers

# P(exactly k of the 6 drawn numbers are on one ticket)
H = {k: math.comb(6, k) * math.comb(39, 6 - k) / math.comb(45, 6) for k in range(7)}


def chi2_sf(x, k):
    """Upper tail of the chi-square distribution (regularized incomplete gamma)."""
    a, x = k / 2.0, x / 2.0
    if x <= 0:
        return 1.0
    lg = math.lgamma(a)
    if x < a + 1:
        s = t = 1.0 / a
        n = a
        for _ in range(2000):
            n += 1
            t *= x / n
            s += t
            if abs(t) < 1e-15 * s:
                break
        return max(0.0, 1.0 - s * math.exp(-x + a * math.log(x) - lg))
    b, c, d = x + 1 - a, 1e300, 1.0 / (x + 1 - a)
    h = d
    for i in range(1, 2000):
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
    """Gaussian elimination with partial pivoting; A is modified."""
    n = len(b)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        if abs(piv) < 1e-12:
            continue
        inv = 1.0 / piv
        for r in range(c + 1, n):
            f = M[r][c] * inv
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

def randomness_report(draws):
    T = len(draws)
    out = {"draws": T}
    cnt = [0] * 46
    for d in draws:
        for x in d["balls"]:
            cnt[x] += 1
    E = T * 6 / 45
    fpc = (45 - 6) / (45 - 1)  # six balls are drawn without replacement
    chi = sum((cnt[i] - E) ** 2 / E for i in range(1, 46)) / fpc
    out["freq_p"] = chi2_sf(chi, 44)
    out["min_count"] = min(cnt[1:])
    out["max_count"] = max(cnt[1:])
    out["expected"] = E
    pos_p = []
    for pos in range(6):
        c = [0] * 46
        for d in draws:
            c[d["balls"][pos]] += 1
        e = T / 45
        pos_p.append(chi2_sf(sum((c[i] - e) ** 2 / e for i in range(1, 46)), 44))
    out["pos_p"] = pos_p
    pc = {}
    for d in draws:
        for p in combinations(sorted(d["balls"]), 2):
            pc[p] = pc.get(p, 0) + 1
    ep = T * 15 / 990
    out["pairs_p"] = chi2_sf(sum((pc.get(p, 0) - ep) ** 2 / ep for p in combinations(range(1, 46), 2)), 989)
    ov = [len(set(draws[i]["balls"]) & set(draws[i - 1]["balls"])) for i in range(1, T)]
    m = sum(ov) / len(ov)
    sd = math.sqrt(sum((o - m) ** 2 for o in ov) / len(ov))
    out["overlap_mean"] = m
    out["overlap_z"] = (m - 0.8) / (sd / math.sqrt(len(ov)))
    return out


def bias_model(draws, gate=10.0):
    """Prequential check of every frequency forecast we could build from the archive.

    For each draw the forecast is made only from the draws before it (with several memory lengths),
    and is scored by sum(log(45 * p_i)) over the six balls. Under truly random draws the score of any
    forecast drifts below zero, so a clearly positive total would be a real, exploitable bias.
    Returns per-number probabilities p[1..45] (uniform unless the gate is passed) and the test table.
    """
    table = []
    best = None
    for hl in (300, 1000, 3000, None):
        dec = 0.5 ** (1.0 / hl) if hl else 1.0
        for a in (450.0, 4500.0):
            c = [0.0] * 46
            n = 0.0
            score = 0.0
            for t, d in enumerate(draws):
                if t >= 200:
                    for x in d["balls"]:
                        score += math.log(45.0 * (c[x] + a / 45.0) / (n + a))
                if dec != 1.0:
                    for i in range(1, 46):
                        c[i] *= dec
                    n *= dec
                for x in d["balls"]:
                    c[x] += 1.0
                n += 6.0
            p = [0.0] + [(c[i] + a / 45.0) / (n + a) for i in range(1, 46)]
            table.append((hl, a, score))
            if best is None or score > best[2]:
                best = (hl, a, score, p)
    if best[2] > gate:
        return best[3], table, best
    return [0.0] + [1.0 / 45] * 45, table, best


# ----------------------------------------------------------------------------- 2. what does the crowd play?

def _pf(a, b):
    """Pair features of two numbers a < b: consecutive, same ten, same last digit, same column of a 9-wide grid."""
    return (1.0 if b - a == 1 else 0.0, 1.0 if a // 10 == b // 10 else 0.0,
            1.0 if a % 10 == b % 10 else 0.0, 1.0 if (b - a) % 9 == 0 else 0.0)


PF = {(a, b): _pf(a, b) for a, b in combinations(range(1, 46), 2)}
CROWD_CFG = {2: (1500.0, 0.003), 3: (1500.0, 0.012), 4: (4000.0, 0.05)}  # memory half-life (draws), noise floor
NF = 45 + 4 + 1  # numbers, pair features, intercept


def _row(d):
    s = sorted(d["balls"])
    f = [0.0, 0.0, 0.0, 0.0]
    for p in combinations(s, 2):
        q = PF[p]
        for i in range(4):
            f[i] += q[i]
    return [x - 1 for x in s], f


class CrowdFit:
    """Weighted ridge regression of log(winners / expected winners) on the drawn numbers.

    The more popular the drawn numbers are among players, the more winners a draw has. Fitted on every
    draw before `end`; older draws count less (half-life chosen by out-of-sample tests on this archive).
    Kept incrementally so a walk-forward backtest can refit cheaply.
    """

    def __init__(self, draws, k):
        self.draws, self.k = draws, k
        self.hl, self.floor = CROWD_CFG[k]
        self.A = [[0.0] * NF for _ in range(NF)]
        self.b = [0.0] * NF
        self.pos = 0
        self.rows = {}

    def advance(self, end):
        k = self.k
        if end < self.pos:
            raise ValueError("cannot go back")
        shrink = 0.5 ** ((end - self.pos) / self.hl)
        if shrink != 1.0:
            for r in self.A:
                for j in range(NF):
                    r[j] *= shrink
            self.b = [v * shrink for v in self.b]
        for t in range(self.pos, end):
            d = self.draws[t]
            W, N = d[f"w{k}"], d["columns"]
            if W is None or N <= 0:
                continue
            e = N * H[k]
            y = math.log((W + 0.5) / e)
            w = 0.5 ** ((end - 1 - t) / self.hl) / (1.0 / e + self.floor)
            idx, f = _row(d)
            ent = [(i, 1.0) for i in idx] + [(45 + i, f[i]) for i in range(4) if f[i]] + [(NF - 1, 1.0)]
            for j, vj in ent:
                Aj = self.A[j]
                wv = w * vj
                for l, vl in ent:
                    Aj[l] += wv * vl
                self.b[j] += wv * y
        self.pos = end

    def solve(self):
        A = [r[:] for r in self.A]
        for j in range(45):
            A[j][j] += 50.0
        for j in range(45, 49):
            A[j][j] += 0.5
        sol = solve(A, self.b[:])
        return sol[:45], sol[45:49], sol[49]


class Crowd:
    """Scores a ticket: how much more (or less) it is expected to pay per hit than an average ticket."""

    def __init__(self, coefs, p=None, n_norm=3000, seed=7):
        self.coefs = coefs
        p = p or [0.0] + [1.0 / 45] * 45
        self.e, self.q, self.beta = {}, {}, {}
        for k, (beta, theta, _mu) in coefs.items():
            b = [0.0] + list(beta)
            self.beta[k] = b
            # chance factor 45*p_i (1.0 when the draws are fair) times the crowd factor exp(-beta_i)
            self.e[k] = [0.0] + [45.0 * p[i] * math.exp(-b[i]) for i in range(1, 46)]
            qk = [[1.0] * 46 for _ in range(46)]
            for (a, c), f in PF.items():
                v = math.exp(-sum(theta[i] * f[i] for i in range(4)))
                qk[a][c] = qk[c][a] = v
            self.q[k] = qk
        rng = random.Random(seed)
        self.norm = {k: 1.0 for k in coefs}
        acc = {k: 0.0 for k in coefs}
        for _ in range(n_norm):
            g = self.raw(sorted(rng.sample(range(1, 46), 6)))
            for k in coefs:
                acc[k] += g[k]
        self.norm = {k: acc[k] / n_norm for k in coefs}

    def raw(self, C):
        out = {}
        for k in self.coefs:
            e, q, b = self.e[k], self.q[k], self.beta[k]
            rest = math.exp((6 - k) / 39.0 * sum(b[x] for x in C))  # the other drawn numbers come from outside C
            if k == 2:
                s = sum(e[a] * e[c] * q[a][c] for a, c in combinations(C, 2)) / 15.0
            elif k == 3:
                s = sum(e[a] * e[c] * e[d] * q[a][c] * q[a][d] * q[c][d] for a, c, d in combinations(C, 3)) / 20.0
            else:
                s = 0.0
                for a, c, d, f in combinations(C, 4):
                    s += e[a] * e[c] * e[d] * e[f] * q[a][c] * q[a][d] * q[a][f] * q[c][d] * q[c][f] * q[d][f]
                s /= 15.0
            out[k] = s * rest
        return out

    def mult(self, C):
        g = self.raw(C)
        return {k: g[k] / self.norm[k] for k in g}


def fit_crowd(draws, end=None, p=None, fits=None):
    end = len(draws) if end is None else end
    fits = fits or {k: CrowdFit(draws, k) for k in CROWD_CFG}
    coefs = {}
    for k, f in fits.items():
        f.advance(end)
        coefs[k] = f.solve()
    return Crowd(coefs, p), fits


# ----------------------------------------------------------------------------- 3. how the prize fund pays right now

def prize_regime(draws, window=14 * 24):
    """Read the current payout rules straight from the latest draws: which tiers split their fund between
    winners, what a fixed tier pays, and what one ticket is worth on average in each daily draw slot."""
    def sig(d):
        return (tuple(k for k in (2, 3, 4, 5) if d[f"w{k}"] is not None), d["ticket_price"])
    last = sig(draws[-1])
    start = len(draws) - 1
    while start > 0 and sig(draws[start - 1]) == last:
        start -= 1
    reg = [d for d in draws[max(start, len(draws) - window):] if d["columns"] > 0]
    info = {"start_number": draws[start]["number"], "draws": len(reg), "price": draws[-1]["ticket_price"],
            "superprize": draws[-1]["superprize"], "tiers": {}}
    for k in (2, 3, 4, 5):
        vals = [d[f"d{k}"] for d in reg if d[f"w{k}"] and d[f"d{k}"]]
        if not vals:
            continue
        distinct = len(set(vals)) / len(vals)
        mean = sum(vals) / len(vals)
        cv = math.sqrt(sum((v - mean) ** 2 for v in vals) / len(vals)) / mean if mean else 0.0
        shared = distinct > 0.5 and cv > 0.05
        fixed = sorted(vals)[len(vals) // 2]
        # a shared tier's fund in one draw = fixed part + share of every bet; fit it on the current rules
        xs = [d["columns"] for d in reg]
        ys = [(d[f"w{k}"] or 0) * (d[f"d{k}"] or 0) for d in reg]
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        sxx = sum((x - mx) ** 2 for x in xs)
        b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx else 0.0
        a = my - b * mx
        if not shared or len(reg) < 8 or a < 0 or b < 0:
            a, b = 0.0, sum(y / x for x, y in zip(xs, ys)) / len(xs)
        per_col = sum(y / x for x, y in zip(xs, ys)) / len(xs)
        info["tiers"][k] = {"shared": shared, "fixed": fixed, "per_col": per_col, "a": a, "b": b}
    slots = {}
    for d in reg:
        slots.setdefault(d["date"][11:16], []).append(d)
    info["slots"] = {s: {"columns": sorted(d["columns"] for d in ds[-10:])[len(ds[-10:]) // 2], "draws": len(ds)}
                     for s, ds in sorted(slots.items())}
    return info


def ticket_value(info, mult, columns):
    """Expected return of one bet in a draw with `columns` bets: (average ticket, this ticket)."""
    avg = our = H[6] * info["superprize"]
    for k, t in info["tiers"].items():
        if t["shared"]:
            ev = (t["a"] + t["b"] * columns) / columns
            avg += ev
            our += ev * mult.get(k, 1.0)
        else:
            avg += H[k] * t["fixed"]
            our += H[k] * t["fixed"]
    return avg, our


# ----------------------------------------------------------------------------- 4. choosing tickets

def acceptable(C, recent):
    """Skip shapes that pattern players fill in by hand: they make prizes shared more often."""
    s = sorted(C)
    run = best = 1
    for a, b in zip(s, s[1:]):
        run = run + 1 if b - a == 1 else 1
        best = max(best, run)
    if best >= 3:
        return False
    tens = [0] * 5
    for x in s:
        tens[x // 10] += 1
    if max(tens) >= 4:
        return False
    for w in (7, 8, 9, 10):
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


def pick_tickets(score, n, recent, rng, restarts=6, max_shared=2):
    """Local search over 6-number tickets maximizing `score`; tickets share at most `max_shared` numbers."""
    chosen = []
    for _ in range(n):
        best_c, best_s = None, -1e18
        for _r in range(restarts):
            for _try in range(200):
                C = sorted(rng.sample(range(1, 46), 6))
                if acceptable(C, recent) and all(len(set(C) & set(o)) <= max_shared for o in chosen):
                    break
            else:
                continue
            cur = score(C)
            improved = True
            while improved:
                improved = False
                cand_best, cand_c = cur, None
                for i in range(6):
                    rest = C[:i] + C[i + 1:]
                    for x in range(1, 46):
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


def objective(crowd, weights):
    def f(C):
        m = crowd.mult(C)
        return sum(weights[k] * m[k] for k in weights)
    return f


def tier_weights(info):
    """How much each shared tier contributes to a ticket's value under the current rules."""
    w = {k: info["tiers"][k]["per_col"] for k in (2, 3, 4) if k in info["tiers"] and info["tiers"][k]["shared"]}
    if not w:  # fixed prizes everywhere: crowd only matters for sharing the superprize
        w = {2: 0.2, 3: 0.3, 4: 0.5}
    return w


# ----------------------------------------------------------------------------- commands

def fmt_p(p):
    return "< 0,0001" if p < 1e-4 else num(p, 3)


def num(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def rub(x, d=1):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def cmd_analyze(draws):
    r = randomness_report(draws)
    print(f"\n1. Случайность тиражей: {r['draws']} тиражей, №{draws[0]['number']}–№{draws[-1]['number']}")
    print(f"   частоты 45 чисел: p = {fmt_p(r['freq_p'])} (от {r['min_count']} до {r['max_count']} при ожидании {r['expected']:.0f})")
    print(f"   частоты по позиции шара: p = {'; '.join(fmt_p(p) for p in r['pos_p'])}")
    print(f"   частоты 990 пар: p = {fmt_p(r['pairs_p'])}")
    print(f"   совпадение с прошлым тиражом: {num(r['overlap_mean'], 3)} при теории 0,800 (z = {num(r['overlap_z'])})")
    p, table, best = bias_model(draws)
    hl = "вся история" if best[0] is None else f"полупериод {best[0]} тиражей"
    print(f"   лучший прогноз частот, проверенный тираж за тиражом: {num(best[2], 1)} нат против равных шансов ({hl})")
    if best[2] > 10:
        print("   → найдено устойчивое смещение, оно учтено при выборе чисел")
    else:
        print("   → числа выпадают равновероятно: ни один прогноз по частотам не угадывал лучше случая")
    return p


def cmd_predict(draws, n_tickets=3, bets=1, seed=None):
    last = draws[-1]
    print(f"Архив: {len(draws)} тиражей, последний №{last['number']} ({last['date']}): {' '.join(map(str, sorted(last['balls'])))}")
    p = cmd_analyze(draws)
    crowd, _ = fit_crowd(draws, p=p)
    pop = sorted(range(1, 46), key=lambda i: crowd.beta[3][i])
    print("\n2. Выбор других игроков (по числу победителей во всех тиражах):")
    print("   реже всего ставят: " + ", ".join(map(str, pop[:12])))
    print("   чаще всего ставят: " + ", ".join(map(str, pop[::-1][:12])))
    info = prize_regime(draws)
    print(f"\n3. Правила выплат сейчас (с тиража №{info['start_number']}, тиражей: {info['draws']}): "
          f"ставка {info['price']} ₽, суперприз {rub(info['superprize'], 0)} ₽")
    for k, t in sorted(info["tiers"].items()):
        if t["shared"]:
            kind = f"делится между победителями, фонд ≈ {rub(t['a'], 0)} ₽ + {num(t['b'])} ₽ с каждой ставки"
        else:
            kind = f"фиксированный, {rub(t['fixed'], 0)} ₽"
        print(f"   угадано {k}: {kind}")
    rng = random.Random(seed)
    recent = [set(d["balls"]) for d in draws[-50:]]
    many = n_tickets > 10
    tickets = pick_tickets(objective(crowd, tier_weights(info)), n_tickets, recent, rng,
                           restarts=2 if many else 6, max_shared=3 if n_tickets > 20 else 2)
    print("\n4. Комбинации на следующий тираж:")
    for C in tickets:
        m = crowd.mult(C)
        print("   " + " ".join(f"{x:2d}" for x in C) +
              "   приз при выигрыше: " + ", ".join(f"за {k} ×{num(m[k])}" for k in (2, 3, 4)))
    m0 = crowd.mult(tickets[0])
    extra = f" (вместе с вашими {bets} ставками)" if bets > 1 else ""
    print(f"\n5. Сколько в среднем возвращает одна ставка (до налогов), по времени тиража{extra}:")
    print("   время   ставок   обычный билет   билет №1   на 1 ₽")
    rows = []
    for s, v in info["slots"].items():
        avg, our = ticket_value(info, m0, v["columns"] + bets)
        rows.append((s, v["columns"], avg, our))
        mark = "  ←" if our >= info["price"] else ""
        print(f"   {s}  {v['columns']:7d}   {rub(avg):>9} ₽   {rub(our):>7} ₽   {num(our / info['price'])}{mark}")
    best = max(rows, key=lambda r: r[3])
    print(f"\n   Выгоднее всего тираж в {best[0]}: {num(best[3] / info['price'])} ₽ на 1 ₽ ставки "
          f"(обычный билет там же — {num(best[2] / info['price'])}).")
    return tickets


def cmd_backtest(draws, start=5000, block=1000, k=10, seed=1):
    """Walk-forward test: for every block of draws the model sees only earlier draws."""
    rng = random.Random(seed)
    info = prize_regime(draws)
    weights = tier_weights(info)
    # a hit pays today's average prize per expected winner, divided by the draw's actual winners
    A = {kk: info["tiers"][kk]["per_col"] / H[kk] for kk in (2, 3, 4) if kk in info["tiers"]}
    names = ["антитолпа", "случайные", "популярные", "горячие", "холодные"]
    # per block and strategy: hits by tier, sum of relative prize and hits per tier, payouts
    blocks = []
    fits = None
    t0 = time.time()
    for b0 in range(start, len(draws), block):
        crowd, fits = fit_crowd(draws, end=b0, fits=fits)
        recent = [set(d["balls"]) for d in draws[max(0, b0 - 50):b0]]
        obj = objective(crowd, weights)
        anti = pick_tickets(obj, k, recent, rng, restarts=2)
        popular = pick_tickets(lambda C: -obj(C), k, [], rng, restarts=2)
        rnd = [sorted(rng.sample(range(1, 46), 6)) for _ in range(k)]
        freq = [0] * 46
        for d in draws[max(0, b0 - 300):b0]:
            for x in d["balls"]:
                freq[x] += 1
        order = sorted(range(1, 46), key=lambda i: -freq[i])
        hot = [sorted(rng.sample(order[:12], 6)) for _ in range(k)]
        cold = [sorted(rng.sample(order[-12:], 6)) for _ in range(k)]
        sets = dict(zip(names, (anti, rnd, popular, hot, cold)))
        st = {s: {"hits": [0] * 7, "rel": {m: [0.0, 0] for m in (2, 3, 4)}, "sim": [0.0, 0], "real": [0.0, 0]} for s in names}
        for t in range(b0, min(len(draws), b0 + block)):
            d = draws[t]
            D = set(d["balls"])
            full = d["columns"] > 0 and all(d[f"w{kk}"] is not None for kk in (2, 3, 4))
            for s, tk in sets.items():
                x = st[s]
                for C in tk:
                    m = len(D & set(C))
                    x["hits"][m] += 1
                    if full:
                        if m in A:
                            r = d["columns"] * H[m] / (d[f"w{m}"] + 1)
                            x["sim"][0] += A[m] * r
                            x["rel"][m][0] += r
                            x["rel"][m][1] += 1
                        x["sim"][1] += 1
                    if m in (2, 3, 4, 5) and d[f"d{m}"] is not None:
                        x["real"][0] += d[f"d{m}"]
                    x["real"][1] += 1
        blocks.append(st)
        print(f"  блок с тиража №{draws[b0]['number']}: билет «антитолпы» {' '.join(map(str, anti[0]))}  ({time.time() - t0:.0f} с)", flush=True)

    def agg(bl, s):
        hits = [sum(b[s]["hits"][m] for b in bl) for m in range(7)]
        rel = {m: (sum(b[s]["rel"][m][0] for b in bl), sum(b[s]["rel"][m][1] for b in bl)) for m in (2, 3, 4)}
        sim = sum(b[s]["sim"][0] for b in bl) / max(1, sum(b[s]["sim"][1] for b in bl))
        real = sum(b[s]["real"][0] for b in bl) / max(1, sum(b[s]["real"][1] for b in bl))
        size = sum(H[m] * A[m] * rel[m][0] / max(1, rel[m][1]) for m in A)  # prize size only, hits at theory rate
        return hits, rel, sim, real, size

    def ci(metric, s):
        r = random.Random(3)
        L = len(blocks)
        vals = []
        for _ in range(1000):
            bl = [blocks[r.randrange(L)] for _ in range(L)]
            a, b = metric(agg(bl, s)), metric(agg(bl, "случайные"))
            vals.append(a / b if b else 0.0)
        vals.sort()
        return vals[25], vals[974]

    n_test = len(draws) - start
    print(f"\nПроверка на {n_test} тиражах (№{draws[start]['number']}–№{draws[-1]['number']}): "
          f"по {k} билетов каждой стратегии на тираж, модель знает только прошлое и переобучается каждые {block} тиражей.")
    res = {s: agg(blocks, s) for s in names}
    print("\nА. Вероятность угадать (доля билетов):")
    print("   стратегия     2 числа   3 числа   4 числа   5 чисел")
    print(f"   теория       {num(H[2], 5)}   {num(H[3], 5)}   {num(H[4], 5)}   {num(H[5], 6)}")
    for s in names:
        h = res[s][0]
        n = sum(h)
        print(f"   {s:<11}  " + "   ".join(num(h[m] / n, 5) for m in (2, 3, 4)) + f"   {num(h[5] / n, 6)}")
    print("\nБ. Размер приза при выигрыше по сравнению со средним тиражом (1,00 — как у всех):")
    print("   стратегия     2 числа  3 числа  4 числа")
    for s in names:
        rel = res[s][1]
        print(f"   {s:<11}  " + "  ".join(f"{num(rel[m][0] / max(1, rel[m][1]), 3):>7}" for m in (2, 3, 4)))
    print("\nВ. Выплата за 2–4 числа на билет по нынешним правилам:")
    print("   стратегия    только размер приза*        с фактическими попаданиями")
    for s in names:
        lo1, hi1 = ci(lambda r: r[4], s)
        lo2, hi2 = ci(lambda r: r[2], s)
        b4, b2 = res["случайные"][4], res["случайные"][2]
        print(f"   {s:<11}  {rub(res[s][4]):>5} ₽ ×{num(res[s][4] / b4, 3)} ({num(lo1, 3)}…{num(hi1, 3)})"
              f"   {rub(res[s][2]):>5} ₽ ×{num(res[s][2] / b2, 3)} ({num(lo2, 3)}…{num(hi2, 3)})")
    print("   * как если бы все стратегии угадывали ровно с теоретической частотой; в скобках 95% интервал")
    print("\nГ. Фактически выплаченные тогда призы за 2–5 чисел (правила тех лет, в основном фиксированные призы):")
    for s in names:
        lo, hi = ci(lambda r: r[3], s)
        print(f"   {s:<11}  {rub(res[s][3]):>5} ₽ ×{num(res[s][3] / res['случайные'][3], 3)} ({num(lo, 3)}…{num(hi, 3)})")
    return res


def main():
    try:  # old Windows consoles cannot print the rouble sign
        sys.stdout.reconfigure(errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Гослото «6 из 45»: архив, проверка случайности, подбор билетов, тест на истории.")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("update", help="скачать новые тиражи")
    pr = sub.add_parser("predict", help="комбинации на следующий тираж (по умолчанию)")
    pr.add_argument("-n", "--tickets", type=int, default=3, help="сколько комбинаций (по умолчанию 3)")
    pr.add_argument("--bets", type=int, default=1, help="сколько ставок вы покупаете в один тираж (влияет на выгоду)")
    pr.add_argument("--offline", action="store_true", help="не обновлять архив")
    sub.add_parser("analyze", help="только проверка случайности")
    bt = sub.add_parser("backtest", help="проверка метода на прошлых тиражах")
    bt.add_argument("--start", type=int, default=5000, help="с какого по счёту тиража начинать проверку")
    bt.add_argument("--block", type=int, default=1000, help="как часто переобучать модель, в тиражах")
    bt.add_argument("-k", type=int, default=10, help="билетов каждой стратегии на тираж")
    a = ap.parse_args()
    cmd = a.cmd or "predict"
    if cmd == "update" or (cmd == "predict" and not getattr(a, "offline", False)):
        print("Обновляю архив тиражей…")
        try:
            update()
        except Exception as e:
            print(f"Не удалось обновить архив ({e}); считаю по сохранённому.")
        if cmd == "update":
            return
    draws = load_draws()
    if len(draws) < 1000:
        sys.exit("Архив пуст: запустите `python gosloto645.py update` с доступом к интернету.")
    if cmd == "predict":
        cmd_predict(draws, getattr(a, "tickets", 3), getattr(a, "bets", 1))
    elif cmd == "analyze":
        cmd_analyze(draws)
    elif cmd == "backtest":
        cmd_backtest(draws, a.start, a.block, a.k)


if __name__ == "__main__":
    main()
