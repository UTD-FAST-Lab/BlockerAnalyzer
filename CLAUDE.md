# BlockerAnalyzer

A research project for analyzing fuzzing "blockers" — branches that coverage-guided fuzzers fail to reach — and diagnosing why.

## Project Structure

```
BlockerAnalyzer/
├── out/                # Symlink → /20TB/miao/fuzz-blocker (shared with libafl_fuzzbench)
│   ├── coverage_ts/<target>/<fuzzer>/trial<N>/
│   │   ├── coverage_timeseries.csv      # time_s, branch_covered, branch_total
│   │   ├── reports/<time_s>/branch_coverage_show.txt
│   │   └── profraw_ts/running.profdata
│   ├── <target>/<fuzzer>/trial<N>/queue/  # raw LibAFL corpus
│   └── coverage_curves.png                # plot_coverage_curves.py output
├── csvs/               # Analysis CSV outputs (significance, candidates, reps)
├── templates/          # Feature catalog — created by feature-hypothesis-generator agent (step 4)
│   ├── feature_spec.template.json    # JSON schema for feature_spec.json
│   ├── branch_index.json             # Append-only (target, branch_id) → template_id map
│   ├── <feature_id>/                 # One subdir per surviving hypothesis (template.c + params.json + feature_spec.json)
│   └── legacy/                       # Refuted / superseded hypotheses (kept as methodology record)
├── fuzzer_mechanism_library.md  # Per-fuzzer mechanism paragraphs, spliced into prompts by study_units.py evidence-per-branch
├── db/                 # SQLite: blockers.sqlite (branches + study_subjects + subject_branches + seeds)
├── tools/              # Reusable analysis scripts
│   ├── blocker_db.py             # Schema management for the SQLite database (init only)
│   ├── subject_significance.py   # Per-(target,A,B) AUC + final-coverage MW U-test
│   ├── study_units.py            # Per-target coverage walk + per-subject admission + evidence prompt assembly
│   ├── build_candidates.py       # Per-branch ≥8/≥8 aggregation → blocker_candidates.csv
│   ├── select_representatives.py # Shape × region dedup → blocker_representatives.csv + dedup_map
│   ├── run_hypothesis_fanout.py  # Manifest builder; reads reps, calls evidence-per-branch
│   ├── lint_template_shapes.py   # Post-agent: intra/cross-template shape consistency check
│   ├── seed_bisect.py            # 10-bucket bisection to find seeds that hit blocking branches
│   ├── extract_functions.py      # Library: llvm-cov export per target → (file, name, start, end) list; imported by study_units.py at add-canonical time to populate branches.function with the real C/C++ function name (demangled via c++filt)
│   └── plot_coverage_curves.py   # Coverage-by-time spaghetti plot (per-target panels)
├── docker/             # Docker infrastructure for coverage-instrumented builds
│   ├── Dockerfile.coverage-base  # Base image: clang-18, llvm-18, COV_FLAGS env, bakes in the two scripts below → libafl-coverage-base
│   ├── bisect_in_container.py    # 10-bucket bisection seed scanner; run inside container as /seed_scanner.py (also bind-mounted by seed_bisect.py at run time so unrebuilt images still work)
│   ├── run_bisect_entrypoint.sh  # Standalone /run_bisect.sh helper: corpus dir → branch_coverage_show.txt (ad-hoc, not used by seed_bisect.py)
│   └── targets/                  # Per-target coverage Dockerfiles → libafl-<target>-cov
│       ├── Dockerfile.curl.cov
│       ├── Dockerfile.harfbuzz.cov
│       ├── Dockerfile.libpng.cov
│       ├── Dockerfile.libxml2.cov
│       └── Dockerfile.openthread.cov
└── .claude/
    ├── agents/         # Specialized Claude agents for analysis
    └── settings.json   # Project permissions (Bash allowed for all agents)
```

**Note:** `out/` is a symlink to `/20TB/miao/fuzz-blocker`, the same physical
directory as `/home/miao/libafl_fuzzbench/out/`. Coverage Dockerfiles for
the new canonical targets (jsoncpp, woff2 already present in libafl_fuzzbench;
libpng, libxml2, openthread, harfbuzz, curl pending) live in
`libafl_fuzzbench/docker/targets/`, not here.

## Coverage Report Format

Reports are llvm-cov annotated source files. Branch data appears inline:

```
  |  Branch (900:11): [True: 37, False: 4]
  |  Branch (900:31): [True: 2, False: 2]
  |  Branch (900:48): [True: 0, False: 2]
```

`True: 0` or `False: 0` indicates an unvisited branch side.

## Agents

Specialized agents live in `.claude/agents/`:

| Agent | Output | Purpose |
|-------|--------|---------|
| **feature-hypothesis-generator** (Opus) | `templates/<feature_id>/{template.c, params.json, feature_spec.json}` | Hypothesis-generation step of the metaphorical-testing pipeline. Receives a structured prompt (push-mode) emitted by `tools/study_units.py evidence-per-branch` for ONE (target, branch). Diffs winner-resolving vs loser-blocking seed bytes at the highest-prob_div decisive pair, reads source CMP shape, searches `templates/` for prior art, decides whether multi-pair evidence collapses to ONE template or splits into multiple, writes the three template files per surviving hypothesis. Modeled after the `i2s_corpus_pollution` pilot. One per-branch prompt per call; designed for parallel fan-out across (target, branch_id) pairs. |

The metaphorical-testing pipeline uses **push-mode**: the orchestrator
runs `tools/study_units.py evidence-per-branch --target T --branch-id M`
to assemble the structured prompt (BLOCKER / TRIAL VECTOR / DECISIVE
PAIRS / SOURCE CONTEXT / PAIR-N SEEDS / MECHANISM CONTEXT / TASK), then
feeds that prompt to `feature-hypothesis-generator`. The agent never
queries the DB itself — the prompt IS the auditable evidence record.

## Permissions

`.claude/settings.json` grants `Bash(*)` project-wide so agents can run shell
commands without prompting. The DB-population step (per-target coverage walk
in `study_units.py`) needs Bash access to read large `branch_coverage_show.txt`
files under `out/coverage_ts/`.

## Tools

### `tools/blocker_db.py`

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

### `tools/seed_bisect.py`

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

**Options:** `--max-seeds N` (default 5; was 50 — small max suffices for hypothesis evidence), `--batch-size N` (seeds per `FUZZ_BIN` invocation, default 500), `--branches-from-csv PATH` (scope branches), `--queue-sample-size N` (per-queue sample cap, default 0 = no sampling).

**Docker images:** Named `libafl-{target}-cov`, built from `docker/Dockerfile.coverage-base` + `docker/targets/Dockerfile.{target}.cov`.

**LibAFL metadata format:** Each seed `HASH` has a `.HASH.metadata` JSON file containing:
- Parent info: `parent_id`, `parent_file` (hex hash of parent seed), `execs`, `elapsed_ms`
- Coverage map: list of coverage index IDs
- Mutation ops: list like `["ByteRandMutator", "BytesDeleteMutator"]`

### LibAFL Fuzzers

The LibAFL FuzzBench experiment uses 4 fuzzer variants:

| Fuzzer | Technique |
|--------|-----------|
| `naive` | Baseline coverage-guided only |
| `cmplog` | Input-to-state (I2S) comparison logging |
| `value_profile` | Hamming-similarity comparison feedback |
| `value_profile_cmplog` | Both I2S and value profile |

Time-series coverage snapshots:
```
/home/miao/BlockerAnalyzer/out/coverage_ts/<target>/<fuzzer>/trial<N>/reports/<time_s>/branch_coverage_show.txt
```

### `tools/subject_significance.py`

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

### `tools/study_units.py`

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
TRIAL VECTOR / DECISIVE PAIRS / SOURCE CONTEXT / PAIR-N SEEDS /
MECHANISM CONTEXT / TASK. Collapses ALL canonical pairs satisfying ≥8/≥8
at this branch into a single prompt; verification is scoped to the
decisive fuzzers only.

```bash
python3 tools/study_units.py evidence-per-branch \
    --target curl --branch-id 26 \
    [--winner-threshold 7] [--loser-threshold 7] \
    [--admissible-only | --no-admissible-only] \
    [--mechanism-library fuzzer_mechanism_library.md] \
    [--queue-base /20TB/miao/fuzz-blocker] \
    [--source-lines 30] [--seeds-per-side 5] [--seed-bytes 64] \
    [--output -]
```

Reads `study_subjects` + `branches` + `subject_branches` for trial counts
and decisive-pair classification; the per-fuzzer trial vector is
assembled by cross-subject join on `subject_branches` (reference fuzzers
with no admitting subject get blank stats and `-` shape character); reads
`resolving_seeds` + `blocking_seeds` for per-pair winner-resolving and
loser-blocking seed examples; reads source from inside the
`libafl-<target>-cov` Docker image via `docker run --entrypoint sed`;
splices the per-fuzzer mechanism paragraphs from
`fuzzer_mechanism_library.md`. The output prompt is what you feed
to the agent (one `(target, branch_id)` per agent invocation).

### `tools/build_candidates.py` (per-branch, ≥8/≥8 rule)

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

### `tools/select_representatives.py` (shape × region dedup)

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

### `tools/run_hypothesis_fanout.py`

Prompt-prep + manifest builder. Reads `csvs/blocker_representatives.csv`
**by default** (158 reps); pass `--input csvs/blocker_candidates.csv` to fan
out across all 275. Generates one structured prompt per row via
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

### `tools/lint_template_shapes.py`

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

### `tools/plot_coverage_curves.py`

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

### `fuzzer_mechanism_library.md`

Stable canonical paragraphs describing each canonical fuzzer's mechanism
(naive / cmplog / value_profile / value_profile_cmplog). Used by
`study_units.py evidence-per-branch` to fill the `Mechanism — <fuzzer>:` blocks of
the structured prompt. Edits should be deliberate — the prompt-record
needs to be reproducible across sessions.

### Canonical 10-target set (paper scope, locked 2026-05-02)

```
lcms, bloaty, jsoncpp, libpng, libxml2, openthread, sqlite3, woff2, harfbuzz, curl
```

Targets are picked for *technique sensitivity* (rich blocker surface that can
expose I2S vs VP vs naive divergence) and *domain diversity* (font shaping,
binary executables, image codecs, text grammars, network protocols, fonts,
SQL VM, color management).

**Dropped:**
- **mbedtls** — saturated at our 12h budget (all ΔAUC < 3.4M, only 25
  branches in DB; 1–2 orders of magnitude smaller deltas than lcms/bloaty).
  Likely the harness exits a shallow handshake/parser entry. Kept in the DB
  as a "saturated baseline" exhibit but not part of the paper set.
- **libpcap** — data quality. 8 of 12 canonical-fuzzer trials had only one
  checkpoint (cmplog 3/3 single-checkpoint, vp 3/3, naive 2/3, vpc 0/3).
  Trials died before the 30-min checkpoint, making AUC degenerate.

**Setup status (as of 2026-05-02):**
- Ready: `lcms`, `bloaty`, `sqlite3` (3 trials each in `out/coverage_ts/`;
  trials 4–10 fuzzed but not yet extracted for lcms/sqlite3, in flight for
  bloaty extras)
- `Dockerfile.cov` exists but no campaign yet: `jsoncpp`, `woff2`
- Need full plumbing (Dockerfile + Dockerfile.cov + harness wiring):
  `libpng`, `libxml2`, `openthread`, `harfbuzz`, `curl`. Oss-fuzz harnesses
  exist for all of them at `/home/miao/oss-fuzz/projects/<target>/`.

**Per-target divergence assessment** lives in
`.claude/projects/-home-miao-BlockerAnalyzer/memory/project_target_set.md`
— includes domain × format × expected-divergence-driver table and design-space
coverage axes (I2S magic / fixed-keyword / checksum / state / network / font / image).

#### Function-name resolution

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


## Feature Catalog (templates/)

Output of the `feature-hypothesis-generator` agent (step 4). Each entry
`templates/<feature_id>/` is a falsifiable hypothesis about ONE
program-side parameter controlling ONE fuzzer-pair divergence, with three
files:

| File | Purpose |
|------|---------|
| `template.c` | Parameterized C harness. One compile-time `-D` knob is the program-feature axis. |
| `params.json` | Sweep grid (`scan_values`), fuzzer list, trials_per_point, duration_s, acceptance rule, expected curve. |
| `feature_spec.json` | Canonical record: pair (A, B, delta), hypothesis, verification block (results + verdict ∈ reproduced / reproduced-in-median / partially-reproduced / refuted / inconclusive). |

`templates/branch_index.json` is the append-only catalog index:
`(target, branch_id) → template_id` with role (`primary` / `extension`)
and `verdict_at_time`. `run_hypothesis_fanout.py --skip-existing` reads it
to avoid re-dispatching agents for branches already covered.

The harness IS the falsifiable hypothesis; the dose-response curve IS the
verdict. No free-form RCA text. Verification runs only the
**involved fuzzers** (decisive winners + losers); reference fuzzers carry
prompt context, not verdict weight.

### Current entries

**Verified / active** (under `templates/`):

| feature_id | verdict |
|---|---|
| `i2s_magic_number_gate` | reproduced (cmplog vs naive, I2S substitution) |
| `i2s_anchored_length_trap` | reproduced |
| `i2s_anchored_seed_deviation_trap` | reproduced (v5/v6/v7a/v8, three subtypes) |
| `i2s_corpus_pollution` | reproduced (4-fuzzer synergy) |
| `i2s_grammar_chain_length` | reproduced (v2) |
| `i2s_pair_relational_lookup` | reproduced |
| `vp_gradient_derived_operand` | reproduced (v2, full 4-fuzzer) |
| `vp_length_anchor_rescue` | (no feature_spec.json yet) |

**Refuted / superseded** (under `templates/legacy/`):

| feature_id | verdict |
|---|---|
| `i2s_indirect_dispatch_opacity` | refuted |
| `i2s_inequality_anchor_trap` | refuted (family-bounded) |
| `i2s_jump_table_opacity` | refuted on mechanism (2026-05-08; replaced by `i2s_indirect_dispatch_opacity`) |
| `i2s_runtime_bound_substitution` | refuted |
| `i2s_whitelist_anchor_trap` | refuted (remap to strpres family) |
| `vp_rescues_i2s_derived_operand` | refuted |

## Typical Workflow (metaphorical-testing pipeline, n=10)

The canonical pipeline is **6 phases** (with one optional auxiliary phase
+ a post-agent lint):

```
Step 1: Statistical significance — admissibility per (target, A, B)
Step 2: DB population            — branches + study_subjects + subject_branches
Step 3a: Build candidate dictionary  (per-branch, ≥8/≥8 rule)
Step 3b: Pick representatives        (decisive-shape × source-region dedup)
Step 3.5 (optional): Seed bisection on representatives
Step 4: Hypothesis fan-out — manifest + per-rep prompts → Claude dispatch
Step 5: Verification sweep — verdict per template
Step 6: Lint template-shape consistency (post-agent quality check)
```

**Step 1 — significance** (`tools/subject_significance.py`):

```bash
python3 tools/subject_significance.py per-trial  # → csvs/subject_per_trial.csv
python3 tools/subject_significance.py pair       # → csvs/subject_pair_significance.csv
```

Computes per-trial AUC + final-coverage scalars; pair-level Mann-Whitney
U-test over the 4 canonical pairs. `admissible = (p_auc < α OR p_final
< α)` — at n=10 this is meaningful (smallest 2-sided MW p ≈ 0.0079).

**Step 2 — DB population** (`tools/study_units.py add-canonical`):

```bash
python3 tools/study_units.py add-canonical \
    --targets curl libxml2 libpng openthread harfbuzz
```

One per-target coverage walk shared across the 4 canonical subjects
(Option A). The walk reads every `branch_coverage_show.txt` under
`out/coverage_ts/<target>/<fuzzer>/trial<N>/reports/<time_s>/` once and
caches per-(branch, fuzzer, trial) state in memory: `hit_status`
(-1/0/1), `duration_h` (-1.0 = never blocked, ≥0 = time spent blocked),
`hitcount` (this side at final), `other_hitcount` (other side at final).

Then for each of the 4 canonical subjects:
1. Apply per-subject admission rule: across the 20 trials of (A, B),
   ≥1 blocked AND ≥1 resolved at final checkpoint.
2. For admitted branches: ensure `branches` row exists; insert
   `subject_branches` row with per-arm counts (`n_*`), trial-set JSON
   arrays (`A_resolved_trials` etc.), per-arm aggregates (avg duration,
   avg hits, p_blocked), and direction-oriented divergences.

The `branches` table is the union of per-subject admissions across the 4
subjects. No separate target-level extraction step exists.

**Step 3a — build candidate dictionary** (`tools/build_candidates.py`):

```bash
python3 tools/build_candidates.py
# → csvs/blocker_candidates.csv (one row per (target, branch_id))
```

Per-branch aggregation. A canonical pair at a branch is **decisive** iff
`winner_resolved >= 8 AND loser_blocked >= 8`. A branch is admitted iff
it has ≥1 decisive pair (admissible-only by default). Reads
`subject_branches` directly — per-subject admission already filtered out
navigation-gap pathology upstream.

**Step 3b — pick representatives** (`tools/select_representatives.py`):

```bash
python3 tools/select_representatives.py
# → csvs/blocker_representatives.csv (one row per (shape × region) group)
# → csvs/blocker_dedup_map.csv       (auditable full → reps mapping)
```

Decisive-only shape is a 4-char string over (naive, cmp, vp, vpc) with
`R`/`B`/`-` per fuzzer (winner / loser / non-decisive). Group by
`(shape, file, function, line // 50)`, pick one rep per group by
`(max_prob_div, max_dur_div, max_hit_div)`. Reps drive the agent fan-out;
the dedup map records implied corroborations without inflating
`branch_index.json` (corroboration honesty: agent-verified count only).

**Step 3.5 — seed bisection** (optional but needed for full evidence
prompts):

```bash
for t in curl libxml2 libpng openthread harfbuzz; do
    python3 tools/seed_bisect.py run --target $t --queue-base ./out \
        --branches-from-csv csvs/blocker_representatives.csv \
        [--queue-sample-size 10000]   # for big targets with 100K+ seeds/queue
done
```

Per-target Docker container scans the queues for the selected reps only
(one resolving + one blocking queue per branch), populates
`resolving_seeds` + `blocking_seeds` + lineage tables. seed_bisect picks
the representative trial from `subject_branches.{A,B}_{resolved,blocked}_trials`
JSON arrays — lexicographic min, one per direction. Without this step,
evidence prompts show `[no seeds available]` for the affected branches;
agent can still propose hypotheses from source + per-trial counts.

**Step 4 — hypothesis fan-out** (`tools/run_hypothesis_fanout.py` +
Claude session):

```bash
python3 tools/run_hypothesis_fanout.py
# → out/hypothesis_fanout/manifest.json + per-rep prompt files
# Then: Claude reads manifest, fans out N parallel × M sequential
# Agent(feature-hypothesis-generator) calls.
# → templates/<feature_id>/{template.c, params.json, feature_spec.json}
```

Default input is `csvs/blocker_representatives.csv`; pass
`--input csvs/blocker_candidates.csv` for the full candidate set.
Each agent call receives a per-branch prompt from
`tools/study_units.py evidence-per-branch` containing the trial vector
**only for fuzzers in decisive pairs** (winner/loser tags). Reference
fuzzers (`-` slot in the decisive shape) carry no numeric stats —
they're indicated only via their position. Each decisive pair's seeds
are included, plus source context and a TASK section instructing the
agent to scope verification to `involved_fuzzers` only.

Default grouping is `(target, primary_delta)` — across groups parallel,
within group sequential so later calls see prior templates. The script
auto-skips reps already covered (per `templates/branch_index.json`).

**Step 5 — verification sweep** (not implemented yet):

For each `templates/<feature_id>/` produced in step 4, build the
parameterized harness across `params.json:scan_values`, run the
`involved_fuzzers` for `trials_per_point` × `duration_s`, then fill the
`feature_spec.json` verification block: per-trial results, medians,
summary, verdict ∈ {reproduced, reproduced-in-median,
partially-reproduced, refuted, inconclusive}.

Synthetic verification runs **only the involved fuzzers** (decisive
winners + losers). Reference fuzzers are auxiliary context in the prompt,
not part of the verdict.

**Step 6 — lint template-shape consistency**:

```bash
python3 tools/lint_template_shapes.py
# → stdout report (or --output FILE)
# Exit codes: 0=clean, 1=intra-only, 2=cross-template
```

Verifies (a) intra-template: reps assigned to the same template share a
single decisive shape; (b) cross-template: a given shape doesn't span
≥2 templates. Catches over-lumping and missed merges by the agent.

**Auxiliary tools:**
- `tools/plot_coverage_curves.py` — coverage-by-time spaghetti plot.
  Per-target panels, per-fuzzer thin lines (one per trial) + bold mean.
  Outputs `out/coverage_curves.png`. Use to visually verify which subjects
  show clean fuzzer separation vs. heavy overlap.

