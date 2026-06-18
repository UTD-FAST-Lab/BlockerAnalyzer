ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_L_WL**. Overwrite `step5b_new_v3/i2s_vp_L_WL/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_L_WL/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (14 decisive branches: 5 confirmed, 9 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 5x  vp_gradient_value_distance_climb

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - libpng/3999  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6649  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=20
  - libxml2/6654  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=3,
  - libxml2/6673  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6696  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6726  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7352  [seed_starved]  unscorable: insufficient seeds (W=2, L=28; need >=3 each) -> rank-10 re-bisect candidate
  - libxml2/7451  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=8,
  - libxml2/7459  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=9,

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=vp_gradient_value_distance_climb tool=value_distance_reached decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: vpc's CMP_MAP gradient ratchets the corpus byte-by-byte toward a CONCRETE literal token that cmplog's edge-only signal cannot bank near-miss progress toward
      rule: "distance_gap >= 0.25 AND w_min_hamming_to_literal <= 0.30"
  - id=vp_gradient_structural_depth_assembly tool=depth_reach decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: vpc's CMP_MAP gradient accumulates partial credit across chained comparisons to drive the corpus to a structurally DEEPER parse state (multi-child content model / namespace binding / internal subset /
      rule: "depth_lift >= 1.5 AND w_depth > l_depth"

Built tools ALREADY used by the prior test: ['depth_reach', 'value_distance_reached'].
Built tools NOT yet tried here (likely pivots): ['operand_enrichment/byte_freq_ratio', 'joint_necessity/struct_size_and_token_count', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.