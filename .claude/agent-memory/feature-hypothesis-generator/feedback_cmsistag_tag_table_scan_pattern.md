---
name: cmsIsTag tag-table-scan FOURCC pattern
description: lcms cmsIsTag(hProfile, tag16) tag-table linear scan extends i2s_magic_number_gate MAGIC_BYTES=4 even though tag16 is runtime-selected from Device2PCS16[Intent]
type: feedback
---

When the lcms cmsIsTag(hProfile, tag16) call site is the trap CMP, the per-CMP equality is `tag.sig == tag16` per tag-table entry. Even though `tag16 = Device2PCS16[Intent]` is runtime-selected (Intent at input offset 0x08), sancov logs the runtime literal at the time of the CMP via `__sanitizer_cov_trace_const_cmp4`. So I2S still substitutes the AToBx tag-signature constant in one step. This goes into `i2s_magic_number_gate` as MAGIC_BYTES=4, NOT a new template.

**Why:** Three plausible-but-falsified novel-axis candidates were considered:
- `i2s_runtime_selected_literal` — falsified: sancov logs runtime literal value, identical to compile-time literal mechanism
- `i2s_tag_table_scan_depth` — falsified: each scan iter is independent CMP, longer table = more I2S surface, not different mechanism
- `i2s_intent_dispatch_arity` — falsified: array-indexing dispatches WHICH literal, but per-CMP equality is identical

**How to apply:** Whenever a prompt's source line is `cmsIsTag(hProfile, X)` or any equivalent linear scan over a struct-field signature comparing against a runtime-selected literal, classify as i2s_magic_number_gate MAGIC_BYTES=4 extension. Side-B seeds will diversify input bytes that route through an Intent/dispatch byte to the matching tag-table entry; vp's hitcount=0 indicates upstream colorspace gating (offset 0x10 / 0x14) already routes vp away. The trio cmsio1.c br82/br87/br88 forms a canonical exemplar: direct PCS-CMP@0x14, tag-table-scan-CMP, direct dataColorSpace-CMP@0x10 — all three are MAGIC_BYTES=4 sites in the same file but at different CMP shapes.
