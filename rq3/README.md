# RQ3 — cross-engine fuzzer evaluation on the mechanism-labeled benchmark

**Goal:** run 4 *whole* fuzzers on the benchmark's targets, measure their
resolve-rate **per mechanism class** (RQ2's labels), and test whether the
mechanism labels generalize across fuzzer engines.

## Configuration (locked 2026-06-14)

| | |
|---|---|
| Fuzzers | `aflplusplus`, `honggfuzz`, `libfuzzer`, `libafl` (FuzzBench integrations under `/home/miao/work/fuzzbench/fuzzers/<f>`) |
| Targets | the 8 labeled: `curl harfbuzz openthread sqlite3 lcms libxml2 libpng bloaty` |
| Trials | 10 |
| Duration | 24 h (86400 s) per trial |
| Parallelism | 60 cores (cpuset `4..63`) |
| Output | `./out/rq3/<target>/<fuzzer>/trial<N>/` (out → /data2/miao/icse27) |
| Total | 4 × 8 × 10 = **320 trial-runs**; ~6 waves × 24h ≈ **6 days** wall-clock |

## Design — the toolchain marriage

Two halves must be combined:

1. **Target build + SEEDS** come from `/home/miao/work/LibAFL_Experiments/docker/targets/Dockerfile.<target>`
   — the *exact* source commits, harness, and **the same baked `/seeds`** the
   prior LibAFL campaign used (e.g. curl deliberately bakes a SINGLE seed
   "to isolate fuzzer capability from corpus richness"). We must reproduce each
   target's seed recipe verbatim — the prior experiment's seeds are NOT a host
   mount, they are baked at build time.
2. **Compiler toolchain + run command** come from each FuzzBench fuzzer
   (`fuzzbench/fuzzers/<f>/builder.Dockerfile` + `fuzzer.py`):
   - build via the OSS-Fuzz model the LibAFL target Dockerfiles already use
     (`$CC/$CXX/$CFLAGS/$LIB_FUZZING_ENGINE/$OUT`), but with the **fuzzer's**
     toolchain instead of the LibAFL `<fuzzer>_cc` wrappers + `--libafl`.
   - run via the fuzzer's `fuzz()`:
     - `aflplusplus`: needs a **cmplog** build dir + uninstrumented build; AFL run.
     - `libfuzzer`: `<bin> -o <out> -i <in>` (libFuzzer args).
     - `libafl`: `<bin> -o <out> -i <in>` (+ jemalloc LD_PRELOAD).
     - `honggfuzz`: `./honggfuzz --persistent --input <in> --output <out>/corpus --crashdir ...`.

So each `rq3/Dockerfile.<target>` is the LibAFL target build recipe with the
toolchain swapped to a FuzzBench fuzzer (selected by `--build-arg FUZZER`), the
same seed baked, and the fuzzer's run command as `CMD`.

## Measurement (reuses the existing pipeline — branch IDs MUST align)

RQ3 fuzzers are measured with **our** coverage binaries, NOT FuzzBench's coverage
(whose branch IDs wouldn't match the benchmark):

```
out/rq3/<t>/<f>/trial<N>/corpus  --replay-->  libafl-<t>-cov  -->  branch_coverage_show.txt
   -> study_units add-canonical (new fuzzer arm) -> subject_branches
   -> bench_score: resolve-rate per mechanism class
```

`LibAFL_Experiments/docker/run_coverage_timeseries.sh --fuzzers "aflplusplus honggfuzz libfuzzer libafl"`
is the replay step (already corpus-format-agnostic; point it at each fuzzer's
corpus dir).

## Build order

1. **Prereq: FuzzBench base images** — `base-image`, `base-builder`, `base-runner`
   (none present locally). Build via FuzzBench `make` (docker/base-*/Dockerfile)
   or pull from gcr.io.
2. **Fuzzer toolchain images** — build each `fuzzbench/fuzzers/<f>/builder.Dockerfile`
   (parent = base-builder) → toolchain image per fuzzer.
3. **rq3 target images** — `rq3/Dockerfile.<target>` × 8, `--build-arg FUZZER=<f>` × 4 = 32.
4. **Run** — `rq3/run_rq3.sh` (build-skip + 320-trial scheduler, 60-way).
5. **Measure** — cov-replay → study_units arms → `bench_score`.

## Toolchain build (per fuzzer, ONCE) — pin the base-builder digest

```bash
docker build --build-arg parent_image=gcr.io/oss-fuzz-base/base-builder@sha256:87ca1e9e19235e731fac8de8d1892ebe8d55caf18e7aa131346fc582a2034fdd \
  -t rq3-toolchain-<FUZZER> -f /home/miao/work/fuzzbench/fuzzers/<FUZZER>/builder.Dockerfile \
  /home/miao/work/fuzzbench/fuzzers/<FUZZER>
```
**MUST pin the digest** — `base-builder:latest` builds AFL++ *without LLVM mode*
("LLVM mode is not available") and the target build aborts. Pin = the digest
FuzzBench's benchmark Dockerfiles use.

Per-fuzzer `FUZZER_LIB` (the engine the target links; set in `rq3/Dockerfile.<target>`):
`aflplusplus` = `/libAFLDriver.a`; the others read from their builder.Dockerfile
(libfuzzer = libFuzzer compile flag, honggfuzz = libhfuzz, libafl = its harness lib).

Per-fuzzer output corpus layout (the measurement step must point cov-replay here):
`aflplusplus` = `<trial>/default/queue/`; `libfuzzer`/`libafl` = flat `<trial>/`;
`honggfuzz` = `<trial>/corpus/`.

## Status

- [x] Config + design locked
- [x] `rq3/run_rq3.sh` driver (build + 60-way run scheduler, out/rq3)
- [x] FuzzBench base images (pulled `base-image` + pinned `base-builder`)
- [x] `rq3-toolchain-aflplusplus` built (pinned base-builder)
- [x] `rq3/Dockerfile.curl` + **PILOT `aflplusplus × curl` VALIDATED end-to-end**
      (build → 180 s run = 1263 corpus → replay through `libafl-curl-cov` = 7.21% branch cov)
- [x] Toolchains: aflplusplus, honggfuzz, libfuzzer (our `rq3/toolchain/`, pinned base-builder);
      libafl = `libafl-base` (LibAFL_Experiments `generic`).
- [x] **ALL 4 FUZZERS VALIDATED end-to-end (curl):** build → 180 s run → replay through
      `libafl-curl-cov`. Corpus from 1 seed: afl 1263 / honggfuzz 1422 / libfuzzer 767 /
      libafl 5460 files; ~60 curl lib files covered each. All chains proven.
- [x] **libafl resolved by NOT using FuzzBench's bitrotted fuzzers/libafl.** Its pin
      f856092f is dep-drifted (stale Cargo.lock; fresh deps need Rust 1.88+; the nightly
      that compiles it (1.98) SIGABRTs at runtime). Instead libafl = the PROVEN
      `generic` variant from LibAFL_Experiments (`libafl-base` toolchain, same engine
      family + same seed as RQ1/2). Built via `LibAFL_Experiments/docker/targets/
      Dockerfile.<target>` FUZZER=generic; `run_rq3.sh` build_one special-cases it.
- [x] **`rq3/Dockerfile.<target>` for all 8 targets** (curl, harfbuzz, openthread, sqlite3,
      lcms, libxml2, libpng, bloaty) — each VALIDATED for aflplusplus (build → 90 s run grows
      the corpus; openthread also cov-replayed). Pattern: FuzzBench benchmark deps+clone @ the
      pinned commit (== LibAFL_Experiments) + FuzzBench's per-benchmark build.sh + fuzzer.build()
      run from the SOURCE WORKDIR (cwd-sensitive) + the LibAFL single seed + fuzzer.fuzz() runner.
      Per-target fixes baked into build.sh: libxml2 `--without-threads`, libpng `-pthread -ldl`
      (afl static libc++ needs pthread; FuzzBench build.sh omits it). libafl reuses
      LibAFL_Experiments' 8 target Dockerfiles (FUZZER=generic) as-is.
- [x] **Verified fuzzer-agnostic** — spot-checked honggfuzz + libfuzzer on libxml2 (pthread)
      and bloaty (cmake): all 4 build + run (corpus 6293/3764/796/300). The 8 Dockerfiles work
      for all 3 FuzzBench fuzzers via `--build-arg FUZZER`.
- [x] **Full build DONE — all 32 images built** (`BUILD_ONLY=1 ./rq3/run_rq3.sh`).
- [ ] **Launch 320 trials** — `tmux new -s rq3; ./rq3/run_rq3.sh` (skips the 32 cached images,
      then runs phase 2 60-way, ~6 days). **← user launches in tmux.**
- [x] **`tools/bench_score.py` written + validated** (score logic on synthetic data). Flow:
      1. `LibAFL_Experiments/docker/run_coverage_timeseries.py` (or run_icse2027's cov workers)
         replay `out/rq3/<t>/<f>/trial<N>/` corpora through `libafl-<t>-cov` → an RQ3
         `coverage_ts` tree.
      2. `python3 tools/bench_score.py measure --ts-base <that tree>` → `csvs/rq3_resolve.csv`
         (per-branch n_resolved/n_blocked, via the SAME `study_units.walk_target_state` hit_status
         the benchmark used).
      3. `python3 tools/bench_score.py score` → per (fuzzer × mechanism class) resolve-rate matrix
         (`resolved_frac >= 0.8`), overall row, coverage/G3 footer, libafl-lineage caveat →
         `csvs/rq3_score.csv`. **This is the RQ3 result table.**
- [ ] Full build (32 images) + launch 320 trials (`rq3/run_rq3.sh`)
- [ ] Measurement: corpus → cov-replay → `study_units` arms → `bench_score.py` (per-mechanism resolve-rate)

**De-risk before the 6-day commit:** pilot ONE combo end-to-end
(build → 1 short run → replay through `libafl-curl-cov` → confirm it hits labeled
curl branches) before building all 32 / launching all 320.
