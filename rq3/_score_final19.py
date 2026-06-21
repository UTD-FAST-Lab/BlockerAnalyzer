import json, csv, collections

# final-19 umbrella from canonical_label; family tag from direction/label prefix
FAMILY = {
    'i2s_string_literal_substitution': 'I2S-pro',
    'i2s_numeric_tag_substitution': 'I2S-pro',
    'i2s_structural_assembly_reach_depth': 'I2S-pro',
    'i2s_operand_value_precision': 'I2S-pro',
    'i2s_relational_collision_gate': 'I2S-pro',
    'i2s_anti_target_depletion': 'I2S-anti',
    'i2s_anti_decoy_overfit': 'I2S-anti',
    'i2s_anti_structural_byte_corruption': 'I2S-anti',
    'vp_gradient_value_distance_closure': 'VP-pro',
    'vp_gradient_drives_assembly_depth': 'VP-pro',
    'vp_operand_byte_enrichment': 'VP-pro',
    'vp_admits_structurally_richer_corpus': 'VP-pro',
    'joint_assembly_depth': 'JOINT',
    'vpc_anti_depth_diversion': 'VPC-anti',
    'ctx_iteration_path_depth': 'ctx-coverage',
    'ctx_corpus_inflation': 'ctx-coverage',
    'ngram_sequential_depth_reach': 'ngram-coverage',
    'grimoire_structural_token_assembly': 'grimoire',
    'grimoire_structural_size_depth': 'grimoire',
}

lab = {}
for l in open('bench/dataset.jsonl'):
    r = json.loads(l)
    if r.get('evidence', {}).get('status') != 'validated':
        continue
    cl = r['mechanism'].get('canonical_label')
    lab[(r['target'], r['branch_id'])] = cl

# audit: do canonical_labels match the final-19 list?
allcl = collections.Counter(lab.values())
print("=== canonical_label distribution (validated) ===")
unknown = [c for c in allcl if c not in FAMILY]
for c, n in allcl.most_common():
    flag = '' if c in FAMILY else '  <-- NOT in final-19'
    print(f"  {str(c):42} {n:>4}{flag}")
print(f"distinct canonical_labels: {len(allcl)}  (final-19 known: {sum(1 for c in allcl if c in FAMILY)})")
if unknown:
    print("UNKNOWN:", unknown)

rows = collections.defaultdict(dict)
for r in csv.DictReader(open('csvs/rq3_resolve.csv')):
    k = (r['target'], int(r['branch_id']))
    rows[k][r['fuzzer']] = (int(r['n_resolved']), int(r['n_blocked']), int(r['n_reached']))

fz = ['aflplusplus', 'honggfuzz', 'libfuzzer', 'libafl']

def resolved(k, f, tau=0.8):
    if k not in rows or f not in rows[k]:
        return None
    nr, nb, nrch = rows[k][f]
    if nrch == 0:
        return None
    return (nr / (nr + nb) if nr + nb > 0 else 0) >= tau

agg = collections.defaultdict(lambda: {'meas': 0, **{f: 0 for f in fz}})
for k, cl in lab.items():
    if resolved(k, 'libafl') is None:   # measured by the s4 campaign at all
        continue
    agg[cl]['meas'] += 1
    for f in fz:
        if resolved(k, f):
            agg[cl][f] += 1

print("\n=== RQ3 resolve-rate per FINAL-19 category (s4 targets, measured only) ===")
print(f"{'family':14} {'final feature':40} {'meas':>4} " + " ".join(f"{f[:5]:>6}" for f in fz))
order = sorted(agg, key=lambda c: (FAMILY.get(c, 'zzz'), -agg[c]['meas']))
tot = {f: 0 for f in fz}
totm = 0
for c in order:
    a = agg[c]
    m = a['meas']
    totm += m
    for f in fz:
        tot[f] += a[f]
    rates = " ".join(f"{(a[f]/m if m else 0):>6.2f}" for f in fz)
    print(f"{FAMILY.get(c,'?'):14} {c:40} {m:>4} {rates}")
print(f"{'OVERALL':14} {'':40} {totm:>4} " + " ".join(f"{tot[f]/totm:>6.2f}" for f in fz))
