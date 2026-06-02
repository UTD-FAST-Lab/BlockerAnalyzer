#!/usr/bin/env python3
"""
bisect_in_container.py — Runs INSIDE the Docker container.

Multi-branch 10-bucket bisection: for each queue, divides seeds into 10
buckets, runs each bucket in batch (many seeds per fuzz_bin invocation),
checks which branches are hit per bucket via one llvm-cov call, then
recurses into hitting buckets until individual seeds are identified.

Usage (inside container):
    python3 /seed_scanner.py \
        --jobs /work/jobs.json \
        --queues /queues \
        --fuzz-bin /fuzz/binary \
        --output /work/out/results.json \
        [--max-seeds 50] [--batch-size 500] [--timeout 3600]

jobs.json format:
    {
      "queues": {
        "cmplog/trial1/queue": {
          "branches": [
            {"branch_id": 85, "file": "/src/foo.c", "line": 343, "col": 13,
             "side": "T", "type": "resolving"},
            ...
          ]
        },
        ...
      }
    }

Output: results.json with per-branch hitting seeds.
"""

import argparse
import json
import multiprocessing
import os
import re
import subprocess
import sys
import tempfile
import time


# Set True when queues are scanned in parallel workers, to suppress the
# per-bucket depth-0 progress prints (they would interleave illegibly across
# workers). The per-queue start/Done summary is still printed from the parent.
_QUIET = False


# ---------------------------------------------------------------------------
# Coverage checking
# ---------------------------------------------------------------------------

def _parse_count(s):
    s = s.strip().replace(',', '')
    mult = {'k': 1_000, 'M': 1_000_000, 'G': 1_000_000_000}
    if s and s[-1] in mult:
        return int(float(s[:-1]) * mult[s[-1]])
    # llvm-cov-18 sometimes emits truncated scientific notation like '18.4E'
    s = s.rstrip('eE')
    if not s:
        return 0
    return int(float(s))


_BRANCH_RE = re.compile(
    r'Branch \((\d+):(\d+)\): \[True: ([^\],]+), False: ([^\]]+)\]'
)


_FILE_HEADER_RE = re.compile(r'^(/\S+\.\w+):$')


def check_branches_from_profdata(profdata_path, fuzz_bin, branch_specs):
    """
    Run llvm-cov show ONCE (all files) and check multiple branches.

    branch_specs: list of (file, line, col, side, branch_id)
    Returns: set of branch_ids that are hit.
    """
    # Group branch_specs by file: {file: {(line, col): [(side, bid), ...]}}.
    by_file = {}
    for file, line, col, side, bid in branch_specs:
        by_file.setdefault(file, {}).setdefault((line, col), []).append((side, bid))

    def _scoped(source_args):
        return subprocess.run(
            ['llvm-cov-18', 'show', fuzz_bin,
             '-instr-profile=' + profdata_path,
             '-show-branches=count', '-format=text', *source_args],
            capture_output=True, text=True, timeout=120
        )

    hit_bids = set()
    missed_files = []  # files whose scoped render came back empty

    # Scope llvm-cov to ONE file per call. Passing source args makes llvm-cov
    # render only that file (a 5-20x speedup on large targets), but it also
    # OMITS the "/src/...:" filename header that a full render prints — so we
    # must NOT rely on the header to know which file we're in. Because the whole
    # output IS this one file's source, every Branch line belongs to `file`.
    # (Per-file calls cost one llvm-cov each, but blockers span few files per
    # queue, so this stays cheap while being correct for single-file scopes —
    # the case the previous single-call/header-tracking version silently missed.)
    for file, targets in by_file.items():
        try:
            result = _scoped([file])
        except subprocess.TimeoutExpired:
            continue
        if not result.stdout.strip():
            # Source-path mismatch between DB file path and the binary's
            # recorded path: defer to a single full render below.
            missed_files.append(file)
            continue
        for text_line in result.stdout.splitlines():
            m = _BRANCH_RE.search(text_line)
            if m:
                key = (int(m.group(1)), int(m.group(2)))
                if key in targets:
                    t_hits = _parse_count(m.group(3))
                    f_hits = _parse_count(m.group(4))
                    for side, bid in targets[key]:
                        if (t_hits if side == 'T' else f_hits) > 0:
                            hit_bids.add(bid)

    # Fallback: any file whose scoped render was empty gets resolved from ONE
    # full (unscoped) render, which DOES print per-file headers — so here we
    # track the current file the original way and only inspect missed files.
    if missed_files:
        missed = set(missed_files)
        try:
            full = _scoped([])
        except subprocess.TimeoutExpired:
            full = None
        if full is not None:
            current_file = None
            skip_file = True
            for text_line in full.stdout.splitlines():
                hm = _FILE_HEADER_RE.match(text_line)
                if hm:
                    current_file = hm.group(1)
                    skip_file = current_file not in missed
                    continue
                if skip_file:
                    continue
                m = _BRANCH_RE.search(text_line)
                if m:
                    key = (int(m.group(1)), int(m.group(2)))
                    targets = by_file.get(current_file, {})
                    if key in targets:
                        t_hits = _parse_count(m.group(3))
                        f_hits = _parse_count(m.group(4))
                        for side, bid in targets[key]:
                            if (t_hits if side == 'T' else f_hits) > 0:
                                hit_bids.add(bid)

    return hit_bids


# ---------------------------------------------------------------------------
# Batch execution
# ---------------------------------------------------------------------------

def run_seeds_batch(seed_paths, fuzz_bin, profraw_path, batch_size=500):
    """
    Run fuzz_bin on seed_paths in sub-batches (to avoid ARG_MAX),
    writing each sub-batch to a unique profraw file.

    profraw_path is used as the base: sub-batches write to
    profraw_path.0, profraw_path.1, etc.
    """
    env = os.environ.copy()
    wrote_any = False

    for i in range(0, len(seed_paths), batch_size):
        chunk = seed_paths[i:i + batch_size]
        batch_idx = i // batch_size
        batch_profraw = f'{profraw_path}.{batch_idx}'
        env['LLVM_PROFILE_FILE'] = batch_profraw
        t = max(30, len(chunk) // 10)
        try:
            subprocess.run(
                [fuzz_bin] + chunk,
                capture_output=True, timeout=t, env=env
            )
        except subprocess.TimeoutExpired:
            pass
        if os.path.exists(batch_profraw):
            wrote_any = True

    return wrote_any


def make_profdata(profraw_path, profdata_path):
    """Merge profraw file(s) into profdata.

    profraw_path is the base name; actual files are profraw_path.0,
    profraw_path.1, etc. (written by run_seeds_batch).
    """
    import glob as _glob
    profraw_files = sorted(_glob.glob(f'{profraw_path}.*'))
    if not profraw_files:
        return False
    try:
        subprocess.run(
            ['llvm-profdata-18', 'merge', '-sparse'] +
            profraw_files + ['-o', profdata_path],
            capture_output=True, timeout=120
        )
    except subprocess.TimeoutExpired:
        return False
    return os.path.exists(profdata_path)


def run_and_check(seed_paths, fuzz_bin, branch_specs, work_dir, tag=''):
    """
    Run seeds in batch, produce coverage, check which branches are hit.
    Returns set of hit branch_ids.
    """
    profraw = os.path.join(work_dir, f'{tag}.profraw')
    profdata = os.path.join(work_dir, f'{tag}.profdata')

    try:
        if not run_seeds_batch(seed_paths, fuzz_bin, profraw):
            return set()
        if not make_profdata(profraw, profdata):
            return set()
        return check_branches_from_profdata(profdata, fuzz_bin, branch_specs)
    finally:
        import glob as _glob
        for p in _glob.glob(f'{profraw}.*'):
            os.remove(p)
        if os.path.exists(profdata):
            os.remove(profdata)


# ---------------------------------------------------------------------------
# 10-bucket recursive bisection
# ---------------------------------------------------------------------------

def scan_queue(queue_dir, fuzz_bin, branch_specs, work_dir, max_seeds=50,
               batch_size=500, deadline=None):
    """
    10-bucket recursive bisection for one queue.

    Splits seeds into 10 buckets, runs each in batch, checks which branches
    are hit, recurses into hitting buckets. Stops at individual seeds.
    """
    seeds = []
    for name in sorted(os.listdir(queue_dir)):
        if name.startswith('.'):
            continue
        if os.path.isfile(os.path.join(queue_dir, name)):
            seeds.append(name)

    if not seeds:
        return {}

    results = {}  # branch_id -> [seed_name, ...]
    completed = set()  # branch_ids with enough seeds

    _bisect_recursive(
        queue_dir, seeds, fuzz_bin, branch_specs, work_dir, results,
        completed, max_seeds, batch_size, deadline, depth=0
    )

    return {bid: slist for bid, slist in results.items() if slist}


def _bisect_recursive(queue_dir, seed_names, fuzz_bin, branch_specs, work_dir,
                      results, completed, max_seeds, batch_size, deadline,
                      depth):
    """Recursive 10-bucket bisection."""
    if deadline and time.time() > deadline:
        return
    if not seed_names or not branch_specs:
        return

    # Filter out already-completed branches
    active_specs = [s for s in branch_specs if s[4] not in completed]
    if not active_specs:
        return

    # Base case: small enough to test individually
    if len(seed_names) <= 10:
        for seed_name in seed_names:
            if deadline and time.time() > deadline:
                break
            active_specs = [s for s in branch_specs if s[4] not in completed]
            if not active_specs:
                break

            seed_path = os.path.join(queue_dir, seed_name)
            tag = f'd{depth}_leaf_{hash(seed_name) % 100000}'
            hits = run_and_check(
                [seed_path], fuzz_bin, active_specs, work_dir, tag=tag
            )

            for bid in hits:
                if bid not in completed:
                    results.setdefault(bid, []).append(seed_name)
                    if len(results[bid]) >= max_seeds:
                        completed.add(bid)
        return

    # Split into 10 buckets
    n = len(seed_names)
    bucket_size = (n + 9) // 10
    buckets = []
    for i in range(0, n, bucket_size):
        buckets.append(seed_names[i:i + bucket_size])

    if depth == 0 and not _QUIET:
        print(f"      Depth 0: {n} seeds -> {len(buckets)} buckets "
              f"of ~{bucket_size}, {len(active_specs)} branches",
              file=sys.stderr)

    # Run each bucket in batch, check which branches are hit
    for bi, bucket in enumerate(buckets):
        if deadline and time.time() > deadline:
            break
        active_specs = [s for s in branch_specs if s[4] not in completed]
        if not active_specs:
            break

        seed_paths = [os.path.join(queue_dir, s) for s in bucket]
        tag = f'd{depth}_b{bi}'
        hits = run_and_check(
            seed_paths, fuzz_bin, active_specs, work_dir, tag=tag
        )

        if not hits:
            continue

        if depth == 0 and not _QUIET:
            print(f"        bucket {bi}: {len(hits)} branches hit "
                  f"({len(completed)} complete)", file=sys.stderr)

        # Recurse into this bucket for the hit branches
        hit_specs = [s for s in active_specs if s[4] in hits]
        _bisect_recursive(
            queue_dir, bucket, fuzz_bin, hit_specs, work_dir,
            results, completed, max_seeds, batch_size, deadline,
            depth=depth + 1
        )


# ---------------------------------------------------------------------------
# Parallel queue worker
# ---------------------------------------------------------------------------

def _scan_one_queue(task):
    """Worker entry point: scan ONE queue in its own tempdir.

    task = (qi, n_queues, queue_subdir, branches, queues_root, fuzz_bin,
            max_seeds, batch_size, deadline)
    Returns (queue_subdir, branches, elapsed, results_list) where
    results_list is the list of all_results dicts for this queue (empty if the
    queue dir was missing).
    """
    (qi, n_queues, queue_subdir, branches, queues_root, fuzz_bin,
     max_seeds, batch_size, deadline) = task

    queue_dir = os.path.join(queues_root, queue_subdir)
    if not os.path.isdir(queue_dir):
        print(f"  [{qi+1}/{n_queues}] SKIP {queue_subdir} — not found",
              file=sys.stderr)
        return (queue_subdir, branches, 0.0, [])

    branch_specs = [
        (b['file'], b['line'], b['col'], b['side'], b['branch_id'])
        for b in branches
    ]

    work_dir = tempfile.mkdtemp(prefix='scan_work_')
    t0 = time.time()
    try:
        hits = scan_queue(
            queue_dir, fuzz_bin, branch_specs, work_dir,
            max_seeds=max_seeds, batch_size=batch_size, deadline=deadline
        )
    finally:
        for root, dirs, files in os.walk(work_dir, topdown=False):
            for f in files:
                os.remove(os.path.join(root, f))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
        if os.path.exists(work_dir):
            os.rmdir(work_dir)
    elapsed = time.time() - t0

    branch_lookup = {b['branch_id']: b for b in branches}
    results = []
    for bid, seed_list in hits.items():
        b = branch_lookup[bid]
        results.append({
            'branch_id': bid,
            'queue_subdir': queue_subdir,
            'type': b['type'],
            'hitting_seeds': seed_list,
        })

    print(f"  [{qi+1}/{n_queues}] {queue_subdir}: "
          f"{len(hits)}/{len(branches)} branches hit, "
          f"{sum(len(v) for v in hits.values())} seeds, {elapsed:.1f}s",
          file=sys.stderr)
    return (queue_subdir, branches, elapsed, results)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='In-container 10-bucket batch bisection seed scan')
    parser.add_argument('--jobs', required=True)
    parser.add_argument('--queues', required=True)
    parser.add_argument('--fuzz-bin', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--max-seeds', type=int, default=50)
    parser.add_argument('--batch-size', type=int, default=500,
                        help='Max seeds per fuzz_bin invocation (default 500)')
    parser.add_argument('--timeout', type=int, default=0,
                        help='Total timeout in seconds (0 = no timeout)')
    parser.add_argument('--workers', type=int,
                        default=int(os.environ.get('BISECT_WORKERS', '24')),
                        help='Parallel queue workers (default 24 or '
                             '$BISECT_WORKERS). Queues are independent, so this '
                             'is near-linear speedup. Capped to #queues.')
    args = parser.parse_args()

    with open(args.jobs) as f:
        jobs = json.load(f)

    queues = jobs.get('queues', {})
    total_branches = sum(len(q['branches']) for q in queues.values())
    workers = max(1, min(args.workers, len(queues)))
    print(f"Processing {len(queues)} queues, {total_branches} branch-jobs "
          f"({workers} parallel workers)", file=sys.stderr)

    deadline = (time.time() + args.timeout) if args.timeout > 0 else None

    # One task per queue; each worker scans in its own tempdir (queue scans
    # share no state), so the box's cores collapse the serial walk to roughly
    # one queue's wall-clock.
    tasks = [
        (qi, len(queues), queue_subdir, queue_info['branches'], args.queues,
         args.fuzz_bin, args.max_seeds, args.batch_size, deadline)
        for qi, (queue_subdir, queue_info) in enumerate(queues.items())
    ]

    all_results = []
    if workers > 1 and len(tasks) > 1:
        global _QUIET
        _QUIET = True  # children inherit via fork; suppress interleaved prints
        with multiprocessing.Pool(workers) as pool:
            for _qsub, _branches, _elapsed, results in pool.imap_unordered(
                    _scan_one_queue, tasks):
                all_results.extend(results)
    else:
        for task in tasks:
            _qsub, _branches, _elapsed, results = _scan_one_queue(task)
            all_results.extend(results)

    with open(args.output, 'w') as f:
        json.dump({'results': all_results}, f)

    total_seeds = sum(len(r['hitting_seeds']) for r in all_results)
    print(f"\nDone: {len(all_results)} branch results, {total_seeds} total seeds",
          file=sys.stderr)


if __name__ == '__main__':
    main()