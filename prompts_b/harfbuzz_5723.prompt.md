==== BLOCKER ====
Target: harfbuzz
Branch ID: 5723
Location: /src/harfbuzz/src/hb-ot-shape.cc:491:11
Enclosing function: hb-ot-shape.cc:hb_set_unicode_props(hb_buffer_t*)
Source line:       if (i + 1 < count &&
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           1        9          0  loser (I2S vs naive)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             4        6          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         2        8          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=7.80h  loser=19.50h
  avg hitcount on branch: winner=11  loser=0
  prob_div=0.90  dur_div=11.70h  hit_div=11
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5723/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shape.cc:hb_set_unicode_props(hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shape.cc:457-517) ---
[ ]   455  static void
[ ]   456  hb_set_unicode_props (hb_buffer_t *buffer)
[B]   457  {
[ ]   458    /* Implement enough of Unicode Graphemes here that shaping
[ ]   459     * in reverse-direction wouldn't break graphemes.  Namely,
[ ]   460     * we mark all marks and ZWJ and ZWJ,Extended_Pictographic
[ ]   461     * sequences as continuations.  The foreach_grapheme()
[ ]   462     * macro uses this bit.
[ ]   463     *
[ ]   464     * https://www.unicode.org/reports/tr29/#Regex_Definitions
[ ]   465     */
[B]   466    unsigned int count = buffer->len;
[B]   467    hb_glyph_info_t *info = buffer->info;
[B]   468    for (unsigned int i = 0; i < count; i++)
[B]   469    {
[B]   470      _hb_glyph_info_set_unicode_props (&info[i], buffer);
[ ]   471  
[ ]   472      /* Marks are already set as continuation by the above line.
[ ]   473       * Handle Emoji_Modifier and ZWJ-continuation. */
[B]   474      if (unlikely (_hb_glyph_info_get_general_category (&info[i]) == HB_UNICODE_GENERAL_CATEGORY_MODIFIER_SYMBOL &&
[B]   475  		  hb_in_range<hb_codepoint_t> (info[i].codepoint, 0x1F3FBu, 0x1F3FFu)))
[ ]   476      {
[ ]   477        _hb_glyph_info_set_continuation (&info[i]);
[ ]   478      }
[ ]   479      /* Regional_Indicators are hairy as hell...
[ ]   480       * https://github.com/harfbuzz/harfbuzz/issues/2265 */
[B]   481      else if (unlikely (i && _hb_codepoint_is_regional_indicator (info[i].codepoint)))
[ ]   482      {
[ ]   483        if (_hb_codepoint_is_regional_indicator (info[i - 1].codepoint) &&
[ ]   484  	  !_hb_glyph_info_is_continuation (&info[i - 1]))
[ ]   485  	_hb_glyph_info_set_continuation (&info[i]);
[ ]   486      }
[B]   487  #ifndef HB_NO_EMOJI_SEQUENCES
[B]   488      else if (unlikely (_hb_glyph_info_is_zwj (&info[i])))
[B]   489      {
[B]   490        _hb_glyph_info_set_continuation (&info[i]);
[B]   491        if (i + 1 < count && <-- BLOCKER
[B]   492  	  _hb_unicode_is_emoji_Extended_Pictographic (info[i + 1].codepoint))
[L]   493        {
[L]   494  	i++;
[L]   495  	_hb_glyph_info_set_unicode_props (&info[i], buffer);
[L]   496  	_hb_glyph_info_set_continuation (&info[i]);
[L]   497        }
[B]   498      }
[B]   499  #endif
[ ]   500      /* Or part of the Other_Grapheme_Extend that is not marks.
[ ]   501       * As of Unicode 15 that is just:
[ ]   502       *
[ ]   503       * 200C          ; Other_Grapheme_Extend # Cf       ZERO WIDTH NON-JOINER
[ ]   504       * FF9E..FF9F    ; Other_Grapheme_Extend # Lm   [2] HALFWIDTH KATAKANA VOICED SOUND MARK..HALFWIDTH KATAKANA SEMI-VOICED SOUND MARK
[ ]   505       * E0020..E007F  ; Other_Grapheme_Extend # Cf  [96] TAG SPACE..CANCEL TAG
[ ]   506       *
[ ]   507       * ZWNJ is special, we don't want to merge it as there's no need, and keeping
[ ]   508       * it separate results in more granular clusters.
[ ]   509       * Tags are used for Emoji sub-region flag sequences:
[ ]   510       * https://github.com/harfbuzz/harfbuzz/issues/1556
[ ]   511       * Katakana ones were requested:
[ ]   512       * https://github.com/harfbuzz/harfbuzz/issues/3844
[ ]   513       */
[B]   514      else if (unlikely (hb_in_ranges<hb_codepoint_t> (info[i].codepoint, 0xFF9Eu, 0xFF9Fu, 0xE0020u, 0xE007Fu)))
[ ]   515        _hb_glyph_info_set_continuation (&info[i]);
[B]   516    }
[B]   517  }

--- Caller (1 hop): hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*) (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195, calls hb-ot-shape.cc:hb_set_unicode_props(hb_buffer_t*) at line 1170) (full body — short) ---
[B]  1163  {
[ ]  1164    /* Save the original direction, we use it later. */
[B]  1165    c->target_direction = c->buffer->props.direction;
[ ]  1166  
[B]  1167    _hb_buffer_allocate_unicode_vars (c->buffer);
[ ]  1168  
[B]  1169    hb_ot_shape_initialize_masks (c);
[B]  1170    hb_set_unicode_props (c->buffer); <-- CALL
[B]  1171    hb_insert_dotted_circle (c->buffer, c->font);
[ ]  1172  
[B]  1173    hb_form_clusters (c->buffer);
[ ]  1174  
[B]  1175    hb_ensure_native_direction (c->buffer);
[ ]  1176  
[B]  1177    if (c->plan->shaper->preprocess_text &&
[B]  1178        c->buffer->message(c->font, "start preprocess-text"))
[B]  1179    {
[B]  1180      c->plan->shaper->preprocess_text (c->plan, c->buffer, c->font);
[B]  1181      (void) c->buffer->message(c->font, "end preprocess-text");
[B]  1182    }
[ ]  1183  
[B]  1184    hb_ot_substitute_pre (c);
[B]  1185    hb_ot_position (c);
[B]  1186    hb_ot_substitute_post (c);
[ ]  1187  
[B]  1188    hb_propagate_flags (c->buffer);
[ ]  1189  
[B]  1190    _hb_buffer_deallocate_unicode_vars (c->buffer);
[ ]  1191  
[B]  1192    c->buffer->props.direction = c->target_direction;
[ ]  1193  
[B]  1194    c->buffer->leave ();
[B]  1195  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195, calls hb-ot-shape.cc:hb_set_unicode_props(hb_buffer_t*) at line 1170)
hop 3  _hb_ot_shape  (/src/harfbuzz/src/hb-ot-shape.cc:1204-1209, calls hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*) at line 1206)

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195) ---
  d=2   L1178  T=8 F=0  T=4 F=0  c->buffer->message(c->font, "start preprocess-text"))
--- d=1  hb-ot-shape.cc:hb_set_unicode_props(hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:457-517) ---
  d=1   L 491  T=35 F=10  T=11 F=0  if (i + 1 < count &&  <-- BLOCKER
  d=1   L 492  T=0 F=35  T=3 F=8  _hb_unicode_is_emoji_Extended_Pictographic (info[i + 1].c...

[off-chain: 13 additional divergent branches across 7 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=003db5f36a454aa7, size=62 bytes, fuzzer=naive, trial=1, discovered_at=236s, mutation_op=DwordAddMutator,BytesRandSetMutator):
  0000: 01 10 00 00 00 00 00 ff 00 ef 01 0e 00 0c 00 00   ................
  0010: 00 2b 19 00 00 00 0c 19 00 00 00 20 00 00 f0 ff   .+......... ....
  0020: 00 00 00 00 00 00 08 00 00 0c 00 f5 ff 32 32 32   .............222
  0030: 32 32 32 32 32 00 00 00 00 0c 00 00 0d 20         22222........ 
Seed 2 (id=d0519a15402d6c35, size=62 bytes, fuzzer=naive, trial=1, discovered_at=238s, mutation_op=TokenReplace,QwordAddMutator,CrossoverInsertMutator,ByteIncMutator):
  0000: e9 17 00 00 00 80 00 00 f7 00 e9 66 74 73 70 00   ...........ftsp.
  0010: 00 64 00 00 00 95 17 00 00 ff 80 08 00 00 95 95   .d..............
  0020: 95 95 00 00 20 00 20 00 80 00 00 00 20 00 96 95   .... . ..... ...
  0030: 95 95 95 95 95 95 95 96 95 95 00 00 0d 20         ............. 
Seed 3 (id=1a191f11c5d15c02, size=106 bytes, fuzzer=naive, trial=1, discovered_at=10287s, mutation_op=ByteIncMutator):
  0000: ff 6e 74 2d 68 6b 00 75 6e 12 ff 00 75 74 00 85   .nt-hk.un...ut..
  0010: 85 85 85 85 85 85 85 85 85 85 85 74 7f 75 8a 00   ...........t.u..
  0020: ff ff 85 85 85 85 74 7f 75 8a b2 1f 01 00 04 00   ......t.u.......
  0030: 00 00 03 00 00 00 01 10 01 00 00 ff ff ff 7f 00   ................
Seed 4 (id=d926b58e7b1a08ea, size=114 bytes, fuzzer=naive, trial=1, discovered_at=36276s, mutation_op=ByteNegMutator,ByteNegMutator,BytesCopyMutator,BytesInsertMutator,ByteAddMutator,QwordAddMutator):
  0000: ff 6e 74 2d 68 6b 00 75 6e 12 ff 00 75 74 00 85   .nt-hk.un...ut..
  0010: 85 85 85 85 85 85 85 85 85 85 85 74 7f 75 8a 00   ...........t.u..
  0020: ff ff 85 85 85 85 74 7f 75 76 b2 1f 01 00 04 00   ......t.uv......
  0030: 00 00 03 00 00 00 01 10 01 00 00 04 00 00 80 09   ................
Seed 5 (id=3c7a73ea6f0aa9ae, size=94 bytes, fuzzer=naive, trial=1, discovered_at=37264s, mutation_op=BytesRandInsertMutator,BytesCopyMutator):
  0000: 00 00 16 ff ff e9 00 00 00 00 00 f0 ff ff 10 00   ................
  0010: 03 1c 07 64 ff 00 00 01 00 0c 20 00 0d 00 17 00   ...d...... .....
  0020: 00 af be 00 00 00 00 f0 ff ff 10 a3 a3 a3 a3 18   ................
  0030: 00 00 0d 20 00 00 0b 18 00 00 0d 20 00 00 0d 20   ... ....... ... 

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=a4c7f66375cfc805, size=64 bytes, fuzzer=cmplog, trial=1, discovered_at=118s, mutation_op=ByteFlipMutator,CrossoverInsertMutator,ByteIncMutator,BytesRandSetMutator):
  0000: e2 17 00 00 01 e2 17 00 00 01 03 e8 e2 17 00 00   ................
  0010: 01 2c 20 20 00 01 0d 00 00 00 7f ff 20 00 1a 20   .,  ........ .. 
  0020: 20 ad 74 66 63 69 6f 6f 6f 6f 6f 20 0d 20 00 00    .tfciooooo . ..
  0030: 00 09 20 ff 20 20 20 85 5a 04 00 1a 20 e0 ba 20   .. .   .Z... .. 
Seed 2 (id=c08a0a25532c98d6, size=27 bytes, fuzzer=cmplog, trial=1, discovered_at=177s, mutation_op=DwordInterestingMutator,ByteFlipMutator,ByteIncMutator,CrossoverReplaceMutator):
  0000: 0c 20 00 00 0c 20 00 00 0d 20 00 00 20 20 20 4d   . ... ... ..   M
  0010: 4d 4e 4d 4d 6a 64 0d 00 00 7b 20                  MNMMjd...{ 
Seed 3 (id=9a80f6355a1b9baa, size=83 bytes, fuzzer=cmplog, trial=1, discovered_at=279s, mutation_op=CrossoverInsertMutator,BytesExpandMutator,TokenInsert,ByteFlipMutator,CrossoverInsertMutator,ByteIncMutator):
  0000: ba b9 b9 b9 b9 b9 b4 b4 b4 b4 b4 b9 b9 b9 ae 1d   ................
  0010: 0d 00 00 0d 20 00 00 ae 00 00 00 00 00 00 00 05   .... ...........
  0020: 00 00 00 03 00 00 00 03 00 00 b9 01 00 00 00 03   ................
  0030: 00 00 00 03 76 00 00 00 03 00 00 00 03 00 00 00   ....v...........
Seed 4 (id=2b8dd4f86fbae553, size=35 bytes, fuzzer=cmplog, trial=1, discovered_at=283s, mutation_op=BytesExpandMutator,CrossoverReplaceMutator):
  0000: 0c 20 00 00 0c 20 00 01 20 20 00 00 0c 20 00 00   . ... ..  ... ..
  0010: 0d 20 00 00 20 20 20 4d 4d 4e 4d 4d 6a 64 0d 00   . ..   MMNMMjd..
  0020: 00 7b 20                                          .{ 
Seed 5 (id=8d314f148dddb832, size=89 bytes, fuzzer=cmplog, trial=1, discovered_at=401s, mutation_op=WordInterestingMutator,BytesDeleteMutator,BytesExpandMutator):
  0000: ba b9 b9 b9 b9 b9 b4 b4 b4 b4 b4 b9 b9 b9 b9 b9   ................
  0010: b4 b4 b4 b4 b4 b9 b9 b9 ae 1d 0d 00 00 0d 20 00   .............. .
  0020: 00 ae 00 00 00 00 00 00 02 05 00 00 00 03 00 00   ................
  0030: 00 03 00 00 b9 01 00 00 00 03 00 00 00 03 76 00   ..............v.


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0002  0d(.)x3 00(.)x2 74(t)x2 16(.)x2 +1u  00(.)x6 b9(.)x2 10(.)x1 01(.)x1     PARTIAL
   0x0003  0d(.)x3 00(.)x2 2d(-)x2 ff(.)x2 +1u  00(.)x7 b9(.)x2 80(.)x1             PARTIAL
   0x0006  00(.)x7 0c(.)x2 0d(.)x1             00(.)x4 17(.)x2 b4(.)x2 34(4)x1 +1u  PARTIAL
   0x0007  00(.)x4 75(u)x2 0d(.)x2 ff(.)x1 +1u  00(.)x5 b4(.)x2 01(.)x2 20( )x1     PARTIAL
   0x000f  00(.)x6 85(.)x2 08(.)x1 0b(.)x1     00(.)x3 4d(M)x1 1d(.)x1 b9(.)x1 +3u  PARTIAL
   0x0012  00(.)x3 85(.)x2 07(.)x2 19(.)x1 +2u  00(.)x6 20( )x1 4d(M)x1 b4(.)x1     PARTIAL
   0x0018  00(.)x6 85(.)x2 68(h)x1 0d(.)x1     00(.)x5 4d(M)x1 ae(.)x1 6b(k)x1 +1u  PARTIAL
   0x001d  00(.)x5 75(u)x2 6a(j)x2 18(.)x1     00(.)x4 64(d)x1 0d(.)x1 20( )x1 +1u  PARTIAL
   0x001e  8a(.)x2 17(.)x2 00(.)x2 6a(j)x2 +2u  00(.)x5 1a(.)x1 0d(.)x1 20( )x1     PARTIAL
   0x0023  00(.)x6 85(.)x2 0b(.)x1 69(i)x1     00(.)x3 66(f)x1 03(.)x1 72(r)x1 +1u  PARTIAL
   0x0026  00(.)x5 74(t)x2 08(.)x1 20( )x1 +1u  00(.)x5 6f(o)x1                     PARTIAL
   0x0027  00(.)x4 7f(.)x2 f0(.)x2 0d(.)x1 +1u  00(.)x3 6f(o)x1 03(.)x1 10(.)x1     PARTIAL
   0x002a  00(.)x5 b2(.)x2 10(.)x2 1d(.)x1     00(.)x3 6f(o)x1 b9(.)x1 ff(.)x1     PARTIAL
   0x002c  0b(.)x3 01(.)x2 a3(.)x2 ff(.)x1 +2u  00(.)x4 0d(.)x1 ff(.)x1             PARTIAL
   0x002e  00(.)x4 04(.)x2 a3(.)x2 32(2)x1 +1u  00(.)x6                             PARTIAL
   0x002f  00(.)x5 18(.)x2 32(2)x1 95(.)x1 +1u  00(.)x4 03(.)x1 ff(.)x1             PARTIAL
   0x0030  00(.)x4 0d(.)x3 32(2)x1 95(.)x1 +1u  00(.)x5 36(6)x1                     PARTIAL
   0x0031  00(.)x5 20( )x3 32(2)x1 95(.)x1     00(.)x2 09(.)x1 03(.)x1 01(.)x1 +1u  PARTIAL
   0x0032  00(.)x4 03(.)x2 0d(.)x2 32(2)x1 +1u  00(.)x4 20( )x1 09(.)x1             PARTIAL
   0x0034  00(.)x4 32(2)x1 95(.)x1 18(.)x1 +3u  00(.)x3 20( )x1 76(v)x1 b9(.)x1     PARTIAL
   0x0035  00(.)x6 18(.)x2 95(.)x1 20( )x1     20( )x1 00(.)x1 01(.)x1 fe(.)x1 +2u  PARTIAL
   0x0036  00(.)x4 01(.)x2 0b(.)x2 95(.)x1 +1u  00(.)x3 20( )x2                     PARTIAL
   0x0037  00(.)x4 10(.)x2 18(.)x2 96(.)x1 +1u  00(.)x3 85(.)x1 06(.)x1             PARTIAL
   0x0038  00(.)x3 01(.)x2 0d(.)x2 95(.)x1 +2u  00(.)x2 5a(Z)x1 03(.)x1             PARTIAL
   0x0039  00(.)x5 20( )x2 0c(.)x1 95(.)x1 +1u  04(.)x2 00(.)x1 03(.)x1             PARTIAL
   0x003a  00(.)x8 0d(.)x2                     00(.)x4                             PARTIAL
   0x003b  00(.)x5 20( )x2 ff(.)x1 04(.)x1 +1u  00(.)x2 1a(.)x1 10(.)x1             PARTIAL
   0x003c  0d(.)x5 00(.)x3 ff(.)x1 0b(.)x1     00(.)x2 20( )x1 03(.)x1             PARTIAL
   0x003d  20( )x4 00(.)x4 ff(.)x1 18(.)x1     e0(.)x1 00(.)x1 03(.)x1 01(.)x1     PARTIAL
   0x003e  00(.)x4 0d(.)x2 7f(.)x1 80(.)x1     00(.)x2 ba(.)x1 76(v)x1             PARTIAL
   0x003f  00(.)x5 20( )x2 09(.)x1             00(.)x2 20( )x1 10(.)x1             PARTIAL
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
  prompts_b/harfbuzz_5723.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5723,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5723 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5723 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5723 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).