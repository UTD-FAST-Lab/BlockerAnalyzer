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

Family = "<technique>_pro" / "<technique>_anti" for any single-technique edge
set, plus two I2S×VP-specific composites and one escape hatch:

  <T>_pro      — all edges isolate technique T and T helped (winner carries T)
  <T>_anti     — all edges isolate technique T and T hurt (winner lacks T)
                 T ∈ {I2S, VP, ctx_coverage, ngram_coverage, mopt_mutation,
                      calibrated_energy, aflfast_rarity, grimoire_structural}
  synergy      — pro = {I2S, VP} AND every winner is value_profile_cmplog
                 (neither single technique suffices; the -BBR pollution shape)
  independent  — pro = {I2S, VP} won by single-technique arms (the BRR- shape)
  mixed        — the same technique both helped and hurt, OR a cross-technique
                 mix that is not the I2S×VP composite (rare; route to a human,
                 do not force into a family)

synergy/independent are SPECIFIC to value_profile_cmplog bundling I2S+VP. The
six newer techniques each have their own isolating pair (e.g. naive_ctx/naive,
grimoire/cmplog), so they only ever produce <T>_pro / <T>_anti; a hypothesis
mixing one of them with another technique falls to `mixed`.

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
# is exactly the one technique that differs between the two arms (see
# subject_significance.CANONICAL_PAIRS); edge_tag only needs the WINNER's
# content, so a variant that bundles a 2nd technique still tags correctly as
# long as its baseline shares that 2nd technique (fast/minimizer share
# calibrated_energy; grimoire/cmplog share I2S).
TECH = {
    "naive": frozenset(),
    "cmplog": frozenset({"I2S"}),
    "value_profile": frozenset({"VP"}),
    "value_profile_cmplog": frozenset({"I2S", "VP"}),
    "naive_ctx": frozenset({"ctx_coverage"}),
    "naive_ngram4": frozenset({"ngram_coverage"}),
    "mopt": frozenset({"mopt_mutation"}),
    "minimizer": frozenset({"calibrated_energy"}),
    "fast": frozenset({"calibrated_energy", "aflfast_rarity"}),  # minimizer + AFLfast
    "grimoire": frozenset({"I2S", "grimoire_structural"}),       # cmplog + structural
}

# covers_pairs spells the delta technique as one of these tokens (value_profile
# has a short alias; the rest are identity).
TECH_ALIAS = {
    "I2S": "I2S",
    "value_profile": "VP", "VP": "VP",
    "ctx_coverage": "ctx_coverage",
    "ngram_coverage": "ngram_coverage",
    "mopt_mutation": "mopt_mutation",
    "calibrated_energy": "calibrated_energy",
    "aflfast_rarity": "aflfast_rarity",
    "grimoire_structural": "grimoire_structural",
}


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
    """pro if the winner carries the technique, else anti. Works for any
    technique token in TECH_ALIAS, not just I2S/VP."""
    return f"{tech}_pro" if tech in TECH[winner] else f"{tech}_anti"


def coarse_family(covers_pairs):
    """covers_pairs (list of strings) -> one family label.

    Single-technique edge sets map to "<technique>_pro" / "<technique>_anti".
    The pro == {I2S, VP} composite stays special (synergy vs independent, the
    only case where two techniques co-help via value_profile_cmplog). Anything
    else with >1 technique, or a technique that both helped and hurt, is
    `mixed` (route to a human).
    """
    edges = [parse_edge(e) for e in covers_pairs]
    tags = {edge_tag(*e) for e in edges}
    pro = {t[:-4] for t in tags if t.endswith("_pro")}    # strip "_pro"
    anti = {t[:-5] for t in tags if t.endswith("_anti")}  # strip "_anti"

    if pro & anti:                       # same technique helped and hurt
        return "mixed"
    if pro == {"I2S", "VP"} and not anti:   # I2S×VP composite (vpc bundling)
        winners = {w for (w, _l, _t) in edges}
        return "synergy" if winners == {"value_profile_cmplog"} else "independent"
    if len(pro) == 1 and not anti:
        return f"{next(iter(pro))}_pro"
    if len(anti) == 1 and not pro:
        return f"{next(iter(anti))}_anti"
    return "mixed"


# ---- branch-level routing (synergy recovery) --------------------------------
# coarse_family is per-edge-set; the analysis-only agents decompose a branch into
# multi_feature (one hyp per technique), so a synergy branch's I2S hyp and VP hyp
# each classify single-technique and the I2S×VP composite never appears per-hyp.
# branch_family recovers it by unioning a branch's covers_pairs BEFORE classifying;
# route_branch then makes synergy AUTHORITATIVE — a synergy branch routes ALL its
# hypotheses to `synergy`, so the composite is distilled/clustered once and the
# single-technique families (I2S_pro, VP_pro) exclude it at the source (no later
# de-dup needed). Every other branch — including `independent` (each arm resolves
# alone) and `mixed` — routes per-hypothesis exactly as coarse_family dictates.

def branch_family(hyps):
    """Branch-level composite family: classify the UNION of a branch's hypotheses'
    covers_pairs. Same label space as coarse_family; None for an empty branch.
    This is the only view in which `synergy` is visible (the per-hyp view can't
    see both techniques at once)."""
    union = [cp for h in hyps for cp in h.get("covers_pairs", [])]
    return coarse_family(union) if union else None


def route_branch(hyps):
    """Family label per hypothesis (list aligned to `hyps`), applying the synergy
    override: if the branch unions to `synergy`, every hypothesis routes to
    `synergy`; otherwise each routes to its own per-hyp coarse_family."""
    if branch_family(hyps) == "synergy":
        return ["synergy"] * len(hyps)
    return [coarse_family(h.get("covers_pairs", [])) for h in hyps]


# ---- self-test --------------------------------------------------------------

_EDGE_CASES = {
    "cmplog>naive (I2S)": "I2S_pro",
    "value_profile_cmplog>value_profile (I2S)": "I2S_pro",
    "value_profile_cmplog>cmplog (value_profile)": "VP_pro",
    "value_profile>naive (value_profile)": "VP_pro",
    "naive>cmplog (I2S)": "I2S_anti",
    "value_profile>value_profile_cmplog (I2S)": "I2S_anti",
    # 10-fuzzer techniques (pro = technique-carrying arm wins; anti = it loses)
    "naive_ctx>naive (ctx_coverage)": "ctx_coverage_pro",
    "naive>naive_ctx (ctx_coverage)": "ctx_coverage_anti",
    "naive_ngram4>naive (ngram_coverage)": "ngram_coverage_pro",
    "naive>naive_ngram4 (ngram_coverage)": "ngram_coverage_anti",
    "mopt>naive (mopt_mutation)": "mopt_mutation_pro",
    "minimizer>naive (calibrated_energy)": "calibrated_energy_pro",
    "naive>minimizer (calibrated_energy)": "calibrated_energy_anti",
    "fast>minimizer (aflfast_rarity)": "aflfast_rarity_pro",
    "minimizer>fast (aflfast_rarity)": "aflfast_rarity_anti",
    "grimoire>cmplog (grimoire_structural)": "grimoire_structural_pro",
    "cmplog>grimoire (grimoire_structural)": "grimoire_structural_anti",
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
    # 10-fuzzer single-technique families
    ("naive_ctx>naive (ctx_coverage)",): "ctx_coverage_pro",
    ("naive>naive_ctx (ctx_coverage)",): "ctx_coverage_anti",
    ("naive>naive_ngram4 (ngram_coverage)",): "ngram_coverage_anti",
    ("mopt>naive (mopt_mutation)",): "mopt_mutation_pro",
    ("minimizer>naive (calibrated_energy)",): "calibrated_energy_pro",
    ("fast>minimizer (aflfast_rarity)",): "aflfast_rarity_pro",
    ("minimizer>fast (aflfast_rarity)",): "aflfast_rarity_anti",
    ("grimoire>cmplog (grimoire_structural)",): "grimoire_structural_pro",
    # cross-technique mix that is NOT the I2S×VP composite -> mixed
    ("cmplog>naive (I2S)", "grimoire>cmplog (grimoire_structural)"): "mixed",
    ("naive_ctx>naive (ctx_coverage)", "naive>naive_ngram4 (ngram_coverage)"): "mixed",
}


def self_test():
    # Every canonical fuzzer must have a TECH entry, or parse_edge raises on it.
    from subject_significance import CANONICAL_FUZZERS
    missing = [f for f in CANONICAL_FUZZERS if f not in TECH]
    assert not missing, f"TECH missing canonical fuzzers: {missing}"
    for s, want in _EDGE_CASES.items():
        got = edge_tag(*parse_edge(s))
        assert got == want, f"edge {s!r}: got {got}, want {want}"
    for cps, want in _FAMILY_CASES.items():
        got = coarse_family(list(cps))
        assert got == want, f"family {cps}: got {got}, want {want}"
    # branch-level routing: a multi_feature synergy branch (separate I2S + VP hyp)
    # routes BOTH hyps to synergy; an independent branch routes per-hyp to the
    # single-technique families; a single-technique branch is unaffected.
    _syn = [{"covers_pairs": ["value_profile_cmplog>value_profile (I2S)"]},
            {"covers_pairs": ["value_profile_cmplog>cmplog (value_profile)"]}]
    assert branch_family(_syn) == "synergy", branch_family(_syn)
    assert route_branch(_syn) == ["synergy", "synergy"], route_branch(_syn)
    _ind = [{"covers_pairs": ["cmplog>naive (I2S)"]},
            {"covers_pairs": ["value_profile>naive (value_profile)"]}]
    assert branch_family(_ind) == "independent", branch_family(_ind)
    assert route_branch(_ind) == ["I2S_pro", "VP_pro"], route_branch(_ind)
    _solo = [{"covers_pairs": ["cmplog>naive (I2S)"]}]
    assert route_branch(_solo) == ["I2S_pro"], route_branch(_solo)
    print(f"self-test OK ({len(CANONICAL_FUZZERS)} fuzzers, "
          f"{len(_EDGE_CASES)} edges, {len(_FAMILY_CASES)} families, "
          f"+branch routing)")


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
