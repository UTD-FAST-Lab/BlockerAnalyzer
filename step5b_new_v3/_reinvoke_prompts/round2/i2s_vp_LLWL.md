ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_LLWL**. Overwrite `step5b_new_v3/i2s_vp_LLWL/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_LLWL/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (23 decisive branches: 13 confirmed, 10 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 6x  joint_value_precision
  - 6x  joint_assembly_depth
  - 1x  joint_value_gradient_closure

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - lcms/2107  [rule_not_met]  tested: 1/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - lcms/2184  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - lcms/2196  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - lcms/2209  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6414  [rule_not_met]  tested: 1/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/8161  [rule_not_met]  tested: 1/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5609  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5614  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5616  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5980  [rule_not_met]  tested: 1/3 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=joint_assembly_depth tool=joint_necessity decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: vpc assembles a LARGER, multi-field structure than I2S-only (cmplog) ever reaches; the gradient is necessary to grow size/token-count past where exact substitution stalls, and I2S is necessary because
      rule: "vp_tags < 0.3 AND size_lift >= 1.3"
  - id=joint_value_precision tool=value_distance_reached decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: vpc and cmplog reach a SIMILARLY-sized structure (size_lift ~ 1, sometimes vpc smaller), but vpc places a specific gradient-climbed VALUE that the cmplog-blocking seeds approach yet never reach; I2S i
      rule: "size_lift < 1.3 AND cmp_min_distance > 0 AND distance_closure_ratio >= 0.5"
  - id=joint_value_gradient_closure tool=value_distance_reached decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: NEW (round 1). The cmplog-BLOCKING arm reaches a value that is STRICTLY CLOSER to the gate operand than naive/value_profile but still NON-zero, while the vpc-RESOLVING arm lands it (distance ~ 0): the
      rule: "winner_closer == true AND cmp_min_distance > 0 AND distance_closure_ratio >= 0.34"
  - id=joint_sequence_or_structural_nondiscriminable tool=value_distance_reached decidable=False
      label: NEW (round 1, honest inconclusive). Joint gates whose discriminating content is a CATEGORY-SEQUENCE / range gradient or a multi-token STRUCTURAL-PRESENCE condition with NO single fixed operand value t
      rule: "false"

Built tools ALREADY used by the prior test: ['joint_necessity', 'value_distance_reached'].
Built tools NOT yet tried here (likely pivots): ['operand_enrichment/byte_freq_ratio', 'depth_reach', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.