#!/usr/bin/env python3
"""
build_signature_cards.py — build Pass-A distiller input cards for ONE mechanism family.

Selects every hypothesis whose `covers_pairs` maps (via
`mechanism_family.coarse_family`) to --family, and emits one "card" per
hypothesis: the deterministic locators (target/branch/file/function/line,
joined from the candidates CSV) plus the four free-text fields the distiller
normalizes into a structured signature.

The distiller itself is an agent that reads ONE card in isolation and writes a
signature; this driver only prepares its inputs. The agent contract (schema +
rules) lives in .claude/agents/hypothesis-signature-distiller.md — dispatch
with subagent_type "hypothesis-signature-distiller", giving it the cards path,
the card ids, and an output path.

  python3 tools/build_signature_cards.py --family I2S_pro \
      --out step5a/I2S_pro.cards.json
"""

import argparse
import csv
import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mechanism_family import coarse_family  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["what_input_feature", "why_winner_satisfies",
          "why_loser_doesnt", "mechanism_attribution"]


def load_locators(candidates_csv):
    out = {}
    with open(candidates_csv) as f:
        for r in csv.DictReader(f):
            out[(r["target"], int(r["branch_id"]))] = {
                "file": r["file"], "function": r["function"],
                "line": r["line"], "source_line": r["source_line"],
            }
    return out


def build_cards(family, glob_pat, candidates_csv):
    loc = load_locators(candidates_csv)
    cards = []
    for f in sorted(glob.glob(str(REPO_ROOT / glob_pat), recursive=True)):
        if "/_examples/" in f:
            continue
        d = json.load(open(f))
        hyps = d.get("hypotheses", [])
        for i, h in enumerate(hyps):
            fam = coarse_family(h.get("covers_pairs", []))
            if fam != family:
                continue
            key = (d["target"], int(d["branch_id"]))
            cid = f"{d['target']}_{d['branch_id']}" + (f"_h{i}" if len(hyps) > 1 else "")
            cards.append({
                "id": cid,
                "family": fam,
                "target": d["target"],
                "branch_id": d["branch_id"],
                "analysis_path": str(Path(f).relative_to(REPO_ROOT)),
                **loc.get(key, {"file": "", "function": "", "line": "", "source_line": ""}),
                "covers_pairs": h.get("covers_pairs", []),
                **{k: h.get(k, "") for k in FIELDS},
            })
    return cards


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--family", required=True)
    ap.add_argument("--glob", default="prompts/**/*.analysis.json")
    ap.add_argument("--candidates", default=str(REPO_ROOT / "csvs" / "blocker_candidates.csv"))
    ap.add_argument("--out", default="-")
    a = ap.parse_args()
    cards = build_cards(a.family, a.glob, a.candidates)
    js = json.dumps(cards, indent=2)
    if a.out == "-":
        print(js)
    else:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(js)
        print(f"wrote {len(cards)} {a.family} cards to {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
