ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_LWL_**. Overwrite `step5b_new_v3/i2s_vp_LWL_/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_LWL_/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (2 decisive branches: 1 confirmed, 1 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 1x  vpc_anti_sibling_subtree_depth_diversion

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - libxml2/6343  [rule_not_met]  tested: 2/2 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=vpc_anti_literal_flood_token_enrichment tool=joint_necessity decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: Adding I2S in vpc intercepts the gate's own literal comparands and SPLICES them back into inputs, flooding the vpc corpus with copies of the gate's exact literals (encoding magics for 6343; '<![CDATA[
      rule: "vpc_tags > vp_tags AND tag_lift <= -0.5 AND vpc_tags >= 0.5"
  - id=vpc_anti_sibling_subtree_depth_diversion tool=depth_reach decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: The I2S liability in vpc manifests as EXECUTION-DEPTH diversion at the target branch line: the vpc-BLOCKING corpus, having spliced the gate's logged comparands, gets funneled into the SIBLING / true-s
      rule: "winner_deeper == true AND depth_lift >= 1.5 AND winner_depth > loser_depth"

Built tools ALREADY used by the prior test: ['depth_reach', 'joint_necessity'].
Built tools NOT yet tried here (likely pivots): ['operand_enrichment/byte_freq_ratio', 'value_distance_reached', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.