#!/usr/bin/env python3
"""
extract_functions.py — Produce per-target function→line-range sidecar.

Runs `llvm-cov export` inside the target's coverage-instrumented Docker image,
extracts per-function primary-file line ranges, and writes:

    data/functions/<target>.json

Each entry: {"file": <path>, "name": <func>, "start_line": int, "end_line": int}

Used by tools/cluster.py to group sub-clusters by enclosing C function instead
of by line-proximity gap.

Usage:
    python3 tools/extract_functions.py --target lcms
    python3 tools/extract_functions.py --target lcms --output data/functions/lcms.json
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
IMAGE_FMT = "blocker-{target}-cov"

DOCKER_SCRIPT = r"""
set -e
mkdir -p /tmp/seeds
printf '\x00' > /tmp/seeds/empty
export LLVM_PROFILE_FILE=/tmp/x.profraw
timeout 15 "$FUZZ_BIN" /tmp/seeds/empty >/dev/null 2>&1 || true
llvm-profdata-18 merge -sparse /tmp/x.profraw -o /tmp/x.profdata
llvm-cov-18 export "$FUZZ_BIN" -instr-profile=/tmp/x.profdata \
    --format=text --skip-expansions
"""


def extract(target: str) -> list[dict]:
    image = IMAGE_FMT.format(target=target)
    result = subprocess.run(
        ["docker", "run", "--rm", "--entrypoint=bash", image, "-c", DOCKER_SCRIPT],
        check=True, capture_output=True, text=True, timeout=300,
    )
    data = json.loads(result.stdout)

    fns: list[dict] = []
    for dataset in data.get("data", []):
        for fn in dataset.get("functions", []):
            name = fn.get("name")
            filenames = fn.get("filenames") or []
            regions = fn.get("regions") or []
            if not name or not filenames or not regions:
                continue

            primary = filenames[0]
            primary_regions = [r for r in regions if len(r) >= 6 and r[5] == 0]
            if not primary_regions:
                continue

            start_line = min(r[0] for r in primary_regions)
            end_line = max(r[2] for r in primary_regions)
            fns.append({
                "file": primary,
                "name": name,
                "start_line": int(start_line),
                "end_line": int(end_line),
            })

    fns.sort(key=lambda f: (f["file"], f["start_line"]))
    return fns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--output",
                    help="Default: data/functions/<target>.json")
    args = ap.parse_args()

    out = Path(args.output) if args.output else REPO / "data" / "functions" / f"{args.target}.json"
    out.parent.mkdir(parents=True, exist_ok=True)

    fns = extract(args.target)
    out.write_text(json.dumps(fns, indent=2))

    files_seen = {f["file"] for f in fns}
    print(f"{args.target}: {len(fns)} functions across {len(files_seen)} files → {out}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
