ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_L_W_**. Overwrite `step5b_new_v3/i2s_vp_L_W_/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_L_W_/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (7 decisive branches: 1 confirmed, 6 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 1x  vp_enriches_size_tag_bytes

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - lcms/2090  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6719  [rule_not_met]  tested: 2/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/8100  [rule_not_met]  tested: 2/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/9841  [rule_not_met]  tested: 2/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5474  [rule_not_met]  tested: 2/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5477  [rule_not_met]  tested: 2/2 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=vp_enriches_size_tag_bytes tool=operand_enrichment decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: value_profile's CMP_MAP gradient enriches the VPC-resolving corpus for the target 'size' tag bytes (73 69 7a 65) relative to decoy tag bytes (GSUB/GPOS) at the gate offset: near-miss byte matches regi
      rule: "signed_target_enrich > 0 AND signed_target_enrich > decoy_enrich"
  - id=vp_admits_size_tag_richer_corpus tool=joint_necessity decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: corroborant: value_profile's CMP_MAP gradient drives corpus admission toward seeds that physically CONTAIN the 'size' feature tag (and toward larger seeds carrying a feature-list with the size record)
      rule: "tag_lift >= 1.0 OR size_lift >= 1.3"
  - id=vp_advantage_no_corpus_unmeasurable tool=? decidable=False
      label: honest non-discriminable: the 5 lcms/libpng/libxml2 branches have NO on-disk corpus (off-server: sB owns these targets; on-disk corpora exist only for curl/harfbuzz/openthread/sqlite3) AND confirmed Z
      rule: "decidable:false -> these branches carry the Layer-1 VP-gradient label but get NO independent confirmation on this server; the arbiter leaves them inconclusive (fallback). If sB owns the corpus, sB ap

Built tools ALREADY used by the prior test: ['joint_necessity', 'operand_enrichment'].
Built tools NOT yet tried here (likely pivots): ['value_distance_reached', 'depth_reach', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.