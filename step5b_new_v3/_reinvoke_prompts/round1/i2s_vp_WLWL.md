ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_WLWL**. Overwrite `step5b_new_v3/i2s_vp_WLWL/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_WLWL/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (106 decisive branches: 73 confirmed, 33 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 73x  i2s_fixed_offset_literal_value_gate

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - bloaty/141  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - lcms/2113  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - lcms/2226  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - lcms/2330  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/3877  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/3896  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/3980  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/4006  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/4031  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/4039  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6381  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/118  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/129  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/19  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/21  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/210  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/22  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/23  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/298  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/322  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/415  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/416  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/422  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/426  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/430  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/441  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/442  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/459  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/470  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/567  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/73  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5560  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/6236  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=i2s_fixed_offset_literal_value_gate tool=operand_enrichment decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: cmplog (I2S) substitutes a logged CMP literal at a fixed gate offset, so its corpus is enriched in the target value at that offset relative to naive; value_profile/naive cannot synthesize the exact li
      rule: "signed_target_enrich >= 0.8"
  - id=i2s_multi_literal_scaffold_state_gate tool=value_enrichment decidable=False
      label: I2S assembles two or more co-dependent, dispersed CMP literals (URL scheme+port+HTTP tokens; cookie/header chains; deep multi-field ICC structure) whose accumulated downstream program state, not the s
      rule: "any_anchor_token_enrich >= 0.8"

Built tools ALREADY used by the prior test: ['operand_enrichment'].
Built tools NOT yet tried here (likely pivots): ['joint_necessity/struct_size_and_token_count', 'value_distance_reached', 'depth_reach', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.