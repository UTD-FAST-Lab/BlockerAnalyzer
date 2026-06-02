==== BLOCKER ====
Target: harfbuzz
Branch ID: 5619
Location: /src/harfbuzz/src/hb-ot-shape-fallback.cc:46:15
Enclosing function: hb-ot-shape-fallback.cc:recategorize_combining_class(unsigned int, unsigned int)
Source line:       switch (u)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           1        9          0  loser (I2S vs naive)
value_profile                   10        0          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             2        8          0  loser (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=0.80h  loser=20.60h
  avg hitcount on branch: winner=100  loser=0
  prob_div=0.90  dur_div=19.80h  hit_div=99
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=0.50h  loser=17.60h
  avg hitcount on branch: winner=111  loser=0
  prob_div=0.80  dur_div=17.10h  hit_div=110
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5619/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shape-fallback.cc:recategorize_combining_class(unsigned int, unsigned int) (/src/harfbuzz/src/hb-ot-shape-fallback.cc:37-166) ---
[ ]    35  recategorize_combining_class (hb_codepoint_t u,
[ ]    36  			      unsigned int klass)
[B]    37  {
[B]    38    if (klass >= 200)
[B]    39      return klass;
[ ]    40  
[ ]    41    /* Thai / Lao need some per-character work. */
[B]    42    if ((u & ~0xFF) == 0x0E00u)
[B]    43    {
[B]    44      if (unlikely (klass == 0))
[B]    45      {
[B]    46        switch (u) <-- BLOCKER
[B]    47        {
[B]    48  	case 0x0E31u:
[B]    49  	case 0x0E34u:
[B]    50  	case 0x0E35u:
[B]    51  	case 0x0E36u:
[B]    52  	case 0x0E37u:
[B]    53  	case 0x0E47u:
[B]    54  	case 0x0E4Cu:
[B]    55  	case 0x0E4Du:
[B]    56  	case 0x0E4Eu:
[B]    57  	  klass = HB_UNICODE_COMBINING_CLASS_ABOVE_RIGHT;
[B]    58  	  break;
[ ]    59  
[L]    60  	case 0x0EB1u:
[L]    61  	case 0x0EB4u:
[L]    62  	case 0x0EB5u:
[L]    63  	case 0x0EB6u:
[L]    64  	case 0x0EB7u:
[L]    65  	case 0x0EBBu:
[B]    66  	case 0x0ECCu:
[B]    67  	case 0x0ECDu:
[B]    68  	  klass = HB_UNICODE_COMBINING_CLASS_ABOVE;
[B]    69  	  break;
[ ]    70  
[B]    71  	case 0x0EBCu:
[B]    72  	  klass = HB_UNICODE_COMBINING_CLASS_BELOW;
[B]    73  	  break;
[B]    74        }
[B]    75      } else {
[ ]    76        /* Thai virama is below-right */
[B]    77        if (u == 0x0E3Au)
[ ]    78  	klass = HB_UNICODE_COMBINING_CLASS_BELOW_RIGHT;
[B]    79      }
[B]    80    }
[ ]    81  
[B]    82    switch (klass)
[B]    83    {
[ ]    84  
[ ]    85      /* Hebrew */
[ ]    86  
[ ]    87      case HB_MODIFIED_COMBINING_CLASS_CCC10: /* sheva */
[ ]    88      case HB_MODIFIED_COMBINING_CLASS_CCC11: /* hataf segol */
[ ]    89      case HB_MODIFIED_COMBINING_CLASS_CCC12: /* hataf patah */
[ ]    90      case HB_MODIFIED_COMBINING_CLASS_CCC13: /* hataf qamats */
[ ]    91      case HB_MODIFIED_COMBINING_CLASS_CCC14: /* hiriq */
[ ]    92      case HB_MODIFIED_COMBINING_CLASS_CCC15: /* tsere */
[ ]    93      case HB_MODIFIED_COMBINING_CLASS_CCC16: /* segol */
[ ]    94      case HB_MODIFIED_COMBINING_CLASS_CCC17: /* patah */
[ ]    95      case HB_MODIFIED_COMBINING_CLASS_CCC18: /* qamats & qamats qatan */
[ ]    96      case HB_MODIFIED_COMBINING_CLASS_CCC20: /* qubuts */
[W]    97      case HB_MODIFIED_COMBINING_CLASS_CCC22: /* meteg */
[W]    98        return HB_UNICODE_COMBINING_CLASS_BELOW;
[ ]    99  
[ ]   100      case HB_MODIFIED_COMBINING_CLASS_CCC23: /* rafe */
[ ]   101        return HB_UNICODE_COMBINING_CLASS_ATTACHED_ABOVE;
[ ]   102  
[ ]   103      case HB_MODIFIED_COMBINING_CLASS_CCC24: /* shin dot */
[ ]   104        return HB_UNICODE_COMBINING_CLASS_ABOVE_RIGHT;
[ ]   105  
[ ]   106      case HB_MODIFIED_COMBINING_CLASS_CCC25: /* sin dot */
[W]   107      case HB_MODIFIED_COMBINING_CLASS_CCC19: /* holam & holam haser for vav */
[W]   108        return HB_UNICODE_COMBINING_CLASS_ABOVE_LEFT;
[ ]   109  
[W]   110      case HB_MODIFIED_COMBINING_CLASS_CCC26: /* point varika */
[W]   111        return HB_UNICODE_COMBINING_CLASS_ABOVE;
[ ]   112  
[ ]   113      case HB_MODIFIED_COMBINING_CLASS_CCC21: /* dagesh */
[ ]   114        break;
[ ]   115  
[ ]   116  
[ ]   117      /* Arabic and Syriac */
[ ]   118  
[ ]   119      case HB_MODIFIED_COMBINING_CLASS_CCC27: /* fathatan */
[ ]   120      case HB_MODIFIED_COMBINING_CLASS_CCC28: /* dammatan */
[ ]   121      case HB_MODIFIED_COMBINING_CLASS_CCC30: /* fatha */
[ ]   122      case HB_MODIFIED_COMBINING_CLASS_CCC31: /* damma */
[ ]   123      case HB_MODIFIED_COMBINING_CLASS_CCC33: /* shadda */
[ ]   124      case HB_MODIFIED_COMBINING_CLASS_CCC34: /* sukun */
[ ]   125      case HB_MODIFIED_COMBINING_CLASS_CCC35: /* superscript alef */
[ ]   126      case HB_MODIFIED_COMBINING_CLASS_CCC36: /* superscript alaph */
[ ]   127        return HB_UNICODE_COMBINING_CLASS_ABOVE;
[ ]   128  
[W]   129      case HB_MODIFIED_COMBINING_CLASS_CCC29: /* kasratan */
[W]   130      case HB_MODIFIED_COMBINING_CLASS_CCC32: /* kasra */
[W]   131        return HB_UNICODE_COMBINING_CLASS_BELOW;
[ ]   132  
[ ]   133  
[ ]   134      /* Thai */
[ ]   135  
[B]   136      case HB_MODIFIED_COMBINING_CLASS_CCC103: /* sara u / sara uu */
[B]   137        return HB_UNICODE_COMBINING_CLASS_BELOW_RIGHT;
[ ]   138  
[ ]   139      case HB_MODIFIED_COMBINING_CLASS_CCC107: /* mai */
[ ]   140        return HB_UNICODE_COMBINING_CLASS_ABOVE_RIGHT;
[ ]   141  
[ ]   142  
[ ]   143      /* Lao */
[ ]   144  
[ ]   145      case HB_MODIFIED_COMBINING_CLASS_CCC118: /* sign u / sign uu */
[ ]   146        return HB_UNICODE_COMBINING_CLASS_BELOW;
[ ]   147  
[B]   148      case HB_MODIFIED_COMBINING_CLASS_CCC122: /* mai */
[B]   149        return HB_UNICODE_COMBINING_CLASS_ABOVE;
[ ]   150  
[ ]   151  
[ ]   152      /* Tibetan */
[ ]   153  
[ ]   154      case HB_MODIFIED_COMBINING_CLASS_CCC129: /* sign aa */
[ ]   155        return HB_UNICODE_COMBINING_CLASS_BELOW;
[ ]   156  
[ ]   157      case HB_MODIFIED_COMBINING_CLASS_CCC130: /* sign i*/
[ ]   158        return HB_UNICODE_COMBINING_CLASS_ABOVE;
[ ]   159  
[ ]   160      case HB_MODIFIED_COMBINING_CLASS_CCC132: /* sign u */
[ ]   161        return HB_UNICODE_COMBINING_CLASS_BELOW;
[ ]   162  
[B]   163    }
[ ]   164  
[B]   165    return klass;
[B]   166  }

--- Caller (1 hop): _hb_ot_shape_fallback_mark_position_recategorize_marks(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shape-fallback.cc:172-185, calls hb-ot-shape-fallback.cc:recategorize_combining_class(unsigned int, unsigned int) at line 182) (full body — short) ---
[B]   172  {
[ ]   173  #ifdef HB_NO_OT_SHAPE_FALLBACK
[ ]   174    return;
[ ]   175  #endif
[ ]   176  
[B]   177    unsigned int count = buffer->len;
[B]   178    hb_glyph_info_t *info = buffer->info;
[B]   179    for (unsigned int i = 0; i < count; i++)
[B]   180      if (_hb_glyph_info_get_general_category (&info[i]) == HB_UNICODE_GENERAL_CATEGORY_NON_SPACING_MARK) {
[B]   181        unsigned int combining_class = _hb_glyph_info_get_modified_combining_class (&info[i]);
[B]   182        combining_class = recategorize_combining_class (info[i].codepoint, combining_class); <-- CALL
[B]   183        _hb_glyph_info_set_modified_combining_class (&info[i], combining_class);
[B]   184      }
[B]   185  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  _hb_ot_shape_fallback_mark_position_recategorize_marks(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:172-185, calls hb-ot-shape-fallback.cc:recategorize_combining_class(unsigned int, unsigned int) at line 182)
hop 3  hb-ot-shape.cc:hb_ot_substitute_default(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:882-900, calls _hb_ot_shape_fallback_mark_position_recategorize_marks(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) at line 895)
hop 4  hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:923-934, calls hb-ot-shape.cc:hb_ot_substitute_default(hb_ot_shape_context_t const*) at line 924)
hop 5  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195, calls hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*) at line 1184)
hop 6  _hb_ot_shape  (/src/harfbuzz/src/hb-ot-shape.cc:1204-1209, calls hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*) at line 1206)

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-shape-fallback.cc:recategorize_combining_class(unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:37-166) ---
  d=1   L  46  T=35 F=22  T=0 F=30  switch (u)  <-- BLOCKER
  d=1   L  49  T=0 F=57  T=4 F=26  case 0x0E34u:
  d=1   L  50  T=0 F=57  T=2 F=28  case 0x0E35u:
  d=1   L  51  T=0 F=57  T=1 F=29  case 0x0E36u:
  d=1   L  52  T=0 F=57  T=4 F=26  case 0x0E37u:
  d=1   L  60  T=0 F=57  T=1 F=29  case 0x0EB1u:
  d=1   L  61  T=0 F=57  T=2 F=28  case 0x0EB4u:
  d=1   L  63  T=0 F=57  T=1 F=29  case 0x0EB6u:
  d=1   L  67  T=4 F=53  T=0 F=30  case 0x0ECDu:
  d=1   L  97  T=5 F=79  T=0 F=46  case HB_MODIFIED_COMBINING_CLASS_CCC22: /* meteg */
  d=1   L 107  T=1 F=83  T=0 F=46  case HB_MODIFIED_COMBINING_CLASS_CCC19: /* holam & holam ...
  d=1   L 110  T=6 F=78  T=0 F=46  case HB_MODIFIED_COMBINING_CLASS_CCC26: /* point varika */
  d=1   L 129  T=1 F=83  T=0 F=46  case HB_MODIFIED_COMBINING_CLASS_CCC29: /* kasratan */

[off-chain: 3 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=053d0247691f7c01, size=113 bytes, fuzzer=value_profile, trial=1, discovered_at=499s, mutation_op=QwordAddMutator,ByteAddMutator,WordInterestingMutator):
  0000: ff ff 00 00 01 00 00 00 00 00 00 00 00 00 00 00   ................
  0010: 22 00 00 00 00 00 7f 4c 4c 00 0e 0e 0e 0e ff 4c   "......LL......L
  0020: 4c 4c 4c 4c 4c 4c ff ff 0e 0e 0e 0e 0e 0e 0e 0e   LLLLLL..........
  0030: 0e 0e 0e 0e 0e ff 0c 00 00 01 00 00 00 00 00 00   ................
Seed 2 (id=060872d3eb5bff14, size=55 bytes, fuzzer=naive, trial=1, discovered_at=527s, mutation_op=DwordInterestingMutator,CrossoverReplaceMutator,ByteNegMutator,BytesDeleteMutator):
  0000: ea 00 10 00 00 ea ea ea ea 00 00 00 00 0e 00 01   ................
  0010: 00 00 07 ff ff 00 00 00 ce 0e 00 00 00 1b 00 18   ................
  0020: 00 00 5c 20 00 00 00 a0 00 00 00 1a 00 fe 00 00   ..\ ............
  0030: 31 0e 00 00 00 00 00                              1......
Seed 3 (id=024ab24c2d0c686c, size=92 bytes, fuzzer=value_profile, trial=1, discovered_at=627s, mutation_op=TokenInsert,BytesDeleteMutator,BytesCopyMutator):
  0000: 00 00 62 00 00 62 6e 2d 00 4c 0d f4 00 83 83 83   ..b..bn-.L......
  0010: 83 83 83 83 83 83 00 00 cc 0e 95 95 95 95 95 95   ................
  0020: 95 95 95 95 95 95 95 95 95 4c 0e 00 00 ce 0e 00   .........L......
  0030: 00 ff 5e 0d 00 20 b3 0d ed 00 cc fc fb ff 7f 0e   ..^.. ..........
Seed 4 (id=0badbfab64577430, size=42 bytes, fuzzer=value_profile, trial=1, discovered_at=688s, mutation_op=TokenReplace,BytesExpandMutator,TokenInsert):
  0000: f2 08 00 00 ce 0e 00 00 4d 0e 00 00 2d 7b 6e 70   ........M...-{np
  0010: 00 16 01 00 2d 68 61 00 ce 0e 00 00 4d 0e 00 00   ....-ha.....M...
  0020: 2d 7b 6e 70 2d 68 61 6e 74 00                     -{np-hant.
Seed 5 (id=1568e4f29e03ed34, size=96 bytes, fuzzer=naive, trial=1, discovered_at=812s, mutation_op=DwordInterestingMutator,WordAddMutator,BytesDeleteMutator):
  0000: fe fe 00 cc 05 05 05 05 05 05 05 00 b5 c4 00 96   ................
  0010: 68 e7 19 00 00 00 19 ad ad ad ad 00 00 17 e7 e7   h...............
  0020: 19 00 00 00 00 00 40 00 0e 00 00 cb 0b 69 12 00   ......@......i..
  0030: 00 60 00 00 00 0c 20 00 00 00 64 68 cd 0e 00 00   .`.... ...dh....

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0e56b0a0b0bf691f, size=60 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=496s, mutation_op=WordInterestingMutator,BitFlipMutator,ByteFlipMutator):
  0000: 01 03 00 11 20 20 20 20 4e 0e 02 00 1a fa fa fa   ....    N.......
  0010: fa fa fa fa fa 11 1e fa 02 00 01 64 00 20 5f 0f   ...........d. _.
  0020: 5f 0f 6e 20 00 18 0d 00 10 0e 1e fa 02 00 01 20   _.n ........... 
  0030: 20 20 5f 0f b1 0e 00 00 1a 11 6e 20                 _.......n 
Seed 2 (id=0eb8a04033f2ab8b, size=72 bytes, fuzzer=cmplog, trial=1, discovered_at=583s, mutation_op=ByteNegMutator,ByteAddMutator,BytesRandInsertMutator,QwordAddMutator,ByteFlipMutator,TokenReplace,ByteRandMutator):
  0000: 00 00 02 ff 0f 0e ff ff ff 03 00 00 31 0e 00 00   ............1...
  0010: f4 1d 00 00 00 80 ff 16 73 f3 21 20 01 00 00 00   ........s.! ....
  0020: 00 03 00 00 00 70 20 00 64 20 20 20 20 ff ff 6a   .....p .d    ..j
  0030: 79 2d 68 61 6e 74 2d 68 6b 00 ff ec 00 00 03 00   y-hant-hk.......
Seed 3 (id=120732f140ed6558, size=121 bytes, fuzzer=cmplog, trial=1, discovered_at=659s, mutation_op=BytesDeleteMutator,ByteInterestingMutator,DwordAddMutator,ByteInterestingMutator,BytesDeleteMutator,BytesCopyMutator):
  0000: 00 ff 00 fe ff 10 00 01 20 20 20 01 00 00 80 0d   ........   .....
  0010: 04 00 e0 20 1d 6b 65 df e0 20 04 00 05 0d 04 00   ... .ke.. ......
  0020: e0 20 1d 6b 65 72 6e 01 00 03 00 34 35 0e 00 00   . .kern....45...
  0030: 1a 20 20 20 00 00 00 03 02 00 01 01 01 20 20 20   .   .........   
Seed 4 (id=118636ec222fddec, size=94 bytes, fuzzer=cmplog, trial=1, discovered_at=660s, mutation_op=CrossoverInsertMutator,ByteDecMutator,BytesRandSetMutator,CrossoverReplaceMutator,BytesSetMutator,BytesInsertCopyMutator,CrossoverReplaceMutator):
  0000: 00 ff 00 fe ff 10 00 01 20 20 04 00 00 00 80 df   ........  ......
  0010: e0 fe ff ff 7f 0d 00 0e e0 20 1d 6b 65 72 6e 04   ......... .kern.
  0020: 7f 00 00 00 00 34 b6 0e 02 00 01 03 00 00 00 03   .....4..........
  0030: 00 01 b6 0e 00 00 4f 03 00 00 00 03 00 01 01 01   ......O.........
Seed 5 (id=036121913c51bdeb, size=66 bytes, fuzzer=cmplog, trial=1, discovered_at=796s, mutation_op=ByteFlipMutator,BytesExpandMutator,ByteFlipMutator,BytesDeleteMutator,WordAddMutator,CrossoverInsertMutator,CrossoverReplaceMutator):
  0000: 0e 02 00 34 0e 02 00 00 20 00 0e 00 5a 5a 5a 5a   ...4.... ...ZZZZ
  0010: 5a 5a 5a 5a 5a fe ff 02 00 01 ff 0f 0e 03 1a 20   ZZZZZ.......... 
  0020: 20 02 00 70 df 00 00 71 6e 20 6b 00 65 04 4d 0e    ..p...qn k.e.M.
  0030: 00 00 b4 0e 00 00 00 00 00 00 b4 0e 00 00 00 00   ................


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x003e  00(.)x10 7f(.)x1 16(.)x1 ff(.)x1    03(.)x4 01(.)x2 00(.)x2 0e(.)x2 +8u  PARTIAL
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
  prompts_b/harfbuzz_5619.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5619,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S), value_profile>value_profile_cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5619 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5619 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5619 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).