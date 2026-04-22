# BlockerAnalyzer

A research project for analyzing fuzzing "blockers" — branches that coverage-guided fuzzers fail to reach — and diagnosing why.

## Project Structure

```
BlockerAnalyzer/
├── coverage/           # Fuzzer coverage reports (llvm-cov annotated source format)
│   ├── harfbuzz/
│   │   ├── cmplog.cov  # Coverage from AFL++ cmplog fuzzer
│   │   └── n4.cov      # Coverage from AFL++ n4 fuzzer
│   ├── htslib/
│   └── libpcap/
├── fuzz/               # AFL++ fuzzing campaign output (per-target)
│   └── <target>_out/default/  # queue/, crashes/, fuzzer_stats, etc.
├── targets/            # Source code of fuzz targets
│   ├── harfbuzz/       # Real-world target: HarfBuzz text shaping library
│   ├── htslib/         # Real-world target: HTSlib genomics library
│   ├── libpcap/        # Real-world target: libpcap packet capture library
│   ├── blocker_1/      # Synthetic: indirect input dependency
│   ├── blocker_2/      # Synthetic: missing function call
│   ├── blocker_3/      # Synthetic: compile-time gate
│   └── blocker_4/      # Synthetic: magic value conjunction
├── blockers/           # Output from fuzzing-branch-analyzer (<target>_blockers.md)
├── clusters/           # 3-dim clustering output: <target>_3dim_clusters.json (nested L1→L2→L3)
├── reports/            # Per-L3 RCA findings: <target>/<cluster_id>__<fn_slug>__<l3_range>.json
│   └── <target>/legacy/  # Reports from prior clustering schemes (kept for reference)
├── data/functions/     # Per-target function sidecars: <target>.json (file, name, start_line, end_line)
├── db/                 # SQLite database (blockers.sqlite)
├── tables/             # Exported CSV tables from the database
├── tools/              # Reusable analysis scripts
│   ├── extract_blockers_ts.py  # Time-series blocker extraction (chronological forward pass)
│   ├── blocker_db.py           # CLI for managing the blockers SQLite database
│   ├── seed_bisect.py          # 10-bucket bisection to find seeds that hit blocking branches
│   ├── seed_diff.py            # MI-based seed diff: pre-computes byte-level mutual information
│   ├── extract_functions.py    # Runs llvm-cov export in Docker; writes data/functions/<target>.json
│   ├── cluster.py              # 3-dim clustering lib; emits nested L1→L2→L3 (function groups + Tukey splits)
│   ├── cluster_runner.py       # CLI: load DB → run clustering → write clusters/<target>_3dim_clusters.json
│   ├── select_rca_targets.py   # Selector: filter L3 regions by size, emit one RCA job per L3
│   ├── cluster_verify.py       # Docker-based branch-hypothesis verification
│   └── (legacy) cluster_orchestrator*.py, cluster_t2.py, cluster_report*.py  # T1/T2/T3 pipeline — superseded
├── docker/             # Docker infrastructure for coverage-instrumented builds
│   ├── Dockerfile.coverage-base  # Base image (clang-18, llvm-18, COV_FLAGS)
│   ├── run_bisect_entrypoint.sh  # Entrypoint: run seeds, produce llvm-cov show output
│   └── targets/                  # Per-target coverage Dockerfiles
│       ├── Dockerfile.bloaty.cov
│       ├── Dockerfile.lcms.cov
│       ├── Dockerfile.libpcap.cov
│       ├── Dockerfile.mbedtls.cov
│       └── Dockerfile.sqlite3.cov
├── output/             # Legacy one-off reports (superseded by blockers/reports/analysis/)
└── .claude/
    ├── agents/         # Specialized Claude agents for analysis
    └── settings.json   # Project permissions (Bash allowed for all agents)
```

## Synthetic Blocker Benchmarks

These are minimal libFuzzer harnesses designed to represent specific blocker patterns:

- **blocker_1**: Indirect input dependency — the blocking branch `if (secret_unlocked)` at line 65 guards on a variable, not directly on input bytes. `secret_unlocked` is set via two input-dependent paths: directly when `data[0] == 0xFF`, or indirectly via `process_secret()` when `compute_checksum(fp->data) == PROTO_SECURE (0x04)`. The fuzzer sees a branch on a derived/intermediate variable rather than on the raw input, making the dependency indirect and harder to infer.
- **blocker_2**: Missing function call — `process_secret()` (which sets `secret_unlocked = 1`) is defined but never called from any reachable code path. The `if (secret_unlocked)` branch is permanently dead because the function that would flip the flag is simply absent from the call graph.
- **blocker_3**: Compile-time gate — `g_session.unlocked` is controlled by the `UNLOCK_SECRET` preprocessor macro, not runtime input. The blocking branch cannot be reached without recompilation.
- **blocker_4**: Magic value conjunction — `__builtin_trap()` requires matching three separate magic byte sequences simultaneously: header `0xDEAD`, type `0xCAFEBABE`, and footer `0xC0DE`.

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
| **fuzzing-branch-analyzer** | `blockers/<target>_blockers.md` | Parses coverage reports, identifies asymmetric branch pairs, cross-references fuzzers to confirm input-dependency |
| **cluster-root-cause-analyst** (current RCA unit) | `reports/<target>/<cluster_id>__<slug>.json` | One call per **sub-cluster** from the 3-dim pipeline. Reads branches, pulls seeds/lineage from DB, reads source, writes one structured JSON hypothesis. Sonnet model. Designed for parallel fan-out. |
| **fuzzing-root-cause-analyzer** | `reports/<target>_report.md` | Legacy whole-target RCA; superseded by per-sub-cluster agent but still available for summary reports |
| **seed-generator** | `seeds/<target>_seeds.md` | Reads blocker lists, traces constraints backward, constructs concrete seed bytes that hit blocked sides |

**Legacy (T1/T2/T3 pipeline, superseded):** `branch-cluster`, `cluster-fit`, `switch-cluster`. Their `.md` files remain in `.claude/agents/` for reference but are not part of the current pipeline.

## Permissions

`.claude/settings.json` grants `Bash(*)` project-wide, so all agents can run shell commands (including `extract_blockers_ts.py`) without prompting. Do not remove this — the `fuzzing-branch-analyzer` agent requires Bash to invoke the extraction tool on large coverage files.

## Tools

### `tools/extract_blockers_ts.py` (primary)

Time-series blocker extraction. Walks coverage checkpoints chronologically (30-min intervals), maintaining per-(fuzzer, trial) state for every branch. At each checkpoint: parses all reports, identifies asymmetric branches, applies 3-level confirmation, and accumulates duration. Writes directly to the DB.

```bash
python3 tools/extract_blockers_ts.py \
  --target lcms \
  --ts-base ./out/coverage_ts \
  [--fuzzers naive cmplog value_profile value_profile_cmplog] \
  [--trials 3] \
  [--step 1800]
```

**Algorithm (single forward pass):**
1. For each checkpoint T (1800s, 3600s, ...):
   - Parse all (fuzzer, trial) `branch_coverage_show.txt` at T
   - For each branch side, update `hit_status`: -1 (unreached) → 0 (blocked) → 1 (resolved)
   - Accumulate `duration_h` only while `hit_status=0` (+0.5h per step)
2. Apply 3-level confirmation (L1: cross-trial same fuzzer, L2: same fuzzer final T, L3: cross-fuzzer)
3. Write confirmed blockers to DB (`branches` + `trial_coverage`), then run `compute-derived`

**Duration values:** -1.0 = N/A (never blocked — unreached or resolved from first checkpoint), ≥0 = time spent blocked.

**Data path:** `{ts-base}/{target}/{fuzzer}/trial{N}/reports/{time_s}/branch_coverage_show.txt`

### `tools/blocker_db.py`

CLI for managing the blockers SQLite database at `db/blockers.sqlite`.

```bash
python3 tools/blocker_db.py init                          # Initialize schema
python3 tools/blocker_db.py compute-derived --target <name>  # Recompute derived metrics
python3 tools/blocker_db.py query --target <name> [--format md|csv|json]
python3 tools/blocker_db.py export --target <name> [--format md|csv|json]
python3 tools/blocker_db.py import-clusters --input clusters/<target>_state.json  # JSON → DB
```

**Database schema (8 tables):**

| Table | Purpose | Key fields |
|-------|---------|------------|
| `branches` | One row per confirmed blocker | `target`, `file`, `function`, `line`, `col`, `blocked_side`, `source_line`, `confirmation_level` (1/2/3) |
| `trial_coverage` | Per-(fuzzer, trial) metrics | `hit_status` (-1=unreached/0=blocked/1=resolved), `duration_h` (-1=N/A, ≥0=time blocked), `hitcount`, `other_hitcount` |
| `derived_metrics` | Per-branch summary | `fuzzer_block_probability` (JSON), `fuzzer_avg_hitcount` (JSON), `fuzzer_avg_duration_h` (JSON), `blocking_fuzzers`, `resolving_fuzzers`, `unreached_fuzzers`, `prob_div`, `dur_div`, `hit_div`, `selection_tags` (JSON) |
| `cluster_assignments` | Branch-to-cluster mapping per clustering run | `branch_id`, `target`, `cluster_id`, `tier` (1=T1/2=T2), `controlling_bytes`, `semantic_label`, `run_date` |
| `resolving_seeds` | Seeds hitting the **blocked** side (from resolving fuzzers) | `branch_id`, `fuzzer`, `trial`, `seed_id`, `parent_seed_id`, `mutation_op`, `discovery_time_s` |
| `resolving_seed_lineage` | Parent chain for resolving seeds | `branch_id`, `fuzzer`, `trial`, `seed_id`, `depth`, `ancestor_id`, `mutation_op` |
| `blocking_seeds` | Seeds hitting the **other** side (from blocking fuzzers) | Same schema as `resolving_seeds` |
| `blocking_seed_lineage` | Parent chain for blocking seeds | Same schema as `resolving_seed_lineage` |

**Selection tags:** Branches are tagged for analysis based on three divergence metrics:
- `prob_div` — max(p) - min(p) across fuzzers (excluding unreached). Tagged when = 1.0
- `dur_div` — max(avg_dur) - min(avg_dur), null/-1 treated as 0. Tagged when > 8.0h
- `hit_div` — max(avg_hits) - min(avg_hits) (excluding unreached). Tagged when > 100

`selection_tags` is a JSON array (e.g., `["prob_div", "dur_div"]`). Branches with any tag are candidates for clustering and root cause analysis. Branches with more tags are higher priority.

### `tools/seed_bisect.py`

Finds which seeds in each fuzzer's queue hit each confirmed blocker. Runs **one Docker container per target** — inside, scans each unique queue once checking ALL target branches simultaneously.

```bash
python3 tools/seed_bisect.py build --target <name>      # Build Docker image (one-time)
python3 tools/seed_bisect.py scan --target <name> --queue-base ./out   # Docker scan only → results.json
python3 tools/seed_bisect.py insert --target <name> --results <path> --queue-base ./out  # Insert results into DB
python3 tools/seed_bisect.py run --target <name> --queue-base ./out    # scan + insert in one step
python3 tools/seed_bisect.py plan --target <name> --queue-base ./out   # Dry-run
```

`scan` and `insert` are separated so multiple targets can scan in parallel (Docker containers) and insert sequentially (no DB contention). Results are saved to `db/bisect_results/<target>_results.json`.

**End-to-end flow:**

1. **Select branches and trials** (`get_branches_to_process`): For each branch, find resolving trials (fuzzers with `hit_status=1`, pick `MIN(trial)` per fuzzer) and blocking trials (`hit_status=0`, same). Skip branches with no resolving trials.

2. **Build jobs** (`build_jobs`): Group work by queue directory. For each branch:
   - Each resolving `(fuzzer, trial)` → job searching for seeds that hit the **blocked side** → `resolving_seeds`
   - Each blocking `(fuzzer, trial)` → job searching for seeds that hit the **other side** → `blocking_seeds`
   - Jobs sharing the same queue path are scanned together in one pass.

3. **Container scan** (`bisect_in_container.py`): One Docker container per target. For each queue:
   - **10-bucket bisection**: split seeds into 10 buckets, run each bucket as a batch through `FUZZ_BIN` (many seeds per invocation, one profraw), merge → one `llvm-cov show` per bucket checking ALL active branches at once.
   - For branches hit in a bucket, recurse (split into 10 again). At ≤10 seeds, test individually.
   - **Early-stop per branch** at `max_seeds` hits — removes completed branches from active specs so deeper buckets skip them.
   - Output: `results.json` with `{branch_id: [seed_name, ...]}` per queue.

4. **Insert into DB** (`insert_seeds_and_lineage`): For each hitting seed, parse its `.metadata` file for parent + mutation ops, insert into seed table, walk parent chain (up to 50 depth) for lineage table.

**`max_seeds` semantics:** The limit is per **(branch, queue)**, where each queue is one `(fuzzer, trial)`. A branch with 3 resolving queues and `max_seeds=10` can accumulate up to 30 resolving seeds total (10 from each queue). For branch clustering, `--max-seeds 10` is sufficient.

**Options:** `--max-seeds N` (default 50), `--batch-size N` (seeds per `FUZZ_BIN` invocation, default 500).

**Docker images:** Named `blocker-{target}-cov`, built from `docker/Dockerfile.coverage-base` + `docker/targets/Dockerfile.{target}.cov`.

**LibAFL metadata format:** Each seed `HASH` has a `.HASH.metadata` JSON file containing:
- Parent info: `parent_id`, `parent_file` (hex hash of parent seed), `execs`, `elapsed_ms`
- Coverage map: list of coverage index IDs
- Mutation ops: list like `["ByteRandMutator", "BytesDeleteMutator"]`

### LibAFL Fuzzers

The LibAFL FuzzBench experiment uses 4 fuzzer variants on 5 targets (`bloaty`, `lcms`, `libpcap`, `mbedtls`, `sqlite3`), 3 trials each:

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

### 3-Dimensional Clustering (current pipeline)

Cluster branches by fuzzer *behavior* along three independent dimensions, then hypothesize a root cause per L3 line region. Supersedes the legacy T1/T2/T3 agent pipeline.

#### The three dimensions (L1)

Each branch has a 4-tuple (one entry per fuzzer) in each dimension, sourced from `derived_metrics`:

| Dim | Signal | Clustering method |
|-----|--------|-------------------|
| **dim1** — block probability | ternary label per fuzzer (`never`/`rarely`/`sometimes`/`mostly`/`always`/`never_reached`) | Exact `GROUP BY` on the 4-tuple. Pattern **interesting** iff it contains both `never` and `always` (deterministic capability gap). Divergence = normalized label entropy. |
| **dim2** — blocking duration | hours blocked per fuzzer (averaged across trials) | HDBSCAN on log1p + z-scored 4-d vector with `-1` sentinels handled; keep clusters above `--dim2-min-div` divergence. |
| **dim3** — hitcount | hits on current/opposite side per fuzzer | HDBSCAN on log1p + z-scored vector; keep clusters above `--dim3-min-div`. |

Dimensions are *independent* — same branch may appear in a dim1 cluster AND a dim2 cluster AND a dim3 cluster.

#### Three-level hierarchy (L1 → L2 → L3)

- **L1 — dim cluster.** Top-level group of branches sharing a dim pattern.
- **L2 — function group.** Within each L1, branches grouped by enclosing C function (from `data/functions/<target>.json`, built by `tools/extract_functions.py` via `llvm-cov export`). One L2 per unique `(file, function)`.
- **L3 — line region.** Within each L2, Tukey's-fence adaptive splitting on consecutive-line gaps. A function with uniformly spaced branches → 1 L3 covering the whole function. A function with branches split across multiple distinct code regions → multiple L3s. Threshold: `gap > max(adaptive_floor=20, Q3 + 1.5·IQR)`; requires ≥ `adaptive_min_n=4` branches to attempt a split (smaller groups stay as one L3).

**The RCA unit is L3.** Fan out one `cluster-root-cause-analyst` agent per L3 region.

#### Function sidecar

```bash
python3 tools/extract_functions.py --target <name>
# Runs llvm-cov export inside blocker-<target>-cov Docker.
# Writes data/functions/<target>.json with [{file, name, start_line, end_line}, ...].
```

Required before clustering; `cluster_runner.py` auto-loads it from `data/functions/<target>.json` (override with `--functions PATH`). If absent, clustering falls back to legacy file+line-proximity grouping (function=null).

#### Pipeline

```bash
python3 tools/cluster_runner.py --target <name> \
    [--output clusters/<target>_3dim_clusters.json] \
    [--min-cluster-size 5] [--min-size 3] \
    [--dim2-min-div 1.0] [--dim3-min-div 1.0] \
    [--functions data/functions/<target>.json]
```

Loads branches + `trial_coverage` from the DB, patches `cluster.FUZZERS`, loads the function sidecar, runs `cluster.run_clustering()`, writes one combined JSON.

#### Output schema (`clusters/<target>_3dim_clusters.json`)

```json
{
  "summary": {"total_branches": 670,
              "dim1_clusters_found": 69, "dim1_clusters_kept": 8,
              "dim2_clusters_found": 21, "dim2_clusters_kept": 8,
              "dim3_clusters_found": 27, "dim3_clusters_kept": 5},
  "dim1_clusters": [
    {
      "cluster_id": "dim1_cluster_004",
      "pattern": {"cmplog": "always", "naive": "never", ...},
      "size": 34,
      "is_interesting": true,
      "divergence": {"dim1": 0.3138},
      "sub_clusters": [                                 // L2: function groups
        {
          "file": "/src/sqlite3/bld/sqlite3.c",
          "function": "sqlite3.c:sqlite3VdbeExec",
          "size": 9,
          "line_range": [86324, 87289],
          "tukey_split": true,
          "line_regions": [                             // L3: split by Tukey
            {"line_range": [86802, 87289], "size": 8, "branches": [...]},
            {"line_range": [86324, 86324], "size": 1, "branches": [...]}
          ]
        }
      ]
    }
  ],
  "dim2_clusters": [...],
  "dim3_clusters": [...]
}
```

Key invariants: every L2 has `line_regions` with ≥1 entry. `tukey_split=false` → exactly 1 entry. `function=null` → L2 came from unmapped-branch fallback (legacy line-proximity grouping).

#### Selecting RCA targets

`tools/select_rca_targets.py` reads the cluster JSON and emits one job per L3 region whose `size` meets a per-target threshold. The threshold is **fan-out policy**, not a clustering property — the JSON is never filtered.

```bash
python3 tools/select_rca_targets.py --target sqlite3             # default threshold
python3 tools/select_rca_targets.py --target sqlite3 --min-size 3
python3 tools/select_rca_targets.py --target all                 # summary across targets
python3 tools/select_rca_targets.py --target sqlite3 --format json  # feed into orchestrator
```

Per-target default threshold (`DEFAULT_MIN_SIZE` in the script):

| target | threshold | rationale |
|---|---|---|
| mbedtls | 1 | Only 25 candidate branches — every one worth a look |
| bloaty  | 2 | 214 candidate branches |
| sqlite3 | 2 | 670 candidate branches |
| lcms    | 2 | 358 candidate branches |
| libpcap | 2 | 679 candidate branches |

Under function grouping, size=2 is a meaningful unit (two branches in the same function sharing a dim pattern). Singletons under function grouping don't benefit from the shared-hypothesis framing and are skipped by default (except mbedtls).

#### Per-L3 root cause analysis

Fan out `cluster-root-cause-analyst` agents (sonnet, parallel) — one per L3 job emitted by the selector. Each agent:

1. Receives an L3 region plus L2 function context and L1 dim-cluster context.
2. Pulls resolving/blocking seeds + lineage from the DB for the L3 branches.
3. Reads source context (L3 line range ± 30, plus a skim of the full L2 function).
4. Formulates ONE hypothesis and classifies it into a `root_cause_class` (e.g., `I2S_constant_match`).
5. Optionally produces a `sibling_observation` if L2 had a Tukey split — a short note on whether the hypothesis plausibly extends to other L3 regions in the same function (NOT a deep re-analysis).
6. Writes one JSON to `reports/<target>/<cluster_id>__<function_slug>__<l3_line_range>.json`.

`status` values: `"ok"` | `"insufficient_input"` | `"no_clear_root_cause"`.

One hypothesis per call — do not try to find multiple root causes in one L3.

## Typical Workflow

1. Run LibAFL fuzzers; run `run_coverage_timeseries.sh` to generate per-checkpoint coverage reports under `out/coverage_ts/`.
2. `extract_blockers_ts.py` — chronological forward pass, writes `branches`, `trial_coverage`, `derived_metrics` to `db/blockers.sqlite`.
3. `seed_bisect.py scan` (parallel per target) → `insert` (sequential) — writes resolving/blocking seeds + lineage to DB.
4. `extract_functions.py --target <name>` — runs `llvm-cov export` in Docker, writes `data/functions/<target>.json`.
5. `cluster_runner.py --target <name>` — runs 3-dim clustering (L1 dim cluster → L2 function group → L3 Tukey split), writes `clusters/<target>_3dim_clusters.json`.
6. `select_rca_targets.py --target <name>` — emits one RCA job per L3 region passing the per-target threshold.
7. **Fan out `cluster-root-cause-analyst`** — one agent per L3 job, in parallel. Each writes a JSON hypothesis to `reports/<target>/<cluster_id>__<function_slug>__<l3_range>.json`.
8. (Optional) roll per-L3 findings into a per-target summary report.
