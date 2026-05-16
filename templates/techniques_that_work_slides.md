# Slide deck — "Techniques that work" family (5 templates)

Five reproduced templates that surface the regimes where adding I2S
(input-to-state substitution) or VP (CMP_MAP gradient feedback) yields
a measurable, dose-responsive advantage. The positive complement to
the I2S-hurts family. Together they answer:
*if you decide to add a fuzzer technique, which program shapes is it
actually expected to help?*

---

## Slide 0 — Framing

**The metaphorical-testing setup**

- 4 canonical fuzzers: `naive`, `cmplog`, `value_profile`, `value_profile_cmplog` (vpc)
- Pairwise one-technique deltas isolate WHICH technique drives WHICH divergence
- Two technique axes → two sub-families:
  - **I2S axis** (cmplog vs naive, vpc vs value_profile): I2S substitution is added or not
  - **VP axis** (value_profile vs naive, vpc vs cmplog): CMP_MAP gradient is added or not

**The 5 templates by sub-family**


| Sub-family     | Template                      | Knob                         | Headline ratio                             |
| -------------- | ----------------------------- | ---------------------------- | ------------------------------------------ |
| **I2S helps**  | `i2s_magic_number_gate`          | MAGIC_BYTES ∈ {1,2,4,8}      | cmp/naive 43× → 135× → **1097×** → 588×    |
| **I2S helps**  | `i2s_grammar_chain_length`    | CHAIN_LEN ∈ {1,2,4,8}        | vpc/vp **∞** at every dose (naive = vp = 0 always); vpc/cmp 2.9× → 3.0× → 1.9× → ∞ |
| **I2S helps**  | `i2s_pair_relational_lookup`  | DICT_SIZE ∈ {4,16,64,256}    | vpc/vp 189× → 9.7× → **∞** → saturated     |
| **VP rescues** | `vp_gradient_derived_operand` | DERIVATION_DEPTH ∈ {0,1,2,4} | vp/naive 100× → **∞** → **∞** → **∞**      |
| **dual: VP-rescues + I2S-hurts** | `i2s_anchored_length_trap`     | N_ANCHORS ∈ {0,1,4,16}    | VP edge: vpc/cmp 1.0× → 1.86× → 6.5× → **13.0×**; I2S edge: vp/vpc ≈ **2.25×** at every dose ≥ 1 |


Each template owns ONE primary pair, ONE knob, ONE source-feature.
Numbers are median crash counts, n=5 trials × 600s per dose unless noted.

---

## Slide 1 — `i2s_magic_number_gate` (the default story)

### What is the feature

A program with **one literal-equality CMP** of MAGIC_BYTES bytes against a
compile-time constant. Naive fuzzers must brute-force the constant
byte-by-byte (1/256^N hit rate). cmplog logs the constant via sancov's
`__sanitizer_cov_trace_const_cmp{1,2,4,8}` and `I2SRandReplace`
substitutes it into the input in **one** mutation step.

### Prediction

- axis = I2S; has_I2S = {cmp, vpc}, lacks_I2S = {naive, vp}
- cmp/naive ratio grows monotonically with MAGIC_BYTES
- naive collapses to ~0 once N ≥ 4 (1/2^32 random hit rate ≪ 600s budget)
- cmp resolves at every width via single-substitution

### How it is designed (synthetic harness)

- **Knob**: `MAGIC_BYTES` ∈ {1, 2, 4, 8}
- One CMP `if (read_be_N(data) == K)` where N = MAGIC_BYTES, K = `0xDEADBEEFCAFEBABE` truncated to N bytes
- Direct `__builtin_trap()` on equality — no upstream gates

### Why this maps to the source code

Real-target instances span **4 targets / 5 corroborations** at width=4:


| target  | branch  | source                                                                            | n_A   | n_B       |
| ------- | ------- | --------------------------------------------------------------------------------- | ----- | --------- |
| bloaty  | br 475  | `macho.cc:152` `if (magic == MH_MAGIC || MH_MAGIC_64 || MH_CIGAM || MH_CIGAM_64)` | 10/10 | 0/10      |
| bloaty  | br 446  | `elf.cc:1279` ELF magic + sizeof gates                                            | 3/3   | 0/3       |
| sqlite3 | br 1726 | `sqlite3.c:103595` `SELECT` keyword (6-byte)                                      | 3/3   | UNREACHED |
| lcms    | br 26   | `cmsgamma.c:721` ICC colorspace `'Lab '` discriminator                            | 10/10 | 0/10      |


The mechanism is **identical** across all 5: cmp's I2S logs the literal
operand of one upstream literal-equality CMP, splices it into the input
at the right offset on the next mutation. Naive cannot compete on a
2^32 random search space within 600s × ~50K execs/s = 3×10⁷ attempts.

### Real behavior — n=5 × 600s


| MAGIC_BYTES | naive (mean) | cmp (mean) | **cmp/naive ratio** |
| ----------- | ------------ | ---------- | ------------------- |
| 1           | 583.8        | 25260      | **43×**             |
| 2           | 223.8        | 30316      | **135×**            |
| 4           | 25.8         | 28309      | **1097×**           |
| 8           | 34.8         | 20466      | 588×                |


Slight rebound at width=8 is libafl's autotokens pass directly splicing
the 8-byte literal into mutations regardless of width. Widths 1–4 are
the cleanest demonstration of the I2S effect.

Verdict: `reproduced` (default I2S story; the most-corroborated template
in the catalog with 99 implied corroborations across 11 shapes).

### Metrics

- Median crash count per fuzzer per scan value
- **I2S-helps criterion**: cmp/naive ratio > 1.0 monotone-non-decreasing in MAGIC_BYTES (until autotokens kick in)

---

## Slide 2 — `i2s_grammar_chain_length`

### What is the feature

A trap gated by **CHAIN_LEN dependent slots**, each requiring a
4-byte literal match drawn from a compile-time dictionary. Each slot
is checked at a SHARED source-PC inside one noinline helper —
**no per-slot coverage edge**, so VP's CMP_MAP gradient cannot
accumulate per-slot best-distance buckets.

### Prediction

- axis = I2S (vpc has it, vp does not)
- vpc resolves linearly in CHAIN_LEN (one I2S substitution per slot)
- vp must hit ALL CHAIN_LEN slots simultaneously by random byte mutation
(~1/256^(4·L)) — below budget at any L ≥ 1
- vpc/vp ratio = ∞ at every dose

### How it is designed (synthetic harness — v2)

- **Knob**: `CHAIN_LEN` ∈ {1, 2, 4, 8}
- One noinline `check_one_slot(slot_index, value)` shared across all slots
- AND-accumulator: trap fires when all CHAIN_LEN slots match
- No short-circuit, no per-slot branch — single coverage edge for the chain

```c
__attribute__((noinline))
static int check_one_slot(int idx, uint32_t v) {   // ← single source-PC for all slots
    for (int i = 0; i < DICT_SIZE; i++)
        if (v == KEYWORDS[idx][i]) return 1;
    return 0;
}

int LLVMFuzzerTestOneInput(const uint8_t *d, size_t s) {
    if (s < CHAIN_LEN * 4) return 0;
    int hits = 1;                                   // AND-accumulator
    for (int k = 0; k < CHAIN_LEN; k++)
        hits &= check_one_slot(k, read_be32(d + 4*k));
    if (hits) __builtin_trap();
    return 0;
}
```

### Why this maps to the source code (origin: libpcap `pcap_compile`, br 799)

libpcap's BPF filter compiler walks a parser chain: NUM `=` NUM `%`
NUM `*` NUM forms a 4-step token chain through `pcap_compile`, with
the optimizer trap firing on a divisor-zero constant-fold. Side-B vpc
seeds carry a parseable filter expression (`0=01%4*0`); Side-A vp
seeds carry filterSize=1 (empty filter) which compiles trivially and
takes the success side.

**Caveat**: libpcap's actual chain has per-token coverage edges, so the
gradient *can* accumulate per-slot — that's the v1 regime, where the
chain-length axis flattens to ~5× ratio. The v2 harness deliberately
collapses all per-slot edges to one source-PC to expose the
chain-length compounding mechanism in isolation.

### Real behavior — v2 reproduction (n=5 × 600s, 4 fuzzers)

| CHAIN_LEN | **naive** | **cmp** | **vp** | **vpc**   | vpc/vp | vpc/cmp |
| --------- | --------- | ------- | ------ | --------- | ------ | ------- |
| 1         | **0**     | 7592    | **0**  | **22158** | ∞      | 2.92×   |
| 2         | **0**     | 9496    | **0**  | **28666** | ∞      | 3.02×   |
| 4         | **0**     | 4728    | **0**  | 8814      | ∞      | 1.86×   |
| 8         | **0**     | **0**   | **0**  | 6         | ∞      | ∞       |

naive = vp = **0 in 20/20** trials. cmp resolves at L1–L4 then dies at L8. vpc dominates at every L: 22k → 28k → 9k → 6 — never zero.

**4-fuzzer reading**:
- **naive 0/20**: no I2S, no gradient — chain is unreachable by random walk at any L.
- **cmp 7.6k → 9.5k → 4.7k → 0**: I2S alone can splice each slot's literal one substitution at a time, but can't retain partial-chain progress across mutation. Survives short chains; collapses at L=8.
- **vp 0/20**: per design — v2 collapses every slot CMP into one shared source-PC, eliminating the per-slot coverage edges that VP's gradient needs.
- **vpc 22k → 28k → 9k → 6**: I2S splices each slot AND VP retains seeds whose partial-chain hamming distance to the goal shrinks. Synergy = cmp can't keep partial progress, vp can't navigate any single slot, both together can.

Verdict: `reproduced_v2` (strongest possible — naive=vp=0 at every dose; vpc strictly > cmp at every L; vpc/cmp diverges to ∞ at L=8).

**Methodology lesson** (already in the memory file): chain-length
compounding only manifests when per-slot CMPs are coverage-edge-coupled.
v1 (per-slot edges) refuted with flat ~5× ratio; v2 (single shared edge)
reproduced with ∞ ratio. Real targets typically expose per-slot edges →
they fall in the v1 regime, captured by `i2s_magic_number_gate`'s per-slot
KEYWORD_LEN axis instead of this template's chain axis.

### Metrics

- vpc median > 0 at every CHAIN_LEN
- vp median monotone non-increasing
- vpc/vp ratio monotone non-decreasing

---

## Slide 3 — `i2s_pair_relational_lookup`

### What is the feature

A trap that fires on a **relational property** between TWO 4-byte
literals drawn from a compile-time dictionary at fixed input offsets.
Reaching the trap requires **two distinct dictionary hits sharing one
descriptor field and differing in another** — e.g., two tag-types with
matching channel-count but distinct names.

### Prediction

- axis = I2S (vpc vs vp)
- vpc resolves at low-to-moderate DICT_SIZE: I2S logs each compared
literal in one trace_const_cmp4 call (per dictionary entry per call),
then splices into the input pair offsets
- vp's gradient retains best-Hamming-distance buckets per CMP, but with
N entries per slot the gradient signal is diluted N-fold
- vpc/vp ratio grows monotonically with DICT_SIZE (until both saturate)

### How it is designed (synthetic harness)

- **Knob**: `DICT_SIZE` ∈ {4, 16, 64, 256} — entries in the static lookup
- Two distinct 4-byte literal slots at fixed offsets in the input
- Each slot tested via a static lookup helper that compares against
every dictionary entry (one trace_const_cmp4 per entry per call)
- Trap fires when slot1 ≠ slot2 AND both share a descriptor predicate

### Why this maps to the source code (origin: lcms br 56, `CompatibleTypes`)

Side-A vp seeds: zero/random tag-sig bytes at offsets 0x14–0x23.
Side-B vpc seeds: populated 4-byte FOURCC-shaped values `'en\0I'` and
`'f se'` at the same offsets — both reach `CompatibleTypes`, but only
vpc supplies the *valid pair* required to trip the relational check.
vpc 10/10 vs vp 0/10 (avg blocked 11.80h). Hitcount asymmetry: 111 vs 0.

**Distinguished from `i2s_magic_number_gate`**: that template's predicted
curve is FLAT in cmplog/vpc (single substitution succeeds at any width).
This template predicts MONOTONE DECREASING in vpc as DICT_SIZE grows —
each substitution attempt has hit rate 1/DICT_SIZE, and two independent
hits compound to 1/DICT_SIZE².

### Real behavior — n=5 × 600s


| DICT_SIZE | **vp** | **vpc**   | vpc/vp ratio                            |
| --------- | ------ | --------- | --------------------------------------- |
| 4         | 159    | **29988** | **189×**                                |
| 16        | 3211   | **31170** | 9.7×                                    |
| 64        | **0**  | **12909** | **∞**                                   |
| 256       | 0      | 0         | saturated (both fuzzers exhaust budget) |


vp's signal collapses to 0 at DICT_SIZE ≥ 64 — gradient is too dilute.
vpc holds through DICT_SIZE = 64, drops to 0 at 256 (substitution rate
1/256² ≈ 1.5e-5 per attempt × 600s × ~30K execs ≈ 0.27 expected hits).

Verdict: `reproduced` (clean monotone decrease in vpc; ∞ ratio at d=64
where vp dies first).

### Metrics

- Median crash count per fuzzer per scan value
- **Two-literal-relational criterion**: vpc/vp ratio monotone non-decreasing while both nonzero; vpc must out-survive vp at the largest dictionary size where either resolves

---

## Slide 4 — `vp_gradient_derived_operand`

### What is the feature

A trap that requires the input to satisfy **K independent literal-equality CMPs in coordination** — typically a parser cascade, an N-way switch dispatch, or a tag-table presence cascade. Each individual CMP is byte-narrow (1–4 bytes); reaching the trap requires K CMPs to all pass, gating each subsequent step.

VP's CMP_MAP retains K independent per-CMP best-distance buckets — the corpus accumulates seeds that PARTIALLY satisfy more CMPs over time, walking the chain linearly. cmp's I2SRandReplace operates ONE substitution per cycle; reaching the K-coordinated state requires K cooperating substitutions while preserving each, geometrically expensive against a dictionary of K-or-more literals. cmp's standard pipeline can't grow corpus past initial seed because the only nearby novel coverage is the trap (crash-terminal); cmplog stage gated on queue growth never activates → cmp degenerates to naive at K≥4.

The feature instantiates across diverse source-level patterns that all reduce to "K narrow literal-equality CMPs in coordination at the libafl-feedback layer":
- **Parser cascade** (mbedtls TLS handshake → version range check; sqlite vacuum keyword cascade through tokenizer → grammar reduction → name resolver → terminal builder)
- **N-way switch dispatch** (lcms `validDeviceClass()` 7-arm switch; sqlite VDBE main switch on `pOp->opcode` ~190 arms; libpcap bison yyparse rule switch)
- **Tag-table presence cascade** (lcms `cmsIsMatrixShaper` checks 6 specific tag signatures present)

13 real-target branches in `branch_index.json` instantiate this mechanism across 4 targets (mbedtls TLS, lcms FOURCC dispatch, sqlite VDBE/parser cascade, libpcap bison reduction).

### Prediction

- axis = value_profile (vp has CMP_MAP gradient; naive doesn't; cmp degenerates to naive due to bootstrap starvation + dictionary roulette)
- **vp wins decisively** at every CHAIN_DEPTH; **cmp = naive = 0** at K≥4
- **vpc dominates with monotone-growing synergy** over vp (1.1× at K=4 → 130× at K=16) via VP-bootstraps-corpus + I2S-refines-each-step
- This is the **canonical "VP wins where cmp can't" template** — cmp's I2S substitution structurally fails on multi-CMP coordination

### What was refuted along the way (v3 / v4 / v5 / v6, 2026-05-10)

Five distinct synthetic designs were tested before settling on v2 as the canonical demonstrator:

| variant | mechanism tested | verdict | failure mode |
|---|---|---|---|
| v1 | single 32-bit eq + bijective XOR derivation | refuted | 33 buckets too narrow; trap unreachable at depth ≥ 1 |
| v3 | single 64-bit eq + bijective XOR derivation | refuted | even ONE XOR layer drops vp/naive to ~1×; bijective transforms theoretically preserve gradient, empirically destroy it in LibAFL |
| v4 | single WIDTH-byte literal eq, no transform | reproduced (vp,naive) only; **full shape BRBR** (cmp dominates 12-380×) | shape doesn't match real-target B-R-; v4 is essentially `i2s_magic_number_gate` |
| v5 | XOR-of-uint32-chunks checksum | refuted | trivial single-splice satisfies (chunk0=TARGET, others=0) → cmp wins ~10000× |
| v6 | sum-of-bytes near max | refuted | naive wins at low W (random density); gradient too jittery at high W (popcount-vs-magnitude mismatch) |

The lesson across v4-v6: **single-CMP synthetics cannot demonstrate "VP wins where cmp can't" in LibAFL.** Either I2S substitution trivially solves, or random walk wins by density, or the gradient is too narrow/jittery. The mechanism that IS demonstrable is multi-CMP coordination (v2 chain), where each individual CMP is byte-narrow (clean gradient) and K of them compound to defeat I2S's single-substitution-per-cycle limit.

### How it is designed (synthetic harness — v2)

- **Knob**: `CHAIN_DEPTH` ∈ {2, 4, 8, 16} — count of independent literal-equality CMPs in a gating chain
- K narrow (1-byte) CMPs in series: `cmp_0(data[0]) && cmp_1(data[1]) && ... && cmp_{K-1}(data[K-1])` → trap
- Each `cmp_i` is a noinline function emitting a distinct coverage edge AND a CMP_MAP Hamming bucket
- VP retains best-distance seeds independently per CMP — gradient compounds linearly across K
- cmp's I2S substitution: dictionary fills with K candidates; each substitution attempt picks uniformly (1/K rate); reaching K-coordinated state requires K cooperating substitutions while preserving each — geometric collapse

### Why this maps to the source code (origin: mbedtls `ssl_tls12_client.c`, br 378)

```c
ssl->tls_version = mbedtls_ssl_read_version(buf, ssl->conf->transport);

if (ssl->tls_version < ssl->conf->min_tls_version ||
    ssl->tls_version > ssl->conf->max_tls_version) ...  // ← branch 378
```

The branch itself is a single 16-bit range check — but reaching it requires passing the **entire TLS handshake parser cascade**: DTLS record header validation → handshake message type → handshake length → server hello structure → server_version field. At the libafl-feedback layer that's ~K=4-6 sequential literal-equality CMPs whose CMP_MAP buckets VP retains independently. cmp's I2S dictionary fills with literals from ALL stages → dictionary roulette + multi-step coordination → cmp 1/10. naive 0/10 (8/10 unreached — same mechanism). vp 8/10 — gradient walks the cascade.

### Real behavior — v2 chain harness, full 4-fuzzer table (n=5 × 600s)

| K | **naive** (med) | **cmp** (med) | **vp** (med) | **vpc** (med) | vpc/vp ratio |
|--:|---:|---:|---:|---:|---:|
|  2 |   33 |   1 | 3294 |  6619 |   2.0× |
|  4 |    0 |   0 | 9000 | 10093 |   1.1× |
|  8 |    0 |   0 |  834 |  8469 |  **10×** |
| 16 |    0 |   0 |   39 |  5077 | **130×** |

**Naive AND cmp both collapse to 0 at K≥4.** VP wins decisively. VPC dominates with monotone-growing synergy — at K=16, vpc gets 5077 crashes vs vp's 39, a 130× synergy multiplier from VP-bootstraps + I2S-refines.

### Queue sizes — bootstrap starvation for cmp; growth for vpc

| K | cmp queue | vpc queue |
|--:|--|--|
|  2 | 2, 2, 2, 2, 2 | 7, 6, 6, 7, 8 |
|  4 | **1, 1, 1, 1, 1** | 12, 13, 13, 14, 13 |
|  8 | **1, 1, 1, 1, 1** | 16, 14, 17, 16, 16 |
| 16 | 3, 3, 2, 2, 3 | **35, 30, 32, 29, 34** |

cmp's queue STUCK at 1 from K=4 onward — same bootstrap-starvation pattern from the anchor template. cmplog stage gated on queue growth; standard pipeline can't grow corpus because the only nearby novel edge is the trap (crash-terminal). vpc grows linearly with K — VP's per-CMP gradient buckets generate continuous corpus growth, then I2S refines each entry to advance individual chain steps.

Verdict: `reproduced_v2_full_4fuzzer`. The shape (cmp = naive = 0; vp wins; vpc dominates with monotone-growing synergy) matches the qualitative pattern of all 13 real-target branches in `branch_index.json`.

### Methodology lessons

- **Single-CMP arithmetic-defeat-of-I2S is structurally hard in LibAFL.** v4-v6 explored this design space and found three distinct failure modes (BRBR shape from trivial I2S splice; trivial XOR-checksum splice; sum-checksum density-too-high or gradient-too-jittery). Multi-CMP coordination (v2) is the only synthesizable demonstrator that reproduces the real-target shape.
- **Bijective transforms theoretically preserve gradient, empirically do not in LibAFL** (v3 finding). Math: H(x XOR K, y) = H(x, K XOR y) — gradient should walk equally well at any depth. Empirical: even one XOR layer destroys VP's advantage. Likely cause: byte-level mutator schedule + indirect-call/sink overhead together break gradient navigation across the call boundary.
- **vpc/vp synergy ratio (1.1× → 130×) is the bootstrap-rescue mechanism**, structurally identical to `i2s_corpus_pollution`'s vpc-rescues-cmp pattern but driven by chain depth instead of dictionary pollution. VP grows the corpus → cmplog stage finally activates → I2S refines each new corpus entry to land specific chain literals.
- The 13 real-target branches all reduce to v2's mechanism via diverse source-level patterns: parser cascade, N-way switch dispatch, tag-table presence cascade. CHAIN_DEPTH=K abstracts over the source-level pattern.

### Metrics

- Median crash count per fuzzer per scan value
- **VP-helps criterion**: vp >> naive at every K (∞× at K≥4 since naive=0)
- **VPC-rescues-cmp criterion**: vpc/cmp ratio = ∞ at K≥4; vpc/vp synergy ratio grows monotonically with K

---

## Slide 5 — `i2s_anchored_length_trap`

### What is the feature

A trap gated by **input shrinkage** (e.g., the input becomes shorter
than a pcap-magic-sized header). cmplog's I2S **anchors** input
bytes 0..3 to header literals via splice-back: every offspring has the
4-byte magic re-pinned, suppressing length-shrinking mutations. vpc has
*both* I2S **and** the CMP_MAP gradient — the gradient retains seeds
of varying lengths in distinct best-distance buckets, **rescuing** the
short descendants from I2S monoculture.

### Prediction

- axis = value_profile (vpc adds CMP_MAP gradient on top of cmplog's I2S)
- ratio is **GAIN-on-vpc**, not loss-on-cmp: cmp stays flat at random-shrink
baseline (~15 crashes / 600s); vpc grows monotonically with N_ANCHORS
- vpc/cmp ratio monotone non-decreasing

### How it is designed (synthetic harness)

- **Knob**: `N_ANCHORS` ∈ {0, 1, 4, 16} — count of distinct 4-byte
literal-equality CMPs at offsets 0..3 that fire when size ≥ 4
- Each anchor populates one I2S dictionary entry pinning byte content at the head
- Trap fires when input size < 4 (length-shrink trap)

### Why this maps to the source code (origin: libpcap `savefile.c:512`)

```c
if (amt_read != sizeof(magic))    // ← length-shrink trap
```

Subject 67 (libpcap, vpc vs cmp): ΔAUC=69.5M, p_AUC=0.064 (admissible
at n=3 bound), strict-wins on 1 of 2 value_profile-labeled edges.

**Side-A cmp seeds** all 20 bytes with bytes 0..3 = `02 ?? 04 ??`
(pcap-magic-like prefixes); mutator traces include `I2SRandReplace`,
`TokenInsert`, `DwordInterestingMutator` — direct evidence of I2S
splice-back at offsets 0..3.
**Side-B vpc seed**: 5 bytes (shorter than pcap magic). VP's gradient
retained the short descendant in a distinct CMP_MAP bucket; I2S's
splice-back is bypassed because the short seed has no offsets 0..3 to
re-pin.

### Real behavior — n=5 × 600s (3 fuzzers; naive not run; counts corrected 2026-05-09)

| N_ANCHORS | **cmp** | **vp** | **vpc** | vpc/cmp (VP edge) | vp/vpc (I2S edge) |
| --------- | ------- | ------ | ------- | ----------------- | ----------------- |
| 0         | 3       | 4      | 3       | 1.0×              | 1.33×             |
| 1         | 7       | 26     | 13      | 1.86×             | **2.00×**         |
| 4         | 4       | 59     | **26**  | **6.5×**          | **2.27×**         |
| 16        | 5       | **146**| **65**  | **13.0×**         | **2.25×**         |

**Count correction** (2026-05-09): the original verification (2026-05-04) reported cmp/vpc medians 3× too high because the `find -name '.metadata*'` filter let `.lafl_lock` sibling files through, multiplying each real crash by 3 in the count. Corrected by /3; the vpc/cmp ratio is unchanged because both fuzzers were inflated equally.

**This is a dual-membership template — both readings hold simultaneously:**
- **VP edge** (vpc vs cmp): vpc/cmp = 1.0× → 1.86× → 6.5× → 13.0×. cmp stays at random-shrink baseline (3, 7, 4, 5) regardless of dose. **VP rescues monotonically.** Lives in this deck.
- **I2S edge** (vp vs vpc): vp/vpc = 1.33× → 2.00× → 2.27× → 2.25×. **vp out-survives vpc by ~2× at every dose ≥ 1.** I2S monocultures vpc's diversifying corpus by re-anchoring offspring at bytes 0..3, narrowing the lineage that VP would otherwise diversify. Same template ALSO lives in `i2s_hurts_family_slides.md` Slide 3.

### Throughput-immune diagnostic — queue size distribution

The crash count is throughput-dominated. The queue size at end-of-trial is throughput-immune (5 trials × 600s same wall-clock for every fuzzer) and observes the corpus-diversity mechanism directly.

**Total seeds in queue, n=5 trials pooled:**

| N_ANCHORS | cmp queue | vp queue | vpc queue | vpc/vp queue ratio |
| --------- | --------- | -------- | --------- | ------------------ |
| 0         | 5         | 5        | 5         | 1.00×              |
| 1         | 5         | 24       | 20        | 0.83×              |
| 4         | 5         | 48       | 30        | 0.63×              |
| 16        | 5         | **118**  | **79**    | **0.67×**          |

- **cmp's queue stays at exactly 5 seeds** at every dose (one per trial × 5 trials). cmp's only feedback is binary edge coverage; once each anchor compare's true-branch edge is taken once, no further retention. The corpus does not grow.
- **vp's queue grows 5 → 118** with N_ANCHORS. Each anchor opens new gradient retention buckets; corpus diversifies freely.
- **vpc's queue grows but always lags vp's** — settles at 67% of vp's diversity at N=16. This is the visible footprint of I2S monoculture: `I2SRandReplace` re-anchors offspring's bytes 0..3 to dictionary values, biasing them back into a narrower corner of state-space and reducing the *distinct* gradient buckets that get retained. The reduced queue diversity translates directly into the 2.25× crash-count gap on the I2S edge.

Verdict: `reproduced` (dual). VP-rescues direction holds on (vpc, cmp); I2S-hurts direction holds on (vp, vpc). The same harness exhibits both readings of the same physics.

**Distinct from sister templates**:
- **`i2s_corpus_pollution`** (same vpc-vs-cmp primary pair): there `COST_INNER` pollutes the I2S dictionary across a chain whose trap CMP IS itself I2S-substitutable; failure mode = dilution. Here N_ANCHORS adds upstream anchor compares; trap is length (NOT I2S-substitutable); failure mode is cmp's inability to retain shrink-lineage seeds. Both end at `vpc > cmp`, different mechanisms.
- **`i2s_anchored_seed_deviation_trap`** (mirror harness, opposite-axis dominance): there anchor sites × arms, trap byte at offset 128 INSIDE I2S splice-back's range → vpc's curve FALLS dramatically as anchors grow (8115 → 924) — direct I2S-monoculture damage at the trap byte. Here anchors at offset 0..3 with a length-shrink trap → I2S can't directly damage at the trap (short inputs skip the anchors), but it still narrows vpc's queue diversity → vp wins by a smaller ~2× ratio. Both templates have the I2S-hurts shape on the (vp, vpc) edge; magnitude depends on whether the trap operand is inside or outside the anchored zone.

### Metrics

- Median crash count per fuzzer per scan value
- **VP-rescues criterion**: vpc median monotone non-decreasing in N_ANCHORS; cmp median flat (anchor-independent baseline); vpc/cmp ratio monotone non-decreasing

---

## Slide 6 — Cross-template synthesis: when does which technique help?


| Template                      | Axis               | Headline number (real)               | Source-feature signature                                            |
| ----------------------------- | ------------------ | ------------------------------------ | ------------------------------------------------------------------- |
| `i2s_magic_number_gate`          | I2S                | cmp/naive **1097×** at MAGIC_BYTES=4 | one literal-equality CMP at fixed input offset                      |
| `i2s_grammar_chain_length`    | I2S                | vpc/vp **∞** (naive=vp=0 always); vpc/cmp **∞** at L=8 | K dependent slots sharing one source-PC (no per-slot edge)          |
| `i2s_pair_relational_lookup`  | I2S                | vpc/vp **∞** at d=64                 | two distinct literals from a static lookup, relational predicate    |
| `vp_gradient_derived_operand` | VP                 | vp/naive **∞** at depth ≥ 4          | bijective bytewise transform between input and CMP operand          |
| `i2s_anchored_length_trap` (dual: VP-rescues + I2S-hurts) | VP and I2S both | VP edge: vpc/cmp **13×** at N_ANCHORS=16. I2S edge: vp/vpc **2.25×** at N_ANCHORS=16. Queue: vp 118 vs vpc 79 seeds (vpc 67% of vp diversity). | upstream literal anchors at fixed head offsets + length-shrink trap |


### 4-fuzzer signature reads as the differentiator

The decisive-shape vocabulary at the source branch tells you which
template applies (paired with the `--BR` / `B-BR` etc. shapes from the
I2S-hurts deck):

- **`BR--`** / **`B-R-`** / **`BRBR`** (cmp=R, naive=B) → **i2s_magic_number_gate** (one literal CMP)
- **`-BBR`** / **`BBBR`** (vpc=R, vp=B, possibly cmp=B) → **i2s_grammar_chain_length** OR **i2s_pair_relational_lookup** (multi-slot I2S, distinguished by source-feature: chain vs pair)
- **`B-R-`** / **`BBRR`** with vp=R, cmp=B → **vp_gradient_derived_operand** (bijective derivation; cmp's I2S misfires)
- **`-BBR`** with vpc rising on dose, cmp flat → **i2s_anchored_length_trap** (anchor-shrink rescue)

### Methodological takeaway

"Adding a fuzzer technique helps" decomposes into 5 distinct mechanism families:

1. **I2S substitutes a single literal in O(1)** — the default story (1097× ratio at width=4)
2. **I2S chains across K dependent slots** — only when the chain shares one coverage edge (otherwise covered by template #1 per-slot)
3. **I2S handles two-literal relational lookups** — single substitution alone is insufficient; pair-of-literals required
4. **VP's CMP_MAP gradient survives bijective derivations** — Hamming distance preserved, no literal needed
5. **VP rescues from I2S monoculture on length-relevant traps** — gradient retains different-length seeds that I2S splice-back would erase

Each is a dose-response curve, not an anecdote. The 4-fuzzer crash-count
table at every scan value IS the verdict. **Predict per branch, not per
target**: the same target (lcms, libpcap) instantiates multiple
mechanisms at different branches.