#!/usr/bin/env python3
"""N1 — joint-necessity evidence tool (vpc-needs-both family). 2026-06-12.

Tests whether a branch the SHAPE marks as `joint` (only value_profile_cmplog
resolves; cmplog, value_profile, naive all block) is genuinely explained by
JOINT NECESSITY of I2S + the CMP_MAP gradient — as opposed to vpc resolving for
some single reason.

Why not lineage: I2S is NOT tagged in `mutation_op` (verified 2026-06-12 — the
havoc mutator vocabulary is identical across all 4 fuzzers), so "the resolving
seed shows an I2S event" is unmeasurable.

Why not byte-complementarity: the joint branches are STRUCTURAL-ASSEMBLY gates
(deep table parsing), so the winning seeds are different-SIZED structural inputs
(404-805 B) than the singles' truncated blocking seeds (13-260 B) — not byte-
alignable (verified on harfbuzz/6814).

The buildable signal is a STRUCTURAL capability decomposition over the blocking
seeds each single LEFT BEHIND — independent of the resolve pattern that defined
the shape (guardrail G2):

  W      = value_profile_cmplog RESOLVING seeds (the joint solution)
  L_cmp  = cmplog BLOCKING seeds         (I2S got partway, stalled)
  L_vp   = value_profile BLOCKING seeds  (the gradient got partway, stalled)

Two structural quantities per seed set:
  tags  = count of exact structural tokens placed (I2S's job; --tokens, e.g. the
          sfnt/OT table tags for fonts). value_profile cannot place these.
  size  = input length (assembly extent; the gradient's job is to grow/assemble).

JOINT-NECESSITY signature (each technique supplies a part the other can't):
  i2s_necessary      = cmp_tags > --tau-tag  AND  vp_tags < --tau-tag
                       (I2S places tokens; the gradient alone places ~none)
  assembly_necessary = vpc_size >= cmp_size * (1 + --tau-size)
                       (the gradient assembles structure BEYOND what I2S-only reaches)
  joint_confirmed    = i2s_necessary AND assembly_necessary

PREDICTION (G1, discriminating): a genuine joint branch shows vp can't place the
tokens (vp_tags ~ 0) AND I2S-only assembly stalls short of the winner
(cmp_size << vpc_size). ALTERNATIVES the test catches: if vp_tags is high too,
tokens are not I2S-exclusive (not joint on the I2S axis); if vpc_size ~ cmp_size,
I2S-only already assembled enough (it's really i2s-pro, mis-shaped).

`--tokens` is target-specific (the design agent supplies it per shape — font
table tags here, SQL keywords for sqlite3, ...); default = sfnt/OT tags.

Usage:
  python3 bench/tools/joint_necessity.py branch --target harfbuzz --branch-id 6814
  python3 bench/tools/joint_necessity.py study --branches-csv <csv> --out <csv>
"""
import argparse
import collections
import json
import random
import sqlite3
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "db" / "blockers.sqlite"
QUEUE = ROOT / "out"

WIN_FUZZER = "value_profile_cmplog"
CMP_FUZZER = "cmplog"
VP_FUZZER = "value_profile"


# default structural tokens = sfnt/OpenType table tags (font targets)
DEFAULT_TOKENS = [b"COLR", b"CPAL", b"GPOS", b"GSUB", b"GDEF", b"glyf", b"head",
                  b"hhea", b"hmtx", b"maxp", b"name", b"post", b"cmap", b"OS/2",
                  b"loca", b"CFF ", b"sbix", b"kern", b"morx", b"feat", b"fvar",
                  b"avar", b"STAT", b"BASE", b"MATH", b"vhea", b"vmtx"]


def read_full(target, fz, trial, sid, cap):
    p = QUEUE / target / fz / f"trial{trial}" / "queue" / sid
    try:
        return p.read_bytes()[:cap]
    except OSError:
        return None


def seed_bytes(con, table, branch_id, fuzzer, target, cap, maxn=300):
    rows = con.execute(
        f"select trial, seed_id from {table} where branch_id=? and fuzzer=?",
        (branch_id, fuzzer)).fetchall()
    random.shuffle(rows)
    out = []
    for tr, sid in rows:  # read until maxn SUCCESSFUL reads (stale files don't shrink the sample)
        b = read_full(target, fuzzer, tr, sid, cap)
        if b is not None:
            out.append(b)
            if len(out) >= maxn:
                break
    return out


def struct_stats(seeds, tokens):
    if not seeds:
        return None
    size = statistics.median(len(b) for b in seeds)
    tags = statistics.mean(sum(1 for t in tokens if t in b) for b in seeds)
    return {"n": len(seeds), "size": size, "tags": round(tags, 2)}


def analyze(target, branch_id, tokens, tau_tag, tau_size, cap=4096):
    con = sqlite3.connect(DB)
    W = seed_bytes(con, "resolving_seeds", branch_id, WIN_FUZZER, target, cap)
    Lc = seed_bytes(con, "blocking_seeds", branch_id, CMP_FUZZER, target, cap)
    Lv = seed_bytes(con, "blocking_seeds", branch_id, VP_FUZZER, target, cap)
    con.close()
    if len(W) < 1 or len(Lc) < 3 or len(Lv) < 3:
        return {"target": target, "branch_id": branch_id,
                "skip": f"insufficient seeds (W={len(W)} Lc={len(Lc)} Lv={len(Lv)})"}
    w, cs, vs = (struct_stats(W, tokens), struct_stats(Lc, tokens),
                 struct_stats(Lv, tokens))
    i2s_necessary = (cs["tags"] > tau_tag) and (vs["tags"] < tau_tag)
    # guard: if cmplog's blocking seeds are degenerate (size 0), the ratio test is
    # vacuous (w_size >= 0 is always true) -> don't claim assembly necessity.
    assembly_necessary = cs["size"] > 0 and w["size"] >= cs["size"] * (1 + tau_size)
    if i2s_necessary and assembly_necessary:
        verdict = "joint_confirmed"                       # assembly-depth subtype
    elif not i2s_necessary and vs["tags"] >= tau_tag:
        verdict = "tokens_not_i2s_exclusive (vp places them too -> not joint on I2S axis)"
    elif i2s_necessary and not assembly_necessary:
        # I2S IS necessary (vp can't place tokens) but vpc is not bigger than
        # cmplog -> the gradient's contribution is a precise VALUE, not assembly
        # depth, which this structural proxy cannot see. A candidate second
        # subtype, NOT i2s-pro (cmplog still blocks).
        verdict = "i2s_necessary_value_subtype (needs value-level test)"
    elif cs["tags"] <= tau_tag:
        verdict = "no_tokens (structural-token proxy doesn't fire here)"
    else:
        verdict = "inconclusive"
    return {
        "target": target, "branch_id": branch_id, "verdict": verdict,
        "i2s_necessary": i2s_necessary, "assembly_necessary": assembly_necessary,
        "vpc_size": w["size"], "cmp_size": cs["size"], "vp_size": vs["size"],
        "vpc_tags": w["tags"], "cmp_tags": cs["tags"], "vp_tags": vs["tags"],
        "size_lift": round(w["size"] / cs["size"], 2) if cs["size"] else None,
        "tag_lift": round(cs["tags"] - vs["tags"], 2),
        "n_W": w["n"], "n_Lc": cs["n"], "n_Lv": vs["n"],
    }


def _armtag(fz):
    return {"value_profile_cmplog": "vpc", "cmplog": "cmp", "value_profile": "vp"}.get(fz, fz)


def analyze_pair(target, branch_id, winner_fz, loser_fz, tokens, tau_tag, tau_size, cap=4096):
    """Generic 2-arm structural comparison (grimoire/mopt/calibrated vs naive, etc.):
    does the WINNER arm's resolving seeds carry more structural tokens / larger
    structure than the LOSER arm's blocking seeds? Reuses the same struct_stats;
    emits canonical winner_/loser_/tag_lift/size_lift plus armtag-prefixed aliases
    (e.g. grimoire_tags, naive_tags, grimoire_tokens) so the agents' rule names match."""
    if winner_fz == loser_fz:
        return {"target": target, "branch_id": branch_id,
                "skip": "winner and loser fuzzer are the same arm"}
    con = sqlite3.connect(DB)
    W = seed_bytes(con, "resolving_seeds", branch_id, winner_fz, target, cap)
    L = seed_bytes(con, "blocking_seeds", branch_id, loser_fz, target, cap)
    con.close()
    if len(W) < 1 or len(L) < 3:
        return {"target": target, "branch_id": branch_id,
                "skip": f"insufficient seeds (W={len(W)} L={len(L)})"}
    w, lo = struct_stats(W, tokens), struct_stats(L, tokens)
    tag_lift = round(w["tags"] - lo["tags"], 2)
    size_lift = round(w["size"] / lo["size"], 2) if lo["size"] else None
    wt, lt = _armtag(winner_fz), _armtag(loser_fz)
    # token DENSITY = structural tokens per byte (a token-RICH small seed vs a
    # token-sparse large one). Distinct from size_lift (raw extent) and tag_lift
    # (raw count): VP can admit small syntactically-dense seeds while naive bloats
    # the corpus with large token-sparse garbage.
    wd = round(w["tags"] / w["size"], 5) if w["size"] else 0.0
    ld = round(lo["tags"] / lo["size"], 5) if lo["size"] else 0.0
    out = {"target": target, "branch_id": branch_id,
           "winner_tags": w["tags"], "loser_tags": lo["tags"],
           "winner_size": w["size"], "loser_size": lo["size"],
           "tag_lift": tag_lift, "token_lift": tag_lift,
           "size_lift": size_lift, "n_W": w["n"], "n_L": lo["n"],
           "winner_token_density": wd, "loser_token_density": ld,
           "token_density_lift": round(wd / ld, 2) if ld else None}
    for tag, st, dens in ((wt, w, wd), (lt, lo, ld)):
        out[f"{tag}_tags"] = st["tags"]
        out[f"{tag}_tokens"] = st["tags"]
        out[f"{tag}_size"] = st["size"]
        out[f"{tag}_token_density"] = dens
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("branch", "study"):
        p = sub.add_parser(name)
        p.add_argument("--tokens", default=None,
                       help="comma-separated structural tokens (default sfnt/OT tags)")
        p.add_argument("--tau-tag", type=float, default=0.3,
                       help="min mean tags for I2S-present")
        p.add_argument("--tau-size", type=float, default=0.3,
                       help="min vpc/cmplog size lift for assembly-necessary")
        p.add_argument("--winner-fuzzer", default=None,
                       help="2-arm pair mode: the resolving arm (e.g. grimoire)")
        p.add_argument("--loser-fuzzer", default=None,
                       help="2-arm pair mode: the blocking arm (e.g. naive)")
        if name == "branch":
            p.add_argument("--target", required=True)
            p.add_argument("--branch-id", type=int, required=True)
        else:
            p.add_argument("--branches-csv", required=True,
                           help="CSV with columns target,branch_id")
            p.add_argument("--out", required=True)
    args = ap.parse_args()
    random.seed(11)
    tokens = ([t.encode() for t in args.tokens.split(",")] if args.tokens
              else DEFAULT_TOKENS)

    if args.cmd == "branch":
        if args.winner_fuzzer and args.loser_fuzzer:
            res = analyze_pair(args.target, args.branch_id, args.winner_fuzzer,
                               args.loser_fuzzer, tokens, args.tau_tag, args.tau_size)
        else:
            res = analyze(args.target, args.branch_id, tokens, args.tau_tag, args.tau_size)
        print(json.dumps(res, indent=1))
        return

    if args.winner_fuzzer or args.loser_fuzzer:
        sys.exit("pair mode (--winner-fuzzer/--loser-fuzzer) is branch-only; "
                 "study mode runs the 3-arm joint analysis")
    import csv
    rows = []
    with open(args.branches_csv) as fh:
        for r in csv.DictReader(fh):
            res = analyze(r["target"].strip(), int(r["branch_id"]),
                          tokens, args.tau_tag, args.tau_size)
            rows.append(res)
            tag = res.get("skip") or (f"{res['verdict']} "
                  f"(vpc {res['vpc_size']}B/{res['vpc_tags']}t  cmp {res['cmp_size']}B/{res['cmp_tags']}t  vp {res['vp_size']}B/{res['vp_tags']}t)")
            print(f"  {res['target']}/{res['branch_id']}: {tag}", flush=True)
    keys = ["target", "branch_id", "verdict", "i2s_necessary", "assembly_necessary",
            "vpc_size", "cmp_size", "vp_size", "vpc_tags", "cmp_tags", "vp_tags",
            "size_lift", "tag_lift", "n_W", "n_Lc", "n_Lv", "skip"]
    with open(args.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    conf = sum(1 for r in rows if r.get("verdict") == "joint_confirmed")
    scored = [r for r in rows if not r.get("skip")]
    print(f"\njoint_confirmed: {conf}/{len(scored)} scored ({len(rows)-len(scored)} skipped)")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
