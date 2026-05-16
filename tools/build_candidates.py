#!/usr/bin/env python3
"""
build_candidates.py — per-branch candidate aggregation.

For each (target, branch_id), collapses the up-to-4 canonical pair-edges
into ONE row containing every pair that satisfies the >=7/>=7 rule, plus
the per-fuzzer trial profile assembled by cross-subject join on
`subject_branches`.

Decisive-pair rule (per pair):
    winner_resolved >= --winner-threshold (default 7) AND
    loser_blocked   >= --loser-threshold  (default 7)

A branch is emitted iff it has >=1 decisive pair (under --admissible-only,
that pair's subject must also be admissible).

Output columns
--------------
    target, branch_id,
    file, function, line, col, side, source_line,
    n_decisive_pairs,
    decisive_pairs   -- JSON array; one element per pair:
                        {A, B, delta, direction, winner, loser,
                         winner_resolved, loser_blocked,
                         prob_div, dur_div, hit_div}
    involved_fuzzers -- JSON array; union of fuzzers across decisive pairs.
                        This is the set the synthetic experiment will run.
    <fuzzer>_resolved/_blocked/_unreached for each canonical fuzzer
        (naive, cmplog, value_profile, value_profile_cmplog).
        Sourced via cross-subject join on subject_branches: a fuzzer's
        counts at this branch come from any canonical subject involving
        that fuzzer that ADMITTED the branch. Reference fuzzers (no
        admitting subject involving them) are blank — represented as '-'
        in the decisive shape.
    max_prob_div, max_dur_div, max_hit_div  -- magnitudes across decisive
                                                pairs (abs).

Default output: csvs/blocker_candidates[_<targets>].csv.
"""

import argparse
import csv
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = REPO_ROOT / "db" / "blockers.sqlite"
DEFAULT_CSV_DIR = REPO_ROOT / "csvs"

CANONICAL_FUZZERS = ["naive", "cmplog", "value_profile", "value_profile_cmplog"]


def _default_output(targets):
    """csvs/blocker_candidates[_<targets>].csv."""
    if targets:
        suffix = "_" + "-".join(targets)
    else:
        suffix = ""
    return DEFAULT_CSV_DIR / f"blocker_candidates{suffix}.csv"


def _build_headers():
    base = [
        "target", "branch_id",
        "file", "function", "line", "col", "side", "source_line",
        "n_decisive_pairs", "decisive_pairs", "involved_fuzzers",
    ]
    counts = []
    for fz in CANONICAL_FUZZERS:
        counts += [f"{fz}_resolved", f"{fz}_blocked", f"{fz}_unreached"]
    tail = ["max_prob_div", "max_dur_div", "max_hit_div"]
    return base + counts + tail


HEADERS = _build_headers()


def fetch_decisive_pairs(conn, loser_thr, winner_thr, admissible_only, targets=None):
    """One row per (target, branch_id, decisive canonical pair)."""
    clauses = []
    params = [winner_thr, loser_thr] * 4
    if admissible_only:
        clauses.append("s.admissible = 1")
    if targets:
        placeholders = ",".join("?" * len(targets))
        clauses.append(f"s.target IN ({placeholders})")
        params.extend(targets)
    extra = (" AND " + " AND ".join(clauses)) if clauses else ""
    sql = f"""
        SELECT s.target, sb.branch_id,
               s.A, s.B, s.delta_technique AS delta,
               CASE
                 WHEN sb.n_A_resolved >= ? AND sb.n_B_blocked >= ? THEN 'A>B'
                 WHEN sb.n_B_resolved >= ? AND sb.n_A_blocked >= ? THEN 'B>A'
               END AS direction,
               sb.n_A_resolved, sb.n_A_blocked,
               sb.n_B_resolved, sb.n_B_blocked,
               sb.prob_div, sb.dur_div, sb.hit_div
        FROM subject_branches sb
        JOIN study_subjects s USING (subject_id)
        WHERE ((sb.n_A_resolved >= ? AND sb.n_B_blocked >= ?)
            OR (sb.n_B_resolved >= ? AND sb.n_A_blocked >= ?))
              {extra}
    """
    return [dict(r) for r in conn.execute(sql, params).fetchall()]


def fetch_fuzzer_counts(conn, targets=None):
    """(target, branch_id, fuzzer) -> {n_resolved, n_blocked, n_unreached}.

    Assembled by cross-subject join on subject_branches. Each canonical
    fuzzer appears in 2 of the 4 canonical subjects; whichever ones admitted
    the branch contribute counts. Counts for a (branch, fuzzer) tuple are
    deterministic (same fuzzer at same branch has the same trial outcomes
    regardless of which pair admitted) — UNION DISTINCT collapses duplicates.
    Reference fuzzers (no admitting subject involving them) are absent.
    """
    target_filter = ""
    params = []
    if targets:
        placeholders = ",".join("?" * len(targets))
        target_filter = f" WHERE b.target IN ({placeholders})"
        params = list(targets) + list(targets)  # used in both UNION halves
    sql = f"""
        SELECT b.target, sb.branch_id, s.A AS fuzzer,
               sb.n_A_resolved AS n_resolved,
               sb.n_A_blocked  AS n_blocked,
               sb.n_A_unreached AS n_unreached
          FROM subject_branches sb
          JOIN study_subjects s USING (subject_id)
          JOIN branches b ON b.branch_id = sb.branch_id
        {target_filter}
        UNION
        SELECT b.target, sb.branch_id, s.B AS fuzzer,
               sb.n_B_resolved, sb.n_B_blocked, sb.n_B_unreached
          FROM subject_branches sb
          JOIN study_subjects s USING (subject_id)
          JOIN branches b ON b.branch_id = sb.branch_id
        {target_filter}
    """
    out = {}
    for r in conn.execute(sql, params).fetchall():
        out[(r["target"], r["branch_id"], r["fuzzer"])] = {
            "n_resolved": r["n_resolved"],
            "n_blocked":  r["n_blocked"],
            "n_unreached": r["n_unreached"],
        }
    return out


def fetch_branch_meta(conn, targets=None):
    where = ""
    params = []
    if targets:
        placeholders = ",".join("?" * len(targets))
        where = f" WHERE target IN ({placeholders})"
        params = list(targets)
    sql = f"""
        SELECT branch_id, target, file, function, line, col,
               blocked_side AS side, source_line
        FROM branches{where}
    """
    return {r["branch_id"]: dict(r) for r in conn.execute(sql, params).fetchall()}


def _abs_or_zero(x):
    return round(abs(x), 4) if x is not None else 0.0


def aggregate(decisive_rows, fuzzer_counts, branch_meta):
    by_branch = {}
    for d in decisive_rows:
        key = (d["target"], d["branch_id"])
        if d["direction"] == "A>B":
            winner, loser = d["A"], d["B"]
            w_res, l_blk = d["n_A_resolved"], d["n_B_blocked"]
        else:
            winner, loser = d["B"], d["A"]
            w_res, l_blk = d["n_B_resolved"], d["n_A_blocked"]
        pair = {
            "A": d["A"], "B": d["B"],
            "delta": d["delta"], "direction": d["direction"],
            "winner": winner, "loser": loser,
            "winner_resolved": w_res, "loser_blocked": l_blk,
            "prob_div": _abs_or_zero(d["prob_div"]),
            "dur_div":  round(abs(d["dur_div"] or 0), 2),
            "hit_div":  round(abs(d["hit_div"] or 0), 1),
        }
        by_branch.setdefault(key, []).append(pair)

    rows = []
    for (target, branch_id), pairs in by_branch.items():
        meta = branch_meta.get(branch_id, {})
        involved = sorted({fz for p in pairs for fz in (p["winner"], p["loser"])})
        row = {
            "target": target,
            "branch_id": branch_id,
            "file": meta.get("file"),
            "function": meta.get("function"),
            "line": meta.get("line"),
            "col": meta.get("col"),
            "side": meta.get("side"),
            "source_line": meta.get("source_line"),
            "n_decisive_pairs": len(pairs),
            "decisive_pairs": json.dumps(pairs, separators=(",", ":")),
            "involved_fuzzers": json.dumps(involved),
            "max_prob_div": max(p["prob_div"] for p in pairs),
            "max_dur_div":  max(p["dur_div"]  for p in pairs),
            "max_hit_div":  max(p["hit_div"]  for p in pairs),
        }
        for fz in CANONICAL_FUZZERS:
            c = fuzzer_counts.get((target, branch_id, fz))
            row[f"{fz}_resolved"]  = c["n_resolved"]   if c else None
            row[f"{fz}_blocked"]   = c["n_blocked"]    if c else None
            row[f"{fz}_unreached"] = c["n_unreached"]  if c else None
        rows.append(row)

    rows.sort(key=lambda r: (r["target"], -r["n_decisive_pairs"],
                             -r["max_prob_div"], r["branch_id"]))
    return rows


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=str(DEFAULT_DB),
                    help=f"SQLite path (default {DEFAULT_DB})")
    ap.add_argument("--targets", nargs="+",
                    help="restrict to these targets (default: all in DB)")
    ap.add_argument("--output", default=None,
                    help="output CSV path or - for stdout "
                         "(default: csvs/blocker_candidates[_<targets>].csv)")
    ap.add_argument("--admissible-only", action="store_true", default=True,
                    help="restrict to admissible subjects (default ON)")
    ap.add_argument("--no-admissible-only", action="store_false",
                    dest="admissible_only",
                    help="include all subjects regardless of admissibility")
    ap.add_argument("--loser-threshold", type=int, default=7,
                    help="loser must have n_blocked >= THIS (default 7)")
    ap.add_argument("--winner-threshold", type=int, default=7,
                    help="winner must have n_resolved >= THIS (default 7)")
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row

    decisive = fetch_decisive_pairs(conn, args.loser_threshold,
                                    args.winner_threshold,
                                    args.admissible_only,
                                    args.targets)
    counts   = fetch_fuzzer_counts(conn, args.targets)
    meta     = fetch_branch_meta(conn, args.targets)
    conn.close()

    rows = aggregate(decisive, counts, meta)

    output = args.output if args.output is not None else str(_default_output(args.targets))
    if output == "-":
        w = csv.DictWriter(sys.stdout, fieldnames=HEADERS)
        w.writeheader(); w.writerows(rows)
    else:
        out = Path(output)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=HEADERS)
            w.writeheader(); w.writerows(rows)
        print(f"wrote {len(rows)} rows to {out}", file=sys.stderr)

    per_target = Counter(r["target"] for r in rows)
    multi_pair = Counter(r["target"] for r in rows if r["n_decisive_pairs"] >= 2)
    print(f"  total branches             : {len(rows)}", file=sys.stderr)
    for t in sorted(per_target):
        print(f"  {t:<10} branches: {per_target[t]:>4}  "
              f"(>=2 decisive pairs: {multi_pair[t]})",
              file=sys.stderr)


if __name__ == "__main__":
    main()
