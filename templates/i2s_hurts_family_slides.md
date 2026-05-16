# Slide deck — "I2S hurts" family (2 templates)

Two reproduced templates that surface the corner cases where adding
the I2S (input-to-state) substitution technique to a fuzzer becomes a
liability rather than an asset. Together they explain why "more
techniques is always better" is naive engineering — each captures a
distinct regime.

A third template (`i2s_jump_table_opacity` / `i2s_indirect_dispatch_opacity`)
attempted to demonstrate compiler-induced visibility loss as an "I2S
hurts" mechanism. Both were refuted (the first on mechanism after
inspecting LibAFL's `__sanitizer_cov_trace_switch` hook; the second on
direction — opacity yielded TIE, not LOSS). They are kept in
`templates/legacy/` as methodology lessons. See
`notes/benchmark_verification_log.md` (2026-05-08 → 2026-05-09 entry)
for the refutation analysis.

---

## Slide 0 — Framing

**The metaphorical-testing setup**
- 4 canonical fuzzers: `naive`, `cmplog`, `value_profile`, `value_profile_cmplog` (vpc)
- Pairwise one-technique deltas isolate WHICH technique drives WHICH divergence
- I2S axis partitions the 4 fuzzers as:
  - **has_I2S** = {cmplog, vpc}
  - **lacks_I2S** = {naive, value_profile}

**The default story** (`i2s_magic_number_gate`, 99 corroborations)
- has_I2S beats lacks_I2S by 100×–1000× on branches gated by literal-equality CMPs.
- *I2S substitution logs the literal, splices it back at the right offset, naive can't guess 2^32.*

**These three templates surface where that default inverts or breaks**
- They differ in WHICH knob makes I2S hurt and HOW the failure manifests across the 4 fuzzers.
- The 4-fuzzer signature (decisive shape) is itself the mechanism diagnostic.

---

## Slide 1 — `i2s_anchored_seed_deviation_trap` (v6)

### What is the feature
A program with **N upstream literal-equality CMPs** (an "anchor zone")
followed by a trap gated on a **separate attribute** (input length, or a
deviation-from-anchor byte) that the I2S dictionary cannot help with.
As N grows, I2S substitution **monocultures** the corpus — every offspring
preserves the N anchors at fixed offsets, starving mutations that would
diversify trap-relevant bytes.

### Prediction
- axis = I2S; has_I2S = {cmp, vpc}, lacks_I2S = {naive, vp}
- **vpc/vp ratio decreases monotonically in N_ARMS_PER_OFFSET** — clean crossover from "I2S helps" to "I2S hurts"
- At N=1 (sparse dict, 16 entries): vpc wins via I2S substitution
- At N=224 (dense dict, 3584 entries): vp wins because I2S monocultures vpc's queue away from the trap field

### How it is designed (synthetic harness — v6)
- **Knob**: `N_ARMS_PER_OFFSET` ∈ {1, 7, 56, 224} — number of valid signatures accepted at each anchor site
- **Fixed 16 anchor sites** packed in bytes 0–64; total I2S dict entries = `16 × N_ARMS_PER_OFFSET` = {16, 112, 896, 3584}
- **Fixed seed length 132B** — eliminates v5's confound where seed length grew with N (which let random mutation hit the trap less often regardless of mechanism)
- Magic anchor `'acsp'` at offset 36; trap fires when `read_be32(data + 128) > 100` (the trap pair (V=10, K=100) lives in cmplog's dictionary as a side-effect of the trap CMP)
- Crash via `__builtin_trap()` so crash count is the resolution proxy
- Throughput-immune secondary metric: corpus byte-distribution at offset 128 (% of queue seeds with bytes 128–131 ∈ {V=10, K=100} anchored values, end-of-trial)

### Why this maps to the source code (origin: lcms `cmsio0.c:776` `_cmsReadHeader`, branch 68)

**ICC profile header byte layout** (`cmsICCHeader`, 128 bytes; example bytes from a typical 564-byte display profile):
```
 offset  size  field            bytes (BE)             interpretation
 ─────  ────  ───────────────  ────────────────────  ──────────────────────────
   0      4   size              00 00 02 34          564 (total profile size)
   4      4   cmmId             41 70 70 6c          'Appl'  ┐
   8      4   version           02 20 00 00          v2.2    │
  12      4   deviceClass       6d 6e 74 72          'mntr'  │ → validDeviceClass()
  16      4   colorSpace        52 47 42 20          'RGB '  │   7-arm switch
  20      4   pcs               58 59 5a 20          'XYZ '  │
  24     12   date              08 dc 00 0a … 00     2014/10/20 ...
  36      4   magic             61 63 73 70          'acsp'  ← THE magic check
  40      4   platform          41 50 50 4c          'APPL'
  44      4   flags             00 00 00 00
  48      4   manufacturer      41 50 50 4c          'APPL'
  52      4   model             00 00 00 00
  56      8   attributes        00 … 00
  64      4   renderingIntent   00 00 00 00
  68     12   illuminant        00 00 f6 d6 …
  80      4   creator           41 50 50 4c          'APPL'
  84     16   profileID         (md5)
 100     28   reserved          00 … 00
 ─────  ────
 total: 128-byte header, followed by TagCount(4B) + TagTable(N×12B) + tag bodies
```

**Key observations**:
- `hdr->size` lives at **offset 0** (first 4 bytes). It declares the *total profile size*, not the header size.
- `hdr->magic = 'acsp'` is at **offset 36** — exactly mirrored by the synthetic's `MAGIC_OFFSET = 36`.
- The four FOURCC fields at offsets **12 / 16 / 20** (deviceClass / colorSpace / pcs) plus magic at **36** are the literal-equality CMPs that fill cmplog's I2S dictionary.

**Simplified real source** (`_cmsReadHeader` at `cmsio0.c:768–830`):
```c
cmsBool _cmsReadHeader(_cmsICCPROFILE* Icc) {
    cmsICCHeader Header;
    cmsIOHANDLER* io = Icc->IOhandler;
    cmsUInt32Number TagCount;

    /* line 776: branch 68 ↓
     * Trap fires when the input has < sizeof(cmsICCHeader) = 128 bytes.
     * No literal CMP — the failure is "I/O handler couldn't read 128 bytes."  */
    if (io->Read(io, &Header, sizeof(cmsICCHeader), 1) != 1) return FALSE;

    /* ── after the read, the literal-CMP gauntlet ── */
    if (_cmsAdjustEndianess32(Header.magic) != cmsMagicNumber) return FALSE;  // 'acsp' at offset 36

    Icc->DeviceClass = _cmsAdjustEndianess32(Header.deviceClass);             // offset 12
    Icc->ColorSpace  = _cmsAdjustEndianess32(Header.colorSpace);              // offset 16
    Icc->PCS         = _cmsAdjustEndianess32(Header.pcs);                     // offset 20
    if (Icc->Version > 0x5000000)                       return FALSE;
    if (!validDeviceClass(Icc->DeviceClass))            return FALSE;         // 7-arm switch on offset 12

    /* ── lines 824–829: the deviation trap that the synthetic mimics ── */
    if (!_cmsReadUInt32Number(io, &TagCount)) return FALSE;                   // bytes 128-131
    if (TagCount > MAX_TABLE_TAG) {                                           // MAX_TABLE_TAG = 100
        cmsSignalError(Icc->ContextID, cmsERROR_RANGE, "Too many tags (%d)", TagCount);
        return FALSE;                                                         // ← THE EXACT CHECK
    }

    /* ... continues into tag-table loop with ~30 more tag-type FOURCC switches ... */
}
```

**The structural pattern**:
- **Branch 68 at line 776 is the I/O-read sentinel** — it fires when input size < 128. vpc's queue is full of well-formed 564-byte ICC inputs (I2S splice-back preserves long structures); vp's queue is free to shrink via `BytesDeleteMutator`, so vp's seeds drop below 128 bytes and trigger the trap.
- The literal-CMP "anchor zone" comes from the cumulative chain *downstream* of the I/O check: `magic` (offset 36) + `validDeviceClass` (7-arm switch on offset 12) + `validColorSpace` + `validPCS` + ~30 tag-type FOURCC switches in the tag-table reader. The I2S dictionary fills with **~50–200 logged FOURCCs** by the time it tries to mutate any input.
- The synthetic v6 abstracts these N upstream literal-equality CMPs into 16 fixed sites × `N_ARMS_PER_OFFSET` valid signatures per site; total dictionary entries 16 × N ∈ {16, 112, 896, 3584} cover the real-target regime (~200) at the a56 dose.

### The synthetic's `TagCount > 100` trap is a 1:1 mapping to a real lcms check

The synthetic uses `if (tag_count > TRAP_K)` where `TRAP_K = 100` and `TRAP_OFFSET = 128`. This is **literally the same shape and constant** as a real lcms check at `cmsio0.c:824–829`:

```c
// cmsio0.c, just after _cmsReadHeader's literal-CMP gauntlet:
if (!_cmsReadUInt32Number(io, &TagCount)) return FALSE;       // bytes 128-131 from input
if (TagCount > MAX_TABLE_TAG) {                                // ← THE EXACT CHECK
    cmsSignalError(Icc->ContextID, cmsERROR_RANGE, "Too many tags (%d)", TagCount);
    return FALSE;
}
```
And in `lcms2_internal.h:801`:
```c
#define MAX_TABLE_TAG       100
```

**The byte-position match is also exact**:
- Real lcms reads TagCount as the 4 bytes immediately after the 128-byte header — i.e. **offset 128** of the input.
- Synthetic v6 reads `TagCount` at `TRAP_OFFSET = 128` from the input.

So the synthetic isn't a structural analog — it directly mimics the real constant `MAX_TABLE_TAG = 100` and the real byte position 128. The mechanism prediction is precise:

| Aspect | Real lcms | Synthetic v6 |
|---|---|---|
| Trap shape | `if (TagCount > MAX_TABLE_TAG)` | `if (tag_count > TRAP_K)` |
| Trap constant | `MAX_TABLE_TAG = 100` | `TRAP_K = 100` |
| Input byte offset | 128 (right after 128B header) | 128 (`TRAP_OFFSET = 128`) |
| What's in the I2S dict | the trap CMP logs `(observed_TagCount, 100)` per execution | identical: `(read_be32(data+128), 100)` per execution |

vpc's I2S dictionary contains both `100` (the threshold) AND `observed_TagCount` (the seed's current value, e.g. 10). `I2SRandReplace` snaps bytes 128–131 to one of those two values when it mutates — keeping vpc's queue forever in the "≤ 100" regime. vp's CMP_MAP gradient walks bytes 128–131 toward larger values without dictionary pressure, eventually finding `TagCount > 100` and tripping the trap.

This is why the **corpus byte-distribution metric** (Slide 1's "% of queue seeds with bytes 128–131 ∈ {V, K=100}") is the right diagnostic — it directly measures the dictionary's pull on the trap field.

**Synthetic harness skeleton** (`template_v6.c`):
```c
#define N_ARMS_PER_OFFSET 56     // ← knob ∈ {1, 7, 56, 224}: dose-controls dict density
#define N_SITES   16             // FIXED: 16 anchor offsets, regardless of knob
#define MAX_ARMS  224            // upper bound for SIGS_TABLE
#define MAGIC_VALUE  0x61637370U // 'acsp'
#define TRAP_OFFSET  128
#define TRAP_K       100

/* 16 anchor offsets packed in bytes [0, 64], skipping 36 (magic).
 * Trap region [128, 132) deliberately kept clear of anchors. */
static const size_t SITE_OFFSETS[16] = {
    0, 4, 8, 12, 16, 20, 24, 28, 32, 40, 44, 48, 52, 56, 60, 64
};

/* SIGS_TABLE[16 × MAX_ARMS]: each site uses a DISTINCT slice of the table.
 * Total UNIQUE I2S dictionary entries = 16 × N_ARMS_PER_OFFSET.
 * Distinct slices ⇒ no inter-site collisions ⇒ dose count is exact. */
static uint32_t SIGS_TABLE[N_SITES * MAX_ARMS];

__attribute__((noinline))
static int valid_at_site(int site, uint32_t v) {  // emits N_ARMS_PER_OFFSET cmps
    for (int i = 0; i < N_ARMS_PER_OFFSET; i++)
        if (v == SIGS_TABLE[site * MAX_ARMS + i]) return 1;
    return 0;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    setup_sigs();                            // initialize SIGS_TABLE once
    if (size < TRAP_OFFSET + 4) return 0;    // FIXED 132B minimum
    if (read_be32(data + 36) != MAGIC_VALUE) return 0;
    /* 16 multi-anchor sites with N_ARMS_PER_OFFSET sigs each */
    for (int s = 0; s < N_SITES; s++)
        if (!valid_at_site(s, read_be32(data + SITE_OFFSETS[s]))) return 0;
    /* ── the trap: deviation check with NO literal for I2S to substitute ── */
    if (read_be32(data + TRAP_OFFSET) > TRAP_K) __builtin_trap();
    return 0;
}
```

**v6 vs v5 — what changed**:
- v5 varied **N_SITES** (4 → 256) ⇒ seed length grew with N ⇒ random mutation hit the trap field LESS often as N grew. Two confounded effects (dict breadth + seed length).
- v6 **fixes 16 sites** at fixed offsets in fixed-size 132B inputs; varies **arms per site** instead. Total dict entries = 16 × N_ARMS_PER_OFFSET ∈ {16, 112, 896, 3584}, but the trap region (offsets 128–131) stays in identical relative position to the input head. Random-mutation hit rate at the trap is constant; only the I2S monoculture pressure varies.

### Real behavior — v6 reproduction (n=5 trials × 600s, fixed 132B seeds)

**Median crash count, all 4 fuzzers** (clean monotonic crossover from "I2S helps" to "I2S hurts" on the vp/vpc pair; naive/cmp pinned at the floor):

| N_ARMS | dict | naive | cmp | **vp** | **vpc** | vpc/vp | reading |
|---:|---:|---:|---:|---:|---:|---:|---|
| 1   | 16   | 12 | 15   | 1725 | **8115** | **4.70×** | I2S helps — sparse dict, vpc substitutes cheaply |
| 7   | 112  | 15 | 15   | 2094 | **4590** | **2.19×** | I2S still helps but margin shrinking |
| 56  | 896  | 27 | 1176 | **2709** | 1092 | **0.40×** | **CROSSOVER** — vp now beats vpc by 2.5× |
| 224 | 3584 | 12 | 15   | **4830** | 924  | **0.19×** | I2S hurts at full strength — vp beats vpc by 5.2× |

The crossover between N=7 and N=56 is the defining v6 result: the same fuzzer pair flips from has_I2S-wins to has_I2S-loses as a SINGLE compile-time knob crosses a dictionary-density threshold.

**What the absolute curves show separately**:
- **vpc**: monotone-decreasing (8115 → 4590 → 1092 → 924) — its I2S advantage erodes as the dictionary grows past the useful regime; at high density the splice-back monocultures the queue away from the trap.
- **vp**: monotone-increasing (1725 → 2094 → 2709 → 4830) — vp's CMP_MAP gradient is dose-immune to I2S dictionary size; it actually *gains* slightly as N grows because the per-anchor-site coverage edges accumulate, giving vp's gradient more retention buckets.
- **naive** and **cmp**: floor at 12–27 across all densities (cmp briefly bumps to 1176 at a56 from a single high-variance trial, otherwise stuck at 15). Neither has a CMP_MAP gradient, so neither can navigate the 16-anchor upstream gate within budget; cmp has I2S but the 16 sites × N arms still demand sequential matches that I2S alone can't compound. Both are pinned at the floor regardless of dose — confirming the divergence is genuinely on the **I2S axis among CMP_MAP-equipped fuzzers** (vp vs vpc), not a wider 4-fuzzer story.

The crossover is driven by **both vp and vpc** moving in opposite directions, not just one fuzzer falling. That's the cleanest possible signature of an I2S-hurts mechanism: I2S actively damages vpc while VP positively benefits from the same dose, with naive/cmp held flat as control floors.

v5's design couldn't see this because seed length was a confound; v6 fixes seed length and isolates the dictionary-density axis.

**Secondary metric: corpus byte-distribution at offset 128** (throughput-immune — measured at end-of-trial; v5 numbers, v6 sweep didn't re-measure since the mechanism transferred):

| dict density | vp anchored % | vpc anchored % | gap (pp) |
|---:|---:|---:|---:|
| sparse  | **30%** | 100% | 70 |
| medium  | 36% | 75%  | 39 |
| dense   | 50% | 100% | 50 |
| densest | 78% | 100% | 22 |

vpc's queue stays pinned (100% anchored) at most densities; vp's queue diversifies. This is the proximate monoculture mechanism — vpc's I2S splice-back keeps re-snapping bytes 128–131 to dictionary values regardless of random mutations.

Verdict: `reproduced_v5_v6_v7a_v8_all_three_subtypes` (v6 isolates the dictionary-density axis from v5's seed-length confound; v7a/v8 are further sub-type variants — length / threshold / set-membership traps — all reproduced).

### Metrics
- **Primary**: median crash count per fuzzer per scan value (median, not mean — bimodal stochasticity)
- **Secondary**: median anchor-fraction in corpus at offset 128 (throughput-immune monoculture proxy)
- **Stratification check**: vp > vpc on BOTH metrics at every scan value; vp's queue diversifies (anchor-fraction lower) while vpc's stays pinned (anchor-fraction ≈ 100%)

---

## Slide 2 — `i2s_corpus_pollution`

### What is the feature
A useful chain of K literal-equality CMPs gating a trap, but the chain
shares scope with **N "pollute" CMPs** whose constants are also logged
into I2S. Useful-substitution rate per chain step = K/(K+N); over a
K-step chain it compounds to (K/(K+N))^K → **exponential dilution**
kills cmp at high N. vpc has VP's CMP_MAP gradient as a dilution-immune
fallback channel.

### Prediction
- axis = value_profile (the rescue technique); has_VP = {vp, vpc}, lacks_VP = {naive, cmp}
- **vpc resolves at every COST_INNER**; cmp's resolution decays exponentially
- vpc/cmp ratio diverges as COST_INNER grows
- *The "I2S hurts" angle*: at high pollute, cmp's I2S dictionary is mostly noise — substitutions misfire, cmp burns mutations on dead-end FOURCCs, while naive (no I2S, no overhead) is unaffected at low pollute and dies for a different reason at high.

### How it is designed
- **Knob**: `COST_INNER` ∈ {0, 64, 512, 4096} — pollute-table invocations per execution
- **64-entry pollute table** (constants outside the chain, deliberately distinct)
- **Useful chain**: K=4 sequential equality CMPs → `__builtin_trap()`
- The harness forces a clean K vs N substitution-rate ratio

### Why this maps to the source code (origin: lcms `cmsplugin.c:444` `_cmsReadTypeBase`)

**ICC tag-table byte layout** (what comes after the 128-byte header):
```
 offset            size           field
 ────────         ──────         ──────────────────────────────────────
 128              4              TagCount (uint32 BE)         ← N tags
 132              N × 12         TagTable[N]                  ← per-tag entry:
                                   sig (4B) | offset (4B) | size (4B)
 ...              variable       Tag bodies, located via TagTable[i].offset
                                  Each body starts with _cmsTagBase (8B):
                                     sig (4B FOURCC) | reserved (4B = 0)
                                  followed by tag-type-specific payload.
```

**The 30+ tag-type FOURCCs** that fill cmplog's I2S dictionary (each appears in a `case cmsSig*Type:` of the tag-type dispatch elsewhere in `cmstypes.c`):
```
'curv' 0x63757276  cmsSigCurveType            'mft1' 0x6d667431  cmsSigLut8Type
'para' 0x70617261  cmsSigParametricCurveType  'mft2' 0x6d667432  cmsSigLut16Type
'XYZ ' 0x58595A20  cmsSigXYZType              'mAB ' 0x6d414220  cmsSigLutAtoBType
'text' 0x74657874  cmsSigTextType             'mBA ' 0x6d424120  cmsSigLutBtoAType
'desc' 0x64657363  cmsSigTextDescriptionType  'meas' 0x6D656173  cmsSigMeasurementType
'sf32' 0x73663332  cmsSigS15Fixed16ArrayType  'mluc' 0x6D6C7563  cmsSigMultiLocalizedUnicodeType
'mpet' 0x6D706574  cmsSigMultiProcessElementType                'data' 0x64617461  cmsSigDataType
'sig ' 0x73696720  cmsSigSignatureType        'view' 0x76696577  cmsSigViewingConditionsType
'chrm' 0x6368726D  cmsSigChromaticityType     'cicp' 0x63696370  cmsSigcicpType
'clro' 0x636C726F  cmsSigColorantOrderType    'clrt' 0x636C7274  cmsSigColorantTableType
... (~30 total)
```
Every time the parser dispatches on a tag-type signature, all 30 case literals get logged into vpc's I2S dictionary. After parsing N tags from the table, dictionary breadth ≈ N×K where K ≈ 30 — vpc's queue starts seeing splice-back from a deep pool of FOURCC noise.

**Simplified real source** (`_cmsReadTypeBase` at `cmsplugin.c:438–448`):
```c
cmsTagTypeSignature CMSEXPORT _cmsReadTypeBase(cmsIOHANDLER* io) {
    _cmsTagBase Base;            // 8 bytes: sig (4B) + reserved (4B)
    /* line 444: branch (boolean read-failure) ↓
     * Trap fires when the io handler can't deliver 8 bytes — i.e., the
     * tag body is truncated mid-base-read. NO literal CMP at this site. */
    if (io->Read(io, &Base, sizeof(_cmsTagBase), 1) != 1)
        return (cmsTagTypeSignature) 0;
    return (cmsTagTypeSignature) _cmsAdjustEndianess32(Base.sig);
}
```
And the dispatching switch (caller-side, e.g. `cmstypes.c:2474+`):
```c
sig = _cmsReadTypeBase(io);
switch (sig) {
    case cmsSigCurveType:      Type_Curve_Read(io); break;       // 'curv'
    case cmsSigParametricCurveType: Type_ParametricCurve_Read(io); break;  // 'para'
    case cmsSigLut8Type:       Type_LUT8_Read(io); break;        // 'mft1'
    case cmsSigLut16Type:      Type_LUT16_Read(io); break;       // 'mft2'
    case cmsSigLutAtoBType:    Type_LUTA2B_Read(io); break;      // 'mAB '
    /* ... ~25 more cases — each is a trace_const_cmp4 visible to I2S ... */
}
```
**Pollution mechanism**: each tag-type case in this switch logs a 4-byte FOURCC into cmplog's I2S dictionary. With N tags processed × 30 case values, vpc accumulates dozens to hundreds of "valid signature" entries. When `I2SRandReplace` mutates the input later, it picks uniformly from this dictionary — most picks are useless FOURCCs that don't help the truncation-trap mechanism that the boolean read-failure check actually depends on.

### How the synthetic's `COST_INNER` maps to real lcms

The mapping is **dose-calibrated**, not byte-identical:

| Aspect | Real lcms | Synthetic |
|---|---|---|
| Pollution source | ~30 tag-type case literals × N tags processed | 64 noinline `pollute_<I>(v)` functions, each with one `if (v == K) ...` |
| Pollution dosing | Variable per profile (counts ALL tag-type CMPs visited during parsing — typically 30–500 across the tag table) | `COST_INNER` ∈ {0, 64, 512, 4096} loop count over the 64-entry table |
| What enters the I2S dict | tag-type FOURCC literals (`'curv'`, `'mft1'`, `'mft2'`, `'mAB '`, …) | non-FOURCC constants (`0x10000001`, `0x10000002`, …, `0x40000040`) — deliberately distinct from the chain operands so there's NO incidental useful substitution |
| Useful chain | Magic `'acsp'` + `validDeviceClass` + `validColorSpace` + `validPCS` (~4 sequential gates the seed must pass) | `OP_LD_K → OP_MUL_K → OP_XOR_K → OP_ADD_K` at positions 0/1/2/3 (K=4 chain) |
| Trap shape | Boolean read failure on truncated tag body (`!_cmsReadUInt32Number(...)`) | Equality on the 4-bit `hits` mask (`if (hits == 0xF)`) |

**Why dose-calibrated, not byte-identical**: the corpus_pollution mechanism is a *rate equation* — useful-substitution rate per attempt = K/(K+N), compounding to (K/(K+N))^K over the chain. The mechanism is invariant to *which* literals are in the dictionary; what matters is the **count ratio**. The synthetic uses non-overlapping integer constants on purpose — if pollute values matched the chain operands, they'd accidentally help, polluting the experiment. Real-lcms regime sits at K≈4, N≈30–500, mapping to the synthetic's `COST_INNER ∈ [64, 512]`.

**The 4 useful chain operands** in the synthetic correspond directly to the cumulative chain a seed must pass through to reach the truncation trap: magic check (offset 36) + 7-arm device class (offset 12) + N-arm color space (offset 16) + 2-arm PCS (offset 20). Both have K≈4 sequential equality gates whose substitution probabilities multiply.

**Simplified real source** (paraphrased, abstracted):
```c
void* _cmsReadTypeBase(cmsIOHANDLER* io) {
    cmsTagBase base;
    if (!io->Read(io, &base, sizeof(base), 1)) return NULL;
    /* ── pollute zone: ~30 literal-equality cases fill the I2S dict ── */
    switch (base.sig) {
      case cmsSigCurveType:        return ReadCurveType(io);          // 'curv'
      case cmsSigParametricCurveType: return ReadParametricCurve(io); // 'para'
      case cmsSigLut8Type:         return ReadLut8(io);               // 'mft1'
      case cmsSigLut16Type:        return ReadLut16(io);              // 'mft2'
      case cmsSigLutAtoBType:      return ReadLutAtoB(io);            // 'mAB '
      /* ... ~25 more tag-type cases ... */
      default:                     return NULL;
    }
}
/* Inside ReadLutAtoB(): */
cmsBool ReadLutAtoB(cmsIOHANDLER* io) {
    cmsUInt32Number offsetB;
    if (!_cmsReadUInt32Number(io, &offsetB)) return FALSE; // ← trap branch (truncation)
    /* ... rest of LUT reader ... */
}
```
The tag-type switch logs ~30 FOURCC literals into vpc's I2S dictionary. The trap branch is a boolean check on a stream-read return — fires only when the tag body is truncated mid-`uint32` read, which is **not** in the dictionary. cmp wastes substitutions on polluting FOURCCs; vpc's CMP_MAP gradient navigates truncation byte-arithmetically.

**Synthetic harness skeleton** (`template.c`):
```c
#define COST_INNER 4096                // ← knob: pollute invocations per execution

/* 64-entry pollute table — each function emits one trace_const_cmp4 */
#define POLLUTE_LIST(M) M(0,0x10000001) M(1,0x10000002) ... M(63,0x40000040)
#define DEFINE_POLLUTE(I, K) \
  __attribute__((noinline)) static void pollute_##I(uint32_t v) { \
    if (v == (K)) g_sink += (I); else g_sink ^= v ^ (K); }
POLLUTE_LIST(DEFINE_POLLUTE)
static const pollute_fn_t pollute_table[64] = { POLLUTE_LIST(POLLUTE_NAME) };

static void apply_pollute(const uint8_t* data, size_t size) {
    if (COST_INNER == 0 || size < 4) return;
    uint32_t v = read_u32_be(data);
    for (int j = 0; j < COST_INNER; j++)         // ← dose-controlled pollution
        pollute_table[j % 64](v);
}

/* The useful K=4 chain — the trap requires 4 specific opcodes at 4 specific positions */
static int interp(const uint8_t* prog) {
    int hits = 0;
    for (int i = 0; i < N_INSTR; i++) {
        switch (prog[i*2]) {
          case OP_LD_K:  if (i==0) hits |= 1; break;   // CHAIN[0]
          case OP_MUL_K: if (i==1) hits |= 2; break;   // CHAIN[1]
          case OP_XOR_K: if (i==2) hits |= 4; break;   // CHAIN[2]
          case OP_ADD_K: if (i==3) hits |= 8; break;   // CHAIN[3]
          /* ... 8 other no-op cases ... */
        }
    }
    return hits;
}

int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size) {
    apply_pollute(data, size);                    // ← noise CMPs (dilutes I2S)
    if (size < 16) return 0;
    if (interp(data) == 0xF) __builtin_trap();    // ← K=4 chain trap
    return 0;
}
```
The synthetic abstracts the dispatcher's many useless-FOURCC pollution into a parameterizable `COST_INNER` knob, isolating the (K useful)/(K + N noise) substitution-rate compounding mechanism.

### Real behavior — 4-fuzzer median crash count
**The signature plot of the I2S-hurts family.** n=10 × 600s, bigger is better:

| COST_INNER | naive | cmp | vp | **vpc** |
|---:|---:|---:|---:|---:|
| 0    | 122 | 993 | 43 | **632** |
| 64   | 0   | 109 | 9  | **376** |
| 512  | 0   | **0** ☠ | 30 | **258** |
| 4096 | 0   | **0** ☠ | 1  | **6**   |

- cmp: **993 → 109 → 0 → 0** (exponential decay, dies at c=512)
- vpc: **632 → 376 → 258 → 6** (graceful, never zero — VP rescues)
- vp:  **43 → 9 → 30 → 1** (small but persistent; CMP_MAP gradient is dilution-immune)
- naive: **122 → 0 → 0 → 0** (high-variance bimodal at c=0; collapses for c≥1)

Verdict: `reproduced_4fuzzer_synergy`

### Metrics
- Median crash count per fuzzer per scan value
- **Synergy stratification check**: at scan_values where cmp=0, is vpc>0? (yes at c=512, c=4096)
- has_VP cluster outperforming lacks_VP cluster at high COST_INNER

---

## Slide 3 — (removed; see legacy/)

The original Slide 3 covered `i2s_jump_table_opacity`, later replaced
by `i2s_indirect_dispatch_opacity`. Both refuted; both moved to
`templates/legacy/`. Detail and the methodology lesson are in
`notes/benchmark_verification_log.md`.

<!-- Original Slide 3 content kept below for reference; not part of the deck.

### What is the feature
Clang at -O2 lowers dense contiguous switch statements to **jump tables**:
a single indirect branch indexed by the dispatch value, no per-case
integer comparison emitted. CmpLogObserver hooks `__sanitizer_cov_trace_cmp{1,2,4,8}`
only; the dispatch is **invisible to I2S**. cmp pays tracing-stage
overhead with zero I2S signal to recover; naive is unhindered.

### Prediction
- axis = I2S; has_I2S = {cmp, vpc}, lacks_I2S = {naive, vp}
- **Direction crosses parity** as N_CASES grows:
  - Small N (compare-chain regime) → has_I2S wins (`i2s_magic_number_gate` territory)
  - Large N (jump-table regime) → has_I2S LOSES
- The only "I2S hurts" template where the loss isn't corpus-pollution but pure **compiler-induced visibility loss**.

### How it is designed
- **Knob**: `N_CASES` — number of contiguous switch cases (target case at fixed position)
- Below clang -O2's chain-vs-table threshold (~5–8 dense cases): per-case `trace_const_cmp4` emitted; cmp wins
- Above threshold: jump-table emitted; cmp blind, paying pure overhead

### Why this maps to the source code (origin: libpcap, 39 of 148 RCA reports)

**Simplified real source** (libpcap `gen_load_llc_linktype`, paraphrased):
```c
struct block* gen_load_llc_linktype(compiler_state_t *cstate) {
    /* dense switch over DLT_* — 60+ contiguous case values, lines 3218-3623 */
    switch (cstate->linktype) {
      case DLT_NULL:                  return gen_loadx_iphl(cstate);
      case DLT_EN10MB:                return gen_etherload_link(cstate);
      case DLT_PPP:                   return gen_ppp_load_link(cstate);
      case DLT_PPP_BSDOS:             return gen_pppbsd_load_link(cstate);
      case DLT_PPP_SERIAL:            return gen_ppp_load_serial(cstate);
      case DLT_LOOP:                  return gen_loop_load_link(cstate);
      /* ... 60+ more DLT case values ... */
      case DLT_LINUX_PPP_WITHDIRECTION: return gen_lwd_load_link(cstate);
      default:                        bpf_error(...);
    }
}
```
At `clang -O2` this lowers to a **jump table**: one indirect branch + a `.rodata` table of jump targets. **No per-case `trace_const_cmp4` emitted.** CmpLogObserver registers no hooks; the case literals never enter the I2S dictionary; `I2SRandReplace` has nothing to substitute. cmp pays full cmplog tracing-stage overhead with zero I2S signal.

**Synthetic harness skeleton** (`template.c`):
```c
#define N_CASES 64                          // ← knob: forces jump-table lowering at N>=16
#define TARGET_CASE  (N_CASES / 2)

#define CASE_BODY(I) case I: \
    if ((I) == TARGET_CASE) __builtin_trap(); \
    g_sink ^= (uint32_t)((I) + 1); break;
/* Macros expand to N_CASES contiguous cases. Compile-time-folded
 * conditional makes only TARGET_CASE compile to __builtin_trap();
 * non-target cases compile to just the sink + break. NO runtime
 * comparison — the only path to the trap is the dispatch landing
 * on case TARGET_CASE. */
#define CASES_64(start) /* expands to 64 CASE_BODY entries */
/* ... CASES_4 / CASES_16 / CASES_256 variants ... */

__attribute__((noinline))
static void dispatch(uint32_t v) {
    uint32_t m = v % (uint32_t)N_CASES;     // forces dense contiguous range [0..N)
    switch (m) {
      CASES_64(0)                            // ← clang lowers to jump table at N>=16
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;
    dispatch(read_u32_be(data));
    return 0;
}
```
The synthetic abstracts "any dense contiguous switch the compiler lowers to a jump table." `N_CASES ∈ {4, 16, 64, 256}` lets us cross the chain-vs-table threshold; below it, the per-case CMPs ARE visible and cmp wins (`i2s_magic_number_gate` regime); above, the dispatch is opaque and naive wins.

### How the synthetic's `N_CASES` maps to real libpcap

The mapping is **at the compiler-decision level**, not at the byte-position level:

**Real libpcap** (`gencode.c:1214`, `gen_load_dlt_internal`):
```c
switch (cstate->linktype) {            // 60+ DLT_* case values
    case DLT_ARCNET:        /* DLT=7 */         ...
    case DLT_EN10MB:        /* DLT=1 */         ...
    case DLT_SLIP:          /* DLT=8 */         ...
    case DLT_NULL:          /* DLT=0 */
    case DLT_LOOP:          /* DLT=12 */        ...
    case DLT_PPP:           /* DLT=9 */         ...
    case DLT_PPP_SERIAL:    /* DLT=50 */        ...
    case DLT_RAW:           /* DLT=12,14 */
    case DLT_FDDI:          /* DLT=10 */        ...
    case DLT_IEEE802_11:    /* DLT=105 */
    case DLT_PRISM_HEADER:  /* DLT=119 */       ...
    case DLT_LINUX_SLL:     /* DLT=113 */       ...
    case DLT_LINUX_PPP_WITHDIRECTION: /* DLT=166 */ ...
    /* ... 60+ more ... */
}
```

DLT values aren't perfectly contiguous, but the case set is **dense enough in [0..200] that clang -O2 picks jump-table lowering** (clang's heuristic: dense range + ≥5 cases ⇒ jump table). 39 of 148 libpcap RCA reports concentrate at this and sibling switches (`gen_linktype`, `gen_load_llc_linktype`).

**Synthetic** (`template.c`):
```c
switch (m) {                           // m = v % N_CASES, m ∈ [0..N_CASES)
    case 0:   ...                      // contiguous case values 0..N-1
    case 1:   ...
    /* ... up to N_CASES-1 ... */
}
```

The synthetic uses **strictly contiguous case values** to *guarantee* jump-table lowering at any reasonable -O2 threshold, regardless of clang version.

**Compiler-level 1:1 match**:
| Aspect | Real libpcap | Synthetic |
|---|---|---|
| Source shape | `switch (linktype)` over 60+ DLT_* case values | `switch (m)` over N_CASES contiguous values |
| Case-value density | ~60 cases in [0..200] range — dense enough | N cases in [0..N) range — maximum density (1.0) |
| Compiler decision (clang -O2) | Jump-table lowering | Jump-table lowering at N≥16; comparison-chain at N=4 |
| Sancov instrumentation emitted | NO `trace_const_cmp4` per case (the dispatch is an indirect branch) | NO `trace_const_cmp4` per case at N≥16; per-case CMPs at N=4 |
| What enters the I2S dictionary | Nothing from the dispatch (the DLT_* literals never appear in a `cmp` instruction) | Nothing from the dispatch at N≥16 |

**Why N=4 is the control point**: at N=4 (only 4 contiguous cases), clang typically falls back to a comparison chain — emitting 4 `trace_const_cmp4` instructions that ARE visible to cmplog's I2S. This makes the synthetic span both regimes:
- **N=4**: compare-chain regime, cmp **wins** (this is the `i2s_magic_number_gate` direction)
- **N≥16**: jump-table regime, cmp **loses** (the I2S-hurts direction)

The same fuzzer pair (cmp, naive) flips direction within a single template, on a single knob, demonstrating that "I2S helps" and "I2S hurts" depend on **what the compiler emits**, not on what the source code looks like.

**The byte position isn't 1:1**: in real libpcap, `linktype` doesn't come from a fixed input offset — it's set by the application (or pcap file header) and stored in the `compiler_state_t` structure. The synthetic reads bytes 0–3 of the input as the dispatch value, which is a *simplification*. The mechanism mapping survives because dispatch-value source is irrelevant to the compiler's lowering decision; both produce the same machine-code shape.

### Real behavior — v3 dose-response (n=5 trials × 600s, jump-table dispatch isolated)

**4-fuzzer median crash count** at every distractor-count `d` (bigger is better):

| d (distractors) | naive   | cmp  | vp   | vpc  | **cmp/naive ratio** |
|---:|---:|---:|---:|---:|---:|
| 0    | **17817** | 3162 | 4491 | 2127 | **0.18×** ← cmp 5.6× WORSE |
| 16   | **17346** | 4554 | 4413 | 1689 | 0.26× |
| 64   | **15147** | 3693 | 4359 | 1719 | 0.24× |
| 4096 |  1674 |  468 | 1161 |  411 | 0.28× |

- Full ranking at every d: **naive ≫ vp > cmp ≥ vpc**
- naive dominates by 3.5×–8.4× across all scan values — augmentation overhead dominates when no I2S/VP signal is available from the dispatch.
- vpc loses to cmp at every d — adding VP on top of cmp doesn't rescue here because the dispatch is opaque to BOTH techniques.

Verdict: `reproduced (direction only)` — the load-bearing claim (cmp < naive at jump-table dispatch) holds at all 4 scan values. Dose-response on `d` is roughly flat (ratio ≈ 0.18–0.28), consistent with the hypothesis that the loss is from compiler-induced visibility loss + tracing tax, not from a corpus-pollution effect that scales with `d`.

### Metrics
- cmp/naive median ratio at fixed d=0 (jump-table regime isolated)
- **"I2S hurts" criterion**: ratio < 1.0 (cmp loses to naive)
- Counter-example to `i2s_magic_number_gate` (where ratio is 43×–1097×) — same axis, **opposite direction**

-->

---

## Slide 4 — Cross-template synthesis: when does I2S hurt?

| Template | Axis | "I2S hurts" mechanism | Knob (scan values) | Headline number (real) |
|---|---|---|---|---|
| `i2s_anchored_seed_deviation_trap` | I2S | Dictionary monocultures vpc's queue, biasing away from trap-relevant bytes | `N_ARMS_PER_OFFSET` ∈ {1, 7, 56, 224} (fixed 16 sites, fixed 132B seed) | vpc/vp = **4.70×** → **0.19×** (clean crossover at N≈56); vpc anchor-fraction stays 75–100% across all densities |
| `i2s_corpus_pollution` | value_profile | I2S dictionary diluted by N noise CMPs; useful rate (K/(K+N))^K → 0 | `COST_INNER` ∈ {0, 64, 512, 4096} | cmp median = **0** at c≥512; vpc median = **6** at c=4096 (VP rescues; ratio diverges) |

### 4-fuzzer signature reads as the differentiator

The decisive-shape vocabulary at the source branch tells you which template applies:

- **`--RB`** / **`B-RB`** (vpc=B, vp=R) → **anchored seed deviation** (I2S over-preservation)
- **`-BBR`** / **`BBRR`** (cmp=B, vpc=R) → **corpus pollution** (VP rescues from polluted I2S)

The shape vocabulary IS the mechanism family. A new branch with one of
these signatures probably maps to the matching template; a branch with
an unfamiliar shape is a candidate for a new template.

**`RBRB` is NOT in the family.** The earlier conjecture that jump-table /
indirect-dispatch opacity would yield `RBRB` (lacks_I2S wins both edges)
was refuted: pure absence of I2S signal yields a TIE between cmp and
naive, not a LOSS. Producing `RBRB` requires an actively penalizing
mechanism, not just instrumentation invisibility. The few `RBRB`-shape
branches in the canonical DB resolve to anchored-seed or
switch-default mechanisms after source inspection, not to opacity.

### Methodological takeaway

Calling cmplog "the I2S fuzzer that helps" is incomplete. Two falsifiable
synthetic harnesses show:
1. I2S **monocultures** queues when many literal CMPs precede an attribute-gated trap.
2. I2S **dilutes** under noise CMPs unless paired with VP's gradient fallback.

Each is a dose-response curve, not an anecdote. The 4-fuzzer crash-count
table at every scan value IS the verdict.

A third candidate ("I2S **invisible** to compiler-emitted dispatches —
jump tables / function-pointer tables") was refuted. The mechanism
exists (the dispatch is opaque to all sancov value-side hooks) but the
predicted consequence does not: cmp's tax under opacity is too small
to measurably lose to naive at synthetic-budget. The lesson is recorded
in `notes/benchmark_verification_log.md` (2026-05-08 → 2026-05-09).

---

## Slide 5 — Predicting the template from the source code

The 4-fuzzer signature shows up *after* fuzzing. To predict it *before* fuzzing — given a branch in some target — answer one question and walk a short tree.

### The single diagnostic question

> **Where do the upstream literal-equality CMPs take their operand from?**

Both anchored-seed and corpus-pollution have a pile of `if (X == LITERAL)` CMPs ahead of the trap. The only thing that distinguishes them is what `X` is.

### Decision tree

```
[Branch B you want to predict]
          │
          ▼
Q1. Is B itself a literal-equality CMP (`x == K`)?
          │
   ┌──────┴──────┐
  yes            no  →  I2S-hurts territory (continue)
   │
   ▼
i2s_magic_number_gate  →  vpc wins big (default story, 99 corroborations)


[I2S-hurts continued: B is range / length / set-membership / IO-fail / default-arm]
          │
          ▼
Q2. Trace upstream. What feeds the literal-CMPs the seed must
    already pass to reach B?
          │
   ┌──────┴──────────────────────────────────────────────┐
   ▼                                                      ▼
Operand = bytes at FIXED input offsets                 Operand = parser-/dispatcher-
(header fields read as data[k] for compile-time k)     derived values (token, opcode,
                                                        tag-type after stream-read)
          │                                                      │
          ▼                                                      ▼
    ANCHORED SEED                                         CORPUS POLLUTION
    primary pair: vp > vpc                                primary pair: vpc > cmp
    axis: I2S                                             axis: value_profile
    shape: --BR / B-BR                                    shape: -BBR / BBRR
```

(A previously-included third branch on "compiler dispatch opacity"
predicted shape `RBRB` was refuted. Dense switches and function-pointer
tables produce TIE between cmp and naive, not LOSS. Branches reached
via such dispatch don't fall into the I2S-hurts family — investigate
them as anchored-seed / corpus-pollution / switch-default candidates
instead.)

### Source-pattern crib sheet

**Anchored seed** — the "fixed-position header" pattern:

```c
/* Each upstream cmp pins offset → literal in the I2S dict. */
if (read_be32(data + 0)  != ICC_MAGIC)        return BAD;   // offset 0 pinned
if (read_be32(data + 12) != DEVICE_CLASS_OK)  return BAD;   // offset 12 pinned
if (read_be32(data + 36) != 'acsp')           return BAD;   // offset 36 pinned
...
/* THE TRAP — operand at a different fixed offset, NOT a literal-equality */
if (read_be32(data + 128) > 100) __builtin_trap();          // length / threshold
```

Diagnostic source features:
- ✓ Binary file format with **fixed-position magic / discriminator fields** at compile-time-known byte offsets
- ✓ Trap byte position is **outside** the cluster of pinned offsets
- ✓ Trap predicate is **NOT** literal-equality: `>`, `<`, `size < N`, `!validSet()`, `Read(...) != 1`
- ✓ Seed corpus is **long** (must pass many upstream gates → seeds carry full structure)
- Real instances: ICC profile header (lcms `cmsio0.c:776/824`), PNG/JPEG/TTF magic-validators, ELF header, ZIP central-directory, any record-with-magic format

**Corpus pollution** — the "wide dispatch" pattern:

```c
/* Operand isn't from a fixed offset — it's a parsed / dispatched value. */
parse_input(data, &state);
sig = read_next_token(&state);          // parsed value, not data[k]
switch (sig) {                          // ⬅ POLLUTION SOURCE: many sibling arms
    case TAG_CURVE:    handle_curve(); break;     // 'curv' → I2S dict
    case TAG_LUT8:     handle_lut8();  break;     // 'mft1' → I2S dict
    case TAG_LUTAB:    handle_lutab(); break;     // 'mAB ' → I2S dict
    /* ... ~30+ more arms, each adds one polluting entry ... */
}
/* Inside one of those handlers, a chain of K useful CMPs gates the trap: */
if (channels == 0 || channels >= MAX_CHANNELS) return;  // ⬅ THE TRAP
```

Diagnostic source features:
- ✓ A **wide switch / chained-if** with many literal arms — opcode VM, token table, message-type, tag-type, link-type
- ✓ Dispatched operand from `parse_*()` / `read_*()` calls, **not from a fixed input offset**
- ✓ Reaching the trap requires landing on **one specific arm out of N** (N typically ≥ 30)
- ✓ Arms are sibling literals at the same call site (single dictionary fill point)
- Real instances: VDBE opcode dispatch (sqlite3, ~190 opcodes), TLS record/handshake-type chain (mbedtls), BPF VM dispatch (libpcap), DLT link-type switch (libpcap), tag-type dispatch (lcms cmstypes.c)

**Compiler-opaque dispatch** (jump table or function-pointer table) — *not* an I2S-hurts pattern despite earlier conjecture:

```c
/* Looks like corpus pollution but lowered to an indirect branch + .rodata
 * table (or to TABLE[tag](...) via function pointers). No trace_const_cmp4
 * emitted per arm. Synthetic verification (templates/legacy/i2s_indirect_dispatch_opacity)
 * shows naive ≈ cmp at every dose — opacity yields TIE, not LOSS. Treat
 * such branches as anchored-seed / corpus-pollution / switch-default
 * candidates instead. */
switch (linktype) {                     // 60+ DLT_* arms in [0..200]
    case DLT_NULL:        ...
    case DLT_EN10MB:      ...
    case DLT_PPP:         ...
    /* ... 60+ more dense cases ... */
}
```

### 30-second checklist (when in a hurry)

| Question | Anchored | Pollution |
|---|:---:|:---:|
| Upstream cmps at `data[k]` for compile-time `k`? | ✓ | ✗ |
| Upstream cmps from `switch` over `parse_*()` return? | ✗ | ✓ |
| Trap at a different input position than upstream cmps? | ✓ | irrelevant |
| Trap requires a chain of K ≥ 2 literals? | ✗ | ✓ |
| Polluting cluster ≥ 30 entries from one switch site? | rare | ✓ |
| Seed corpus needs to be long (>100 B) to reach branch? | ✓ | usually |
| Trap is length / range / set-non-membership / IO-fail? | ✓ | possible |
| Trap is equality on a parser-derived value? | ✗ | ✓ |

≥ 3 anchored signals → expect `--BR` / `B-BR`.
≥ 3 pollution signals → expect `-BBR` / `BBRR`.
Dense contiguous switch (jump table) or function-pointer dispatch → expect TIE on the I2S edge (cmp ≈ naive); diagnose by other features.

### One last thing worth keeping in mind

A target isn't anchored or polluted — **a branch is**. lcms is the textbook example: header-validation branches (br68 / br72) are anchored-seed; tag-type-dispatch branches (br326 / br233 / br2355) are corpus-pollution. **Same target, same input, different mechanism per branch.** Predict per branch, not per target.
