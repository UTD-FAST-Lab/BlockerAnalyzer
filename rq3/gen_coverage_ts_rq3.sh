#!/usr/bin/env bash
# gen_coverage_ts_rq3.sh — generate branch-coverage timeseries for every
# (target, fuzzer, trial) in the RQ3 cross-engine campaign, in parallel.
#
# Output: out/rq3/coverage_ts/<target>/<fuzzer>/trial<N>/coverage_timeseries.csv
#
# The RQ3 fuzzing campaign may still be running (cpuset 4..63). Keep JOBS modest
# and bound each replay container to CELL_CPUS cores so we don't starve it.
set -euo pipefail

TARGETS=(${RQ3_TARGETS:-curl harfbuzz openthread})
FUZZERS=(${RQ3_FUZZERS:-aflplusplus honggfuzz libfuzzer libafl})
TRIALS="${RQ3_TRIALS:-10}"
INTERVAL="${RQ3_INTERVAL:-60}"
JOBS="${JOBS:-12}"
export CELL_CPUS="${CELL_CPUS:-2}"

HERE="$(cd "$(dirname "$0")" && pwd)"
WORKER="${HERE}/cov_ts_worker_rq3.sh"

list=$(mktemp)
for target in "${TARGETS[@]}"; do
    for fuzzer in "${FUZZERS[@]}"; do
        for trial in $(seq 1 "$TRIALS"); do
            echo "$target $fuzzer $trial $INTERVAL"
        done
    done
done > "$list"

total=$(wc -l < "$list")
echo "==> $total jobs, ${JOBS}-way parallel, interval=${INTERVAL}min, ${CELL_CPUS} cpu/cell"
echo "==> targets: ${TARGETS[*]}  fuzzers: ${FUZZERS[*]}"
xargs -P "$JOBS" -L1 -a "$list" "$WORKER" 2>&1 \
    | awk '{print; fflush()}' \
    || true
rm -f "$list"
echo "==> all jobs dispatched"
