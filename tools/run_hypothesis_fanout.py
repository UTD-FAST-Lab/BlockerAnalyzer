#!/usr/bin/env python3
"""
run_hypothesis_fanout.py — prompt-prep + manifest builder for the
feature-hypothesis-generator fan-out (per-branch view).

Reads `out/blocker_representatives.csv` by default (one row per
(decisive-shape × source-region) representative; produced by
select_representatives.py from blocker_candidates.csv). Pass
`--input out/blocker_candidates.csv` to fan out across the full 275
candidate set instead of the deduped 158 reps. Non-rep branches stay
in `out/blocker_dedup_map.csv` as the implied-corroboration record;
they are NOT re-dispatched to the agent.

Generates one structured prompt per row via
`tools/study_units.py evidence-per-branch`, writes prompts under
`out/hypothesis_fanout/<group>/`, and emits manifest.json describing
the parallel/sequential dispatch plan.

This script does NOT invoke the agent — feature-hypothesis-generator
is a Claude Code subagent dispatched from a Claude session. The
manifest is the contract Claude reads to drive dispatch:
- across groups: parallel (one Agent call per group running concurrently)
- within group: sequential (each call sees prior templates on disk)

Grouping. By default, groups are `(target, primary_delta)` where
primary_delta is the delta of the highest-prob_div decisive pair on
the branch. Most branches have all decisive pairs under one delta, so
this is a clean partition. Use `--group-by target` to merge all deltas
for a target into one group (fewer parallel groups, longer sequential
chains).

Skipping. By default reads `templates/branch_index.json` and skips any
(target, branch_id) already covered by an existing template. Pass
`--skip-existing /dev/null` to disable.

Output layout:
  out/hypothesis_fanout/
  ├── manifest.json
  └── <group_id>/                       # e.g. lcms__I2S, bloaty__value_profile
      ├── 00_<target>_br<id>.prompt.md  # ordered by CSV ranking
      ├── 01_<target>_br<id>.prompt.md
      └── ...
"""

import argparse
import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "out" / "blocker_representatives.csv"
DEFAULT_OUTDIR = REPO_ROOT / "out" / "hypothesis_fanout"
DEFAULT_SKIP_INDEX = REPO_ROOT / "templates" / "branch_index.json"
STUDY_UNITS = REPO_ROOT / "tools" / "study_units.py"


def _rel_to_repo(p):
    try:
        return str(Path(p).relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


CANONICAL_FUZZERS = ["naive", "cmplog", "value_profile", "value_profile_cmplog"]


def primary_delta(decisive_pairs):
    """Delta of the pair with highest prob_div; ties broken alphabetically."""
    best = max(decisive_pairs, key=lambda p: (p.get("prob_div", 0), -ord(p["delta"][0])))
    return best["delta"]


def shape_from_row(row, winner_thr=7, loser_thr=7):
    """Decisive-only shape: fixed 4-char string over canonical fuzzers.

    Prefers the 'shape' column if present (from select_representatives.py
    output); otherwise computes from involved_fuzzers + per-fuzzer counts.
    """
    if row.get("shape"):
        return row["shape"]
    involved = set(json.loads(row["involved_fuzzers"]))
    chars = []
    for fz in CANONICAL_FUZZERS:
        if fz not in involved:
            chars.append("-")
            continue
        R = int(row.get(f"{fz}_resolved") or 0)
        B = int(row.get(f"{fz}_blocked")  or 0)
        if R >= winner_thr:
            chars.append("R")
        elif B >= loser_thr:
            chars.append("B")
        else:
            chars.append("?")
    return "".join(chars)


def group_key(row, group_by):
    if group_by == "shape":
        return (shape_from_row(row),)
    if group_by == "shape-target":
        return (shape_from_row(row), row["target"])
    if group_by == "target":
        return (row["target"],)
    if group_by == "target-delta":
        pairs = json.loads(row["decisive_pairs"])
        return (row["target"], primary_delta(pairs))
    raise ValueError(f"unknown group_by: {group_by}")


def group_id(key):
    return "__".join(key)


def load_skip_index(path):
    if path == Path("/dev/null") or not Path(path).is_file():
        return {}, []
    with open(path) as f:
        data = json.load(f)
    by_branch = {}
    for e in data.get("entries", []):
        if "target" not in e or "branch_id" not in e:
            continue
        by_branch[(e["target"], int(e["branch_id"]))] = e
    return by_branch, data.get("entries", [])


def gen_evidence_per_branch(target, branch_id, output_path, queue_base=None):
    cmd = [
        sys.executable, str(STUDY_UNITS), "evidence-per-branch",
        "--target", target,
        "--branch-id", str(branch_id),
        "--output", str(output_path),
    ]
    if queue_base:
        cmd.extend(["--queue-base", queue_base])
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return False, proc.stderr.strip() or proc.stdout.strip()
    return True, ""


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", default=str(DEFAULT_INPUT),
                    help=f"per-branch CSV — reps by default; pass "
                         f"out/blocker_candidates.csv to fan out across "
                         f"all 275 (default {DEFAULT_INPUT})")
    ap.add_argument("--outdir", default=str(DEFAULT_OUTDIR),
                    help=f"manifest + prompts root (default {DEFAULT_OUTDIR})")
    ap.add_argument("--group-by",
                    choices=["shape", "shape-target", "target", "target-delta"],
                    default="shape",
                    help="grouping key for the dispatch plan. Default 'shape': "
                         "branches with the same decisive shape go in one "
                         "sequential chain so later agents see prior templates "
                         "and can match-existing rather than re-create.")
    ap.add_argument("--skip-existing", default=str(DEFAULT_SKIP_INDEX),
                    help=f"branch index JSON for skip-already-covered "
                         f"(default {DEFAULT_SKIP_INDEX}; /dev/null to disable)")
    ap.add_argument("--queue-base", default=None,
                    help="override queue base passed to evidence-per-branch")
    ap.add_argument("--dry-run", action="store_true",
                    help="don't run evidence; just write manifest + skip plan")
    ap.add_argument("--force", action="store_true",
                    help="overwrite existing prompt files")
    args = ap.parse_args()

    in_path = Path(args.input)
    out_root = Path(args.outdir)
    skip_path = Path(args.skip_existing)

    if not in_path.is_file():
        print(f"ERROR: input CSV not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    out_root.mkdir(parents=True, exist_ok=True)

    skip_map, _ = load_skip_index(skip_path)
    if skip_map:
        print(f"loaded {len(skip_map)} skip entries from {skip_path}", file=sys.stderr)
    else:
        print(f"skip index empty or missing ({skip_path})", file=sys.stderr)

    with open(in_path) as f:
        rows = list(csv.DictReader(f))

    groups = {}
    for r in rows:
        key = group_key(r, args.group_by)
        groups.setdefault(key, []).append(r)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_csv": str(in_path),
        "skip_index": str(skip_path),
        "group_by": args.group_by,
        "dispatch_plan": {
            "across_groups": "parallel",
            "within_group": "sequential",
            "rationale": "across-group calls are independent (different "
                         "(target, delta) cells); within-group is sequential "
                         "so each agent sees prior templates on disk and can "
                         "match-existing rather than re-create.",
        },
        "groups": [],
        "skipped": [],
        "errors": [],
    }

    total_calls = 0
    total_skipped = 0

    for key in sorted(groups):
        gid = group_id(key)
        group_dir = out_root / gid
        group_dir.mkdir(parents=True, exist_ok=True)

        ordered_calls = []
        for r in groups[key]:
            target = r["target"]
            branch_id = int(r["branch_id"])
            skip = skip_map.get((target, branch_id))
            if skip:
                manifest["skipped"].append({
                    "target": target,
                    "branch_id": branch_id,
                    "group_id": gid,
                    "template_id": skip.get("template_id"),
                    "role": skip.get("role"),
                    "verdict_at_time": skip.get("verdict_at_time"),
                })
                total_skipped += 1
                continue

            order = len(ordered_calls)
            prompt_path = group_dir / f"{order:02d}_{target}_br{branch_id}.prompt.md"
            wrote = "skipped (exists)"
            if args.force or not prompt_path.is_file():
                if args.dry_run:
                    wrote = "dry-run (not generated)"
                else:
                    ok, err = gen_evidence_per_branch(
                        target, branch_id, prompt_path, args.queue_base)
                    if not ok:
                        manifest["errors"].append({
                            "target": target,
                            "branch_id": branch_id,
                            "group_id": gid,
                            "error": err,
                        })
                        print(f"  [error] {gid} br{branch_id}: {err}",
                              file=sys.stderr)
                        continue
                    wrote = "generated"

            decisive_pairs = json.loads(r["decisive_pairs"])
            involved_fuzzers = json.loads(r["involved_fuzzers"])
            ordered_calls.append({
                "order": order,
                "target": target,
                "branch_id": branch_id,
                "n_decisive_pairs": int(r["n_decisive_pairs"]),
                "primary_delta": primary_delta(decisive_pairs),
                "involved_fuzzers": involved_fuzzers,
                "decisive_pairs": decisive_pairs,
                "max_prob_div": float(r["max_prob_div"]),
                "max_dur_div": float(r["max_dur_div"]),
                "max_hit_div": float(r["max_hit_div"]),
                "file": r["file"],
                "function": r["function"],
                "line": int(r["line"]),
                "side": r["side"],
                "source_line": r["source_line"],
                "prompt_path": _rel_to_repo(prompt_path),
                "prompt_status": wrote,
            })
            total_calls += 1

        group_entry = {
            "id": gid,
            "n_calls": len(ordered_calls),
            "ordered_calls": ordered_calls,
        }
        if args.group_by == "shape":
            group_entry["shape"] = key[0]
        elif args.group_by == "shape-target":
            group_entry["shape"] = key[0]
            group_entry["target"] = key[1]
        elif args.group_by == "target":
            group_entry["target"] = key[0]
        elif args.group_by == "target-delta":
            group_entry["target"] = key[0]
            group_entry["primary_delta"] = key[1]
        manifest["groups"].append(group_entry)

    manifest["dispatch_plan"]["total_calls_planned"] = total_calls
    manifest["dispatch_plan"]["total_skipped"] = total_skipped
    manifest["dispatch_plan"]["max_parallel_groups"] = sum(
        1 for g in manifest["groups"] if g["n_calls"] > 0
    )

    manifest_path = out_root / "manifest.json"
    with manifest_path.open("w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nwrote manifest to {manifest_path}", file=sys.stderr)
    print(f"  total candidate rows: {len(rows)}", file=sys.stderr)
    print(f"  agent calls planned : {total_calls}", file=sys.stderr)
    print(f"  skipped (covered)   : {total_skipped}", file=sys.stderr)
    print(f"  errors              : {len(manifest['errors'])}", file=sys.stderr)
    print(f"  parallel groups     : {manifest['dispatch_plan']['max_parallel_groups']}",
          file=sys.stderr)
    if manifest["errors"]:
        print(f"\nerrors written to manifest.json under .errors", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
