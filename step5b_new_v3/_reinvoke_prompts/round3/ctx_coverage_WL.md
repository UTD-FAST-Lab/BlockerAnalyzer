ROUND re-design (loop-until-dry) for decisive shape **ctx_coverage_WL**. Overwrite `step5b_new_v3/ctx_coverage_WL/evidence_test.json` (the current version is the most-recent prior; the original is preserved at `evidence_test.r0.json`).

Read your standard inputs: `step5a_new_v3/ctx_coverage_WL/{signatures.json,cards.json}` and `bench/tool_registry.json` (BUILT descriptors + the `data_realities` you MUST respect).

## Shape state (53 decisive branches: 14 confirmed, 39 UNLABELED)

### CONFIRMED branches — FROZEN (keep their hypotheses verbatim; do NOT re-test, relabel, or drop them)
  - 14x  iteration_path_depth_reach

### UNLABELED branches — YOUR TARGET (propose new discriminating mechanisms for these)
  - lcms/2342  [unmeasurable]  unscorable: measurement unavailable (no operand / unbuilt tool) though seeds present (W=12
  - libpng/3864  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/3874  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/3896  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/3951  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/3966  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/3980  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/4032  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/4039  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/4042  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/4055  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/4061  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libpng/4085  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/12282  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6405  [seed_starved]  unscorable: insufficient seeds (W=1, L=27; need >=3 each) -> rank-10 re-bisect candidate
  - libxml2/6483  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6581  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6616  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6887  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6924  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6925  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6926  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/6948  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7476  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/7783  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - libxml2/8630  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5237  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5302  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5517  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5708  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5839  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5878  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5887  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/5990  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - harfbuzz/6130  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - sqlite3/14535  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - sqlite3/14745  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - sqlite3/14762  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)
  - sqlite3/15434  [rule_not_met]  tested: 1/2 rule(s) scored, none held (mechanism not supported by campaign data)

## PRIOR hypotheses already tried (do NOT re-propose these as-is; a relaxed-threshold re-test is forbidden)
  - id=iteration_path_depth_reach tool=depth_reach decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: naive_ctx's resolving corpus drives the blocker line DEEPER per seed (more loop/recursion/path re-entries, or actually takes the blocked side) than naive's blocking corpus
      rule: "depth_lift >= 2.0 AND winner_deeper == True"
  - id=ctx_corpus_inflation tool=corpus_size_ratio decidable=True <- KEEP (confirmed >=1 branch; carry forward in your superset)
      label: naive_ctx hoards far more (context-redundant) saved-corpus entries than naive — a whole-campaign corpus-scale advantage independent of any single seed's terminal depth
      rule: "corpus_count_ratio >= 1.5"

Built tools ALREADY used by the prior test: ['corpus_size_ratio', 'depth_reach'].
Built tools NOT yet tried here (likely pivots): ['operand_enrichment/byte_freq_ratio', 'joint_necessity/struct_size_and_token_count', 'value_distance_reached', 'token_count'].

## Rules for this re-design
1. **Superset / monotonic:** your output MUST retain every prior hypothesis marked KEEP, unchanged, so the confirmed branches re-validate. Add NEW hypotheses only for the UNLABELED branches.
2. **Novelty (G1):** each new hypothesis is a *genuinely different* mechanism than any already refuted for these branches — falsifiable AND discriminating (rules out the obvious alternative). Reuse a BUILT registry descriptor by its key where the measurement fits; only propose a NEW descriptor if none does.
3. **Honest non-discriminable (G3):** if no built measurement can discriminate a sub-group's mechanism, mark those hypotheses `decidable:false`. An honest inconclusive is a CORRECT outcome — do NOT invent a mechanism to force a label. (Non-local families — scheduling/ctx/ngram/grimoire — are often legitimately non-discriminable.)
4. **Cross-server:** do NOT mark a branch `decidable:false` merely because its corpus is absent on the running server — the owning server arbitrates its own targets. Design tests valid for ALL branches; respect `data_realities` (e.g. corpora exist only for curl/harfbuzz/openthread/sqlite3 on s4 / lcms,libxml2,libpng,bloaty on sB; I2S is not lineage-tagged; value_profile is a feedback not a mutator).
5. Emit the standard `evidence_test.json` schema (shape, n_branches, hypotheses[...], decision_order, fallback, data_realities_respected, notes). Report which priors you kept, which new mechanism(s) you propose, and any sub-group you judge honestly `decidable:false`.