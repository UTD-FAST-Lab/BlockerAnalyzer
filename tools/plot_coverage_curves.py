#!/usr/bin/env python3
"""
plot_coverage_curves.py — coverage-by-time plot for canonical targets
× 4 fuzzers, aggregated across 10 trials.

Each panel shows, per fuzzer:
  - one thin semi-transparent line per trial (per-trial "spaghetti"),
  - one bold line for the cross-trial mean.

This makes distributional separation visible at a glance — two fuzzers
with overlapping mean lines but cleanly displaced per-trial bands are
significant under Mann-Whitney; two with heavy per-trial overlap are not,
even if the means look offset.

Reads `out/coverage_ts/<target>/<fuzzer>/trial<N>/coverage_timeseries.csv`
(columns: time_s, branch_covered, branch_total).

Usage:
    python3 tools/plot_coverage_curves.py [--targets curl harfbuzz ...]
                                          [--output out/coverage_curves.png]

Output: out/coverage_curves.png (default)
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
TS_BASE = REPO_ROOT / "out" / "coverage_ts"
DEFAULT_OUTPUT = REPO_ROOT / "out" / "coverage_curves.png"

FUZZERS = ["naive", "cmplog", "value_profile", "value_profile_cmplog"]
COLORS = {
    "naive":                "#888888",
    "cmplog":               "#1f77b4",
    "value_profile":        "#2ca02c",
    "value_profile_cmplog": "#d62728",
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


def gather_trials(target, fuzzer, n_trials=10):
    """Return list of per-trial series and a (times, mean) tuple for the mean line.
    Trials may have slightly different checkpoint times; we align on the union
    of times and forward-fill missing values."""
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
    mean = matrix.mean(axis=0)
    return (times_h, matrix), (times_h, mean)


def discover_targets():
    if not TS_BASE.is_dir():
        return []
    return sorted(p.name for p in TS_BASE.iterdir() if p.is_dir())


def grid_shape(n):
    """Pick (rows, cols) for n panels — roughly square, columns >= rows."""
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    return rows, cols


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--targets", nargs="+",
                   help="targets to plot (default: all under out/coverage_ts/)")
    p.add_argument("--output", default=str(DEFAULT_OUTPUT),
                   help=f"output path (default: {DEFAULT_OUTPUT.relative_to(REPO_ROOT)})")
    args = p.parse_args()

    targets = args.targets or discover_targets()
    if not targets:
        print(f"error: no targets under {TS_BASE}", flush=True)
        return

    rows, cols = grid_shape(len(targets))
    fig, axes = plt.subplots(rows, cols, figsize=(5.5 * cols, 3.8 * rows),
                             sharex=False, squeeze=False)
    axes_flat = axes.flatten()

    for idx, target in enumerate(targets):
        ax = axes_flat[idx]
        for fuzzer in FUZZERS:
            trials_pkt, mean_pkt = gather_trials(target, fuzzer)
            if trials_pkt is None:
                continue
            times_h, matrix = trials_pkt
            _, mean = mean_pkt
            color = COLORS[fuzzer]
            # per-trial spaghetti
            for row in matrix:
                ax.plot(times_h, row, color=color, alpha=0.22,
                        linewidth=0.7, zorder=1)
            # mean line on top
            ax.plot(times_h, mean, color=color,
                    label=f"{fuzzer} (n={matrix.shape[0]})",
                    linewidth=2.0, zorder=3)
        ax.set_title(target, fontweight="bold")
        ax.set_xlabel("time (hours)")
        ax.set_ylabel("branch_covered")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8, loc="lower right")

    # hide unused panels
    for k in range(len(targets), len(axes_flat)):
        axes_flat[k].set_visible(False)

    fig.suptitle(
        "LibAFL coverage time-series — n=10 trials, 12h each "
        "(thin = per-trial, bold = mean)",
        fontsize=12,
    )
    fig.tight_layout()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=130)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
