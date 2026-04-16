#!/usr/bin/env python3
"""
seed_diff_v2.py — Structured candidate detection for the v2 cluster pipeline.

The v2 branch-cluster (T1) agent does NOT freeform-interpret seed diff output.
Instead, this tool emits a *list of candidate controlling conditions* — each
typed and ready to be plugged into a necessity test. The agent's job becomes:
verify each candidate via Docker mutation, drop the failing ones, return the
passing ones as ClusterCandidate records.

Five condition types are detected, in order of priority:

  1. ByteRegionMagic       — same value across ALL resolving seeds at a region
  2. ByteRegionTokenSet    — small set of values across resolving (tokens)
  3. LengthThreshold       — clean length partition between resolving/blocking
  4. ByteRange             — resolving values in a contiguous numerical range
  5. BitMask               — specific bits consistent in resolving but not blocking

The tool reuses load_seeds() from the existing seed_diff module so it shares
the same DB-driven seed loading. The MI computation is reused too. The new
logic is the structured detector layer on top.

Usage:
    python3 tools/seed_diff_v2.py --target lcms --branch-id 358 --queue-base ./out
    python3 tools/seed_diff_v2.py --target lcms --branch-id 358 --queue-base ./out --json

JSON output is a dict:
    {
      "branch_id": 358,
      "target": "lcms",
      "n_resolving": 8,
      "n_blocking": 12,
      "candidates": [ <ClusterCandidate JSON>, ... ]
    }

The orchestrator passes the candidates list straight to the T1 agent.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

# Reuse the existing loader and MI implementation
sys.path.insert(0, str(Path(__file__).parent))
from seed_diff import load_seeds, compute_mi, compute_entropy  # noqa: E402

from cluster_schema import (  # noqa: E402
    BitMask,
    ByteRange,
    ByteRegionMagic,
    ByteRegionTokenSet,
    ClusterCandidate,
    LengthThreshold,
    SourceContext,
)


# ---------------------------------------------------------------------------
# Tunables — defaults chosen conservatively, override per-target if needed
# ---------------------------------------------------------------------------

# A region is considered "high MI" if at least one byte exceeds this MI score.
# Lower threshold → more candidates surfaced (good recall, more verification cost).
HIGH_MI_THRESHOLD = 0.5

# A magic-value candidate requires the resolving seeds to have entropy below
# this in the controlling region. Entropy 0 = all the same value; higher = noise.
MAGIC_RESOLVING_ENTROPY_MAX = 0.5

# Token set: how many distinct values can resolving have before we stop calling
# it a token set and downgrade to a noisier candidate type?
TOKEN_SET_MAX_DISTINCT = 8

# Length threshold: require this minimum gap between resolving and blocking
# size distributions. Otherwise it's noise, not a real partition.
LENGTH_GAP_MIN = 4

# Region merging: how many adjacent low-MI bytes can be tolerated within a
# high-MI region before we split it. Allows magic values that have one byte
# of noise.
REGION_MERGE_GAP = 1

# Per-bit MI threshold for bit-mask detection. Lower than the byte threshold
# because bit-level signal is naturally weaker.
BIT_MI_THRESHOLD = 0.3


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------


def _bytes_at_region(seed_data: bytes, offset: int, length: int) -> bytes | None:
    """Return seed_data[offset:offset+length] or None if out of bounds."""
    if offset + length > len(seed_data):
        return None
    return seed_data[offset : offset + length]


def _hex(b: bytes) -> str:
    return b.hex()


def _per_byte_mi(resolving: list[dict], blocking: list[dict]) -> list[float]:
    """
    Compute per-offset MI between resolving and blocking byte values.

    Returns a list of MI scores indexed by offset, padded to the max seed size.
    Offsets where one side has no data return MI=0.
    """
    max_off = max(
        max(s["size"] for s in resolving),
        max(s["size"] for s in blocking),
    )
    mi_per_offset = []
    for off in range(max_off):
        r_vals = [s["data"][off] for s in resolving if off < s["size"]]
        b_vals = [s["data"][off] for s in blocking if off < s["size"]]
        if not r_vals or not b_vals:
            mi_per_offset.append(0.0)
        else:
            mi_per_offset.append(compute_mi(r_vals, b_vals))
    return mi_per_offset


def _find_high_mi_regions(
    mi_per_offset: list[float],
    threshold: float = HIGH_MI_THRESHOLD,
    merge_gap: int = REGION_MERGE_GAP,
) -> list[tuple[int, int]]:
    """
    Group adjacent high-MI offsets into contiguous (start, length) regions.

    Allows up to `merge_gap` low-MI bytes within a region — useful for magic
    values with one noisy byte.

    Returns regions sorted by max MI in the region, descending.
    """
    regions: list[tuple[int, int, float]] = []  # (start, length, max_mi)
    cur_start: int | None = None
    cur_max_mi: float = 0.0
    cur_gap_run: int = 0

    for off, mi in enumerate(mi_per_offset):
        if mi >= threshold:
            if cur_start is None:
                cur_start = off
            cur_max_mi = max(cur_max_mi, mi)
            cur_gap_run = 0
        else:
            if cur_start is not None:
                cur_gap_run += 1
                if cur_gap_run > merge_gap:
                    # Close region
                    end = off - cur_gap_run
                    regions.append((cur_start, end - cur_start + 1, cur_max_mi))
                    cur_start = None
                    cur_max_mi = 0.0
                    cur_gap_run = 0
    if cur_start is not None:
        end = len(mi_per_offset) - 1 - cur_gap_run
        regions.append((cur_start, end - cur_start + 1, cur_max_mi))

    # Sort by max MI descending; return (start, length) only
    regions.sort(key=lambda r: -r[2])
    return [(s, ln) for s, ln, _ in regions]


# ---------------------------------------------------------------------------
# Detector: byte region magic value
# ---------------------------------------------------------------------------


def detect_byte_region_magic(
    resolving: list[dict],
    blocking: list[dict],
    region: tuple[int, int],
) -> ByteRegionMagic | None:
    """
    A region passes magic detection if all (or near-all) resolving seeds have
    the SAME value at that region, and the value does NOT appear in any
    blocking seed at that same region.

    The "near-all" tolerance is one outlier — sometimes a single resolving
    seed is noisy. We require >=80% agreement.
    """
    offset, length = region
    r_vals = []
    for s in resolving:
        chunk = _bytes_at_region(s["data"], offset, length)
        if chunk is not None:
            r_vals.append(chunk)
    if not r_vals:
        return None

    counts = Counter(r_vals)
    most_common_val, most_common_count = counts.most_common(1)[0]
    if most_common_count / len(r_vals) < 0.8:
        return None  # too noisy to be a single magic value

    # Check that this value doesn't appear in blocking seeds at this region
    for s in blocking:
        chunk = _bytes_at_region(s["data"], offset, length)
        if chunk == most_common_val:
            return None  # blocking seed has the same value — not a discriminator

    return ByteRegionMagic(
        offset=offset,
        length=length,
        value_hex=_hex(most_common_val),
    )


# ---------------------------------------------------------------------------
# Detector: byte region token set
# ---------------------------------------------------------------------------


def detect_byte_region_token_set(
    resolving: list[dict],
    blocking: list[dict],
    region: tuple[int, int],
) -> ByteRegionTokenSet | None:
    """
    A region passes token-set detection if resolving seeds have a small set
    (2 to TOKEN_SET_MAX_DISTINCT) of distinct values, AND none of those values
    appear in any blocking seed at the same region.

    Models cases like "the controlling field accepts one of a few keywords"
    (e.g., libpcap protocol keywords: 'tcp', 'udp', 'icmp').
    """
    offset, length = region
    r_vals = set()
    for s in resolving:
        chunk = _bytes_at_region(s["data"], offset, length)
        if chunk is not None:
            r_vals.add(chunk)
    if len(r_vals) < 2 or len(r_vals) > TOKEN_SET_MAX_DISTINCT:
        return None

    # Check resolving values don't appear in blocking
    for s in blocking:
        chunk = _bytes_at_region(s["data"], offset, length)
        if chunk in r_vals:
            return None

    return ByteRegionTokenSet(
        offset=offset,
        length=length,
        value_set_hex=tuple(_hex(v) for v in r_vals),
    )


# ---------------------------------------------------------------------------
# Detector: length threshold
# ---------------------------------------------------------------------------


def detect_length_threshold(
    resolving: list[dict],
    blocking: list[dict],
) -> LengthThreshold | None:
    """
    A length threshold exists if the size distributions of resolving and
    blocking seeds are cleanly partitioned with a gap of at least LENGTH_GAP_MIN.

    Two cases:
      - resolving min > blocking max + GAP → "len(input) >= resolving_min"
      - blocking min > resolving max + GAP → "len(input) <= resolving_max"

    Other configurations (overlapping ranges) do NOT emit a candidate — those
    cases are not cleanly length-controlled.
    """
    r_sizes = [s["size"] for s in resolving]
    b_sizes = [s["size"] for s in blocking]
    if not r_sizes or not b_sizes:
        return None

    r_min, r_max = min(r_sizes), max(r_sizes)
    b_min, b_max = min(b_sizes), max(b_sizes)

    if r_min > b_max + LENGTH_GAP_MIN:
        return LengthThreshold(op="ge", threshold=r_min)
    if b_min > r_max + LENGTH_GAP_MIN:
        return LengthThreshold(op="le", threshold=r_max)

    return None


# ---------------------------------------------------------------------------
# Detector: byte range
# ---------------------------------------------------------------------------


def detect_byte_range(
    resolving: list[dict],
    blocking: list[dict],
    region: tuple[int, int],
) -> ByteRange | None:
    """
    A region passes range detection if resolving values fall in a contiguous
    numerical range (interpreted little-endian) AND blocking values mostly fall
    outside that range.

    Conservative: only emit if the resolving range is small (<=64 distinct
    integer values, well below the full byte space) AND no blocking value
    falls inside the range.
    """
    offset, length = region
    if length > 4:
        return None  # >4 byte ranges are usually magic, not range checks
    r_ints = []
    for s in resolving:
        chunk = _bytes_at_region(s["data"], offset, length)
        if chunk is not None:
            r_ints.append(int.from_bytes(chunk, "little"))
    if not r_ints:
        return None
    lo, hi = min(r_ints), max(r_ints)
    if hi - lo > 64 or hi == lo:
        return None  # range too wide or degenerate (becomes a magic)

    # Check no blocking value falls in the range
    for s in blocking:
        chunk = _bytes_at_region(s["data"], offset, length)
        if chunk is None:
            continue
        v = int.from_bytes(chunk, "little")
        if lo <= v <= hi:
            return None

    return ByteRange(offset=offset, length=length, lo=lo, hi=hi)


# ---------------------------------------------------------------------------
# Detector: bit-mask on a single byte
# ---------------------------------------------------------------------------


def detect_bit_mask(
    resolving: list[dict],
    blocking: list[dict],
    offset: int,
) -> BitMask | None:
    """
    A bit-mask condition exists when a specific bit (or bit pattern) at one
    byte offset is consistently set/clear in resolving seeds and the opposite
    in blocking seeds. Models flag-byte gates: `if (data[X] & FLAG)`.

    Detection: for each of 8 bit positions, check if all resolving seeds agree
    on the bit value AND blocking seeds disagree (the value is different in at
    least one blocking seed). Combine the agreeing bits into a mask.
    """
    r_bytes = [s["data"][offset] for s in resolving if offset < s["size"]]
    b_bytes = [s["data"][offset] for s in blocking if offset < s["size"]]
    if not r_bytes or not b_bytes:
        return None

    mask = 0
    value = 0
    for bit in range(8):
        bit_mask = 1 << bit
        r_bits = {(b & bit_mask) >> bit for b in r_bytes}
        if len(r_bits) != 1:
            continue  # resolving seeds disagree on this bit — not consistent
        r_bit_val = next(iter(r_bits))

        b_bits = {(b & bit_mask) >> bit for b in b_bytes}
        if r_bit_val not in b_bits or len(b_bits) != 1 or next(iter(b_bits)) != r_bit_val:
            # Resolving has fixed bit value; blocking has different / mixed.
            # This bit IS a discriminator.
            mask |= bit_mask
            if r_bit_val:
                value |= bit_mask

    if mask == 0:
        return None  # no discriminating bits found
    if mask == 0xFF:
        return None  # all 8 bits discriminate → upgrade to ByteRegionMagic instead

    return BitMask(
        offset=offset,
        mask_hex=f"{mask:02x}",
        value_hex=f"{value:02x}",
    )


# ---------------------------------------------------------------------------
# Top-level analysis
# ---------------------------------------------------------------------------


def analyze_branch_v2(
    target: str,
    branch_id: int,
    queue_base: str,
    source_context: SourceContext | None = None,
    db_path: str | None = None,
    max_seeds: int = 10,
) -> dict:
    """
    Run all detectors and return a list of structured ClusterCandidate records.

    The detectors are run in priority order: magic > token set > length >
    range > bit-mask. A region that produces a magic candidate is NOT also
    checked for token-set / range / bit-mask, since the more specific
    candidate dominates. But length is checked independently of byte regions
    because they are orthogonal dimensions.

    The source_context arg is optional — if not provided, the orchestrator
    must fill it in before promoting candidates to clusters. (We can't
    determine source context from seed data alone; the agent or orchestrator
    looks it up from the DB's `branches` table.)
    """
    groups = load_seeds(branch_id, queue_base, target, db_path, max_seeds)
    resolving = groups["resolving"]
    blocking = groups["blocking"]

    if not resolving or not blocking:
        return {
            "branch_id": branch_id,
            "target": target,
            "error": (
                f"Insufficient seeds: {len(resolving)} resolving, "
                f"{len(blocking)} blocking"
            ),
            "candidates": [],
        }

    candidates: list[ClusterCandidate] = []

    # 1. Length threshold (orthogonal to byte regions)
    length_cond = detect_length_threshold(resolving, blocking)
    if length_cond is not None:
        candidates.append(
            ClusterCandidate(
                branch_id=branch_id,
                target=target,
                controlling_condition=length_cond,
                source_context=source_context or SourceContext(file="<unknown>"),
                notes="detected by length partition",
            )
        )

    # 2. Find high-MI regions for byte-level detectors
    mi_per_offset = _per_byte_mi(resolving, blocking)
    regions = _find_high_mi_regions(mi_per_offset)

    for region in regions:
        # Try the more specific detectors first; stop at the first hit per region
        magic = detect_byte_region_magic(resolving, blocking, region)
        if magic is not None:
            candidates.append(
                ClusterCandidate(
                    branch_id=branch_id,
                    target=target,
                    controlling_condition=magic,
                    source_context=source_context or SourceContext(file="<unknown>"),
                    notes=f"high-MI region {region}",
                )
            )
            continue

        tokenset = detect_byte_region_token_set(resolving, blocking, region)
        if tokenset is not None:
            candidates.append(
                ClusterCandidate(
                    branch_id=branch_id,
                    target=target,
                    controlling_condition=tokenset,
                    source_context=source_context or SourceContext(file="<unknown>"),
                    notes=f"high-MI region {region}, {len(tokenset.value_set_hex)} tokens",
                )
            )
            continue

        rng = detect_byte_range(resolving, blocking, region)
        if rng is not None:
            candidates.append(
                ClusterCandidate(
                    branch_id=branch_id,
                    target=target,
                    controlling_condition=rng,
                    source_context=source_context or SourceContext(file="<unknown>"),
                    notes=f"high-MI region {region}, range [{rng.lo}, {rng.hi}]",
                )
            )
            continue

        # Bit-mask only fires for single-byte regions
        if region[1] == 1:
            bm = detect_bit_mask(resolving, blocking, region[0])
            if bm is not None:
                candidates.append(
                    ClusterCandidate(
                        branch_id=branch_id,
                        target=target,
                        controlling_condition=bm,
                        source_context=source_context or SourceContext(file="<unknown>"),
                        notes=f"single-byte region @ {region[0]}, bit mask",
                    )
                )

    return {
        "branch_id": branch_id,
        "target": target,
        "n_resolving": len(resolving),
        "n_blocking": len(blocking),
        "n_candidates": len(candidates),
        "candidates": [c.model_dump(mode="json") for c in candidates],
    }


# ---------------------------------------------------------------------------
# Self-test (synthetic seed sets)
# ---------------------------------------------------------------------------


def _self_test() -> None:
    """
    Test detectors against synthetic seed sets. Doesn't touch the DB.
    """
    print("=== seed_diff_v2 self-test ===")

    # ---- Test 1: ByteRegionMagic ----
    # All resolving seeds have 'Lab ' at offset 16. Blocking seeds have RGB.
    resolving = [
        {"data": b"\x00" * 16 + b"Lab " + b"\x00" * 12, "size": 32}
        for _ in range(5)
    ]
    blocking = [
        {"data": b"\x00" * 16 + b"RGB " + b"\x00" * 12, "size": 32}
        for _ in range(5)
    ]
    cond = detect_byte_region_magic(resolving, blocking, (16, 4))
    assert cond is not None, "magic detector failed on clean signal"
    assert cond.value_hex == "4c616220", f"got {cond.value_hex}"
    print(f"  magic: {cond.human_label()}  OK")

    # ---- Test 2: ByteRegionTokenSet ----
    # Resolving has one of {tcp, udp, ip\0}; blocking has 'arp'
    resolving = [
        {"data": b"\x00" + b"tcp\x00" + b"\x00" * 27, "size": 32},
        {"data": b"\x00" + b"udp\x00" + b"\x00" * 27, "size": 32},
        {"data": b"\x00" + b"ip\x00\x00" + b"\x00" * 27, "size": 32},
        {"data": b"\x00" + b"tcp\x00" + b"\x00" * 27, "size": 32},
    ]
    blocking = [{"data": b"\x00" + b"arp\x00" + b"\x00" * 27, "size": 32} for _ in range(5)]
    cond = detect_byte_region_token_set(resolving, blocking, (1, 4))
    assert cond is not None, "token set detector failed"
    assert len(cond.value_set_hex) == 3
    print(f"  token set: {cond.human_label()}  OK")

    # ---- Test 3: LengthThreshold (resolving longer) ----
    resolving = [{"data": b"\x00" * 50, "size": 50} for _ in range(5)]
    blocking = [{"data": b"\x00" * 10, "size": 10} for _ in range(5)]
    cond = detect_length_threshold(resolving, blocking)
    assert cond is not None and cond.op == "ge" and cond.threshold == 50
    print(f"  length: {cond.human_label()}  OK")

    # ---- Test 4: LengthThreshold (resolving shorter) ----
    resolving = [{"data": b"\x00" * 5, "size": 5} for _ in range(5)]
    blocking = [{"data": b"\x00" * 50, "size": 50} for _ in range(5)]
    cond = detect_length_threshold(resolving, blocking)
    assert cond is not None and cond.op == "le" and cond.threshold == 5
    print(f"  length-le: {cond.human_label()}  OK")

    # ---- Test 5: LengthThreshold (overlap → no candidate) ----
    resolving = [{"data": b"\x00" * 30, "size": 30} for _ in range(5)]
    blocking = [{"data": b"\x00" * 32, "size": 32} for _ in range(5)]
    cond = detect_length_threshold(resolving, blocking)
    assert cond is None, "should reject overlapping length distributions"
    print("  length overlap rejected: OK")

    # ---- Test 6: ByteRange ----
    # Resolving values 5..10 at offset 0; blocking values 100..150
    resolving = [
        {"data": bytes([v]) + b"\x00" * 31, "size": 32} for v in range(5, 11)
    ]
    blocking = [
        {"data": bytes([v]) + b"\x00" * 31, "size": 32} for v in range(100, 151, 10)
    ]
    cond = detect_byte_range(resolving, blocking, (0, 1))
    assert cond is not None, "range detector failed"
    assert cond.lo == 5 and cond.hi == 10
    print(f"  range: {cond.human_label()}  OK")

    # ---- Test 7: BitMask ----
    # Resolving: bit 0 always set at offset 0
    # Blocking:  bit 0 always clear at offset 0
    resolving = [{"data": bytes([0x01 | (i << 1)]) + b"\x00" * 31, "size": 32} for i in range(5)]
    blocking = [{"data": bytes([(i << 1) & 0xFE]) + b"\x00" * 31, "size": 32} for i in range(5)]
    cond = detect_bit_mask(resolving, blocking, 0)
    assert cond is not None, "bit mask detector failed"
    assert cond.mask_hex == "01" and cond.value_hex == "01"
    print(f"  bitmask: {cond.human_label()}  OK")

    # ---- Test 8: high-MI region finder merges 4 contiguous offsets ----
    mi = [0.0] * 16 + [0.9, 0.95, 0.92, 0.88] + [0.0] * 12
    regions = _find_high_mi_regions(mi)
    assert regions == [(16, 4)], f"got {regions}"
    print(f"  region merge (contiguous): {regions}  OK")

    # ---- Test 9: high-MI region finder tolerates single-byte gap ----
    mi = [0.0] * 16 + [0.9, 0.0, 0.92] + [0.0] * 13
    regions = _find_high_mi_regions(mi)
    assert regions == [(16, 3)], f"got {regions}"
    print(f"  region merge (1-byte gap): {regions}  OK")

    # ---- Test 10: high-MI region finder splits on 2-byte gap ----
    mi = [0.0] * 16 + [0.9, 0.0, 0.0, 0.92] + [0.0] * 12
    regions = _find_high_mi_regions(mi)
    assert sorted(regions) == [(16, 1), (19, 1)], f"got {regions}"
    print(f"  region split (2-byte gap): {regions}  OK")

    # ---- Test 11: Magic rejected when blocking shares value ----
    resolving = [
        {"data": b"\x00" * 16 + b"Lab " + b"\x00" * 12, "size": 32}
        for _ in range(5)
    ]
    blocking = [
        {"data": b"\x00" * 16 + b"Lab " + b"\x00" * 12, "size": 32}  # SAME!
        for _ in range(5)
    ]
    cond = detect_byte_region_magic(resolving, blocking, (16, 4))
    assert cond is None, "should reject when blocking has same value"
    print("  magic non-discriminating rejected: OK")

    # ---- Test 12: Magic tolerates one outlier in resolving ----
    resolving = [
        {"data": b"\x00" * 16 + b"Lab " + b"\x00" * 12, "size": 32}
        for _ in range(4)
    ] + [{"data": b"\x00" * 16 + b"XYZ " + b"\x00" * 12, "size": 32}]
    blocking = [
        {"data": b"\x00" * 16 + b"RGB " + b"\x00" * 12, "size": 32}
        for _ in range(5)
    ]
    cond = detect_byte_region_magic(resolving, blocking, (16, 4))
    assert cond is not None and cond.value_hex == "4c616220"
    print("  magic with one outlier: OK")

    print("=== all detector self-tests passed ===")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Structured candidate detection (v2) for branch clustering"
    )
    parser.add_argument("--target")
    parser.add_argument("--branch-id", type=int)
    parser.add_argument("--queue-base")
    parser.add_argument("--max-seeds", type=int, default=10)
    parser.add_argument("--db")
    parser.add_argument("--json", action="store_true", help="Print JSON to stdout")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run synthetic detector tests and exit",
    )
    args = parser.parse_args()

    if args.self_test:
        _self_test()
        return

    if not (args.target and args.branch_id and args.queue_base):
        parser.error("--target, --branch-id, --queue-base required (or use --self-test)")

    result = analyze_branch_v2(
        target=args.target,
        branch_id=args.branch_id,
        queue_base=args.queue_base,
        db_path=args.db,
        max_seeds=args.max_seeds,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"# seed_diff_v2 — branch {result['branch_id']} ({result['target']})")
        if "error" in result:
            print(f"Error: {result['error']}")
            return
        print(f"Seeds: {result['n_resolving']} resolving, {result['n_blocking']} blocking")
        print(f"Candidates found: {result['n_candidates']}")
        print()
        for i, cand in enumerate(result["candidates"], start=1):
            cond = cand["controlling_condition"]
            print(f"## Candidate {i} ({cond['type']})")
            print(f"  notes: {cand['notes']}")
            print(f"  raw:   {json.dumps(cond)}")
            print()


if __name__ == "__main__":
    main()
