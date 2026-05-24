# BlockerAnalyzer — Tool Reference

Full CLI reference for `tools/`. Loaded on demand — `CLAUDE.md` keeps a
one-line index per tool plus the pipeline phase map; this file carries the
flags, schemas, and per-tool detail. See the "Typical Workflow" section of
`CLAUDE.md` for the phase ordering that strings these together.

## `tools/blocker_db.py`

Schema-management for `db/blockers.sqlite`. Owns the schema definition
and the `init` command only. Population is handled elsewhere:
`study_units.py add-canonical` writes `branches` + `study_subjects` +
`subject_branches`; `seed_bisect.py` writes the 4 seed tables directly.

```bash
python3 tools/blocker_db.py init    # Initialize schema (idempotent)
```

**Database schema (subject-centric):**

| Table | Purpose | Key fields |
|-------|---------|------------|
| `branches` | One row per admitted blocker. Admission rule: ≥1 canonical subject admits the branch under the per-subject rule below. Branch identity is `(target, file, line, col, blocked_side)`; `function` is descriptive (real C/C++ name, demangled via c++filt; resolved at `add-canonical` time by `extract_functions.extract`). | `target`, `file`, `function`, `line`, `col`, `blocked_side`, `source_line` |
| `study_subjects` | One row per (target, A, B) canonical pair. | `target`, `A`, `B`, `delta_technique`, `n_A`/`n_B`, `mean_auc_*`, `delta_auc`, `p_auc`, `auc_dir`, `mean_final_*`, `delta_final`, `p_final`, `final_dir`, `admissible`, `direction`, `n_branches`, `refreshed_at` |
| `subject_branches` | Per-(subject, branch) row, one per (subject, branch) that meets the **per-subject admission rule**: across the 20 trials of (A, B), ≥1 blocked AND ≥1 resolved at final checkpoint. | `n_A_resolved/_blocked/_unreached`, `n_B_resolved/_blocked/_unreached`, `A_resolved_trials`/`A_blocked_trials`/`B_resolved_trials`/`B_blocked_trials` (JSON arrays of trial numbers), `p_A_blocked`, `p_B_blocked`, `prob_div` (oriented), `avg_dur_A/B`, `dur_div`, `avg_hits_A/B`, `hit_div`, optional `hypothesis_label`, `template_id` |
| `resolving_seeds` | Seeds hitting the **blocked** side (from resolving fuzzers). | `branch_id`, `fuzzer`, `trial`, `seed_id`, `parent_seed_id`, `mutation_op`, `discovery_time_s` |
| `resolving_seed_lineage` | Parent chain for resolving seeds. | `branch_id`, `fuzzer`, `trial`, `seed_id`, `depth`, `ancestor_id`, `mutation_op` |
| `blocking_seeds` | Seeds hitting the **other** side (from blocking fuzzers). | Same schema as `resolving_seeds` |
| `blocking_seed_lineage` | Parent chain for blocking seeds. | Same schema as `resolving_seed_lineage` |

**Trial-list JSON columns:** `A_resolved_trials` etc. store trial numbers
(1..N) as JSON arrays — e.g., `[1, 3, 4, 5, 7, 8, 9]`. Unreached trials are
omitted (derive as `{1..N} − resolved ∪ blocked`). `seed_bisect.py` reads
these to pick a representative resolving/blocking `(fuzzer, trial)` without
re-introducing a per-trial fact table.

**Per-branch divergence tags:** there is no longer a `selection_tags`
table column — tag derivation is done at candidate-build time from
`subject_branches.{prob_div, dur_div, hit_div}` using thresholds:
`prob_div ≥ 1.0`, `dur_div > 8.0` h, `hit_div > 100`.

## `tools/seed_bisect.py`

Finds which seeds in each fuzzer's queue hit each confirmed blocker. Runs **one Docker container per target** — inside, scans each unique queue once checking ALL target branches simultaneously.

```bash
python3 tools/seed_bisect.py build --target <name>      # Build Docker image (one-time)
python3 tools/seed_bisect.py scan --target <name> --queue-base ./out \
        [--branches-from-csv csvs/blocker_representatives.csv] \
        [--queue-sample-size 10000]                     # Docker scan only → results.json
python3 tools/seed_bisect.py insert --target <name> --results <path> --queue-base ./out
python3 tools/seed_bisect.py run --target <name> --queue-base ./out \
        [--branches-from-csv csvs/blocker_representatives.csv]  # scan + insert in one step
python3 tools/seed_bisect.py plan --target <name> --queue-base ./out
```

`scan` and `insert` are separated so multiple targets can scan in parallel (Docker containers) and insert sequentially (no DB contention). Results are saved to `db/bisect_results/<target>_results.json`.

**End-to-end flow:**

1. **Select branches and trials** (`get_branches_to_process`): For each branch, pick **exactly ONE** resolving `(fuzzer, trial)` and ONE blocking `(fuzzer, trial)` (lexicographic min). One queue per direction is enough evidence; scanning every resolving/blocking trial wasted bisection time on huge queues. With `--branches-from-csv PATH`, only the branches listed in the CSV are processed (used after `select_candidates.py` to scope work to the 100–200 selected branches).

2. **Build jobs** (`build_jobs`): Group work by queue directory. For each branch:
   - The chosen resolving `(fuzzer, trial)` → job searching for seeds that hit the **blocked side** → `resolving_seeds`
   - The chosen blocking `(fuzzer, trial)` → job searching for seeds that hit the **other side** → `blocking_seeds`
   - Jobs sharing the same queue path are scanned together in one pass.

3. **Optional sampling** (`--queue-sample-size N`): if set and a queue has more than N seeds, randomly sample N seeds via a temp dir of symlinks; the sampled mirror is mounted into the container as `/queues`. Insert phase reads the original (full) queue for `.metadata` lookup, so lineage tracing is unaffected. Use 10000 for sqlite3/bloaty (~100K+ seeds per queue at n=10).

4. **Container scan** (`seed_scanner.py` baked into image): One Docker container per target. For each queue:
   - **10-bucket bisection**: split seeds into 10 buckets, run each bucket as a batch through `FUZZ_BIN` (many seeds per invocation, one profraw), merge → one `llvm-cov show` per bucket checking ALL active branches at once.
   - For branches hit in a bucket, recurse (split into 10 again). At ≤10 seeds, test individually.
   - **Early-stop per branch** at `max_seeds` hits — removes completed branches from active specs so deeper buckets skip them.
   - Output: `results.json` with `{branch_id: [seed_name, ...]}` per queue.

5. **Insert into DB** (`insert_seeds_and_lineage`): For each hitting seed, parse its `.metadata` file for parent + mutation ops, insert into seed table, walk parent chain (up to 50 depth) for lineage table.

**`max_seeds` semantics:** The limit is per **(branch, queue)**. With one queue per direction (after step 1), a branch accumulates at most `max_seeds` resolving + `max_seeds` blocking seeds.

**Options:** `--max-seeds N` (default 10; was 5, then 50 — 10 keeps byte-diff stable while bounding scan time), `--batch-size N` (seeds per `FUZZ_BIN` invocation, default 500), `--branches-from-csv PATH` (scope branches), `--queue-sample-size N` (per-queue sample cap, default 0 = no sampling).

**Existing data caveat:** the 2026-05-16 5-target bisect was populated at the old default `max_seeds=5`. The bytes per direction in the smoke-test prompts therefore come from up to 5 seeds, not 10. When scaling to the 50-rep pilot (or beyond), re-run seed_bisect with the new default to refresh those branches; old branches outside the pilot retain max=5 data until refreshed.

**Docker images:** Named `libafl-{target}-cov`, built from `docker/Dockerfile.coverage-base` + `docker/targets/Dockerfile.{target}.cov`.

**LibAFL metadata format:** Each seed `HASH` has a `.HASH.metadata` JSON file containing:
- Parent info: `parent_id`, `parent_file` (hex hash of parent seed), `execs`, `elapsed_ms`
- Coverage map: list of coverage index IDs
- Mutation ops: list like `["ByteRandMutator", "BytesDeleteMutator"]`

## `tools/subject_significance.py`

Per-subject coverage-curve scalars + Mann-Whitney U-test for the
metaphorical-testing pipeline. Reads `out/coverage_ts/<target>/<fuzzer>/trial<N>/coverage_timeseries.csv`
(produced upstream by `libafl_fuzzbench/docker/run_coverage_timeseries.sh`).

```bash
python3 tools/subject_significance.py per-trial \
    [--targets curl harfbuzz ...] [--fuzzers naive cmplog ...] \
    [--output csvs/subject_per_trial.csv]

python3 tools/subject_significance.py pair \
    [--targets curl harfbuzz ...] [--alpha 0.05] \
    [--output csvs/subject_pair_significance.csv]
```

Defaults write to `csvs/subject_per_trial[_<targets>].csv` and
`csvs/subject_pair_significance[_<targets>].csv`. When `--targets` is
explicit, the target list is appended to the filename so per-target runs
don't overwrite each other.

`per-trial` emits one row per (target, fuzzer, trial) with
`auc_branch_seconds` (trapezoidal AUC of the coverage-over-time curve),
`auc_normalized`, `final_branches`, plus data-quality columns.

`pair` emits one row per canonical (target, A, B) subject with `delta_auc`,
`p_auc`, `delta_final`, `p_final`, and an advisory `admissible` flag.
**Important:** at n=3 vs n=3 the smallest two-sided MW p-value is 0.10, so
`admissible` is structurally False until trials per arm reach ≥5. Use the
delta columns as ranking signals at low n.

`CANONICAL_PAIRS` is locked to the four one-technique-delta pairs:
`(cmplog, naive, I2S)`, `(value_profile, naive, value_profile)`,
`(value_profile_cmplog, cmplog, value_profile)`,
`(value_profile_cmplog, value_profile, I2S)`.

## `tools/study_units.py`

Per-subject blocker tables for the metaphorical-testing pipeline. Adds
two tables to `db/blockers.sqlite`:

- `study_subjects` — one row per (target, A, B) with significance stats
  (delegated to `subject_significance.pair_significance`) plus a `direction`
  column ('A>B' / 'B>A' / 'tie') used to orient divergences.
- `subject_branches` — one row per (subject, branch) for branches that
  were *input-dependent within the subject* (resolved by ≥1 A or B trial).
  Stores per-fuzzer per-status counts, per-fuzzer p_blocked/avg_dur/avg_hits,
  and **direction-oriented** divergences `prob_div`, `dur_div`, `hit_div`
  (positive ⇒ the loser is worse than the winner at this branch).

```bash
python3 tools/study_units.py init                           # Idempotent — preserves data
python3 tools/study_units.py add --target lcms \
        --A value_profile_cmplog --B value_profile          # Register/refresh ONE subject
python3 tools/study_units.py add-canonical                  # All 4 canonical pairs × all targets
python3 tools/study_units.py list                           # Tab-sep summary of all subjects
python3 tools/study_units.py top --subject-id N --k 20 \
        [--policy strict|majority|all]                      # Ranked candidate B-unique blockers
```

**Policy semantics:** `strict` requires winner resolved every trial AND
loser resolved zero trials (default — clean attribution). `majority` relaxes
to ≥⌈n/2⌉ vs ≤⌊n/2⌋. `all` disables filtering and shows raw ranking.

**Ranking** sorts by `prob_div DESC, dur_div DESC, hit_div DESC` — three
interpretable columns instead of one opaque weighted score.

**`evidence-per-branch` subcommand** assembles the structured prompt for
`feature-hypothesis-generator` (push-mode). Emits sections: BLOCKER /
TRIAL VECTOR / DECISIVE PAIRS / SOURCE CONTEXT / BRANCH SEEDS /
MECHANISM CONTEXT / TASK (full layout below). Collapses ALL canonical pairs satisfying ≥8/≥8
at this branch into a single prompt; verification is scoped to the
decisive fuzzers only.

```bash
python3 tools/study_units.py evidence-per-branch \
    --target curl --branch-id 26 \
    [--winner-threshold 7] [--loser-threshold 7] \
    [--admissible-only | --no-admissible-only] \
    [--mechanism-library fuzzer_mechanism_library.md] \
    [--queue-base out] \
    [--source-lines 30] [--seeds-per-side 5] [--seed-bytes 64] \
    [--per-role-cache db/per_role_coverage] \
    [--callers-index db/callers_index] \
    [--trace-callers 1] [--caller-context 10] [--full-body-threshold 40] \
    [--call-chain-depth 8] [--call-chain-per-hop 2] \
    [--hit-divergence-rows 15] [--hit-divergence-min-ratio 3.0] \
    [--output -]
```

Reads `study_subjects` + `branches` + `subject_branches` for trial counts
and decisive-pair classification; the per-fuzzer trial vector is
assembled by cross-subject join on `subject_branches` (reference fuzzers
with no admitting subject get blank stats and `-` shape character); reads
`resolving_seeds` + `blocking_seeds` for branch-shared winner-resolving and
loser-blocking seed examples (one section per branch, not per pair —
seeds are tagged with the actual `(fuzzer, trial)` that found them);
reads the per-role cov reports from `db/per_role_coverage/` (when
present) to render the SOURCE CONTEXT overlay, HIT-COUNT DIVERGENCE, and
DIVERGENT BRANCHES sections; reads `db/callers_index/<target>.json`
for the cross-file 1-hop caller block and the call-chain signatures;
splices the per-fuzzer mechanism paragraphs from
`fuzzer_mechanism_library.md`. Falls back to a static ±N source window
when the per-role cov cache is missing. The output prompt is what you
feed to the agent (one `(target, branch_id)` per agent invocation).

**Prompt section layout (in emission order):**

1. **BLOCKER** — branch identity (target, branch_id, file:line:col, enclosing function, source line, blocked side).
2. **TRIAL VECTOR** — per-fuzzer (n=10) resolved/blocked/unreached counts with role tags (winner/loser/REFERENCE).
3. **DECISIVE PAIRS (n)** — per pair satisfying ≥winner/loser thresholds: subject id, counts, avg duration blocked, avg hits, divergences (prob/dur/hit), subject-level Δ_AUC / p_AUC / Δ_Final / p_final.
4. **SOURCE CONTEXT (per-role coverage overlay)** — per-line `[W]`/`[L]`/`[B]`/`[ ]` hit diff over the enclosing function (full body, signature padded) + 1-hop caller block (full body if ≤ `--full-body-threshold` lines, else ±`--caller-context` around the call site). Plus call-chain signatures for depths 2..`--call-chain-depth` (no overlay, just `caller_func (file:start-end, calls X at line Y)`).
5. **HIT-COUNT DIVERGENCE** — per-function W vs L invocation counts (entry-line count as proxy), filtered to functions with ≥`--hit-divergence-min-ratio` ratio or one side zero. Sorted by absolute count diff.
6. **DIVERGENT BRANCHES (on call chain, rough order)** — per-branch W/L T/F direction counts for branches in chain functions only (enclosing + 1-hop + chain). Ordered by call-chain depth (descending) then source line (ascending) to approximate execution chronology. Off-chain divergences summarized as a single count line.
7. **BRANCH SEEDS (shared across decisive pairs)** — one block per direction: winner-resolving seeds + loser-blocking seeds, each tagged with `(fuzzer, trial)` and shown as size + mutation-op chain + hex+ASCII dump (first `--seed-bytes` bytes). Followed by BYTE DIFF: per-offset W vs L byte-set comparison, filtered to "informative" offsets (sets differ AND ≤4 distinct bytes on at least one side) — surfaces input-byte→gate-operand dataflow hints.
8. **MECHANISM CONTEXT** — canonical paragraph per **involved** fuzzer from `fuzzer_mechanism_library.md`.
9. **TASK** — agent instruction (single-pair vs multi-pair phrasing; VERIFICATION SCOPE restricted to involved fuzzers).

### Function-name resolution

`branches.function` is populated at `add-canonical` time:
`study_units.py.build_function_index(target)` imports
`extract_functions.extract(target)`, which runs `llvm-cov export` inside
`libafl-<target>-cov` Docker (~1–2s per target), then batch-demangles the
names via `c++filt`. The result is held in memory and used at upsert time —
no on-disk sidecar.

If Docker is unavailable or the coverage image is missing, the lookup falls
back to `basename(file)` with a stderr warning, and the run still succeeds.
The schema's UNIQUE constraint excludes `function` (branch identity is
`(target, file, line, col, blocked_side)`), so a subsequent run with the
function index available will refresh in place via `ON CONFLICT … DO UPDATE
SET function = COALESCE(excluded.function, branches.function)`.

## `tools/check_analysis.py` — validate agent analysis.json against the prompt

Per-branch analyses produced by the hypothesis-generator agent must
follow the structured schema embedded in the prompt's TASK section.
This script catches hallucination and schema drift before downstream
classification consumes the data.

```bash
python3 tools/check_analysis.py prompts/<group>/NN_<target>_<bid>.analysis.json
python3 tools/check_analysis.py --recursive prompts/         # all analyses
```

Checks performed:
1. Required top-level fields present + non-empty (`branch_id`, `target`,
   `summary_one_line`, `pair_decision`, `hypotheses`, `evidence_trail`,
   `mechanism_consistency_check`, `falsifiability`,
   `weakest_evidence_point`, `confidence`).
2. `evidence_trail` is a non-empty list; each entry carries
   `claim` + `cited_section` + `cited_locator` + `exact_quote`.
3. **Every `exact_quote` appears LITERALLY in the sibling .prompt.md**
   (whitespace-tolerant substring check). This is the core hallucination
   filter — claims with quotes that aren't actually in the prompt are
   automatically flagged.
4. `cited_section` names a real section of the prompt
   (BLOCKER, TRIAL VECTOR, DECISIVE PAIRS, SOURCE CONTEXT,
   HIT-COUNT DIVERGENCE, DIVERGENT BRANCHES, BRANCH SEEDS, BYTE DIFF,
   MECHANISM CONTEXT).
5. `mechanism_consistency_check`: if `claimed_mechanism` contains
   "I2S" or "I2SRandReplace", `verified_in_lineage` MUST be `true` —
   OR `verification_method` must explain (>= 20 chars) why verification
   was not possible. Forces the agent to invoke `db_query.py lineage`
   on a winning seed before claiming I2S did the work.
6. `pair_decision` matches `hypotheses` count: `single_feature` → 1,
   `multi_feature` → ≥2.
7. Each `hypotheses[i].covers_pairs` label matches a decisive-pair label
   from the prompt's DECISIVE PAIRS section (e.g. "cmplog>naive (I2S)").

Exit code: 0 = all clean; 1 = at least one violation; 2 = usage error.

## `tools/db_query.py` — agent-facing pull queries (lineage, more-seeds)

Companion to the push-mode prompts. The prompt carries the core
evidence for the common case; this CLI is the **escape hatch** when
the agent needs more detail than the prompt embeds. The prompt's TASK
section ends with an explicit pointer to this tool.

```bash
python3 tools/db_query.py lineage \
    --branch 19 --role W --fuzzer cmplog --trial 1 \
    --seed 006459fd40731a4e
    # ancestor chain for a specific seed (up to 50 levels). Useful for
    # mechanism attribution — was `I2SRandReplace` in the chain that
    # produced this cmplog-winning seed?

python3 tools/db_query.py more-seeds \
    --branch 19 --role W [--fuzzer cmplog] [--limit 20] \
    [--show-bytes 64] [--queue-base out]
    # additional seeds beyond the 5 the prompt shows. Capped by what
    # seed_bisect actually stored (max_seeds default is now 10 per branch ×
    # direction, but the 5-target DB was populated at the old default 5
    # — re-run seed_bisect with the new default if you
    # need more raw material).
```

`--role W` = winner-resolving (`resolving_seeds` / `resolving_seed_lineage`).
`--role L` = loser-blocking (`blocking_seeds` / `blocking_seed_lineage`).

Both subcommands are read-only. Designed to be invoked by the
hypothesis-generator agent during analysis (the agent has `Bash(*)`
in `.claude/settings.json`). The push-mode prompt remains the canonical
audit record; queries are unlogged — if reproducibility matters for a
particular verdict, copy the query's output into the templates'
`feature_spec.json` evidence trail manually.

## `tools/per_role_coverage.py` — W vs L cov dumps per branch

Per-branch coverage runner that produces the source dumps powering the
SOURCE CONTEXT overlay (§4 of the prompt layout). For each branch with decisive pairs,
unions all seeds in `resolving_seeds` as the **W** set and all seeds in
`blocking_seeds` as the **L** set (any fuzzer — the seed-bisect fuzzer
tag is provenance only; the side a seed took is what matters), then
runs each set through `libafl-<target>-cov` and dumps llvm-cov show
annotated source for the blocker's file plus any 1-hop caller files
from the callers index. Output cached at
`db/per_role_coverage/<target>/<branch_id>/{W,L}/branch_coverage_show.txt`
with `cache_key.txt` = sha1(sorted seed_ids + sorted file list).

```bash
python3 tools/per_role_coverage.py plan     --target curl
python3 tools/per_role_coverage.py generate --target curl \
    [--branches-from-csv csvs/blocker_representatives.csv] \
    [--branch-id 19] [--queue-base out] [--force]
python3 tools/per_role_coverage.py status   --target curl
```

One docker run per target processes all requested branches sequentially
inside. Cache hits are skipped; pass `--force` to regenerate.

## `tools/callers_index.py` — per-target source-grep callers index

One-time per-target source-grep that builds
`db/callers_index/<target>.json` mapping demangled callee name → list
of caller records. Used by `per_role_coverage.py` (to know which caller
files to add to the cov dump) and by the SOURCE CONTEXT overlay (to
render the cross-file 1-hop caller block and the call-chain section).

```bash
python3 tools/callers_index.py build   --target curl \
    [--source-root /src/curl]
python3 tools/callers_index.py inspect --target curl --func Curl_unencode_cleanup
python3 tools/callers_index.py status  --target curl
```

`extract_functions.extract` provides all function ranges; `short_name`
extracts the call-site identifier (last `::` segment, then last `:`
segment to strip the `<basename>:<name>` disambiguator extract_functions
emits for static C functions). One `grep -F -f tokens.txt` per target
inside docker; ~3–30s depending on codebase size.

### Known limits of the source-grep callers index (v1)

- **Function-pointer dispatch breaks the call chain.** curl's
  `handler->done = Curl_http_done` style wiring is not detected; for
  curl/libxml2/openthread the chain typically stops 2–4 hops up rather
  than reaching `LLVMFuzzerTestOneInput`.
- **C++ template / vtable polymorphism not detected.** harfbuzz uses
  templated accelerator structs and operator overloads; the chain
  often only walks a class's own destructor/wrapper.
- **Short-name overlap creates noisy edges in C++ codebases.** For
  harfbuzz, ~1M edges total — many false positives where common
  method names (`init`, `fini`, `sanitize`) match across unrelated
  classes. The "filter to callers whose call_site_line fired in W"
  rule in the overlay reduces noise to a few candidates per branch.
- **Same-file declaration matches.** Destructor or forward-declaration
  lines like `~Foo()` can match the `Foo(` pattern when the class
  name is the same as a constructor; harmless but occasionally
  surfaces a "caller" that is really a declaration site.
- **Execution order in DIVERGENT BRANCHES is rough.** Within a
  function we use source-line order, which is wrong inside loops or
  with gotos. Across functions we use call-chain depth, which is
  correct under non-recursive assumptions.
- **No dataflow / no real CFG.** The BYTE DIFF section is the
  cheap-proxy for "which input bytes flow to the gate". For
  blockers where the operand is computed via a hash, checksum, or
  state machine, the BYTE DIFF will show divergence but not
  necessarily the right bytes to mutate. A real taint analysis
  is the right long-term answer but out of scope for v1.

A real `opt -callgraph` build per target would resolve fn-pointer
dispatch but requires per-target Dockerfile mods and a callgraph
extractor. Considered and deferred: the agent's task is "which
input bytes clear this gate", and a precise call chain to entry
contributes less to that question than the per-role overlay +
BYTE DIFF already do.

## `tools/build_candidates.py` (per-branch, ≥8/≥8 rule)

Reads `study_subjects` + `subject_branches` + `branches` and writes
`csvs/blocker_candidates[_<target>].csv` — **one row per (target, branch_id)**
with all canonical pair-edges satisfying the ≥8/≥8 rule collapsed into a
single record.

```bash
python3 tools/build_candidates.py \
    [--admissible-only | --no-admissible-only] \
    [--winner-threshold 7] [--loser-threshold 7] \
    [--output csvs/blocker_candidates.csv]
```

**Decisive-pair rule (per canonical pair at a branch):**
- `winner_resolved >= --winner-threshold` AND `loser_blocked >= --loser-threshold`.
  Default 7/7 (80% at n=10).
- Per-subject admission already eliminates the (all-unreached, navigation-gap)
  pathology — branches reach `subject_branches` only if some trial blocked AND
  some resolved within the subject. ≥8/≥8 then keeps the strong-signal subset.

A branch is emitted iff it has ≥1 decisive pair (under `--admissible-only`,
the pair's subject must also be admissible).

**Output schema (one row per branch):**
```
target, branch_id, file, function, line, col, side, source_line,
n_decisive_pairs,
decisive_pairs   -- JSON array; each element:
                    {A, B, delta, direction, winner, loser,
                     winner_resolved, loser_blocked, prob_div, dur_div, hit_div}
involved_fuzzers -- JSON array; union across decisive pairs.
                    Synthetic verification scope.
<fuzzer>_resolved/_blocked/_unreached  -- per-fuzzer (4 cols × ≤4 fuzzers),
                                          assembled by cross-subject join on
                                          subject_branches. ONLY fuzzers
                                          appearing in some subject that
                                          admits this branch are populated.
                                          Reference fuzzers (no admitting
                                          subject) are absent — represented
                                          as '-' in the decisive shape.
max_prob_div, max_dur_div, max_hit_div  -- magnitudes across decisive pairs.
```

## `tools/select_representatives.py` (shape × region dedup)

Reads `csvs/blocker_candidates.csv` and writes `csvs/blocker_representatives.csv`
(one rep per group) + `csvs/blocker_dedup_map.csv` (full mapping).

```bash
python3 tools/select_representatives.py \
    [--input csvs/blocker_candidates.csv] \
    [--reps-output csvs/blocker_representatives.csv] \
    [--map-output  csvs/blocker_dedup_map.csv] \
    [--line-bucket 50]
```

**Decisive-only shape** (4-char string, fixed order naive/cmp/vp/vpc):
- `R` — fuzzer is winner in ≥1 decisive pair (`n_resolved ≥ 8`)
- `B` — fuzzer is loser  in ≥1 decisive pair (`n_blocked  ≥ 7`)
- `-` — fuzzer is NOT in any decisive pair at this branch (reference context)

By construction (n=10 + ≥8/≥8), every decisive fuzzer is unambiguously R or B
(≥8R AND ≥8B requires n≥16).

**Group key**: `(decisive_shape, file, function, line // bucket)`. Default
bucket=50 lines. Pick rep per group: highest `(max_prob_div, max_dur_div,
max_hit_div)`, ties by branch_id.

**Mechanism taxonomy**: 11 distinct shapes across the canonical-target candidates.
Top shapes read directly as mechanism families:

| Shape | Reading |
|---|---|
| `BRBR` | Pure I2S — cmp & vpc resolve, naive & vp block |
| `BRR-` | Both techniques individually resolve; vpc non-decisive |
| `--BR` | Narrow VP-controlled — only vpc-vs-vp decisive |
| `B-R-` | vp wins over naive only |
| `BR--` | cmp wins over naive only |
| `-BBR` | Synergy required (i2s_corpus_pollution shape) |
| `RBRB` | I2S *hurts* — vpc loses to vp |
| `BBRR` | I2S doesn't help, only VP works |

**Corroboration honesty (locked 2026-05-06):** non-rep branches stay in
`blocker_dedup_map.csv` as the auditable "implied corroboration" record.
There is NO automatic inheritance into `branch_index.json` — corroboration
count per template = agent-verified count, not group-size-weighted.

## `tools/run_hypothesis_fanout.py`

Prompt-prep + manifest builder. Reads `csvs/blocker_representatives.csv`
**by default** (275 reps); pass `--input csvs/blocker_candidates.csv` to fan
out across all 355. Generates one structured prompt per row via
`tools/study_units.py evidence-per-branch`, writes prompts under
`out/hypothesis_fanout/<group_id>/`, and emits manifest.json.

```bash
python3 tools/run_hypothesis_fanout.py \
    [--input csvs/blocker_representatives.csv] \
    [--outdir out/hypothesis_fanout] \
    [--group-by target-delta | target] \
    [--skip-existing templates/branch_index.json] \
    [--dry-run] [--force]
```

**This script does NOT invoke agents** — `feature-hypothesis-generator`
is a Claude Code subagent dispatched from a Claude session. The manifest
is the dispatch contract:
- Across groups: parallel (one Agent batch per `(target, primary_delta)` group).
- Within group: sequential (each agent sees prior templates on disk and
  can match-existing rather than re-create).

**Grouping**: default `target-delta` (e.g., `lcms__I2S`, `bloaty__value_profile`).
`primary_delta` per branch = delta of the highest-prob_div decisive pair.
Use `--group-by target` to merge all deltas per target (fewer parallel
groups, longer sequential chains).

**Skip behavior**: by default reads `templates/branch_index.json` and
omits any (target, branch_id) already covered. Pass `--skip-existing
/dev/null` to disable.

## `tools/lint_template_shapes.py`

Verifies the agent's per-rep template assignments are consistent with the
decisive-shape × region equivalence rule. Two checks:
1. **Intra-template**: reps assigned to the same template should share a
   single decisive shape. ≥2 distinct shapes per template hints at overlumping.
2. **Cross-template**: a given decisive shape should NOT span ≥2 templates.
   A split shape hints at a missed merge.

```bash
python3 tools/lint_template_shapes.py \
    [--index templates/branch_index.json] \
    [--reps  csvs/blocker_representatives.csv] \
    [--map   csvs/blocker_dedup_map.csv] \
    [--include-legacy] [--show-clean] [--output -]
```

Exit codes: 0=clean, 1=intra-only warnings, 2=cross-template warnings.

## `tools/plot_coverage_curves.py`

Coverage-by-time plot for canonical targets × 4 fuzzers, n=10 trials each.
Each panel shows per-fuzzer thin spaghetti lines (one per trial) plus a
bold mean line, so distributional separation is visible at a glance —
two fuzzers with overlapping means but cleanly displaced per-trial bands
are significant under MW, two with heavy per-trial overlap are not. Reads
`out/coverage_ts/<target>/<fuzzer>/trial<N>/coverage_timeseries.csv`.

```bash
python3 tools/plot_coverage_curves.py
# → out/coverage_curves.png
```

## `fuzzer_mechanism_library.md`

Stable canonical paragraphs describing each canonical fuzzer's mechanism
(naive / cmplog / value_profile / value_profile_cmplog). Used by
`study_units.py evidence-per-branch` to fill the `Mechanism — <fuzzer>:` blocks of
the structured prompt. Edits should be deliberate — the prompt-record
needs to be reproducible across sessions.

## `tools/mechanism_family.py` — deterministic mechanism-family bucketing (step 5a)

`coarse_family(covers_pairs)` maps one hypothesis to a single coarse mechanism
family, as a pure function of the `(winner, loser, technique)` already encoded
in `covers_pairs` — no thresholds re-applied, no prose read. This is the
deterministic first pass of step 5a, and it is robust to the one-trial ≥8/8
cutoff wobble that flips the fine decisive-shape (a branch with `value_profile`
blocked 7/10 vs 8/10 lands in the same family).

An edge `"W>L (T)"` is `T_pro` if the winner carries technique T (it helped),
else `T_anti`. The edge multiset reduces to one family:

| family | meaning |
|---|---|
| `I2S_pro` / `VP_pro` | only that technique's edges, technique helped |
| `I2S_anti` / `VP_anti` | only that technique's edges, technique hurt |
| `synergy` | both techniques help AND every winner is `value_profile_cmplog` (neither single technique suffices; the `-BBR` shape) |
| `independent` | both techniques help, won by single-technique arms (the `BRR-` shape) |
| `mixed` | a technique both helped and hurt at one branch — escape hatch, route to a human |

```bash
python3 tools/mechanism_family.py            # self-test + scan prompts/, print distribution
python3 tools/mechanism_family.py --no-scan  # self-test only
```

Exit codes: 0 = self-test passed and no `mixed` in the scan; 1 = scan found a
`mixed`; 2 = self-test failed. Importable as `coarse_family(covers_pairs)`.

## `tools/build_signature_cards.py` — per-family distiller cards (step 5a Pass A)

Selects every hypothesis whose `covers_pairs` maps (via `coarse_family`) to
`--family`, and emits one **card** per hypothesis: deterministic locators
(`family` (from `coarse_family`, so the distiller frames `mechanism_summary` for
the right family), `analysis_path` (back-pointer to the full `.analysis.json`,
used by Pass B), `target`, `branch_id`, and
`file`/`function`/`line`/`source_line` joined from the candidates CSV) plus the
four free-text fields the distiller normalizes (`what_input_feature`,
`why_winner_satisfies`, `why_loser_doesnt`, `mechanism_attribution`).

```bash
python3 tools/build_signature_cards.py --family I2S_pro \
    [--glob 'prompts/**/*.analysis.json'] \
    [--candidates csvs/blocker_candidates.csv] \
    --out step5a/I2S_pro.cards.json
```

The card JSON is the input to the `hypothesis-signature-distiller` agent
(`.claude/agents/`), dispatched per family with a list of card ids and an
output path. This driver does the deterministic prep (family filter + locator
join + back-pointer resolution + field selection) so the agent only does the
semantic distillation. Pass B (the `signature-feature-classifier` agent) reads
the distiller's `signatures.json` plus this cards file (for `analysis_path` and
the full mechanism text) and clusters the branches itself — there is no
deterministic group-by tool.

## `tools/verify_template.py` — synthetic-harness verification sweep (step 5b)

Runs the dose-response sweep that turns a feature template into a verdict. Reads
`templates/<feature_id>/params.json` (`parameter`, `scan_values`, `fuzzers`,
`trials_per_point`, `duration_s`, `expected_direction`) and builds
`template.c` once per (scan_value, fuzzer), then runs `trials_per_point` trials.

```bash
# serial by default (--jobs 1): the shared host runs other fuzz campaigns.
python3 tools/verify_template.py --template i2s_magic_number_gate
python3 tools/verify_template.py --template <id> --dry-run             # cell matrix, no docker
python3 tools/verify_template.py --template <id> \
    --trials 2 --duration-s 15 --scan-values 1,8                       # smoke
python3 tools/verify_template.py --template <id> --jobs 4              # parallel (only w/ spare cores)
python3 tools/verify_template.py --template <id> --write-spec          # also patch feature_spec.json
```

**Build/run model.** Each fuzzer variant ships a `<fuzzer>_cc` LibAFL compiler
wrapper on PATH in the `libafl-base` image (built from `../libafl_fuzzbench`;
wrappers live at `/build/target/release`). One container per cell:
`<fuzzer>_cc --libafl -D<PARAMETER>=<val> template.c -o /w/harness`, then
`timeout <duration_s> harness -o <corpus> -i <seeds>` per trial. The harness's
`__builtin_trap()` is a `CrashFeedback` objective; solutions land in
`<corpus>/crashes/` (an `OnDiskCorpus`). **crash_count = files in `crashes/`**,
which matches the engine's own `objectives:` counter (verified).

**Output.** Writes `templates/<feature_id>/verification_run.json`:
`results_per_trial[scan_value][fuzzer] = [counts]`, `results_median`, the
`verdict`, and `verdict_signals` (the medians/ratios/strictness it judged on, so
the verdict is auditable). Never clobbers a historical verdict unless
`--write-spec` is given (which patches the `feature_spec.json` `verification`
block in place and appends an auto-verified note).

**Verdict.** Parsed from `params.json:expected_direction` ("WINNER > LOSER"). The
prediction is: winner stays high while loser degrades as the knob grows;
stratification holds at the high-end scan value.
- `reproduced` — winner > loser at high end with margin (ratio ≥ 3 or loser → 0),
  loser degrades from low→high, winner holds, **and** per-trial strict (min
  winner trial > max loser trial at high end).
- `reproduced_in_median` — same but only in medians (per-trial overlap).
- `partially_reproduced` — right direction at high end but weak margin / loser
  didn't clearly drop.
- `refuted` — direction reversed at high end.
- `inconclusive` — no separation, or nothing crashed anywhere (duration too
  short / harness inert).
`verdict_provenance` is recorded as `auto`; the raw counts let a human re-judge.

**Machine-load safety.** `--jobs` defaults to **1** (serial, +1 core). Each cell
pegs a core for `trials × duration_s`. Check `nproc` vs `cat /proc/loadavg` and
`docker ps -q | wc -l` before raising `--jobs`.

**Authoring (5b author half).** `template.c` / `params.json` /
`feature_spec.json` are generated per cluster by the `template-author` agent
from a brief built by `build_template_briefs.py` (below), preflighted by
`check_template.py` (below). Authored templates stage in `step5b/<id>/` and
promote to `templates/<id>/` (reproduced) or `templates/legacy/<id>/`
(genuine_refutation).

## `tools/build_template_briefs.py` — per-cluster authoring brief (step 5b)

For each step-5a cluster (`step5a/<family>/clusters.json`), joins the cluster
definition with (a) its members' distilled signatures
(`step5a/<family>/signatures.json`) and (b) each member's full `.analysis.json`
(via `analysis_path`) into ONE self-contained brief — the only input the
`template-author` agent reads. Carries the harness blueprint already present in
each analysis (`falsifiability.would_be_refuted_by`), the gate signatures, the
decisive winner/loser/technique pairs, and a derived `involved_fuzzers` +
`suggested_axis_partition`.

```bash
python3 tools/build_template_briefs.py --family all                 # all 13 clusters
python3 tools/build_template_briefs.py --feature-id <id>            # one cluster
# -> step5b/briefs/<feature_id>.json
```

Mirrors `build_signature_cards.py` for 5a: deterministic prep so the agent only
does the semantic synthesis (one parameterized `template.c` + `params.json` +
`feature_spec.json`).

## `tools/check_template.py` — deterministic 5b preflight (gates the sweep)

Cheap, judgment-free checks run after the author writes `step5b/<id>/` and before
`verify_template.py`, so an author-agent retry (budget 2) is spent on a real
mechanical defect — never on a scientific refutation.

```bash
python3 tools/check_template.py --template step5b/<feature_id>
# exit 0 = pass; non-zero = fail (reasons printed as author retry feedback)
```

Checks: (1) schema/sanity — `parameter`, `scan_values` (≥2), `fuzzers` ⊆ the
canonical four, `expected_direction` "WINNER > LOSER" with both ∈ `fuzzers`,
`parameter` token present in `template.c`; (2) every `scan_value` compiles
(one container, plain `clang-18 -S`, no fuzzer/link); (3) **dead-knob detection**
— assembly at `min(scan_values)` must differ from `max(scan_values)`; if
identical, the `-D<parameter>` changed no code (the macro name in `params.json`
doesn't match a live `#if/#ifndef` in `template.c`) — the classic author/params
drift that would otherwise flatten the dose-response into a false `refuted`.
Uses `libafl-coverage-base` (has clang-18, smaller than `libafl-base`).
