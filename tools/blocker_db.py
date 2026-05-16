#!/usr/bin/env python3
"""
blocker_db.py — schema management for db/blockers.sqlite.

The DB is populated by tools/study_units.py (`add-canonical`, which writes
`branches` + `study_subjects` + `subject_branches`) and tools/seed_bisect.py
(which writes the seed + lineage tables directly). This module only owns
the schema definition and the `init` command.

Usage:
    python3 tools/blocker_db.py init
"""

import argparse
import os
import sqlite3
import sys

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'blockers.sqlite')


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

SCHEMA_SQL = """
-- Core branch identity. One row per unique blocking branch per target.
-- Admission rule (subject-centric, 2026-05-16): a branch is in this table iff
-- ≥1 canonical subject's per-subject input-dependence rule admits it.
-- Per-subject admission (in subject_branches): across the 20 trials of (A, B)
-- canonical pair, ≥1 trial blocked AND ≥1 trial resolved at final checkpoint.
-- Branch identity is (target, file, line, col, blocked_side) — `function` is a
-- deterministic derivation from (file, line) via tools/extract_functions.py and
-- is descriptive only, not part of the unique key (so it can be refreshed
-- in-place when the function index is rebuilt).
CREATE TABLE IF NOT EXISTS branches (
    branch_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    target          TEXT NOT NULL,
    file            TEXT NOT NULL,
    function        TEXT NOT NULL,
    line            INTEGER NOT NULL,
    col             INTEGER NOT NULL,
    blocked_side    TEXT NOT NULL CHECK (blocked_side IN ('T', 'F')),
    source_line     TEXT,
    UNIQUE(target, file, line, col, blocked_side)
);

-- Resolving seeds: seeds from resolving fuzzers that hit the BLOCKED side.
-- Populated by seed_bisect.py (`insert` / `run`).
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


def main():
    parser = argparse.ArgumentParser(description='Blocker database CLI')
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('init', help='Initialize the database schema')

    args = parser.parse_args()
    if args.command == 'init':
        init_db()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
