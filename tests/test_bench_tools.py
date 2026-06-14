"""Tests for the bench measurement tools + arbiter wiring + dataset invariants.

Run:  python3 -m pytest tests/test_bench_tools.py -q
Corpus/seed-dependent checks SKIP when on-disk corpora are absent (so this is
portable to server B / CI without the fuzz campaign mounted).
"""
import collections
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _load(modpath):
    spec = importlib.util.spec_from_file_location(modpath.stem, modpath)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


tc = _load(ROOT / "bench" / "tools" / "token_count.py")
csr = _load(ROOT / "bench" / "tools" / "corpus_size_ratio.py")

HARFBUZZ_ONDISK = (ROOT / "out" / "harfbuzz" / "naive" / "trial1" / "queue").is_dir()
DATASET = ROOT / "bench" / "dataset.jsonl"


# ---------- token_count units ----------
def test_parse_literal_hex():
    assert tc.parse_literal("0x03") == b"\x03"
    assert tc.parse_literal("0x0a0b") == b"\x0a\x0b"
    assert tc.parse_literal("0x00010000") == b"\x00\x01\x00\x00"


def test_parse_literal_odd_nibble_padded():
    # a 3-nibble hex must left-pad, not raise
    assert tc.parse_literal("0x309") == b"\x03\x09"


def test_parse_literal_string_and_none():
    assert tc.parse_literal("'GSUB'") == b"GSUB"
    assert tc.parse_literal(None) is None
    assert tc.parse_literal("derived_integer (no literal)") is None


def test_mean_count():
    assert tc.mean_count([b"a\x00b\x00", b"\x00\x00\x00"], b"\x00") == 2.5
    assert tc.mean_count([], b"\x00") is None


def test_token_count_skips_without_literal():
    out = tc.analyze("harfbuzz", 5311, None, "naive", "grimoire")
    assert out["skip"] and "literal" in out["skip"]


# ---------- corpus_size_ratio ----------
def test_corpus_size_ratio_skip_missing_arm():
    out = csr.analyze("harfbuzz", "no_such_fuzzer_arm", "also_missing")
    assert out["skip"] and "no on-disk corpus" in out["skip"]


@pytest.mark.skipif(not HARFBUZZ_ONDISK, reason="harfbuzz corpus not on disk")
def test_corpus_size_ratio_i2s_inflation():
    out = csr.analyze("harfbuzz", "cmplog", "naive")
    assert out["skip"] is None
    # I2S (cmplog) inflates its saved corpus well past naive (memory: ~105k vs 36k)
    assert out["corpus_count_ratio"] > 1.5
    assert out["corpus_size_ratio"] == out["corpus_count_ratio"]
    assert out["composition_entropy_ratio"] is not None


@pytest.mark.skipif(not HARFBUZZ_ONDISK, reason="harfbuzz corpus not on disk")
def test_corpus_size_ratio_branch_independent():
    # whole-corpus metric: identical regardless of --branch-id
    a = csr.analyze("harfbuzz", "cmplog", "naive")
    b = csr.analyze("harfbuzz", "cmplog", "naive")
    assert a["corpus_count_ratio"] == b["corpus_count_ratio"]


# ---------- arbiter wiring ----------
def test_arbiter_registers_new_tools():
    arb = _load(ROOT / "bench" / "arbitrate.py")
    assert "corpus_size_ratio" in arb.TOOL_CMD and "corpus_size_ratio" in arb.BUILT
    assert "token_count" in arb.TOOL_CMD and "token_count" in arb.BUILT
    # metric -> tool dispatch
    assert arb.METRIC_TOOL["corpus_count_ratio"] == "corpus_size_ratio"
    assert arb.METRIC_TOOL["composition_entropy_ratio"] == "corpus_size_ratio"
    assert arb.METRIC_TOOL["naive_literal_count"] == "token_count"
    assert arb.METRIC_TOOL["literal_presence_ratio"] == "token_count"
    # arm maps
    assert arb.CS_ARMS["ctx_coverage_LW"] == ("naive_ctx", "naive")
    assert arb.CS_ARMS["i2s_vp_LWLW"] == ("cmplog", "naive")
    assert arb.TC_ARMS["grimoire_structural_LW"] == ("naive", "grimoire")


# ---------- dataset invariants (multi-label) ----------
@pytest.fixture(scope="module")
def rows():
    if not DATASET.exists():
        pytest.skip("dataset.jsonl not built")
    return [json.loads(l) for l in open(DATASET)]


def test_dataset_no_duplicate_branch_shape(rows):
    # branch_id is NOT globally unique across servers (bloaty_57 vs curl_57 are
    # different branches), so identity is (target, branch_id, shape) — one row per
    # that axis. A bare (branch_id, shape) can legitimately recur across targets.
    keys = [(r["target"], r["branch_id"], r["shape"]) for r in rows]
    assert len(keys) == len(set(keys)), "a (target, branch_id, shape) axis must be one row"


def test_dataset_label_status_consistency(rows):
    for r in rows:
        lab = (r["mechanism"] or {}).get("label")
        if r["evidence"]["status"] == "validated":
            assert lab, f"validated row {r['branch_id']}/{r['shape']} has no label"
        else:
            assert lab is None, f"inconclusive row {r['branch_id']}/{r['shape']} carries a label"


def test_dataset_no_duplicate_validated_axis(rows):
    # The real multi-label safety invariant: identity is (target, branch_id, shape)
    # — branch_id is NOT unique across servers — and each such AXIS is validated at
    # most once (no competing label on the same axis). A branch MAY be validated on
    # multiple DISTINCT axes/technique families (legitimate multi-label: different
    # fuzzer pairs cracking the same hard branch by different mechanisms — e.g.
    # libxml2/6674 = ctx iteration-depth AND i2s relational-collision).
    seen = collections.Counter((r["target"], r["branch_id"], r["shape"])
                               for r in rows if r["evidence"]["status"] == "validated")
    dup = {k: c for k, c in seen.items() if c > 1}
    assert not dup, f"same (target,branch_id,shape) validated more than once: {dup}"


def test_dataset_multivalidated_are_distinct_axes(rows):
    # A branch validated on >1 axis must be on DISTINCT shapes (genuine multi-axis),
    # never the same shape twice. Report the (rare) cross-technique-family branches.
    vrows = [r for r in rows if r["evidence"]["status"] == "validated"]
    by_branch = collections.defaultdict(set)              # (target,bid) -> {shape}
    by_tech = collections.defaultdict(set)                # (target,bid) -> {technique}
    for r in vrows:
        key = (r["target"], r["branch_id"])
        by_branch[key].add(r["shape"])
        by_tech[key].add(r["decisive_shape"].get("technique") or "i2s_vp")
    # every validated row of a multi-validated branch is a distinct shape
    assert all(len(sh) == sum(1 for r in vrows
                              if (r["target"], r["branch_id"]) == k) for k, sh in by_branch.items())
    multi_tech = {k: t for k, t in by_tech.items() if len(t) > 1}
    if multi_tech:
        print(f"\n  [info] {len(multi_tech)} branch(es) validated across >1 technique "
              f"family (legitimate multi-axis): {dict(list(multi_tech.items())[:5])}")
