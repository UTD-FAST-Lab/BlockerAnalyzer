ROUND re-design (loop-until-dry) for decisive shape **aflfast_rarity_WL**. Overwrite `step5b_new_v3/aflfast_rarity_WL/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/aflfast_rarity_WL/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (2 decisive branches: 0 confirmed, 2 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  (none — this shape has 0 confirmed branches; round-0 may have under-explored it)

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - curl/129  [decidable_false_only]  all hypotheses decidable:false (corpus-scale / non-discriminable)
  - curl/165  [decidable_false_only]  all hypotheses decidable:false (corpus-scale / non-discriminable)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=rare_edge_energy_overdrive tool=energy_share decidable=False
      label: fast over-invests havoc energy in the rare-edge seed, so its corpus shows more exploration past the rare edge than minimizer's
      rule: "rare_seed_descendant_share >= 1.5 AND rare_seed_depth_reach > 0"

Built tools ALREADY used by the prior test: (none).
Built tools NOT yet tried here (likely pivots): ['operand_enrichment/byte_freq_ratio', 'joint_necessity/struct_size_and_token_count', 'value_distance_reached', 'depth_reach', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.