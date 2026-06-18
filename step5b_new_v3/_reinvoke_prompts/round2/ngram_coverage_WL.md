ROUND re-design (loop-until-dry) for decisive shape **ngram_coverage_WL**. Overwrite `step5b_new_v3/ngram_coverage_WL/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/ngram_coverage_WL/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (4 decisive branches: 2 confirmed, 2 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 2x  ngram_sequential_depth_reach

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - libxml2/6359  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=10
  - libxml2/6887  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=ngram_sequential_depth_reach tool=depth_reach decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: n-gram path-tuple retention lets naive_ngram4 reach deeper sequential-decode path states that plain edge coverage collapses and discards
      rule: "depth_lift >= 1.5 AND winner_depth > loser_depth"
  - id=ngram_value_approach_retention tool=value_distance_reached decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: n-gram path-tuple retention keeps naive_ngram4 seeds that progressively approach the gate operand VALUE (threshold magnitude), so the winner corpus lands measurably closer to the operand than the naiv
      rule: "winner_closer == true AND distance_gap > 0"
  - id=ngram_flat_cascade_bom_retention tool=? decidable=False
      label: n-gram path-diversity retention of near-miss UTF-8-BOM-adjacent inputs in a FLAT detection cascade (no iteration depth, no magnitude gradient) — honestly non-discriminable by any built measurement
      rule: null

Built tools ALREADY used by the prior test: ['depth_reach', 'value_distance_reached'].
Built tools NOT yet tried here (likely pivots): ['operand_enrichment/byte_freq_ratio', 'joint_necessity/struct_size_and_token_count', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.