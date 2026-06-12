#!/usr/bin/env bash
set -e
cd /home/miao/work/BlockerAnalyzer
# NOTE: run this AFTER seed_bisect has finished (do not rely on a pgrep wait —
# matching a process by command-string self-matches any shell holding that string).
echo "[rescore] bisection done; rebuilding OE label set (now-seeded branches included)"
python3 - <<'PY'
import json, glob, re, sqlite3, csv
con=sqlite3.connect('db/blockers.sqlite'); ondisk={'curl','harfbuzz','openthread','sqlite3'}
seen=set(); rows=[]
for sf in glob.glob('step5a_new_v3/i2s_vp_*/signatures.json'):
    for s in (lambda d: d if isinstance(d,list) else d.values())(json.load(open(sf))):
        m=re.match(r'([a-z0-9]+)_(\d+)',s.get('id',''))
        if not m: continue
        t,b=m.group(1),int(m.group(2))
        if t not in ondisk or b in seen: continue
        r=con.execute('select count(*) from resolving_seeds where branch_id=?',(b,)).fetchone()[0]
        l=con.execute('select count(*) from blocking_seeds where branch_id=?',(b,)).fetchone()[0]
        if r>=3 and l>=3: rows.append(('x',t,b)); seen.add(b)
csv.writer(open('csvs/arb_oe_labels.csv','w',newline='')).writerows([['label','target','branch_id']]+rows)
print(f"[rescore] OE labels: {len(rows)} branches")
PY
echo "[rescore] re-running operand_enrichment study (corpus reload)..."
python3 bench/tools/i2s_operand_availability.py study --label-csv csvs/arb_oe_labels.csv --out csvs/arb_operand_enrich.csv --sample 8000 --head 256
echo "[rescore] arbiter --all"
BENCH_SERVER=s4 python3 bench/arbitrate.py --all
echo "[rescore] build_dataset"
python3 bench/build_dataset.py
echo "[rescore] DONE"
