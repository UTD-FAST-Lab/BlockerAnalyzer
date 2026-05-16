---
name: switch dispatcher Pattern A vs Pattern B duality
description: same K-arm switch can map to i2s_magic_number_gate (Pattern A, cmp>naive) AND i2s_anchored_seed_deviation_trap sub-type C (Pattern B, vp>vpc) on different fuzzer-pair edges
type: feedback
---

A K-arm switch on a multi-byte literal (e.g., 5-arm `switch(magic)` with MH_MAGIC/MH_MAGIC_64/MH_CIGAM/MH_CIGAM_64/FAT_CIGAM) is the same source CMP set, but maps to TWO DIFFERENT templates depending on which fuzzer-pair edge the analysis is on:

- **Pattern A — (cmp, naive, I2S) edge → `i2s_magic_number_gate` MAGIC_BYTES=K_byte_width.** I2S HELPS cmp because each `case <SIG>:` lowers (under compare-chain regime) to a per-case `trace_const_cmp4` that cmp logs and substitutes via I2SRandReplace. naive without I2S can't substitute. cmp wins.
- **Pattern B — (vp, vpc, I2S) edge → `i2s_anchored_seed_deviation_trap` sub-type C (set-membership-deviation).** I2S HURTS vpc because the K case literals all enter vpc's I2S dictionary; I2SRandReplace at offset 0 draws uniformly from K, locking vpc's queue into whichever sister arm establishes residency first. vp's per-arm CMP_MAP Hamming-distance gradient is arm-invariant (one bucket per case edge), so vp walks each arm freely. vp wins on the SPECIFIC target arm that vpc happens to monoculture away from.

**Why:** I2S as mechanism is **direction-asymmetric** depending on the comparison fuzzer. Against naive (no per-CMP feedback), I2S provides one-shot literal substitution — pure win. Against vp (CMP_MAP Hamming gradient), I2S adds dictionary-roulette overhead ON TOP OF gradient feedback — pure loss when the trap requires hitting one specific arm out of K. The strict-2-fuzzer rule preserves this: each template makes its claim about exactly one one-tech-delta pair.

**How to apply:** When the source line is `case <SIG>:` of a K-arm switch (K ≥ 2) on a multi-byte input field, check WHICH PAIR the prompt specifies before choosing template:
- Pair `(cmp, naive)` or `(vp, naive)` → `i2s_magic_number_gate` (or `vp_gradient_derived_operand` for the vp,naive variant of switch-arm reachability)
- Pair `(vp, vpc)` with vp winning → `i2s_anchored_seed_deviation_trap` sub-type C (set-membership). Note this in branch_index as a cross-target_corroboration of v8 flavor (dictionary-pollution-AT-anchor-zone), and explicitly cross-reference the Pattern A entry on the same source switch if one exists.

**Canonical example:** bloaty macho.cc 5-arm `switch(magic)` switch.
- macho.cc:152 → br475 → `i2s_magic_number_gate` extension #4 (cmp helps via per-case CMP, Pattern A).
- macho.cc:187 `case FAT_CIGAM:` → br457 → `i2s_anchored_seed_deviation_trap` cross-target #2 (vpc loses via 5-way I2S dictionary roulette, Pattern B sub-type C). Side-A vpc seeds carry MH_CIGAM/MH_CIGAM_64 magic (sister arms); Side-B vp seeds carry FAT_CIGAM target.
