# Pass-C review flags (manual merge step — task #4)

Decision (2026-06-18): the re-design loop (Rounds 1–2 + the depth_reach wiring fix)
relabeled **28 previously-labeled branches** (label X → label Y), because the arbiter
is stateless and follows each round's `decision_order` — the "freeze confirmed / no
silent relabel" invariant was NOT enforced at arbitration time. Per decision, we
**accept the relabels and reconcile them in Pass-C** (this manual merge step) rather
than enforce the freeze retroactively. 0 regressions (no branch lost its label);
the depth bug itself was false-negative only (never created/corrupted a label).

## Cosmetic renames — ACCEPTED, no action (24 branches)
Same underlying mechanism, sharper id. Pass-C should just pick the canonical name:
- `ctx_coverage_WL` (14): `iteration_depth_threshold` → `iteration_path_depth_reach`
- `grimoire_structural_WL` (4): `structural_depth_only` → `structural_size_depth_only`;
  `structural_token_assembly` → `structural_token_richness`
- `i2s_vp__WWL` (5): `vp_cmpmap_gradient_distance_closure` → `vp_cmpmap_distance_closure_fixed_operand`
- `i2s_vp_LWWL` (1): `vp_gradient_value_distance_closed` → `vp_gradient_scalar_operand_distance`

## ⚠ SUBSTANTIVE re-categorization — NEEDS EXPLICIT REVIEW (i2s_vp_LW_L, 4 branches)
All 4 were ONE category in round-0 (`vp_gradient_climbs_numeric_threshold`); the
re-design **SPLIT** them into 4 different mechanisms. Question for Pass-C: was the
round-0 label an over-lumped under-split (split is correct), or did the redesign /
the now-working depth_reach drift them apart spuriously?

| branch  | round-0 label                       | new label                                          |
|---------|-------------------------------------|----------------------------------------------------|
| lcms/2141    | vp_gradient_climbs_numeric_threshold | vp_gradient_assembles_multibyte_literal            |
| sqlite3/14438| vp_gradient_climbs_numeric_threshold | vp_drives_parser_depth_into_structured_true_side   |
| sqlite3/15242| vp_gradient_climbs_numeric_threshold | vp_climbs_numeric_magnitude_to_threshold           |
| sqlite3/15515| vp_gradient_climbs_numeric_threshold | vp_enriches_fixed_offset_fourcc_operand            |

Action: verify each new label against the branch's signature/card; confirm the
4-way split is mechanism-justified (not a decision_order artifact). If any pair is
really the same mechanism, merge them back in Pass-C.

**Preliminary signature check (2026-06-18) — split looks PARTLY SPURIOUS:**
| branch | gate / operand | new label | fit |
|---|---|---|---|
| lcms/2141 | switch_case, multibyte `scnr` w4 | assembles_multibyte_literal | ✓ fits |
| sqlite3/14438 | switch_case, multibyte `>>` w2 | drives_parser_depth | sibling of 15242 but diff label |
| sqlite3/15242 | switch_case, multibyte `>=` w2 | climbs_numeric_magnitude | sibling of 14438 but diff label |
| sqlite3/15515 | equality, single-byte `=` w1 | enriches_fixed_offset_fourcc | ✗ a 1-byte `=` is NOT a FOURCC |

14438 + 15242 are near-identical (width-2 operator literals in a switch) yet split
into two mechanisms → likely a decision_order artifact; 15515's FOURCC label
mismatches its 1-byte operand. **Likely resolution: merge 14438/15242 (and probably
15515) back toward a single short-operator-literal VP-gradient mechanism in Pass-C.**
The depth_reach pivot firing first on 14438 is the suspected cause of its parser_depth
label — re-check whether depth_lift was genuinely strong there or marginal.
