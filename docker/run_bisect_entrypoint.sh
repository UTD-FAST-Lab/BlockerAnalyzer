#!/bin/bash
# run_bisect_entrypoint.sh — Run a bucket of seeds and produce branch coverage.
#
# Usage (inside container):
#   /run_bisect.sh /corpus /cov_out [SOURCE_FILE]
#
# Env:
#   FUZZ_BIN — path to the coverage-instrumented binary
#   BATCH_SIZE — seeds per llvm-profdata invocation (default 500)
#
# Output:
#   /cov_out/branch_coverage_show.txt — llvm-cov show with branch counts
#   Exit 0 on success, 1 on no inputs.

set -euo pipefail

CORPUS_DIR="${1:-/corpus}"
OUT_DIR="${2:-/cov_out}"
SOURCE_FILE="${3:-}"
BATCH_SIZE="${BATCH_SIZE:-500}"

mkdir -p "${OUT_DIR}/profraw"

# Collect all non-hidden corpus files
files=()
for f in "${CORPUS_DIR}"/*; do
    [ -f "$f" ] || continue
    [[ "$(basename "$f")" == .* ]] && continue
    files+=("$f")
done

count=${#files[@]}

if [ "$count" -eq 0 ]; then
    echo "NO_INPUTS" > "${OUT_DIR}/status"
    exit 1
fi

echo "Processing $count inputs (batch size ${BATCH_SIZE})..." >&2

# Run in batches to avoid ARG_MAX limits
batch=0
i=0
while [ "$i" -lt "$count" ]; do
    batch_files=("${files[@]:$i:$BATCH_SIZE}")
    export LLVM_PROFILE_FILE="${OUT_DIR}/profraw/${batch}.profraw"
    timeout 30 "${FUZZ_BIN}" "${batch_files[@]}" >/dev/null 2>&1 || true
    i=$((i + BATCH_SIZE))
    batch=$((batch + 1))
done

echo "Ran $batch batches, merging profiles..." >&2

llvm-profdata-18 merge -sparse "${OUT_DIR}/profraw"/*.profraw \
    -o "${OUT_DIR}/merged.profdata"

# If SOURCE_FILE is specified, only show that file's coverage (much smaller output)
if [ -n "${SOURCE_FILE}" ]; then
    llvm-cov-18 show "${FUZZ_BIN}" \
        -instr-profile="${OUT_DIR}/merged.profdata" \
        -show-branches=count \
        -show-line-counts \
        -format=text \
        "${SOURCE_FILE}" \
        > "${OUT_DIR}/branch_coverage_show.txt"
else
    llvm-cov-18 show "${FUZZ_BIN}" \
        -instr-profile="${OUT_DIR}/merged.profdata" \
        -show-branches=count \
        -show-line-counts \
        -format=text \
        > "${OUT_DIR}/branch_coverage_show.txt"
fi

echo "OK" > "${OUT_DIR}/status"
echo "Done. Output: ${OUT_DIR}/branch_coverage_show.txt" >&2
