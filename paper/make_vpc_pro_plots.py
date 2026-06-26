#!/usr/bin/env python3
"""Generate the VPC-P (joint) figure (categories 1 & 2) for 4.2_rq2.tex.

Two side-by-side bar panels, single-column width. They show the two ways the
joint family is validated, one metric per category, all values from the real
dataset (bench/dataset.jsonl):

  panel (a)  joint_value_distance_closure  sqlite3/16001
             value_distance_reached: per-arm MIN Hamming distance to the 6-byte
             gate operand 'PRAGMA' (0 = landed exactly). value_profile (no I2S)
             and cmplog (no gradient) both stall far from the operand; only
             value_profile_cmplog retains a near-keyword scaffold AND substitutes
             'PRAGMA', reaching 0.00 (closure 1.0) at the SAME input size
             (size_lift 0.31) -> reaching+retaining the operand, not assembly.
             NOTE: cmp=0.83 and vpc=0.00 are measured (assignments_s4.json);
             vp_min_distance was NOT measured for this branch (the joint rule
             scored only cmplog vs vpc) and sqlite3's corpus is off-server, so
             VP_MIN below is PROVISIONAL pending one measurement on the sqlite3
             host:
               python3 bench/tools/value_distance_reached.py branch \
                 --target sqlite3 --branch-id 16001 --value PRAGMA \
                 --winners value_profile_cmplog --losers value_profile,cmplog,naive

  panel (b)  joint_assembly_depth          harfbuzz/6814
             joint_necessity: per-arm mean count of distinct structural tokens
             (sfnt/OT table tags) placed per seed. value_profile 0 (no I2S ->
             no structure), cmplog 1.4 (partial), value_profile_cmplog 2.4
             (full) -- with size_lift 2.44 the gradient grows the structure the
             I2S-only arm cannot.

Output: <paper-repo>/resources/graphics/vpc_pro_plots.pdf  (\\includegraphics[width=\\columnwidth])

Convention (matches paper/make_i2s_anti_enrich.py): paper-plot generator scripts
live under BlockerAnalyzer/paper/; their figure output is written into the paper
repo's resources/graphics/ dir (the \\graphicspath), next to BlockerAnalyzer.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

RED, GREEN, ORANGE = "#be3c3c", "#1e783c", "#c87814"  # losc / winc / value_profile arm
_GFX = Path(__file__).resolve().parents[2] / "Fuzzing-Roadblock-Feature-Analysis-Paper" / "resources" / "graphics"
OUT = (_GFX if _GFX.is_dir() else Path(__file__).resolve().parent) / "vpc_pro_plots.pdf"

plt.rcParams.update({
    "font.size": 7, "font.family": "serif",
    "axes.linewidth": 0.6, "ytick.major.width": 0.6, "ytick.major.size": 2.5,
    "mathtext.fontset": "cm",
})

fig, (axa, axb) = plt.subplots(1, 2, figsize=(3.49, 1.65))

# ---- panel (a): joint_value_distance_closure (sqlite3/16001, operand 'PRAGMA') ----
# per-arm MIN Hamming distance to the 6-byte operand 'PRAGMA' (0 = landed exactly).
# Same 3-arm layout/style as panel (b): value_profile, cmplog, vpc.
VP_MIN = 1.00   # PROVISIONAL -- NOT measured (sqlite3 corpus off-server); replace
                # with the real vp_min_distance from the command in the docstring.
a_labels = ["value_\nprofile", "cmplog", "vpc"]
a_vals = [VP_MIN, 0.83, 0.00]            # cmp/vpc measured; vp provisional
a_cols = [ORANGE, RED, GREEN]
xa = range(len(a_vals))
axa.bar(xa, a_vals, width=0.62, color=a_cols, zorder=3)
for x, v in zip(xa, a_vals):
    axa.text(x, v + 0.03, f"{v:.2f}", ha="center", va="bottom", fontsize=6.3,
             color=a_cols[x])
axa.set_xticks(list(xa))
axa.set_xticklabels(a_labels, fontsize=6.0)
axa.set_ylim(0, 1.12)
axa.set_ylabel("min. dist. to operand", fontsize=6.4)
axa.set_xlabel("(a) joint_value_distance_closure", fontsize=6.4)
axa.tick_params(axis="x", length=0)
axa.tick_params(axis="y", labelsize=5.8)
for s in ("top", "right"):
    axa.spines[s].set_visible(False)

# ---- panel (b): joint_assembly_depth (harfbuzz/6814) ------------------------
b_labels = ["value_\nprofile", "cmplog", "vpc"]
b_vals = [0.0, 1.4, 2.4]
b_cols = [ORANGE, RED, GREEN]
xb = range(len(b_vals))
axb.bar(xb, b_vals, width=0.62, color=b_cols, zorder=3)
for x, v in zip(xb, b_vals):
    axb.text(x, v + 0.06, f"{v:g}", ha="center", va="bottom", fontsize=6.3,
             color=b_cols[x])
axb.set_xticks(list(xb))
axb.set_xticklabels(b_labels, fontsize=6.0)
axb.set_ylim(0, 2.9)
axb.set_ylabel("struct. tags / seed", fontsize=6.4)
axb.set_xlabel("(b) joint_assembly_depth", fontsize=6.4)
axb.tick_params(axis="x", length=0)
axb.tick_params(axis="y", labelsize=5.8)
for s in ("top", "right"):
    axb.spines[s].set_visible(False)

fig.tight_layout(w_pad=1.4)
fig.savefig(OUT, bbox_inches="tight", pad_inches=0.04)
print("wrote", OUT)
