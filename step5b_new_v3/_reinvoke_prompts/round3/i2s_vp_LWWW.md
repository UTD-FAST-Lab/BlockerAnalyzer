ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_LWWW**. Overwrite `step5b_new_v3/i2s_vp_LWWW/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_LWWW/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (11 decisive branches: 8 confirmed, 3 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 7x  i2s_anti_structural_byte_corruption
  - 1x  vp_pro_cmpmap_gradient_rescue

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - libpng/3974  [rule_not_met]  tested: 5/5 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5977  [rule_not_met]  tested: 4/5 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5998  [rule_not_met]  tested: 4/5 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=i2s_anti_structural_byte_corruption tool=operand_enrichment decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: I2S RandReplace overwrites the exact structural/category/literal bytes naive havoc assembles, depleting (not enriching) the target byte in cmplog's corpus relative to naive
      rule: "signed_target_enrich < -0.3"
  - id=i2s_anti_no_input_preimage_misdirection tool=operand_enrichment decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: Gate has no input-side CMP preimage (category-table / state-machine classification, length threshold, or internally-derived overflow sentinel); I2S substitution finds no fixed-offset value to copy, so
      rule: "signed_target_enrich == no_gate_signature"
  - id=vp_pro_cmpmap_gradient_rescue tool=value_distance_reached decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: VP CMP_MAP Hamming/prefix-distance gradient gives graded partial-progress feedback toward the gate comparand, letting value_profile/vpc retain near-miss inputs that approach the target while cmplog's 
      rule: "winner_closer == true AND distance_gap >= 0.15"
  - id=i2s_anti_structural_token_content_starvation tool=joint_necessity decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: For the harfbuzz USE-shaper structural-assembly gates (5977 ZWNJ-plus-following-non-ignorable loop-exit; 5998 halant-bearing reorder syllable), the gate is reached only by a buffer carrying intact, re
      rule: "cmp_tags < 1 AND size_lift >= 1.3"
  - id=vp_pro_structural_token_content_climb tool=joint_necessity decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: For the same harfbuzz USE structural-assembly gates (5977/5998), value_profile's CMP_MAP gradient rewards partial progress toward the byte patterns selecting the ZWNJ-plus-non-ignorable / halant glyph
      rule: "tag_lift >= 1.3 AND size_lift >= 1.3"

Built tools ALREADY used by the prior test: ['joint_necessity', 'operand_enrichment', 'value_distance_reached'].
Built tools NOT yet tried here (likely pivots): ['depth_reach', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.