#!/usr/bin/env python3
"""plot_rq3_heatmaps.py — RQ3 mechanism heatmaps + ranking decomposition.

Goal: explain WHY one engine beats another on a target, by decomposing
per-target performance into  (fuzzer strength per category) x (target's category
composition).

Outputs (out/rq3/):
  A  rq3_heat_fuzzer_x_category.png  — resolve-rate, 4 fuzzers x 13 categories
  B  rq3_heat_target_x_category.png  — composition (share within target), targets x 13 cats
  C  rq3_heat_target_x_fuzzer.png    — actual per-target resolve-rate (the ranking)
Plus a printed predicted-vs-actual ranking check (s4 targets, where fuzzer data exists).
"""
import json, csv, collections, argparse
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FUZZERS = ["aflplusplus", "honggfuzz", "libfuzzer", "libafl"]
TAU = 0.8
_ap = argparse.ArgumentParser()
_ap.add_argument("--resolve", default=str(ROOT / "csvs/rq3_resolve.csv"))
ARGS = _ap.parse_args()

# category -> family (current 13-category / merged taxonomy; uppercase paper codes)
FAMILY = {
    'i2s_string_literal_substitution': 'I2S-P', 'i2s_numeric_tag_substitution': 'I2S-P',
    'i2s_anti_target_depletion': 'I2S-A', 'i2s_anti_decoy_overfit': 'I2S-A',
    'i2s_anti_structural_byte_corruption': 'I2S-A',
    'vp_gradient_value_distance_closure': 'VP-P', 'vp_gradient_assembly_depth': 'VP-P',
    'joint_value_distance_closure': 'VPC-P', 'joint_assembly_depth': 'VPC-P',
    'ctx_iteration_path_depth': 'CTX-P', 'ctx_inflation': 'CTX-A',
    'grimoire_structural_assembly': 'GRIM-P', 'ngram_sequential_depth_reach': 'NGRAM-P',
}
FAM_ORDER = ['I2S-P', 'I2S-A', 'VP-P', 'VPC-P', 'CTX-P', 'CTX-A', 'GRIM-P', 'NGRAM-P']

# ---- load labels (canonical_label = final-19) and target ----
lab, tgt = {}, {}
for l in open(ROOT / "bench/dataset.jsonl"):
    r = json.loads(l)
    if r.get("evidence", {}).get("status") != "validated":
        continue
    k = (r["target"], r["branch_id"])
    lab[k] = r["mechanism"].get("canonical_label") or r["mechanism"].get("label")
    tgt[k] = r["target"]

# ---- resolve outcomes ----
rows = collections.defaultdict(dict)
for r in csv.DictReader(open(ARGS.resolve)):
    k = (r["target"], int(r["branch_id"]))
    rows[k][r["fuzzer"]] = (int(r["n_resolved"]), int(r["n_blocked"]), int(r["n_reached"]))

def resolved(k, f):
    if k not in rows or f not in rows[k]:
        return None
    nr, nb, nrch = rows[k][f]
    if nrch == 0:
        return None
    return (nr / (nr + nb) if nr + nb > 0 else 0) >= TAU

CATS = sorted(set(lab.values()), key=lambda c: (FAM_ORDER.index(FAMILY[c]), c))
ALL_TARGETS = sorted(set(tgt.values()))
# targets that actually have RQ3 fuzzer resolve data (any measured branch)
_have = {tgt[k] for k in lab if any(k in rows and f in rows[k] and rows[k][f][2] > 0 for f in FUZZERS)}
S4 = [t for t in ALL_TARGETS if t in _have]

# ===== matrix A: fuzzer x category resolve-rate (over measured branches) =====
A = np.full((len(FUZZERS), len(CATS)), np.nan)
An = np.zeros(len(CATS), dtype=int)
for j, c in enumerate(CATS):
    ks = [k for k in lab if lab[k] == c and resolved(k, "libafl") is not None]
    An[j] = len(ks)
    for i, f in enumerate(FUZZERS):
        if ks:
            A[i, j] = np.mean([1.0 if resolved(k, f) else 0.0 for k in ks])

# ===== matrix B: target x category composition (count + within-target share) =====
comp = collections.defaultdict(lambda: collections.Counter())
for k in lab:
    comp[tgt[k]][lab[k]] += 1
B_cnt = np.zeros((len(ALL_TARGETS), len(CATS)), dtype=int)
for i, t in enumerate(ALL_TARGETS):
    for j, c in enumerate(CATS):
        B_cnt[i, j] = comp[t][c]
B_share = B_cnt / B_cnt.sum(axis=1, keepdims=True).clip(min=1)

# ===== matrix C: target x fuzzer actual resolve-rate (s4 only) =====
C = np.full((len(S4), len(FUZZERS)), np.nan)
for i, t in enumerate(S4):
    ks = [k for k in lab if tgt[k] == t and resolved(k, "libafl") is not None]
    for jf, f in enumerate(FUZZERS):
        if ks:
            C[i, jf] = np.mean([1.0 if resolved(k, f) else 0.0 for k in ks])

def short(c):
    return c.replace("i2s_", "i2s·").replace("vp_", "vp·").replace("structural_", "struct_")

def heat(mat, rlabels, clabels, title, fname, fmt="{:.2f}", cmap="YlOrRd",
         vmax=1.0, ann2=None, figsize=None):
    fig, ax = plt.subplots(figsize=figsize or (max(8, len(clabels) * 0.55 + 3), len(rlabels) * 0.5 + 2))
    m = np.ma.masked_invalid(mat)
    im = ax.imshow(m, cmap=cmap, vmin=0, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(clabels)))
    ax.set_xticklabels(clabels, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(rlabels)))
    ax.set_yticklabels(rlabels, fontsize=8)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = mat[i, j]
            if np.isnan(v):
                ax.text(j, i, "·", ha="center", va="center", color="grey", fontsize=8)
                continue
            txt = fmt.format(v)
            if ann2 is not None:
                txt += f"\n{ann2[i, j]}"
            ax.text(j, i, txt, ha="center", va="center", fontsize=7,
                    color="black" if v < 0.6 * vmax else "white")
    ax.set_title(title, fontweight="bold", fontsize=11)
    fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    fig.tight_layout()
    outdir = ROOT / "out/rq3/coverage_plots"; outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / fname
    fig.savefig(out, dpi=140)
    print(f"wrote {out}")

clabels = [short(c) for c in CATS]
clabels_n = [f"{short(c)}\n(n={An[j]})" for j, c in enumerate(CATS)]

# A
heat(A, FUZZERS, clabels_n,
     "RQ3-A  fuzzer × mechanism category — resolve-rate (frac of branches resolved, ≥8/10 trials)",
     "rq3_heat_fuzzer_x_category.png", figsize=(13, 4.2))
# B (color = within-target share, annot = raw count)
heat(B_share, ALL_TARGETS, clabels,
     "RQ3-B  target × mechanism category — composition (color=share of target's blockers, n=count)",
     "rq3_heat_target_x_category.png", fmt="{:.0%}", cmap="Blues", vmax=0.6,
     ann2=B_cnt.astype(int).astype(str), figsize=(13, 5))
# C
heat(C, S4, FUZZERS,
     "RQ3-C  target × fuzzer — actual resolve-rate (the per-target ranking)",
     "rq3_heat_target_x_fuzzer.png", cmap="YlGnBu", figsize=(7, 3.6))

# ===== decomposition check: does (B composition) x (global A strength) predict C? =====
print("\n=== Ranking decomposition (s4 targets): predicted = Σ_c share[t,c]·rate_global[f,c] ===")
global_rate = {f: {c: A[FUZZERS.index(f), CATS.index(c)] for c in CATS} for f in FUZZERS}
for t in S4:
    ks = [k for k in lab if tgt[k] == t and resolved(k, "libafl") is not None]
    n = len(ks)
    comp_t = collections.Counter(lab[k] for k in ks)
    print(f"\n{t} (n={n}):")
    print(f"  {'fuzzer':12} {'actual':>7} {'predicted':>10}")
    act, pred = {}, {}
    for f in FUZZERS:
        a = np.mean([1.0 if resolved(k, f) else 0.0 for k in ks]) if ks else float("nan")
        p = sum((comp_t[c] / n) * (global_rate[f][c] if not np.isnan(global_rate[f][c]) else 0) for c in comp_t)
        act[f], pred[f] = a, p
        print(f"  {f:12} {a:>7.2f} {p:>10.2f}")
    ra = [f for f, _ in sorted(act.items(), key=lambda x: -x[1])]
    rp = [f for f, _ in sorted(pred.items(), key=lambda x: -x[1])]
    print(f"  actual rank : {' > '.join(ra)}")
    print(f"  predicted   : {' > '.join(rp)}   {'MATCH' if ra == rp else 'differ'}")
