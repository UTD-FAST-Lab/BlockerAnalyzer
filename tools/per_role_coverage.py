#!/usr/bin/env python3
"""
per_role_coverage.py — generate per-role (W winner-resolving / L
loser-blocking) annotated source coverage per branch.

For each branch with decisive pairs, unions the winner-resolving seeds
across all decisive winner fuzzers (from `resolving_seeds`) and the
loser-blocking seeds across all decisive losers (from `blocking_seeds`),
then runs each set through `libafl-<target>-cov` to produce an
`llvm-cov show` annotated dump of the branch's enclosing source file.

The dumps power the SOURCE CONTEXT overlay in evidence-per-branch:
the host parser extracts per-line hit counts and emits a `[W]`/`[L]`/
`[B]`/`[ ]` diff over the enclosing function (and 1-hop callers).

Cache layout:
    db/per_role_coverage/<target>/<branch_id>/
        W/branch_coverage_show.txt
        W/cache_key.txt        # sha1 of sorted winner seed_ids + file list
        W/status.txt           # 'ok' | 'no_seeds' | 'failed: ...'
        L/...                  # same for losers

Cache is invalidated when sha1 differs (e.g., seed_bisect re-run added
new seeds). Both W and L must be 'ok' for the overlay to use the cache;
otherwise evidence-per-branch falls back to the static ±N source window.

Usage:
    python3 tools/per_role_coverage.py plan    --target curl
    python3 tools/per_role_coverage.py generate --target curl
    python3 tools/per_role_coverage.py generate --target curl \
        --branches-from-csv csvs/blocker_representatives.csv
    python3 tools/per_role_coverage.py status  --target curl
"""

import argparse
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = TOOLS_DIR.parent
DB_PATH = PROJECT_DIR / 'db' / 'blockers.sqlite'
DOCKER_DIR = PROJECT_DIR / 'docker'
CACHE_DIR = PROJECT_DIR / 'db' / 'per_role_coverage'
CALLERS_INDEX_DIR = PROJECT_DIR / 'db' / 'callers_index'
DEFAULT_QUEUE_BASE = PROJECT_DIR / 'out'
DOCKER_TARGET_IMAGE_FMT = 'libafl-{target}-cov'

sys.path.insert(0, str(TOOLS_DIR))
from blocker_db import get_db


_CALLERS_CACHE = {}


def _load_callers_index(target):
    """Return {callee_func: [caller_entry, ...]} or {} if missing."""
    if target in _CALLERS_CACHE:
        return _CALLERS_CACHE[target]
    p = CALLERS_INDEX_DIR / f'{target}.json'
    if not p.is_file():
        _CALLERS_CACHE[target] = {}
        return {}
    data = json.load(p.open())
    _CALLERS_CACHE[target] = data.get('callers', {})
    return _CALLERS_CACHE[target]


def _caller_files_for(target, enclosing_name, max_files=8):
    """Files of 1-hop callers of `enclosing_name` per the index.
    Deduped, ordered by frequency of appearance. Empty if no index.
    """
    callers = _load_callers_index(target).get(enclosing_name, [])
    if not callers:
        return []
    seen = []
    for c in callers:
        f = c.get('file')
        if f and f not in seen:
            seen.append(f)
        if len(seen) >= max_files:
            break
    return seen


# ---------------------------------------------------------------------------
# DB queries
# ---------------------------------------------------------------------------

def _decisive_pairs_per_branch(conn, target, branch_ids,
                               winner_thr=8, loser_thr=8, admissible_only=True):
    """For each branch, return {(winner_fz, loser_fz), ...} = decisive pairs.

    Mirrors evidence-per-branch's pair-detection logic. Used to pick which
    fuzzers' seeds go into the W and L sets for the coverage runs.
    """
    where_extra = " AND s.admissible = 1" if admissible_only else ""
    placeholders = ",".join("?" * len(branch_ids)) if branch_ids else None
    if placeholders:
        target_filter = f" AND b.target = ? AND sb.branch_id IN ({placeholders})"
        params = [winner_thr, loser_thr, winner_thr, loser_thr, target, *branch_ids]
    else:
        target_filter = " AND b.target = ?"
        params = [winner_thr, loser_thr, winner_thr, loser_thr, target]

    rows = conn.execute(
        f"""SELECT sb.branch_id, s.A, s.B,
                   sb.n_A_resolved, sb.n_A_blocked,
                   sb.n_B_resolved, sb.n_B_blocked
              FROM subject_branches sb
              JOIN study_subjects s USING(subject_id)
              JOIN branches b ON b.branch_id = sb.branch_id
             WHERE ((sb.n_A_resolved >= ? AND sb.n_B_blocked >= ?)
                 OR (sb.n_B_resolved >= ? AND sb.n_A_blocked >= ?))
                  {where_extra}
                  {target_filter}""",
        params,
    ).fetchall()

    by_branch = {}
    for bid, A, B, A_res, A_blk, B_res, B_blk in rows:
        if A_res >= winner_thr and B_blk >= loser_thr:
            winner, loser = A, B
        else:
            winner, loser = B, A
        by_branch.setdefault(bid, set()).add((winner, loser))
    return by_branch


def _seeds_for_role(conn, branch_id, table):
    """Return [(fuzzer, trial, seed_id)] from `table` for this branch.

    table is 'resolving_seeds' or 'blocking_seeds'. We do NOT filter by
    fuzzer: seed_bisect picks one (fuzzer, trial) per direction by
    lex-min, which is often a non-decisive fuzzer for shapes like --BR.
    The side the seed takes (winning vs losing) is what matters for the
    coverage overlay; the fuzzer that produced it is incidental.
    """
    rows = conn.execute(
        f"""SELECT fuzzer, trial, seed_id
              FROM {table}
             WHERE branch_id = ?
             ORDER BY fuzzer, trial, discovery_time_s, seed_id""",
        [branch_id],
    ).fetchall()
    return [(r[0], r[1], r[2]) for r in rows]


def _file_for_branch(conn, branch_id):
    row = conn.execute(
        "SELECT target, file, function FROM branches WHERE branch_id = ?",
        (branch_id,)
    ).fetchone()
    if not row:
        return None, None, None
    return row[0], row[1], row[2]


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------

def _cache_key(seed_ids, files):
    h = hashlib.sha1()
    for s in sorted(seed_ids):
        h.update(s.encode() + b'\n')
    h.update(b'--files--\n')
    for f in sorted(files):
        h.update(f.encode() + b'\n')
    return h.hexdigest()


def _cache_paths(target, branch_id, role):
    base = CACHE_DIR / target / str(branch_id) / role
    return {
        'dir':     base,
        'report':  base / 'branch_coverage_show.txt',
        'cache':   base / 'cache_key.txt',
        'status':  base / 'status.txt',
    }


def _cache_hit(target, branch_id, role, expected_key):
    paths = _cache_paths(target, branch_id, role)
    if not paths['cache'].is_file():
        return False
    return paths['cache'].read_text().strip() == expected_key


def _write_cache_meta(target, branch_id, role, key, status):
    paths = _cache_paths(target, branch_id, role)
    paths['dir'].mkdir(parents=True, exist_ok=True)
    paths['cache'].write_text(key + '\n')
    if status is not None:
        paths['status'].write_text(status + '\n')


# ---------------------------------------------------------------------------
# Job building
# ---------------------------------------------------------------------------

def build_jobs(target, branch_ids, queue_base, force=False,
               winner_thr=8, loser_thr=8, admissible_only=True,
               db_path=None):
    """Build the in-container jobs.json + per-job cache_key plan.

    Returns (jobs_dict, planned_keys) where planned_keys is
    {(branch_id, role): cache_key} for entries we expect to write.
    Branches whose W and L caches are both hit get omitted from jobs.
    """
    conn = get_db(db_path)
    pairs_by_branch = _decisive_pairs_per_branch(
        conn, target, branch_ids,
        winner_thr=winner_thr, loser_thr=loser_thr,
        admissible_only=admissible_only,
    )

    jobs = {'branches': []}
    planned_keys = {}
    skipped = 0

    for bid in branch_ids:
        if bid not in pairs_by_branch:
            continue  # no decisive pair under thresholds
        tgt, file_path, function = _file_for_branch(conn, bid)
        if tgt is None or tgt != target:
            continue
        w_seeds_db = _seeds_for_role(conn, bid, 'resolving_seeds')
        l_seeds_db = _seeds_for_role(conn, bid, 'blocking_seeds')

        # Cov dump includes the blocker's file plus the files of any 1-hop
        # callers known from the callers index — so the overlay can render
        # cross-file caller annotations from the same cached report.
        files = [file_path]
        for cf in _caller_files_for(target, function):
            if cf not in files:
                files.append(cf)

        w_key = _cache_key([s[2] for s in w_seeds_db], files)
        l_key = _cache_key([s[2] for s in l_seeds_db], files)

        planned_keys[(bid, 'W')] = w_key
        planned_keys[(bid, 'L')] = l_key

        w_hit = (not force) and _cache_hit(target, bid, 'W', w_key)
        l_hit = (not force) and _cache_hit(target, bid, 'L', l_key)
        if w_hit and l_hit:
            skipped += 1
            continue

        def _pack(seeds):
            return [{'queue_subdir': f'{fz}/trial{tr}/queue', 'name': sid}
                    for (fz, tr, sid) in seeds]

        jobs['branches'].append({
            'branch_id': bid,
            'files': files,
            'W_seeds': _pack(w_seeds_db) if not w_hit else [],
            'L_seeds': _pack(l_seeds_db) if not l_hit else [],
            'W_role_skip': w_hit,
            'L_role_skip': l_hit,
        })

    conn.close()
    return jobs, planned_keys, skipped


# ---------------------------------------------------------------------------
# Docker run
# ---------------------------------------------------------------------------

def run_container(target, jobs, queue_base):
    docker_image = DOCKER_TARGET_IMAGE_FMT.format(target=target)
    proc = subprocess.run(['docker', 'image', 'inspect', docker_image],
                          capture_output=True)
    if proc.returncode != 0:
        print(f"Error: image '{docker_image}' not found. "
              f"Run: python3 tools/seed_bisect.py build --target {target}",
              file=sys.stderr)
        sys.exit(1)

    tmpdir = tempfile.mkdtemp(prefix='per_role_cov_')
    jobs_file = os.path.join(tmpdir, 'jobs.json')
    out_root  = os.path.join(tmpdir, 'out')
    os.makedirs(out_root)
    with open(jobs_file, 'w') as f:
        json.dump(jobs, f)

    queue_target_dir = os.path.abspath(os.path.join(queue_base, target))
    container_script = os.path.abspath(DOCKER_DIR / 'per_role_in_container.py')

    cmd = [
        'docker', 'run', '--rm', '--entrypoint', '',
        '-v', f'{queue_target_dir}:/queues:ro',
        '-v', f'{os.path.abspath(tmpdir)}:/work',
        '-v', f'{container_script}:/per_role_cov.py:ro',
        docker_image,
        '/bin/bash', '-c',
        'python3 /per_role_cov.py'
        ' --jobs /work/jobs.json --queues /queues'
        ' --fuzz-bin "$FUZZ_BIN"'
        ' --outdir /work/out',
    ]
    t0 = time.time()
    print(f"Starting container for {target} "
          f"({len(jobs.get('branches', []))} branches)...", file=sys.stderr)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.stderr:
        for line in proc.stderr.strip().splitlines():
            print(f"  {line}", file=sys.stderr)
    print(f"Container finished in {time.time() - t0:.1f}s", file=sys.stderr)
    return tmpdir, out_root


def harvest_outputs(out_root, target, jobs, planned_keys):
    """Copy container outputs into the cache, then clean up tmpdir."""
    for br in jobs.get('branches', []):
        bid = br['branch_id']
        for role in ('W', 'L'):
            if br.get(f'{role}_role_skip'):
                continue
            src_dir = Path(out_root) / str(bid) / role
            paths = _cache_paths(target, bid, role)
            paths['dir'].mkdir(parents=True, exist_ok=True)
            src_report = src_dir / 'branch_coverage_show.txt'
            src_status = src_dir / 'status.txt'
            if src_report.is_file():
                shutil.copy2(src_report, paths['report'])
            status = (src_status.read_text().strip()
                      if src_status.is_file() else 'failed: missing status')
            key = planned_keys[(bid, role)]
            _write_cache_meta(target, bid, role, key, status)


# ---------------------------------------------------------------------------
# Subcommand wiring
# ---------------------------------------------------------------------------

def _load_branch_ids(target, csv_path, single_id):
    if single_id:
        return [int(single_id)]
    if csv_path:
        with open(csv_path) as f:
            return [int(r['branch_id']) for r in csv.DictReader(f)
                    if r.get('target') == target]
    return []


def cmd_plan(args):
    branch_ids = _load_branch_ids(args.target, args.branches_from_csv,
                                  args.branch_id)
    if not branch_ids:
        print(f"no branch ids for target={args.target}", file=sys.stderr)
        return
    jobs, _, skipped = build_jobs(
        args.target, branch_ids, args.queue_base,
        force=args.force,
        winner_thr=args.winner_threshold,
        loser_thr=args.loser_threshold,
        admissible_only=args.admissible_only,
        db_path=args.db,
    )
    n = len(jobs['branches'])
    print(f"# Plan — {args.target}")
    print(f"Branches considered: {len(branch_ids)}")
    print(f"Branches with decisive pairs: {n + skipped}")
    print(f"Cache hits (skipped): {skipped}")
    print(f"To generate: {n}")
    for br in jobs['branches'][:10]:
        w = 'skip' if br['W_role_skip'] else f"{len(br['W_seeds'])} seeds"
        l = 'skip' if br['L_role_skip'] else f"{len(br['L_seeds'])} seeds"
        print(f"  br{br['branch_id']:>5}  W={w:>14}  L={l}")
    if n > 10:
        print(f"  ... and {n - 10} more")


def cmd_generate(args):
    branch_ids = _load_branch_ids(args.target, args.branches_from_csv,
                                  args.branch_id)
    if not branch_ids:
        print(f"no branch ids for target={args.target}", file=sys.stderr)
        return
    jobs, planned_keys, skipped = build_jobs(
        args.target, branch_ids, args.queue_base,
        force=args.force,
        winner_thr=args.winner_threshold,
        loser_thr=args.loser_threshold,
        admissible_only=args.admissible_only,
        db_path=args.db,
    )
    if not jobs['branches']:
        print(f"nothing to do ({skipped} cache hits)", file=sys.stderr)
        return
    print(f"target={args.target}  to_generate={len(jobs['branches'])}  "
          f"cache_hits={skipped}", file=sys.stderr)
    tmpdir, out_root = run_container(args.target, jobs, args.queue_base)
    try:
        harvest_outputs(out_root, args.target, jobs, planned_keys)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    print("done", file=sys.stderr)


def cmd_status(args):
    if not CACHE_DIR.is_dir():
        print("no cache dir yet")
        return
    target_dir = CACHE_DIR / args.target
    if not target_dir.is_dir():
        print(f"no cache for target={args.target}")
        return
    for branch_dir in sorted(target_dir.iterdir(), key=lambda p: int(p.name)):
        w = _cache_paths(args.target, int(branch_dir.name), 'W')['status']
        l = _cache_paths(args.target, int(branch_dir.name), 'L')['status']
        ws = w.read_text().strip() if w.is_file() else '-'
        ls = l.read_text().strip() if l.is_file() else '-'
        print(f"  br{branch_dir.name:>5}  W={ws:<25}  L={ls}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--db', default=str(DB_PATH))
    sub = p.add_subparsers(dest='cmd', required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--target', required=True)
    common.add_argument('--queue-base', default=str(DEFAULT_QUEUE_BASE),
                        help=f'default {DEFAULT_QUEUE_BASE}')
    common.add_argument('--branch-id', type=int)
    common.add_argument('--branches-from-csv',
                        help='CSV with target,branch_id columns (e.g. '
                             'csvs/blocker_representatives.csv)')
    common.add_argument('--winner-threshold', type=int, default=8)
    common.add_argument('--loser-threshold',  type=int, default=8)
    common.add_argument('--admissible-only', action='store_true', default=True)
    common.add_argument('--no-admissible-only', action='store_false',
                        dest='admissible_only')
    common.add_argument('--force', action='store_true',
                        help='ignore cache key match')

    p_plan = sub.add_parser('plan', parents=[common])
    p_plan.set_defaults(func=cmd_plan)

    p_gen = sub.add_parser('generate', parents=[common])
    p_gen.set_defaults(func=cmd_generate)

    p_status = sub.add_parser('status')
    p_status.add_argument('--target', required=True)
    p_status.set_defaults(func=cmd_status)

    args = p.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
