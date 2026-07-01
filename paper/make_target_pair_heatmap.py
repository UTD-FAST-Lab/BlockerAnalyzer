#!/usr/bin/env python3
"""RQ1 variant-pair x target significance heatmap (single-column, with margins).

Rows = the 10 single-technique-delta variant pairs, columns = the 8 targets.
A cell is coloured only when that pair is significant on that target, shaded by the
effect size: the relative final-coverage gain of the stronger variant over the
weaker one, (cov_A - cov_B) / cov_B in percent (red = the technique helps, blue =
it hurts). Non-significant cells are pale grey. The right margin gives each pair's
breadth (# significant targets); the top margin gives each target's # significant
pairs.

Sized to fit one IEEE column.

Run from the BlockerAnalyzer repo root:
    python3 paper/make_target_pair_heatmap.py
"""
import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CSVS = [
    os.path.join(ROOT, "csvs", "subject_pair_significance_bloaty-lcms-libpng-libxml2.csv"),
    os.path.join(ROOT, "csvs", "subject_pair_significance_curl-harfbuzz-openthread-sqlite3.csv"),
]
# The paper \includegraphics{target_pair_heatmap} with \graphicspath{{./resources/graphics/}},
# so write straight into the paper repo's graphics dir when it exists (fallback: here).
_PAPER_GFX = os.path.join(os.path.dirname(ROOT),
                          "Fuzzing-Roadblock-Feature-Analysis-Paper",
                          "resources", "graphics")
OUT = os.path.join(_PAPER_GFX if os.path.isdir(_PAPER_GFX) else HERE,
                   "target_pair_heatmap.pdf")

PAIR_LABEL = {
    ("cmplog", "naive"):                       "cmp/naive",
    ("value_profile_cmplog", "value_profile"): "vpc/vp",
    ("value_profile_cmplog", "cmplog"):        "vpc/cmp",
    ("value_profile", "naive"):                "vp/naive",
    ("naive_ctx", "naive"):                    "ctx/naive",
    ("grimoire", "cmplog"):                    "grim/cmp",
    ("minimizer", "naive"):                    "min/naive",
    ("mopt", "naive"):                         "mopt/naive",
    ("fast", "minimizer"):                     "fast/min",
    ("naive_ngram4", "naive"):                 "ngram/naive",
}
TARGETS = ["bloaty", "lcms", "libpng", "libxml2",
           "curl", "harfbuzz", "openthread", "sqlite3"]

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 8,                       # match RQ3 heatmap (fig_heatmap)
    "axes.linewidth": 0.5,
    "pdf.fonttype": 42,
})
# shared font sizes — identical to RQ3 rq3_capability_figures.fig_heatmap
FS_TICK, FS_CELL, FS_CBAR_LAB, FS_CBAR_TICK = 7, 6, 6.5, 6


def load():
    rows = []
    for path in CSVS:
        with open(path) as f:
            rows.extend(csv.DictReader(f))
    table = {pk: {} for pk in PAIR_LABEL}
    for r in rows:
        pk = (r["A"], r["B"])
        if pk not in table:
            raise SystemExit(f"unexpected pair {pk}")
        base = float(r["mean_final_B"])
        rel = 100.0 * float(r["delta_final"]) / base if base else 0.0
        table[pk][r["target"]] = {
            "sig": r["admissible"].strip().lower() == "true",
            "rel": rel,
        }
    return table


def main():
    table = load()
    pairs = list(PAIR_LABEL)
    pair_tot = {pk: sum(table[pk][t]["sig"] for t in TARGETS) for pk in pairs}
    targ_tot = {t: sum(table[pk][t]["sig"] for pk in pairs) for t in TARGETS}
    pair_order = sorted(pairs, key=lambda pk: -pair_tot[pk])    # broadest pair on top
    targ_order = sorted(TARGETS, key=lambda t: -targ_tot[t])    # busiest target left

    nP, nT = len(pair_order), len(targ_order)
    eff = np.full((nP, nT), np.nan)            # rows = pairs, cols = targets
    for i, pk in enumerate(pair_order):
        for j, t in enumerate(targ_order):
            d = table[pk][t]
            if d["sig"]:
                eff[i, j] = d["rel"]

    vmax = np.nanmax(eff)
    vmin = min(np.nanmin(eff), -1)
    norm = TwoSlopeNorm(vmin=vmin, vcenter=0.0, vmax=vmax)
    cmap = plt.cm.RdBu_r.copy()
    cmap.set_bad("#ECECEC")

    fig, ax = plt.subplots(figsize=(3.45, nP * 0.14 + 1.0))   # shorter cells

    im = ax.imshow(eff, cmap=cmap, norm=norm, aspect="auto")
    for i in range(nP):
        for j in range(nT):
            if not np.isnan(eff[i, j]):
                v = eff[i, j]
                txt = "0" if abs(v) < 0.5 else f"{v:.0f}"
                tc = "white" if (v > 0.6 * vmax or v < 0.6 * vmin) else "black"
                ax.text(j, i, txt, ha="center", va="center", fontsize=FS_CELL, color=tc)

    ax.set_xticks(range(nT))
    ax.set_xticklabels(targ_order, rotation=45, ha="right",
                       rotation_mode="anchor", fontsize=FS_TICK)
    ax.set_yticks(range(nP))
    ax.set_yticklabels([PAIR_LABEL[pk] for pk in pair_order], fontsize=FS_TICK)
    ax.set_xticks(np.arange(-0.5, nT), minor=True)
    ax.set_yticks(np.arange(-0.5, nP), minor=True)
    ax.grid(which="minor", color="white", lw=0.8)
    ax.tick_params(which="minor", length=0)
    ax.tick_params(which="major", length=2)

    div = make_axes_locatable(ax)
    cax = div.append_axes("right", size="4%", pad=0.06)
    cb = fig.colorbar(im, cax=cax)
    cb.set_label("coverage gain, A vs B (%)", fontsize=FS_CBAR_LAB)
    cb.ax.tick_params(labelsize=FS_CBAR_TICK)

    fig.savefig(OUT, bbox_inches="tight")
    plt.close(fig)

    print("per-target # significant pairs:")
    for t in targ_order:
        print(f"  {t:<11} {targ_tot[t]}")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
