#!/usr/bin/env bash
# finish_measure_chain.sh — wait for bloaty cov-replay to finish, then run the
# RQ3 measurement chain over all 8 targets: bench_score measure → score →
# regenerate the 2×4 coverage plot. Ad-hoc driver (2026-06-21).
set -uo pipefail
cd "$(dirname "$0")/.."

log() { echo "[$(date '+%F %T')] $*"; }

# 1. Wait until bloaty has 10/10 cov-ts CSVs for all 4 fuzzers (or gen proc dies).
log "waiting for bloaty cov-ts to complete..."
while true; do
    done=0
    for f in aflplusplus honggfuzz libfuzzer libafl; do
        n=$(ls out/rq3/coverage_ts/bloaty/$f/trial*/coverage_timeseries.csv 2>/dev/null | wc -l)
        done=$((done + n))
    done
    if [ "$done" -ge 40 ]; then
        log "bloaty cov-ts complete ($done/40)"
        break
    fi
    if ! pgrep -f gen_coverage_ts_rq3 >/dev/null; then
        log "gen_coverage proc gone but only $done/40 bloaty CSVs — proceeding anyway"
        break
    fi
    sleep 60
done

# 2. measure (targets present in db/blockers.sqlite = s4) → s4 component
log "running bench_score measure (s4 targets)..."
python3 tools/bench_score.py measure --ts-base out/rq3/coverage_ts \
    --out csvs/rq3_resolve_s4.csv 2>&1
# canonical resolve = s4 until sB is merged in by rq3/score_sB.sh
cp csvs/rq3_resolve_s4.csv csvs/rq3_resolve.csv
log "measure done"

# 3. score → csvs/rq3_score.csv (canonical; final-19 taxonomy)
log "running bench_score score..."
python3 tools/bench_score.py score --resolve csvs/rq3_resolve.csv \
    --out csvs/rq3_score.csv 2>&1
log "score done"

# 4. regenerate final 2×4 plots (all 8 targets) — both mean and median
for metric in mean median; do
    log "regenerating 2×4 coverage plot (${metric})..."
    mkdir -p out/rq3/coverage_plots
    python3 rq3/plot_rq3_coverage.py \
        --targets curl harfbuzz openthread sqlite3 lcms libxml2 libpng bloaty \
        --cols 4 --metric "$metric" \
        --output "out/rq3/coverage_plots/rq3_coverage_curves_2x4_${metric}.png" 2>&1
done
log "ALL DONE"
