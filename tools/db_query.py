#!/usr/bin/env python3
"""
db_query.py — agent-facing pull queries against blockers.sqlite.

Companion to the push-mode prompts in `tools/study_units.py
evidence-per-branch`. The prompt carries the core evidence for the
common case; this CLI is the escape hatch when the agent needs more
detail than the prompt embeds. Two queries today:

  - `lineage`     ancestor chain of a specific seed (mutation ops walked
                  back from the leaf via the {resolving,blocking}_seed_lineage
                  table). Useful for mechanism attribution — e.g., did
                  `I2SRandReplace` appear in the ancestor chain of a
                  cmplog-winning seed.

  - `more-seeds`  beyond the 5 seeds per direction the prompt shows. Pulls
                  from {resolving,blocking}_seeds with optional fuzzer
                  filter and optional hex-dump of the first N bytes.

Usage:
    python3 tools/db_query.py lineage \\
        --branch 19 --role W --fuzzer cmplog --trial 1 \\
        --seed 006459fd40731a4e

    python3 tools/db_query.py more-seeds \\
        --branch 19 --role W [--fuzzer cmplog] [--limit 20] \\
        [--show-bytes 64] [--queue-base out]

`--role W` = winner-resolving (resolving_seeds / _lineage tables).
`--role L` = loser-blocking  (blocking_seeds  / _lineage tables).

Both subcommands are read-only.
"""

import argparse
import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = TOOLS_DIR.parent
DEFAULT_DB = PROJECT_DIR / 'db' / 'blockers.sqlite'
DEFAULT_QUEUE_BASE = PROJECT_DIR / 'out'

sys.path.insert(0, str(TOOLS_DIR))
from blocker_db import get_db
from seed_utils import hex_dump, read_seed_bytes


def _tables_for_role(role):
    if role == 'W':
        return 'resolving_seeds', 'resolving_seed_lineage'
    if role == 'L':
        return 'blocking_seeds', 'blocking_seed_lineage'
    raise ValueError(f"--role must be W or L, got {role!r}")


def cmd_lineage(args):
    seed_table, lineage_table = _tables_for_role(args.role)
    conn = get_db(args.db)

    # Branch + role sanity
    br = conn.execute(
        "SELECT target, file, line, function, blocked_side FROM branches "
        "WHERE branch_id = ?",
        (args.branch,),
    ).fetchone()
    if br is None:
        print(f"no branch with id={args.branch}", file=sys.stderr)
        sys.exit(2)
    target, file_path, line, function, blocked_side = br

    # Leaf seed metadata (so the agent can see what the lineage leads to)
    leaf = conn.execute(
        f"SELECT discovery_time_s, mutation_op FROM {seed_table} "
        f"WHERE branch_id = ? AND fuzzer = ? AND trial = ? AND seed_id = ?",
        (args.branch, args.fuzzer, args.trial, args.seed),
    ).fetchone()

    lineage = conn.execute(
        f"SELECT depth, ancestor_id, mutation_op FROM {lineage_table} "
        f"WHERE branch_id = ? AND fuzzer = ? AND trial = ? AND seed_id = ? "
        f"ORDER BY depth ASC",
        (args.branch, args.fuzzer, args.trial, args.seed),
    ).fetchall()
    conn.close()

    role_label = "winner-resolving" if args.role == 'W' else "loser-blocking"
    print(f"==== LINEAGE — {role_label} seed {args.seed} ====")
    print(f"branch  : {args.branch}  ({target} {file_path}:{line} "
          f"in {function}, blocked side={blocked_side})")
    print(f"fuzzer  : {args.fuzzer}  trial={args.trial}")
    if leaf is not None:
        disc_t, leaf_op = leaf
        print(f"leaf    : discovered_at={disc_t}s  "
              f"leaf_mutation_op={leaf_op or '-'}")
    else:
        print(f"leaf    : [no row in {seed_table} for this (branch, fuzzer, "
              "trial, seed) — seed_id may be wrong]")
    print()

    if not lineage:
        print(f"[no lineage rows in {lineage_table}]")
        return

    print(f"{'depth':>5}  {'ancestor_id':<20}  mutation_op")
    for depth, ancestor_id, mut in lineage:
        print(f"{depth:>5}  {ancestor_id:<20}  {mut or '-'}")
    print()
    print(f"# {len(lineage)} ancestor levels (max recorded = 50)")


def cmd_more_seeds(args):
    seed_table, _ = _tables_for_role(args.role)
    conn = get_db(args.db)

    br = conn.execute(
        "SELECT target, file, line, function, blocked_side FROM branches "
        "WHERE branch_id = ?",
        (args.branch,),
    ).fetchone()
    if br is None:
        print(f"no branch with id={args.branch}", file=sys.stderr)
        sys.exit(2)
    target, file_path, line, function, blocked_side = br

    where = ["branch_id = ?"]
    params = [args.branch]
    if args.fuzzer:
        where.append("fuzzer = ?")
        params.append(args.fuzzer)
    params.append(args.limit)

    rows = conn.execute(
        f"SELECT fuzzer, trial, seed_id, mutation_op, discovery_time_s "
        f"FROM {seed_table} "
        f"WHERE {' AND '.join(where)} "
        f"ORDER BY discovery_time_s ASC, seed_id ASC LIMIT ?",
        params,
    ).fetchall()
    conn.close()

    role_label = "winner-resolving" if args.role == 'W' else "loser-blocking"
    print(f"==== MORE SEEDS — {role_label} (up to {args.limit}) ====")
    print(f"branch  : {args.branch}  ({target} {file_path}:{line} "
          f"in {function}, blocked side={blocked_side})")
    fz_str = args.fuzzer if args.fuzzer else "<any>"
    print(f"fuzzer  : {fz_str}")
    print()

    if not rows:
        print(f"[no seeds in {seed_table} matching filter]")
        return

    if not args.show_bytes:
        print(f"{'#':>3}  {'fuzzer':<22}  {'trial':>5}  "
              f"{'disc_t':>7}  seed_id (mutation_op)")
        for i, (fz, tr, sid, mut, disc) in enumerate(rows, 1):
            disc_s = "?" if disc is None or disc == -1 else f"{disc}s"
            print(f"{i:>3}  {fz:<22}  {tr:>5}  {disc_s:>7}  "
                  f"{sid}  ({mut or '-'})")
        return

    queue_base = Path(args.queue_base)
    for i, (fz, tr, sid, mut, disc) in enumerate(rows, 1):
        size, data = read_seed_bytes(queue_base, target, fz, tr, sid,
                                     args.show_bytes)
        header = (f"Seed {i} (id={sid}, "
                  f"size={size if size is not None else '?'} bytes, "
                  f"fuzzer={fz}, trial={tr}")
        if disc is not None and disc != -1:
            header += f", discovered_at={disc}s"
        if mut:
            header += f", mutation_op={mut}"
        header += "):"
        print(header)
        if isinstance(data, bytes):
            print(hex_dump(data, args.show_bytes))
        else:
            print(f"  {data}")
    print(f"# {len(rows)} seed(s) shown")


def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument('--db', default=str(DEFAULT_DB),
                   help=f'sqlite DB path (default {DEFAULT_DB})')
    sub = p.add_subparsers(dest='cmd', required=True)

    p_lin = sub.add_parser('lineage',
                           help='ancestor chain for one (branch, fuzzer, trial, seed)')
    p_lin.add_argument('--branch', type=int, required=True)
    p_lin.add_argument('--role', choices=['W', 'L'], required=True,
                       help='W=resolving_seed_lineage, L=blocking_seed_lineage')
    p_lin.add_argument('--fuzzer', required=True)
    p_lin.add_argument('--trial', type=int, required=True)
    p_lin.add_argument('--seed', required=True,
                       help='seed_id hash (the value shown as `id=...` in the prompt)')
    p_lin.set_defaults(handler=cmd_lineage)

    p_more = sub.add_parser('more-seeds',
                            help='extra seeds beyond the 5 the prompt shows')
    p_more.add_argument('--branch', type=int, required=True)
    p_more.add_argument('--role', choices=['W', 'L'], required=True,
                        help='W=resolving_seeds, L=blocking_seeds')
    p_more.add_argument('--fuzzer', help='optional fuzzer filter')
    p_more.add_argument('--limit', type=int, default=20)
    p_more.add_argument('--show-bytes', type=int, default=0,
                        help='if >0, also hex-dump the first N bytes per seed')
    p_more.add_argument('--queue-base', default=str(DEFAULT_QUEUE_BASE),
                        help=f'queue base for byte reads (default {DEFAULT_QUEUE_BASE})')
    p_more.set_defaults(handler=cmd_more_seeds)

    args = p.parse_args()
    args.handler(args)


if __name__ == '__main__':
    main()
