#!/usr/bin/env python3
"""
cluster_verify.py — Tier 2 branch cluster verification tool.

Starts ONE persistent Docker container, then mechanically tests whether
unassigned branches fit existing clusters by mutating controlling bytes
in seeds and checking branch coverage.

Usage:
    python3 tools/cluster_verify.py \
        --target bloaty \
        --clusters clusters/bloaty_clusters.json \
        [--db db/blockers.sqlite] \
        [--queue-base ./out] \
        [--output clusters/bloaty_t2_results.json]
"""

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import time


def get_db(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def _parse_count(s):
    s = s.strip().replace(',', '')
    mult = {'k': 1_000, 'M': 1_000_000, 'G': 1_000_000_000}
    if s and s[-1] in mult:
        return int(float(s[:-1]) * mult[s[-1]])
    s = s.rstrip('eE')
    if not s:
        return 0
    return int(float(s))


class DockerRunner:
    """Persistent Docker container for running seeds and checking coverage."""

    def __init__(self, image, queue_dir, work_dir):
        self.image = image
        self.work_dir = work_dir
        # Start persistent container with queues and work dir mounted
        self.container_id = subprocess.check_output([
            'docker', 'run', '-d', '--entrypoint', '',
            '-v', f'{os.path.abspath(queue_dir)}:/queues:ro',
            '-v', f'{os.path.abspath(work_dir)}:/work',
            image,
            '/bin/bash', '-c', 'sleep infinity'
        ], text=True).strip()
        print(f"Started container {self.container_id[:12]}", file=sys.stderr)

    def exec(self, cmd):
        """Run a command inside the container, return stdout."""
        result = subprocess.run(
            ['docker', 'exec', self.container_id, '/bin/bash', '-c', cmd],
            capture_output=True, text=True, timeout=30
        )
        return result.stdout

    def run_seed_and_check(self, seed_container_path, line, col):
        """
        Run seed, get branch coverage. Returns (true_hits, false_hits).
        seed_container_path: path inside container (e.g. /work/mutated.bin or /queues/...)
        """
        cmd = (
            f'export LLVM_PROFILE_FILE=/tmp/t.profraw; '
            f'rm -f /tmp/t.profraw /tmp/t.profdata; '
            f'timeout 10 $FUZZ_BIN {seed_container_path} >/dev/null 2>&1 || true; '
            f'[ -f /tmp/t.profraw ] && '
            f'llvm-profdata-18 merge -sparse /tmp/t.profraw -o /tmp/t.profdata 2>/dev/null && '
            f'llvm-cov-18 show $FUZZ_BIN -instr-profile=/tmp/t.profdata '
            f'-show-branches=count -format=text 2>/dev/null | '
            f'grep "Branch ({line}:{col})" || true'
        )
        try:
            out = self.exec(cmd)
        except subprocess.TimeoutExpired:
            return None, None

        import re
        for out_line in out.strip().splitlines():
            if f'Branch ({line}:{col})' in out_line:
                m = re.search(r'True: ([^\],]+), False: ([^\]]+)', out_line)
                if m:
                    return _parse_count(m.group(1)), _parse_count(m.group(2))
        return 0, 0

    def write_mutated_seed(self, src_path, mutations, use_positive, dest_name='mutated.bin'):
        """Read seed from host, mutate, write to container work dir."""
        with open(src_path, 'rb') as f:
            data = bytearray(f.read())

        for mut in mutations:
            offset = mut['offset']
            length = mut['length']
            hex_val = mut['positive'] if use_positive else mut['negative']
            new_bytes = bytes.fromhex(hex_val)
            if len(new_bytes) != length:
                continue
            if offset + length > len(data):
                return None  # seed too short
            data[offset:offset + length] = new_bytes

        out_path = os.path.join(self.work_dir, dest_name)
        with open(out_path, 'wb') as f:
            f.write(data)
        return f'/work/{dest_name}'

    def kill(self):
        subprocess.run(['docker', 'kill', self.container_id],
                       capture_output=True)
        subprocess.run(['docker', 'rm', self.container_id],
                       capture_output=True)
        print(f"Stopped container {self.container_id[:12]}", file=sys.stderr)


def seed_path(queue_base, target, fuzzer, trial, seed_id):
    return os.path.join(queue_base, target, fuzzer, f'trial{trial}', 'queue', seed_id)


def main():
    parser = argparse.ArgumentParser(description='Tier 2 cluster verification (single container)')
    parser.add_argument('--target', required=True)
    parser.add_argument('--clusters', required=True, help='Cluster definitions JSON')
    parser.add_argument('--db', default='db/blockers.sqlite')
    parser.add_argument('--queue-base', default='./out')
    parser.add_argument('--output', help='Output JSON')
    parser.add_argument('--branch-id', type=int, help='Test single branch')
    args = parser.parse_args()

    if not args.output:
        args.output = f'clusters/{args.target}_t2_results.json'

    docker_image = f'blocker-{args.target}-cov'
    conn = get_db(args.db)

    with open(args.clusters) as f:
        cluster_defs = json.load(f)
    clusters = cluster_defs['clusters']

    # Get divergent branches
    if args.branch_id:
        branches = conn.execute('''
            SELECT b.branch_id, dm.rank, b.file, b.function, b.line, b.col, b.blocked_side
            FROM branches b JOIN derived_metrics dm ON dm.branch_id = b.branch_id
            WHERE b.target = ? AND b.branch_id = ?
        ''', (args.target, args.branch_id)).fetchall()
    else:
        branches = conn.execute('''
            SELECT b.branch_id, dm.rank, b.file, b.function, b.line, b.col, b.blocked_side
            FROM branches b JOIN derived_metrics dm ON dm.branch_id = b.branch_id
            WHERE b.target = ? AND dm.blocking_fuzzers != '[]' AND dm.resolving_fuzzers != '[]'
            ORDER BY dm.rank
        ''', (args.target,)).fetchall()

    print(f"Target {args.target}: {len(branches)} divergent branches, "
          f"{len(clusters)} clusters", file=sys.stderr)

    # Prepare work dir and start container
    work_dir = tempfile.mkdtemp(prefix='cluster_verify_')
    queue_dir = os.path.join(args.queue_base, args.target)
    runner = DockerRunner(docker_image, queue_dir, work_dir)

    results = []
    assigned = 0
    partial = 0
    skipped = 0
    unfitted = 0
    t0 = time.time()

    try:
        for bi, branch in enumerate(branches):
            bid = branch['branch_id']
            rank = branch['rank']
            line = branch['line']
            col = branch['col']
            blocked_side = branch['blocked_side']
            other_side = 'F' if blocked_side == 'T' else 'T'

            # Get seeds from DB — either side may be missing
            pos_db = conn.execute(
                'SELECT seed_id, fuzzer, trial FROM resolving_seeds WHERE branch_id=? LIMIT 1',
                (bid,)).fetchone()
            neg_db = conn.execute(
                'SELECT seed_id, fuzzer, trial FROM blocking_seeds WHERE branch_id=? LIMIT 1',
                (bid,)).fetchone()
            has_pos = pos_db is not None
            has_neg = neg_db is not None
            seed_status = 'both' if (has_pos and has_neg) else ('pos' if has_pos else ('neg' if has_neg else 'none'))

            result = {
                'branch_id': bid, 'rank': rank,
                'file': branch['file'], 'function': branch['function'],
                'line': line, 'col': col, 'blocked_side': blocked_side,
                'seed_status': seed_status,
                'cluster': None, 'test_a': None, 'test_b': None,
                'details': '', 'seed_source': seed_status,
            }

            fitted = False
            for cid, cdef in clusters.items():
                mutations = cdef['mutations']
                rep_pos = cdef.get('rep_positive_seed')
                rep_neg = cdef.get('rep_negative_seed')

                # Resolve positive seed path: own DB seed or cluster rep
                if has_pos:
                    pos_path = seed_path(args.queue_base, args.target,
                                         pos_db['fuzzer'], pos_db['trial'], pos_db['seed_id'])
                    pos_source = 'db'
                elif rep_pos:
                    pos_path = seed_path(args.queue_base, args.target,
                                         rep_pos['fuzzer'], rep_pos['trial'], rep_pos['id'])
                    pos_source = 'rep'
                else:
                    continue

                # Resolve negative seed path: own DB seed or cluster rep
                if has_neg:
                    neg_path = seed_path(args.queue_base, args.target,
                                         neg_db['fuzzer'], neg_db['trial'], neg_db['seed_id'])
                    neg_source = 'db'
                elif rep_neg:
                    neg_path = seed_path(args.queue_base, args.target,
                                         rep_neg['fuzzer'], rep_neg['trial'], rep_neg['id'])
                    neg_source = 'db'
                else:
                    continue

                if not os.path.exists(pos_path) or not os.path.exists(neg_path):
                    continue

                # If using any rep seed, verify it hits this branch
                import shutil
                if pos_source == 'rep':
                    orig_pos = os.path.join(work_dir, 'orig_pos.bin')
                    shutil.copy2(pos_path, orig_pos)
                    t_hits, f_hits = runner.run_seed_and_check('/work/orig_pos.bin', line, col)
                    if t_hits is None:
                        continue
                    if (t_hits if blocked_side == 'T' else f_hits) == 0:
                        continue

                if neg_source == 'rep':
                    orig_neg = os.path.join(work_dir, 'orig_neg.bin')
                    shutil.copy2(neg_path, orig_neg)
                    t_hits, f_hits = runner.run_seed_and_check('/work/orig_neg.bin', line, col)
                    if t_hits is None:
                        continue
                    if (t_hits if other_side == 'T' else f_hits) == 0:
                        continue

                result['seed_source'] = f'pos={pos_source},neg={neg_source}'

                # Check mode: whole_seed skips mutation, just checks if seeds hit
                mode = cdef.get('mode', 'mutate')

                if mode == 'whole_seed':
                    # No mutation — just check if pos seed hits blocked side
                    # and neg seed hits other side (already done above for rep seeds)
                    import shutil
                    if has_pos and has_neg:
                        # Need to check own seeds against this branch
                        chk_pos = os.path.join(work_dir, 'chk_pos.bin')
                        shutil.copy2(pos_path, chk_pos)
                        t_hits, f_hits = runner.run_seed_and_check('/work/chk_pos.bin', line, col)
                        if t_hits is None:
                            continue
                        test_a = (t_hits if blocked_side == 'T' else f_hits) > 0

                        chk_neg = os.path.join(work_dir, 'chk_neg.bin')
                        shutil.copy2(neg_path, chk_neg)
                        t_hits, f_hits = runner.run_seed_and_check('/work/chk_neg.bin', line, col)
                        if t_hits is None:
                            test_b = None
                        else:
                            test_b = (t_hits if other_side == 'T' else f_hits) > 0
                    else:
                        # Rep seeds already checked above — if we got here, both hit
                        test_a = True
                        test_b = True
                else:
                    # Byte mutation mode
                    mut_path = runner.write_mutated_seed(pos_path, mutations, use_positive=False, dest_name='test_a.bin')
                    if mut_path is None:
                        continue  # seed too short

                    t_hits, f_hits = runner.run_seed_and_check(mut_path, line, col)
                    if t_hits is None:
                        continue
                    blocked_hits_a = t_hits if blocked_side == 'T' else f_hits
                    test_a = blocked_hits_a == 0

                    # Test B: negative seed with positive bytes -> blocked side should appear
                    mut_path = runner.write_mutated_seed(neg_path, mutations, use_positive=True, dest_name='test_b.bin')
                    if mut_path is None:
                        test_b = None
                    else:
                        t_hits, f_hits = runner.run_seed_and_check(mut_path, line, col)
                        if t_hits is None:
                            test_b = None
                        else:
                            blocked_hits_b = t_hits if blocked_side == 'T' else f_hits
                            test_b = blocked_hits_b > 0

                if test_a and test_b:
                    result['cluster'] = cid
                    result['test_a'] = True
                    result['test_b'] = True
                    result['details'] = f'A:✓ B:✓'
                    fitted = True
                    assigned += 1
                    break
                elif test_a:
                    result['cluster'] = cid
                    result['test_a'] = True
                    result['test_b'] = False
                    result['details'] = f'A:✓ B:✗'
                    fitted = True
                    partial += 1
                    break

            if not fitted:
                if not has_pos and not has_neg:
                    result['details'] = 'no seeds, no rep seeds hit'
                    skipped += 1
                else:
                    result['details'] = 'no cluster fit'
                    unfitted += 1

            results.append(result)

            if (bi + 1) % 10 == 0:
                elapsed = time.time() - t0
                rate = (bi + 1) / elapsed
                eta = (len(branches) - bi - 1) / rate
                print(f"  [{bi+1}/{len(branches)}] assigned={assigned} partial={partial} "
                      f"skipped={skipped} unfitted={unfitted} "
                      f"({elapsed:.0f}s, ETA {eta:.0f}s)",
                      file=sys.stderr)

    finally:
        runner.kill()
        # Cleanup work dir
        for f in os.listdir(work_dir):
            os.remove(os.path.join(work_dir, f))
        os.rmdir(work_dir)

    output_data = {
        'target': args.target,
        'total_branches': len(branches),
        'assigned': assigned,
        'partial': partial,
        'skipped': skipped,
        'unfitted': unfitted,
        'results': results,
    }
    with open(args.output, 'w') as f:
        json.dump(output_data, f, indent=2)

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.0f}s. assigned={assigned} partial={partial} "
          f"skipped={skipped} unfitted={unfitted}",
          file=sys.stderr)

    cluster_counts = {}
    for r in results:
        c = r['cluster'] or 'NONE'
        cluster_counts[c] = cluster_counts.get(c, 0) + 1
    print(f"\nCluster assignments:", file=sys.stderr)
    for c, n in sorted(cluster_counts.items()):
        print(f"  {c}: {n}", file=sys.stderr)

    conn.close()


if __name__ == '__main__':
    main()
