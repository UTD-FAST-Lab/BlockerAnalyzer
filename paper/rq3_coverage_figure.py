#!/usr/bin/env python3
"""paper/rq3_coverage_figure.py — RQ3 cross-engine coverage-over-time, (3,3,2) one-column.

8 target panels in a 3x3 grid (rows of 3, 3, 2); the empty 9th cell holds the shared
engine legend. Sized for a single paper column. Each panel: per-engine cross-trial
mean line + shaded min..max band over the 10 trials.

Reads csvs/rq3_coverage_agg.csv (produced by rq3/extract_coverage_agg.py on the server
that holds the coverage tree). Style matches the paper (serif; same engine colors as
the RQ3 heatmap).

  python3 paper/rq3_coverage_figure.py [--src csvs/rq3_coverage_agg.csv]
"""
import argparse, csv, collections
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator, FuncFormatter

plt.rcParams.update({"font.family": "serif"})
ROOT = Path(__file__).resolve().parent.parent
PAPER = Path("/home/miao/Fuzzing-Roadblock-Feature-Analysis-Paper/resources/graphics")
PREVIEW = ROOT / "out/rq3/coverage_plots"; PREVIEW.mkdir(parents=True, exist_ok=True)

FUZZERS = ["aflplusplus", "honggfuzz", "libfuzzer", "libafl"]
FLABEL = {"aflplusplus": "AFL++", "honggfuzz": "Honggfuzz",
          "libfuzzer": "LibFuzzer", "libafl": "LibAFL"}
FCOLOR = {"aflplusplus": "#1f77b4", "honggfuzz": "#2ca02c",
          "libfuzzer": "#ff7f0e", "libafl": "#d62728"}
# (3,3,2): order targets so rows read 3 / 3 / 2; 9th cell (2,2) = legend.
TARGETS = ["bloaty", "curl", "harfbuzz", "lcms", "libpng", "libxml2", "openthread", "sqlite3"]

ap = argparse.ArgumentParser()
ap.add_argument("--src", default=str(ROOT / "csvs/rq3_coverage_agg.csv"))
args = ap.parse_args()

rowmap = collections.defaultdict(list)   # (target,fuzzer) -> [(t_h, mean, min, max)]
for r in csv.DictReader(open(args.src)):
    rowmap[(r["target"], r["fuzzer"])].append(
        (float(r["time_h"]), float(r["mean_branch"]), float(r["min_branch"]), float(r["max_branch"])))

def kfmt(v, _):
    return f"{v/1000:.0f}k" if v >= 1000 else f"{v:.0f}"

fig, axes = plt.subplots(3, 3, figsize=(3.4, 2.6), sharex=True)
for idx, t in enumerate(TARGETS):
    ax = axes[idx // 3][idx % 3]
    for fz in FUZZERS:
        d = sorted(rowmap.get((t, fz), []))
        if not d:
            continue
        th = [x[0] for x in d]; mn = [x[1] for x in d]; lo = [x[2] for x in d]; hi = [x[3] for x in d]
        ax.fill_between(th, lo, hi, color=FCOLOR[fz], alpha=0.15, lw=0)
        ax.plot(th, mn, color=FCOLOR[fz], lw=1.0)
    ax.set_title(t, fontsize=7, fontweight="bold", pad=1.5)
    ax.tick_params(labelsize=5, length=1.8, pad=1)
    ax.grid(alpha=0.3, lw=0.4)
    ax.yaxis.set_major_locator(MaxNLocator(3)); ax.yaxis.set_major_formatter(FuncFormatter(kfmt))
    ax.xaxis.set_major_locator(MaxNLocator(3))
    ax.margins(x=0)

# legend in the empty (2,2) cell
lax = axes[2][2]; lax.axis("off")
handles = [Line2D([0], [0], color=FCOLOR[f], lw=1.8, label=FLABEL[f]) for f in FUZZERS]
lax.legend(handles=handles, loc="center", fontsize=6.5, frameon=False,
           handlelength=1.5, labelspacing=0.6)

fig.supxlabel("time (h)", fontsize=7.5, y=0.01)
fig.supylabel("branches covered", fontsize=7.5, x=0.005)
fig.tight_layout(pad=0.3, w_pad=0.4, h_pad=0.5)
for ext, path in (("pdf", PAPER / "rq3_coverage_curves.pdf"), ("png", PREVIEW / "rq3_coverage_curves.png")):
    fig.savefig(path, bbox_inches="tight", dpi=150)
    print("wrote", path)
