#!/usr/bin/env python3
"""
study_units.py — per-subject (target, A, B) blocker tables for the
metaphorical-testing pipeline.

A subject is `(target, fuzzer A, fuzzer B)` where A and B differ in exactly
one technique (the canonical comparable-pair set). For each subject we
register significance stats (delegating to subject_significance.pair_significance)
and materialize one row per branch that was resolved by A or B in at least
one trial. Per-branch aggregates and direction-oriented divergences let us
rank candidate B-unique blockers (or A-unique, when B beats A).

Subcommands
-----------
    init           create the two tables (idempotent)
    add            register/refresh ONE subject; populate subject_branches
    add-canonical  add all 4 canonical pairs for one or more targets
    list           list registered subjects
    top            print ranked candidate branches for one subject (legacy, per-subject)
    candidates     emit the dictionary `(target, A, B, delta, direction) → branches`
                   as a flat table — the primary data structure for hypothesis-
                   generation prioritization.
    rank           per-(target, delta, direction) priority queue: branches sorted by
                   evidence count (how many edges in this delta-direction cell flag
                   them strict).
    evidence       emit the structured prompt for feature-hypothesis-generator
                   for one (target, delta, direction, branch_id) cell.

Design choices (locked 2026-05-02):
- Canonical pairs only by default — non-canonical pairs require an explicit
  --delta-technique override, since one-technique-delta is the admissibility
  cornerstone of metaphorical testing.
- prob_div / dur_div / hit_div are stored *direction-oriented*: positive
  always means "the loser is worse than the winner at this branch". Sign is
  fixed at populate time; refreshing the subject re-derives it.
- Strict policy (default) for top: winner resolved every trial, loser
  resolved zero. Majority is a knob; "all" disables filtering and surfaces
  the raw ranking.
- `branches` only contains confirmed blockers; we do not add new branches.
  Eligibility within a subject = at least one A or B trial resolved it.
"""

import argparse
import sqlite3
import sys
from datetime import datetime, timezone
from math import ceil, floor
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = REPO_ROOT / "db" / "blockers.sqlite"
DEFAULT_TS_BASE = REPO_ROOT / "out" / "coverage_ts"

CANONICAL_TARGETS = ["bloaty", "lcms", "mbedtls", "sqlite3"]
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
    p_A_blocked     REAL,    p_B_blocked REAL,    prob_div REAL,  -- direction-oriented
    avg_dur_A       REAL,    avg_dur_B   REAL,    dur_div  REAL,  -- direction-oriented
    avg_hits_A      REAL,    avg_hits_B  REAL,    hit_div  REAL,  -- direction-oriented
    hypothesis_label TEXT,   template_id TEXT,
    PRIMARY KEY (subject_id, branch_id)
);
CREATE INDEX IF NOT EXISTS idx_sb_subject ON subject_branches(subject_id);
"""


def open_db(path):
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


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


# ── DB-side aggregates ──────────────────────────────────────────────────────

# duration_h sentinel: -1.0 means 'never blocked' (unreached or resolved
# from first checkpoint) per CLAUDE.md. Treat as 0 for averaging.

AGG_SQL = """
SELECT b.branch_id,
       SUM(CASE WHEN tc.hit_status =  1 THEN 1 ELSE 0 END) AS n_resolved,
       SUM(CASE WHEN tc.hit_status =  0 THEN 1 ELSE 0 END) AS n_blocked,
       SUM(CASE WHEN tc.hit_status = -1 THEN 1 ELSE 0 END) AS n_unreached,
       SUM(CASE WHEN tc.hit_status != -1 THEN 1 ELSE 0 END) AS n_reached,
       SUM(CASE WHEN tc.hit_status != -1 AND tc.duration_h >= 0
                THEN tc.duration_h ELSE 0 END)             AS sum_dur_h,
       SUM(CASE WHEN tc.hit_status != -1 THEN tc.hitcount        ELSE 0 END) AS sum_hits,
       SUM(CASE WHEN tc.hit_status != -1 THEN tc.other_hitcount  ELSE 0 END) AS sum_other_hits,
       COUNT(tc.id) AS n_total
FROM branches b
LEFT JOIN trial_coverage tc
       ON tc.branch_id = b.branch_id AND tc.fuzzer = ?
WHERE b.target = ?
GROUP BY b.branch_id
"""


def fetch_branch_aggregates(conn, target, fuzzer):
    rows = conn.execute(AGG_SQL, (fuzzer, target)).fetchall()
    return {
        r[0]: {
            "n_resolved":  r[1] or 0,
            "n_blocked":   r[2] or 0,
            "n_unreached": r[3] or 0,
            "n_reached":   r[4] or 0,
            "sum_dur_h":   r[5] or 0.0,
            "sum_hits":    r[6] or 0,
            "sum_other":   r[7] or 0,
            "n_total":     r[8] or 0,
        }
        for r in rows
    }


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


def populate_subject_branches(conn, subject_id, target, a, b, direction):
    """Re-populate subject_branches for one subject. Returns row count."""
    conn.execute("DELETE FROM subject_branches WHERE subject_id = ?", (subject_id,))
    aggs_a = fetch_branch_aggregates(conn, target, a)
    aggs_b = fetch_branch_aggregates(conn, target, b)

    # Direction sign for div orientation. A>B → loser=B, so prob_div = p_B - p_A
    # is positive when B blocks more (= the loser is worse). B>A → flip sign.
    sign = {"A>B": +1, "B>A": -1}.get(direction, 0)

    rows = []
    for branch_id in set(aggs_a) | set(aggs_b):
        ra = aggs_a.get(branch_id, {})
        rb = aggs_b.get(branch_id, {})
        n_A_res = ra.get("n_resolved", 0); n_A_blk = ra.get("n_blocked", 0); n_A_unr = ra.get("n_unreached", 0)
        n_B_res = rb.get("n_resolved", 0); n_B_blk = rb.get("n_blocked", 0); n_B_unr = rb.get("n_unreached", 0)
        n_A_reached = ra.get("n_reached", 0); n_B_reached = rb.get("n_reached", 0)

        # Eligibility: input-dependent within (A, B) = resolved by ≥1 A-or-B trial.
        if (n_A_res + n_B_res) == 0:
            continue

        denom_a = n_A_blk + n_A_res
        denom_b = n_B_blk + n_B_res
        p_A = (n_A_blk / denom_a) if denom_a > 0 else None
        p_B = (n_B_blk / denom_b) if denom_b > 0 else None

        avg_dur_A  = (ra["sum_dur_h"] / n_A_reached) if n_A_reached > 0 else None
        avg_dur_B  = (rb["sum_dur_h"] / n_B_reached) if n_B_reached > 0 else None
        avg_hits_A = (ra["sum_hits"]  / n_A_reached) if n_A_reached > 0 else None
        avg_hits_B = (rb["sum_hits"]  / n_B_reached) if n_B_reached > 0 else None

        # Direction-oriented divergences. Loser - winner (positive ⇒ loser worse).
        # For tie (sign=0) store unsigned magnitudes so ranking still works.
        def _div(loser_val, winner_val):
            if loser_val is None and winner_val is None:
                return None
            l = loser_val or 0
            w = winner_val or 0
            return abs(l - w) if sign == 0 else (l - w) * (1 if direction == "A>B" else -1)

        # In A>B: loser=B → prob/dur use B-A; hits use A-B (winner-loser, since
        # high hits = more frequently exercised = winner advantage on the SIDE
        # of the branch we care about; for input-distance ranking, larger gap
        # in hits is informative regardless of sign).
        if sign == 1:    # A>B
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
            n_A_res, n_A_blk, n_A_unr,
            n_B_res, n_B_blk, n_B_unr,
            p_A, p_B, prob_div,
            avg_dur_A, avg_dur_B, dur_div,
            avg_hits_A, avg_hits_B, hit_div,
        ))

    conn.executemany(
        """INSERT INTO subject_branches (
               subject_id, branch_id,
               n_A_resolved, n_A_blocked, n_A_unreached,
               n_B_resolved, n_B_blocked, n_B_unreached,
               p_A_blocked, p_B_blocked, prob_div,
               avg_dur_A, avg_dur_B, dur_div,
               avg_hits_A, avg_hits_B, hit_div
           ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
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


def _add_one(conn, target, a, b, delta_tech, ts_base, alpha, mannwhitneyu):
    sys.path.insert(0, str(REPO_ROOT / "tools"))
    from subject_significance import pair_significance
    stats = pair_significance(target, a, b, delta_tech, ts_base, mannwhitneyu, alpha)
    stats["delta_technique"] = delta_tech
    sid = upsert_subject(conn, target, a, b, stats)
    direction = conn.execute(
        "SELECT direction FROM study_subjects WHERE subject_id=?", (sid,)
    ).fetchone()[0]
    n_branches = populate_subject_branches(conn, sid, target, a, b, direction)
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
    conn = open_db(args.db)
    conn.executescript(SCHEMA_SQL)
    for tgt in targets:
        for a, b, dt in CANONICAL_PAIRS:
            try:
                sid, direction, n_branches, stats = _add_one(
                    conn, tgt, a, b, dt,
                    Path(args.ts_base).resolve(), args.alpha, mannwhitneyu,
                )
                print(
                    f"  {tgt:<8} {a:<22} vs {b:<22}  Δ={dt:<14} "
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


# ── candidates: dictionary `(target, A, B, delta, direction) → branches` ──

def _direction_predicate(policy):
    """SQL fragment that classifies a (subject_branches, study_subjects) row
    into 'wins' / 'loses' / NULL based on per-branch resolution counts.

    'wins'  : A is strict per-branch winner (delta-helps)
    'loses' : A is strict per-branch loser  (delta-hurts)
    Direction here is per-edge per-branch and is INDEPENDENT of the subject's
    AUC-level direction.
    """
    if policy == "strict":
        # New strict filter (2026-05-03): loser_blocked >= 7 AND
        # winner_resolved >= 7 (= the build_candidates.py filter).
        # Catches both n=1 noise and navigation-gap pathologies.
        wins  = "(sb.n_B_blocked >= 7 AND sb.n_A_resolved >= 7)"
        loses = "(sb.n_A_blocked >= 7 AND sb.n_B_resolved >= 7)"
    elif policy == "majority":
        # winner ≥ ⌈n/2⌉, loser ≤ ⌊n/2⌋
        wins  = ("(sb.n_A_resolved >= (s.n_A + 1) / 2 "
                 "AND sb.n_B_resolved <= s.n_B / 2)")
        loses = ("(sb.n_A_resolved <= s.n_A / 2 "
                 "AND sb.n_B_resolved >= (s.n_B + 1) / 2)")
    else:  # 'all' — no filter; both wins and loses based on simple comparison
        wins  = "(sb.n_A_resolved > sb.n_B_resolved)"
        loses = "(sb.n_A_resolved < sb.n_B_resolved)"
    return wins, loses


def cmd_candidates(args):
    """Emit the (target, A, B, delta, direction) → branches dictionary as a flat table."""
    conn = open_db(args.db)
    wins_pred, loses_pred = _direction_predicate(args.policy)

    where = ["1=1"]
    params = []
    if args.targets:
        where.append("s.target IN (" + ",".join("?" * len(args.targets)) + ")")
        params.extend(args.targets)
    if args.delta:
        where.append("s.delta_technique = ?")
        params.append(args.delta)
    if args.direction:
        if args.direction == "wins":
            where.append(wins_pred)
        elif args.direction == "loses":
            where.append(loses_pred)
    else:
        where.append(f"({wins_pred} OR {loses_pred})")

    sql = f"""
        SELECT s.target, s.A, s.B, s.delta_technique AS delta,
               CASE
                 WHEN {wins_pred}  THEN 'wins'
                 WHEN {loses_pred} THEN 'loses'
               END AS direction,
               sb.subject_id, sb.branch_id,
               b.file, b.function, b.line, b.col, b.blocked_side,
               sb.n_A_resolved AS A_res, s.n_A AS n_A,
               sb.n_B_resolved AS B_res, s.n_B AS n_B,
               ROUND(sb.prob_div, 3) AS prob_div,
               ROUND(sb.dur_div, 2)  AS dur_div,
               ROUND(sb.hit_div, 1)  AS hit_div,
               b.source_line
        FROM subject_branches sb
        JOIN study_subjects s ON s.subject_id = sb.subject_id
        JOIN branches b ON b.branch_id = sb.branch_id
        WHERE {' AND '.join(where)}
        ORDER BY s.target, s.delta_technique, direction, sb.branch_id
    """
    rows = conn.execute(sql, params).fetchall()
    conn.close()

    headers = [
        "target", "A", "B", "delta", "direction",
        "subj_id", "branch_id",
        "file", "function", "line", "col", "side",
        "A_res", "n_A", "B_res", "n_B",
        "prob_div", "dur_div", "hit_div",
        "source_line",
    ]
    print("# policy=" + args.policy + ", targets=" + (",".join(args.targets) if args.targets else "all")
          + ", delta=" + (args.delta or "all") + ", direction=" + (args.direction or "all"))
    print("\t".join(headers))
    for r in rows:
        print("\t".join("" if v is None else str(v) for v in r))


# ── candidates-csv: per-edge candidate rows with cross-edge n_edges denorm ─

DEFAULT_CANDIDATES_CSV = REPO_ROOT / "out" / "blocker_candidates.csv"


def cmd_candidates_csv(args):
    """Emit a deterministic CSV that drives hypothesis-generator orchestration.

    One row per (target, A, B, delta, direction, branch_id) where the row
    classifies into 'wins' or 'loses' (`A_resolved != B_resolved`). Each row
    carries a denormalized `n_edges` column = how many distinct (A, B) edges
    within the same (target, delta, direction) show this branch with
    `|prob_div| >= --replication-threshold` (default 0.5). The threshold makes
    `n_edges` a soft cross-edge replication signal that survives n=10 strict
    flakiness — at n=3 it matches strict (prob_div=1.0); at n=10 it admits
    near-strict cases (e.g. 9/10 vs 0/10 = prob_div=0.9).
    """
    conn = open_db(args.db)
    wins_pred, loses_pred = _direction_predicate(args.policy)

    where = ["1=1"]
    params = []
    if args.targets:
        where.append("s.target IN (" + ",".join("?" * len(args.targets)) + ")")
        params.extend(args.targets)
    if args.delta:
        where.append("s.delta_technique = ?")
        params.append(args.delta)
    if args.direction:
        if args.direction == "wins":
            where.append(wins_pred)
        elif args.direction == "loses":
            where.append(loses_pred)
    else:
        where.append(f"({wins_pred} OR {loses_pred})")

    if args.admissible_only:
        where.append("s.admissible = 1")

    threshold = args.replication_threshold

    sql = f"""
        WITH classified AS (
            SELECT s.target, s.A AS fuzzer_a, s.B AS fuzzer_b,
                   s.delta_technique AS delta,
                   CASE
                     WHEN {wins_pred}  THEN 'wins'
                     WHEN {loses_pred} THEN 'loses'
                   END AS direction,
                   sb.branch_id,
                   sb.prob_div, sb.dur_div, sb.hit_div,
                   b.file, b.function, b.line, b.col, b.blocked_side AS side,
                   b.source_line
            FROM subject_branches sb
            JOIN study_subjects s ON s.subject_id = sb.subject_id
            JOIN branches b ON b.branch_id = sb.branch_id
            WHERE {' AND '.join(where)}
        )
        SELECT fuzzer_a, fuzzer_b, delta, direction, target, branch_id,
               SUM(CASE WHEN ABS(prob_div) >= {threshold} THEN 1 ELSE 0 END)
                   OVER (PARTITION BY target, delta, direction, branch_id) AS n_edges,
               ROUND(ABS(prob_div), 3) AS blocking_prob_diff,
               ROUND(ABS(dur_div),  2) AS duration_diff,
               ROUND(ABS(hit_div),  1) AS hit_diff,
               file, function, line, col, side, source_line
        FROM classified
        ORDER BY delta, direction, fuzzer_a, fuzzer_b,
                 n_edges DESC, blocking_prob_diff DESC, duration_diff DESC, hit_diff DESC,
                 target, branch_id
    """
    rows = conn.execute(sql, params).fetchall()
    conn.close()

    headers = [
        "fuzzer_a", "fuzzer_b", "delta", "direction", "target", "branch_id",
        "n_edges", "blocking_prob_diff", "duration_diff", "hit_diff",
        "file", "function", "line", "col", "side", "source_line",
    ]

    import csv
    output = args.output
    if output == "-":
        writer = csv.writer(sys.stdout)
        writer.writerow(headers)
        for r in rows:
            writer.writerow(["" if v is None else v for v in r])
    else:
        out_path = Path(output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for r in rows:
                writer.writerow(["" if v is None else v for v in r])
        print(f"wrote {len(rows)} rows to {out_path}", file=sys.stderr)


# ── rank: per-(target, delta, direction) priority queue ───────────────────

def cmd_rank(args):
    """Per-branch evidence count within one (target, delta, direction) cell.
    Branches with higher counts have stronger evidence for the technique claim."""
    conn = open_db(args.db)
    wins_pred, loses_pred = _direction_predicate(args.policy)
    pred = wins_pred if args.direction == "wins" else loses_pred

    sql = f"""
        WITH strict_edges AS (
            SELECT sb.branch_id, sb.subject_id, s.A, s.B, s.delta_technique,
                   sb.prob_div, sb.dur_div, sb.hit_div
            FROM subject_branches sb
            JOIN study_subjects s ON s.subject_id = sb.subject_id
            WHERE s.target = ? AND s.delta_technique = ? AND {pred}
        ),
        agg AS (
            SELECT branch_id,
                   COUNT(*) AS edge_count,
                   GROUP_CONCAT(subject_id || '(' || A || '>' || B || ')', ', ') AS edges,
                   AVG(prob_div) AS avg_prob_div,
                   AVG(dur_div)  AS avg_dur_div,
                   AVG(hit_div)  AS avg_hit_div
            FROM strict_edges
            GROUP BY branch_id
        )
        SELECT a.branch_id, a.edge_count,
               (SELECT COUNT(*) FROM study_subjects
                WHERE target=? AND delta_technique=?) AS edges_total,
               a.edges,
               b.file, b.function, b.line, b.col, b.blocked_side,
               ROUND(a.avg_prob_div, 3) AS prob_div,
               ROUND(a.avg_dur_div,  2) AS dur_div,
               ROUND(a.avg_hit_div,  1) AS hit_div,
               b.source_line
        FROM agg a
        JOIN branches b ON b.branch_id = a.branch_id
        ORDER BY a.edge_count DESC, a.avg_prob_div DESC, a.avg_dur_div DESC, a.avg_hit_div DESC
        LIMIT ?
    """
    rows = conn.execute(
        sql,
        (args.target, args.delta, args.target, args.delta, args.k),
    ).fetchall()
    conn.close()

    print(f"# rank: target={args.target} delta={args.delta} direction={args.direction} "
          f"policy={args.policy} top={args.k}")
    headers = [
        "branch_id", "n_edges", "n_total", "edges",
        "file", "function", "line", "col", "side",
        "prob_div", "dur_div", "hit_div", "source_line",
    ]
    print("\t".join(headers))
    for r in rows:
        print("\t".join("" if v is None else str(v) for v in r))


# ── evidence: emit structured prompt for feature-hypothesis-generator ─────

import subprocess
from pathlib import Path as _P

DEFAULT_QUEUE_BASE = _P("/20TB/miao/fuzz-blocker")
DEFAULT_MECHANISM_LIB = REPO_ROOT / "notes" / "fuzzer_mechanism_library.md"

CANONICAL_FUZZERS_LIST = ["naive", "cmplog", "value_profile", "value_profile_cmplog"]


def _mechanism_for(library_path, fuzzer):
    """Pull the fuzzer's section paragraph from the mechanism library.
    Section header may include a parenthetical, e.g. `## value_profile (CMP_MAP gradient feedback)`.
    """
    if not library_path.is_file():
        return f"[mechanism library not found at {library_path}]"
    text = library_path.read_text()
    import re
    pattern = re.compile(rf"^## {re.escape(fuzzer)}(?:\s|\(|$)", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return f"[no entry for '{fuzzer}' in {library_path.name}]"
    body_start = text.find("\n", match.start()) + 1
    next_section = re.search(r"^## ", text[body_start:], re.MULTILINE)
    body_end = body_start + next_section.start() if next_section else len(text)
    return text[body_start:body_end].strip()


def _read_source_window(target, container_path, line, n_lines):
    """Read ±n_lines around `line` from `container_path` inside libafl-<target>-cov."""
    lo = max(1, line - n_lines)
    hi = line + n_lines
    image = f"libafl-{target}-cov"
    try:
        proc = subprocess.run(
            ["docker", "run", "--rm", "--entrypoint", "sed",
             image, "-n", f"{lo},{hi}p", container_path],
            capture_output=True, text=True, timeout=30,
        )
        if proc.returncode != 0:
            return f"[failed to read {container_path} from {image}: {proc.stderr.strip()}]"
        return proc.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        return f"[failed to read {container_path}: {exc}]"


def _hex_dump(data, max_bytes):
    """Standard 16-byte-per-row hex+ASCII dump of the first max_bytes."""
    chunk = data[:max_bytes]
    rows = []
    for off in range(0, len(chunk), 16):
        slice_ = chunk[off:off + 16]
        hex_part = " ".join(f"{b:02x}" for b in slice_)
        hex_part = hex_part.ljust(48)
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in slice_)
        rows.append(f"  {off:04x}: {hex_part}  {ascii_part}")
    return "\n".join(rows)


def _read_seed_bytes(queue_base, target, fuzzer, trial, seed_id, max_bytes):
    """Read first max_bytes of the seed file, return (size, bytes) or (None, error_msg)."""
    p = queue_base / target / fuzzer / f"trial{trial}" / "queue" / seed_id
    try:
        size = p.stat().st_size
        with p.open("rb") as f:
            data = f.read(max_bytes)
        return size, data
    except FileNotFoundError:
        return None, f"[seed file not found: {p}]"
    except OSError as exc:
        return None, f"[error reading {p}: {exc}]"


def _format_seed_block(label, rows, queue_base, target, max_bytes):
    """Format one of the SIDE-A / SIDE-B blocks. rows: list of (fuzzer, trial, seed_id, mutation_op, discovery_time_s)."""
    if not rows:
        return f"==== {label} ====\n[no seeds available — run seed_bisect.py to populate]\n"
    out = [f"==== {label} ===="]
    for i, r in enumerate(rows, 1):
        fuzzer, trial, seed_id, mutation_op, disc_t = r
        size, data = _read_seed_bytes(queue_base, target, fuzzer, trial, seed_id, max_bytes)
        header = f"Seed {i} (size={size if size is not None else '?'} bytes, fuzzer={fuzzer}, trial={trial}"
        if disc_t is not None and disc_t != -1:
            header += f", discovered_at={disc_t}s"
        if mutation_op:
            header += f", mutation_op={mutation_op}"
        header += "):"
        out.append(header)
        if isinstance(data, bytes):
            out.append(_hex_dump(data, max_bytes))
        else:
            out.append(f"  {data}")
    return "\n".join(out) + "\n"


def cmd_evidence(args):
    """Emit the structured prompt for feature-hypothesis-generator,
    keyed by (target, delta_technique, direction, branch_id).

    Per-branch direction here is independent of the subject's AUC-level direction:
      direction='wins'  : the augmented fuzzer (A) beats the baseline (B) per-branch
                          → strict means A_resolved=n_A AND B_resolved=0
      direction='loses' : the augmented fuzzer (A) loses to the baseline (B) per-branch
                          → strict means A_resolved=0 AND B_resolved=n_B
    """
    conn = open_db(args.db)
    wins_pred, loses_pred = _direction_predicate(args.policy)
    pred = wins_pred if args.direction == "wins" else loses_pred

    # Find subjects (edges) flagging this branch in the requested (delta, direction)
    candidates = conn.execute(
        f"""SELECT s.subject_id, s.A, s.B, s.n_A, s.n_B,
                   s.delta_auc, s.p_auc, s.delta_final, s.p_final,
                   ABS(IFNULL(s.delta_auc, 0)) AS abs_dauc
            FROM study_subjects s
            JOIN subject_branches sb ON sb.subject_id = s.subject_id
            WHERE s.target = ? AND s.delta_technique = ? AND sb.branch_id = ?
              AND {pred}
            ORDER BY abs_dauc DESC, s.subject_id""",
        (args.target, args.delta, args.branch_id),
    ).fetchall()
    if not candidates:
        print(
            f"no edge in target={args.target} flagging branch {args.branch_id} "
            f"strict-{args.direction} for delta={args.delta} (policy={args.policy})",
            file=sys.stderr,
        )
        sys.exit(2)

    # Total edges available for this target × delta (for strength denominator)
    total_edges_for_delta = conn.execute(
        "SELECT COUNT(*) FROM study_subjects WHERE target = ? AND delta_technique = ?",
        (args.target, args.delta),
    ).fetchone()[0]

    # Pick the canonical edge — strongest |ΔAUC|. The agent reasons over its evidence.
    primary_subject_id, primary_A, primary_B, primary_n_A, primary_n_B, \
        primary_dauc, primary_pauc, primary_dfin, primary_pfin, _ = candidates[0]
    evidence_count = len(candidates)

    # Per-branch direction: who wins per-branch for THIS edge.
    # 'wins' direction → A is per-branch winner. 'loses' → B is per-branch winner.
    if args.direction == "wins":
        winner, loser = primary_A, primary_B
    else:
        winner, loser = primary_B, primary_A

    br = conn.execute(
        "SELECT file, function, line, col, blocked_side, source_line "
        "FROM branches WHERE branch_id=?",
        (args.branch_id,),
    ).fetchone()
    if br is None:
        print(f"no branch with id={args.branch_id}", file=sys.stderr)
        sys.exit(2)
    file_path, function, line, col, blocked_side, source_line = br

    sb = conn.execute(
        """SELECT n_A_resolved, n_A_blocked, n_A_unreached,
                  n_B_resolved, n_B_blocked, n_B_unreached,
                  avg_dur_A, avg_dur_B, avg_hits_A, avg_hits_B
           FROM subject_branches WHERE subject_id=? AND branch_id=?""",
        (primary_subject_id, args.branch_id),
    ).fetchone()
    (n_A_res, n_A_blk, n_A_unr,
     n_B_res, n_B_blk, n_B_unr,
     dur_A, dur_B, hits_A, hits_B) = sb

    # Per-branch winner's resolution counts
    if args.direction == "wins":
        win_res, win_blk, win_unr = n_A_res, n_A_blk, n_A_unr
        los_res, los_blk, los_unr = n_B_res, n_B_blk, n_B_unr
        win_dur, los_dur = dur_A, dur_B
        win_hits, los_hits = hits_A, hits_B
        n_winner, n_loser = primary_n_A, primary_n_B
    else:
        win_res, win_blk, win_unr = n_B_res, n_B_blk, n_B_unr
        los_res, los_blk, los_unr = n_A_res, n_A_blk, n_A_unr
        win_dur, los_dur = dur_B, dur_A
        win_hits, los_hits = hits_B, hits_A
        n_winner, n_loser = primary_n_B, primary_n_A

    # Side-A = side the per-branch loser takes (other branch direction)
    # Side-B = blocked side, the side per-branch winner flips to
    # `branches.blocked_side` was computed across all 4 fuzzers globally — usually
    # matches the per-branch winner's resolved-side; for direction='loses' it may
    # not, so we flag if there's a mismatch.
    side_b_label = blocked_side
    side_a_label = "F" if blocked_side == "T" else "T"
    side_a_branch = "false branch" if side_a_label == "F" else "true branch"
    side_b_branch = "false branch" if side_b_label == "F" else "true branch"

    side_b_seeds = conn.execute(
        """SELECT fuzzer, trial, seed_id, mutation_op, discovery_time_s
           FROM resolving_seeds
           WHERE branch_id=? AND fuzzer=?
           ORDER BY discovery_time_s ASC, seed_id ASC
           LIMIT ?""",
        (args.branch_id, winner, args.seeds_per_side),
    ).fetchall()
    side_a_seeds = conn.execute(
        """SELECT fuzzer, trial, seed_id, mutation_op, discovery_time_s
           FROM blocking_seeds
           WHERE branch_id=? AND fuzzer=?
           ORDER BY discovery_time_s ASC, seed_id ASC
           LIMIT ?""",
        (args.branch_id, loser, args.seeds_per_side),
    ).fetchall()

    conn.close()

    library_path = _P(args.mechanism_library)
    mech_winner = _mechanism_for(library_path, winner)
    mech_loser = _mechanism_for(library_path, loser)

    queue_base = _P(args.queue_base)
    source_window = _read_source_window(args.target, file_path, line, args.source_lines)

    out = []
    out.append("==== FUZZER PAIR ====")
    out.append(f"Fuzzer A: {primary_A}  (augmented; carries delta_{args.delta})")
    out.append(f"Fuzzer B: {primary_B}  (baseline; without delta_{args.delta})")
    out.append(f"Direction (per-branch): {args.direction}  (target {args.target}, "
               f"branch {args.branch_id}, delta {args.delta})")
    out.append(f"  → 'wins'  = augmented A beats baseline B per-branch (delta helps)")
    out.append(f"  → 'loses' = augmented A loses to baseline B per-branch (delta hurts)")
    out.append(f"Subject-level (this edge): ΔAUC={primary_dauc}  p_AUC={primary_pauc}  "
               f"ΔFinal={primary_dfin}  p_final={primary_pfin}  "
               f"n_A={primary_n_A} n_B={primary_n_B}")
    out.append("")
    out.append(f"Mechanism — {winner} (per-branch winner):")
    out.append(mech_winner)
    out.append("")
    out.append(f"Mechanism — {loser} (per-branch loser):")
    out.append(mech_loser)
    out.append("")

    out.append("==== EVIDENCE STRENGTH ====")
    out.append(
        f"This branch is strict-{args.direction} on {evidence_count} of "
        f"{total_edges_for_delta} edges labeled '{args.delta}' for target {args.target}."
    )
    if evidence_count >= 2:
        out.append(
            f"→ The {args.delta} delta-{args.direction} claim REPLICATES across multiple edges."
        )
    elif total_edges_for_delta >= 2:
        out.append(
            f"→ The {args.delta} delta-{args.direction} claim is partial: only one of "
            f"{total_edges_for_delta} edges flags this branch. Consider whether this is "
            f"context-dependent (the technique helps in one fuzzer-position but not another)."
        )
    out.append("Edges flagging this branch:")
    for sid, ca, cb, _, _, dauc, _, _, _, _ in candidates:
        out.append(f"  subject {sid}: edge ({ca} vs {cb}), ΔAUC={dauc}")
    out.append("")

    out.append("==== BLOCKER ====")
    out.append(f"Location: {file_path}:{line}:{col}")
    out.append(f"Enclosing function: {function}")
    out.append(f"Blocked side (globally): {blocked_side}")
    out.append(f"Source line: {source_line}")
    out.append("")
    out.append(f"Trial outcomes (this edge):")
    out.append(f"  winner ({winner}) resolved={win_res}/{n_winner}, "
               f"blocked={win_blk}, unreached={win_unr}")
    out.append(f"  loser  ({loser}) resolved={los_res}/{n_loser}, "
               f"blocked={los_blk}, unreached={los_unr}")
    if win_dur is not None and los_dur is not None:
        out.append(f"Avg duration blocked: winner={win_dur:.2f}h  loser={los_dur:.2f}h")
    if win_hits is not None and los_hits is not None:
        out.append(f"Avg hitcount on branch: winner={win_hits:.0f}  loser={los_hits:.0f}")
    out.append("")

    out.append("==== SOURCE CONTEXT ====")
    out.append(f"# {file_path} (lines {max(1, line-args.source_lines)}–{line+args.source_lines}, "
               f"blocker at line {line})")
    out.append(source_window)
    out.append("")

    out.append(_format_seed_block(
        f"SIDE-A SEEDS (reach blocker, take {side_a_branch})",
        side_a_seeds, queue_base, args.target, args.seed_bytes,
    ))
    out.append(_format_seed_block(
        f"SIDE-B SEEDS (reach blocker, take {side_b_branch} — produced by {winner})",
        side_b_seeds, queue_base, args.target, args.seed_bytes,
    ))

    out.append("==== TASK ====")
    if args.direction == "wins":
        task = (
            f"Produce a single program-feature hypothesis that explains why "
            f"{winner} resolves this branch while {loser} does not, attributable "
            f"to the {args.delta} technique delta. Then emit the parameterized "
            "synthetic that verifies it (templates/<feature_id>/{template.c, "
            "params.json, feature_spec.json}). Match the pilot at "
            "templates/i2s_corpus_pollution/. Reason over Side-A vs Side-B byte "
            "diffs at constraining offsets to identify the program-feature knob. "
            "Search prior templates for falsification before building. Predict "
            "the dose-response shape per scan value."
        )
    else:
        task = (
            f"Produce a single program-feature hypothesis that explains why ADDING "
            f"the {args.delta} technique HURTS performance at this branch — i.e., "
            f"why {primary_A} (augmented) loses to {primary_B} (baseline) here. "
            "Then emit the parameterized synthetic that demonstrates the limitation. "
            "Match the pilot at templates/i2s_corpus_pollution/ in shape, but the "
            "harness should produce a dose-response curve where the augmented fuzzer "
            "underperforms the baseline at the chosen scan values. Reason over "
            "Side-A vs Side-B byte diffs and the source CMP shape to identify "
            "what about this branch makes the technique counterproductive. "
            "Search prior templates for falsification before building."
        )
    out.append(task)

    text = "\n".join(out)
    if args.output == "-":
        sys.stdout.write(text)
    else:
        _P(args.output).write_text(text)
        print(f"wrote evidence prompt to {args.output} ({len(text)} chars)",
              file=sys.stderr)


def cmd_evidence_per_branch(args):
    """Per-branch structured prompt for feature-hypothesis-generator.

    Keyed on (target, branch_id). Collapses ALL canonical pairs satisfying the
    >=7/>=7 rule (winner_resolved >= --winner-threshold AND loser_blocked >=
    --loser-threshold) at this branch into a single prompt. Hypothesis and
    verification are scoped to those decisive pairs and their fuzzers. The
    other canonical fuzzers appear as REFERENCE context only.
    """
    conn = open_db(args.db)

    br = conn.execute(
        "SELECT target, file, function, line, col, blocked_side, source_line "
        "FROM branches WHERE branch_id=?",
        (args.branch_id,),
    ).fetchone()
    if br is None:
        print(f"no branch with id={args.branch_id}", file=sys.stderr)
        sys.exit(2)
    target, file_path, function, line, col, blocked_side, source_line = br
    if args.target and target != args.target:
        print(f"branch {args.branch_id} is in target={target}, not {args.target}",
              file=sys.stderr)
        sys.exit(2)

    where_extra = " AND s.admissible = 1" if args.admissible_only else ""
    decisive_rows = conn.execute(
        f"""SELECT s.subject_id, s.A, s.B, s.delta_technique, s.admissible,
                   sb.n_A_resolved, sb.n_A_blocked, sb.n_A_unreached,
                   sb.n_B_resolved, sb.n_B_blocked, sb.n_B_unreached,
                   sb.avg_dur_A, sb.avg_dur_B, sb.avg_hits_A, sb.avg_hits_B,
                   sb.prob_div, sb.dur_div, sb.hit_div,
                   s.delta_auc, s.p_auc, s.delta_final, s.p_final
            FROM subject_branches sb
            JOIN study_subjects s USING(subject_id)
            WHERE sb.branch_id = ?
              AND ((sb.n_A_resolved >= ? AND sb.n_B_blocked >= ?)
                OR (sb.n_B_resolved >= ? AND sb.n_A_blocked >= ?))
                  {where_extra}
            ORDER BY ABS(IFNULL(sb.prob_div,0)) DESC, s.subject_id""",
        (args.branch_id,
         args.winner_threshold, args.loser_threshold,
         args.winner_threshold, args.loser_threshold),
    ).fetchall()
    if not decisive_rows:
        print(
            f"no decisive canonical pair at (target={target}, branch={args.branch_id}) "
            f"under >={args.winner_threshold}/>={args.loser_threshold} rule "
            f"(admissible_only={args.admissible_only})",
            file=sys.stderr,
        )
        sys.exit(2)

    pairs = []
    for d in decisive_rows:
        (sid, A, B, delta, adm,
         A_res, A_blk, A_unr, B_res, B_blk, B_unr,
         dur_A, dur_B, hits_A, hits_B,
         prob_div, dur_div, hit_div,
         dauc, pauc, dfin, pfin) = d
        if A_res >= args.winner_threshold and B_blk >= args.loser_threshold:
            direction, winner, loser = "A>B", A, B
            w_res, w_blk, w_unr = A_res, A_blk, A_unr
            l_res, l_blk, l_unr = B_res, B_blk, B_unr
            w_dur, l_dur = dur_A, dur_B
            w_hits, l_hits = hits_A, hits_B
        else:
            direction, winner, loser = "B>A", B, A
            w_res, w_blk, w_unr = B_res, B_blk, B_unr
            l_res, l_blk, l_unr = A_res, A_blk, A_unr
            w_dur, l_dur = dur_B, dur_A
            w_hits, l_hits = hits_B, hits_A
        pairs.append({
            "subject_id": sid, "A": A, "B": B, "delta": delta, "admissible": adm,
            "direction": direction, "winner": winner, "loser": loser,
            "w_res": w_res, "w_blk": w_blk, "w_unr": w_unr,
            "l_res": l_res, "l_blk": l_blk, "l_unr": l_unr,
            "w_dur": w_dur, "l_dur": l_dur,
            "w_hits": w_hits, "l_hits": l_hits,
            "prob_div": abs(prob_div) if prob_div is not None else 0.0,
            "dur_div":  abs(dur_div)  if dur_div  is not None else 0.0,
            "hit_div":  abs(hit_div)  if hit_div  is not None else 0.0,
            "delta_auc": dauc, "p_auc": pauc,
            "delta_final": dfin, "p_final": pfin,
        })

    involved_fuzzers = sorted({fz for p in pairs for fz in (p["winner"], p["loser"])})
    reference_fuzzers = [fz for fz in CANONICAL_FUZZERS_LIST if fz not in involved_fuzzers]

    counts = {}
    for fz, R, B_, U in conn.execute(
        """SELECT fuzzer,
                  SUM(CASE WHEN hit_status= 1 THEN 1 ELSE 0 END),
                  SUM(CASE WHEN hit_status= 0 THEN 1 ELSE 0 END),
                  SUM(CASE WHEN hit_status=-1 THEN 1 ELSE 0 END)
           FROM trial_coverage WHERE branch_id=? GROUP BY fuzzer""",
        (args.branch_id,),
    ).fetchall():
        counts[fz] = (R, B_, U)

    pair_seeds = []
    for p in pairs:
        winner_seeds = conn.execute(
            """SELECT fuzzer, trial, seed_id, mutation_op, discovery_time_s
               FROM resolving_seeds
               WHERE branch_id=? AND fuzzer=?
               ORDER BY discovery_time_s ASC, seed_id ASC LIMIT ?""",
            (args.branch_id, p["winner"], args.seeds_per_side),
        ).fetchall()
        loser_seeds = conn.execute(
            """SELECT fuzzer, trial, seed_id, mutation_op, discovery_time_s
               FROM blocking_seeds
               WHERE branch_id=? AND fuzzer=?
               ORDER BY discovery_time_s ASC, seed_id ASC LIMIT ?""",
            (args.branch_id, p["loser"], args.seeds_per_side),
        ).fetchall()
        pair_seeds.append((winner_seeds, loser_seeds))

    conn.close()

    library_path = _P(args.mechanism_library)
    mechanisms = {fz: _mechanism_for(library_path, fz) for fz in involved_fuzzers}
    queue_base = _P(args.queue_base)
    source_window = _read_source_window(target, file_path, line, args.source_lines)

    side_b_label = blocked_side  # T or F (the blocked side, where winner flips to)
    side_a_label = "F" if blocked_side == "T" else "T"
    side_a_branch = "false branch" if side_a_label == "F" else "true branch"
    side_b_branch = "false branch" if side_b_label == "F" else "true branch"

    out = []
    out.append("==== BLOCKER ====")
    out.append(f"Target: {target}")
    out.append(f"Branch ID: {args.branch_id}")
    out.append(f"Location: {file_path}:{line}:{col}")
    out.append(f"Enclosing function: {function}")
    out.append(f"Source line: {source_line}")
    out.append(f"Globally blocked side: {blocked_side}  ({side_b_branch})")
    out.append("")

    out.append("==== TRIAL VECTOR (per fuzzer, n=10 trials) ====")
    out.append(f"{'fuzzer':<24} {'resolved':>9} {'blocked':>8} {'unreached':>10}  role")
    for fz in CANONICAL_FUZZERS_LIST:
        c = counts.get(fz)
        r_, b_, u_ = (c if c else ("?", "?", "?"))
        roles = []
        for p in pairs:
            if p["winner"] == fz:
                roles.append(f"winner ({p['delta']} vs {p['loser']})")
            if p["loser"] == fz:
                roles.append(f"loser ({p['delta']} vs {p['winner']})")
        role_str = "; ".join(roles) if roles else "REFERENCE"
        out.append(f"{fz:<24} {str(r_):>9} {str(b_):>8} {str(u_):>10}  {role_str}")
    out.append("")
    out.append(f"INVOLVED fuzzers (synthetic-verification scope): {involved_fuzzers}")
    out.append(f"REFERENCE fuzzers (auxiliary context only):     {reference_fuzzers}")
    out.append("")

    out.append(f"==== DECISIVE PAIRS ({len(pairs)}) ====")
    for i, p in enumerate(pairs, 1):
        adm_tag = "admissible" if p["admissible"] else "NOT admissible"
        out.append(f"--- Pair {i}: {p['winner']} > {p['loser']}  [delta: {p['delta']}] ---")
        out.append(f"  subject {p['subject_id']}  ({p['A']} vs {p['B']}, {adm_tag})")
        out.append(f"  winner: resolved={p['w_res']}/10  blocked={p['w_blk']}  unreached={p['w_unr']}")
        out.append(f"  loser:  resolved={p['l_res']}/10  blocked={p['l_blk']}  unreached={p['l_unr']}")
        if p["w_dur"] is not None and p["l_dur"] is not None:
            out.append(f"  avg duration blocked: winner={p['w_dur']:.2f}h  loser={p['l_dur']:.2f}h")
        if p["w_hits"] is not None and p["l_hits"] is not None:
            out.append(f"  avg hitcount on branch: winner={p['w_hits']:.0f}  loser={p['l_hits']:.0f}")
        out.append(f"  prob_div={p['prob_div']:.2f}  dur_div={p['dur_div']:.2f}h  hit_div={p['hit_div']:.0f}")
        out.append(f"  subject-level: delta_AUC={p['delta_auc']}  p_AUC={p['p_auc']}  "
                   f"delta_Final={p['delta_final']}  p_final={p['p_final']}")
    out.append("")

    out.append("==== SOURCE CONTEXT ====")
    out.append(f"# {file_path} (lines {max(1, line-args.source_lines)}-"
               f"{line+args.source_lines}, blocker at line {line})")
    out.append(source_window)
    out.append("")

    for i, (p, (winner_seeds, loser_seeds)) in enumerate(zip(pairs, pair_seeds), 1):
        out.append(f"==== PAIR {i} SEEDS — {p['winner']} > {p['loser']} ({p['delta']}) ====")
        out.append(_format_seed_block(
            f"Winner ({p['winner']}) — resolving seeds (take {side_b_branch})",
            winner_seeds, queue_base, target, args.seed_bytes,
        ))
        out.append(_format_seed_block(
            f"Loser ({p['loser']}) — blocking seeds (take {side_a_branch})",
            loser_seeds, queue_base, target, args.seed_bytes,
        ))

    out.append("==== MECHANISM CONTEXT (involved fuzzers only) ====")
    for fz in involved_fuzzers:
        out.append(f"--- {fz} ---")
        out.append(mechanisms.get(fz, f"[no mechanism entry for {fz}]"))
        out.append("")

    out.append("==== TASK ====")
    if len(pairs) == 1:
        p = pairs[0]
        task = (
            f"Produce ONE program-feature hypothesis explaining why {p['winner']} resolves "
            f"this branch while {p['loser']} does not, attributable to the {p['delta']} "
            f"technique delta. Reason over winner-resolving (Side-B) vs loser-blocking "
            f"(Side-A) byte diffs at constraining offsets and the source CMP shape.\n\n"
            f"Search templates/ for existing matches before building a new template; "
            f"if a template fits, output its template_id and stop. Otherwise emit "
            f"templates/<feature_id>/{{template.c, params.json, feature_spec.json}}.\n\n"
            f"VERIFICATION SCOPE: the synthetic experiment MUST run only the involved "
            f"fuzzers ({involved_fuzzers}). The reference fuzzers ({reference_fuzzers}) "
            f"are auxiliary context only and do NOT enter the verdict — feel free to "
            f"comment on whether their trial counts CORROBORATE or COMPLICATE the story, "
            f"but they are not the test."
        )
    else:
        deltas = sorted({p["delta"] for p in pairs})
        task = (
            f"This branch has {len(pairs)} decisive pairs spanning deltas: {deltas}.\n\n"
            f"STEP 1 — Decide explicitly: do these pairs collapse to ONE feature (a "
            f"single mechanism axis explains every decisive pair simultaneously), or do "
            f"they imply MULTIPLE features (independent axes, one per pair)? Justify in "
            f"feature_spec.json's hypothesis section.\n\n"
            f"STEP 2 — Produce one OR more program-feature hypotheses accordingly. For "
            f"each, reason over the per-pair byte diffs (winner-resolving Side-B vs "
            f"loser-blocking Side-A) and the source CMP shape.\n\n"
            f"STEP 3 — Search templates/ for existing matches before building. If "
            f"templates fit, output their template_ids. Otherwise emit "
            f"templates/<feature_id>/{{template.c, params.json, feature_spec.json}} per "
            f"surviving hypothesis.\n\n"
            f"VERIFICATION SCOPE: synthetic experiments MUST run only the involved "
            f"fuzzers ({involved_fuzzers}). Reference fuzzers ({reference_fuzzers}) are "
            f"auxiliary context — they may CORROBORATE the story (e.g., reference fuzzer "
            f"behaves consistently with the proposed mechanism) but do not enter the verdict."
        )
    out.append(task)

    text = "\n".join(out)
    if args.output == "-":
        sys.stdout.write(text)
    else:
        _P(args.output).write_text(text)
        print(f"wrote evidence prompt to {args.output} ({len(text)} chars)",
              file=sys.stderr)


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

    s = sub.add_parser(
        "candidates",
        help="emit dictionary `(target, A, B, delta, direction) → branches` "
             "as a flat table",
    )
    s.add_argument("--targets", nargs="+",
                   help=f"default: all (canonical: {' '.join(CANONICAL_TARGETS)})")
    s.add_argument("--delta", choices=["I2S", "value_profile"],
                   help="filter to one technique label (default: both)")
    s.add_argument("--direction", choices=["wins", "loses"],
                   help="filter to one direction (default: both)")
    s.add_argument("--policy", choices=["strict", "majority", "all"],
                   default="strict")
    s.set_defaults(func=cmd_candidates)

    s = sub.add_parser(
        "candidates-csv",
        help="emit deterministic CSV `(fuzzer_a, fuzzer_b, delta, direction, "
             "target, branch_id, n_edges, blocking_prob_diff, duration_diff, "
             "hit_diff, ...)` to drive hypothesis-generator orchestration. "
             "All diff columns are absolute magnitudes; the `direction` "
             "column tells you who wins.",
    )
    s.add_argument("--targets", nargs="+",
                   help=f"default: all (canonical: {' '.join(CANONICAL_TARGETS)})")
    s.add_argument("--delta", choices=["I2S", "value_profile"],
                   help="filter to one technique label (default: both)")
    s.add_argument("--direction", choices=["wins", "loses"],
                   help="filter to one direction (default: both)")
    s.add_argument("--policy", choices=["strict", "majority", "all"],
                   default="all",
                   help="how to classify a row into wins/loses (default 'all': "
                        "any A_res != B_res). Strict and majority filter rows; "
                        "ranking by (n_edges, blocking_prob_diff) usually does "
                        "the work without the filter.")
    s.add_argument("--admissible-only", action="store_true", default=True,
                   help="restrict to admissible subjects (default ON; "
                        "use --no-admissible-only to disable)")
    s.add_argument("--no-admissible-only", action="store_false",
                   dest="admissible_only",
                   help="include all subjects regardless of admissibility")
    s.add_argument("--replication-threshold", type=float, default=0.5,
                   help="|prob_div| >= THIS counts as 'flagged' for n_edges. "
                        "n_edges = number of same-(delta, direction) edges that "
                        "flag this branch. Default 0.5 — flexible to n=10 "
                        "near-strict cases (e.g. 9/10 vs 0/10 = 0.9).")
    s.add_argument("--output", default=str(DEFAULT_CANDIDATES_CSV),
                   help=f"output CSV path or - for stdout "
                        f"(default {DEFAULT_CANDIDATES_CSV})")
    s.set_defaults(func=cmd_candidates_csv)

    s = sub.add_parser(
        "rank",
        help="per-(target, delta, direction) priority queue: branches sorted "
             "by evidence count (how many edges flag them strict)",
    )
    s.add_argument("--target", required=True)
    s.add_argument("--delta", required=True, choices=["I2S", "value_profile"])
    s.add_argument("--direction", required=True, choices=["wins", "loses"])
    s.add_argument("--k", type=int, default=20)
    s.add_argument("--policy", choices=["strict", "majority", "all"],
                   default="strict")
    s.set_defaults(func=cmd_rank)

    s = sub.add_parser(
        "evidence",
        help="emit structured prompt for feature-hypothesis-generator "
             "for ONE (target, delta, direction, branch_id) cell",
    )
    s.add_argument("--target", required=True)
    s.add_argument("--delta", required=True, choices=["I2S", "value_profile"])
    s.add_argument("--direction", required=True, choices=["wins", "loses"])
    s.add_argument("--branch-id", required=True, type=int)
    s.add_argument("--policy", choices=["strict", "majority", "all"],
                   default="all",
                   help="how strictly to interpret 'wins'/'loses' (default 'all'; "
                        "matches candidates-csv default. Use 'strict' to require "
                        "10/10 vs 0/10 type cleanness, dropping near-strict cases.")
    s.add_argument("--mechanism-library", default=str(DEFAULT_MECHANISM_LIB),
                   help=f"default {DEFAULT_MECHANISM_LIB}")
    s.add_argument("--queue-base", default=str(DEFAULT_QUEUE_BASE),
                   help=f"default {DEFAULT_QUEUE_BASE} (where LibAFL queue dirs live)")
    s.add_argument("--source-lines", type=int, default=30,
                   help="±N lines of source context (default 30)")
    s.add_argument("--seeds-per-side", type=int, default=5,
                   help="how many Side-A and Side-B seeds to include (default 5)")
    s.add_argument("--seed-bytes", type=int, default=64,
                   help="bytes per seed in the hex dump (default 64)")
    s.add_argument("--output", default="-",
                   help="output path or - for stdout (default)")
    s.set_defaults(func=cmd_evidence)

    s = sub.add_parser(
        "evidence-per-branch",
        help="emit per-branch structured prompt for feature-hypothesis-generator: "
             "collapses ALL canonical pairs satisfying >=7/>=7 at this branch into "
             "one prompt; reports the full 4-fuzzer trial vector with role tags. "
             "Hypothesis and verification are scoped to decisive pairs only.",
    )
    s.add_argument("--target", required=True,
                   help="target name (sanity-checked against branches.target)")
    s.add_argument("--branch-id", required=True, type=int)
    s.add_argument("--winner-threshold", type=int, default=7,
                   help="winner must have n_resolved >= THIS (default 7)")
    s.add_argument("--loser-threshold", type=int, default=7,
                   help="loser must have n_blocked >= THIS (default 7)")
    s.add_argument("--admissible-only", action="store_true", default=True,
                   help="restrict to admissible subjects (default ON)")
    s.add_argument("--no-admissible-only", action="store_false",
                   dest="admissible_only",
                   help="include all subjects regardless of admissibility")
    s.add_argument("--mechanism-library", default=str(DEFAULT_MECHANISM_LIB),
                   help=f"default {DEFAULT_MECHANISM_LIB}")
    s.add_argument("--queue-base", default=str(DEFAULT_QUEUE_BASE),
                   help=f"default {DEFAULT_QUEUE_BASE}")
    s.add_argument("--source-lines", type=int, default=30)
    s.add_argument("--seeds-per-side", type=int, default=5,
                   help="winner-resolving + loser-blocking seeds per pair")
    s.add_argument("--seed-bytes", type=int, default=64)
    s.add_argument("--output", default="-",
                   help="output path or - for stdout (default)")
    s.set_defaults(func=cmd_evidence_per_branch)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
