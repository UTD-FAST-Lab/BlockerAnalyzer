# Fuzzer Mechanism Library

Paste-ready descriptions of each LibAFL fuzzer variant's instrumentation,
feedback signal, and mutator stack. Used by `tools/study_units.py
evidence-per-branch` to populate the `Mechanism:` field of the structured
prompt fed to `feature-hypothesis-generator`.

**Scope**: only directly observable / implementation facts (what's
instrumented, what's recorded, what mutators run, what `mutation_op`
labels appear in seed metadata). No claims about when a fuzzer helps or
fails — those are exactly the hypotheses the agent is being asked to
generate from per-branch evidence. Embedding "fails on X" claims here
anchors the agent toward the library's interpretation instead of the
data's.

---

## naive

**Instrumentation**: SanitizerCoverage edge counters
(`__sanitizer_cov_trace_pc_guard*` callbacks compiled in via clang
`-fsanitize-coverage=...`).

**Feedback**: per-edge hit-count bucket; a new bucket triggers a
corpus-add (LibAFL `MaxMapFeedback` over the edge map).

**Mutators**: havoc + token stack — `ByteFlipMutator`, `ByteRandMutator`,
`ByteIncMutator`, `ByteDecMutator`, `ByteAddMutator`, `WordAddMutator`,
`DwordAddMutator`, `QwordAddMutator`, `BytesDeleteMutator`,
`BytesInsertMutator`, `BytesInsertCopyMutator`, `BytesExpandMutator`,
`BytesRandInsertMutator`, `BytesRandSetMutator`, `BytesCopyMutator`,
`BytesSwapMutator`, `WordInterestingMutator`, `DwordInterestingMutator`,
`ByteInterestingMutator`, `CrossoverInsertMutator`,
`CrossoverReplaceMutator`, `TokenInsert`, `TokenReplace`.

**Observed `mutation_op` in seed metadata**: any of the above. No I2S.

**Per-execution cost**: one edge-counter increment per executed BB edge.

## cmplog (input-to-state)

**Instrumentation**: naive's edge counters **plus** integer-CMP
interception (`__sanitizer_cov_trace_cmp1/2/4/8`) and
string/memory-CMP interception (`__sanitizer_weak_hook_strcmp`,
`__sanitizer_weak_hook_memcmp`, etc.). Each CMP callback records
both operands into a per-execution `CmpLogObserver` buffer keyed by
PC.

**Feedback**: same edge-bucket signal as naive. The CMP buffer is
consumed by the mutator, not by feedback.

**Mutators**: naive's havoc + token stack **plus** `I2SRandReplace`.
`I2SRandReplace` reads the post-execution `CmpLogObserver` buffer,
picks a CMP entry, scans the input for byte sequences matching one
operand, and substitutes the other operand at those offsets.

**Observed `mutation_op` in seed metadata**: havoc/token names plus
`I2SRandReplace` (`I2SRandReplace` is exclusive to cmplog and
value_profile_cmplog — its presence in a seed's `mutation_op` is
direct evidence one of those two fuzzers found it).

**Per-execution cost**: edge increment + one callback per intercepted
CMP per execution + post-execution CMP-buffer processing.

## value_profile (CMP_MAP gradient)

**Instrumentation**: naive's edge counters **plus** integer-CMP
interception, but instead of buffering operands per execution (cmplog),
each CMP callback writes into a `CMP_MAP` keyed by (PC, operand-distance
bucket). The distance bucket is a coarse encoding of how close the two
operands were (Hamming distance bucket for `trace_cmp*`; matching-prefix
length for string/memory CMPs).

**Feedback**: edge-bucket signal **plus** new-CMP_MAP-bucket signal
(both via `MaxMapFeedback`-style coverage). An input that produces a
CMP-operand pair closer to matching than any previously-seen pair
adds a new CMP_MAP bucket and is preserved as corpus.

**Mutators**: naive's havoc + token stack. No `I2SRandReplace`.

**Observed `mutation_op` in seed metadata**: havoc/token names only.
Absence of `I2SRandReplace` is direct evidence the seed was found by
naive or value_profile.

**Per-execution cost**: edge increment + CMP_MAP update per intercepted
CMP per execution.

## value_profile_cmplog (I2S + CMP_MAP, stacked)

**Instrumentation**: union of cmplog and value_profile — edge counters,
per-execution CMP buffer (`CmpLogObserver`), and CMP_MAP gradient buckets.

**Feedback**: edge-bucket + CMP_MAP-bucket signals.

**Mutators**: naive's havoc + token stack **plus** `I2SRandReplace`.

**Observed `mutation_op` in seed metadata**: havoc/token names plus
`I2SRandReplace`.

**Per-execution cost**: edge increment + CMP-buffer record + CMP_MAP
update per intercepted CMP per execution.
