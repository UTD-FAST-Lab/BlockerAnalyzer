#!/usr/bin/env python3
"""Publication Heatmap A: mechanism category (rows, grouped by family) x fuzzer
(cols) resolve-rate. Outputs vector PDF + PNG to out/rq3/."""
import json, csv, collections, argparse
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parent.parent
FUZZERS = ["aflplusplus", "honggfuzz", "libfuzzer", "libafl"]
FZ_DISP = ["AFL++", "honggfuzz", "libFuzzer", "LibAFL$^\\dagger$"]
TAU = 0.8
ap = argparse.ArgumentParser()
ap.add_argument("--resolve", default=str(ROOT / "csvs/rq3_resolve.csv"))
A = ap.parse_args()

FAMILY = {
    'i2s_string_literal_substitution': 'I2S-pro', 'i2s_numeric_tag_substitution': 'I2S-pro',
    'i2s_structural_assembly_reach_depth': 'I2S-pro', 'i2s_operand_value_precision': 'I2S-pro',
    'i2s_relational_collision_gate': 'I2S-pro',
    'i2s_anti_target_depletion': 'I2S-anti', 'i2s_anti_decoy_overfit': 'I2S-anti',
    'i2s_anti_structural_byte_corruption': 'I2S-anti',
    'vp_gradient_value_distance_closure': 'VP-pro', 'vp_gradient_drives_assembly_depth': 'VP-pro',
    'vp_operand_byte_enrichment': 'VP-pro', 'vp_admits_structurally_richer_corpus': 'VP-pro',
    'joint_assembly_depth': 'JOINT', 'vpc_anti_depth_diversion': 'VPC-anti',
    'ctx_iteration_path_depth': 'ctx-cov', 'ctx_corpus_inflation': 'ctx-cov',
    'ngram_sequential_depth_reach': 'ngram', 'grimoire_structural_token_assembly': 'grimoire',
    'grimoire_structural_size_depth': 'grimoire',
}
FAM_ORDER = ['I2S-pro', 'I2S-anti', 'VP-pro', 'JOINT', 'VPC-anti', 'ctx-cov', 'ngram', 'grimoire']
DISP = {
    'i2s_string_literal_substitution': 'string-literal substitution',
    'i2s_numeric_tag_substitution': 'numeric-tag substitution',
    'i2s_structural_assembly_reach_depth': 'structural assembly / reach-depth',
    'i2s_operand_value_precision': 'operand value-precision',
    'i2s_relational_collision_gate': 'relational collision gate',
    'i2s_anti_target_depletion': 'target depletion (decoy operand)',
    'i2s_anti_decoy_overfit': 'decoy overfit (energy diversion)',
    'i2s_anti_structural_byte_corruption': 'structural byte corruption',
    'vp_gradient_value_distance_closure': 'gradient value-distance closure',
    'vp_gradient_drives_assembly_depth': 'gradient drives assembly depth',
    'vp_operand_byte_enrichment': 'operand byte enrichment',
    'vp_admits_structurally_richer_corpus': 'admits richer corpus',
    'joint_assembly_depth': 'assembly depth (I2S$\\times$VP)',
    'vpc_anti_depth_diversion': 'depth diversion',
    'ctx_iteration_path_depth': 'iteration / path depth',
    'ctx_corpus_inflation': 'corpus inflation',
    'ngram_sequential_depth_reach': 'sequential depth reach',
    'grimoire_structural_token_assembly': 'structural token assembly',
    'grimoire_structural_size_depth': 'structural size depth',
}

lab = {}
for l in open(ROOT / "bench/dataset.jsonl"):
    r = json.loads(l)
    if r.get("evidence", {}).get("status") != "validated":
        continue
    lab[(r["target"], r["branch_id"])] = r["mechanism"].get("canonical_label") or r["mechanism"].get("label")

rows = collections.defaultdict(dict)
for r in csv.DictReader(open(A.resolve)):
    k = (r["target"], int(r["branch_id"]))
    rows[k][r["fuzzer"]] = (int(r["n_resolved"]), int(r["n_blocked"]), int(r["n_reached"]))

def resolved(k, f):
    if k not in rows or f not in rows[k]:
        return None
    nr, nb, nrch = rows[k][f]
    if nrch == 0:
        return None
    return (nr / (nr + nb) if nr + nb > 0 else 0) >= TAU

CATS = sorted(set(lab.values()), key=lambda c: (FAM_ORDER.index(FAMILY[c]), -sum(1 for k in lab if lab[k] == c)))
M = np.full((len(CATS), len(FUZZERS)), np.nan)
N = np.zeros(len(CATS), int)
for i, c in enumerate(CATS):
    ks = [k for k in lab if lab[k] == c and resolved(k, "libafl") is not None]
    N[i] = len(ks)
    for j, f in enumerate(FUZZERS):
        if ks:
            M[i, j] = np.mean([1.0 if resolved(k, f) else 0.0 for k in ks])

fig, ax = plt.subplots(figsize=(6.4, 8.2))
im = ax.imshow(np.ma.masked_invalid(M), cmap="YlGnBu", vmin=0, vmax=1, aspect="auto")
ax.set_xticks(range(len(FUZZERS)))
ax.set_xticklabels(FZ_DISP, fontsize=10)
ax.xaxis.set_ticks_position("top")
ax.set_yticks(range(len(CATS)))
ax.set_yticklabels([f"{DISP[c]}  (n={N[i]})" for i, c in enumerate(CATS)], fontsize=8.5)
for i in range(len(CATS)):
    for j in range(len(FUZZERS)):
        v = M[i, j]
        if np.isnan(v):
            ax.text(j, i, "n/a", ha="center", va="center", color="grey", fontsize=8)
        else:
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8.5,
                    color="white" if v > 0.55 else "black")
# family dividers + labels
bounds, cur, start = [], FAMILY[CATS[0]], 0
fams = [FAMILY[c] for c in CATS]
for i in range(1, len(CATS) + 1):
    if i == len(CATS) or fams[i] != fams[i - 1]:
        bounds.append((start, i - 1, fams[start]))
        if i < len(CATS):
            ax.axhline(i - 0.5, color="black", lw=1.6)
        start = i
for s, e, fam in bounds:
    ax.text(-0.62, (s + e) / 2, fam, rotation=90, va="center", ha="center",
            fontsize=8.5, fontweight="bold")
ax.set_xlim(-0.5, len(FUZZERS) - 0.5)
cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
cb.set_label("resolve-rate  (frac. of category's blockers resolved, $\\geq$8/10 trials)", fontsize=8.5)
ax.set_title("Per-mechanism resolve-rate across four fuzzing engines\n"
             "(8 targets, 382 validated blockers)", fontsize=10.5, pad=26)
fig.tight_layout()
outdir = ROOT / "out/rq3/coverage_plots"; outdir.mkdir(parents=True, exist_ok=True)
for ext in ("pdf", "png"):
    out = outdir / f"rq3_heatmapA_pub.{ext}"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"wrote {out}")
