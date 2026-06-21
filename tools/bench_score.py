#!/usr/bin/env python3
"""tools/bench_score.py — RQ3 scorer: per-fuzzer resolve-rate PER MECHANISM CLASS.

The benchmark (RQ2) labels each blocker branch with a mechanism class in
bench/dataset.jsonl. RQ3 runs whole fuzzers (aflplusplus / honggfuzz / libfuzzer /
libafl) on the same targets+seeds and asks: does each engine resolve different
mechanism classes? This tool produces the answer matrix.

Two stages:

  measure  — turn the RQ3 fuzzers' campaign coverage into a per-branch resolve
             verdict, using the SAME signal the benchmark used for its canonical
             fuzzers (study_units.walk_target_state → hit_status per
             (file,line,col,blocked_side); resolved == hit_status 1). Maps each
             benchmark branch_id (DB: branches.{file,line,col,blocked_side}) to
             that key and counts n_resolved / n_blocked across the fuzzer's trials.
             → writes csvs/rq3_resolve.csv (fuzzer,target,branch_id,n_resolved,
             n_blocked,n_reached,n_trials).

             PREREQ: the RQ3 corpora (out/rq3/<t>/<f>/trial<N>/) must first be
             replayed through the libafl-<t>-cov binaries into a coverage_ts tree
             (LibAFL_Experiments/docker/run_coverage_timeseries.py --fuzzers
             "aflplusplus honggfuzz libfuzzer libafl", pointed at out/rq3). Pass
             that tree as --ts-base.

  score    — join csvs/rq3_resolve.csv with bench/dataset.jsonl (validated branch
             → mechanism label) and report, per (fuzzer × mechanism class), the
             resolve-rate = #resolved / #measured, where a branch is RESOLVED by a
             fuzzer iff resolved_frac = n_resolved/(n_resolved+n_blocked) >= TAU.

Resolve metric: resolved_frac >= TAU (default 0.8), the same threshold family the
benchmark's decisive_shape uses (>=8/10 trials). A branch the fuzzer never reached
(n_reached==0) is UNMEASURED, reported separately — NOT counted as blocked (G3).

CAVEAT (printed): `libafl` is the LibAFL `generic` engine — the SAME family that
produced the benchmark's labeled campaign — so its scores are a within-family
consistency check, not an independent cross-engine test. AFL++/honggfuzz/libFuzzer
are the clean cross-engine signal.

Usage:
  python3 tools/bench_score.py measure --ts-base out/rq3/coverage_ts \
      [--targets curl harfbuzz ...] [--trials 10] [--out csvs/rq3_resolve.csv]
  python3 tools/bench_score.py score [--resolve csvs/rq3_resolve.csv] \
      [--dataset bench/dataset.jsonl] [--tau 0.8] [--out csvs/rq3_score.csv]
"""
import argparse
import collections
import csv
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "blockers.sqlite"
DATASET = ROOT / "bench" / "dataset.jsonl"
RESOLVE_CSV = ROOT / "csvs" / "rq3_resolve.csv"
SCORE_CSV = ROOT / "csvs" / "rq3_score.csv"
FUZZERS = ["aflplusplus", "honggfuzz", "libfuzzer", "libafl"]
TARGETS = ["curl", "harfbuzz", "openthread", "sqlite3", "lcms", "libxml2", "libpng", "bloaty"]
TAU = 0.8


# ───────────────────────── measure ─────────────────────────
def measure(ts_base, targets, fuzzers, n_trials, out, db=None):
    # Read ONLY the final checkpoint per (fuzzer, trial): coverage is cumulative and
    # hit_status is monotonic, so the last report == the cumulative resolve state, and
    # it matches the benchmark's own "resolved at FINAL checkpoint" admission rule.
    sys.path.insert(0, str(ROOT / "tools"))
    from study_units import _trial_report_map, _parse_coverage_file

    ts_base = Path(ts_base)
    con = sqlite3.connect(db or DB)   # sB targets live in a separate DB (disjoint branch_id space)
    rows = []
    for target in targets:
        # benchmark branches for this target: (file,line,col) -> [(branch_id, blocked_side)]
        bmap = collections.defaultdict(list)
        for bid, f, ln, col, side in con.execute(
                "select branch_id, file, line, col, blocked_side from branches where target=?",
                (target,)):
            bmap[(f, ln, col)].append((bid, side))
        if not bmap:
            print(f"  {target}: no branches in DB, skip", file=sys.stderr)
            continue
        tally = collections.defaultdict(lambda: {"r": 0, "b": 0})   # (fz,bid) -> counts
        for fz in fuzzers:
            for trial in range(1, n_trials + 1):
                rmap = _trial_report_map(ts_base / target / fz / f"trial{trial}")
                if not rmap:
                    continue
                bd = _parse_coverage_file(str(rmap[max(rmap)]))      # final checkpoint
                for (f, ln, col), (th, fh) in bd.items():
                    for bid, side in bmap.get((f, ln, col), ()):
                        blocked = th if side == "T" else fh
                        other = fh if side == "T" else th
                        if blocked > 0:
                            tally[(fz, bid)]["r"] += 1
                        elif other > 0:
                            tally[(fz, bid)]["b"] += 1
                        # neither -> unreached, not counted
        for (fz, bid), t in tally.items():
            rows.append({"fuzzer": fz, "target": target, "branch_id": bid,
                         "n_resolved": t["r"], "n_blocked": t["b"],
                         "n_reached": t["r"] + t["b"], "n_trials": n_trials})
        nb = len({bid for (_fz, bid) in tally})
        print(f"  {target}: {nb} benchmark branches measured across {len(fuzzers)} fuzzers")
    con.close()
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["fuzzer", "target", "branch_id",
                                           "n_resolved", "n_blocked", "n_reached", "n_trials"])
        w.writeheader(); w.writerows(rows)
    print(f"wrote {out}: {len(rows)} (fuzzer,branch) resolve records")


# ───────────────────────── score ─────────────────────────
def load_labels(dataset, field="canonical_label"):
    """(target, branch_id) -> mechanism label, for VALIDATED branches only. Keyed by
    (target, branch_id) because branch_id is NOT unique across servers (bloaty_7 and
    curl_7 are different branches) — joining on bare id would conflate them.

    `field` selects the taxonomy granularity:
      canonical_label = the FINAL merged feature set (19 categories, Pass-C; default)
      label           = the raw pre-merge clusters (~50; debugging only)
    Falls back to `label` if a record lacks the requested field."""
    lab = {}
    for line in open(dataset):
        r = json.loads(line)
        if r.get("evidence", {}).get("status") != "validated":
            continue
        m = (r.get("mechanism") or {})
        v = m.get(field) or m.get("label")
        if v:
            lab[(r["target"], r["branch_id"])] = v
    return lab


def score(resolve_csv, dataset, tau, out, label_field="canonical_label"):
    labels = load_labels(dataset, label_field)          # (target,bid) -> class (validated)
    classes = sorted(set(labels.values()))
    class_branches = collections.defaultdict(set)       # class -> {(target,bid)}
    for key, c in labels.items():
        class_branches[c].add(key)

    # per (fuzzer, (target,bid)): resolved?  + which branches a fuzzer measured
    resolved = collections.defaultdict(dict)            # fuzzer -> {(target,bid): bool}
    measured = collections.defaultdict(set)             # fuzzer -> {(target,bid) reached}
    if not Path(resolve_csv).exists():
        sys.exit(f"{resolve_csv} not found — run `bench_score.py measure` first.")
    for r in csv.DictReader(open(resolve_csv)):
        key = (r["target"], int(r["branch_id"]))        # (target,bid): branch_id not unique across servers
        if key not in labels:
            continue                                    # only score labeled branches
        nr, nb = int(r["n_resolved"]), int(r["n_blocked"])
        if nr + nb == 0:
            continue                                    # never reached -> unmeasured (G3)
        fz = r["fuzzer"]
        measured[fz].add(key)
        resolved[fz][key] = (nr / (nr + nb)) >= tau

    # fuzzer columns: those present in the resolve CSV (RQ3 order first, extras sorted)
    present = set(measured)
    fz_cols = [f for f in FUZZERS if f in present] + sorted(present - set(FUZZERS))

    # matrix: class x fuzzer -> resolve-rate (#resolved / #measured-in-class)
    print(f"\nresolve-rate per mechanism class  (resolved_frac >= {tau}; "
          f"rate = #resolved / #measured)\n")
    hdr = f"{'mechanism class':42} {'#br':>4} " + " ".join(f"{f[:9]:>10}" for f in fz_cols)
    print(hdr); print("-" * len(hdr))
    out_rows = []
    for c in classes:
        cbs = class_branches[c]
        cells = []
        row = {"mechanism_class": c, "n_branches": len(cbs)}
        for fz in fz_cols:
            meas = cbs & measured[fz]
            res = sum(1 for b in meas if resolved[fz].get(b))
            rate = (res / len(meas)) if meas else None
            cells.append(f"{rate:.2f}({len(meas)})" if rate is not None else "—")
            row[fz] = f"{rate:.3f}" if rate is not None else ""
            row[f"{fz}_n"] = len(meas)
        print(f"{c[:42]:42} {len(cbs):>4} " + " ".join(c2.rjust(10) for c2 in cells))
        out_rows.append(row)

    # overall per-fuzzer (across all labeled+measured branches)
    print("-" * len(hdr))
    allb = set(labels)
    tot = []
    for fz in fz_cols:
        meas = allb & measured[fz]
        res = sum(1 for b in meas if resolved[fz].get(b))
        tot.append(f"{(res/len(meas) if meas else 0):.2f}({len(meas)})")
    print(f"{'OVERALL (all labeled, measured)':42} {len(allb):>4} " + " ".join(t.rjust(10) for t in tot))
    # coverage / honesty footer
    print("\ncoverage (labeled branches each fuzzer actually reached, of "
          f"{len(allb)} validated):")
    for fz in fz_cols:
        m = len(allb & measured[fz])
        print(f"  {fz:20} measured {m:4}/{len(allb)}  ({len(allb)-m} unmeasured: no corpus / never reached)")
    if "libafl" in fz_cols:
        print("\nCAVEAT: `libafl` is the LibAFL generic engine = the benchmark's own lineage "
              "(within-family consistency check). AFL++/honggfuzz/libFuzzer are the clean "
              "cross-engine signal.")

    Path(out).parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as fh:
        cols = ["mechanism_class", "n_branches"] + sum(([f, f"{f}_n"] for f in fz_cols), [])
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader(); w.writerows(out_rows)
    print(f"\nwrote {out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("measure")
    m.add_argument("--ts-base", required=True, help="coverage_ts tree for the RQ3 corpora")
    m.add_argument("--targets", nargs="*", default=TARGETS)
    m.add_argument("--fuzzers", nargs="*", default=FUZZERS)
    m.add_argument("--trials", type=int, default=10)
    m.add_argument("--db", default=None,
                   help="branches DB (default db/blockers.sqlite; use a separate DB for sB targets)")
    m.add_argument("--out", default=str(RESOLVE_CSV))
    s = sub.add_parser("score")
    s.add_argument("--resolve", default=str(RESOLVE_CSV))
    s.add_argument("--dataset", default=str(DATASET))
    s.add_argument("--tau", type=float, default=TAU)
    s.add_argument("--label-field", default="canonical_label",
                   choices=["canonical_label", "label"],
                   help="taxonomy granularity: canonical_label=final-19 (default), label=raw clusters")
    s.add_argument("--out", default=str(SCORE_CSV))
    a = ap.parse_args()
    if a.cmd == "measure":
        measure(a.ts_base, a.targets, a.fuzzers, a.trials, a.out, a.db)
    else:
        score(a.resolve, a.dataset, a.tau, a.out, a.label_field)


if __name__ == "__main__":
    main()
