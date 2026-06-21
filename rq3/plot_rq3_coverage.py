#!/usr/bin/env python3
"""
plot_rq3_coverage.py — coverage-by-time plot for the RQ3 cross-engine campaign:
each target × 4 whole-fuzzer engines, aggregated across 10 trials.

Per panel, per fuzzer: one bold cross-trial mean line + a shaded band spanning
the across-trial range (min..max). Mirrors tools/plot_coverage_curves.py but
points at the RQ3 coverage_ts tree and the 4 FuzzBench engines.

Reads out/rq3/coverage_ts/<target>/<fuzzer>/trial<N>/coverage_timeseries.csv.

Usage:
    python3 rq3/plot_rq3_coverage.py [--targets curl harfbuzz openthread]
                                     [--output out/rq3/rq3_coverage_curves.png]
"""

import argparse
import csv
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
TS_BASE = REPO_ROOT / "out" / "rq3" / "coverage_ts"
DEFAULT_OUTPUT = REPO_ROOT / "out" / "rq3" / "coverage_plots" / "rq3_coverage_curves.png"

FUZZERS = ["aflplusplus", "honggfuzz", "libfuzzer", "libafl"]
COLORS = {
    "aflplusplus": "#1f77b4",
    "honggfuzz":   "#2ca02c",
    "libfuzzer":   "#ff7f0e",
    "libafl":      "#d62728",
}


def read_per_trial(target, fuzzer, trial):
    path = TS_BASE / target / fuzzer / f"trial{trial}" / "coverage_timeseries.csv"
    if not path.is_file():
        return None
    series = []
    with path.open() as f:
        for r in csv.DictReader(f):
            series.append((float(r["time_s"]), int(r["branch_covered"])))
    return sorted(series)


def gather_trials(target, fuzzer, n_trials=10, metric="mean"):
    trials = []
    for t in range(1, n_trials + 1):
        s = read_per_trial(target, fuzzer, t)
        if s:
            trials.append(s)
    if not trials:
        return None, None

    all_times = sorted(set(t for s in trials for t, _ in s))
    matrix = np.zeros((len(trials), len(all_times)))
    for i, s in enumerate(trials):
        d = dict(s)
        last = 0
        for j, t in enumerate(all_times):
            if t in d:
                last = d[t]
            matrix[i, j] = last

    times_h = np.array(all_times) / 3600.0
    agg = np.median(matrix, axis=0) if metric == "median" else matrix.mean(axis=0)
    return (times_h, matrix), (times_h, agg)


def grid_shape(n, cols=4):
    cols = min(cols, n)
    rows = math.ceil(n / cols)
    return rows, cols


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--targets", nargs="+", default=["curl", "harfbuzz", "openthread"])
    p.add_argument("--output", default=str(DEFAULT_OUTPUT))
    p.add_argument("--cols", type=int, default=4,
                   help="panels per row (default 4 → 2×4 grid for 8 targets)")
    p.add_argument("--metric", choices=["mean", "median"], default="mean",
                   help="cross-trial aggregate for the bold line (default mean)")
    args = p.parse_args()

    targets = args.targets
    rows, cols = grid_shape(len(targets), args.cols)
    fig, axes = plt.subplots(rows, cols, figsize=(6.0 * cols, 4.2 * rows),
                             sharex=False, squeeze=False)
    axes_flat = axes.flatten()

    for idx, target in enumerate(targets):
        ax = axes_flat[idx]
        for fuzzer in FUZZERS:
            trials_pkt, agg_pkt = gather_trials(target, fuzzer, metric=args.metric)
            if trials_pkt is None:
                continue
            times_h, matrix = trials_pkt
            _, agg = agg_pkt
            color = COLORS[fuzzer]
            # shaded across-trial range (min..max)
            ax.fill_between(times_h, matrix.min(axis=0), matrix.max(axis=0),
                            color=color, alpha=0.18, linewidth=0, zorder=1)
            # aggregate line on top
            ax.plot(times_h, agg, color=color,
                    label=f"{fuzzer} (n={matrix.shape[0]})",
                    linewidth=2.0, zorder=3)
        ax.set_title(target, fontweight="bold")
        ax.set_xlabel("time (hours)")
        ax.set_ylabel("branch_covered")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8, loc="lower right")

    for k in range(len(targets), len(axes_flat)):
        axes_flat[k].set_visible(False)

    fig.suptitle(
        "RQ3 cross-engine coverage time-series — n=10 trials, 24h each "
        f"(line = {args.metric}, shade = trial range)",
        fontsize=12,
    )
    fig.tight_layout()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=130)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
