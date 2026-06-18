ROUND re-design (loop-until-dry) for decisive shape **i2s_vp__LW_**. Overwrite `step5b_new_v3/i2s_vp__LW_/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp__LW_/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (3 decisive branches: 0 confirmed, 3 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  (none — this shape has 0 confirmed branches; round-0 may have under-explored it)

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - libxml2/6193  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/8138  [rule_not_met]  tested: 1/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/9435  [rule_not_met]  tested: 1/3 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=i2s_multibyte_literal_splice_vp_gradient_blind tool=operand_enrichment decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: vpc's I2S enriches the exact multibyte literal in its corpus; value_profile's gradient does not
      rule: "signed_target_enrich > 0 AND decoy_enrich < 0.5"
  - id=i2s_lands_literal_vp_gradient_stalls_distance tool=value_distance_reached decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: vpc's I2S lands AT the exact multibyte literal; value_profile's Hamming gradient stalls a measurable distance short of it
      rule: "winner_closer == true AND distance_gap >= 0.2 AND vpc_min_distance <= 0.05"
  - id=i2s_xmlns_token_present_vp_corpus_lacks tool=joint_necessity decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: the 'xmlns' attribute-name token appears in vpc's resolving corpus but is absent/depleted in value_profile's blocking corpus
      rule: "vpc_tags >= 1 AND vp_tags < 0.3 AND tag_lift >= 2.0"

Built tools ALREADY used by the prior test: ['joint_necessity', 'operand_enrichment', 'value_distance_reached'].
Built tools NOT yet tried here (likely pivots): ['depth_reach', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.