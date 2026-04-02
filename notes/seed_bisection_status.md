# Seed Bisection — Status and Next Steps

Updated: 2026-04-02

## Current State

### What's done
- `tools/seed_bisect.py` — orchestrator: one container per target, groups jobs by queue
- `docker/bisect_in_container.py` — 10-bucket batch bisection inside Docker: batches seeds through `FUZZ_BIN` (many per invocation), one `llvm-cov show` per bucket, recursive bisection to find individual seeds
- `tools/extract_blockers_ts.py` — time-series blocker extraction, working for all 5 targets
- DB schema: 7 tables including `resolving_seeds`, `resolving_seed_lineage`, `blocking_seeds`, `blocking_seed_lineage`
- Docker images built for all 5 targets
- CLAUDE.md fully updated with end-to-end flow documentation

### What's in the DB now
- All 5 targets: branches + trial_coverage + derived_metrics fully populated
- **lcms**: 11,506 resolving + 28,350 blocking seeds — verified correct
- **mbedtls**: 908 resolving + 1,671 blocking seeds — verified correct
- **libpcap**: 43,564 resolving + 69,198 blocking seeds — verified correct (2026-04-02)
- **bloaty**: NOT YET — previous run timed out, needs re-run with --max-seeds 10
- **sqlite3**: NOT YET — previous run timed out, needs re-run with --max-seeds 10

### Verification results (libpcap, 2026-04-02)
- 2/2 seeds verified: hit exactly the claimed branch side in Docker
- 6/6 lineage depths verified: DB chain matches raw .metadata files (ancestor IDs + mutation ops)
- Previous lcms/mbedtls verification (2026-04-01): 6/6 seeds, 10/10 lineage chains correct

## Performance History

### Old approach (per-seed scanning)
Each seed → separate `FUZZ_BIN` run → separate `llvm-profdata merge` → separate `llvm-cov show`. For libpcap (9K seeds), crashed with parse error before completing. For bloaty (47K seeds), timed out at 4h with zero output.

### New approach (10-bucket batch bisection, 2026-04-02)
Seeds batched through `FUZZ_BIN` (many per invocation), one `llvm-cov show` per bucket (all files at once = ~352ms for bloaty). 10-bucket recursive bisection to find individual hitting seeds.

| Target | Queues | Total Seeds | Time | Status |
|--------|--------|-------------|------|--------|
| lcms | 12 | ~10K | ~11 min | Done (old approach) |
| mbedtls | 12 | small | ~8 min | Done (old approach) |
| libpcap | 12 | ~31K | **46 min** | Done (new approach) |
| bloaty | 12 | ~291K | TBD | Needs re-run (--max-seeds 10) |
| sqlite3 | 12 | ~1.23M | TBD | Needs re-run (--max-seeds 10) |

### Why libpcap still took 46 min
The bottleneck is `llvm-cov show` calls during bisection. naive/trial1 (9,333 seeds, 636 branches, max_seeds=50) needed ~2,800 llvm-cov calls = 984s for one queue. With `--max-seeds 10`, branches complete faster → fewer recursion levels → fewer llvm-cov calls.

## Bug Fixes (2026-04-02)

- **`_parse_count` fix**: llvm-cov-18 emits truncated scientific notation like `18.4E`. Fixed in both `extract_blockers_ts.py` and `bisect_in_container.py` by stripping trailing `E`/`e` before parsing.

## Design Decisions

- **One trial per fuzzer**: Pick MIN(trial) where hit_status=1 (resolving) or 0 (blocking). Same fuzzer across trials uses same mutation strategy, so one trial is representative.
- **max_seeds is per (branch, queue)**: A branch with 3 resolving queues and max_seeds=10 gets up to 30 resolving seeds total. For branch clustering, --max-seeds 10 is sufficient.
- **Resolving + blocking seeds**: Two separate table pairs. Resolving seeds = hit blocked side in resolving fuzzer. Blocking seeds = hit other side in blocking fuzzer. Comparing them reveals what the blocking fuzzer is doing wrong.
- **10-bucket bisection**: Splits seeds into 10 buckets, batches each through FUZZ_BIN, one llvm-cov per bucket. Recurses into hit buckets. At ≤10 seeds, tests individually. Early-stops branches at max_seeds.

## Files

- `tools/seed_bisect.py` — host-side orchestrator
- `docker/bisect_in_container.py` — in-container 10-bucket batch bisection
- `tools/blocker_db.py` — DB CLI with seed tables
- `docker/Dockerfile.coverage-base` — base Docker image (copies bisect_in_container.py)
- `docker/targets/Dockerfile.{target}.cov` — per-target images
