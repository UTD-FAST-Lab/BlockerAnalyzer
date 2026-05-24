#!/usr/bin/env python3
"""
mechanism_family.py — deterministic first-pass bucketing for step 5a.

Maps a hypothesis's ``covers_pairs`` to ONE coarse mechanism family, using
nothing but the (winner, loser, delta-technique) already encoded in each
``covers_pairs`` string. No thresholds are re-applied and no prose is read —
the family is a pure function of ``covers_pairs``, so it is stable against the
one-trial >=8/8 cutoff wobble that flips the fine decisive-shape (e.g. a branch
with ``value_profile`` blocked 7/10 vs 8/10 lands in the same family either
way). The vp-block-rate / vpc-rescue nuance that the shape encodes is deferred
to the Pass-A signature, where it is a graded dimension rather than a brittle
category.

Pro vs anti falls straight out of technique membership: an edge "W>L (T)" is
``T_pro`` if the winner carries technique T (it helped), else ``T_anti`` (the
technique-having arm lost, so T hurt).

Six families + one escape hatch:
  I2S_pro     — only I2S edges, technique helped
  I2S_anti    — only I2S edges, technique hurt
  VP_pro      — only value_profile edges, technique helped
  VP_anti     — only value_profile edges, technique hurt
  synergy     — both techniques help AND every winner is value_profile_cmplog
                (neither single technique suffices; the -BBR corpus-pollution shape)
  independent — both techniques help, won by single-technique arms
                (each technique clears it alone; the BRR- shape)
  mixed       — a technique both helped and hurt at the same branch (rare;
                route to a human, do not force into a family)

Usage:
  python3 tools/mechanism_family.py            # self-test + scan pilot analyses
  python3 tools/mechanism_family.py --glob 'prompts/**/*.analysis.json'

Exit codes: 0 = self-test passed and no unexpected `mixed` in the scan;
            1 = scan found a `mixed` family (review); 2 = self-test failed.
"""

import argparse
import glob as globmod
import json
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GLOB = "prompts/**/*.analysis.json"

# What each canonical fuzzer contains. The delta technique of a canonical pair
# is exactly the one technique that differs between the two arms.
TECH = {
    "naive": frozenset(),
    "cmplog": frozenset({"I2S"}),
    "value_profile": frozenset({"VP"}),
    "value_profile_cmplog": frozenset({"I2S", "VP"}),
}

# covers_pairs spells the delta technique as one of these tokens.
TECH_ALIAS = {"I2S": "I2S", "value_profile": "VP", "VP": "VP"}


def parse_edge(s):
    """'value_profile_cmplog>value_profile (I2S)' -> ('value_profile_cmplog', 'value_profile', 'I2S')."""
    pair, sep, rest = s.partition("(")
    if not sep:
        raise ValueError(f"no technique in parens: {s!r}")
    tech_raw = rest.rstrip(") ").strip()
    if tech_raw not in TECH_ALIAS:
        raise ValueError(f"unknown technique token {tech_raw!r} in {s!r}")
    winner, sep, loser = pair.partition(">")
    if not sep:
        raise ValueError(f"no '>' in pair: {s!r}")
    winner, loser = winner.strip(), loser.strip()
    for arm in (winner, loser):
        if arm not in TECH:
            raise ValueError(f"unknown fuzzer {arm!r} in {s!r}")
    return winner, loser, TECH_ALIAS[tech_raw]


def edge_tag(winner, loser, tech):
    """tech in {'I2S','VP'}; pro if the winner carries the technique, else anti."""
    return f"{tech}_pro" if tech in TECH[winner] else f"{tech}_anti"


def coarse_family(covers_pairs):
    """covers_pairs (list of strings) -> one of the seven family labels."""
    edges = [parse_edge(e) for e in covers_pairs]
    tags = {edge_tag(*e) for e in edges}
    pro = {t[:-4] for t in tags if t.endswith("_pro")}     # subset of {"I2S","VP"}
    anti = {t[:-5] for t in tags if t.endswith("_anti")}

    if pro & anti:                       # same technique helped and hurt
        return "mixed"
    if pro == {"I2S", "VP"}:
        winners = {w for (w, _l, _t) in edges}
        return "synergy" if winners == {"value_profile_cmplog"} else "independent"
    if pro == {"I2S"}:
        return "I2S_pro"
    if pro == {"VP"}:
        return "VP_pro"
    if anti == {"I2S"}:
        return "I2S_anti"
    if anti == {"VP"}:
        return "VP_anti"
    return "mixed"


# ---- self-test --------------------------------------------------------------

_EDGE_CASES = {
    "cmplog>naive (I2S)": "I2S_pro",
    "value_profile_cmplog>value_profile (I2S)": "I2S_pro",
    "value_profile_cmplog>cmplog (value_profile)": "VP_pro",
    "value_profile>naive (value_profile)": "VP_pro",
    "naive>cmplog (I2S)": "I2S_anti",
    "value_profile>value_profile_cmplog (I2S)": "I2S_anti",
}

_FAMILY_CASES = {
    # shape -> covers_pairs -> expected family
    ("cmplog>naive (I2S)", "value_profile_cmplog>value_profile (I2S)"): "I2S_pro",        # BRBR
    ("cmplog>naive (I2S)",): "I2S_pro",                                                   # BR--
    ("value_profile_cmplog>value_profile (I2S)",): "I2S_pro",                             # --BR
    ("value_profile>naive (value_profile)",): "VP_pro",                                   # B-R-
    ("cmplog>naive (I2S)", "value_profile>naive (value_profile)"): "independent",         # BRR-
    ("value_profile_cmplog>cmplog (value_profile)",
     "value_profile_cmplog>value_profile (I2S)"): "synergy",                              # -BBR
    ("naive>cmplog (I2S)", "value_profile>value_profile_cmplog (I2S)"): "I2S_anti",       # RBRB
    # contradictory edge set -> the escape hatch fires
    ("cmplog>naive (I2S)", "value_profile>value_profile_cmplog (I2S)"): "mixed",
}


def self_test():
    for s, want in _EDGE_CASES.items():
        got = edge_tag(*parse_edge(s))
        assert got == want, f"edge {s!r}: got {got}, want {want}"
    for cps, want in _FAMILY_CASES.items():
        got = coarse_family(list(cps))
        assert got == want, f"family {cps}: got {got}, want {want}"
    print(f"self-test OK ({len(_EDGE_CASES)} edges, {len(_FAMILY_CASES)} families)")


# ---- pilot scan -------------------------------------------------------------

def scan(glob_pat):
    files = sorted(f for f in globmod.glob(str(REPO_ROOT / glob_pat), recursive=True)
                   if "/_examples/" not in f)
    dist = Counter()
    mixed = []
    rows = []
    for f in files:
        d = json.load(open(f))
        for i, h in enumerate(d.get("hypotheses", [])):
            fam = coarse_family(h.get("covers_pairs", []))
            dist[fam] += 1
            rel = Path(f).relative_to(REPO_ROOT)
            rows.append((str(rel), i, fam, h.get("covers_pairs", [])))
            if fam == "mixed":
                mixed.append((str(rel), i, h.get("covers_pairs", [])))

    print(f"\nscanned {len(files)} analyses, {sum(dist.values())} hypotheses\n")
    print("family distribution:")
    for fam, n in dist.most_common():
        print(f"  {fam:<12} {n}")
    if mixed:
        print(f"\n{len(mixed)} MIXED (review):")
        for rel, i, cps in mixed:
            print(f"  {rel} [hyp {i}]: {cps}")
    return 1 if mixed else 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--glob", default=DEFAULT_GLOB,
                    help=f"analysis glob relative to repo root (default {DEFAULT_GLOB})")
    ap.add_argument("--no-scan", action="store_true", help="self-test only")
    args = ap.parse_args()
    try:
        self_test()
    except AssertionError as e:
        print(f"SELF-TEST FAILED: {e}", file=sys.stderr)
        sys.exit(2)
    if args.no_scan:
        return
    sys.exit(scan(args.glob))


if __name__ == "__main__":
    main()
