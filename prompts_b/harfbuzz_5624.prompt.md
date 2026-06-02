==== BLOCKER ====
Target: harfbuzz
Branch ID: 5624
Location: /src/harfbuzz/src/hb-ot-shape-fallback.cc:52:2
Enclosing function: hb-ot-shape-fallback.cc:recategorize_combining_class(unsigned int, unsigned int)
Source line: 	case 0x0E37u:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  REFERENCE
cmplog                           8        2          0  winner (value_profile vs value_profile_cmplog)
value_profile                   10        0          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             1        9          0  loser (I2S vs value_profile); loser (value_profile vs cmplog)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         5        5          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=1.60h  loser=18.70h
  avg hitcount on branch: winner=166  loser=5
  prob_div=0.90  dur_div=17.10h  hit_div=160
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002
--- Pair 2: cmplog > value_profile_cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=7.60h  loser=18.70h
  avg hitcount on branch: winner=4  loser=5
  prob_div=0.70  dur_div=11.10h  hit_div=1
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5624/{W,L}/branch_coverage_show.txt

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
[B]    46        switch (u)
[B]    47        {
[L]    48  	case 0x0E31u:
[B]    49  	case 0x0E34u:
[B]    50  	case 0x0E35u:
[B]    51  	case 0x0E36u:
[B]    52  	case 0x0E37u: <-- BLOCKER
[B]    53  	case 0x0E47u:
[B]    54  	case 0x0E4Cu:
[B]    55  	case 0x0E4Du:
[B]    56  	case 0x0E4Eu:
[B]    57  	  klass = HB_UNICODE_COMBINING_CLASS_ABOVE_RIGHT;
[B]    58  	  break;
[ ]    59  
[ ]    60  	case 0x0EB1u:
[ ]    61  	case 0x0EB4u:
[L]    62  	case 0x0EB5u:
[L]    63  	case 0x0EB6u:
[L]    64  	case 0x0EB7u:
[L]    65  	case 0x0EBBu:
[L]    66  	case 0x0ECCu:
[L]    67  	case 0x0ECDu:
[L]    68  	  klass = HB_UNICODE_COMBINING_CLASS_ABOVE;
[L]    69  	  break;
[ ]    70  
[L]    71  	case 0x0EBCu:
[L]    72  	  klass = HB_UNICODE_COMBINING_CLASS_BELOW;
[L]    73  	  break;
[B]    74        }
[B]    75      } else {
[ ]    76        /* Thai virama is below-right */
[W]    77        if (u == 0x0E3Au)
[ ]    78  	klass = HB_UNICODE_COMBINING_CLASS_BELOW_RIGHT;
[W]    79      }
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
[W]    90      case HB_MODIFIED_COMBINING_CLASS_CCC13: /* hataf qamats */
[W]    91      case HB_MODIFIED_COMBINING_CLASS_CCC14: /* hiriq */
[W]    92      case HB_MODIFIED_COMBINING_CLASS_CCC15: /* tsere */
[W]    93      case HB_MODIFIED_COMBINING_CLASS_CCC16: /* segol */
[W]    94      case HB_MODIFIED_COMBINING_CLASS_CCC17: /* patah */
[W]    95      case HB_MODIFIED_COMBINING_CLASS_CCC18: /* qamats & qamats qatan */
[W]    96      case HB_MODIFIED_COMBINING_CLASS_CCC20: /* qubuts */
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
[ ]   107      case HB_MODIFIED_COMBINING_CLASS_CCC19: /* holam & holam haser for vav */
[ ]   108        return HB_UNICODE_COMBINING_CLASS_ABOVE_LEFT;
[ ]   109  
[B]   110      case HB_MODIFIED_COMBINING_CLASS_CCC26: /* point varika */
[B]   111        return HB_UNICODE_COMBINING_CLASS_ABOVE;
[ ]   112  
[ ]   113      case HB_MODIFIED_COMBINING_CLASS_CCC21: /* dagesh */
[ ]   114        break;
[ ]   115  
[ ]   116  
[ ]   117      /* Arabic and Syriac */
[ ]   118  
[W]   119      case HB_MODIFIED_COMBINING_CLASS_CCC27: /* fathatan */
[W]   120      case HB_MODIFIED_COMBINING_CLASS_CCC28: /* dammatan */
[W]   121      case HB_MODIFIED_COMBINING_CLASS_CCC30: /* fatha */
[W]   122      case HB_MODIFIED_COMBINING_CLASS_CCC31: /* damma */
[W]   123      case HB_MODIFIED_COMBINING_CLASS_CCC33: /* shadda */
[W]   124      case HB_MODIFIED_COMBINING_CLASS_CCC34: /* sukun */
[W]   125      case HB_MODIFIED_COMBINING_CLASS_CCC35: /* superscript alef */
[W]   126      case HB_MODIFIED_COMBINING_CLASS_CCC36: /* superscript alaph */
[W]   127        return HB_UNICODE_COMBINING_CLASS_ABOVE;
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
[ ]   139      case HB_MODIFIED_COMBINING_CLASS_CCC107: /* mai */
[ ]   140        return HB_UNICODE_COMBINING_CLASS_ABOVE_RIGHT;
[ ]   141  
[ ]   142  
[ ]   143      /* Lao */
[ ]   144  
[ ]   145      case HB_MODIFIED_COMBINING_CLASS_CCC118: /* sign u / sign uu */
[ ]   146        return HB_UNICODE_COMBINING_CLASS_BELOW;
[ ]   147  
[W]   148      case HB_MODIFIED_COMBINING_CLASS_CCC122: /* mai */
[W]   149        return HB_UNICODE_COMBINING_CLASS_ABOVE;
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
  d=1   L  38  T=12 F=55  T=2 F=21  if (klass >= 200)
  d=1   L  42  T=44 F=11  T=15 F=6  if ((u & ~0xFF) == 0x0E00u)
  d=1   L  46  T=0 F=42  T=0 F=15  switch (u)
  d=1   L  48  T=0 F=42  T=5 F=10  case 0x0E31u:
  d=1   L  49  T=5 F=37  T=0 F=15  case 0x0E34u:
  d=1   L  50  T=0 F=42  T=2 F=13  case 0x0E35u:
  d=1   L  51  T=0 F=42  T=0 F=15  case 0x0E36u:
  d=1   L  52  T=23 F=19  T=0 F=15  case 0x0E37u:  <-- BLOCKER
  d=1   L  53  T=2 F=40  T=1 F=14  case 0x0E47u:
  d=1   L  54  T=8 F=34  T=1 F=14  case 0x0E4Cu:
  d=1   L  55  T=4 F=38  T=1 F=14  case 0x0E4Du:
  d=1   L  56  T=0 F=42  T=0 F=15  case 0x0E4Eu:
  d=1   L  60  T=0 F=42  T=0 F=15  case 0x0EB1u:
  d=1   L  61  T=0 F=42  T=0 F=15  case 0x0EB4u:
  d=1   L  62  T=0 F=42  T=1 F=14  case 0x0EB5u:
  d=1   L  63  T=0 F=42  T=0 F=15  case 0x0EB6u:
  d=1   L  64  T=0 F=42  T=1 F=14  case 0x0EB7u:
  d=1   L  65  T=0 F=42  T=1 F=14  case 0x0EBBu:
  d=1   L  66  T=0 F=42  T=0 F=15  case 0x0ECCu:
  d=1   L  67  T=0 F=42  T=0 F=15  case 0x0ECDu:
  d=1   L  71  T=0 F=42  T=2 F=13  case 0x0EBCu:
  d=1   L  77  T=0 F=2  T=0 F=0  if (u == 0x0E3Au)
  d=1   L  82  T=46 F=9  T=19 F=2  switch (klass)
  d=1   L  87  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC10: /* sheva */
  d=1   L  88  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC11: /* hataf segol */
  d=1   L  89  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC12: /* hataf patah */
  d=1   L  90  T=1 F=54  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC13: /* hataf qamats */
  d=1   L  91  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC14: /* hiriq */
  d=1   L  92  T=1 F=54  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC15: /* tsere */
  d=1   L  93  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC16: /* segol */
  d=1   L  94  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC17: /* patah */
  d=1   L  95  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC18: /* qamats & qamat...
  d=1   L  96  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC20: /* qubuts */
  d=1   L  97  T=1 F=54  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC22: /* meteg */
  d=1   L 100  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC23: /* rafe */
  d=1   L 103  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC24: /* shin dot */
  d=1   L 106  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC25: /* sin dot */
  d=1   L 107  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC19: /* holam & holam ...
  d=1   L 110  T=1 F=54  T=2 F=19  case HB_MODIFIED_COMBINING_CLASS_CCC26: /* point varika */
  d=1   L 113  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC21: /* dagesh */
  d=1   L 119  T=1 F=54  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC27: /* fathatan */
  d=1   L 120  T=2 F=53  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC28: /* dammatan */
  d=1   L 121  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC30: /* fatha */
  d=1   L 122  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC31: /* damma */
  d=1   L 123  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC33: /* shadda */
  d=1   L 124  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC34: /* sukun */
  d=1   L 125  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC35: /* superscript al...
  d=1   L 126  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC36: /* superscript al...
  d=1   L 129  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC29: /* kasratan */
  d=1   L 130  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC32: /* kasra */
  d=1   L 136  T=1 F=54  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC103: /* sara u / sara...
  d=1   L 139  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC107: /* mai */
  d=1   L 145  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC118: /* sign u / sign...
  d=1   L 148  T=1 F=54  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC122: /* mai */
  d=1   L 154  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC129: /* sign aa */
  d=1   L 157  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC130: /* sign i*/
  d=1   L 160  T=0 F=55  T=0 F=21  case HB_MODIFIED_COMBINING_CLASS_CCC132: /* sign u */

[off-chain: 10 additional divergent branches across 5 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=d484b55bd133cd62, size=26 bytes, fuzzer=cmplog, trial=1, discovered_at=91s, mutation_op=ByteAddMutator,WordAddMutator,CrossoverInsertMutator,TokenInsert):
  0000: 6e 00 10 00 00 01 61 6e 2d 00 01 00 00 f8 1e 20   n.....an-...... 
  0010: 20 00 1a 4d 6b 64 00 f8 37 0e                      ..Mkd..7.
Seed 2 (id=025be01a9b9fc036, size=64 bytes, fuzzer=value_profile, trial=1, discovered_at=778s, mutation_op=ByteDecMutator,TokenReplace,DwordAddMutator,BytesRandSetMutator,ByteDecMutator,ByteInterestingMutator):
  0000: c6 c6 c6 ab 00 01 00 00 4c 0e 53 53 4c 0e 00 00   ........L.SSL...
  0010: 4c 20 ed eb eb eb eb eb eb eb eb 10 00 d7 68 68   L ............hh
  0020: 68 7a 6f 2d 68 61 6e 74 2d 6d 6f 00 37 0e 00 00   hzo-hant-mo.7...
  0030: b6 0e 00 ff 4c 0e 00 00 b6 0e 00 21 81 00 00 00   ....L......!....
Seed 3 (id=08aeeeefa81f5fb4, size=56 bytes, fuzzer=value_profile, trial=1, discovered_at=854s, mutation_op=BytesDeleteMutator,BytesDeleteMutator):
  0000: 12 01 00 00 00 80 17 20 80 12 00 00 00 00 80 fc   ....... ........
  0010: ff ff ff 00 37 0e 00 00 47 07 00 00 b9 0d ff ff   ....7...G.......
  0020: f5 00 00 80 20 40 20 00 00 00 00 00 37 0e 00 00   .... @ .....7...
  0030: 47 07 00 00 ad 0e 00 00                           G.......
Seed 4 (id=087d01cc6daaeb6f, size=41 bytes, fuzzer=value_profile, trial=1, discovered_at=863s, mutation_op=BytesRandInsertMutator,BytesInsertMutator):
  0000: d6 08 00 00 4c 37 37 37 37 37 37 37 37 37 37 37   ....L77777777777
  0010: 37 0e 00 00 47 0e 00 00 37 0e 00 00 00 00 0e 00   7...G...7.......
  0020: 01 37 0d ff 10 ff ff f3 0e                        .7.......
Seed 5 (id=000502d87c3cfa20, size=68 bytes, fuzzer=value_profile, trial=1, discovered_at=915s, mutation_op=BytesRandSetMutator):
  0000: f1 08 00 00 10 06 00 00 37 1c 00 00 f1 08 3b 3b   ........7.....;;
  0010: 3b 06 00 00 37 1c 00 00 4c 9f 9f 9f 4c 06 00 00   ;...7...L...L...
  0020: 37 0e 00 00 4c 9f 9f 9f 0e 17 00 36 0e 00 00 4c   7...L......6...L
  0030: 0e 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 91   ................

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=123324ab77c303d0, size=54 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=716s, mutation_op=BytesExpandMutator,DwordInterestingMutator,BytesDeleteMutator):
  0000: d7 0a 01 35 d7 0a 00 04 74 74 63 66 d7 0a 01 01   ...5....ttcf....
  0010: 01 fd fd fd fd fd fd fd fd 13 03 03 ff 58 08 de   .............X..
  0020: 26 20 fd fd fd fd fd fd fd fd fd fd fe 20 20 20   & ...........   
  0030: 20 6b 4f ff 47 0e                                  kO.G.
Seed 2 (id=785f25d29ad373fc, size=50 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=852s, mutation_op=DwordInterestingMutator,ByteFlipMutator,ByteFlipMutator,BytesDeleteMutator,CrossoverReplaceMutator,TokenInsert):
  0000: 00 00 ff ff 04 ff ff 02 00 00 00 02 66 68 70 72   ............fhpr
  0010: 02 ff 03 00 20 20 31 70 78 2d 68 61 91 73 ff 0f   ....  1px-ha.s..
  0020: 0e 00 ff ff 00 00 00 02 00 00 00 20 0a 03 00 00   ........... ....
  0030: 31 0e                                             1.
Seed 3 (id=2f71a183b995a857, size=58 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1082s, mutation_op=BytesDeleteMutator,BytesRandSetMutator,TokenReplace):
  0000: 0e 0e 00 20 04 ff ff 00 00 00 00 02 66 68 70 72   ... ........fhpr
  0010: 02 ff 03 0d 00 20 20 20 20 f3 f3 f3 f3 00 ff 04   .....    .......
  0020: 00 20 31 70 78 2d 68 61 6e 73 ff ff 06 02 01 05   . 1px-hans......
  0030: 0e 03 00 00 4e 0e 01 00 31 0e                     ....N...1.
Seed 4 (id=49054c97656b5a65, size=105 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1207s, mutation_op=QwordAddMutator,BytesInsertCopyMutator,DwordAddMutator,BitFlipMutator,BytesDeleteMutator):
  0000: ff 02 18 e8 40 4a e8 e8 ff 02 18 e8 40 4a 80 8f   ....@J......@J..
  0010: 73 0a 00 22 e2 e2 e2 e2 e2 e2 2d 68 61 6e 74 08   s.."......-hant.
  0020: 02 20 ff 04 02 01 00 20 61 6e 73 00 7f 01 01 00   . ..... ans.....
  0030: 01 03 02 00 61 6e 73 00 00 03 00 00 74 66 ff ff   ....ans.....tf..
Seed 5 (id=41b092eee9e8a8f1, size=44 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1327s, mutation_op=BytesDeleteMutator):
  0000: 00 2b 6e 6f 6e 64 df ff 32 0e 00 20 1f e2 02 00   .+nond..2.. ....
  0010: ff 00 00 00 31 0e 00 00 1f e2 00 00 b7 0e 00 00   ....1...........
  0020: 00 1f 01 00 31 0e 00 00 1f 00 1f e2               ....1.......


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0033  00(.)x3 ff(.)x1 9f(.)x1 0e(.)x1 +3u  00(.)x3 ff(.)x2 80(.)x1             PARTIAL
   0x0035  0e(.)x2 00(.)x2 9f(.)x1 6b(k)x1 +3u  0e(.)x2 6e(n)x1 10(.)x1 1a(.)x1     PARTIAL
   0x0036  00(.)x4 9f(.)x1 4f(O)x1 10(.)x1 +2u  01(.)x2 73(s)x1 02(.)x1             DIFFER
   0x0037  00(.)x5 9f(.)x1 01(.)x1 10(.)x1 +1u  00(.)x3 f2(.)x1                     PARTIAL
   0x0038  00(.)x3 b6(.)x1 9f(.)x1 10(.)x1 +2u  31(1)x1 00(.)x1 2e(.)x1 db(.)x1     PARTIAL
   0x0039  00(.)x4 0e(.)x1 9f(.)x1 35(5)x1 +1u  0e(.)x1 03(.)x1 00(.)x1             PARTIAL
   0x003a  00(.)x4 9f(.)x1 03(.)x1 05(.)x1 +1u  00(.)x2                             PARTIAL
   0x003b  00(.)x3 21(!)x1 9f(.)x1 03(.)x1 +1u  00(.)x1 4c(L)x1                     PARTIAL
   0x003c  00(.)x4 81(.)x1 9f(.)x1 02(.)x1     74(t)x1 0e(.)x1                     DIFFER
   0x003d  00(.)x4 9f(.)x1 37(7)x1 01(.)x1     66(f)x1 00(.)x1                     PARTIAL
   0x003e  0e(.)x3 00(.)x1 9f(.)x1 01(.)x1 +1u  ff(.)x1 00(.)x1                     PARTIAL
   0x003f  00(.)x4 91(.)x1 01(.)x1 4d(M)x1     ff(.)x1 bc(.)x1                     DIFFER
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
  prompts_b/harfbuzz_5624.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5624,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5624 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5624 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5624 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).