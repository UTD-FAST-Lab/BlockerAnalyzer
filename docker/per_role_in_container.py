#!/usr/bin/env python3
"""
per_role_in_container.py — Runs INSIDE the Docker container.

For each branch in jobs.json, takes W (winner-resolving) and L
(loser-blocking) seed sets, runs each set through FUZZ_BIN, merges
profraw, and dumps the llvm-cov annotated source for the
branch-containing file (and any caller files we were asked to track).
The host extracts per-line hit counts from the dumps to build the
per-fuzzer-role SOURCE CONTEXT overlay.

Usage (inside container):
    python3 /per_role_cov.py \
        --jobs /work/jobs.json \
        --queues /queues \
        --fuzz-bin /fuzz/binary \
        --outdir /work/out \
        [--batch-size 500]

jobs.json format:
    {
      "branches": [
        {
          "branch_id": 19,
          "files": ["/src/curl/lib/content_encoding.c"],
          "W_seeds": [{"queue_subdir": "cmplog/trial1/queue", "name": "abc..."}],
          "L_seeds": [{"queue_subdir": "naive/trial1/queue",  "name": "def..."}]
        },
        ...
      ]
    }

Output: per branch, writes
    <outdir>/<branch_id>/<role>/branch_coverage_show.txt
    <outdir>/<branch_id>/<role>/status.txt   ('ok' | 'no_seeds' | 'failed: ...')
"""

import argparse
import glob
import json
import os
import subprocess
import sys
import tempfile
import time


def run_seeds_batch(seed_paths, fuzz_bin, profraw_base, batch_size=500):
    env = os.environ.copy()
    wrote_any = False
    for i in range(0, len(seed_paths), batch_size):
        chunk = seed_paths[i:i + batch_size]
        idx = i // batch_size
        profraw = f'{profraw_base}.{idx}'
        env['LLVM_PROFILE_FILE'] = profraw
        t = max(30, len(chunk) // 10)
        try:
            subprocess.run([fuzz_bin] + chunk,
                           capture_output=True, timeout=t, env=env)
        except subprocess.TimeoutExpired:
            pass
        if os.path.exists(profraw):
            wrote_any = True
    return wrote_any


def merge_profraw(profraw_base, profdata_path):
    files = sorted(glob.glob(f'{profraw_base}.*'))
    if not files:
        return False
    try:
        subprocess.run(['llvm-profdata-18', 'merge', '-sparse']
                       + files + ['-o', profdata_path],
                       capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        return False
    return os.path.exists(profdata_path)


def llvm_cov_show(fuzz_bin, profdata, sources):
    """Run llvm-cov show scoped to the requested source files.

    Uses --show-branches=count + --show-line-counts so the dump has
    per-line execution counts and per-branch True/False counts. Per-line
    counts power the diff overlay; branch counts let us see whether a
    line ran but the blocker side was never taken.
    """
    # llvm-cov show takes source file paths as POSITIONAL args after the
    # binary to scope output to those files. (`--sources=` is not a filter.)
    cmd = ['llvm-cov-18', 'show', fuzz_bin,
           '-instr-profile=' + profdata,
           '-show-branches=count',
           '-show-line-counts-or-regions',
           '-format=text']
    cmd += list(sources)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


def process_branch(branch, queues_root, fuzz_bin, outdir, batch_size):
    bid = branch['branch_id']
    files = branch.get('files', [])
    branch_outdir = os.path.join(outdir, str(bid))
    os.makedirs(branch_outdir, exist_ok=True)

    for role, seed_list in (('W', branch.get('W_seeds') or []),
                            ('L', branch.get('L_seeds') or [])):
        role_dir = os.path.join(branch_outdir, role)
        os.makedirs(role_dir, exist_ok=True)
        status_path = os.path.join(role_dir, 'status.txt')
        out_path    = os.path.join(role_dir, 'branch_coverage_show.txt')

        if not seed_list:
            with open(status_path, 'w') as f:
                f.write('no_seeds')
            continue

        # Resolve seed paths against the mounted queues root
        seed_paths = []
        for s in seed_list:
            p = os.path.join(queues_root, s['queue_subdir'], s['name'])
            if os.path.exists(p):
                seed_paths.append(p)
        if not seed_paths:
            with open(status_path, 'w') as f:
                f.write('no_seeds (none on disk)')
            continue

        with tempfile.TemporaryDirectory() as td:
            profraw_base = os.path.join(td, 'cov.profraw')
            profdata = os.path.join(td, 'cov.profdata')
            if not run_seeds_batch(seed_paths, fuzz_bin, profraw_base,
                                   batch_size=batch_size):
                with open(status_path, 'w') as f:
                    f.write('failed: no profraw produced')
                continue
            if not merge_profraw(profraw_base, profdata):
                with open(status_path, 'w') as f:
                    f.write('failed: profdata merge')
                continue
            text = llvm_cov_show(fuzz_bin, profdata, files)
            if text is None:
                with open(status_path, 'w') as f:
                    f.write('failed: llvm-cov show')
                continue
            with open(out_path, 'w') as f:
                f.write(text)
            with open(status_path, 'w') as f:
                f.write('ok')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jobs', required=True)
    ap.add_argument('--queues', required=True)
    ap.add_argument('--fuzz-bin', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--batch-size', type=int, default=500)
    args = ap.parse_args()

    with open(args.jobs) as f:
        jobs = json.load(f)

    branches = jobs.get('branches', [])
    print(f"Processing {len(branches)} branches", file=sys.stderr)
    os.makedirs(args.outdir, exist_ok=True)

    t0 = time.time()
    for i, br in enumerate(branches, 1):
        bt = time.time()
        process_branch(br, args.queues, args.fuzz_bin, args.outdir,
                       args.batch_size)
        print(f"  [{i}/{len(branches)}] branch {br['branch_id']}: "
              f"{time.time() - bt:.1f}s", file=sys.stderr)

    print(f"\nDone in {time.time() - t0:.1f}s", file=sys.stderr)


if __name__ == '__main__':
    main()
