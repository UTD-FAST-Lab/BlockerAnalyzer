#!/usr/bin/env python3
"""tools/apply_canonical_labels.py — Pass-C: apply the canonical mechanism taxonomy.

Reads bench/canonical_label_map.json (57 raw labels -> 19 canonical features) and adds
a `canonical_label` field to each validated branch in bench/dataset.jsonl, PRESERVING the
raw `mechanism.label` (non-destructive, reversible). The I2S fixed-offset-literal family is
split string-vs-numeric by the branch's signature operand_kind (RQ3-driven).

Idempotent: re-running recomputes canonical_label from the raw label + map. Run after any
build_dataset.py rebuild to refresh canonical_label.

  python3 tools/apply_canonical_labels.py            # apply + report
  python3 tools/apply_canonical_labels.py --report   # report only (no write)
"""
import argparse, glob, json, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DS = ROOT / "bench" / "dataset.jsonl"
MAP = ROOT / "bench" / "canonical_label_map.json"
OVERRIDE = ROOT / "bench" / "branch_canonical_override.json"  # per-branch Pass-C family fixes


def load_operand_kinds():
    ok = {}
    for sf in glob.glob(str(ROOT / "step5a_new_v3" / "*" / "signatures.json")):
        for s in json.load(open(sf)):
            if s.get("id"):
                ok[s["id"]] = s.get("operand_kind")
    return ok


def canonical(label, target, branch_id, opkinds, m):
    lf = m["literal_family_split"]
    if label in lf["labels"]:
        k = str(opkinds.get(f"{target}_{branch_id}"))
        if any(sub in k for sub in lf["numeric_operand_kind_substrings"]):
            return lf["numeric_canonical"]
        return lf["string_canonical"]
    return m["direct_map"].get(label, label)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", action="store_true", help="report only, no write")
    a = ap.parse_args()
    m = json.load(open(MAP))
    override = {k: v for k, v in (json.load(open(OVERRIDE)) if OVERRIDE.exists() else {}).items()
                if not k.startswith("_")}
    opkinds = load_operand_kinds()
    rows = [json.loads(l) for l in open(DS)]
    counts = collections.Counter()
    unmapped = collections.Counter()
    direct = set(m["direct_map"].values()) | {m["literal_family_split"]["string_canonical"],
                                              m["literal_family_split"]["numeric_canonical"]}
    for r in rows:
        mech = r.get("mechanism") or {}
        lab = mech.get("label")
        if not lab:
            continue
        canon = canonical(lab, r["target"], r["branch_id"], opkinds, m)
        canon = override.get(f"{r['target']}_{r['branch_id']}_{r['shape']}", canon)  # per-branch Pass-C fix
        mech["canonical_label"] = canon
        counts[canon] += 1
        if lab not in m["direct_map"] and lab not in m["literal_family_split"]["labels"]:
            unmapped[lab] += 1
    if not a.report:
        with open(DS, "w") as fh:
            for r in rows:
                fh.write(json.dumps(r) + "\n")
    print(f"{'WROTE' if not a.report else 'REPORT'}: {len(counts)} canonical features over "
          f"{sum(counts.values())} validated branches")
    for f, n in counts.most_common():
        print(f"  {n:4d}  {f}")
    if unmapped:
        print("\nUNMAPPED raw labels (kept as-is — add to map if real):")
        for L, n in unmapped.most_common():
            print(f"  {n:4d}  {L}")


if __name__ == "__main__":
    main()
