"""
extract_functions.py — library: per-target function → line-range list.

Runs `llvm-cov export` inside the target's coverage-instrumented Docker image
(`libafl-<target>-cov`) and returns a list of dicts:

    [{"file": <path>, "name": <mangled or demangled name>,
      "start_line": int, "end_line": int}, ...]

Used by tools/study_units.py (`build_function_index`) at `add-canonical` time
to populate `branches.function` with the enclosing function name. Caller is
responsible for demangling (typically via `c++filt` batch) — this module
returns whatever llvm-cov export produces.

Not a CLI — invoke via `import extract_functions; fns = extract_functions.extract("curl")`.
"""

import json
import subprocess

IMAGE_FMT = "libafl-{target}-cov"

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
    """Return [{file, name, start_line, end_line}, ...] for the target."""
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
            # region tuple: (start_line, start_col, end_line, end_col, count, file_id, ...)
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
