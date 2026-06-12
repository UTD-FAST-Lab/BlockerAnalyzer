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
    """Read head bytes of a fixed random sample of fuzzer's corpus ONCE, into
    memory, so every branch of this target reuses the same sample (the corpus is
    shared across all branches of a target — re-globbing per branch was the
    bottleneck)."""
    files = []
    for tr in trials:
        files += glob.glob(str(QUEUE_BASE / target / fuzzer / f"trial{tr}" / "queue" / "*"))
    files = [f for f in files if os.path.isfile(f)]
    if not files:
        return None
    if len(files) > sample:
        files = random.sample(files, sample)
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


def analyze_branch(target, branch_id, sample, head, purity, cache=None):
    gate, nw, nl = gate_signature(target, branch_id, head, purity)
    if not gate:
        return {"target": target, "branch_id": branch_id, "skip": "no_gate_signature",
                "n_w_seeds": nw, "n_l_seeds": nl}
    if cache is None:
        cache = {"cmplog": load_corpus_sample(target, "cmplog", sample, head),
                 "naive": load_corpus_sample(target, "naive", sample, head)}
    cm = offset_freqs_from_cache(cache["cmplog"], gate) if cache.get("cmplog") else None
    nv = offset_freqs_from_cache(cache["naive"], gate) if cache.get("naive") else None
    if not cm or not nv:
        return {"target": target, "branch_id": branch_id, "skip": "no_corpus",
                "gate_offsets": sorted(gate)}
    # per-offset log2 enrichment of target/decoy byte in cmplog vs naive corpus
    offs = sorted(set(cm["target_freq"]) & set(nv["target_freq"]))
    t_enr = [math.log2((cm["target_freq"][o] + EPS) / (nv["target_freq"][o] + EPS)) for o in offs]
    d_enr = [math.log2((cm["decoy_freq"][o] + EPS) / (nv["decoy_freq"][o] + EPS)) for o in offs]
    signed = statistics.median(t_enr) if t_enr else 0.0
    decoy = statistics.median(d_enr) if d_enr else 0.0
    return {
        "target": target, "branch_id": branch_id,
        "gate_offsets": offs, "gate_width": len(offs),
        "n_w_seeds": nw, "n_l_seeds": nl,
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

    s = sub.add_parser("study")
    s.add_argument("--label-csv", required=True,
                   help="CSV with columns: label,target,branch_id (label in {pro,anti})")
    s.add_argument("--out", required=True)
    s.add_argument("--sample", type=int, default=15000)
    s.add_argument("--head", type=int, default=48)
    s.add_argument("--purity", type=float, default=0.6)
    args = ap.parse_args()
    random.seed(7)

    if args.cmd == "branch":
        print(json.dumps(analyze_branch(args.target, args.branch_id,
                                        args.sample, args.head, args.purity), indent=1))
        return

    import csv
    by_target = collections.OrderedDict()
    with open(args.label_csv) as fh:
        for r in csv.DictReader(fh):
            t = r["target"].strip()
            by_target.setdefault(t, []).append(
                (r["label"].strip(), int(r["branch_id"])))

    rows = []
    for target, items in by_target.items():
        # load this target's cmplog/naive corpus sample ONCE, reuse for all branches
        print(f"== loading {target} corpus sample (cmplog,naive) ...", flush=True)
        cache = {"cmplog": load_corpus_sample(target, "cmplog", args.sample, args.head),
                 "naive": load_corpus_sample(target, "naive", args.sample, args.head)}
        ncm = len(cache["cmplog"] or []); nnv = len(cache["naive"] or [])
        print(f"   {target}: cmplog={ncm} naive={nnv} heads cached", flush=True)
        for label, bid in items:
            res = analyze_branch(target, bid, args.sample, args.head, args.purity, cache=cache)
            res["label"] = label
            rows.append(res)
            tag = res.get("skip") or f"signed={res.get('signed_target_enrich')}"
            print(f"  [{label:4s}] {target}/{bid}: {tag}", flush=True)

    keys = ["label", "target", "branch_id", "signed_target_enrich", "decoy_enrich", "anti_score",
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
