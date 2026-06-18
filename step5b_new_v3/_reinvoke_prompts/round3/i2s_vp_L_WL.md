ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_L_WL**. Overwrite `step5b_new_v3/i2s_vp_L_WL/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_L_WL/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (14 decisive branches: 7 confirmed, 7 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 5x  vp_gradient_value_distance_climb
  - 1x  vp_gradient_fixedoffset_byte_enrichment
  - 1x  vp_gradient_structural_depth_assembly

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - libxml2/6649  [rule_not_met]  tested: 3/5 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6654  [rule_not_met]  tested: 3/5 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6696  [rule_not_met]  tested: 4/5 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6726  [rule_not_met]  tested: 4/5 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7352  [rule_not_met]  tested: 2/5 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7451  [rule_not_met]  tested: 3/5 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7459  [rule_not_met]  tested: 3/5 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=vp_gradient_value_distance_climb tool=value_distance_reached decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: vpc's CMP_MAP gradient ratchets the corpus byte-by-byte toward a CONCRETE literal token that cmplog's edge-only signal cannot bank near-miss progress toward
      rule: "distance_gap >= 0.25 AND w_min_hamming_to_literal <= 0.30"
  - id=vp_gradient_structural_depth_assembly tool=depth_reach decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: vpc's CMP_MAP gradient accumulates partial credit across chained comparisons to drive the corpus to a structurally DEEPER parse state (multi-child content model / namespace binding / internal subset /
      rule: "depth_lift >= 1.5 AND w_depth > l_depth"
  - id=vp_gradient_fixedoffset_byte_enrichment tool=operand_enrichment decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: vpc's CMP_MAP gradient enriches the saved corpus with the target byte at a FIXED file offset on a single-byte enumerated-constant gate, where a Hamming-distance climb is degenerate (1-byte distance is
      rule: "signed_target_enrich >= 1.0 AND decoy_enrich < signed_target_enrich"
  - id=vp_gradient_structural_token_assembly tool=joint_necessity decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: vpc's CMP_MAP gradient assembles a LARGER, MORE structural-token-dense input than cmplog leaves behind, climbing a multi-token grammar (DTD content model / namespaced start-tag / interned attribute na
      rule: "size_lift >= 1.3 AND tag_lift > 0"
  - id=vp_gradient_literal_token_presence tool=token_count decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: vpc's CMP_MAP gradient assembles a DISTINCTIVE multi-byte gate keyword/token that is PRESENT in the vpc-resolving corpus but DEPLETED in the cmplog-blocking corpus — a token-presence signature (does t
      rule: "winner_literal_count >= 1.0 AND literal_presence_ratio <= 0.34"
  - id=vp_gradient_streamposition_single_byte_dispatch tool=? decidable=False
      label: vpc resolves a single-byte dispatch/terminator gate whose required byte sits at a PARSE-STATE-DEPENDENT (non-fixed-file) position — a terminator following a variable-length name — where no built tool 
      rule: null

Built tools ALREADY used by the prior test: ['depth_reach', 'joint_necessity', 'operand_enrichment', 'token_count', 'value_distance_reached'].
Built tools NOT yet tried here (likely pivots): ['corpus_size_ratio'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.