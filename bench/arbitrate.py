#!/usr/bin/env python3
"""bench/arbitrate.py — the deterministic per-branch arbiter (benchmark pivot).

For one shape (or all), reads step5b_new_v3/<shape>/evidence_test.json, and for
every branch in the shape runs the referenced measurement tools, evaluates each
hypothesis's decision rule in decision_order, and assigns the branch its
evidence-confirmed mechanism label / refuted / inconclusive. NO LLM: the only
judgment is the agent-authored rule; this just applies it.

Resolution: a hypothesis names a tool via measurement.registry_tool, OR (when the
agent designed it before the tool existed) via measurement.descriptor.compute.
Metrics from MULTIPLE tools can appear in one rule (e.g. operand_enrichment.skip
+ joint_necessity.size_lift); the arbiter runs each needed tool once per branch
(cached) and merges their metric dicts before evaluating the rule.

Scope (v1): the 3 BUILT tools (operand_enrichment, joint_necessity,
value_distance_reached). Rules needing an unbuilt tool (depth_reach,
corpus_size_ratio) or metrics no built tool emits are UNSCORABLE -> the branch
falls through to inconclusive (honest, G3). Only local-corpus targets
(curl/harfbuzz/openthread/sqlite3) are scorable here; others -> inconclusive
(other server).

Usage:
  python3 bench/arbitrate.py --shape i2s_vp_WLWL
  python3 bench/arbitrate.py --all
"""
import argparse
import json
import os
import re
import subprocess
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "blockers.sqlite"
# Each server scores only the targets whose corpora/seeds it holds. Override both
# on the OTHER server, e.g. BENCH_SERVER=sB BENCH_ONDISK=lcms,libxml2,libpng,bloaty
# The server tag makes assignments_<server>.json so the two never clobber;
# build_dataset.py merges assignments_*.json across servers.
ONDISK = {t.strip() for t in os.environ.get("BENCH_ONDISK", "curl,harfbuzz,openthread,sqlite3").split(",") if t.strip()}
SERVER = os.environ.get("BENCH_SERVER", "s4")

# operand_enrichment is corpus-heavy (reloads the whole corpus per call), so it is
# pre-run in STUDY mode (one corpus load per target) into this CSV; the arbiter
# reads the cache instead of invoking it per branch. joint_necessity and
# value_distance_reached read small SEED sets, so per-branch subprocess is fine.
OE_CACHE_CSV = ROOT / "csvs" / "arb_operand_enrich.csv"
OE_CACHE = {}
TOOL_CMD = {
    "joint_necessity": ["python3", "bench/tools/joint_necessity.py", "branch"],
    "value_distance_reached": ["python3", "bench/tools/value_distance_reached.py", "branch"],
    "depth_reach": ["python3", "bench/tools/depth_reach.py", "branch"],
}
BUILT = {"operand_enrichment", *TOOL_CMD}


def load_oe_cache():
    if not OE_CACHE_CSV.exists():
        return
    import csv as _csv
    for r in _csv.DictReader(open(OE_CACHE_CSV)):
        try:
            bid = int(r["branch_id"])
        except (KeyError, ValueError):
            continue
        d = {}
        for k in ("signed_target_enrich", "decoy_enrich", "cmplog_target_frac",
                  "naive_target_frac", "cmplog_decoy_frac", "naive_decoy_frac"):
            v = r.get(k, "")
            if v not in ("", None):
                try:
                    d[k] = float(v)
                except ValueError:
                    pass
        d["skip"] = r.get("skip") or None
        OE_CACHE[bid] = d
# metric name -> the tool that emits it (canonical names the tools actually print)
METRIC_TOOL = {}
for m in ("signed_target_enrich", "decoy_enrich", "cmplog_target_frac",
          "naive_target_frac", "cmplog_decoy_frac", "naive_decoy_frac"):
    METRIC_TOOL[m] = "operand_enrichment"
for m in ("size_lift", "tag_lift", "token_lift", "vp_tags", "cmp_tags", "vpc_tags",
          "winner_tags", "loser_tags", "i2s_necessary", "assembly_necessary"):
    METRIC_TOOL[m] = "joint_necessity"

# non-i2s/vp families: the decisive technique fuzzer vs the baseline. Used to aim
# joint_necessity's 2-arm pair mode (token/size comparison) at the right arms.
NONI2S_TECH = {"grimoire_structural": "grimoire", "mopt_mutation": "mopt",
               "ctx_coverage": "naive_ctx", "ngram_coverage": "naive_ngram4",
               "aflfast_rarity": "fast", "calibrated_energy": "minimizer"}
CANONICAL_TOKEN = "tag_lift >= 1.0 and winner_tags >= 2"
CANONICAL_DEPTH = "depth_lift >= 2.0 and winner_deeper == True"
for m in ("depth_lift", "side_lift", "winner_depth", "loser_depth", "winner_deeper"):
    METRIC_TOOL[m] = "depth_reach"
for m in ("vp_min_distance", "vpc_min_distance", "cmp_min_distance",
          "naive_min_distance", "distance_gap", "distance_closure_ratio",
          "winner_closer"):
    METRIC_TOOL[m] = "value_distance_reached"
# `skip` is emitted by every tool; resolve it from whichever tool ran.

# common alias normalizations agents used -> canonical metric names
ALIAS = {
    r"\bvp_min_dist\b": "vp_min_distance", r"\bvpc_min_dist\b": "vpc_min_distance",
    r"\bcmp_min_dist\b": "cmp_min_distance", r"\bnaive_min_dist\b": "naive_min_distance",
    r"\bdist_gap\b": "distance_gap", r"\bvp_dist\b": "vp_min_distance",
    r"\bcmp_dist\b": "cmp_min_distance", r"\bnaive_dist\b": "naive_min_distance",
    r"\bvpc_dist\b": "vpc_min_distance",
}


def shape_arms(shape):
    """winner/loser fuzzer arms from the i2s_vp code (cmp,vp,vpc,naive)."""
    m = re.match(r"i2s_vp_(.{4})$", shape)
    if not m:
        return None, None
    code = m.group(1)
    fz = ["cmplog", "value_profile", "value_profile_cmplog", "naive"]
    winners = [fz[i] for i, c in enumerate(code) if c == "W"]
    losers = [fz[i] for i, c in enumerate(code) if c == "L"]
    return winners, losers


def noni2s_pair_arms(shape, bid, con):
    """For the non-i2s/vp TOKEN families (grimoire/mopt/calibrated) that reuse
    joint_necessity in 2-arm mode: (winner_fz resolving, loser_fz blocking).
    WL = technique resolves -> winner=tech, loser=a real blocking arm. LW =
    technique blocks -> winner=naive, loser=tech. ctx/ngram use depth_reach (not
    built), so they are NOT routed here."""
    m = re.match(r"(grimoire_structural|mopt_mutation|calibrated_energy)_(WL|LW)$", shape)
    if not m:
        return None, None
    tech, d = NONI2S_TECH[m.group(1)], m.group(2)
    if d == "WL":
        wn = con.execute("select count(*) from resolving_seeds where branch_id=? and fuzzer=?",
                         (bid, tech)).fetchone()[0]
        if wn < 1:
            return None, None
        # prefer naive as the token-absent baseline (the agent's intended loser);
        # only fall back to another blocking arm if naive has too few seeds.
        nb = con.execute("select count(*) from blocking_seeds where branch_id=? and fuzzer='naive'",
                         (bid,)).fetchone()[0]
        if nb >= 3:
            return tech, "naive"
        row = con.execute("select fuzzer, count(*) c from blocking_seeds where branch_id=? "
                          "and fuzzer!=? group by fuzzer order by c desc", (bid, tech)).fetchone()
        if row and row[1] >= 3:
            return tech, row[0]
    else:  # LW
        wn = con.execute("select count(*) from resolving_seeds where branch_id=? and fuzzer='naive'",
                         (bid,)).fetchone()[0]
        ln = con.execute("select count(*) from blocking_seeds where branch_id=? and fuzzer=?",
                         (bid, tech)).fetchone()[0]
        if wn >= 1 and ln >= 3:
            return "naive", tech
    return None, None


def depth_arms(shape, bid, con):
    """ctx/ngram shapes -> (winner_fz resolving, loser_fz blocking) for depth_reach."""
    m = re.match(r"(ctx_coverage|ngram_coverage)_(WL|LW)$", shape)
    if not m:
        return None, None
    tech, d = NONI2S_TECH[m.group(1)], m.group(2)
    w, l = (tech, "naive") if d == "WL" else ("naive", tech)
    wn = con.execute("select count(*) from resolving_seeds where branch_id=? and fuzzer=?",
                     (bid, w)).fetchone()[0]
    ln = con.execute("select count(*) from blocking_seeds where branch_id=? and fuzzer=?",
                     (bid, l)).fetchone()[0]
    return (w, l) if wn >= 2 and ln >= 2 else (None, None)


def run_tool(tool, target, bid, extra):
    cmd = list(TOOL_CMD[tool]) + ["--target", target, "--branch-id", str(bid)] + extra
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=400)
        out = p.stdout.strip()
        # branch mode prints ONLY the json object; parse the whole stdout first,
        # fall back to the last balanced object if the tool ever prepends a log.
        try:
            return json.loads(out)
        except json.JSONDecodeError:
            i = out.rfind("\n{")
            if i >= 0:
                try:
                    return json.loads(out[i + 1:])
                except json.JSONDecodeError:
                    pass
            i = out.find("{")
            if i < 0:
                return {"_error": "no_json", "_log": (out + p.stderr)[:300]}
            return json.loads(out[i:])
    except subprocess.TimeoutExpired:
        return {"_error": "timeout"}
    except Exception as e:  # noqa
        return {"_error": str(e)[:200]}


# When an agent's value_distance rule uses idiosyncratic metric names the tool
# doesn't emit (lit_dist_gap, vp_dist_frac, distance_lift, ...), the arbiter falls
# back to this CANONICAL rule over the tool's validated metrics — which faithfully
# encode the gradient mechanism (winner lands closer to the operand than any loser).
CANONICAL_VD = "winner_closer == True and distance_gap >= 0.15"


def metrics_for_rule(rule, target, bid, shape, sig, cache, force_vd=False, force_jn=False, force_depth=False):
    """Run whichever BUILT tools the rule references; merge their metrics.
    force_vd/force_jn ensure value_distance/joint_necessity run even if the rule's
    metric names don't match the tool's canonical output (so a canonical fallback
    can score it)."""
    needed = set()
    for name, tool in METRIC_TOOL.items():
        if re.search(r"\b" + re.escape(name) + r"\b", rule):
            needed.add(tool)
    if force_vd:
        needed.add("value_distance_reached")
    if force_jn:
        needed.add("joint_necessity")
    if force_depth:
        needed.add("depth_reach")
    if re.search(r"\bskip\b", rule) and not (force_jn or force_depth):
        needed.add("operand_enrichment")  # `skip` is the operand tool's field — but
        # NOT for token/depth families (they emit their own skip; don't force OE there)
    merged = {}
    for tool in needed:
        if tool not in BUILT:
            return None  # unscorable: needs an unbuilt tool
        if tool == "operand_enrichment":
            if bid not in OE_CACHE:
                return None  # not in the pre-run cache (no seeds / non-local)
            cache[tool] = OE_CACHE[bid]
            merged.update(cache[tool])
            continue
        if tool not in cache:
            extra = []
            if tool == "joint_necessity":
                tok = sig.get("_tokens")
                if tok:
                    extra = ["--tokens", tok]
                jw, jl = sig.get("_jn_winner"), sig.get("_jn_loser")
                if jw and jl:  # non-i2s token family -> 2-arm pair mode
                    extra += ["--winner-fuzzer", jw, "--loser-fuzzer", jl]
            if tool == "value_distance_reached":
                val = sig.get("_operand")
                if not val:
                    return None  # no operand to test
                wa, la = shape_arms(shape)
                # winners = the shape's actual decisive W arms among the gradient
                # carriers; do NOT fall back to a hardcoded set (that would compare
                # arms the shape never asserted, biasing winner_closer).
                w = [a for a in (wa or []) if a in ("value_profile", "value_profile_cmplog")]
                l = [a for a in (la or []) if a in ("cmplog", "naive")]
                if not w or not l:
                    return None  # not a vp-gradient comparison this tool can score
                extra = ["--value", val, "--winners", ",".join(w), "--losers", ",".join(l)]
            if tool == "depth_reach":
                dw, dl = sig.get("_depth_winner"), sig.get("_depth_loser")
                if not (dw and dl):
                    return None  # not a ctx/ngram comparison this tool can score
                extra = ["--winner-fuzzer", dw, "--loser-fuzzer", dl]
            cache[tool] = run_tool(tool, target, bid, extra)
        r = cache[tool]
        if r.get("_error"):
            return None
        merged.update(r)
    # `skip` may be absent (tool scored) -> represent as None
    if "skip" in rule and "skip" not in merged:
        merged["skip"] = None
    return merged


def eval_rule(rule, metrics):
    expr = rule
    for pat, repl in ALIAS.items():
        expr = re.sub(pat, repl, expr)
    expr = re.sub(r"\bAND\b", " and ", expr)
    expr = re.sub(r"\bOR\b", " or ", expr)
    expr = re.sub(r"\btrue\b", "True", expr)
    expr = re.sub(r"\bfalse\b", "False", expr)
    try:
        return bool(eval(expr, {"__builtins__": {}}, dict(metrics)))  # noqa: S307
    except Exception:  # NameError(missing metric)/ZeroDivisionError/Attr/Value/...
        return None  # unscorable: never let one malformed rule crash the run


def parse_operand(sig):
    """Best-effort target operand from the signature for value_distance."""
    lit = sig.get("operand_literal")
    if not lit or not isinstance(lit, str):
        return None
    h = re.search(r"0x([0-9A-Fa-f]{2,16})", lit)
    if h:
        return "0x" + h.group(1)
    q = re.search(r"'([^']{1,12})'", lit) or re.search(r'"([^"]{1,12})"', lit)
    if q:
        return q.group(1)
    if re.fullmatch(r"[\x20-\x7e]{1,12}", lit):
        return lit
    return None


def shape_tokens(shape, target):
    # sfnt tags default for font targets; SQL keywords for sqlite3; XML/DTD for libxml2
    if target == "libxml2":
        return "<?xml,<!DOCTYPE,<![CDATA[,xmlns,<!ENTITY,SYSTEM,PUBLIC,</,<!ELEMENT,<!ATTLIST"
    if target == "lcms":
        return "acsp,mntr,scnr,prtr,XYZ ,Lab ,RGB ,GRAY,CMYK,mft2,mAB ,mBA ,curv,para,text"
    if target == "sqlite3":
        return "SELECT,CREATE,TABLE,INSERT,WHERE,FROM,VALUES,INDEX,PRAGMA,<<,||"
    return None  # joint_necessity default (sfnt tags) for harfbuzz/others


def branch_target(con, bid):
    r = con.execute("select target from branches where branch_id=?", (bid,)).fetchone()
    return r[0] if r else None


def arbitrate_shape(shape):
    et = ROOT / "step5b_new_v3" / shape / "evidence_test.json"
    sf = ROOT / "step5a_new_v3" / shape / "signatures.json"
    if not et.exists() or not sf.exists():
        return None
    test = json.loads(et.read_text())
    sigs = json.loads(sf.read_text())
    sigs = sigs if isinstance(sigs, list) else list(sigs.values())
    order = test.get("decision_order") or [h["id"] for h in test.get("hypotheses", [])]
    hyp_by_id = {h["id"]: h for h in test.get("hypotheses", [])}
    con = sqlite3.connect(DB)
    assignments = []
    for sig in sigs:
        sid = sig.get("id", "")
        m = re.match(r"([a-z0-9]+)_(\d+)", sid)
        if not m:
            continue
        target, bid = m.group(1), int(m.group(2))
        if target not in ONDISK:
            continue  # other server's target — it writes its own assignments file
        sig = dict(sig)
        sig["_operand"] = parse_operand(sig)
        sig["_tokens"] = shape_tokens(shape, target)
        jw, jl = noni2s_pair_arms(shape, bid, con)  # non-i2s token families
        sig["_jn_winner"], sig["_jn_loser"] = jw, jl
        dw, dl = depth_arms(shape, bid, con)         # ctx/ngram depth families
        sig["_depth_winner"], sig["_depth_loser"] = dw, dl
        cache = {}
        label = None
        for hid in order:
            h = hyp_by_id.get(hid)
            if not h or h.get("decidable") is False:
                continue
            rule = h.get("rule")
            if not rule:
                continue
            meas = h.get("measurement") or {}
            compute = (meas.get("descriptor") or {}).get("compute") if isinstance(meas, dict) else None
            is_vd = (meas.get("registry_tool") == "value_distance_reached"
                     or compute == "value_distance_reached")
            is_jn_pair = (meas.get("registry_tool") == "joint_necessity") and jw and jl
            is_depth = (compute == "depth_reach") and dw and dl
            met = metrics_for_rule(rule, target, bid, shape, sig, cache,
                                   force_vd=is_vd, force_jn=is_jn_pair, force_depth=is_depth)
            if met is None:
                continue  # unscorable by this hypothesis (no operand / unbuilt tool)
            applied = rule
            ok = eval_rule(rule, met)
            if ok is None and is_vd and "distance_gap" in met:
                applied, ok = CANONICAL_VD, eval_rule(CANONICAL_VD, met)  # reconcile to tool vocab
            if ok is None and is_jn_pair and "tag_lift" in met:
                applied, ok = CANONICAL_TOKEN, eval_rule(CANONICAL_TOKEN, met)
            if ok is None and is_depth and "depth_lift" in met:
                applied, ok = CANONICAL_DEPTH, eval_rule(CANONICAL_DEPTH, met)
            if ok:
                label = {"branch": sid, "target": target, "status": "validated",
                         "hypothesis": hid, "direction": h.get("direction"),
                         "rule": applied, "metrics": {k: met[k] for k in met
                                                      if not k.startswith("_") and k != "gate_offsets"}}
                break
        if label is None:
            assignments.append({"branch": sid, "target": target, "status": "inconclusive",
                                "reason": "no hypothesis rule matched / unscorable"})
        else:
            assignments.append(label)
    con.close()
    out = ROOT / "step5b_new_v3" / shape / f"assignments_{SERVER}.json"
    out.write_text(json.dumps({"shape": shape, "server": SERVER,
                               "n": len(assignments), "assignments": assignments}, indent=2))
    val = sum(1 for a in assignments if a["status"] == "validated")
    return {"shape": shape, "local": len(assignments), "validated": val}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--shape")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    load_oe_cache()
    print(f"operand_enrichment cache: {len(OE_CACHE)} branches", flush=True)
    shapes = ([args.shape] if args.shape else
              sorted(p.parent.name for p in (ROOT / "step5b_new_v3").glob("*/evidence_test.json")))
    rows = []
    for sh in shapes:
        r = arbitrate_shape(sh)
        if r:
            rows.append(r)
            print(f"  {r['shape']:28s} local={r['local']:3d}  validated={r['validated']:3d}", flush=True)
    tv = sum(r["validated"] for r in rows)
    tl = sum(r["local"] for r in rows)
    print(f"\nTOTAL: {tv} validated / {tl} local-target branches across {len(rows)} shapes")


if __name__ == "__main__":
    main()
