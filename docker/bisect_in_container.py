#!/usr/bin/env python3
"""
bisect_in_container.py — Runs INSIDE the Docker container.

Multi-branch single-pass: for each unique queue, scans seeds and checks ALL
target branches at once. Much faster than per-branch bisection when many
branches share the same queue.

Usage (inside container):
    python3 /bisect.py \
        --jobs /work/jobs.json \
        --queues /queues \
        --fuzz-bin /fuzz/binary \
        --output /work/out/results.json \
        [--parallel 8] [--max-seeds 50] [--timeout 3600]

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
from concurrent.futures import ThreadPoolExecutor, as_completed


# ---------------------------------------------------------------------------
# Coverage checking — multi-branch
# ---------------------------------------------------------------------------

def _parse_count(s):
    s = s.strip().replace(',', '')
    mult = {'k': 1_000, 'M': 1_000_000, 'G': 1_000_000_000}
    if s and s[-1] in mult:
        return int(float(s[:-1]) * mult[s[-1]])
    return int(float(s))


_BRANCH_RE = re.compile(
    r'Branch \((\d+):(\d+)\): \[True: ([^\],]+), False: ([^\]]+)\]'
)


def check_branches_from_profdata(profdata_path, fuzz_bin, branch_specs):
    """
    Run llvm-cov show ONCE and check multiple branches.

    branch_specs: list of (file, line, col, side, branch_id)
    Returns: set of branch_ids that are hit.
    """
    # Group by source file to minimize llvm-cov calls
    by_file = {}
    for file, line, col, side, bid in branch_specs:
        by_file.setdefault(file, []).append((line, col, side, bid))

    hit_bids = set()

    for source_file, branches in by_file.items():
        try:
            result = subprocess.run(
                ['llvm-cov-18', 'show', fuzz_bin,
                 '-instr-profile=' + profdata_path,
                 '-show-branches=count', '-format=text', source_file],
                capture_output=True, text=True, timeout=30
            )
        except subprocess.TimeoutExpired:
            continue

        # Build lookup for what we're searching
        targets = {}  # (line, col) -> [(side, bid), ...]
        for line, col, side, bid in branches:
            targets.setdefault((line, col), []).append((side, bid))

        for text_line in result.stdout.splitlines():
            m = _BRANCH_RE.search(text_line)
            if m:
                ln, col = int(m.group(1)), int(m.group(2))
                key = (ln, col)
                if key in targets:
                    t_hits = _parse_count(m.group(3))
                    f_hits = _parse_count(m.group(4))
                    for side, bid in targets[key]:
                        hits = t_hits if side == 'T' else f_hits
                        if hits > 0:
                            hit_bids.add(bid)

    return hit_bids


# ---------------------------------------------------------------------------
# Single-seed coverage run
# ---------------------------------------------------------------------------

def run_one_seed(seed_path, fuzz_bin, work_dir):
    """Run one seed, return profdata path or None."""
    profraw_path = os.path.join(work_dir, f'seed_{os.getpid()}_{id(seed_path)}.profraw')
    profdata_path = profraw_path.replace('.profraw', '.profdata')

    env = os.environ.copy()
    env['LLVM_PROFILE_FILE'] = profraw_path

    try:
        subprocess.run([fuzz_bin, seed_path], capture_output=True, timeout=10, env=env)
    except subprocess.TimeoutExpired:
        pass

    if not os.path.exists(profraw_path):
        return None

    try:
        subprocess.run(
            ['llvm-profdata-18', 'merge', '-sparse', profraw_path, '-o', profdata_path],
            capture_output=True, timeout=10
        )
    except subprocess.TimeoutExpired:
        pass
    finally:
        if os.path.exists(profraw_path):
            os.remove(profraw_path)

    if os.path.exists(profdata_path):
        return profdata_path
    return None


# ---------------------------------------------------------------------------
# Multi-branch scan for one queue
# ---------------------------------------------------------------------------

def scan_queue(queue_dir, fuzz_bin, branch_specs, work_dir, max_seeds=50,
               parallel=8, deadline=None):
    """
    Scan all seeds in queue_dir, checking all branch_specs for each seed.

    branch_specs: list of (file, line, col, side, branch_id)
    max_seeds: stop collecting for a branch after this many hits
    Returns: dict {branch_id: [seed_name, ...]}
    """
    seeds = []
    for name in os.listdir(queue_dir):
        if name.startswith('.'):
            continue
        if os.path.isfile(os.path.join(queue_dir, name)):
            seeds.append(name)
    seeds.sort()

    if not seeds:
        return {}

    results = {bid: [] for _, _, _, _, bid in branch_specs}
    # Track which branches still need seeds
    active_specs = list(branch_specs)
    completed = set()

    print(f"    Scanning {len(seeds)} seeds for {len(branch_specs)} branches...",
          file=sys.stderr)

    processed = 0
    found_total = 0

    def process_seed(seed_name):
        seed_path = os.path.join(queue_dir, seed_name)
        profdata = run_one_seed(seed_path, fuzz_bin, work_dir)
        if profdata is None:
            return seed_name, set()
        try:
            hit_bids = check_branches_from_profdata(profdata, fuzz_bin, active_specs)
        finally:
            if os.path.exists(profdata):
                os.remove(profdata)
        return seed_name, hit_bids

    with ThreadPoolExecutor(max_workers=parallel) as pool:
        futures = {}
        for seed_name in seeds:
            if deadline and time.time() > deadline:
                break
            if not active_specs:
                break
            fut = pool.submit(process_seed, seed_name)
            futures[fut] = seed_name

        for fut in as_completed(futures):
            seed_name, hit_bids = fut.result()
            processed += 1

            for bid in hit_bids:
                if bid not in completed:
                    results[bid].append(seed_name)
                    found_total += 1
                    if len(results[bid]) >= max_seeds:
                        completed.add(bid)
                        # Remove from active specs
                        active_specs = [s for s in active_specs if s[4] != bid]

            if processed % 200 == 0:
                n_done = len(completed)
                print(f"    ... {processed}/{len(seeds)} seeds, "
                      f"{found_total} hits, {n_done}/{len(branch_specs)} branches done",
                      file=sys.stderr)

            if deadline and time.time() > deadline:
                break
            if not active_specs:
                break

    # Filter empty
    return {bid: slist for bid, slist in results.items() if slist}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='In-container multi-branch seed scan')
    parser.add_argument('--jobs', required=True, help='JSON file with job specs')
    parser.add_argument('--queues', required=True, help='Base dir containing queue subdirs')
    parser.add_argument('--fuzz-bin', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--parallel', type=int, default=8)
    parser.add_argument('--max-seeds', type=int, default=50)
    parser.add_argument('--timeout', type=int, default=3600,
                        help='Total timeout in seconds (default 3600)')
    args = parser.parse_args()

    with open(args.jobs) as f:
        jobs = json.load(f)

    queues = jobs.get('queues', {})
    total_branches = sum(len(q['branches']) for q in queues.values())
    print(f"Processing {len(queues)} queues, {total_branches} branch-jobs",
          file=sys.stderr)

    work_dir = tempfile.mkdtemp(prefix='scan_work_')
    deadline = time.time() + args.timeout
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

            print(f"  [{qi+1}/{len(queues)}] {queue_subdir}: {len(branches)} branches",
                  file=sys.stderr)

            t0 = time.time()
            hits = scan_queue(
                queue_dir, args.fuzz_bin, branch_specs, work_dir,
                max_seeds=args.max_seeds, parallel=args.parallel,
                deadline=deadline
            )
            elapsed = time.time() - t0

            total_found = sum(len(v) for v in hits.values())
            branches_hit = len(hits)
            print(f"    Done: {branches_hit}/{len(branches)} branches hit, "
                  f"{total_found} seeds, {elapsed:.1f}s", file=sys.stderr)

            # Map results back to individual branch jobs
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
        os.rmdir(work_dir)

    with open(args.output, 'w') as f:
        json.dump({'results': all_results}, f)

    total_seeds = sum(len(r['hitting_seeds']) for r in all_results)
    print(f"\nDone: {len(all_results)} branch results, {total_seeds} total seeds",
          file=sys.stderr)


if __name__ == '__main__':
    main()
