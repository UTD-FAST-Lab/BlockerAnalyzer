ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_LW_L**. Overwrite `step5b_new_v3/i2s_vp_LW_L/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_LW_L/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (7 decisive branches: 4 confirmed, 3 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 2x  vp_climbs_numeric_magnitude_to_threshold
  - 1x  vp_drives_parser_depth_into_structured_true_side
  - 1x  vp_enriches_fixed_offset_fourcc_operand

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - lcms/2446  [rule_not_met]  tested: 3/6 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6756  [rule_not_met]  tested: 6/6 rule(s) scored, none held (mechanism not supported by campaign data)
  - sqlite3/14777  [rule_not_met]  tested: 3/6 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=vp_admits_token_richer_structural_corpus tool=joint_necessity decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: value_profile's CMP_MAP gradient drives corpus admission toward structurally larger / more-token-rich seeds: the VP-RESOLVING corpus physically CONTAINS more of the gate's required structural tokens (
      rule: "tag_lift >= 1.0 OR size_lift >= 1.5"
  - id=vp_enriches_fixed_offset_fourcc_operand tool=operand_enrichment decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: for the fixed-offset FOURCC gate (lcms_2141 DeviceClass 'scnr' at offset 0x0c-0x0f, decoy 'mntr'), value_profile's gradient enriches the resolving corpus for the TARGET operand bytes relative to the D
      rule: "signed_target_enrich > 0 AND signed_target_enrich > decoy_enrich"
  - id=vp_drives_parser_depth_into_structured_true_side tool=depth_reach decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: NEW (round3): for the token-CLASS / structural-ENTRY gates that have NO single counted literal -- sqlite3_14777 (GetToken classifies a char into the token class whose true branch fires) and libxml2_67
      rule: "winner_deeper == true AND side_lift >= 2.0"
  - id=vp_climbs_numeric_magnitude_to_threshold tool=value_distance_reached decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: NEW (round3): lcms_2446 (TagCount > MAX_TABLE_TAG, inequality_or_range, derived_integer u32) -- value_profile's gradient drives the parsed numeric TagCount field MONOTONICALLY toward / across the MAX_
      rule: "winner_closer == true AND distance_gap > 0"
  - id=vp_gradient_assembles_multibyte_literal tool=value_distance_reached decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: value_profile-resolving seeds reach a multi-byte operator/keyword/structural LITERAL strictly closer than cmplog-blocking AND naive-blocking seeds; the operand is not a single spliceable constant, so 
      rule: "lit_dist_gap >= 1.0 AND vp_dist_frac <= 0.34 AND cmp_dist > vp_dist AND naive_dist > vp_dist"
  - id=vp_gradient_climbs_numeric_threshold tool=value_distance_reached decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: value_profile-resolving seeds drive a derived NUMERIC field past an inequality/range threshold; there is no exact literal to splice, so distance is the MAGNITUDE GAP to crossing the threshold -- vp cl
      rule: "vp_crossed_frac >= 0.5 AND mag_gap_lift > 0 AND cmp_gap > vp_gap AND naive_gap > vp_gap"

Built tools ALREADY used by the prior test: ['depth_reach', 'joint_necessity', 'operand_enrichment', 'value_distance_reached'].
Built tools NOT yet tried here (likely pivots): ['corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.