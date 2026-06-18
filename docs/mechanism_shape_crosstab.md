# Mechanism × direction-family × decisive-shape cross-tab

_Generated from `bench/dataset.jsonl` (canonical_label) — 393 validated branches, 19 canonical mechanism features. The benchmark's two-layer structure: **Layer 1** (resolve/block decisive-shape → technique direction, mechanical) and **Layer 2** (direction → discovered mechanism/effect, evidence-validated by the 3-round loop)._

## Layer 1 — resolve/block shape → technique direction (mechanical)

The decisive-shape is a 4-char W(resolve)/L(block)/`_`(non-decisive) code over `(cmp, vp, vpc, naive)`. Which technique helps (pro) or hurts (anti) is just which fuzzers are in the resolve vs block set:

| shape pattern | direction | reading |
|---|---|---|
| cmp (or vpc) resolves, naive/vp blocks | **I2S-pro** | I2S substitution clears the gate |
| cmp **blocks** where vp/naive resolve | **I2S-anti** | I2S substitution *hurts* |
| vp/vpc resolves, cmp/naive blocks | **VP-pro** | VP gradient clears the gate |
| vpc **blocks** where vp resolves | **VPC-anti** | adding I2S to VP hurts (anti-synergy) |
| **vpc-only** resolves (needs both) | **JOINT (I2S×VP)** | joint necessity |
| `ctx_/ngram_/grimoire_*` shapes | that technique | non-local feedback/mutation |

## Layer 2 — direction → mechanism (discovered)

| direction-family | n | mechanisms (n) |
|---|---|---|
| **I2S-pro** | 240 | string_literal_substitution (184), numeric_tag_substitution (39), structural_assembly_reach_depth (8), operand_value_precision (6), relational_collision_gate (3) |
| **I2S-anti** | 46 | target_depletion (25), decoy_overfit (14), structural_byte_corruption (7) |
| **VP-pro** | 66 | gradient_value_distance_closure (39), gradient_drives_assembly_depth (17), operand_byte_enrichment (5), admits_structurally_richer_corpus (5) |
| **JOINT (I2S×VP)** | 7 | assembly_depth (7) |
| **VPC-anti** | 3 | depth_diversion (3) |
| **ctx-coverage** | 18 | iteration_path_depth (16), corpus_inflation (2) |
| **ngram-coverage** | 2 | sequential_depth_reach (2) |
| **grimoire** | 11 | structural_token_assembly (9), structural_size_depth (2) |

## Full cross-tab — each mechanism × the shapes it spans

### I2S-pro

**`i2s_string_literal_substitution`** — n=184

| n | decisive-shape | resolve / block |
|---|---|---|
| 77 | `i2s_vp_WLWL` | resolve=cmp+vpc / block=vp+naive |
| 67 | `i2s_vp__LWL` | resolve=vpc / block=vp+naive |
| 20 | `i2s_vp_W_WL` | resolve=cmp+vpc / block=naive |
| 7 | `i2s_vp_WWWL` | resolve=cmp+vp+vpc / block=naive |
| 6 | `i2s_vp_WW_L` | resolve=cmp+vp / block=naive |
| 3 | `i2s_vp_WLW_` | resolve=cmp+vpc / block=vp |
| 2 | `i2s_vp_LLW_` | resolve=vpc / block=cmp+vp |
| 1 | `i2s_vp_WL_L` | resolve=cmp / block=vp+naive |
| 1 | `i2s_vp_W__L` | resolve=cmp / block=naive |

**`i2s_numeric_tag_substitution`** — n=39

| n | decisive-shape | resolve / block |
|---|---|---|
| 17 | `i2s_vp_W_WL` | resolve=cmp+vpc / block=naive |
| 11 | `i2s_vp__LWL` | resolve=vpc / block=vp+naive |
| 6 | `i2s_vp_WLWL` | resolve=cmp+vpc / block=vp+naive |
| 5 | `i2s_vp_WL_L` | resolve=cmp / block=vp+naive |

**`i2s_structural_assembly_reach_depth`** — n=8

| n | decisive-shape | resolve / block |
|---|---|---|
| 6 | `i2s_vp_W_WL` | resolve=cmp+vpc / block=naive |
| 2 | `i2s_vp_WLWL` | resolve=cmp+vpc / block=vp+naive |

**`i2s_operand_value_precision`** — n=6

| n | decisive-shape | resolve / block |
|---|---|---|
| 6 | `i2s_vp_WLWL` | resolve=cmp+vpc / block=vp+naive |

**`i2s_relational_collision_gate`** — n=3

| n | decisive-shape | resolve / block |
|---|---|---|
| 3 | `i2s_vp_W__L` | resolve=cmp / block=naive |

### I2S-anti

**`i2s_anti_target_depletion`** — n=25

| n | decisive-shape | resolve / block |
|---|---|---|
| 23 | `i2s_vp_LW_W` | resolve=vp+naive / block=cmp |
| 2 | `i2s_vp_L__W` | resolve=naive / block=cmp |

**`i2s_anti_decoy_overfit`** — n=14

| n | decisive-shape | resolve / block |
|---|---|---|
| 7 | `i2s_vp_LWLW` | resolve=vp+naive / block=cmp+vpc |
| 6 | `i2s_vp__WLW` | resolve=vp+naive / block=vpc |
| 1 | `i2s_vp_L_LW` | resolve=naive / block=cmp+vpc |

**`i2s_anti_structural_byte_corruption`** — n=7

| n | decisive-shape | resolve / block |
|---|---|---|
| 7 | `i2s_vp_LWWW` | resolve=vp+vpc+naive / block=cmp |

### VP-pro

**`vp_gradient_value_distance_closure`** — n=39

| n | decisive-shape | resolve / block |
|---|---|---|
| 9 | `i2s_vp_LLW_` | resolve=vpc / block=cmp+vp |
| 7 | `i2s_vp_LLWL` | resolve=vpc / block=cmp+vp+naive |
| 5 | `i2s_vp_L_WL` | resolve=vpc / block=cmp+naive |
| 5 | `i2s_vp__WWL` | resolve=vp+vpc / block=naive |
| 4 | `i2s_vp_WWWL` | resolve=cmp+vp+vpc / block=naive |
| 3 | `i2s_vp__W_L` | resolve=vp / block=naive |
| 2 | `i2s_vp_LW_L` | resolve=vp / block=cmp+naive |
| 1 | `i2s_vp_LWLL` | resolve=vp / block=cmp+vpc+naive |
| 1 | `i2s_vp_LWWL` | resolve=vp+vpc / block=cmp+naive |
| 1 | `i2s_vp_LWWW` | resolve=vp+vpc+naive / block=cmp |
| 1 | `i2s_vp_WW_L` | resolve=cmp+vp / block=naive |

**`vp_gradient_drives_assembly_depth`** — n=17

| n | decisive-shape | resolve / block |
|---|---|---|
| 5 | `i2s_vp_LWWL` | resolve=vp+vpc / block=cmp+naive |
| 3 | `i2s_vp__WWL` | resolve=vp+vpc / block=naive |
| 2 | `i2s_vp_LLWL` | resolve=vpc / block=cmp+vp+naive |
| 2 | `i2s_vp_LWLL` | resolve=vp / block=cmp+vpc+naive |
| 2 | `i2s_vp_LWW_` | resolve=vp+vpc / block=cmp |
| 1 | `i2s_vp_LW_L` | resolve=vp / block=cmp+naive |
| 1 | `i2s_vp_L_WL` | resolve=vpc / block=cmp+naive |
| 1 | `i2s_vp_L_W_` | resolve=vpc / block=cmp |

**`vp_operand_byte_enrichment`** — n=5

| n | decisive-shape | resolve / block |
|---|---|---|
| 1 | `i2s_vp_LWWL` | resolve=vp+vpc / block=cmp+naive |
| 1 | `i2s_vp_LWW_` | resolve=vp+vpc / block=cmp |
| 1 | `i2s_vp_LW_L` | resolve=vp / block=cmp+naive |
| 1 | `i2s_vp_L_WL` | resolve=vpc / block=cmp+naive |
| 1 | `i2s_vp_L_W_` | resolve=vpc / block=cmp |

**`vp_admits_structurally_richer_corpus`** — n=5

| n | decisive-shape | resolve / block |
|---|---|---|
| 5 | `i2s_vp__WWL` | resolve=vp+vpc / block=naive |

### JOINT (I2S×VP)

**`joint_assembly_depth`** — n=7

| n | decisive-shape | resolve / block |
|---|---|---|
| 6 | `i2s_vp_LLWL` | resolve=vpc / block=cmp+vp+naive |
| 1 | `i2s_vp_LLW_` | resolve=vpc / block=cmp+vp |

### VPC-anti

**`vpc_anti_depth_diversion`** — n=3

| n | decisive-shape | resolve / block |
|---|---|---|
| 2 | `i2s_vp__WLW` | resolve=vp+naive / block=vpc |
| 1 | `i2s_vp_LWL_` | resolve=vp / block=cmp+vpc |

### ctx-coverage

**`ctx_iteration_path_depth`** — n=16

| n | decisive-shape | resolve / block |
|---|---|---|
| 14 | `ctx_coverage_WL` | ctx_coverage_WL |
| 2 | `ctx_coverage_LW` | ctx_coverage_LW |

**`ctx_corpus_inflation`** — n=2

| n | decisive-shape | resolve / block |
|---|---|---|
| 2 | `ctx_coverage_LW` | ctx_coverage_LW |

### ngram-coverage

**`ngram_sequential_depth_reach`** — n=2

| n | decisive-shape | resolve / block |
|---|---|---|
| 2 | `ngram_coverage_WL` | ngram_coverage_WL |

### grimoire

**`grimoire_structural_token_assembly`** — n=9

| n | decisive-shape | resolve / block |
|---|---|---|
| 9 | `grimoire_structural_WL` | grimoire_structural_WL |

**`grimoire_structural_size_depth`** — n=2

| n | decisive-shape | resolve / block |
|---|---|---|
| 2 | `grimoire_structural_WL` | grimoire_structural_WL |

## The relationship is many-to-many (by design)

- **One mechanism spans many shapes:** `vp_gradient_value_distance_closure` lives in **11 shapes** (`i2s_vp_LLW_`, `i2s_vp_LLWL`, `i2s_vp_L_WL`, `i2s_vp__WWL`, `i2s_vp_WWWL`…) — all sharing 'an I2S-carrying fuzzer resolves where naive blocks'. The mechanism is the *effect*, abstracted over the exact W/L pattern.
- **One shape hosts many mechanisms:** `i2s_vp_WLWL` hosts **4 mechanisms** (i2s_string_literal_substitution (77), i2s_numeric_tag_substitution (6), i2s_operand_value_precision (6), i2s_structural_assembly_reach_depth (2)).

**Why this matters (RQ3 construct validity):** Layer 1 (the shape) is what the LibAFL variants *defined* — it is technique-direction by construction. Layer 2 (the mechanism) is the discovered, campaign-validated stratification. Because they are separable, RQ3 can ask whether the mechanism labels generalize to *independent* engines (AFL++/honggfuzz/libFuzzer) — i.e. whether the labels are intrinsic to the blocker, not an artifact of the LibAFL variant that surfaced them.
