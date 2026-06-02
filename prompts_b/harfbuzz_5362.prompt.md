==== BLOCKER ====
Target: harfbuzz
Branch ID: 5362
Location: /src/harfbuzz/src/hb-font.cc:1973:7
Enclosing function: hb_font_destroy
Source line:   if (font->destroy)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           6        4          0  REFERENCE
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        2          0  winner (I2S vs value_profile)
naive_ctx                        6        4          0  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             3        7          0  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             3        7          0  REFERENCE
grimoire                         9        1          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=9.90h  loser=24.00h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.80  dur_div=14.10h  hit_div=2
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5362/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb_font_destroy (/src/harfbuzz/src/hb-font.cc:1968-1984) ---
[ ]  1966  void
[ ]  1967  hb_font_destroy (hb_font_t *font)
[B]  1968  {
[B]  1969    if (!hb_object_destroy (font)) return;
[ ]  1970  
[B]  1971    font->data.fini ();
[ ]  1972  
[B]  1973    if (font->destroy) <-- BLOCKER
[L]  1974      font->destroy (font->user_data);
[ ]  1975  
[B]  1976    hb_font_destroy (font->parent);
[B]  1977    hb_face_destroy (font->face);
[B]  1978    hb_font_funcs_destroy (font->klass);
[ ]  1979  
[B]  1980    hb_free (font->coords);
[B]  1981    hb_free (font->design_coords);
[ ]  1982  
[B]  1983    hb_free (font);
[B]  1984  }

--- Caller (1 hop): LLVMFuzzerTestOneInput (/src/harfbuzz/test/fuzzing/hb-shape-fuzzer.cc:13-64, calls hb_font_destroy at line 60) (±10 around call site) ---
[ ]    50    /* Misc calls on font. */
[B]    51    text32[10] = test_font (font, text32[15]) % 256;
[ ]    52  
[B]    53    hb_buffer_t *buffer = hb_buffer_create ();
[ ]    54   // hb_buffer_set_flags (buffer, (hb_buffer_flags_t) (HB_BUFFER_FLAG_VERIFY | HB_BUFFER_FLAG_PRODUCE_UNSAFE_TO_CONCAT));
[B]    55    hb_buffer_add_utf32 (buffer, text32, sizeof (text32) / sizeof (text32[0]), 0, -1);
[B]    56    hb_buffer_guess_segment_properties (buffer);
[B]    57    hb_shape (font, buffer, nullptr, 0);
[B]    58    hb_buffer_destroy (buffer);
[ ]    59  
[B]    60    hb_font_destroy (font); <-- CALL
[B]    61    hb_face_destroy (face);
[B]    62    hb_blob_destroy (blob);
[B]    63    return 0;
[B]    64  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  OT::glyf::subset(hb_subset_context_t*) const  (/src/harfbuzz/src/OT/glyf/glyf.hh:72-125, calls hb_font_destroy at line 95)
hop 2  hb_font_set_parent  (/src/harfbuzz/src/hb-font.cc:2119-2136, calls hb_font_destroy at line 2135)
hop 3  OT::cff2::subset(hb_subset_context_t*) const  (/src/harfbuzz/src/hb-ot-cff2-table.hh:526-526, calls OT::glyf::subset(hb_subset_context_t*) const at line 526)
hop 3  OT::HVAR::subset(hb_subset_context_t*) const  (/src/harfbuzz/src/hb-ot-var-hvar-table.hh:360-360, calls OT::glyf::subset(hb_subset_context_t*) const at line 360)
hop 4  OT::VVAR::subset(hb_subset_context_t*) const  (/src/harfbuzz/src/hb-ot-var-hvar-table.hh:392-392, calls OT::cff2::subset(hb_subset_context_t*) const at line 392)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     206      3760  hb_font_t::has_func_set(unsigned int)  (/src/harfbuzz/src/hb-font.cc:950-952)
      63      3560  hb_font_t::has_func(unsigned int)  (/src/harfbuzz/src/hb-font.cc:956-959)
       0      2350  hb_font_get_glyph  (/src/harfbuzz/src/hb-font.cc:1023-1027)
       1       189  hb_font_funcs_destroy  (/src/harfbuzz/src/hb-font.cc:772-787)
       0       143  OT::glyf_accelerator_t::get_extents(hb_font_t*, unsigned int, hb_glyph_extents_t*) const  (/src/harfbuzz/src/OT/glyf/glyf.hh:333-341)
       2       144  hb-font.cc:hb_font_get_glyph_h_advance_default(hb_font_t*, void*, unsigned int, void*)  (/src/harfbuzz/src/hb-font.cc:212-220)
       0       140  hb_font_funcs_reference  (/src/harfbuzz/src/hb-font.cc:756-758)
       0       140  hb_font_set_funcs  (/src/harfbuzz/src/hb-font.cc:2221-2242)
       2        96  hb_font_destroy  (/src/harfbuzz/src/hb-font.cc:1968-1984)  <-- enclosing
      77         0  hb-font.cc:hb_font_get_nominal_glyph_nil(hb_font_t*, void*, unsigned int, unsigned int*, void*)  (/src/harfbuzz/src/hb-font.cc:125-128)
      56         0  hb-font.cc:hb_font_get_nominal_glyph_default(hb_font_t*, void*, unsigned int, unsigned int*, void*)  (/src/harfbuzz/src/hb-font.cc:136-142)
      56         0  hb-font.cc:hb_font_get_glyph_h_advance_nil(hb_font_t*, void*, unsigned int, void*)  (/src/harfbuzz/src/hb-font.cc:203-205)
       0        48  OT::glyf_accelerator_t::glyf_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/OT/glyf/glyf.hh:153-183)
       0        48  OT::glyf_accelerator_t::~glyf_accelerator_t()  (/src/harfbuzz/src/OT/glyf/glyf.hh:185-187)
       0        48  bool OT::glyf_accelerator_t::get_points<OT::glyf_accelerator_t::points_aggregator_t>(hb_font_t*, unsigned int, OT::glyf_accelerator_t::points_aggregator_t) const  (/src/harfbuzz/src/OT/glyf/glyf.hh:194-224)
... (65 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb_font_destroy  (/src/harfbuzz/src/hb-font.cc:1968-1984) ---
  d=1   L1969  T=1 F=1  T=48 F=48  if (!hb_object_destroy (font)) return;
  d=1   L1973  T=0 F=1  T=48 F=0  if (font->destroy)  <-- BLOCKER

[off-chain: 58 additional divergent branches across 26 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=1cb3b750bf156a0a, size=936 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=9325s, mutation_op=BytesCopyMutator,ByteNegMutator,DwordInterestingMutator):
  0000: 00 01 00 00 00 02 ee ff 00 30 00 20 47 50 4f 53   .........0. GPOS
  0010: 20 20 20 20 00 00 00 00 ff ff 00 ec ec ec ec ec       ............
  0020: ec ec ec ec ec ec ec 18 18 17 20 00 02 00 fd ff   .......... .....
  0030: 00 34 03 00 94 01 01 00 1d 43 20 20 02 01 01 01   .4.......C  ....

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=000f552b447e20c9, size=71 bytes, fuzzer=value_profile, trial=4, discovered_at=0s, mutation_op=ByteFlipMutator,BytesRandInsertMutator,BytesInsertCopyMutator,BytesRandInsertMutator,DwordAddMutator):
  0000: 00 00 1e 1e 1e 1e 0a 1e 1e 1e 01 00 01 ff ff 20   ............... 
  0010: 20 20 20 20 6b 65 72 6e 20 19 20 1f 00 00 c6 c6       kern . .....
  0020: c6 c6 c6 c6 c6 c6 c6 c6 c6 c6 73 6e 2d 20 6e 20   ..........sn- n 
  0030: 20 20 fd ff 10 00 c6 c6 c6 c6 c6 c6 c6 c6 1a 00     ..............
Seed 2 (id=0020f5003f74d6cc, size=31 bytes, fuzzer=value_profile, trial=4, discovered_at=9s, mutation_op=WordInterestingMutator,BytesDeleteMutator,BytesRandInsertMutator,DwordAddMutator,TokenReplace,BitFlipMutator,BytesCopyMutator):
  0000: 00 01 00 1d 00 18 00 00 00 66 66 66 06 20 20 20   .........fff.   
  0010: 6b 65 72 6e 20 80 00 00 ff 20 20 20 6b 65 20      kern ....   ke 
Seed 3 (id=00546490999c9c0b, size=57 bytes, fuzzer=value_profile, trial=1, discovered_at=13s, mutation_op=DwordAddMutator,BytesDeleteMutator,ByteInterestingMutator,TokenInsert,BytesCopyMutator,ByteNegMutator):
  0000: fe ff ff ff f4 01 e0 e0 20 00 00 00 01 20 e0 6a   ........ .... .j
  0010: 79 2d 68 61 6e 74 2d 68 6b 00 20 00 00 00 ff 01   y-hant-hk. .....
  0020: 00 07 00 00 01 20 20 20 01 5b 00 00 00 e0 20 00   .....   .[.... .
  0030: 00 00 01 20 ff 09 fd 20 ff                        ... ... .
Seed 4 (id=000e42f806790cfb, size=96 bytes, fuzzer=value_profile, trial=3, discovered_at=51s, mutation_op=BytesDeleteMutator,TokenInsert,BytesDeleteMutator,BytesDeleteMutator):
  0000: 2d 68 61 6e 73 00 20 20 1a 1a 20 7a 68 2d 68 61   -hans.  .. zh-ha
  0010: 6e 74 fd 1f 1a 1a 3f 1f 1a 1a 3f 10 00 1a 01 00   nt....?...?.....
  0020: 00 00 20 20 6a 62 61 6e 00 1a 1a 1a 20 20 01 3f   ..  jban....  .?
  0030: 20 df 20 00 1a 00 00 00 04 20 00 00 ba 14 01 00    . ...... ......
Seed 5 (id=002a5b2b8b5c414d, size=54 bytes, fuzzer=value_profile, trial=2, discovered_at=70s, mutation_op=TokenReplace,BytesCopyMutator,ByteAddMutator,BytesSetMutator):
  0000: 92 92 92 df 68 2d 68 81 6e 74 00 9a 9a 20 8e 8e   ....h-h.nt... ..
  0010: 8e 8e 79 8e 9a 17 00 00 00 01 20 20 44 46 ff 54   ..y.......  DF.T
  0020: 70 7f 70 70 70 70 70 52 9a 9a ff df 68 2d 68 61   p.pppppR....h-ha
  0030: 6e 74 00 9a 9a 74                                 nt...t


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x1                             00(.)x10 2d(-)x2 e0(.)x2 20( )x2 +30u  PARTIAL
   0x0001  01(.)x1                             00(.)x8 01(.)x3 06(.)x3 ff(.)x2 +29u  PARTIAL
   0x0002  00(.)x1                             00(.)x22 ff(.)x3 61(a)x2 01(.)x2 +18u  PARTIAL
   0x0003  00(.)x1                             00(.)x21 ff(.)x2 6e(n)x2 80(.)x2 +20u  PARTIAL
   0x0004  00(.)x1                             00(.)x8 20( )x2 df(.)x2 f3(.)x2 +34u  PARTIAL
   0x0005  02(.)x1                             00(.)x13 20( )x5 0e(.)x4 01(.)x3 +16u  DIFFER
   0x0006  ee(.)x1                             00(.)x25 01(.)x5 e0(.)x2 20( )x2 +14u  DIFFER
   0x0007  ff(.)x1                             00(.)x28 20( )x2 39(9)x2 1e(.)x1 +15u  PARTIAL
   0x0008  00(.)x1                             00(.)x17 20( )x3 10(.)x3 4c(L)x2 +22u  PARTIAL
   0x0009  30(0)x1                             00(.)x13 20( )x3 0e(.)x3 17(.)x2 +25u  DIFFER
   0x000a  00(.)x1                             00(.)x26 01(.)x4 20( )x2 10(.)x2 +14u  PARTIAL
   0x000b  20( )x1                             00(.)x24 66(f)x1 7a(z)x1 9a(.)x1 +20u  DIFFER
   0x000c  47(G)x1                             00(.)x11 01(.)x3 b9(.)x2 4d(M)x2 +28u  DIFFER
   0x000d  50(P)x1                             00(.)x11 20( )x7 18(.)x4 2d(-)x3 +14u  DIFFER
   0x000e  4f(O)x1                             00(.)x22 20( )x4 ff(.)x3 01(.)x3 +13u  DIFFER
   0x000f  53(S)x1                             00(.)x20 20( )x5 61(a)x2 6a(j)x1 +18u  DIFFER
   0x0010  20( )x1                             00(.)x7 20( )x5 6e(n)x2 11(.)x2 +27u  PARTIAL
   0x0011  20( )x1                             00(.)x7 20( )x5 a9(.)x2 0e(.)x2 +28u  PARTIAL
   0x0012  20( )x1                             00(.)x23 20( )x4 01(.)x3 0a(.)x2 +14u  PARTIAL
   0x0013  20( )x1                             00(.)x18 20( )x3 55(U)x2 0e(.)x2 +21u  PARTIAL
   0x0014  00(.)x1                             00(.)x11 20( )x3 6e(n)x2 0e(.)x2 +25u  PARTIAL
   0x0015  00(.)x1                             00(.)x10 17(.)x3 0e(.)x3 20( )x3 +23u  PARTIAL
   0x0016  00(.)x1                             00(.)x20 01(.)x4 ff(.)x2 1c(.)x2 +15u  PARTIAL
   0x0017  00(.)x1                             00(.)x19 6e(n)x2 01(.)x2 20( )x2 +17u  PARTIAL
   0x0018  ff(.)x1                             00(.)x9 20( )x6 10(.)x3 68(h)x2 +23u  PARTIAL
   0x0019  ff(.)x1                             00(.)x12 20( )x3 01(.)x3 19(.)x2 +21u  PARTIAL
   0x001a  00(.)x1                             00(.)x17 20( )x6 6e(n)x3 01(.)x2 +16u  PARTIAL
   0x001b  ec(.)x1                             00(.)x18 20( )x4 1f(.)x2 01(.)x2 +17u  DIFFER
   0x001c  ec(.)x1                             00(.)x12 20( )x3 6b(k)x2 4b(K)x2 +23u  DIFFER
   0x001d  ec(.)x1                             00(.)x10 20( )x5 65(e)x2 06(.)x2 +22u  DIFFER
   0x001e  ec(.)x1                             00(.)x21 01(.)x5 ff(.)x2 06(.)x2 +13u  DIFFER
   0x001f  ec(.)x1                             00(.)x20 01(.)x2 54(T)x2 10(.)x2 +16u  DIFFER
   0x0020  ec(.)x1                             00(.)x15 df(.)x2 11(.)x2 6a(j)x2 +20u  DIFFER
   0x0021  ec(.)x1                             00(.)x6 20( )x4 10(.)x3 07(.)x2 +25u  DIFFER
   0x0022  ec(.)x1                             00(.)x18 20( )x3 01(.)x2 2d(-)x2 +15u  DIFFER
   0x0023  ec(.)x1                             00(.)x22 5a(Z)x2 0e(.)x2 c6(.)x1 +14u  DIFFER
   0x0024  ec(.)x1                             00(.)x15 20( )x3 6a(j)x2 10(.)x2 +19u  DIFFER
   0x0025  ec(.)x1                             00(.)x9 0e(.)x4 01(.)x3 20( )x2 +22u  DIFFER
   0x0026  ec(.)x1                             00(.)x22 01(.)x3 c6(.)x1 20( )x1 +14u  DIFFER
   0x0027  18(.)x1                             00(.)x14 20( )x3 ff(.)x2 61(a)x2 +19u  DIFFER
   ... (24 more divergent offsets)
==== MECHANISM CONTEXT (involved fuzzers only) ====
--- value_profile ---
**Instrumentation**: naive's edge counters **plus** integer-CMP
interception, but instead of buffering operands per execution (cmplog),
each CMP callback writes into a `CMP_MAP` keyed by (PC, operand-distance
bucket). The distance bucket is a coarse encoding of how close the two
operands were (Hamming distance bucket for `trace_cmp*`; matching-prefix
length for string/memory CMPs).

**Feedback**: edge-bucket signal **plus** new-CMP_MAP-bucket signal
(both via `MaxMapFeedback`-style coverage). An input that produces a
CMP-operand pair closer to matching than any previously-seen pair
adds a new CMP_MAP bucket and is preserved as corpus.

**Mutators**: naive's havoc + token stack. No `I2SRandReplace`.

**Observed `mutation_op` in seed metadata**: havoc/token names only —
no ParentInfo-only entries (no `mutation_op = -` rows). Absence of
the dash signal is direct evidence the seed was found by naive or
value_profile, not by an I2S stage.
<!-- TODO(i2s-logging-bug): when the I2SRandReplace logging fix lands,
     this section becomes "Absence of `I2SRandReplace` is direct
     evidence ..." again. See the cmplog section above for the floor
     caveat. -->


**Per-execution cost**: edge increment + CMP_MAP update per intercepted
CMP per execution.

--- value_profile_cmplog ---
**Instrumentation**: union of cmplog and value_profile — edge counters,
per-execution CMP buffer (`CmpLogObserver`), and CMP_MAP gradient buckets.

**Feedback**: edge-bucket + CMP_MAP-bucket signals.

**Mutators**: naive's havoc + token stack **plus** `I2SRandReplace`.

**Observed `mutation_op` in seed metadata**: havoc/token names; **plus**
silent ParentInfo-only entries (`mutation_op = -` in lineage) — same
floor signal as cmplog. See the cmplog section's
`TODO(i2s-logging-bug)` note.

**Per-execution cost**: edge increment + CMP-buffer record + CMP_MAP
update per intercepted CMP per execution.

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  prompts_b/harfbuzz_5362.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5362,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S)]
  "hypotheses": [
    {
      "covers_pairs": ["cmplog>naive (I2S)"],
        // labels MUST match exactly as in DECISIVE PAIRS (e.g. "cmplog>naive (I2S)")
      "what_input_feature": "concrete description of the bytes/structure required",
      "why_winner_satisfies": "what about the winner inputs meets the requirement",
      "why_loser_doesnt": "what is missing in the loser inputs",
      "mechanism_attribution": "free text — explain which fuzzer technique enables the winner; must agree with claimed_mechanism below"
    }
    // pair_decision="single_feature" => exactly 1 hypothesis whose covers_pairs lists ALL decisive pairs
    // pair_decision="multi_feature"  => 2+ hypotheses, each covers_pairs listing its subset
  ],
  "evidence_trail": [
    {
      "claim": "atomic factual claim (1 sentence)",
      "cited_section": "BLOCKER",
        // pick the canonical short name of the cited section, one of:
        //   BLOCKER | TRIAL VECTOR | DECISIVE PAIRS | SOURCE CONTEXT |
        //   HIT-COUNT DIVERGENCE | DIVERGENT BRANCHES | BRANCH SEEDS |
        //   BYTE DIFF | MECHANISM CONTEXT
        // validator accepts the full section header too (e.g. "BYTE DIFF (W vs L at common offsets)")
      "cited_locator": "offsets 0x06-0x0f | L1701 | seed_id ab12... | etc.",
      "exact_quote": "verbatim substring of the prompt — COPY-PASTE, do not paraphrase"
    }
    // at least ONE entry per hypothesis sub-field (what / why_winner / why_loser / mechanism)
  ],
  "mechanism_consistency_check": {
    "claimed_mechanism": "I2SRandReplace",
      // pick EXACTLY ONE — the technique that enables the WINNER:
      //   comparison-solving (roadblock dimension):
      //     "I2SRandReplace"     (cmplog / vpc input-to-state substitution)
      //     "CMP_MAP gradient"   (vp / vpc Hamming/prefix-distance feedback)
      //   coverage-granularity (feedback dimension):
      //     "context-sensitive coverage" (naive_ctx CtxHook: (call-context, edge) pairs are new coverage)
      //     "ngram coverage"            (naive_ngram4: N-gram edge tuples are new coverage)
      //   mutation/scheduling (mutation dimension):
      //     "grimoire structural"  (grimoire GeneralizationStage + structural/grammar recombination)
      //     "mopt mutation"        (mopt: MOpt-scheduled mutation-operator probabilities)
      //     "calibrated energy"    (minimizer/fast: corpus-minimization / calibrated power schedule)
      //     "aflfast rarity"       (fast: AFLFast rare-edge power schedule)
      //   baseline / fallback:
      //     "havoc-only"         (lucky havoc byte mutation, no CMP introspection)
      //     "token-replace"      (TokenInsert/TokenReplace dictionary mutations)
      //     "other"              (genuinely cannot classify — NOT a substitute for a known technique above)
    "verified_in_lineage": true,
      // pick true or false
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5362 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
    // TODO(i2s-logging-bug): the LibAFL cmplog harness does NOT log
    //   the literal "I2SRandReplace" string into seed metadata. Until
    //   that is fixed, the verification signal is the dash-row floor
    //   (ParentInfo-only entries; SQL NULL mutation_op). Confirmed
    //   2026-05-17: dash rows are exclusive to cmplog/vpc in the
    //   current data (zero occurrences in 6000 naive/vp samples).
    //   When the logging fix lands, revert this rule to require the
    //   literal "I2SRandReplace" name and treat the dash signal as
    //   secondary corroboration.
    // MANDATORY when claimed_mechanism="I2SRandReplace": invoke db_query.py lineage on >=1 winning seed
    //   - if you find at least one I2S-floor row in the ancestor chain (mutation_op = -
    //     for ancestors of a cmplog/vpc-discovered seed): verified_in_lineage=true,
    //     and cite the depth(s) in verification_method.
    //   - if the chain is all-havoc (no dash rows): verified_in_lineage=false; note that
    //     I2S contribution may still exist in the leaked havoc bucket, explain (>=20 chars).
    //   - if you could not run db_query (data missing, etc.): verified_in_lineage=false; explain what blocked you
  },
  "falsifiability": {
    "would_be_refuted_by": "ONE concrete observation that, if true, would kill this hypothesis (something a synthetic experiment could observe, not a story)"
  },
  "weakest_evidence_point": "one sentence naming your single most uncertain claim",
  "confidence": "medium"
    // pick EXACTLY ONE of: "high" | "medium" | "low"
}

RULES:
 - No reference to templates/ anywhere in your output. Classification is a separate later pass.
 - Every hypothesis sub-claim must be supported by >=1 evidence_trail entry.
 - exact_quote must be a LITERAL substring of this prompt — COPY-PASTE, do NOT paraphrase, abbreviate, or summarize. A script (tools/check_analysis.py) will reject quotes that do not appear verbatim (whitespace-tolerant).
 - cited_section: the validator accepts either the canonical short name (BLOCKER, BYTE DIFF, etc.) or the full section header from the prompt.
 - claimed_mechanism and mechanism_attribution must agree on the same technique.
 - When claimed_mechanism = "I2SRandReplace": you MUST invoke `python3 tools/db_query.py lineage` on >=1 winning seed BEFORE finalizing the analysis. Record what you observed in verification_method.


DEEP-DIVE QUERIES:
  python3 tools/db_query.py lineage --branch 5362 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5362 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).