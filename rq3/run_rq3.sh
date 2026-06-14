#!/usr/bin/env bash
# run_rq3.sh — RQ3 cross-engine fuzzer evaluation launcher.
#
# 4 fuzzers × 8 targets × 10 trials × 24 h, 60-way parallel, priority queue by
# target order. Adapted from LibAFL_Experiments/docker/run_icse2027.sh.
#
# Phase 1: build any missing rq3-<target>-<fuzzer> images (parallel, BUILD_PAR).
# Phase 2: run 320 fuzzing trials; freed slot → next pending (target,fuzzer,trial).
#
# Output: ./out/rq3/<target>/<fuzzer>/trial<N>/      (out -> /data2/miao/icse27)
# Logs:   ./out/rq3/_logs/
#
# Seeds are baked into each image's /seeds at build time (the SAME seeds as the
# prior LibAFL campaign — reproduced verbatim from the target Dockerfiles).
#
# Run inside tmux:  tmux new -s rq3 ; ./rq3/run_rq3.sh
# Resume: just re-run — built images + non-empty trial corpora are skipped.

set -euo pipefail

# ── configuration ───────────────────────────────────────────────────────────
FUZZERS=(aflplusplus honggfuzz libfuzzer libafl)
TARGETS=(curl harfbuzz openthread sqlite3 lcms libxml2 libpng bloaty)
TRIALS=10
DURATION=86400                          # 24h per trial
PARALLEL=60                             # concurrent containers
BUILD_PAR=4                             # concurrent docker builds
CPU_BASE=4                              # cores CPU_BASE..CPU_BASE+PARALLEL-1 (4..63)
MEM_PER_JOB=4g

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"          # BlockerAnalyzer
RQ3_DIR="${REPO_ROOT}/rq3"
FUZZBENCH="/home/miao/work/fuzzbench"                  # build context for the 3 FuzzBench fuzzers (COPY fuzzers)
LIBAFL_EXP="/home/miao/work/LibAFL_Experiments"        # proven libafl (generic) build
RESULTS_DIR="${REPO_ROOT}/out/rq3"                     # -> /data2/miao/icse27/rq3
LOG_DIR="${RESULTS_DIR}/_logs"
mkdir -p "$LOG_DIR"

ORCH_LOG="${LOG_DIR}/orchestrator.log"
exec > >(tee -a "$ORCH_LOG") 2>&1
LOG()  { printf '[%(%F %T)T] %s\n' -1 "$*"; }
LOGE() { printf '[%(%F %T)T] [ERR] %s\n' -1 "$*" >&2; }

LOG "==== RQ3 campaign start ===="
LOG "fuzzers: ${FUZZERS[*]}"
LOG "targets: ${TARGETS[*]}"
LOG "trials=${TRIALS} duration=${DURATION}s parallel=${PARALLEL} cpu_base=${CPU_BASE} out=${RESULTS_DIR}"
cd "$REPO_ROOT"

# ── phase 1: build rq3-<target>-<fuzzer> images (skip already-built) ─────────
# Each rq3/Dockerfile.<target> reproduces the LibAFL_Experiments target build +
# the SAME baked seed, with the toolchain swapped to FUZZER's FuzzBench toolchain.
build_one() {
    local target="$1" fuzzer="$2"
    local image="rq3-${target}-${fuzzer}"
    local log="${LOG_DIR}/build-${target}-${fuzzer}.log"
    if docker image inspect "$image" >/dev/null 2>&1; then LOG "skip build ${image} (cached)"; return 0; fi
    LOG "build ${image}"
    local rc
    if [ "$fuzzer" = "libafl" ]; then
        # libafl = the PROVEN LibAFL `generic` build (LibAFL_Experiments toolchain;
        # FuzzBench's fuzzers/libafl is bitrotted — see rq3/toolchain/Dockerfile.libafl).
        docker build --build-arg FUZZER=generic \
            -f "${LIBAFL_EXP}/docker/targets/Dockerfile.${target}" -t "$image" "$LIBAFL_EXP" >"$log" 2>&1; rc=$?
    else
        # aflplusplus/honggfuzz/libfuzzer: our FuzzBench-toolchain marriage; context =
        # fuzzbench so the Dockerfile's `COPY fuzzers` resolves.
        docker build --build-arg FUZZER="$fuzzer" \
            -f "${RQ3_DIR}/Dockerfile.${target}" -t "$image" "$FUZZBENCH" >"$log" 2>&1; rc=$?
    fi
    if [ $rc -eq 0 ]; then LOG "ok    ${image}"; else LOGE "FAIL  ${image} (see ${log})"; return 1; fi
}
export -f build_one LOG LOGE
export LOG_DIR RQ3_DIR FUZZBENCH LIBAFL_EXP

LOG "Phase 1: building images (parallel=${BUILD_PAR})"
build_queue="${LOG_DIR}/build_queue.tsv"; : > "$build_queue"
for target in "${TARGETS[@]}"; do for fuzzer in "${FUZZERS[@]}"; do
    printf '%s\t%s\n' "$target" "$fuzzer" >> "$build_queue"
done; done
parallel --colsep '\t' -j "$BUILD_PAR" --joblog "${LOG_DIR}/build_joblog.tsv" \
    build_one {1} {2} :::: "$build_queue" \
    || LOG "Some builds failed; their trials are skipped (see build-*.log)."
LOG "Phase 1 complete."
# BUILD_ONLY=1 (env) or --build-only (arg) stops here — build the 32 images without
# launching the 6-day 320-trial run (which should be started in tmux separately).
if [ -n "${BUILD_ONLY:-}" ] || [[ " $* " == *" --build-only "* ]]; then
    LOG "BUILD_ONLY set — images built; skipping the 320-trial run phase."
    for target in "${TARGETS[@]}"; do for fuzzer in "${FUZZERS[@]}"; do
        docker image inspect "rq3-${target}-${fuzzer}" >/dev/null 2>&1 && echo "  OK   rq3-${target}-${fuzzer}" || echo "  MISS rq3-${target}-${fuzzer}"
    done; done
    exit 0
fi

# ── phase 2: run trials ─────────────────────────────────────────────────────
run_one() {
    local target="$1" fuzzer="$2" trial="$3" slot="$4"
    local image="rq3-${target}-${fuzzer}"
    local name="rq3-${target}-${fuzzer}-t${trial}"
    local corpus="${RESULTS_DIR}/${target}/${fuzzer}/trial${trial}"
    local cpu=$((CPU_BASE + slot - 1))
    local rlog="${LOG_DIR}/${target}-${fuzzer}-t${trial}.log"

    if ! docker image inspect "$image" >/dev/null 2>&1; then LOGE "skip-no-image ${name}"; return 0; fi
    if [[ -d "$corpus" ]] && [[ -n "$(ls -A "$corpus" 2>/dev/null)" ]]; then LOG "skip-done ${name}"; return 0; fi
    mkdir -p "$corpus"
    docker rm -f "$name" >/dev/null 2>&1 || true
    LOG "START ${name} slot=${slot} cpu=${cpu}"
    docker run --rm --name "$name" --cpuset-cpus "$cpu" --memory "$MEM_PER_JOB" \
        -v "${corpus}:/corpus" -e DURATION="$DURATION" "$image" >"$rlog" 2>&1 \
        && LOG "DONE ${name}" || LOGE "FAIL ${name} (see ${rlog})"
    return 0
}
export -f run_one
export RESULTS_DIR LOG_DIR DURATION MEM_PER_JOB CPU_BASE

job_queue="${LOG_DIR}/job_queue.tsv"; : > "$job_queue"
for target in "${TARGETS[@]}"; do for fuzzer in "${FUZZERS[@]}"; do
    for trial in $(seq 1 "$TRIALS"); do printf '%s\t%s\t%s\n' "$target" "$fuzzer" "$trial" >> "$job_queue"; done
done; done
LOG "Phase 2: queued $(wc -l < "$job_queue") trials"
parallel --colsep '\t' -j "$PARALLEL" --joblog "${LOG_DIR}/run_joblog.tsv" --resume-failed \
    run_one {1} {2} {3} '{%}' :::: "$job_queue" \
    || LOG "parallel exited non-zero — check ${LOG_DIR}/run_joblog.tsv"
LOG "==== RQ3 campaign complete ===="
