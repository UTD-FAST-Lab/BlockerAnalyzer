# BlockerAnalyzer

A research project for analyzing fuzzing "blockers" — branches that coverage-guided fuzzers fail to reach — and diagnosing why.

## Project Structure

```
BlockerAnalyzer/
├── out/                # Symlink → shared fuzz-campaign root (see Note below)
│   ├── coverage_ts/<target>/<fuzzer>/trial<N>/
│   │   ├── coverage_timeseries.csv      # time_s, branch_covered, branch_total
│   │   ├── reports/<time_s>/branch_coverage_show.txt
│   │   └── profraw_ts/running.profdata
│   ├── <target>/<fuzzer>/trial<N>/queue/  # raw LibAFL corpus
│   └── coverage_curves.png                # plot_coverage_curves.py output
├── csvs/               # Analysis CSV outputs (significance, candidates, reps)
├── step5a/             # Step 5a intermediates — per-family distiller cards + signature JSONs
├── templates/          # Feature catalog — parameterized hypothesis harnesses (see Feature Catalog section)
│   ├── feature_spec.template.json    # JSON schema for feature_spec.json
│   ├── branch_index.json             # Append-only (target, branch_id) → template_id map
│   ├── <feature_id>/                 # One subdir per surviving hypothesis (template.c + params.json + feature_spec.json)
│   └── legacy/                       # Refuted / superseded hypotheses (kept as methodology record)
├── fuzzer_mechanism_library.md  # Per-fuzzer mechanism paragraphs, spliced into prompts by study_units.py evidence-per-branch
├── db/                 # SQLite: blockers.sqlite (branches + study_subjects + subject_branches + seeds)
├── tools/              # Reusable analysis scripts
│   ├── blocker_db.py             # Schema management for the SQLite database (init only)
│   ├── subject_significance.py   # Per-(target,A,B) AUC + final-coverage MW U-test
│   ├── study_units.py            # Per-target coverage walk + per-subject admission + CLI dispatch. Schema + population only — prompt assembly lives in evidence_prompt.py
│   ├── evidence_prompt.py        # Per-branch structured prompt assembly (SOURCE CONTEXT overlay, HIT-COUNT DIVERGENCE, DIVERGENT BRANCHES, BRANCH SEEDS + byte diff, MECHANISM CONTEXT, TASK). Registers `evidence-per-branch` subcommand into study_units' CLI.
│   ├── seed_utils.py             # Dependency-free helpers: parse_count, hex_dump, read_seed_bytes, format_seed_block, byte_diff_section. Imported by evidence_prompt.py and db_query.py.
│   ├── check_analysis.py         # Validates agent .analysis.json against sibling .prompt.md — schema completeness + exact_quote hallucination filter + mechanism-attribution self-consistency check.
│   ├── build_candidates.py       # Per-branch ≥8/≥8 aggregation → blocker_candidates.csv
│   ├── select_representatives.py # Shape × region dedup → blocker_representatives.csv + dedup_map
│   ├── run_hypothesis_fanout.py  # Manifest builder; reads reps, calls evidence-per-branch
│   ├── seed_bisect.py            # 10-bucket bisection to find seeds that hit blocking branches
│   ├── per_role_coverage.py      # Per-branch W (winner-resolving) / L (loser-blocking) seed-set coverage gen → db/per_role_coverage/<target>/<branch_id>/{W,L}/branch_coverage_show.txt (powers SOURCE CONTEXT overlay diff)
│   ├── callers_index.py          # Per-target source-grep callers index → db/callers_index/<target>.json. {callee_demangled: [(caller, file, line, c_start, c_end)]}. One-time per target; powers the cross-file 1-hop caller block and call-chain section in the overlay.
│   ├── extract_functions.py      # Library: llvm-cov export per target → (file, name, start, end) list; imported by study_units.py at add-canonical time to populate branches.function with the real C/C++ function name (demangled via c++filt). Also used by callers_index.py and the overlay function-range lookup.
│   └── plot_coverage_curves.py   # Coverage-by-time spaghetti plot (per-target panels)
├── docker/             # Docker infrastructure for coverage-instrumented builds
│   ├── Dockerfile.coverage-base  # Base image: clang-18, llvm-18, COV_FLAGS env, bakes in the two scripts below → libafl-coverage-base
│   ├── bisect_in_container.py    # 10-bucket bisection seed scanner; run inside container as /seed_scanner.py (also bind-mounted by seed_bisect.py at run time so unrebuilt images still work)
│   ├── per_role_in_container.py  # Per-branch W/L cov runner: takes seed sets, runs FUZZ_BIN, llvm-cov show <blocker_file + caller_files> → annotated source dumps. Bind-mounted by per_role_coverage.py at /per_role_cov.py.
│   ├── run_bisect_entrypoint.sh  # Standalone /run_bisect.sh helper: corpus dir → branch_coverage_show.txt (ad-hoc, not used by seed_bisect.py)
│   └── targets/                  # Per-target coverage Dockerfiles → libafl-<target>-cov
│       ├── Dockerfile.curl.cov
│       ├── Dockerfile.harfbuzz.cov
│       ├── Dockerfile.libpng.cov
│       ├── Dockerfile.libxml2.cov
│       └── Dockerfile.openthread.cov
├── docs/
│   └── TOOLS.md         # Full per-tool CLI reference + DB schema (indexed from the Tools section)
└── .claude/
    ├── agents/         # Specialized Claude agents for analysis
    └── settings.json   # Project permissions (Bash allowed for all agents)
```

**Note:** `out/` is a symlink to the shared fuzz-campaign root (currently
`/data/miao/libafl_experiments/`; verify with `readlink out` if a path
hardcoded somewhere goes stale). All tools default to relative `out/` so
the symlink target can change without code edits. The coverage Dockerfiles
for curl/harfbuzz/libpng/libxml2/openthread live here under `docker/targets/`;
jsoncpp/woff2 cov Dockerfiles live in `libafl_fuzzbench/docker/targets/`.

`db/per_role_coverage/<target>/<branch_id>/{W,L}/` — per-branch W
(winner-resolving) and L (loser-blocking) llvm-cov annotated source
dumps, generated by `tools/per_role_coverage.py`. Cache key in
`cache_key.txt` = sha1(sorted seed_ids + sorted file list). Powers the
SOURCE CONTEXT per-role hit overlay.

`db/callers_index/<target>.json` — one-time per-target source-grep
callers index built by `tools/callers_index.py`. Maps demangled callee
name → list of (caller, file, line, c_start, c_end). Used by both
per_role_coverage (to include caller files in the cov dump) and the
overlay builder (to render cross-file 1-hop callers + call chain).

`prompts/<target>_<branch_id>.prompt.md` — per-rep agent prompts.
Default outdir for `tools/run_hypothesis_fanout.py`. **Layout is FLAT**
(2026-05-30): all prompts sit directly under `prompts/` with no
subfolders (default `--group-by flat`). Filenames key on
(target, branch_id), which is globally unique, so they are stable
regardless of grouping. (`--group-by shape|target|target-delta` still
exist as alternative FOLDER layouts but carry no dispatch meaning — see
the dispatch note below.) Optional curated subdirs:
- `prompts/_examples/` — GOLD-STANDARD reference pair (prompt +
  hand-written analysis.json) that passes every check in
  `tools/check_analysis.py`. Concrete reference of what a high-quality
  analysis looks like; point agents / contributors here when briefing.
  See `prompts/_examples/README.md`.

Each agent-produced analysis lives as a sibling `.analysis.json` next
to its `.prompt.md` (e.g. `prompts/curl_19.analysis.json`).

**Dispatch is FLAT PARALLEL** (analysis-only contract): under the
analysis-only contract each branch is analyzed in isolation — no agent
reads another's output — so all calls are mutually independent. The
manifest exposes a flat `all_calls` list (`dispatch_plan.mode =
flat_parallel`); shape/group is a cosmetic label, NOT an ordering axis.
The old across-group-parallel / within-group-sequential scheme (whose
only purpose was letting a later agent see earlier `template.c` on disk)
is dead, since 4b no longer writes templates. **Operational note:**
dispatch ≤25 agents per message — 40-wide fan-out saturates and triggers
API stream-idle timeouts (observed 2026-05-30).

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
| **feature-hypothesis-generator** (Opus) | `prompts/<target>_<bid>.analysis.json` (one sibling per prompt) | Per-branch analysis step (step 4b) of the metaphorical-testing pipeline. Receives a structured prompt (push-mode) emitted by `tools/study_units.py evidence-per-branch` for ONE (target, branch). Diffs winner-resolving vs loser-blocking seed bytes at the highest-prob_div decisive pair, reads source CMP shape, and writes ONE `.analysis.json` (hypotheses + evidence_trail + falsifiability). Under the **analysis-only contract (2026-05-17)** it does NOT compare against `templates/`, NOT classify into existing categories, and NOT emit template files — classification + verification are deferred to steps 5a/5b to avoid anchoring bias. One per-branch prompt per call; designed for parallel fan-out across (target, branch_id) pairs. |
| **hypothesis-signature-distiller** (Sonnet) | `step5a/<family>/signatures.json` (one signature per card) | Pass-A distiller of **step 5a**. Reads ONE hypothesis card (built by `tools/build_signature_cards.py`, family-tagged by `tools/mechanism_family.py`) and normalizes it into ONE structured signature `{gate_structure, operand_kind, operand_literal, operand_width_bytes, byte_signature, mechanism_summary, one_line}` — closed-vocab gate slots plus an **open** `mechanism_summary` (the technique's effect in free text, no fixed taxonomy, so Pass B can *discover* categories rather than have them imposed). Does NOT cluster or read source/DB — **tool-restricted to Read+Write** so per-card isolation is enforced. |
| **signature-feature-classifier** (Sonnet) | `step5a/<family>/clusters.json` (discovered feature clusters) | Pass-B classifier of **step 5a**. **Discovers** feature categories from a family's signatures — clusters branches by `mechanism_summary` similarity (gate slots secondary; opens member analyses via `analysis_path` when ambiguous), and coins an emergent `mechanism_label` + `feature_id` + definition per cluster. Applies NO pre-defined taxonomy (categories are the output, not an input). Does NOT author templates (that is 5b). Read+Write. |
| **template-author** (Opus) | `step5b/<feature_id>/{template.c, params.json, feature_spec.json}` (verdict: pending) | **Author** stage of **step 5b**. Reads ONE cluster brief (`step5b/briefs/<feature_id>.json`, built by `tools/build_template_briefs.py`) and generates the synthetic program: ONE parameterized libFuzzer harness isolating the cluster's shared mechanism with exactly ONE compile-time `-D` knob = the program-feature axis. Does NOT run the sweep (`verify_template.py`) or judge verdicts (`verdict-adjudicator`). Read+Write. The macro↔params consistency + live-knob are enforced by `tools/check_template.py`. |
| **verdict-adjudicator** (Opus) | `step5b/<feature_id>/adjudication.json` | **Adjudicator** stage of **step 5b** — the INDEPENDENT judge invoked only when `verify_template.py` returns refuted / inconclusive(with-crashes) / partially_reproduced. Reads the harness + `verification_run.json` signals + the brief, and rules `harness_artifact` (→ regenerate with feedback, retry budget 2), `genuine_refutation` (→ ACCEPT the verdict, record to `templates/legacy/`, no retry), or `underpowered` (→ bounded rerun). Deliberately separate from the author to block confirmation bias. Read+Write. |

The metaphorical-testing pipeline uses **push-mode**: the orchestrator
runs `tools/study_units.py evidence-per-branch --target T --branch-id M`
to assemble the structured prompt (BLOCKER / TRIAL VECTOR / DECISIVE
PAIRS / SOURCE CONTEXT / BRANCH SEEDS / MECHANISM CONTEXT / TASK), then
feeds that prompt to `feature-hypothesis-generator`. The agent never
queries the DB itself — the prompt IS the auditable evidence record.

## Permissions

`.claude/settings.json` grants `Bash(*)` project-wide so agents can run shell
commands without prompting. The DB-population step (per-target coverage walk
in `study_units.py`) needs Bash access to read large `branch_coverage_show.txt`
files under `out/coverage_ts/`.

## Tools

Full CLI, flags, and the DB schema for every tool live in
[`docs/TOOLS.md`](docs/TOOLS.md). A compact **step → tool map** is at the top of
that file and mirrored in [`tools/README.md`](tools/README.md) (filenames are
NOT step-prefixed — the tools import each other as flat siblings, so the mapping
is documented rather than baked into names). One-line index below, grouped by
pipeline phase (see "Typical Workflow" further down for the phase ordering):

**Schema & shared libraries**
- `blocker_db.py` — `db/blockers.sqlite` schema + `init` (full schema table in docs/TOOLS.md).
- `extract_functions.py` — `llvm-cov export` → (file, name, start, end) ranges; used at `add-canonical` time.
- `seed_utils.py` — dependency-free seed/byte helpers (parse_count, hex_dump, byte_diff_section).

**Steps 1–2 — significance & DB population**
- `subject_significance.py` — per-(target, A, B) AUC + final-coverage Mann-Whitney U-test.
- `study_units.py` — per-target coverage walk + per-subject admission; also hosts `evidence-per-branch` prompt assembly.
- `evidence_prompt.py` — per-branch structured-prompt assembly; registers the `evidence-per-branch` subcommand.

**Step 3 — candidates & representatives**
- `build_candidates.py` — per-branch ≥8/≥8 aggregation → `blocker_candidates.csv`.
- `select_representatives.py` — decisive-shape × region dedup → `blocker_representatives.csv` + dedup map.

**Steps 3.5–3.7 — evidence enrichment**
- `seed_bisect.py` — 10-bucket Docker bisection: which seeds hit each blocker.
- `callers_index.py` — one-time per-target source-grep callers index.
- `per_role_coverage.py` — W (resolving) / L (blocking) llvm-cov dumps powering the SOURCE CONTEXT overlay.

**Step 4 — fan-out & validation**
- `run_hypothesis_fanout.py` — prompt-prep + manifest builder (does NOT dispatch agents).
- `check_analysis.py` — validate agent `.analysis.json` against the sibling prompt (exact_quote hallucination filter).
- `db_query.py` — agent-facing pull queries (lineage, more-seeds).

**Step 5a — cross-branch classification**
- `mechanism_family.py` — deterministic `coarse_family(covers_pairs)` → per-technique `<T>_pro`/`<T>_anti` families (all 10 techniques) plus the I2S×VP `synergy`/`independent` composite; first-pass bucketing + self-test/scan.
- `build_signature_cards.py` — build per-family distiller cards (family-tagged, with `analysis_path` back-pointers; analysis fields + candidates-CSV locators) for the `hypothesis-signature-distiller` agent. Pass B (the classifier) reads the signatures + cards directly — no group-by tool.

**Step 5b — author + verify loop**
- `build_template_briefs.py` — per-cluster authoring brief (cluster def + members' signatures + full analyses incl. the falsifiability harness-blueprint) → `step5b/briefs/<feature_id>.json` for the `template-author` agent.
- `check_template.py` — deterministic preflight gating the sweep: schema/fuzzer sanity + every `scan_value` compiles + **dead-knob detection** (min vs max scan value must yield different assembly, else the `-D` macro/params drifted). Catches mechanical defects so an author retry isn't spent on a refutation.
- `verify_template.py` — synthetic-harness sweep runner. Builds `step5b/<feature_id>/template.c` under each involved fuzzer (`<fuzzer>_cc --libafl -D<knob>=<val>` in the `libafl-base` image), sweeps `params.json:scan_values`, counts crashes (`<corpus>/crashes/`), scores a dose-response verdict. **Serial by default (`--jobs 1`) — host runs other campaigns.**
- `run_full_verify.py` — full PARALLEL verification driver: runs the complete `params.json` budget for every `step5b/` template across a worker pool (reuses `verify_template`'s run_cell + judge). `--jobs` must not exceed cores (wall-clock duration).
- `screen_templates.py` — fast SCREENING sweep across all `step5b/` templates: 1 trial, short duration, decisive pair + 3 scan points. 1-trial `reproduced` is PROVISIONAL — confirm before promoting.

**Auxiliary**
- `plot_coverage_curves.py` — coverage-by-time spaghetti plot → `out/coverage_curves.png`.
- `fuzzer_mechanism_library.md` — canonical per-fuzzer mechanism paragraphs spliced into prompts.


## Fuzzer Variants

The LibAFL FuzzBench experiment uses 4 fuzzer variants:

| Fuzzer | Technique |
|--------|-----------|
| `naive` | Baseline coverage-guided only |
| `cmplog` | Input-to-state (I2S) comparison logging |
| `value_profile` | Hamming-similarity comparison feedback |
| `value_profile_cmplog` | Both I2S and value profile |

Time-series coverage snapshots:
```
out/coverage_ts/<target>/<fuzzer>/trial<N>/reports/<time_s>/branch_coverage_show.txt
```

## Canonical 10-target set (paper scope, locked 2026-05-02)

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

**Setup status:** full pipeline plumbing (Dockerfile.cov + n=10 campaign)
exists for curl, harfbuzz, libpng, libxml2, openthread (the 50-rep pilot
set) plus lcms, bloaty, sqlite3 from prior runs. jsoncpp/woff2 have
`Dockerfile.cov` but no campaign yet. See `TODO.md` (P2 — Scope expansion)
for the remaining 5-→10-target work.

## Feature Catalog (templates/)

Falsifiable hypothesis harnesses, one per surviving program-feature
hypothesis. Under the analysis-only contract (2026-05-17) these are
produced by the **step 5a Pass B classifier** (not yet
implemented) from the per-branch `.analysis.json` files — NOT directly by
the `feature-hypothesis-generator` agent. The existing entries below
predate the contract (prior template-writing era) and are kept as the
verified/refuted methodology record. Each entry `templates/<feature_id>/`
is a falsifiable hypothesis about ONE program-side parameter controlling
ONE fuzzer-pair divergence, with three files:

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
Step 3.6 (optional): Per-target callers index (one-time per target)
Step 3.7 (optional): Per-role coverage gen for selected branches
Step 4a: Hypothesis fan-out — manifest + per-rep prompts → Claude dispatch
Step 4b: Per-branch analysis — each agent writes .analysis.json (NO template comparison, NO template.c — those are deferred to step 5+)
Step 4c: Validate analyses — tools/check_analysis.py catches schema gaps + exact_quote hallucinations
Step 5a: Cross-branch classification — coarse family (mechanism_family.py) → Pass A distill (hypothesis-signature-distiller → open mechanism_summary signatures) → Pass B discover (signature-feature-classifier clusters by mechanism + coins categories) → clusters.json
Step 5b: Author→preflight→verify→adjudicate loop (build_template_briefs → template-author → check_template → verify_template → verdict-adjudicator). Built + validated 2026-05-24. Retry twice on artifacts; record genuine refutations.
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

**Step 3.6 — per-target callers index** (one-time per target; powers
cross-file caller block + call chain + caller-file coverage scope):

```bash
for t in curl libxml2 libpng openthread harfbuzz; do
    python3 tools/callers_index.py build --target $t
done
```

~3–30s per target. Cached at `db/callers_index/<target>.json`. Without
this step, the overlay falls back to "no callers index for <target>"
and per_role_coverage scopes the cov dump to the blocker's file only.

**Step 3.7 — per-role coverage gen** (needed for SOURCE CONTEXT
overlay + HIT-COUNT DIVERGENCE + DIVERGENT BRANCHES sections):

```bash
for t in curl libxml2 libpng openthread harfbuzz; do
    python3 tools/per_role_coverage.py generate --target $t \
        --branches-from-csv csvs/blocker_representatives.csv
done
```

Per-target Docker container processes all branches with decisive pairs
sequentially. For each branch: unions all `resolving_seeds` as W,
all `blocking_seeds` as L (any fuzzer), runs each set through
`FUZZ_BIN`, emits annotated llvm-cov source for the blocker file
plus 1-hop caller files (from the callers index). Cached at
`db/per_role_coverage/<target>/<branch_id>/{W,L}/branch_coverage_show.txt`.
Without this step, evidence prompts fall back to a static ±N source
window with no per-role overlay.

**Step 4a — hypothesis fan-out** (`tools/run_hypothesis_fanout.py` +
Claude session):

```bash
python3 tools/run_hypothesis_fanout.py
# → prompts/manifest.json + flat per-rep .prompt.md files directly under prompts/
# Then: Claude reads manifest.all_calls (flat list), fans out independent
# Agent(feature-hypothesis-generator) calls — all parallel, no ordering.
# Dispatch in batches of <=25 (40-wide saturates / times out).
```

Default input is `csvs/blocker_representatives.csv`; pass
`--input csvs/blocker_candidates.csv` for the full candidate set.

**Step 4b — per-branch analysis (NEW DESIGN, 2026-05-17)**: each agent
analyzes its assigned branch IN ISOLATION and writes a sibling
`<target>_<bid>.analysis.json` file. Critically: the agent does NOT
compare against `templates/`, NOT classify into existing categories, and
NOT emit `template.c` — those are deferred to step 5+ so that
classification happens AFTER all branches have independent hypotheses,
avoiding anchoring bias.

Analysis schema (enforced by `tools/check_analysis.py`):
- `summary_one_line`, `pair_decision` ("single_feature"/"multi_feature"),
  `hypotheses` (list of 1+ with covers_pairs + what/why_winner/why_loser
  + mechanism_attribution).
- `evidence_trail` — every hypothesis sub-claim must be backed by an
  entry with cited_section + cited_locator + **exact_quote that appears
  literally in the prompt** (mechanically verified by `check_analysis.py`).
- `mechanism_consistency_check.claimed_mechanism` — one of an **11-token
  closed vocabulary** (extended 2026-05-30 from 5 → 11 for the 10-fuzzer
  set): `I2SRandReplace`, `CMP_MAP gradient` (roadblock); `context-sensitive
  coverage`, `ngram coverage` (feedback); `grimoire structural`, `mopt
  mutation`, `calibrated energy`, `aflfast rarity` (mutation/scheduling);
  `havoc-only`, `token-replace`, `other` (baseline/fallback — `other` only
  when genuinely unclassifiable). If claimed = `I2SRandReplace`, the agent
  must invoke `db_query.py lineage` on a winning seed and confirm the I2S
  floor (dash-row) signal (or explain why verification failed) — this is the
  only mechanism requiring lineage. The agent↔attribution consistency
  cross-check (no hypothesis may name a different mechanism) applies ONLY to
  `single_feature`; `multi_feature` legitimately carries a distinct mechanism
  per hypothesis.
- `falsifiability.would_be_refuted_by` — one concrete observation that
  would kill the hypothesis (Popper test).
- `weakest_evidence_point` + `confidence` — forced self-criticism.

**Step 4c — validate analyses**:

```bash
python3 tools/check_analysis.py --recursive prompts/
```

Catches: schema gaps, exact_quote hallucinations (claims with quotes
that aren't in the prompt), invalid section names, weak mechanism
attribution, pair-label mismatches. Run before step 5a — bad analyses
poison downstream classification.

**Step 5a — cross-branch classification**:

Aggregates the per-branch `.analysis.json` files into **discovered** feature
clusters, in three stages so the feature taxonomy is found in the data rather
than imposed:

1. **Coarse family** — deterministic (`tools/mechanism_family.py`).
   `coarse_family(covers_pairs)` maps each hypothesis to one of six mechanism
   families (`I2S_pro`, `I2S_anti`, `VP_pro`, `VP_anti`, `synergy`,
   `independent`; plus a `mixed` escape) from the technique + direction in
   `covers_pairs` — robust to the ≥8/8 cutoff wobble that flips the fine
   decisive-shape. Families are hard buckets; clustering never crosses them.
2. **Pass A — distill** (`hypothesis-signature-distiller` agent, per family).
   `build_signature_cards.py --family F` builds per-hypothesis cards (with
   `analysis_path` back-pointers); each card → one signature `{gate_structure,
   operand_kind, operand_literal, operand_width_bytes, byte_signature,
   mechanism_summary, one_line}`, derived in isolation (Read+Write only). The
   gate slots use a closed vocabulary; **`mechanism_summary` is OPEN free text**
   — the technique's effect in the distiller's own words, no fixed taxonomy.
3. **Pass B — discover** (`signature-feature-classifier` agent, per family).
   Reads the family's `signatures.json` + `<family>.cards.json`, **clusters
   branches by `mechanism_summary` similarity** (gate slots secondary; opens
   member analyses via `analysis_path` when ambiguous), and coins an emergent
   `mechanism_label` + `feature_id` + definition per cluster →
   `step5a/<family>/clusters.json`. Each cluster = one proposed feature/template
   for 5b; members carry `analysis_path` so 5b authors from the full analyses.

**Why discovery, not a fixed mechanism vocabulary:** an earlier closed
`technique_effect` taxonomy was *induced from the pilot then applied back to it*
— circular, and it would anchor every future run. Keeping `mechanism_summary`
open and clustering it in Pass B makes the categories an output (discovered),
preserving the no-anchoring property of the analysis-only contract. The gate
slots stay closed — they describe structure, not the feature, so they don't bias
discovery. (Once a taxonomy is stable, a future *application*-mode distiller
could emit a closed mechanism label for reproducibility at scale.)

```bash
python3 tools/mechanism_family.py                                   # family distribution + self-test
for fam in I2S_pro I2S_anti VP_pro synergy independent; do
  python3 tools/build_signature_cards.py --family $fam --out step5a/$fam.cards.json
  # dispatch hypothesis-signature-distiller over $fam.cards.json -> step5a/$fam/signatures.json
  # dispatch signature-feature-classifier on signatures.json + cards -> step5a/$fam/clusters.json
done
```

**Step 5b — author → preflight → verify → adjudicate loop**
(built + end-to-end validated 2026-05-24):

The loop turns each step-5a cluster into a verified-or-refuted template. Two
agents (author, adjudicator) bracket two deterministic tools (preflight, runner).
**Retry policy (locked): two regenerations on a harness artifact; a genuine
refutation is recorded, never retried** (no re-clustering back to 5a).

```
build_template_briefs.py  → step5b/briefs/<id>.json   (cluster + members' analyses)
  └─ template-author agent → step5b/<id>/{template.c, params.json, feature_spec.json}  (verdict: pending)
       └─ check_template.py (preflight) ──FAIL──────────────┐ mechanical → regenerate
            └─ PASS → verify_template.py (sweep)             │  (budget 2)
                 ├─ reproduced / reproduced_in_median → ACCEPT → promote to templates/<id>/
                 ├─ build_fail / execs=0 / all-zero ─────────┘ mechanical → regenerate
                 └─ refuted / inconclusive(w/crashes) / partially
                      └─ verdict-adjudicator agent →
                           harness_artifact   → regenerate w/ feedback (budget 2)
                           genuine_refutation → record to templates/legacy/<id>/
                           underpowered       → rerun (more trials / wider scan)
```

```bash
python3 tools/build_template_briefs.py --family all          # step5b/briefs/*.json (13)
# dispatch template-author over a brief -> step5b/<id>/{template.c, params.json, feature_spec.json}
python3 tools/check_template.py  --template step5b/<id>      # preflight (cheap; gates the sweep)
python3 tools/verify_template.py --template step5b/<id>      # full sweep -> verification_run.json
python3 tools/verify_template.py --template step5b/<id> --trials 2 --duration-s 15 \
    --fuzzers naive,cmplog --scan-values 1,8                 # smoke (decisive pair, tiny budget)
# if non-reproduced: dispatch verdict-adjudicator over step5b/<id>/ -> adjudication.json
```

Build model: each variant ships a `<fuzzer>_cc` LibAFL wrapper on PATH in the
`libafl-base` image (`../libafl_fuzzbench`); `<fuzzer>_cc --libafl -D<knob>=<val>
template.c` → libFuzzer-compat binary; `__builtin_trap()` objectives land in
`<corpus>/crashes/`; `crash_count` = files there. `verify_template.py` writes a
standalone `verification_run.json` (per-trial counts + medians + verdict signals);
verdict ∈ {reproduced, reproduced_in_median, partially_reproduced, refuted,
inconclusive}, judged from `params.json:expected_direction` (auditable heuristic,
`verdict_provenance: auto`). `--write-spec` patches the `feature_spec.json`
verification block in place.

Runs **only the involved fuzzers** (decisive winners + losers). Reference
fuzzers are auxiliary context, not part of the verdict.

**Staging vs catalog:** authored templates land in `step5b/<id>/` (proposals).
On `reproduced` they promote to `templates/<id>/`; on `genuine_refutation` to
`templates/legacy/<id>/` — keeping `templates/` the verified catalog. (Promotion
is currently manual.) **Validated 2026-05-24:** the loop ran end-to-end on
`opaque_exact_literal_dispatch_gate` (author → preflight PASS → smoke verify
`reproduced`).

**(Removed) Step 6 — lint template-shape consistency.** `lint_template_shapes.py`
was deleted 2026-05-29: it checked decisive-shape purity of the *agent's*
`branch_index.json` template assignments, but under the analysis-only contract
(2026-05-17) the agent no longer classifies — Step 5a Pass-B clusters by
`mechanism_summary` (shape demoted to secondary signal), so shape-purity is no
longer a desired invariant. If a Step-6 quality gate is wanted, write a new lint
over `step5a/<family>/clusters.json` (mechanism-aware), not over shape.

**Auxiliary tools:**
- `tools/plot_coverage_curves.py` — coverage-by-time spaghetti plot.
  Per-target panels, per-fuzzer thin lines (one per trial) + bold mean.
  Outputs `out/coverage_curves.png`. Use to visually verify which subjects
  show clean fuzzer separation vs. heavy overlap.

