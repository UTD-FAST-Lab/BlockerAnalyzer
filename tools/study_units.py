#!/usr/bin/env python3
"""
study_units.py — per-subject (target, A, B) blocker tables for the
metaphorical-testing pipeline.

A subject is `(target, fuzzer A, fuzzer B)` where A and B differ in exactly
one technique (the canonical comparable-pair set). For each subject we
register significance stats (delegating to subject_significance.pair_significance)
and materialize one row per branch that meets the per-subject admission
rule: across the 20 trials of (A, B), ≥1 blocked AND ≥1 resolved at final
checkpoint. Per-branch aggregates and direction-oriented divergences let
us rank candidate B-unique blockers (or A-unique, when B beats A).

Subcommands
-----------
    init                  create the two tables (idempotent)
    add                   register/refresh ONE subject; populate subject_branches
    add-canonical         add all 4 canonical pairs for one or more targets
                          (per-target coverage walk shared across the 4 subjects)
    list                  list registered subjects
    top                   print ranked candidate branches for one subject
    evidence-per-branch   emit per-branch structured prompt for
                          feature-hypothesis-generator — collapses ALL
                          canonical pairs satisfying ≥8/≥8 at this branch
                          into one prompt.

The legacy `candidates`, `candidates-csv`, `rank`, and `evidence`
subcommands were removed 2026-05-16; per-branch candidate aggregation lives
in tools/build_candidates.py and the agent prompt builder is
`evidence-per-branch`.

Design choices:
- Canonical pairs only by default — non-canonical pairs require an explicit
  --delta-technique override, since one-technique-delta is the admissibility
  cornerstone of metaphorical testing.
- prob_div / dur_div / hit_div are stored *direction-oriented*: positive
  always means "the loser is worse than the winner at this branch". Sign is
  fixed at populate time; refreshing the subject re-derives it.
- Strict policy (default) for top: winner resolved every trial, loser
  resolved zero. Majority is a knob; "all" disables filtering and surfaces
  the raw ranking.
- (2026-05-16 redesign) Admission is per-subject: a branch lands in
  `branches` iff some canonical subject admits it (≥1 of 20 trials blocked
  AND ≥1 resolved at final checkpoint). Per-target coverage walk happens
  once and is shared across the 4 subjects (Option A).
"""

import argparse
import json
import re
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timezone
from math import ceil, floor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seed_utils import parse_count as _shared_parse_count  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = REPO_ROOT / "db" / "blockers.sqlite"
DEFAULT_TS_BASE = REPO_ROOT / "out" / "coverage_ts"

CANONICAL_TARGETS = [
    "curl", "harfbuzz", "jsoncpp", "libpng", "libxml2",
    "openthread", "woff2", "lcms", "bloaty", "sqlite3",
]
CANONICAL_PAIRS = [
    ("cmplog",                "naive",         "I2S"),
    ("value_profile",         "naive",         "value_profile"),
    ("value_profile_cmplog",  "cmplog",        "value_profile"),
    ("value_profile_cmplog",  "value_profile", "I2S"),
]

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS study_subjects (
    subject_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    target          TEXT NOT NULL,
    A               TEXT NOT NULL,
    B               TEXT NOT NULL,
    delta_technique TEXT NOT NULL,
    n_A             INTEGER, n_B INTEGER,
    mean_auc_A      REAL,    mean_auc_B    REAL,
    delta_auc       REAL,    p_auc         REAL,    auc_dir   TEXT,
    mean_final_A    REAL,    mean_final_B  REAL,
    delta_final     REAL,    p_final       REAL,    final_dir TEXT,
    admissible      INTEGER,
    direction       TEXT,    -- 'A>B' / 'B>A' / 'tie' (orientation for divs)
    n_branches      INTEGER, -- count of input-dependent branches in this subject
    refreshed_at    TEXT,
    UNIQUE(target, A, B)
);
CREATE INDEX IF NOT EXISTS idx_subjects_target ON study_subjects(target);

CREATE TABLE IF NOT EXISTS subject_branches (
    subject_id      INTEGER NOT NULL REFERENCES study_subjects(subject_id) ON DELETE CASCADE,
    branch_id       INTEGER NOT NULL REFERENCES branches(branch_id),
    n_A_resolved    INTEGER, n_A_blocked INTEGER, n_A_unreached INTEGER,
    n_B_resolved    INTEGER, n_B_blocked INTEGER, n_B_unreached INTEGER,
    -- Trial-set JSON arrays (which specific trials had each outcome). Used by
    -- seed_bisect to pick a representative resolving/blocking (fuzzer, trial)
    -- without re-introducing a per-trial fact table. Unreached trials omitted
    -- (derivable as {1..n} minus resolved ∪ blocked).
    A_resolved_trials TEXT, A_blocked_trials TEXT,
    B_resolved_trials TEXT, B_blocked_trials TEXT,
    p_A_blocked     REAL,    p_B_blocked REAL,    prob_div REAL,  -- direction-oriented
    avg_dur_A       REAL,    avg_dur_B   REAL,    dur_div  REAL,  -- direction-oriented
    avg_hits_A      REAL,    avg_hits_B  REAL,    hit_div  REAL,  -- direction-oriented
    hypothesis_label TEXT,   template_id TEXT,
    PRIMARY KEY (subject_id, branch_id)
);
CREATE INDEX IF NOT EXISTS idx_sb_subject ON subject_branches(subject_id);
CREATE INDEX IF NOT EXISTS idx_sb_branch  ON subject_branches(branch_id);
"""


CANONICAL_FUZZERS = ["naive", "cmplog", "value_profile", "value_profile_cmplog"]
DEFAULT_N_TRIALS = 10
DEFAULT_STEP_S = 1800  # 30 min checkpoint cadence


def open_db(path):
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# ─── coverage parser (inlined from extract_blockers_ts.py, retired 2026-05-16) ──

_BRANCH_RE = re.compile(
    r'Branch \((\d+):(\d+)\): \[True: ([^\],]+), False: ([^\]]+)\]'
)


def _parse_count(s):
    """Wrapper around seed_utils.parse_count that returns 0 instead of None.

    Legacy callers (the per-target coverage walk) expect an int. Branch
    counts in llvm-cov output are never empty, so None handling defensively
    becomes 0.
    """
    return _shared_parse_count(s) or 0


def _parse_coverage_file(path):
    """Parse an llvm-cov show file. Returns {(file, line, col): (T_hits, F_hits)}."""
    results = {}
    current_file = None
    with open(path) as f:
        for line in f:
            stripped = line.strip()
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


def _extract_source_lines(cov_file):
    """Extract source-line text per (file, line) from one llvm-cov show file."""
    results = {}
    current_file = None
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


# ─── per-target walk (Option A: parse once, share across subjects) ──────────

def walk_target_state(target, ts_base, fuzzers=None, n_trials=DEFAULT_N_TRIALS,
                      step_s=DEFAULT_STEP_S, verbose=False):
    """Walk all checkpoints for (fuzzer, trial) under one target.

    Returns:
      branch_state: dict {(file, line, col, side): dict {(fuzzer, trial): leaf}}
        leaf has: hit_status (-1/0/1), duration_h (-1.0 = never blocked,
        ≥0 = time spent blocked), hitcount (this side at final),
        other_hitcount (other side at final).
      source_lines: dict {(file, line): str}
    """
    fuzzers = fuzzers or CANONICAL_FUZZERS
    ts_base = Path(ts_base)
    target_dir = ts_base / target
    if not target_dir.is_dir():
        raise FileNotFoundError(f"target dir not found: {target_dir}")

    # Discover checkpoints across the whole target
    checkpoints = set()
    for fz in fuzzers:
        for trial in range(1, n_trials + 1):
            reports = target_dir / fz / f"trial{trial}" / "reports"
            if reports.is_dir():
                for d in reports.iterdir():
                    if d.name.isdigit():
                        checkpoints.add(int(d.name))
    if not checkpoints:
        return {}, {}
    checkpoints = sorted(checkpoints)
    step_h = step_s / 3600.0

    branch_state = defaultdict(dict)

    for cp in checkpoints:
        for fz in fuzzers:
            for trial in range(1, n_trials + 1):
                cov = target_dir / fz / f"trial{trial}" / "reports" / str(cp) / "branch_coverage_show.txt"
                if not cov.is_file():
                    continue
                bd = _parse_coverage_file(str(cov))
                ft = (fz, trial)
                for (file, line, col), (th, fh) in bd.items():
                    for side in ('T', 'F'):
                        bkey = (file, line, col, side)
                        blocked_hits = th if side == 'T' else fh
                        other_hits   = fh if side == 'T' else th
                        if ft not in branch_state[bkey]:
                            branch_state[bkey][ft] = {
                                'hit_status': -1, 'duration_h': -1.0,
                                'hitcount': 0, 'other_hitcount': 0,
                            }
                        s = branch_state[bkey][ft]
                        s['hitcount'] = blocked_hits
                        s['other_hitcount'] = other_hits
                        if blocked_hits > 0:
                            new = 1
                        elif other_hits > 0:
                            new = 0
                        else:
                            new = -1
                        if new > s['hit_status']:
                            s['hit_status'] = new
                        if s['hit_status'] == 0:
                            if s['duration_h'] < 0:
                                s['duration_h'] = 0.0
                            s['duration_h'] += step_h
        if verbose:
            n_asym = sum(1 for sts in branch_state.values()
                         if any(s['hit_status'] == 0 for s in sts.values()))
            print(f"  T={cp/3600:.1f}h: {len(branch_state)} sides tracked, "
                  f"{n_asym} with ≥1 blocked trial", file=sys.stderr)

    # Source lines: take from first available trial1 final-checkpoint coverage
    final_t = checkpoints[-1]
    source_lines = {}
    for fz in fuzzers:
        cov = target_dir / fz / "trial1" / "reports" / str(final_t) / "branch_coverage_show.txt"
        if cov.is_file():
            source_lines.update(_extract_source_lines(str(cov)))
            break

    return dict(branch_state), source_lines


def _empty(v):
    """pair_significance returns '' for fields when n is too small. Convert to None."""
    return None if v == "" else v


def _adm(v):
    # pair_significance returns numpy.bool_ at scipy>=1.x, plain bool elsewhere,
    # 'insufficient_trials' (str) when n<2, or '' when no trials. Use truthiness
    # only for genuine booleans.
    if v is None or isinstance(v, str):
        return None
    return int(bool(v))


def _direction_from(stats):
    auc_dir = stats.get("auc_dir") or ""
    fin_dir = stats.get("final_dir") or ""
    if auc_dir in ("A>B", "B>A"):
        return auc_dir
    if fin_dir in ("A>B", "B>A"):
        return fin_dir
    return "tie"


def _infer_delta_technique(a, b):
    for ca, cb, dt in CANONICAL_PAIRS:
        if ca == a and cb == b:
            return dt
    return None


# ── upsert subject + populate branches ─────────────────────────────────────

def upsert_subject(conn, target, a, b, stats):
    direction = _direction_from(stats)
    cols_vals = {
        "target":           target, "A": a, "B": b,
        "delta_technique":  stats["delta_technique"],
        "n_A":              stats.get("n_A") or 0,
        "n_B":              stats.get("n_B") or 0,
        "mean_auc_A":       _empty(stats.get("mean_auc_A")),
        "mean_auc_B":       _empty(stats.get("mean_auc_B")),
        "delta_auc":        _empty(stats.get("delta_auc")),
        "p_auc":            _empty(stats.get("p_auc")),
        "auc_dir":          _empty(stats.get("auc_dir")),
        "mean_final_A":     _empty(stats.get("mean_final_A")),
        "mean_final_B":     _empty(stats.get("mean_final_B")),
        "delta_final":      _empty(stats.get("delta_final")),
        "p_final":          _empty(stats.get("p_final")),
        "final_dir":        _empty(stats.get("final_dir")),
        "admissible":       _adm(stats.get("admissible")),
        "direction":        direction,
        "refreshed_at":     datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    cols = list(cols_vals.keys())
    placeholders = ",".join("?" * len(cols))
    cols_list = ",".join(cols)
    update_clause = ",".join(
        f"{c}=excluded.{c}" for c in cols if c not in ("target", "A", "B")
    )
    conn.execute(
        f"INSERT INTO study_subjects ({cols_list}) VALUES ({placeholders}) "
        f"ON CONFLICT(target, A, B) DO UPDATE SET {update_clause}",
        [cols_vals[c] for c in cols],
    )
    return conn.execute(
        "SELECT subject_id FROM study_subjects WHERE target=? AND A=? AND B=?",
        (target, a, b),
    ).fetchone()[0]


def _basename(file):
    return file.rsplit('/', 1)[-1] if '/' in file else file


def build_function_index(target):
    """Per-target {file: [(start_line, end_line, name), ...]} index for
    (file, line) → function lookup. Function names are demangled (c++filt).

    Built by importing tools/extract_functions.py, which runs `llvm-cov export`
    inside the `libafl-<target>-cov` Docker image (~1-2s per target).

    Returns {} if extraction fails (Docker unavailable, image missing, etc.) —
    callers should fall back to basename(file) for the function column.
    """
    sys.path.insert(0, str(REPO_ROOT / "tools"))
    try:
        import extract_functions
        fns = extract_functions.extract(target)
    except Exception as exc:
        print(f"  function-index extraction failed for {target}: {exc}; "
              f"falling back to basename(file) for branches.function",
              file=sys.stderr)
        return {}

    if not fns:
        return {}

    # Demangle once per unique name (batch into one c++filt invocation)
    unique_names = sorted({f["name"] for f in fns})
    try:
        import subprocess
        proc = subprocess.run(
            ["c++filt"], input="\n".join(unique_names),
            capture_output=True, text=True, check=True, timeout=30,
        )
        name_map = dict(zip(unique_names, proc.stdout.rstrip("\n").split("\n")))
    except (FileNotFoundError, subprocess.SubprocessError) as exc:
        print(f"  c++filt unavailable ({exc}); function names will be mangled",
              file=sys.stderr)
        name_map = {n: n for n in unique_names}

    idx = defaultdict(list)
    for f in fns:
        idx[f["file"]].append((f["start_line"], f["end_line"], name_map.get(f["name"], f["name"])))
    return dict(idx)


def _lookup_function(fn_index, file, line, fallback):
    """Innermost function (smallest range) containing (file, line). Falls back
    to `fallback` (typically basename(file)) when no match or no index."""
    if not fn_index:
        return fallback
    candidates = [t for t in fn_index.get(file, []) if t[0] <= line <= t[1]]
    if not candidates:
        return fallback
    # smallest range; tie-break by start_line then name
    return min(candidates, key=lambda t: (t[1] - t[0], t[0], t[2]))[2]


def _upsert_branch(conn, target, file, line, col, side, source_line, function):
    """Insert branches row (or find existing). Branch identity is
    (target, file, line, col, side); `function` is descriptive and refreshed
    on conflict so re-runs with a rebuilt function index update in-place.
    Returns branch_id.
    """
    conn.execute(
        """INSERT INTO branches (target, file, function, line, col, blocked_side, source_line)
           VALUES (?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(target, file, line, col, blocked_side) DO UPDATE SET
               function    = COALESCE(excluded.function, branches.function),
               source_line = COALESCE(excluded.source_line, branches.source_line)""",
        (target, file, function, line, col, side, source_line),
    )
    return conn.execute(
        """SELECT branch_id FROM branches
           WHERE target=? AND file=? AND line=? AND col=? AND blocked_side=?""",
        (target, file, line, col, side),
    ).fetchone()[0]


def populate_subject_branches(conn, subject_id, target, a, b, direction,
                              state, source_lines, fn_index=None):
    """Apply per-subject admission rule to the per-target state dict and
    materialize subject_branches for (subject_id, target, A=a, B=b).

    Per-subject admission: across the 20 trials of (A, B), ≥1 blocked AND
    ≥1 resolved at final checkpoint. (Trials with unreached side are
    neither — they don't contribute to admission.)

    `fn_index` (optional, from build_function_index) maps (file, line) to the
    enclosing function name. When provided, admitted branches store the real
    function name; otherwise they fall back to basename(file).

    Side effect: ensures branches rows exist for admitted (file,line,col,side)
    tuples (target-level admission = union of per-subject admissions).

    Returns row count.
    """
    conn.execute("DELETE FROM subject_branches WHERE subject_id = ?", (subject_id,))
    sign = {"A>B": +1, "B>A": -1}.get(direction, 0)
    rows = []

    for bkey, ft_states in state.items():
        file, line, col, side = bkey

        # Partition trial states into A and B arms
        a_trials = {}  # trial → leaf state
        b_trials = {}
        for (fz, trial), s in ft_states.items():
            if fz == a:
                a_trials[trial] = s
            elif fz == b:
                b_trials[trial] = s

        a_res = sorted(t for t, s in a_trials.items() if s['hit_status'] == 1)
        a_blk = sorted(t for t, s in a_trials.items() if s['hit_status'] == 0)
        a_unr = sum(1 for s in a_trials.values() if s['hit_status'] == -1)
        b_res = sorted(t for t, s in b_trials.items() if s['hit_status'] == 1)
        b_blk = sorted(t for t, s in b_trials.items() if s['hit_status'] == 0)
        b_unr = sum(1 for s in b_trials.values() if s['hit_status'] == -1)

        # Per-subject admission rule (≥1 blocked AND ≥1 resolved across 20)
        if (len(a_res) + len(b_res)) == 0 or (len(a_blk) + len(b_blk)) == 0:
            continue

        function = _lookup_function(fn_index, file, line, fallback=_basename(file))
        branch_id = _upsert_branch(
            conn, target, file, line, col, side,
            source_lines.get((file, line)), function,
        )

        n_A_res, n_A_blk = len(a_res), len(a_blk)
        n_B_res, n_B_blk = len(b_res), len(b_blk)
        n_A_reached = n_A_res + n_A_blk
        n_B_reached = n_B_res + n_B_blk

        p_A = (n_A_blk / n_A_reached) if n_A_reached > 0 else None
        p_B = (n_B_blk / n_B_reached) if n_B_reached > 0 else None

        def _avg_dur(trial_states):
            reached = [s for s in trial_states if s['hit_status'] != -1]
            if not reached:
                return None
            return sum(max(0.0, s['duration_h']) for s in reached) / len(reached)

        def _avg_hits(trial_states):
            reached = [s for s in trial_states if s['hit_status'] != -1]
            if not reached:
                return None
            return sum(s['hitcount'] for s in reached) / len(reached)

        avg_dur_A  = _avg_dur(a_trials.values())
        avg_dur_B  = _avg_dur(b_trials.values())
        avg_hits_A = _avg_hits(a_trials.values())
        avg_hits_B = _avg_hits(b_trials.values())

        # Direction-oriented divergences (positive ⇒ loser worse than winner).
        if sign == 1:    # A>B (A winner, B loser)
            prob_div = (p_B or 0) - (p_A or 0) if (p_A is not None or p_B is not None) else None
            dur_div  = (avg_dur_B  or 0) - (avg_dur_A  or 0)
            hit_div  = (avg_hits_A or 0) - (avg_hits_B or 0)
        elif sign == -1: # B>A
            prob_div = (p_A or 0) - (p_B or 0) if (p_A is not None or p_B is not None) else None
            dur_div  = (avg_dur_A  or 0) - (avg_dur_B  or 0)
            hit_div  = (avg_hits_B or 0) - (avg_hits_A or 0)
        else:            # tie — unsigned magnitudes
            prob_div = abs((p_B or 0) - (p_A or 0)) if (p_A is not None or p_B is not None) else None
            dur_div  = abs((avg_dur_B  or 0) - (avg_dur_A  or 0))
            hit_div  = abs((avg_hits_A or 0) - (avg_hits_B or 0))

        rows.append((
            subject_id, branch_id,
            n_A_res, n_A_blk, a_unr,
            n_B_res, n_B_blk, b_unr,
            json.dumps(a_res), json.dumps(a_blk),
            json.dumps(b_res), json.dumps(b_blk),
            p_A, p_B, prob_div,
            avg_dur_A, avg_dur_B, dur_div,
            avg_hits_A, avg_hits_B, hit_div,
        ))

    conn.executemany(
        """INSERT INTO subject_branches (
               subject_id, branch_id,
               n_A_resolved, n_A_blocked, n_A_unreached,
               n_B_resolved, n_B_blocked, n_B_unreached,
               A_resolved_trials, A_blocked_trials,
               B_resolved_trials, B_blocked_trials,
               p_A_blocked, p_B_blocked, prob_div,
               avg_dur_A, avg_dur_B, dur_div,
               avg_hits_A, avg_hits_B, hit_div
           ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        rows,
    )
    return len(rows)


# ── subcommands ─────────────────────────────────────────────────────────────

def cmd_init(args):
    conn = open_db(args.db)
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()
    print(f"initialized {args.db}", file=sys.stderr)


def _add_one(conn, target, a, b, delta_tech, ts_base, alpha, mannwhitneyu,
             state=None, source_lines=None, fn_index=None):
    """Register/refresh one subject (target, a, b).

    If `state`, `source_lines`, and `fn_index` are provided (per-target walk
    + function index shared across the 4 canonical subjects), they're used
    directly. Otherwise this builds them on-the-fly (single-subject use case).
    """
    sys.path.insert(0, str(REPO_ROOT / "tools"))
    from subject_significance import pair_significance
    stats = pair_significance(target, a, b, delta_tech, ts_base, mannwhitneyu, alpha)
    stats["delta_technique"] = delta_tech
    sid = upsert_subject(conn, target, a, b, stats)
    direction = conn.execute(
        "SELECT direction FROM study_subjects WHERE subject_id=?", (sid,)
    ).fetchone()[0]
    if state is None or source_lines is None:
        state, source_lines = walk_target_state(target, ts_base)
    if fn_index is None:
        fn_index = build_function_index(target)
    n_branches = populate_subject_branches(
        conn, sid, target, a, b, direction, state, source_lines, fn_index=fn_index,
    )
    conn.execute(
        "UPDATE study_subjects SET n_branches=? WHERE subject_id=?",
        (n_branches, sid),
    )
    return sid, direction, n_branches, stats


def cmd_add(args):
    try:
        from scipy.stats import mannwhitneyu
    except ImportError:
        print("error: scipy required for significance computation", file=sys.stderr)
        sys.exit(2)

    delta_tech = args.delta_technique or _infer_delta_technique(args.A, args.B)
    if delta_tech is None:
        print(
            f"error: ({args.A}, {args.B}) is not a canonical comparable pair; "
            f"pass --delta-technique to override",
            file=sys.stderr,
        )
        sys.exit(2)

    conn = open_db(args.db)
    conn.executescript(SCHEMA_SQL)
    sid, direction, n_branches, stats = _add_one(
        conn, args.target, args.A, args.B, delta_tech,
        Path(args.ts_base).resolve(), args.alpha, mannwhitneyu,
    )
    conn.commit()
    conn.close()
    print(
        f"subject {sid}: target={args.target} A={args.A} B={args.B} "
        f"Δ={delta_tech} n_A={stats.get('n_A')} n_B={stats.get('n_B')} "
        f"dir={direction} adm={stats.get('admissible')!r} "
        f"n_branches={n_branches}",
        file=sys.stderr,
    )


def cmd_add_canonical(args):
    try:
        from scipy.stats import mannwhitneyu
    except ImportError:
        print("error: scipy required", file=sys.stderr)
        sys.exit(2)

    targets = args.targets or CANONICAL_TARGETS
    ts_base = Path(args.ts_base).resolve()
    conn = open_db(args.db)
    conn.executescript(SCHEMA_SQL)
    for tgt in targets:
        # Option A: walk the target's coverage once, share state across the 4 subjects.
        print(f"== walking {tgt} ==", file=sys.stderr)
        try:
            state, source_lines = walk_target_state(tgt, ts_base)
        except FileNotFoundError as e:
            print(f"  skip {tgt}: {e}", file=sys.stderr)
            continue
        n_sides = len(state)
        n_asym = sum(
            1 for sts in state.values()
            if any(s['hit_status'] == 0 for s in sts.values())
        )
        print(f"  {n_sides} branch sides tracked, {n_asym} with ≥1 blocked trial",
              file=sys.stderr)
        # Build the demangled function index once per target (Docker, ~1-2s).
        # Used at upsert time so branches.function gets the real C/C++ name
        # rather than the basename placeholder.
        fn_index = build_function_index(tgt)

        for a, b, dt in CANONICAL_PAIRS:
            try:
                sid, direction, n_branches, stats = _add_one(
                    conn, tgt, a, b, dt, ts_base, args.alpha, mannwhitneyu,
                    state=state, source_lines=source_lines, fn_index=fn_index,
                )
                print(
                    f"  {tgt:<10} {a:<22} vs {b:<22}  Δ={dt:<14} "
                    f"n=({stats.get('n_A')},{stats.get('n_B')}) "
                    f"dir={direction:<3}  n_br={n_branches}",
                    file=sys.stderr,
                )
            except Exception as exc:
                print(f"  {tgt} {a} vs {b}: FAILED — {exc}", file=sys.stderr)
    conn.commit()
    conn.close()


def cmd_list(args):
    conn = open_db(args.db)
    rows = conn.execute(
        """SELECT subject_id, target, A, B, delta_technique, n_A, n_B,
                  ROUND(delta_auc, 0), p_auc, auc_dir,
                  ROUND(delta_final, 0), p_final, final_dir,
                  admissible, direction, n_branches, refreshed_at
           FROM study_subjects
           ORDER BY target, A, B"""
    ).fetchall()
    conn.close()
    if not rows:
        print("(no subjects)")
        return
    headers = [
        "id", "target", "A", "B", "Δtech", "n_A", "n_B",
        "ΔAUC", "p_AUC", "auc_dir",
        "Δfin", "p_fin", "fin_dir",
        "adm", "dir", "n_br", "refreshed",
    ]
    print("\t".join(headers))
    for r in rows:
        print("\t".join("" if v is None else str(v) for v in r))


def cmd_top(args):
    conn = open_db(args.db)
    subj = conn.execute(
        "SELECT target, A, B, n_A, n_B, direction FROM study_subjects WHERE subject_id=?",
        (args.subject_id,),
    ).fetchone()
    if subj is None:
        print(f"no subject with id={args.subject_id}", file=sys.stderr)
        sys.exit(2)
    target, a, b, n_a, n_b, direction = subj

    where = ["sb.subject_id = ?"]
    params = [args.subject_id]
    if args.policy != "all" and direction in ("A>B", "B>A"):
        if direction == "A>B":
            winner_col, loser_col = "n_A_resolved", "n_B_resolved"
            n_winner, n_loser = n_a, n_b
        else:
            winner_col, loser_col = "n_B_resolved", "n_A_resolved"
            n_winner, n_loser = n_b, n_a
        if args.policy == "strict":
            where.append(f"{winner_col} = ?")
            where.append(f"{loser_col} = 0")
            params.append(n_winner)
        elif args.policy == "majority":
            where.append(f"{winner_col} >= ?")
            where.append(f"{loser_col} <= ?")
            params.append(ceil(n_winner / 2))
            params.append(floor(n_loser / 2))

    sql = f"""
        SELECT sb.branch_id,
               b.file, b.function, b.line, b.col, b.blocked_side,
               sb.n_A_resolved, sb.n_A_blocked, sb.n_A_unreached,
               sb.n_B_resolved, sb.n_B_blocked, sb.n_B_unreached,
               ROUND(sb.p_A_blocked, 3), ROUND(sb.p_B_blocked, 3), ROUND(sb.prob_div, 3),
               ROUND(sb.avg_dur_A, 2),   ROUND(sb.avg_dur_B,   2), ROUND(sb.dur_div,  2),
               ROUND(sb.avg_hits_A, 1),  ROUND(sb.avg_hits_B,  1), ROUND(sb.hit_div,  1),
               b.source_line
        FROM subject_branches sb
        JOIN branches b ON b.branch_id = sb.branch_id
        WHERE {' AND '.join(where)}
        ORDER BY sb.prob_div DESC, sb.dur_div DESC, sb.hit_div DESC
        LIMIT ?
    """
    params.append(args.k)
    rows = conn.execute(sql, params).fetchall()
    conn.close()

    print(f"# subject {args.subject_id}: target={target}, A={a}, B={b}, "
          f"dir={direction}, n=({n_a},{n_b}), policy={args.policy}, top={args.k}")
    cols = [
        "br_id", "file", "function", "line", "col", "side",
        "Ares", "Ablk", "Aunr",
        "Bres", "Bblk", "Bunr",
        "p_A_blk", "p_B_blk", "prob_div",
        "dur_A", "dur_B", "dur_div",
        "hit_A", "hit_B", "hit_div",
        "source",
    ]
    print("\t".join(cols))
    for r in rows:
        print("\t".join("" if v is None else str(v) for v in r))



# Evidence-prompt assembly (the `evidence-per-branch` subcommand and
# its helpers — SOURCE CONTEXT overlay, byte diff, hit-count and
# branch-divergence sections, etc.) lives in tools/evidence_prompt.py.
# Its CLI is wired into main() below via evidence_prompt.register_subparser.


# ── main ────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--db", default=str(DEFAULT_DB))
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="create the two tables (idempotent)")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("add", help="register/refresh ONE subject")
    s.add_argument("--target", required=True)
    s.add_argument("--A", required=True)
    s.add_argument("--B", required=True)
    s.add_argument("--delta-technique",
                   help="override (auto-inferred for canonical pairs)")
    s.add_argument("--ts-base", default=str(DEFAULT_TS_BASE))
    s.add_argument("--alpha", type=float, default=0.05)
    s.set_defaults(func=cmd_add)

    s = sub.add_parser("add-canonical",
                       help="add all 4 canonical pairs for the listed targets")
    s.add_argument("--targets", nargs="+",
                   help=f"default: {' '.join(CANONICAL_TARGETS)}")
    s.add_argument("--ts-base", default=str(DEFAULT_TS_BASE))
    s.add_argument("--alpha", type=float, default=0.05)
    s.set_defaults(func=cmd_add_canonical)

    s = sub.add_parser("list", help="list registered subjects")
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("top", help="rank candidate branches for one subject")
    s.add_argument("--subject-id", required=True, type=int)
    s.add_argument("--k", type=int, default=20)
    s.add_argument("--policy", choices=["strict", "majority", "all"],
                   default="strict")
    s.set_defaults(func=cmd_top)

    # evidence-per-branch lives in evidence_prompt.py to keep this file
    # focused on schema/population concerns; the subparser is installed
    # via the registration hook so the CLI surface stays identical.
    import evidence_prompt
    evidence_prompt.register_subparser(sub)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
