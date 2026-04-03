#!/bin/bash
# run_clustering.sh — End-to-end branch clustering for a target.
#
# Orchestrates T1 (claude agents) + T2 (Python tool) in a loop.
# State is saved to JSON after every step — safe to interrupt and resume.
#
# Usage:
#   bash tools/run_clustering.sh <target> [queue_base]
#
# Example:
#   bash tools/run_clustering.sh libpcap ./out

set -euo pipefail

TARGET="${1:?Usage: $0 <target> [queue_base]}"
QUEUE_BASE="${2:-./out}"
RUN_DATE=$(date +%Y-%m-%d)
STATE="clusters/${TARGET}_state.json"
LOG="clusters/${TARGET}_clustering.log"
T1_PARALLEL=10
T2_BATCH=20

cd /home/miao/BlockerAnalyzer

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }

# ============================================================
# Step 0: Initialize state if needed
# ============================================================
if [ ! -f "$STATE" ]; then
    log "=== Initializing state for $TARGET ==="
    python3 -c "
import json, sqlite3
from collections import defaultdict

conn = sqlite3.connect('db/blockers.sqlite')
conn.row_factory = sqlite3.Row
rows = conn.execute('''
    SELECT b.branch_id, b.file, b.function, b.line, b.col, b.blocked_side,
           dm.selection_tags, dm.prob_div, dm.dur_div, dm.hit_div,
           dm.blocking_fuzzers, dm.resolving_fuzzers, dm.unreached_fuzzers
    FROM branches b JOIN derived_metrics dm ON dm.branch_id=b.branch_id
    WHERE b.target = \"$TARGET\" AND dm.selection_tags != \"[]\"
    AND dm.blocking_fuzzers != \"[]\" AND dm.resolving_fuzzers != \"[]\"
''').fetchall()
conn.close()

state = {
    'target': '$TARGET',
    'run_date': '$RUN_DATE',
    'clusters': {},
    'skipped': [],
    'unfitted': [],
    'next_cluster_id': 1,
    'all_candidates': [r['branch_id'] for r in rows],
}
with open('$STATE', 'w') as f:
    json.dump(state, f, indent=2)
print(f'Initialized: {len(rows)} candidates')
"
fi

# ============================================================
# Main loop
# ============================================================
ROUND=0
while true; do
    ROUND=$((ROUND + 1))
    log "=========================================="
    log "Round $ROUND"

    # ----------------------------------------------------------
    # Select T1 representatives
    # ----------------------------------------------------------
    T1_REPS=$(python3 -c "
import json, sqlite3
from collections import defaultdict

with open('$STATE') as f:
    state = json.load(f)

conn = sqlite3.connect('db/blockers.sqlite')
conn.row_factory = sqlite3.Row

assigned = set()
for c in state['clusters'].values():
    for m in c['members']:
        assigned.add(m['branch_id'])
for s in state.get('skipped', []):
    assigned.add(s['branch_id'])

all_cands = state.get('all_candidates', [])
pool = [bid for bid in all_cands if bid not in assigned]

if not pool:
    print('DONE')
    exit(0)

# Get branch info
by_func = defaultdict(list)
for bid in pool:
    r = conn.execute('''
        SELECT b.branch_id, b.function, dm.selection_tags, dm.prob_div, dm.dur_div, dm.hit_div
        FROM branches b JOIN derived_metrics dm ON dm.branch_id=b.branch_id
        WHERE b.branch_id=?
    ''', (bid,)).fetchone()
    if r:
        by_func[r['function']].append(dict(r))

# Sort per function: more tags first
for func in by_func:
    by_func[func].sort(key=lambda c: (
        -len(json.loads(c['selection_tags'])),
        -(c['prob_div'] or 0), -(c['dur_div'] or 0), -(c['hit_div'] or 0),
    ))

n_funcs = len(by_func)
total = max(10, n_funcs)
total_branches = sum(len(v) for v in by_func.values())

reps = []
for func, branches in by_func.items():
    n = max(1, round(len(branches) / total_branches * total))
    reps.extend([b['branch_id'] for b in branches[:n]])

# Cap at pool size
reps = reps[:len(pool)]
print(' '.join(str(r) for r in reps))
conn.close()
")

    if [ "$T1_REPS" = "DONE" ]; then
        log "All branches processed!"
        break
    fi

    T1_ARRAY=($T1_REPS)
    log "T1: ${#T1_ARRAY[@]} representatives: ${T1_REPS}"

    # ----------------------------------------------------------
    # Pre-compute seed diffs
    # ----------------------------------------------------------
    log "Pre-computing seed diffs..."
    for BID in "${T1_ARRAY[@]}"; do
        python3 tools/seed_diff.py --target "$TARGET" --branch-id "$BID" \
            --queue-base "$QUEUE_BASE" > "/tmp/seed_diff_${TARGET}_${BID}.txt" 2>&1
    done

    # ----------------------------------------------------------
    # Run T1 agents in parallel batches
    # ----------------------------------------------------------
    NEW_CLUSTERS=0

    for ((i=0; i<${#T1_ARRAY[@]}; i+=T1_PARALLEL)); do
        BATCH=("${T1_ARRAY[@]:i:T1_PARALLEL}")
        log "T1 batch: ${BATCH[*]}"

        # Spawn claude agents in parallel
        PIDS=()
        for BID in "${BATCH[@]}"; do
            DIFF=$(head -30 "/tmp/seed_diff_${TARGET}_${BID}.txt" 2>/dev/null || echo "No diff")

            # Get branch info
            BRANCH_INFO=$(python3 -c "
import sqlite3, json
conn = sqlite3.connect('db/blockers.sqlite')
conn.row_factory = sqlite3.Row
b = conn.execute('SELECT file, function, line, col, blocked_side FROM branches WHERE branch_id=?', ($BID,)).fetchone()
dm = conn.execute('SELECT blocking_fuzzers, resolving_fuzzers FROM derived_metrics WHERE branch_id=?', ($BID,)).fetchone()
print(f'{b[\"function\"]}:{b[\"line\"]}:{b[\"col\"]} {b[\"blocked_side\"]} blk={dm[\"blocking_fuzzers\"]} res={dm[\"resolving_fuzzers\"]}')
conn.close()
")

            PROMPT="Analyze branch $BID for target $TARGET.

Branch: $BRANCH_INFO
Docker image: blocker-${TARGET}-cov. Queue base: $QUEUE_BASE. DB: db/blockers.sqlite.

PRE-COMPUTED SEED DIFF:
$DIFF

Run seed_diff yourself for full details: python3 tools/seed_diff.py --target $TARGET --branch-id $BID --queue-base $QUEUE_BASE

Focus on high-MI regions. Trace source in Docker. Formulate hypothesis. Verify with 1 Test A + 3-5 Test B (diverse fuzzers/trials). One Docker container, unique profraw per seed.

Print RESULT: JSON at the end:
{\"branch_id\": $BID, \"status\": \"confirmed\"|\"unresolved\"|\"skipped\", \"cluster_id\": \"NEW\", \"controlling_bytes\": \"...\", \"semantic_label\": \"...\", \"source_mapping\": \"...\", \"verification_rounds\": N, \"notes\": \"\"}"

            log "  Spawning agent for B${BID}..."
            claude --print -p "$PROMPT" > "/tmp/t1_result_${TARGET}_${BID}.txt" 2>&1 &
            PIDS+=($!)
        done

        # Wait for all agents in this batch
        log "  Waiting for ${#PIDS[@]} agents..."
        for PID in "${PIDS[@]}"; do
            wait "$PID" || true
        done

        # Parse results and update state
        for BID in "${BATCH[@]}"; do
            RESULT_LINE=$(grep "^RESULT:" "/tmp/t1_result_${TARGET}_${BID}.txt" 2>/dev/null | tail -1 || echo "")
            if [ -z "$RESULT_LINE" ]; then
                # Try to find RESULT: anywhere in the output
                RESULT_LINE=$(grep "RESULT:" "/tmp/t1_result_${TARGET}_${BID}.txt" 2>/dev/null | tail -1 || echo "")
            fi

            if [ -z "$RESULT_LINE" ]; then
                log "  B${BID}: NO RESULT (agent failed or timed out)"
                continue
            fi

            # Extract JSON after "RESULT:"
            RESULT_JSON=$(echo "$RESULT_LINE" | sed 's/.*RESULT:\s*//')

            log "  B${BID}: $(echo "$RESULT_JSON" | python3 -c 'import sys,json; d=json.loads(sys.stdin.read()); print(f"{d[\"status\"]} — {d.get(\"semantic_label\",\"\")[:60]}")' 2>/dev/null || echo "parse error")"

            # Update state
            python3 -c "
import json, sqlite3
conn = sqlite3.connect('db/blockers.sqlite')
conn.row_factory = sqlite3.Row

result = json.loads('''$RESULT_JSON''')
bid = result['branch_id']
status = result.get('status', 'error')

with open('$STATE') as f:
    state = json.load(f)

if status in ('confirmed', 'CONFIRMED'):
    b = conn.execute('SELECT file, line, col, blocked_side FROM branches WHERE branch_id=?', (bid,)).fetchone()
    dm = conn.execute('SELECT selection_tags, resolving_fuzzers, blocking_fuzzers FROM derived_metrics WHERE branch_id=?', (bid,)).fetchone()

    cid = result.get('cluster_id', 'NEW')
    if cid == 'NEW' or cid not in state['clusters']:
        cid = f'BC{state[\"next_cluster_id\"]:02d}'
        state['next_cluster_id'] += 1
        state['clusters'][cid] = {
            'controlling_bytes': result.get('controlling_bytes', ''),
            'semantic_label': result.get('semantic_label', ''),
            'source_mapping': result.get('source_mapping', ''),
            'representative': bid,
            'members': [],
        }
    state['clusters'][cid]['members'].append({
        'branch_id': bid,
        'file': b['file'], 'line': b['line'], 'col': b['col'],
        'blocked_side': b['blocked_side'],
        'selection_tags': json.loads(dm['selection_tags']),
        'resolving_fuzzers': json.loads(dm['resolving_fuzzers']),
        'blocking_fuzzers': json.loads(dm['blocking_fuzzers']),
        'tier': 1, 'status': 'confirmed', 'test_a': None, 'test_b': None,
    })
elif status == 'skipped':
    state.setdefault('skipped', []).append({
        'branch_id': bid, 'reason': result.get('notes', 'insufficient seeds'),
    })

with open('$STATE', 'w') as f:
    json.dump(state, f, indent=2)
conn.close()
" 2>/dev/null || log "  B${BID}: state update failed"
        done
    done

    # Count new clusters this round
    NEW_CLUSTERS=$(python3 -c "
import json
with open('$STATE') as f:
    state = json.load(f)
# Count clusters that have only tier-1 members from this round
print(len(state['clusters']))
")
    log "Clusters so far: $NEW_CLUSTERS"

    # ----------------------------------------------------------
    # T2: fit remaining branches
    # ----------------------------------------------------------
    REMAINING=$(python3 -c "
import json
with open('$STATE') as f:
    state = json.load(f)
assigned = set()
for c in state['clusters'].values():
    for m in c['members']:
        assigned.add(m['branch_id'])
for s in state.get('skipped', []):
    assigned.add(s['branch_id'])
remaining = [b for b in state.get('all_candidates', []) if b not in assigned]
print(' '.join(str(b) for b in remaining))
")

    if [ -z "$REMAINING" ]; then
        log "All branches assigned after T1!"
        break
    fi

    REMAINING_ARRAY=($REMAINING)
    log "T2: ${#REMAINING_ARRAY[@]} branches remaining"

    # Run T2 in batches
    UNFITTED=()
    for ((i=0; i<${#REMAINING_ARRAY[@]}; i+=T2_BATCH)); do
        BATCH_IDS=$(echo "${REMAINING_ARRAY[@]:i:T2_BATCH}" | tr ' ' ',')
        log "  T2 batch: $BATCH_IDS"

        T2_OUTPUT=$(python3 tools/cluster_t2.py batch \
            --target "$TARGET" \
            --branches "$BATCH_IDS" \
            --cluster-json "$STATE" \
            --queue-base "$QUEUE_BASE" 2>&1)

        # Parse T2 results and update state
        python3 -c "
import json, sqlite3

conn = sqlite3.connect('db/blockers.sqlite')
conn.row_factory = sqlite3.Row

with open('$STATE') as f:
    state = json.load(f)

results = json.loads('''$(echo "$T2_OUTPUT" | grep -v '^  B')''')
fitted = 0
unfitted_ids = []

for r in results:
    bid = r['branch_id']
    if r['status'] == 'confirmed' and r.get('cluster_id') and r['cluster_id'] in state['clusters']:
        b = conn.execute('SELECT file, line, col, blocked_side FROM branches WHERE branch_id=?', (bid,)).fetchone()
        dm = conn.execute('SELECT selection_tags, resolving_fuzzers, blocking_fuzzers FROM derived_metrics WHERE branch_id=?', (bid,)).fetchone()
        state['clusters'][r['cluster_id']]['members'].append({
            'branch_id': bid,
            'file': b['file'], 'line': b['line'], 'col': b['col'],
            'blocked_side': b['blocked_side'],
            'selection_tags': json.loads(dm['selection_tags']),
            'resolving_fuzzers': json.loads(dm['resolving_fuzzers']),
            'blocking_fuzzers': json.loads(dm['blocking_fuzzers']),
            'tier': 2, 'status': 'confirmed',
            'test_a': r.get('test_a'), 'test_b': r.get('test_b'),
        })
        fitted += 1
    else:
        unfitted_ids.append(bid)

state['unfitted'] = [{'branch_id': b} for b in unfitted_ids]

with open('$STATE', 'w') as f:
    json.dump(state, f, indent=2)
conn.close()
print(f'{fitted} fitted, {len(unfitted_ids)} unfitted')
" 2>&1 | tee -a "$LOG"
    done

    # Check if any unfitted remain
    UNFITTED_COUNT=$(python3 -c "
import json
with open('$STATE') as f:
    state = json.load(f)
print(len(state.get('unfitted', [])))
")

    if [ "$UNFITTED_COUNT" = "0" ]; then
        log "All branches assigned!"
        break
    fi

    log "Unfitted: $UNFITTED_COUNT — promoting to next T1 round"
done

# ============================================================
# Validate and generate report
# ============================================================
log ""
log "=== Validation ==="
python3 tools/cluster_orchestrator.py validate \
    --target "$TARGET" --state "$STATE" 2>&1 | tee -a "$LOG"

log ""
log "=== Generating report ==="
python3 tools/cluster_report.py --target "$TARGET" \
    --from-json "$STATE" \
    -o "clusters/${TARGET}_clusters_${RUN_DATE}.md" 2>&1 | tee -a "$LOG"

log ""
log "=== Importing to DB ==="
python3 tools/blocker_db.py import-clusters --input "$STATE" 2>&1 | tee -a "$LOG"

log ""
log "=== DONE ==="
python3 -c "
import json
with open('$STATE') as f:
    state = json.load(f)
n_clusters = len(state['clusters'])
n_assigned = sum(len(c['members']) for c in state['clusters'].values())
n_skipped = len(state.get('skipped', []))
print(f'Clusters: {n_clusters}, Assigned: {n_assigned}, Skipped: {n_skipped}')
" | tee -a "$LOG"
