ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_W_WL**. Overwrite `step5b_new_v3/i2s_vp_W_WL/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_W_WL/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (56 decisive branches: 43 confirmed, 13 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 37x  i2s_fixed_offset_literal_substitution
  - 6x  i2s_structural_assembly_depth

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - libpng/3887  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/3892  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/3902  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/4051  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/4055  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/4061  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6205  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6359  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6597  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6930  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6946  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6976  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7250  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=i2s_fixed_offset_literal_substitution tool=operand_enrichment decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: I2S enriches the cmplog corpus with the exact CMP-target byte(s) at the gate offset (literal substitution), which naive's blind havoc cannot place
      rule: "signed_target_enrich >= 1.0"
  - id=i2s_structural_assembly_depth tool=depth_reach decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: I2S repairs interdependent multi-field structure (ELF section table / PNG iTXt chunk grammar / XML scheme+attribute parse) so the winner corpus drives the gated loop/branch line DEEPER per seed than t
      rule: "depth_lift >= 1.5 AND winner_deeper == true"
  - id=i2s_operand_reached_offset_agnostic tool=value_distance_reached decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: I2S plants the exact multi-byte CMP operand literal SOMEWHERE in the cmplog corpus (at a variable / floating chunk offset), so the I2S arm's seeds reach Hamming-distance ~0 to the operand anywhere in 
      rule: "winner_closer == true AND distance_closure_ratio >= 0.5 AND cmp_min_distance <= 0.1"

Built tools ALREADY used by the prior test: ['depth_reach', 'operand_enrichment', 'value_distance_reached'].
Built tools NOT yet tried here (likely pivots): ['joint_necessity/struct_size_and_token_count', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.