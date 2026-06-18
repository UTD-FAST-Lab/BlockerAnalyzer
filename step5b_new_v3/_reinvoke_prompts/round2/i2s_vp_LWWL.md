ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_LWWL**. Overwrite `step5b_new_v3/i2s_vp_LWWL/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_LWWL/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (17 decisive branches: 1 confirmed, 16 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 1x  vp_gradient_scalar_operand_distance

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - lcms/2143  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6436  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=4,
  - libxml2/6466  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6687  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=4,
  - libxml2/6924  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6925  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6926  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=23
  - libxml2/6948  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=18
  - libxml2/7143  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=10
  - libxml2/7317  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=21
  - sqlite3/14475  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=14
  - sqlite3/14479  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=14
  - sqlite3/14589  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=9,
  - sqlite3/14623  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=19
  - sqlite3/14675  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=18
  - sqlite3/14765  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=18

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=vp_gradient_scalar_operand_distance tool=value_distance_reached decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: value_profile's CMP_MAP gradient lands its corpus closer to a FIXED scalar gate operand than cmplog/naive get -- the genuine value-distance subtype, restricted to the one gate that has an extractable 
      rule: "winner_closer == true AND distance_gap >= 0.25 AND cmp_min_distance >= 0.40"
  - id=vp_gradient_structural_depth tool=depth_reach decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: value_profile's gradient-built corpus reaches a DEEPER parse/codegen state along the gating call-chain than cmplog/naive -- the structural/derived/grammar subtype where the gate is a parse DEPTH, not 
      rule: "winner_deeper == true AND depth_lift >= 1.5 AND side_lift >= 1.5"

Built tools ALREADY used by the prior test: ['depth_reach', 'value_distance_reached'].
Built tools NOT yet tried here (likely pivots): ['operand_enrichment/byte_freq_ratio', 'joint_necessity/struct_size_and_token_count', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.