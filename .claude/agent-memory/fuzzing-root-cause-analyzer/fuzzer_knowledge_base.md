# LibAFL FuzzBench Fuzzer Knowledge Base

## Fuzzer Variants

All 4 variants share the same scheduler (`IndexesLenTimeMinimizerScheduler` + `QueueScheduler`), corpus handling, and harness wrapper. They differ only in **feedback** and **mutation** configuration.

### Component Matrix

| Component | naive | cmplog | value_profile | value_profile_cmplog |
|-----------|-------|--------|---------------|----------------------|
| Edge coverage feedback | Yes | Yes | Yes | Yes |
| Value profile feedback (CMP_MAP) | No | No | **Yes** (inline) | **Yes** (inline) |
| Comparison logging (CmpLogObserver) | No | **Yes** (tracing stage) | No | **Yes** (tracing stage) |
| I2S/Redqueen mutations | No | **Yes** | No | **Yes** |
| Havoc + token mutations | Yes | Yes | Yes | Yes |
| Stages | 1 (mutate) | 3 (trace, i2s, mutate) | 1 (mutate) | 3 (trace, i2s, mutate) |
| Feedback sources | 2 (edges, time) | 2 (edges, time) | 3 (edges, cmps, time) | 3 (edges, cmps, time) |

### naive

Baseline. Edge coverage only. Havoc + token mutations. No comparison awareness. Fastest execution.

### cmplog

Adds a **tracing stage** that replays each corpus entry with comparison instrumentation (CmpLogObserver, 10x timeout). Logged comparisons feed an **I2S (Input-to-State) redqueen pass** that identifies input bytes matching one side of a comparison and replaces them with the other side. Runs redqueen BEFORE standard havoc mutations.

**Mechanism:** For `memcmp(buf, "CRAM", 4)`, cmplog logs that bytes at offset 0 are being compared against `"CRAM"`. The I2S pass then tries replacing those bytes with `"CRAM"` to satisfy the comparison.

### value_profile

Adds a **CMP_MAP observer** that tracks Hamming distance on comparisons inline during normal execution (no separate tracing stage). When a mutation brings a comparison operand closer to the target value (e.g., 3 of 4 bytes match instead of 2), this registers as new feedback, even if no new edge is covered. Uses this as a feedback signal only - no directed mutations.

**Mechanism:** For `if (x == 0xDEADBEEF)`, value_profile rewards inputs where `x` is closer to `0xDEADBEEF` in Hamming distance, creating a gradient toward the solution. Lighter than cmplog (no tracing overhead) but less direct (no byte substitution).

### value_profile_cmplog

Combines both: inline CMP_MAP feedback (value_profile) + comparison logging tracing stage + I2S redqueen mutations (cmplog). Most capable but heaviest overhead.

## Known Barrier Types and Fuzzer Performance

Source: `notes/n4_vs_cmplog_barrier_types.md` and experiments.

### Type 1: Magic Value / Format Header

**Pattern:** Fixed byte sequence at input boundary, expressed as a direct comparison (e.g., `memcmp(buf, "CRAM", 4)`).

**Example:** htslib CRAM header — bytes 0-5 must be `CRAM\x03\x01`.

| Fuzzer | Performance | Why |
|--------|-------------|-----|
| naive | Fails | ~2^-48 probability of random mutation producing 6 correct bytes |
| cmplog | **Wins** | I2S logs the `memcmp` and directly substitutes the expected bytes |
| value_profile | Gradual | Hamming feedback creates gradient, but slower than direct substitution |
| value_profile_cmplog | **Wins** | Has both gradient and direct substitution |

**Diagnostic signal:** Divergence point is **upstream** of the blocking branch (the branch is unreachable without the magic value). Resolving seeds contain the exact magic bytes at a fixed offset. Blocking seeds have random bytes there.

### Type 2: Structural / Semantic Invariant

**Pattern:** Cross-table or multi-step property not expressed as a single comparison. Requires maintaining a global relationship across multiple data structures.

**Example:** harfbuzz GDEF+GSUB — a glyph must be classified as LIGATURE in GDEF but NOT processed by `ligate_input()` in GSUB.

| Fuzzer | Performance | Why |
|--------|-------------|-----|
| naive | **Wins** | Blind mutations + coverage feedback; structural property preserved by accident |
| cmplog | Fails | Redqueen pass targets comparison bytes (glyph IDs, class values) which are exactly the bytes that define the structural invariant. Replacing them satisfies local comparisons but destroys the cross-table relationship |
| value_profile | **Wins** | Same as naive — no directed mutations to corrupt the invariant |
| value_profile_cmplog | Fails | Same as cmplog — redqueen destroys the invariant |

**Diagnostic signal:** Divergence point is **at the branch itself** (both fuzzers reach the predicate, only the non-cmplog fuzzer satisfies it). Resolving seed lineage shows the property was found via standard havoc mutations, not I2S.

**Key insight:** Redqueen's I2S pass is a *local* oracle — it knows what value a specific comparison expects but doesn't know that changing that value breaks a relationship several table-lookups away. This is systematic, not accidental: redqueen fires on every interesting seed, including those that have the right structural property, and corrupts them before coverage feedback can preserve them.

### Type 3: Iteration Depth / Accumulation

**Pattern:** Branch requires accumulating state across many loop iterations (e.g., pushing N values onto a stack before checking `count >= 12`).

**Example:** CFF2 charstring interpreter — `hvcurveto` needs `arg_stack.count >= 12`.

| Fuzzer | Performance | Why |
|--------|-------------|-----|
| naive (edge) | Moderate | Edge coverage saturates after first loop iteration — no incentive to grow inputs |
| naive (4-gram/n4) | **Wins** | 4-gram coverage creates new feedback for each loop iteration, rewarding longer inputs |
| cmplog | Moderate | Redqueen doesn't help (barrier is iteration count, not a comparison) |
| value_profile | Moderate | Value profile doesn't help (no comparison to gradient toward) |

**Note:** Our FuzzBench fuzzers all use standard edge coverage, not 4-gram. This barrier type primarily differentiates edge vs n-gram coverage, not our 4 variants. However, value_profile's extra comparison feedback may incidentally reward some accumulation patterns.

## Diagnostic Framework for Root Cause Analysis

When analyzing why fuzzer A resolves a cluster but fuzzer B doesn't:

1. **Check the resolving seed's lineage:** Does the critical mutation use I2S/redqueen? If yes → magic value barrier, cmplog advantage.

2. **Check controlling bytes:** Are they a fixed magic value at a consistent offset? If yes → Type 1. Are they part of a complex multi-field relationship? If yes → Type 2.

3. **Check divergence location:** Is the blocking branch unreachable by the blocking fuzzer (upstream divergence)? → Type 1 (accessibility barrier). Does the blocking fuzzer reach the branch but fail the predicate? → Type 2 or 3 (predicate barrier).

4. **Check if cmplog is the blocker:** If cmplog/value_profile_cmplog block and naive/value_profile resolve → suspect redqueen is destroying a structural invariant (Type 2).

5. **Check seed sizes:** If resolving seeds are consistently larger → suspect iteration depth barrier (Type 3).

## LibAFL Metadata Caveats

**I2S/cmplog mutations are NOT recorded in the mutation op list.** When cmplog's I2S stage produces a seed, the `.metadata` file records `parent_file` and `execs`/`elapsed_ms` but the mutation op list is **empty** (no entry in the metadata map). This means:

- Seeds produced by I2S show `mutation_op = None` in the DB lineage
- Seeds produced by havoc show `mutation_op = "ByteFlipMutator,..."` etc.
- To identify I2S-produced seeds, look for: `mutation_op IS NULL` AND the seed is from a cmplog/value_profile_cmplog fuzzer AND the controlling bytes changed from parent to child
- Confirmed: lcms BC01, seed `e0b9d6ba5f14d659` → `c5a238c9e6b7b24f` changed bytes[16:20] from `52474220` (RGB) to `4c616220` (Lab) with no recorded mutation ops, at execs=7 (near-instant discovery). This is a classic I2S substitution.

**Discovery time correlation:** I2S seeds are typically discovered very early (within the first few seconds) because the tracing stage runs on initial seeds immediately. A resolving seed with `discovery_time_s < 60` and `mutation_op = None` in its ancestry is strong evidence of I2S.

## Source Code Locations

- Fuzzer implementations: `libafl_fuzzbench/{naive,cmplog,value_profile,value_profile_cmplog}/src/lib.rs`
- LibAFL paper: `libafl.pdf`
- Barrier type analysis: `notes/n4_vs_cmplog_barrier_types.md`
- Experiment (blocker_10): `notes/blocker_10.md`

### Type 4: I2S Inequality Substitution Barrier

**Pattern:** Branch condition is a strict inequality (`a > b` or `a < b`) where `b` is a constant
threshold. I2S logs the pair (a, b) and substitutes `a = b` (the comparand), but `b > b = False` --
the substituted value still hits the wrong branch side.

**Example:** lcms `_validatedVersion()` -- `if (*pByte > 0x09)` with initial pByte[0]=0x02.
Also: lcms `_cmsReadHeader()` -- `if (TagCount > MAX_TABLE_TAG)` (100) with initial TagCount=10.

| Fuzzer | Performance | Why |
|--------|-------------|-----|
| naive | Wins | Havoc freely produces any byte value; P(byte > threshold) is high for large threshold space |
| cmplog | Fails | I2S substitutes exactly the comparand (threshold), which is NOT > threshold |
| value_profile | Wins | No I2S, Hamming gradient may help incrementally |
| value_profile_cmplog | Fails | Same as cmplog |

**Diagnostic signal:** Corpus analysis shows exactly 0 seeds with comparand value in corpus
(minimizer discards them -- same coverage as original). Seeds cluster at initial value and 0x00,
never at threshold+1. Fix: seed with input value > threshold, OR extend I2S to try `threshold+1`.

### Type 5: I2S Switch-Case Valid-Value Barrier

**Pattern:** A switch statement over N recognized constants. I2S substitutes each case constant in
turn (good for per-case path exploration) but never generates values outside the case set, permanently
blocking the `default` branch.

**Example:** lcms `validDeviceClass()` -- switch over 7 ICC class signatures. cmplog corpus has 5
distinct valid classes (all recognized cases explored) but 0 seeds with unrecognized DeviceClass
(default case never hit).

| Fuzzer | Performance | Why |
|--------|-------------|-----|
| naive | Wins | Havoc corrupts bytes accidentally to unrecognized values; most random 4-byte values miss all 7 cases |
| cmplog | Fails | I2S logs all case constants, substitutes recognized values, never generates values outside the set |
| value_profile | Wins | Same as naive |
| value_profile_cmplog | Fails | Same as cmplog |

**Diagnostic signal:** cmplog corpus contains all valid switch-case variants but zero invalid/default
values. naive corpus has only the initial seed's case value but occasional accidental invalid values.
Fix: add a seed with an unrecognized value, or extend I2S to also try one non-case value per switch.

### Type 6: I2S Corpus Inflation / Size Barrier

**Pattern:** Blocking branch requires very short inputs (below a struct read size). I2S-generated
derivatives maintain the initial seed's large size, biasing all subsequent havoc away from
the small-input regime. No active value-locking -- the harm is through corpus composition.

**Example:** lcms `_cmsReadHeader()` B68 -- `io->Read(io, &Header, 128, 1) != 1` requires input
< 128 bytes. Initial seed is 564 bytes; all I2S derivatives are 300-600 bytes; smallest cmplog seed
after 12h is 129 bytes (1 byte above the trigger boundary).

| Fuzzer | Performance | Why |
|--------|-------------|-----|
| naive | Wins | Without I2S flood, havoc on 564-byte parent can reach sub-128-byte range via delete chains |
| cmplog | Fails | I2S fills corpus with 400-600 byte seeds; havoc selecting these parents rarely produces sub-128 byte outputs |
| value_profile | Wins | Same as naive |
| value_profile_cmplog | Fails | Same as cmplog |

**Diagnostic signal:** All cmplog seeds > threshold size; all naive seeds span a broader size range
including sub-threshold. Fix: add explicit short/boundary seeds to corpus, or use a smaller initial
seed (132-byte instead of 564-byte for lcms ICC).

## I2S Harm Mechanism Summary

| Mechanism | Description | Affected Branch Types | Fix |
|-----------|-------------|----------------------|-----|
| Equality substitution helps | I2S finds magic constants | Magic value == checks | (positive, no fix needed) |
| Inequality substitution fails | I2S substitutes threshold; still hits False | a > b, a < b checks | Seed with value > threshold; or I2S tries threshold+1 |
| Switch-case locks | I2S substitutes all case values; blocks default | switch default: paths | Seed with non-case value; or I2S tries one non-case value |
| Corpus inflation | I2S derivatives maintain large size; blocks small-input paths | Size-based early exits | Add short seeds; use smaller initial seed |
| Structural invariant destruction | I2S changes bytes that participate in cross-field invariants | Cross-table relationships | (harfbuzz / htslib pattern -- see separate notes) |
