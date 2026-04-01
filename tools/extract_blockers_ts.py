#!/usr/bin/env python3
"""
extract_blockers_ts.py — Time-series blocker extraction.

Walks coverage checkpoints chronologically (30-min intervals), maintaining
per-(fuzzer, trial) tuples of (hit_status, duration, hitcount, other_hitcount)
for every branch. At each checkpoint:

1. Parse all (fuzzer, trial) coverage reports
2. Identify asymmetric branches (one side >0, other =0)
3. Apply 3-level input-dependency confirmation (L1/L2/L3)
4. Accumulate duration only while hit_status=0

Writes final state directly to the DB (branches + trial_coverage tables),
then triggers compute-derived.

Usage:
    python3 tools/extract_blockers_ts.py \
        --target lcms \
        --ts-base ./out/coverage_ts \
        [--fuzzers naive cmplog value_profile value_profile_cmplog] \
        [--trials 3] \
        [--step 1800]
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))
from blocker_db import get_db, SCHEMA_SQL, compute_derived

DB_PATH = TOOLS_DIR.parent / 'db' / 'blockers.sqlite'


# ---------------------------------------------------------------------------
# Coverage parsing
# ---------------------------------------------------------------------------

_BRANCH_RE = re.compile(
    r'Branch \((\d+):(\d+)\): \[True: ([^\],]+), False: ([^\]]+)\]'
)


def _parse_count(s):
    """Parse '35.7M', '2.20k', '0', '1,234' into int."""
    s = s.strip().replace(',', '')
    mult = {'k': 1_000, 'M': 1_000_000, 'G': 1_000_000_000}
    if s and s[-1] in mult:
        return int(float(s[:-1]) * mult[s[-1]])
    return int(float(s))


def parse_coverage_file(path):
    """
    Parse an llvm-cov show file into branch hit counts.

    Returns dict: {(file, line, col): (true_hits, false_hits)}
    """
    results = {}
    current_file = None

    with open(path) as f:
        for line in f:
            stripped = line.strip()

            # File header: "/src/foo/bar.c:" on its own line, no "|"
            if stripped.endswith(':') and '|' not in line and '/' in stripped:
                current_file = stripped.rstrip(':')
                continue

            if current_file is None:
                continue

            m = _BRANCH_RE.search(line)
            if m:
                ln, col = int(m.group(1)), int(m.group(2))
                try:
                    t_hits = _parse_count(m.group(3))
                    f_hits = _parse_count(m.group(4))
                except (ValueError, IndexError):
                    continue
                results[(current_file, ln, col)] = (t_hits, f_hits)

    return results


# ---------------------------------------------------------------------------
# Core: chronological forward pass
# ---------------------------------------------------------------------------

def extract_blockers_ts(target, ts_base, fuzzers, n_trials, step_s, db_path=None):
    """
    Walk checkpoints chronologically, build blocker state, write to DB.
    """
    db_path = db_path or str(DB_PATH)

    # Discover all available checkpoints (union across all fuzzer/trial combos)
    all_checkpoints = set()
    for fz in fuzzers:
        for trial in range(1, n_trials + 1):
            reports_dir = os.path.join(ts_base, target, fz, f'trial{trial}', 'reports')
            if os.path.isdir(reports_dir):
                for d in os.listdir(reports_dir):
                    if d.isdigit():
                        all_checkpoints.add(int(d))

    if not all_checkpoints:
        print(f"No checkpoints found under {ts_base}/{target}/", file=sys.stderr)
        return

    checkpoints = sorted(all_checkpoints)
    step_h = step_s / 3600.0
    final_t = checkpoints[-1]
    print(f"Target: {target}", file=sys.stderr)
    print(f"Fuzzers: {fuzzers}", file=sys.stderr)
    print(f"Checkpoints: {len(checkpoints)} ({checkpoints[0]}s – {final_t}s)", file=sys.stderr)

    # State tracking per branch side per (fuzzer, trial):
    #   key: (file, line, col, side)
    #   value: dict[(fuzzer, trial)] -> {hit_status, duration_h, hitcount, other_hitcount}
    #
    # hit_status: -1=uncovered, 0=blocked (other side hit, this side not), 1=resolved
    # duration_h: accumulates +step_h while hit_status=0; stops on flip to 1
    # hitcount: blocked side count at current checkpoint
    # other_hitcount: other side count at current checkpoint
    branch_state = defaultdict(lambda: {})

    # We also need the final-T data for L2/L3 confirmation.
    # We'll do a two-pass approach:
    #   Pass 1: walk all checkpoints, build per-trial state
    #   Pass 2: apply L2/L3 confirmation using final-T state, filter

    # --- Pass 1: Forward walk ---
    for cp_time in checkpoints:
        cp_h = cp_time / 3600.0

        for fz in fuzzers:
            for trial in range(1, n_trials + 1):
                cov_file = os.path.join(
                    ts_base, target, fz, f'trial{trial}', 'reports',
                    str(cp_time), 'branch_coverage_show.txt'
                )
                if not os.path.exists(cov_file):
                    continue

                branch_data = parse_coverage_file(cov_file)
                ft_key = (fz, trial)

                for (file, line, col), (t_hits, f_hits) in branch_data.items():
                    # Process both T and F sides
                    for side in ('T', 'F'):
                        bkey = (file, line, col, side)
                        blocked_hits = t_hits if side == 'T' else f_hits
                        other_hits = f_hits if side == 'T' else t_hits

                        # Initialize state if first time seeing this branch
                        if ft_key not in branch_state[bkey]:
                            branch_state[bkey][ft_key] = {
                                'hit_status': -1,
                                'duration_h': -1.0,  # -1 = N/A (never blocked)
                                'hitcount': 0,
                                'other_hitcount': 0,
                            }

                        state = branch_state[bkey][ft_key]

                        # Update hitcounts to current checkpoint values
                        state['hitcount'] = blocked_hits
                        state['other_hitcount'] = other_hits

                        # Determine current hit_status
                        if blocked_hits > 0:
                            new_status = 1  # resolved
                        elif other_hits > 0:
                            new_status = 0  # blocked
                        else:
                            new_status = -1  # uncovered

                        prev_status = state['hit_status']

                        # Status transitions (can only advance: -1 -> 0 -> 1)
                        if new_status > prev_status:
                            state['hit_status'] = new_status

                        # Duration tracking:
                        #   -1.0 = N/A (never was a blocker: unreached or resolved without ever being blocked)
                        #   ≥ 0  = time spent as a blocker (accumulates while hit_status=0)
                        if state['hit_status'] == 0:
                            # First time becoming blocked: initialize to 0
                            if state['duration_h'] < 0:
                                state['duration_h'] = 0.0
                            state['duration_h'] += step_h
                        # If hit_status=1 and duration is still -1, it was never blocked → stays -1
                        # If hit_status=1 and duration >= 0, it was blocked then resolved → stop accumulating

        if cp_time % (step_s * 10) == 0 or cp_time == final_t:
            # Count how many branch sides have at least one blocked trial
            n_asymmetric = sum(
                1 for bkey, ft_states in branch_state.items()
                if any(s['hit_status'] == 0 for s in ft_states.values())
            )
            print(f"  T={cp_h:.1f}h: {len(branch_state)} branch sides tracked, "
                  f"{n_asymmetric} with at least one blocked trial", file=sys.stderr)

    # --- Pass 2: 3-Level confirmation ---
    # For each branch side, check if it's input-dependent (not structurally dead)
    confirmed = {}  # bkey -> ft_states (only confirmed blockers)
    stats = {'l1': 0, 'l2': 0, 'l3': 0, 'discarded': 0}

    for bkey, ft_states in branch_state.items():
        # A branch side is a candidate if at least one (fuzzer, trial) has hit_status=0
        has_blocked = any(s['hit_status'] == 0 for s in ft_states.values())
        if not has_blocked:
            continue

        # Check if any (fuzzer, trial) resolved it (hit_status=1)
        has_resolved = any(s['hit_status'] == 1 for s in ft_states.values())
        if not has_resolved:
            # Falls through all levels — structurally unreachable
            stats['discarded'] += 1
            continue

        # Determine confirmation level
        # Group by fuzzer
        by_fuzzer = defaultdict(dict)
        for (fz, trial), state in ft_states.items():
            by_fuzzer[fz][trial] = state

        level = None

        # L1: Any trial of same fuzzer resolves it at same time?
        # (We check final state since coverage is cumulative — if resolved at any T,
        #  it's resolved at final T too)
        for fz, trial_states in by_fuzzer.items():
            has_blocked_trial = any(s['hit_status'] == 0 for s in trial_states.values())
            has_resolved_trial = any(s['hit_status'] == 1 for s in trial_states.values())
            if has_blocked_trial and has_resolved_trial:
                level = 'l1'
                break

        # L2: Same fuzzer resolves at final T (same as L1 since we use final state)
        if level is None:
            for fz, trial_states in by_fuzzer.items():
                has_blocked_trial = any(s['hit_status'] == 0 for s in trial_states.values())
                has_resolved_trial = any(s['hit_status'] == 1 for s in trial_states.values())
                if has_blocked_trial and has_resolved_trial:
                    level = 'l2'
                    break

        # L3: Any other fuzzer resolves at final T
        if level is None:
            blocked_fuzzers = {fz for fz, ts in by_fuzzer.items()
                               if all(s['hit_status'] != 1 for s in ts.values())}
            resolved_fuzzers = {fz for fz, ts in by_fuzzer.items()
                                if any(s['hit_status'] == 1 for s in ts.values())}
            if blocked_fuzzers and resolved_fuzzers:
                level = 'l3'

        if level is None:
            stats['discarded'] += 1
            continue

        stats[level] += 1
        level_int = {'l1': 1, 'l2': 2, 'l3': 3}[level]
        confirmed[bkey] = (ft_states, level_int)

    total = stats['l1'] + stats['l2'] + stats['l3']
    print(f"\nConfirmed: {total} input-dependent blockers "
          f"(L1={stats['l1']}, L2={stats['l2']}, L3={stats['l3']}, "
          f"discarded={stats['discarded']})", file=sys.stderr)

    # --- Pass 3: Write to DB ---
    conn = get_db(db_path)
    conn.executescript(SCHEMA_SQL)

    # Get source lines from the final checkpoint for each file
    source_lines = {}
    for fz in fuzzers:
        cov_file = os.path.join(
            ts_base, target, fz, f'trial1', 'reports',
            str(final_t), 'branch_coverage_show.txt'
        )
        if os.path.exists(cov_file):
            source_lines.update(_extract_source_lines(cov_file))
            break  # one file is enough

    inserted = 0
    for bkey, (ft_states, conf_level) in confirmed.items():
        file, line, col, side = bkey

        src_line = source_lines.get((file, line))

        # Use file basename as function placeholder
        function = os.path.basename(file)

        # Upsert branch with confirmation_level
        conn.execute("""
            INSERT INTO branches (target, file, function, line, col, blocked_side,
                                  source_line, confirmation_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(target, file, function, line, col, blocked_side) DO UPDATE SET
                source_line = excluded.source_line,
                confirmation_level = excluded.confirmation_level
        """, (target, file, function, line, col, side, src_line, conf_level))

        branch_id = conn.execute("""
            SELECT branch_id FROM branches
            WHERE target=? AND file=? AND function=? AND line=? AND col=? AND blocked_side=?
        """, (target, file, function, line, col, side)).fetchone()[0]

        # Insert trial_coverage for each (fuzzer, trial)
        for (fz, trial), state in ft_states.items():
            conn.execute("""
                INSERT INTO trial_coverage
                    (branch_id, fuzzer, trial, hit_status, duration_h,
                     hitcount, other_hitcount)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(branch_id, fuzzer, trial) DO UPDATE SET
                    hit_status = excluded.hit_status,
                    duration_h = excluded.duration_h,
                    hitcount = excluded.hitcount,
                    other_hitcount = excluded.other_hitcount
            """, (branch_id, fz, trial, state['hit_status'],
                  state['duration_h'], state['hitcount'],
                  state['other_hitcount']))

        inserted += 1

    conn.commit()
    conn.close()

    print(f"Wrote {inserted} blockers to DB", file=sys.stderr)

    # Compute derived metrics
    compute_derived(target, db_path)


def _extract_source_lines(cov_file):
    """
    Extract source line text for each (file, line) from an llvm-cov show file.
    Returns dict: {(file, line): source_text}
    """
    results = {}
    current_file = None
    # Pattern: "  123|     45|    if (x > 0) {"
    line_re = re.compile(r'^\s*(\d+)\|[^|]*\|(.*)$')

    with open(cov_file) as f:
        for raw_line in f:
            stripped = raw_line.strip()
            if stripped.endswith(':') and '|' not in raw_line and '/' in stripped:
                current_file = stripped.rstrip(':')
                continue
            if current_file is None:
                continue
            m = line_re.match(raw_line)
            if m:
                ln = int(m.group(1))
                text = m.group(2).rstrip()
                if text:
                    results[(current_file, ln)] = text

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Time-series blocker extraction — chronological forward pass'
    )
    parser.add_argument('--target', required=True,
                        help='Target name (bloaty, lcms, libpcap, mbedtls, sqlite3)')
    parser.add_argument('--ts-base', required=True,
                        help='Path to coverage_ts dir (e.g. ./out/coverage_ts)')
    parser.add_argument('--fuzzers', nargs='+',
                        default=['naive', 'cmplog', 'value_profile', 'value_profile_cmplog'],
                        help='Fuzzer names (default: all 4)')
    parser.add_argument('--trials', type=int, default=3,
                        help='Number of trials per fuzzer (default: 3)')
    parser.add_argument('--step', type=int, default=1800,
                        help='Checkpoint interval in seconds (default: 1800 = 30min)')
    parser.add_argument('--db', help='Path to SQLite database')

    args = parser.parse_args()

    extract_blockers_ts(
        target=args.target,
        ts_base=args.ts_base,
        fuzzers=args.fuzzers,
        n_trials=args.trials,
        step_s=args.step,
        db_path=args.db,
    )


if __name__ == '__main__':
    main()
