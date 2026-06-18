ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_WLWL**. Overwrite `step5b_new_v3/i2s_vp_WLWL/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_WLWL/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (106 decisive branches: 85 confirmed, 21 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 73x  i2s_fixed_offset_literal_value_gate
  - 10x  i2s_planted_anchor_literal_presence_scaffold_gate
  - 2x  i2s_structural_assembly_reach_depth_gate

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - bloaty/141  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - lcms/2226  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - lcms/2330  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/3877  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/3896  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/3980  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/4006  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/4031  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/4039  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6381  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/129  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/19  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/22  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/23  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/298  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/322  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/422  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/470  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/567  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/73  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5560  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=i2s_fixed_offset_literal_value_gate tool=operand_enrichment decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: cmplog (I2S) substitutes a logged CMP literal at a fixed gate offset, so its corpus is enriched in the target value at that offset relative to naive; value_profile/naive cannot synthesize the exact li
      rule: "signed_target_enrich >= 0.8"
  - id=i2s_planted_anchor_literal_presence_scaffold_gate tool=token_count decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: I2S splices one or more logged CMP anchor literals (URL scheme '://', 'HTTP/'/'HTTP/2', header names, protocol tokens 'pop3', chunk-type FOURCCs 'IDAT'/'sRGB'/'eXIf'/'sCAL'/'tIME', OpenType table tags
      rule: "winner_literal_count >= 1.0 AND literal_presence_ratio <= 0.34"
  - id=i2s_structural_assembly_reach_depth_gate tool=depth_reach decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: I2S does NOT just plant one token — it assembles a MULTI-FIELD structure (a full scheme://host:port URL + 'HTTP/' version line that seats a cached connection; a complete sfnt header + table-directory 
      rule: "depth_lift >= 2.0 AND side_lift >= 3.0 AND winner_deeper == true"
  - id=i2s_derived_state_no_recoverable_literal_no_cov_image tool=depth_reach decidable=False
      label: The blocked branch is a DERIVED-state / structural-chain condition (lcms tone-curve float magnitude over 131072.0; lcms deep LUT-A2B NULL guard reached only by traversing a multi-FOURCC chain; lcms di
      rule: "decidable:false"

Built tools ALREADY used by the prior test: ['depth_reach', 'operand_enrichment', 'token_count'].
Built tools NOT yet tried here (likely pivots): ['value_distance_reached', 'corpus_size_ratio'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.