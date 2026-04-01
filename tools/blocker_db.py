#!/usr/bin/env python3
"""
blocker_db.py — CLI for managing the blockers SQLite database.

Usage:
    python3 tools/blocker_db.py init
    python3 tools/blocker_db.py add-blockers --target <name> --input <file.json>
    python3 tools/blocker_db.py enrich --target <name> --table <table> --input <file.json>
    python3 tools/blocker_db.py query --target <name> [--fuzzer F] [--probability ">0.5"] [--format md|csv|json]
    python3 tools/blocker_db.py export --target <name> [--format md|csv|json]
    python3 tools/blocker_db.py compute-derived --target <name>
"""

import argparse
import csv
import io
import json
import os
import sqlite3
import sys

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'blockers.sqlite')


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

SCHEMA_SQL = """
-- Core branch identity. One row per unique blocking branch per target.
CREATE TABLE IF NOT EXISTS branches (
    branch_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    target          TEXT NOT NULL,
    file            TEXT NOT NULL,
    function        TEXT NOT NULL,
    line            INTEGER NOT NULL,
    col             INTEGER NOT NULL,
    blocked_side    TEXT NOT NULL CHECK (blocked_side IN ('T', 'F')),
    source_line     TEXT,
    confirmation_level INTEGER CHECK (confirmation_level IN (1, 2, 3)),
    UNIQUE(target, file, function, line, col, blocked_side)
);

-- Per-fuzzer, per-trial coverage metrics. Populated by branch analyzer.
CREATE TABLE IF NOT EXISTS trial_coverage (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_id       INTEGER NOT NULL REFERENCES branches(branch_id),
    fuzzer          TEXT NOT NULL,
    trial           INTEGER NOT NULL,
    hit_status      INTEGER NOT NULL CHECK (hit_status IN (-1, 0, 1)),
    duration_h      REAL NOT NULL DEFAULT 0.0,
    hitcount        INTEGER NOT NULL DEFAULT 0,
    other_hitcount  INTEGER NOT NULL DEFAULT 0,
    UNIQUE(branch_id, fuzzer, trial)
);

-- Derived per-branch summary metrics. Recomputed from trial_coverage.
CREATE TABLE IF NOT EXISTS derived_metrics (
    branch_id            INTEGER PRIMARY KEY REFERENCES branches(branch_id),
    fuzzer_block_probability   TEXT,    -- JSON: {"fuzzer": p, ...} p = blocked / (blocked+resolved), null if unreached
    fuzzer_avg_hitcount  TEXT,    -- JSON: {"fuzzer": avg, ...} avg hitcount of blocked side across resolved trials; 0 if all blocked; null if unreached
    fuzzer_avg_duration_h TEXT,   -- JSON: {"fuzzer": avg, ...} avg duration across reached trials; null if unreached
    blocking_fuzzers     TEXT,    -- JSON array: fuzzers where p = 1.0 (blocked ALL reached trials)
    resolving_fuzzers    TEXT,    -- JSON array: fuzzers where 0 < p < 1.0 (resolved some but not all)
    unreached_fuzzers    TEXT,    -- JSON array: fuzzers where branch is never reached (all trials = -1)
    rank                 INTEGER
);

-- Resolving seeds: seeds from resolving fuzzers that hit the BLOCKED side.
CREATE TABLE IF NOT EXISTS resolving_seeds (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_id       INTEGER NOT NULL REFERENCES branches(branch_id),
    fuzzer          TEXT NOT NULL,
    trial           INTEGER NOT NULL,
    seed_id         TEXT NOT NULL,
    parent_seed_id  TEXT,
    mutation_op     TEXT,
    discovery_time_s INTEGER,
    UNIQUE(branch_id, fuzzer, trial, seed_id)
);

-- Lineage for resolving seeds.
CREATE TABLE IF NOT EXISTS resolving_seed_lineage (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_id       INTEGER NOT NULL REFERENCES branches(branch_id),
    fuzzer          TEXT NOT NULL,
    trial           INTEGER NOT NULL,
    seed_id         TEXT NOT NULL,
    depth           INTEGER NOT NULL,
    ancestor_id     TEXT NOT NULL,
    mutation_op     TEXT,
    UNIQUE(branch_id, fuzzer, trial, seed_id, depth)
);

-- Blocking seeds: seeds from blocking fuzzers that hit the NON-BLOCKED (other) side.
-- These are the "negative" contrast set — what the blocking fuzzer is stuck producing.
CREATE TABLE IF NOT EXISTS blocking_seeds (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_id       INTEGER NOT NULL REFERENCES branches(branch_id),
    fuzzer          TEXT NOT NULL,
    trial           INTEGER NOT NULL,
    seed_id         TEXT NOT NULL,
    parent_seed_id  TEXT,
    mutation_op     TEXT,
    discovery_time_s INTEGER,
    UNIQUE(branch_id, fuzzer, trial, seed_id)
);

-- Lineage for blocking seeds.
CREATE TABLE IF NOT EXISTS blocking_seed_lineage (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_id       INTEGER NOT NULL REFERENCES branches(branch_id),
    fuzzer          TEXT NOT NULL,
    trial           INTEGER NOT NULL,
    seed_id         TEXT NOT NULL,
    depth           INTEGER NOT NULL,
    ancestor_id     TEXT NOT NULL,
    mutation_op     TEXT,
    UNIQUE(branch_id, fuzzer, trial, seed_id, depth)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_tc_branch ON trial_coverage(branch_id);
CREATE INDEX IF NOT EXISTS idx_tc_fuzzer ON trial_coverage(fuzzer);
CREATE INDEX IF NOT EXISTS idx_branches_target ON branches(target);
CREATE INDEX IF NOT EXISTS idx_rs_branch ON resolving_seeds(branch_id);
CREATE INDEX IF NOT EXISTS idx_rsl_branch ON resolving_seed_lineage(branch_id);
CREATE INDEX IF NOT EXISTS idx_bs_branch ON blocking_seeds(branch_id);
CREATE INDEX IF NOT EXISTS idx_bsl_branch ON blocking_seed_lineage(branch_id);
"""


def get_db(db_path=None):
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    conn = get_db(db_path)
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    print(f"Initialized database at {db_path or DB_PATH}", file=sys.stderr)
    conn.close()


# ---------------------------------------------------------------------------
# add-blockers: insert branch + trial_coverage rows from JSON
# ---------------------------------------------------------------------------

def add_blockers(target, input_file, db_path=None):
    """
    Expected JSON format:
    [
      {
        "file": "elf.cc",
        "function": "ReadSections",
        "line": 1279,
        "col": 29,
        "blocked_side": "T",
        "source_line": "for (Elf64_Xword i = 1; ...)",
        "fuzzers": {
          "naive": {
            "trials": [
              {"trial": 1, "hit_status": 0, "duration_h": 12.0, "hitcount": 0, "other_hitcount": 2968, "confirmation_level": 3},
              {"trial": 2, "hit_status": 0, "duration_h": 12.0, "hitcount": 0, "other_hitcount": 469},
              {"trial": 3, "hit_status": 0, "duration_h": 12.0, "hitcount": 0, "other_hitcount": 5500}
            ]
          },
          "cmplog": { ... }
        }
      },
      ...
    ]
    """
    conn = get_db(db_path)
    conn.executescript(SCHEMA_SQL)  # ensure tables exist

    with open(input_file) as f:
        blockers = json.load(f)

    inserted = 0
    for b in blockers:
        # Upsert branch
        conn.execute("""
            INSERT INTO branches (target, file, function, line, col, blocked_side, source_line)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(target, file, function, line, col, blocked_side) DO UPDATE SET
                source_line = excluded.source_line
        """, (target, b['file'], b['function'], b['line'], b['col'],
              b['blocked_side'], b.get('source_line')))

        branch_id = conn.execute("""
            SELECT branch_id FROM branches
            WHERE target=? AND file=? AND function=? AND line=? AND col=? AND blocked_side=?
        """, (target, b['file'], b['function'], b['line'], b['col'], b['blocked_side'])).fetchone()[0]

        # Insert trial_coverage per fuzzer
        for fuzzer_name, fuzzer_data in b.get('fuzzers', {}).items():
            for t in fuzzer_data.get('trials', []):
                conn.execute("""
                    INSERT INTO trial_coverage (branch_id, fuzzer, trial, hit_status, duration_h, hitcount, other_hitcount, confirmation_level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(branch_id, fuzzer, trial) DO UPDATE SET
                        hit_status = excluded.hit_status,
                        duration_h = excluded.duration_h,
                        hitcount = excluded.hitcount,
                        other_hitcount = excluded.other_hitcount,
                        confirmation_level = excluded.confirmation_level
                """, (branch_id, fuzzer_name, t['trial'], t['hit_status'],
                      t.get('duration_h', 0.0), t.get('hitcount', 0),
                      t.get('other_hitcount', 0), t.get('confirmation_level')))
        inserted += 1

    conn.commit()
    print(f"Added {inserted} blockers for target '{target}'", file=sys.stderr)
    conn.close()


# ---------------------------------------------------------------------------
# compute-derived: recompute derived_metrics from trial_coverage
# ---------------------------------------------------------------------------

def compute_derived(target, db_path=None):
    conn = get_db(db_path)

    branches = conn.execute("""
        SELECT branch_id FROM branches WHERE target = ?
    """, (target,)).fetchall()

    for row in branches:
        bid = row['branch_id']

        trials = conn.execute("""
            SELECT fuzzer, trial, hit_status, duration_h, hitcount
            FROM trial_coverage WHERE branch_id = ?
        """, (bid,)).fetchall()

        if not trials:
            continue

        # Group by fuzzer
        by_fuzzer = {}
        for t in trials:
            by_fuzzer.setdefault(t['fuzzer'], []).append(t)

        # Per-fuzzer: probability, avg_hitcount, avg_duration_h
        # Trials with hit_status=-1 (unreached) are excluded from all calculations
        # duration_h=-1 means N/A (never blocked); excluded from avg
        fuzzer_prob = {}
        fuzzer_hitcount = {}
        fuzzer_duration = {}
        for fz, fz_trials in by_fuzzer.items():
            reached = [t for t in fz_trials if t['hit_status'] in (0, 1)]
            if not reached:
                fuzzer_prob[fz] = None
                fuzzer_hitcount[fz] = None
                fuzzer_duration[fz] = None
                continue

            blocked = sum(1 for t in reached if t['hit_status'] == 0)
            fuzzer_prob[fz] = blocked / len(reached)

            # avg_duration: only over trials that were actually blocked (duration >= 0)
            blocked_trials = [t for t in fz_trials if t['duration_h'] >= 0]
            fuzzer_duration[fz] = (sum(t['duration_h'] for t in blocked_trials) / len(blocked_trials)) if blocked_trials else None

            resolved = [t for t in fz_trials if t['hit_status'] == 1]
            fuzzer_hitcount[fz] = (sum(t['hitcount'] for t in resolved) / len(resolved)) if resolved else 0.0

        # Classify fuzzers:
        # blocking: p = 1.0 (blocked in ALL reached trials)
        # resolving: 0 <= p < 1.0 (resolved at least one trial)
        # unreached: p = None (branch never reached)
        blocking = [f for f, p in fuzzer_prob.items() if p is not None and p == 1.0]
        resolving = [f for f, p in fuzzer_prob.items() if p is not None and p < 1.0]
        unreached = [f for f, p in fuzzer_prob.items() if p is None]

        conn.execute("""
            INSERT INTO derived_metrics
                (branch_id, fuzzer_block_probability, fuzzer_avg_hitcount,
                 fuzzer_avg_duration_h,
                 blocking_fuzzers, resolving_fuzzers, unreached_fuzzers)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(branch_id) DO UPDATE SET
                fuzzer_block_probability = excluded.fuzzer_block_probability,
                fuzzer_avg_hitcount = excluded.fuzzer_avg_hitcount,
                fuzzer_avg_duration_h = excluded.fuzzer_avg_duration_h,
                blocking_fuzzers = excluded.blocking_fuzzers,
                resolving_fuzzers = excluded.resolving_fuzzers,
                unreached_fuzzers = excluded.unreached_fuzzers
        """, (bid, json.dumps(fuzzer_prob), json.dumps(fuzzer_hitcount),
              json.dumps(fuzzer_duration),
              json.dumps(blocking), json.dumps(resolving), json.dumps(unreached)))

    # Rank by fuzzer divergence — larger differences = more interesting
    # 1. probability_div DESC: max - min across fuzzers (excluding unreached)
    # 2. duration_div DESC: max - min across fuzzers (excluding N/A)
    # 3. hitcount_div DESC: max - min across fuzzers (excluding unreached)
    all_derived = conn.execute("""
        SELECT d.branch_id, d.fuzzer_block_probability, d.fuzzer_avg_hitcount,
               d.fuzzer_avg_duration_h
        FROM derived_metrics d
        JOIN branches b ON d.branch_id = b.branch_id
        WHERE b.target = ?
    """, (target,)).fetchall()

    def _divergence(values_dict, null_as=None):
        """Max - min of non-None values. If null_as is set, replace None with that value."""
        if null_as is not None:
            vals = [v if v is not None else null_as for v in values_dict.values()]
        else:
            vals = [v for v in values_dict.values() if v is not None]
        if len(vals) < 2:
            return 0.0
        return max(vals) - min(vals)

    def rank_key(row):
        fp = json.loads(row['fuzzer_block_probability']) if row['fuzzer_block_probability'] else {}
        fh = json.loads(row['fuzzer_avg_hitcount']) if row['fuzzer_avg_hitcount'] else {}
        fd = json.loads(row['fuzzer_avg_duration_h']) if row['fuzzer_avg_duration_h'] else {}
        # prob/hitcount: exclude unreached (null) fuzzers — no data
        # duration: null means "never blocked" = 0 hours stuck — include as 0
        prob_div = _divergence(fp)
        dur_div = _divergence(fd, null_as=0.0)
        hit_div = _divergence(fh)
        # Negate for descending sort (larger divergence = higher priority = lower rank)
        return (-prob_div, -dur_div, -hit_div)

    ranked = sorted(all_derived, key=rank_key)

    for i, row in enumerate(ranked, 1):
        conn.execute("UPDATE derived_metrics SET rank = ? WHERE branch_id = ?",
                     (i, row['branch_id']))

    conn.commit()
    print(f"Computed derived metrics for {len(ranked)} blockers in target '{target}'", file=sys.stderr)
    conn.close()


# ---------------------------------------------------------------------------
# enrich: add seed/lineage data from JSON
# ---------------------------------------------------------------------------

def enrich(target, table, input_file, db_path=None):
    """
    Enrich a seed table with data from JSON.

    Valid tables: resolving_seeds, resolving_seed_lineage, blocking_seeds, blocking_seed_lineage

    Seeds JSON format:
    [
      {
        "file": "elf.cc", "function": "ReadSections", "line": 1279, "col": 29, "blocked_side": "T",
        "fuzzer": "cmplog", "trial": 1,
        "seeds": [
          {"seed_id": "id:000123", "parent_seed_id": "id:000001",
           "mutation_op": "havoc", "discovery_time_s": 3600}
        ]
      }
    ]

    Lineage JSON format:
    [
      {
        "file": "elf.cc", "function": "ReadSections", "line": 1279, "col": 29, "blocked_side": "T",
        "fuzzer": "cmplog", "trial": 1, "seed_id": "id:000123",
        "lineage": [
          {"depth": 0, "ancestor_id": "id:000123", "mutation_op": "havoc"},
          {"depth": 1, "ancestor_id": "id:000001", "mutation_op": "splice"}
        ]
      }
    ]
    """
    seed_tables = ('resolving_seeds', 'blocking_seeds')
    lineage_tables = ('resolving_seed_lineage', 'blocking_seed_lineage')
    if table not in seed_tables + lineage_tables:
        print(f"Error: unknown table '{table}'. Use one of: {seed_tables + lineage_tables}", file=sys.stderr)
        sys.exit(1)

    conn = get_db(db_path)
    with open(input_file) as f:
        data = json.load(f)

    count = 0
    for entry in data:
        branch_id = conn.execute("""
            SELECT branch_id FROM branches
            WHERE target=? AND file=? AND function=? AND line=? AND col=? AND blocked_side=?
        """, (target, entry['file'], entry['function'], entry['line'],
              entry['col'], entry['blocked_side'])).fetchone()

        if not branch_id:
            print(f"Warning: branch not found: {entry['file']}:{entry['line']}:{entry['col']} {entry['blocked_side']}", file=sys.stderr)
            continue
        bid = branch_id[0]

        if table in seed_tables:
            for s in entry.get('seeds', []):
                conn.execute(f"""
                    INSERT INTO {table} (branch_id, fuzzer, trial, seed_id, parent_seed_id, mutation_op, discovery_time_s)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(branch_id, fuzzer, trial, seed_id) DO UPDATE SET
                        parent_seed_id = excluded.parent_seed_id,
                        mutation_op = excluded.mutation_op,
                        discovery_time_s = excluded.discovery_time_s
                """, (bid, entry['fuzzer'], entry['trial'],
                      s['seed_id'], s.get('parent_seed_id'),
                      s.get('mutation_op'), s.get('discovery_time_s')))
                count += 1

        else:  # lineage table
            for l in entry.get('lineage', []):
                conn.execute(f"""
                    INSERT INTO {table} (branch_id, fuzzer, trial, seed_id, depth, ancestor_id, mutation_op)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(branch_id, fuzzer, trial, seed_id, depth) DO UPDATE SET
                        ancestor_id = excluded.ancestor_id,
                        mutation_op = excluded.mutation_op
                """, (bid, entry['fuzzer'], entry['trial'],
                      entry['seed_id'], l['depth'], l['ancestor_id'], l.get('mutation_op')))
                count += 1

    conn.commit()
    print(f"Enriched {count} rows in '{table}' for target '{target}'", file=sys.stderr)
    conn.close()


# ---------------------------------------------------------------------------
# query / export
# ---------------------------------------------------------------------------

def query_blockers(target, fuzzer=None, min_prob=None, max_prob=None, fmt='json', db_path=None):
    conn = get_db(db_path)

    sql = """
        SELECT b.*, d.fuzzer_block_probability, d.fuzzer_avg_hitcount,
               d.fuzzer_avg_duration_h,
               d.blocking_fuzzers, d.resolving_fuzzers, d.unreached_fuzzers, d.rank
        FROM branches b
        LEFT JOIN derived_metrics d ON b.branch_id = d.branch_id
        WHERE b.target = ?
    """
    params = [target]

    # min_prob/max_prob filter not applicable with per-fuzzer probability;
    # kept for backward compat but no-ops
    if min_prob is not None or max_prob is not None:
        pass  # TODO: filter by specific fuzzer probability if needed

    sql += " ORDER BY d.rank ASC"

    rows = conn.execute(sql, params).fetchall()

    if fmt == 'json':
        result = []
        for r in rows:
            entry = dict(r)
            # Parse JSON fields for cleaner output
            for jfield in ('fuzzer_block_probability', 'fuzzer_avg_hitcount',
                          'fuzzer_avg_duration_h', 'blocking_fuzzers',
                          'resolving_fuzzers', 'unreached_fuzzers'):
                if entry.get(jfield) and isinstance(entry[jfield], str):
                    entry[jfield] = json.loads(entry[jfield])
            # Attach trial_coverage
            trials = conn.execute("""
                SELECT fuzzer, trial, hit_status, duration_h, hitcount, other_hitcount, confirmation_level
                FROM trial_coverage WHERE branch_id = ?
                ORDER BY fuzzer, trial
            """, (r['branch_id'],)).fetchall()
            entry['trial_coverage'] = [dict(t) for t in trials]

            # Attach resolving and blocking seeds if any
            for seed_table, key in [('resolving_seeds', 'resolving_seeds'),
                                    ('blocking_seeds', 'blocking_seeds')]:
                seeds = conn.execute(f"""
                    SELECT fuzzer, trial, seed_id, parent_seed_id, mutation_op, discovery_time_s
                    FROM {seed_table} WHERE branch_id = ?
                    ORDER BY fuzzer, trial
                """, (r['branch_id'],)).fetchall()
                if seeds:
                    entry[key] = [dict(s) for s in seeds]

            result.append(entry)
        print(json.dumps(result, indent=2))

    elif fmt == 'csv':
        if not rows:
            return
        writer = csv.writer(sys.stdout)
        writer.writerow(['rank', 'file', 'function', 'line', 'col', 'blocked_side',
                         'source_line', 'fuzzer_block_probability', 'fuzzer_avg_hitcount',
                         'fuzzer_avg_duration_h', 'max_probability',
                         'blocking_fuzzers', 'resolving_fuzzers'])
        for r in rows:
            writer.writerow([r['rank'], r['file'], r['function'], r['line'], r['col'],
                             r['blocked_side'], r['source_line'], r['fuzzer_block_probability'],
                             r['fuzzer_avg_hitcount'], r['fuzzer_avg_duration_h'],
                             r['max_probability'],
                             r['blocking_fuzzers'], r['resolving_fuzzers']])

    elif fmt == 'md':
        if not rows:
            print("No blockers found.")
            return
        # Discover all fuzzers from the first row's fuzzer_block_probability
        fuzzers = []
        if rows and rows[0]['fuzzer_block_probability']:
            fuzzers = sorted(json.loads(rows[0]['fuzzer_block_probability']).keys())

        # Column headers: per-fuzzer probability and hitcount
        hdr_p = " | ".join(f"p({f})" for f in fuzzers)
        hdr_h = " | ".join(f"hits({f})" for f in fuzzers)
        sep_p = " | ".join("------" for _ in fuzzers)
        sep_h = " | ".join("------" for _ in fuzzers)
        print(f"# Blockers — {target}\n")
        print(f"| Rank | File | Line:Col | Side | {hdr_p} | {hdr_h} | Blocking | Resolving | Unreached |")
        print(f"|------|------|----------|------|{sep_p}|{sep_h}|----------|-----------|-----------|")
        for r in rows:
            fp = json.loads(r['fuzzer_block_probability']) if r['fuzzer_block_probability'] else {}
            fh = json.loads(r['fuzzer_avg_hitcount']) if r['fuzzer_avg_hitcount'] else {}

            def fmt_p(f):
                v = fp.get(f)
                if v is None: return "  —"
                return f"{v:.2f}"

            def fmt_h(f):
                v = fh.get(f)
                if v is None: return "  —"
                if v == 0: return "  0"
                if v >= 1_000_000: return f"{v/1e6:.1f}M"
                if v >= 1_000: return f"{v/1e3:.1f}k"
                return f"{v:.0f}"

            probs = " | ".join(fmt_p(f) for f in fuzzers)
            hits = " | ".join(fmt_h(f) for f in fuzzers)
            blocking = r['blocking_fuzzers'] or "[]"
            resolving = r['resolving_fuzzers'] or "[]"
            unreached = r['unreached_fuzzers'] or "[]"
            fname = r['file'].split('/')[-1] if r['file'] else '—'
            print(f"| {r['rank'] or '—'} | {fname} | {r['line']}:{r['col']} | {r['blocked_side']} | {probs} | {hits} | {blocking} | {resolving} | {unreached} |")

    conn.close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Blocker database CLI')
    sub = parser.add_subparsers(dest='command')

    # init
    sub.add_parser('init', help='Initialize the database schema')

    # add-blockers
    p_add = sub.add_parser('add-blockers', help='Insert branch + coverage data from JSON')
    p_add.add_argument('--target', required=True)
    p_add.add_argument('--input', required=True, help='JSON file with blocker data')

    # compute-derived
    p_comp = sub.add_parser('compute-derived', help='Recompute derived metrics from trial_coverage')
    p_comp.add_argument('--target', required=True)

    # enrich
    p_enrich = sub.add_parser('enrich', help='Add seed/lineage data')
    p_enrich.add_argument('--target', required=True)
    p_enrich.add_argument('--table', required=True,
                          choices=['resolving_seeds', 'resolving_seed_lineage',
                                   'blocking_seeds', 'blocking_seed_lineage'])
    p_enrich.add_argument('--input', required=True, help='JSON file with enrichment data')

    # query
    p_query = sub.add_parser('query', help='Query blockers')
    p_query.add_argument('--target', required=True)
    p_query.add_argument('--fuzzer', help='Filter by fuzzer')
    p_query.add_argument('--min-prob', type=float, help='Minimum probability')
    p_query.add_argument('--max-prob', type=float, help='Maximum probability')
    p_query.add_argument('--format', choices=['json', 'csv', 'md'], default='json')

    # export (alias for query with no filters)
    p_export = sub.add_parser('export', help='Export all blockers for a target')
    p_export.add_argument('--target', required=True)
    p_export.add_argument('--format', choices=['json', 'csv', 'md'], default='json')

    args = parser.parse_args()

    if args.command == 'init':
        init_db()
    elif args.command == 'import-extract':
        import_extract(args.target, args.input)
    elif args.command == 'add-blockers':
        add_blockers(args.target, args.input)
    elif args.command == 'compute-derived':
        compute_derived(args.target)
    elif args.command == 'enrich':
        enrich(args.target, args.table, args.input)
    elif args.command == 'query':
        query_blockers(args.target, fuzzer=args.fuzzer,
                       min_prob=args.min_prob, max_prob=args.max_prob,
                       fmt=args.format)
    elif args.command == 'export':
        query_blockers(args.target, fmt=args.format)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
