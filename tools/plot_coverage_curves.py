#!/usr/bin/env python3
"""
plot_coverage_curves.py — coverage-by-time plot for the canonical 4 targets
× 4 fuzzers, aggregated across 10 trials (mean line + IQR band).

Reads `out/coverage_ts/<target>/<fuzzer>/trial<N>/coverage_timeseries.csv`
(columns: time_s, branch_covered, branch_total). Aggregates per
(target, fuzzer, time_s) checkpoint across trials, plots one panel per
target with one line per fuzzer.

Output: out/coverage_curves.png
"""

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
TS_BASE = REPO_ROOT / "out" / "coverage_ts"
OUTPUT = REPO_ROOT / "out" / "coverage_curves.png"

TARGETS = ["lcms", "bloaty", "sqlite3", "mbedtls"]
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


def aggregate(target, fuzzer, n_trials=10):
    """Return (sorted_times, mean_at_each, p25, p75) across all available trials.
    Trials may have different checkpoint times (rare but possible); we use
    the union of times and forward-fill missing values."""
    trials = []
    for t in range(1, n_trials + 1):
        series = read_per_trial(target, fuzzer, t)
        if series:
            trials.append(series)
    if not trials:
        return None

    all_times = sorted(set(t for s in trials for t, _ in s))
    matrix = np.zeros((len(trials), len(all_times)))
    for i, s in enumerate(trials):
        d = dict(s)
        last = 0
        for j, t in enumerate(all_times):
            if t in d:
                last = d[t]
            matrix[i, j] = last

    mean = matrix.mean(axis=0)
    p25 = np.percentile(matrix, 25, axis=0)
    p75 = np.percentile(matrix, 75, axis=0)
    return np.array(all_times) / 3600.0, mean, p25, p75, matrix.shape[0]


def main():
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
    axes_flat = axes.flatten()

    for idx, target in enumerate(TARGETS):
        ax = axes_flat[idx]
        for fuzzer in FUZZERS:
            agg = aggregate(target, fuzzer)
            if agg is None:
                continue
            times_h, mean, p25, p75, n_trials = agg
            color = COLORS[fuzzer]
            ax.plot(times_h, mean, color=color,
                    label=f"{fuzzer} (n={n_trials})", linewidth=1.6)
            ax.fill_between(times_h, p25, p75, color=color, alpha=0.15,
                            linewidth=0)
        ax.set_title(target, fontweight="bold")
        ax.set_xlabel("time (hours)")
        ax.set_ylabel("branch_covered")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8, loc="lower right")

    fig.suptitle(
        "LibAFL coverage time-series — n=10 trials, 12h each (mean line, IQR band)",
        fontsize=12,
    )
    fig.tight_layout()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=130)
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
