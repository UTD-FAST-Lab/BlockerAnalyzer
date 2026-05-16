#!/usr/bin/env python3
"""
subject_significance.py — Coverage-curve scalars and pair-level significance for
the metaphorical-testing pipeline.

Subcommands:
    per-trial   Step 1: emit per-trial AUC + final-coverage scalars.
    pair        Step 2: per (target, A, B) subject, compute ΔAUC, p_AUC, ΔFinal,
                p_MW via Mann-Whitney U-tests over the per-trial scalars. Emits
                a CSV with one row per subject and an advisory `admissible`
                column gated by --alpha.

Reads:
    out/coverage_ts/<target>/<fuzzer>/trial<N>/coverage_timeseries.csv
    (columns: time_s, branch_covered, branch_total)

Per trial computes:
    - n_checkpoints, t_first_s, t_last_s  (data-quality columns)
    - branch_total                          (instrumentation-fixed per target)
    - auc_branch_seconds  = trapezoidal integral of branch_covered over time_s
                            from first to last checkpoint of THAT trial.
                            No padding — short trials get small AUCs by construction.
                            Alignment across trials is a Step 2 concern.
    - auc_normalized      = auc_branch_seconds / (branch_total * (t_last - t_first))
                            unitless; in [0, 1] if curve is monotone non-decreasing.
    - final_branches      = max(branch_covered)  (last value, but max-guards against
                            non-monotone artifacts in the source CSV)

Per-pair (Step 2) computes, for each (target, A, B) where (A, B, delta) is one of
the canonical pairs (cmplog/naive=I2S, value_profile/naive=VP, vpc/cmplog=VP,
vpc/value_profile=I2S):
    - n_A, n_B                              (trial counts on disk)
    - mean_auc_A, mean_auc_B, delta_auc     (delta = A - B)
    - p_auc                                 (two-sided MW U-test on per-trial AUC)
    - auc_dir                               ("A>B" / "B>A" / "tie")
    - mean_final_A, mean_final_B, delta_final, p_final, final_dir
    - admissible                            (True iff p_auc < alpha OR p_final < alpha)

Note: With small n (e.g. n=3 vs n=3) the smallest two-sided MW p-value is 0.10,
so `admissible` is advisory; treat it as a ranking signal, not a hard filter,
until trials per arm are scaled up.

Usage:
    python3 tools/subject_significance.py per-trial [--targets ...] [--fuzzers ...]
    python3 tools/subject_significance.py pair [--targets ...] [--alpha 0.05]
"""

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TS_BASE = REPO_ROOT / "out" / "coverage_ts"

CANONICAL_TARGETS = ["bloaty", "lcms", "mbedtls", "sqlite3"]
CANONICAL_FUZZERS = ["naive", "cmplog", "value_profile", "value_profile_cmplog"]

# Each entry is (A, B, delta_technique). A and B differ in exactly one technique.
CANONICAL_PAIRS = [
    ("cmplog", "naive", "I2S"),
    ("value_profile", "naive", "value_profile"),
    ("value_profile_cmplog", "cmplog", "value_profile"),
    ("value_profile_cmplog", "value_profile", "I2S"),
]


def read_timeseries(csv_path: Path):
    """Return list of (time_s, branch_covered, branch_total) tuples, or None if unreadable."""
    if not csv_path.is_file():
        return None
    rows = []
    with csv_path.open() as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                rows.append((int(r["time_s"]), int(r["branch_covered"]), int(r["branch_total"])))
            except (KeyError, ValueError):
                return None
    return rows or None


def trapezoid(times, values):
    """Trapezoidal rule. times and values must be same length, sorted by time."""
    if len(times) < 2:
        return 0.0
    auc = 0.0
    for i in range(1, len(times)):
        dt = times[i] - times[i - 1]
        auc += 0.5 * dt * (values[i] + values[i - 1])
    return auc


def per_trial_scalars(target: str, fuzzer: str, trial: int, ts_base: Path):
    csv_path = ts_base / target / fuzzer / f"trial{trial}" / "coverage_timeseries.csv"
    rows = read_timeseries(csv_path)
    if rows is None:
        return None
    rows.sort(key=lambda r: r[0])
    times = [r[0] for r in rows]
    covered = [r[1] for r in rows]
    branch_total = rows[-1][2]
    n = len(rows)
    t_first, t_last = times[0], times[-1]
    auc = trapezoid(times, covered)
    span = t_last - t_first
    auc_norm = (auc / (branch_total * span)) if (branch_total > 0 and span > 0) else 0.0
    return {
        "target": target,
        "fuzzer": fuzzer,
        "trial": trial,
        "n_checkpoints": n,
        "t_first_s": t_first,
        "t_last_s": t_last,
        "branch_total": branch_total,
        "auc_branch_seconds": round(auc, 2),
        "auc_normalized": round(auc_norm, 6),
        "final_branches": max(covered),
    }


def discover_trials(target: str, fuzzer: str, ts_base: Path):
    fuzzer_dir = ts_base / target / fuzzer
    if not fuzzer_dir.is_dir():
        return []
    trials = []
    for entry in fuzzer_dir.iterdir():
        if entry.is_dir() and entry.name.startswith("trial"):
            try:
                trials.append(int(entry.name[len("trial"):]))
            except ValueError:
                continue
    return sorted(trials)


def cmd_per_trial(args):
    ts_base = Path(args.ts_base).resolve()
    targets = args.targets or CANONICAL_TARGETS
    fuzzers = args.fuzzers or CANONICAL_FUZZERS

    rows = []
    for t in targets:
        for f in fuzzers:
            for n in discover_trials(t, f, ts_base):
                row = per_trial_scalars(t, f, n, ts_base)
                if row is not None:
                    rows.append(row)

    fieldnames = [
        "target", "fuzzer", "trial",
        "n_checkpoints", "t_first_s", "t_last_s",
        "branch_total",
        "auc_branch_seconds", "auc_normalized", "final_branches",
    ]
    out_stream = sys.stdout if args.output == "-" else open(args.output, "w", newline="")
    try:
        writer = csv.DictWriter(out_stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    finally:
        if out_stream is not sys.stdout:
            out_stream.close()
    if args.output != "-":
        print(f"wrote {len(rows)} rows to {args.output}", file=sys.stderr)


def _direction(delta: float) -> str:
    if delta > 0:
        return "A>B"
    if delta < 0:
        return "B>A"
    return "tie"


def pair_significance(target, a, b, delta_tech, ts_base, mannwhitneyu, alpha):
    a_trials = [per_trial_scalars(target, a, n, ts_base) for n in discover_trials(target, a, ts_base)]
    b_trials = [per_trial_scalars(target, b, n, ts_base) for n in discover_trials(target, b, ts_base)]
    a_trials = [r for r in a_trials if r is not None]
    b_trials = [r for r in b_trials if r is not None]

    base = {
        "target": target,
        "A": a,
        "B": b,
        "delta_technique": delta_tech,
        "n_A": len(a_trials),
        "n_B": len(b_trials),
        "mean_auc_A": "",
        "mean_auc_B": "",
        "delta_auc": "",
        "p_auc": "",
        "auc_dir": "",
        "mean_final_A": "",
        "mean_final_B": "",
        "delta_final": "",
        "p_final": "",
        "final_dir": "",
        "admissible": "",
    }
    if len(a_trials) < 2 or len(b_trials) < 2:
        base["admissible"] = "insufficient_trials"
        return base

    auc_a = [r["auc_branch_seconds"] for r in a_trials]
    auc_b = [r["auc_branch_seconds"] for r in b_trials]
    fin_a = [r["final_branches"] for r in a_trials]
    fin_b = [r["final_branches"] for r in b_trials]

    mean_auc_a = sum(auc_a) / len(auc_a)
    mean_auc_b = sum(auc_b) / len(auc_b)
    delta_auc = mean_auc_a - mean_auc_b
    try:
        _, p_auc = mannwhitneyu(auc_a, auc_b, alternative="two-sided")
    except ValueError:
        p_auc = 1.0  # all values identical

    mean_fin_a = sum(fin_a) / len(fin_a)
    mean_fin_b = sum(fin_b) / len(fin_b)
    delta_fin = mean_fin_a - mean_fin_b
    try:
        _, p_fin = mannwhitneyu(fin_a, fin_b, alternative="two-sided")
    except ValueError:
        p_fin = 1.0

    base.update({
        "mean_auc_A": round(mean_auc_a, 2),
        "mean_auc_B": round(mean_auc_b, 2),
        "delta_auc": round(delta_auc, 2),
        "p_auc": round(p_auc, 4),
        "auc_dir": _direction(delta_auc),
        "mean_final_A": round(mean_fin_a, 2),
        "mean_final_B": round(mean_fin_b, 2),
        "delta_final": round(delta_fin, 2),
        "p_final": round(p_fin, 4),
        "final_dir": _direction(delta_fin),
        "admissible": (p_auc < alpha) or (p_fin < alpha),
    })
    return base


def cmd_pair(args):
    try:
        from scipy.stats import mannwhitneyu
    except ImportError:
        print("error: scipy is required for the `pair` subcommand (Mann-Whitney U-test).", file=sys.stderr)
        sys.exit(2)

    ts_base = Path(args.ts_base).resolve()
    targets = args.targets or CANONICAL_TARGETS
    pairs = CANONICAL_PAIRS  # deliberate: one-tech delta is enforced by this list

    rows = []
    for target in targets:
        for a, b, delta_tech in pairs:
            rows.append(pair_significance(target, a, b, delta_tech, ts_base, mannwhitneyu, args.alpha))

    fieldnames = [
        "target", "A", "B", "delta_technique",
        "n_A", "n_B",
        "mean_auc_A", "mean_auc_B", "delta_auc", "p_auc", "auc_dir",
        "mean_final_A", "mean_final_B", "delta_final", "p_final", "final_dir",
        "admissible",
    ]
    out_stream = sys.stdout if args.output == "-" else open(args.output, "w", newline="")
    try:
        writer = csv.DictWriter(out_stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    finally:
        if out_stream is not sys.stdout:
            out_stream.close()
    if args.output != "-":
        print(f"wrote {len(rows)} rows to {args.output}", file=sys.stderr)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pt = sub.add_parser("per-trial", help="emit per-trial AUC and final-coverage scalars")
    pt.add_argument("--targets", nargs="+", help=f"default: {CANONICAL_TARGETS}")
    pt.add_argument("--fuzzers", nargs="+", help=f"default: {CANONICAL_FUZZERS}")
    pt.add_argument("--ts-base", default=str(DEFAULT_TS_BASE), help="root of coverage_ts/")
    pt.add_argument("--output", default="-", help="CSV output path or - for stdout (default)")
    pt.set_defaults(func=cmd_per_trial)

    pr = sub.add_parser("pair", help="per-(A,B,T) MW U-test over per-trial AUC and final coverage")
    pr.add_argument("--targets", nargs="+", help=f"default: {CANONICAL_TARGETS}")
    pr.add_argument("--ts-base", default=str(DEFAULT_TS_BASE), help="root of coverage_ts/")
    pr.add_argument("--alpha", type=float, default=0.05,
                    help="significance threshold for the advisory admissible column (default 0.05)")
    pr.add_argument("--output", default="-", help="CSV output path or - for stdout (default)")
    pr.set_defaults(func=cmd_pair)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
