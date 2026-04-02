#!/usr/bin/env python3
"""
seed_bisect.py — Find seeds that hit blocking branches.

Runs ONE Docker container per target. Inside, for each unique queue
(fuzzer/trial), scans all seeds once and checks ALL target branches.
Much faster than per-branch bisection.

Usage:
    python3 tools/seed_bisect.py build --target bloaty
    python3 tools/seed_bisect.py run --target bloaty --queue-base ./out
    python3 tools/seed_bisect.py run --target bloaty --queue-base ./out --branch-id 5
    python3 tools/seed_bisect.py plan --target bloaty --queue-base ./out
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from collections import defaultdict
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = TOOLS_DIR.parent
DB_PATH = PROJECT_DIR / 'db' / 'blockers.sqlite'
DOCKER_DIR = PROJECT_DIR / 'docker'

sys.path.insert(0, str(TOOLS_DIR))
from blocker_db import get_db, SCHEMA_SQL

DOCKER_BASE_IMAGE = 'blocker-coverage-base'
DOCKER_TARGET_IMAGE_FMT = 'blocker-{target}-cov'


# ---------------------------------------------------------------------------
# Docker build
# ---------------------------------------------------------------------------

def build_base_image():
    print("Building coverage base image...", file=sys.stderr)
    subprocess.run(
        ['docker', 'build',
         '-f', str(DOCKER_DIR / 'Dockerfile.coverage-base'),
         '-t', DOCKER_BASE_IMAGE, str(PROJECT_DIR)],
        check=True
    )


def build_target_image(target):
    dockerfile = DOCKER_DIR / 'targets' / f'Dockerfile.{target}.cov'
    if not dockerfile.exists():
        print(f"Error: {dockerfile} not found", file=sys.stderr)
        sys.exit(1)
    image_name = DOCKER_TARGET_IMAGE_FMT.format(target=target)
    print(f"Building {image_name}...", file=sys.stderr)
    subprocess.run(
        ['docker', 'build',
         '-f', str(dockerfile), '-t', image_name, str(PROJECT_DIR)],
        check=True
    )
    return image_name


# ---------------------------------------------------------------------------
# Metadata parsing and lineage (runs on host)
# ---------------------------------------------------------------------------

def parse_seed_metadata(queue_dir, seed_name):
    meta_path = os.path.join(queue_dir, f'.{seed_name}.metadata')
    if not os.path.exists(meta_path):
        return None
    try:
        with open(meta_path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    result = {'parent_file': None, 'mutation_ops': [], 'elapsed_ms': None}
    meta_map = data.get('metadata', {}).get('map', {})
    for _key, value in meta_map.items():
        inner = value[1] if isinstance(value, list) and len(value) > 1 else value
        if not isinstance(inner, dict):
            continue
        if 'parent_file' in inner:
            result['parent_file'] = inner.get('parent_file')
            result['elapsed_ms'] = inner.get('elapsed_ms')
        elif 'list' in inner:
            lst = inner['list']
            if lst and isinstance(lst[0], str):
                result['mutation_ops'] = lst
    return result


def build_lineage(queue_dir, seed_name, max_depth=50):
    lineage = []
    current = seed_name
    seen = set()
    for depth in range(max_depth):
        if current in seen:
            break
        seen.add(current)
        meta = parse_seed_metadata(queue_dir, current)
        if meta is None:
            lineage.append({'depth': depth, 'ancestor_id': current, 'mutation_op': None})
            break
        mutation_op = ','.join(meta['mutation_ops']) if meta['mutation_ops'] else None
        lineage.append({'depth': depth, 'ancestor_id': current, 'mutation_op': mutation_op})
        parent = meta.get('parent_file')
        if not parent:
            break
        current = parent
    return lineage


# ---------------------------------------------------------------------------
# DB insertion
# ---------------------------------------------------------------------------

def insert_seeds_and_lineage(branch_id, fuzzer, trial, queue_dir, seed_names,
                             seed_table, lineage_table, db_path=None):
    conn = get_db(db_path)
    conn.executescript(SCHEMA_SQL)
    sc = lc = 0

    for seed_name in seed_names:
        meta = parse_seed_metadata(queue_dir, seed_name)
        conn.execute(f"""
            INSERT INTO {seed_table}
                (branch_id, fuzzer, trial, seed_id, parent_seed_id, mutation_op, discovery_time_s)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(branch_id, fuzzer, trial, seed_id) DO UPDATE SET
                parent_seed_id = excluded.parent_seed_id,
                mutation_op = excluded.mutation_op,
                discovery_time_s = excluded.discovery_time_s
        """, (
            branch_id, fuzzer, trial, seed_name,
            meta['parent_file'] if meta else None,
            ','.join(meta['mutation_ops']) if meta and meta['mutation_ops'] else None,
            int(meta['elapsed_ms'] / 1000) if meta and meta.get('elapsed_ms') else None,
        ))
        sc += 1

        for entry in build_lineage(queue_dir, seed_name):
            conn.execute(f"""
                INSERT INTO {lineage_table}
                    (branch_id, fuzzer, trial, seed_id, depth, ancestor_id, mutation_op)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(branch_id, fuzzer, trial, seed_id, depth) DO UPDATE SET
                    ancestor_id = excluded.ancestor_id, mutation_op = excluded.mutation_op
            """, (branch_id, fuzzer, trial, seed_name,
                  entry['depth'], entry['ancestor_id'], entry['mutation_op']))
            lc += 1

    conn.commit()
    conn.close()
    return sc, lc


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def get_branches_to_process(target, branch_id=None, db_path=None):
    conn = get_db(db_path)
    conn.executescript(SCHEMA_SQL)

    if branch_id:
        branches = conn.execute("""
            SELECT branch_id, file, function, line, col, blocked_side
            FROM branches WHERE target = ? AND branch_id = ?
        """, (target, branch_id)).fetchall()
    else:
        branches = conn.execute("""
            SELECT branch_id, file, function, line, col, blocked_side
            FROM branches WHERE target = ?
        """, (target,)).fetchall()

    result = []
    for b in branches:
        resolving = conn.execute("""
            SELECT fuzzer, MIN(trial) as trial FROM trial_coverage
            WHERE branch_id = ? AND hit_status = 1 GROUP BY fuzzer
        """, (b['branch_id'],)).fetchall()

        blocking = conn.execute("""
            SELECT fuzzer, MIN(trial) as trial FROM trial_coverage
            WHERE branch_id = ? AND hit_status = 0 GROUP BY fuzzer
        """, (b['branch_id'],)).fetchall()

        if resolving:
            result.append({
                'branch_id': b['branch_id'],
                'file': b['file'], 'line': b['line'], 'col': b['col'],
                'blocked_side': b['blocked_side'],
                'resolving_trials': [(t['fuzzer'], t['trial']) for t in resolving],
                'blocking_trials': [(t['fuzzer'], t['trial']) for t in blocking],
            })

    conn.close()
    return result


def build_jobs(branches, queue_base, target):
    """
    Group all (branch, fuzzer, trial) jobs by queue_subdir.
    Returns dict: {queue_subdir: [branch_job, ...]}
    """
    queues = defaultdict(list)

    for branch in branches:
        bid = branch['branch_id']
        other_side = 'F' if branch['blocked_side'] == 'T' else 'T'

        for fuzzer, trial in branch['resolving_trials']:
            subdir = f'{fuzzer}/trial{trial}/queue'
            full = os.path.join(queue_base, target, subdir)
            if os.path.isdir(full):
                queues[subdir].append({
                    'branch_id': bid,
                    'file': branch['file'],
                    'line': branch['line'],
                    'col': branch['col'],
                    'side': branch['blocked_side'],
                    'type': 'resolving',
                })

        for fuzzer, trial in branch.get('blocking_trials', []):
            subdir = f'{fuzzer}/trial{trial}/queue'
            full = os.path.join(queue_base, target, subdir)
            if os.path.isdir(full):
                queues[subdir].append({
                    'branch_id': bid,
                    'file': branch['file'],
                    'line': branch['line'],
                    'col': branch['col'],
                    'side': other_side,
                    'type': 'blocking',
                })

    return dict(queues)


def run_bisection(target, queue_base, branch_id=None, parallel=8,
                  max_seeds=50, batch_size=500, timeout=3600, db_path=None):
    db_path = db_path or str(DB_PATH)
    docker_image = DOCKER_TARGET_IMAGE_FMT.format(target=target)

    result = subprocess.run(
        ['docker', 'image', 'inspect', docker_image], capture_output=True
    )
    if result.returncode != 0:
        print(f"Error: image '{docker_image}' not found. "
              f"Run: python3 tools/seed_bisect.py build --target {target}",
              file=sys.stderr)
        sys.exit(1)

    branches = get_branches_to_process(target, branch_id, db_path)
    if not branches:
        print(f"No branches with resolving trials for '{target}'", file=sys.stderr)
        return

    queue_jobs = build_jobs(branches, queue_base, target)
    total_jobs = sum(len(v) for v in queue_jobs.values())
    print(f"Target {target}: {len(branches)} branches, {len(queue_jobs)} queues, "
          f"{total_jobs} branch-jobs", file=sys.stderr)

    # Write jobs file
    tmpdir = tempfile.mkdtemp(prefix='bisect_batch_')
    jobs_file = os.path.join(tmpdir, 'jobs.json')
    outdir = os.path.join(tmpdir, 'out')
    os.makedirs(outdir)

    jobs_data = {
        'queues': {subdir: {'branches': blist} for subdir, blist in queue_jobs.items()}
    }
    with open(jobs_file, 'w') as f:
        json.dump(jobs_data, f)

    queue_target_dir = os.path.join(queue_base, target)
    results_file = os.path.join(outdir, 'results.json')

    container_timeout_args = f' --timeout {timeout}' if timeout > 0 else ''
    cmd = [
        'docker', 'run', '--rm', '--entrypoint', '',
        '-v', f'{os.path.abspath(queue_target_dir)}:/queues:ro',
        '-v', f'{os.path.abspath(tmpdir)}:/work',
        docker_image,
        '/bin/bash', '-c',
        f'python3 /seed_scanner.py'
        f' --jobs /work/jobs.json'
        f' --queues /queues'
        f' --fuzz-bin "$FUZZ_BIN"'
        f' --output /work/out/results.json'
        f' --max-seeds {max_seeds}'
        f' --batch-size {batch_size}'
        + container_timeout_args
    ]

    print(f"Starting container...", file=sys.stderr)
    t0 = time.time()

    host_timeout = timeout + 60 if timeout > 0 else None
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=host_timeout
        )
        if proc.stderr:
            for line in proc.stderr.strip().splitlines():
                print(f"  {line}", file=sys.stderr)
    except subprocess.TimeoutExpired:
        print(f"Container timed out", file=sys.stderr)

    elapsed = time.time() - t0
    print(f"Container finished in {elapsed:.1f}s", file=sys.stderr)

    # Parse results
    if not os.path.exists(results_file):
        print("No results file", file=sys.stderr)
        shutil.rmtree(tmpdir, ignore_errors=True)
        return

    with open(results_file) as f:
        data = json.load(f)

    total_seeds = total_lineage = 0

    for r in data.get('results', []):
        hitting = r.get('hitting_seeds', [])
        if not hitting:
            continue

        bid = r['branch_id']
        parts = r['queue_subdir'].split('/')
        fuzzer = parts[0]
        trial = int(parts[1].replace('trial', ''))
        queue_dir = os.path.join(queue_base, target, r['queue_subdir'])

        if r['type'] == 'resolving':
            st, lt = 'resolving_seeds', 'resolving_seed_lineage'
        else:
            st, lt = 'blocking_seeds', 'blocking_seed_lineage'

        sc, lc = insert_seeds_and_lineage(
            bid, fuzzer, trial, queue_dir, hitting,
            seed_table=st, lineage_table=lt, db_path=db_path
        )
        total_seeds += sc
        total_lineage += lc

    print(f"\nDone. {total_seeds} seeds, {total_lineage} lineage entries",
          file=sys.stderr)
    shutil.rmtree(tmpdir, ignore_errors=True)


def plan_bisection(target, queue_base, branch_id=None, db_path=None):
    db_path = db_path or str(DB_PATH)
    branches = get_branches_to_process(target, branch_id, db_path)
    if not branches:
        print(f"No branches for '{target}'")
        return
    queue_jobs = build_jobs(branches, queue_base, target)
    total_jobs = sum(len(v) for v in queue_jobs.values())
    print(f"# Plan — {target}")
    print(f"Branches: {len(branches)}")
    print(f"Queues: {len(queue_jobs)}")
    print(f"Branch-jobs: {total_jobs}")
    print(f"Containers: 1")
    print()
    for subdir, blist in sorted(queue_jobs.items()):
        queue_dir = os.path.join(queue_base, target, subdir)
        n_seeds = len([f for f in os.listdir(queue_dir) if not f.startswith('.')])
        n_res = sum(1 for b in blist if b['type'] == 'resolving')
        n_blk = sum(1 for b in blist if b['type'] == 'blocking')
        print(f"  {subdir}: {n_seeds} seeds, {n_res} resolving + {n_blk} blocking branches")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Seed bisection')
    sub = parser.add_subparsers(dest='command')

    p_build = sub.add_parser('build')
    p_build.add_argument('--target', required=True)

    p_run = sub.add_parser('run')
    p_run.add_argument('--target', required=True)
    p_run.add_argument('--queue-base', required=True)
    p_run.add_argument('--branch-id', type=int)
    p_run.add_argument('--parallel', type=int, default=8)
    p_run.add_argument('--max-seeds', type=int, default=50)
    p_run.add_argument('--batch-size', type=int, default=500,
                       help='Seeds per fuzz_bin invocation (default: 500)')
    p_run.add_argument('--timeout', type=int, default=3600,
                       help='Total timeout in seconds (default: 3600)')
    p_run.add_argument('--db')

    p_plan = sub.add_parser('plan')
    p_plan.add_argument('--target', required=True)
    p_plan.add_argument('--queue-base', required=True)
    p_plan.add_argument('--branch-id', type=int)
    p_plan.add_argument('--db')

    args = parser.parse_args()

    if args.command == 'build':
        build_base_image()
        build_target_image(args.target)
    elif args.command == 'run':
        run_bisection(
            args.target, args.queue_base,
            branch_id=args.branch_id,
            parallel=args.parallel,
            max_seeds=args.max_seeds,
            batch_size=args.batch_size,
            timeout=args.timeout,
            db_path=args.db,
        )
    elif args.command == 'plan':
        plan_bisection(args.target, args.queue_base,
                       branch_id=args.branch_id, db_path=args.db)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
