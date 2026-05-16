#!/usr/bin/env python3
"""
lint_template_shapes.py — verify the agent's per-rep template assignments
are consistent with the decisive-shape × source-region equivalence rule.

Two checks
----------
1. Intra-template: reps assigned to the SAME template should share a
   single decisive shape. >=2 distinct shapes per template hints at
   overlumping (the agent may have grouped two distinct mechanisms).

2. Cross-template: a given decisive shape should NOT span >=2 templates.
   A split shape hints at a missed merge — the agent may have created a
   redundant template for the same fuzzer-divergence pattern.

Inputs
------
- templates/branch_index.json    (agent's (target, branch_id) -> template_id)
- out/blocker_representatives.csv (rep -> shape, region_id, group_size)
- out/blocker_dedup_map.csv      (rep -> implied member count, optional)

Output: stdout report (or --output FILE) with WARN lines for review.

Exit codes: 0=clean, 1=intra-only warnings, 2=cross-template warnings.
"""

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INDEX = REPO_ROOT / "templates" / "branch_index.json"
DEFAULT_REPS  = REPO_ROOT / "out" / "blocker_representatives.csv"
DEFAULT_MAP   = REPO_ROOT / "out" / "blocker_dedup_map.csv"


def load_index(path):
    if not path.is_file():
        return {}
    with open(path) as f:
        data = json.load(f)
    out = {}
    for e in data.get("entries", []):
        if "target" in e and "branch_id" in e and "template_id" in e:
            out[(e["target"], int(e["branch_id"]))] = {
                "template_id": e["template_id"],
                "role": e.get("role", ""),
                "verdict": e.get("verdict_at_time", ""),
            }
    return out


def load_reps(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def load_implied_counts(path):
    """Returns (target, rep_branch_id) -> count of implied members in dedup group."""
    if not path.is_file():
        return {}
    with open(path) as f:
        rows = list(csv.DictReader(f))
    out = Counter()
    for r in rows:
        out[(r["target"], int(r["rep_branch_id"]))] += 1
    return out


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--index", default=str(DEFAULT_INDEX),
                    help=f"branch_index.json (default {DEFAULT_INDEX})")
    ap.add_argument("--reps", default=str(DEFAULT_REPS),
                    help=f"reps CSV (default {DEFAULT_REPS})")
    ap.add_argument("--map", default=str(DEFAULT_MAP),
                    help=f"dedup map CSV (default {DEFAULT_MAP})")
    ap.add_argument("--output", default="-",
                    help="output path or - for stdout")
    ap.add_argument("--include-legacy", action="store_true",
                    help="include templates under legacy/ (default: skip)")
    ap.add_argument("--show-clean", action="store_true",
                    help="list all templates including ones with no warnings")
    args = ap.parse_args()

    index = load_index(Path(args.index))
    reps  = load_reps(Path(args.reps))
    implied = load_implied_counts(Path(args.map))

    if not args.include_legacy:
        index = {k: v for k, v in index.items()
                 if not v["template_id"].startswith("legacy/")}

    template_to_reps = defaultdict(list)
    rep_to_template = {}
    pending_reps = []
    for r in reps:
        key = (r["target"], int(r["branch_id"]))
        if key in index:
            tid = index[key]["template_id"]
            template_to_reps[tid].append(r)
            rep_to_template[key] = tid
        else:
            pending_reps.append(r)

    intra_warnings = []
    for tid, rep_list in template_to_reps.items():
        shapes = Counter(r["shape"] for r in rep_list)
        if len(shapes) >= 2:
            intra_warnings.append((tid, shapes, rep_list))

    shape_to_templates = defaultdict(lambda: defaultdict(list))
    for tid, rep_list in template_to_reps.items():
        for r in rep_list:
            shape_to_templates[r["shape"]][tid].append(r)
    cross_warnings = []
    for shape, tmap in shape_to_templates.items():
        if len(tmap) >= 2:
            cross_warnings.append((shape, dict(tmap)))

    out = []
    out.append("==== TEMPLATE-SHAPE LINT REPORT ====")
    out.append(f"reps total                    : {len(reps)}")
    out.append(f"reps assigned to a template   : {len(rep_to_template)}")
    out.append(f"reps pending (no verdict yet) : {len(pending_reps)}")
    out.append(f"templates active              : {len(template_to_reps)}")
    out.append(f"intra-template warnings (mixed shapes per template): {len(intra_warnings)}")
    out.append(f"cross-template warnings (shape spans >=2 templates): {len(cross_warnings)}")
    out.append("")

    if intra_warnings:
        out.append("---- INTRA-TEMPLATE WARNINGS ----")
        for tid, shapes, rep_list in sorted(intra_warnings, key=lambda x: -len(x[2])):
            out.append(f"\n[INTRA] template {tid}: {len(rep_list)} reps, "
                       f"{len(shapes)} distinct shapes")
            by_shape = defaultdict(list)
            for r in rep_list:
                by_shape[r["shape"]].append(r)
            for sh in sorted(by_shape, key=lambda s: -len(by_shape[s])):
                rs = by_shape[sh]
                out.append(f"  shape {sh} ({len(rs)} reps):")
                for r in rs[:5]:
                    impl = implied.get((r["target"], int(r["branch_id"])), 1)
                    out.append(f"    {r['target']:<10} br{r['branch_id']:<5} "
                               f"{r['file']}:{r['line']}  "
                               f"group={r['group_size']} implied={impl}")
                if len(rs) > 5:
                    out.append(f"    ... +{len(rs)-5} more")
        out.append("")

    if cross_warnings:
        out.append("---- CROSS-TEMPLATE WARNINGS ----")
        for shape, tmap in sorted(cross_warnings, key=lambda x: -sum(len(v) for v in x[1].values())):
            total = sum(len(v) for v in tmap.values())
            out.append(f"\n[CROSS] shape {shape}: {total} reps split across "
                       f"{len(tmap)} templates")
            for tid in sorted(tmap, key=lambda t: -len(tmap[t])):
                rs = tmap[tid]
                out.append(f"  -> {tid}: {len(rs)} reps")
                for r in rs[:3]:
                    out.append(f"     {r['target']:<10} br{r['branch_id']:<5} "
                               f"{r['file']}:{r['line']}")
                if len(rs) > 3:
                    out.append(f"     ... +{len(rs)-3} more")
        out.append("")

    if args.show_clean or not (intra_warnings or cross_warnings):
        out.append("---- TEMPLATE SHAPE SUMMARY ----")
        for tid in sorted(template_to_reps):
            rep_list = template_to_reps[tid]
            shapes = Counter(r["shape"] for r in rep_list)
            shape_str = ", ".join(f"{sh}×{n}" for sh, n in shapes.most_common())
            impl_total = sum(implied.get((r["target"], int(r["branch_id"])), 1)
                             for r in rep_list)
            tag = " [WARN]" if len(shapes) >= 2 else ""
            out.append(f"  {tid:<42} reps={len(rep_list):>3}  "
                       f"implied={impl_total:>3}  shapes=[{shape_str}]{tag}")

    text = "\n".join(out)
    if args.output == "-":
        sys.stdout.write(text + "\n")
    else:
        Path(args.output).write_text(text)
        print(f"wrote lint report to {args.output} ({len(text)} chars)",
              file=sys.stderr)

    if cross_warnings:
        sys.exit(2)
    if intra_warnings:
        sys.exit(1)


if __name__ == "__main__":
    main()
