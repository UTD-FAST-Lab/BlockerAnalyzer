#!/usr/bin/env python3
"""token_count — exact-literal-presence evidence tool (grimoire <GAP> erasure family).

Tests gap_erases_exact_literal (grimoire_structural_LW): grimoire's
GeneralizationStage replaces a concrete gate literal (I2S/havoc planted) with a
<GAP> token, so a byte-equality gate that literal-preserving naive satisfies stays
blocked under grimoire. The signature: the literal is present in the WINNER
(naive, resolving) seeds but ERASED in the LOSER (grimoire, blocking) seeds.

Counts the exact gate literal in each arm's DB-stored seed set (resolving for the
winner, blocking for the loser) and reads bytes from the on-disk queue:
  <winner>_literal_count   mean occurrences of the literal per winner seed
  <loser>_literal_count    mean occurrences per loser seed
  literal_presence_ratio   (loser_count + eps) / (winner_count + eps)
                           (< 1 => the literal is depleted in the loser arm)

PREDICTION (G1): erasure => winner_count >= 1 AND ratio << 1 (e.g. < 0.34). A
"no erasure" alternative predicts comparable counts (ratio ~ 1). G2-clean: it reads
seed byte composition, never the resolve pattern.

data_realities: reads on-disk seed bytes, so it scores only targets whose corpus
is on this server (libpng/libxml2 live on server B). Skips when bytes unreadable.

Usage:
  python3 bench/tools/token_count.py branch --target libpng --branch-id 3892 \
      --literal 0x03 --winner-fuzzer naive --loser-fuzzer grimoire
"""
import argparse
import json
import random
import re
import sqlite3
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "db" / "blockers.sqlite"
QUEUE = ROOT / "out"
EPS = 0.5
CAP = 1 << 16   # bytes read per seed
MAXN = 300


def read_full(target, fz, trial, sid):
    p = QUEUE / target / fz / f"trial{trial}" / "queue" / sid
    try:
        return p.read_bytes()[:CAP]
    except OSError:
        return None


def seed_bytes(con, table, branch_id, fuzzer, target):
    rows = con.execute(f"select trial, seed_id from {table} where branch_id=? and fuzzer=?",
                       (branch_id, fuzzer)).fetchall()
    random.shuffle(rows)
    out = []
    for tr, sid in rows:
        b = read_full(target, fuzzer, tr, sid)
        if b is not None:
            out.append(b)
            if len(out) >= MAXN:
                break
    return out


def parse_literal(lit):
    """'0x03' / '0x0a0b' -> bytes; a short quoted/printable string -> its bytes."""
    if not lit:
        return None
    h = re.search(r"0x([0-9A-Fa-f]{2,16})", str(lit))
    if h:
        s = h.group(1)
        if len(s) % 2:
            s = "0" + s
        return bytes.fromhex(s)
    q = re.search(r"'([^']{1,16})'", lit) or re.search(r'"([^"]{1,16})"', lit)
    if q:
        return q.group(1).encode()
    if re.fullmatch(r"[\x20-\x7e]{1,16}", str(lit)):
        return lit.encode()
    return None


def mean_count(seeds, lit):
    if not seeds:
        return None
    return statistics.mean(b.count(lit) for b in seeds)


def analyze(target, branch_id, literal, winner, loser):
    lit = parse_literal(literal)
    if lit is None:
        return {"target": target, "branch_id": branch_id, "skip": "no parseable gate literal"}
    con = sqlite3.connect(DB)
    w = seed_bytes(con, "resolving_seeds", branch_id, winner, target)
    l = seed_bytes(con, "blocking_seeds", branch_id, loser, target)
    con.close()
    wc, lc = mean_count(w, lit), mean_count(l, lit)
    if wc is None or lc is None:
        miss = winner if wc is None else loser
        return {"target": target, "branch_id": branch_id,
                "skip": f"no readable {miss} seeds (on-disk corpus required)"}
    ratio = round((lc + EPS) / (wc + EPS), 3)
    return {
        "target": target, "branch_id": branch_id,
        "literal": "0x" + lit.hex(), "winner": winner, "loser": loser,
        f"{winner}_literal_count": round(wc, 3),
        f"{loser}_literal_count": round(lc, 3),
        "winner_literal_count": round(wc, 3), "loser_literal_count": round(lc, 3),
        "literal_presence_ratio": ratio,
        "n_winner": len(w), "n_loser": len(l), "skip": None,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("branch")
    b.add_argument("--target", required=True)
    b.add_argument("--branch-id", type=int, required=True)
    b.add_argument("--literal", required=True, help="gate literal, e.g. 0x03 or 'GAP'")
    b.add_argument("--winner-fuzzer", default="naive")
    b.add_argument("--loser-fuzzer", default="grimoire")
    args = ap.parse_args()
    random.seed(11)
    print(json.dumps(analyze(args.target, args.branch_id, args.literal,
                             args.winner_fuzzer, args.loser_fuzzer), indent=1))


if __name__ == "__main__":
    main()
