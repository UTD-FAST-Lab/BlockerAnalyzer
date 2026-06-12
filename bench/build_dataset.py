#!/usr/bin/env python3
"""bench/build_dataset.py — assemble step5b_new_v3/*/assignments.json into the
benchmark dataset bench/dataset.jsonl (one row per branch, schema = spec §6).

Joins each branch's arbiter assignment with its deterministic facts from the DB
(loc, decisive_shape, per-arm resolve/block counts) and the signature
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
    # 1) merge every server's assignments (assignments_*.json), prefer validated
    assigned = {}           # branch_id -> (shape, assignment, server)
    for af in sorted((ROOT / "step5b_new_v3").glob("*/assignments_*.json")):
        shape = af.parent.name
        data = json.loads(af.read_text())
        server = data.get("server", af.stem.split("assignments_")[-1])
        for a in data.get("assignments", []):
            m = re.match(r"[a-z0-9]+_(\d+)", a["branch"])
            if not m:
                continue
            bid = int(m.group(1))
            cur = assigned.get(bid)
            chosen = best(cur[1] if cur else None, a)
            assigned[bid] = (shape, chosen, server if chosen is a else (cur[2] if cur else server))
    # 2) per-branch seed counts in ONE pass (GROUP BY), not 8 queries/branch
    seeds = {}
    for tbl, key in (("resolving_seeds", "n_resolving_seeds"),
                     ("blocking_seeds", "n_blocking_seeds")):
        for bid, fz, n in con.execute(f"select branch_id, fuzzer, count(*) from {tbl} group by branch_id, fuzzer"):
            seeds.setdefault(bid, {}).setdefault(fz, {})[key] = n
    # 3) enumerate EVERY decisive branch from the signatures; unscored -> inconclusive
    rows = []
    seen = set()
    for sf in sorted((ROOT / "step5a_new_v3").glob("*/signatures.json")):
        shape = sf.parent.name
        decisive = shape_decode(shape)
        sigs = json.loads(sf.read_text())
        for s in (sigs if isinstance(sigs, list) else sigs.values()):
            m = re.match(r"([a-z0-9]+)_(\d+)", s.get("id", ""))
            if not m:
                continue
            target, bid = m.group(1), int(m.group(2))
            if bid in seen:
                continue
            seen.add(bid)
            br = con.execute("select file, function, line from branches where branch_id=?",
                             (bid,)).fetchone()
            loc = ({"file": br[0], "function": br[1], "line": br[2]} if br else {})
            a = assigned.get(bid)
            shp = a[0] if a else shape
            asg = a[1] if a else {"status": "inconclusive", "reason": "not scored by any server"}
            srv = a[2] if a else (SERVER if target in ONDISK else "other")
            rows.append({
                "branch_id": bid, "target": target, "loc": loc,
                "shape": shp, "decisive_shape": decisive,
                "per_arm_seeds": {k: v for k, v in (seeds.get(bid) or {}).items()},
                "mechanism": {"label": asg.get("hypothesis"),
                              "direction": asg.get("direction"),
                              "shape_source": f"step5b_new_v3/{shp}/evidence_test.json"},
                "evidence": {"status": asg.get("status"), "rule": asg.get("rule"),
                             "metrics": asg.get("metrics"), "reason": asg.get("reason"),
                             "report": f"step5b_new_v3/{shp}/assignments_{srv}.json"},
                "server": srv,
            })
    con.close()
    out = ROOT / "bench" / "dataset.jsonl"
    with open(out, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    import collections
    st = collections.Counter(r["evidence"]["status"] for r in rows)
    print(f"wrote {out}: {len(rows)} branches | status {dict(st)}")
    val = [r for r in rows if r["evidence"]["status"] == "validated"]
    byfam = collections.Counter(r["mechanism"]["label"] for r in val)
    print("\nvalidated by mechanism label:")
    for k, v in byfam.most_common():
        print(f"  {v:3d}  {k}")


if __name__ == "__main__":
    main()
