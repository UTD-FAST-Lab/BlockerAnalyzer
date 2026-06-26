#!/usr/bin/env python3
"""Generate the I2S-anti enrichment figure (categories 1 & 3) for 4.2_rq2.tex.

Two side-by-side diverging bar plots, single-column width. Each panel shows the
shared I2S-anti signature on the campaign corpus: the I2S (cmplog) corpus is
DEPLETED of the byte the resolving arm needs (red, signed_target_enrich < 0) and
instead over-represents a decoy byte (green, decoy_enrich > 0). Values are the
real dataset log2 cmplog/naive per-offset frequency ratios.

  panel 1  target_depletion           libpng/3977   target -0.82  decoy +0.68
  panel 2  decoy_substitution_overfit  harfbuzz/5323 target -2.79  decoy +11.3

Output: <paper-repo>/resources/graphics/i2s_anti_enrich.pdf  (\includegraphics[width=\columnwidth])

Convention (matches paper/make_target_pair_heatmap.py): paper-plot generator scripts
live under BlockerAnalyzer/paper/; their figure output is written into the paper repo's
resources/graphics/ dir (the \graphicspath), which sits next to BlockerAnalyzer.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

RED, GREEN = "#be3c3c", "#1e783c"
# this file: <BlockerAnalyzer>/paper/<file>  ->  parents[2] = /home/miao (holds both repos)
_GFX = Path(__file__).resolve().parents[2] / "Fuzzing-Roadblock-Feature-Analysis-Paper" / "resources" / "graphics"
OUT = (_GFX if _GFX.is_dir() else Path(__file__).resolve().parent) / "i2s_anti_enrich.pdf"

plt.rcParams.update({
    "font.size": 7, "font.family": "serif",
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "xtick.major.size": 2.5,
    "mathtext.fontset": "cm",
})

# (category, branch, signed_target_enrich, decoy_enrich, decoy label, placement)
# placement of the decoy-identity label: "right" of a short bar, or "above" a long bar.
panels = [
    ("target_depletion", "libpng/3977", -0.82, 0.68, "rival 0x65", "right"),
    ("decoy_substitution_overfit", "harfbuzz/5323", -2.79, 11.3, "GPOS", "above"),
]
XLIM = (-4.2, 13.5)
XTICKS = [0, 5, 10]

fig, axes = plt.subplots(1, 2, figsize=(3.49, 1.5), sharex=True)
for i, (ax, (name, br, tgt, dec, declab, place)) in enumerate(zip(axes, panels)):
    ax.axvspan(XLIM[0], 0, color=RED, alpha=0.06, lw=0)
    ax.axvspan(0, XLIM[1], color=GREEN, alpha=0.06, lw=0)
    ax.barh([1.0], [tgt], height=0.5, color=RED, zorder=3)
    ax.barh([0.0], [dec], height=0.5, color=GREEN, zorder=3)
    ax.axvline(0, color="black", lw=0.7, zorder=4)
    # value labels sit just past the zero line (opposite side of each bar) so they
    # never collide with the left-margin y tick labels.
    ax.text(0.35, 1.0, f"{tgt:g}", va="center", ha="left",
            color=RED, fontsize=6.3)
    ax.text(-0.35, 0.0, f"+{dec:g}", va="center", ha="right",
            color=GREEN, fontsize=6.3)
    # decoy identity: to the RIGHT of a short bar, or ABOVE a long bar (white space)
    if place == "right":
        ax.text(dec + 0.6, 0.0, declab, va="center", ha="left",
                color=GREEN, fontsize=5.6)
    else:
        ax.text(dec * 0.5, 0.52, declab, va="center", ha="center",
                color=GREEN, fontsize=5.6)
    ax.set_yticks([1.0, 0.0])
    ax.set_yticklabels(["target", "decoy"], fontsize=6.5)
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(XLIM)
    ax.set_ylim(-0.65, 1.7)
    ax.set_xticks(XTICKS)
    ax.tick_params(axis="x", labelsize=5.8)
    # subplot caption below the plot: "(a) target_depletion"
    ax.set_xlabel(f"({chr(97 + i)}) {name}", fontsize=6.4)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)

fig.tight_layout(w_pad=1.0)
fig.savefig(OUT, bbox_inches="tight", pad_inches=0.04)
print("wrote", OUT)
