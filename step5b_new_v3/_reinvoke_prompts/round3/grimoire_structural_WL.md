ROUND re-design (loop-until-dry) for decisive shape **grimoire_structural_WL**. Overwrite `step5b_new_v3/grimoire_structural_WL/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/grimoire_structural_WL/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (42 decisive branches: 11 confirmed, 31 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 7x  structural_token_assembly
  - 2x  structural_size_depth_only
  - 2x  structural_token_richness

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - libxml2/13869  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/15063  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6210  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6411  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6414  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6475  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6649  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6985  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7018  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7022  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7040  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7069  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7099  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7101  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7105  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7107  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7123  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7138  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7143  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7161  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7268  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7288  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7294  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7317  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/8363  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/8556  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/8567  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/9784  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5440  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5810  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5866  [rule_not_met]  tested: 3/4 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=structural_token_richness tool=joint_necessity decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: grimoire's GeneralizationStage + structural splice/recurse mutators place MORE DISTINCT coherent structural tokens/constructs per seed than cmplog's I2S byte-substitution can, even though cmplog can p
      rule: "tag_lift >= 1.0 AND grimoire_tags >= 2 AND size_lift >= 1.0"
  - id=structural_size_depth_only tool=joint_necessity decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: fallback: grimoire reaches the gate via larger/deeper structure (state-machine depth, repeated category blocks, nested clusters) without a countable target-vocabulary tag signal
      rule: "size_lift >= 1.3"
  - id=structural_token_assembly tool=joint_necessity decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: grimoire's grammar mutators place structural tokens/constructs into the corpus that naive's byte havoc cannot, building larger/deeper inputs
      rule: "tag_lift >= 1.0 AND naive_tags < grimoire_tags AND grimoire_tags >= 2"
  - id=structural_iteration_depth_reach tool=depth_reach decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: NEW (round 2): grimoire's structural recombination drives the gated branch LINE deeper -- it builds the well-nested element/state-machine structure that advances the shaper/parser INTO the gated case 
      rule: "winner_deeper == true AND depth_lift >= 1.5"

Built tools ALREADY used by the prior test: ['depth_reach', 'joint_necessity'].
Built tools NOT yet tried here (likely pivots): ['operand_enrichment/byte_freq_ratio', 'value_distance_reached', 'corpus_size_ratio', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.