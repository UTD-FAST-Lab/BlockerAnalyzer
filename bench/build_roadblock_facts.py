#!/usr/bin/env python3
"""bench/build_roadblock_facts.py — the single deterministic FACT TABLE over all 558
roadblocks, from which every paper count is a transparent GROUP BY (no mixed bases).

One ROW per (branch, shape, family-membership). Columns:
  row_id, target, branch_id, shape, status, family, category, raw_category
where
  status   ∈ {validated, inconclusive}
  family   = the deterministic Layer-1 technique-direction (I2S-pro, VP-pro, I2S-anti,
             VPC-anti, JOINT, ctx, grimoire, ngram, calibrated_energy, aflfast, mopt),
             derived from the branch's covers_pairs (deciding pairs) — the SAME source
             for validated and inconclusive branches.
  category = the final canonical mechanism for validated rows; "inconclusive" otherwise.
  raw_category = the raw distilled label (mechanism.label); "-" for inconclusive.

A branch with two deciding-pair families (or two decisive shapes) legitimately gets
multiple rows. Distinct-branch counts (558 / 382 / 176) come from COUNT(DISTINCT
target,branch_id); membership counts come from row counts.

Outputs:
  bench/roadblock_facts.csv         — the table
  bench/roadblock_facts_README.md   — column semantics + every count as an exact query
"""
import json, glob, csv, collections, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DS = ROOT / "bench" / "dataset.jsonl"

# canonical_label -> paper family CODE (directional; validated rows: authoritative).
# VPC-A is MERGED into I2S-A (2026-06-23): adding I2S on top of value-profile and adding
# I2S on top of naive are one phenomenon -- "the I2S substitution backfires" -- separated only
# by which baseline cmplog/vpc loses to. The former vpc_anti_* categories were renamed to
# i2s_anti_* in canonical_label_map.json / branch_canonical_override.json.
FAMILY = {
    "i2s_string_literal_substitution": "I2S-P", "i2s_numeric_tag_substitution": "I2S-P",
    # i2s_operand_value_precision (2026-06-25) AND i2s_structural_assembly_reach_depth (2026-06-25)
    # both folded into i2s_string_literal_substitution -- dead keys removed. I2S-P = 2 categories.
    "vp_gradient_value_distance_closure": "VP-P", "vp_gradient_drives_assembly_depth": "VP-P",
    # vp_operand_byte_enrichment (2026-06-25, n=5) folded into vp_gradient_value_distance_closure
    # -- same VP gradient-to-operand mechanism, enrichment vs distance is just the measurement
    # route (fixed vs floating offset). Dead key removed. VP-P = 3 categories.
    "vp_admits_structurally_richer_corpus": "VP-P",
    "i2s_anti_target_depletion": "I2S-A", "i2s_anti_decoy_overfit": "I2S-A",
    "i2s_anti_structural_byte_corruption": "I2S-A",
    "joint_value_distance_closure": "VPC-P", "joint_assembly_depth": "VPC-P",
    "ctx_iteration_path_depth": "CTX-P", "ctx_corpus_inflation": "CTX-A",
    "ctx_depth_inflation": "CTX-A",
    "grimoire_structural_token_assembly": "GRIM-P", "grimoire_structural_size_depth": "GRIM-P",
    "ngram_sequential_depth_reach": "NGRAM-P",
}

# covers_pairs string -> paper family CODE (deciding-pair semantics). vp>vpc and cmplog>vpc
# (the old VPC-anti pairs) now route to I2S-A.
PAIR_FAMILY = {
    "cmplog>naive (I2S)": "I2S-P",
    "value_profile_cmplog>value_profile (I2S)": "I2S-P",
    "value_profile>naive (value_profile)": "VP-P",
    "value_profile_cmplog>cmplog (value_profile)": "VP-P",
    "naive>cmplog (I2S)": "I2S-A",
    "value_profile>value_profile_cmplog (I2S)": "I2S-A",        # merged (was VPC-anti)
    "cmplog>value_profile_cmplog (value_profile)": "I2S-A",     # merged (was VPC-anti)
    "naive_ctx>naive (ctx_coverage)": "CTX-P", "naive>naive_ctx (ctx_coverage)": "CTX-A",
    "grimoire>cmplog (grimoire_structural)": "GRIM-P",
    "cmplog>grimoire (grimoire_structural)": "GRIM-A",
    "naive_ngram4>naive (ngram_coverage)": "NGRAM-P", "naive>naive_ngram4 (ngram_coverage)": "NGRAM-A",
    "minimizer>naive (calibrated_energy)": "CALI-P",
    "minimizer>fast (aflfast_rarity)": "FAST-A", "fast>minimizer (aflfast_rarity)": "FAST-P",
    "naive>mopt (mopt_mutation)": "MOPT-A",
}


def families_from_pairs(pairs):
    """Deciding-pairs -> set of paper families. JOINT (synergy) override: vpc beats BOTH
    single arms (and neither single arm beats naive) -> resolves only under vpc."""
    P = set(pairs)
    vpc_beats_vp = "value_profile_cmplog>value_profile (I2S)" in P
    vpc_beats_cmp = "value_profile_cmplog>cmplog (value_profile)" in P
    single_beats_naive = ("cmplog>naive (I2S)" in P) or ("value_profile>naive (value_profile)" in P)
    if vpc_beats_vp and vpc_beats_cmp and not single_beats_naive:
        return {"VPC-P"}
    # VPC-A = symmetric mirror of VPC-P: both single arms resolve but the combined vpc
    # BLOCKS (vpc loses to BOTH) -> genuine anti-synergy. vp>vpc ALONE is just "I2S
    # backfires on VP" and routes to I2S-A via PAIR_FAMILY below.
    vp_beats_vpc = "value_profile>value_profile_cmplog (I2S)" in P
    cmp_beats_vpc = "cmplog>value_profile_cmplog (value_profile)" in P
    if vp_beats_vpc and cmp_beats_vpc:
        return {"VPC-A"}
    fams = set()
    for p in P:
        f = PAIR_FAMILY.get(p)
        if f:
            fams.add(f)
    return fams


def load_covers():
    """(target, branch_id, shape) -> set(covers_pairs), unioned across the branch's cards."""
    cov = collections.defaultdict(set)
    for cf in glob.glob(str(ROOT / "step5a_new_v3" / "*" / "cards.json")):
        data = json.load(open(cf))
        for c in (data if isinstance(data, list) else data.values()):
            shape = str(c.get("family", "")).replace("/", "_")
            key = (c.get("target"), c.get("branch_id"), shape)
            for p in c.get("covers_pairs", []):
                cov[key].add(p)
    return cov


# fallback shape decode for inc branches with no card (pure W/L pattern)
def decode_shape(shape):
    if not shape.startswith("i2s_vp_"):
        base = {"ctx_coverage": "CTX", "grimoire_structural": "GRIM", "ngram_coverage": "NGRAM",
                "calibrated_energy": "CALI", "aflfast_rarity": "FAST", "mopt_mutation": "MOPT"}
        b = base.get(shape.rsplit("_", 1)[0], shape.rsplit("_", 1)[0])
        return {f"{b}-{'P' if shape.endswith('_WL') else 'A'}"}
    c, v, p, n = shape.replace("i2s_vp_", "")
    if p == "W" and c == "L" and v == "L":
        return {"VPC-P"}
    if p == "L" and v == "W" and c == "W":     # vpc loses to BOTH single arms
        return {"VPC-A"}                        # symmetric anti-synergy mirror of VPC-P
    f = set()
    if c == "W" and n == "L": f.add("I2S-P")
    if p == "W" and v == "L": f.add("I2S-P")
    if v == "W" and n == "L": f.add("VP-P")
    if p == "W" and c == "L": f.add("VP-P")
    if n == "W" and c == "L": f.add("I2S-A")
    if v == "W" and p == "L": f.add("I2S-A")   # vp>vpc alone: I2S backfires on VP
    return f or {"?" + shape}


def main():
    cov = load_covers()
    # authoritative per-branch assignment round, reconstructed from the git boundaries
    # where evidence_test.r0/r1/r2.json were archived (start of each next round). See
    # bench/branch_assigned_round.json (built from those commit diffs).
    rnd_f = ROOT / "bench" / "branch_assigned_round.json"
    rounds = json.load(open(rnd_f)) if rnd_f.exists() else {}
    prov_f = ROOT / "bench" / "branch_first_validated.json"
    prov = json.load(open(prov_f)) if prov_f.exists() else {}
    rows = [json.loads(l) for l in open(DS)]
    facts = []
    mism = []
    used_fallback = 0
    for r in rows:
        t, bid, shape = r["target"], r["branch_id"], r["shape"]
        status = r["evidence"]["status"]
        canon = (r.get("mechanism") or {}).get("canonical_label")
        raw = (r.get("mechanism") or {}).get("label")
        key = (t, bid, shape)
        pair_fams = families_from_pairs(cov[key]) if key in cov else None
        if status == "validated":
            fam = FAMILY.get(canon, "?" + str(canon))
            # sanity: does the deciding-pair routing contain the canonical family?
            if pair_fams and fam not in pair_fams:
                mism.append((t, bid, shape, canon, fam, sorted(pair_fams)))
            rnd = rounds.get(f"{t}_{bid}", "?")   # authoritative git-boundary round
            pv = prov.get(f"{t}_{bid}", {})
            facts.append([t, bid, shape, status, fam, canon, raw or "-", rnd,
                          pv.get("date", "?")])
        else:
            fams = pair_fams or decode_shape(shape)
            if not pair_fams:
                used_fallback += 1
            for fam in sorted(fams):
                facts.append([t, bid, shape, status, fam, "inconclusive", "-", "-", "-"])
    facts.sort(key=lambda x: (x[0], x[1], x[2], x[4]))
    out = ROOT / "bench" / "roadblock_facts.csv"
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["row_id", "target", "branch_id", "shape", "status", "family",
                    "category", "raw_category", "assigned_round", "first_validated_date"])
        for i, f in enumerate(facts, 1):
            w.writerow([i] + f)
    # ---------- reconciliation report ----------
    F = facts
    dbranch = lambda rows_: len({(x[0], x[1]) for x in rows_})
    val = [x for x in F if x[3] == "validated"]
    inc = [x for x in F if x[3] == "inconclusive"]
    valbr = {(x[0], x[1]) for x in val}
    incbr_only = {(x[0], x[1]) for x in inc} - valbr
    R = []
    R.append("# Roadblock fact table — reconciliation\n")
    R.append(f"Source: `bench/dataset.jsonl` + deciding-pairs from `step5a_new_v3/*/cards.json`. "
             f"`bench/roadblock_facts.csv` has **{len(F)} rows** (one per branch×shape×family "
             f"membership).\n")
    R.append("Every paper number is a GROUP BY on this one table:\n")
    R.append("| quantity | query | value |")
    R.append("|---|---|--:|")
    R.append(f"| distinct roadblocks | COUNT(DISTINCT target,branch_id) | **{dbranch(F)}** |")
    R.append(f"| assigned roadblocks | DISTINCT branch WHERE any row status=validated | **{len(valbr)}** |")
    R.append(f"| inconclusive roadblocks | DISTINCT branch WHERE no row is validated | **{len(incbr_only)}** |")
    R.append(f"| assigned memberships | COUNT(rows WHERE status=validated) | {len(val)} |")
    R.append(f"| final categories | COUNT(DISTINCT category WHERE validated) | {len({x[5] for x in val})} |")
    R.append(f"| raw categories | COUNT(DISTINCT raw_category WHERE validated) | {len({x[6] for x in val})} |")
    R.append(f"| families (all) | COUNT(DISTINCT family) | {len({x[4] for x in F})} |")
    R.append(f"| families with an assigned branch | DISTINCT family WHERE validated | {len({x[4] for x in val})} |")
    R.append(f"| all decisive shapes | COUNT(DISTINCT shape) | {len({x[2] for x in F})} |")
    R.append(f"| shapes with an assigned branch | DISTINCT shape WHERE validated | {len({x[2] for x in val})} |")
    R.append(f"| inconclusive branch×shape axes | COUNT(DISTINCT branch,shape WHERE status=inconclusive) "
             f"| {len({(x[0],x[1],x[2]) for x in inc})} |")
    R.append("")
    R.append("## assigned branches per family (DISTINCT branch, status=validated)")
    R.append("| family | #assigned | #inconclusive |")
    R.append("|---|--:|--:|")
    af = collections.defaultdict(set); incf = collections.defaultdict(set)
    for x in val: af[x[4]].add((x[0], x[1]))
    for x in inc:   # per-family GROUP BY: every decisive-inconclusive branch in the family
        incf[x[4]].add((x[0], x[1]))
    order = ["I2S-P", "I2S-A", "VP-P", "VPC-P", "VPC-A", "CTX-P", "CTX-A", "GRIM-P", "GRIM-A",
             "NGRAM-P", "NGRAM-A", "CALI-P", "FAST-P", "FAST-A", "MOPT-A"]
    for fam in order:
        R.append(f"| {fam} | {len(af.get(fam,())) or '-'} | {len(incf.get(fam,())) or '-'} |")
    R.append(f"| **distinct total** | **{len({b for s in af.values() for b in s})}** "
             f"| **{len({b for s in incf.values() for b in s})}** |")
    R.append(f"| sum (memberships, dual-counted) | {sum(len(s) for s in af.values())} "
             f"| {sum(len(s) for s in incf.values())} |")
    # ---- assignment round (authoritative, from git round boundaries) ----
    R.append("")
    R.append("## assignment round (`assigned_round` column)")
    R.append("Reconstructed EXACTLY from git: the loop archived its hypothesis menu as "
             "`evidence_test.r0/r1/r2.json` at the start of each next round, so diffing the "
             "validated set across those boundary commits gives the per-round branch "
             "additions (`bench/branch_assigned_round.json`).")
    R.append("| round | new branches | cumulative |")
    R.append("|--:|--:|--:|")
    br_round = {}
    for x in val:
        k = (x[0], x[1]); rr = x[7]
        if k not in br_round or (isinstance(rr, int) and (not isinstance(br_round[k], int) or rr < br_round[k])):
            br_round[k] = rr
    bc = collections.Counter(br_round.values())
    cum = 0
    for rr in sorted(k for k in bc if isinstance(k, int)):
        cum += bc[rr]
        R.append(f"| R{rr} | {bc[rr]} | {cum} |")
    R.append("")
    R.append("`first_validated_date` column = the git commit date the branch first appeared "
             "as `validated` (`bench/branch_first_validated.json`), the underlying provenance.")
    R.append("")
    R.append("NOTE: the paper's earlier `tab:rounds` showed 330/358/384/393, but only R0 (330) "
             "and R3 (393, pre-multicat) were ever real — R1/R2 were `\\rndph` placeholders later "
             "filled with interpolated values. The authoritative curve above (329/355/373/382 "
             "distinct branches) is the reproducible replacement.")
    (ROOT / "bench" / "roadblock_facts_README.md").write_text("\n".join(R) + "\n")

    print(f"wrote {out} ({len(F)} rows)")
    print(f"  distinct {dbranch(F)} | assigned {len(valbr)} | inconclusive {len(incbr_only)}")
    print(f"  inc rows with no card -> shape-decode fallback: {used_fallback}")
    if mism:
        print(f"\n  !! {len(mism)} validated rows whose canonical family is NOT in the "
              f"deciding-pair routing (review):")
        for m in mism[:40]:
            print("    ", m)
    else:
        print("  OK: every validated row's canonical family is consistent with its deciding pairs")


if __name__ == "__main__":
    main()
