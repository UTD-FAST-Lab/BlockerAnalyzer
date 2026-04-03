#!/usr/bin/env python3
"""
cluster_report.py — Generate cluster report from DB.

Reads cluster_assignments + derived_metrics + seeds tables and produces
a clean structured markdown report.

Usage:
    python3 tools/cluster_report.py --target lcms [--run-date 2026-04-03] [--output clusters/lcms_clusters.md]
"""

import argparse
import json
import os
import sqlite3
import sys
from collections import defaultdict

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'blockers.sqlite')


def get_db(db_path=None):
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn


def generate_report(target, run_date=None, db_path=None, output=None):
    conn = get_db(db_path)

    # Find the latest run_date if not specified
    if not run_date:
        row = conn.execute(
            'SELECT MAX(run_date) FROM cluster_assignments WHERE target = ?',
            (target,)).fetchone()
        run_date = row[0] if row and row[0] else None
        if not run_date:
            print(f"No cluster assignments found for '{target}'", file=sys.stderr)
            return

    # Load all assignments for this target + run_date
    assignments = conn.execute('''
        SELECT ca.*, b.file, b.function, b.line, b.col, b.blocked_side, b.source_line,
               dm.selection_tags, dm.prob_div, dm.dur_div, dm.hit_div,
               dm.blocking_fuzzers, dm.resolving_fuzzers, dm.unreached_fuzzers
        FROM cluster_assignments ca
        JOIN branches b ON ca.branch_id = b.branch_id
        JOIN derived_metrics dm ON dm.branch_id = b.branch_id
        WHERE ca.target = ? AND ca.run_date = ?
        ORDER BY ca.cluster_id, ca.tier, b.line
    ''', (target, run_date)).fetchall()

    if not assignments:
        print(f"No assignments for '{target}' on {run_date}", file=sys.stderr)
        return

    # Group by cluster
    clusters = defaultdict(list)
    for a in assignments:
        clusters[a['cluster_id']].append(a)

    # Count seeds per branch
    def seed_counts(branch_id):
        rs = conn.execute(
            'SELECT COUNT(*) FROM resolving_seeds WHERE branch_id = ?',
            (branch_id,)).fetchone()[0]
        bs = conn.execute(
            'SELECT COUNT(*) FROM blocking_seeds WHERE branch_id = ?',
            (branch_id,)).fetchone()[0]
        return rs, bs

    # Get all fuzzers for this target
    fuzzers_row = conn.execute('''
        SELECT DISTINCT fuzzer FROM trial_coverage tc
        JOIN branches b ON tc.branch_id = b.branch_id
        WHERE b.target = ? ORDER BY fuzzer
    ''', (target,)).fetchall()
    fuzzers = [r['fuzzer'] for r in fuzzers_row]

    # Build report
    lines = []
    lines.append(f'# Branch Clusters — {target} ({run_date})')
    lines.append(f'')
    lines.append(f'**Clusters:** {len(clusters)}')
    lines.append(f'**Branches assigned:** {len(assignments)}')
    lines.append(f'**Fuzzers:** {", ".join(fuzzers)}')
    lines.append(f'')

    # Summary table
    lines.append('## Summary')
    lines.append('')
    lines.append(f'| Cluster | Branches | Semantic | ' + ' | '.join(fuzzers) + ' |')
    lines.append(f'|---------|----------|----------|' + '|'.join('---' for _ in fuzzers) + '|')

    # Sort clusters by branch count descending
    sorted_clusters = sorted(clusters.items(),
                             key=lambda x: len(x[1]), reverse=True)

    for cid, members in sorted_clusters:
        n = len(members)
        label = members[0]['semantic_label'] or ''
        if len(label) > 30:
            label = label[:27] + '...'

        # Fuzzer distribution
        fcounts = {f: {'R': 0, 'B': 0, 'U': 0} for f in fuzzers}
        for m in members:
            blocking = json.loads(m['blocking_fuzzers']) if m['blocking_fuzzers'] else []
            resolving = json.loads(m['resolving_fuzzers']) if m['resolving_fuzzers'] else []
            unreached = json.loads(m['unreached_fuzzers']) if m['unreached_fuzzers'] else []
            for f in fuzzers:
                if f in resolving:
                    fcounts[f]['R'] += 1
                elif f in blocking:
                    fcounts[f]['B'] += 1
                elif f in unreached:
                    fcounts[f]['U'] += 1

        cells = []
        for f in fuzzers:
            r, b, u = fcounts[f]['R'], fcounts[f]['B'], fcounts[f]['U']
            parts = []
            if r:
                parts.append(f'{r}R')
            if b:
                parts.append(f'{b}B')
            if u:
                parts.append(f'{u}U')
            cells.append('/'.join(parts) if parts else '-')

        lines.append(f'| {cid} | {n} | {label} | ' + ' | '.join(cells) + ' |')

    lines.append('')

    # Detailed cluster sections
    lines.append('## Cluster Details')
    lines.append('')

    for cid, members in sorted_clusters:
        first = members[0]
        lines.append(f'### {cid} — {first["semantic_label"] or ""}')
        lines.append(f'')
        lines.append(f'**Controlling bytes:** {first["controlling_bytes"] or ""}')
        if first['source_mapping']:
            lines.append(f'**Source mapping:** {first["source_mapping"]}')
        lines.append(f'')

        # Branch table
        lines.append(f'| Branch | File | Line:Col | Side | Tags | Resolving | Blocking | RS | BS | Tier | Status |')
        lines.append(f'|--------|------|----------|------|------|-----------|----------|----|----|------|--------|')

        for m in members:
            bid = m['branch_id']
            fname = m['file'].split('/')[-1] if m['file'] else '—'
            tags_raw = json.loads(m['selection_tags']) if m['selection_tags'] else []
            tags = ','.join(t.replace('_div', '') for t in tags_raw) if tags_raw else '—'
            resolving = json.loads(m['resolving_fuzzers']) if m['resolving_fuzzers'] else []
            blocking = json.loads(m['blocking_fuzzers']) if m['blocking_fuzzers'] else []
            res_short = ','.join(_short_fuzzer(f) for f in resolving) if resolving else '—'
            blk_short = ','.join(_short_fuzzer(f) for f in blocking) if blocking else '—'
            rs, bs = seed_counts(bid)
            tier = f'T{m["tier"]}' if m['tier'] else '—'
            status = m['status'] or '—'

            lines.append(f'| {bid} | {fname} | {m["line"]}:{m["col"]} | {m["blocked_side"]} | {tags} | {res_short} | {blk_short} | {rs} | {bs} | {tier} | {status} |')

        # Fuzzer summary for this cluster
        fcounts = {f: {'R': 0, 'B': 0, 'U': 0} for f in fuzzers}
        for m in members:
            blocking = json.loads(m['blocking_fuzzers']) if m['blocking_fuzzers'] else []
            resolving = json.loads(m['resolving_fuzzers']) if m['resolving_fuzzers'] else []
            unreached = json.loads(m['unreached_fuzzers']) if m['unreached_fuzzers'] else []
            for f in fuzzers:
                if f in resolving:
                    fcounts[f]['R'] += 1
                elif f in blocking:
                    fcounts[f]['B'] += 1
                elif f in unreached:
                    fcounts[f]['U'] += 1

        summary_parts = []
        for f in fuzzers:
            r, b, u = fcounts[f]['R'], fcounts[f]['B'], fcounts[f]['U']
            n = len(members)
            pct_r = f'{r/n*100:.0f}%R' if r else ''
            pct_b = f'{b/n*100:.0f}%B' if b else ''
            pct_u = f'{u/n*100:.0f}%U' if u else ''
            parts = '/'.join(p for p in [pct_r, pct_b, pct_u] if p)
            summary_parts.append(f'{_short_fuzzer(f)}: {parts}')

        lines.append(f'')
        lines.append(f'**Fuzzer summary:** {" | ".join(summary_parts)}')
        lines.append(f'')
        lines.append('---')
        lines.append('')

    report = '\n'.join(lines)

    if output:
        with open(output, 'w') as f:
            f.write(report)
        print(f"Report written to {output} ({len(lines)} lines)", file=sys.stderr)
    else:
        print(report)

    conn.close()


def _short_fuzzer(name):
    """Shorten fuzzer names for table display."""
    return {
        'naive': 'naive',
        'cmplog': 'cmplog',
        'value_profile': 'vp',
        'value_profile_cmplog': 'vpc',
    }.get(name, name)


def generate_report_from_json(json_path, db_path=None, output=None):
    """Generate report from orchestrator JSON state file."""
    conn = get_db(db_path)

    with open(json_path) as f:
        state = json.load(f)

    target = state['target']
    run_date = state.get('run_date', '')
    clusters = state.get('clusters', {})

    if not clusters:
        print(f"No clusters in {json_path}", file=sys.stderr)
        return

    # Get fuzzers
    fuzzers_row = conn.execute('''
        SELECT DISTINCT fuzzer FROM trial_coverage tc
        JOIN branches b ON tc.branch_id = b.branch_id
        WHERE b.target = ? ORDER BY fuzzer
    ''', (target,)).fetchall()
    fuzzers = [r['fuzzer'] for r in fuzzers_row]

    def seed_counts(branch_id):
        rs = conn.execute('SELECT COUNT(*) FROM resolving_seeds WHERE branch_id=?',
                          (branch_id,)).fetchone()[0]
        bs = conn.execute('SELECT COUNT(*) FROM blocking_seeds WHERE branch_id=?',
                          (branch_id,)).fetchone()[0]
        return rs, bs

    total_members = sum(len(c['members']) for c in clusters.values())

    lines = []
    lines.append(f'# Branch Clusters — {target} ({run_date})')
    lines.append(f'')
    lines.append(f'**Clusters:** {len(clusters)}')
    lines.append(f'**Branches assigned:** {total_members}')
    lines.append(f'**Skipped:** {len(state.get("skipped", []))}')
    lines.append(f'**Fuzzers:** {", ".join(fuzzers)}')
    lines.append(f'')

    # Summary table
    lines.append('## Summary')
    lines.append('')
    lines.append(f'| Cluster | Branches | Semantic | ' + ' | '.join(fuzzers) + ' |')
    lines.append(f'|---------|----------|----------|' + '|'.join('---' for _ in fuzzers) + '|')

    sorted_clusters = sorted(clusters.items(),
                             key=lambda x: len(x[1]['members']), reverse=True)

    for cid, cdata in sorted_clusters:
        members = cdata['members']
        n = len(members)
        label = cdata.get('semantic_label', '')[:30]

        fcounts = {f: {'R': 0, 'B': 0, 'U': 0} for f in fuzzers}
        for m in members:
            for f in fuzzers:
                if f in m.get('resolving_fuzzers', []):
                    fcounts[f]['R'] += 1
                elif f in m.get('blocking_fuzzers', []):
                    fcounts[f]['B'] += 1
                else:
                    fcounts[f]['U'] += 1

        cells = []
        for f in fuzzers:
            r, b, u = fcounts[f]['R'], fcounts[f]['B'], fcounts[f]['U']
            parts = []
            if r: parts.append(f'{r}R')
            if b: parts.append(f'{b}B')
            if u: parts.append(f'{u}U')
            cells.append('/'.join(parts) if parts else '-')

        lines.append(f'| {cid} | {n} | {label} | ' + ' | '.join(cells) + ' |')

    lines.append('')

    # Detail sections
    lines.append('## Cluster Details')
    lines.append('')

    for cid, cdata in sorted_clusters:
        members = cdata['members']
        lines.append(f'### {cid} — {cdata.get("semantic_label", "")}')
        lines.append(f'')
        lines.append(f'**Controlling bytes:** {cdata.get("controlling_bytes", "")}')
        if cdata.get('source_mapping'):
            lines.append(f'**Source mapping:** {cdata["source_mapping"]}')
        lines.append(f'**Representative:** B{cdata.get("representative", "?")}')
        lines.append(f'')

        lines.append(f'| Branch | File | Line:Col | Side | Tags | Resolving | Blocking | RS | BS | Tier | Status |')
        lines.append(f'|--------|------|----------|------|------|-----------|----------|----|----|------|--------|')

        for m in sorted(members, key=lambda x: (x.get('tier', 9), x.get('line', 0))):
            bid = m['branch_id']
            fname = m.get('file', '').split('/')[-1] or '—'
            tags = ','.join(t.replace('_div', '') for t in m.get('selection_tags', [])) or '—'
            res_short = ','.join(_short_fuzzer(f) for f in m.get('resolving_fuzzers', [])) or '—'
            blk_short = ','.join(_short_fuzzer(f) for f in m.get('blocking_fuzzers', [])) or '—'
            rs, bs = seed_counts(bid)
            tier = f'T{m["tier"]}' if m.get('tier') else '—'
            status = m.get('status', '—')
            test_b = m.get('test_b')
            if test_b and isinstance(test_b, list):
                b_summary = f'{sum(1 for t in test_b if t=="pass")}/{len(test_b)}'
                status = f'{status} (B:{b_summary})'

            lines.append(f'| {bid} | {fname} | {m.get("line","")}:{m.get("col","")} | {m.get("blocked_side","")} | {tags} | {res_short} | {blk_short} | {rs} | {bs} | {tier} | {status} |')

        # Fuzzer summary
        fcounts = {f: {'R': 0, 'B': 0, 'U': 0} for f in fuzzers}
        for m in members:
            for f in fuzzers:
                if f in m.get('resolving_fuzzers', []):
                    fcounts[f]['R'] += 1
                elif f in m.get('blocking_fuzzers', []):
                    fcounts[f]['B'] += 1
                else:
                    fcounts[f]['U'] += 1

        summary_parts = []
        n = len(members)
        for f in fuzzers:
            r, b, u = fcounts[f]['R'], fcounts[f]['B'], fcounts[f]['U']
            pct_r = f'{r/n*100:.0f}%R' if r else ''
            pct_b = f'{b/n*100:.0f}%B' if b else ''
            pct_u = f'{u/n*100:.0f}%U' if u else ''
            parts = '/'.join(p for p in [pct_r, pct_b, pct_u] if p)
            summary_parts.append(f'{_short_fuzzer(f)}: {parts}')

        lines.append(f'')
        lines.append(f'**Fuzzer summary:** {" | ".join(summary_parts)}')
        lines.append(f'')
        lines.append('---')
        lines.append('')

    # Skipped branches
    skipped = state.get('skipped', [])
    if skipped:
        lines.append('## Skipped Branches')
        lines.append('')
        lines.append('| Branch | Reason |')
        lines.append('|--------|--------|')
        for s in skipped:
            lines.append(f'| {s["branch_id"]} | {s.get("reason", "")} |')
        lines.append('')

    report = '\n'.join(lines)

    if output:
        with open(output, 'w') as f:
            f.write(report)
        print(f"Report written to {output} ({len(lines)} lines)", file=sys.stderr)
    else:
        print(report)

    conn.close()


def main():
    parser = argparse.ArgumentParser(description='Generate cluster report')
    parser.add_argument('--target', required=True)
    parser.add_argument('--run-date', help='Run date (default: latest)')
    parser.add_argument('--from-json', help='Read from orchestrator JSON state file instead of DB')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    parser.add_argument('--db', help='Database path')
    args = parser.parse_args()

    if args.from_json:
        generate_report_from_json(args.from_json, db_path=args.db, output=args.output)
    else:
        generate_report(args.target, run_date=args.run_date,
                        db_path=args.db, output=args.output)


if __name__ == '__main__':
    main()
