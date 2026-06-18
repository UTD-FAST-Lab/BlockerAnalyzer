ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_LWW_**. Overwrite `step5b_new_v3/i2s_vp_LWW_/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_LWW_/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (9 decisive branches: 3 confirmed, 6 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 2x  vp_drives_corpus_deeper_into_assembly
  - 1x  vp_enriches_gate_operand_bytes

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - libpng/3833  [rule_not_met]  tested: 1/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6792  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6800  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7069  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7138  [rule_not_met]  tested: 2/3 rule(s) scored, none held (mechanism not supported by campaign data)
  - sqlite3/14493  [rule_not_met]  tested: 3/3 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=vp_admits_token_richer_assembly tool=joint_necessity decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: value_profile's CMP_MAP gradient drives corpus admission toward structurally larger / more-token-rich seeds: the VPC-resolving corpus physically CONTAINS more of the gate's required structural tokens 
      rule: "tag_lift >= 1.0 OR size_lift >= 1.3"
  - id=vp_enriches_gate_operand_bytes tool=operand_enrichment decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: secondary / corroborant: for the exact-codepoint conjunction gates, value_profile's gradient enriches the VPC corpus for the target operand bytes (vs decoy bytes) at the gate site, because near-miss c
      rule: "signed_target_enrich > 0 AND signed_target_enrich > decoy_enrich"
  - id=vp_drives_corpus_deeper_into_assembly tool=depth_reach decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: NEW (round-2): for the STATE-MACHINE / RECURSIVE-ASSEMBLY gates, value_profile's CMP_MAP gradient admits corpus members that DYNAMICALLY REACH a deeper point in the parse/recursion than the cmplog-blo
      rule: "depth_lift >= 2.0 AND winner_branch_taken AND (loser_branch_taken == false)"
  - id=vp_magnitude_inequality_no_discriminable_tool tool=? decidable=False
      label: honest non-discriminable (G3): libpng_3833 is a SINGLE scalar magnitude-inequality guard (greenx > PNG_FP_1 == 100000 == 0x000186A0). Its only mechanistically-fitting discriminator is scalar value-DIS
      rule: "decidable:false -> libpng_3833 carries the Layer-1 VP-gradient label but gets NO independent confirmation; the arbiter must leave it inconclusive (fallback). An honest non-discriminable is a CORRECT 

Built tools ALREADY used by the prior test: ['depth_reach', 'joint_necessity', 'operand_enrichment'].
Built tools NOT yet tried here (likely pivots): ['value_distance_reached', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.