#!/usr/bin/env python3
"""
check_synergy_clusters.py — deterministic validator for the synergy Pass-B output.

Synergy is a COMPOSITE family: under the analysis-only contract each synergy
branch is split into two hypotheses (an I2S view `_h0` and a VP view `_h1`) that
describe ONE joint-necessity mechanism. The Pass-B classifier (an agent) is told
to keep a branch's two halves together and to cluster by the joint mechanism, but
that is a semantic instruction the agent could violate. This checker enforces the
structural invariants deterministically — the `check_*.py` half of the
"agent does semantics, a tool enforces invariants" split used elsewhere
(check_analysis.py, check_template.py).

Invariants enforced against step5a/synergy/{clusters.json, ..}, with the
authoritative member set taken from step5a/synergy.cards.json:

  1. coverage      — every card id appears in exactly one cluster (no drop, no dup)
  2. co-cluster    — for every branch, ALL its hypotheses (_h0/_h1/...) sit in the
                     SAME cluster (the load-bearing synergy invariant)
  3. schema        — each cluster has feature_id, mechanism_family=="synergy",
                     mechanism_label, definition, n_members==len(members);
                     each member has id/target/branch_id/analysis_path
  4. named (warn)  — feature_id is descriptive, not the boilerplate
                     "i2s_vp_joint_necessity_<target>" placeholder

Exit 0 = all invariants hold; 1 = a hard invariant failed; 2 = inputs missing.

  python3 tools/check_synergy_clusters.py
  python3 tools/check_synergy_clusters.py --family synergy   # any composite family
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STEP5A = REPO_ROOT / "step5a"

REQUIRED_CLUSTER = ("feature_id", "mechanism_family", "mechanism_label",
                    "definition", "n_members", "members")
REQUIRED_MEMBER = ("id", "target", "branch_id", "analysis_path")


def branch_of(card):
    """Branch key shared by a branch's hypotheses (id minus the _h<i> suffix)."""
    return f"{card['target']}_{card['branch_id']}"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--family", default="synergy")
    a = ap.parse_args()

    cards_path = STEP5A / f"{a.family}.cards.json"
    clusters_path = STEP5A / a.family / "clusters.json"
    for p in (cards_path, clusters_path):
        if not p.is_file():
            print(f"MISSING: {p}", file=sys.stderr)
            sys.exit(2)

    cards = {c["id"]: c for c in json.loads(cards_path.read_text())}
    clusters = json.loads(clusters_path.read_text())

    errs, warns = [], []

    # which cluster each member id landed in
    home = {}
    for ci, c in enumerate(clusters):
        for k in REQUIRED_CLUSTER:
            if k not in c:
                errs.append(f"cluster[{ci}] missing key {k!r}")
        if c.get("mechanism_family") != a.family:
            errs.append(f"cluster {c.get('feature_id')!r}: mechanism_family "
                        f"{c.get('mechanism_family')!r} != {a.family!r}")
        members = c.get("members", [])
        if c.get("n_members") != len(members):
            errs.append(f"cluster {c.get('feature_id')!r}: n_members "
                        f"{c.get('n_members')} != len(members) {len(members)}")
        fid = c.get("feature_id", "")
        if fid.startswith("i2s_vp_joint_necessity"):
            warns.append(f"cluster {fid!r}: boilerplate placeholder name "
                         f"(Pass B should coin a descriptive feature_id)")
        for m in members:
            for k in REQUIRED_MEMBER:
                if k not in m:
                    errs.append(f"cluster {fid!r} member missing key {k!r}: {m}")
            mid = m.get("id")
            if mid in home:
                errs.append(f"member {mid!r} appears in >1 cluster "
                            f"({home[mid]!r} and {fid!r})")
            else:
                home[mid] = fid

    # 1. coverage
    card_ids, clustered_ids = set(cards), set(home)
    for mid in card_ids - clustered_ids:
        errs.append(f"card {mid!r} is in NO cluster")
    for mid in clustered_ids - card_ids:
        errs.append(f"clustered id {mid!r} has no matching card")

    # 2. co-cluster: every branch's hypotheses in the same cluster
    by_branch = defaultdict(set)
    for mid in clustered_ids & card_ids:
        by_branch[branch_of(cards[mid])].add(home[mid])
    for br, homes in sorted(by_branch.items()):
        if len(homes) > 1:
            errs.append(f"branch {br!r} SPLIT across clusters {sorted(homes)} "
                        f"(synergy halves must co-cluster)")

    n_branches = len(by_branch)
    print(f"synergy clusters: {len(clusters)}  members: {len(card_ids)}  "
          f"branches: {n_branches}")
    for w in warns:
        print(f"  WARN  {w}")
    if errs:
        print(f"\nFAIL ({len(errs)} error(s)):")
        for e in errs:
            print(f"  - {e}")
        sys.exit(1)
    print("OK — coverage + co-cluster + schema invariants hold")


if __name__ == "__main__":
    main()
