#!/usr/bin/env python3
"""value_distance_reached — the vp-gradient evidence tool (2026-06-12).

The most-requested new descriptor from the step5b_new_v3 design fleet (16
hypotheses). Tests the CMP_MAP-gradient mechanism: value_profile (or vpc) climbs
a Hamming gradient toward a gate's target operand, so the WINNER's seed set lands
a value CLOSE to the target while the LOSER's (cmplog / naive) stalls farther
away — the signature the structural size/token proxy (joint_necessity) is blind
to.

descriptor: seed_set:value_distance_reached:<operand>:per_branch
This is G2-independent (it reads what each arm's seeds REACHED, not who resolved)
and discriminating (G1): a pure I2S-substitution alternative predicts the loser
(cmplog, which HAS I2S) lands distance ~0 too; the approach-but-miss gap is the
gradient's unique contribution.

Per seed: min over sliding windows of Hamming(window, target)/width  -> residual
distance in [0,1] (0 = the literal is present / exactly reached). Per arm: the
MINIMUM residual across the arm's seeds (the closest any seed got). Emits one
`<arm>_min_distance` per requested fuzzer (named vp/vpc/cmp/naive to match the
agents' rules) plus distance_gap and distance_closure_ratio.

  distance_gap            = closest_loser_min - winner_min   (>0 => winner closer)
  distance_closure_ratio  = (closest_loser_min - winner_min) / max(closest_loser_min, eps)

Numeric/threshold gates (inequality) use --numeric: distance = |value - target|
magnitude gap over the operand-width integer window (min over windows), then the
same metrics. Short operands (width<=2) are chance-alignment prone — flagged.

Usage:
  python3 bench/tools/value_distance_reached.py branch --target sqlite3 --branch-id 14437 \
      --value '<<' --winners value_profile_cmplog --losers cmplog,naive
  python3 bench/tools/value_distance_reached.py branch --target lcms --branch-id 2446 \
      --value 0xFFFF --width 4 --numeric --winners value_profile --losers cmplog,naive
"""
import argparse
import json
import random
import sqlite3
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "db" / "blockers.sqlite"
QUEUE = ROOT / "out"
EPS = 1e-6
ARM = {"value_profile": "vp", "value_profile_cmplog": "vpc",
       "cmplog": "cmp", "naive": "naive"}


def read_seed(target, fz, trial, sid, cap):
    p = QUEUE / target / fz / f"trial{trial}" / "queue" / sid
    try:
        return p.read_bytes()[:cap]
    except OSError:
        return None


def arm_seeds(con, branch_id, fuzzer, target, cap, maxn=200):
    rows = []
    for table in ("resolving_seeds", "blocking_seeds"):
        rows += con.execute(
            f"select trial, seed_id from {table} where branch_id=? and fuzzer=?",
            (branch_id, fuzzer)).fetchall()
    random.shuffle(rows)
    out = []
    for tr, sid in rows:  # read until maxn SUCCESSFUL reads (stale files don't shrink the sample)
        b = read_seed(target, fuzzer, tr, sid, cap)
        if b is not None:
            out.append(b)
            if len(out) >= maxn:
                break
    return out


def parse_value(s, width_arg):
    """Return (bytes target, width). Accepts hex (0x..) or a literal string."""
    s = s.strip()
    if s.lower().startswith("0x") and len(s) > 2:
        h = s[2:]
        if len(h) % 2:
            h = "0" + h
        try:
            b = bytes.fromhex(h)
            return b, (width_arg or len(b))
        except ValueError:
            pass  # '0x...' that isn't valid hex -> treat as literal text
    b = s.encode("latin-1", "replace")
    return b, (width_arg or len(b))


def min_residual_hamming(seed, target):
    w = len(target)
    if len(seed) < w:
        return 1.0
    best = w
    for i in range(len(seed) - w + 1):
        d = 0
        for j in range(w):
            if seed[i + j] != target[j]:
                d += 1
                if d >= best:
                    break
        if d < best:
            best = d
            if best == 0:
                break
    return best / w


def min_residual_numeric(seed, target_int, width):
    if len(seed) < width:
        return 1.0
    best = None
    for i in range(len(seed) - width + 1):
        v = int.from_bytes(seed[i:i + width], "big")
        gap = abs(v - target_int)
        if best is None or gap < best:
            best = gap
    span = max(target_int, 1)
    return min(best / span, 1.0)


def arm_distance(seeds, target, numeric, width):
    if not seeds:
        return None
    if numeric:
        ti = int.from_bytes(target, "big")
        res = [min_residual_numeric(s, ti, width) for s in seeds]
    else:
        res = [min_residual_hamming(s, target) for s in seeds]
    return {"n": len(seeds), "min": round(min(res), 4),
            "median": round(statistics.median(res), 4)}


def analyze(target, branch_id, value, width, winners, losers, numeric, cap=8192):
    tb, w = parse_value(value, width)
    if not numeric:
        w = len(tb)  # Hamming window is the literal width; --width applies to numeric mode only
    con = sqlite3.connect(DB)
    out = {"target": target, "branch_id": branch_id, "operand": value,
           "width": w, "numeric": numeric}
    dists = {}
    for fz in (*winners, *losers):
        d = arm_distance(arm_seeds(con, branch_id, fz, target, cap), tb, numeric, w)
        if d is None:
            continue
        dists[fz] = d
        out[f"{ARM.get(fz, fz)}_min_distance"] = d["min"]
        out[f"{ARM.get(fz, fz)}_median_distance"] = d["median"]
        out[f"{ARM.get(fz, fz)}_n"] = d["n"]
    con.close()
    w_arms = [f for f in winners if f in dists]
    l_arms = [f for f in losers if f in dists]
    if not w_arms or not l_arms:
        out["skip"] = (f"missing arm seeds (winners={[f for f in winners if f in dists]} "
                       f"losers={[f for f in losers if f in dists]})")
        return out
    winner_min = min(dists[f]["min"] for f in w_arms)
    closest_loser_min = min(dists[f]["min"] for f in l_arms)
    out["distance_gap"] = round(closest_loser_min - winner_min, 4)
    out["distance_closure_ratio"] = round(
        (closest_loser_min - winner_min) / max(closest_loser_min, EPS), 4)
    out["winner_closer"] = winner_min < closest_loser_min
    if w <= 2:
        out["caveat"] = "short operand (width<=2): chance-alignment prone"
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("branch", "study"):
        p = sub.add_parser(name)
        p.add_argument("--value", required=(name == "branch"),
                       help="target operand: hex (0x..) or literal string")
        p.add_argument("--width", type=int, default=None)
        p.add_argument("--winners", default="value_profile,value_profile_cmplog")
        p.add_argument("--losers", default="cmplog,naive")
        p.add_argument("--numeric", action="store_true",
                       help="inequality/threshold gate: magnitude gap not Hamming")
        if name == "branch":
            p.add_argument("--target", required=True)
            p.add_argument("--branch-id", type=int, required=True)
        else:
            p.add_argument("--branches-csv", required=True,
                           help="CSV columns: target,branch_id,value[,width][,numeric][,winners][,losers]")
            p.add_argument("--out", required=True)
    args = ap.parse_args()
    random.seed(13)

    if args.cmd == "branch":
        res = analyze(args.target, args.branch_id, args.value, args.width,
                      args.winners.split(","), args.losers.split(","), args.numeric)
        print(json.dumps(res, indent=1))
        return

    import csv
    rows = []
    with open(args.branches_csv) as fh:
        for r in csv.DictReader(fh):
            nflag = (r.get("numeric") or "").strip().lower() in ("1", "true", "yes", "y")
            res = analyze(r["target"].strip(), int(r["branch_id"]), r["value"],
                          int(r["width"]) if r.get("width") else None,
                          (r.get("winners") or args.winners).split(","),
                          (r.get("losers") or args.losers).split(","),
                          nflag)
            rows.append(res)
            tag = res.get("skip") or (f"gap={res.get('distance_gap')} "
                  f"closer={res.get('winner_closer')}")
            print(f"  {res['target']}/{res['branch_id']}: {tag}", flush=True)
    keys = sorted({k for r in rows for k in r})
    with open(args.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
