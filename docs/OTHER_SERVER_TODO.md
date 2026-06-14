# Other-server TODO — score the benchmark on YOUR targets

You are Claude on the **second server** of the BlockerAnalyzer benchmark pivot.
Server "s4" (curl/harfbuzz/openthread/sqlite3) already built the shared pipeline
and scored its targets. Your job: run the **same deterministic pipeline** on
**your** targets (lcms / libxml2 / libpng / bloaty) and push your results back so
the two halves merge into one dataset.

Read `docs/benchmark_pivot_spec.md` first for the full design. This file is the
operational checklist. **Nothing here regenerates hypotheses or rebuilds tools —
the design (`step5b_new_v3/*/evidence_test.json`) and the tools are shared and
fixed.** You only *measure + arbitrate* on your corpora.

> **⚠ RE-RUN REQUIRED (2026-06-13) if you already scored once.** Two tool fixes
> landed after the first multi-server merge, so `assignments_sB.json` produced
> before this date must be regenerated:
> 1. **Deterministic corpus sampling.** `load_corpus_sample` used `random.sample`,
>    so `signed_target_enrich` depended on RNG state and was *not reproducible*
>    across runs (it flipped borderline labels — e.g. a corpus > the sample cap
>    gave ste −0.589 vs −0.293 on two runs). It now sorts + even-strides
>    (no RNG), and the cap was raised to `--sample 20000`. Re-run the OE study so
>    your cache is stable.
> 2. **OE cache is now server-suffixed.** The arbiter reads
>    `csvs/arb_operand_enrich_<SERVER>.csv` (falling back to the unsuffixed name),
>    and `_rescore_after_bisect.sh` now WRITES that suffixed file. So a re-run
>    overwrites *your* `arb_operand_enrich_sB.csv` and the arbiter picks it up.
>    (Before this fix a re-run wrote the unsuffixed file while the arbiter kept
>    reading your stale suffixed cache — no effect.)
>
> To re-run: `git pull`, then
> `export BENCH_SERVER=sB BENCH_ONDISK=lcms,libxml2,libpng,bloaty` and
> `./bench/_rescore_after_bisect.sh` (now env-respecting + deterministic). Sanity:
> run `i2s_operand_availability.py branch ...` twice — output must be byte-identical.
> Then push the refreshed `assignments_sB.json` back. Note: degenerate `ste≈17`
> values in the first run came from near-zero `naive_frac` (log2 of ~EPS); the
> full-corpus deterministic read will stabilize the magnitude (the label holds).

> **⚠ RE-RUN ALSO REQUIRED (2026-06-14) — two NEW tools + a target-routing fix.**
> `git pull` then re-arbitrate (`arbitrate.py --all`). Three changes land:
> 1. **Two new measurement tools — and their candidates are almost all YOUR
>    targets.** `bench/tools/corpus_size_ratio.py` (corpus inflation /
>    homogenization) and `bench/tools/token_count.py` (grimoire `<GAP>` literal
>    erasure) are now built + wired into the arbiter. They were previously the
>    `*` unbuilt tools behind 4 *decidable* empty clusters whose members are
>    libxml2/libpng/lcms. **s4 scored 0 of them (no corpus); you score the real
>    ones.** Re-anchor both (§3) and re-arbitrate. Neither needs Docker — pure
>    corpus/seed reads (cheaper than `depth_reach`).
> 2. **branch_id target-routing fix (load-bearing for you).** `branch_id` is
>    globally unique, but 4 shapes carried a *stale/wrong* target-prefix in their
>    signature ids — e.g. `libxml2_6210`/`libxml2_6616` are really **harfbuzz**
>    branches (s4), and `bloaty_301`/`bloaty_141` are really **curl** (s4). The
>    arbiter + `build_dataset` now resolve target from `branches.target` (the DB),
>    not the id prefix. **Effect on you:** those mis-prefixed rows that *look* like
>    your targets (libxml2/bloaty) are correctly skipped as s4's — so you won't
>    waste a scan reading the wrong corpus, and you won't emit a bogus
>    `assignments_sB.json` row for a branch that isn't yours. (Requires the
>    `branches` row to exist in YOUR db; it always does for your own branches.)
> 3. **Arbiter merge is now deterministic** (`sorted(needed)`) and
>    `corpus_size_ratio` is memoized per (target, arm-pair) so a 100k-file corpus
>    is scanned once, not per branch. No action — just faster + stable diffs.

> **⚠ RE-ARBITRATE REQUIRED (2026-06-14) — branch_id collision residue.**
> `branch_id` is NOT globally unique across servers (each DB numbers independently),
> so `bloaty_57` (yours) and `curl_57` (s4) are DIFFERENT branches. An earlier
> build_dataset/arbitrate bug resolved target from the local DB by bare id, so each
> server SCORED the OTHER server's colliding branches against its OWN (wrong) corpus
> and wrote them into its assignments. Code is now fixed (commit `da8ff06`: the
> signature-id PREFIX is authoritative + a DB-consistency guard), **but the fix is
> code-only — committed assignments still carry the residue.** s4 already re-ran and
> cleared 92 bogus entries; **you must `git pull` then re-run `arbitrate.py --all`**
> to drop your s4-prefixed residue (~78 entries), then rebuild + push. Verify:
> `grep -hoE '"branch": "(curl|harfbuzz|openthread|sqlite3)_[0-9]+' step5b_new_v3/*/assignments_sB.json | wc -l`
> must be **0** after re-arbitrating.

## 0. What you have vs what was shipped

- **You have (local, NOT in git):** your `db/blockers.sqlite` (your targets'
  branches + seeds), your corpora at `out/` (symlink to your campaign root).
- **Shipped to you (the shared layer — see the file manifest at the bottom):**
  the 38 `evidence_test.json` design specs, the measurement tools, the arbiter,
  the dataset builder, the registry, this doc, and s4's `assignments_s4.json`.

## 1. Configure (env, no code edits)

```bash
export BENCH_SERVER=sB                              # your server tag
export BENCH_ONDISK=lcms,libxml2,libpng,bloaty      # YOUR on-disk targets
```
The arbiter/build_dataset read these; they default to s4's targets otherwise.

## 2. Make sure your branches have enough seeds (>=3 resolving AND >=3 blocking)

The measurement tools need >=3 resolving + >=3 blocking seeds per branch.
**Lesson from s4:** the initial `seed_bisect` at `--fallback-ranks 3` captured
only 1-2 resolving seeds for hard branches even though they resolved in 8-10
trials. Re-bisect at rank 10 to recover them (idempotent, `ON CONFLICT UPDATE`):

```bash
# find YOUR branches with <3 resolving or <3 blocking seeds, write per-target CSVs
# (filter csvs/blocker_representatives*.csv to those branch_ids), then:
python3 tools/seed_bisect.py run --target <T> --queue-base ./out \
    --branches-from-csv csvs/sparse_<T>.csv --fallback-ranks 10
```
The 10-bucket bisection is ~log-cost per trial; expect ~10-40 min/target on a
slow FS. (s4's harfbuzz took ~40 min for 36 branches × 9 trial-queues.)

## 3. RE-ANCHOR each tool on one of YOUR targets  ← THE CRITICAL GATE

A tool validated on harfbuzz is **not** automatically trustworthy on libxml2 —
s4 saw the `operand_enrichment` separation weaken on sqlite3, and per-target
calibration is the spec's known risk. **Before mass-running, validate each tool
on a known branch of yours and confirm the expected direction; re-tune the
threshold in the arbiter's canonical rules if the separation is weaker.**

- `bench/tools/i2s_operand_availability.py branch --target libxml2 --branch-id <a known i2s-pro branch>`
  → expect `signed_target_enrich > 0` (pro) / `< 0` (anti). If the band is
  compressed vs s4's +3.12/-0.55, loosen the rule thresholds.
- `bench/tools/value_distance_reached.py branch --target <T> --branch-id <vp-gradient branch> --value <operand> --winners value_profile,value_profile_cmplog --losers cmplog,naive`
  → expect `winner_closer=true`, `distance_gap` > 0.
- `bench/tools/joint_necessity.py branch --target <T> --branch-id <vpc-both branch>`
  → expect `joint_confirmed` (or `i2s_necessary_value_subtype`).
- `bench/tools/joint_necessity.py branch --target libxml2 --branch-id <grimoire branch> --winner-fuzzer grimoire --loser-fuzzer cmplog --tokens '<?xml,<!DOCTYPE,...'`
  → expect grimoire `tag_lift >= 1`.
- `bench/tools/depth_reach.py ...` (ctx/ngram) — re-anchor on a local ctx branch.
- `bench/tools/corpus_size_ratio.py branch --target libxml2 --branch-id <any> --winner-fuzzer cmplog --loser-fuzzer naive`
  → expect `corpus_count_ratio` > 1 (the I2S arm hoards more saved seeds; s4 saw
  harfbuzz cmplog/naive ≈ 2.7×). Also test the **ctx** arm pair
  `--winner-fuzzer naive_ctx --loser-fuzzer naive` (the `ctx_coverage_LW` rule
  wants `corpus_count_ratio >= 1.5`). This tool is **branch-independent**
  (whole-corpus arm comparison) and reads the on-disk queue directly — no DB
  seeds, no Docker. If your corpora don't show inflation, the inflation/
  homogenization hypotheses honestly stay inconclusive (G3 — fine, not a tuning
  failure). `composition_entropy_ratio < 0.85` (LWLW homogenization) is the
  stricter clause; confirm the entropy ratio is a sane ~0.5–1.5 on a known branch.
- `bench/tools/token_count.py branch --target libpng --branch-id 3892 --literal 0x03 --winner-fuzzer naive --loser-fuzzer grimoire`
  (and `--target libxml2 --branch-id 6597 --literal 0x09`) — these are the **real
  `grimoire_structural_LW` members**, so this is a direct anchor *and* score.
  Expect `naive_literal_count >= 1 AND literal_presence_ratio < 1` (grimoire's
  `<GAP>` stage depletes the literal; the rule fires at `< 0.34`). Needs the
  branch's resolving (naive) + blocking (grimoire) seeds bisected first (§2);
  reads on-disk seed bytes, no Docker.

Per-target structural tokens are already wired in `bench/arbitrate.py:shape_tokens`
for libxml2 (XML/DTD) and lcms (ICC tags); add your targets if missing. The new
tools' shape→arm pairs (`CS_ARMS`, `TC_ARMS`) and gate literals (from each
signature's `operand_literal`) are already wired for the shared shapes — nothing
to add unless you introduce a new shape.

## 4. Pre-run operand_enrichment (corpus-heavy → do it once in study mode)

```bash
# build a label CSV of YOUR local i2s_vp branches with >=3 W & >=3 L seeds, then:
python3 bench/tools/i2s_operand_availability.py study --label-csv csvs/arb_oe_labels.csv \
    --out csvs/arb_operand_enrich.csv --sample 8000 --head 256
```
(See `bench/_rescore_after_bisect.sh` for the exact label-CSV builder s4 used —
copy it, it's target-agnostic.)

## 5. Arbitrate → your assignments

```bash
BENCH_SERVER=sB BENCH_ONDISK=lcms,libxml2,libpng,bloaty python3 bench/arbitrate.py --all
```
This writes `step5b_new_v3/<shape>/assignments_sB.json` (your branches only;
non-local → skipped). It reuses the cached `operand_enrichment` + runs
`joint_necessity` / `value_distance_reached` / `depth_reach` per branch.

Expected coverage on your side: **i2s/vp ~194 branches + grimoire ~32 + ctx ~36**
are the bulk. ctx/ngram use `depth_reach` (built; verifies the iteration-depth subtype, context-reach subtype stays inconclusive).
`corpus_size_ratio` (ctx_coverage_LW, i2s_vp_LWLW/L__W) + `token_count`
(grimoire_structural_LW) now also run in `--all` — these target YOUR branches
specifically (s4 had no corpus for them), so expect a few extra labels iff your
corpora show the inflation / literal-erasure the rules predict.

## 6. Merge to the full dataset

Pull s4's `step5b_new_v3/*/assignments_s4.json` (shipped), then:
```bash
python3 bench/build_dataset.py        # merges assignments_*.json across servers
```
`build_dataset` enumerates ALL signature branches and prefers `validated` over
`inconclusive`, so the output `bench/dataset.jsonl` is the combined benchmark.
Push your `assignments_sB.json` back so s4 can also rebuild the merged set.

## 7. (Optional, LAST) re-design only RESISTANT shapes

Only after seeds + tools are complete: if a shape comes back with a *wall* of
inconclusive (menu likely missed a mechanism), re-invoke the
`evidence-test-author` agent on that shape with the inconclusive branches'
evidence (spec §8.4, bounded ≤2 rounds). **Do NOT chase 100% assignment** —
honest `inconclusive` (the test ran, mechanism didn't hold) and `decidable:false`
(corpus-scale / non-discriminable) are correct outcomes (guardrail G3).

## Gotchas
- The shared `step5a_new_v3/*/signatures.json` lists BOTH servers' branches; the
  arbiter filters to `BENCH_ONDISK` and queries YOUR db, so non-local rows are
  simply skipped — no conflict.
- Don't edit `evidence_test.json` rules; reconcile metric-name mismatches via the
  arbiter's canonical-rule fallbacks (already handle value_distance + token
  families), not by rewriting agent output.
- `out/` and `db/` are local; never commit them. Only `assignments_sB.json` +
  any new `csvs/*` you want to share travel back.

---

## File manifest — what s4 must ship you (the shared layer)

```
step5a_new_v3/<shape>/{signatures.json, cards.json}     # 38 shapes — branch source + design input
step5b_new_v3/<shape>/evidence_test.json                # 38 — the design specs (the rules you apply)
step5b_new_v3/<shape>/assignments_s4.json               # s4's results (for the final merge; can come later)
bench/tools/joint_necessity.py                          # measurement tools
bench/tools/value_distance_reached.py
bench/tools/depth_reach.py                              # ctx/ngram (built; needs your libafl-<target>-cov Docker images)
bench/tools/corpus_size_ratio.py                        # NEW (2026-06-14) corpus inflation/homogenization (no Docker)
bench/tools/token_count.py                              # NEW (2026-06-14) grimoire <GAP> literal erasure (no Docker)
bench/arbitrate.py                                      # the deterministic arbiter
bench/build_dataset.py                                  # dataset assembler/merger
bench/tool_registry.json                                # tool catalog (reference)
bench/_rescore_after_bisect.sh                          # the OE-label + rescore chain (copy/adapt)
bench/tools/i2s_operand_availability.py                       # operand_enrichment (Leg-1 tool)
tests/test_bench_tools.py                               # tool/arbiter/dataset invariants (pytest; corpus checks skip w/o corpora)
docs/benchmark_pivot_spec.md                            # full design
docs/OTHER_SERVER_TODO.md                               # this file
.claude/agents/evidence-test-author.md                  # design agent (only for §7 re-design)
```
NOT needed: s4's `db/`, `out/`, `csvs/arb_operand_enrich.csv` (you regenerate
these on your own corpora/DB).
