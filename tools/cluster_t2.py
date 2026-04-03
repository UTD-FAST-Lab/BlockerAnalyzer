#!/usr/bin/env python3
"""
cluster_t2.py — Mechanical T2 cluster verification.

For a given branch, tries to fit it into each candidate cluster by:
  Test A (necessity): mutate 1 positive seed — break controlling bytes → branch should disappear
  Test B (sufficiency): mutate N negative seeds — inject controlling bytes → branch should appear

One Docker container per branch. All mutated seeds run inside with unique profraw files.

Usage:
    # Single branch against one cluster
    python3 tools/cluster_t2.py verify \
        --target lcms --branch-id 143 \
        --cluster-json clusters/lcms_state.json \
        --cluster-id BC01 \
        --queue-base ./out

    # Batch: try all clusters for a branch
    python3 tools/cluster_t2.py verify \
        --target lcms --branch-id 143 \
        --cluster-json clusters/lcms_state.json \
        --queue-base ./out

    # Batch file: process multiple branches
    python3 tools/cluster_t2.py batch \
        --target lcms \
        --cluster-json clusters/lcms_state.json \
        --branches 143,145,146,150 \
        --queue-base ./out
"""

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import re

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_DIR, 'db', 'blockers.sqlite')
DOCKER_IMAGE_FMT = 'blocker-{target}-cov'


def get_db(db_path=None):
    conn = sqlite3.connect(db_path or DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_branch_info(branch_id, db_path=None):
    conn = get_db(db_path)
    row = conn.execute('''
        SELECT b.branch_id, b.file, b.line, b.col, b.blocked_side
        FROM branches b WHERE b.branch_id = ?
    ''', (branch_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_seeds(branch_id, table, fuzzer=None, limit=5, db_path=None):
    """Get seed IDs and their queue paths."""
    conn = get_db(db_path)
    if fuzzer:
        rows = conn.execute(f'''
            SELECT seed_id, fuzzer, trial FROM {table}
            WHERE branch_id = ? AND fuzzer = ? LIMIT ?
        ''', (branch_id, fuzzer, limit)).fetchall()
    else:
        rows = conn.execute(f'''
            SELECT seed_id, fuzzer, trial FROM {table}
            WHERE branch_id = ? LIMIT ?
        ''', (branch_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_diverse_seeds(branch_id, table, limit=5, db_path=None):
    """Get seeds maximizing (fuzzer, trial) diversity."""
    conn = get_db(db_path)
    # Get all available (fuzzer, trial) combos
    combos = conn.execute(f'''
        SELECT DISTINCT fuzzer, trial FROM {table}
        WHERE branch_id = ?
    ''', (branch_id,)).fetchall()

    seeds = []
    seen_combos = set()
    # First pass: one seed per unique (fuzzer, trial)
    for combo in combos:
        if len(seeds) >= limit:
            break
        key = (combo['fuzzer'], combo['trial'])
        if key not in seen_combos:
            row = conn.execute(f'''
                SELECT seed_id, fuzzer, trial FROM {table}
                WHERE branch_id = ? AND fuzzer = ? AND trial = ? LIMIT 1
            ''', (branch_id, combo['fuzzer'], combo['trial'])).fetchone()
            if row:
                seeds.append(dict(row))
                seen_combos.add(key)

    # Second pass: fill remaining slots
    if len(seeds) < limit:
        extra = conn.execute(f'''
            SELECT seed_id, fuzzer, trial FROM {table}
            WHERE branch_id = ? LIMIT ?
        ''', (branch_id, limit * 2)).fetchall()
        for row in extra:
            if len(seeds) >= limit:
                break
            if row['seed_id'] not in {s['seed_id'] for s in seeds}:
                seeds.append(dict(row))

    conn.close()
    return seeds


def read_seed_bytes(queue_base, target, fuzzer, trial, seed_id):
    path = os.path.join(queue_base, target, fuzzer, f'trial{trial}', 'queue', seed_id)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return f.read()
    return None


def mutate_bytes(data, offset, new_bytes):
    """Replace bytes at offset with new_bytes."""
    data = bytearray(data)
    end = offset + len(new_bytes)
    if end <= len(data):
        data[offset:end] = new_bytes
    return bytes(data)


def parse_controlling_bytes(spec):
    """Parse 'bytes[16:20] = 4c616220' into (offset, value_hex)."""
    # Handle various formats
    m = re.match(r'bytes\[(\d+):(\d+)\]\s*=\s*([0-9a-fA-F]+)', spec)
    if m:
        offset = int(m.group(1))
        value_hex = m.group(3)
        return offset, bytes.fromhex(value_hex)

    # Try 'offset N-M = HEX'
    m = re.match(r'offset\s+(\d+)[-–](\d+).*?([0-9a-fA-F]{2,})', spec)
    if m:
        offset = int(m.group(1))
        value_hex = m.group(3)
        return offset, bytes.fromhex(value_hex)

    return None, None


def run_verification(target, branch_info, mutated_seeds, docker_image=None):
    """
    Run all mutated seeds in one Docker container.
    Returns dict: {seed_name: branch_line} where branch_line is the grep output.
    """
    if not docker_image:
        docker_image = DOCKER_IMAGE_FMT.format(target=target)

    tmpdir = tempfile.mkdtemp(prefix='t2_verify_')
    seeds_dir = os.path.join(tmpdir, 'seeds')
    os.makedirs(seeds_dir)

    # Write mutated seeds
    for name, data in mutated_seeds.items():
        with open(os.path.join(seeds_dir, f'{name}.bin'), 'wb') as f:
            f.write(data)

    line = branch_info['line']
    col = branch_info['col']

    cmd = [
        'docker', 'run', '--rm', '--entrypoint', '',
        '-v', f'{seeds_dir}:/seeds:ro',
        docker_image,
        '/bin/bash', '-c',
        f'''
        for seed in /seeds/*.bin; do
            name=$(basename "$seed" .bin)
            LLVM_PROFILE_FILE="/tmp/${{name}}.profraw" \
                timeout 10 $FUZZ_BIN "$seed" >/dev/null 2>&1 || true
            if [ -f "/tmp/${{name}}.profraw" ]; then
                llvm-profdata-18 merge -sparse "/tmp/${{name}}.profraw" \
                    -o "/tmp/${{name}}.profdata" 2>/dev/null
                echo "=== $name ==="
                llvm-cov-18 show $FUZZ_BIN \
                    -instr-profile="/tmp/${{name}}.profdata" \
                    -show-branches=count -format=text 2>/dev/null \
                    | grep "Branch ({line}:{col})" || echo "NO_BRANCH"
            else
                echo "=== $name ==="
                echo "NO_PROFRAW"
            fi
        done
        '''
    ]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        output = proc.stdout
    except subprocess.TimeoutExpired:
        shutil.rmtree(tmpdir, ignore_errors=True)
        return {}

    # Parse output
    results = {}
    current_name = None
    for out_line in output.splitlines():
        if out_line.startswith('=== ') and out_line.endswith(' ==='):
            current_name = out_line[4:-4]
        elif current_name:
            results[current_name] = out_line.strip()

    shutil.rmtree(tmpdir, ignore_errors=True)
    return results


def check_branch_hit(cov_line, side):
    """Check if the branch's blocked side is hit in the coverage output."""
    if not cov_line or cov_line in ('NO_BRANCH', 'NO_PROFRAW'):
        return False
    m = re.search(r'True: ([^\],]+), False: ([^\]]+)', cov_line)
    if not m:
        return False
    t_hits = int(m.group(1).strip().replace(',', ''))
    f_hits = int(m.group(2).strip().replace(',', ''))
    if side == 'T':
        return t_hits > 0
    else:
        return f_hits > 0


def verify_branch(target, branch_id, cluster, queue_base,
                   num_neg_seeds=3, db_path=None):
    """
    Try to fit branch_id into a cluster.
    Returns: {'status': 'confirmed'|'failed', 'test_a': 'pass'|'fail',
              'test_b': ['pass'|'fail', ...], 'details': '...'}
    """
    branch = get_branch_info(branch_id, db_path)
    if not branch:
        return {'status': 'error', 'details': f'Branch {branch_id} not found'}

    # Parse cluster hypothesis
    offset, pos_value = parse_controlling_bytes(cluster['controlling_bytes'])
    if offset is None:
        return {'status': 'error', 'details': f'Cannot parse: {cluster["controlling_bytes"]}'}

    rep_id = cluster['representative']
    blocked_side = branch['blocked_side']

    # Get positive seed (resolving seed for the representative)
    pos_seeds = get_seeds(rep_id, 'resolving_seeds', limit=1, db_path=db_path)
    if not pos_seeds:
        return {'status': 'error', 'details': 'No positive seeds for representative'}

    # Get negative seeds (blocking seeds for the representative)
    # Maximize fuzzer/trial diversity
    neg_seeds = get_diverse_seeds(rep_id, 'blocking_seeds',
                                  limit=num_neg_seeds, db_path=db_path)
    if not neg_seeds:
        return {'status': 'error', 'details': 'No negative seeds for representative'}

    # Read seed bytes
    pos_data = read_seed_bytes(queue_base, target,
                               pos_seeds[0]['fuzzer'], pos_seeds[0]['trial'],
                               pos_seeds[0]['seed_id'])
    if not pos_data:
        return {'status': 'error', 'details': f'Cannot read positive seed {pos_seeds[0]["seed_id"]}'}

    neg_data_list = []
    for ns in neg_seeds:
        nd = read_seed_bytes(queue_base, target, ns['fuzzer'], ns['trial'], ns['seed_id'])
        if nd:
            neg_data_list.append((ns, nd))

    if not neg_data_list:
        return {'status': 'error', 'details': 'Cannot read any negative seeds'}

    # Build mutated seeds
    mutated = {}

    # Test A: break positive seed (replace controlling bytes with negative value)
    # Use the first negative seed's bytes at the controlling offset as the "wrong" value
    neg_value = neg_data_list[0][1][offset:offset + len(pos_value)]
    if neg_value == pos_value:
        neg_value = b'\x00' * len(pos_value)  # fallback: use zeros
    mutated['test_a'] = mutate_bytes(pos_data, offset, neg_value)

    # Test B: fix each negative seed (inject positive controlling bytes)
    for i, (ns, nd) in enumerate(neg_data_list):
        if len(nd) > offset + len(pos_value):
            mutated[f'test_b_{i}'] = mutate_bytes(nd, offset, pos_value)

    if not any(k.startswith('test_b') for k in mutated):
        return {'status': 'error', 'details': 'All negative seeds too short for injection'}

    # Run all in one Docker container
    results = run_verification(target, branch, mutated)

    # Evaluate
    test_a_hit = check_branch_hit(results.get('test_a', ''), blocked_side)
    test_a_result = 'fail' if test_a_hit else 'pass'  # Test A passes if blocked side DISAPPEARS

    test_b_results = []
    for key in sorted(k for k in results if k.startswith('test_b')):
        hit = check_branch_hit(results.get(key, ''), blocked_side)
        test_b_results.append('pass' if hit else 'fail')  # Test B passes if blocked side APPEARS

    all_b_pass = all(r == 'pass' for r in test_b_results) if test_b_results else False

    if test_a_result == 'pass' and all_b_pass:
        status = 'confirmed'
    elif test_a_result == 'pass' and not all_b_pass:
        status = 'partial'  # necessary but not sufficient
    else:
        status = 'failed'

    return {
        'status': status,
        'test_a': test_a_result,
        'test_b': test_b_results,
        'details': f'Test A: {test_a_result}, Test B: {test_b_results}',
    }


def verify_branch_all_clusters(target, branch_id, cluster_json_path, queue_base,
                                cluster_id=None, db_path=None):
    """Try to fit a branch into one or all clusters."""
    with open(cluster_json_path) as f:
        state = json.load(f)

    clusters = state.get('clusters', {})

    if cluster_id:
        # Try specific cluster
        if cluster_id not in clusters:
            print(f"Cluster {cluster_id} not found", file=sys.stderr)
            return None
        result = verify_branch(target, branch_id, clusters[cluster_id],
                               queue_base, db_path=db_path)
        result['cluster_id'] = cluster_id
        return result

    # Try all clusters, starting with same-function clusters
    branch = get_branch_info(branch_id, db_path)
    if not branch:
        return None

    # Get branch's function
    conn = get_db(db_path)
    func = conn.execute('SELECT function FROM branches WHERE branch_id=?',
                        (branch_id,)).fetchone()['function']
    conn.close()

    # Sort: same-function clusters first
    def cluster_sort_key(cid):
        rep = clusters[cid]['representative']
        conn2 = get_db(db_path)
        rep_func = conn2.execute('SELECT function FROM branches WHERE branch_id=?',
                                 (rep,)).fetchone()
        conn2.close()
        return (0 if rep_func and rep_func['function'] == func else 1, cid)

    for cid in sorted(clusters.keys(), key=cluster_sort_key):
        result = verify_branch(target, branch_id, clusters[cid],
                               queue_base, db_path=db_path)
        if result['status'] == 'confirmed':
            result['cluster_id'] = cid
            return result

    return {'status': 'unfitted', 'cluster_id': None, 'details': 'No cluster fits'}


def batch_verify(target, branch_ids, cluster_json_path, queue_base, db_path=None):
    """Process multiple branches, output results as JSON."""
    results = []
    for bid in branch_ids:
        print(f"  B{bid}...", file=sys.stderr, end=' ')
        r = verify_branch_all_clusters(target, bid, cluster_json_path,
                                        queue_base, db_path=db_path)
        if r:
            r['branch_id'] = bid
            results.append(r)
            print(f"{r['status']} → {r.get('cluster_id', '—')}", file=sys.stderr)
        else:
            print("error", file=sys.stderr)
    return results


def main():
    parser = argparse.ArgumentParser(description='T2 cluster verification')
    sub = parser.add_subparsers(dest='command')

    p_verify = sub.add_parser('verify', help='Verify one branch')
    p_verify.add_argument('--target', required=True)
    p_verify.add_argument('--branch-id', type=int, required=True)
    p_verify.add_argument('--cluster-json', required=True)
    p_verify.add_argument('--cluster-id', help='Try specific cluster (default: try all)')
    p_verify.add_argument('--queue-base', required=True)
    p_verify.add_argument('--db')

    p_batch = sub.add_parser('batch', help='Verify multiple branches')
    p_batch.add_argument('--target', required=True)
    p_batch.add_argument('--branches', required=True, help='Comma-separated branch IDs')
    p_batch.add_argument('--cluster-json', required=True)
    p_batch.add_argument('--queue-base', required=True)
    p_batch.add_argument('--db')

    args = parser.parse_args()

    if args.command == 'verify':
        result = verify_branch_all_clusters(
            args.target, args.branch_id, args.cluster_json,
            args.queue_base, cluster_id=args.cluster_id, db_path=args.db)
        print(json.dumps(result, indent=2))

    elif args.command == 'batch':
        bids = [int(x) for x in args.branches.split(',')]
        results = batch_verify(args.target, bids, args.cluster_json,
                               args.queue_base, db_path=args.db)
        print(json.dumps(results, indent=2))

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
