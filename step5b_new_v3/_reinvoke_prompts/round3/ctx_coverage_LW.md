ROUND re-design (loop-until-dry) for decisive shape **ctx_coverage_LW**. Overwrite `step5b_new_v3/ctx_coverage_LW/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/ctx_coverage_LW/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (6 decisive branches: 4 confirmed, 2 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 2x  ctx_corpus_inflation
  - 2x  ctx_depth_inflation_at_gate

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - libxml2/6605  [rule_not_met]  tested: 2/4 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5802  [rule_not_met]  tested: 2/4 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=ctx_corpus_inflation tool=corpus_size_ratio decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: ctx inflates the corpus / map so naive_ctx hoards far more (context-redundant) entries than naive
      rule: "corpus_count_ratio >= 1.5"
  - id=ctx_depth_inflation_at_gate tool=depth_reach decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: a high-call-count / multi-context path at the gate is what ctx fragments (flooding) vs a shallow exact-literal gate (dilution)
      rule: "call_count_lift >= 3.0 (flooding sub-mechanism) vs call_count_lift < 3.0 (dilution sub-mechanism)"
  - id=ctx_literal_corpus_depletion tool=byte_freq_ratio decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: at a SHALLOW exact-literal equality gate (not a loop, not a hoard), naive's corpus is enriched in the gate's target byte while naive_ctx's corpus is DEPLETED of it -- the per-edge reward that should p
      rule: "signed_target_enrich <= -0.5"
  - id=ctx_literal_window_approach tool=value_distance_reached decidable=None <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: at the shallow exact-literal gate, naive's corpus contains a sliding window that lands CLOSE to the gate operand (low Hamming distance, offset-tolerant) while naive_ctx's best window stalls FAR from i
      rule: "winner_closer == true AND distance_gap >= 0.15"

Built tools ALREADY used by the prior test: ['byte_freq_ratio', 'corpus_size_ratio', 'depth_reach', 'value_distance_reached'].
Built tools NOT yet tried here (likely pivots): ['joint_necessity/struct_size_and_token_count', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.