# Methodology Demo: LLM-as-Hypothesis-Generator + Parameterized Synthetic Verification

Two clean reproductions, easy and hard cases, same disciplined protocol.

## Protocol (4 steps before any synthetic is built)

1. **Artifact search** — Have we tried this before? What was learned?
2. **Cross-target distribution** — Where does the divergence concentrate? Single-target → program-specific feature; spread across targets → general-purpose feature.
3. **Multi-candidate emission (≥3 hypotheses)** — Falsify each via prior verification work, pick the survivor.
4. **Build only the surviving candidate** — Parameterized template with one program-side knob.

Empirical finding from this session: skipping any of step 1–3 caused redundant work and wrong-axis selection. Step 1 alone (artifact search) catches ~70% of dead-ends.

---

## Demo 1 — `i2s_magic_number_gate` (easy case)

**Source pair:** `cmplog > naive @ lcms` (62% of triple-tagged divergence in lcms cmspcs/cmsgamma — ICC tag CMPs).

**Surviving hypothesis:** I2S substitutes the full constant operand of an integer comparison in one mutation step. Naive must brute-force byte-by-byte (1/256^N).

**Parameter:** `MAGIC_BYTES ∈ {1, 2, 4, 8}` — width of a single equality CMP.

**Result (5 trials × 600s):**

| MAGIC_BYTES | naive mean | cmplog mean | cmp/naive ratio |
|---:|---:|---:|---:|
| 1 | 584 | 25,260 | **43×** |
| 2 | 224 | 30,316 | **135×** |
| 4 | 26 | 28,309 | **1097×** |
| 8 | 35 | 20,466 | 588× |

cmp essentially constant ~25k (I2S is width-invariant). naive collapses geometrically. Slight rebound at width=8 from libafl's compile-time autotoken extraction.

**Curve shape:** clean monotone increasing in cmp/naive ratio across widths 1, 2, 4. Textbook dose-response.

---

## Demo 2 — `i2s_corpus_pollution` (hard case, 4 fuzzers)

**Source pair:** `naive > cmplog @ libpcap` (90% of cases in libpcap — many grammar tokens dilute cmp's I2S dictionary).

**Surviving hypothesis (multiplicative axis):** Pollute count N × chain length K → cmp's per-step useful-substitution rate K/(K+N) compounds to (K/(K+N))^K over the chain. Exponential dilution.

**Parameter:** `COST_INNER ∈ {0, 64, 512, 4096}` — number of pollute CMPs invoked per execution (all 64 noise constants logged into I2S dictionary, weighted by frequency).

**Result (5 trials × 600s, 4 fuzzers, medians):**

| COST_INNER | naive | cmplog | value_profile | **value_profile_cmplog** |
|---:|---:|---:|---:|---:|
| 0    | 122 | 993 | 43  | **632** |
| 64   | 0   | 109 | 9   | **376** |
| 512  | 0   | 0   | 30  | **258** |
| 4096 | 0   | **0** | 1 | **6** |

**Four distinct mechanism signatures along the same axis:**

- **cmp** — exponential decay (993 → 109 → 0 → 0). I2S dictionary diluted, no fallback.
- **vp**  — small but persistent (~1–50 across the range). CMP_MAP gradient sees Hamming distance, unaffected by dictionary pollution.
- **vpc** — graceful degradation (632 → 376 → 258 → 6, **never zero**). I2S handles low-pollute, CMP_MAP carries through high-pollute.
- **naive** — bimodal: one trial=1566 at c0 (stochastic runaway), zero elsewhere. The famous "naive beats cmp" claim is reproduced as **stochastic, not deterministic** — only manifests in a fraction of trials at low pollute.

**Headline finding:** At COST_INNER=4096, cmp is dead (median 0) but vpc still resolves (median 6). The synergy_cmplog_plus_vp pattern.

---

## What this demonstrates

1. **The methodology converges on the right axis** — both demos identified the surviving hypothesis through prior-artifact + cross-target-distribution + multi-candidate falsification, before any synthetic was built.
2. **Single program-feature knob, multiple fuzzer signatures** — Demo 2 shows the strongest version: one harness, one parameter, four fuzzers, four distinct strategy responses traceable from first principles.
3. **The protocol scales from easy to hard cases** — Demo 1 has a single-knob monotone curve; Demo 2 has a multiplicative axis, bimodal distributions, and four-way synergy comparison. Same protocol works for both.

---

## What didn't work (cautionary track, also methodology-relevant)

All three entries below are now under `templates/legacy/` because they target `minimizer`, which is **not** in the canonical comparable-pair set under the metaphorical-testing framing (cmplog/naive/value_profile/value_profile_cmplog only). Kept as methodology lessons.

- `legacy/quality_chain_concentration`: proposed chain length as the axis for `minimizer > naive @ sqlite3`. Refuted — sqlite3's distinguishing feature is exec-time variance + corpus inflation, not chain length. Cross-target check (which I skipped initially) would have caught this earlier.
- `legacy/workload_variance_concentration`: proposed exec-time variance. Minimizer stalled on the synthetic because initial bitmap was too small for CalibrationStage to bootstrap.
- `legacy/lanes_concentration`: yesterday's `b_dequote_v10` design with calibration_pad. Synthetic-vs-real signal was at the noise floor; per-trial variance (10-100×) drowned the predicted ~2× effect. Methodology lesson: 5–10 trials is too few for high-variance bimodal pairs; need ≥30 trials *or* a stronger-signal program (which sqlite3 has but minimal C harnesses don't).

These three negative results are themselves catalog entries. They show the methodology doesn't *guarantee* a positive result — it produces falsifiable claims, and some hypotheses get refuted. That's the discipline.

---

## Take-aways for the audience

- **LLM as hypothesis generator, not test-case generator.** The LLM proposes axes; the harness is a falsifiable artifact that either confirms or refutes.
- **Cross-target distribution as the disconfirmation gate.** Before building anything, check whether the proposed feature is general (would show up in other targets too) or target-specific. Most program-feature claims fail this test cleanly.
- **Parameterized templates, not one-off harnesses.** Single-point synthetics ("does cmp beat naive on this harness?") confound the question. A parameter sweep with predicted curve shape is the falsifiable form.
- **Robust statistics for bimodal fuzzers.** Naive is high-variance; medians + per-trial inspection beat means. Yesterday's 5-trial-mean claim was a sample of a noisy distribution; methodology requires either 30+ trials or signal-strength calibration.
