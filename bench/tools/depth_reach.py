#!/usr/bin/env python3
"""depth_reach — ctx/ngram (and vp-structural) evidence tool. 2026-06-12.

Tests the coverage-DEPTH mechanism: the winner arm's saved corpus reaches the
branch DEEPER (higher line execution count / the blocked side actually taken)
than the loser arm's corpus. For ctx (naive_ctx vs naive) the winner's
context-sensitive coverage retains seeds that drive the shared function from
call-contexts / iteration depths the loser collapses; for ngram (naive_ngram4 vs
naive) it retains sequential-decode states.

Unlike the byte tools this RUNS seeds through the instrumented binary (the
libafl-<target>-cov Docker image + per_role_in_container.py), then reads the
branch line's execution count from the llvm-cov dump. Per-FUZZER seed sets:
W = winner_fz resolving seeds, L = loser_fz blocking seeds.

  winner_line_count / loser_line_count = total executions of the branch line
  depth_lift = winner_line_count / max(loser_line_count, 1)
  winner_branch_taken / loser_branch_taken = was the blocker side taken (count>0)

PREDICTION (G1): winner reaches the line far more / takes the blocked side, loser
stalls (depth_lift >> 1, winner_branch_taken AND not loser_branch_taken). An
alternative (the seeds are equally deep, the difference is elsewhere) predicts
depth_lift ~ 1. G2-independent: measures what each arm's CORPUS reaches, not the
resolve label.

Usage:
  python3 bench/tools/depth_reach.py branch --target harfbuzz --branch-id 5878 \
      --winner-fuzzer naive_ctx --loser-fuzzer naive
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "db" / "blockers.sqlite"
QUEUE_BASE = ROOT / "out"
DOCKER_DIR = ROOT / "docker"
IMAGE_FMT = "libafl-{target}-cov"
sys.path.insert(0, str(ROOT / "tools"))
try:
    from seed_utils import parse_count as _pc
except Exception:  # noqa
    _pc = None


def pcount(s):
    """Robust count parse that NEVER returns None (callers do arithmetic)."""
    s = (s or "").strip().lower().replace(",", "")
    if not s:
        return 0
    if _pc is not None:
        try:
            v = _pc(s)
            if v is not None:
                return int(v)
        except Exception:  # noqa
            pass
    mult = 1
    if s and s[-1] in "kmg":
        mult = {"k": 1000, "m": 1_000_000, "g": 1_000_000_000}[s[-1]]
        s = s[:-1]
    try:
        return int(float(s) * mult)
    except ValueError:
        return 0


def seeds(con, table, branch_id, fuzzer, target, cap=60):
    """Seed file-refs for an arm, deterministic order, filtered to files that
    actually exist on disk (so the per-seed normalization divides by the count
    that the container will really run, not the count requested)."""
    rows = con.execute(
        f"select fuzzer, trial, seed_id from {table} where branch_id=? and fuzzer=? "
        f"order by trial, seed_id limit ?", (branch_id, fuzzer, cap)).fetchall()
    out = []
    for fz, tr, sid in rows:
        if (QUEUE_BASE / target / fz / f"trial{tr}" / "queue" / sid).exists():
            out.append({"queue_subdir": f"{fz}/trial{tr}/queue", "name": sid})
    return out


def run_container(target, jobs):
    image = IMAGE_FMT.format(target=target)
    if subprocess.run(["docker", "image", "inspect", image],
                      capture_output=True).returncode != 0:
        return None, f"image {image} not found"
    tmp = tempfile.mkdtemp(prefix="depth_reach_")
    (Path(tmp) / "out").mkdir()
    (Path(tmp) / "jobs.json").write_text(json.dumps(jobs))
    qdir = os.path.abspath(os.path.join(QUEUE_BASE, target))
    script = os.path.abspath(DOCKER_DIR / "per_role_in_container.py")
    cmd = ["docker", "run", "--rm", "--entrypoint", "",
           "-v", f"{qdir}:/queues:ro", "-v", f"{os.path.abspath(tmp)}:/work",
           "-v", f"{script}:/per_role_cov.py:ro", image, "/bin/bash", "-c",
           'python3 /per_role_cov.py --jobs /work/jobs.json --queues /queues '
           '--fuzz-bin "$FUZZ_BIN" --outdir /work/out']
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    except subprocess.TimeoutExpired:
        return tmp, "container timeout"
    return tmp, (None if p.returncode == 0 else (p.stderr or "")[:300])


# llvm-cov show format is  <lineno>|  <count>|<source>  (count column may be blank)
LINE_RE = re.compile(r"^\s*(\d+)\|\s*([\d.kKmM]*)\s*\|")
BR_RE = re.compile(r"Branch \((\d+):\d+\):\s*\[True:\s*([\d.]+[kKmM]?),\s*False:\s*([\d.]+[kKmM]?)\]")


def parse_line_depth(report_path, line):
    """Return (line_execution_count, max_blocked_side_count) at the branch line.
    The blocked-side count (the True/False arm actually taken) is the sharper
    depth signal than the bare line count."""
    if not report_path.is_file():
        return None, None
    count, side = 0, 0
    for ln in report_path.read_text(errors="replace").splitlines():
        m = LINE_RE.match(ln)
        if m and int(m.group(1)) == line and m.group(2).strip():
            count = max(count, pcount(m.group(2)))  # MAX, not last-write (macro expansion regions)
        b = BR_RE.search(ln)
        if b and int(b.group(1)) == line:
            side = max(side, pcount(b.group(2)), pcount(b.group(3)))
    return count, side


def analyze(target, branch_id, winner_fz, loser_fz):
    con = sqlite3.connect(DB)
    br = con.execute("select file, line from branches where branch_id=?", (branch_id,)).fetchone()
    if not br:
        return {"target": target, "branch_id": branch_id, "skip": "branch not in db"}
    bfile, bline = br
    W = seeds(con, "resolving_seeds", branch_id, winner_fz, target)
    L = seeds(con, "blocking_seeds", branch_id, loser_fz, target)
    con.close()
    if len(W) < 1 or len(L) < 1:
        return {"target": target, "branch_id": branch_id,
                "skip": f"insufficient on-disk seeds (W={len(W)} L={len(L)})"}
    jobs = {"branches": [{"branch_id": branch_id, "files": [bfile],
                          "W_seeds": W, "L_seeds": L,
                          "W_role_skip": False, "L_role_skip": False}]}
    tmp, err = run_container(target, jobs)
    if err:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)
        return {"target": target, "branch_id": branch_id, "skip": f"container: {err}"}
    base = Path(tmp) / "out" / str(branch_id)
    wc, ws = parse_line_depth(base / "W" / "branch_coverage_show.txt", bline)
    lc, ls = parse_line_depth(base / "L" / "branch_coverage_show.txt", bline)
    shutil.rmtree(tmp, ignore_errors=True)  # don't leak /tmp/depth_reach_* dumps
    if wc is None or lc is None:
        return {"target": target, "branch_id": branch_id, "skip": "no coverage dump"}
    # the merged llvm-cov count SUMS over the seed set, so normalize by seed count
    # (otherwise the arm with more seeds always "wins"). Per-seed depth = iteration
    # depth / reach of the AVERAGE input in that arm's corpus.
    nW, nL = len(W), len(L)
    w_ps, l_ps = wc / nW, lc / nL
    ws_ps, ls_ps = ws / nW, ls / nL
    return {
        "target": target, "branch_id": branch_id, "line": bline,
        "winner_fuzzer": winner_fz, "loser_fuzzer": loser_fz, "n_W": nW, "n_L": nL,
        "winner_depth": round(w_ps, 2), "loser_depth": round(l_ps, 2),
        "winner_side_depth": round(ws_ps, 2), "loser_side_depth": round(ls_ps, 2),
        "depth_lift": round(w_ps / max(l_ps, 0.5), 2),
        "side_lift": round(ws_ps / max(ls_ps, 0.5), 2),
        "winner_deeper": w_ps > l_ps,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("branch")
    b.add_argument("--target", required=True)
    b.add_argument("--branch-id", type=int, required=True)
    b.add_argument("--winner-fuzzer", required=True)
    b.add_argument("--loser-fuzzer", required=True)
    args = ap.parse_args()
    print(json.dumps(analyze(args.target, args.branch_id,
                             args.winner_fuzzer, args.loser_fuzzer), indent=1))


if __name__ == "__main__":
    main()
