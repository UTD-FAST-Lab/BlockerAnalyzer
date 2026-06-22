#!/usr/bin/env python3
"""READ-ONLY diagnostic: for each 'independent' candidate branch (deciding pairs
span two families), test whether the SECOND family's hypothesis rule ALSO fires.
Reuses arbitrate.py's rule machinery; writes ONLY csvs/diag_multimatch_<server>.json.
Does NOT touch dataset.jsonl or assignments. Run with the same env as the arbiter:
  BENCH_SERVER=sB BENCH_ONDISK=lcms,libxml2,libpng,bloaty python3 bench/diag_collect_all.py
"""
import os, json, re, sqlite3
import arbitrate as arb

FAM = {'i2s_string_literal_substitution':'I2S-pro','i2s_numeric_tag_substitution':'I2S-pro','i2s_structural_assembly_reach_depth':'I2S-pro','i2s_operand_value_precision':'I2S-pro','i2s_relational_collision_gate':'I2S-pro','i2s_anti_target_depletion':'I2S-anti','i2s_anti_decoy_overfit':'I2S-anti','i2s_anti_structural_byte_corruption':'I2S-anti','vp_gradient_value_distance_closure':'VP-pro','vp_gradient_drives_assembly_depth':'VP-pro','vp_operand_byte_enrichment':'VP-pro','vp_admits_structurally_richer_corpus':'VP-pro','joint_assembly_depth':'JOINT','joint_value_distance_closure':'JOINT','vpc_anti_depth_diversion':'VPC-anti','vpc_anti_decoy_diversion':'VPC-anti'}

# hypothesis (raw) -> canonical, via the canonical map (for family of each hypothesis)
cm = json.load(open(arb.ROOT / "bench" / "canonical_label_map.json"))
LIT = set(cm['literal_family_split']['labels'])
def hyp_family(hraw):
    if hraw in LIT: return 'I2S-pro'  # literal family -> I2S-pro
    canon = cm['direct_map'].get(hraw, hraw)
    return FAM.get(canon)

# candidates passed via env JSON file (target,bid,shape,curfam,second)
CANDS = json.load(open(os.environ["DIAG_CANDS"]))

con = sqlite3.connect(arb.DB)
out = []
for c in CANDS:
    target, bid, shape, curfam, second = c['target'], c['branch_id'], c['shape'], c['cur'], c['second']
    et = arb.ROOT / "step5b_new_v3" / shape / "evidence_test.json"
    sf = arb.ROOT / "step5a_new_v3" / shape / "signatures.json"
    test = json.loads(et.read_text()); sigs = json.loads(sf.read_text())
    sigs = sigs if isinstance(sigs, list) else list(sigs.values())
    mysigs = [s for s in sigs if re.match(rf"{target}_{bid}(_|$)", s.get("id",""))]
    if not mysigs:
        out.append({**c, "result": "no_signature"}); continue
    # second-family hypotheses to test
    hyps2 = [h for h in test.get("hypotheses", [])
             if h.get("rule") and h.get("decidable") is not False and hyp_family(h.get("mechanism_label") or h.get("id","")) == second]
    if not hyps2:
        out.append({**c, "result": "no_2nd_family_hypothesis"}); continue
    fired = None
    for sig in mysigs:
        sig = dict(sig); sig["_operand"] = arb.parse_operand(sig); sig["_tokens"] = arb.shape_tokens(shape, target)
        jw, jl = arb.noni2s_pair_arms(shape, bid, con)
        if shape in arb.JN_PAIR_ARMS: jw, jl = arb.JN_PAIR_ARMS[shape]
        sig["_jn_winner"], sig["_jn_loser"] = jw, jl
        dw, dl = arb.depth_arms(shape, bid, con); sig["_depth_winner"], sig["_depth_loser"] = dw, dl
        cw, cl = arb.CS_ARMS.get(shape, (None, None)); sig["_cs_winner"], sig["_cs_loser"] = cw, cl
        tw, tl = arb.TC_ARMS.get(shape, (None, None)); sig["_tc_winner"], sig["_tc_loser"] = tw, tl
        cache = {}
        for h in hyps2:
            rule = h["rule"]; meas = h.get("measurement") or {}
            compute = (meas.get("descriptor") or {}).get("compute") if isinstance(meas, dict) else None
            is_vd = (meas.get("registry_tool")=="value_distance_reached" or compute=="value_distance_reached")
            is_jn = ((meas.get("registry_tool")=="joint_necessity" or compute=="struct_size_and_token_count") and jw and jl)
            is_dp = (compute=="depth_reach") and dw and dl
            met = arb.metrics_for_rule(rule, target, bid, shape, sig, cache, force_vd=is_vd, force_jn=is_jn, force_depth=is_dp)
            if met is None: continue
            applied = rule; ok = arb.eval_rule(rule, met)
            if ok is None and is_vd and "distance_gap" in met: applied, ok = arb.CANONICAL_VD, arb.eval_rule(arb.CANONICAL_VD, met)
            if ok is None and is_jn and "tag_lift" in met: applied, ok = arb.CANONICAL_TOKEN, arb.eval_rule(arb.CANONICAL_TOKEN, met)
            if ok is None and is_dp and "depth_lift" in met: applied, ok = arb.CANONICAL_DEPTH, arb.eval_rule(arb.CANONICAL_DEPTH, met)
            if ok:
                fired = {"hypothesis": h.get("id"), "rule": applied, "metrics": {k:met[k] for k in met if not k.startswith("_")}}
                break
        if fired: break
    out.append({**c, "result": "2nd_validated" if fired else "2nd_not_met", "fired": fired})

rep = arb.ROOT / "csvs" / f"diag_multimatch_{arb.SERVER}.json"
rep.write_text(json.dumps(out, indent=1))
n2 = sum(1 for o in out if o["result"]=="2nd_validated")
print(f"candidates tested: {len(out)}; 2nd category VALIDATED: {n2}; not met/other: {len(out)-n2}")
for o in out: print(f"  {o['target']}/{o['branch_id']} cur={o['cur']} +{o['second']} -> {o['result']}")
print("report:", rep)
