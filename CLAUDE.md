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
├── slices/             # Output from program-slice-builder (<target>_slices.md)
├── reports/            # Output from fuzzing-root-cause-analyzer (<target>_report.md)
├── analysis/           # Output from fuzzing-coverage-analyst (<target>_analysis.md)
├── seeds/              # Output from seed-generator (<target>_seeds.md)
├── db/                 # SQLite database (blockers.sqlite)
├── tables/             # Exported CSV tables from the database
├── tools/              # Reusable analysis scripts
│   ├── extract_blockers_ts.py  # Time-series blocker extraction (chronological forward pass)
│   ├── blocker_db.py           # CLI for managing the blockers SQLite database
│   └── seed_bisect.py          # 10-bucket bisection to find seeds that hit blocking branches
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

Five specialized agents are available in `.claude/agents/`:

| Agent | Output folder | File naming | Purpose |
|-------|--------------|-------------|---------|
| **fuzzing-branch-analyzer** | `blockers/` | `<target>_blockers.md` | Parses coverage reports, identifies asymmetric branch pairs, cross-references across fuzzers to confirm input-dependency |
| **program-slice-builder** | `slices/` | `<target>_slices.md` | Applies NEG pre-screening and traces execution paths (program slices) from the fuzzer entry point to each blocking branch; default batch size 10 |
| **fuzzing-root-cause-analyzer** | `reports/` | `<target>_report.md` | Reads pre-built slices, clusters by slice similarity, classifies root causes, and writes findings with mitigations |
| **fuzzing-coverage-analyst** | `analysis/` | `<target>_analysis.md` | Analyzes fuzzing campaigns (seed queues, mutation patterns) to diagnose why a fuzzer failed to penetrate input-dependent blockers |
| **seed-generator** | `seeds/` | `<target>_seeds.md` | Reads blocker lists, traces constraints backward from blocked branches, constructs concrete seed byte sequences that hit blocked sides, and clusters blockers by seed similarity |

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
```

**Database schema (7 tables):**

| Table | Purpose | Key fields |
|-------|---------|------------|
| `branches` | One row per confirmed blocker | `target`, `file`, `function`, `line`, `col`, `blocked_side`, `source_line`, `confirmation_level` (1/2/3) |
| `trial_coverage` | Per-(fuzzer, trial) metrics | `hit_status` (-1=unreached/0=blocked/1=resolved), `duration_h` (-1=N/A, ≥0=time blocked), `hitcount`, `other_hitcount` |
| `derived_metrics` | Per-branch summary | `fuzzer_block_probability` (JSON), `fuzzer_avg_hitcount` (JSON), `fuzzer_avg_duration_h` (JSON), `blocking_fuzzers`, `resolving_fuzzers`, `unreached_fuzzers`, `rank` |
| `resolving_seeds` | Seeds hitting the **blocked** side (from resolving fuzzers) | `branch_id`, `fuzzer`, `trial`, `seed_id`, `parent_seed_id`, `mutation_op`, `discovery_time_s` |
| `resolving_seed_lineage` | Parent chain for resolving seeds | `branch_id`, `fuzzer`, `trial`, `seed_id`, `depth`, `ancestor_id`, `mutation_op` |
| `blocking_seeds` | Seeds hitting the **other** side (from blocking fuzzers) | Same schema as `resolving_seeds` |
| `blocking_seed_lineage` | Parent chain for blocking seeds | Same schema as `resolving_seed_lineage` |

**Ranking:** Blockers are ranked by **fuzzer divergence** (larger differences = more interesting):
1. `probability_div` DESC — max(p) - min(p) across fuzzers (excluding unreached)
2. `duration_div` DESC — max(avg_dur) - min(avg_dur) (null treated as 0 = never stuck)
3. `hitcount_div` DESC — max(avg_hits) - min(avg_hits) (excluding unreached)

### `tools/seed_bisect.py`

Finds which seeds in each fuzzer's queue hit each confirmed blocker. Runs **one Docker container per target** — inside, scans each unique queue once checking ALL target branches simultaneously.

```bash
python3 tools/seed_bisect.py build --target <name>      # Build Docker image (one-time)
python3 tools/seed_bisect.py run --target <name> --queue-base ./out  # Run
python3 tools/seed_bisect.py plan --target <name> --queue-base ./out  # Dry-run
```

**Algorithm (multi-branch single-pass):**
1. Group all (branch, fuzzer, trial) jobs by queue
2. Start ONE Docker container per target with all queues mounted
3. For each unique queue: scan each seed once through `FUZZ_BIN`, check ALL target branches against the coverage
4. Early-stop per branch when `--max-seeds` reached (default 50)
5. Container outputs JSON with hitting seeds per branch
6. Host side: parse `.metadata` files for lineage, insert into `resolving_seeds`/`blocking_seeds` + lineage tables

**Options:** `--max-seeds N` (default 50, use 30 for large targets), `--parallel N` (default 8, inside container), `--timeout N` (total seconds, default 3600).

**Docker images:** Named `blocker-{target}-cov`, built from `docker/Dockerfile.coverage-base` + `docker/targets/Dockerfile.{target}.cov`.

**LibAFL metadata format:** Each seed `HASH` has a `.HASH.metadata` JSON file containing:
- Parent info: `parent_id`, `parent_file` (hex hash of parent seed), `execs`, `elapsed_ms`
- Coverage map: list of coverage index IDs
- Mutation ops: list like `["ByteRandMutator", "BytesDeleteMutator"]`

### Program Slices

`program-slice-builder` constructs a **dynamic program slice** for each confirmed blocker: an ordered sequence of control and data flow nodes from the fuzzer entry point to the blocking branch, filtered to only nodes actually executed by at least one fuzzer. Each node carries the exact statement text, file:line, types, function signatures, and per-fuzzer execution counts `[cmplog: N | n4: N]`.

Node types: `ENTRY` (fuzzer entry), `CALL` (function call on path), `CTRL` (control flow condition, annotated with required direction), `DATA` (variable binding that feeds the blocking condition), `BRANCH` (the blocking branch, always last).

**Dynamic filtering:** nodes with 0 hits in all fuzzers are dropped — they are not on the actual runtime path. If dropping a node creates a gap in the path, the agent searches for an alternate caller with non-zero hits, catching wrong-path traces early.

Each slice includes a one-line **Divergence point**: the earliest node where one fuzzer's count drops to 0 while the other remains non-zero. The slice carries no analysis or interpretation — all reasoning is deferred to `fuzzing-root-cause-analyzer`.

Slices are written to `slices/<target>_slices.md` and consumed by `fuzzing-root-cause-analyzer`. The file is appended to across batches, so multiple runs accumulate into a single target file.

### Branch Clustering

Clustering is performed by `fuzzing-root-cause-analyzer` from pre-built slices, using **program slice similarity**.

Two blockers are clustered when their slices share structural ancestry:

| Relationship | Criterion | Cluster role |
|--------------|-----------|-------------|
| **Downstream** | Slice A ⊇ Slice B (A has all of B's nodes plus more) | B is the cluster root; A is a downstream member |
| **Peer** | Slices share the same root node but neither contains the other | Both are peers; the shared root variable/condition is the cluster focus |

The cluster representative is always the blocker with the simplest (most upstream) slice. Resolving the root blocker's barrier also unblocks all downstream members. Peer members share the same fix strategy.

Cluster IDs (C01, C02, …) are assigned by the root cause analyzer in Step 2 and carried through the report.

### Negative Rules (Pre-screening)

`program-slice-builder` screens each blocker against four negative rules before building its slice. A blocker that matches is **skipped** and recorded in the Skipped Blockers section of the slices file, then carried through to the Skipped Blockers section of the root cause report.

| Rule | Criterion |
|------|-----------|
| **NEG-1** | Blocked block body contains only a `return` statement |
| **NEG-2** | Blocked block body contains only an error handler (`opt_error`, `fprintf`+`exit`, `abort`, `assert`, etc.) |
| **NEG-3** | Blocked block body contains only cleanup (`free`, `close`, `destroy`, etc.) |
| **NEG-4** | Branch or context is annotated `deprecated`, `legacy`, or `obsolete` |

Rules are defined inline in `program-slice-builder.md` — `rules.md` is superseded.

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

## Typical Workflow

1. Run LibAFL fuzzers on target; run `run_coverage_timeseries.sh` to generate per-checkpoint coverage reports under `out/coverage_ts/`.
2. Run `extract_blockers_ts.py` to extract blockers via chronological forward pass → writes `branches`, `trial_coverage`, `derived_metrics` to `db/blockers.sqlite`.
3. Run `seed_bisect.py` to find resolving and blocking seeds for each blocker → writes `resolving_seeds`, `resolving_seed_lineage`, `blocking_seeds`, `blocking_seed_lineage` to DB. One Docker container per target.
4. Use `program-slice-builder` on the DB to apply NEG screening and trace execution paths → output in `slices/`.
5. Use `fuzzing-root-cause-analyzer` on the slices file to cluster, classify root causes, and write findings → output in `reports/`.
6. Use `fuzzing-coverage-analyst` on input-dependent blockers with seed/lineage data to diagnose fuzzer logic weaknesses → output in `analysis/`.
