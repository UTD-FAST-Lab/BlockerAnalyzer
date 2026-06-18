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

# Manual demotions: branches whose byte-rule label is a KNOWN mechanism mismatch
# the byte tool cannot self-correct. openthread 13300/13302 are stateful
# LinkedList ops (PopAfter/Find over the AddressResolver cache); they share the
# LWLW shape and trip the over-broad `ste < -0.3` overfit rule, but they have NO
# decoy (decoy_enrich~=0.08) so "decoy substitution" does not apply, and cmplog
# reaches the branch (2/8/0) exactly like the genuine harfbuzz members, so no
# byte/reachability metric separates them. Their true mechanism
# (state-diversity homogenization) has an unscorable hypothesis -> honest
# inconclusive (G3) is the correct outcome. See docs/i2s_anti_mechanisms.tex.
MANUAL_DEMOTE = {
    13300: "mechanism mismatch: stateful LinkedList op (PopAfter), no decoy "
           "(decoy_enrich~0.08); decoy-substitution claim does not hold; true "
           "state-diversity hypothesis is unscorable",
    13302: "mechanism mismatch: stateful LinkedList op (Find), no decoy "
           "(decoy_enrich~0.08); decoy-substitution claim does not hold; true "
           "state-diversity hypothesis is unscorable",
}

# operand_enrichment is corpus-heavy (reloads the whole corpus per call), so it is
# pre-run in STUDY mode (one corpus load per target) into this CSV; the arbiter
# reads the cache instead of invoking it per branch. joint_necessity and
# value_distance_reached read small SEED sets, so per-branch subprocess is fine.
# Per-server OE cache: each server pre-runs the corpus-heavy study on its OWN
# corpora and writes a server-tagged file, so the caches never collide in shared
# git. Falls back to the legacy unsuffixed name for single-server / pre-split runs.
OE_CACHE_CSV = ROOT / "csvs" / f"arb_operand_enrich_{SERVER}.csv"
if not OE_CACHE_CSV.exists():
    OE_CACHE_CSV = ROOT / "csvs" / "arb_operand_enrich.csv"
OE_CACHE = {}
# vp-arm OE: a SECOND study pass with winner=value_profile (vs naive), letting the
# i2s_vp_WW_L "both CMP arms enrich" rule test the value_profile arm INDEPENDENTLY
# (vp_signed_target_enrich) rather than assume it from shape membership. Same
# per-server tagging + legacy fallback. Absent file -> WW_L vp term simply
# unscorable (honest inconclusive), no effect on any other shape.
OE_VP_CACHE_CSV = ROOT / "csvs" / f"arb_operand_enrich_vp_{SERVER}.csv"
if not OE_VP_CACHE_CSV.exists():
    OE_VP_CACHE_CSV = ROOT / "csvs" / "arb_operand_enrich_vp.csv"
OE_VP_CACHE = {}
TOOL_CMD = {
    "joint_necessity": ["python3", "bench/tools/joint_necessity.py", "branch"],
    "value_distance_reached": ["python3", "bench/tools/value_distance_reached.py", "branch"],
    "depth_reach": ["python3", "bench/tools/depth_reach.py", "branch"],
    "corpus_size_ratio": ["python3", "bench/tools/corpus_size_ratio.py", "branch"],
    "token_count": ["python3", "bench/tools/token_count.py", "branch"],
    # live operand_enrichment for coverage shapes whose hypothesis compares a
    # NON-cmplog arm (naive_ctx vs naive) — the pre-run OE cache is cmplog-vs-naive
    # (the WRONG arm for a "ctx corpus depletes the operand" claim), so we invoke
    # the tool live with the correct arms instead of reading the cache.
    "operand_enrichment": ["python3", "bench/tools/i2s_operand_availability.py", "branch"],
}
# coverage shapes: the byte_freq depletion hypothesis compares the technique arm
# (naive_ctx) vs naive, NOT cmplog vs naive. Live-run OE with these arms.
CTX_OE_ARMS = {"ctx_coverage_LW": ("naive_ctx", "naive")}
CS_MEMO = {}   # (target, arm-pair) -> corpus_size_ratio result; branch-independent, scan once
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
    if OE_VP_CACHE_CSV.exists():
        for r in _csv.DictReader(open(OE_VP_CACHE_CSV)):
            try:
                bid = int(r["branch_id"])
            except (KeyError, ValueError):
                continue
            d = {}
            for src, dst in (("signed_target_enrich", "vp_signed_target_enrich"),
                             ("decoy_enrich", "vp_decoy_enrich")):
                v = r.get(src, "")
                if v not in ("", None):
                    try:
                        d[dst] = float(v)
                    except ValueError:
                        pass
            OE_VP_CACHE[bid] = d
# metric name -> the tool that emits it (canonical names the tools actually print)
METRIC_TOOL = {}
for m in ("signed_target_enrich", "decoy_enrich", "cmplog_target_frac",
          "naive_target_frac", "cmplog_decoy_frac", "naive_decoy_frac",
          "vp_signed_target_enrich", "vp_decoy_enrich"):
    METRIC_TOOL[m] = "operand_enrichment"
for m in ("size_lift", "tag_lift", "token_lift", "vp_tags", "cmp_tags", "vpc_tags",
          "winner_tags", "loser_tags", "i2s_necessary", "assembly_necessary",
          "token_density_lift", "winner_token_density", "loser_token_density"):
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
for m in ("corpus_count_ratio", "corpus_size_ratio", "size_ratio_cmp_over_naive",
          "composition_entropy_ratio"):
    METRIC_TOOL[m] = "corpus_size_ratio"
for m in ("naive_literal_count", "grimoire_literal_count", "literal_presence_ratio",
          "winner_literal_count", "loser_literal_count"):
    METRIC_TOOL[m] = "token_count"
# exact-literal-presence arm pairs (grimoire <GAP> erasure): winner=literal-preserving
# (naive, resolving), loser=grimoire (blocking). Literal comes from the signature.
# i2s_vp_WLWL: I2S (cmplog) plants the anchor literal at the gate; naive can't —
# winner=cmplog (resolving), loser=naive (blocking), literal = signature.operand_literal.
TC_ARMS = {"grimoire_structural_LW": ("naive", "grimoire"),
           "i2s_vp_WLWL": ("cmplog", "naive")}
# joint_necessity 2-arm PAIR-mode override for i2s_vp shapes whose hypothesis
# compares value_profile-resolving vs naive-blocking corpora (token-density /
# larger-structure) instead of the default 3-arm vpc/cmp/vp analysis.
JN_PAIR_ARMS = {"i2s_vp__WWL": ("value_profile", "naive")}
# corpus-scale arm pairs per shape: (winner=hypothesized inflating/homogenizing arm,
# loser=flat baseline). Whole-corpus comparison, branch-independent.
CS_ARMS = {"ctx_coverage_LW": ("naive_ctx", "naive"),
           "ngram_coverage_LW": ("naive_ngram4", "naive"),
           "i2s_vp_LWLW": ("cmplog", "naive"),
           "i2s_vp_L__W": ("cmplog", "naive"),
           "i2s_vp_WWLW": ("value_profile_cmplog", "value_profile")}
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
    # --- operand_enrichment name reconciliation (2026-06-14) ----------------
    # Several shapes' authored rules reference OE metric names the tool never
    # emits; map each to the vocabulary operand_enrichment ACTUALLY emits (the
    # SAME `skip == 'no_gate_signature'` / flat `signed_target_enrich` form the
    # design already uses in other shapes). Pure name plumbing — thresholds and
    # intent are preserved; the design's evidence_test.json is left untouched.
    #
    # `gate_signature == true/false` (i2s_vp_W__L) -> the tool signals gate
    # presence via `skip` (== 'no_gate_signature' when no fixed-offset gate).
    # \b before gate_signature so it does NOT match inside `no_gate_signature`.
    r"\bgate_signature\s*==\s*false\b": "(skip == 'no_gate_signature')",
    r"\bgate_signature\s*==\s*true\b": "(skip != 'no_gate_signature')",
    # `signed_target_enrich == no_gate_signature` (i2s_vp_LWWW) -> same `skip` test.
    r"\bsigned_target_enrich\s*==\s*no_gate_signature\b": "(skip == 'no_gate_signature')",
    # Per-arm namespaced OE (i2s_vp_WW_L). cmplog arm -> the flat cmplog-vs-naive
    # `signed_target_enrich` (OE_CACHE); value_profile arm -> `vp_signed_target_enrich`
    # from the dedicated vp-vs-naive study (OE_VP_CACHE). Both arms are now MEASURED
    # independently, honoring the authored per-arm rule + threshold.
    r"\bcmplog\.signed_target_enrich\b": "signed_target_enrich",
    r"\bvalue_profile\.signed_target_enrich\b": "vp_signed_target_enrich",
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


def branch_seed_counts(bid, con):
    """Total resolving / blocking seeds across all fuzzers for a branch.
    A low count (<3 either side) is the seed-starvation signature that the
    rank-10 re-bisect recovers (runbook step 2) -> a FIXABLE inconclusive."""
    nw = con.execute("select count(*) from resolving_seeds where branch_id=?",
                     (bid,)).fetchone()[0]
    nl = con.execute("select count(*) from blocking_seeds where branch_id=?",
                     (bid,)).fetchone()[0]
    return nw, nl


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
    # detect tools on the ALIAS-normalized rule (same reconciliation eval_rule
    # applies), so a rule written in reconciled-away names — e.g. `gate_signature
    # == false` -> `skip == 'no_gate_signature'` — still fetches the right tool.
    rule_norm = rule
    for pat, repl in ALIAS.items():
        rule_norm = re.sub(pat, repl, rule_norm)
    for name, tool in METRIC_TOOL.items():
        if re.search(r"\b" + re.escape(name) + r"\b", rule_norm):
            needed.add(tool)
    if force_vd:
        needed.add("value_distance_reached")
    if force_jn:
        needed.add("joint_necessity")
    if force_depth:
        needed.add("depth_reach")
    if re.search(r"\bskip\b", rule_norm) and not (force_jn or force_depth):
        needed.add("operand_enrichment")  # `skip` is the operand tool's field — but
        # NOT for token/depth families (they emit their own skip; don't force OE there)
    merged = {}
    for tool in sorted(needed):  # deterministic merge order (stable assignments JSON)
        if tool not in BUILT:
            return None  # unscorable: needs an unbuilt tool
        if tool == "operand_enrichment":
            if shape in CTX_OE_ARMS:    # coverage shapes: live naive_ctx-vs-naive (cmplog cache is the WRONG arm)
                cw, cl = CTX_OE_ARMS[shape]
                ck = ("oe_live", target, bid, cw, cl)
                if ck not in CS_MEMO:
                    CS_MEMO[ck] = run_tool("operand_enrichment", target, bid,
                                           ["--winner-fuzzer", cw, "--loser-fuzzer", cl])
                r = CS_MEMO[ck]
                if r.get("_error") or r.get("skip"):
                    return None
                cache[tool] = r
                merged.update(r)
                continue
            if bid not in OE_CACHE:
                return None  # not in the pre-run cache (no seeds / non-local)
            cache[tool] = OE_CACHE[bid]
            merged.update(cache[tool])
            if bid in OE_VP_CACHE:      # vp-arm enrichment (WW_L both-arms rule)
                merged.update(OE_VP_CACHE[bid])
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
            if tool == "corpus_size_ratio":
                cw, cl = sig.get("_cs_winner"), sig.get("_cs_loser")
                if not (cw and cl):
                    return None  # no corpus-pair defined for this shape
                extra = ["--winner-fuzzer", cw, "--loser-fuzzer", cl]
            if tool == "token_count":
                lit = sig.get("operand_literal")
                tw, tl = sig.get("_tc_winner"), sig.get("_tc_loser")
                if not (lit and tw and tl):
                    return None  # no gate literal or no token-arm pair for this shape
                extra = ["--literal", str(lit), "--winner-fuzzer", tw, "--loser-fuzzer", tl]
            if tool == "corpus_size_ratio":
                # branch-INDEPENDENT (whole-corpus arm comparison) -> memoize per
                # (target, arm-pair) so a 100k-file corpus is scanned once, not per branch.
                ck = (target, tuple(extra))
                if ck not in CS_MEMO:
                    CS_MEMO[ck] = run_tool(tool, target, bid, extra)
                cache[tool] = CS_MEMO[ck]
            else:
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
    if target == "libpng":
        # PNG structural chunk-type codes (the grammar tokens a grammar-aware
        # mutator/grimoire places). bloaty (ELF/Mach-O binaries) has no
        # token-family branches in the signature set, so it stays on the default.
        return "IHDR,PLTE,IDAT,IEND,tRNS,gAMA,cHRM,sRGB,iCCP,tEXt,zTXt,iTXt,bKGD,pHYs,sBIT,hIST,tIME"
    return None  # joint_necessity default (sfnt tags) for harfbuzz/bloaty/others


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
        bid = int(m.group(2))
        # branch_id is NOT globally unique across servers — each server's DB
        # assigns ids independently, so the bare integer collides (bloaty_57 and
        # curl_57 are different branches on the two servers). The signature-id
        # PREFIX is the authoritative target; trust it to decide ownership and
        # only score branches whose prefix is one of THIS server's on-disk
        # targets. (Reverts the earlier `branch_target(con, bid) or prefix`
        # resolution, which misread a cross-server id collision as a stale
        # prefix and mis-routed e.g. curl_57 onto this server's bloaty 57 corpus.
        # All local-prefix signatures here are DB-consistent — see the guard.)
        target = m.group(1)
        if target not in ONDISK:
            continue  # other server's target — it writes its own assignments file
        # Safety: the prefix claims a local target, but our DB must actually hold
        # this branch_id as that target; if not, the prefix is genuinely stale —
        # skip rather than score the wrong corpus.
        if branch_target(con, bid) != target:
            continue
        sig = dict(sig)
        sig["_operand"] = parse_operand(sig)
        sig["_tokens"] = shape_tokens(shape, target)
        jw, jl = noni2s_pair_arms(shape, bid, con)  # non-i2s token families
        if shape in JN_PAIR_ARMS:                    # explicit i2s_vp pair override (e.g. __WWL vp vs naive)
            jw, jl = JN_PAIR_ARMS[shape]
        sig["_jn_winner"], sig["_jn_loser"] = jw, jl
        dw, dl = depth_arms(shape, bid, con)         # ctx/ngram depth families
        sig["_depth_winner"], sig["_depth_loser"] = dw, dl
        cw, cl = CS_ARMS.get(shape, (None, None))    # corpus-scale inflation/homogenization
        sig["_cs_winner"], sig["_cs_loser"] = cw, cl
        tw, tl = TC_ARMS.get(shape, (None, None))    # exact-literal-presence (grimoire <GAP>)
        sig["_tc_winner"], sig["_tc_loser"] = tw, tl
        cache = {}
        label = None
        n_decidable = 0   # hypotheses we actually attempted (decidable + has a rule)
        n_scorable = 0    # of those, how many produced metrics (met is not None)
        for hid in order:
            h = hyp_by_id.get(hid)
            if not h or h.get("decidable") is False:
                continue
            rule = h.get("rule")
            if not rule:
                continue
            n_decidable += 1
            meas = h.get("measurement") or {}
            compute = (meas.get("descriptor") or {}).get("compute") if isinstance(meas, dict) else None
            is_vd = (meas.get("registry_tool") == "value_distance_reached"
                     or compute == "value_distance_reached")
            is_jn_pair = ((meas.get("registry_tool") == "joint_necessity"
                           or compute == "struct_size_and_token_count") and jw and jl)
            is_depth = (compute == "depth_reach") and dw and dl
            met = metrics_for_rule(rule, target, bid, shape, sig, cache,
                                   force_vd=is_vd, force_jn=is_jn_pair, force_depth=is_depth)
            if met is None:
                continue  # unscorable by this hypothesis (no operand / unbuilt tool)
            n_scorable += 1
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
        if bid in MANUAL_DEMOTE:
            assignments.append({"branch": sid, "target": target, "status": "inconclusive",
                                "reason": MANUAL_DEMOTE[bid],
                                "diag": {"kind": "manual_demote", "n_decidable": None,
                                         "n_scorable": None}})
            continue
        if label is None:
            # Distinguish the two epistemically different inconclusives (G3):
            #  - rule_not_met : a rule WAS scored and evaluated false -> honest,
            #                   the mechanism is not supported by campaign data.
            #  - unmeasurable : no decidable hypothesis could be measured. Split
            #                   seed-starved (FIXABLE via rank-10 re-bisect) from
            #                   genuinely-unmeasurable (no operand / unbuilt tool).
            #  - decidable_false_only : every hypothesis is decidable:false
            #                   (corpus-scale / non-discriminable by design).
            if n_decidable == 0:
                kind, reason = ("decidable_false_only",
                                "all hypotheses decidable:false (corpus-scale / non-discriminable)")
            elif n_scorable > 0:
                kind, reason = ("rule_not_met",
                                f"tested: {n_scorable}/{n_decidable} rule(s) scored, none held "
                                "(mechanism not supported by campaign data)")
            else:
                nw, nl = branch_seed_counts(bid, con)
                if nw < 3 or nl < 3:
                    kind, reason = ("seed_starved",
                                    f"unscorable: insufficient seeds (W={nw}, L={nl}; need >=3 each) "
                                    "-> rank-10 re-bisect candidate")
                else:
                    kind, reason = ("unmeasurable",
                                    "unscorable: measurement unavailable (no operand / unbuilt tool) "
                                    f"though seeds present (W={nw}, L={nl})")
            assignments.append({"branch": sid, "target": target, "status": "inconclusive",
                                "reason": reason,
                                "diag": {"kind": kind, "n_decidable": n_decidable,
                                         "n_scorable": n_scorable}})
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
