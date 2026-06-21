#!/usr/bin/env bash
# cov_ts_worker_rq3.sh — compute a single (target, fuzzer, trial) coverage
# timeseries for the RQ3 cross-engine campaign.
#
# Reuses LibAFL_Experiments' fuzzer-agnostic replay entrypoint
# (run_coverage_timeseries_csvonly.py — mtime-based, works for every corpus
# format) but maps each FuzzBench fuzzer's corpus layout and writes into the
# RQ3 coverage_ts tree.
#
# Usage: cov_ts_worker_rq3.sh <target> <fuzzer> <trial> <interval_min>
# Resume-friendly: skips if the output CSV + show sentinel already exist.
set -euo pipefail

target="$1"; fuzzer="$2"; trial="$3"; interval="${4:-60}"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RQ3_DIR="${REPO_ROOT}/out/rq3"
ENTRYPOINT="/home/miao/work/LibAFL_Experiments/docker/run_coverage_timeseries_csvonly.py"

# Per-fuzzer corpus layout (see rq3/README.md "Per-fuzzer output corpus layout").
case "$fuzzer" in
    aflplusplus) sub="default/queue" ;;
    honggfuzz)   sub="corpus" ;;
    libfuzzer)   sub="corpus" ;;
    libafl)      sub="queue" ;;
    *) echo "FAIL  unknown fuzzer ${fuzzer}"; exit 1 ;;
esac

trial_dir="${RQ3_DIR}/${target}/${fuzzer}/trial${trial}"
corpus="${trial_dir}/${sub}"
out_dir="${RQ3_DIR}/coverage_ts/${target}/${fuzzer}/trial${trial}"
csv="${out_dir}/coverage_timeseries.csv"

# NB: aflplusplus's default/ is root-owned 0700, so the host user can't stat
# default/queue — gate on the trial dir (readable) and let the docker container
# (uid 0) read the corpus; a genuinely-absent corpus makes the entrypoint exit 1.
if [ ! -d "$trial_dir" ]; then
    echo "SKIP  ${target}/${fuzzer}/t${trial}: no trial dir"
    exit 0
fi
if [ -s "$csv" ] && [ "$(wc -l < "$csv")" -gt 1 ] && [ -f "${out_dir}/show_reports/.done" ]; then
    echo "DONE  ${target}/${fuzzer}/t${trial}: csv+show exist"
    exit 0
fi

mkdir -p "$out_dir"
start=$(date +%s)
if docker run --rm \
    --cpus "${CELL_CPUS:-1}" \
    -v "${corpus}:/corpus:ro" \
    -v "${out_dir}:/cov_out" \
    -v "${ENTRYPOINT}:/run_coverage_timeseries.py:ro" \
    --entrypoint python3 \
    "libafl-${target}-cov" \
    /run_coverage_timeseries.py /corpus /cov_out "$interval" \
    > "${out_dir}/replay.log" 2>&1; then
    n=$(($(wc -l < "$csv") - 1))
    echo "OK    ${target}/${fuzzer}/t${trial}: ${n} points ($(( $(date +%s) - start ))s)"
else
    echo "FAIL  ${target}/${fuzzer}/t${trial}: see ${out_dir}/replay.log"
fi
