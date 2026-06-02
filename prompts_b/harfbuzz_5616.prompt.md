==== BLOCKER ====
Target: harfbuzz
Branch ID: 5616
Location: /src/harfbuzz/src/hb-ot-post-table.hh:255:11
Enclosing function: OT::post::accelerator_t::find_glyph_name(unsigned int) const
Source line:       if (version != 0x00020000 || glyph >= glyphNameIndex->len)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           2        8          0  loser (value_profile vs value_profile_cmplog)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile); winner (value_profile vs cmplog)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         2        8          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=4.20h  loser=24.00h
  avg hitcount on branch: winner=55089  loser=0
  prob_div=1.00  dur_div=19.80h  hit_div=55089
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=4.20h  loser=19.80h
  avg hitcount on branch: winner=55089  loser=1820
  prob_div=0.80  dur_div=15.60h  hit_div=53269
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5616/{W,L}/branch_coverage_show.txt

--- Enclosing function: OT::post::accelerator_t::find_glyph_name(unsigned int) const (/src/harfbuzz/src/hb-ot-post-table.hh:246-272) ---
[ ]   244  
[ ]   245      hb_bytes_t find_glyph_name (hb_codepoint_t glyph) const
[B]   246      {
[B]   247        if (version == 0x00010000)
[ ]   248        {
[ ]   249  	if (glyph >= format1_names_length)
[ ]   250  	  return hb_bytes_t ();
[ ]   251  
[ ]   252  	return format1_names (glyph);
[ ]   253        }
[ ]   254  
[B]   255        if (version != 0x00020000 || glyph >= glyphNameIndex->len) <-- BLOCKER
[B]   256  	return hb_bytes_t ();
[ ]   257  
[W]   258        unsigned int index = glyphNameIndex->arrayZ[glyph];
[W]   259        if (index < format1_names_length)
[W]   260  	return format1_names (index);
[W]   261        index -= format1_names_length;
[ ]   262  
[W]   263        if (index >= index_to_offset.length)
[W]   264  	return hb_bytes_t ();
[W]   265        unsigned int offset = index_to_offset[index];
[ ]   266  
[W]   267        const uint8_t *data = pool + offset;
[W]   268        unsigned int name_length = *data;
[W]   269        data++;
[ ]   270  
[W]   271        return hb_bytes_t ((const char *) data, name_length);
[W]   272      }

--- Caller (1 hop): OT::post::accelerator_t::cmp_gids(void const*, void const*, void*) (/src/harfbuzz/src/hb-ot-post-table.hh:230-235, calls OT::post::accelerator_t::find_glyph_name(unsigned int) const at line 234) (full body — short) ---
[W]   230      {
[W]   231        const accelerator_t *thiz = (const accelerator_t *) arg;
[W]   232        uint16_t a = * (const uint16_t *) pa;
[W]   233        uint16_t b = * (const uint16_t *) pb;
[W]   234        return thiz->find_glyph_name (b).cmp (thiz->find_glyph_name (a)); <-- CALL
[W]   235      }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  OT::post::accelerator_t::cmp_gids(void const*, void const*, void*)  (/src/harfbuzz/src/hb-ot-post-table.hh:230-235, calls OT::post::accelerator_t::find_glyph_name(unsigned int) const at line 234)
hop 2  OT::post::accelerator_t::get_glyph_name(unsigned int, char*, unsigned int) const  (/src/harfbuzz/src/hb-ot-post-table.hh:163-171, calls OT::post::accelerator_t::find_glyph_name(unsigned int) const at line 164)
hop 3  hb_font_t::glyph_to_string(unsigned int, char*, unsigned int)  (/src/harfbuzz/src/hb-font.hh:628-633, calls OT::post::accelerator_t::get_glyph_name(unsigned int, char*, unsigned int) const at line 629)
hop 3  hb-ot-font.cc:hb_ot_get_glyph_name(hb_font_t*, void*, unsigned int, char*, unsigned int, void*)  (/src/harfbuzz/src/hb-ot-font.cc:406-415, calls OT::post::accelerator_t::get_glyph_name(unsigned int, char*, unsigned int) const at line 410)
hop 4  hb_font_glyph_to_string  (/src/harfbuzz/src/hb-font.cc:1728-1730, calls hb_font_t::glyph_to_string(unsigned int, char*, unsigned int) at line 1729)
hop 5  hb-buffer-serialize.cc:_hb_buffer_serialize_glyphs_json(hb_buffer_t*, unsigned int, unsigned int, char*, unsigned int, unsigned int*, hb_font_t*, hb_buffer_serialize_flags_t)  (/src/harfbuzz/src/hb-buffer-serialize.cc:110-202, calls hb_font_glyph_to_string at line 137)
hop 5  hb-buffer-serialize.cc:_hb_buffer_serialize_glyphs_text(hb_buffer_t*, unsigned int, unsigned int, char*, unsigned int, unsigned int*, hb_font_t*, hb_buffer_serialize_flags_t)  (/src/harfbuzz/src/hb-buffer-serialize.cc:266-348, calls hb_font_glyph_to_string at line 288)
hop 6  hb_buffer_serialize_glyphs  (/src/harfbuzz/src/hb-buffer-serialize.cc:468-507, calls hb-buffer-serialize.cc:_hb_buffer_serialize_glyphs_json(hb_buffer_t*, unsigned int, unsigned int, char*, unsigned int, unsigned int*, hb_font_t*, hb_buffer_serialize_flags_t) at line 498)
hop 7  hb_buffer_serialize  (/src/harfbuzz/src/hb-buffer-serialize.cc:668-685, calls hb_buffer_serialize_glyphs at line 673)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     786        20  OT::post::accelerator_t::find_glyph_name(unsigned int) const  (/src/harfbuzz/src/hb-ot-post-table.hh:246-272)  <-- enclosing
     380         0  OT::post::accelerator_t::cmp_gids(void const*, void const*, void*)  (/src/harfbuzz/src/hb-ot-post-table.hh:230-235)
      21         0  OT::post::accelerator_t::cmp_key(void const*, void const*, void*)  (/src/harfbuzz/src/hb-ot-post-table.hh:238-243)
       5        20  OT::post::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-post-table.hh:136-154)
       5        20  OT::post::accelerator_t::~accelerator_t()  (/src/harfbuzz/src/hb-ot-post-table.hh:156-159)
       5        20  OT::post::accelerator_t::get_glyph_name(unsigned int, char*, unsigned int) const  (/src/harfbuzz/src/hb-ot-post-table.hh:163-171)
       5        20  OT::post::accelerator_t::get_glyph_from_name(char const*, int, unsigned int*) const  (/src/harfbuzz/src/hb-ot-post-table.hh:175-212)
       5        20  OT::post::accelerator_t::get_glyph_count() const  (/src/harfbuzz/src/hb-ot-post-table.hh:219-227)
       5        20  OT::post_accelerator_t::post_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-post-table.hh:330-330)
       5         0  OT::postV2Tail::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-post-table.hh:54-57)
       5         0  OT::post::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-post-table.hh:285-291)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  OT::post::accelerator_t::get_glyph_name(unsigned int, char*, unsigned int) const  (/src/harfbuzz/src/hb-ot-post-table.hh:163-171) ---
  d=2   L 165  T=1 F=4  T=20 F=0  if (!s.length) return false;
  d=2   L 166  T=0 F=4  T=0 F=0  if (!buf_len) return true;
--- d=1  OT::post::accelerator_t::find_glyph_name(unsigned int) const  (/src/harfbuzz/src/hb-ot-post-table.hh:246-272) ---
  d=1   L 247  T=0 F=786  T=0 F=20  if (version == 0x00010000)
  d=1   L 255  T=1 F=785  T=0 F=0  if (version != 0x00020000 || glyph >= glyphNameIndex->len)  <-- BLOCKER
  d=1   L 255  T=0 F=786  T=20 F=0  if (version != 0x00020000 || glyph >= glyphNameIndex->len)  <-- BLOCKER
  d=1   L 259  T=412 F=373  T=0 F=0  if (index < format1_names_length)
  d=1   L 263  T=362 F=11  T=0 F=0  if (index >= index_to_offset.length)

[off-chain: 9 additional divergent branches across 3 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=7253f27adf424cfd, size=166 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=2155s, mutation_op=BytesCopyMutator,TokenInsert,BytesExpandMutator,ByteRandMutator,CrossoverReplaceMutator,DwordAddMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 70 6f 73 74   ......      post
  0010: a0 20 20 20 00 00 00 18 00 02 00 00 00 0a 03 00   .   ............
  0020: 43 43 43 08 05 00 00 00 08 08 08 43 43 43 03 00   CCC........CCC..
  0030: 00 04 03 00 00 0a 01 00 00 01 00 00 6c 62 08 b0   ............lb..
Seed 2 (id=6fbffc772b0bc907, size=142 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=52540s, mutation_op=BytesExpandMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 70 6f 73 74   ......      post
  0010: a0 20 20 20 00 00 00 18 00 02 00 00 00 0a 03 00   .   ............
  0020: 43 43 43 08 05 01 00 00 08 08 08 43 43 43 43 43   CCC........CCCCC
  0030: 43 43 43 00 00 1b 03 00 00 1a 00 00 01 20 20 20   CCC..........   
Seed 3 (id=da22058013804ee1, size=170 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=63153s, mutation_op=ByteFlipMutator,ByteRandMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 70 6f 73 74   ......      post
  0010: a0 20 20 03 00 00 00 18 00 02 00 00 00 0a 03 00   .  .............
  0020: 43 43 43 08 05 00 00 00 08 08 08 43 43 43 43 43   CCC........CCCCC
  0030: 43 43 43 00 00 1b 03 00 00 10 03 01 00 1a 03 00   CCC.............
Seed 4 (id=09b1805ebe195383, size=423 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=74240s, mutation_op=BytesExpandMutator,TokenInsert):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 70 6f 73 74   ......      post
  0010: a0 20 20 20 00 00 00 18 00 02 00 00 00 0a 03 00   .   ............
  0020: 43 43 43 08 05 00 00 00 08 08 08 43 43 43 43 43   CCC........CCCCC
  0030: 43 43 43 01 00 1b 03 00 00 75 75 2d 68 61 6e 73   CCC......uu-hans
Seed 5 (id=84626b769f6a478d, size=429 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=85011s, mutation_op=ByteAddMutator,CrossoverReplaceMutator,BytesInsertCopyMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 70 6f 73 74   ......      post
  0010: a0 20 20 20 00 00 00 18 00 02 00 00 00 0a 03 00   .   ............
  0020: 43 43 43 08 05 00 00 00 08 08 08 43 43 43 43 43   CCC........CCCCC
  0030: 43 43 43 00 00 1b 03 00 00 2d 75 2d 68 61 6e 73   CCC......-u-hans

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=00546490999c9c0b, size=57 bytes, fuzzer=value_profile, trial=1, discovered_at=13s, mutation_op=DwordAddMutator,BytesDeleteMutator,ByteInterestingMutator,TokenInsert,BytesCopyMutator,ByteNegMutator):
  0000: fe ff ff ff f4 01 e0 e0 20 00 00 00 01 20 e0 6a   ........ .... .j
  0010: 79 2d 68 61 6e 74 2d 68 6b 00 20 00 00 00 ff 01   y-hant-hk. .....
  0020: 00 07 00 00 01 20 20 20 01 5b 00 00 00 e0 20 00   .....   .[.... .
  0030: 00 00 01 20 ff 09 fd 20 ff                        ... ... .
Seed 2 (id=0003cbd2b6f5fff8, size=13 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=BitFlipMutator,BytesDeleteMutator,WordAddMutator):
  0000: e0 17 00 00 1a 20 00 00 29 2b 29 29 2c            ..... ..)+)),
Seed 3 (id=00280212c7547f95, size=27 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=WordInterestingMutator,WordAddMutator,ByteAddMutator):
  0000: e0 e8 ff ff 20 00 00 55 e0 17 00 00 2b 20 00 fa   .... ..U....+ ..
  0010: 20 00 00 55 e0 17 00 00 61 2e 69                   ..U....a.i
Seed 4 (id=00167ff70704a0e0, size=23 bytes, fuzzer=value_profile, trial=1, discovered_at=120s, mutation_op=BytesInsertCopyMutator,CrossoverInsertMutator,ByteDecMutator):
  0000: 4c 0e 00 00 4c 0e 00 00 4c 16 00 00 00 18 18 00   L...L...L.......
  0010: 00 42 18 65 0e 00 ff                              .B.e...
Seed 5 (id=0059bffc70552fa0, size=62 bytes, fuzzer=value_profile, trial=1, discovered_at=197s, mutation_op=DwordInterestingMutator,BytesRandInsertMutator,BytesInsertMutator):
  0000: 00 01 0e 00 df 20 00 00 00 00 aa 13 df 20 3d 3d   ..... ....... ==
  0010: 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 00 ff   ==============..
  0020: df 20 00 00 00 00 00 20 20 20 20 20 20 20 20 20   . .....         
  0030: 2c 00 00 00 64 55 55 55 df 20 00 00 00 00         ,...dUUU. ....


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x5                             00(.)x11 e0(.)x2 fe(.)x1 4c(L)x1 +5u  PARTIAL
   0x0001  01(.)x5                             01(.)x11 ff(.)x1 17(.)x1 e8(.)x1 +6u  PARTIAL
   0x0002  00(.)x5                             00(.)x15 ff(.)x2 0e(.)x1 8a(.)x1 +1u  PARTIAL
   0x0003  00(.)x5                             00(.)x16 ff(.)x2 8a(.)x1 b7(.)x1    PARTIAL
   0x0004  00(.)x5                             00(.)x10 df(.)x2 f4(.)x1 1a(.)x1 +6u  PARTIAL
   0x0005  01(.)x5                             01(.)x11 20( )x3 00(.)x3 0e(.)x2 +1u  PARTIAL
   0x0006  20( )x5                             00(.)x8 07(.)x6 20( )x3 e0(.)x1 +2u  PARTIAL
   0x0007  20( )x5                             00(.)x8 20( )x8 e0(.)x1 55(U)x1 +2u  PARTIAL
   0x0008  20( )x5                             21(!)x9 20( )x3 00(.)x2 29())x1 +5u  PARTIAL
   0x0009  20( )x5                             20( )x9 00(.)x2 2b(+)x1 17(.)x1 +7u  PARTIAL
   0x000a  20( )x5                             1e(.)x7 00(.)x5 20( )x3 29())x1 +4u  PARTIAL
   0x000b  20( )x5                             20( )x10 00(.)x7 29())x1 13(.)x1 +1u  PARTIAL
   0x000c  70(p)x5                             47(G)x9 00(.)x2 01(.)x1 2c(,)x1 +7u  DIFFER
   0x000d  6f(o)x5                             50(P)x7 20( )x4 53(S)x2 18(.)x1 +5u  DIFFER
   0x000e  73(s)x5                             4f(O)x7 00(.)x3 55(U)x2 e0(.)x1 +6u  DIFFER
   0x000f  74(t)x5                             53(S)x7 00(.)x3 42(B)x2 6a(j)x1 +6u  DIFFER
   0x0010  a0(.)x5                             00(.)x12 20( )x2 79(y)x1 3d(=)x1 +3u  DIFFER
   0x0011  20( )x5                             01(.)x10 20( )x2 2d(-)x1 00(.)x1 +5u  PARTIAL
   0x0012  20( )x5                             00(.)x14 68(h)x1 18(.)x1 3d(=)x1 +2u  PARTIAL
   0x0013  20( )x4 03(.)x1                     0d(.)x8 00(.)x3 61(a)x1 55(U)x1 +6u  PARTIAL
   0x0014  00(.)x5                             00(.)x11 6e(n)x1 e0(.)x1 0e(.)x1 +5u  PARTIAL
   0x0015  00(.)x5                             00(.)x11 74(t)x1 17(.)x1 3d(=)x1 +5u  PARTIAL
   0x0016  00(.)x5                             00(.)x14 2d(-)x1 ff(.)x1 3d(=)x1 +2u  PARTIAL
   0x0017  18(.)x5                             10(.)x10 00(.)x5 68(h)x1 3d(=)x1 +1u  DIFFER
   0x0018  00(.)x5                             00(.)x11 20( )x2 6b(k)x1 61(a)x1 +3u  PARTIAL
   0x0019  02(.)x5                             02(.)x9 20( )x2 00(.)x1 2e(.)x1 +5u  PARTIAL
   0x001a  00(.)x5                             00(.)x12 20( )x2 69(i)x1 3d(=)x1 +2u  PARTIAL
   0x001b  00(.)x5                             47(G)x8 00(.)x5 3d(=)x1 9f(.)x1 +2u  PARTIAL
   0x001c  00(.)x5                             00(.)x5 01(.)x2 02(.)x2 3d(=)x1 +7u  PARTIAL
   0x001d  0a(.)x5                             00(.)x7 01(.)x2 3d(=)x1 06(.)x1 +6u  DIFFER
   0x001e  03(.)x5                             00(.)x12 ff(.)x1 80(.)x1 01(.)x1 +2u  DIFFER
   0x001f  00(.)x5                             00(.)x9 03(.)x2 01(.)x1 ff(.)x1 +4u  PARTIAL
   0x0020  43(C)x5                             00(.)x9 10(.)x2 df(.)x1 37(7)x1 +4u  DIFFER
   0x0021  43(C)x5                             00(.)x9 0e(.)x2 07(.)x1 20( )x1 +4u  DIFFER
   0x0022  43(C)x5                             00(.)x15 1b(.)x1 01(.)x1            DIFFER
   0x0023  08(.)x5                             00(.)x5 02(.)x3 08(.)x3 04(.)x2 +4u  PARTIAL
   0x0024  05(.)x5                             00(.)x6 4f(O)x6 01(.)x1 4c(L)x1 +3u  DIFFER
   0x0025  00(.)x4 01(.)x1                     00(.)x6 02(.)x4 20( )x1 9f(.)x1 +5u  PARTIAL
   0x0026  00(.)x5                             00(.)x12 20( )x1 9f(.)x1 09(.)x1 +2u  PARTIAL
   0x0027  00(.)x5                             10(.)x7 20( )x3 9f(.)x1 02(.)x1 +5u  DIFFER
   ... (23 more divergent offsets)
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
  prompts_b/harfbuzz_5616.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5616,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5616 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5616 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5616 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).