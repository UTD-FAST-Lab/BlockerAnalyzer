#!/usr/bin/env python3
"""
seed_bisect.py — Find seeds that hit blocking branches.

Runs ONE Docker container per target. Inside, for each unique queue
(fuzzer/trial), scans all seeds once and checks ALL target branches.
Much faster than per-branch bisection.

Usage:
    python3 tools/seed_bisect.py build --target bloaty
    python3 tools/seed_bisect.py run --target bloaty --queue-base ./out \
        --branches-from-csv csvs/blocker_representatives.csv
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
from blocker_db import get_db

DOCKER_BASE_IMAGE = 'libafl-coverage-base'
DOCKER_TARGET_IMAGE_FMT = 'libafl-{target}-cov'


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

def _decisive_fuzzers_for_branch(conn, branch_id, winner_thr=8, loser_thr=8):
    """From the branch's DECISIVE pairs, return (resolving, blocking) where
    each is {fuzzer: sorted([trial, ...])}.

    A canonical pair (subject A,B) is decisive at this branch iff
    (n_A_resolved >= winner_thr AND n_B_blocked >= loser_thr) — winner A, loser B
    — or the symmetric B>A case (anti-direction). resolving = the decisive
    WINNERS (with their resolved-trial lists), blocking = the decisive LOSERS
    (with their blocked-trial lists). This matches build_candidates' >=8/8 rule,
    so we scan exactly the fuzzers that define the branch's divergence — not all
    10, and not the arbitrary lex-min one. A fuzzer cannot be both winner and
    loser here (>=8 resolved AND >=8 blocked is impossible at n=10). Trials are
    unioned across pairs where a fuzzer wins/loses in more than one subject.
    """
    rows = conn.execute("""
        SELECT s.A, s.B,
               sb.n_A_resolved, sb.n_A_blocked, sb.n_B_resolved, sb.n_B_blocked,
               sb.A_resolved_trials, sb.A_blocked_trials,
               sb.B_resolved_trials, sb.B_blocked_trials
          FROM subject_branches sb JOIN study_subjects s USING (subject_id)
         WHERE sb.branch_id = ?
    """, (branch_id,)).fetchall()

    resolving, blocking = {}, {}
    for r in rows:
        if r['n_A_resolved'] >= winner_thr and r['n_B_blocked'] >= loser_thr:
            w, wtr = r['A'], json.loads(r['A_resolved_trials'] or '[]')
            l, ltr = r['B'], json.loads(r['B_blocked_trials'] or '[]')
        elif r['n_B_resolved'] >= winner_thr and r['n_A_blocked'] >= loser_thr:
            w, wtr = r['B'], json.loads(r['B_resolved_trials'] or '[]')
            l, ltr = r['A'], json.loads(r['A_blocked_trials'] or '[]')
        else:
            continue  # pair not decisive at this branch
        if wtr:
            resolving.setdefault(w, set()).update(wtr)
        if ltr:
            blocking.setdefault(l, set()).update(ltr)

    return ({fz: sorted(ts) for fz, ts in resolving.items()},
            {fz: sorted(ts) for fz, ts in blocking.items()})


def get_branches_to_process(target, branch_id=None, db_path=None,
                            branch_ids=None, winner_thr=8, loser_thr=8,
                            trial_rank=0):
    """Pull branch metadata + the DECISIVE-pair (fuzzer, trial)s per direction.

    Args:
        target: target name (e.g. "curl").
        branch_id: single branch id, or None.
        branch_ids: iterable of branch ids to scope work, or None for ALL
                    branches in the target. Mutually exclusive with branch_id.
        winner_thr/loser_thr: decisive-pair thresholds (default 8/8, matching
                    build_candidates).

    Each branch yields ALL decisive WINNERS as resolving (fuzzer, trial)s and
    ALL decisive LOSERS as blocking (fuzzer, trial)s — one representative trial
    (lex-min) per fuzzer. This scans exactly the fuzzers that define the
    branch's divergence (so per-fuzzer positives/negatives + lineage are
    captured for every decisive arm), not the single arbitrary lex-min fuzzer
    the previous version picked, and not all 10.
    """
    conn = get_db(db_path)

    if branch_id:
        branches = conn.execute("""
            SELECT branch_id, file, line, col, blocked_side
            FROM branches WHERE target = ? AND branch_id = ?
        """, (target, branch_id)).fetchall()
    elif branch_ids:
        ids = list(branch_ids)
        if not ids:
            conn.close()
            return []
        placeholders = ",".join("?" * len(ids))
        branches = conn.execute(f"""
            SELECT branch_id, file, line, col, blocked_side
            FROM branches WHERE target = ? AND branch_id IN ({placeholders})
        """, [target, *ids]).fetchall()
    else:
        branches = conn.execute("""
            SELECT branch_id, file, line, col, blocked_side
            FROM branches WHERE target = ?
        """, (target,)).fetchall()

    result = []
    for b in branches:
        resolving, blocking = _decisive_fuzzers_for_branch(
            conn, b['branch_id'], winner_thr, loser_thr)
        if not resolving:
            continue  # no decisive pair at this branch (shouldn't happen for reps)
        # The trial_rank-th trial (lex-min order) per decisive fuzzer per
        # direction. rank 0 = primary; rank 1+ = fallback for branches whose
        # primary-trial queue returned no hitting seed. Fuzzers with fewer than
        # trial_rank+1 trials of that outcome are skipped at this rank.
        resolving_trials = sorted((fz, ts[trial_rank]) for fz, ts in resolving.items()
                                  if len(ts) > trial_rank)
        blocking_trials  = sorted((fz, ts[trial_rank]) for fz, ts in blocking.items()
                                  if len(ts) > trial_rank)
        if not resolving_trials and not blocking_trials:
            continue  # no fuzzer has a trial at this rank
        result.append({
            'branch_id': b['branch_id'],
            'file': b['file'], 'line': b['line'], 'col': b['col'],
            'blocked_side': b['blocked_side'],
            'resolving_trials': resolving_trials,
            'blocking_trials':  blocking_trials,
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


RESULTS_DIR = PROJECT_DIR / 'db' / 'bisect_results'


def _build_sampled_queue_mirror(queue_target_dir, queue_subdirs,
                                sample_size, tmpdir):
    """Create a temp dir mirroring the queue layout but with at most
    sample_size symlinks per queue (random sample). Returns the mirror
    path. If sample_size is 0 or None, returns the original path."""
    if not sample_size:
        return os.path.abspath(queue_target_dir)
    import random
    mirror = os.path.join(tmpdir, 'sampled_queues')
    os.makedirs(mirror, exist_ok=True)
    for subdir in queue_subdirs:
        src = os.path.join(queue_target_dir, subdir)
        if not os.path.isdir(src):
            continue
        dst = os.path.join(mirror, subdir)
        os.makedirs(dst, exist_ok=True)
        seeds = [f for f in os.listdir(src)
                 if not f.startswith('.') and os.path.isfile(os.path.join(src, f))]
        if len(seeds) > sample_size:
            seeds = random.sample(seeds, sample_size)
        for s in seeds:
            try:
                os.symlink(os.path.join(os.path.abspath(src), s),
                           os.path.join(dst, s))
            except FileExistsError:
                pass
    return mirror


def scan_bisection(target, queue_base, branch_id=None,
                   max_seeds=10, batch_size=500, db_path=None,
                   branch_ids=None, queue_sample_size=None, trial_rank=0):
    """Run Docker bisection only — write results.json, no DB writes.

    queue_sample_size: if set, randomly sample at most this many seeds per
    queue before bisection. Massively speeds up scans on huge queues
    (sqlite3/bloaty have ~100K+ seeds per queue at n=10) at the cost of
    possibly missing rare hits. Insert phase reads from the original (full)
    queue, so metadata + lineage tracing is unaffected."""
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

    branches = get_branches_to_process(target, branch_id, db_path, branch_ids,
                                       trial_rank=trial_rank)
    if not branches:
        print(f"No branches with resolving trials for '{target}' (trial_rank={trial_rank})",
              file=sys.stderr)
        return

    queue_jobs = build_jobs(branches, queue_base, target)
    total_jobs = sum(len(v) for v in queue_jobs.values())
    print(f"Target {target}: {len(branches)} branches, {len(queue_jobs)} queues, "
          f"{total_jobs} branch-jobs", file=sys.stderr)
    if queue_sample_size:
        print(f"  queue sample size: {queue_sample_size} seeds/queue",
              file=sys.stderr)

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
    queues_mount = _build_sampled_queue_mirror(
        queue_target_dir, list(queue_jobs.keys()), queue_sample_size, tmpdir,
    )
    tmp_results_file = os.path.join(outdir, 'results.json')

    # Build the mount list. When sampling is on, the symlink mirror points
    # to absolute host paths (e.g., /20TB/...); the container needs that
    # path bind-mounted at the SAME path so symlinks resolve.
    mounts = [
        '-v', f'{queues_mount}:/queues:ro',
        '-v', f'{os.path.abspath(tmpdir)}:/work',
        # Bind-mount the scanner so it's available at /seed_scanner.py inside
        # the container without rebuilding the image. The same script is also
        # COPY'd into Dockerfile.coverage-base for fresh builds; the bind-mount
        # just overrides whatever's in the image with the on-disk version.
        '-v', f'{os.path.abspath(DOCKER_DIR / "bisect_in_container.py")}:/seed_scanner.py:ro',
    ]
    if queue_sample_size:
        host_queue_abs = os.path.abspath(queue_target_dir)
        mounts.extend(['-v', f'{host_queue_abs}:{host_queue_abs}:ro'])

    cmd = [
        'docker', 'run', '--rm', '--entrypoint', '',
        *mounts,
        docker_image,
        '/bin/bash', '-c',
        f'python3 /seed_scanner.py'
        f' --jobs /work/jobs.json'
        f' --queues /queues'
        f' --fuzz-bin "$FUZZ_BIN"'
        f' --output /work/out/results.json'
        f' --max-seeds {max_seeds}'
        f' --batch-size {batch_size}'
        f' --timeout 0'
    ]

    print(f"Starting container (no timeout)...", file=sys.stderr)
    t0 = time.time()

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.stderr:
        for line in proc.stderr.strip().splitlines():
            print(f"  {line}", file=sys.stderr)

    elapsed = time.time() - t0
    print(f"Container finished in {elapsed:.1f}s", file=sys.stderr)

    if not os.path.exists(tmp_results_file):
        print("No results file produced", file=sys.stderr)
        shutil.rmtree(tmpdir, ignore_errors=True)
        return

    # Copy results to stable location
    os.makedirs(RESULTS_DIR, exist_ok=True)
    suffix = f'_{branch_id}' if branch_id else ''
    out_path = RESULTS_DIR / f'{target}{suffix}_results.json'
    shutil.copy2(tmp_results_file, out_path)
    shutil.rmtree(tmpdir, ignore_errors=True)

    with open(out_path) as f:
        data = json.load(f)
    total = sum(len(r.get('hitting_seeds', [])) for r in data.get('results', []))
    print(f"\nScan done. {total} seeds found. Results: {out_path}", file=sys.stderr)


def insert_results(target, results_path, queue_base, db_path=None):
    """Read results.json and insert seeds + lineage into the DB."""
    db_path = db_path or str(DB_PATH)

    with open(results_path) as f:
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

    print(f"Inserted {total_seeds} seeds, {total_lineage} lineage entries "
          f"for '{target}'", file=sys.stderr)


def _all_branch_ids(target, db_path):
    conn = get_db(db_path)
    ids = [r[0] for r in conn.execute(
        "SELECT branch_id FROM branches WHERE target = ?", (target,))]
    conn.close()
    return ids


def _branches_missing_seeds(target, ids, db_path):
    """Subset of `ids` with 0 resolving seeds OR 0 blocking seeds — i.e. a
    branch that didn't get at least one seed in each direction."""
    if not ids:
        return []
    conn = get_db(db_path)
    ph = ",".join("?" * len(ids))
    have_r = {r[0] for r in conn.execute(
        f"SELECT DISTINCT branch_id FROM resolving_seeds WHERE branch_id IN ({ph})", list(ids))}
    have_b = {r[0] for r in conn.execute(
        f"SELECT DISTINCT branch_id FROM blocking_seeds WHERE branch_id IN ({ph})", list(ids))}
    conn.close()
    return [i for i in ids if i not in have_r or i not in have_b]


def _total_seeds(target, ids, db_path):
    if not ids:
        return 0
    conn = get_db(db_path)
    ph = ",".join("?" * len(ids))
    n = 0
    for t in ("resolving_seeds", "blocking_seeds"):
        n += conn.execute(
            f"SELECT COUNT(*) FROM {t} WHERE branch_id IN ({ph})", list(ids)).fetchone()[0]
    conn.close()
    return n


def run_bisection(target, queue_base, branch_id=None,
                  max_seeds=10, batch_size=500, db_path=None,
                  branch_ids=None, queue_sample_size=None, fallback_ranks=3):
    """Scan + insert, with a trial-fallback: branches whose primary
    decisive-fuzzer queue returns no hitting seed are re-scanned against
    successive trials of the same fuzzers until they get a seed in each
    direction or the fallback budget / available trials run out."""
    db_path = db_path or str(DB_PATH)
    suffix = f'_{branch_id}' if branch_id else ''
    results_path = RESULTS_DIR / f'{target}{suffix}_results.json'

    def scan_insert(ids, rank):
        # Clear any stale results so a no-op scan can't re-insert a prior phase.
        if results_path.exists():
            results_path.unlink()
        scan_bisection(target, queue_base, branch_id=branch_id,
                       max_seeds=max_seeds, batch_size=batch_size, db_path=db_path,
                       branch_ids=ids, queue_sample_size=queue_sample_size,
                       trial_rank=rank)
        if results_path.exists():
            insert_results(target, str(results_path), queue_base, db_path=db_path)

    # Phase 0: primary (lex-min) trial per decisive fuzzer.
    scan_insert(branch_ids, 0)

    # Trial-fallback (multi-branch path only).
    if branch_id is None and fallback_ranks > 0:
        pool = list(branch_ids) if branch_ids else _all_branch_ids(target, db_path)
        for rank in range(1, fallback_ranks + 1):
            missing = _branches_missing_seeds(target, pool, db_path)
            if not missing:
                print(f"  fallback: all {len(pool)} branches have seeds in both "
                      f"directions (after rank {rank-1})", file=sys.stderr)
                break
            print(f"  fallback rank {rank}: {len(missing)} branches still missing "
                  f"a direction; retrying next trial", file=sys.stderr)
            before = _total_seeds(target, missing, db_path)
            scan_insert(sorted(missing), rank)
            if _total_seeds(target, missing, db_path) == before:
                print(f"  fallback: no new seeds at rank {rank} (trials exhausted); "
                      f"stopping", file=sys.stderr)
                break


def plan_bisection(target, queue_base, branch_id=None, db_path=None,
                   branch_ids=None):
    db_path = db_path or str(DB_PATH)
    branches = get_branches_to_process(target, branch_id, db_path, branch_ids)
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

    p_scan = sub.add_parser('scan', help='Run Docker bisection only (no DB writes)')
    p_scan.add_argument('--target', required=True)
    p_scan.add_argument('--queue-base', required=True)
    p_scan.add_argument('--branch-id', type=int)
    p_scan.add_argument('--branches-from-csv',
                        help='CSV with target,branch_id columns (e.g. '
                             'csvs/blocker_representatives.csv); scopes scan '
                             'to rows whose target column matches --target')
    p_scan.add_argument('--max-seeds', type=int, default=10)
    p_scan.add_argument('--batch-size', type=int, default=500,
                        help='Seeds per fuzz_bin invocation (default: 500)')
    p_scan.add_argument('--queue-sample-size', type=int, default=0,
                        help='If >0, randomly sample at most N seeds per '
                             'queue before bisection. Speeds up scans on '
                             'huge queues (sqlite3/bloaty ~100K+) at the '
                             'cost of possibly missing rare hits. 0 = no '
                             'sampling (use full queue).')
    p_scan.add_argument('--db')

    p_insert = sub.add_parser('insert', help='Insert results.json into DB')
    p_insert.add_argument('--target', required=True)
    p_insert.add_argument('--results', required=True, help='Path to results.json')
    p_insert.add_argument('--queue-base', required=True)
    p_insert.add_argument('--db')

    p_run = sub.add_parser('run', help='Scan + insert in one step')
    p_run.add_argument('--target', required=True)
    p_run.add_argument('--queue-base', required=True)
    p_run.add_argument('--branch-id', type=int)
    p_run.add_argument('--branches-from-csv',
                       help='CSV with target,branch_id columns (e.g. '
                            'csvs/blocker_representatives.csv); scopes work '
                            'to rows whose target matches --target')
    p_run.add_argument('--max-seeds', type=int, default=10)
    p_run.add_argument('--batch-size', type=int, default=500,
                       help='Seeds per fuzz_bin invocation (default: 500)')
    p_run.add_argument('--queue-sample-size', type=int, default=0,
                       help='If >0, randomly sample at most N seeds per '
                            'queue before bisection. 0 = no sampling.')
    p_run.add_argument('--fallback-ranks', type=int, default=3,
                       help='Trial-fallback budget: re-scan branches missing a '
                            'direction against up to N successive trials of '
                            'their decisive fuzzers (default 3; 0 = disable).')
    p_run.add_argument('--db')

    p_plan = sub.add_parser('plan', help='Dry-run: show queues and branch counts')
    p_plan.add_argument('--target', required=True)
    p_plan.add_argument('--queue-base', required=True)
    p_plan.add_argument('--branch-id', type=int)
    p_plan.add_argument('--branches-from-csv',
                        help='CSV with target,branch_id columns (e.g. '
                             'csvs/blocker_representatives.csv)')
    p_plan.add_argument('--db')

    args = parser.parse_args()

    branch_ids = None
    if getattr(args, 'branches_from_csv', None):
        import csv
        with open(args.branches_from_csv) as f:
            branch_ids = [
                int(r['branch_id'])
                for r in csv.DictReader(f)
                if r.get('target') == args.target
            ]
        print(f"loaded {len(branch_ids)} branch ids from "
              f"{args.branches_from_csv} (target={args.target})",
              file=sys.stderr)
        if not branch_ids:
            print(f"  no rows for target={args.target}; nothing to do",
                  file=sys.stderr)
            return

    if args.command == 'build':
        build_base_image()
        build_target_image(args.target)
    elif args.command == 'scan':
        scan_bisection(
            args.target, args.queue_base,
            branch_id=args.branch_id,
            max_seeds=args.max_seeds,
            batch_size=args.batch_size,
            db_path=args.db,
            branch_ids=branch_ids,
            queue_sample_size=args.queue_sample_size,
        )
    elif args.command == 'insert':
        insert_results(args.target, args.results, args.queue_base,
                       db_path=args.db)
    elif args.command == 'run':
        run_bisection(
            args.target, args.queue_base,
            branch_id=args.branch_id,
            max_seeds=args.max_seeds,
            batch_size=args.batch_size,
            db_path=args.db,
            branch_ids=branch_ids,
            queue_sample_size=args.queue_sample_size,
            fallback_ranks=args.fallback_ranks,
        )
    elif args.command == 'plan':
        plan_bisection(args.target, args.queue_base,
                       branch_id=args.branch_id, db_path=args.db,
                       branch_ids=branch_ids)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
