==== BLOCKER ====
Target: harfbuzz
Branch ID: 5660
Location: /src/harfbuzz/src/hb-ot-shape-fallback.cc:145:5
Enclosing function: hb-ot-shape-fallback.cc:recategorize_combining_class(unsigned int, unsigned int)
Source line:     case HB_MODIFIED_COMBINING_CLASS_CCC118: /* sign u / sign uu */
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  REFERENCE
cmplog                           8        2          0  winner (value_profile vs value_profile_cmplog)
value_profile                   10        0          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             2        8          0  loser (I2S vs value_profile); loser (value_profile vs cmplog)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         4        6          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=0.50h  loser=19.90h
  avg hitcount on branch: winner=267  loser=0
  prob_div=0.80  dur_div=19.40h  hit_div=266
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002
--- Pair 2: cmplog > value_profile_cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=7.40h  loser=19.90h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.60  dur_div=12.50h  hit_div=2
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5660/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shape-fallback.cc:recategorize_combining_class(unsigned int, unsigned int) (/src/harfbuzz/src/hb-ot-shape-fallback.cc:37-166) ---
[ ]    35  recategorize_combining_class (hb_codepoint_t u,
[ ]    36  			      unsigned int klass)
[B]    37  {
[B]    38    if (klass >= 200)
[B]    39      return klass;
[ ]    40  
[ ]    41    /* Thai / Lao need some per-character work. */
[B]    42    if ((u & ~0xFF) == 0x0E00u)
[W]    43    {
[W]    44      if (unlikely (klass == 0))
[W]    45      {
[W]    46        switch (u)
[W]    47        {
[ ]    48  	case 0x0E31u:
[ ]    49  	case 0x0E34u:
[ ]    50  	case 0x0E35u:
[W]    51  	case 0x0E36u:
[W]    52  	case 0x0E37u:
[W]    53  	case 0x0E47u:
[W]    54  	case 0x0E4Cu:
[W]    55  	case 0x0E4Du:
[W]    56  	case 0x0E4Eu:
[W]    57  	  klass = HB_UNICODE_COMBINING_CLASS_ABOVE_RIGHT;
[W]    58  	  break;
[ ]    59  
[ ]    60  	case 0x0EB1u:
[ ]    61  	case 0x0EB4u:
[W]    62  	case 0x0EB5u:
[W]    63  	case 0x0EB6u:
[W]    64  	case 0x0EB7u:
[W]    65  	case 0x0EBBu:
[W]    66  	case 0x0ECCu:
[W]    67  	case 0x0ECDu:
[W]    68  	  klass = HB_UNICODE_COMBINING_CLASS_ABOVE;
[W]    69  	  break;
[ ]    70  
[ ]    71  	case 0x0EBCu:
[ ]    72  	  klass = HB_UNICODE_COMBINING_CLASS_BELOW;
[ ]    73  	  break;
[W]    74        }
[W]    75      } else {
[ ]    76        /* Thai virama is below-right */
[W]    77        if (u == 0x0E3Au)
[ ]    78  	klass = HB_UNICODE_COMBINING_CLASS_BELOW_RIGHT;
[W]    79      }
[W]    80    }
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
[L]    94      case HB_MODIFIED_COMBINING_CLASS_CCC17: /* patah */
[B]    95      case HB_MODIFIED_COMBINING_CLASS_CCC18: /* qamats & qamats qatan */
[B]    96      case HB_MODIFIED_COMBINING_CLASS_CCC20: /* qubuts */
[B]    97      case HB_MODIFIED_COMBINING_CLASS_CCC22: /* meteg */
[B]    98        return HB_UNICODE_COMBINING_CLASS_BELOW;
[ ]    99  
[L]   100      case HB_MODIFIED_COMBINING_CLASS_CCC23: /* rafe */
[L]   101        return HB_UNICODE_COMBINING_CLASS_ATTACHED_ABOVE;
[ ]   102  
[L]   103      case HB_MODIFIED_COMBINING_CLASS_CCC24: /* shin dot */
[L]   104        return HB_UNICODE_COMBINING_CLASS_ABOVE_RIGHT;
[ ]   105  
[ ]   106      case HB_MODIFIED_COMBINING_CLASS_CCC25: /* sin dot */
[W]   107      case HB_MODIFIED_COMBINING_CLASS_CCC19: /* holam & holam haser for vav */
[W]   108        return HB_UNICODE_COMBINING_CLASS_ABOVE_LEFT;
[ ]   109  
[B]   110      case HB_MODIFIED_COMBINING_CLASS_CCC26: /* point varika */
[B]   111        return HB_UNICODE_COMBINING_CLASS_ABOVE;
[ ]   112  
[L]   113      case HB_MODIFIED_COMBINING_CLASS_CCC21: /* dagesh */
[L]   114        break;
[ ]   115  
[ ]   116  
[ ]   117      /* Arabic and Syriac */
[ ]   118  
[B]   119      case HB_MODIFIED_COMBINING_CLASS_CCC27: /* fathatan */
[B]   120      case HB_MODIFIED_COMBINING_CLASS_CCC28: /* dammatan */
[B]   121      case HB_MODIFIED_COMBINING_CLASS_CCC30: /* fatha */
[B]   122      case HB_MODIFIED_COMBINING_CLASS_CCC31: /* damma */
[B]   123      case HB_MODIFIED_COMBINING_CLASS_CCC33: /* shadda */
[B]   124      case HB_MODIFIED_COMBINING_CLASS_CCC34: /* sukun */
[B]   125      case HB_MODIFIED_COMBINING_CLASS_CCC35: /* superscript alef */
[B]   126      case HB_MODIFIED_COMBINING_CLASS_CCC36: /* superscript alaph */
[B]   127        return HB_UNICODE_COMBINING_CLASS_ABOVE;
[ ]   128  
[ ]   129      case HB_MODIFIED_COMBINING_CLASS_CCC29: /* kasratan */
[ ]   130      case HB_MODIFIED_COMBINING_CLASS_CCC32: /* kasra */
[ ]   131        return HB_UNICODE_COMBINING_CLASS_BELOW;
[ ]   132  
[ ]   133  
[ ]   134      /* Thai */
[ ]   135  
[W]   136      case HB_MODIFIED_COMBINING_CLASS_CCC103: /* sara u / sara uu */
[W]   137        return HB_UNICODE_COMBINING_CLASS_BELOW_RIGHT;
[ ]   138  
[W]   139      case HB_MODIFIED_COMBINING_CLASS_CCC107: /* mai */
[W]   140        return HB_UNICODE_COMBINING_CLASS_ABOVE_RIGHT;
[ ]   141  
[ ]   142  
[ ]   143      /* Lao */
[ ]   144  
[W]   145      case HB_MODIFIED_COMBINING_CLASS_CCC118: /* sign u / sign uu */ <-- BLOCKER
[W]   146        return HB_UNICODE_COMBINING_CLASS_BELOW;
[ ]   147  
[ ]   148      case HB_MODIFIED_COMBINING_CLASS_CCC122: /* mai */
[ ]   149        return HB_UNICODE_COMBINING_CLASS_ABOVE;
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

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0         2  hb-ot-shape-fallback.cc:position_mark(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, hb_glyph_extents_t&, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:215-313)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  _hb_ot_shape_fallback_mark_position_recategorize_marks(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:172-185) ---
  d=2   L 179  T=1080 F=420  T=540 F=210  for (unsigned int i = 0; i < count; i++)
  d=2   L 180  T=95 F=985  T=40 F=500  if (_hb_glyph_info_get_general_category (&info[i]) == HB_...
--- d=1  hb-ot-shape-fallback.cc:recategorize_combining_class(unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:37-166) ---
  d=1   L  38  T=12 F=83  T=16 F=24  if (klass >= 200)
  d=1   L  42  T=54 F=29  T=0 F=24  if ((u & ~0xFF) == 0x0E00u)
  d=1   L  46  T=0 F=13  T=0 F=0  switch (u)
  d=1   L  48  T=0 F=13  T=0 F=0  case 0x0E31u:
  d=1   L  49  T=0 F=13  T=0 F=0  case 0x0E34u:
  d=1   L  50  T=0 F=13  T=0 F=0  case 0x0E35u:
  d=1   L  51  T=1 F=12  T=0 F=0  case 0x0E36u:
  d=1   L  52  T=0 F=13  T=0 F=0  case 0x0E37u:
  d=1   L  53  T=5 F=8  T=0 F=0  case 0x0E47u:
  d=1   L  54  T=1 F=12  T=0 F=0  case 0x0E4Cu:
  d=1   L  55  T=0 F=13  T=0 F=0  case 0x0E4Du:
  d=1   L  56  T=0 F=13  T=0 F=0  case 0x0E4Eu:
  d=1   L  60  T=0 F=13  T=0 F=0  case 0x0EB1u:
  d=1   L  61  T=0 F=13  T=0 F=0  case 0x0EB4u:
  d=1   L  62  T=4 F=9  T=0 F=0  case 0x0EB5u:
  d=1   L  63  T=1 F=12  T=0 F=0  case 0x0EB6u:
  d=1   L  64  T=0 F=13  T=0 F=0  case 0x0EB7u:
  d=1   L  65  T=0 F=13  T=0 F=0  case 0x0EBBu:
  d=1   L  66  T=1 F=12  T=0 F=0  case 0x0ECCu:
  d=1   L  67  T=0 F=13  T=0 F=0  case 0x0ECDu:
  d=1   L  71  T=0 F=13  T=0 F=0  case 0x0EBCu:
  d=1   L  77  T=0 F=41  T=0 F=0  if (u == 0x0E3Au)
  d=1   L  82  T=20 F=63  T=10 F=14  switch (klass)
  d=1   L  87  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC10: /* sheva */
  d=1   L  88  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC11: /* hataf segol */
  d=1   L  89  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC12: /* hataf patah */
  d=1   L  90  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC13: /* hataf qamats */
  d=1   L  91  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC14: /* hiriq */
  d=1   L  92  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC15: /* tsere */
  d=1   L  93  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC16: /* segol */
  d=1   L  94  T=0 F=83  T=2 F=22  case HB_MODIFIED_COMBINING_CLASS_CCC17: /* patah */
  d=1   L  95  T=1 F=82  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC18: /* qamats & qamat...
  d=1   L  96  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC20: /* qubuts */
  d=1   L  97  T=2 F=81  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC22: /* meteg */
  d=1   L 100  T=0 F=83  T=1 F=23  case HB_MODIFIED_COMBINING_CLASS_CCC23: /* rafe */
  d=1   L 103  T=0 F=83  T=1 F=23  case HB_MODIFIED_COMBINING_CLASS_CCC24: /* shin dot */
  d=1   L 106  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC25: /* sin dot */
  d=1   L 107  T=5 F=78  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC19: /* holam & holam ...
  d=1   L 110  T=6 F=77  T=8 F=16  case HB_MODIFIED_COMBINING_CLASS_CCC26: /* point varika */
  d=1   L 113  T=0 F=83  T=1 F=23  case HB_MODIFIED_COMBINING_CLASS_CCC21: /* dagesh */
  d=1   L 119  T=5 F=78  T=1 F=23  case HB_MODIFIED_COMBINING_CLASS_CCC27: /* fathatan */
  d=1   L 120  T=3 F=80  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC28: /* dammatan */
  d=1   L 121  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC30: /* fatha */
  d=1   L 122  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC31: /* damma */
  d=1   L 123  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC33: /* shadda */
  d=1   L 124  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC34: /* sukun */
  d=1   L 125  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC35: /* superscript al...
  d=1   L 126  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC36: /* superscript al...
  d=1   L 129  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC29: /* kasratan */
  d=1   L 130  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC32: /* kasra */
  d=1   L 136  T=3 F=80  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC103: /* sara u / sara...
  d=1   L 139  T=2 F=81  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC107: /* mai */
  d=1   L 145  T=36 F=47  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC118: /* sign u / sign...  <-- BLOCKER
  d=1   L 148  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC122: /* mai */
  d=1   L 154  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC129: /* sign aa */
  d=1   L 157  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC130: /* sign i*/
  d=1   L 160  T=0 F=83  T=0 F=24  case HB_MODIFIED_COMBINING_CLASS_CCC132: /* sign u */

[off-chain: 44 additional divergent branches across 6 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=04dbb8139e6820e9, size=39 bytes, fuzzer=value_profile, trial=1, discovered_at=690s, mutation_op=CrossoverInsertMutator):
  0000: 01 01 00 00 47 0e 00 00 00 0e 00 00 4b 0e 00 00   ....G.......K...
  0010: 00 00 1a 00 b9 0e 00 00 4c ff 7f ff ff 1b 00 f0   ........L.......
  0020: 4b 0e 00 00 4c 0e 00                              K...L..
Seed 2 (id=6639a9032f7ffe2a, size=84 bytes, fuzzer=cmplog, trial=1, discovered_at=920s, mutation_op=BytesRandSetMutator,CrossoverReplaceMutator,TokenReplace,CrossoverReplaceMutator,BytesDeleteMutator,BytesCopyMutator,BytesSwapMutator):
  0000: b9 b9 b9 b9 b9 b9 b4 b4 b4 b4 b4 b9 b9 b9 ae ae   ................
  0010: 0c 00 01 02 00 fe 10 00 55 06 02 03 00 03 02 00   ........U.......
  0020: b9 0e 00 00 00 fe 01 01 00 03 00 00 00 fe 02 00   ................
  0030: b9 06 06 02 00 03 01 01 00 03 01 03 00 03 02 00   ................
Seed 3 (id=8f2a9151726c6119, size=67 bytes, fuzzer=cmplog, trial=1, discovered_at=1008s, mutation_op=ByteIncMutator,TokenInsert,WordInterestingMutator,BytesRandInsertMutator,ByteIncMutator):
  0000: b9 b9 66 63 05 04 03 00 03 0c 00 20 03 03 00 b8   ..fc....... ....
  0010: 05 00 00 00 00 0d 00 00 fe 00 00 20 03 00 00 b9   ........... ....
  0020: 0e 00 00 00 00 00 00 00 00 39 00 00 e9 4b 00 00   .........9...K..
  0030: 03 00 00 00 03 00 20 26 18 21 10 00 20 20 20 20   ...... &.!..    
Seed 4 (id=4f41fde8d44e9817, size=63 bytes, fuzzer=cmplog, trial=1, discovered_at=1162s, mutation_op=WordAddMutator):
  0000: b9 10 10 10 b9 66 63 05 04 03 00 03 0c 00 2d 68   .....fc.......-h
  0010: 20 03 03 00 b8 05 0e 00 00 00 0d 00 00 fe 00 00    ...............
  0020: 20 03 01 00 b9 0e 00 00 ff 15 00 00 20 03 00 20    ........... .. 
  0030: b9 0e 00 00 18 21 10 00 00 20 20 20 20 6b 65      .....!...    ke
Seed 5 (id=458230754de4d2bf, size=89 bytes, fuzzer=cmplog, trial=1, discovered_at=1210s, mutation_op=BytesDeleteMutator,BytesDeleteMutator,ByteDecMutator):
  0000: cb cb cb cb cb cb cb cb cb cb cb cb 20 35 21 20   ............ 5! 
  0010: 00 ef 4c 0e 00 00 34 20 20 20 cd cc 06 ff 03 04   ..L...4   ......
  0020: 00 02 03 00 6a 79 2c 02 00 00 00 6d 64 20 40 20   ....jy,....md @ 
  0030: 2c ff 5a 5a ff 5a 5a 5a 5a 5a 00 20 20 4c 4c 4c   ,.ZZ.ZZZZZ.  LLL

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=05ccefe62cd4035d, size=50 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=297s, mutation_op=WordInterestingMutator,BytesSwapMutator,TokenReplace,DwordAddMutator,TokenInsert):
  0000: 20 20 3f 00 01 04 00 00 6f 74 61 6c 01 20 1c 20     ?.....otal. . 
  0010: 4a e9 01 00 20 01 00 00 00 01 00 02 7a 6f 2d 00   J... .......zo-.
  0020: 4a e9 01 00 20 20 20 20 00 00 16 00 d6 20 20 00   J...    .....  .
  0030: ff 08                                             ..
Seed 2 (id=028c60a6bf99e5e5, size=90 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=637s, mutation_op=BitFlipMutator,BytesCopyMutator):
  0000: b2 b2 b2 b2 b2 b2 00 00 00 00 00 00 00 00 02 00   ................
  0010: 20 00 00 00 00 72 60 f1 f3 ff bf 05 00 00 ff bf    ....r`.........
  0020: 05 00 00 00 00 01 00 1e fa 67 76 5b 5b 5b 5b 5b   .........gv[[[[[
  0030: 5b 5b 5b 5b 5b 47 47 ff 08 00 05 72 20 f3 f3 f3   [[[[[GG....r ...
Seed 3 (id=06458dae620cb2e6, size=59 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=646s, mutation_op=BytesInsertMutator,BytesSwapMutator,ByteFlipMutator,BytesDeleteMutator,BytesInsertMutator):
  0000: 20 74 74 63 66 20 20 20 20 20 20 20 20 20 20 20    ttcf           
  0010: 20 20 20 20 20 00 01 20 b4 20 20 20 20 6e 6f 72        .. .    nor
  0020: 73 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20   s               
  0030: 04 03 00 02 06 03 00 00 f0 08 00                  ...........
Seed 4 (id=00d38771b6ed0d47, size=85 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=756s, mutation_op=QwordAddMutator,BytesCopyMutator,WordInterestingMutator,BitFlipMutator,ByteInterestingMutator):
  0000: 5a 5a 5a 17 00 00 00 5a 5a 5a 5a 5a 5a ff 00 80   ZZZ....ZZZZZZ...
  0010: 00 04 0a 00 00 02 01 00 04 02 01 24 47 ba 64 00   ...........$G.d.
  0020: 00 01 bb dc dc dc c7 dc dc dc dc dc 23 00 0c 00   ............#...
  0030: 00 00 00 00 00 00 20 00 00 47 0c 00 00 00 00 00   ...... ..G......
Seed 5 (id=02d96aca4be980d2, size=52 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=843s, mutation_op=BytesSetMutator,ByteRandMutator,ByteFlipMutator,BytesRandSetMutator,BytesDeleteMutator,CrossoverInsertMutator,DwordAddMutator):
  0000: e8 06 00 00 e8 06 00 00 00 02 64 10 ce 06 00 00   ..........d.....
  0010: ca 08 00 00 00 02 64 10 e8 06 00 00 e8 06 00 00   ......d.........
  0020: f4 24 01 d7 11 07 70 78 2d 00 9d aa 7e 18 80 20   .$....px-...~.. 
  0030: 02 00 00 00                                       ....


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0006  00(.)x8 b4(.)x2 b9(.)x2 03(.)x1 +7u  00(.)x6 20( )x3 18(.)x1             PARTIAL
   0x0013  00(.)x8 02(.)x3 b9(.)x2 0e(.)x1 +6u  00(.)x6 20( )x2 e4(.)x1 e7(.)x1     PARTIAL
   0x0032  00(.)x6 b9(.)x2 06(.)x1 5a(Z)x1 +6u  00(.)x6 5b([)x1 2e(.)x1             PARTIAL
   0x003c  00(.)x6 20( )x3 40(@)x1 10(.)x1 +4u  20( )x2 00(.)x2 e9(.)x1 03(.)x1     PARTIAL
   0x003e  00(.)x7 20( )x2 02(.)x1 65(e)x1 +4u  00(.)x4 f3(.)x1 0a(.)x1             PARTIAL
   0x003f  00(.)x6 22(")x2 20( )x1 4c(L)x1 +4u  00(.)x4 f3(.)x1 0a(.)x1             PARTIAL
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
  prompts_b/harfbuzz_5660.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5660,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>value_profile_cmplog (I2S), cmplog>value_profile_cmplog (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5660 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5660 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5660 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).