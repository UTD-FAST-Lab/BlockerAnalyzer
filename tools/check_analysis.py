#!/usr/bin/env python3
"""
check_analysis.py — validate a `.analysis.json` against its sibling
`.prompt.md`.

Per-branch analysis files produced by the hypothesis-generator agent
must follow the schema embedded in the prompt's TASK section. This
script enforces:

  1. Required top-level fields present and non-empty.
  2. evidence_trail is a non-empty list; each entry has the four
     required sub-fields (claim, cited_section, cited_locator,
     exact_quote).
  3. Every exact_quote appears LITERALLY in the prompt file (whitespace
     tolerance: collapses runs of spaces/newlines to a single space
     before substring search).
  4. cited_section names a section that actually exists in the prompt.
  5. mechanism_consistency_check: if claimed_mechanism contains "I2S"
     or "I2SRandReplace", verified_in_lineage MUST be true (or the
     analysis must explain why it could not be verified — the
     verification_method field cannot be empty).
  6. pair_decision matches the number of hypotheses (single_feature =>
     exactly 1; multi_feature => >= 2).
  7. Each hypothesis.covers_pairs entry names a decisive pair label
     that appears in the prompt's DECISIVE PAIRS section.

Usage:
    python3 tools/check_analysis.py path/to/01_curl_19.analysis.json
    python3 tools/check_analysis.py prompts/_smoke_v1/*.analysis.json
    python3 tools/check_analysis.py --recursive prompts/

Exit codes:
  0 — all analyses validated cleanly.
  1 — at least one analysis has violations.
  2 — usage error.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_TOPLEVEL = [
    "branch_id", "target", "summary_one_line", "pair_decision",
    "hypotheses", "evidence_trail", "mechanism_consistency_check",
    "falsifiability", "weakest_evidence_point", "confidence",
]
REQUIRED_HYPOTHESIS = [
    "covers_pairs", "what_input_feature", "why_winner_satisfies",
    "why_loser_doesnt", "mechanism_attribution",
]
REQUIRED_EVIDENCE_ENTRY = ["claim", "cited_section", "cited_locator", "exact_quote"]
REQUIRED_MCC = ["claimed_mechanism", "verified_in_lineage", "verification_method"]
VALID_CITED_SECTIONS = {
    "BYTE DIFF", "SOURCE CONTEXT", "DIVERGENT BRANCHES", "BRANCH SEEDS",
    "DECISIVE PAIRS", "TRIAL VECTOR", "HIT-COUNT DIVERGENCE",
    "MECHANISM CONTEXT", "BLOCKER",
}
VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_MECHANISMS = {
    # comparison-solving (roadblock)
    "I2SRandReplace", "CMP_MAP gradient",
    # coverage-granularity (feedback)
    "context-sensitive coverage", "ngram coverage",
    # mutation/scheduling
    "grimoire structural", "mopt mutation", "calibrated energy",
    "aflfast rarity",
    # baseline / fallback
    "havoc-only", "token-replace", "other",
}
# When claimed_mechanism is in this set, verified_in_lineage must be true OR
# verification_method must explain (>= MIN_VMETHOD_LEN chars) why not.
#
# TODO(i2s-logging-bug): in the current LibAFL fuzzbench build, the literal
# string "I2SRandReplace" never lands in seed metadata because the cmplog
# harness does not wrap I2SRandReplace in LogMutationMetadata. The agent
# therefore verifies I2S via the dash-row floor signal (mutation_op = NULL
# in cmplog/vpc lineage; see tools/db_query.py lineage output and
# fuzzer_mechanism_library.md cmplog section). The rule below still works
# under the floor signal — verified_in_lineage=true when the agent cites a
# dash-row ancestor, false with an explanation otherwise. When the logging
# fix lands, no schema change is needed; only the agent-facing description
# in evidence_prompt.py needs to flip back to requiring the literal mutator
# name. Keep this MECHANISMS_REQUIRING_LINEAGE_CHECK set as-is.
MECHANISMS_REQUIRING_LINEAGE_CHECK = {"I2SRandReplace"}
MIN_VMETHOD_LEN = 20


def _normalize_whitespace(s):
    return re.sub(r"\s+", " ", s).strip()


def _sibling_prompt_path(analysis_path):
    """Map foo.analysis.json -> foo.prompt.md (or foo.md, .txt) as best-effort."""
    p = Path(analysis_path)
    name = p.name
    for ext in (".analysis.json",):
        if name.endswith(ext):
            base = name[: -len(ext)]
            for sib_ext in (".prompt.md", ".md", ".txt"):
                cand = p.with_name(base + sib_ext)
                if cand.is_file():
                    return cand
    # Fallback: drop the suffix
    return p.with_suffix("").with_suffix(".prompt.md")


def _decisive_pair_labels_from_prompt(prompt_text):
    """Extract 'cmplog>naive (I2S)' style labels from DECISIVE PAIRS lines.

    Lines look like:
        --- Pair 1: cmplog > naive  [delta: I2S] ---
    """
    out = []
    pat = re.compile(r"^---\s*Pair\s+\d+:\s*(\S+)\s*>\s*(\S+)\s*\[delta:\s*([^\]]+)\]",
                     re.MULTILINE)
    for m in pat.finditer(prompt_text):
        out.append(f"{m.group(1)}>{m.group(2)} ({m.group(3).strip()})")
    return out


def validate(analysis_path, prompt_path=None):
    """Return (ok, [violation_messages, ...])."""
    violations = []
    try:
        data = json.loads(Path(analysis_path).read_text())
    except json.JSONDecodeError as exc:
        return False, [f"FATAL: invalid JSON ({exc})"]

    if prompt_path is None:
        prompt_path = _sibling_prompt_path(analysis_path)
    if not Path(prompt_path).is_file():
        violations.append(f"WARN: sibling prompt not found at {prompt_path}; "
                          "skipping exact_quote and pair-label checks")
        prompt_text = None
    else:
        prompt_text = Path(prompt_path).read_text()

    # 1. required top-level fields
    for f in REQUIRED_TOPLEVEL:
        if f not in data:
            violations.append(f"missing required field: {f}")
        elif data[f] in (None, "", []):
            violations.append(f"empty required field: {f}")

    # 2. confidence value
    conf = data.get("confidence")
    if conf is not None and conf not in VALID_CONFIDENCE:
        violations.append(f"confidence must be one of {VALID_CONFIDENCE}, got {conf!r}")

    # 3. hypotheses structure
    hyps = data.get("hypotheses", [])
    if not isinstance(hyps, list) or not hyps:
        violations.append("hypotheses must be a non-empty list")
    else:
        for i, h in enumerate(hyps):
            if not isinstance(h, dict):
                violations.append(f"hypotheses[{i}] must be an object")
                continue
            for f in REQUIRED_HYPOTHESIS:
                if f not in h:
                    violations.append(f"hypotheses[{i}].{f} missing")
                elif h[f] in (None, "", []):
                    violations.append(f"hypotheses[{i}].{f} is empty")
            cov = h.get("covers_pairs", [])
            if not isinstance(cov, list) or not cov:
                violations.append(f"hypotheses[{i}].covers_pairs must be non-empty list")

    # 4. pair_decision <-> hypotheses count
    pd = data.get("pair_decision")
    if pd == "single_feature" and len(hyps) != 1:
        violations.append(f"pair_decision='single_feature' requires exactly 1 hypothesis, got {len(hyps)}")
    elif pd == "multi_feature" and len(hyps) < 2:
        violations.append(f"pair_decision='multi_feature' requires >=2 hypotheses, got {len(hyps)}")
    elif pd not in (None, "single_feature", "multi_feature"):
        violations.append(f"pair_decision must be 'single_feature' or 'multi_feature', got {pd!r}")

    # 5. evidence_trail structure + exact_quote check
    ev = data.get("evidence_trail", [])
    if not isinstance(ev, list) or not ev:
        violations.append("evidence_trail must be a non-empty list")
    else:
        prompt_normalized = _normalize_whitespace(prompt_text) if prompt_text else None
        for i, e in enumerate(ev):
            if not isinstance(e, dict):
                violations.append(f"evidence_trail[{i}] must be an object")
                continue
            for f in REQUIRED_EVIDENCE_ENTRY:
                if f not in e or not e[f]:
                    violations.append(f"evidence_trail[{i}].{f} missing or empty")
            cs = e.get("cited_section", "")
            # Accept canonical short name OR full section header (e.g.
            # "BYTE DIFF" or "BYTE DIFF (W vs L at common offsets)").
            if cs and not any(cs == canon or cs.startswith(canon + " ") or cs.startswith(canon + "\t")
                              for canon in VALID_CITED_SECTIONS):
                violations.append(
                    f"evidence_trail[{i}].cited_section {cs!r} does not match any "
                    f"canonical section name (allowed: {sorted(VALID_CITED_SECTIONS)})"
                )
            q = e.get("exact_quote")
            if q and prompt_normalized is not None:
                q_norm = _normalize_whitespace(q)
                if q_norm not in prompt_normalized:
                    snippet = (q[:60] + "...") if len(q) > 60 else q
                    violations.append(
                        f"evidence_trail[{i}].exact_quote not found in prompt: "
                        f"{snippet!r}"
                    )

    # 6. mechanism_consistency_check
    mcc = data.get("mechanism_consistency_check", {})
    if isinstance(mcc, dict):
        for f in REQUIRED_MCC:
            if f not in mcc or mcc[f] in (None, ""):
                violations.append(f"mechanism_consistency_check.{f} missing/empty")
        claim = mcc.get("claimed_mechanism", "")
        verified = mcc.get("verified_in_lineage")
        vmethod = mcc.get("verification_method", "")
        # Controlled vocabulary: claimed_mechanism must be one of the
        # enumerated values from the prompt schema.
        if claim and claim not in VALID_MECHANISMS:
            violations.append(
                f"mechanism_consistency_check.claimed_mechanism {claim!r} not in "
                f"valid set {sorted(VALID_MECHANISMS)}"
            )
        # verified_in_lineage must be a real boolean, not None/string.
        if verified is not None and not isinstance(verified, bool):
            violations.append(
                f"mechanism_consistency_check.verified_in_lineage must be true or false, "
                f"got {verified!r}"
            )
        # Mandatory lineage verification for I2S-class claims.
        if claim in MECHANISMS_REQUIRING_LINEAGE_CHECK and verified is not True:
            if not vmethod or len(vmethod) < MIN_VMETHOD_LEN:
                violations.append(
                    f"claimed_mechanism={claim!r} requires either verified_in_lineage=true "
                    f"(after running db_query.py lineage) OR a verification_method >= "
                    f"{MIN_VMETHOD_LEN} chars explaining why verification was not possible."
                )
        # mechanism_attribution (from each hypothesis) and claimed_mechanism
        # should be consistent. We can't do strict NLP matching, but we can
        # flag the obvious case where the agent contradicts itself by
        # naming a different technique outright (e.g., claim="havoc-only"
        # but mechanism_attribution mentions I2SRandReplace).
        #
        # Only meaningful for single_feature: the top-level claimed_mechanism
        # describes the whole branch, so a hypothesis naming a DIFFERENT
        # technique is a contradiction. For multi_feature, distinct hypotheses
        # legitimately attribute distinct mechanisms (e.g. one I2S hypothesis +
        # one "grimoire structural" hypothesis on the same gate), so a global
        # "must all match the one claimed_mechanism" check would false-positive.
        pair_decision = data.get("pair_decision")
        if claim in VALID_MECHANISMS and pair_decision == "single_feature":
            other_mechs = VALID_MECHANISMS - {claim, "other"}
            for i, h in enumerate(hyps if isinstance(hyps, list) else []):
                if not isinstance(h, dict):
                    continue
                ma = (h.get("mechanism_attribution") or "")
                for other in other_mechs:
                    # Don't fire on substring overlaps (e.g. "havoc" inside
                    # "havoc-only"); use exact-token match.
                    if re.search(rf"\b{re.escape(other)}\b", ma):
                        violations.append(
                            f"hypotheses[{i}].mechanism_attribution mentions "
                            f"{other!r} but mechanism_consistency_check.claimed_mechanism "
                            f"is {claim!r} — they must agree on one technique."
                        )
                        break
    else:
        violations.append("mechanism_consistency_check must be an object")

    # 7. falsifiability
    falsi = data.get("falsifiability", {})
    if not isinstance(falsi, dict) or not falsi.get("would_be_refuted_by"):
        violations.append("falsifiability.would_be_refuted_by missing/empty")

    # 8. covers_pairs labels (cross-check against prompt's DECISIVE PAIRS)
    if prompt_text:
        valid_pairs = set(_decisive_pair_labels_from_prompt(prompt_text))
        if valid_pairs:
            for i, h in enumerate(hyps):
                cov = h.get("covers_pairs", [])
                for label in cov if isinstance(cov, list) else []:
                    if label not in valid_pairs:
                        violations.append(
                            f"hypotheses[{i}].covers_pairs entry {label!r} not in "
                            f"prompt's DECISIVE PAIRS labels: {sorted(valid_pairs)}"
                        )

    return (not violations, violations)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="analysis.json files (or dirs with --recursive)")
    ap.add_argument("--recursive", action="store_true",
                    help="treat positional args as directories; recurse for *.analysis.json")
    ap.add_argument("--prompt", help="explicit prompt path (only valid with a single analysis arg)")
    args = ap.parse_args()

    if not args.paths:
        ap.error("at least one path required")

    files = []
    for p in args.paths:
        pp = Path(p)
        if args.recursive and pp.is_dir():
            files.extend(sorted(pp.rglob("*.analysis.json")))
        elif pp.is_file():
            files.append(pp)
        else:
            print(f"skip: {p} (not a file; pass --recursive for directories)",
                  file=sys.stderr)
    if not files:
        print("no analysis files matched", file=sys.stderr)
        sys.exit(2)

    n_ok = 0
    n_fail = 0
    for f in files:
        prompt_path = Path(args.prompt) if args.prompt else None
        ok, vio = validate(f, prompt_path)
        if ok:
            n_ok += 1
            print(f"OK   {f}")
        else:
            n_fail += 1
            print(f"FAIL {f}  ({len(vio)} violation(s))")
            for v in vio:
                print(f"     - {v}")

    print(f"\nsummary: {n_ok} OK, {n_fail} FAIL  ({len(files)} total)")
    sys.exit(0 if n_fail == 0 else 1)


if __name__ == "__main__":
    main()
