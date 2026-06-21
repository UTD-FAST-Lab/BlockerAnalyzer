import json, collections
by_label = collections.defaultdict(lambda: collections.Counter())
shape_of = collections.defaultdict(set)
for l in open('bench/dataset.jsonl'):
    r = json.loads(l)
    lb = str(r['mechanism'].get('label'))
    d = r.get('decisive_shape') or {}
    key = (str(d.get('code')), tuple(d.get('resolve', [])),
           tuple(d.get('block', [])), tuple(d.get('nondecisive', [])))
    by_label[lb][key] += 1
    shape_of[lb].add(str(r.get('shape')))

for lb in sorted(by_label):
    if lb == 'i2s_exact_literal_gate' or lb.startswith('joint'):
        print(f'--- {lb}   shapes={sorted(shape_of[lb])} ---')
        for (code, res, blk, nd), n in by_label[lb].most_common():
            print(f'   code={code}  resolve={list(res)}  block={list(blk)}  nd={list(nd)}  n={n}')
