ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_WL_L**. Overwrite `step5b_new_v3/i2s_vp_WL_L/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_WL_L/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (7 decisive branches: 6 confirmed, 1 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 6x  i2s_exact_literal_constant_gate

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - harfbuzz/5562  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=i2s_exact_literal_constant_gate tool=operand_enrichment decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: cmplog plants an exact fixed-offset literal/magic constant the VP gradient cannot climb to
      rule: "signed_target_enrich >= 1.0 AND decoy_enrich <= 0.0"
  - id=i2s_derived_signed_operand_construction tool=operand_enrichment decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: cmplog constructs a DERIVED negative/range value across parser-routing bytes (no stored literal)
      rule: "no_gate_signature == true (operand_enrichment returns no fixed-offset literal); hypothesis confirmed by the diagnostic ABSENCE of literal enrichment under the i2s-pro shape, falling to inconclusive i
  - id=i2s_multiliteral_structural_assembly_gate tool=joint_necessity decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: cmplog assembles MULTIPLE dispersed table/script-tag literals into a coherent multi-part structure (no single fixed-offset gate byte) that the VP gradient cannot build
      rule: "size_lift >= 1.3 AND cmp_tags >= 2"

Built tools ALREADY used by the prior test: ['joint_necessity', 'operand_enrichment'].
Built tools NOT yet tried here (likely pivots): ['value_distance_reached', 'depth_reach', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.