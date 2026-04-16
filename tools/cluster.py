"""
Fuzzer branch clustering across three dimensions:
  dim1 — blocking/resolved counts (discrete, groupby)
  dim2 — duration level + pattern (continuous, HDBSCAN)
  dim3 — hitcount level + pattern (continuous, HDBSCAN)

Each top-level cluster carries a sub_clusters list: members grouped by file,
then by line proximity (gap-based) within file.

Branch name format: file:function:line:col:side
"""

import json
import math
import numpy as np
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional
import hdbscan

FUZZERS = ["fuzzer_A", "fuzzer_B", "fuzzer_C", "fuzzer_D"]
NUM_TRIALS = 10
SUB_CLUSTER_GAP = 20  # max line gap for same sub-cluster within a file

# ─────────────────────────────────────────────
# Data structures
# ─────────────────────────────────────────────

@dataclass
class BranchRecord:
    """Raw input record for one branch."""
    name: str                          # file:function:line:col:side

    # dim1 — per fuzzer: blocked and resolved counts (int, 0..NUM_TRIALS)
    # never_reached when blocked=0, resolved=0
    blocked:  dict[str, int]           # fuzzer -> count
    resolved: dict[str, int]           # fuzzer -> count

    # dim2 — per fuzzer: duration in seconds from first reach to resolution
    # None if fuzzer never reached the branch
    duration: dict[str, Optional[float]]

    # dim3 — per fuzzer: hitcount on THIS side and OPPOSITE side
    # None if fuzzer never reached the condition at all (both sides = 0)
    current_hits:  dict[str, Optional[int]]
    opposite_hits: dict[str, Optional[int]]

    # Optional: source line text for this branch (from DB)
    source_line: Optional[str] = None

    @property
    def file(self) -> str:
        return self.name.split(":")[0]

    @property
    def function(self) -> str:
        return self.name.split(":")[1]

    @property
    def line(self) -> int:
        return int(self.name.split(":")[2])

    @property
    def col(self) -> int:
        return int(self.name.split(":")[3])

    @property
    def side(self) -> str:
        return self.name.split(":")[4]

    @property
    def opposite_name(self) -> str:
        parts = self.name.split(":")
        parts[4] = "false" if parts[4] == "true" else "true"
        return ":".join(parts)


# ─────────────────────────────────────────────
# Dim 1 — probability (blocking/resolved counts)
# ─────────────────────────────────────────────

RATE_BUCKETS = [
    ("never_reached", lambda b, r: b == 0 and r == 0),
    ("never",         lambda b, r: r == 0 and b > 0),
    ("rarely",        lambda b, r: 0 < r / (b + r) <= 0.3),
    ("sometimes",     lambda b, r: 0.3 < r / (b + r) < 0.7),
    ("mostly",        lambda b, r: 0.7 <= r / (b + r) < 1.0 and b > 0),
    ("always",        lambda b, r: b == 0 and r > 0),
]

def dim1_label(blocked: int, resolved: int) -> str:
    for label, condition in RATE_BUCKETS:
        if condition(blocked, resolved):
            return label
    return "sometimes"  # fallback

def dim1_cluster_key(record: BranchRecord) -> tuple:
    """The cluster key IS the pattern — unique tuple of per-fuzzer labels."""
    return tuple(
        dim1_label(record.blocked[f], record.resolved[f])
        for f in FUZZERS
    )

def dim1_is_interesting(pattern: tuple) -> bool:
    """
    A dim1 pattern is interesting if it contains at least one `never` AND
    at least one `always` — i.e., a deterministic capability gap where one
    fuzzer always blocks while another always resolves.
    """
    return "never" in pattern and "always" in pattern


def dim1_divergence(pattern: tuple) -> float:
    """Normalized entropy of fuzzer labels. 0 = all same, 1 = max divergence."""
    label_counts = defaultdict(int)
    for label in pattern:
        label_counts[label] += 1
    n = len(pattern)
    entropy = 0.0
    for count in label_counts.values():
        p = count / n
        if p > 0:
            entropy -= p * math.log(p)
    max_entropy = math.log(len(RATE_BUCKETS))
    return entropy / max_entropy if max_entropy > 0 else 0.0

def cluster_dim1(records: list[BranchRecord]) -> list[dict]:
    """Group branches by exact dim1 pattern tuple."""
    groups = defaultdict(list)
    for rec in records:
        key = dim1_cluster_key(rec)
        groups[key].append(rec)

    clusters = []
    for cluster_idx, (pattern_key, members) in enumerate(groups.items()):
        pattern = {f: label for f, label in zip(FUZZERS, pattern_key)}
        divergence = dim1_divergence(pattern_key)

        branches = []
        for rec in members:
            branches.append({
                "name":        rec.name,
                "opposite":    rec.opposite_name,
                "file":        rec.file,
                "line":        rec.line,
                "col":         rec.col,
                "side":        rec.side,
                "source_line": rec.source_line,
                "raw_counts": {
                    f: {"blocked": rec.blocked[f], "resolved": rec.resolved[f]}
                    for f in FUZZERS
                },
            })

        clusters.append({
            "cluster_id":     f"dim1_cluster_{cluster_idx:03d}",
            "pattern":        pattern,
            "size":           len(members),
            "is_interesting": dim1_is_interesting(pattern_key),
            "divergence":     {"dim1": round(divergence, 4)},
            "sub_clusters":   build_sub_clusters(branches),
        })

    return clusters


# ─────────────────────────────────────────────
# Dim 2 — duration (level + pattern, HDBSCAN)
# ─────────────────────────────────────────────

def dim2_features(record: BranchRecord) -> Optional[np.ndarray]:
    """
    Compute [level, Δ_A, Δ_B, Δ_C, Δ_D] for dim2.
    Returns None if fewer than 2 fuzzers have duration data.
    NaN for fuzzers that never reached.
    """
    log_durations = {}
    for f in FUZZERS:
        d = record.duration.get(f)
        if d is not None:
            log_durations[f] = math.log1p(d)

    if len(log_durations) < 2:
        return None

    level = np.mean(list(log_durations.values()))
    vec = [level]
    for f in FUZZERS:
        if f in log_durations:
            vec.append(log_durations[f] - level)
        else:
            vec.append(np.nan)

    return np.array(vec)

def nan_aware_distance(u: np.ndarray, v: np.ndarray) -> float:
    """
    Euclidean distance computed only over dimensions where
    both vectors have real values. Level (index 0) always included.
    """
    # always include level (index 0)
    valid = [0]
    for i in range(1, len(u)):
        if not np.isnan(u[i]) and not np.isnan(v[i]):
            valid.append(i)
    if len(valid) == 0:
        return np.inf
    diff = u[valid] - v[valid]
    return float(np.sqrt(np.dot(diff, diff)))

def build_nan_aware_distance_matrix(features: list[np.ndarray]) -> np.ndarray:
    n = len(features)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d = nan_aware_distance(features[i], features[j])
            D[i, j] = d
            D[j, i] = d
    return D

def dim2_divergence(members_features: list[np.ndarray]) -> float:
    """Mean std of Δ values across fuzzers, averaged over branches in cluster."""
    spreads = []
    for vec in members_features:
        deltas = [vec[i] for i in range(1, len(vec)) if not np.isnan(vec[i])]
        if len(deltas) >= 2:
            spreads.append(float(np.std(deltas)))
    return round(float(np.mean(spreads)), 4) if spreads else 0.0

def dim2_pattern(members_features: list[np.ndarray]) -> dict:
    """Centroid of the cluster — mean level and mean Δ per fuzzer."""
    levels = [vec[0] for vec in members_features]
    level = float(np.mean(levels))

    pattern = {"level": round(level, 3)}
    for i, f in enumerate(FUZZERS):
        deltas = [vec[i + 1] for vec in members_features if not np.isnan(vec[i + 1])]
        pattern[f] = round(float(np.mean(deltas)), 3) if deltas else None

    return pattern

def dim2_interpretation(pattern: dict) -> dict:
    """Human-readable summary of the duration pattern."""
    level_seconds = round(math.expm1(pattern["level"]))
    fast, slow, absent = [], [], []
    for f in FUZZERS:
        delta = pattern.get(f)
        if delta is None:
            absent.append(f)
        elif delta < -0.5:
            fast.append(f)
        elif delta > 0.5:
            slow.append(f)
    return {
        "level_seconds": level_seconds,
        "fast_fuzzers":  fast,
        "slow_fuzzers":  slow,
        "absent_fuzzers": absent,
    }

def cluster_dim2(records: list[BranchRecord],
                 min_cluster_size: int = 5) -> list[dict]:
    """HDBSCAN clustering on dim2 duration features."""
    valid_records, features = [], []
    for rec in records:
        vec = dim2_features(rec)
        if vec is not None:
            valid_records.append(rec)
            features.append(vec)

    if len(features) < min_cluster_size:
        return []

    D = build_nan_aware_distance_matrix(features)
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        metric="precomputed"
    )
    labels = clusterer.fit_predict(D)

    # group by cluster label (-1 = noise, skip)
    groups = defaultdict(list)
    for idx, label in enumerate(labels):
        if label != -1:
            groups[label].append(idx)

    clusters = []
    for cluster_idx, indices in groups.items():
        members = [valid_records[i] for i in indices]
        member_features = [features[i] for i in indices]

        pattern = dim2_pattern(member_features)
        divergence = dim2_divergence(member_features)

        branches = []
        for rec, vec in zip(members, member_features):
            raw_d = {f: rec.duration.get(f) for f in FUZZERS}
            log_d = {}
            for i, f in enumerate(FUZZERS):
                log_d[f] = round(float(vec[i + 1]), 3) if not np.isnan(vec[i + 1]) else None
            branches.append({
                "name":          rec.name,
                "opposite":      rec.opposite_name,
                "file":          rec.file,
                "line":          rec.line,
                "col":           rec.col,
                "side":          rec.side,
                "source_line":   rec.source_line,
                "raw_durations": raw_d,
                "log_durations": log_d,
            })

        clusters.append({
            "cluster_id":     f"dim2_cluster_{cluster_idx:03d}",
            "pattern":        pattern,
            "interpretation": dim2_interpretation(pattern),
            "size":           len(members),
            "divergence":     {"dim2": divergence},
            "sub_clusters":   build_sub_clusters(branches),
        })

    return clusters


# ─────────────────────────────────────────────
# Dim 3 — hitcount (level + pattern, HDBSCAN)
# ─────────────────────────────────────────────

def dim3_hitcount(record: BranchRecord, fuzzer: str) -> Optional[int]:
    """
    Returns hitcount value to use for this fuzzer on this branch:
      current > 0 (regardless of opposite) → resolved, use current
      current = 0, opposite > 0            → blocked, use 0
      current = 0, opposite = 0            → never reached, return None
    """
    current  = record.current_hits.get(fuzzer) or 0
    opposite = record.opposite_hits.get(fuzzer) or 0
    if current == 0 and opposite == 0:
        return None       # never reached — exclude
    return current        # 0 if blocked, >0 if resolved

def dim3_features(record: BranchRecord) -> Optional[np.ndarray]:
    """
    Compute [level, Δ_A, Δ_B, Δ_C, Δ_D] for dim3.
    Returns None if fewer than 2 fuzzers have hitcount data.
    """
    log_hits = {}
    for f in FUZZERS:
        h = dim3_hitcount(record, f)
        if h is not None:
            log_hits[f] = math.log1p(h)

    if len(log_hits) < 2:
        return None

    level = np.mean(list(log_hits.values()))
    vec = [level]
    for f in FUZZERS:
        if f in log_hits:
            vec.append(log_hits[f] - level)
        else:
            vec.append(np.nan)

    return np.array(vec)

def dim3_divergence(members_features: list[np.ndarray]) -> float:
    """Mean std of Δ values across fuzzers, averaged over branches in cluster."""
    spreads = []
    for vec in members_features:
        deltas = [vec[i] for i in range(1, len(vec)) if not np.isnan(vec[i])]
        if len(deltas) >= 2:
            spreads.append(float(np.std(deltas)))
    return round(float(np.mean(spreads)), 4) if spreads else 0.0

def dim3_pattern(members_features: list[np.ndarray]) -> dict:
    """Centroid of the cluster."""
    level = float(np.mean([vec[0] for vec in members_features]))
    pattern = {"level": round(level, 3)}
    for i, f in enumerate(FUZZERS):
        deltas = [vec[i + 1] for vec in members_features if not np.isnan(vec[i + 1])]
        pattern[f] = round(float(np.mean(deltas)), 3) if deltas else None
    return pattern

def dim3_interpretation(pattern: dict, members: list[BranchRecord]) -> dict:
    """Human-readable summary of hitcount pattern."""
    level_hits = round(math.expm1(pattern["level"]))
    high_exploration, low_exploration, blocked_fuzzers, absent_fuzzers = [], [], [], []

    for f in FUZZERS:
        delta = pattern.get(f)
        if delta is None:
            # check if absent (never reached) or blocked
            # absent = all members have None for this fuzzer
            all_none = all(dim3_hitcount(rec, f) is None for rec in members)
            if all_none:
                absent_fuzzers.append(f)
            else:
                # has data but delta is None — shouldn't happen, safety fallback
                absent_fuzzers.append(f)
        else:
            # determine if mostly blocked (hitcount=0) or exploring
            hits = [dim3_hitcount(rec, f) for rec in members
                    if dim3_hitcount(rec, f) is not None]
            mostly_zero = hits and all(h == 0 for h in hits)
            if mostly_zero:
                blocked_fuzzers.append(f)
            elif delta > 0.5:
                high_exploration.append(f)
            elif delta < -0.5:
                low_exploration.append(f)

    return {
        "level_hits":       level_hits,
        "high_exploration": high_exploration,
        "low_exploration":  low_exploration,
        "blocked":          blocked_fuzzers,
        "absent_fuzzers":   absent_fuzzers,
    }

def cluster_dim3(records: list[BranchRecord],
                 min_cluster_size: int = 5) -> list[dict]:
    """HDBSCAN clustering on dim3 hitcount features."""
    valid_records, features = [], []
    for rec in records:
        vec = dim3_features(rec)
        if vec is not None:
            valid_records.append(rec)
            features.append(vec)

    if len(features) < min_cluster_size:
        return []

    D = build_nan_aware_distance_matrix(features)
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        metric="precomputed"
    )
    labels = clusterer.fit_predict(D)

    groups = defaultdict(list)
    for idx, label in enumerate(labels):
        if label != -1:
            groups[label].append(idx)

    clusters = []
    for cluster_idx, indices in groups.items():
        members = [valid_records[i] for i in indices]
        member_features = [features[i] for i in indices]

        pattern = dim3_pattern(member_features)
        divergence = dim3_divergence(member_features)

        branches = []
        for rec, vec in zip(members, member_features):
            raw_h = {f: dim3_hitcount(rec, f) for f in FUZZERS}
            log_h = {}
            for i, f in enumerate(FUZZERS):
                log_h[f] = round(float(vec[i + 1]), 3) if not np.isnan(vec[i + 1]) else None
            branches.append({
                "name":          rec.name,
                "opposite":      rec.opposite_name,
                "file":          rec.file,
                "line":          rec.line,
                "col":           rec.col,
                "side":          rec.side,
                "source_line":   rec.source_line,
                "raw_hitcounts": raw_h,
                "log_hitcounts": log_h,
            })

        clusters.append({
            "cluster_id":     f"dim3_cluster_{cluster_idx:03d}",
            "pattern":        pattern,
            "interpretation": dim3_interpretation(pattern, members),
            "size":           len(members),
            "divergence":     {"dim3": divergence},
            "sub_clusters":   build_sub_clusters(branches),
        })

    return clusters


# ─────────────────────────────────────────────
# Sub-clustering: group by file → line-proximity
# ─────────────────────────────────────────────

def build_sub_clusters(branch_dicts: list[dict],
                       gap: int = SUB_CLUSTER_GAP) -> list[dict]:
    """
    Group branch dicts (each with 'file' and 'line' keys) by file, then by
    line proximity within each file. Lines whose gap to the previous line
    is ≤ `gap` belong to the same sub-cluster.

    Sub-clusters are sorted by size descending.
    """
    by_file = defaultdict(list)
    for b in branch_dicts:
        by_file[b["file"]].append(b)

    sub_clusters = []
    for file, branches in by_file.items():
        branches.sort(key=lambda b: (b["line"], b["col"]))
        group = [branches[0]]
        for b in branches[1:]:
            if b["line"] - group[-1]["line"] <= gap:
                group.append(b)
            else:
                sub_clusters.append(_make_sub(file, group))
                group = [b]
        sub_clusters.append(_make_sub(file, group))

    sub_clusters.sort(key=lambda s: -s["size"])
    return sub_clusters


def _make_sub(file: str, group: list[dict]) -> dict:
    return {
        "file":       file,
        "line_range": [group[0]["line"], group[-1]["line"]],
        "size":       len(group),
        "branches":   group,
    }


# ─────────────────────────────────────────────
# Size filter
# ─────────────────────────────────────────────

def passes_size_filter(cluster: dict, min_size: int = 3) -> bool:
    """
    Keep only clusters with enough members. Per-cluster interestingness
    (dim1 is_interesting, dim2/dim3 divergence) is reported and used for
    ordering, not as a filter.
    """
    return cluster["size"] >= min_size


# ─────────────────────────────────────────────
# Main entry point
# ─────────────────────────────────────────────

def run_clustering(records: list[BranchRecord],
                   min_cluster_size: int = 5,
                   min_size: int = 3,
                   dim2_min_div: float = 1.0,
                   dim3_min_div: float = 1.0) -> dict:
    """
    Run three-dim clustering pipeline and return JSON-ready result.
    Each dim is independent; each cluster carries sub_clusters grouped by
    file and line proximity.

    Filters applied:
      dim1 — size >= min_size AND is_interesting (has both `never` and `always`)
      dim2 — size >= min_size AND divergence >= dim2_min_div
      dim3 — size >= min_size AND divergence >= dim3_min_div
    """
    all_dim1 = cluster_dim1(records)
    all_dim2 = cluster_dim2(records, min_cluster_size=min_cluster_size)
    all_dim3 = cluster_dim3(records, min_cluster_size=min_cluster_size)

    kept_dim1 = [c for c in all_dim1
                 if passes_size_filter(c, min_size) and c["is_interesting"]]
    kept_dim2 = [c for c in all_dim2
                 if passes_size_filter(c, min_size)
                 and c["divergence"]["dim2"] >= dim2_min_div]
    kept_dim3 = [c for c in all_dim3
                 if passes_size_filter(c, min_size)
                 and c["divergence"]["dim3"] >= dim3_min_div]

    kept_dim1.sort(key=lambda c: -c["size"])
    kept_dim2.sort(key=lambda c: -c["divergence"]["dim2"])
    kept_dim3.sort(key=lambda c: -c["divergence"]["dim3"])

    return {
        "summary": {
            "total_branches":      len(records),
            "dim1_clusters_found": len(all_dim1),
            "dim1_clusters_kept":  len(kept_dim1),
            "dim2_clusters_found": len(all_dim2),
            "dim2_clusters_kept":  len(kept_dim2),
            "dim3_clusters_found": len(all_dim3),
            "dim3_clusters_kept":  len(kept_dim3),
        },
        "dim1_clusters": kept_dim1,
        "dim2_clusters": kept_dim2,
        "dim3_clusters": kept_dim3,
    }


# ─────────────────────────────────────────────
# Example usage with synthetic data
# ─────────────────────────────────────────────

def make_synthetic_data() -> list[BranchRecord]:
    """
    Synthetic dataset covering the four key patterns:
      cluster A — fuzzer_A blocks, fuzzer_B resolves  (branches in parse_expr)
      cluster B — fuzzer_B blocks, fuzzer_A resolves  (branches in eval_stmt)
      cluster C — all fuzzers resolve fast            (branches in lex_token)
      cluster D — all fuzzers resolve slow            (branches in type_check)
    """
    records = []

    # cluster A — fuzzer_A blocks, fuzzer_B resolves (8 branches)
    for i in range(8):
        records.append(BranchRecord(
            name=f"src/parser.c:parse_expr:{100+i}:4:true",
            blocked  = {"fuzzer_A": 10, "fuzzer_B": 0,  "fuzzer_C": 9,  "fuzzer_D": 0},
            resolved = {"fuzzer_A": 0,  "fuzzer_B": 10, "fuzzer_C": 1,  "fuzzer_D": 0},
            duration = {
                "fuzzer_A": None,
                "fuzzer_B": 200 + i * 30,
                "fuzzer_C": 180 + i * 20,
                "fuzzer_D": None,
            },
            current_hits  = {"fuzzer_A": 0,              "fuzzer_B": 5000 + i*200, "fuzzer_C": 100+i*10, "fuzzer_D": 0},
            opposite_hits = {"fuzzer_A": 8000 + i*100,   "fuzzer_B": 200,          "fuzzer_C": 500,      "fuzzer_D": 0},
        ))

    # cluster B — fuzzer_B blocks, fuzzer_A resolves (8 branches)
    for i in range(8):
        records.append(BranchRecord(
            name=f"src/eval.c:eval_stmt:{200+i}:8:true",
            blocked  = {"fuzzer_A": 0,  "fuzzer_B": 10, "fuzzer_C": 0,  "fuzzer_D": 9},
            resolved = {"fuzzer_A": 10, "fuzzer_B": 0,  "fuzzer_C": 10, "fuzzer_D": 1},
            duration = {
                "fuzzer_A": 150 + i * 20,
                "fuzzer_B": None,
                "fuzzer_C": 170 + i * 25,
                "fuzzer_D": 28000 + i * 500,
            },
            current_hits  = {"fuzzer_A": 6000+i*300, "fuzzer_B": 0,            "fuzzer_C": 4000+i*200, "fuzzer_D": 50+i},
            opposite_hits = {"fuzzer_A": 100,         "fuzzer_B": 9000+i*200,  "fuzzer_C": 80,         "fuzzer_D": 300},
        ))

    # cluster C — all fast (6 branches)
    for i in range(6):
        records.append(BranchRecord(
            name=f"src/lexer.c:lex_token:{300+i}:2:true",
            blocked  = {"fuzzer_A": 0, "fuzzer_B": 0, "fuzzer_C": 0, "fuzzer_D": 0},
            resolved = {"fuzzer_A": 10,"fuzzer_B": 10,"fuzzer_C": 10,"fuzzer_D": 10},
            duration = {
                "fuzzer_A": 25 + i * 5,
                "fuzzer_B": 30 + i * 5,
                "fuzzer_C": 28 + i * 4,
                "fuzzer_D": 22 + i * 6,
            },
            current_hits  = {"fuzzer_A": 8000+i*100,"fuzzer_B": 7500+i*80,"fuzzer_C": 8200+i*90,"fuzzer_D": 7800+i*110},
            opposite_hits = {"fuzzer_A": 50,         "fuzzer_B": 60,       "fuzzer_C": 45,       "fuzzer_D": 55},
        ))

    # cluster D — all slow (6 branches)
    for i in range(6):
        records.append(BranchRecord(
            name=f"src/typechk.c:type_check:{400+i}:6:true",
            blocked  = {"fuzzer_A": 0, "fuzzer_B": 0, "fuzzer_C": 0, "fuzzer_D": 0},
            resolved = {"fuzzer_A": 10,"fuzzer_B": 10,"fuzzer_C": 10,"fuzzer_D": 10},
            duration = {
                "fuzzer_A": 25000 + i * 1000,
                "fuzzer_B": 27000 + i * 800,
                "fuzzer_C": 26000 + i * 900,
                "fuzzer_D": 28000 + i * 700,
            },
            current_hits  = {"fuzzer_A": 200+i*10,"fuzzer_B": 180+i*8,"fuzzer_C": 210+i*9,"fuzzer_D": 190+i*11},
            opposite_hits = {"fuzzer_A": 30,       "fuzzer_B": 25,     "fuzzer_C": 28,     "fuzzer_D": 32},
        ))

    return records


if __name__ == "__main__":
    records = make_synthetic_data()
    result = run_clustering(
        records,
        min_cluster_size=3,
        min_size=3,
        min_divergence_dim1=0.3,
        min_divergence_dim2=0.5,
        min_divergence_dim3=0.5,
    )
    print(json.dumps(result, indent=2))