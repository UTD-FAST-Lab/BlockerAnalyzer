#!/usr/bin/env python3
"""corpus_size_ratio — corpus-scale evidence tool (homogenization / inflation family).

Tests the NON-LOCAL "the technique-arm hoards / homogenizes its saved corpus"
mechanisms that no per-branch byte tool can see:
  - ctx_corpus_inflation (ctx_coverage_LW): naive_ctx hoards far more context-
    redundant entries than naive  -> corpus_count_ratio >= 1.5
  - i2s_homogenizes_corpus (i2s_vp_LWLW): the I2S arm inflates AND collapses its
    byte composition -> corpus_size_ratio >= 1.3 AND composition_entropy_ratio < 0.85
  - i2s_corpus_channeling (i2s_vp_L__W): size_ratio_cmp_over_naive >= 1.5 AND a
    target-reach drop (the reach half is NOT measured here — needs depth_reach /
    Docker — so a channeling rule that also asks for target_reach stays unscorable).

It is a WHOLE-CORPUS comparison of two fuzzer arms, so it is branch-independent
(the same target+arm-pair gives the same numbers for every branch of that pair);
--branch-id is accepted for the uniform arbiter CLI but only the arms matter.

  winner = the arm hypothesized to inflate/homogenize (e.g. cmplog, naive_ctx)
  loser  = the flat baseline                          (e.g. naive)

Metrics (per-trial median, winner/loser):
  corpus_count_ratio          median(#saved seeds winner) / median(#saved seeds loser)
  corpus_size_ratio           alias of corpus_count_ratio ("saved-corpus size" = entries)
  size_ratio_cmp_over_naive   alias (the i2s_vp_L__W rule's name)
  composition_entropy_ratio   byte-value Shannon entropy(winner sample) / (loser sample)
                              (<1 => winner corpus homogenized onto few byte patterns)

PREDICTION (G1): inflation => ratio >> 1; homogenization => entropy ratio < 1.
A "no corpus effect" alternative predicts ratio ~ 1 and entropy ratio ~ 1. G2-clean:
it reads only saved-corpus composition, never the resolve pattern.

data_realities: on-disk corpora exist ONLY for curl/harfbuzz/openthread/sqlite3 on
s4 (the rest on server B). Both arms must have an on-disk queue or the tool skips.

Usage:
  python3 bench/tools/corpus_size_ratio.py branch --target harfbuzz --branch-id 5391 \
      --winner-fuzzer cmplog --loser-fuzzer naive
  python3 bench/tools/corpus_size_ratio.py study --pairs-csv <csv> --out <csv>
      # csv cols: target,winner,loser   (one corpus-pair per row)
"""
import argparse
import json
import math
import os
import random
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "out"
TRIALS = (1, 2, 3)
ENTROPY_SAMPLE = 300      # seeds sampled per arm for the byte-entropy estimate
ENTROPY_CAP = 4096        # bytes read per sampled seed


def trial_counts(target, fuzzer):
    """Per-trial count of saved seeds in each on-disk queue (fast scandir)."""
    counts = []
    for tr in TRIALS:
        d = QUEUE / target / fuzzer / f"trial{tr}" / "queue"
        if not d.is_dir():
            continue
        n = 0
        with os.scandir(d) as it:
            for e in it:
                if e.is_file():
                    n += 1
        if n > 0:
            counts.append(n)
    return counts


def byte_entropy(target, fuzzer, sample=ENTROPY_SAMPLE):
    """Shannon entropy (bits) of the pooled byte-value histogram of a random
    seed sample across the arm's trials. None if no readable seeds."""
    files = []
    for tr in TRIALS:
        d = QUEUE / target / fuzzer / f"trial{tr}" / "queue"
        if not d.is_dir():
            continue
        with os.scandir(d) as it:
            for e in it:
                if e.is_file():
                    files.append(e.path)
    if not files:
        return None
    random.shuffle(files)
    hist = [0] * 256
    total = 0
    read = 0
    for p in files:
        if read >= sample:
            break
        try:
            b = open(p, "rb").read(ENTROPY_CAP)
        except OSError:
            continue
        if not b:
            continue
        read += 1
        for x in b:
            hist[x] += 1
        total += len(b)
    if total == 0:
        return None
    h = 0.0
    for c in hist:
        if c:
            pp = c / total
            h -= pp * math.log2(pp)
    return h


def analyze(target, winner, loser):
    wc = trial_counts(target, winner)
    lc = trial_counts(target, loser)
    if not wc or not lc:
        miss = winner if not wc else loser
        return {"target": target, "winner": winner, "loser": loser,
                "skip": f"no on-disk corpus for {miss}"}
    wmed, lmed = statistics.median(wc), statistics.median(lc)
    ratio = round(wmed / lmed, 3) if lmed else None
    we, le = byte_entropy(target, winner), byte_entropy(target, loser)
    if we is None or le is None:
        ent_ratio = None
    elif le == 0:                       # loser maximally homogenized (single byte value)
        ent_ratio = 1.0 if we == 0 else 99.0   # winner not-more-homogenized -> rule (<0.85) False
    else:
        ent_ratio = round(we / le, 3)
    return {
        "target": target, "winner": winner, "loser": loser,
        "corpus_count_ratio": ratio,
        "corpus_size_ratio": ratio,
        "size_ratio_cmp_over_naive": ratio,
        "composition_entropy_ratio": ent_ratio,
        "winner_corpus_count": int(wmed), "loser_corpus_count": int(lmed),
        "winner_entropy": round(we, 3) if we is not None else None,
        "loser_entropy": round(le, 3) if le is not None else None,
        "n_trials_winner": len(wc), "n_trials_loser": len(lc),
        "skip": None,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("branch")
    b.add_argument("--target", required=True)
    b.add_argument("--branch-id", type=int, required=True)  # accepted, branch-independent
    b.add_argument("--winner-fuzzer", required=True)
    b.add_argument("--loser-fuzzer", required=True)
    s = sub.add_parser("study")
    s.add_argument("--pairs-csv", required=True, help="cols: target,winner,loser")
    s.add_argument("--out", required=True)
    args = ap.parse_args()
    random.seed(11)

    if args.cmd == "branch":
        print(json.dumps(analyze(args.target, args.winner_fuzzer, args.loser_fuzzer), indent=1))
        return

    import csv
    rows = []
    with open(args.pairs_csv) as fh:
        for r in csv.DictReader(fh):
            res = analyze(r["target"].strip(), r["winner"].strip(), r["loser"].strip())
            rows.append(res)
            tag = res.get("skip") or (f"count_ratio={res['corpus_count_ratio']} "
                                      f"entropy_ratio={res['composition_entropy_ratio']}")
            print(f"  {res['target']} {res['winner']}/{res['loser']}: {tag}", flush=True)
    keys = ["target", "winner", "loser", "corpus_count_ratio", "composition_entropy_ratio",
            "winner_corpus_count", "loser_corpus_count", "winner_entropy", "loser_entropy", "skip"]
    with open(args.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {args.out}: {len(rows)} pairs")


if __name__ == "__main__":
    main()
