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

**Observed `mutation_op` in seed metadata**:
<!-- TODO(i2s-logging-bug): the current LibAFL fuzzbench build does NOT
     wrap I2SRandReplace in LogMutationMetadata, so the string
     "I2SRandReplace" never appears in `.metadata`. Instead, I2S finds
     surface as seeds whose metadata has ParentInfo but NO mutator-name
     list — these render as `mutation_op = -` in `db_query.py lineage`
     output and `resolving_seeds.mutation_op IS NULL` in SQL.
     Confirmed 2026-05-17: naive/vp produce ZERO such seeds in 6000
     samples; cmplog/vpc produce them at ~0.1–0.3%. This is a LOWER
     BOUND ("floor") — some I2S finds leak into the havoc bucket
     because other stages wrap I2S as a sub-mutator and tag the result
     with their own havoc/token list. When the logging fix lands,
     revert this caveat and require the literal `I2SRandReplace`
     string instead. -->
havoc/token names; **plus** silent ParentInfo-only entries
(`mutation_op = -` in lineage output) that — in cmplog/vpc only —
indicate an I2SRandReplace find under the current build. The dash
rows are exclusive to cmplog and value_profile_cmplog **within the
original 4-fuzzer canonical set**; there their presence in a winning
seed's ancestor chain is direct (lower-bound) evidence of I2S
contribution.
<!-- CAVEAT(10-fuzzer set, 2026-05-27): dash-row = I2S only holds when
     comparing against naive / value_profile. `mopt` and `grimoire`
     wrap their mutators in LineageMutatorWrap with an EMPTY names list,
     so they ALSO emit nameless (`mutation_op = -`) rows for non-I2S
     finds — see the mopt / grimoire sections. Against those two the
     dash signal is NOT I2S-exclusive. fast / minimizer / naive_ctx /
     naive_ngram4 use plain LineageMutator (names captured), so they do
     NOT emit dash rows and the signal stays clean against them. -->

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

**Observed `mutation_op` in seed metadata**: havoc/token names only —
no ParentInfo-only entries (no `mutation_op = -` rows). Absence of
the dash signal is direct evidence the seed was found by naive or
value_profile, not by an I2S stage.
<!-- TODO(i2s-logging-bug): when the I2SRandReplace logging fix lands,
     this section becomes "Absence of `I2SRandReplace` is direct
     evidence ..." again. See the cmplog section above for the floor
     caveat. -->


**Per-execution cost**: edge increment + CMP_MAP update per intercepted
CMP per execution.

## value_profile_cmplog (I2S + CMP_MAP, stacked)

**Instrumentation**: union of cmplog and value_profile — edge counters,
per-execution CMP buffer (`CmpLogObserver`), and CMP_MAP gradient buckets.

**Feedback**: edge-bucket + CMP_MAP-bucket signals.

**Mutators**: naive's havoc + token stack **plus** `I2SRandReplace`.

**Observed `mutation_op` in seed metadata**: havoc/token names; **plus**
silent ParentInfo-only entries (`mutation_op = -` in lineage) — same
floor signal as cmplog. See the cmplog section's
`TODO(i2s-logging-bug)` note.

**Per-execution cost**: edge increment + CMP-buffer record + CMP_MAP
update per intercepted CMP per execution.

## naive_ctx (context-sensitive edge coverage)

**Instrumentation**: naive's SanitizerCoverage edge counters, but the
executor installs a `CtxHook` (`HookableInProcessExecutor`). The hook
keeps a running hash of the current call context (caller chain) and
folds it into the edge-map index, so the same basic-block edge is
recorded at different map slots depending on the call path that
reached it.

**Feedback**: the same `MaxMapFeedback` edge-bucket signal as naive,
computed over the context-indexed map — a "new bucket" is a new
(call-context, edge) pair rather than a bare edge.

**Mutators**: naive's havoc + token stack. No `I2SRandReplace`, no
CMP_MAP. Stages are `[mutator]` (`LineageMutator`, names captured).

**Observed `mutation_op` in seed metadata**: havoc/token names only;
no ParentInfo-only / dash rows.

**Per-execution cost**: one edge-counter increment per executed edge
plus a context-hash update per call/return.

## naive_ngram4 (n-gram-4 path coverage)

**Instrumentation**: naive's edge counters, but the executor installs
an `NgramHook` (`HookableInProcessExecutor`) that folds a rolling
history of the last 4 edge IDs into the map index. A map slot
therefore encodes a length-4 edge path (an n-gram of N=4) rather than
a single edge.

**Feedback**: `MaxMapFeedback` over the n-gram-indexed map — a "new
bucket" is a previously-unseen 4-edge path tuple.

**Mutators**: naive's havoc + token stack. No I2S, no CMP_MAP. Stages
are `[mutator]` (`LineageMutator`, names captured).

**Observed `mutation_op` in seed metadata**: havoc/token names only;
no dash rows.

**Per-execution cost**: edge increment plus a rolling 4-edge-history
update per executed edge.

## mopt (MOpt mutation-operator scheduling)

**Instrumentation**: naive's edge counters only. No CMP interception,
no CMP_MAP.

**Feedback**: naive's `MaxMapFeedback` edge-bucket signal, unchanged.

**Mutators**: the same havoc + token operator set as naive, but driven
by `StdMOptMutator` (`StdMOptMutator::new(state, havoc+tokens, 7, 5)`).
MOpt keeps per-operator success statistics and uses a particle-swarm
-optimised probability distribution (pilot/core phases) to choose
which operators to apply and how to stack them, instead of naive's
uniform random selection. Corpus scheduler is unchanged
(`IndexesLenTimeMinimizerScheduler(QueueScheduler)`); stages `[mutator]`.

**Observed `mutation_op` in seed metadata**: MOpt stacks operators
internally and is wrapped in `LineageMutatorWrap`, which records
execs/elapsed_ms but **no per-operator name list**. MOpt seeds
therefore appear nameless in lineage (rendered as `mutation_op = -`,
the same way as cmplog's I2S finds). NOTE: nameless rows are therefore
NOT exclusive to I2S once mopt is in the fuzzer set — see the cmplog
caveat.

**Per-execution cost**: same as naive (one edge increment per edge);
MOpt's bookkeeping lives in the mutation stage, not per-execution.

## minimizer (calibrated_energy — calibration-scaled mutation budget)

**Instrumentation**: naive's edge counters only.

**Feedback**: naive's edge-bucket `MaxMapFeedback`, plus a
`CalibrationStage` that measures each new corpus entry's execution
time, edge-map fill, and stability into `SchedulerMetadata`/testcase
metadata.

**Mutators / stages**: havoc + token mutator (`LineageMutator`, names
captured) run inside a `StdPowerMutationalStage` rather than naive's
plain `StdMutationalStage`. Stages are `[calibration, power]`. The
power stage derives the number of havoc mutations per seed visit (the
"energy") from a calibration-based `perf_score` — faster, smaller,
more-stable seeds earn more mutations. PowerSchedule is `None`, so the
energy uses ONLY intrinsic calibration and is NOT weighted by how often
a region has been hit. Corpus selection is plain FIFO `QueueScheduler`
(same order as naive).

**Observed `mutation_op` in seed metadata**: havoc/token names
(captured); no dash rows.

**Per-execution cost**: one edge increment per edge, plus a one-time
calibration burst per new corpus entry.

## fast (aflfast_rarity — AFLFast n_fuzz energy weighting)

**Baseline relationship**: identical to `minimizer` (same
`[calibration, power]` stages, same `StdPowerMutationalStage`, same
FIFO corpus order) EXCEPT the corpus scheduler is
`PowerQueueScheduler::fast()`, which sets PowerSchedule `FAST` in
`SchedulerMetadata`. The single-technique delta is therefore `fast`
vs `minimizer`, not vs naive.

**Instrumentation**: naive's edge counters only.

**Feedback**: edge-bucket `MaxMapFeedback` + `CalibrationStage` (as
minimizer).

**Mutators / stages**: `[calibration, power]` with the havoc+token
`StdPowerMutationalStage` (as minimizer). The FAST schedule changes the
`perf_score` energy formula: the per-seed mutation budget is multiplied
by an AFLFast factor based on `n_fuzz` — log2 of how many times that
seed's coverage bucket has been exercised campaign-wide. Rarely-hit
paths get up to 4× energy; saturated paths are damped to 0.4×. Seed
*selection* order is still FIFO (`PowerQueueScheduler::next()` walks the
corpus in order); only the energy allocation differs from minimizer.

**Observed `mutation_op` in seed metadata**: havoc/token names
(captured); no dash rows.

**Per-execution cost**: one edge increment per edge; calibration burst
per new entry; `n_fuzz` bookkeeping per execution.

## grimoire (grimoire_structural — generalization + structural mutators)

**Baseline relationship**: grimoire builds on the full cmplog stack —
it includes the `CmpLogObserver`, the `TracingStage`, and the
`I2SRandReplace` (i2s) stage — and ADDS a `GeneralizationStage` plus
Grimoire structural mutators. The single-technique delta is therefore
`grimoire` vs `cmplog` (both have I2S; grimoire adds generalization +
Grimoire mutators), not vs naive.

**Instrumentation**: cmplog's edge counters + per-execution CMP buffer
(`CmpLogObserver`).

**Feedback**: edge-bucket `MaxMapFeedback`.

**Mutators / stages**: stages are
`[generalization, tracing, i2s, havoc, grimoire]`. `GeneralizationStage`
replaces concrete byte runs in a corpus entry with `<GAP>` placeholders
(a generalised input) by repeatedly re-executing and checking that
coverage is preserved. The Grimoire mutators —
`GrimoireExtensionMutator`, `GrimoireRecursiveReplacementMutator`,
`GrimoireStringReplacementMutator`, `GrimoireRandomDeleteMutator` —
splice and recurse on these generalised token/gap structures
(string-based, grammar-free structural mutation). `I2SRandReplace` (the
cmplog i2s stage) also runs.

**Observed `mutation_op` in seed metadata**: all grimoire stages (i2s,
havoc, grimoire) are wrapped in `LineageMutatorWrap` with **no
per-operator name list**, so grimoire seeds appear nameless in lineage
(`mutation_op = -`). As with mopt, nameless rows are NOT an
I2S-exclusive signal here — and grimoire genuinely runs I2S too, so the
two are not separable from lineage names.

**Per-execution cost**: cmplog's per-CMP cost, plus extra executions
during generalization (each candidate gap is validated by a re-run).
