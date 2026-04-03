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
├── clusters/           # Output from branch-cluster (<target>_clusters.md)
├── reports/            # Output from fuzzing-root-cause-analyzer (<target>_report.md)
├── db/                 # SQLite database (blockers.sqlite)
├── tables/             # Exported CSV tables from the database
├── tools/              # Reusable analysis scripts
│   ├── extract_blockers_ts.py  # Time-series blocker extraction (chronological forward pass)
│   ├── blocker_db.py           # CLI for managing the blockers SQLite database
│   ├── seed_bisect.py          # 10-bucket bisection to find seeds that hit blocking branches
│   ├── seed_diff.py            # MI-based seed diff: pre-computes byte-level mutual information
│   ├── cluster_orchestrator.py # Orchestrates parallel T1 agents + T2 verification loop
│   ├── cluster_t2.py           # Mechanical T2 cluster verification (no LLM, Docker-based)
│   └── cluster_report.py       # Generate cluster report from DB or JSON (deterministic, no LLM)
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

Four specialized agents are available in `.claude/agents/`:

| Agent | Output folder | File naming | Purpose |
|-------|--------------|-------------|---------|
| **fuzzing-branch-analyzer** | `blockers/` | `<target>_blockers.md` | Parses coverage reports, identifies asymmetric branch pairs, cross-references across fuzzers to confirm input-dependency |
| **branch-cluster** | `clusters/` | `<target>_clusters.md` | Identifies which input bytes control each blocking branch via seed diff + source tracing + Docker mutation verification, then clusters branches by shared controlling byte regions |
| **fuzzing-root-cause-analyzer** | `reports/` | `<target>_report.md` | Reads cluster results, analyzes seed lineage and coverage divergence per cluster, diagnoses why specific fuzzers fail, writes findings |
| **seed-generator** | `seeds/` | `<target>_seeds.md` | Reads blocker lists, traces constraints backward from blocked branches, constructs concrete seed byte sequences that hit blocked sides |

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

### Branch Clustering

Orchestrated by `cluster_orchestrator.py`, which manages a parallel T1→T2 loop:

**Selection:** Branches from DB where `selection_tags != '[]'` and both blocking and resolving fuzzers exist.

**Architecture:**
- **Orchestrator** (`cluster_orchestrator.py`): Selects candidates, samples T1 reps, spawns agents/tools, maintains JSON state at `clusters/<target>_state.json`
- **T1 workers** (`branch-cluster` agent): One agent per branch, spawned in parallel (default 10). Diffs seeds, traces source, formulates + verifies byte hypothesis. Returns JSON result.
- **T2 verification** (`cluster_t2.py`): Python tool (no LLM). One Docker container per branch, tests necessity (Test A: 1 positive seed) and sufficiency (Test B: 3-5 negative seeds from different fuzzers/trials). All seeds run inside one container with unique profraw per seed.
- **Report** (`cluster_report.py`): Generates markdown from JSON state or DB. Deterministic, no LLM.

**T1 sampling:** Proportional per function, min 10 total, at least 1 per function. Priority: more selection tags > higher divergence values.

**T2 strengthened sufficiency:** Test B uses 3-5 negative seeds. All must pass (blocked side appears after injecting controlling bytes). Partial pass → unfitted (promoted to T1).

**Loop:**
- T1 produces ≥1 new cluster → T2 fits remaining → unfitted promoted to next T1 round
- T1 produces 0 new clusters → re-select different reps → retry
- Two consecutive T1 rounds with 0 new clusters → mark remaining as SKIPPED

## Typical Workflow

1. Run LibAFL fuzzers on target; run `run_coverage_timeseries.sh` to generate per-checkpoint coverage reports under `out/coverage_ts/`.
2. Run `extract_blockers_ts.py` to extract blockers via chronological forward pass → writes `branches`, `trial_coverage`, `derived_metrics` (with selection tags) to `db/blockers.sqlite`.
3. Run `seed_bisect.py scan` to find resolving and blocking seeds (parallel per target), then `insert` sequentially → writes `resolving_seeds`, `resolving_seed_lineage`, `blocking_seeds`, `blocking_seed_lineage` to DB.
4. Run `cluster_orchestrator.py` to manage parallel T1 (agent) + T2 (tool) clustering → state in `clusters/<target>_state.json`.
5. Run `cluster_report.py --from-json` to generate the clean cluster report → output in `clusters/`.
6. Run `blocker_db.py import-clusters` to populate DB for SQL queries (optional).
7. Use `fuzzing-root-cause-analyzer` on cluster results to analyze seed lineage, coverage divergence, and diagnose why specific fuzzers fail per cluster → output in `reports/`.
