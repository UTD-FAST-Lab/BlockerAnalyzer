ROUND re-design (loop-until-dry) for decisive shape **i2s_vp__LWL**. Overwrite `step5b_new_v3/i2s_vp__LWL/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp__LWL/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (90 decisive branches: 78 confirmed, 12 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 78x  i2s_exact_literal_gate

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - lcms/2334  [seed_starved]  unscorable: insufficient seeds (W=1, L=10; need >=3 each) -> rank-10 re-bisect candidate
  - libxml2/6233  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6643  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6740  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6809  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6929  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6936  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7249  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - curl/263  [seed_starved]  unscorable: insufficient seeds (W=1, L=15; need >=3 each) -> rank-10 re-bisect candidate
  - curl/427  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5362  [seed_starved]  unscorable: insufficient seeds (W=1, L=48; need >=3 each) -> rank-10 re-bisect candidate
  - harfbuzz/5745  [rule_not_met]  tested: 1/1 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=i2s_exact_literal_gate tool=operand_enrichment decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: vpc resolves an exact-literal equality gate because its I2SRandReplace splices the logged comparand literal into a fixed input offset, which value_profile's Hamming/CMP_MAP gradient cannot land
      rule: "signed_target_enrich >= 1.0"

Built tools ALREADY used by the prior test: ['operand_enrichment'].
Built tools NOT yet tried here (likely pivots): ['joint_necessity/struct_size_and_token_count', 'value_distance_reached', 'depth_reach', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.