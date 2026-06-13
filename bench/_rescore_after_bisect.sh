#!/usr/bin/env bash
set -e
# Portable: cd to the repo root (this script lives in bench/), so it runs on
# either server regardless of checkout path.
cd "$(dirname "$0")/.."
# Server tag + on-disk targets come from the environment so server B can run
# this verbatim: BENCH_SERVER=sB BENCH_ONDISK=lcms,libxml2,libpng,bloaty ./bench/_rescore_after_bisect.sh
: "${BENCH_SERVER:=s4}"
export BENCH_SERVER
# NOTE: run this AFTER seed_bisect has finished (do not rely on a pgrep wait —
# matching a process by command-string self-matches any shell holding that string).
echo "[rescore] bisection done; rebuilding OE label set (now-seeded branches included)"
python3 - <<'PY'
import json, glob, re, sqlite3, csv, collections, os
con=sqlite3.connect('db/blockers.sqlite')
ondisk=set((os.environ.get('BENCH_ONDISK') or 'curl,harfbuzz,openthread,sqlite3').split(','))
def cnt(tbl,b,fz): return con.execute(f'select count(*) from {tbl} where branch_id=? and fuzzer=?',(b,fz)).fetchone()[0]
seen=set(); rows=[]; armc=collections.Counter()
for sf in sorted(glob.glob('step5a_new_v3/i2s_vp_*/signatures.json')):
    for s in (lambda d: d if isinstance(d,list) else d.values())(json.load(open(sf))):
        m=re.match(r'([a-z0-9]+)_(\d+)',s.get('id',''))
        if not m: continue
        t,b=m.group(1),int(m.group(2))
        if t not in ondisk or b in seen: continue
        r=con.execute('select count(*) from resolving_seeds where branch_id=?',(b,)).fetchone()[0]
        l=con.execute('select count(*) from blocking_seeds where branch_id=?',(b,)).fetchone()[0]
        if r<3 or l<3: continue
        seen.add(b)
        cw=cnt('resolving_seeds',b,'cmplog'); vw=cnt('resolving_seeds',b,'value_profile_cmplog')
        nw=cnt('resolving_seeds',b,'naive');  pw=cnt('resolving_seeds',b,'value_profile')
        # Repoint the OE winner arm to vpc ONLY for genuine vpc-SOLE-winner branches
        # (cmplog, vp AND naive all fail to resolve; only value_profile_cmplog does).
        # That is the vpc-only-winner shape where cmplog is non-decisive so the
        # canonical cmplog/naive contrast measures the wrong arm. The sole-winner
        # guard EXCLUDES anti shapes (naive resolves -> keep cmplog/naive so the
        # depletion contrast holds) and VP-gradient shapes (vp resolves -> VP-driven,
        # not an I2S literal gate). Everything else keeps the canonical cmplog/naive.
        if cw==0 and vw>0 and nw==0 and pw==0: winner='value_profile_cmplog'
        else: winner='cmplog'
        rows.append(('x',t,b,winner,'naive')); armc[winner]+=1
w=csv.writer(open('csvs/arb_oe_labels.csv','w',newline=''))
w.writerow(['label','target','branch_id','winner','loser']); w.writerows(rows)
print(f"[rescore] OE labels: {len(rows)} branches | arms {dict(armc)}")
PY
echo "[rescore] re-running operand_enrichment study (corpus reload)..."
python3 bench/tools/i2s_operand_availability.py study --label-csv csvs/arb_oe_labels.csv --out "csvs/arb_operand_enrich_${BENCH_SERVER}.csv" --sample 20000 --head 256
echo "[rescore] arbiter --all (server=$BENCH_SERVER)"
python3 bench/arbitrate.py --all
echo "[rescore] build_dataset"
python3 bench/build_dataset.py
echo "[rescore] DONE"
