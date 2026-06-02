==== BLOCKER ====
Target: harfbuzz
Branch ID: 5967
Location: /src/harfbuzz/src/hb-ot-shaper-thai.cc:148:5
Enclosing function: hb-ot-shaper-thai.cc:thai_pua_shape(unsigned int, thai_action_t, hb_font_t*)
Source line:     case SDL: pua_mappings = SDL_mappings; break;
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           2        8          0  loser (I2S vs naive)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             5        5          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     9        1          0  REFERENCE
mopt                             9        1          0  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         0       10          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=3.90h  loser=17.40h
  avg hitcount on branch: winner=24  loser=0
  prob_div=0.80  dur_div=13.50h  hit_div=24
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5967/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-thai.cc:thai_pua_shape(unsigned int, thai_action_t, hb_font_t*) (/src/harfbuzz/src/hb-ot-shaper-thai.cc:99-163) ---
[ ]    97  static hb_codepoint_t
[ ]    98  thai_pua_shape (hb_codepoint_t u, thai_action_t action, hb_font_t *font)
[B]    99  {
[B]   100    struct thai_pua_mapping_t {
[B]   101      uint16_t u;
[B]   102      uint16_t win_pua;
[B]   103      uint16_t mac_pua;
[B]   104    } const *pua_mappings = nullptr;
[B]   105    static const thai_pua_mapping_t SD_mappings[] = {
[B]   106      {0x0E48u, 0xF70Au, 0xF88Bu}, /* MAI EK */
[B]   107      {0x0E49u, 0xF70Bu, 0xF88Eu}, /* MAI THO */
[B]   108      {0x0E4Au, 0xF70Cu, 0xF891u}, /* MAI TRI */
[B]   109      {0x0E4Bu, 0xF70Du, 0xF894u}, /* MAI CHATTAWA */
[B]   110      {0x0E4Cu, 0xF70Eu, 0xF897u}, /* THANTHAKHAT */
[B]   111      {0x0E38u, 0xF718u, 0xF89Bu}, /* SARA U */
[B]   112      {0x0E39u, 0xF719u, 0xF89Cu}, /* SARA UU */
[B]   113      {0x0E3Au, 0xF71Au, 0xF89Du}, /* PHINTHU */
[B]   114      {0x0000u, 0x0000u, 0x0000u}
[B]   115    };
[B]   116    static const thai_pua_mapping_t SDL_mappings[] = {
[B]   117      {0x0E48u, 0xF705u, 0xF88Cu}, /* MAI EK */
[B]   118      {0x0E49u, 0xF706u, 0xF88Fu}, /* MAI THO */
[B]   119      {0x0E4Au, 0xF707u, 0xF892u}, /* MAI TRI */
[B]   120      {0x0E4Bu, 0xF708u, 0xF895u}, /* MAI CHATTAWA */
[B]   121      {0x0E4Cu, 0xF709u, 0xF898u}, /* THANTHAKHAT */
[B]   122      {0x0000u, 0x0000u, 0x0000u}
[B]   123    };
[B]   124    static const thai_pua_mapping_t SL_mappings[] = {
[B]   125      {0x0E48u, 0xF713u, 0xF88Au}, /* MAI EK */
[B]   126      {0x0E49u, 0xF714u, 0xF88Du}, /* MAI THO */
[B]   127      {0x0E4Au, 0xF715u, 0xF890u}, /* MAI TRI */
[B]   128      {0x0E4Bu, 0xF716u, 0xF893u}, /* MAI CHATTAWA */
[B]   129      {0x0E4Cu, 0xF717u, 0xF896u}, /* THANTHAKHAT */
[B]   130      {0x0E31u, 0xF710u, 0xF884u}, /* MAI HAN-AKAT */
[B]   131      {0x0E34u, 0xF701u, 0xF885u}, /* SARA I */
[B]   132      {0x0E35u, 0xF702u, 0xF886u}, /* SARA II */
[B]   133      {0x0E36u, 0xF703u, 0xF887u}, /* SARA UE */
[B]   134      {0x0E37u, 0xF704u, 0xF888u}, /* SARA UEE */
[B]   135      {0x0E47u, 0xF712u, 0xF889u}, /* MAITAIKHU */
[B]   136      {0x0E4Du, 0xF711u, 0xF899u}, /* NIKHAHIT */
[B]   137      {0x0000u, 0x0000u, 0x0000u}
[B]   138    };
[B]   139    static const thai_pua_mapping_t RD_mappings[] = {
[B]   140      {0x0E0Du, 0xF70Fu, 0xF89Au}, /* YO YING */
[B]   141      {0x0E10u, 0xF700u, 0xF89Eu}, /* THO THAN */
[B]   142      {0x0000u, 0x0000u, 0x0000u}
[B]   143    };
[ ]   144  
[B]   145    switch (action) {
[B]   146      case NOP: return u;
[L]   147      case SD:  pua_mappings = SD_mappings; break;
[W]   148      case SDL: pua_mappings = SDL_mappings; break; <-- BLOCKER
[ ]   149      case SL:  pua_mappings = SL_mappings; break;
[ ]   150      case RD:  pua_mappings = RD_mappings; break;
[B]   151    }
[B]   152    for (; pua_mappings->u; pua_mappings++)
[B]   153      if (pua_mappings->u == u)
[B]   154      {
[B]   155        hb_codepoint_t glyph;
[B]   156        if (hb_font_get_glyph (font, pua_mappings->win_pua, 0, &glyph))
[ ]   157  	return pua_mappings->win_pua;
[B]   158        if (hb_font_get_glyph (font, pua_mappings->mac_pua, 0, &glyph))
[ ]   159  	return pua_mappings->mac_pua;
[B]   160        break;
[B]   161      }
[B]   162    return u;
[B]   163  }

--- Caller (1 hop): hb-ot-shaper-thai.cc:do_thai_pua_shaping(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) (/src/harfbuzz/src/hb-ot-shaper-thai.cc:224-261, calls hb-ot-shaper-thai.cc:thai_pua_shape(unsigned int, thai_action_t, hb_font_t*) at line 259) (full body — short) ---
[B]   224  {
[ ]   225  #ifdef HB_NO_OT_SHAPER_THAI_FALLBACK
[ ]   226    return;
[ ]   227  #endif
[ ]   228  
[B]   229    thai_above_state_t above_state = thai_above_start_state[NOT_CONSONANT];
[B]   230    thai_below_state_t below_state = thai_below_start_state[NOT_CONSONANT];
[B]   231    unsigned int base = 0;
[ ]   232  
[B]   233    hb_glyph_info_t *info = buffer->info;
[B]   234    unsigned int count = buffer->len;
[B]   235    for (unsigned int i = 0; i < count; i++)
[B]   236    {
[B]   237      thai_mark_type_t mt = get_mark_type (info[i].codepoint);
[ ]   238  
[B]   239      if (mt == NOT_MARK) {
[B]   240        thai_consonant_type_t ct = get_consonant_type (info[i].codepoint);
[B]   241        above_state = thai_above_start_state[ct];
[B]   242        below_state = thai_below_start_state[ct];
[B]   243        base = i;
[B]   244        continue;
[B]   245      }
[ ]   246  
[B]   247      const thai_above_state_machine_edge_t &above_edge = thai_above_state_machine[above_state][mt];
[B]   248      const thai_below_state_machine_edge_t &below_edge = thai_below_state_machine[below_state][mt];
[B]   249      above_state = above_edge.next_state;
[B]   250      below_state = below_edge.next_state;
[ ]   251  
[ ]   252      /* At least one of the above/below actions is NOP. */
[B]   253      thai_action_t action = above_edge.action != NOP ? above_edge.action : below_edge.action;
[ ]   254  
[B]   255      buffer->unsafe_to_break (base, i);
[B]   256      if (action == RD)
[ ]   257        info[base].codepoint = thai_pua_shape (info[base].codepoint, action, font);
[B]   258      else
[B]   259        info[i].codepoint = thai_pua_shape (info[i].codepoint, action, font); <-- CALL
[B]   260    }
[B]   261  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-thai.cc:do_thai_pua_shaping(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-thai.cc:224-261, calls hb-ot-shaper-thai.cc:thai_pua_shape(unsigned int, thai_action_t, hb_font_t*) at line 257)
hop 3  hb-ot-shaper-thai.cc:preprocess_text_thai(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-thai.cc:268-372, calls hb-ot-shaper-thai.cc:do_thai_pua_shaping(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) at line 371)

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  hb-ot-shaper-thai.cc:preprocess_text_thai(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-thai.cc:268-372) ---
  d=3   L 326  T=80 F=5  T=160 F=10  for (buffer->idx = 0; buffer->idx < count /* No need for:...
  d=3   L 346  T=0 F=0  T=2 F=1  while (start > 0 && IS_ABOVE_BASE_MARK (buffer->out_info[...
  d=3   L 349  T=0 F=0  T=0 F=3  if (start + 2 < end)
  d=3   L 363  T=0 F=0  T=2 F=1  if (start && buffer->cluster_level == HB_BUFFER_CLUSTER_L...
  d=3   L 363  T=0 F=0  T=2 F=0  if (start && buffer->cluster_level == HB_BUFFER_CLUSTER_L...
  d=3   L 370  T=5 F=0  T=10 F=0  if (plan->props.script == HB_SCRIPT_THAI && !plan->map.fo...
  d=3   L 370  T=5 F=0  T=10 F=0  if (plan->props.script == HB_SCRIPT_THAI && !plan->map.fo...
--- d=2  hb-ot-shaper-thai.cc:do_thai_pua_shaping(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-thai.cc:224-261) ---
  d=2   L 235  T=80 F=5  T=163 F=10  for (unsigned int i = 0; i < count; i++)
  d=2   L 239  T=69 F=11  T=148 F=15  if (mt == NOT_MARK) {
  d=2   L 253  T=7 F=4  T=0 F=15  thai_action_t action = above_edge.action != NOP ? above_e...
--- d=1  hb-ot-shaper-thai.cc:thai_pua_shape(unsigned int, thai_action_t, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-thai.cc:99-163) ---
  d=1   L 147  T=0 F=11  T=3 F=12  case SD:  pua_mappings = SD_mappings; break;
  d=1   L 148  T=7 F=4  T=0 F=15  case SDL: pua_mappings = SDL_mappings; break;  <-- BLOCKER
  d=1   L 156  T=0 F=7  T=0 F=3  if (hb_font_get_glyph (font, pua_mappings->win_pua, 0, &g...
  d=1   L 158  T=0 F=7  T=0 F=3  if (hb_font_get_glyph (font, pua_mappings->mac_pua, 0, &g...

[off-chain: 14 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=7ef4c9441fb609a2, size=37 bytes, fuzzer=naive, trial=1, discovered_at=2635s, mutation_op=WordInterestingMutator,BytesSetMutator,ByteInterestingMutator,ByteDecMutator,QwordAddMutator,BytesDeleteMutator):
  0000: 98 cb 0d 4e 0d 0e 0e 0e 01 0e 0e 00 0f 0e 00 01   ...N............
  0010: 1e fa 02 4e 1b 0e 00 00 4b 0e 00 00 01 0e 00 01   ...N....K.......
  0020: 1e fa 01 c2 c2                                    .....
Seed 2 (id=bccf91475d0ee4f2, size=143 bytes, fuzzer=naive, trial=1, discovered_at=10751s, mutation_op=BitFlipMutator,BytesDeleteMutator,TokenReplace,WordAddMutator,BytesSwapMutator,TokenInsert,BytesCopyMutator):
  0000: 64 00 00 00 ff 06 06 df 20 03 03 03 03 03 03 03   d....... .......
  0010: 0c 03 03 03 03 00 9c 97 e0 95 00 72 00 e7 e7 65   ...........r...e
  0020: c6 c6 00 00 00 73 6d 63 2b 2c 12 01 00 46 e7 65   .....smc+,...F.e
  0030: c6 c6 00 00 00 73 6d 4e 06 00 c6 c6 c6 c6 c6 c6   .....smN........
Seed 3 (id=1e3773c0ab32fdf6, size=68 bytes, fuzzer=naive, trial=1, discovered_at=45471s, mutation_op=BytesCopyMutator,BytesSetMutator,ByteDecMutator,ByteRandMutator,BytesInsertMutator,WordInterestingMutator,BytesExpandMutator):
  0000: 98 cb 0d 4e 10 0e 00 00 1d 0e 00 00 4b 0e 00 00   ...N........K...
  0010: 0f 0e 00 00 1e fa fa 02 7f ff ff ff bf 92 90 b1   ................
  0020: cb cb 92 cb 92 5d 6f ff 7f ff ff ff ff 00 00 c2   .....]o.........
  0030: 7a 6f d2 92 92 92 97 4b 4b 4b 4b a0 a0 a0 a0 a0   zo.....KKKK.....
Seed 4 (id=d7519fa8924ad473, size=208 bytes, fuzzer=naive, trial=1, discovered_at=45630s, mutation_op=QwordAddMutator,TokenInsert,TokenInsert):
  0000: 64 00 00 00 ff 06 06 df 20 03 03 03 03 03 03 03   d....... .......
  0010: 0c 03 03 03 03 8b 8b 8b 8b 8b 8b 8b 8b 8b 8b 14   ................
  0020: 01 00 ba 14 01 00 81 7a 97 7a 68 2d 68 00 02 00   .......z.zh-h...
  0030: 9c 97 e0 95 19 72 00 e7 e7 65 c6 c6 00 00 00 73   .....r...e.....s
Seed 5 (id=a9858a6c8b36d7c3, size=42 bytes, fuzzer=naive, trial=1, discovered_at=52846s, mutation_op=ByteIncMutator,BytesCopyMutator,BytesSetMutator,TokenReplace):
  0000: fa 02 00 73 70 2d 00 4e 1d 0e 00 00 4b 0e 00 00   ...sp-.N....K...
  0010: 0f 0e 00 ff 98 cb 0d 4e 1d 0e 00 00 4b 0e 00 00   .......N....K...
  0020: 92 a2 92 b0 0f 0f 0f 0f 02 02                     ..........

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=37f8e71ac2ac9677, size=21 bytes, fuzzer=cmplog, trial=1, discovered_at=163s, mutation_op=BytesInsertCopyMutator):
  0000: 05 0d 01 74 05 0d 01 74 ba c0 22 06 38 0e 00 00   ...t...t..".8...
  0010: 00 00 ff 40 20                                    ...@ 
Seed 2 (id=0568144a6b4b248e, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=246s, mutation_op=TokenInsert,QwordAddMutator,BytesSetMutator,ByteInterestingMutator,TokenInsert,WordAddMutator,WordAddMutator):
  0000: 00 01 40 9b 14 01 20 6e 6e 00 1b 1b 1b 1b 1b 1b   ..@... nn.......
  0010: 1b 1b 70 67 6c 73 1b 1b 20 20 20 6b 34 0e 00 00   ..pgls..   k4...
  0020: 05 65 72 6f 25 49 92 04 20 00 1b 1b 1b ff ff fb   .ero%I.. .......
  0030: 01 00 04 dd 0f 0e 00 00 05                        .........
Seed 3 (id=0dbfc616ba80cfe4, size=76 bytes, fuzzer=cmplog, trial=1, discovered_at=972s, mutation_op=BytesDeleteMutator):
  0000: ff fc 00 00 5a 5b 5a 5a 5a 5a 5a 48 00 fe ff 00   ....Z[ZZZZZH....
  0010: 00 01 ff 0f d6 03 1b 20 4d 0e 00 00 34 1d 17 ff   ....... M...4...
  0020: 00 ff fc 00 00 5a 5b 5a 5a 5a 5a 5a 48 00 00 00   .....Z[ZZZZZH...
  0030: 34 0e 4d 0e 00 00 34 20 01 04 4d 0e 4d 0e 00 20   4.M...4 ..M.M.. 
Seed 4 (id=1789cc0d2b4c5f5c, size=78 bytes, fuzzer=cmplog, trial=1, discovered_at=972s, mutation_op=BytesExpandMutator,ByteDecMutator,ByteRandMutator):
  0000: 00 00 00 10 5a 5b 5a 5a 5a 63 5a 48 00 fe ff 00   ....Z[ZZZcZH....
  0010: 00 01 ff 0f 0e 03 1b 20 4d 0e 00 00 34 e2 17 ff   ....... M...4...
  0020: 00 5b 5b 5b 01 00 01 01 20 20 01 04 6b 0e 00 00   .[[[....  ..k...
  0030: 33 0e 4d 0e 00 00 34 20 01 04 4d 0e 00 00 3a 0e   3.M...4 ..M...:.
Seed 5 (id=0beabfa6abb311a7, size=126 bytes, fuzzer=cmplog, trial=1, discovered_at=2025s, mutation_op=BytesCopyMutator,BytesDeleteMutator,ByteDecMutator,ByteInterestingMutator,BytesRandInsertMutator,ByteNegMutator):
  0000: 4f 54 54 4f 00 02 20 20 20 20 00 1b 00 12 dc 03   OTTO..    ......
  0010: 00 7f 00 1b 02 00 ff 0e 02 01 00 1b 4d 41 54 48   ............MATH
  0020: 00 01 fe 40 0c 00 00 20 00 0c 20 0c 18 03 00 0c   ...@... .. .....
  0030: 00 00 00 0d 20 02 ff ff 00 00 02 00 1a ab 20 0e   .... ......... .


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  98(.)x2 64(d)x2 fa(.)x1             00(.)x7 05(.)x1 ff(.)x1 4f(O)x1     DIFFER
   0x0001  cb(.)x2 00(.)x2 02(.)x1             01(.)x6 0d(.)x1 fc(.)x1 00(.)x1 +1u  PARTIAL
   0x0002  00(.)x3 0d(.)x2                     00(.)x7 01(.)x1 40(@)x1 54(T)x1     PARTIAL
   0x0003  4e(N)x2 00(.)x2 73(s)x1             00(.)x6 74(t)x1 9b(.)x1 10(.)x1 +1u  PARTIAL
   0x0004  ff(.)x2 0d(.)x1 10(.)x1 70(p)x1     00(.)x6 5a(Z)x2 05(.)x1 14(.)x1     DIFFER
   0x0005  0e(.)x2 06(.)x2 2d(-)x1             01(.)x5 5b([)x2 02(.)x2 0d(.)x1     DIFFER
   0x0006  06(.)x2 00(.)x2 0e(.)x1             20( )x5 5a(Z)x2 07(.)x2 01(.)x1     DIFFER
   0x0007  df(.)x2 0e(.)x1 00(.)x1 4e(N)x1     20( )x6 5a(Z)x2 74(t)x1 6e(n)x1     DIFFER
   0x0008  20( )x2 1d(.)x2 01(.)x1             20( )x3 5a(Z)x2 21(!)x2 ba(.)x1 +2u  PARTIAL
   0x0009  0e(.)x3 03(.)x2                     20( )x5 c0(.)x1 00(.)x1 5a(Z)x1 +2u  DIFFER
   0x000a  03(.)x2 00(.)x2 0e(.)x1             5a(Z)x2 00(.)x2 20( )x2 1e(.)x2 +2u  PARTIAL
   0x000b  00(.)x3 03(.)x2                     20( )x4 1b(.)x2 48(H)x2 06(.)x1 +1u  PARTIAL
   0x000c  03(.)x2 4b(K)x2 0f(.)x1             00(.)x4 4d(M)x2 47(G)x2 38(8)x1 +1u  DIFFER
   0x000d  0e(.)x3 03(.)x2                     fe(.)x2 41(A)x2 53(S)x2 0e(.)x1 +3u  PARTIAL
   0x000e  00(.)x3 03(.)x2                     ff(.)x2 54(T)x2 55(U)x2 00(.)x1 +3u  PARTIAL
   0x000f  03(.)x2 00(.)x2 01(.)x1             00(.)x3 48(H)x2 42(B)x2 1b(.)x1 +2u  PARTIAL
   0x0010  0c(.)x2 0f(.)x2 1e(.)x1             00(.)x8 1b(.)x1 ff(.)x1             DIFFER
   0x0011  03(.)x2 0e(.)x2 fa(.)x1             01(.)x6 00(.)x1 1b(.)x1 7f(.)x1 +1u  DIFFER
   0x0012  03(.)x2 00(.)x2 02(.)x1             00(.)x5 ff(.)x3 70(p)x1 b9(.)x1     PARTIAL
   0x0013  03(.)x2 4e(N)x1 00(.)x1 ff(.)x1     0f(.)x2 80(.)x2 2e(.)x2 40(@)x1 +3u  DIFFER
   0x0014  03(.)x2 1b(.)x1 1e(.)x1 98(.)x1     00(.)x4 20( )x1 6c(l)x1 d6(.)x1 +3u  DIFFER
   0x0015  0e(.)x1 00(.)x1 fa(.)x1 8b(.)x1 +1u  00(.)x5 03(.)x2 73(s)x1 b9(.)x1     PARTIAL
   0x0016  00(.)x1 9c(.)x1 fa(.)x1 8b(.)x1 +1u  00(.)x4 1b(.)x3 ff(.)x1 01(.)x1     PARTIAL
   0x0018  4b(K)x1 e0(.)x1 7f(.)x1 8b(.)x1 +1u  00(.)x4 20( )x2 4d(M)x2 02(.)x1     DIFFER
   0x0019  0e(.)x2 95(.)x1 ff(.)x1 8b(.)x1     20( )x2 0e(.)x2 10(.)x2 02(.)x2 +1u  PARTIAL
   0x001a  00(.)x3 ff(.)x1 8b(.)x1             00(.)x3 fa(.)x2 20( )x1 3c(<)x1 +2u  PARTIAL
   0x001b  00(.)x2 72(r)x1 ff(.)x1 8b(.)x1     00(.)x2 46(F)x2 6b(k)x1 1b(.)x1 +3u  PARTIAL
   0x001d  0e(.)x2 e7(.)x1 92(.)x1 8b(.)x1     10(.)x2 04(.)x2 0e(.)x1 1d(.)x1 +3u  PARTIAL
   0x001e  00(.)x2 e7(.)x1 90(.)x1 8b(.)x1     00(.)x4 17(.)x2 54(T)x1 4f(O)x1 +1u  PARTIAL
   0x0020  1e(.)x1 c6(.)x1 cb(.)x1 01(.)x1 +1u  00(.)x5 0d(.)x2 05(.)x1 08(.)x1     DIFFER
   0x0022  92(.)x2 01(.)x1 00(.)x1 ba(.)x1     00(.)x4 72(r)x1 fc(.)x1 5b([)x1 +2u  PARTIAL
   0x0025  73(s)x1 5d(])x1 00(.)x1 0f(.)x1     00(.)x4 04(.)x2 49(I)x1 5a(Z)x1 +1u  PARTIAL
   0x0026  6d(m)x1 6f(o)x1 81(.)x1 0f(.)x1     00(.)x4 01(.)x3 92(.)x1 5b([)x1     DIFFER
   0x0027  63(c)x1 ff(.)x1 7a(z)x1 0f(.)x1     10(.)x3 01(.)x2 04(.)x1 5a(Z)x1 +2u  DIFFER
   0x0028  2b(+)x1 7f(.)x1 97(.)x1 02(.)x1     00(.)x5 20( )x2 5a(Z)x1 01(.)x1     DIFFER
   0x0029  2c(,)x1 ff(.)x1 7a(z)x1 02(.)x1     00(.)x2 10(.)x2 5a(Z)x1 20( )x1 +3u  PARTIAL
   0x002a  12(.)x1 ff(.)x1 68(h)x1             00(.)x4 1b(.)x1 5a(Z)x1 01(.)x1 +2u  DIFFER
   0x002b  01(.)x1 ff(.)x1 2d(-)x1             04(.)x2 10(.)x2 1b(.)x1 5a(Z)x1 +3u  PARTIAL
   0x002c  00(.)x1 ff(.)x1 68(h)x1             00(.)x4 1b(.)x1 48(H)x1 6b(k)x1 +2u  PARTIAL
   0x002d  00(.)x2 46(F)x1                     00(.)x2 03(.)x2 10(.)x2 ff(.)x1 +2u  PARTIAL
   ... (18 more divergent offsets)
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

--- naive ---
**Instrumentation**: SanitizerCoverage edge counters
(`__sanitizer_cov_trace_pc_guard*` callbacks compiled in via clang
`-fsanitize-coverage=...`).

**Feedback**: per-edge hit-count bucket; a new bucket triggers a
corpus-add (LibAFL `MaxMapFeedback` over the edge map).

**Mutators**: havoc + token stack — `ByteFlipMutator`, `ByteRandMutator`,
`ByteIncMutator`, `ByteDecMutator`, `ByteAddMutator`, `WordAddMutator`,
`DwordAddMutator`, `QwordAddMutator`, `BytesDeleteMutator`,
`BytesInsertMutator`, `BytesInsertCopyMutator`, `BytesExpandMutator`,
`BytesRandInsertMutator`, `BytesRandSetMutator`, `BytesCopyMutator`,
`BytesSwapMutator`, `WordInterestingMutator`, `DwordInterestingMutator`,
`ByteInterestingMutator`, `CrossoverInsertMutator`,
`CrossoverReplaceMutator`, `TokenInsert`, `TokenReplace`.

**Observed `mutation_op` in seed metadata**: any of the above. No I2S.

**Per-execution cost**: one edge-counter increment per executed BB edge.

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  prompts_b/harfbuzz_5967.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5967,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5967 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5967 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5967 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).