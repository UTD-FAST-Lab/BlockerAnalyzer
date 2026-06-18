# BlockerAnalyzer

A research project for analyzing fuzzing "blockers" — branches that coverage-guided fuzzers fail to reach — and diagnosing why.

## ⚑ CURRENT DIRECTION — Benchmark pivot (2026-06-12)

**Step 5 changed.** The old "synthesize a mini-program per feature and verify its
dose-response" (step 5b) was abandoned for *non-local* features: corpus
contamination, joint-necessity, scheduling, ctx/ngram coverage are properties of
the *whole target + campaign*, not capturable in a mini-program (the repeated
"non-synthesizable" verdicts were the symptom). **New frame:** the decisive
branches (≥8/8 rule, already in the DB) ARE the dataset; classify them by
decisive-shape + mechanism, then **validate each hypothesis with evidence from
the real target + fuzzing campaign** (corpus byte-stats, seed lineage, coverage
depth). Validated hypotheses become **mechanism labels** → the labeled branches
are a real-world, mechanism-stratified benchmark of fuzzer-discriminating
blockers. Synthetic harnesses are kept ONLY as an optional causal sidecar for
*local* features.

**Full design:** `docs/benchmark_pivot_spec.md`. **Other-server runbook:**
`docs/OTHER_SERVER_TODO.md`. **Categories:** `bench/hypothesis_categories.md`.

**Pipeline now (replaces step 5):**
- `step5a_new_v3/<shape>/{signatures.json, cards.json}` — 38 decisive-shape
  buckets (Pass-A signatures; Pass-B classifier RETIRED — the design agent does
  classification). `tools/mechanism_family_v3.py` is the deterministic Layer-1
  shape split.
- `step5b_new_v3/<shape>/` — `evidence_test.json` (the **`evidence-test-author`**
  agent's per-shape hypothesis menu + measurement descriptors + decision rules)
  and `assignments_<server>.json` (the arbiter's per-branch verdicts).
- `bench/` — the deterministic machinery: `tools/{joint_necessity,
  value_distance_reached,depth_reach}.py` + `bench/tools/i2s_operand_availability.py`
  (operand_enrichment) are the ~4 shared **measurement tools**; `tool_registry.json`
  catalogs them; `arbitrate.py` applies each shape's rules per branch (NO LLM);
  `build_dataset.py` merges `assignments_*.json` across servers → `dataset.jsonl`.
- **Multi-server:** two servers hold disjoint targets' corpora. Each sets
  `BENCH_SERVER` + `BENCH_ONDISK`, scores its own targets, writes
  `assignments_<server>.json`; `build_dataset.py` merges. **Each server must
  re-anchor every tool on a LOCAL target before trusting labels** (cross-target
  transfer isn't free).
- **Rigor guardrails:** G1 every label makes a falsifiable + *discriminating*
  real-data prediction; G2 label-SOURCE (analysis) independent from
  verification-SIGNAL (campaign data); G3 keep refuted/inconclusive labeled —
  honest `inconclusive`/`decidable:false` are correct outcomes, don't chase 100%.
- **Labeling loop (loop-until-dry, ≤3 rounds; spec §8.4):** round 0 = original
  design; rounds 1–3 re-invoke `evidence-test-author` on **every shape with ≥1
  unlabeled decisive branch** (selection by presence-of-unlabeled, NOT a "high %"
  threshold; `seed_starved`-only branches route to re-bisection instead). Prompt is
  assembled deterministically by `tools/build_reinvoke_prompt.py --shape <S>`.
  Invariants: re-design TARGETS the unlabeled branches only (confirmed ones FROZEN);
  **monotonic superset** (keep every prior hypothesis that confirmed ≥1 branch, so
  re-arbitration never loses a label — enforce by diffing for label→inconclusive
  regressions and restoring the dropped hypothesis from `evidence_test.r0.json`);
  **novelty** (a refuted mechanism may not be re-tested with a relaxed threshold —
  only a genuinely different one). **Both servers re-arbitrate each round before the
  next** (the shared `evidence_test.json` covers both; arbiter scores only its
  `BENCH_ONDISK` targets). Stop at convergence (a round adds no new labels); the
  per-round label-gain curve is the reported rigor artifact; identical categories
  are merged in the manual Pass-C review.
- The end-goal beyond the benchmark: distil each validated feature into a
  **static/cheap-dynamic recognizer** (gate shape + operand provenance + CFG
  context) so an adaptive fuzzer can recognize a blocker type online and enable
  the right technique — the benchmark is its training + validation set.

The sections below describe the ORIGINAL steps 1–5b; steps 1–4 are unchanged and
still produce the labeled branches. Step 5b's synthesize-and-verify is
superseded by the above (kept as historical record + local-feature sidecar).

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
├── step5b/             # Step 5b — author→verify→adjudicate→revise loop, ALL outcomes in place
│   ├── briefs/<feature_id>.json      # Per-cluster authoring brief (build_template_briefs.py)
│   └── <feature_id>/
│       ├── verdict.json              # TERMINAL: status ∈ reproduced | rejected | inconclusive
│       ├── loop_state.json           # Append-only revision trail (one row per attempt)
│       └── attempts/<hN_tM>/         # Per-attempt: brief.json + template.c + params.json
│                                     #   + feature_spec.json + verification_run.json + adjudication.json
├── templates/          # DEPRECATED 2026-06-05 — prior promote-on-reproduce catalog; no longer
│   └── legacy/         #   written/read. Outcomes now live in step5b/<id>/verdict.json. Kept as
│                       #   historical methodology record only (see Feature Catalog section).
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
| **verdict-adjudicator** (Opus) | `step5b/<feature_id>/attempts/<hN_tM>/adjudication.json` | **Adjudicator** stage of **step 5b** — the INDEPENDENT judge invoked only when `verify_template.py` returns refuted / inconclusive(with-crashes) / partially_reproduced. Reads the harness + `verification_run.json` signals + the brief, and rules `harness_artifact` (→ INNER loop: re-author with feedback, budget N=3), `genuine_refutation` (→ OUTER loop: escalate to `hypothesis-reviser`, budget M=3; may early-escalate), or `underpowered` (→ bounded rerun). Writes the per-attempt decision; the terminal `verdict.json` (reproduced/rejected/inconclusive) is the orchestrator's. Deliberately separate from author + reviser to block confirmation bias. Read+Write. |
| **hypothesis-reviser** (Opus) | `step5b/<feature_id>/attempts/<h(N+1)>/brief.json` (revised) or `no_viable_revision.json` | **Outer-loop** stage of **step 5b** — invoked on `genuine_refutation`. Reads the refuted brief + `verification_run.json` + `adjudication.json` + `loop_state.json` and emits ONE **shallow** revision: a new `mechanism_label` / `definition` / suggested axis+knob for the **same member set** (NO re-cluster, NO 4b re-analysis, NO membership change). Leads on the observation the old hypothesis failed to explain; declines (`no_viable_revision` → feature goes `inconclusive`) rather than relabel cosmetically. The only 5b agent that consumes empirical verification feedback to re-form a hypothesis; separate from both author and `feature-hypothesis-generator` (whose isolation contract it must not break). Read+Write. |

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
- `mechanism_family.py` — deterministic per-technique `<T>_pro`/`<T>_anti` bucketing (all 10 techniques) via `coarse_family(covers_pairs)`, plus **branch-level `route_branch(hyps)`**: unions a branch's pairs and routes ALL its hyps to `synergy` when the union is the I2S×VP joint-necessity composite (synergy is AUTHORITATIVE → I2S_pro/VP_pro exclude it at the source; `independent` is not built; contradictions → `mixed`). Self-test/scan.
- `build_signature_cards.py` — build per-family distiller cards (routed via `route_branch`, with `analysis_path` back-pointers; analysis fields + candidates-CSV locators) for the `hypothesis-signature-distiller` agent. Pass B (the classifier) reads the signatures + cards directly — no group-by tool.
- `check_synergy_clusters.py` — deterministic validator for the synergy Pass-B output: coverage (every card in exactly one cluster) + the **co-cluster invariant** (a branch's `_h0`/`_h1` halves must share a cluster) + schema. Synergy Pass B uses the canonical `step5a/synergy/PASSB_PROMPT.md`; this tool is its backstop.

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

## Feature Catalog (templates/ — DEPRECATED 2026-06-05)

> **DEPRECATED:** the `templates/` and `templates/legacy/` folders are no longer
> used. Step 5b now keeps every outcome in place under `step5b/<feature_id>/`,
> with the verdict as the `status` field of `step5b/<feature_id>/verdict.json`
> (`reproduced` / `rejected` / `inconclusive`) — there is no promote-to-`templates/`
> or record-to-`legacy/` step. To enumerate verified features, query
> `step5b/*/verdict.json` for `status == reproduced`. The tables below are the
> **historical** verified/refuted methodology record from the prior
> template-writing era and are retained for reference only.

Falsifiable hypothesis harnesses, one per surviving program-feature
hypothesis. Under the analysis-only contract (2026-05-17) these are
produced by the **step 5a Pass B classifier** from the per-branch
`.analysis.json` files — NOT directly by the `feature-hypothesis-generator`
agent. The existing entries below predate the contract (prior template-writing
era) and are kept as the verified/refuted methodology record. Each entry
(historically `templates/<feature_id>/`)
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
   `coarse_family(covers_pairs)` maps each hypothesis to one `<technique>_pro` /
   `<technique>_anti` family (for all 10 techniques) from the technique +
   direction in `covers_pairs` — robust to the ≥8/8 cutoff wobble that flips the
   fine decisive-shape. **Branch-level routing** (`route_branch(hyps)`) sits on
   top: it unions a branch's `covers_pairs` and, if the union is the I2S×VP
   joint-necessity composite (`synergy`, resolves ONLY under
   `value_profile_cmplog`), routes **all** that branch's hypotheses to `synergy`
   — making synergy a first-class, AUTHORITATIVE family so the single-technique
   families (`I2S_pro`/`VP_pro`) exclude those branches at the source (no later
   de-dup). Everything else routes per-hypothesis; the old `independent`
   composite is **not built** (its arms each resolve alone, so they belong in
   `I2S_pro`/`VP_pro`), and a contradictory edge-set falls to the `mixed` escape.
   Families are hard buckets; clustering never crosses them.
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
   **Composite (`synergy`) caveat:** each synergy branch carries two signatures
   (an I2S `_h0` + a VP `_h1`) of ONE joint mechanism, so its Pass B uses the
   canonical prompt in `step5a/synergy/PASSB_PROMPT.md` (cluster by joint
   mechanism, keep a branch's `_h0`/`_h1` together, no per-target lumping) and is
   verified by `tools/check_synergy_clusters.py` (deterministic coverage +
   co-cluster invariant). The classifier agent definition stays generic.

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
# Families are whatever route_branch emits (single-technique <T>_pro/<T>_anti +
# synergy). build_signature_cards --family synergy now builds synergy directly
# (route_branch handles the I2S×VP union); there is no separate detect_synergy step.
for fam in I2S_pro VP_pro I2S_anti synergy \
           grimoire_structural_pro grimoire_structural_anti \
           ctx_coverage_pro ctx_coverage_anti \
           ngram_coverage_pro ngram_coverage_anti \
           calibrated_energy_pro aflfast_rarity_anti; do
  python3 tools/build_signature_cards.py --family $fam --out step5a/$fam.cards.json
  # dispatch hypothesis-signature-distiller over $fam.cards.json -> step5a/$fam/signatures.json
  # dispatch signature-feature-classifier on signatures.json + cards -> step5a/$fam/clusters.json
done
# synergy Pass B: use step5a/synergy/PASSB_PROMPT.md, then:
python3 tools/check_synergy_clusters.py                            # co-cluster invariant
```

**Step 5b — author → preflight → verify → adjudicate loop**
(built + end-to-end validated 2026-05-24):

The loop turns each step-5a cluster into a verified / rejected / inconclusive
template. THREE agents bracket two deterministic tools: `template-author`
(inner), `verdict-adjudicator` (judge), `hypothesis-reviser` (outer). It is a
**two-level loop** (revised 2026-06-05):
- **INNER (template revision), budget N=3** — fix a *broken harness* while
  holding the hypothesis fixed (minimal attributable diff).
- **OUTER (hypothesis revision), budget M=3** — when a *faithful* harness
  refutes, the `hypothesis-reviser` re-forms the mechanism for the SAME members
  (shallow: no re-cluster, no 4b re-analysis) and the inner loop restarts.

The adjudicator may **early-escalate** to the outer loop (rule `genuine_refutation`
before N is spent) when the *hypothesis*, not the harness, is the problem.

**No `templates/` or `legacy/` move — all outcomes stay in place under
`step5b/<feature_id>/`;** the terminal status is a field in
`verdict.json`, one of **reproduced** (a sweep reproduced the predicted
divergence), **rejected** (faithful harnesses refuted cleanly across all
revisions — confident negative), or **inconclusive** (reviser declined / M
exhausted / unresolved underpowered — left for manual review).

```
build_template_briefs.py  → step5b/briefs/<id>.json   (cluster + members' analyses)
  └─ template-author agent → step5b/<id>/attempts/<hN_tM>/{template.c, params.json, feature_spec.json}
       └─ check_template.py (preflight) ──FAIL──────────────┐ mechanical → re-author  (INNER, N=3)
            └─ PASS → verify_template.py (smoke→full sweep)  │
                 ├─ reproduced / reproduced_in_median → verdict.json status=reproduced  ✓
                 ├─ build_fail / execs=0 / all-zero ─────────┘ mechanical → re-author  (INNER, N=3)
                 └─ refuted / inconclusive(w/crashes) / partially
                      └─ verdict-adjudicator agent → attempts/<hN_tM>/adjudication.json
                           harness_artifact   → re-author w/ feedback        (INNER, N=3)
                           genuine_refutation → hypothesis-reviser agent      (OUTER, M=3)
                           │                       → attempts/<h(N+1)>/brief.json (new mechanism)
                           │                       → restart INNER on the revised brief
                           │                       → reviser declines / M exhausted → status=inconclusive
                           │                       → all revisions refute cleanly    → status=rejected
                           underpowered       → bounded rerun (more trials / wider scan)
```

Every attempt is preserved under `step5b/<id>/attempts/<hN_tM>/`
(brief + harness + `verification_run.json` + `adjudication.json` + feedback);
`step5b/<id>/loop_state.json` is the append-only revision trail (one row per
attempt: ids, verify verdict, adjudication decision, feedback, next action).
**Cost guard:** run a *smoke* sweep inside the loop; spend the full `params.json`
budget only to confirm an attempt that looks `reproduced`.

Orchestration is **Claude-orchestrated** (a documented procedure, not yet a
driver script): Claude dispatches the agents, runs the tools, and maintains
`loop_state.json` + `verdict.json` per the two-level budgets (N=3 inner, M=3
outer).

```bash
python3 tools/build_template_briefs.py --family all          # step5b/briefs/*.json
# INNER: dispatch template-author over a brief -> step5b/<id>/attempts/<hN_tM>/{template.c, params.json, feature_spec.json}
python3 tools/check_template.py  --template step5b/<id>/attempts/<hN_tM>   # preflight (cheap; gates the sweep)
python3 tools/verify_template.py --template step5b/<id>/attempts/<hN_tM> --trials 2 --duration-s 15 \
    --fuzzers naive,cmplog --scan-values 1,8                 # SMOKE first (decisive pair, tiny budget)
python3 tools/verify_template.py --template step5b/<id>/attempts/<hN_tM>   # FULL sweep only to confirm a `reproduced`-looking smoke
# if non-reproduced: dispatch verdict-adjudicator -> attempts/<hN_tM>/adjudication.json
#   harness_artifact   -> re-author (INNER, N=3)
#   genuine_refutation -> dispatch hypothesis-reviser -> attempts/<h(N+1)>/brief.json (OUTER, M=3), restart INNER
#   underpowered       -> bounded rerun
# on terminate: write step5b/<id>/verdict.json {status: reproduced|rejected|inconclusive}
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

**Outcomes stay in place (no separate catalog).** Everything for a feature lives
under `step5b/<feature_id>/`; the verdict is the `status` field of
`verdict.json` (`reproduced` / `rejected` / `inconclusive`), NOT a move into a
`templates/` or `legacy/` folder. **The `templates/` and `legacy/` folders are
deprecated (2026-06-05)** — they were the prior "promote-on-reproduce" staging
model and are no longer written or read by the loop. To find verified features,
query `step5b/*/verdict.json` for `status == reproduced`. **Validated 2026-05-24:**
the loop ran end-to-end on `opaque_exact_literal_dispatch_gate` (author →
preflight PASS → smoke verify `reproduced`); the two-level revision loop +
in-place verdicts were added 2026-06-05.

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

