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
import os
import re
import subprocess
import sys
import tempfile
import time


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
    # Build lookup: (file, line, col) -> [(side, bid), ...]
    targets = {}
    for file, line, col, side, bid in branch_specs:
        targets.setdefault((file, line, col), []).append((side, bid))

    # Also build a set of target files to skip irrelevant sections quickly
    target_files = {file for file, _, _, _, _ in branch_specs}

    try:
        result = subprocess.run(
            ['llvm-cov-18', 'show', fuzz_bin,
             '-instr-profile=' + profdata_path,
             '-show-branches=count', '-format=text'],
            capture_output=True, text=True, timeout=60
        )
    except subprocess.TimeoutExpired:
        return set()

    hit_bids = set()
    current_file = None
    skip_file = True

    for text_line in result.stdout.splitlines():
        # Track current source file from headers like "/src/bloaty/src/elf.cc:"
        hm = _FILE_HEADER_RE.match(text_line)
        if hm:
            current_file = hm.group(1)
            skip_file = current_file not in target_files
            continue

        if skip_file:
            continue

        m = _BRANCH_RE.search(text_line)
        if m:
            ln, col = int(m.group(1)), int(m.group(2))
            key = (current_file, ln, col)
            if key in targets:
                t_hits = _parse_count(m.group(3))
                f_hits = _parse_count(m.group(4))
                for side, bid in targets[key]:
                    hits = t_hits if side == 'T' else f_hits
                    if hits > 0:
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

    if depth == 0:
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

        if depth == 0:
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
    args = parser.parse_args()

    with open(args.jobs) as f:
        jobs = json.load(f)

    queues = jobs.get('queues', {})
    total_branches = sum(len(q['branches']) for q in queues.values())
    print(f"Processing {len(queues)} queues, {total_branches} branch-jobs",
          file=sys.stderr)

    work_dir = tempfile.mkdtemp(prefix='scan_work_')
    deadline = (time.time() + args.timeout) if args.timeout > 0 else None
    all_results = []

    try:
        for qi, (queue_subdir, queue_info) in enumerate(queues.items()):
            queue_dir = os.path.join(args.queues, queue_subdir)
            if not os.path.isdir(queue_dir):
                print(f"  [{qi+1}/{len(queues)}] SKIP {queue_subdir} — not found",
                      file=sys.stderr)
                continue

            branches = queue_info['branches']
            branch_specs = [
                (b['file'], b['line'], b['col'], b['side'], b['branch_id'])
                for b in branches
            ]

            print(f"  [{qi+1}/{len(queues)}] {queue_subdir}: "
                  f"{len(branches)} branches", file=sys.stderr)

            t0 = time.time()
            hits = scan_queue(
                queue_dir, args.fuzz_bin, branch_specs, work_dir,
                max_seeds=args.max_seeds, batch_size=args.batch_size,
                deadline=deadline
            )
            elapsed = time.time() - t0

            total_found = sum(len(v) for v in hits.values())
            branches_hit = len(hits)
            print(f"    Done: {branches_hit}/{len(branches)} branches hit, "
                  f"{total_found} seeds, {elapsed:.1f}s", file=sys.stderr)

            branch_lookup = {b['branch_id']: b for b in branches}
            for bid, seed_list in hits.items():
                b = branch_lookup[bid]
                all_results.append({
                    'branch_id': bid,
                    'queue_subdir': queue_subdir,
                    'type': b['type'],
                    'hitting_seeds': seed_list,
                })

            if deadline and time.time() > deadline:
                print("  Total timeout reached", file=sys.stderr)
                break

    finally:
        for root, dirs, files in os.walk(work_dir, topdown=False):
            for f in files:
                os.remove(os.path.join(root, f))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
        if os.path.exists(work_dir):
            os.rmdir(work_dir)

    with open(args.output, 'w') as f:
        json.dump({'results': all_results}, f)

    total_seeds = sum(len(r['hitting_seeds']) for r in all_results)
    print(f"\nDone: {len(all_results)} branch results, {total_seeds} total seeds",
          file=sys.stderr)


if __name__ == '__main__':
    main()
