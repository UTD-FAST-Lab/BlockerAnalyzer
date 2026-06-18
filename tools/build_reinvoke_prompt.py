#!/usr/bin/env python3
"""tools/build_reinvoke_prompt.py — assemble the STANDARDIZED re-invoke prompt for
the evidence-test-author (design) agent, for ONE decisive-shape, during a
re-design round of the loop-until-dry labeling loop (benchmark pivot).

WHY a fixed assembler (vs a hand-written prompt): the re-invoke logic differs from
the first invoke and must be IDENTICAL across shapes for reproducibility (a paper
methods requirement). It encodes the loop invariants:

  - TARGET = the shape's UNLABELED decisive branches only (already-confirmed
    branches are FROZEN; their hypotheses are carried forward = monotonic superset).
  - NOVELTY (G1): propose mechanisms NOT already refuted for the unlabeled branches;
    each must be falsifiable AND discriminating. Re-testing a refuted mechanism with
    a relaxed threshold is forbidden (that is chasing-100%).
  - SUPERSET: keep every prior hypothesis that confirmed >=1 branch, verbatim.
  - G3: an honest `decidable:false` / inconclusive for a genuinely non-discriminable
    sub-group is a CORRECT outcome — do not invent a mechanism to force a label.
  - Cross-server: do NOT mark a branch decidable:false merely because its corpus is
    absent on this server; design tests valid for ALL branches (the owning server
    arbitrates its own targets).

Reads (all shared, server-agnostic):
  step5b_new_v3/<shape>/evidence_test.json   — the most-recent prior test (hyps to avoid)
  bench/dataset.jsonl                         — per-branch confirmed/unlabeled split + diag
Writes the assembled prompt to stdout (or --out FILE).

Usage:
  python3 tools/build_reinvoke_prompt.py --shape i2s_vp_WLWL
  python3 tools/build_reinvoke_prompt.py --shape i2s_vp_WLWL --out /tmp/p.md
"""
import argparse, json, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILT_TOOLS = ("value_distance_reached", "depth_reach", "operand_enrichment",
               "joint_necessity", "corpus_size_ratio", "token_count", "byte_freq_ratio",
               "struct_size_and_token_count")


def load_shape_rows(shape):
    ss = f"step5b_new_v3/{shape}/evidence_test.json"
    out = []
    for l in open(ROOT / "bench" / "dataset.jsonl"):
        r = json.loads(l)
        if (r.get("mechanism") or {}).get("shape_source") == ss:
            out.append(r)
    return out


def prior_hypotheses(shape):
    p = ROOT / "step5b_new_v3" / shape / "evidence_test.json"
    if not p.exists():
        return []
    et = json.load(open(p))
    hs = []
    for h in et.get("hypotheses", []):
        m = h.get("measurement") or {}
        desc = (m.get("descriptor") or {})
        tool = m.get("registry_tool") or desc.get("compute") or "?"
        hs.append({"id": h.get("id"), "label": (h.get("label") or "")[:200],
                   "tool": tool, "decidable": h.get("decidable"),
                   "rule": json.dumps(h.get("rule"))[:200]})
    return hs


def build(shape):
    rows = load_shape_rows(shape)
    confirmed = [r for r in rows if (r.get("mechanism") or {}).get("label")]
    unlabeled = [r for r in rows if not (r.get("mechanism") or {}).get("label")]
    priors = prior_hypotheses(shape)
    used = sorted({h["tool"] for h in priors if h["tool"] in BUILT_TOOLS})
    untried = [t for t in ("operand_enrichment/byte_freq_ratio",
                           "joint_necessity/struct_size_and_token_count",
                           "value_distance_reached", "depth_reach",
                           "corpus_size_ratio", "token_count")
               if not any(u in t for u in used)]

    L = []
    L.append(f"ROUND re-design (loop-until-dry) for decisive shape **{shape}**. "
             f"Overwrite `step5b_new_v3/{shape}/evidence_test.json` "
             f"(the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).")
    L.append("")
    L.append(f"Read your standard inputs: `step5a_new_v3/{shape}/{{signatures.json,cards.json}}` "
             f"and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).")
    L.append("")
    L.append(f"## Shape state ({len(rows)} decisive branches: {len(confirmed)} confirmed, {len(unlabeled)} UNLABELED)")
    L.append("")
    L.append("### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)")
    bylabel = collections.Counter((r.get("mechanism") or {}).get("label") for r in confirmed)
    if bylabel:
        for lab, n in bylabel.most_common():
            L.append(f"  - {n}x  {lab}")
    else:
        L.append("  (none — this shape has 0 confirmed branches; round-0 may have under-explored it)")
    L.append("")
    L.append("### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)")
    for r in unlabeled:
        ev = r.get("evidence") or {}
        k = (ev.get("diag") or {}).get("kind")
        L.append(f"  - {r['target']}/{r['branch_id']}  [{k}]  {str(ev.get('reason'))[:90]}")
    L.append("")
    L.append("## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)")
    for h in priors:
        keep = " <- KEEP (confirmed >=1 branch; carry forward in your superset)" if h["decidable"] is not False else ""
        L.append(f"  - id={h['id']} tool={h['tool']} decidable={h['decidable']}{keep}")
        L.append(f"      label: {h['label']}")
        L.append(f"      rule: {h['rule']}")
    L.append("")
    L.append(f"Built tools ALREADY used by the prior test: {used or '(none)'}.")
    L.append(f"Built tools NOT yet tried here (likely pivots): {untried or '(all tried)'}.")
    L.append("")
    L.append("## Rules for this re-design")
    L.append("1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, "
             "so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.")
    L.append("2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted "
             "for these branches — falsifiable AND discriminating (rules out the obvious alternative). "
             "Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.")
    L.append("3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, "
             "mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a "
             "mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)")
    L.append("4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the "
             "running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; "
             "respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; "
             "I2S is not lineage-tagged; value_profile is a feedback not a mutator).")
    L.append("5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, "
             "fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, "
             "and any sub-group you judge honestly `decidable:false`.")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--shape", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    txt = build(a.shape)
    if a.out:
        Path(a.out).write_text(txt)
        print(f"wrote {a.out} ({len(txt)} chars)")
    else:
        print(txt)


if __name__ == "__main__":
    main()
