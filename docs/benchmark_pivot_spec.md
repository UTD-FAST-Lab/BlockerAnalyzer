# Step 5 Pivot — Mechanism-Labeled Real-Branch Benchmark

**Status:** spec, locked 2026-06-12 (supersedes the synthesize-and-verify
framing of step 5b). Decisions in this doc were converged with the user
2026-06-12; see [[project_benchmark_pivot_2026-06-12]],
[[project_i2s_sign_discriminator_2026-06-12]].

**Why:** the repeated "non-synthesizable" verdicts
([[project_v3_decisive_set_reclassification_2026-06-11]]) are the
synthesize-a-mini-program frame breaking on a *class* of features. Magic-gate /
gradient blockers are **local** (a few lines) → a mini-program contains them.
Corpus contamination, budget drain, joint-necessity, scheduling, ctx/ngram/
grimoire coverage are **non-local** — properties of the *whole target* (its
control-flow shape, its corpus's byte distribution, the scheduler over thousands
of queue entries). No mini-program can contain a feature whose substrate *is* the
program + campaign. Leg 1 (`bench/tools/i2s_operand_availability.py`) proved the
alternative: a "non-synthesizable" hypothesis validated **directly on the real
campaign corpora**, 88% pro/anti separation, no synthesis.

---

## 1. The deliverable

A **mechanism-labeled benchmark of fuzzer-discriminating blockers**: the decisive
branches (≥8/≥8 rule, already in the DB), each annotated with an
*evidence-confirmed* mechanism label, packaged so a new fuzzer / technique-combo
is scored by **which mechanism classes of blocker it resolves**.

Three artifacts:
1. `bench/dataset.jsonl` — one row per labeled branch (§6).
2. `bench/tools/` + `bench/tool_registry.json` — the deterministic measurement
   tools + their catalog (§4, §5).
3. `tools/bench_score.py` — given a new fuzzer's campaign, report its resolve-rate
   **per mechanism class** (§10).

Success = a branch carries a mechanism label backed by a falsifiable,
discriminating real-data signature — *not* "a synthetic template reproduced."

---

## 2. The classification → evidence flow (three layers)

The spine is the **decisive shape**, not the mechanism. A branch is *not*
pre-sorted into "the i2s-anti family"; it gets a deterministic shape, and its
mechanism is an **output of the evidence**. This is what dissolves the old
"a branch is both i2s-anti and joint" non-cleanness — mechanism stops being an
input.

- **Layer 1 — deterministic shape split (the spine).** `mechanism_family_v3.py`
  → a 4-position code over `cmp,vp,vpc,naive` (W=resolve≥8, L=block≥8,
  `_`=non-decisive). Each branch has **exactly one** shape. This already
  separates pro from anti *per technique* (`i2s_vp_WLWL` = i2s-pro vs
  `i2s_vp_LW_W` = i2s-anti; `ctx_coverage_WL` vs `ctx_coverage_LW`). **38 shape
  buckets** (verified 2026-06-12).
- **Layer 2 — candidate hypothesis menu (per shape), DISCOVERED by the design
  agent.** Its input is the shape's **per-branch Pass-A signatures**
  (`step5a_new_v3/<shape>/signatures.json`); the agent discovers + collapses the
  candidate hypotheses itself. The 100 prior Pass-B clusters are handed in as an
  **optional, non-authoritative reference seed menu** (a hint), not the input of
  record. There is no per-origin-cluster artifact.
- **Layer 3 — evidence (design + arbiter).** The design agent collapses the menu
  to what real data can discriminate and emits a decision rule; the deterministic
  arbiter assigns each branch its evidence-confirmed label / `refuted` /
  `inconclusive`. **Evidence is the arbiter — it can reassign a branch** the
  prior clustering put elsewhere.

### Pass B is dropped; Pass A is consolidated (not re-run)
The design agent's menu-discovery + collapse **is** classification, so the
separate `signature-feature-classifier` (Pass B) is redundant going forward —
retired. **Pass A** (`hypothesis-signature-distiller`) output already exists
per-shape in `step5a_new_v2/` (38 `signatures.json`, 28 `cards.json`); we do NOT
re-run the distiller agents (the analyses haven't changed). We **consolidate**
into `step5a_new_v3/<shape>/{signatures.json, cards.json}` — copy the 38
signatures, complete the ~10 missing cards deterministically
(`build_signature_cards.py`) — so every shape has exactly one of each as the
design agent's input.

**Lean flow:** generate (4b) → deterministic shape split → consolidate Pass-A
signatures (`step5a_new_v3`) → **`evidence-test-author` agent** (discover +
collapse menu + design test) → **deterministic arbiter** (assign) → bounded
re-round on inconclusive shapes.

---

## 3. Agent & tool architecture — who does what

The benchmark backbone must be reproducible, so the only LLM judgment is *design*;
measurement and per-branch assignment are deterministic.

| component | owner | count | nature |
|---|---|---|---|
| **`evidence-test-author` agent** (the "design agent") | LLM, parallel | **×38 (per shape)** | reads candidate menu → collapses to discriminable set → emits {collapsed hypotheses, normalized measurement **descriptors**, decision rule}. Does NOT write tools or make the per-branch call. The pivot's analog of `template-author`. |
| core measurement tools | engineered (orchestrator), reviewed | **~8–11** | deterministic; one per technique-signature; reused across shapes/directions; live in `bench/tools/`. NOT agent-written. |
| generic arbiter | engineered | **1** | applies any shape's decision-rule spec per branch → label/refuted/inconclusive |
| dataset builder | engineered | **1** | assembles `bench/dataset.jsonl` from all `assignments.json` |
| synthetic sidecar agents (`template-author`/`verdict-adjudicator`/`hypothesis-reviser`) | LLM | demoted | local families only (§11) |

**Tool correctness (trust mechanism, not self-certification):** every tool must
(a) reproduce a **known answer on an anchor branch** we understand from source
*before* running on the full set (Leg 1: branch 5391 → `signed=−1.5`), (b)
produce a **sensible pro/anti separation**, and (c) pass an **independent
`/code-review`** (reviewer ≠ author). Build → run → assign is otherwise
deterministic; no LLM in the per-branch loop.

**Build timing:** just-in-time, per family, in build order — not all upfront. A
tool's shape only crystallizes once the design exposes the hypotheses (Leg 1's
`no_gate_signature` skip *became* the no-operand discriminator). Order: design
(agent) → build tool to spec → validate on anchor → arbiter runs. Tool #1
(operand-enrichment) done.

---

## 4. Parallel design + build-time dedup (the no-duplicate-tools guarantee)

Design agents run **in parallel** (flat fan-out, like 4b). They have no live
shared state, so **duplicate tool specs across shapes are expected and fine** —
because nothing is built from a spec directly. The **build step is the
deterministic dedup gate, owned by the orchestrator:**

- identical measurement → build once; other specs become references;
- same measurement, different threshold/param → **one parameterized tool**;
- genuinely new → build + register in `bench/tool_registry.json`.

So duplicate *specs* are free; duplicate *tools* never get built.

**This requires a normalized measurement descriptor** so two parallel specs for
the same measurement collapse to the same key automatically (not me reading 38
prose specs). The agent designs the *discriminator + rule* in free text, but
names its *measurements* in a **closed descriptor vocabulary**:

```jsonc
{ "source": "corpus_queue | seed_lineage | coverage_timeseries | exec_stats | source_cfg",
  "compute": "<closed verb>",      // e.g. byte_freq_ratio, value_enrichment, event_cooccurrence,
                                    //      corpus_size_ratio, plateau_time, energy_share, depth_reach
  "operand": "<what>",             // e.g. {target_value, decoy_value} | {i2s_event, gradient_event}
  "unit": "per_gate_offset | per_branch | per_trial | per_seed" }
```

Two shapes emitting `{corpus_queue, byte_freq_ratio, {target,decoy}, per_gate_offset}`
map to the *same tool* regardless of prose. Reuse is *informative*: a descriptor
many shapes request = a real general mechanism-signature (bottom-up validation of
the category map); a descriptor only one shape needs = a flag for a distinct/rare
mechanism or a misclassified singleton.

`bench/tool_registry.json`: `{ descriptor_key → {tool_path, params, metrics,
anchor_branch, review_status} }`.

---

## 5. Evidence-rigor guardrails (load-bearing — the pivot fails without them)

Without the synthetic knob, the bar moves to:
- **G1 — Falsifiable & discriminating.** Every label states a prediction about a
  *measured* quantity that (a) could come out the other way and (b) an
  *alternative* mechanism would predict differently. Report where it fails.
  (Leg 1: pro→enrich, anti→deplete; could have been flat; separated 88%.)
- **G2 — Independence of label-source and verification-signal.** Label from
  source-level analysis (`.analysis.json`); verification from an *independent*
  campaign measurement. Never label by signal X and verify X with X.
- **G3 — Report the negative.** Refuted/inconclusive branches stay in the
  dataset, labeled as such; never dropped.

`evidence_status ∈ {validated, refuted, inconclusive, unvalidated}`, set by the
arbiter, not by hand.

---

## 6. Dataset schema (`bench/dataset.jsonl`, one object per branch)

```jsonc
{
  "branch_id": 5391, "target": "harfbuzz",
  "loc": {"file": "src/hb-open-file.hh", "function": "OT::OpenTypeFontFile::get_face", "line": 490},
  "build": "docker/targets/Dockerfile.harfbuzz.cov",
  "decisive_shape": {"code": "LW_W", "resolve": ["value_profile","naive"],
                     "block": ["cmplog"], "nondecisive": ["value_profile_cmplog"]},
  "per_arm": {"cmplog": {"n_resolved":1,"n_blocked":9}, "value_profile": {"n_resolved":8,"n_blocked":1},
              "naive": {"n_resolved":7,"n_blocked":3}, "value_profile_cmplog": {"n_resolved":6,"n_blocked":2}},
  "mechanism": {"label": "i2s_splices_decoy_depletes_target", "direction": "anti",
                "candidate_source": "step5b_new_v3/i2s_vp_LW_W/evidence_test.json (design-discovered)",
                "analysis_path": "prompts_b/harfbuzz_5391.analysis.json"},   // label SOURCE (G2)
  "evidence": {"status": "validated", "test": "corpus_operand_enrichment",
               "descriptor": {"source":"corpus_queue","compute":"byte_freq_ratio","operand":{"target":"...","decoy":"..."},"unit":"per_gate_offset"},
               "metric": {"signed_target_enrich": -1.56, "decoy_enrich": 5.63},
               "prediction": "anti -> signed_target_enrich < 0", "rule": "signed < -0.3",
               "report": "step5b_new_v3/i2s_vp_LW_W/assignments.json"},
  "synthetic_sidecar": {"status": "n/a"},        // local families only; else n/a
  "seeds": {"resolving": 4, "blocking": 10},
  "gate_locality": "nonlocal"
}
```

**Dataset unit & rep expansion.** The working unit is the **representative
branch** — the ~286 reps already analyzed *and* seeded (kept; rep-selection is
NOT dropped, since that would need fresh 4b analysis for no real gain). Because
the arbiter labels by *measurement*, the dataset can be **expanded on demand** at
build time via `csvs/blocker_dedup_map-new.csv`: each rep's represented near-dups
(same shape × source-region) **inherit the rep's mechanism label**, and the
arbiter confirms any that have seeds. So `dataset.jsonl` ships the rep set now and
can grow to the full decisive set (~400) later **without re-running any agent** —
"more test points per mechanism" is a free dataset-build option, not a pipeline
change.

**Multi-cluster branches (~138, the `_h0/_h1` joint halves).** A branch still has
**one shape**; the multi-membership is *within* its shape. A *joint* candidate's
row simply requires **both** half-tests to pass. The arbiter handles "this branch
carries ≥1 candidate; assign the supported one; for a joint candidate, both
halves must hold."

---

## 7. Mechanism families & locality (the evidence test per family)

`local` → optional synthetic sidecar; `nonlocal` → real-evidence only. Pro/anti
are separate (opposite predicted sign of the *same* shared tool).

| family | locality | discriminating real-data prediction (G1) |
|---|---|---|
| i2s literal substitution (magic/FOURCC) | local | resolving value IS a harvestable CMP operand; cmplog corpus enriched (signed > 0) |
| i2s operand-availability (anti / decoy) | **nonlocal** | cmplog corpus **depleted** of target, enriched in decoy (signed < 0) — **Leg 1 ✅** |
| i2s overhead / no-operand | nonlocal | target value harvestable nowhere (`no_gate_signature`) + I2S execs/s tax |
| vp cmpmap gradient | local | VP coverage-timeseries climbs while cmplog/naive stall; corpus Hamming-distance shrinks |
| joint necessity (vpc-needs-both) | nonlocal | I2S necessary (value_profile blocking seeds place ~0 structural tokens) AND gradient necessary. TWO subtypes (2026-06-12): **assembly-depth** (vpc builds a bigger structure than cmplog — `bench/tools/joint_necessity.py` size+token proxy) and **value-precision** (vpc places a gradient-climbed value at ~same size — needs a value-level sub-test). NB: lineage CANNOT show "an I2S event" — I2S is untagged in mutation_op. |
| corpus inflation / contamination | **nonlocal** | cmplog corpus size ≫ naive; composition collapses onto few arms |
| anti-synergy (vpc loses) | nonlocal | cmplog/vpc corpus ≫ others + per-trial resolve inversion (hardest; honest `inconclusive` likely) |
| ctx coverage | nonlocal | ctx arm's corpus reaches call-context/path depths others don't |
| grimoire structural | nonlocal | grimoire corpus carries structural tokens absent from others |
| ngram path coverage | nonlocal | ngram arm retains corpus at sequential-decode states others collapse |
| scheduling (aflfast rarity / calibrated energy) | nonlocal | scheduler energy/exec skewed to rare-edge / target seed (no sidecar — scheduler-incompat) |

---

## 8. Per-shape workflow + the inconclusive re-round

Per shape (worked example `LW_W`, 7 candidates):

1. **Design agent** reads the 7-candidate menu + branches' signatures:
   - `font_tag_pollution`, `misdirects_from_protocol_byte`, `steers_toward_valid_range`,
     `wrong_offset_codepoint` → **collapse to one**: *decoy-substitution / target-depletion*
     (rule: `signed_target_enrich < −0.3`).
   - `overhead_on_derived_gate_no_operand` (15 br) → **distinct**: no operand to splice
     (rule: `no_gate_signature` + execs/s tax).
   - `over_solves_true_starves_false`, `disrupts_havoc_accumulation` → corpus-dynamics;
     keep only if a metric separates them, else fold into decoy-substitution.
   - emits `evidence_test.json`: ~3 hypotheses + descriptors + decision rule.
2. **Build gate** maps descriptors → tools (dedup against registry), validates on anchor.
3. **Arbiter** runs per branch → `assignments.json`: each branch → one of the ~3 /
   `refuted` / `inconclusive`. Refutation reassigns *within the menu* first
   (try the next candidate's rule); only if no candidate fits → `inconclusive`.
4. **Inconclusive re-rounds — the loop-until-dry labeling loop (bounded, ≤3 rounds).**
   The deliverable is grown by *re-invoking the design agent on shapes that still
   carry unlabeled decisive branches*, until a round produces no new confirmed
   labels (or 3 rounds elapse). Numbering: **round 0** = the original design pass;
   **rounds 1–3** = re-design passes. Each round:

   - **Selection (no threshold).** Re-design **every shape with ≥1 unlabeled
     decisive branch** — NOT a "high unlabeled %" heuristic. Rationale: you cannot
     tell *a priori* whether an unlabeled branch hides an undiscovered mechanism or
     is genuinely non-discriminable — you find out by trying, and convergence (not a
     selection filter) is what bounds it. *Exception:* a branch unlabeled **only**
     because of `seed_starved` routes to seed re-bisection, not re-design (the design
     agent has no seeds to measure).
   - **Standardized prompt.** `tools/build_reinvoke_prompt.py --shape <S>` assembles
     the re-invoke prompt deterministically from the shape's prior `evidence_test.json`
     + the per-branch confirmed/unlabeled split. A re-invoke prompt differs from a
     first-invoke: it hands the agent the prior (refuted) hypotheses, the
     confirmed-vs-unlabeled split, and the loop invariants. (The agent *definition*
     is unchanged — it already accepts a prior hint.)
   - **Invariants.** (i) **Target = unlabeled branches only**; already-confirmed
     branches are FROZEN. (ii) **Monotonic superset** — the new `evidence_test.json`
     MUST retain every prior hypothesis that confirmed ≥1 branch, so the stateless
     arbiter re-validates them (never lose a label; no silent relabel — renames are
     deferred to the Pass-C manual merge). (iii) **Novelty (G1)** — new hypotheses
     must be *genuinely different* mechanisms, not a refuted one re-tested with a
     relaxed threshold (that is chasing-100%, forbidden). (iv) **Honest
     non-discriminable (G3)** — `decidable:false`/`inconclusive` for a sub-group no
     built tool can discriminate is a CORRECT outcome; do not force labels.
   - **Enforce the freeze at merge.** After re-arbitrating, diff against the prior
     dataset: if any branch regressed labeled→inconclusive (the agent dropped a
     still-working hypothesis), restore that round-0 hypothesis into the test and
     re-arbitrate.
   - **Cross-server (per round).** `evidence_test.json` is shared; the arbiter scores
     only `BENCH_ONDISK` targets, so **both servers must re-arbitrate each round's
     redesigned shapes before the next round** — else the merged residual mixes
     round-N (one server) with round-0 (the other) and the next round's selection is
     wrong. See `docs/OTHER_SERVER_TODO.md` §7.
   - **Stop / report.** Stop when a round adds no new labels (convergence) or at
     round 3. The per-round label-gain curve (round 1 ≫ round 2 ≫ round 3 → plateau)
     is the reported rigor artifact; the residual at convergence is the honest
     non-discriminable tail. Identical mechanism categories produced across shapes or
     rounds are merged in the manual Pass-C review (G3), not deduped during re-invoke.

---

## 9. Folder layout

```
step5a_new_v3/
  <shape_family>/                     e.g. i2s_vp_LW_W/
    signatures.json                   # per-branch Pass-A signatures (CONSOLIDATED from step5a_new_v2; not re-run)
    cards.json                        # distiller cards (completed for all 38 shapes)
step5b_new_v3/
  <shape_family>/                     # FLAT — no per-origin-cluster subfolder (Pass B retired)
    evidence_test.json                # design-agent OUTPUT: discovered+collapsed hypotheses + measurement descriptors + decision rule
    assignments.json                  # arbiter OUTPUT: per-branch label / refuted / inconclusive
    round2/                           # only if re-invoked on inconclusive (§8.4)
bench/
  tools/                              # the ~8–11 deterministic measurement tools (shared across shapes)
  tool_registry.json                 # descriptor_key -> {tool_path, params, metrics, anchor_branch, review_status}
  arbitrate.py                        # generic arbiter (applies a shape's decision rule)
  dataset.jsonl                       # assembled from all assignments.json (rep set; expandable via dedup_map)
  bench_score.py                      # score a new fuzzer's resolve-rate per mechanism class
```

The design agent reads `step5a_new_v3/<shape>/signatures.json` as input; the 100
prior Pass-B clusters are passed as an optional reference hint, not stored as
per-cluster folders.

---

## 10. Resolve metric & benchmark harness

**"Did fuzzer F resolve branch B?"** — `resolved_frac(F,B) = n_resolved /
(n_resolved + n_blocked)` at the final checkpoint (from `subject_branches`
per-arm counts / the `*_trials` JSON). F **resolves** B if `resolved_frac ≥ τ`
(default τ=0.8, mirroring ≥8/10). Same signal that assigns `decisive_shape`, so a
new fuzzer just needs `study_units.py add-canonical` to populate its arm.

**`tools/bench_score.py`** (engineered): over every dataset branch, compute a new
fuzzer's `resolved_frac`, report **resolve-rate per mechanism family** + the
branches it newly resolves / still blocks. Scoring is **per-mechanism** (don't
credit a non-I2S fuzzer on an I2S-pro branch it was never expected to need).

---

## 11. Synthetic causal sidecar (local families only)

For `local` families a 1-knob synthetic harness still adds the causal control
real-corpus correlation lacks. Reuse the step-5b infra (`libafl-base`,
`<fuzzer>_cc --libafl -D…`). Lessons (`tools/leg2_signflip/`, probe 2026-06-12):
- cmplog harvests **≥4-byte** CMP operands, **not single bytes** (4-byte gate
  cmplog 407 vs naive 9; per-byte gate cmplog 0).
- **Chained** gates can make cmplog underperform naive for unrelated reasons
  (SHAPE=3: naive 225 > cmplog 111) — keep the target a single clean gate, vary
  only the feature knob.
- For *anti* features the verdict is the **sign-flip of the cmplog−naive margin
  across the knob** + the synthetic corpus reproducing the Leg-1 enrichment
  metric — NOT absolute crash count (why the original anti harnesses refuted).

A sidecar upgrades `synthetic_sidecar.status` to `causal_confirmed`; it never
*overrides* a real-evidence `validated` (real is primary).

---

## 12. Counts, migration, open questions

**Counts (verified 2026-06-12):** 38 shape buckets · 100 Pass-B clusters · 558
analyzed (target, branch) across both servers · 696 cluster-memberships (~138
branches in 2+ clusters = joint halves). Rep-selection: **400 decisive → 286
reps** (~114 near-dups dropped, ~28%; *not* 700→500 as earlier misremembered);
all 286 reps analyzed + seeded. On-disk corpora: curl, harfbuzz, openthread,
sqlite3.

**Migration:** steps 1–4 unchanged (they produce the labeled branches +
analyses); **rep-selection kept**. `step5a_new_v3/` = a *consolidation* of the
existing Pass-A signatures (not a distiller re-run). `step5b_new_v2/`
reproduced/inconclusive verdicts are **inputs** (reproduced → local sidecars in
hand; inconclusive → nonlocal, real-evidence validators). `templates/`-era
catalog stays deprecated. Pass B retired.

**Build order:** N1 joint-necessity (lineage in DB → cheapest 2nd tool) →
corpus-inflation → vp-gradient-climb → overhead-tax → ctx/grimoire/ngram/scheduling.

**Open questions:** τ sensitivity (sweep 0.7–0.9); cross-target label transfer
(curl/sqlite3 were weaker in Leg 1 — per-target calibration?); benchmark leakage
(branches selected by the decisive rule on THESE fuzzers — a new technique may
expose blockers not in the set; the benchmark scores known mechanism classes, it
is not exhaustive).

---

## 13. Implementation status (2026-06-12)

**Built & in place (this server, s4 = curl/harfbuzz/openthread/sqlite3):**
- 38 `step5b_new_v3/<shape>/evidence_test.json` (design agents, all shapes).
- Tools: `bench/tools/i2s_operand_availability.py` (operand_enrichment), `bench/tools/
  joint_necessity.py` (+ 2-arm pair mode for grimoire/mopt/calibrated), `bench/
  tools/value_distance_reached.py`, `bench/tools/depth_reach.py` (ctx/ngram).
  `bench/tool_registry.json`.
- `bench/arbitrate.py` — deterministic arbiter: metric→tool dispatch, multi-tool
  rule merge, `compute→built-tool` resolution, **canonical-rule fallbacks** for
  value_distance (`winner_closer AND distance_gap>=0.15`) and token families
  (`tag_lift>=1.0 AND winner_tags>=2`). operand_enrichment pre-run in study mode →
  `csvs/arb_operand_enrich.csv`. Writes `assignments_<SERVER>.json`.
- `bench/build_dataset.py` — merges `assignments_*.json` across servers (prefers
  validated), dedups by branch_id → `bench/dataset.jsonl`. `BENCH_SERVER` /
  `BENCH_ONDISK` env-driven.
- Reviewed (`/code-review` high): the 3 byte-tools + arbiter (fixes applied);
  `depth_reach` + pair mode pending review.

**Current dataset:** 554 distinct branches; ~124 validated (s4), rest
inconclusive / non-local. Honest non-results: anti-synergy + scheduling
(`decidable:false`).

**Multi-server run:** `docs/OTHER_SERVER_TODO.md`. Each server sets BENCH_SERVER+
BENCH_ONDISK, re-bisects sparse branches (`--fallback-ranks 10`), **re-anchors
each tool on a local target**, pre-runs operand_enrichment, arbitrates →
`assignments_<srv>.json`, `build_dataset` merges. Push the shared layer (not
`db/`/`out/`) per that doc's file manifest.
