==== BLOCKER ====
Target: harfbuzz
Branch ID: 6814
Location: /src/harfbuzz/src/OT/Color/CPAL/CPAL.hh:176:11
Enclosing function: OT::CPAL::get_palette_colors(unsigned int, unsigned int, unsigned int*, unsigned int*) const
Source line:       if (color_count) *color_count = 0;
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            ?        ?          ?  REFERENCE
cmplog                           0       10          0  loser (value_profile vs value_profile_cmplog)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog); winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=10.40h  loser=24.00h
  avg hitcount on branch: winner=220  loser=0
  prob_div=0.80  dur_div=13.60h  hit_div=220
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=10.40h  loser=24.00h
  avg hitcount on branch: winner=220  loser=0
  prob_div=0.80  dur_div=13.60h  hit_div=220
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/6814/{W,L}/branch_coverage_show.txt

--- Enclosing function: OT::CPAL::get_palette_colors(unsigned int, unsigned int, unsigned int*, unsigned int*) const (/src/harfbuzz/src/OT/Color/CPAL/CPAL.hh:173-190) ---
[ ]   171  				   unsigned int *color_count, /* IN/OUT.  May be NULL. */
[ ]   172  				   hb_color_t   *colors       /* OUT.     May be NULL. */) const
[B]   173    {
[B]   174      if (unlikely (palette_index >= numPalettes))
[B]   175      {
[B]   176        if (color_count) *color_count = 0; <-- BLOCKER
[B]   177        return 0;
[B]   178      }
[ ]   179      unsigned int start_index = colorRecordIndicesZ[palette_index];
[ ]   180      hb_array_t<const BGRAColor> all_colors ((this+colorRecordsZ).arrayZ, numColorRecords);
[ ]   181      hb_array_t<const BGRAColor> palette_colors = all_colors.sub_array (start_index,
[ ]   182  								       numColors);
[ ]   183      if (color_count)
[ ]   184      {
[ ]   185        + palette_colors.sub_array (start_offset, color_count)
[ ]   186        | hb_sink (hb_array (colors, *color_count))
[ ]   187        ;
[ ]   188      }
[ ]   189      return numColors;
[B]   190    }

--- Caller (1 hop): hb_ot_color_palette_get_colors (/src/harfbuzz/src/hb-ot-color.cc:184-186, calls OT::CPAL::get_palette_colors(unsigned int, unsigned int, unsigned int*, unsigned int*) const at line 185) (full body — short) ---
[B]   184  {
[B]   185    return face->table.CPAL->get_palette_colors (palette_index, start_offset, colors_count, colors); <-- CALL
[B]   186  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb_ot_color_palette_get_colors  (/src/harfbuzz/src/hb-ot-color.cc:184-186, calls OT::CPAL::get_palette_colors(unsigned int, unsigned int, unsigned int*, unsigned int*) const at line 185)
hop 3  OT::hb_paint_context_t::get_color(unsigned int, float, int*)  (/src/harfbuzz/src/OT/Color/COLR/COLR.hh:92-114, calls hb_ot_color_palette_get_colors at line 104)
hop 3  hb-shape-fuzzer.cc:test_font(hb_font_t*, unsigned int)  (/src/harfbuzz/test/api/test-ot-face.c:38-198, calls hb_ot_color_palette_get_colors at line 71)
hop 4  OT::ColorStop::get_color_stop(OT::hb_paint_context_t*, hb_color_stop_t*, unsigned int, OT::VarStoreInstancer const&) const  (/src/harfbuzz/src/OT/Color/COLR/COLR.hh:359-364, calls OT::hb_paint_context_t::get_color(unsigned int, float, int*) at line 361)
hop 4  OT::PaintSolid::paint_glyph(OT::hb_paint_context_t*, unsigned int) const  (/src/harfbuzz/src/OT/Color/COLR/COLR.hh:598-606, calls OT::hb_paint_context_t::get_color(unsigned int, float, int*) at line 602)
hop 4  LLVMFuzzerTestOneInput  (/src/harfbuzz/test/fuzzing/hb-shape-fuzzer.cc:13-64, calls hb-shape-fuzzer.cc:test_font(hb_font_t*, unsigned int) at line 51)
hop 5  OT::NoVariable<OT::ColorStop>::get_color_stop(OT::hb_paint_context_t*, hb_color_stop_t*, OT::VarStoreInstancer const&) const  (/src/harfbuzz/src/OT/Color/COLR/COLR.hh:319-321, calls OT::ColorStop::get_color_stop(OT::hb_paint_context_t*, hb_color_stop_t*, unsigned int, OT::VarStoreInstancer const&) const at line 320)
hop 5  OT::Variable<OT::ColorStop>::get_color_stop(OT::hb_paint_context_t*, hb_color_stop_t*, OT::VarStoreInstancer const&) const  (/src/harfbuzz/src/OT/Color/COLR/COLR.hh:266-268, calls OT::ColorStop::get_color_stop(OT::hb_paint_context_t*, hb_color_stop_t*, unsigned int, OT::VarStoreInstancer const&) const at line 267)
hop 5  hb_font_t::paint_glyph(unsigned int, hb_paint_funcs_t*, void*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-font.hh:419-425, calls OT::PaintSolid::paint_glyph(OT::hb_paint_context_t*, unsigned int) const at line 420)
hop 5  hb-ot-font.cc:hb_ot_paint_glyph(hb_font_t*, void*, unsigned int, hb_paint_funcs_t*, void*, unsigned int, unsigned int, void*)  (/src/harfbuzz/src/hb-ot-font.cc:484-498, calls OT::PaintSolid::paint_glyph(OT::hb_paint_context_t*, unsigned int) const at line 486)
hop 6  OT::ColorLine<OT::NoVariable>::get_color_stops(OT::hb_paint_context_t*, unsigned int, unsigned int*, hb_color_stop_t*, OT::VarStoreInstancer const&) const  (/src/harfbuzz/src/OT/Color/COLR/COLR.hh:424-436, calls OT::Variable<OT::ColorStop>::get_color_stop(OT::hb_paint_context_t*, hb_color_stop_t*, OT::VarStoreInstancer const&) const at line 431)
hop 7  OT::ColorLine<OT::NoVariable>::static_get_color_stops(hb_color_line_t*, void*, unsigned int, unsigned int*, hb_color_stop_t*, void*)  (/src/harfbuzz/src/OT/Color/COLR/COLR.hh:444-448, calls OT::ColorLine<OT::NoVariable>::get_color_stops(OT::hb_paint_context_t*, unsigned int, unsigned int*, hb_color_stop_t*, OT::VarStoreInstancer const&) const at line 447)
hop 7  hb_color_line_get_color_stops  (/src/harfbuzz/src/hb-paint.cc:410-416, calls OT::ColorLine<OT::NoVariable>::get_color_stops(OT::hb_paint_context_t*, unsigned int, unsigned int*, hb_color_stop_t*, OT::VarStoreInstancer const&) const at line 411)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     526        60  OT::CPAL::get_palette_colors(unsigned int, unsigned int, unsigned int*, unsigned int*) const  (/src/harfbuzz/src/OT/Color/CPAL/CPAL.hh:173-190)  <-- enclosing
     526        60  hb_ot_color_palette_get_colors  (/src/harfbuzz/src/hb-ot-color.cc:184-186)
      30       180  OT::CPAL::v1() const  (/src/harfbuzz/src/OT/Color/CPAL/CPAL.hh:194-197)
      10        60  OT::CPALV1Tail::get_palette_flags(void const*, unsigned int, unsigned int) const  (/src/harfbuzz/src/OT/Color/CPAL/CPAL.hh:53-57)
      10        60  OT::CPALV1Tail::get_palette_name_id(void const*, unsigned int, unsigned int) const  (/src/harfbuzz/src/OT/Color/CPAL/CPAL.hh:62-65)
      10        60  OT::CPALV1Tail::get_color_name_id(void const*, unsigned int, unsigned int) const  (/src/harfbuzz/src/OT/Color/CPAL/CPAL.hh:70-73)
      10        60  OT::CPAL::has_data() const  (/src/harfbuzz/src/OT/Color/CPAL/CPAL.hh:152-152)
      10        60  OT::CPAL::get_palette_count() const  (/src/harfbuzz/src/OT/Color/CPAL/CPAL.hh:157-157)
      10        60  OT::CPAL::get_palette_flags(unsigned int) const  (/src/harfbuzz/src/OT/Color/CPAL/CPAL.hh:161-161)
      10        60  OT::CPAL::get_palette_name_id(unsigned int) const  (/src/harfbuzz/src/OT/Color/CPAL/CPAL.hh:164-164)
      10        60  OT::CPAL::get_color_name_id(unsigned int) const  (/src/harfbuzz/src/OT/Color/CPAL/CPAL.hh:167-167)
      10        60  hb_ot_color_has_palettes  (/src/harfbuzz/src/hb-ot-color.cc:70-72)
      10        60  hb_ot_color_palette_get_count  (/src/harfbuzz/src/hb-ot-color.cc:86-88)
      10        60  hb_ot_color_palette_get_name_id  (/src/harfbuzz/src/hb-ot-color.cc:109-111)
      10        60  hb_ot_color_palette_color_get_name_id  (/src/harfbuzz/src/hb-ot-color.cc:131-133)
... (7 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OT::CPAL::get_palette_colors(unsigned int, unsigned int, unsigned int*, unsigned int*) const  (/src/harfbuzz/src/OT/Color/CPAL/CPAL.hh:173-190) ---
  d=1   L 176  T=516 F=10  T=0 F=60  if (color_count) *color_count = 0;  <-- BLOCKER

[off-chain: 9 additional divergent branches across 6 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=21547386f8d16a62, size=449 bytes, fuzzer=value_profile_cmplog, trial=4, discovered_at=8128s, mutation_op=ByteRandMutator,BytesInsertMutator,ByteRandMutator,BytesRandInsertMutator):
  0000: 00 01 00 00 00 02 01 02 00 00 00 09 00 00 00 00   ................
  0010: 00 08 00 20 68 cb 74 73 01 19 00 5f 43 4f 4c 52   ... h.ts..._COLR
  0020: 17 fe 02 02 00 00 00 00 00 ff 7f 00 00 ff f9 01   ................
  0030: 00 00 00 00 00 20 20 00 20 20 20 47 50 4f 53 d2   .....  .   GPOS.
Seed 2 (id=11f5184341a1306c, size=452 bytes, fuzzer=value_profile_cmplog, trial=4, discovered_at=8902s, mutation_op=ByteAddMutator,BytesRandInsertMutator,TokenReplace,CrossoverInsertMutator,DwordInterestingMutator):
  0000: 00 01 00 00 00 02 00 00 00 00 00 09 00 00 00 00   ................
  0010: 00 08 00 00 68 63 74 73 00 19 00 5f 43 4f 4c 52   ....hcts..._COLR
  0020: ff fe 40 00 00 00 00 00 00 ff 7f 00 00 ff e6 02   ..@.............
  0030: 00 01 02 00 00 20 20 00 20 20 20 47 50 4f 53 d2   .....  .   GPOS.
Seed 3 (id=0bf9ca2e02fda02b, size=444 bytes, fuzzer=value_profile_cmplog, trial=4, discovered_at=9094s, mutation_op=BytesDeleteMutator,CrossoverInsertMutator):
  0000: 00 01 00 00 00 02 08 00 00 00 00 09 00 00 00 00   ................
  0010: 00 08 0a 00 68 63 74 73 00 19 00 5f 43 4f 4c 52   ....hcts..._COLR
  0020: ff fe 40 02 00 00 00 00 00 ff 7f 00 00 ff e6 02   ..@.............
  0030: 00 01 02 00 00 20 20 00 20 20 20 47 50 4f 53 d2   .....  .   GPOS.
Seed 4 (id=2a485cde89b81906, size=404 bytes, fuzzer=value_profile_cmplog, trial=4, discovered_at=9397s, mutation_op=CrossoverInsertMutator,BytesSetMutator,BytesRandInsertMutator,QwordAddMutator,QwordAddMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 02 01 00 00 00 00 09 00 00 00 00   ................
  0010: 00 08 00 00 68 63 74 73 00 19 00 5f 43 4f 4c 52   ....hcts..._COLR
  0020: ff fe 02 7f 00 00 00 00 00 ff 7f 00 00 ff f9 ff   ................
  0030: ff 00 00 00 00 20 20 00 20 20 20 47 00 00 fc fe   .....  .   G....
Seed 5 (id=0d3525519f286c61, size=715 bytes, fuzzer=value_profile_cmplog, trial=4, discovered_at=10113s, mutation_op=ByteRandMutator,BytesCopyMutator,ByteAddMutator):
  0000: 00 01 00 00 00 02 00 00 00 00 00 09 00 00 00 00   ................
  0010: 00 08 00 00 97 63 74 73 02 19 00 5f 43 4f 4c 52   .....cts..._COLR
  0020: ff fe 01 00 00 00 00 00 00 ff 7f 00 00 ff f9 00   ................
  0030: 00 00 00 00 00 ff ff ff ff 14 0d 47 50 4f 53 d2   ...........GPOS.

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00546490999c9c0b, size=57 bytes, fuzzer=value_profile, trial=1, discovered_at=13s, mutation_op=DwordAddMutator,BytesDeleteMutator,ByteInterestingMutator,TokenInsert,BytesCopyMutator,ByteNegMutator):
  0000: fe ff ff ff f4 01 e0 e0 20 00 00 00 01 20 e0 6a   ........ .... .j
  0010: 79 2d 68 61 6e 74 2d 68 6b 00 20 00 00 00 ff 01   y-hant-hk. .....
  0020: 00 07 00 00 01 20 20 20 01 5b 00 00 00 e0 20 00   .....   .[.... .
  0030: 00 00 01 20 ff 09 fd 20 ff                        ... ... .
Seed 2 (id=000e42f806790cfb, size=96 bytes, fuzzer=value_profile, trial=3, discovered_at=51s, mutation_op=BytesDeleteMutator,TokenInsert,BytesDeleteMutator,BytesDeleteMutator):
  0000: 2d 68 61 6e 73 00 20 20 1a 1a 20 7a 68 2d 68 61   -hans.  .. zh-ha
  0010: 6e 74 fd 1f 1a 1a 3f 1f 1a 1a 3f 10 00 1a 01 00   nt....?...?.....
  0020: 00 00 20 20 6a 62 61 6e 00 1a 1a 1a 20 20 01 3f   ..  jban....  .?
  0030: 20 df 20 00 1a 00 00 00 04 20 00 00 ba 14 01 00    . ...... ......
Seed 3 (id=002a5b2b8b5c414d, size=54 bytes, fuzzer=value_profile, trial=2, discovered_at=70s, mutation_op=TokenReplace,BytesCopyMutator,ByteAddMutator,BytesSetMutator):
  0000: 92 92 92 df 68 2d 68 81 6e 74 00 9a 9a 20 8e 8e   ....h-h.nt... ..
  0010: 8e 8e 79 8e 9a 17 00 00 00 01 20 20 44 46 ff 54   ..y.......  DF.T
  0020: 70 7f 70 70 70 70 70 52 9a 9a ff df 68 2d 68 61   p.pppppR....h-ha
  0030: 6e 74 00 9a 9a 74                                 nt...t
Seed 4 (id=0003cbd2b6f5fff8, size=13 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=BitFlipMutator,BytesDeleteMutator,WordAddMutator):
  0000: e0 17 00 00 1a 20 00 00 29 2b 29 29 2c            ..... ..)+)),
Seed 5 (id=00280212c7547f95, size=27 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=WordInterestingMutator,WordAddMutator,ByteAddMutator):
  0000: e0 e8 ff ff 20 00 00 55 e0 17 00 00 2b 20 00 fa   .... ..U....+ ..
  0010: 20 00 00 55 e0 17 00 00 61 2e 69                   ..U....a.i


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x10                            00(.)x26 74(t)x9 2d(-)x2 e0(.)x2 +20u  PARTIAL
   0x0001  01(.)x10                            01(.)x21 72(r)x8 00(.)x4 08(.)x2 +23u  PARTIAL
   0x0002  00(.)x10                            00(.)x32 75(u)x8 ff(.)x2 61(a)x2 +15u  PARTIAL
   0x0003  00(.)x10                            00(.)x32 65(e)x8 ff(.)x2 6e(n)x2 +15u  PARTIAL
   0x0004  00(.)x10                            00(.)x32 df(.)x2 f4(.)x1 73(s)x1 +24u  PARTIAL
   0x0005  02(.)x10                            01(.)x21 00(.)x7 02(.)x6 20( )x3 +16u  PARTIAL
   0x0007  00(.)x8 02(.)x1 03(.)x1             00(.)x26 20( )x18 01(.)x2 39(9)x2 +12u  PARTIAL
   0x0008  00(.)x10                            00(.)x18 20( )x12 21(!)x9 10(.)x2 +19u  PARTIAL
   0x0009  00(.)x10                            20( )x21 00(.)x7 18(.)x7 10(.)x2 +23u  PARTIAL
   0x000a  00(.)x10                            00(.)x15 df(.)x9 1e(.)x7 ff(.)x7 +14u  PARTIAL
   0x000b  09(.)x10                            00(.)x21 20( )x17 7a(z)x2 9a(.)x1 +19u  DIFFER
   0x000c  00(.)x10                            47(G)x25 00(.)x7 4d(M)x3 01(.)x2 +23u  PARTIAL
   0x000d  00(.)x10                            50(P)x20 20( )x6 00(.)x6 53(S)x5 +13u  PARTIAL
   0x000e  00(.)x10                            4f(O)x20 00(.)x13 55(U)x5 68(h)x2 +17u  PARTIAL
   0x000f  00(.)x10                            53(S)x20 00(.)x14 42(B)x5 61(a)x2 +17u  PARTIAL
   0x0010  00(.)x10                            00(.)x18 20( )x8 02(.)x8 6e(n)x2 +21u  PARTIAL
   0x0011  08(.)x10                            01(.)x12 20( )x10 00(.)x5 04(.)x5 +22u  DIFFER
   0x0012  00(.)x9 0a(.)x1                     00(.)x34 20( )x9 68(h)x1 fd(.)x1 +14u  PARTIAL
   0x0013  00(.)x9 20( )x1                     00(.)x15 0d(.)x8 07(.)x7 06(.)x5 +22u  PARTIAL
   0x0014  68(h)x5 97(.)x5                     00(.)x37 6e(n)x2 10(.)x2 20( )x2 +16u  DIFFER
   0x0015  63(c)x9 cb(.)x1                     00(.)x35 17(.)x2 20( )x2 2d(-)x2 +18u  DIFFER
   0x0016  74(t)x10                            00(.)x42 2d(-)x1 3f(?)x1 ff(.)x1 +14u  DIFFER
   0x0017  73(s)x10                            00(.)x23 10(.)x12 20( )x9 2d(-)x2 +12u  DIFFER
   0x0018  02(.)x5 00(.)x4 01(.)x1             00(.)x29 02(.)x6 20( )x5 68(h)x2 +16u  PARTIAL
   0x0019  19(.)x10                            00(.)x16 02(.)x10 20( )x4 1d(.)x4 +19u  PARTIAL
   0x001a  00(.)x10                            00(.)x24 71(q)x8 20( )x3 6e(n)x2 +20u  PARTIAL
   0x001b  5f(_)x10                            00(.)x18 47(G)x8 f8(.)x6 01(.)x3 +21u  DIFFER
   0x001c  43(C)x10                            00(.)x16 02(.)x5 17(.)x5 20( )x2 +28u  DIFFER
   0x001d  4f(O)x10                            00(.)x24 20( )x5 01(.)x4 03(.)x3 +20u  PARTIAL
   0x001e  4c(L)x10                            00(.)x32 01(.)x5 20( )x3 10(.)x3 +13u  DIFFER
   0x001f  52(R)x10                            00(.)x24 04(.)x6 01(.)x5 53(S)x4 +16u  DIFFER
   0x0020  ff(.)x7 17(.)x3                     00(.)x29 53(S)x6 df(.)x2 10(.)x2 +17u  PARTIAL
   0x0021  fe(.)x10                            00(.)x11 01(.)x8 53(S)x6 20( )x3 +24u  DIFFER
   0x0022  02(.)x5 40(@)x3 01(.)x1 0c(.)x1     00(.)x24 53(S)x7 6e(n)x5 20( )x2 +15u  PARTIAL
   0x0024  00(.)x10                            00(.)x17 20( )x8 4f(O)x6 53(S)x6 +19u  PARTIAL
   0x0025  00(.)x10                            00(.)x10 20( )x9 53(S)x7 02(.)x4 +22u  PARTIAL
   0x0026  00(.)x10                            00(.)x27 20( )x8 53(S)x6 01(.)x2 +13u  PARTIAL
   0x0027  00(.)x10                            00(.)x10 10(.)x8 53(S)x5 04(.)x5 +20u  PARTIAL
   0x0028  00(.)x10                            00(.)x36 ff(.)x2 01(.)x1 9a(.)x1 +15u  PARTIAL
   0x0029  ff(.)x10                            20( )x10 00(.)x8 02(.)x5 10(.)x5 +21u  PARTIAL
   ... (21 more divergent offsets)
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
  prompts_b/harfbuzz_6814.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6814,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>cmplog (value_profile), value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6814 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6814 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6814 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).