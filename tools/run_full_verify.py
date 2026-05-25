#!/usr/bin/env python3
"""Step-5b FULL parallel verification driver.

Runs the FULL params.json budget (duration_s, trials_per_point, all scan_values,
all involved fuzzers) for every template under step5b/, scheduling cells across
a fixed-width worker pool. One cell = one (scan_value, fuzzer) = one docker
container running trials_per_point trials sequentially. Because duration_s is
WALL-CLOCK, the pool width MUST NOT exceed available cores, or fuzzers get
starved of CPU and crash counts are distorted. Default --jobs 24.

Reuses verify_template.py's run_cell + judge so the verdict logic is identical.
Writes each template's verification_run.json as soon as its cells finish (crash-
safe progress) and a rolling csvs/full_verify_summary.json. Mirrors the
run_record schema of verify_template.main().
"""
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_template as vt  # noqa: E402  (run_cell, judge, med, parse_direction)

ROOT = Path(__file__).resolve().parent.parent
STEP5B = ROOT / "step5b"
SUMMARY = ROOT / "csvs" / "full_verify_summary.json"


def build_record(m):
    fz_list, svs, res = m["fuzzers"], m["scan_values"], m["results"]
    per_med = {sv: {fz: vt.med(res[sv].get(fz, {}).get("crashes", [])) for fz in fz_list}
               for sv in svs}
    per_trials = {sv: {fz: res[sv].get(fz, {}).get("crashes", []) for fz in fz_list}
                  for sv in svs}
    verdict, signals = vt.judge(svs, m["winner"], m["loser"], per_med, per_trials)
    errors = [{"scan_value": sv, "fuzzer": fz, "error": res[sv][fz]["error"]}
              for sv in svs for fz in fz_list
              if res[sv].get(fz, {}).get("error")]
    rec = {
        "feature_id": m["fid"],
        "ran_at": datetime.now(timezone.utc).isoformat(),
        "image": m["image"],
        "parameter": m["param"],
        "scan_values": svs,
        "fuzzers": fz_list,
        "trials_per_point": m["trials"],
        "duration_s": m["duration"],
        "results_per_trial": {sv: {fz: res[sv].get(fz, {}).get("crashes", []) for fz in fz_list}
                              for sv in svs},
        "results_median": {"by_" + m["param"]: svs,
                           **{fz: [per_med[sv][fz] for sv in svs] for fz in fz_list}},
        "verdict": verdict,
        "verdict_provenance": "auto (run_full_verify.py -> verify_template.judge)",
        "verdict_signals": signals,
        "errors": errors,
    }
    return rec, verdict


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--jobs", type=int, default=24,
                    help="max concurrent containers; MUST be <= host cores (wall-clock).")
    ap.add_argument("--image", default=vt.DEFAULT_IMAGE)
    ap.add_argument("--skip-existing", action="store_true",
                    help="skip templates that already have verification_run.json; "
                         "preload their verdicts into the summary so it stays complete.")
    ap.add_argument("--duration-s", type=int, default=None,
                    help="override params.json duration_s for ALL templates "
                         "(reduced-budget rerun; recorded in each verification_run.json).")
    ap.add_argument("--trials", type=int, default=None,
                    help="override params.json trials_per_point for ALL templates.")
    args = ap.parse_args()

    meta, cells, summary = {}, [], {}
    for tdir in sorted(STEP5B.iterdir()):
        if not ((tdir / "template.c").is_file() and (tdir / "params.json").is_file()):
            continue
        pdir, params, src = vt.load_params(str(tdir))
        existing = tdir / "verification_run.json"
        if args.skip_existing and existing.is_file():
            er = json.loads(existing.read_text())
            w, l = vt.parse_direction(params)
            summary[er.get("feature_id", tdir.name)] = {
                "verdict": er.get("verdict"), "winner": w, "loser": l,
                "medians": er.get("results_median", {}),
                "errors": len(er.get("errors", [])),
            }
            print(f"SKIP {tdir.name}  (existing verdict={er.get('verdict')})", flush=True)
            continue
        svs = [str(v) for v in params["scan_values"]]
        fz_list = params["fuzzers"]
        winner, loser = vt.parse_direction(params)
        meta[tdir.name] = {
            "tdir": pdir, "src": src, "param": params["parameter"],
            "scan_values": svs, "fuzzers": fz_list,
            "trials": args.trials if args.trials is not None else params.get("trials_per_point", 5),
            "duration": args.duration_s if args.duration_s is not None else params.get("duration_s", 600),
            "ccext": "cc" if src.endswith(".c") else "cxx",
            "winner": winner, "loser": loser,
            "fid": params.get("template_id", tdir.name), "image": args.image,
            "results": {sv: {} for sv in svs}, "remaining": len(svs) * len(fz_list),
        }
        for sv in svs:
            for fz in fz_list:
                cells.append((tdir.name, sv, fz))

    total = len(cells)
    print(f"START {datetime.now(timezone.utc).isoformat()}  cells={total}  "
          f"templates={len(meta)}  jobs={args.jobs}  image={args.image}", flush=True)

    def work(tid, sv, fz):
        m = meta[tid]
        r = vt.run_cell(args.image, m["tdir"], m["src"], m["param"], sv, fz,
                        m["trials"], m["duration"], m["ccext"])
        return tid, sv, fz, r

    done = 0
    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = [ex.submit(work, tid, sv, fz) for tid, sv, fz in cells]
        for f in as_completed(futs):
            tid, sv, fz, r = f.result()
            m = meta[tid]
            m["results"][sv][fz] = r
            m["remaining"] -= 1
            done += 1
            tag = r.get("error") or r.get("crashes")
            print(f"[{done}/{total}] {m['fid']} {m['param']}={sv} {fz}: {tag}", flush=True)
            if m["remaining"] == 0:
                rec, verdict = build_record(m)
                (m["tdir"] / "verification_run.json").write_text(json.dumps(rec, indent=2) + "\n")
                summary[m["fid"]] = {"verdict": verdict, "winner": m["winner"],
                                     "loser": m["loser"],
                                     "medians": rec["results_median"],
                                     "errors": len(rec["errors"])}
                SUMMARY.write_text(json.dumps(summary, indent=2) + "\n")
                print(f"  ==> WROTE {m['fid']}  verdict={verdict}  "
                      f"({m['remaining']==0 and 'complete'})", flush=True)

    print(f"\nDONE {datetime.now(timezone.utc).isoformat()}", flush=True)
    print("========== FULL VERIFY SUMMARY ==========", flush=True)
    for fid, s in sorted(summary.items()):
        print(f"{s['verdict']:<24} {fid:<52} ({s['winner']} vs {s['loser']})"
              + (f"  [{s['errors']} cell-errors]" if s['errors'] else ""), flush=True)
    print(f"\nwrote {SUMMARY}", flush=True)


if __name__ == "__main__":
    main()
