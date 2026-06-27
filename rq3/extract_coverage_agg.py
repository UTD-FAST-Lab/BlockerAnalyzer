#!/usr/bin/env python3
"""rq3/extract_coverage_agg.py — RUN ON THE SERVER THAT HOLDS THE RQ3 COVERAGE TREE.

Collapses the cross-engine coverage time-series (8 targets x 4 engines x 10 trials =
320 files) into ONE small CSV so only that file needs transferring back.

Reads:  <ts-base>/<target>/<fuzzer>/trial<N>/coverage_timeseries.csv
        (columns: time_s, branch_covered, branch_total)
Writes: csvs/rq3_coverage_agg.csv  with columns
        target, fuzzer, time_h, mean_branch, min_branch, max_branch, n_trials
        (one row per (target, fuzzer, time-grid-point); ~1.5k rows total)

Each trial's coverage is a monotone step function; we forward-fill it onto a fixed
hour grid, then take the per-grid-point mean / min / max across the trials (the bold
line + shaded band the plot uses).

Usage (on the data server):
  python3 rq3/extract_coverage_agg.py --ts-base out/rq3/coverage_ts \
      --targets bloaty curl harfbuzz lcms libpng libxml2 openthread sqlite3
  # then copy csvs/rq3_coverage_agg.csv back to the paper machine.
"""
import argparse, csv
from pathlib import Path
import numpy as np

FUZZERS = ["aflplusplus", "honggfuzz", "libfuzzer", "libafl"]


def read_trial(p):
    if not p.is_file():
        return None
    s = []
    for r in csv.DictReader(open(p)):
        s.append((float(r["time_s"]), int(r["branch_covered"])))
    return sorted(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ts-base", required=True, help="dir holding <target>/<fuzzer>/trial<N>/coverage_timeseries.csv")
    ap.add_argument("--targets", nargs="+", required=True)
    ap.add_argument("--fuzzers", nargs="+", default=FUZZERS)
    ap.add_argument("--n-trials", type=int, default=10)
    ap.add_argument("--max-hours", type=float, default=24.0)
    ap.add_argument("--step-h", type=float, default=0.5)
    ap.add_argument("--out", default="csvs/rq3_coverage_agg.csv")
    a = ap.parse_args()

    base = Path(a.ts_base)
    grid = np.arange(0.0, a.max_hours + 1e-9, a.step_h)
    rows = []
    for t in a.targets:
        for fz in a.fuzzers:
            trials = []
            for n in range(1, a.n_trials + 1):
                s = read_trial(base / t / fz / f"trial{n}" / "coverage_timeseries.csv")
                if s:
                    trials.append(s)
            if not trials:
                print(f"  WARN: no data for {t}/{fz}")
                continue
            M = np.zeros((len(trials), len(grid)))
            for i, s in enumerate(trials):
                ts = [x[0] / 3600.0 for x in s]
                cv = [x[1] for x in s]
                last, j = 0, 0
                for gi, g in enumerate(grid):
                    while j < len(ts) and ts[j] <= g:
                        last = cv[j]; j += 1
                    M[i, gi] = last
            for gi, g in enumerate(grid):
                col = M[:, gi]
                rows.append({"target": t, "fuzzer": fz, "time_h": round(float(g), 3),
                             "mean_branch": round(float(col.mean()), 2),
                             "min_branch": int(col.min()), "max_branch": int(col.max()),
                             "n_trials": len(trials)})
            print(f"  {t}/{fz}: {len(trials)} trials")
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["target", "fuzzer", "time_h", "mean_branch",
                                          "min_branch", "max_branch", "n_trials"])
        w.writeheader(); w.writerows(rows)
    print(f"wrote {out}: {len(rows)} rows")


if __name__ == "__main__":
    main()
