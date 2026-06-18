ROUND re-design (loop-until-dry) for decisive shape **i2s_vp__WLW**. Overwrite `step5b_new_v3/i2s_vp__WLW/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp__WLW/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (12 decisive branches: 8 confirmed, 4 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 6x  decoy_overcommit_wrong_literal
  - 2x  vpc_corpus_shallower_context_reach

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - bloaty/301  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - lcms/2137  [rule_not_met]  tested: 1/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/4072  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5865  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=decoy_overcommit_wrong_literal tool=operand_enrichment decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: vpc's I2S substitution pins the corpus to a WRONG decoy literal (sibling case / enumerated case / valid-range boundary), flooding the loser corpus with a value that blocks the target arm
      rule: "decoy_enrich > 0.8 AND signed_target_enrich < 0.3"
  - id=vp_gradient_reaches_exact_literal_i2s_stalls_short tool=value_distance_reached decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: value_profile's CMP_MAP Hamming gradient lands ON the exact 4-byte switch-case codepoint while vpc's added I2S stage diverts mutation onto sibling operands and never closes the last bits to the exact 
      rule: "winner_closer == true AND distance_gap > 0.15 AND vp_min_distance < 0.1"
  - id=vpc_corpus_shallower_context_reach tool=depth_reach decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: vpc's I2S substitution pulls the loser corpus toward shallow / degenerate inputs that never DRIVE THE CALL CHAIN to the deep shaping context where the gate is dispatched; vp's gradient-grown corpus re
      rule: "winner_deeper == true AND depth_lift >= 1.5"

Built tools ALREADY used by the prior test: ['depth_reach', 'operand_enrichment', 'value_distance_reached'].
Built tools NOT yet tried here (likely pivots): ['joint_necessity/struct_size_and_token_count', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.