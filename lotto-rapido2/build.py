#!/usr/bin/env python3
"""Builds the web page for «Рапидо 2.0»: index.html (analysis of the whole archive, rebuilt once a day or when the
page template changes) and state.json (the latest draws and the next draw's superprizes, rebuilt every time).

Usage: python lotto-rapido2/build.py --out rapido2      (after `python lotto-rapido2/rapido2.py update`)
"""
import argparse
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rapido2 as G  # noqa: E402

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
                 "sp": last["sp"], "price": last["ticket_price"], "columns": last["columns"]},
        "next": nxt,
        "rules": {"price": rules["price"], "ev_small": r4(rules["ev_small"]), "columns": rules["columns"],
                  "prizes": rules["prizes"], "slot_price": rules["slot_price"]},
        "times": [d["date"] for d in draws[-12:]],
        "count": len(draws),
    }


def clean(v):
    if isinstance(v, float):
        return r4(v)
    if isinstance(v, dict):
        return {k: clean(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [clean(x) for x in v]
    return v


def analysis(draws):
    r = G.patterns_report(draws)
    fc = G.forecast_models(draws)
    rc = G.repeat_choice(draws)
    crowd = G.Crowd(G.crowd_model(draws))
    main, small, _memory = G.values(draws)
    hist = G.jackpot_history(draws, main)
    tc = G.timing_check(draws, main)
    # what the superprize added to a ruble, best draw of each day over the whole history, for the chart
    days = {}
    for d, v in zip(draws, main):
        day = d["date"][:10]
        if v > days.get(day, (-1,))[0]:
            days[day] = (v, d["sp"], d["ticket_price"])
    series = [[k, r4(v[0]), v[1], v[2]] for k, v in sorted(days.items())]
    nb = G.number_bias(draws)
    scores = G.number_scores(nb, crowd)
    return {
        "first": {"n": draws[0]["number"], "date": draws[0]["date"]},
        "patterns": clean(r),
        "forecasts": {k: r4(fc[k]["score"]) for k, _n in G.FORECASTS},
        "passed": fc["passed"],
        "bonus_p": clean(fc["bonus"]["p"]),
        "repeat": clean(rc),
        "bias": clean(nb),
        "scores": clean(scores),
        "crowd": {"q": clean(crowd.q), "norm": crowd.norm},
        "hist": clean(hist),
        "timing": clean(tc),
        "series": series,
        "consts": {"P": G.P_SUPER, "TOTAL": G.TOTAL, "H": [G.H[k] for k in range(G.K + 1)], "N": G.N, "K": G.K, "NB": G.NB},
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
