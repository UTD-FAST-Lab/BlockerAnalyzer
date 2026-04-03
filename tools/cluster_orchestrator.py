#!/usr/bin/env python3
"""
cluster_orchestrator.py — Orchestrates parallel branch clustering.

Manages the T1→T2→promote loop:
  1. Selects candidate branches from DB (selection_tags != '[]')
  2. Samples T1 representatives proportionally per function
  3. Spawns parallel branch-cluster agents for T1 analysis
  4. Runs parallel T2 verification via cluster_t2.py
  5. Promotes unfitted branches to next T1 round
  6. Repeats until all branches assigned or skipped
  7. Writes final JSON state to clusters/<target>_state.json

Usage:
    python3 tools/cluster_orchestrator.py \
        --target lcms \
        --queue-base ./out \
        [--t1-parallel 10] \
        [--t2-parallel 20] \
        [--run-date 2026-04-03] \
        [--output clusters/lcms_state.json]
"""

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import time
from collections import defaultdict
from datetime import date

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_DIR, 'db', 'blockers.sqlite')
T2_TOOL = os.path.join(PROJECT_DIR, 'tools', 'cluster_t2.py')


def get_db(db_path=None):
    conn = sqlite3.connect(db_path or DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_candidates(target, db_path=None):
    """Get all tagged divergent branches."""
    conn = get_db(db_path)
    rows = conn.execute('''
        SELECT b.branch_id, b.file, b.function, b.line, b.col, b.blocked_side,
               dm.selection_tags, dm.prob_div, dm.dur_div, dm.hit_div,
               dm.blocking_fuzzers, dm.resolving_fuzzers, dm.unreached_fuzzers
        FROM branches b
        JOIN derived_metrics dm ON dm.branch_id = b.branch_id
        WHERE b.target = ? AND dm.selection_tags != '[]'
          AND dm.blocking_fuzzers != '[]' AND dm.resolving_fuzzers != '[]'
    ''', (target,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def sample_t1_representatives(candidates, assigned, t1_failures, min_total=10):
    """
    Sample T1 representatives proportionally per function.
    At least 1 per function, minimum min_total total.
    Prioritize branches with more selection tags.
    Exclude already-assigned and prior T1 failures.
    """
    pool = [c for c in candidates
            if c['branch_id'] not in assigned
            and c['branch_id'] not in t1_failures]

    if not pool:
        return []

    # Group by function
    by_func = defaultdict(list)
    for c in pool:
        by_func[c['function']].append(c)

    # Sort within each function: more tags first, then by divergence
    for func in by_func:
        by_func[func].sort(key=lambda c: (
            -len(json.loads(c['selection_tags'])),
            -(c['prob_div'] or 0),
            -(c['dur_div'] or 0),
            -(c['hit_div'] or 0),
        ))

    n_funcs = len(by_func)
    total = max(min_total, n_funcs)

    # Allocate slots proportionally
    func_counts = {f: len(branches) for f, branches in by_func.items()}
    total_branches = sum(func_counts.values())

    slots = {}
    for func, count in func_counts.items():
        slots[func] = max(1, round(count / total_branches * total))

    # Pick top branches per function
    reps = []
    for func, n in slots.items():
        reps.extend(by_func[func][:n])

    return reps


def run_t1_agent(target, branch_id, queue_base):
    """
    Spawn a branch-cluster agent for T1 analysis.
    Returns the parsed JSON result or None.
    """
    # TODO: In production, this would use the Agent tool to spawn
    # a branch-cluster agent. For now, we use claude CLI directly.
    # The orchestrator is designed to be called from the main conversation
    # where the Agent tool is available.
    #
    # For standalone testing, this is a placeholder.
    print(f"  [T1] Spawning agent for B{branch_id}...", file=sys.stderr)
    return None  # Placeholder — real implementation uses Agent tool


def run_t2_batch(target, branch_ids, state_path, queue_base, db_path=None):
    """Run T2 verification for a batch of branches using cluster_t2.py."""
    if not branch_ids:
        return []

    bids_str = ','.join(str(b) for b in branch_ids)
    cmd = [
        sys.executable, T2_TOOL, 'batch',
        '--target', target,
        '--branches', bids_str,
        '--cluster-json', state_path,
        '--queue-base', queue_base,
    ]
    if db_path:
        cmd.extend(['--db', db_path])

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        if proc.returncode != 0:
            print(f"  [T2] Error: {proc.stderr[:500]}", file=sys.stderr)
            return []
        return json.loads(proc.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        print(f"  [T2] Error: {e}", file=sys.stderr)
        return []


def initialize_state(target, run_date):
    """Create initial state JSON."""
    return {
        'target': target,
        'run_date': run_date,
        'clusters': {},
        'skipped': [],
        'unfitted': [],
        'next_cluster_id': 1,
    }


def assign_cluster_id(state):
    """Get next cluster ID like BC01, BC02, ..."""
    n = state['next_cluster_id']
    state['next_cluster_id'] = n + 1
    return f'BC{n:02d}'


def add_t1_result(state, result, branch_info):
    """Add a T1 analysis result to the state."""
    bid = result['branch_id']
    status = result.get('status', 'error')

    if status == 'confirmed':
        cid = assign_cluster_id(state)
        state['clusters'][cid] = {
            'controlling_bytes': result.get('controlling_bytes', ''),
            'semantic_label': result.get('semantic_label', ''),
            'source_mapping': result.get('source_mapping', ''),
            'representative': bid,
            'members': [{
                'branch_id': bid,
                'file': branch_info.get('file', ''),
                'line': branch_info.get('line', 0),
                'col': branch_info.get('col', 0),
                'blocked_side': branch_info.get('blocked_side', ''),
                'selection_tags': json.loads(branch_info.get('selection_tags', '[]')),
                'resolving_fuzzers': json.loads(branch_info.get('resolving_fuzzers', '[]')),
                'blocking_fuzzers': json.loads(branch_info.get('blocking_fuzzers', '[]')),
                'tier': 1,
                'status': 'confirmed',
                'test_a': None,
                'test_b': None,
            }],
        }
        return cid

    elif status == 'skipped':
        state['skipped'].append({
            'branch_id': bid,
            'reason': result.get('notes', 'insufficient seeds'),
        })
        return None

    else:  # unresolved or error
        return None


def add_t2_result(state, result, branch_info):
    """Add a T2 verification result to the state."""
    bid = result['branch_id']
    cid = result.get('cluster_id')
    status = result.get('status', 'failed')

    if status == 'confirmed' and cid and cid in state['clusters']:
        state['clusters'][cid]['members'].append({
            'branch_id': bid,
            'file': branch_info.get('file', ''),
            'line': branch_info.get('line', 0),
            'col': branch_info.get('col', 0),
            'blocked_side': branch_info.get('blocked_side', ''),
            'selection_tags': json.loads(branch_info.get('selection_tags', '[]')),
            'resolving_fuzzers': json.loads(branch_info.get('resolving_fuzzers', '[]')),
            'blocking_fuzzers': json.loads(branch_info.get('blocking_fuzzers', '[]')),
            'tier': 2,
            'status': 'confirmed',
            'test_a': result.get('test_a'),
            'test_b': result.get('test_b'),
        })
        return True

    return False


def save_state(state, path):
    """Write state JSON."""
    with open(path, 'w') as f:
        json.dump(state, f, indent=2)


def print_summary(state):
    """Print current clustering summary."""
    n_clusters = len(state['clusters'])
    n_assigned = sum(len(c['members']) for c in state['clusters'].values())
    n_skipped = len(state['skipped'])
    n_unfitted = len(state['unfitted'])
    print(f"\n  Summary: {n_clusters} clusters, {n_assigned} assigned, "
          f"{n_skipped} skipped, {n_unfitted} unfitted", file=sys.stderr)


def orchestrate(target, queue_base, t1_parallel=10, t2_parallel=20,
                run_date=None, output=None, db_path=None):
    """Main orchestration loop."""
    if not run_date:
        run_date = date.today().isoformat()
    if not output:
        output = os.path.join(PROJECT_DIR, 'clusters', f'{target}_state.json')

    # Load or create state
    if os.path.exists(output):
        with open(output) as f:
            state = json.load(f)
        print(f"Resuming from {output}", file=sys.stderr)
    else:
        state = initialize_state(target, run_date)
        print(f"Starting fresh for {target}", file=sys.stderr)

    # Get all candidates
    candidates = get_candidates(target, db_path)
    if not candidates:
        print(f"No candidates for {target}", file=sys.stderr)
        return

    candidate_map = {c['branch_id']: c for c in candidates}
    print(f"Candidates: {len(candidates)} divergent tagged branches", file=sys.stderr)

    # Track assigned and failed branches
    assigned = set()
    for cluster in state['clusters'].values():
        for m in cluster['members']:
            assigned.add(m['branch_id'])
    for s in state['skipped']:
        assigned.add(s['branch_id'])
    t1_failures = set()

    round_num = 0
    consecutive_no_new = 0

    while True:
        round_num += 1
        remaining = [c for c in candidates if c['branch_id'] not in assigned
                     and c['branch_id'] not in t1_failures]

        if not remaining:
            print(f"\nAll branches processed.", file=sys.stderr)
            break

        print(f"\n{'='*60}", file=sys.stderr)
        print(f"Round {round_num}: {len(remaining)} branches remaining", file=sys.stderr)

        # --- T1: select representatives ---
        reps = sample_t1_representatives(candidates, assigned, t1_failures)
        if not reps:
            # No more candidates for T1
            for c in remaining:
                state['skipped'].append({
                    'branch_id': c['branch_id'],
                    'reason': 'no T1 candidates remaining',
                })
                assigned.add(c['branch_id'])
            break

        print(f"  T1: {len(reps)} representatives selected", file=sys.stderr)

        # Spawn T1 agents (in parallel batches)
        new_clusters = 0
        for i in range(0, len(reps), t1_parallel):
            batch = reps[i:i + t1_parallel]
            print(f"  T1 batch {i//t1_parallel + 1}: "
                  f"branches {[r['branch_id'] for r in batch]}", file=sys.stderr)

            # NOTE: In real usage, this is where we'd spawn parallel agents.
            # The orchestrator prints the batch info; the main conversation
            # uses the Agent tool to spawn branch-cluster agents in parallel.
            #
            # For each completed agent, call add_t1_result(state, result, branch_info)
            # and save_state(state, output).
            #
            # For standalone mode, we just mark them as needing manual processing.
            print(f"  *** Spawn {len(batch)} branch-cluster agents in parallel ***",
                  file=sys.stderr)
            print(f"  *** Waiting for results... ***", file=sys.stderr)

            # Placeholder: in production, agents return results here
            # For now, break out and let the caller handle agent spawning
            print(f"\nOrchestrator paused. Spawn agents for these branches:",
                  file=sys.stderr)
            for r in batch:
                print(f"  B{r['branch_id']} ({r['function']}:{r['line']}:{r['col']})",
                      file=sys.stderr)

            save_state(state, output)
            print(f"\nState saved to {output}", file=sys.stderr)
            print(f"After agents complete, feed results back and re-run.", file=sys.stderr)
            return  # Exit — caller handles agent spawning

        # --- T2: fit remaining into clusters ---
        if not state['clusters']:
            print("  No clusters yet, skipping T2", file=sys.stderr)
            continue

        save_state(state, output)

        remaining_ids = [c['branch_id'] for c in candidates
                         if c['branch_id'] not in assigned
                         and c['branch_id'] not in t1_failures]

        print(f"  T2: {len(remaining_ids)} branches to verify", file=sys.stderr)

        # Run T2 in batches
        unfitted = []
        for i in range(0, len(remaining_ids), t2_parallel):
            batch_ids = remaining_ids[i:i + t2_parallel]
            print(f"  T2 batch {i//t2_parallel + 1}: {len(batch_ids)} branches",
                  file=sys.stderr)

            results = run_t2_batch(target, batch_ids, output, queue_base, db_path)

            for r in results:
                bid = r['branch_id']
                if r['status'] == 'confirmed':
                    add_t2_result(state, r, candidate_map.get(bid, {}))
                    assigned.add(bid)
                else:
                    unfitted.append(bid)

            save_state(state, output)

        state['unfitted'] = [{'branch_id': b} for b in unfitted]

        if new_clusters == 0:
            consecutive_no_new += 1
            if consecutive_no_new >= 2:
                print(f"  Two consecutive rounds with no new clusters. "
                      f"Marking {len(unfitted)} as skipped.", file=sys.stderr)
                for bid in unfitted:
                    state['skipped'].append({
                        'branch_id': bid,
                        'reason': 'unresolvable (no new clusters in 2 rounds)',
                    })
                    assigned.add(bid)
                break
        else:
            consecutive_no_new = 0

    save_state(state, output)
    print_summary(state)
    print(f"\nFinal state: {output}", file=sys.stderr)


def validate_clusters(target, state_path, db_path=None):
    """
    Post-clustering validation: check per-trial consistency within each cluster.

    For each cluster with ≥2 members, verify that within any single (fuzzer, trial),
    all members are consistently resolved or blocked. Inconsistency means the
    controlling bytes are necessary but not sufficient for some members.
    """
    conn = get_db(db_path)

    with open(state_path) as f:
        state = json.load(f)

    print(f"Validating {len(state['clusters'])} clusters for {target}...",
          file=sys.stderr)

    issues = []
    for cid, cdata in state['clusters'].items():
        bids = [m['branch_id'] for m in cdata['members']]
        if len(bids) < 2:
            continue

        fts = conn.execute('''
            SELECT DISTINCT fuzzer, trial FROM trial_coverage
            WHERE branch_id IN ({})
        '''.format(','.join(str(b) for b in bids))).fetchall()

        cluster_issues = []
        for fuzzer, trial in fts:
            statuses = {}
            for bid in bids:
                r = conn.execute(
                    'SELECT hit_status FROM trial_coverage '
                    'WHERE branch_id=? AND fuzzer=? AND trial=?',
                    (bid, fuzzer, trial)).fetchone()
                if r:
                    statuses[bid] = r[0]

            resolved = [b for b, s in statuses.items() if s == 1]
            blocked = [b for b, s in statuses.items() if s == 0]

            if resolved and blocked:
                cluster_issues.append({
                    'fuzzer': fuzzer, 'trial': trial,
                    'resolved': resolved, 'blocked': blocked,
                })

        if cluster_issues:
            issues.append({
                'cluster_id': cid,
                'n_members': len(bids),
                'n_inconsistent_trials': len(cluster_issues),
                'details': cluster_issues,
            })
            # Find the outlier branches (minority in most trials)
            outlier_counts = defaultdict(int)
            for ci in cluster_issues:
                minority = ci['resolved'] if len(ci['resolved']) < len(ci['blocked']) else ci['blocked']
                for b in minority:
                    outlier_counts[b] += 1
            worst = sorted(outlier_counts.items(), key=lambda x: -x[1])

            print(f"  {cid}: INCONSISTENT in {len(cluster_issues)}/{len(fts)} "
                  f"(fuzzer,trial) pairs", file=sys.stderr)
            for bid, count in worst[:3]:
                print(f"    B{bid} disagrees in {count}/{len(fts)} pairs "
                      f"— candidate for split", file=sys.stderr)
        else:
            print(f"  {cid}: consistent ✓", file=sys.stderr)

    conn.close()

    if not issues:
        print(f"\nAll clusters validated — per-trial consistency confirmed.",
              file=sys.stderr)
    else:
        print(f"\n{len(issues)} cluster(s) have inconsistencies — "
              f"consider splitting.", file=sys.stderr)

    return issues


def main():
    parser = argparse.ArgumentParser(description='Cluster orchestrator')
    sub = parser.add_subparsers(dest='command')

    p_run = sub.add_parser('run', help='Run clustering')
    p_run.add_argument('--target', required=True)
    p_run.add_argument('--queue-base', required=True)
    p_run.add_argument('--t1-parallel', type=int, default=10)
    p_run.add_argument('--t2-parallel', type=int, default=20)
    p_run.add_argument('--run-date')
    p_run.add_argument('--output', '-o')
    p_run.add_argument('--db')

    p_val = sub.add_parser('validate', help='Validate cluster consistency')
    p_val.add_argument('--target', required=True)
    p_val.add_argument('--state', required=True, help='Path to state JSON')
    p_val.add_argument('--db')

    args = parser.parse_args()

    if args.command == 'run':
        orchestrate(
            args.target, args.queue_base,
            t1_parallel=args.t1_parallel,
            t2_parallel=args.t2_parallel,
            run_date=args.run_date,
            output=args.output,
            db_path=args.db,
        )
    elif args.command == 'validate':
        validate_clusters(args.target, args.state, db_path=args.db)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
