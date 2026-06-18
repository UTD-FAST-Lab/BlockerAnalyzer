# Pass-C canonical taxonomy (2026-06-18) — 57 raw labels → 19 canonical features

**Update:** the I2S-anti family is kept as the documented 3-way split (cluster_triage_table
page 8), NOT collapsed: `i2s_anti_target_depletion` (25, ← target_depletion + energy_diversion_decoy_pin),
`i2s_anti_decoy_overfit` (14, ← overfit + decoy_overcommit_wrong_literal + case_constant +
diverts_from_exact_codepoint), `i2s_anti_structural_byte_corruption` (7). joint_assembly_depth
also split out (user). So 19 features, not the 17 first drafted below.


The 3-round loop produced 57 distinct mechanism labels over 393 validated branches.
Many are cosmetic renames / cross-shape duplicates of the same mechanism. Pass-C
merges them by MECHANISM (technique-direction × effect), NOT by surface gate shape.
This resolves the 24 cosmetic renames + the i2s_vp_LW_L over-split automatically, and
applies the RQ3-flagged string-vs-numeric split to the dominant I2S-literal family.

## Final canonical features (17)

| n | canonical feature | technique/dir |
|---|---|---|
| 184 | i2s_string_literal_substitution | I2S-pro |
| 39 | i2s_numeric_tag_substitution | I2S-pro (RQ3 split from the literal family) |
| 39 | i2s_decoy_substitution | I2S-anti |
| 39 | vp_gradient_value_distance_closure | VP-pro |
| 24 | vp_gradient_drives_assembly_depth | VP-pro |
| 16 | ctx_iteration_path_depth | ctx-coverage |
| 9  | grimoire_structural_token_assembly | grimoire |
| 8  | i2s_structural_assembly_reach_depth | I2S-pro |
| 7  | i2s_anti_structural_byte_corruption | I2S-anti |
| 6  | i2s_operand_value_precision | I2S-pro |
| 5  | vp_operand_byte_enrichment | VP-pro |
| 5  | vp_admits_structurally_richer_corpus | VP-pro |
| 3  | vpc_anti_depth_diversion | VPC-anti |
| 3  | i2s_relational_collision_gate | I2S-pro |
| 2  | ctx_corpus_inflation | ctx-coverage |
| 2  | grimoire_structural_size_depth | grimoire |
| 2  | ngram_sequential_depth_reach | ngram-coverage |

## RQ3 split (the one value-adding split, not a merge)
The I2S fixed-offset-literal family (223 br) splits by operand_kind:
**string/char-literal (184) → i2s_string_literal_substitution** vs
**numeric/tag/enum (39) → i2s_numeric_tag_substitution**. RQ3 showed these behave
differently across engines (honggfuzz solves string but scores ~0 on numeric-tag
I2S), so they are genuinely distinct mechanisms. (none_structural/presence/unknown
default to the string bucket — a minor boundary to refine.)

## Judgment calls flagged (decide before/at apply)
1. **joint_assembly_depth (I2S×VP joint, 7 br) folded into vp_gradient_drives_assembly_depth.**
   Alternative: keep it as its own JOINT feature (resolves only under both techniques).
2. **vp_gradient_value_distance_closure (39) merged basin_escape + numeric_magnitude**
   subtypes. Alternative: keep 1–2 sub-features.
3. **string/numeric boundary**: 16 unknown + 7 none_structural + 1 presence default to
   string. A few may be numeric — refine by re-reading signatures if it matters.

## LW_L over-split (from pass_c_review_flags.md) — RESOLVED by this map
The 4 LW_L branches collapse: 14438→vp_gradient_drives_assembly_depth,
15242→vp_gradient_value_distance_closure, 15515→vp_operand_byte_enrichment,
2141→vp_operand_byte_enrichment. No longer 4 singleton labels.
