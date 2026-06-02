==== BLOCKER ====
Target: harfbuzz
Branch ID: 5442
Location: /src/harfbuzz/src/hb-ot-font.cc:426:7
Enclosing function: hb-ot-font.cc:hb_ot_get_glyph_from_name(hb_font_t*, void*, char const*, int, unsigned int*, void*)
Source line:   if (ot_face->post->get_glyph_from_name (name, len, glyph)) return true;
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           1        9          0  loser (value_profile vs value_profile_cmplog)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        2          0  winner (I2S vs value_profile); winner (value_profile vs cmplog)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=10.10h  loser=24.00h
  avg hitcount on branch: winner=4  loser=0
  prob_div=0.80  dur_div=13.90h  hit_div=4
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=10.10h  loser=22.40h
  avg hitcount on branch: winner=4  loser=0
  prob_div=0.70  dur_div=12.30h  hit_div=4
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5442/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-font.cc:hb_ot_get_glyph_from_name(hb_font_t*, void*, char const*, int, unsigned int*, void*) (/src/harfbuzz/src/hb-ot-font.cc:422-431) ---
[ ]   420  			   hb_codepoint_t *glyph,
[ ]   421  			   void *user_data HB_UNUSED)
[B]   422  {
[B]   423    const hb_ot_font_t *ot_font = (const hb_ot_font_t *) font_data;
[B]   424    const hb_ot_face_t *ot_face = ot_font->ot_face;
[ ]   425  
[B]   426    if (ot_face->post->get_glyph_from_name (name, len, glyph)) return true; <-- BLOCKER
[L]   427  #ifndef HB_NO_OT_FONT_CFF
[L]   428      if (ot_face->cff1->get_glyph_from_name (name, len, glyph)) return true;
[L]   429  #endif
[L]   430    return false;
[L]   431  }

--- No 1-hop callers of hb-ot-font.cc:hb_ot_get_glyph_from_name(hb_font_t*, void*, char const*, int, unsigned int*, void*) fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     168      5810  hb-ot-font.cc:hb_ot_get_nominal_glyph(hb_font_t*, void*, unsigned int, unsigned int*, void*)  (/src/harfbuzz/src/hb-ot-font.cc:136-140)
      72      1740  hb-ot-font.cc:hb_ot_get_glyph_h_advances(hb_font_t*, void*, unsigned int, unsigned int const*, unsigned int, int*, unsigned int, void*)  (/src/harfbuzz/src/hb-ot-font.cc:183-261)
      63      1500  hb-ot-font.cc:hb_ot_get_nominal_glyphs(hb_font_t*, void*, unsigned int, unsigned int const*, unsigned int, unsigned int*, unsigned int, void*)  (/src/harfbuzz/src/hb-ot-font.cc:151-158)
       9       240  hb-ot-font.cc:_hb_ot_font_create(hb_font_t*)  (/src/harfbuzz/src/hb-ot-font.cc:81-116)
       9       240  hb_ot_font_set_funcs  (/src/harfbuzz/src/hb-ot-font.cc:570-579)
       9       238  hb-ot-font.cc:_hb_ot_font_destroy(void*)  (/src/harfbuzz/src/hb-ot-font.cc:120-128)
       9       238  hb-ot-font.cc:_hb_ot_get_font_funcs()  (/src/harfbuzz/src/hb-ot-font.cc:555-557)
       6       160  hb-ot-font.cc:hb_ot_get_font_h_extents(hb_font_t*, void*, hb_font_extents_t*, void*)  (/src/harfbuzz/src/hb-ot-font.cc:439-443)
       3       119  hb-ot-font.cc:hb_ot_get_glyph_extents(hb_font_t*, void*, unsigned int, hb_glyph_extents_t*, void*)  (/src/harfbuzz/src/hb-ot-font.cc:379-397)
       3        92  hb-ot-font.cc:hb_ot_get_variation_glyph(hb_font_t*, void*, unsigned int, unsigned int, unsigned int*, void*)  (/src/harfbuzz/src/hb-ot-font.cc:167-173)
       3        80  hb-ot-font.cc:hb_ot_get_glyph_v_advances(hb_font_t*, void*, unsigned int, unsigned int const*, unsigned int, int*, unsigned int, void*)  (/src/harfbuzz/src/hb-ot-font.cc:272-311)
       3        80  hb-ot-font.cc:hb_ot_get_glyph_v_origin(hb_font_t*, void*, unsigned int, int*, int*, void*)  (/src/harfbuzz/src/hb-ot-font.cc:322-370)
       3        80  hb-ot-font.cc:hb_ot_get_glyph_name(hb_font_t*, void*, unsigned int, char*, unsigned int, void*)  (/src/harfbuzz/src/hb-ot-font.cc:406-415)
       3        80  hb-ot-font.cc:hb_ot_get_glyph_from_name(hb_font_t*, void*, char const*, int, unsigned int*, void*)  (/src/harfbuzz/src/hb-ot-font.cc:422-431)  <-- enclosing
       3        80  hb-ot-font.cc:hb_ot_draw_glyph(hb_font_t*, void*, unsigned int, hb_draw_funcs_t*, void*, void*)  (/src/harfbuzz/src/hb-ot-font.cc:465-472)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-font.cc:hb_ot_get_glyph_from_name(hb_font_t*, void*, char const*, int, unsigned int*, void*)  (/src/harfbuzz/src/hb-ot-font.cc:422-431) ---
  d=1   L 426  T=3 F=0  T=0 F=80  if (ot_face->post->get_glyph_from_name (name, len, glyph)...  <-- BLOCKER
  d=1   L 428  T=0 F=0  T=0 F=80  if (ot_face->cff1->get_glyph_from_name (name, len, glyph)...

[off-chain: 22 additional divergent branches across 9 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=39fb20c9e671238a, size=424 bytes, fuzzer=value_profile_cmplog, trial=6, discovered_at=27785s, mutation_op=CrossoverInsertMutator):
  0000: 74 72 75 65 00 02 20 01 10 00 01 00 70 6f 73 74   true.. .....post
  0010: 02 06 01 00 00 00 00 2d 68 21 00 00 0c 00 0c 00   .......-h!......
  0020: 80 00 9a 9a 66 72 61 48 06 00 2d 68 20 00 02 00   ....fraH..-h ...
  0030: 00 03 04 00 09 54 ef 01 0e 00 20 20 6b 00 76 54   .....T....  k.vT
Seed 2 (id=bff0f4c533988557, size=399 bytes, fuzzer=value_profile_cmplog, trial=6, discovered_at=27785s, mutation_op=BytesSetMutator,BytesInsertMutator,BytesInsertMutator,ByteNegMutator,QwordAddMutator):
  0000: 74 72 75 65 00 02 20 01 10 00 01 00 70 6f 73 74   true.. .....post
  0010: 02 06 01 00 00 00 00 2d 68 21 00 00 0c 00 0c 00   .......-h!......
  0020: 80 00 9a 9a 66 72 61 48 06 00 2d 68 20 00 02 00   ....fraH..-h ...
  0030: 00 03 04 00 09 54 ef 01 0e 00 20 20 6b 00 76 54   .....T....  k.vT
Seed 3 (id=19b2b8630da44940, size=487 bytes, fuzzer=value_profile_cmplog, trial=6, discovered_at=27794s, mutation_op=CrossoverInsertMutator,BytesSetMutator,BytesExpandMutator,BytesRandInsertMutator):
  0000: 74 72 75 65 00 02 20 01 10 00 01 00 70 6f 73 74   true.. .....post
  0010: 02 06 01 00 00 00 00 2d 68 21 00 00 0c 00 0c 00   .......-h!......
  0020: 80 00 9a 9a 66 72 61 48 06 00 2d 68 20 00 02 00   ....fraH..-h ...
  0030: 00 03 04 00 09 54 ef 01 0e 00 20 20 6b 00 76 54   .....T....  k.vT

==== Loser-blocking seeds (take false branch) ====
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
Seed 4 (id=02aaecdd52943718, size=53 bytes, fuzzer=value_profile, trial=3, discovered_at=55s, mutation_op=CrossoverReplaceMutator,ByteRandMutator,BytesInsertCopyMutator,BytesExpandMutator,ByteIncMutator,CrossoverReplaceMutator):
  0000: 00 61 64 6e 4b 19 00 00 10 10 00 00 1a e8 00 00   .adnK...........
  0010: d8 d8 d8 d8 ff 00 00 00 00 10 00 00 00 21 00 83   .............!..
  0020: 65 72 64 6e 4b 19 00 00 6f 4b 19 00 00 ef ff ff   erdnK...oK......
  0030: 00 00 00 00 20                                    .... 
Seed 5 (id=002a5b2b8b5c414d, size=54 bytes, fuzzer=value_profile, trial=2, discovered_at=70s, mutation_op=TokenReplace,BytesCopyMutator,ByteAddMutator,BytesSetMutator):
  0000: 92 92 92 df 68 2d 68 81 6e 74 00 9a 9a 20 8e 8e   ....h-h.nt... ..
  0010: 8e 8e 79 8e 9a 17 00 00 00 01 20 20 44 46 ff 54   ..y.......  DF.T
  0020: 70 7f 70 70 70 70 70 52 9a 9a ff df 68 2d 68 61   p.pppppR....h-ha
  0030: 6e 74 00 9a 9a 74                                 nt...t


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  74(t)x3                             00(.)x37 74(t)x9 e0(.)x2 20( )x2 +29u  PARTIAL
   0x0001  72(r)x3                             01(.)x31 72(r)x8 00(.)x4 17(.)x3 +27u  PARTIAL
   0x0002  75(u)x3                             00(.)x51 75(u)x8 ff(.)x3 6e(n)x2 +16u  PARTIAL
   0x0003  65(e)x3                             00(.)x46 65(e)x8 ff(.)x3 6e(n)x2 +19u  PARTIAL
   0x0004  00(.)x3                             00(.)x44 20( )x2 df(.)x2 f3(.)x2 +29u  PARTIAL
   0x0005  02(.)x3                             01(.)x28 00(.)x7 02(.)x6 20( )x4 +24u  PARTIAL
   0x0006  20( )x3                             00(.)x31 02(.)x9 a0(.)x7 07(.)x6 +18u  PARTIAL
   0x0007  01(.)x3                             00(.)x34 20( )x17 02(.)x8 01(.)x2 +18u  PARTIAL
   0x0008  10(.)x3                             00(.)x31 20( )x12 21(!)x9 10(.)x4 +24u  PARTIAL
   0x0009  00(.)x3                             20( )x22 00(.)x11 1a(.)x9 18(.)x8 +26u  PARTIAL
   0x000a  01(.)x3                             00(.)x24 20( )x14 df(.)x10 1e(.)x7 +15u  PARTIAL
   0x000b  00(.)x3                             00(.)x31 20( )x27 08(.)x2 66(f)x1 +18u  PARTIAL
   0x000c  70(p)x3                             47(G)x35 00(.)x12 4d(M)x4 01(.)x2 +23u  DIFFER
   0x000d  6f(o)x3                             50(P)x27 00(.)x12 53(S)x8 20( )x6 +14u  DIFFER
   0x000e  73(s)x3                             4f(O)x27 00(.)x19 55(U)x8 ff(.)x4 +16u  DIFFER
   0x000f  74(t)x3                             53(S)x27 00(.)x20 42(B)x8 20( )x4 +18u  PARTIAL
   0x0010  02(.)x3                             00(.)x23 20( )x10 02(.)x9 82(.)x7 +22u  PARTIAL
   0x0011  06(.)x3                             20( )x12 00(.)x12 01(.)x12 82(.)x6 +27u  PARTIAL
   0x0012  01(.)x3                             00(.)x36 20( )x10 e0(.)x6 ff(.)x2 +21u  PARTIAL
   0x0013  00(.)x3                             00(.)x15 20( )x9 0d(.)x8 07(.)x7 +29u  PARTIAL
   0x0014  00(.)x3                             00(.)x45 20( )x4 ff(.)x2 10(.)x2 +25u  PARTIAL
   0x0015  00(.)x3                             00(.)x49 17(.)x3 20( )x3 09(.)x2 +19u  PARTIAL
   0x0016  00(.)x3                             00(.)x61 ff(.)x3 01(.)x2 20( )x2 +10u  PARTIAL
   0x0017  2d(-)x3                             00(.)x40 10(.)x12 20( )x10 6e(n)x2 +13u  PARTIAL
   0x0018  68(h)x3                             00(.)x36 80(.)x7 20( )x6 02(.)x6 +21u  PARTIAL
   0x0019  21(!)x3                             00(.)x19 02(.)x9 20( )x5 1d(.)x5 +24u  PARTIAL
   0x001a  00(.)x3                             00(.)x41 71(q)x8 20( )x5 05(.)x3 +19u  PARTIAL
   0x001b  00(.)x3                             00(.)x23 20( )x8 47(G)x8 f8(.)x7 +25u  PARTIAL
   0x001c  0c(.)x3                             00(.)x24 17(.)x6 47(G)x6 02(.)x5 +28u  PARTIAL
   0x001d  00(.)x3                             00(.)x25 01(.)x5 20( )x4 02(.)x4 +27u  PARTIAL
   0x001e  0c(.)x3                             00(.)x41 4f(O)x6 01(.)x4 10(.)x4 +18u  PARTIAL
   0x001f  00(.)x3                             00(.)x24 53(S)x11 01(.)x6 04(.)x6 +22u  PARTIAL
   0x0020  80(.)x3                             00(.)x32 53(S)x7 82(.)x6 10(.)x3 +26u  DIFFER
   0x0021  00(.)x3                             00(.)x15 01(.)x10 53(S)x8 20( )x5 +26u  PARTIAL
   0x0022  9a(.)x3                             00(.)x37 53(S)x8 6e(n)x5 64(d)x2 +18u  DIFFER
   0x0023  9a(.)x3                             00(.)x22 20( )x10 53(S)x7 02(.)x3 +27u  DIFFER
   0x0024  66(f)x3                             00(.)x18 20( )x8 53(S)x7 4f(O)x6 +32u  DIFFER
   0x0025  72(r)x3                             00(.)x17 20( )x10 53(S)x8 02(.)x4 +24u  DIFFER
   0x0026  61(a)x3                             00(.)x38 20( )x7 53(S)x7 01(.)x3 +16u  DIFFER
   0x0027  48(H)x3                             00(.)x21 10(.)x9 53(S)x6 04(.)x5 +23u  DIFFER
   ... (24 more divergent offsets)
==== MECHANISM CONTEXT (involved fuzzers only) ====
--- cmplog ---
**Instrumentation**: naive's edge counters **plus** integer-CMP
interception (`__sanitizer_cov_trace_cmp1/2/4/8`) and
string/memory-CMP interception (`__sanitizer_weak_hook_strcmp`,
`__sanitizer_weak_hook_memcmp`, etc.). Each CMP callback records
both operands into a per-execution `CmpLogObserver` buffer keyed by
PC.

**Feedback**: same edge-bucket signal as naive. The CMP buffer is
consumed by the mutator, not by feedback.

**Mutators**: naive's havoc + token stack **plus** `I2SRandReplace`.
`I2SRandReplace` reads the post-execution `CmpLogObserver` buffer,
picks a CMP entry, scans the input for byte sequences matching one
operand, and substitutes the other operand at those offsets.

**Observed `mutation_op` in seed metadata**:
<!-- TODO(i2s-logging-bug): the current LibAFL fuzzbench build does NOT
     wrap I2SRandReplace in LogMutationMetadata, so the string
     "I2SRandReplace" never appears in `.metadata`. Instead, I2S finds
     surface as seeds whose metadata has ParentInfo but NO mutator-name
     list — these render as `mutation_op = -` in `db_query.py lineage`
     output and `resolving_seeds.mutation_op IS NULL` in SQL.
     Confirmed 2026-05-17: naive/vp produce ZERO such seeds in 6000
     samples; cmplog/vpc produce them at ~0.1–0.3%. This is a LOWER
     BOUND ("floor") — some I2S finds leak into the havoc bucket
     because other stages wrap I2S as a sub-mutator and tag the result
     with their own havoc/token list. When the logging fix lands,
     revert this caveat and require the literal `I2SRandReplace`
     string instead. -->
havoc/token names; **plus** silent ParentInfo-only entries
(`mutation_op = -` in lineage output) that — in cmplog/vpc only —
indicate an I2SRandReplace find under the current build. The dash
rows are exclusive to cmplog and value_profile_cmplog **within the
original 4-fuzzer canonical set**; there their presence in a winning
seed's ancestor chain is direct (lower-bound) evidence of I2S
contribution.
<!-- CAVEAT(10-fuzzer set, 2026-05-27): dash-row = I2S only holds when
     comparing against naive / value_profile. `mopt` and `grimoire`
     wrap their mutators in LineageMutatorWrap with an EMPTY names list,
     so they ALSO emit nameless (`mutation_op = -`) rows for non-I2S
     finds — see the mopt / grimoire sections. Against those two the
     dash signal is NOT I2S-exclusive. fast / minimizer / naive_ctx /
     naive_ngram4 use plain LineageMutator (names captured), so they do
     NOT emit dash rows and the signal stays clean against them. -->

**Per-execution cost**: edge increment + one callback per intercepted
CMP per execution + post-execution CMP-buffer processing.

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
  prompts_b/harfbuzz_5442.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5442,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S), value_profile_cmplog>cmplog (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5442 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5442 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5442 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).