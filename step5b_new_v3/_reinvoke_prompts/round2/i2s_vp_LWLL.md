ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_LWLL**. Overwrite `step5b_new_v3/i2s_vp_LWLL/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_LWLL/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (5 decisive branches: 1 confirmed, 4 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 1x  vp_gradient_distance_climb

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - harfbuzz/5237  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - sqlite3/14452  [rule_not_met]  tested: 2/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - sqlite3/14518  [rule_not_met]  tested: 2/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - sqlite3/14577  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=vp_admits_structurally_richer_corpus tool=joint_necessity decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: value_profile's CMP_MAP gradient admits corpus members that physically CONTAIN more of the gate-required structure (longer / more SQL-relational / font-table tokens) than naive's blocking seeds, which
      rule: "size_lift >= 1.3 OR tag_lift >= 1.0"
  - id=vpc_i2s_overhead_regression tool=? decidable=False
      label: adding the I2S CmpLog stage to value_profile (=vpc) diverts mutation energy / dilutes the corpus and so REGRESSES the same gradient climb (vpc-anti half of the shape)
      rule: null
  - id=vp_gradient_distance_climb tool=value_distance_reached decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: value_profile's CMP_MAP gradient climbs a comparison-operand distance ramp toward a structural/syntactic gate state that cmplog- and naive-blocking seeds never approach
      rule: "vp_min_distance < cmplog_min_distance AND vp_min_distance < naive_min_distance AND vp_gate_cmp_satisfied_frac >= naive_gate_cmp_satisfied_frac + 0.2"

Built tools ALREADY used by the prior test: ['joint_necessity', 'value_distance_reached'].
Built tools NOT yet tried here (likely pivots): ['operand_enrichment/byte_freq_ratio', 'depth_reach', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.