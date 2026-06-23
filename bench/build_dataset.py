#!/usr/bin/env python3
"""bench/build_dataset.py — assemble step5b_new_v3/*/assignments.json into the
benchmark dataset bench/dataset.jsonl (one row per (branch, decisive-shape axis),
schema = spec §6).

MULTI-LABEL (2026-06-13): a branch is decisive under one shape PER technique pair
(cmp/vp/vpc/naive for i2s_vp; fast-vs-naive for aflfast; etc.), so it legitimately
carries one label per axis. We therefore emit ONE ROW PER (branch_id, shape) — a
branch validated as an I2S literal gate AND also decisive (unmeasurable) under
aflfast-rarity appears as two rows. This is what per-mechanism-class scoring needs
(class membership = every branch decisive for that technique), and it stops the
`decidable:false` scheduling/coverage classes from being hollowed out by the old
one-row-per-branch dedup. The `_h0`/`_h1` joint-halves of ONE mechanism on ONE
shape are still merged to a single row (they are not a second label). No branch is
validated under two technique families, so multi-label adds no competing labels.

Joins each (branch, shape)'s arbiter assignment with its deterministic facts from
the DB (loc, decisive_shape, per-arm resolve/block counts) and the signature
(analysis-source pointer for G2). Branches scored on this server keep their
`validated|inconclusive` status; non-local branches stay `inconclusive`
(other server). The merge is idempotent — re-run after the other server's
assignments land to produce the full set.
"""
import json
import re
import sqlite3
from pathlib import Path

import os
ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "blockers.sqlite"
FZ = ["cmplog", "value_profile", "value_profile_cmplog", "naive"]
ONDISK = {t.strip() for t in os.environ.get("BENCH_ONDISK", "curl,harfbuzz,openthread,sqlite3").split(",") if t.strip()}
SERVER = os.environ.get("BENCH_SERVER", "s4")


def shape_decode(shape):
    m = re.match(r"i2s_vp_(.{4})$", shape)
    if m:
        code = m.group(1)
        return {"code": code,
                "resolve": [FZ[i] for i, c in enumerate(code) if c == "W"],
                "block": [FZ[i] for i, c in enumerate(code) if c == "L"],
                "nondecisive": [FZ[i] for i, c in enumerate(code) if c == "_"]}
    # non-i2s/vp families: <tech>_<WL|LW>
    m = re.match(r"(.+)_(WL|LW)$", shape)
    if m:
        d = "pro" if m.group(2) == "WL" else "anti"
        return {"code": m.group(2), "technique": m.group(1), "direction": d}
    return {"code": shape}


def best(a, b):
    """Prefer a validated assignment over an inconclusive one when both servers
    (or re-runs) emit a row for the same branch."""
    if a is None:
        return b
    if a.get("status") == "validated":
        return a
    if b.get("status") == "validated":
        return b
    return a


def main():
    con = sqlite3.connect(DB)
    # 1) merge every server's assignments, keyed by (branch_id, SHAPE) so each
    #    decisive axis is kept separately; prefer the validated/scored server per
    #    (branch, shape). _h0/_h1 halves of one joint mechanism collapse here
    #    (same bid + same shape) — they are not a second label.
    assigned = {}           # (bid, shape) -> (assignment, server)
    for af in sorted((ROOT / "step5b_new_v3").glob("*/assignments_*.json")):
        shape = af.parent.name
        data = json.loads(af.read_text())
        server = data.get("server", af.stem.split("assignments_")[-1])
        for a in data.get("assignments", []):
            m = re.match(r"([a-z0-9]+)_(\d+)", a["branch"])
            if not m:
                continue
            # key on the FULL signature id (target prefix + branch_id), NOT the
            # bare integer — branch_id collides across servers (bloaty_57 vs
            # curl_57). Drop any _hN joint-half suffix so _h0/_h1 of one mechanism
            # still collapse to one key.
            key = (f"{m.group(1)}_{m.group(2)}", shape)
            cur = assigned.get(key)
            chosen = best(cur[0] if cur else None, a)
            assigned[key] = (chosen, server if chosen is a else (cur[1] if cur else server))
    # 2) per-branch seed counts in ONE pass (GROUP BY), not 8 queries/branch
    seeds = {}
    for tbl, key in (("resolving_seeds", "n_resolving_seeds"),
                     ("blocking_seeds", "n_blocking_seeds")):
        for bid, fz, n in con.execute(f"select branch_id, fuzzer, count(*) from {tbl} group by branch_id, fuzzer"):
            seeds.setdefault(bid, {}).setdefault(fz, {})[key] = n
    # 3) enumerate EVERY (decisive branch x shape) from the signatures; one row per
    #    axis. The row's shape == decisive_shape source == assignment shape (coherent,
    #    unlike the old dedup which mixed the enumerated shape with a different
    #    preferred-validated assignment). Unscored axis -> inconclusive.
    rows = []
    seen = set()            # (sig_id, shape) — collapses _h0/_h1 within a shape
    for sf in sorted((ROOT / "step5a_new_v3").glob("*/signatures.json")):
        shape = sf.parent.name
        decisive = shape_decode(shape)
        sigs = json.loads(sf.read_text())
        for s in (sigs if isinstance(sigs, list) else sigs.values()):
            m = re.match(r"([a-z0-9]+)_(\d+)", s.get("id", ""))
            if not m:
                continue
            bid = int(m.group(2))
            # branch_id is NOT globally unique across servers, so trust the
            # signature-id PREFIX for target and key on the full id (prefix+bid).
            # The local DB is authoritative ONLY for this server's own targets;
            # for a non-local (other-server) prefix a same-id local branch would
            # supply the wrong loc/seeds, so only read the DB when the prefix is
            # one of our on-disk targets AND the row actually exists as that
            # target (else loc/seeds stay blank — the owning server fills them).
            target = m.group(1)
            key = (f"{target}_{bid}", shape)
            if key in seen:
                continue
            seen.add(key)
            br = None
            if target in ONDISK:
                br = con.execute("select target, file, function, line from branches where branch_id=?",
                                 (bid,)).fetchone()
                if br and br[0] != target:
                    br = None  # bare-id collision with a different local target
            loc = ({"file": br[1], "function": br[2], "line": br[3]} if br else {})
            a = assigned.get(key)
            asg = a[0] if a else {"status": "inconclusive", "reason": "not scored by any server"}
            srv = a[1] if a else (SERVER if target in ONDISK else "other")
            rows.append({
                "branch_id": bid, "target": target, "loc": loc,
                "shape": shape, "decisive_shape": decisive,
                "per_arm_seeds": {k: v for k, v in ((seeds.get(bid) if br else None) or {}).items()},
                "mechanism": {"label": asg.get("hypothesis"),
                              "direction": asg.get("direction"),
                              "shape_source": f"step5b_new_v3/{shape}/evidence_test.json"},
                "evidence": {"status": asg.get("status"), "rule": asg.get("rule"),
                             "metrics": asg.get("metrics"), "reason": asg.get("reason"),
                             "diag": asg.get("diag"),
                             "report": f"step5b_new_v3/{shape}/assignments_{srv}.json"},
                "server": srv,
            })
    # 4) MULTI-CATEGORY 2nd-category rows: an 'independent' branch (deciding pairs span
    #    two technique-directions) whose SECOND family's mechanism ALSO validates gets a
    #    second row -> genuinely multi-family. Source = the collect-all re-arbitration
    #    diagnostic (bench/diag_collect_all.py -> csvs/diag_multimatch_<server>.json),
    #    confirmed entries (result == "2nd_validated"). canonical_label is set downstream
    #    by apply_canonical_labels.py from the fired hypothesis (e.g. cmp_gradient... -> VP).
    import glob as _glob
    base = {(r["target"], r["branch_id"], r["shape"]): r for r in rows}
    for df in sorted(_glob.glob(str(ROOT / "csvs" / "diag_multimatch_*.json"))):
        for o in json.loads(Path(df).read_text()):
            if o.get("result") != "2nd_validated":
                continue
            b = base.get((o["target"], o["branch_id"], o["shape"]))
            if not b or not o.get("fired"):
                continue
            f = o["fired"]
            rows.append({
                "branch_id": b["branch_id"], "target": b["target"], "loc": b["loc"],
                "shape": b["shape"], "decisive_shape": b["decisive_shape"],
                "per_arm_seeds": b["per_arm_seeds"],
                "mechanism": {"label": f["hypothesis"],
                              "direction": o["second"].lower().replace("-", "_") + "_2ndcat",
                              "shape_source": b["mechanism"]["shape_source"]},
                "evidence": {"status": "validated", "rule": f["rule"],
                             "metrics": {k: v for k, v in f["metrics"].items()
                                         if k not in ("target", "branch_id")},
                             "reason": None, "diag": {"kind": "multi_category_2nd"},
                             "report": Path(df).name},
                "server": b["server"],
            })
    con.close()
    out = ROOT / "bench" / "dataset.jsonl"
    with open(out, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    import collections
    st = collections.Counter(r["evidence"]["status"] for r in rows)
    n_br = len({r["branch_id"] for r in rows})
    n_br_val = len({r["branch_id"] for r in rows if r["evidence"]["status"] == "validated"})
    print(f"wrote {out}: {len(rows)} rows (branch x shape axes) over {n_br} distinct branches | status {dict(st)}")
    print(f"  distinct branches with >=1 validated label: {n_br_val}")
    multi = collections.Counter(r["branch_id"] for r in rows)
    print(f"  branches appearing on >=2 axes (multi-label): {sum(1 for v in multi.values() if v >= 2)}")
    val = [r for r in rows if r["evidence"]["status"] == "validated"]
    byfam = collections.Counter(r["mechanism"]["label"] for r in val)
    print("\nvalidated by mechanism label:")
    for k, v in byfam.most_common():
        print(f"  {v:3d}  {k}")
    # inconclusive breakdown by diagnostic kind (G3 transparency: separate honest
    # "rule scored, didn't hold" from FIXABLE seed-starvation and not-yet-scored)
    inc = [r for r in rows if r["evidence"]["status"] == "inconclusive"]
    bykind = collections.Counter((r["evidence"].get("diag") or {}).get("kind", "not_scored")
                                 for r in inc)
    print(f"\ninconclusive by diagnostic kind ({len(inc)} total):")
    for k, v in bykind.most_common():
        print(f"  {v:3d}  {k}")


if __name__ == "__main__":
    main()
