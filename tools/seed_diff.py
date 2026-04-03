#!/usr/bin/env python3
"""
seed_diff.py — Pre-compute byte-level mutual information between resolving
and blocking seeds for a given branch.

Outputs a structured summary that the branch-cluster agent consumes directly,
eliminating the need for the agent to read and diff seeds manually.

Usage:
    python3 tools/seed_diff.py --target lcms --branch-id 358 --queue-base ./out
    python3 tools/seed_diff.py --target mbedtls --branch-id 372 --queue-base ./out --top 20
"""

import argparse
import json
import math
import os
import sqlite3
import sys
from collections import Counter, defaultdict

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'blockers.sqlite')


def get_db(db_path=None):
    conn = sqlite3.connect(db_path or DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def load_seeds(branch_id, queue_base, target, db_path=None, max_seeds=10):
    """Load resolving and blocking seed bytes from disk."""
    conn = get_db(db_path)

    groups = {}
    for table, label in [('resolving_seeds', 'resolving'),
                         ('blocking_seeds', 'blocking')]:
        rows = conn.execute(f'''
            SELECT seed_id, fuzzer, trial FROM {table}
            WHERE branch_id = ? LIMIT ?
        ''', (branch_id, max_seeds)).fetchall()

        seeds = []
        for r in rows:
            path = os.path.join(queue_base, target,
                                r['fuzzer'], f'trial{r["trial"]}',
                                'queue', r['seed_id'])
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    data = f.read()
                seeds.append({
                    'seed_id': r['seed_id'],
                    'fuzzer': r['fuzzer'],
                    'trial': r['trial'],
                    'data': data,
                    'size': len(data),
                })
        groups[label] = seeds

    conn.close()
    return groups


def compute_mi(resolving_bytes, blocking_bytes):
    """
    Compute mutual information between byte value and group label.

    MI(X, Y) = sum over x,y of p(x,y) * log2(p(x,y) / (p(x)*p(y)))
    where X = byte value (0-255), Y = group (resolving/blocking)
    """
    n_r = len(resolving_bytes)
    n_b = len(blocking_bytes)
    n = n_r + n_b

    if n == 0:
        return 0.0

    # Joint counts
    joint = defaultdict(lambda: [0, 0])  # byte_val -> [count_resolving, count_blocking]
    for v in resolving_bytes:
        joint[v][0] += 1
    for v in blocking_bytes:
        joint[v][1] += 1

    mi = 0.0
    for val, (cr, cb) in joint.items():
        for label_idx, (c_label, n_label) in enumerate([(cr, n_r), (cb, n_b)]):
            if c_label == 0:
                continue
            p_xy = c_label / n
            p_x = (cr + cb) / n
            p_y = n_label / n
            if p_x > 0 and p_y > 0:
                mi += p_xy * math.log2(p_xy / (p_x * p_y))

    return mi


def compute_entropy(values):
    """Shannon entropy of a byte value distribution."""
    if not values:
        return 0.0
    n = len(values)
    counts = Counter(values)
    ent = 0.0
    for c in counts.values():
        p = c / n
        if p > 0:
            ent -= p * math.log2(p)
    return ent


def analyze_branch(target, branch_id, queue_base, top_n=15,
                   max_seeds=10, db_path=None):
    """Compute MI-based seed diff for a branch."""
    groups = load_seeds(branch_id, queue_base, target, db_path, max_seeds)

    resolving = groups['resolving']
    blocking = groups['blocking']

    if not resolving or not blocking:
        return {
            'branch_id': branch_id,
            'error': f'Insufficient seeds: {len(resolving)} resolving, {len(blocking)} blocking',
        }

    # Size analysis
    r_sizes = [s['size'] for s in resolving]
    b_sizes = [s['size'] for s in blocking]
    max_offset = max(max(r_sizes), max(b_sizes))

    # Per-offset MI computation
    offsets = []
    for off in range(max_offset):
        r_bytes = [s['data'][off] if off < s['size'] else -1 for s in resolving]
        b_bytes = [s['data'][off] if off < s['size'] else -1 for s in blocking]

        # Only compute MI where we have data from both groups
        r_valid = [v for v in r_bytes if v >= 0]
        b_valid = [v for v in b_bytes if v >= 0]

        if not r_valid or not b_valid:
            continue

        mi = compute_mi(r_valid, b_valid)
        r_entropy = compute_entropy(r_valid)
        b_entropy = compute_entropy(b_valid)

        # Value distribution
        r_counts = Counter(r_valid)
        b_counts = Counter(b_valid)

        # Top values
        r_top = r_counts.most_common(3)
        b_top = b_counts.most_common(3)

        offsets.append({
            'offset': off,
            'mi': mi,
            'r_entropy': r_entropy,
            'b_entropy': b_entropy,
            'r_values': r_top,
            'b_values': b_top,
            'r_count': len(r_valid),
            'b_count': len(b_valid),
        })

    # Sort by MI descending
    offsets.sort(key=lambda x: -x['mi'])

    # Group adjacent high-MI offsets into regions
    top_offsets = [o for o in offsets if o['mi'] > 0]
    regions = _find_regions(top_offsets, top_n)

    return {
        'branch_id': branch_id,
        'target': target,
        'n_resolving': len(resolving),
        'n_blocking': len(blocking),
        'resolving_sizes': {'min': min(r_sizes), 'max': max(r_sizes),
                            'mean': sum(r_sizes) / len(r_sizes)},
        'blocking_sizes': {'min': min(b_sizes), 'max': max(b_sizes),
                           'mean': sum(b_sizes) / len(b_sizes)},
        'size_differs': abs(sum(r_sizes)/len(r_sizes) - sum(b_sizes)/len(b_sizes)) > 10,
        'top_offsets': offsets[:top_n],
        'regions': regions,
        'resolving_seeds': [{'seed_id': s['seed_id'], 'fuzzer': s['fuzzer'],
                             'trial': s['trial'], 'size': s['size']}
                            for s in resolving],
        'blocking_seeds': [{'seed_id': s['seed_id'], 'fuzzer': s['fuzzer'],
                            'trial': s['trial'], 'size': s['size']}
                           for s in blocking],
    }


def _find_regions(top_offsets, top_n):
    """Group adjacent high-MI offsets into contiguous byte regions."""
    if not top_offsets:
        return []

    # Take top N by MI, then sort by offset
    selected = sorted(top_offsets[:top_n * 2], key=lambda x: x['offset'])

    regions = []
    current = None

    for o in selected:
        if current is None:
            current = {'start': o['offset'], 'end': o['offset'],
                       'max_mi': o['mi'], 'offsets': [o]}
        elif o['offset'] <= current['end'] + 2:  # allow 1-byte gap
            current['end'] = o['offset']
            current['max_mi'] = max(current['max_mi'], o['mi'])
            current['offsets'].append(o)
        else:
            regions.append(current)
            current = {'start': o['offset'], 'end': o['offset'],
                       'max_mi': o['mi'], 'offsets': [o]}

    if current:
        regions.append(current)

    # Sort by max MI descending
    regions.sort(key=lambda r: -r['max_mi'])
    return regions


def format_value_dist(values, total):
    """Format value distribution for display."""
    parts = []
    for val, count in values:
        pct = count / total * 100
        if val == -1:
            parts.append(f'EOF({pct:.0f}%)')
        else:
            parts.append(f'0x{val:02x}({pct:.0f}%)')
    return ', '.join(parts)


def print_summary(result):
    """Print human-readable summary."""
    if 'error' in result:
        print(f"Error: {result['error']}")
        return

    print(f"# Seed Diff — Branch {result['branch_id']} ({result['target']})")
    print(f"")
    print(f"Seeds: {result['n_resolving']} resolving, {result['n_blocking']} blocking")
    rs = result['resolving_sizes']
    bs = result['blocking_sizes']
    print(f"Resolving sizes: {rs['min']}-{rs['max']} (mean {rs['mean']:.0f})")
    print(f"Blocking sizes:  {bs['min']}-{bs['max']} (mean {bs['mean']:.0f})")
    if result['size_differs']:
        print(f"*** Size difference detected — length may be a controlling factor ***")
    print()

    # Regions
    if result['regions']:
        print(f"## Top Byte Regions (by mutual information)")
        print()
        for i, reg in enumerate(result['regions'][:10]):
            start, end = reg['start'], reg['end']
            length = end - start + 1
            print(f"### Region {i+1}: bytes[{start}:{end+1}] ({length} byte{'s' if length > 1 else ''}) — MI={reg['max_mi']:.3f}")

            for o in reg['offsets']:
                r_dist = format_value_dist(o['r_values'], o['r_count'])
                b_dist = format_value_dist(o['b_values'], o['b_count'])
                r_ent = f"H={o['r_entropy']:.2f}"
                b_ent = f"H={o['b_entropy']:.2f}"
                print(f"  [{o['offset']:>4}]  resolving: {r_dist:<35} {r_ent}")
                print(f"         blocking:  {b_dist:<35} {b_ent}")

            print()

    # Full top offsets table
    print(f"## Top {len(result['top_offsets'])} Offsets by MI")
    print()
    print(f"| Offset | MI    | Resolving values           | Blocking values            |")
    print(f"|--------|-------|----------------------------|----------------------------|")
    for o in result['top_offsets']:
        r_dist = format_value_dist(o['r_values'], o['r_count'])
        b_dist = format_value_dist(o['b_values'], o['b_count'])
        print(f"| {o['offset']:>6} | {o['mi']:.3f} | {r_dist:<26} | {b_dist:<26} |")


def main():
    parser = argparse.ArgumentParser(
        description='Compute MI-based seed diff for branch clustering')
    parser.add_argument('--target', required=True)
    parser.add_argument('--branch-id', type=int, required=True)
    parser.add_argument('--queue-base', required=True)
    parser.add_argument('--top', type=int, default=15, help='Top N offsets (default 15)')
    parser.add_argument('--max-seeds', type=int, default=10)
    parser.add_argument('--json', action='store_true', help='Output JSON instead of summary')
    parser.add_argument('--db')
    args = parser.parse_args()

    result = analyze_branch(args.target, args.branch_id, args.queue_base,
                            top_n=args.top, max_seeds=args.max_seeds,
                            db_path=args.db)

    if args.json:
        # Clean up for JSON serialization (tuples → lists)
        for o in result.get('top_offsets', []):
            o['r_values'] = [[v, c] for v, c in o['r_values']]
            o['b_values'] = [[v, c] for v, c in o['b_values']]
        for reg in result.get('regions', []):
            for o in reg.get('offsets', []):
                o['r_values'] = [[v, c] for v, c in o['r_values']]
                o['b_values'] = [[v, c] for v, c in o['b_values']]
        print(json.dumps(result, indent=2))
    else:
        print_summary(result)


if __name__ == '__main__':
    main()
