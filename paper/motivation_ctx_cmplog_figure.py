#!/usr/bin/env python3
"""paper/motivation_ctx_cmplog_figure.py — Section 2 motivating-example coverage figure.

Two panels (libxml2, bloaty), two variants each: context-sensitive coverage
(naive_ctx -> "ctx") vs input-to-state (cmplog). Each variant: cross-trial mean
line + shaded min..max band over the 10 trials. Reads the per-trial coverage
timeseries directly from the campaign tree under out/coverage_ts/.

Point of the figure: on bloaty cmplog dominates total coverage; on libxml2 the
two are statistically indistinguishable -- yet at the branch level each technique
uniquely cracks roadblocks the other never flips (Table 1). Whole-program
coverage hides that complementarity.

  python3 paper/motivation_ctx_cmplog_figure.py

Output: <paper>/resources/graphics/motivation_ctx_cmplog_coverage.pdf
        out/motivation/motivation_ctx_cmplog_coverage.png  (preview)
"""
import csv, glob, statistics
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
PREVIEW = ROOT / "out/motivation"; PREVIEW.mkdir(parents=True, exist_ok=True)

TARGETS = ["libxml2", "bloaty"]
# variant -> (display label, color)
VARIANTS = {"naive_ctx": ("ctx", "#1f77b4"), "cmplog": ("cmplog", "#d62728")}


def load(target, fuzzer):
    """Return (times_h, mean, lo, hi) aligned across trials at shared checkpoints."""
    per_t = {}  # time_s -> list of branch_covered across trials
    for cf in glob.glob(str(ROOT / f"out/coverage_ts/{target}/{fuzzer}/trial*/coverage_timeseries.csv")):
        for r in csv.DictReader(open(cf)):
            per_t.setdefault(int(r["time_s"]), []).append(int(r["branch_covered"]))
    if not per_t:
        return None
    ts = sorted(per_t)
    th = [t / 3600.0 for t in ts]
    mean = [statistics.mean(per_t[t]) for t in ts]
    lo = [min(per_t[t]) for t in ts]
    hi = [max(per_t[t]) for t in ts]
    return th, mean, lo, hi


def kfmt(v, _):
    if v < 1000:
        return f"{v:.0f}"
    s = f"{v/1000:.1f}".rstrip("0").rstrip(".")  # 2000->"2k", 1200->"1.2k"
    return s + "k"


fig, axes = plt.subplots(1, 2, figsize=(3.4, 1.7))
for ax, t in zip(axes, TARGETS):
    for fz, (label, color) in VARIANTS.items():
        d = load(t, fz)
        if d is None:
            continue
        th, mean, lo, hi = d
        ax.fill_between(th, lo, hi, color=color, alpha=0.15, lw=0)
        ax.plot(th, mean, color=color, lw=1.1)
    ax.set_title(t, fontsize=7, fontweight="bold", pad=1.5)
    ax.tick_params(labelsize=5, length=1.8, pad=1)
    ax.grid(alpha=0.3, lw=0.4)
    ax.yaxis.set_major_locator(MaxNLocator(4)); ax.yaxis.set_major_formatter(FuncFormatter(kfmt))
    ax.xaxis.set_major_locator(MaxNLocator(4))
    ax.margins(x=0)

handles = [Line2D([0], [0], color=c, lw=1.8, label=lbl) for lbl, c in VARIANTS.values()]
fig.legend(handles=handles, loc="upper center", ncol=2, fontsize=6.5, frameon=False,
           handlelength=1.5, columnspacing=1.4, bbox_to_anchor=(0.5, 1.04))
fig.supxlabel("time (h)", fontsize=7.5, y=0.02)
fig.supylabel("branches covered", fontsize=7.5, x=0.005)
fig.tight_layout(pad=0.3, w_pad=0.6, rect=(0, 0, 1, 0.94))
for path in (PAPER / "motivation_ctx_cmplog_coverage.pdf",
             PREVIEW / "motivation_ctx_cmplog_coverage.png"):
    fig.savefig(path, bbox_inches="tight", dpi=150)
    print("wrote", path)
