#!/usr/bin/env python3
"""paper/rq3_capability_figures.py — RQ3 fuzzer capability-profile figures (paper-quality).

Primary figure: a HORIZONTAL grouped heatmap (rows = 4 engines, cols = family ▸
category) of per-engine resolve-rate over the 13 VALIDATED mechanism categories
(no inconclusive — that completeness is carried by the family-level tables).
Driven straight from bench/roadblock_facts.csv ⋈ csvs/rq3_resolve.csv so per-category
n matches the paper taxonomy table (tab:taxonomy) exactly — multi-category branches
count in every category they belong to.

Style matched to Fig.~5 (target_pair_heatmap): serif font, RdBu_r colormap,
#ECECEC for missing, white minor gridlines, small serif tick labels, side colorbar.

Companion: radar fingerprint + per-fuzzer circular bars (family / validated-category).

Outputs: PDFs -> paper repo resources/graphics/ ; PNG previews -> out/rq3/coverage_plots/.
Regenerate inputs first:  python3 tools/bench_score.py score ; python3 rq3/score_families.py
"""
import csv, collections
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle
from mpl_toolkits.axes_grid1 import make_axes_locatable

plt.rcParams.update({"font.family": "serif"})

ROOT = Path(__file__).resolve().parent.parent
PAPER = Path("/home/miao/Fuzzing-Roadblock-Feature-Analysis-Paper/resources/graphics")
PREVIEW = ROOT / "out/rq3/coverage_plots"; PREVIEW.mkdir(parents=True, exist_ok=True)

FUZZERS = ["aflplusplus", "honggfuzz", "libfuzzer", "libafl"]
FLABEL = {"aflplusplus": "AFL++", "honggfuzz": "Honggfuzz",
          "libfuzzer": "LibFuzzer", "libafl": "LibAFL$^\\dagger$"}
FCOLOR = {"aflplusplus": "#1f77b4", "honggfuzz": "#2ca02c",
          "libfuzzer": "#ff7f0e", "libafl": "#d62728"}
TAU = 0.8

FAM_ORDER = ["I2S-P", "I2S-A", "VP-P", "VPC-P", "CTX-P", "CTX-A", "GRIM-P", "NGRAM-P"]
FAM_COLOR = {"I2S-P": "#1f77b4", "I2S-A": "#5fa8dc", "VP-P": "#2ca02c", "VPC-P": "#8fd18f",
             "CTX-P": "#ff7f0e", "CTX-A": "#ffc081", "GRIM-P": "#9467bd", "NGRAM-P": "#8c564b"}

# canonical_label -> EXACT category name as printed in the paper taxonomy table (Table VI)
DISPLAY = {
    "i2s_string_literal_substitution": "string_literal_substitution",
    "i2s_numeric_tag_substitution": "numeric_tag_substitution",
    "i2s_anti_target_depletion": "target_depletion",
    "i2s_anti_decoy_overfit": "decoy_substitution_overfit",
    "i2s_anti_structural_byte_corruption": "structural_byte_corruption",
    "vp_gradient_value_distance_closure": "gradient_value_distance_closure",
    "vp_gradient_assembly_depth": "gradient_assembly_depth",
    "joint_value_distance_closure": "joint_value_distance_closure",
    "joint_assembly_depth": "joint_assembly_depth",
    "ctx_iteration_path_depth": "iteration_path_depth",
    "ctx_inflation": "corpus_inflation",
    "grimoire_structural_assembly": "structural_assembly",
    "ngram_sequential_depth_reach": "sequential_depth_reach",
}

def save(fig, name):
    fig.savefig(PAPER / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(PREVIEW / f"{name}.png", dpi=150, bbox_inches="tight")
    print("wrote", (PAPER / f'{name}.pdf').name, "+", (PREVIEW / f'{name}.png'))

# ---------------------------------------------------------------- load fact table
members = collections.defaultdict(set)           # (family, category) -> {(target,bid)}  validated only
for r in csv.DictReader(open(ROOT / "bench/roadblock_facts.csv")):
    if r["status"] != "validated":
        continue
    members[(r["family"], r["category"])].add((r["target"], int(r["branch_id"])))
fam_cats = {fam: sorted([c for (f, c) in members if f == fam], key=lambda c: -len(members[(fam, c)]))
            for fam in FAM_ORDER}

# ---------------------------------------------------------------- resolve outcomes
# Cell metric = MEAN per-blocker resolution rate: average over a category's blockers of
# n_resolved/n_reached (the fraction of trials in which the engine takes the blocked side).
# Continuous resolving STRENGTH -- uses every trial, so it separates engines whose decisive
# (>=8/10) rates are both low but differ (e.g. 6/10 vs 3/10); the >=8/10 cut collapses those.
# Mean (not median): ~49% of per-blocker fractions are exactly 1.0, so the median snaps to
# 1.0 and hides the gradation (and can even invert the engine ranking).
counts = collections.defaultdict(dict)   # fuzzer -> {(t,bid): (nr,nb)}
for r in csv.DictReader(open(ROOT / "csvs/rq3_resolve.csv")):
    nr, nb = int(r["n_resolved"]), int(r["n_blocked"])
    if nr + nb == 0:
        continue                          # unreached -> excluded (G3)
    counts[r["fuzzer"]][(r["target"], int(r["branch_id"]))] = (nr, nb)

def rate(memberset, f):
    fr = []
    for b in memberset:
        if b in counts[f]:
            nr, nb = counts[f][b]
            fr.append(nr / (nr + nb))     # per-blocker resolve fraction (reached trials)
    return float(np.mean(fr)) if fr else np.nan

# columns: (family, canonical_category, n)
cols = [(fam, c, len(members[(fam, c)])) for fam in FAM_ORDER for c in fam_cats[fam]]


# ============ 1. HEATMAP (rows = family ▸ category, cols = engines) — Fig.5 style
def fig_heatmap(show_n=True):
    M = np.array([[rate(members[(fam, c)], f) for f in FUZZERS] for (fam, c, n) in cols])
    nrow = len(cols)
    fig, ax = plt.subplots(figsize=(4.1, nrow * 0.32 + 0.9))
    cmap = plt.cm.RdBu_r.copy(); cmap.set_bad("#ECECEC")          # red = favorable (high)
    im = ax.imshow(np.ma.masked_invalid(M), cmap=cmap, vmin=0, vmax=1, aspect="auto")
    # white minor gridlines between cells (Fig.5 style)
    ax.set_xticks(np.arange(-0.5, len(FUZZERS)), minor=True)
    ax.set_yticks(np.arange(-0.5, nrow), minor=True)
    ax.grid(which="minor", color="white", lw=0.8); ax.tick_params(which="minor", length=0)
    # engine (column) labels — 45°, capitalised
    ax.set_xticks(range(len(FUZZERS)))
    ax.set_xticklabels([FLABEL[f] for f in FUZZERS], rotation=45, ha="right",
                       rotation_mode="anchor", fontsize=7)
    # category (row) labels — exact paper names, horizontal, with n
    ax.set_yticks(range(nrow))
    ylabs = [DISPLAY[c] + (f" ($n{{=}}{n}$)" if show_n else "") for (fam, c, n) in cols]
    ax.set_yticklabels(ylabs, fontsize=6)
    for i in range(nrow):
        for j in range(len(FUZZERS)):
            v = M[i, j]
            ax.text(j, i, "·" if np.isnan(v) else f"{v:.2f}", ha="center", va="center",
                    fontsize=5.6, color="white" if (not np.isnan(v) and (v < 0.18 or v > 0.82)) else "black")
    # left gutter: thin family color band (no text); names go in the legend at right
    ax.set_xlim(-0.95, len(FUZZERS) - 0.5)
    start = 0
    for fam in FAM_ORDER:
        h = len(fam_cats[fam])
        if h == 0:
            continue
        if start:
            ax.axhline(start - 0.5, color="black", lw=0.9)
        ax.add_patch(Rectangle((-0.78, start - 0.5), 0.20, h, color=FAM_COLOR[fam],
                               clip_on=False, zorder=3))
        start += h
    ax.set_ylim(nrow - 0.5, -0.5)
    ax.tick_params(which="major", length=0)
    div = make_axes_locatable(ax)
    cax = div.append_axes("right", size="4%", pad=0.06)
    cb = fig.colorbar(im, cax=cax)
    cb.set_label("mean resolution rate (red = favorable)", fontsize=5.5)
    cb.ax.tick_params(labelsize=5)
    # family color-code legend next to the map
    handles = [Patch(facecolor=FAM_COLOR[fam], edgecolor="none", label=fam) for fam in FAM_ORDER]
    ax.legend(handles=handles, title="family", loc="upper left", bbox_to_anchor=(1.55, 1.0),
              fontsize=9, title_fontsize=10, frameon=False, handlelength=1.4,
              handleheight=1.4, labelspacing=0.5, borderaxespad=0)
    save(fig, "rq3_cap_heatmap"); plt.close(fig)


# ---- family / validated-category scores for the companion figs ----
fam_rate, fam_n = {}, {}
for fam in FAM_ORDER:
    s = set().union(*[members[(fam, c)] for c in fam_cats[fam]]) if fam_cats[fam] else set()
    fam_n[fam] = len(s)
    fam_rate[fam] = {f: rate(s, f) for f in FUZZERS}

# ============================================================ 2. RADAR FINGERPRINT
def fig_radar():
    fams = FAM_ORDER
    ang = np.linspace(0, 2 * np.pi, len(fams), endpoint=False).tolist(); ang += ang[:1]
    fig, ax = plt.subplots(figsize=(6.6, 6.6), subplot_kw=dict(polar=True))
    for f in FUZZERS:
        vals = [fam_rate[fam][f] for fam in fams] + [fam_rate[fams[0]][f]]
        lw, z, al = (2.6, 5, 0.10) if f == "libafl" else (1.8, 3, 0.06)
        ax.plot(ang, vals, color=FCOLOR[f], lw=lw, label=FLABEL[f], marker="o", ms=4, zorder=z)
        ax.fill(ang, vals, color=FCOLOR[f], alpha=al, zorder=z - 1)
    ax.set_xticks(ang[:-1])
    ax.set_xticklabels([f"{fam}\n(n={fam_n[fam]})" for fam in fams], fontsize=9)
    ax.set_ylim(0, 1); ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["", "0.5", "", "1.0"], fontsize=7.5); ax.set_rlabel_position(90)
    ax.legend(loc="upper right", bbox_to_anchor=(1.16, 1.13), fontsize=9.5, framealpha=0.9)
    save(fig, "rq3_cap_radar"); plt.close(fig)


fig_heatmap(show_n=True)
fig_radar()
