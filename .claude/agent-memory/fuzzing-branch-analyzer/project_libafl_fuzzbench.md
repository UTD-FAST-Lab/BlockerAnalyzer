---
name: LibAFL FuzzBench blocker patterns
description: Confirmed blocker counts and dataset layout for 5 LibAFL FuzzBench targets analyzed 2026-03-31
type: project
---

LibAFL FuzzBench analysis completed 2026-03-31 with 4 fuzzers (naive, cmplog, value_profile, value_profile_cmplog) x 3 trials each, 5 targets.

Confirmed blocker counts:
- bloaty:   70 confirmed blockers  (31,645 branches per file; 12 files × ~455k lines each)
- lcms:    252 confirmed blockers  (3,708 branches; relatively small target)
- libpcap: 293 confirmed blockers  (branch counts vary slightly across trials: 3,392–3,421)
- mbedtls:  10 confirmed blockers  (7,241 branches; very low — fuzzers converge well, high branch agreement)
- sqlite3: 227 confirmed blockers  (13,494 branches)

Data layout:
- Coverage files: `/home/miao/libafl_fuzzbench/out/coverage/<target>/<fuzzer>/trial{1,2,3}/branch_coverage_show.txt`
- Trials numbered trial1, trial2, trial3 (NOT trial0)
- Output reports: `/home/miao/BlockerAnalyzer/blockers/<target>_blockers.md`

Notable observations:
- libpcap trial branch counts vary slightly across fuzzers/trials (3,392–3,421), likely due to conditional compilation or minor instrumentation differences; the tool handles this gracefully by unioning all seen branches.
- mbedtls is a conspicuous outlier (10 vs 70–293 for others) — all 4 fuzzers achieve near-identical coverage, suggesting the target's branches are well-explored or structurally constrained.
- bloaty has by far the largest coverage files (~455k lines, 31,645 branches) but yielded only 70 confirmed blockers, implying most asymmetric branches are fuzzer-consistent (same side unreachable across all 4 fuzzers).

**Why:** First LibAFL FuzzBench dataset processed in this project — establishes baseline blocker counts for cross-fuzzer comparison.
**How to apply:** Use these counts to calibrate expectations when comparing naive vs. cmplog vs. value_profile strategies on these targets.
