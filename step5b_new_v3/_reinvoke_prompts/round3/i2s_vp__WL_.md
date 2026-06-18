ROUND re-design (loop-until-dry) for decisive shape **i2s_vp__WL_**. Overwrite `step5b_new_v3/i2s_vp__WL_/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp__WL_/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (1 decisive branches: 0 confirmed, 1 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  (none — this shape has 0 confirmed branches; round-0 may have under-explored it)

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - harfbuzz/6010  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=vpc_i2s_inflates_homogenizes_corpus tool=corpus_size_ratio decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: NEW (R3) primary: the I2S substitution mutator that vpc adds INFLATES and HOMOGENIZES vpc's saved corpus relative to value_profile's -- vpc hoards far more saved seeds (corpus churn) whose byte compos
      rule: "corpus_size_ratio >= 1.3 AND composition_entropy_ratio < 0.85"
  - id=vp_admits_token_richer_codepoint_assembly tool=joint_necessity decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: value_profile's UNBURDENED CMP_MAP gradient admits a corpus that physically CONTAINS more of the gate's required Devanagari codepoint tokens (the 0x0905 + 0x094X words) and/or is larger than the value
      rule: "tag_lift >= 1.0 OR size_lift >= 1.3"
  - id=vp_enriches_codepoint_operand_bytes tool=operand_enrichment decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: secondary / corroborant: the value_profile-resolving corpus is enriched for the target Devanagari codepoint bytes (vs decoy bytes) relative to the value_profile_cmplog-blocking corpus at the gate site
      rule: "signed_target_enrich > 0 AND signed_target_enrich > decoy_enrich"

Built tools ALREADY used by the prior test: ['corpus_size_ratio', 'joint_necessity', 'operand_enrichment'].
Built tools NOT yet tried here (likely pivots): ['value_distance_reached', 'depth_reach', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.