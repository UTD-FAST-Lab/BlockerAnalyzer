#!/usr/bin/env python3
"""Leg 1 of the I2S-sign discriminator study (2026-06-12).

Tests the hypothesis (user, 2026-06-12): the program-feature that flips I2S
from helpful to harmful on a branch is whether the target gate's RESOLVING
value is a harvestable CMP operand. When it is, cmplog harvests it and splices
it in -> the corpus is ENRICHED in the target value (I2S-pro). When the target
is a rare complement and abundant DECOY operands surround the dispatch, I2S
splices the decoys -> the corpus is PINNED to the wrong arm and DEPLETED of the
target value (I2S-anti).

We measure this directly on the REAL campaign corpora (no synthesis):

  gate signature  = byte offsets where the resolving (W) seeds and blocking (L)
                    seeds systematically disagree (purity >= --purity), with the
                    W-consensus byte = TARGET pattern, L-consensus = DECOY pattern.
  target_frac_F   = fraction of fuzzer F's saved corpus whose head matches the
                    full TARGET pattern (all gate offsets).
  signed enrich   = log2(target_frac_cmplog / target_frac_naive)
                    > 0  cmplog corpus enriched in target  -> I2S-pro signature
                    < 0  cmplog corpus depleted of target  -> I2S-anti signature
  decoy enrich    = log2(decoy_frac_cmplog / decoy_frac_naive)  (anti expects >0)

Per-branch output is one row; the driver tabulates the signed-enrichment
distribution for the PRO-labeled vs ANTI-labeled branch sets.

Usage:
  python3 tools/i2s_operand_availability.py branch --target harfbuzz --branch-id 5391
  python3 tools/i2s_operand_availability.py study --label-csv csvs/i2s_pro_anti_labels.csv \
      --out csvs/i2s_operand_availability.csv [--sample 15000] [--head 48]
"""
import argparse
import collections
import glob
import json
import math
import os
import random
import sqlite3
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # bench/tools/<file> -> repo root
DB = ROOT / "db" / "blockers.sqlite"
QUEUE_BASE = ROOT / "out"
EPS = 1e-6


def read_head(target, fuzzer, trial, seed_id, n):
    p = QUEUE_BASE / target / fuzzer / f"trial{trial}" / "queue" / seed_id
    try:
        with open(p, "rb") as fh:
            return fh.read(n)
    except OSError:
        return None


def seed_rows(con, table, branch_id):
    return con.execute(
        f"select fuzzer, trial, seed_id from {table} where branch_id=?",
        (branch_id,)).fetchall()


def consensus_pattern(byte_lists, head, purity):
    """Per-offset majority byte + its purity over a list of byte strings."""
    pat = {}
    n = len(byte_lists)
    if n == 0:
        return pat
    for off in range(head):
        col = collections.Counter(b[off] for b in byte_lists if len(b) > off)
        if not col:
            continue
        val, cnt = col.most_common(1)[0]
        seen = sum(1 for b in byte_lists if len(b) > off)
        if seen and cnt / seen >= purity:
            pat[off] = (val, cnt / seen)
    return pat


MIN_SEEDS = 3  # need >=3 W and >=3 L seeds for a non-overfit consensus


def gate_signature(target, branch_id, head, purity, max_seeds=200):
    con = sqlite3.connect(DB)
    W = seed_rows(con, "resolving_seeds", branch_id)
    L = seed_rows(con, "blocking_seeds", branch_id)
    con.close()
    random.shuffle(W); random.shuffle(L)
    wb = [b for fz, tr, sid in W[:max_seeds]
          if (b := read_head(target, fz, tr, sid, head)) is not None]
    lb = [b for fz, tr, sid in L[:max_seeds]
          if (b := read_head(target, fz, tr, sid, head)) is not None]
    # require enough seeds on BOTH sides; few-seed consensus is overfit and
    # structural (different-length W vs L) gates have no fixed-offset signature.
    if len(wb) < MIN_SEEDS or len(lb) < MIN_SEEDS:
        return {}, len(wb), len(lb)
    wpat = consensus_pattern(wb, head, purity)
    lpat = consensus_pattern(lb, head, purity)
    # gate offsets = where both have a consensus AND they disagree
    gate = {off: (wpat[off][0], lpat[off][0])
            for off in wpat if off in lpat and wpat[off][0] != lpat[off][0]}
    return gate, len(wb), len(lb)


def load_corpus_sample(target, fuzzer, sample, head, trials=(1, 2, 3)):
    """Read head bytes of a fuzzer's corpus ONCE, into memory, so every branch of
    this target reuses the same sample (the corpus is shared across all branches
    of a target — re-globbing per branch was the bottleneck).

    DETERMINISTIC subsampling (was random.sample): the previous random draw made
    `signed_target_enrich` depend on the global RNG state, which differs between
    study-mode and branch-mode invocations (gate_signature shuffles the RNG first).
    For a corpus larger than `sample`, that flipped the label of branches sitting
    near a rule threshold (e.g. openthread, corpus 14k > 8k: ste -0.589 vs -0.293
    across runs). We now sort the files and take an even stride, so the subset —
    and hence every metric — is byte-stable regardless of call order or target."""
    files = []
    for tr in trials:
        files += glob.glob(str(QUEUE_BASE / target / fuzzer / f"trial{tr}" / "queue" / "*"))
    files = sorted(f for f in files if os.path.isfile(f))
    if not files:
        return None
    if len(files) > sample:
        step = len(files) / sample           # even, deterministic stride (no RNG)
        files = [files[int(i * step)] for i in range(sample)]
    heads = []
    for f in files:
        try:
            with open(f, "rb") as fh:
                heads.append(fh.read(head))
        except OSError:
            continue
    return heads


def offset_freqs_from_cache(heads, gate):
    """Per-gate-offset frequency the cached corpus byte == target / == decoy byte."""
    offs = sorted(gate)
    t_hit = {o: 0 for o in offs}
    d_hit = {o: 0 for o in offs}
    seen = {o: 0 for o in offs}
    for b in heads:
        for o in offs:
            if o < len(b):
                seen[o] += 1
                tv, dv = gate[o]
                if b[o] == tv:
                    t_hit[o] += 1
                if b[o] == dv:
                    d_hit[o] += 1
    tf = {o: (t_hit[o] / seen[o]) for o in offs if seen[o]}
    df = {o: (d_hit[o] / seen[o]) for o in offs if seen[o]}
    return {"target_freq": tf, "decoy_freq": df,
            "n": max(seen.values()) if seen else 0}


def analyze_branch(target, branch_id, sample, head, purity, cache=None,
                   winner="cmplog", loser="naive"):
    """Enrichment of the target operand in the WINNER fuzzer's corpus vs the
    LOSER's, at the branch's gate offsets. Default winner/loser = cmplog/naive
    (the canonical I2S-pro/anti contrast). For vpc-only-winner shapes (_LWL etc.)
    cmplog is non-decisive, so the canonical contrast measures the wrong arms;
    pass winner=value_profile_cmplog, loser=value_profile to isolate the I2S
    contribution over the VP-only blocker. The signed_target_enrich field is
    arm-agnostic in NAME, so the arbiter's rule keeps working unchanged."""
    gate, nw, nl = gate_signature(target, branch_id, head, purity)
    if not gate:
        return {"target": target, "branch_id": branch_id, "skip": "no_gate_signature",
                "n_w_seeds": nw, "n_l_seeds": nl,
                "winner_fuzzer": winner, "loser_fuzzer": loser}
    if cache is None:
        cache = {winner: load_corpus_sample(target, winner, sample, head),
                 loser: load_corpus_sample(target, loser, sample, head)}
    cm = offset_freqs_from_cache(cache[winner], gate) if cache.get(winner) else None
    nv = offset_freqs_from_cache(cache[loser], gate) if cache.get(loser) else None
    if not cm or not nv:
        return {"target": target, "branch_id": branch_id, "skip": "no_corpus",
                "gate_offsets": sorted(gate),
                "winner_fuzzer": winner, "loser_fuzzer": loser}
    # per-offset log2 enrichment of target/decoy byte in winner vs loser corpus
    offs = sorted(set(cm["target_freq"]) & set(nv["target_freq"]))
    t_enr = [math.log2((cm["target_freq"][o] + EPS) / (nv["target_freq"][o] + EPS)) for o in offs]
    d_enr = [math.log2((cm["decoy_freq"][o] + EPS) / (nv["decoy_freq"][o] + EPS)) for o in offs]
    signed = statistics.median(t_enr) if t_enr else 0.0
    decoy = statistics.median(d_enr) if d_enr else 0.0
    return {
        "target": target, "branch_id": branch_id,
        "winner_fuzzer": winner, "loser_fuzzer": loser,
        "gate_offsets": offs, "gate_width": len(offs),
        "n_w_seeds": nw, "n_l_seeds": nl,
        # column names retain cmplog_/naive_ for backward-compat (= winner_/loser_)
        "cmplog_target_frac": round(statistics.median(list(cm["target_freq"].values())) if cm["target_freq"] else 0, 5),
        "naive_target_frac": round(statistics.median(list(nv["target_freq"].values())) if nv["target_freq"] else 0, 5),
        "cmplog_decoy_frac": round(statistics.median(list(cm["decoy_freq"].values())) if cm["decoy_freq"] else 0, 5),
        "naive_decoy_frac": round(statistics.median(list(nv["decoy_freq"].values())) if nv["decoy_freq"] else 0, 5),
        "signed_target_enrich": round(signed, 3),
        "decoy_enrich": round(decoy, 3),
        "anti_score": round(decoy - signed, 3),
        "cmplog_corpus_n": cm["n"], "naive_corpus_n": nv["n"],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("branch")
    b.add_argument("--target", required=True)
    b.add_argument("--branch-id", type=int, required=True)
    b.add_argument("--sample", type=int, default=15000)
    b.add_argument("--head", type=int, default=48)
    b.add_argument("--purity", type=float, default=0.6)
    b.add_argument("--winner-fuzzer", default="cmplog",
                   help="corpus enriched in the operand (default cmplog; "
                        "use value_profile_cmplog for vpc-only-winner shapes)")
    b.add_argument("--loser-fuzzer", default="naive",
                   help="contrast corpus lacking the winner's I2S advantage "
                        "(default naive; use value_profile to isolate I2S in vpc shapes)")

    s = sub.add_parser("study")
    s.add_argument("--label-csv", required=True,
                   help="CSV columns: label,target,branch_id [,winner,loser]. "
                        "Optional per-row winner/loser override the cmplog/naive default.")
    s.add_argument("--out", required=True)
    s.add_argument("--sample", type=int, default=15000)
    s.add_argument("--head", type=int, default=48)
    s.add_argument("--purity", type=float, default=0.6)
    args = ap.parse_args()
    random.seed(7)

    if args.cmd == "branch":
        print(json.dumps(analyze_branch(args.target, args.branch_id,
                                        args.sample, args.head, args.purity,
                                        winner=args.winner_fuzzer,
                                        loser=args.loser_fuzzer), indent=1))
        return

    import csv
    by_target = collections.OrderedDict()
    with open(args.label_csv) as fh:
        for r in csv.DictReader(fh):
            t = r["target"].strip()
            # per-row arm override (default to the canonical cmplog/naive contrast)
            winner = (r.get("winner") or "").strip() or "cmplog"
            loser = (r.get("loser") or "").strip() or "naive"
            by_target.setdefault(t, []).append(
                (r["label"].strip(), int(r["branch_id"]), winner, loser))

    rows = []
    for target, items in by_target.items():
        # load each distinct fuzzer corpus sample for this target ONCE (the corpus
        # is shared across branches); arms vary per row (cmplog/naive vs vpc/vp).
        needed = sorted({a for _, _, w, l in items for a in (w, l)})
        print(f"== loading {target} corpus samples ({','.join(needed)}) ...", flush=True)
        cache = {fz: load_corpus_sample(target, fz, args.sample, args.head) for fz in needed}
        print("   " + " ".join(f"{fz}={len(cache[fz] or [])}" for fz in needed)
              + " heads cached", flush=True)
        for label, bid, winner, loser in items:
            res = analyze_branch(target, bid, args.sample, args.head, args.purity,
                                 cache=cache, winner=winner, loser=loser)
            res["label"] = label
            rows.append(res)
            tag = res.get("skip") or f"signed={res.get('signed_target_enrich')}"
            print(f"  [{label:4s}] {target}/{bid} ({winner}/{loser}): {tag}", flush=True)

    keys = ["label", "target", "branch_id", "winner_fuzzer", "loser_fuzzer",
            "signed_target_enrich", "decoy_enrich", "anti_score",
            "cmplog_target_frac", "naive_target_frac", "cmplog_decoy_frac",
            "naive_decoy_frac", "gate_width", "gate_offsets", "n_w_seeds", "n_l_seeds",
            "cmplog_corpus_n", "naive_corpus_n", "skip"]
    with open(args.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            r = dict(r)
            if isinstance(r.get("gate_offsets"), list):
                r["gate_offsets"] = " ".join(map(str, r["gate_offsets"]))
            w.writerow(r)

    # summary: signed-enrichment distribution per label
    print("\n=== signed_target_enrich by label (negative = I2S depletes target = anti signature) ===")
    for lab in ("pro", "anti"):
        vals = [r["signed_target_enrich"] for r in rows
                if r.get("label") == lab and "signed_target_enrich" in r]
        if vals:
            neg = sum(1 for v in vals if v < 0)
            print(f"  {lab:4s} n={len(vals):3d}  median={statistics.median(vals):+.2f}  "
                  f"mean={statistics.mean(vals):+.2f}  frac_negative={neg/len(vals):.2f}")
        skipped = sum(1 for r in rows if r.get("label") == lab and r.get("skip"))
        print(f"       ({skipped} skipped: no gate signature / no corpus)")
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
