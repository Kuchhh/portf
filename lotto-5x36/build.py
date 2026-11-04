#!/usr/bin/env python3
"""Builds the web page for «5 из 36»: index.html (analysis of the whole archive, rebuilt once a day or when the
page template changes) and state.json (the latest draws and the next draw's superprizes, rebuilt every time).

Usage: python lotto-5x36/build.py --out 5x36      (after `python lotto-5x36/gosloto536.py update`)
"""
import argparse
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gosloto536 as G  # noqa: E402

TEMPLATE = os.path.join(HERE, "web", "app.html")


def r4(x):
    return round(x, 4)


def state(draws, meta):
    last = draws[-1]
    nxt = (meta or {}).get("next")
    if not nxt or nxt.get("number", 0) <= last["number"]:
        nxt = None
    rules = G.prize_rules(draws)
    return {
        "last": {"n": last["number"], "date": last["date"], "balls": sorted(last["balls"]), "bonus": last["bonus"],
                 "sp1": last["sp1"], "sp2": last["sp2"] or 0, "price": last["ticket_price"], "columns": last["columns"]},
        "next": nxt,
        "rules": {"price": rules["price"], "kind": rules["kind"], "start": rules["start"],
                  "ev_small": r4(rules["ev_small"]), "columns": rules["columns"], "start_number": rules["start_number"],
                  "tiers": {k: {kk: (r4(vv) if isinstance(vv, float) else vv) for kk, vv in t.items()}
                            for k, t in rules["period"]["tiers"].items()},
                  "slots": rules["slots"]},
        "times": [d["date"] for d in draws[-12:]],
        "recent": [sorted(d["balls"]) for d in draws[-100:]],
        "count": len(draws),
    }


def analysis(draws):
    r = G.randomness_report(draws)
    b = G.bias_model(draws)
    crowd_m = G.crowd_model(draws)
    crowd = G.Crowd(crowd_m)
    mains = G.main_values(draws)
    hist = G.jackpot_history(draws, mains)
    tc = G.timing_check(draws, mains)
    # what the superprizes added to a ruble, best draw of each day over the whole history, for the chart
    days = {}
    for d, v in zip(draws, mains):
        day = d["date"][:10]
        if v > days.get(day, (-1,))[0]:
            days[day] = (v, d["sp1"], d["sp2"] or 0, d["ticket_price"])
    series = [[k, r4(v[0]), v[1], v[2], v[3]] for k, v in sorted(days.items())]
    wins = [[d["date"][:10], 1 if d["w51"] else 0, d["sp2"] or 0] for d in draws if d["w5"] or d["w51"]]
    return {
        "first": {"n": draws[0]["number"], "date": draws[0]["date"]},
        "randomness": {k: (r4(v) if isinstance(v, float) else v) for k, v in r.items()},
        "bias": {"passed": b["passed"], "main": r4(b["main"][2]), "bonus": r4(b["bonus"][2]),
                 "p_main": [r4(x * G.N) for x in b["p_main"]], "p_bonus": [r4(x * G.NB) for x in b["p_bonus"]]},
        "crowd": {"q": [r4(x) for x in crowd.q], "norm": crowd.norm,
                  "beta3": [r4(x) for x in crowd_m["beta"][3]], "beta2": [r4(x) for x in crowd_m["beta"][2]]},
        "hist": {k: (r4(v) if isinstance(v, float) else v) for k, v in hist.items()},
        "timing": {k: (r4(v) if isinstance(v, float) else v) for k, v in tc.items()},
        "series": series,
        "wins": wins[-400:],
        "consts": {"P51": G.P51, "P5": G.P5, "H": [G.H[k] for k in range(6)], "N": G.N, "K": G.K, "NB": G.NB},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "web"))
    ap.add_argument("--full", action="store_true", help="rebuild the analysis even if today's is in place")
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    draws = G.load_draws()
    try:
        meta = json.load(open(G.META_FILE, encoding="utf-8"))
    except (OSError, ValueError):
        meta = {}
    st = state(draws, meta)
    with open(os.path.join(out, "state.json"), "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, separators=(",", ":"))
    tpl = open(TEMPLATE, encoding="utf-8").read()
    key = hashlib.sha1((tpl + open(G.__file__, encoding="utf-8").read() + open(__file__, encoding="utf-8").read())
                       .encode("utf-8")).hexdigest()[:12]
    day = draws[-1]["date"][:10]
    page = os.path.join(out, "index.html")
    if not a.full and os.path.exists(page):
        m = re.search(r'"stamp":"([^"]*)"', open(page, encoding="utf-8").read())
        if m and m.group(1) == day + "/" + key:
            print(f"state.json: №{st['last']['n']}; index.html is up to date ({day})", file=sys.stderr)
            return
    init = analysis(draws)
    init["stamp"] = day + "/" + key
    init["state"] = st
    html = tpl.replace("/*@INIT@*/", json.dumps(init, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c"))
    with open(page, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"index.html and state.json: №{st['last']['n']} ({len(html) // 1024} KB)", file=sys.stderr)


if __name__ == "__main__":
    main()
