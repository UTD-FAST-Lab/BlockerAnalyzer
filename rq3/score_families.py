#!/usr/bin/env python3
"""rq3/score_families.py — RQ3 per-FAMILY resolve-rate (cross-engine capability profile).

Companion to tools/bench_score.py (which scores per mechanism CATEGORY). This one
aggregates to the technique-direction FAMILY level, the coarser of the two RQ3 axes.

Family identity is taken from the canonical fact table bench/roadblock_facts.csv
(family column = deciding-pair routing, authoritative for BOTH validated and
inconclusive branches). A branch counts once per family it is a member of
(dual-family branches contribute to each). The resolve signal is the same as
bench_score.py: a branch is RESOLVED by fuzzer f iff
n_resolved/(n_resolved+n_blocked) >= TAU, and MEASURED iff the fuzzer reached it.

Two tables (mirrors the paper's tab:rq3-family + tab:rq3-family-all):
  validated  — only validated members (the 8 families that carry validated categories)
  all        — every roadblock incl. inconclusive (all 15 families; the 7
               inconclusive-only families appear only here)

Usage:
  python3 rq3/score_families.py [--facts bench/roadblock_facts.csv]
      [--resolve csvs/rq3_resolve.csv] [--tau 0.8] [--out csvs/rq3_family_score.csv]
"""
import argparse, csv, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FUZZERS = ["aflplusplus", "honggfuzz", "libfuzzer", "libafl"]

# family display order: validated-bearing first (by technique), then inconclusive-only
FAM_ORDER = ["I2S-P", "I2S-A", "VP-P", "VPC-P", "CTX-P", "CTX-A",
             "GRIM-P", "NGRAM-P",
             "VPC-A", "GRIM-A", "NGRAM-A", "CALI-P", "FAST-P", "FAST-A", "MOPT-A"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--facts", default=str(ROOT / "bench/roadblock_facts.csv"))
    ap.add_argument("--resolve", default=str(ROOT / "csvs/rq3_resolve.csv"))
    ap.add_argument("--tau", type=float, default=0.8)
    ap.add_argument("--out", default=str(ROOT / "csvs/rq3_family_score.csv"))
    a = ap.parse_args()

    # (target, bid) -> {family: status_set}  (a branch may appear under several families)
    fam_members = collections.defaultdict(set)   # family -> {(target,bid)}  (any status)
    fam_members_val = collections.defaultdict(set)
    for r in csv.DictReader(open(a.facts)):
        key = (r["target"], int(r["branch_id"]))
        fam_members[r["family"]].add(key)
        if r["status"] == "validated":
            fam_members_val[r["family"]].add(key)

    # resolve verdict per (target,bid,fuzzer)
    resolved = collections.defaultdict(dict)     # fuzzer -> {(target,bid): bool}
    measured = collections.defaultdict(set)       # fuzzer -> {(target,bid)}
    for r in csv.DictReader(open(a.resolve)):
        key = (r["target"], int(r["branch_id"]))
        nr, nb = int(r["n_resolved"]), int(r["n_blocked"])
        if nr + nb == 0:
            continue                              # never reached -> unmeasured (G3)
        fz = r["fuzzer"]
        measured[fz].add(key)
        resolved[fz][key] = (nr / (nr + nb)) >= a.tau

    def rates(members):
        """family member set -> {fuzzer: (rate, n_measured)}"""
        out = {}
        for fz in FUZZERS:
            meas = members & measured[fz]
            res = sum(1 for b in meas if resolved[fz].get(b))
            out[fz] = ((res / len(meas)) if meas else None, len(meas))
        return out

    out_rows = []
    for scope, table in (("validated", fam_members_val), ("all", fam_members)):
        fams = [f for f in FAM_ORDER if f in table] + sorted(set(table) - set(FAM_ORDER))
        hdr = f"\n=== RQ3 family resolve-rate — scope={scope} (tau={a.tau}) ===\n"
        hdr += f"{'family':10} {'#br':>4} " + " ".join(f"{f[:9]:>10}" for f in FUZZERS)
        print(hdr); print("-" * (16 + 11 * len(FUZZERS)))
        all_keys = set()
        for f in fams:
            all_keys |= table[f]
        for f in fams:
            members = table[f]
            rr = rates(members)
            cells = []
            row = {"scope": scope, "family": f, "n_branches": len(members)}
            for fz in FUZZERS:
                rate, n = rr[fz]
                cells.append(f"{rate:.2f}({n})" if rate is not None else "—")
                row[fz] = f"{rate:.3f}" if rate is not None else ""
                row[f"{fz}_n"] = n
            print(f"{f:10} {len(members):>4} " + " ".join(c.rjust(10) for c in cells))
            out_rows.append(row)
        # overall (distinct branches in scope)
        rr = rates(all_keys)
        print("-" * (16 + 11 * len(FUZZERS)))
        cells = [f"{rr[fz][0]:.2f}({rr[fz][1]})" if rr[fz][0] is not None else "—" for fz in FUZZERS]
        print(f"{'OVERALL':10} {len(all_keys):>4} " + " ".join(c.rjust(10) for c in cells))

    cols = ["scope", "family", "n_branches"] + sum(([f, f"{f}_n"] for f in FUZZERS), [])
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader(); w.writerows(out_rows)
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
