# tools/ — step → tool map

The metaphorical-testing pipeline tools, grouped by pipeline step. **Filenames
are deliberately NOT step-prefixed**: the tools import each other as flat
siblings (each does `sys.path.insert(0, TOOLS_DIR)` then `from <sibling>
import …`), so a `stepN_` rename or subfolder move would break those imports
and every `python3 tools/<x>.py` invocation path. This table is the mapping
instead. Full CLI/flags/schema per tool live in [`../docs/TOOLS.md`](../docs/TOOLS.md);
the phase ordering is the "Typical Workflow" section of [`../CLAUDE.md`](../CLAUDE.md).

| Step | Tool | One-liner |
|------|------|-----------|
| shared lib | `blocker_db.py` | SQLite schema owner + `init` (population done by study_units / seed_bisect) |
| shared lib | `seed_utils.py` | Dependency-free seed/byte helpers (parse_count, hex_dump, read_seed_bytes, format_seed_block, byte_diff_section) |
| shared lib | `extract_functions.py` | `llvm-cov export` → (file, name, start, end) ranges; library (no CLI) |
| **1** significance | `subject_significance.py` | Per-(target, A, B) AUC + final-coverage MW U-test; **source of truth for CANONICAL_TARGETS / FUZZERS / PAIRS** |
| **2** DB population | `study_units.py` | Per-target coverage walk + per-subject admission (`add-canonical`); hosts the `evidence-per-branch` CLI |
| **3a** candidates | `build_candidates.py` | Per-branch ≥8/≥8 decisive aggregation → `blocker_candidates.csv` |
| **3b** representatives | `select_representatives.py` | Decisive-shape × region dedup → `blocker_representatives.csv` + dedup map |
| **3.5** seeds | `seed_bisect.py` | Docker 10-bucket bisection → resolving/blocking seed tables |
| **3.6** callers | `callers_index.py` | One-time per-target source-grep callers index |
| **3.7** per-role cov | `per_role_coverage.py` | W (resolving) / L (blocking) llvm-cov dumps → SOURCE CONTEXT overlay |
| **4a** fan-out | `run_hypothesis_fanout.py` | Manifest + per-rep prompt builder (does NOT dispatch agents) |
| **4a** prompt | `evidence_prompt.py` | Per-branch structured-prompt assembly; registers `evidence-per-branch` into study_units |
| **4c** validate | `check_analysis.py` | Validate agent `.analysis.json` vs sibling prompt (exact_quote hallucination filter) |
| **4** agent pull | `db_query.py` | Agent-facing pull queries (lineage, more-seeds) |
| **5a** classify | `mechanism_family.py` | `coarse_family(covers_pairs)` → per-technique pro/anti families (10 techniques) + I2S×VP synergy/independent |
| **5a** classify | `build_signature_cards.py` | Per-family distiller cards for the signature-distiller agent |
| **5b** author/verify | `build_template_briefs.py` | Per-cluster authoring brief → `step5b/briefs/<id>.json` |
| **5b** author/verify | `check_template.py` | Preflight: schema/fuzzer sanity + scan_value compile + dead-knob detection |
| **5b** author/verify | `verify_template.py` | Synthetic-harness sweep runner (serial `--jobs 1`) → `verification_run.json` |
| **5b** author/verify | `run_full_verify.py` | Full parallel verification driver over all `step5b/` templates (reuses verify_template) |
| **5b** author/verify | `screen_templates.py` | Fast 1-trial screening sweep (decisive pair only) across templates |
| auxiliary | `plot_coverage_curves.py` | Coverage-by-time spaghetti plot → `out/coverage_curves.png` |

(Data, not a tool: `../fuzzer_mechanism_library.md` — per-fuzzer mechanism
paragraphs spliced into Step-4 prompts. Pipeline **agents** are not tools —
see the Agents table in `../CLAUDE.md`.)
