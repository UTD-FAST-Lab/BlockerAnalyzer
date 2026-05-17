"""
evidence_prompt.py — per-branch structured prompt for
feature-hypothesis-generator.

Assembles the 9-section prompt from DB rows (`branches`,
`study_subjects`, `subject_branches`, `resolving_seeds`,
`blocking_seeds`) plus on-disk artifacts (`db/per_role_coverage/*`,
`db/callers_index/*`, `fuzzer_mechanism_library.md`).

Wired into the `study_units.py` CLI via `register_subparser(sub)` so
the entry point stays `python3 tools/study_units.py evidence-per-branch`.

Section emission order (see CLAUDE.md for the full layout):
  1. BLOCKER
  2. TRIAL VECTOR
  3. DECISIVE PAIRS
  4. SOURCE CONTEXT (per-role coverage overlay + 1-hop caller + call chain)
  5. HIT-COUNT DIVERGENCE
  6. DIVERGENT BRANCHES (on call chain)
  7. BRANCH SEEDS (shared across decisive pairs) + BYTE DIFF
  8. MECHANISM CONTEXT
  9. TASK + OPTIONAL DEEP-DIVE QUERIES

Pure DB+files reader; no Docker, no schema mutation. Functions in
`seed_utils` cover hex/byte helpers shared with `db_query.py`.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = TOOLS_DIR.parent

DEFAULT_QUEUE_BASE      = PROJECT_DIR / "out"
DEFAULT_MECHANISM_LIB   = PROJECT_DIR / "fuzzer_mechanism_library.md"
DEFAULT_PER_ROLE_CACHE  = PROJECT_DIR / "db" / "per_role_coverage"
DEFAULT_CALLERS_INDEX   = PROJECT_DIR / "db" / "callers_index"

CANONICAL_FUZZERS_LIST = ["naive", "cmplog", "value_profile", "value_profile_cmplog"]

sys.path.insert(0, str(TOOLS_DIR))
from seed_utils import parse_count, format_seed_block, byte_diff_section  # noqa: E402


# ── mechanism library splice + source-window fallback ─────────────────────

def _mechanism_for(library_path, fuzzer):
    """Pull the fuzzer's section paragraph from the mechanism library.

    Section header may include a parenthetical, e.g.
    `## value_profile (CMP_MAP gradient feedback)`.
    """
    if not library_path.is_file():
        return f"[mechanism library not found at {library_path}]"
    text = library_path.read_text()
    pattern = re.compile(rf"^## {re.escape(fuzzer)}(?:\s|\(|$)", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return f"[no entry for '{fuzzer}' in {library_path.name}]"
    body_start = text.find("\n", match.start()) + 1
    next_section = re.search(r"^## ", text[body_start:], re.MULTILINE)
    body_end = body_start + next_section.start() if next_section else len(text)
    return text[body_start:body_end].strip()


def _read_source_window(target, container_path, line, n_lines):
    """Read ±n_lines around `line` from `container_path` inside libafl-<target>-cov."""
    lo = max(1, line - n_lines)
    hi = line + n_lines
    image = f"libafl-{target}-cov"
    try:
        proc = subprocess.run(
            ["docker", "run", "--rm", "--entrypoint", "sed",
             image, "-n", f"{lo},{hi}p", container_path],
            capture_output=True, text=True, timeout=30,
        )
        if proc.returncode != 0:
            return f"[failed to read {container_path} from {image}: {proc.stderr.strip()}]"
        return proc.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        return f"[failed to read {container_path}: {exc}]"


# ── per-role coverage overlay ──────────────────────────────────────────────
#
# When per_role_coverage.py has generated W (winner-resolving) and L
# (loser-blocking) llvm-cov reports for a branch, we annotate the enclosing
# function (and 1-hop callers in the same file) with per-line hit-diff
# markers — [W] winners-only, [L] losers-only, [B] both, [ ] not hit.

_COV_LINE_RE = re.compile(r"^\s*(\d+)\|\s*([0-9.,kMG]+|)\s*\|(.*)$")
_COV_FILE_HEADER_RE = re.compile(r"^(/\S+\.\w+):$")
_COV_BRANCH_RE = re.compile(
    r"\|\s*Branch \((\d+):(\d+)\):\s*\[True:\s*([^,]+),\s*False:\s*([^\]]+)\]"
)
_FN_INDEX_CACHE = {}
_CALLERS_INDEX_CACHE = {}


def _function_index_cached(target):
    if target in _FN_INDEX_CACHE:
        return _FN_INDEX_CACHE[target]
    # Late import to avoid circular dep: study_units.main() imports this module
    # to register the subparser, so importing study_units at module load time
    # would re-enter. Importing inside the function defers until first use.
    from study_units import build_function_index
    idx = build_function_index(target)
    _FN_INDEX_CACHE[target] = idx
    return idx


def _callers_index_cached(target, cache_dir):
    if target in _CALLERS_INDEX_CACHE:
        return _CALLERS_INDEX_CACHE[target]
    p = cache_dir / f"{target}.json"
    if not p.is_file():
        _CALLERS_INDEX_CACHE[target] = {}
        return {}
    data = json.loads(p.read_text())
    _CALLERS_INDEX_CACHE[target] = data.get("callers", {})
    return _CALLERS_INDEX_CACHE[target]


def _parse_cov_report(path, default_file=None):
    """Parse an llvm-cov show text report — single-file OR multi-file.

    Returns:
      file_counts  = {file_path: {src_line: count_or_None}}
      file_sources = {file_path: {src_line: source_text}}

    For single-file dumps (no `/path:` headers), default_file is used as
    the key; if not provided, '' is used as the key.
    """
    file_counts, file_sources = {}, {}
    if not path.is_file():
        return file_counts, file_sources

    current = default_file or ""
    file_counts.setdefault(current, {})
    file_sources.setdefault(current, {})
    saw_header = False

    for raw in path.read_text(errors="replace").splitlines():
        hm = _COV_FILE_HEADER_RE.match(raw)
        if hm:
            current = hm.group(1)
            file_counts.setdefault(current, {})
            file_sources.setdefault(current, {})
            saw_header = True
            continue
        m = _COV_LINE_RE.match(raw)
        if not m:
            continue
        ln = int(m.group(1))
        file_counts[current][ln]  = parse_count(m.group(2))
        file_sources[current][ln] = m.group(3)

    if not saw_header and default_file is None and not file_counts.get(""):
        file_counts.pop("", None)
        file_sources.pop("", None)
    return file_counts, file_sources


def _marker(w_hit, l_hit):
    if w_hit and l_hit:
        return "B"
    if w_hit:
        return "W"
    if l_hit:
        return "L"
    return " "


def _walk_call_chain(target, enclosing_name, callers_index_dir,
                     max_depth, per_hop_cap):
    """BFS up the callers index from `enclosing_name` for depths 2..max_depth.

    Returns ordered list of (depth, caller_func, caller_file, c_start,
    c_end, called_func, call_line). Depth 1 is rendered separately with
    full overlay; this function intentionally skips depth-1 entries.
    Cycles avoided via visited set.
    """
    idx = _callers_index_cached(target, callers_index_dir)
    visited = {enclosing_name}
    chain = []
    frontier = [(enclosing_name, 1)]
    while frontier and len(chain) < max_depth * per_hop_cap * 4:
        next_frontier = []
        for func, depth in frontier:
            callers = idx.get(func, [])[:per_hop_cap]
            for c in callers:
                cn = c.get("caller")
                if not cn or cn in visited:
                    continue
                visited.add(cn)
                next_depth = depth + 1
                if next_depth > max_depth:
                    continue
                if next_depth >= 2:
                    chain.append((next_depth, cn, c["file"],
                                  c["caller_start"], c["caller_end"],
                                  func, c["line"]))
                next_frontier.append((cn, next_depth))
        frontier = next_frontier
    chain.sort(key=lambda t: (t[0], t[2], t[1]))
    return chain


def _find_callers_from_index(target, enclosing_name, file_counts,
                             callers_index_dir):
    """Cross-file 1-hop callers from the callers index, filtered to those
    whose call_site_line fired in the W report.

    Returns [(caller_name, call_file, call_line, c_start, c_end), ...]
    ordered by W hit count at the call site (most-fired first).
    """
    idx = _callers_index_cached(target, callers_index_dir)
    candidates = idx.get(enclosing_name, [])
    out = []
    seen = set()
    for c in candidates:
        f = c.get("file")
        ln = c.get("line")
        caller_func = c.get("caller")
        if f is None or ln is None or caller_func is None:
            continue
        file_hits = file_counts.get(f)
        if file_hits is None:
            continue
        hit = file_hits.get(ln) or 0
        if hit <= 0:
            continue
        key = (caller_func, f, c["caller_start"], c["caller_end"])
        if key in seen:
            continue
        seen.add(key)
        out.append((caller_func, f, ln, c["caller_start"], c["caller_end"], hit))
    out.sort(key=lambda x: (-x[5], x[1], x[2]))
    return [(n, f, ln, s, e) for (n, f, ln, s, e, _h) in out]


def _annotate_range(start, end, w_counts, w_sources, l_counts, l_sources,
                    marker_line, marker_label="BLOCKER"):
    """Format a [start, end] line range with [W]/[L]/[B]/[ ] markers."""
    lines = []
    for ln in range(start, end + 1):
        src = w_sources.get(ln, l_sources.get(ln, ""))
        wc = w_counts.get(ln)
        lc = l_counts.get(ln)
        if wc is None and lc is None:
            mk = " "
        else:
            mk = _marker(bool(wc), bool(lc))
        tag = f" <-- {marker_label}" if ln == marker_line else ""
        lines.append(f"[{mk}] {ln:>5}  {src}{tag}")
    return "\n".join(lines)


def _load_per_role_reports(target, branch_id, file_path, cache_dir):
    """Read W and L cov reports from cache. Returns:
      (ok, w_file_counts, w_file_sources, l_file_counts, l_file_sources)
    ok=False if reports missing or empty (caller should fall back).
    """
    base = cache_dir / target / str(branch_id)
    w_path = base / "W" / "branch_coverage_show.txt"
    l_path = base / "L" / "branch_coverage_show.txt"
    if not (w_path.is_file() and l_path.is_file()):
        return False, {}, {}, {}, {}
    w_file_counts, w_file_sources = _parse_cov_report(w_path, default_file=file_path)
    l_file_counts, l_file_sources = _parse_cov_report(l_path, default_file=file_path)
    if not w_file_sources or not l_file_sources:
        return False, {}, {}, {}, {}
    return True, w_file_counts, w_file_sources, l_file_counts, l_file_sources


def _function_hit_divergence_section(fn_index, w_file_counts, l_file_counts,
                                     enclosing_name, max_rows=15, min_ratio=3.0):
    """W vs L invocation count per function (entry-line count as proxy)."""
    rows = []
    for file, fns in fn_index.items():
        wcs = w_file_counts.get(file, {})
        lcs = l_file_counts.get(file, {})
        if not wcs and not lcs:
            continue
        for start, end, name in fns:
            entry_w, entry_l = None, None
            for ln in range(start, end + 1):
                wc, lc = wcs.get(ln), lcs.get(ln)
                if wc is None and lc is None:
                    continue
                entry_w = wc or 0
                entry_l = lc or 0
                break
            if entry_w is None:
                continue
            if entry_w == 0 and entry_l == 0:
                continue
            if entry_w > 0 and entry_l > 0:
                ratio = max(entry_w, entry_l) / min(entry_w, entry_l)
                if ratio < min_ratio:
                    continue
            rows.append((file, start, end, name, entry_w, entry_l))

    if not rows:
        return ("==== HIT-COUNT DIVERGENCE (per function) ====\n"
                "[no significant per-function W/L divergence in the cov dump]\n")

    rows.sort(key=lambda r: -abs(r[4] - r[5]))

    lines = [
        "==== HIT-COUNT DIVERGENCE (per function in cov dump) ====",
        f"Functions where W and L invocation counts differ by >={min_ratio}x "
        "or one is zero. 'Entry-line count' = first executable line in the "
        "function body — a proxy for invocation count.",
        "",
        f"{'W hits':>8}  {'L hits':>8}  function  (file:start-end)",
    ]
    for file, start, end, name, w, l in rows[:max_rows]:
        marker = "  <-- enclosing" if name == enclosing_name else ""
        lines.append(f"{w:>8d}  {l:>8d}  {name}  ({file}:{start}-{end}){marker}")
    if len(rows) > max_rows:
        lines.append(f"... ({len(rows) - max_rows} more divergent functions)")
    return "\n".join(lines)


def _parse_branch_counts(report_path):
    """Returns {file: {(line, col): (T_count, F_count)}} from cov show text."""
    out = {}
    if not report_path.is_file():
        return out
    current_file = None
    cur = None
    text = report_path.read_text(errors="replace")
    for raw in text.splitlines():
        hm = _COV_FILE_HEADER_RE.match(raw)
        if hm:
            current_file = hm.group(1)
            cur = out.setdefault(current_file, {})
            continue
        if cur is None:
            cur = out.setdefault("", {})
        m = _COV_BRANCH_RE.search(raw)
        if m:
            ln, col = int(m.group(1)), int(m.group(2))
            t = parse_count(m.group(3))
            f = parse_count(m.group(4))
            cur[(ln, col)] = (t or 0, f or 0)
    if "" in out and not out[""]:
        out.pop("")
    return out


def _branch_divergence_section(target, branch_id, cache_dir, fn_index,
                               enclosing_name, blocker_line, chain,
                               file_path, source_map,
                               default_file_for_branch_parse):
    """Emit DIVERGENT BRANCHES with rough execution order."""
    base = cache_dir / target / str(branch_id)
    w_branches = _parse_branch_counts(base / "W" / "branch_coverage_show.txt")
    l_branches = _parse_branch_counts(base / "L" / "branch_coverage_show.txt")
    if not w_branches and not l_branches:
        return None

    if "" in w_branches and default_file_for_branch_parse:
        w_branches.setdefault(default_file_for_branch_parse, {}).update(w_branches.pop(""))
    if "" in l_branches and default_file_for_branch_parse:
        l_branches.setdefault(default_file_for_branch_parse, {}).update(l_branches.pop(""))

    files = set(w_branches) | set(l_branches)
    divergent = []
    for f in files:
        w_b = w_branches.get(f, {})
        l_b = l_branches.get(f, {})
        keys = set(w_b) | set(l_b)
        for (ln, col) in keys:
            w_t, w_f = w_b.get((ln, col), (0, 0))
            l_t, l_f = l_b.get((ln, col), (0, 0))
            w_dir = ("T" if w_t > 0 else "") + ("F" if w_f > 0 else "")
            l_dir = ("T" if l_t > 0 else "") + ("F" if l_f > 0 else "")
            if w_dir == l_dir and w_t == l_t and w_f == l_f:
                continue
            if w_dir == l_dir == "":
                continue
            if w_dir == l_dir:
                tot_w = w_t + w_f
                tot_l = l_t + l_f
                if tot_w and tot_l and max(tot_w, tot_l) / min(tot_w, tot_l) < 2.0:
                    continue
            file_fns = fn_index.get(f, [])
            cands = [t for t in file_fns if t[0] <= ln <= t[1]]
            if not cands:
                continue
            fn = min(cands, key=lambda t: (t[1] - t[0], t[0]))
            divergent.append({
                "file": f, "fn_start": fn[0], "fn_end": fn[1],
                "fn_name": fn[2], "line": ln, "col": col,
                "w_t": w_t, "w_f": w_f, "l_t": l_t, "l_f": l_f,
            })

    if not divergent:
        return ("==== DIVERGENT BRANCHES (on call chain, rough order) ====\n"
                "[no branches with W/L direction or count divergence in the "
                "cov dump — execution split is at the blocker itself, or in "
                "code outside the dumped files]\n")

    depth_by_fn = {enclosing_name: 1}
    for depth, cn, cf, cs, ce, called, call_ln in chain:
        depth_by_fn.setdefault(cn, depth)

    on_chain = [b for b in divergent if b["fn_name"] in depth_by_fn]
    off_chain = [b for b in divergent if b["fn_name"] not in depth_by_fn]

    on_chain.sort(key=lambda b: (-depth_by_fn[b["fn_name"]], b["line"]))

    lines = [
        "==== DIVERGENT BRANCHES (on call chain, rough order) ====",
        "Branches with W/L divergence in functions on the call chain "
        "(enclosing + 1-hop + chain). Rough execution order: outermost "
        "caller → blocker. Caveats: this assumes no recursion; loops/gotos "
        "break source-line order locally; off-chain divergent branches "
        "(L explored code W didn't, or vice versa) are summarized below "
        "the chain section — see HIT-COUNT DIVERGENCE for the function-level "
        "view.",
        "",
        f"{'depth':>5}  {'src':>6}  W(T/F)  L(T/F)  source",
    ]
    if not on_chain:
        lines.append("  (no divergent branches in chain functions; "
                     "the split is off-chain)")
    cur_fn = None
    for b in on_chain:
        d = depth_by_fn[b["fn_name"]]
        if b["fn_name"] != cur_fn:
            cur_fn = b["fn_name"]
            lines.append(f"--- d={d}  {cur_fn}  ({b['file']}:{b['fn_start']}-{b['fn_end']}) ---")
        marker = "  <-- BLOCKER" if b["line"] == blocker_line and b["file"] == file_path else ""
        src_text = source_map.get(b["file"], {}).get(b["line"], "").strip()
        if len(src_text) > 60:
            src_text = src_text[:57] + "..."
        lines.append(
            f"  d={d:<2}  L{b['line']:>4}  "
            f"T={b['w_t']} F={b['w_f']}  T={b['l_t']} F={b['l_f']}  "
            f"{src_text}{marker}"
        )

    if off_chain:
        off_fns = sorted({(b["fn_name"], b["file"]) for b in off_chain})
        lines.append("")
        lines.append(f"[off-chain: {len(off_chain)} additional divergent "
                     f"branches across {len(off_fns)} functions "
                     "(see HIT-COUNT DIVERGENCE for which functions)]")
    return "\n".join(lines)


def _build_source_context_overlay(target, file_path, blocker_line,
                                  enclosing_name, branch_id,
                                  cache_dir, trace_callers, caller_context,
                                  full_body_threshold,
                                  fallback_source_lines,
                                  callers_index_dir,
                                  call_chain_depth, call_chain_per_hop):
    """Return the full SOURCE CONTEXT body. Falls back to plain ±N window if
    per-role reports are missing or unparseable."""
    ok, w_file_counts, w_file_sources, l_file_counts, l_file_sources = \
        _load_per_role_reports(target, branch_id, file_path, cache_dir)
    if not ok:
        body = _read_source_window(target, file_path, blocker_line,
                                   fallback_source_lines)
        return ("[per-role coverage reports missing/empty — fell back to ±"
                f"{fallback_source_lines} source window]\n"
                f"# {file_path} (lines "
                f"{max(1, blocker_line - fallback_source_lines)}-"
                f"{blocker_line + fallback_source_lines}, "
                f"blocker at line {blocker_line})\n" + body)
    w_counts  = w_file_counts.get(file_path, {})
    w_sources = w_file_sources.get(file_path, {})
    l_counts  = l_file_counts.get(file_path, {})
    l_sources = l_file_sources.get(file_path, {})

    fn_index = _function_index_cached(target)
    file_fns = fn_index.get(file_path, [])
    encl = [t for t in file_fns
            if t[0] <= blocker_line <= t[1] and t[2] == enclosing_name]
    if not encl:
        cands = [t for t in file_fns if t[0] <= blocker_line <= t[1]]
        encl = [min(cands, key=lambda t: (t[1] - t[0], t[0]))] if cands else []
    if not encl:
        lo = max(1, blocker_line - fallback_source_lines)
        hi = blocker_line + fallback_source_lines
        return (
            "Legend: [W] winner-resolving only  [L] loser-blocking only  "
            "[B] both  [ ] not hit\n"
            f"# {file_path} (lines {lo}-{hi}, blocker at {blocker_line}, "
            "function range unknown)\n"
            + _annotate_range(lo, hi, w_counts, w_sources, l_counts, l_sources,
                              blocker_line)
        )

    e_start, e_end, e_name = encl[0]
    e_disp_start = max(1, e_start - 2)

    parts = [
        "Legend: [W] winner-resolving only  [L] loser-blocking only  "
        "[B] both  [ ] not hit",
        "Source: db/per_role_coverage/{}/{}/{{W,L}}/branch_coverage_show.txt"
            .format(target, branch_id),
        "",
        f"--- Enclosing function: {e_name} ({file_path}:{e_start}-{e_end}) ---",
        _annotate_range(e_disp_start, e_end, w_counts, w_sources,
                        l_counts, l_sources, blocker_line),
    ]

    callers = _find_callers_from_index(target, e_name, w_file_counts,
                                       callers_index_dir)
    for c_name, c_file, call_ln, c_start, c_end in callers[:trace_callers]:
        body_size = c_end - c_start + 1
        if body_size <= full_body_threshold:
            lo, hi = c_start, c_end
            note = "(full body — short)"
        else:
            lo = max(c_start, call_ln - caller_context)
            hi = min(c_end,  call_ln + caller_context)
            note = f"(±{caller_context} around call site)"
        c_w_counts  = w_file_counts.get(c_file, {})
        c_w_sources = w_file_sources.get(c_file, {})
        c_l_counts  = l_file_counts.get(c_file, {})
        c_l_sources = l_file_sources.get(c_file, {})
        parts.append("")
        parts.append(f"--- Caller (1 hop): {c_name} "
                     f"({c_file}:{c_start}-{c_end}, "
                     f"calls {e_name} at line {call_ln}) {note} ---")
        parts.append(_annotate_range(lo, hi, c_w_counts, c_w_sources,
                                     c_l_counts, c_l_sources, call_ln,
                                     marker_label="CALL"))

    if not callers:
        idx_present = (callers_index_dir / f"{target}.json").is_file()
        parts.append("")
        if idx_present:
            parts.append(f"--- No 1-hop callers of {e_name} fired in W "
                         "(callers index present but none matched) ---")
        else:
            parts.append(f"--- No callers index for {target} — run "
                         f"tools/callers_index.py build --target {target} ---")

    if call_chain_depth >= 2:
        chain = _walk_call_chain(target, e_name, callers_index_dir,
                                 call_chain_depth, call_chain_per_hop)
        if chain:
            parts.append("")
            parts.append(f"--- Call chain (depth 2..{call_chain_depth}, "
                         "signatures only; depth 1 detailed above) ---")
            for depth, cn, cf, cs, ce, called, call_ln in chain:
                parts.append(f"hop {depth}  {cn}  ({cf}:{cs}-{ce}, "
                             f"calls {called} at line {call_ln})")

    return "\n".join(parts)


# ── command + subparser registration ──────────────────────────────────────

def cmd_evidence_per_branch(args):
    """Per-branch structured prompt for feature-hypothesis-generator.

    Keyed on (target, branch_id). Collapses ALL canonical pairs satisfying
    the >=8/>=8 rule into a single prompt; hypothesis + verification scoped
    to those decisive pairs. Other canonical fuzzers appear as REFERENCE
    context only.
    """
    # Late import: study_units.main() calls register_subparser(...) here,
    # so importing study_units at module-load would be circular.
    from study_units import open_db

    conn = open_db(args.db)

    br = conn.execute(
        "SELECT target, file, function, line, col, blocked_side, source_line "
        "FROM branches WHERE branch_id=?",
        (args.branch_id,),
    ).fetchone()
    if br is None:
        print(f"no branch with id={args.branch_id}", file=sys.stderr)
        sys.exit(2)
    target, file_path, function, line, col, blocked_side, source_line = br
    if args.target and target != args.target:
        print(f"branch {args.branch_id} is in target={target}, not {args.target}",
              file=sys.stderr)
        sys.exit(2)

    where_extra = " AND s.admissible = 1" if args.admissible_only else ""
    decisive_rows = conn.execute(
        f"""SELECT s.subject_id, s.A, s.B, s.delta_technique, s.admissible,
                   sb.n_A_resolved, sb.n_A_blocked, sb.n_A_unreached,
                   sb.n_B_resolved, sb.n_B_blocked, sb.n_B_unreached,
                   sb.avg_dur_A, sb.avg_dur_B, sb.avg_hits_A, sb.avg_hits_B,
                   sb.prob_div, sb.dur_div, sb.hit_div,
                   s.delta_auc, s.p_auc, s.delta_final, s.p_final
            FROM subject_branches sb
            JOIN study_subjects s USING(subject_id)
            WHERE sb.branch_id = ?
              AND ((sb.n_A_resolved >= ? AND sb.n_B_blocked >= ?)
                OR (sb.n_B_resolved >= ? AND sb.n_A_blocked >= ?))
                  {where_extra}
            ORDER BY ABS(IFNULL(sb.prob_div,0)) DESC, s.subject_id""",
        (args.branch_id,
         args.winner_threshold, args.loser_threshold,
         args.winner_threshold, args.loser_threshold),
    ).fetchall()
    if not decisive_rows:
        print(
            f"no decisive canonical pair at (target={target}, branch={args.branch_id}) "
            f"under >={args.winner_threshold}/>={args.loser_threshold} rule "
            f"(admissible_only={args.admissible_only})",
            file=sys.stderr,
        )
        sys.exit(2)

    pairs = []
    for d in decisive_rows:
        (sid, A, B, delta, adm,
         A_res, A_blk, A_unr, B_res, B_blk, B_unr,
         dur_A, dur_B, hits_A, hits_B,
         prob_div, dur_div, hit_div,
         dauc, pauc, dfin, pfin) = d
        if A_res >= args.winner_threshold and B_blk >= args.loser_threshold:
            direction, winner, loser = "A>B", A, B
            w_res, w_blk, w_unr = A_res, A_blk, A_unr
            l_res, l_blk, l_unr = B_res, B_blk, B_unr
            w_dur, l_dur = dur_A, dur_B
            w_hits, l_hits = hits_A, hits_B
        else:
            direction, winner, loser = "B>A", B, A
            w_res, w_blk, w_unr = B_res, B_blk, B_unr
            l_res, l_blk, l_unr = A_res, A_blk, A_unr
            w_dur, l_dur = dur_B, dur_A
            w_hits, l_hits = hits_B, hits_A
        pairs.append({
            "subject_id": sid, "A": A, "B": B, "delta": delta, "admissible": adm,
            "direction": direction, "winner": winner, "loser": loser,
            "w_res": w_res, "w_blk": w_blk, "w_unr": w_unr,
            "l_res": l_res, "l_blk": l_blk, "l_unr": l_unr,
            "w_dur": w_dur, "l_dur": l_dur,
            "w_hits": w_hits, "l_hits": l_hits,
            "prob_div": abs(prob_div) if prob_div is not None else 0.0,
            "dur_div":  abs(dur_div)  if dur_div  is not None else 0.0,
            "hit_div":  abs(hit_div)  if hit_div  is not None else 0.0,
            "delta_auc": dauc, "p_auc": pauc,
            "delta_final": dfin, "p_final": pfin,
        })

    involved_fuzzers = sorted({fz for p in pairs for fz in (p["winner"], p["loser"])})
    reference_fuzzers = [fz for fz in CANONICAL_FUZZERS_LIST if fz not in involved_fuzzers]

    # Per-fuzzer counts derived from subject_branches.
    counts = {}
    for fz, R, B_, U in conn.execute(
        """
        SELECT s.A, sb.n_A_resolved, sb.n_A_blocked, sb.n_A_unreached
          FROM subject_branches sb
          JOIN study_subjects s ON sb.subject_id = s.subject_id
         WHERE sb.branch_id = ?
        UNION
        SELECT s.B, sb.n_B_resolved, sb.n_B_blocked, sb.n_B_unreached
          FROM subject_branches sb
          JOIN study_subjects s ON sb.subject_id = s.subject_id
         WHERE sb.branch_id = ?
        """,
        (args.branch_id, args.branch_id),
    ).fetchall():
        counts[fz] = (R, B_, U)

    # Seeds are stored per-branch by seed_bisect (one (fuzzer, trial) per
    # direction via lex-min). We emit one shared block per direction;
    # each seed line carries its actual (fuzzer, trial).
    winner_seeds = conn.execute(
        """SELECT fuzzer, trial, seed_id, mutation_op, discovery_time_s
           FROM resolving_seeds
           WHERE branch_id=?
           ORDER BY discovery_time_s ASC, seed_id ASC LIMIT ?""",
        (args.branch_id, args.seeds_per_side),
    ).fetchall()
    loser_seeds = conn.execute(
        """SELECT fuzzer, trial, seed_id, mutation_op, discovery_time_s
           FROM blocking_seeds
           WHERE branch_id=?
           ORDER BY discovery_time_s ASC, seed_id ASC LIMIT ?""",
        (args.branch_id, args.seeds_per_side),
    ).fetchall()
    # Unlimited seed lists for the BYTE DIFF — statistical signal benefits
    # from more samples than the 5 shown in the hex dump.
    winner_seeds_all = conn.execute(
        """SELECT fuzzer, trial, seed_id, mutation_op, discovery_time_s
           FROM resolving_seeds
           WHERE branch_id=?
           ORDER BY discovery_time_s ASC, seed_id ASC""",
        (args.branch_id,),
    ).fetchall()
    loser_seeds_all = conn.execute(
        """SELECT fuzzer, trial, seed_id, mutation_op, discovery_time_s
           FROM blocking_seeds
           WHERE branch_id=?
           ORDER BY discovery_time_s ASC, seed_id ASC""",
        (args.branch_id,),
    ).fetchall()

    conn.close()

    library_path = Path(args.mechanism_library)
    mechanisms = {fz: _mechanism_for(library_path, fz) for fz in involved_fuzzers}
    queue_base = Path(args.queue_base)
    source_overlay = _build_source_context_overlay(
        target, file_path, line, function, args.branch_id,
        cache_dir=Path(args.per_role_cache),
        trace_callers=args.trace_callers,
        caller_context=args.caller_context,
        full_body_threshold=args.full_body_threshold,
        fallback_source_lines=args.source_lines,
        callers_index_dir=Path(args.callers_index),
        call_chain_depth=args.call_chain_depth,
        call_chain_per_hop=args.call_chain_per_hop,
    )

    side_b_label = blocked_side
    side_a_label = "F" if blocked_side == "T" else "T"
    side_a_branch = "false branch" if side_a_label == "F" else "true branch"
    side_b_branch = "false branch" if side_b_label == "F" else "true branch"

    out = []
    out.append("==== BLOCKER ====")
    out.append(f"Target: {target}")
    out.append(f"Branch ID: {args.branch_id}")
    out.append(f"Location: {file_path}:{line}:{col}")
    out.append(f"Enclosing function: {function}")
    out.append(f"Source line: {source_line}")
    out.append(f"Globally blocked side: {blocked_side}  ({side_b_branch})")
    out.append("")

    out.append("==== TRIAL VECTOR (per fuzzer, n=10 trials) ====")
    out.append(f"{'fuzzer':<24} {'resolved':>9} {'blocked':>8} {'unreached':>10}  role")
    for fz in CANONICAL_FUZZERS_LIST:
        c = counts.get(fz)
        r_, b_, u_ = (c if c else ("?", "?", "?"))
        roles = []
        for p in pairs:
            if p["winner"] == fz:
                roles.append(f"winner ({p['delta']} vs {p['loser']})")
            if p["loser"] == fz:
                roles.append(f"loser ({p['delta']} vs {p['winner']})")
        role_str = "; ".join(roles) if roles else "REFERENCE"
        out.append(f"{fz:<24} {str(r_):>9} {str(b_):>8} {str(u_):>10}  {role_str}")
    out.append("")
    out.append(f"INVOLVED fuzzers (synthetic-verification scope): {involved_fuzzers}")
    out.append(f"REFERENCE fuzzers (auxiliary context only):     {reference_fuzzers}")
    out.append("")

    out.append(f"==== DECISIVE PAIRS ({len(pairs)}) ====")
    for i, p in enumerate(pairs, 1):
        adm_tag = "admissible" if p["admissible"] else "NOT admissible"
        out.append(f"--- Pair {i}: {p['winner']} > {p['loser']}  [delta: {p['delta']}] ---")
        out.append(f"  subject {p['subject_id']}  ({p['A']} vs {p['B']}, {adm_tag})")
        out.append(f"  winner: resolved={p['w_res']}/10  blocked={p['w_blk']}  unreached={p['w_unr']}")
        out.append(f"  loser:  resolved={p['l_res']}/10  blocked={p['l_blk']}  unreached={p['l_unr']}")
        if p["w_dur"] is not None and p["l_dur"] is not None:
            out.append(f"  avg duration blocked: winner={p['w_dur']:.2f}h  loser={p['l_dur']:.2f}h")
        if p["w_hits"] is not None and p["l_hits"] is not None:
            out.append(f"  avg hitcount on branch: winner={p['w_hits']:.0f}  loser={p['l_hits']:.0f}")
        out.append(f"  prob_div={p['prob_div']:.2f}  dur_div={p['dur_div']:.2f}h  hit_div={p['hit_div']:.0f}")
        out.append(f"  subject-level: delta_AUC={p['delta_auc']}  p_AUC={p['p_auc']}  "
                   f"delta_Final={p['delta_final']}  p_final={p['p_final']}")
    out.append("")

    out.append("==== SOURCE CONTEXT (per-role coverage overlay) ====")
    out.append(source_overlay)
    out.append("")

    # Sections 5 + 6: re-use the per-role cov data.
    ok2, w_fc, w_fs, l_fc, l_fs = _load_per_role_reports(
        target, args.branch_id, file_path, Path(args.per_role_cache),
    )
    if ok2:
        fn_idx_full = _function_index_cached(target)
        out.append(_function_hit_divergence_section(
            fn_idx_full, w_fc, l_fc, function,
            max_rows=args.hit_divergence_rows,
            min_ratio=args.hit_divergence_min_ratio,
        ))
        out.append("")
        chain_for_order = _walk_call_chain(
            target, function, Path(args.callers_index),
            args.call_chain_depth, args.call_chain_per_hop,
        )
        bd = _branch_divergence_section(
            target, args.branch_id, Path(args.per_role_cache),
            fn_idx_full, function, line, chain_for_order,
            file_path, w_fs,
            default_file_for_branch_parse=file_path,
        )
        if bd:
            out.append(bd)
            out.append("")

    out.append("==== BRANCH SEEDS (shared across decisive pairs) ====")
    out.append(
        "Note: seed_bisect picks one (fuzzer, trial) per direction by "
        "lex-min, so the storing fuzzer may differ from a pair's decisive "
        "winner/loser. Each seed below carries its actual (fuzzer, trial); "
        "the bytes exercise the named branch side regardless of provenance."
    )
    out.append("")
    out.append(format_seed_block(
        f"Winner-resolving seeds (take {side_b_branch})",
        winner_seeds, queue_base, target, args.seed_bytes,
    ))
    out.append(format_seed_block(
        f"Loser-blocking seeds (take {side_a_branch})",
        loser_seeds, queue_base, target, args.seed_bytes,
    ))
    out.append("")
    out.append(byte_diff_section(
        winner_seeds_all, loser_seeds_all, queue_base, target, args.seed_bytes,
    ))

    out.append("==== MECHANISM CONTEXT (involved fuzzers only) ====")
    for fz in involved_fuzzers:
        out.append(f"--- {fz} ---")
        out.append(mechanisms.get(fz, f"[no mechanism entry for {fz}]"))
        out.append("")

    out.append("==== TASK ====")
    # Derive the suggested analysis.json output path from the prompt's
    # --output. Agent can override but should default to the sibling file.
    if args.output and args.output != "-":
        suggested_analysis_path = (
            args.output[:-len(".prompt.md")] + ".analysis.json"
            if args.output.endswith(".prompt.md")
            else args.output + ".analysis.json"
        )
    else:
        suggested_analysis_path = "<prompt-path>.analysis.json"

    pair_labels = [f"{p['winner']}>{p['loser']} ({p['delta']})" for p in pairs]
    pair_label_str = ", ".join(pair_labels)

    out.append(
        f"ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against "
        f"templates/. Naming an existing template here anchors the later "
        f"cross-branch classification pass.\n"
    )
    out.append(
        f"WRITE EXACTLY ONE FILE:\n  {suggested_analysis_path}\n\n"
        f"Do NOT produce template.c or params.json — those are the "
        f"deferred verification phase.\n"
    )
    out.append(
        "SCHEMA (every field is mandatory; missing or empty fields = "
        "analysis failure). The example below uses `//` comments for "
        "guidance — REMOVE all `//` lines and inline `//` comments from "
        "your emitted JSON (standard JSON does not allow comments)."
    )
    out.append("")
    schema_lines = [
        "{",
        f'  "branch_id": {args.branch_id},',
        f'  "target": "{target}",',
        '  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",',
        '  "pair_decision": "single_feature",',
        '    // pick EXACTLY ONE of: "single_feature" | "multi_feature"',
        f'    // decisive pairs at this branch: [{pair_label_str}]',
        '  "hypotheses": [',
        '    {',
        '      "covers_pairs": ["cmplog>naive (I2S)"],',
        '        // labels MUST match exactly as in DECISIVE PAIRS (e.g. "cmplog>naive (I2S)")',
        '      "what_input_feature": "concrete description of the bytes/structure required",',
        '      "why_winner_satisfies": "what about the winner inputs meets the requirement",',
        '      "why_loser_doesnt": "what is missing in the loser inputs",',
        '      "mechanism_attribution": "free text — explain which fuzzer technique enables the winner; must agree with claimed_mechanism below"',
        '    }',
        '    // pair_decision="single_feature" => exactly 1 hypothesis whose covers_pairs lists ALL decisive pairs',
        '    // pair_decision="multi_feature"  => 2+ hypotheses, each covers_pairs listing its subset',
        '  ],',
        '  "evidence_trail": [',
        '    {',
        '      "claim": "atomic factual claim (1 sentence)",',
        '      "cited_section": "BLOCKER",',
        '        // pick the canonical short name of the cited section, one of:',
        '        //   BLOCKER | TRIAL VECTOR | DECISIVE PAIRS | SOURCE CONTEXT |',
        '        //   HIT-COUNT DIVERGENCE | DIVERGENT BRANCHES | BRANCH SEEDS |',
        '        //   BYTE DIFF | MECHANISM CONTEXT',
        '        // validator accepts the full section header too (e.g. "BYTE DIFF (W vs L at common offsets)")',
        '      "cited_locator": "offsets 0x06-0x0f | L1701 | seed_id ab12... | etc.",',
        '      "exact_quote": "verbatim substring of the prompt — COPY-PASTE, do not paraphrase"',
        '    }',
        '    // at least ONE entry per hypothesis sub-field (what / why_winner / why_loser / mechanism)',
        '  ],',
        '  "mechanism_consistency_check": {',
        '    "claimed_mechanism": "I2SRandReplace",',
        '      // pick EXACTLY ONE of:',
        '      //   "I2SRandReplace"     (cmplog / vpc input-to-state substitution)',
        '      //   "CMP_MAP gradient"   (vp / vpc Hamming/prefix-distance feedback)',
        '      //   "havoc-only"         (lucky havoc byte mutation, no CMP introspection)',
        '      //   "token-replace"      (TokenInsert/TokenReplace dictionary mutations)',
        '      //   "other"              (anything that does not fit the four above)',
        '    "verified_in_lineage": true,',
        '      // pick true or false',
        f'    "verification_method": "ran `python3 tools/db_query.py lineage --branch {args.branch_id} --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"',
        '    // TODO(i2s-logging-bug): the LibAFL cmplog harness does NOT log',
        '    //   the literal "I2SRandReplace" string into seed metadata. Until',
        '    //   that is fixed, the verification signal is the dash-row floor',
        '    //   (ParentInfo-only entries; SQL NULL mutation_op). Confirmed',
        '    //   2026-05-17: dash rows are exclusive to cmplog/vpc in the',
        '    //   current data (zero occurrences in 6000 naive/vp samples).',
        '    //   When the logging fix lands, revert this rule to require the',
        '    //   literal "I2SRandReplace" name and treat the dash signal as',
        '    //   secondary corroboration.',
        '    // MANDATORY when claimed_mechanism="I2SRandReplace": invoke db_query.py lineage on >=1 winning seed',
        '    //   - if you find at least one I2S-floor row in the ancestor chain (mutation_op = -',
        '    //     for ancestors of a cmplog/vpc-discovered seed): verified_in_lineage=true,',
        '    //     and cite the depth(s) in verification_method.',
        '    //   - if the chain is all-havoc (no dash rows): verified_in_lineage=false; note that',
        '    //     I2S contribution may still exist in the leaked havoc bucket, explain (>=20 chars).',
        '    //   - if you could not run db_query (data missing, etc.): verified_in_lineage=false; explain what blocked you',
        '  },',
        '  "falsifiability": {',
        '    "would_be_refuted_by": "ONE concrete observation that, if true, would kill this hypothesis (something a synthetic experiment could observe, not a story)"',
        '  },',
        '  "weakest_evidence_point": "one sentence naming your single most uncertain claim",',
        '  "confidence": "medium"',
        '    // pick EXACTLY ONE of: "high" | "medium" | "low"',
        "}",
    ]
    out.extend(schema_lines)
    out.append("")
    out.append(
        "RULES:\n"
        " - No reference to templates/ anywhere in your output. Classification is a separate later pass.\n"
        " - Every hypothesis sub-claim must be supported by >=1 evidence_trail entry.\n"
        " - exact_quote must be a LITERAL substring of this prompt — COPY-PASTE, do NOT paraphrase, abbreviate, or summarize. A script (tools/check_analysis.py) will reject quotes that do not appear verbatim (whitespace-tolerant).\n"
        " - cited_section: the validator accepts either the canonical short name (BLOCKER, BYTE DIFF, etc.) or the full section header from the prompt.\n"
        " - claimed_mechanism and mechanism_attribution must agree on the same technique.\n"
        " - When claimed_mechanism = \"I2SRandReplace\": you MUST invoke `python3 tools/db_query.py lineage` on >=1 winning seed BEFORE finalizing the analysis. Record what you observed in verification_method.\n"
    )
    out.append("")
    out.append("DEEP-DIVE QUERIES:")
    out.append(
        f"  python3 tools/db_query.py lineage --branch {args.branch_id} "
        "--role W|L --fuzzer <F> --trial <T> --seed <id>"
    )
    out.append(
        "    MANDATORY when claimed_mechanism=\"I2SRandReplace\" (see RULES). "
        "Optional otherwise. Returns the ancestor chain (mutation ops walked "
        "back from the leaf up to 50 levels). The trailing 'I2S-floor signal' "
        "line summarizes dash rows (mutation_op = -); see "
        "fuzzer_mechanism_library.md cmplog section for the floor interpretation "
        "under the current build."
    )
    out.append(
        f"  python3 tools/db_query.py more-seeds --branch {args.branch_id} "
        "--role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]"
    )
    out.append(
        "    Optional. Additional seeds beyond the 5 shown above "
        "(capped by seed_bisect's max_seeds; default 10 per branch x direction)."
    )

    text = "\n".join(out)
    if args.output == "-":
        sys.stdout.write(text)
    else:
        Path(args.output).write_text(text)
        print(f"wrote evidence prompt to {args.output} ({len(text)} chars)",
              file=sys.stderr)


def register_subparser(sub):
    """Install the `evidence-per-branch` subcommand on the given subparsers."""
    s = sub.add_parser(
        "evidence-per-branch",
        help="emit per-branch structured prompt for feature-hypothesis-generator: "
             "collapses ALL canonical pairs satisfying >=8/>=8 at this branch into "
             "one prompt; reports the full 4-fuzzer trial vector with role tags. "
             "Hypothesis and verification are scoped to decisive pairs only.",
    )
    s.add_argument("--target", required=True,
                   help="target name (sanity-checked against branches.target)")
    s.add_argument("--branch-id", required=True, type=int)
    s.add_argument("--winner-threshold", type=int, default=8,
                   help="winner must have n_resolved >= THIS (default 8)")
    s.add_argument("--loser-threshold", type=int, default=8,
                   help="loser must have n_blocked >= THIS (default 8)")
    s.add_argument("--admissible-only", action="store_true", default=True,
                   help="restrict to admissible subjects (default ON)")
    s.add_argument("--no-admissible-only", action="store_false",
                   dest="admissible_only",
                   help="include all subjects regardless of admissibility")
    s.add_argument("--mechanism-library", default=str(DEFAULT_MECHANISM_LIB),
                   help=f"default {DEFAULT_MECHANISM_LIB}")
    s.add_argument("--queue-base", default=str(DEFAULT_QUEUE_BASE),
                   help=f"default {DEFAULT_QUEUE_BASE}")
    s.add_argument("--source-lines", type=int, default=30,
                   help="fallback ±N source window when per-role coverage is "
                        "absent (default 30)")
    s.add_argument("--per-role-cache", default=str(DEFAULT_PER_ROLE_CACHE),
                   help=f"cache root written by tools/per_role_coverage.py "
                        f"(default {DEFAULT_PER_ROLE_CACHE})")
    s.add_argument("--callers-index", default=str(DEFAULT_CALLERS_INDEX),
                   help=f"cross-file callers index dir built by "
                        f"tools/callers_index.py (default {DEFAULT_CALLERS_INDEX})")
    s.add_argument("--trace-callers", type=int, default=1,
                   help="number of 1-hop callers to include in source overlay "
                        "(same-file only, default 1)")
    s.add_argument("--caller-context", type=int, default=10,
                   help="±N source lines around the call site in each caller "
                        "(default 10)")
    s.add_argument("--full-body-threshold", type=int, default=40,
                   help="if a caller's body is <= this many lines, emit it in "
                        "full instead of ±caller-context (default 40)")
    s.add_argument("--call-chain-depth", type=int, default=8,
                   help="max depth for the signature-only call chain "
                        "rendered after the 1-hop detailed caller block "
                        "(default 8 — reaches public-API entry for most "
                        "blockers; set 1 to disable)")
    s.add_argument("--call-chain-per-hop", type=int, default=2,
                   help="max callers to follow from each function during "
                        "the call-chain BFS (default 2 — picks any one "
                        "path to entry without exploding on broad fan-in)")
    s.add_argument("--hit-divergence-rows", type=int, default=15,
                   help="max rows in HIT-COUNT DIVERGENCE section (default 15)")
    s.add_argument("--hit-divergence-min-ratio", type=float, default=3.0,
                   help="min W/L invocation count ratio to flag a function "
                        "as divergent (default 3.0)")
    s.add_argument("--seeds-per-side", type=int, default=5,
                   help="winner-resolving + loser-blocking seeds per pair")
    s.add_argument("--seed-bytes", type=int, default=64)
    s.add_argument("--output", default="-",
                   help="output path or - for stdout (default)")
    s.set_defaults(func=cmd_evidence_per_branch)
