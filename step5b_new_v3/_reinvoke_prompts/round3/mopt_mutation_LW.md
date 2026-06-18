ROUND re-design (loop-until-dry) for decisive shape **mopt_mutation_LW**. Overwrite `step5b_new_v3/mopt_mutation_LW/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/mopt_mutation_LW/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (1 decisive branches: 0 confirmed, 1 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  (none — this shape has 0 confirmed branches; round-0 may have under-explored it)

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - sqlite3/14748  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=mopt_shallow_parse_depth_deficit tool=depth_reach decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: MOpt's corpus reaches the gate keyword but drives the Lemon parser shallower per seed than naive's, never iterating deep enough to fire the reduce
      rule: "winner_deeper AND depth_lift >= 2.0 AND side_lift >= 2.0"
  - id=mopt_scheduling_keyword_assembly_deficit tool=token_count decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: MOpt operator scheduling under-assembles the gate keyword that naive's havoc reaches
      rule: "token_lift >= 1.5 AND mopt_tokens < naive_tokens"
  - id=mopt_scheduling_root_cause_nonobservable tool=event_cooccurrence decidable=False
      label: The ROOT mechanism — MOpt's particle-swarm operator-scheduling DISTRIBUTION being worse for this structured-SQL goal — is non-observable in the available campaign data; no remaining built tool discrim
      rule: null

Built tools ALREADY used by the prior test: ['depth_reach', 'token_count'].
Built tools NOT yet tried here (likely pivots): ['operand_enrichment/byte_freq_ratio', 'value_distance_reached', 'corpus_size_ratio'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.