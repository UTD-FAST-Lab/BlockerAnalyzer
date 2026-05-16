# Fuzzer Mechanism Library

Paste-ready canonical descriptions of each LibAFL fuzzer variant's mechanism.
Used by `tools/study_units.py evidence` to populate the `Mechanism:` field
of the structured prompt fed to `feature-hypothesis-generator`. Stable text
— do not edit casually; the prompt-record is supposed to be reproducible.

Each entry is one paragraph (3–5 sentences). Keep it implementation-grounded
(reference the LibAFL component or feedback name, the feedback signal, and
the failure mode). Avoid marketing language.

---

## naive

Pure coverage-guided baseline. The only feedback signal is **edge coverage**
(SanitizerCoverage edge counters). Each new edge bucket discovered is a
"corpus-add" event; the fuzzer's mutation loop is havoc-style byte mutations
(`ByteRandMutator`, `BytesDeleteMutator`, `BytesInsertCopyMutator`,
`WordInterestingMutator`, etc.) over the existing corpus. **No comparison
introspection, no input-to-state, no gradient.** Naive succeeds when the
search space is small enough that random byte mutation eventually hits the
constraining bytes — for an N-byte equality CMP this is 1/256^N expected
trials. It fails on multi-byte magic numbers, long substitution chains,
and anything requiring directed byte placement. Notable secondary trait:
**high per-trial variance** — a lucky early havoc step can cascade into a
runaway, while an unlucky one (especially multi-byte mutations clobbering
partial matches) collapses progress.

## cmplog (I2S substitution)

Naive + **input-to-state (I2S) substitution**. LibAFL instruments every
integer comparison with a `__sanitizer_cov_trace_cmp*` callback, recording
both operands at runtime into a per-execution **CMP log**. After each
execution, the operands seen are extracted as substitution candidates and
used by the `I2SRandReplace` mutator to splice the *constant operand* of
each comparison back into the input at offsets where the *variable operand*
appears. This converts an N-byte equality CMP from 1/256^N expected trials
to roughly **one mutation step per byte position**, regardless of N.
Cmplog **does not help when**: (a) the constant is computed at runtime
(checksum, hash, length); (b) the comparison is on a value derived from
input via a non-invertible function (state-machine accumulator); (c) the
**dictionary is polluted** — N noise CMPs reduce useful-substitution rate
to K/(K+N) per attempt and compound exponentially over a chain of length
K. Cost: one extra runtime callback per CMP, cheap in practice.

## value_profile (CMP_MAP gradient feedback)

Naive + **CMP_MAP gradient feedback** (a.k.a. value profile). For each
integer comparison, LibAFL records a per-edge bucket keyed by **Hamming
distance between the two operands** (or a coarser partial-match signal for
strings/memory). New buckets are treated as new coverage — so an input
that gets an operand "closer" to the comparand (without yet matching) is
preserved as a corpus member. This produces a **gradient** that guides the
search even when no exact substitution is possible. Value_profile helps
when: (a) the comparand is a runtime-computed value (checksum, hash,
length-prefix); (b) Hamming distance to the target is a useful proxy for
input-distance (true for most arithmetic CMPs, false for cryptographic
hashes that scramble bits). It is **slower than I2S when I2S is
available** — it explores per-bucket gradient steps rather than substituting
the constant in one shot. It is **dilution-immune**: pollute CMPs add
buckets that are already maxed out (perfect distance = no gradient), so
they don't waste mutations the way they consume cmplog's I2S dictionary.

## value_profile_cmplog (I2S + CMP_MAP, both stacked)

The full feedback set: edge coverage **plus** I2S substitution **plus**
CMP_MAP gradient. At low pollute and clean equality CMPs, vpc behaves
like cmplog (I2S substitutes the constant in one step); at high pollute or
when I2S can't substitute (runtime constants, dataflow-distant CMPs), vpc
falls back to value_profile's CMP_MAP gradient. This is the
**synergy_cmplog_plus_vp** pattern: the two mechanisms cover orthogonal
failure modes for one another. The verified `i2s_corpus_pollution`
template demonstrates this — at COST_INNER=4096 cmplog's I2S dictionary
is 4064/4096 polluted and dies (median 0), but vpc's CMP_MAP gradient
carries through (median 6, never zero). Cost: vpc pays cmplog's I2S
overhead plus value_profile's CMP_MAP storage; in practice both are
cheap at the comparison level. Vpc is **strictly dominant on noise-free
benchmarks** but the per-fuzzer divergence comes from the failure-mode
differences, not the cost.
