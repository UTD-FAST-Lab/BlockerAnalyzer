#!/usr/bin/env python3
"""Ad-hoc: diagnose the RQ3 libafl low-resolve anomaly."""
import json, csv, collections

lab = {}
ds = {}
for l in open('bench/dataset.jsonl'):
    r = json.loads(l)
    if r.get('evidence', {}).get('status') != 'validated':
        continue
    k = (r['target'], r['branch_id'])
    lab[k] = r['mechanism']['label']
    ds[k] = r.get('decisive_shape')

# decisive_shape structure audit
struct = collections.Counter()
for k, d in ds.items():
    if isinstance(d, dict):
        struct[tuple(sorted(d.keys()))] += 1
    else:
        struct[('__nondict__', type(d).__name__)] += 1
print("=== decisive_shape key-sets among validated branches ===")
for s, n in struct.items():
    print(f"  {s}: {n}")

# one example each
seen = set()
print("\n=== examples ===")
for k, d in ds.items():
    sig = tuple(sorted(d.keys())) if isinstance(d, dict) else '__nondict__'
    if sig in seen:
        continue
    seen.add(sig)
    print(f"  {k}: {d}")

# rq3 resolve outcomes
rows = collections.defaultdict(dict)
for r in csv.DictReader(open('csvs/rq3_resolve.csv')):
    k = (r['target'], int(r['branch_id']))
    rows[k][r['fuzzer']] = (int(r['n_resolved']), int(r['n_blocked']), int(r['n_reached']))

def rq3_resolved(k, f):
    if k not in rows or f not in rows[k]:
        return None
    nr, nb, nrch = rows[k][f]
    if nrch == 0:
        return None
    return (nr / (nr + nb) if nr + nb > 0 else 0) >= 0.8

def resolve_set(d):
    if isinstance(d, dict):
        return tuple(sorted(d.get('resolve', d.get('resolvers', []))))
    return ()

# split RQ3 libafl outcome by whether original cmplog-family resolved
print("\n=== RQ3 libafl outcome vs ORIGINAL resolver-set ===")
detail = collections.defaultdict(lambda: [0, 0])
for k in lab:
    lr = rq3_resolved(k, 'libafl')
    if lr is None:
        continue
    detail[resolve_set(ds[k])][0 if lr else 1] += 1
print("original-resolver-set -> [libafl_resolved, libafl_blocked]")
for sig, (rr, bb) in sorted(detail.items(), key=lambda x: -(x[1][0] + x[1][1])):
    print(f"  {str(sig):48} resolved={rr:3} blocked={bb:3}")

# Does original cmplog membership predict RQ3 libafl resolve?
print("\n=== cmplog-in-original-resolve vs RQ3 libafl ===")
tbl = collections.defaultdict(lambda: [0, 0])
for k in lab:
    lr = rq3_resolved(k, 'libafl')
    if lr is None:
        continue
    rs = resolve_set(ds[k])
    has_cmplog = any('cmplog' in x for x in rs)
    tbl[has_cmplog][0 if lr else 1] += 1
for hc in (True, False):
    rr, bb = tbl[hc]
    print(f"  orig cmplog-resolved={hc}: RQ3 libafl resolved={rr} blocked={bb}")

def exact_cmplog(d):
    return 'cmplog' in resolve_set(d)  # exact standalone cmplog variant

# Focus class: i2s_exact_literal_gate
print("\n=== i2s_exact_literal_gate branches: orig cmplog? vs RQ3 per-fuzzer ===")
fz = ['aflplusplus', 'honggfuzz', 'libfuzzer', 'libafl']
hdr = f"{'target/bid':18} {'orig_resolve':34} " + " ".join(f"{f[:5]:>6}" for f in fz)
print(hdr)
for k in sorted(lab):
    if lab[k] != 'i2s_exact_literal_gate':
        continue
    rs = ",".join(resolve_set(ds[k]))
    cells = []
    for f in fz:
        v = rq3_resolved(k, f)
        cells.append('R' if v else ('b' if v is False else '-'))
    print(f"{k[0]+'/'+str(k[1]):18} {rs:34} " + " ".join(f"{c:>6}" for c in cells))

# aggregate: per-class orig-cmplog frac, orig-VP-needed frac, vs RQ3 resolved fracs
print("\n=== per-class: orig resolver profile vs RQ3 resolved frac (measured only) ===")
print(f"{'class':42} {'n':>3} {'oCmpl':>6} {'needVP':>6} " + " ".join(f"{f[:5]:>6}" for f in fz))
def needs_vp(d):
    # original label says cmplog-alone did NOT resolve but a VP-engine did
    rs = resolve_set(d)
    if 'cmplog' in rs:
        return False
    return any('value_profile' in x for x in rs)

agg = collections.defaultdict(lambda: {'n': 0, 'oc': 0, 'vp': 0, **{f: 0 for f in fz}})
for k in lab:
    if rq3_resolved(k, 'libafl') is None:
        continue
    c = lab[k]
    agg[c]['n'] += 1
    if exact_cmplog(ds[k]):
        agg[c]['oc'] += 1
    if needs_vp(ds[k]):
        agg[c]['vp'] += 1
    for f in fz:
        if rq3_resolved(k, f):
            agg[c][f] += 1
for c in sorted(agg, key=lambda x: -agg[x]['n']):
    a = agg[c]
    n = a['n']
    if n < 3:
        continue
    print(f"{c:42} {n:>3} {a['oc']/n:>6.2f} {a['vp']/n:>6.2f} " + " ".join(f"{a[f]/n:>6.2f}" for f in fz))
