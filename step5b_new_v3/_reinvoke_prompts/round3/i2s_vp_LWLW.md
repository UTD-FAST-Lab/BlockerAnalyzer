ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_LWLW**. Overwrite `step5b_new_v3/i2s_vp_LWLW/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_LWLW/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (13 decisive branches: 7 confirmed, 6 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 6x  i2s_decoy_substitution_overfit
  - 1x  i2s_diverts_from_exact_codepoint_literal

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - lcms/2149  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5576  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5619  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5989  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - openthread/13300  [manual_demote]  mechanism mismatch: stateful LinkedList op (PopAfter), no decoy (decoy_enrich~0.08); decoy
  - openthread/13302  [manual_demote]  mechanism mismatch: stateful LinkedList op (Find), no decoy (decoy_enrich~0.08); decoy-sub

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=i2s_decoy_substitution_overfit tool=operand_enrichment decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: I2S substitutes a fixed-offset structural literal (decoy) that pins the loser corpus to the valid-structure path and away from the winner's free-byte target
      rule: "signed_target_enrich < -0.3"
  - id=i2s_homogenizes_corpus_starves_state_diversity tool=corpus_size_ratio decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: I2S operand substitution collapses corpus composition onto a few CMP-matched byte patterns, inflating/homogenizing the I2S-arm corpus so it cannot build the diverse runtime state (linked-list populati
      rule: "corpus_size_ratio >= 1.3 AND composition_entropy_ratio < 0.85"
  - id=i2s_diverts_from_exact_codepoint_literal tool=value_distance_reached decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: Gate is an EXACT-equality test against a short codepoint literal that the WINNER (non-I2S) corpus lands by free havoc byte mutation, while the I2S stage diverts mutation energy away from the literal s
      rule: "winner_closer == true AND distance_gap >= 0.25 AND naive_min_distance <= 0.0"
  - id=i2s_anchors_large_valid_blocks_truncation tool=struct_size_ratio decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: I2S (and ctx) anchor the I2S-arm corpus to LARGE valid-header inputs; the branch's true side needs an input shorter than a fixed structural minimum (128-byte cmsICCHeader) that only plain havoc byte-d
      rule: "median_seed_length_ratio >= 1.5 AND winner_below_minimum == true"
  - id=i2s_no_operand_budget_drain tool=operand_enrichment decidable=False
      label: Gate is a table-/state-machine-derived, mask/range, or shaper-category value with NO fixed-offset input-byte CMP operand and NO exact value literal; I2S substitution finds nothing to copy and its over
      rule: "false"
  - id=i2s_off_path_subtree_diversion tool=event_cooccurrence decidable=False
      label: Branch carries no comparison operand (presence/non-null gate reached by generic table/loop traversal); the I2S stage's operand substitution diverts the loser into an EXPENSIVE SIBLING subtree (deep GP
      rule: "false"

Built tools ALREADY used by the prior test: ['corpus_size_ratio', 'operand_enrichment', 'value_distance_reached'].
Built tools NOT yet tried here (likely pivots): ['joint_necessity/struct_size_and_token_count', 'depth_reach', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.