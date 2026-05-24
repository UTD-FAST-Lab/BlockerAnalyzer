#!/usr/bin/env python3
"""
build_template_briefs.py — step 5b authoring briefs (one per discovered cluster).

Joins each step-5a cluster (step5a/<family>/clusters.json) with (a) its members'
distilled signatures (step5a/<family>/signatures.json) and (b) each member's full
`.analysis.json` (via `analysis_path`), into ONE self-contained brief per cluster.
The brief is the only input the `template-author` agent reads — it carries the
harness blueprint already present in each analysis (`falsifiability.
would_be_refuted_by` literally proposes a synthetic gate + knob), the gate
signatures (operand_kind / operand_width_bytes / gate_structure), and the
per-pair winner/loser/technique decomposition the harness must stratify on.

Output: step5b/briefs/<feature_id>.json (one per cluster).

The author does the semantic synthesis (one parameterized template.c + params.json
+ feature_spec.json); this driver does the deterministic prep (cluster→signature→
analysis join + involved-fuzzer derivation), mirroring build_signature_cards.py
for 5a.
"""

import argparse
import json
import re
from collections import OrderedDict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STEP5A = REPO_ROOT / "step5a"
OUT_DIR = REPO_ROOT / "step5b" / "briefs"

FAMILIES = ["I2S_pro", "I2S_anti", "VP_pro", "synergy", "independent"]

# "cmplog>naive (I2S)" -> winner, loser, technique
PAIR_RE = re.compile(r"\s*(\w+)\s*>\s*(\w+)\s*\(([^)]*)\)")

# axis partition of the canonical 4 fuzzers (see feature_spec.template.json)
AXIS_HAS = {"I2S": {"cmplog", "value_profile_cmplog"},
            "value_profile": {"value_profile", "value_profile_cmplog"}}
CANON = {"naive", "cmplog", "value_profile", "value_profile_cmplog"}


def parse_pair(s):
    m = PAIR_RE.match(s)
    if not m:
        return None
    w, l, tech = m.group(1), m.group(2), m.group(3).strip()
    axis = "I2S" if "i2s" in tech.lower() else (
        "value_profile" if ("value" in tech.lower() or "vp" in tech.lower()) else tech)
    return {"winner": w, "loser": l, "technique": tech, "axis": axis}


def analysis_excerpt(apath):
    p = REPO_ROOT / apath
    if not p.is_file():
        return {"_missing": str(apath)}
    a = json.loads(p.read_text())
    return {
        "summary_one_line": a.get("summary_one_line"),
        "pair_decision": a.get("pair_decision"),
        "hypotheses": a.get("hypotheses", []),
        "evidence_trail": [e for e in a.get("evidence_trail", [])
                           if e.get("exact_quote")],
        "falsifiability": a.get("falsifiability"),
        "weakest_evidence_point": a.get("weakest_evidence_point"),
        "confidence": a.get("confidence"),
    }


def build_brief(cluster, sigs_by_id):
    members = []
    techniques, winners, losers = set(), set(), set()
    for m in cluster["members"]:
        mid = m["id"]
        sig = sigs_by_id.get(mid, {})
        exc = analysis_excerpt(m["analysis_path"])
        pairs = []
        for h in exc.get("hypotheses", []):
            for cp in h.get("covers_pairs", []):
                pp = parse_pair(cp)
                if pp:
                    pairs.append(pp)
                    techniques.add(pp["axis"])
                    winners.add(pp["winner"])
                    losers.add(pp["loser"])
        members.append(OrderedDict([
            ("id", mid),
            ("target", m.get("target")),
            ("branch_id", m.get("branch_id")),
            ("analysis_path", m.get("analysis_path")),
            ("file", sig.get("_file")),
            ("function", sig.get("_function")),
            ("line", sig.get("_line")),
            ("source_line", sig.get("_source_line")),
            ("signature", {k: sig.get(k) for k in (
                "gate_structure", "operand_kind", "operand_literal",
                "operand_width_bytes", "byte_signature", "mechanism_summary",
                "one_line") if k in sig}),
            ("decisive_pairs", pairs),
            ("analysis", exc),
        ]))

    involved = sorted((winners | losers) & CANON)
    primary_axis = (sorted(techniques)[0] if len(techniques) == 1
                    else "multi" if len(techniques) > 1 else None)
    suggested = {}
    if primary_axis in AXIS_HAS:
        suggested = {
            "axis_differ": primary_axis,
            "has_axis": sorted(set(involved) & AXIS_HAS[primary_axis]),
            "lacks_axis": sorted(set(involved) - AXIS_HAS[primary_axis]),
        }

    return OrderedDict([
        ("feature_id", cluster["feature_id"]),
        ("mechanism_family", cluster["mechanism_family"]),
        ("mechanism_label", cluster.get("mechanism_label")),
        ("definition", cluster.get("definition")),
        ("n_members", cluster.get("n_members", len(members))),
        ("involved_fuzzers", involved),
        ("techniques_seen", sorted(techniques)),
        ("suggested_axis_partition", suggested),
        ("authoring_contract", {
            "goal": "ONE parameterized template.c isolating this cluster's shared "
                    "mechanism, with exactly ONE compile-time -D knob = the "
                    "program-feature axis. params.json:parameter MUST name that "
                    "macro; scan_values sweep it; fuzzers = involved_fuzzers; "
                    "expected_direction = '<winner> > <loser>'.",
            "isolate": "No partial-match coverage edges unless the mechanism IS a "
                       "gradient (VP families). Keep the gate the only objective.",
            "verdict_metric": "crash_count at <corpus>/crashes (__builtin_trap()).",
        }),
        ("members", members),
    ])


def load_sigs(family):
    """signatures by id, augmented with locators from the family cards."""
    sig_path = STEP5A / family / "signatures.json"
    card_path = STEP5A / f"{family}.cards.json"
    out = {}
    if sig_path.is_file():
        for s in json.loads(sig_path.read_text()):
            out[s["id"]] = dict(s)
    if card_path.is_file():
        for c in json.loads(card_path.read_text()):
            d = out.setdefault(c["id"], {"id": c["id"]})
            for k in ("file", "function", "line", "source_line"):
                d["_" + k] = c.get(k)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--family", choices=FAMILIES + ["all"], default="all")
    ap.add_argument("--feature-id", default=None,
                    help="only this cluster (across families)")
    ap.add_argument("--out-dir", default=str(OUT_DIR))
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fams = FAMILIES if args.family == "all" else [args.family]

    written = []
    for fam in fams:
        cl_path = STEP5A / fam / "clusters.json"
        if not cl_path.is_file():
            print(f"  skip {fam}: no clusters.json")
            continue
        sigs = load_sigs(fam)
        for cluster in json.loads(cl_path.read_text()):
            if args.feature_id and cluster["feature_id"] != args.feature_id:
                continue
            brief = build_brief(cluster, sigs)
            fp = out_dir / f"{cluster['feature_id']}.json"
            fp.write_text(json.dumps(brief, indent=2) + "\n")
            written.append((cluster["feature_id"], fam, brief["n_members"],
                            brief["involved_fuzzers"]))

    print(f"wrote {len(written)} brief(s) to {out_dir}/")
    for fid, fam, n, inv in written:
        print(f"  {fid:<48} {fam:<11} n={n}  involved={inv}")


if __name__ == "__main__":
    main()
