ROUND re-design (loop-until-dry) for decisive shape **grimoire_structural_LW**. Overwrite `step5b_new_v3/grimoire_structural_LW/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/grimoire_structural_LW/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (3 decisive branches: 0 confirmed, 3 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  (none — this shape has 0 confirmed branches; round-0 may have under-explored it)

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - libpng/3892  [rule_not_met]  tested: 2/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6597  [rule_not_met]  tested: 2/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6869  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=gap_erases_exact_literal tool=token_count decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: Grimoire's GeneralizationStage replaces the concrete literal byte (I2S/havoc planted) with a <GAP> token; structural recombination never restores it, so a byte-equality gate that literal-preserving na
      rule: "naive_literal_count >= 1 AND literal_presence_ratio < 0.34"
  - id=fragmentation_starves_depth tool=struct_size_ratio decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: Grimoire's re-run tax + structural-recombination produce short, fragmented inputs that never advance the parser far enough to pass a quantitative buffer/depth threshold; naive's longer coherent conten
      rule: "size_lift >= 3.0 AND grimoire_median_size < naive_median_size"

Built tools ALREADY used by the prior test: ['token_count'].
Built tools NOT yet tried here (likely pivots): ['operand_enrichment/byte_freq_ratio', 'value_distance_reached', 'depth_reach', 'corpus_size_ratio'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.