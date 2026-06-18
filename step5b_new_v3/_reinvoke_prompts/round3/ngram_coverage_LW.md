ROUND re-design (loop-until-dry) for decisive shape **ngram_coverage_LW**. Overwrite `step5b_new_v3/ngram_coverage_LW/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/ngram_coverage_LW/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (1 decisive branches: 0 confirmed, 1 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  (none — this shape has 0 confirmed branches; round-0 may have under-explored it)

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - libxml2/6939  [rule_not_met]  tested: 2/2 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=ngram_wellformed_skeleton_token_gap tool=token_count decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: naive's blocking-side corpus saves seeds that carry a well-formed XML document skeleton (the <?xml ...?> + <!DOCTYPE declaration + a real '&...;' reference token) that the parser can advance through t
      rule: "winner_token_richer == true AND token_lift >= 2.0"
  - id=ngram_deep_path_reach_gap tool=depth_reach decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: naive's blocking-side corpus actually drives the deep xmlParseReference->xmlAddChild call chain to the null-parent gate true-side per seed, while naive_ngram4's corpus stays mired in shallow tokenizer
      rule: "winner_deeper == true AND side_lift >= 2.0"
  - id=ngram_shallow_corpus_saturation_starves_deep_path tool=corpus_size_ratio decidable=False
      label: ngram-4 feedback floods the corpus with near-duplicate shallow-tokenizer seeds, starving energy from the rare deep xmlParseReference->xmlAddChild path that naive reaches (PRIOR; corpus-SCALE energy st
      rule: "corpus_size_ratio >= 1.5 AND depth_reach_inv == true"

Built tools ALREADY used by the prior test: ['corpus_size_ratio', 'depth_reach', 'token_count'].
Built tools NOT yet tried here (likely pivots): ['operand_enrichment/byte_freq_ratio', 'value_distance_reached'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.