#!/usr/bin/env python3
"""
callers_index.py — build a per-target, source-grep-derived index of
1-hop callers for every function.

Used by the SOURCE CONTEXT overlay (study_units.py) and the per-role
coverage generator (per_role_coverage.py) to find which functions call
the blocker's enclosing function — including CROSS-FILE callers.
Cheaper than a real call graph (no opt -callgraph build step, no
per-target tooling), at the cost of missing function-pointer and
template-indirected calls (typically ~5-10% in practice).

Per target, runs ONE docker invocation that:
  1. Greps every C/C++ source file under /src/<target>/ for any
     function-name token followed by '('.
  2. Maps each hit line to its enclosing function via the function
     index (extract_functions.extract).
  3. Emits db/callers_index/<target>.json keyed by callee function
     name (demangled) -> list of caller records.

Usage:
    python3 tools/callers_index.py build   --target curl
    python3 tools/callers_index.py status  --target curl
    python3 tools/callers_index.py inspect --target curl --func Curl_unencode_cleanup
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = TOOLS_DIR.parent
INDEX_DIR = PROJECT_DIR / 'db' / 'callers_index'

sys.path.insert(0, str(TOOLS_DIR))
import extract_functions  # noqa: E402


SOURCE_EXTS = ('c', 'h', 'cc', 'cpp', 'hpp', 'hh', 'cxx', 'hxx')


def short_name(demangled):
    """Last identifier of a demangled C/C++ name.

    Curl_unencode_cleanup                                  -> Curl_unencode_cleanup
    OT::cff2::accelerator_templ_t<...>::accelerator_templ_t -> accelerator_templ_t
    hb_face_create                                          -> hb_face_create
    operator new                                            -> '' (skipped)
    """
    n = demangled
    # Strip parameter list and everything after.
    n = re.split(r'\(', n, 1)[0]
    # Strip nested template args repeatedly.
    while True:
        new_n = re.sub(r'<[^<>]*>', '', n)
        if new_n == n:
            break
        n = new_n
    leaf = n.split('::')[-1].strip()
    # For static C fns, extract_functions prefixes the file basename
    # ("mime.c:search_header") to disambiguate same-named statics across
    # files. Split on ':' and take the suffix so the grep token is the
    # actual call-site identifier.
    leaf = leaf.split(':')[-1].strip()
    if not leaf or not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', leaf):
        return ''
    return leaf


def demangle_names(unique_names):
    try:
        proc = subprocess.run(
            ['c++filt'], input='\n'.join(unique_names),
            capture_output=True, text=True, check=True, timeout=30,
        )
        return dict(zip(unique_names, proc.stdout.rstrip('\n').split('\n')))
    except (FileNotFoundError, subprocess.SubprocessError):
        return {n: n for n in unique_names}


def grep_callers(target, source_root, tokens):
    """Run grep -F -f tokens.txt inside the docker image. Returns list of
    raw (file_path, line_no, source_line) tuples for any line that
    contains any token. Caller is responsible for filtering to lines
    where the token is followed by '('."""
    if not tokens:
        return []
    tf = tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False)
    tf.write('\n'.join(sorted(tokens)) + '\n')
    tf.close()

    image = f'libafl-{target}-cov'
    include_args = ' '.join(f"--include='*.{e}'" for e in SOURCE_EXTS)
    cmd = ['docker', 'run', '--rm', '--entrypoint', '',
           '-v', f'{tf.name}:/tokens.txt:ro',
           image,
           'bash', '-c',
           f"grep -rnF --no-messages {include_args} -f /tokens.txt "
           f"{source_root} 2>/dev/null"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    finally:
        Path(tf.name).unlink(missing_ok=True)
    # grep exit codes: 0 = match, 1 = no match, 2 = error/warning.
    if proc.returncode not in (0, 1, 2):
        print(f"grep exited rc={proc.returncode}: {proc.stderr[:200]}",
              file=sys.stderr)
        return []

    out = []
    for raw in proc.stdout.splitlines():
        m = re.match(r'^(.+?):(\d+):(.*)$', raw)
        if not m:
            continue
        out.append((m.group(1), int(m.group(2)), m.group(3)))
    return out


def cmd_build(args):
    target = args.target
    print(f"Building callers index for {target}...", file=sys.stderr)

    fns = extract_functions.extract(target)
    if not fns:
        print(f"No functions extracted for {target}", file=sys.stderr)
        sys.exit(1)

    name_map = demangle_names(sorted({f["name"] for f in fns}))

    fn_index = defaultdict(list)
    for f in fns:
        fn_index[f['file']].append(
            (f['start_line'], f['end_line'],
             name_map.get(f['name'], f['name'])))

    # Map short identifier token -> [demangled names having that token]
    token_to_demangled = defaultdict(list)
    for demangled in name_map.values():
        tok = short_name(demangled)
        if tok:
            token_to_demangled[tok].append(demangled)
    tokens = sorted(token_to_demangled.keys())
    print(f"  {len(tokens)} unique tokens across {len(name_map)} functions",
          file=sys.stderr)

    raw_hits = grep_callers(target, args.source_root, tokens)
    print(f"  {len(raw_hits)} candidate hit lines from grep",
          file=sys.stderr)

    # Filter: token must be followed by '(' (with optional whitespace).
    # Map each hit to (callee, caller) via the function index.
    index = defaultdict(list)
    skipped_no_paren = 0
    skipped_no_enclosing = 0
    for file_path, line, src in raw_hits:
        cands = [t for t in fn_index.get(file_path, [])
                 if t[0] <= line <= t[1]]
        if not cands:
            skipped_no_enclosing += 1
            continue
        caller = min(cands, key=lambda t: (t[1] - t[0], t[0]))

        # Find every token in this line that is followed by '('
        any_match = False
        for tok in token_to_demangled:
            # Use a quick substring test before regex
            if tok not in src:
                continue
            # Pattern: token NOT preceded by ident char, followed by '(' (optional ws)
            pat = r'(?<![A-Za-z0-9_])' + re.escape(tok) + r'\s*\('
            if not re.search(pat, src):
                continue
            any_match = True
            for callee_demangled in token_to_demangled[tok]:
                if callee_demangled == caller[2]:
                    continue
                entry = {
                    'caller': caller[2],
                    'file': file_path,
                    'line': line,
                    'caller_start': caller[0],
                    'caller_end': caller[1],
                }
                if entry not in index[callee_demangled]:
                    index[callee_demangled].append(entry)
        if not any_match:
            skipped_no_paren += 1

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    out_path = INDEX_DIR / f'{target}.json'
    with out_path.open('w') as f:
        json.dump({
            'target': target,
            'source_root': args.source_root,
            'n_functions': len(name_map),
            'n_callees_with_callers': len(index),
            'callers': dict(index),
        }, f, indent=2)

    n_calls = sum(len(v) for v in index.values())
    print(f"  filtered: -{skipped_no_paren} no-paren, "
          f"-{skipped_no_enclosing} no-enclosing-fn",
          file=sys.stderr)
    print(f"  wrote {out_path}: "
          f"{len(index)} callees with ≥1 caller, {n_calls} edges",
          file=sys.stderr)


def cmd_status(args):
    p = INDEX_DIR / f'{args.target}.json'
    if not p.is_file():
        print(f"no index at {p}")
        return
    data = json.load(p.open())
    print(f"target           : {data['target']}")
    print(f"source_root      : {data['source_root']}")
    print(f"functions        : {data['n_functions']}")
    print(f"with >=1 caller  : {data['n_callees_with_callers']}")
    print(f"file             : {p}")


def cmd_inspect(args):
    p = INDEX_DIR / f'{args.target}.json'
    if not p.is_file():
        print(f"no index at {p}")
        return
    data = json.load(p.open())
    callers = data['callers'].get(args.func, [])
    if not callers:
        # Try substring match for convenience
        matches = [k for k in data['callers'] if args.func in k]
        if not matches:
            print(f"no callers recorded for '{args.func}' "
                  f"(no demangled name matches)")
            return
        print(f"no exact match; functions matching '{args.func}':")
        for m in matches[:10]:
            print(f"  {m}  ({len(data['callers'][m])} callers)")
        return
    for c in callers:
        print(f"  {c['caller']:60s}  {c['file']}:{c['line']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)

    p_build = sub.add_parser('build')
    p_build.add_argument('--target', required=True)
    p_build.add_argument('--source-root', default=None,
                         help='source dir inside docker '
                              '(default /src/<target>)')
    p_build.set_defaults(handler=cmd_build)

    p_status = sub.add_parser('status')
    p_status.add_argument('--target', required=True)
    p_status.set_defaults(handler=cmd_status)

    p_inspect = sub.add_parser('inspect')
    p_inspect.add_argument('--target', required=True)
    p_inspect.add_argument('--func', required=True,
                           help='demangled function name (substring ok)')
    p_inspect.set_defaults(handler=cmd_inspect)

    args = ap.parse_args()
    if args.cmd == 'build' and args.source_root is None:
        args.source_root = f'/src/{args.target}'
    args.handler(args)


if __name__ == '__main__':
    main()
