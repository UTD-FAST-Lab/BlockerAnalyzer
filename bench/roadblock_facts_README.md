# Roadblock fact table — reconciliation

Source: `bench/dataset.jsonl` + deciding-pairs from `step5a_new_v3/*/cards.json`. `bench/roadblock_facts.csv` has **639 rows** (one per branch×shape×family membership).

Every paper number is a GROUP BY on this one table:

| quantity | query | value |
|---|---|--:|
| distinct roadblocks | COUNT(DISTINCT target,branch_id) | **558** |
| assigned roadblocks | DISTINCT branch WHERE any row status=validated | **382** |
| inconclusive roadblocks | DISTINCT branch WHERE no row is validated | **176** |
| assigned memberships | COUNT(rows WHERE status=validated) | 398 |
| final categories | COUNT(DISTINCT category WHERE validated) | 19 |
| raw categories | COUNT(DISTINCT raw_category WHERE validated) | 57 |
| families (all) | COUNT(DISTINCT family) | 15 |
| families with an assigned branch | DISTINCT family WHERE validated | 8 |
| all decisive shapes | COUNT(DISTINCT shape) | 38 |
| shapes with an assigned branch | DISTINCT shape WHERE validated | 29 |
| inconclusive branch×shape axes | COUNT(DISTINCT branch,shape WHERE status=inconclusive) | 229 |

## assigned branches per family (DISTINCT branch, status=validated)
| family | #assigned | #inconclusive |
|---|--:|--:|
| I2S-P | 238 | 56 |
| I2S-A | 49 | 24 |
| VP-P | 53 | 50 |
| VPC-P | 27 | 12 |
| VPC-A | - | 2 |
| CTX-P | 14 | 39 |
| CTX-A | 4 | 3 |
| GRIM-P | 11 | 31 |
| GRIM-A | - | 3 |
| NGRAM-P | 2 | 2 |
| NGRAM-A | - | 1 |
| CALI-P | - | 13 |
| FAST-P | - | 2 |
| FAST-A | - | 2 |
| MOPT-A | - | 1 |
| **distinct total** | **382** | **203** |
| sum (memberships, dual-counted) | 398 | 241 |

## assignment round (`assigned_round` column)
Reconstructed EXACTLY from git: the loop archived its hypothesis menu as `evidence_test.r0/r1/r2.json` at the start of each next round, so diffing the validated set across those boundary commits gives the per-round branch additions (`bench/branch_assigned_round.json`).
| round | new branches | cumulative |
|--:|--:|--:|
| R0 | 329 | 329 |
| R1 | 26 | 355 |
| R2 | 18 | 373 |
| R3 | 9 | 382 |

`first_validated_date` column = the git commit date the branch first appeared as `validated` (`bench/branch_first_validated.json`), the underlying provenance.

NOTE: the paper's earlier `tab:rounds` showed 330/358/384/393, but only R0 (330) and R3 (393, pre-multicat) were ever real — R1/R2 were `\rndph` placeholders later filled with interpolated values. The authoritative curve above (329/355/373/382 distinct branches) is the reproducible replacement.
