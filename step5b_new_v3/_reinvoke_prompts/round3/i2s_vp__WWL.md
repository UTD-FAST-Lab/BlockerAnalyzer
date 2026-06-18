ROUND re-design (loop-until-dry) for decisive shape **i2s_vp__WWL**. Overwrite `step5b_new_v3/i2s_vp__WWL/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp__WWL/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (14 decisive branches: 13 confirmed, 1 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 5x  vp_cmpmap_distance_closure_fixed_operand
  - 3x  vp_cmpmap_iteration_depth_reach
  - 3x  vp_admits_token_dense_corpus
  - 2x  vp_admits_larger_valid_structure

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - libxml2/6461  [rule_not_met]  tested: 4/4 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=vp_cmpmap_distance_closure_fixed_operand tool=value_distance_reached decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: For gates with a SINGLE fixed comparison operand, value_profile's CMP_MAP gradient admits a corpus that lands at a strictly smaller residual Hamming/prefix distance to that operand than the naive-bloc
      rule: "naive_min_distance > 0 AND distance_closure_ratio >= 0.5"
  - id=vp_admits_token_dense_corpus tool=struct_size_and_token_count decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: value_profile's CMP_MAP gradient admits a token-DENSE corpus: the VP-resolving seed set carries far more of the gate's required grammar/structural tokens PER BYTE than the naive-blocking set, because 
      rule: "token_density_lift >= 2.0 AND vp_token_density > naive_token_density"
  - id=vp_admits_larger_valid_structure tool=joint_necessity decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: For STRUCTURAL FORMAT-INTEGRITY gates (sfnt/font assembly), value_profile's gradient admits a corpus of PHYSICALLY LARGER, valid-header seeds than the naive-blocking corpus -- the gradient toward well
      rule: "size_lift >= 1.3 AND tag_lift >= 1.0"
  - id=vp_cmpmap_iteration_depth_reach tool=depth_reach decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: NEW (round-3 pivot). For RANGE / LOOP / DEEP-DISPATCH gates with NO harvestable single fixed-byte operand (digit-range loops past a counter threshold, a hex-charref loop reaching its non-hex terminato
      rule: "depth_lift >= 1.5 AND winner_deeper"
  - id=vp_advantage_seed_starved tool=? decidable=False
      label: honest non-discriminable residue: branches whose value_profile-RESOLVING arm has too few on-disk seeds for the applicable seed/struct tool to compute a stable median (token-density H2 needs >=3 W), AN
      rule: "decidable:false -> arbiter leaves these inconclusive (fallback) unless a seed re-bisect raises the VP arm to >=3 (re-enters H2) or H4 depth_reach is run for them and separates (depth_lift>=1.5 AND wi

Built tools ALREADY used by the prior test: ['depth_reach', 'joint_necessity', 'struct_size_and_token_count', 'value_distance_reached'].
Built tools NOT yet tried here (likely pivots): ['operand_enrichment/byte_freq_ratio', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.