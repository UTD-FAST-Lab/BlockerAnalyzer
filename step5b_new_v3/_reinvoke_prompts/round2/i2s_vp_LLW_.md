ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_LLW_**. Overwrite `step5b_new_v3/i2s_vp_LLW_/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_LLW_/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (16 decisive branches: 10 confirmed, 6 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 9x  joint_value_precision
  - 1x  joint_assembly_depth

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - lcms/2674  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7296  [rule_not_met]  tested: 1/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7311  [rule_not_met]  tested: 1/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/9361  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/6858  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/7245  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=joint_assembly_depth tool=joint_necessity decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: vpc assembles a LARGER, multi-field structure than I2S-only (cmplog) ever reaches; the gradient is necessary to grow size/token-count past where exact substitution stalls, and I2S is necessary because
      rule: "vp_tags < 0.3 AND size_lift >= 1.3"
  - id=joint_value_precision tool=value_distance_reached decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: vpc and cmplog reach a SIMILARLY-sized input (size_lift ~ 1), but vpc lands a specific gradient-climbed VALUE (a single exact multi-byte keyword/token) that the cmplog-blocking seeds approach byte-by-
      rule: "size_lift < 1.3 AND cmp_min_distance > 0 AND distance_closure_ratio >= 0.5"
  - id=joint_numeric_header_convergence tool=value_distance_reached decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: NEW (round 1). The decisive divergence is on a DERIVED-INTEGER header/count field reached over a range/inequality gate (gid >= num_glyphs; glyf->get_path success on jointly-consistent offset/length dw
      rule: "size_lift < 1.3 AND vp_tags >= 0.3 AND cmp_min_distance > 0 AND distance_closure_ratio >= 0.5 AND winner_closer == true"
  - id=joint_grammar_state_path tool=? decidable=False
      label: NON-DISCRIMINABLE (honest inconclusive). The libxml2 automaton/grammar-state branches (if (to == NULL); nsNr != ctxt->nsNr) resolve because vpc reaches a NON-NULL automaton target state via a GRAMMAR-
      rule: "false"

Built tools ALREADY used by the prior test: ['joint_necessity', 'value_distance_reached'].
Built tools NOT yet tried here (likely pivots): ['operand_enrichment/byte_freq_ratio', 'depth_reach', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.