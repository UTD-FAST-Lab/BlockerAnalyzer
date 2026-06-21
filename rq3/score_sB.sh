#!/usr/bin/env bash
# score_sB.sh — bring the sB targets (bloaty/lcms/libpng/libxml2) into the RQ3
# resolve+score, using their branch COORDINATES exported from the OTHER server.
#
# PREREQ — on the OTHER (sB) server, export the coordinate rows:
#   sqlite3 db/blockers.sqlite -header -csv \
#     "SELECT branch_id,target,file,function,line,col,blocked_side,source_line
#        FROM branches WHERE target IN ('bloaty','lcms','libpng','libxml2');" \
#     > sB_branches.csv
#   # then scp sB_branches.csv to THIS server's repo root.
#
# Usage:  bash rq3/score_sB.sh /path/to/sB_branches.csv
set -euo pipefail
cd "$(dirname "$0")/.."
CSV="${1:?usage: score_sB.sh <sB_branches.csv>}"
SBDB=db/blockers_sB.sqlite

echo "==> 1. build $SBDB from $CSV (preserving original branch_id)"
rm -f "$SBDB"
python3 - "$CSV" "$SBDB" <<'PY'
import csv, sqlite3, sys
csv_path, db = sys.argv[1], sys.argv[2]
con = sqlite3.connect(db)
con.execute("""CREATE TABLE branches(
  branch_id INTEGER PRIMARY KEY, target TEXT, file TEXT, function TEXT,
  line INTEGER, col INTEGER, blocked_side TEXT, source_line TEXT)""")
n=0
with open(csv_path) as f:
    for r in csv.DictReader(f):
        con.execute("INSERT OR IGNORE INTO branches VALUES (?,?,?,?,?,?,?,?)",
            (r['branch_id'], r['target'], r['file'], r.get('function',''),
             r['line'], r['col'], r['blocked_side'], r.get('source_line','')))
        n+=1
con.commit()
for t,c in con.execute("SELECT target,COUNT(*) FROM branches GROUP BY target"):
    print(f"   {t}: {c}")
print(f"   inserted {n} rows")
PY

echo "==> 2. measure sB targets against their own DB"
python3 tools/bench_score.py measure --db "$SBDB" \
    --ts-base out/rq3/coverage_ts \
    --targets bloaty lcms libpng libxml2 \
    --out csvs/rq3_resolve_sB.csv

echo "==> 2b. SANITY: how many sB branches actually mapped (n_reached>0)?"
python3 - <<'PY'
import csv, collections
reached=collections.Counter(); tot=collections.Counter()
for r in csv.DictReader(open('csvs/rq3_resolve_sB.csv')):
    tot[r['target']]+=1
    if int(r['n_reached'])>0: reached[r['target']]+=1
if not tot:
    print("   !! 0 rows — coordinates did NOT map. The sB cov binaries here likely")
    print("      differ from the build the other server extracted coords from.")
    print("      Fallback: ship coverage_ts for sB targets to the other server and")
    print("      run measure there against its own DB.")
for t in sorted(tot):
    print(f"   {t}: {reached[t]}/{tot[t]} (fuzzer,branch) rows reached")
PY

echo "==> 3. merge s4 + sB components -> canonical csvs/rq3_resolve.csv (idempotent)"
# Merge the immutable per-server COMPONENTS (not the canonical file) so re-running
# never double-counts sB.
{ cat csvs/rq3_resolve_s4.csv; tail -n +2 csvs/rq3_resolve_sB.csv; } > csvs/rq3_resolve.csv
echo "   wrote csvs/rq3_resolve.csv ($(($(wc -l < csvs/rq3_resolve.csv)-1)) rows, 8 targets)"

echo "==> 4. score over all 8 targets (final-19 taxonomy) -> canonical csvs/rq3_score.csv"
python3 tools/bench_score.py score --resolve csvs/rq3_resolve.csv --out csvs/rq3_score.csv

echo "==> 5. regenerate figures off the full resolve set"
python3 rq3/plot_heatmapA_pub.py
python3 rq3/rank_decomposition.py
echo "DONE. Canonical full score: csvs/rq3_score.csv"
