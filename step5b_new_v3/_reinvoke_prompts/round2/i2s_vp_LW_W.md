ROUND re-design (loop-until-dry) for decisive shape **i2s_vp_LW_W**. Overwrite `step5b_new_v3/i2s_vp_LW_W/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/i2s_vp_LW_W/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (29 decisive branches: 23 confirmed, 6 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 23x  i2s_decoy_substitution_target_depletion

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - harfbuzz/5311  [rule_not_met]  tested: 3/5 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5723  [rule_not_met]  tested: 3/5 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5881  [rule_not_met]  tested: 3/5 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5931  [rule_not_met]  tested: 3/5 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5934  [rule_not_met]  tested: 3/5 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5954  [rule_not_met]  tested: 4/5 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=i2s_decoy_substitution_target_depletion tool=operand_enrichment decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: I2S splices a WRONG/competing but abundant CMP operand into the input (a well-known font-table tag, a script-tag/codepoint constant, an in-range fixed-point magnitude, or a competing protocol value), 
      rule: "skip != 'no_gate_signature' AND signed_target_enrich < -0.3"
  - id=i2s_disrupts_havoc_sequence_accumulation tool=joint_necessity decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: The winner gate needs havoc to BUILD or PRESERVE a long / periodically-repeated glyph-record byte sequence (multi-matra record runs, long multi-glyph Thai state-machine traversal); the gate value is t
      rule: "skip == 'no_gate_signature' AND size_lift >= 1.3"
  - id=i2s_overhead_on_derived_gate_no_operand tool=operand_enrichment decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: The gate value is computed from shaping tables, Unicode-property lookups, Ragel state-machine internals, or derived category classification -- NOT a literal value compared against input bytes anywhere
      rule: "skip == 'no_gate_signature' AND size_lift < 1.3"
  - id=i2s_overhead_on_iteration_depth_gate tool=depth_reach decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: The winner gate is a loop-exit guard or a deep Ragel state-machine action whose firing depends on how DEEP the input drives the per-buffer traversal (delete_glyphs_inplace backward-cluster loop reachi
      rule: "skip == 'no_gate_signature' AND size_lift < 1.3 AND winner_deeper == true AND depth_lift >= 1.3"
  - id=i2s_decoded_codepoint_byte_reachable_gate tool=value_distance_reached decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: The gate is an equality on a value DECODED inside the shaper (a UTF/codepoint slot compared to a small set of constants, e.g. Thai consonants 0x0E1B/0x0E1D/0x0E1F), so I2S harvests the comparison oper
      rule: "winner_closer == true AND distance_gap >= 0.15"
  - id=i2s_oversolve_postshaping_derived_predicate tool=operand_enrichment decidable=False
      label: (decidable:false) The gate is a post-shaping / decoded-property predicate with NO input-resident operand and NO byte-reachable literal: a multi-codepoint conjunct (ZWJ followed by Extended_Pictographi
      rule: "false"

Built tools ALREADY used by the prior test: ['depth_reach', 'joint_necessity', 'operand_enrichment', 'value_distance_reached'].
Built tools NOT yet tried here (likely pivots): ['corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.