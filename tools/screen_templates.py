#!/usr/bin/env python3
"""
screen_templates.py — fast SCREENING sweep across all step5b/<id>/ templates.

Per the host constraint (only ~2-4 free cores), this runs a cheap screening
config: 1 trial, short duration, the DECISIVE PAIR only (winner+loser from
params.json:expected_direction), and 3 scan points (low/mid/high). Each
template's cells run --jobs N in parallel; templates run sequentially. The honest
5x600 config stays in params.json — screening only overrides at the CLI.

1-trial `reproduced` is PROVISIONAL (judge()'s per-trial-strict check is trivial
at n=1) — confirm clear reproductions with more trials before promoting, and send
non-reproduced to the verdict-adjudicator.

Writes step5b/screen_summary.json + prints a running board.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STEP5B = REPO_ROOT / "step5b"


def pick_scans(scan_values):
    svs = [str(v) for v in scan_values]
    if len(svs) <= 3:
        return svs
    return [svs[0], svs[len(svs) // 2], svs[-1]]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--trials", type=int, default=1)
    ap.add_argument("--duration-s", type=int, default=60)
    ap.add_argument("--only", default=None, help="comma list of feature_ids to run")
    ap.add_argument("--out", default="step5b/screen_summary.json")
    args = ap.parse_args()

    only = set(args.only.split(",")) if args.only else None
    dirs = sorted(d for d in STEP5B.iterdir()
                  if d.is_dir() and d.name != "briefs"
                  and (d / "params.json").is_file())
    if only:
        dirs = [d for d in dirs if d.name in only]

    board = []
    for d in dirs:
        fid = d.name
        params = json.loads((d / "params.json").read_text())
        m = re.match(r"\s*(\S+)\s*>\s*(\S+)\s*$", params.get("expected_direction", ""))
        if not m:
            board.append({"feature_id": fid, "verdict": "SKIP_no_direction"})
            print(f"SKIP  {fid}: no parseable expected_direction", flush=True)
            continue
        winner, loser = m.group(1), m.group(2)
        # optional per-template "screen" override block in params.json
        sc = params.get("screen", {})
        fuzzers = sc.get("fuzzers") or [winner, loser]
        scans = ([str(v) for v in sc["scan_values"]] if sc.get("scan_values")
                 else pick_scans(params["scan_values"]))
        trials = sc.get("trials", args.trials)
        duration = sc.get("duration_s", args.duration_s)
        print(f"\n=== screening {fid}  ({'/'.join(fuzzers)}, scans {scans}, "
              f"{trials}x{duration}s) ===", flush=True)
        cmd = ["python3", "tools/verify_template.py", "--template", f"step5b/{fid}",
               "--fuzzers", ",".join(fuzzers), "--scan-values", ",".join(scans),
               "--trials", str(trials), "--duration-s", str(duration),
               "--jobs", str(args.jobs)]
        p = subprocess.run(cmd, cwd=REPO_ROOT, text=True)
        rec = {"feature_id": fid, "winner": winner, "loser": loser,
               "scans": scans, "verdict": "ERROR", "returncode": p.returncode}
        run_path = d / "verification_run.json"
        if run_path.is_file():
            run = json.loads(run_path.read_text())
            rec["verdict"] = run.get("verdict")
            rec["medians"] = run.get("results_median")
            rec["errors"] = run.get("errors")
        board.append(rec)
        print(f"--- {fid}: {rec['verdict']}", flush=True)

    Path(args.out).write_text(json.dumps(board, indent=2) + "\n")
    print("\n================ SCREEN BOARD ================", flush=True)
    for r in board:
        print(f"  {r['feature_id']:<48} {r.get('verdict')}", flush=True)
    print(f"\nwrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
