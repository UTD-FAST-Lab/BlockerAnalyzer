#!/usr/bin/env python3
"""rank_decomposition.py — test whether a fuzzer's per-CATEGORY resolve fingerprint
(learned cross-target) explains its per-TARGET ranking.

Non-circular: leave-one-target-out (LOTO). For target t,
    predicted[t,f] = Σ_c  share[t,c] · rate_{-t}[f,c]
where rate_{-t}[f,c] = fuzzer f's resolve-rate on category c over ALL targets except t.
Compare predicted vs actual per-target fuzzer ranking (Spearman + exact-match +
libafl-last + top-1).  Also dumps the full target×fuzzer×category cube to CSV.
"""
import json, csv, collections, argparse
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FUZZERS = ["aflplusplus", "honggfuzz", "libfuzzer", "libafl"]
TAU = 0.8
ap = argparse.ArgumentParser()
ap.add_argument("--resolve", default=str(ROOT / "csvs/rq3_resolve.csv"))
ap.add_argument("--cube-out", default=str(ROOT / "csvs/rq3_cube.csv"))
A = ap.parse_args()

lab, tgt = {}, {}
for l in open(ROOT / "bench/dataset.jsonl"):
    r = json.loads(l)
    if r.get("evidence", {}).get("status") != "validated":
        continue
    k = (r["target"], r["branch_id"])
    lab[k] = r["mechanism"].get("canonical_label") or r["mechanism"].get("label")
    tgt[k] = r["target"]

rows = collections.defaultdict(dict)
for r in csv.DictReader(open(A.resolve)):
    k = (r["target"], int(r["branch_id"]))
    rows[k][r["fuzzer"]] = (int(r["n_resolved"]), int(r["n_blocked"]), int(r["n_reached"]))

def resolved(k, f):
    if k not in rows or f not in rows[k]:
        return None
    nr, nb, nrch = rows[k][f]
    if nrch == 0:
        return None
    return 1.0 if (nr / (nr + nb) if nr + nb > 0 else 0) >= TAU else 0.0

# branches that have data for every fuzzer
KEYS = [k for k in lab if all(resolved(k, f) is not None for f in FUZZERS)]
TARGETS = sorted({tgt[k] for k in KEYS})
CATS = sorted({lab[k] for k in KEYS})

# ----- cube[t][f][c] = (n_resolved, n_branches) -----
cube = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0])))
for k in KEYS:
    t, c = tgt[k], lab[k]
    for f in FUZZERS:
        cube[t][f][c][0] += int(resolved(k, f))
        cube[t][f][c][1] += 1

with open(A.cube_out, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["target", "fuzzer", "category", "n_resolved", "n_branches", "rate"])
    for t in TARGETS:
        for f in FUZZERS:
            for c in CATS:
                nr, nb = cube[t][f][c]
                if nb:
                    w.writerow([t, f, c, nr, nb, f"{nr/nb:.4f}"])
print(f"wrote cube -> {A.cube_out}")

# ----- LOTO prediction -----
def loto_rate(f, c, exclude_t):
    nr = sum(cube[t][f][c][0] for t in TARGETS if t != exclude_t)
    nb = sum(cube[t][f][c][1] for t in TARGETS if t != exclude_t)
    return (nr / nb) if nb else None

def actual_rate(t, f):
    nr = sum(cube[t][f][c][0] for c in CATS)
    nb = sum(cube[t][f][c][1] for c in CATS)
    return nr / nb if nb else float("nan")

def spearman(a, b):
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    ra = ra - ra.mean(); rb = rb - rb.mean()
    d = np.sqrt((ra**2).sum() * (rb**2).sum())
    return float((ra*rb).sum()/d) if d else 0.0

print(f"\n{'target':12} {'actual rank':40} {'LOTO-predicted rank':40} {'rho':>5} match")
sp, exact, libafl_last_ok, top1_ok = [], 0, 0, 0
for t in TARGETS:
    comp = collections.Counter()
    for c in CATS:
        comp[c] += cube[t][FUZZERS[0]][c][1]
    n = sum(comp.values())
    act = {f: actual_rate(t, f) for f in FUZZERS}
    pred = {}
    for f in FUZZERS:
        s = 0.0; wsum = 0.0
        for c in CATS:
            if comp[c] == 0:
                continue
            r = loto_rate(f, c, t)
            if r is None:
                continue
            w = comp[c] / n
            s += w * r; wsum += w
        pred[f] = s / wsum if wsum else float("nan")
    av = np.array([act[f] for f in FUZZERS]); pv = np.array([pred[f] for f in FUZZERS])
    rho = spearman(av, pv); sp.append(rho)
    ra = [f for f, _ in sorted(act.items(), key=lambda x: -x[1])]
    rp = [f for f, _ in sorted(pred.items(), key=lambda x: -x[1])]
    exact += (ra == rp)
    libafl_last_ok += (ra[-1] == "libafl" == rp[-1])
    top1_ok += (ra[0] == rp[0])
    print(f"{t:12} {' > '.join(s[:4] for s in ra):40} {' > '.join(s[:4] for s in rp):40} {rho:>5.2f} {'EXACT' if ra==rp else ''}")

nt = len(TARGETS)
print(f"\nmean Spearman rho = {np.mean(sp):.2f}   exact-rank match {exact}/{nt}   "
      f"top-1 correct {top1_ok}/{nt}   libafl-correctly-last {libafl_last_ok}/{nt}")
print(f"(branches with full 4-fuzzer data: {len(KEYS)}; targets {nt}; categories {len(CATS)})")
