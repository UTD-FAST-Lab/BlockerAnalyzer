#!/usr/bin/env python3
"""
select_representatives.py — pick ONE representative per
(decisive-shape × source-region) group from out/blocker_candidates.csv.

Decisive-only shape
-------------------
4-char string over the canonical fuzzer order (naive, cmplog, value_profile,
value_profile_cmplog). Each position is:

    R   fuzzer is a winner in >=1 decisive pair at this branch (n_resolved >= 8)
    B   fuzzer is a loser  in >=1 decisive pair at this branch (n_blocked  >= 8)
    -   fuzzer is NOT in any decisive pair at this branch
        (its trial counts are reference context, not part of the shape)

By construction the >=8/>=8 rule plus n=10 makes each decisive fuzzer
unambiguously R or B (>=8R AND >=8B would require n>=16).

Region
------
(file, function, line // bucket). Default bucket=50 — same as the legacy
distinct-region cap.

Representative pick
-------------------
Within each (shape, region) group, highest priority wins:
    max_prob_div DESC, max_dur_div DESC, max_hit_div DESC, branch_id ASC.

Outputs
-------
- csvs/blocker_representatives[_<targets>].csv  — one row per rep (full
  candidate row + shape, region_id, group_size).
- csvs/blocker_dedup_map[_<targets>].csv        — every input branch mapped
  to its rep: target, branch_id, rep_branch_id, shape, region_id,
  group_size, is_rep. Non-rep branches inherit the rep's template
  assignment after the agent fan-out completes (recovers the corroboration
  record at no agent cost).

Output naming: if --reps-output / --map-output aren't given, the suffix on
the input filename is mirrored. E.g. `blocker_candidates_curl.csv` →
`blocker_representatives_curl.csv` + `blocker_dedup_map_curl.csv`.
"""

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV_DIR   = REPO_ROOT / "csvs"
DEFAULT_INPUT     = DEFAULT_CSV_DIR / "blocker_candidates.csv"

CANONICAL_FUZZERS = ["naive", "cmplog", "value_profile", "value_profile_cmplog"]


def _suffix_from(input_path: Path) -> str:
    """Extract the '_<targets>' suffix from a blocker_candidates filename.
    blocker_candidates_curl.csv → '_curl'; blocker_candidates.csv → ''."""
    m = re.match(r"blocker_candidates(_.+)?\.csv$", input_path.name)
    return (m.group(1) or "") if m else ""


def decisive_shape(row, winner_thr=8, loser_thr=8):
    involved = set(json.loads(row["involved_fuzzers"]))
    chars = []
    for fz in CANONICAL_FUZZERS:
        if fz not in involved:
            chars.append("-")
            continue
        R = int(row[f"{fz}_resolved"] or 0)
        B = int(row[f"{fz}_blocked"]  or 0)
        if R >= winner_thr:
            chars.append("R")
        elif B >= loser_thr:
            chars.append("B")
        else:
            # Should not happen under the >=8/>=8 candidate rule at n=10.
            chars.append("?")
    return "".join(chars)


def region_tuple(row, bucket):
    return (row["file"], row["function"], int(row["line"]) // bucket)


def region_label(rg, bucket):
    f, fn, b = rg
    return f"{f}::{fn}::L{b * bucket}-{b * bucket + bucket - 1}"


def rep_priority(row):
    return (-float(row["max_prob_div"]),
            -float(row["max_dur_div"]),
            -float(row["max_hit_div"]),
            int(row["branch_id"]))


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", default=str(DEFAULT_INPUT),
                    help=f"per-branch candidate CSV (default {DEFAULT_INPUT})")
    ap.add_argument("--reps-output", default=None,
                    help="representatives CSV (default: csvs/blocker_representatives"
                         "<_targets>.csv, suffix mirrors --input)")
    ap.add_argument("--map-output", default=None,
                    help="dedup map CSV (default: csvs/blocker_dedup_map"
                         "<_targets>.csv, suffix mirrors --input)")
    ap.add_argument("--line-bucket", type=int, default=50,
                    help="lines per region bucket (default 50)")
    ap.add_argument("--winner-threshold", type=int, default=8)
    ap.add_argument("--loser-threshold",  type=int, default=8)
    args = ap.parse_args()

    in_path = Path(args.input)
    if not in_path.is_file():
        print(f"ERROR: input CSV not found: {in_path}", file=sys.stderr)
        sys.exit(1)
    suffix = _suffix_from(in_path)
    reps_out = Path(args.reps_output) if args.reps_output else (
        DEFAULT_CSV_DIR / f"blocker_representatives{suffix}.csv"
    )
    map_out = Path(args.map_output) if args.map_output else (
        DEFAULT_CSV_DIR / f"blocker_dedup_map{suffix}.csv"
    )

    with open(in_path) as f:
        rows = list(csv.DictReader(f))

    groups = {}
    shape_for = {}
    region_for = {}
    for r in rows:
        sh = decisive_shape(r, args.winner_threshold, args.loser_threshold)
        rg = region_tuple(r, args.line_bucket)
        shape_for[id(r)] = sh
        region_for[id(r)] = rg
        groups.setdefault((sh, rg), []).append(r)

    reps = {key: sorted(grp, key=rep_priority)[0] for key, grp in groups.items()}

    bad_shapes = sum(1 for sh in shape_for.values() if "?" in sh)
    if bad_shapes:
        print(f"WARNING: {bad_shapes} rows with '?' in shape (decisive fuzzer "
              f"satisfied neither >=8R nor >=8B — should not happen at n=10)",
              file=sys.stderr)

    rep_headers = list(rows[0].keys()) + ["shape", "region_id", "group_size"]
    reps_out.parent.mkdir(parents=True, exist_ok=True)
    with reps_out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rep_headers)
        w.writeheader()
        for key, rep in reps.items():
            sh, rg = key
            w.writerow({**rep,
                        "shape": sh,
                        "region_id": region_label(rg, args.line_bucket),
                        "group_size": len(groups[key])})

    map_headers = ["target", "branch_id", "rep_branch_id", "shape",
                   "region_id", "group_size", "is_rep"]
    map_out.parent.mkdir(parents=True, exist_ok=True)
    with map_out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=map_headers)
        w.writeheader()
        for key, grp in groups.items():
            sh, rg = key
            rep = reps[key]
            rep_id = int(rep["branch_id"])
            label = region_label(rg, args.line_bucket)
            for r in grp:
                bid = int(r["branch_id"])
                w.writerow({
                    "target": r["target"],
                    "branch_id": bid,
                    "rep_branch_id": rep_id,
                    "shape": sh,
                    "region_id": label,
                    "group_size": len(grp),
                    "is_rep": int(bid == rep_id),
                })

    n_rows = len(rows)
    n_groups = len(groups)
    print(f"input candidates                 : {n_rows}", file=sys.stderr)
    print(f"distinct (shape x region) groups : {n_groups}", file=sys.stderr)
    print(f"representatives                  : {n_groups}  "
          f"(reduction: {n_rows - n_groups}, {(n_rows-n_groups)/n_rows*100:.0f}%)",
          file=sys.stderr)

    per_target_orig = Counter(r["target"] for r in rows)
    per_target_reps = Counter(reps[k]["target"] for k in reps)
    print("\nper-target:", file=sys.stderr)
    for t in sorted(per_target_orig):
        print(f"  {t:<10}: {per_target_orig[t]:>3} -> {per_target_reps[t]:>3}  "
              f"(reduction {per_target_orig[t] - per_target_reps[t]:>3})",
              file=sys.stderr)

    sh_count = Counter(shape_for[id(r)] for r in rows)
    print(f"\ndistinct shapes: {len(sh_count)}", file=sys.stderr)
    print("top shapes (over input candidates):", file=sys.stderr)
    for sh, n in sh_count.most_common(10):
        print(f"  {sh}  (naive,cmp,vp,vpc): {n}", file=sys.stderr)

    sizes = Counter(len(g) for g in groups.values())
    print("\ngroup-size distribution:", file=sys.stderr)
    for sz in sorted(sizes):
        print(f"  size {sz:>2}: {sizes[sz]} groups", file=sys.stderr)

    print(f"\nwrote reps to {reps_out}", file=sys.stderr)
    print(f"wrote dedup map to {map_out}", file=sys.stderr)


if __name__ == "__main__":
    main()
