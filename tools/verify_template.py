#!/usr/bin/env python3
"""
verify_template.py — Step 5b verification runner for synthetic feature harnesses.

Takes a feature template (templates/<feature_id>/{template.c, params.json}),
sweeps its one compile-time `-D` knob across params.json:scan_values, builds the
harness under each involved LibAFL fuzzer variant, runs `trials_per_point`
fixed-duration trials per (scan_value, fuzzer), counts crashes, and scores a
verdict against the predicted dose-response direction.

Mechanism (de-risked 2026-05-24)
--------------------------------
Each variant ships a `<fuzzer>_cc` LibAFL compiler wrapper on PATH inside the
`libafl-base` image (built from ../libafl_fuzzbench). Build:

    <fuzzer>_cc --libafl -D<PARAM>=<val> template.c -o /w/harness

Run (libFuzzer-compat shim): `harness -o <corpus> -i <seeds>`. The harness's
`__builtin_trap()` is a CrashFeedback objective; solutions land in
`<corpus>/crashes/` as an OnDiskCorpus. crash_count = files in crashes/ (matches
the engine's own `objectives:` counter, verified).

MACHINE-LOAD SAFETY
-------------------
This launches `docker run` containers that each peg a core for `duration_s`.
The shared host often already has many campaign containers running. Therefore
parallelism is OPT-IN: `--jobs` defaults to 1 (serial). Raise it only when you
know the host has spare cores. One cell = one container running its trials
sequentially inside.

Output
------
By default writes a standalone `templates/<feature_id>/verification_run.json`
(safe: never clobbers a historical verdict). Pass `--write-spec` to also patch
the `verification` block of `feature_spec.json` in place.

Verdict (auto, auditable)
-------------------------
Parsed from params.json `expected_direction` ("WINNER > LOSER"). The runner
records every per-trial count + medians + the signals it judged on, so the
proposed verdict can be re-checked by hand. Verdict ∈ {reproduced,
reproduced_in_median, partially_reproduced, refuted, inconclusive}.
"""

import argparse
import json
import re
import statistics
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = REPO_ROOT / "templates"
DEFAULT_IMAGE = "libafl-base"

# The libFuzzer-compat invocation writes objectives to <corpus>/crashes/.
# This script is the in-container worker: build once, loop trials, print
# "TRIAL <i> crashes=<n> objectives=<o> execs=<e>" per trial.
CONTAINER_SCRIPT = r"""
set -u
mkdir -p /w/seeds
# Seeding policy: if the template dir ships a `seeds/` directory (mounted at
# /tpl/seeds), use those structured seed files verbatim. This is required for
# harnesses whose mechanism lives PAST a deep gauntlet (e.g. the anchored
# structure-preservation port: the test isolates trap behavior only if the
# starting input already satisfies magic + whitelist sites, so the fuzzers do
# not spend the whole budget — confounded by I2S — just reaching the trap).
# Otherwise fall back to a neutral 16-byte seed (covers multi-byte magic
# gates; harness size guards handle shorter knobs). Backward-compatible:
# templates with no seeds/ dir behave exactly as before.
if [ -d /tpl/seeds ] && [ -n "$(ls -A /tpl/seeds 2>/dev/null)" ]; then
  cp /tpl/seeds/* /w/seeds/
else
  printf 'AAAAAAAAAAAAAAAA' > /w/seeds/s0
fi
"${FUZZER}_${CCEXT}" --libafl "-D${PARAM}=${VAL}" "/tpl/${SRC}" -o /w/harness 2>/w/build.log
if [ ! -x /w/harness ]; then echo "BUILD_FAIL"; sed -n '1,40p' /w/build.log; exit 3; fi
cd /w
i=0
while [ "$i" -lt "$TRIALS" ]; do
  rm -rf "/w/c$i"
  timeout --kill-after=5 "$DURATION" /w/harness -o "/w/c$i" -i /w/seeds >/w/log 2>&1 || true
  cr=$(ls "/w/c$i/crashes" 2>/dev/null | grep -vc '\.metadata$')
  last=$(grep -aoE 'objectives: [0-9]+, executions: [0-9]+' /w/log | tail -1)
  obj=$(printf '%s' "$last" | grep -oE 'objectives: [0-9]+' | grep -oE '[0-9]+'); obj=${obj:-NA}
  ex=$(printf '%s' "$last" | grep -oE 'executions: [0-9]+' | grep -oE '[0-9]+'); ex=${ex:-NA}
  echo "TRIAL $i crashes=$cr objectives=$obj execs=$ex"
  i=$((i+1))
done
"""

TRIAL_RE = re.compile(
    r"TRIAL\s+(\d+)\s+crashes=(\d+)\s+objectives=(\S+)\s+execs=(\S+)")


def load_params(feature_id):
    pdir = TEMPLATES / feature_id
    if not pdir.is_dir():
        # allow passing a full path too
        pdir = Path(feature_id)
    params = json.loads((pdir / "params.json").read_text())
    src = None
    for cand in ("template.c", "template.cc", "template.cpp", "template.cxx"):
        if (pdir / cand).is_file():
            src = cand
            break
    if src is None:
        sys.exit(f"no template.c/.cc in {pdir}")
    return pdir, params, src


def parse_direction(params):
    """expected_direction 'WINNER > LOSER' -> (winner, loser). Falls back to
    feature_spec partition if present in the caller."""
    d = params.get("expected_direction", "")
    m = re.match(r"\s*(\S+)\s*>\s*(\S+)\s*$", d)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def run_cell(image, tpl_dir, src, param, val, fuzzer, trials, duration, ccext,
             name=None):
    """One container: build harness at -Dparam=val, run `trials` trials.
    `name` (optional) names the container so `docker ps` shows what each
    one is responsible for."""
    cmd = [
        "docker", "run", "--rm", "--entrypoint", "bash",
        *(["--name", name] if name else []),
        "-v", f"{tpl_dir.resolve()}:/tpl:ro",
        "-e", f"PARAM={param}", "-e", f"VAL={val}", "-e", f"FUZZER={fuzzer}",
        "-e", f"TRIALS={trials}", "-e", f"DURATION={duration}",
        "-e", f"SRC={src}", "-e", f"CCEXT={ccext}",
        image, "-c", CONTAINER_SCRIPT,
    ]
    # Allow build + trials*(duration+kill) + slack.
    to = 120 + trials * (duration + 30)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=to)
    except subprocess.TimeoutExpired:
        return {"error": "container_timeout", "crashes": []}
    out = p.stdout
    if "BUILD_FAIL" in out or "BUILD_FAIL" in p.stderr:
        return {"error": "build_fail", "log": (out + p.stderr)[:2000],
                "crashes": []}
    crashes, objs, execs = [], [], []
    for m in TRIAL_RE.finditer(out):
        crashes.append(int(m.group(2)))
        objs.append(m.group(3))
        execs.append(m.group(4))
    if not crashes:
        return {"error": "no_trials_parsed",
                "log": (out + p.stderr)[:2000], "crashes": []}
    return {"crashes": crashes, "objectives": objs, "executions": execs}


def med(xs):
    return statistics.median(xs) if xs else 0.0


def judge_multi(scan_values, winners, losers, per_fuzzer_med, per_fuzzer_trials):
    """Generalized verdict for a decisive-fuzzer SET (multi-fuzzer ordering).
    winners/losers = lists of fuzzer names predicted W / L (the non-'_' decisive
    set). Acceptance = the WEAKEST winner still beats the STRONGEST loser at the
    high knob, with the dose-response holding for every fuzzer. Reduces EXACTLY
    to judge() when len(winners)==len(losers)==1. '_' (non-decisive) fuzzers are
    not passed in and not scored."""
    if not winners or not losers:
        return "inconclusive", {"reason": "decisive set lacks a W and/or an L fuzzer"}
    lo, hi = scan_values[0], scan_values[-1]
    w_hi = min(per_fuzzer_med[hi][f] for f in winners)   # weakest winner
    l_hi = max(per_fuzzer_med[hi][f] for f in losers)    # strongest loser
    w_lo = min(per_fuzzer_med[lo][f] for f in winners)
    l_lo = max(per_fuzzer_med[lo][f] for f in losers)
    if all(per_fuzzer_med[sv][f] == 0 for sv in scan_values for f in (*winners, *losers)):
        return "inconclusive", {"reason": "no crashes anywhere; harness inert"}

    margin_hi = w_hi > l_hi
    losers_drop = all(per_fuzzer_med[hi][f] < per_fuzzer_med[lo][f]
                      or per_fuzzer_med[hi][f] == 0 for f in losers)
    winners_hold = all(per_fuzzer_med[hi][f] > 0
                       and per_fuzzer_med[hi][f] >= 0.5 * max(per_fuzzer_med[lo][f],
                                                              per_fuzzer_med[hi][f])
                       for f in winners)
    ratio_hi = w_hi / max(l_hi, 0.5)
    w_trials = [x for f in winners for x in per_fuzzer_trials[hi][f]]
    l_trials = [x for f in losers for x in per_fuzzer_trials[hi][f]]
    strict_hi = bool(w_trials) and bool(l_trials) and min(w_trials) > max(l_trials)
    signals = {"winners": winners, "losers": losers,
               "weakest_winner_high": w_hi, "strongest_loser_high": l_hi,
               "ratio_high": round(ratio_hi, 2), "margin_at_high": margin_hi,
               "losers_degrade": losers_drop, "winners_hold_high": winners_hold,
               "strict_per_trial_at_high": strict_hi}
    if not margin_hi:
        if l_hi > w_hi:
            return "refuted", {**signals, "reason": "a loser out-crashes a winner at high end"}
        return "inconclusive", {**signals, "reason": "no separation at high end"}
    strong = losers_drop and winners_hold and (ratio_hi >= 3 or l_hi == 0)
    if strong and strict_hi:
        return "reproduced", signals
    if strong:
        return "reproduced_in_median", signals
    return "partially_reproduced", {**signals,
                                    "reason": "weakest winner > strongest loser but weak margin"}


def judge(scan_values, winner, loser, per_fuzzer_med, per_fuzzer_trials):
    """Heuristic, auditable verdict. scan_values assumed ordered low->high
    effect (as authored). Prediction: winner stays high, loser degrades as the
    knob grows; stratification holds at the high end."""
    if winner is None or loser is None:
        return "inconclusive", {"reason": "no parseable expected_direction"}
    low, high = scan_values[0], scan_values[-1]
    w_hi, l_hi = per_fuzzer_med[high][winner], per_fuzzer_med[high][loser]
    w_lo, l_lo = per_fuzzer_med[low][winner], per_fuzzer_med[low][loser]

    all_zero = all(per_fuzzer_med[sv][f] == 0
                   for sv in scan_values for f in (winner, loser))
    if all_zero:
        return "inconclusive", {"reason": "no crashes anywhere; duration too "
                                "short or harness inert"}

    margin_hi = w_hi > l_hi
    loser_drops = (l_hi < l_lo) or (l_hi == 0)
    winner_holds = w_hi > 0 and w_hi >= 0.5 * max(w_lo, w_hi)
    ratio_hi = w_hi / max(l_hi, 0.5)
    # per-trial strict separation at the high end
    w_trials_hi = per_fuzzer_trials[high][winner]
    l_trials_hi = per_fuzzer_trials[high][loser]
    strict_hi = bool(w_trials_hi) and bool(l_trials_hi) and \
        min(w_trials_hi) > max(l_trials_hi)

    signals = {
        "winner": winner, "loser": loser,
        "winner_median_low": w_lo, "winner_median_high": w_hi,
        "loser_median_low": l_lo, "loser_median_high": l_hi,
        "ratio_high": round(ratio_hi, 2),
        "margin_at_high": margin_hi, "loser_degrades": loser_drops,
        "winner_holds_high": winner_holds, "strict_per_trial_at_high": strict_hi,
    }

    if not margin_hi:
        if l_hi > w_hi:
            return "refuted", {**signals, "reason": "direction reversed at high end"}
        return "inconclusive", {**signals, "reason": "no separation at high end"}
    # winner wins at high end
    strong = loser_drops and winner_holds and (ratio_hi >= 3 or l_hi == 0)
    if strong and strict_hi:
        return "reproduced", signals
    if strong:
        return "reproduced_in_median", signals
    return "partially_reproduced", {**signals,
                                    "reason": "winner > loser at high end but "
                                    "weak margin / loser did not clearly drop"}


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--template", required=True,
                    help="feature_id (dir under templates/) or path to a template dir")
    ap.add_argument("--image", default=DEFAULT_IMAGE)
    ap.add_argument("--duration-s", type=int, default=None,
                    help="override params.json duration_s (use small for smoke tests)")
    ap.add_argument("--trials", type=int, default=None,
                    help="override params.json trials_per_point")
    ap.add_argument("--scan-values", default=None,
                    help="comma list overriding params.json scan_values")
    ap.add_argument("--fuzzers", default=None,
                    help="comma list overriding params.json fuzzers")
    ap.add_argument("--jobs", type=int, default=1,
                    help="parallel containers (DEFAULT 1 = serial). Raise ONLY "
                         "with spare host cores — the host runs other campaigns.")
    ap.add_argument("--write-spec", action="store_true",
                    help="also patch feature_spec.json verification block in place")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the cell matrix + plan, run nothing")
    args = ap.parse_args()

    tpl_dir, params, src = load_params(args.template)
    feature_id = params.get("template_id", tpl_dir.name)
    param = params["parameter"]
    scan_values = (args.scan_values.split(",") if args.scan_values
                   else [str(v) for v in params["scan_values"]])
    fuzzers = (args.fuzzers.split(",") if args.fuzzers
               else params["fuzzers"])
    trials = args.trials or params.get("trials_per_point", 5)
    duration = args.duration_s or params.get("duration_s", 600)
    ccext = "cc" if src.endswith(".c") else "cxx"
    winner, loser = parse_direction(params)

    cells = [(sv, fz) for sv in scan_values for fz in fuzzers]
    est_s = (len(cells) / max(args.jobs, 1)) * (trials * duration + 60)
    print(f"== verify_template: {feature_id} ==")
    print(f"  param={param}  scan_values={scan_values}  fuzzers={fuzzers}")
    print(f"  trials={trials}  duration_s={duration}  jobs={args.jobs}")
    print(f"  direction: winner={winner} loser={loser}")
    print(f"  cells={len(cells)}  est. wall ~{est_s/60:.0f} min "
          f"({'SERIAL' if args.jobs == 1 else f'{args.jobs}-way'})")
    if args.dry_run:
        for sv, fz in cells:
            print(f"    [cell] {param}={sv}  {fz}  x{trials} trials")
        return

    results = {sv: {} for sv in scan_values}
    errors = []

    def work(sv, fz):
        return (sv, fz, run_cell(args.image, tpl_dir, src, param, sv, fz,
                                 trials, duration, ccext))

    if args.jobs == 1:
        for sv, fz in cells:
            sv, fz, r = work(sv, fz)
            _store(results, errors, sv, fz, r)
            tag = r.get("error", r.get("crashes"))
            print(f"  done {param}={sv} {fz}: {tag}")
    else:
        with ThreadPoolExecutor(max_workers=args.jobs) as ex:
            futs = [ex.submit(work, sv, fz) for sv, fz in cells]
            for f in as_completed(futs):
                sv, fz, r = f.result()
                _store(results, errors, sv, fz, r)
                tag = r.get("error", r.get("crashes"))
                print(f"  done {param}={sv} {fz}: {tag}")

    # medians + verdict
    per_med = {sv: {fz: med(results[sv].get(fz, {}).get("crashes", []))
                    for fz in fuzzers} for sv in scan_values}
    per_trials = {sv: {fz: results[sv].get(fz, {}).get("crashes", [])
                       for fz in fuzzers} for sv in scan_values}
    verdict, signals = judge(scan_values, winner, loser, per_med, per_trials)

    run_record = {
        "feature_id": feature_id,
        "ran_at": datetime.now(timezone.utc).isoformat(),
        "image": args.image,
        "parameter": param,
        "scan_values": scan_values,
        "fuzzers": fuzzers,
        "trials_per_point": trials,
        "duration_s": duration,
        "results_per_trial": {sv: {fz: results[sv].get(fz, {}).get("crashes", [])
                                   for fz in fuzzers} for sv in scan_values},
        "results_median": {"by_" + param: scan_values,
                           **{fz: [per_med[sv][fz] for sv in scan_values]
                              for fz in fuzzers}},
        "verdict": verdict,
        "verdict_provenance": "auto (verify_template.py heuristic)",
        "verdict_signals": signals,
        "errors": errors,
    }
    out_path = tpl_dir / "verification_run.json"
    out_path.write_text(json.dumps(run_record, indent=2) + "\n")
    print(f"\n  verdict: {verdict}  ({signals.get('reason','')})")
    print(f"  medians: " + "  ".join(
        f"{param}={sv}:[" + ",".join(f"{fz}={per_med[sv][fz]:g}" for fz in fuzzers) + "]"
        for sv in scan_values))
    print(f"  wrote {out_path}")
    if errors:
        print(f"  WARN {len(errors)} cell error(s): {errors}")

    if args.write_spec:
        spec_path = tpl_dir / "feature_spec.json"
        if spec_path.is_file():
            spec = json.loads(spec_path.read_text())
            v = spec.setdefault("verification", {})
            v["verdict"] = verdict
            v["scan_values"] = scan_values
            v["trials_per_point"] = trials
            v["duration_s"] = duration
            v["results_per_trial"] = run_record["results_per_trial"]
            v["results_median"] = run_record["results_median"]
            v.setdefault("notes", []).append(
                f"auto-verified {run_record['ran_at']} by verify_template.py: "
                f"{verdict}")
            spec_path.write_text(json.dumps(spec, indent=2) + "\n")
            print(f"  patched {spec_path} verification block")
        else:
            print(f"  --write-spec: no feature_spec.json at {spec_path}")


def _store(results, errors, sv, fz, r):
    results[sv][fz] = r
    if r.get("error"):
        errors.append({"scan_value": sv, "fuzzer": fz, "error": r["error"]})


if __name__ == "__main__":
    main()
