"""
seed_utils.py — small, dependency-free helpers shared across tools.

Used by:
  - tools/evidence_prompt.py (for BRANCH SEEDS hex dumps + byte diff)
  - tools/db_query.py        (for the more-seeds --show-bytes output)
  - tools/study_units.py     (legacy coverage parser; uses parse_count)

Functions here intentionally have no DB or Docker dependencies — they
operate on already-fetched seed rows + bytes on disk. Keep it that way:
adding side effects breaks the "pure helpers" contract that lets
db_query import without dragging in the full pipeline stack.
"""

from collections import Counter


# ── llvm-cov count parser ──────────────────────────────────────────────────

def parse_count(s):
    """Parse llvm-cov count column: '35.7M', '2.20k', '0', '1,234', '18.4E', or ''.

    Returns int for numeric counts; returns None for empty input (a
    non-executable source line) or on parse failure. Callers that need
    a 0 fallback should use `parse_count(s) or 0`.
    """
    s = s.strip().replace(",", "")
    if not s:
        return None
    mult = {"k": 1_000, "M": 1_000_000, "G": 1_000_000_000}
    if s[-1] in mult:
        return int(float(s[:-1]) * mult[s[-1]])
    s = s.rstrip("eE")  # llvm-cov-18 sometimes emits truncated '18.4E'
    if not s:
        return 0
    try:
        return int(float(s))
    except ValueError:
        return None


# ── hex dump + seed reading ────────────────────────────────────────────────

def hex_dump(data, max_bytes):
    """16-byte-per-row hex+ASCII dump of the first max_bytes."""
    chunk = data[:max_bytes]
    rows = []
    for off in range(0, len(chunk), 16):
        slice_ = chunk[off:off + 16]
        hex_part = " ".join(f"{b:02x}" for b in slice_).ljust(48)
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in slice_)
        rows.append(f"  {off:04x}: {hex_part}  {ascii_part}")
    return "\n".join(rows)


def read_seed_bytes(queue_base, target, fuzzer, trial, seed_id, max_bytes):
    """Read first max_bytes of the seed file.

    Returns (size, bytes) on success or (None, error_message_str) on
    missing / unreadable file.
    """
    p = queue_base / target / fuzzer / f"trial{trial}" / "queue" / seed_id
    try:
        size = p.stat().st_size
        with p.open("rb") as f:
            data = f.read(max_bytes)
        return size, data
    except FileNotFoundError:
        return None, f"[seed file not found: {p}]"
    except OSError as exc:
        return None, f"[error reading {p}: {exc}]"


# ── prompt sections ────────────────────────────────────────────────────────

def format_seed_block(label, rows, queue_base, target, max_bytes):
    """Format a winner-resolving or loser-blocking seed block.

    rows: list of (fuzzer, trial, seed_id, mutation_op, discovery_time_s)
    """
    if not rows:
        return (f"==== {label} ====\n"
                f"[no seeds available — run seed_bisect.py to populate]\n")
    out = [f"==== {label} ===="]
    for i, r in enumerate(rows, 1):
        fuzzer, trial, seed_id, mutation_op, disc_t = r
        size, data = read_seed_bytes(queue_base, target, fuzzer, trial,
                                     seed_id, max_bytes)
        header = (f"Seed {i} (id={seed_id}, "
                  f"size={size if size is not None else '?'} bytes, "
                  f"fuzzer={fuzzer}, trial={trial}")
        if disc_t is not None and disc_t != -1:
            header += f", discovered_at={disc_t}s"
        if mutation_op:
            header += f", mutation_op={mutation_op}"
        header += "):"
        out.append(header)
        if isinstance(data, bytes):
            out.append(hex_dump(data, max_bytes))
        else:
            out.append(f"  {data}")
    return "\n".join(out) + "\n"


def byte_diff_section(winner_seeds, loser_seeds, queue_base, target,
                      max_bytes, max_rows=40, noise_threshold=4):
    """Per-offset byte-set diff between W and L seeds.

    For each offset 0..min(seed_len, max_bytes), compute the set of W
    bytes vs L bytes across all seeds. Emit only offsets where the sets
    differ AND at least one is small (≤ noise_threshold). Skips offsets
    where both sides show high variability (uninformative noise — those
    bytes look random in both groups).

    The agent uses this to locate which input-byte offsets consistently
    differ between W and L seeds. An offset where W is always 'C' and L
    is always '\\0' is a strong dataflow signal.
    """
    def _read_all(seeds):
        out = []
        for (fz, tr, sid, _mut, _t) in seeds:
            _size, data = read_seed_bytes(queue_base, target, fz, tr, sid,
                                          max_bytes)
            if isinstance(data, bytes):
                out.append(data)
        return out

    w_bytes = _read_all(winner_seeds)
    l_bytes = _read_all(loser_seeds)
    if not w_bytes or not l_bytes:
        return ("==== BYTE DIFF (W vs L at common offsets) ====\n"
                "[no readable seed bytes on at least one side]\n")

    def _fmt_set(s):
        cnt = Counter(s)
        top = cnt.most_common(4)
        items = []
        for b, k in top:
            ch = chr(b) if 32 <= b < 127 else "."
            items.append(f"{b:02x}({ch})x{k}")
        extra = len(cnt) - len(top)
        s_repr = " ".join(items)
        if extra > 0:
            s_repr += f" +{extra}u"
        return f"{s_repr:<34s}"

    rows = []
    max_off = min(max_bytes, max(max((len(s) for s in w_bytes), default=0),
                                 max((len(s) for s in l_bytes), default=0)))
    for off in range(max_off):
        wb = [s[off] for s in w_bytes if off < len(s)]
        lb = [s[off] for s in l_bytes if off < len(s)]
        if not wb or not lb:
            continue
        wset = set(wb)
        lset = set(lb)
        if wset == lset:
            continue
        # Skip uninformative high-entropy offsets where BOTH sides show
        # many distinct bytes (looks random in both — probably padding
        # or fuzz-mutator noise, not a real gate).
        if len(wset) > noise_threshold and len(lset) > noise_threshold:
            continue
        overlap = wset & lset
        tag = "DIFFER" if not overlap else "PARTIAL"
        rows.append((off, _fmt_set(wb), _fmt_set(lb), tag))

    if not rows:
        return ("==== BYTE DIFF (W vs L at common offsets) ====\n"
                "[no informative byte-level divergence — seeds look "
                "structurally similar across W and L at every offset, "
                "OR diverge only at high-entropy positions (noise)]\n")

    lines = [
        "==== BYTE DIFF (W vs L at common offsets) ====",
        "Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets "
        "where W and L bytes differ AND at least one side is concentrated "
        "(≤4 distinct values) — likely-informative dataflow signal.",
        "",
        f"{'Offset':>7}  {'W bytes':<34s}  {'L bytes':<34s}  tag",
    ]
    for off, w_fmt, l_fmt, tag in rows[:max_rows]:
        lines.append(f"   0x{off:04x}  {w_fmt}  {l_fmt}  {tag}")
    if len(rows) > max_rows:
        lines.append(f"   ... ({len(rows) - max_rows} more divergent offsets)")
    return "\n".join(lines)
