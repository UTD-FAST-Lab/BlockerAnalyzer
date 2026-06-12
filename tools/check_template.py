#!/usr/bin/env python3
"""
check_template.py — deterministic preflight for step-5b synthetic templates.

Gates the (expensive) verify_template.py sweep with cheap, judgment-free checks
that catch the MECHANICAL failure modes — so an author-agent retry (budget) is
spent on a real defect, never on a scientific refutation. Run after the
template-author writes step5b/<feature_id>/{template.c, params.json} and before
verify_template.py.

Checks
------
1. Schema/sanity (no container):
   - params.json has parameter, scan_values (>=2), fuzzers, expected_direction.
   - fuzzers ⊆ {naive,cmplog,value_profile,value_profile_cmplog}.
   - expected_direction "WINNER > LOSER"; winner+loser ∈ fuzzers.
   - params.parameter token appears in template.c.
2. Compiles (one container, plain clang-18, no fuzzer/link, fast):
   - every scan_value compiles (catches build errors + invalid -D values).
3. KNOB IS LIVE (the clincher):
   - assembly at min(scan_values) != assembly at max(scan_values). If identical,
     the `-D<parameter>` changed nothing → the macro name in params.json doesn't
     match a live `#if/#ifndef` in template.c (the classic author/params drift
     that would silently flatten the dose-response into a false `refuted`).

Exit 0 = pass; non-zero = fail. On fail, prints structured reasons suitable as
verbatim retry feedback to the template-author.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = REPO_ROOT / "templates"
DEFAULT_IMAGE = "libafl-coverage-base"   # has clang-18, small
# icse27 10-fuzzer set (extended 2026-06-06 from the original 4 canonical
# variants; the campaign now sweeps minimizer/fast/naive_ctx/grimoire/honggfuzz
# in addition to the base I2S/VP grid). Each variant ships a <fuzzer>_cc wrapper
# in the libafl image, so verify_template can build any of them.
CANON = {"naive", "cmplog", "value_profile", "value_profile_cmplog",
         "minimizer", "fast", "naive_ctx", "naive_ngram4", "naive_ngram8",
         "grimoire", "honggfuzz", "mopt"}

# Compile each scan value to assembly (deterministic, no timestamps) and sha it.
COMPILE_SCRIPT = r"""
set -u
ok=1
for V in $VALUES; do
  if clang-18 -O2 -S -x c "-D${PARAM}=${V}" "/tpl/${SRC}" -o "/tmp/a_${V}.s" 2>"/tmp/e_${V}"; then
    sha=$(sha256sum "/tmp/a_${V}.s" | cut -c1-16)
    echo "SV ${V} rc=0 sha=${sha}"
  else
    ok=0
    echo "SV ${V} rc=1 sha=- ERR=$(tr '\n' ' ' < /tmp/e_${V} | cut -c1-300)"
  fi
done
exit 0
"""

SV_RE = re.compile(r"SV\s+(\S+)\s+rc=(\d+)\s+sha=(\S+)(?:\s+ERR=(.*))?")


def load(feature_id):
    pdir = TEMPLATES / feature_id
    if not pdir.is_dir():
        pdir = Path(feature_id)
    params = json.loads((pdir / "params.json").read_text())
    src = next((c for c in ("template.c", "template.cc", "template.cpp")
                if (pdir / c).is_file()), None)
    if not src:
        sys.exit(f"FAIL: no template.c in {pdir}")
    return pdir, params, src


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--template", required=True)
    ap.add_argument("--image", default=DEFAULT_IMAGE)
    ap.add_argument("--scan-values", default=None,
                    help="comma list overriding params.json scan_values (e.g. a screen-tuned range)")
    args = ap.parse_args()

    pdir, params, src = load(args.template)
    src_text = (pdir / src).read_text()
    fails, warns = [], []

    # ---- (1) schema/sanity ----
    param = params.get("parameter")
    svs = (args.scan_values.split(",") if args.scan_values
           else [str(v) for v in params.get("scan_values", [])])
    fuzzers = params.get("fuzzers", [])
    direction = params.get("expected_direction", "")
    if not param:
        fails.append("params.json missing 'parameter'")
    if len(svs) < 2:
        fails.append("scan_values must have >=2 values (need min!=max for the live check)")
    bad = [f for f in fuzzers if f not in CANON]
    if bad:
        fails.append(f"fuzzers not in canonical set: {bad}")
    m = re.match(r"\s*(\S+)\s*>\s*(\S+)\s*$", direction)
    if not m:
        fails.append(f"expected_direction must be 'WINNER > LOSER', got {direction!r}")
    else:
        w, l = m.group(1), m.group(2)
        # judge_multi allows comma-separated winner/loser fuzzer lists.
        for who, side in (("winner", w), ("loser", l)):
            for f in side.split(","):
                if f and f not in fuzzers:
                    fails.append(f"expected_direction {who} {f!r} not in fuzzers {fuzzers}")
    if param and not re.search(r"\b" + re.escape(param) + r"\b", src_text):
        fails.append(f"parameter macro {param!r} does not appear in {src}")
    elif param and not re.search(r"#\s*if.*\b" + re.escape(param) + r"\b|"
                                 r"#\s*ifndef\s+" + re.escape(param) + r"\b|"
                                 r"#\s*ifdef\s+" + re.escape(param) + r"\b|"
                                 r"defined\s*\(\s*" + re.escape(param) + r"\s*\)",
                                 src_text):
        warns.append(f"{param!r} appears but not in a #if/#ifndef/defined() — "
                     "the live-knob compile check is authoritative")

    if fails:
        _report(False, fails, warns, {})
        sys.exit(1)

    # ---- (2)+(3) compile each scan value, check live ----
    cmd = ["docker", "run", "--rm", "--entrypoint", "bash",
           "-v", f"{pdir.resolve()}:/tpl:ro",
           "-e", f"PARAM={param}", "-e", f"SRC={src}",
           "-e", "VALUES=" + " ".join(svs),
           args.image, "-c", COMPILE_SCRIPT]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        _report(False, ["compile preflight container timed out"], warns, {})
        sys.exit(1)

    shas = {}
    for mm in SV_RE.finditer(p.stdout):
        v, rc, sha, err = mm.group(1), mm.group(2), mm.group(3), mm.group(4)
        if rc != "0":
            fails.append(f"scan_value {param}={v} fails to compile: {err}")
        else:
            shas[v] = sha
    if not shas:
        fails.append("no scan values compiled (image/clang issue?); "
                     f"stdout/stderr: {(p.stdout + p.stderr)[:300]}")

    # live-knob check: min vs max assembly must differ
    if len(shas) >= 2 and not fails:
        lo, hi = svs[0], svs[-1]
        if shas.get(lo) and shas.get(lo) == shas.get(hi):
            fails.append(
                f"DEAD KNOB: assembly identical at {param}={lo} and {param}={hi} "
                f"(sha {shas[lo]}). The -D{param} changed no code — params.json "
                f"'parameter' likely does not match a live #if/#ifndef in {src}.")

    ok = not fails
    _report(ok, fails, warns, shas)
    sys.exit(0 if ok else 1)


def _report(ok, fails, warns, shas):
    print(f"check_template: {'PASS' if ok else 'FAIL'}")
    if shas:
        print("  per-scan-value assembly sha16: " +
              ", ".join(f"{v}={s}" for v, s in shas.items()))
    for w in warns:
        print(f"  WARN  {w}")
    for f in fails:
        print(f"  FAIL  {f}")


if __name__ == "__main__":
    main()
