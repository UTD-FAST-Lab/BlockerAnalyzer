==== BLOCKER ====
Target: harfbuzz
Branch ID: 5662
Location: /src/harfbuzz/src/hb-ot-shape-fallback.cc:154:5
Enclosing function: hb-ot-shape-fallback.cc:recategorize_combining_class(unsigned int, unsigned int)
Source line:     case HB_MODIFIED_COMBINING_CLASS_CCC129: /* sign aa */
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            8        2          0  winner (I2S vs cmplog)
cmplog                           2        8          0  loser (I2S vs naive)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             3        7          0  REFERENCE
naive_ctx                        8        2          0  REFERENCE
naive_ngram4                     8        2          0  REFERENCE
mopt                             9        1          0  REFERENCE
minimizer                       10        0          0  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         0       10          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.10h  loser=20.90h
  avg hitcount on branch: winner=9  loser=0
  prob_div=0.60  dur_div=9.80h  hit_div=8
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5662/{W,L}/branch_coverage_show.txt

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
[L]    49  	case 0x0E34u:
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
[ ]    60  	case 0x0EB1u:
[ ]    61  	case 0x0EB4u:
[ ]    62  	case 0x0EB5u:
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
[L]    97      case HB_MODIFIED_COMBINING_CLASS_CCC22: /* meteg */
[L]    98        return HB_UNICODE_COMBINING_CLASS_BELOW;
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
[ ]   119      case HB_MODIFIED_COMBINING_CLASS_CCC27: /* fathatan */
[ ]   120      case HB_MODIFIED_COMBINING_CLASS_CCC28: /* dammatan */
[ ]   121      case HB_MODIFIED_COMBINING_CLASS_CCC30: /* fatha */
[ ]   122      case HB_MODIFIED_COMBINING_CLASS_CCC31: /* damma */
[W]   123      case HB_MODIFIED_COMBINING_CLASS_CCC33: /* shadda */
[W]   124      case HB_MODIFIED_COMBINING_CLASS_CCC34: /* sukun */
[W]   125      case HB_MODIFIED_COMBINING_CLASS_CCC35: /* superscript alef */
[W]   126      case HB_MODIFIED_COMBINING_CLASS_CCC36: /* superscript alaph */
[W]   127        return HB_UNICODE_COMBINING_CLASS_ABOVE;
[ ]   128  
[ ]   129      case HB_MODIFIED_COMBINING_CLASS_CCC29: /* kasratan */
[W]   130      case HB_MODIFIED_COMBINING_CLASS_CCC32: /* kasra */
[W]   131        return HB_UNICODE_COMBINING_CLASS_BELOW;
[ ]   132  
[ ]   133  
[ ]   134      /* Thai */
[ ]   135  
[ ]   136      case HB_MODIFIED_COMBINING_CLASS_CCC103: /* sara u / sara uu */
[ ]   137        return HB_UNICODE_COMBINING_CLASS_BELOW_RIGHT;
[ ]   138  
[L]   139      case HB_MODIFIED_COMBINING_CLASS_CCC107: /* mai */
[L]   140        return HB_UNICODE_COMBINING_CLASS_ABOVE_RIGHT;
[ ]   141  
[ ]   142  
[ ]   143      /* Lao */
[ ]   144  
[L]   145      case HB_MODIFIED_COMBINING_CLASS_CCC118: /* sign u / sign uu */
[L]   146        return HB_UNICODE_COMBINING_CLASS_BELOW;
[ ]   147  
[W]   148      case HB_MODIFIED_COMBINING_CLASS_CCC122: /* mai */
[W]   149        return HB_UNICODE_COMBINING_CLASS_ABOVE;
[ ]   150  
[ ]   151  
[ ]   152      /* Tibetan */
[ ]   153  
[W]   154      case HB_MODIFIED_COMBINING_CLASS_CCC129: /* sign aa */ <-- BLOCKER
[W]   155        return HB_UNICODE_COMBINING_CLASS_BELOW;
[ ]   156  
[W]   157      case HB_MODIFIED_COMBINING_CLASS_CCC130: /* sign i*/
[W]   158        return HB_UNICODE_COMBINING_CLASS_ABOVE;
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
      97       482  hb-ot-shape-fallback.cc:position_cluster(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:418-437)
      42       191  _hb_ot_shape_fallback_mark_position_recategorize_marks(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:172-185)
      42       191  _hb_ot_shape_fallback_mark_position(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:444-465)
      42       191  _hb_ot_shape_fallback_kern(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:494-522)
      11        39  hb-ot-shape-fallback.cc:recategorize_combining_class(unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:37-166)  <-- enclosing
       5        17  hb-ot-shape-fallback.cc:zero_mark_advances(hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:193-206)
       5        17  hb-ot-shape-fallback.cc:position_around_base(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:322-409)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  _hb_ot_shape_fallback_mark_position_recategorize_marks(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:172-185) ---
  d=2   L 179  T=108 F=42  T=521 F=191  for (unsigned int i = 0; i < count; i++)
  d=2   L 180  T=11 F=97  T=39 F=482  if (_hb_glyph_info_get_general_category (&info[i]) == HB_...
--- d=1  hb-ot-shape-fallback.cc:recategorize_combining_class(unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:37-166) ---
  d=1   L  38  T=2 F=9  T=8 F=31  if (klass >= 200)
  d=1   L  42  T=2 F=7  T=15 F=16  if ((u & ~0xFF) == 0x0E00u)
  d=1   L  46  T=0 F=1  T=0 F=11  switch (u)
  d=1   L  48  T=0 F=1  T=3 F=8  case 0x0E31u:
  d=1   L  49  T=0 F=1  T=0 F=11  case 0x0E34u:
  d=1   L  50  T=1 F=0  T=0 F=11  case 0x0E35u:
  d=1   L  51  T=0 F=1  T=1 F=10  case 0x0E36u:
  d=1   L  52  T=0 F=1  T=0 F=11  case 0x0E37u:
  d=1   L  53  T=0 F=1  T=1 F=10  case 0x0E47u:
  d=1   L  54  T=0 F=1  T=2 F=9  case 0x0E4Cu:
  d=1   L  55  T=0 F=1  T=1 F=10  case 0x0E4Du:
  d=1   L  56  T=0 F=1  T=0 F=11  case 0x0E4Eu:
  d=1   L  60  T=0 F=1  T=0 F=11  case 0x0EB1u:
  d=1   L  61  T=0 F=1  T=0 F=11  case 0x0EB4u:
  d=1   L  62  T=0 F=1  T=0 F=11  case 0x0EB5u:
  d=1   L  63  T=0 F=1  T=1 F=10  case 0x0EB6u:
  d=1   L  64  T=0 F=1  T=0 F=11  case 0x0EB7u:
  d=1   L  65  T=0 F=1  T=0 F=11  case 0x0EBBu:
  d=1   L  66  T=0 F=1  T=0 F=11  case 0x0ECCu:
  d=1   L  67  T=0 F=1  T=0 F=11  case 0x0ECDu:
  d=1   L  71  T=0 F=1  T=2 F=9  case 0x0EBCu:
  d=1   L  77  T=0 F=1  T=0 F=4  if (u == 0x0E3Au)
  d=1   L  82  T=2 F=7  T=16 F=15  switch (klass)
  d=1   L  87  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC10: /* sheva */
  d=1   L  88  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC11: /* hataf segol */
  d=1   L  89  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC12: /* hataf patah */
  d=1   L  90  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC13: /* hataf qamats */
  d=1   L  91  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC14: /* hiriq */
  d=1   L  92  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC15: /* tsere */
  d=1   L  93  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC16: /* segol */
  d=1   L  94  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC17: /* patah */
  d=1   L  95  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC18: /* qamats & qamat...
  d=1   L  96  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC20: /* qubuts */
  d=1   L  97  T=0 F=9  T=8 F=23  case HB_MODIFIED_COMBINING_CLASS_CCC22: /* meteg */
  d=1   L 100  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC23: /* rafe */
  d=1   L 103  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC24: /* shin dot */
  d=1   L 106  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC25: /* sin dot */
  d=1   L 107  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC19: /* holam & holam ...
  d=1   L 110  T=1 F=8  T=4 F=27  case HB_MODIFIED_COMBINING_CLASS_CCC26: /* point varika */
  d=1   L 113  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC21: /* dagesh */
  d=1   L 119  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC27: /* fathatan */
  d=1   L 120  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC28: /* dammatan */
  d=1   L 121  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC30: /* fatha */
  d=1   L 122  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC31: /* damma */
  d=1   L 123  T=1 F=8  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC33: /* shadda */
  d=1   L 124  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC34: /* sukun */
  d=1   L 125  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC35: /* superscript al...
  d=1   L 126  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC36: /* superscript al...
  d=1   L 129  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC29: /* kasratan */
  d=1   L 130  T=1 F=8  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC32: /* kasra */
  d=1   L 136  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC103: /* sara u / sara...
  d=1   L 139  T=0 F=9  T=2 F=29  case HB_MODIFIED_COMBINING_CLASS_CCC107: /* mai */
  d=1   L 145  T=0 F=9  T=1 F=30  case HB_MODIFIED_COMBINING_CLASS_CCC118: /* sign u / sign...
  d=1   L 148  T=1 F=8  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC122: /* mai */
  d=1   L 154  T=2 F=7  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC129: /* sign aa */  <-- BLOCKER
  d=1   L 157  T=1 F=8  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC130: /* sign i*/
  d=1   L 160  T=0 F=9  T=0 F=31  case HB_MODIFIED_COMBINING_CLASS_CCC132: /* sign u */

[off-chain: 12 additional divergent branches across 5 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=aee1ecb9daad6b20, size=166 bytes, fuzzer=naive, trial=1, discovered_at=7998s, mutation_op=ByteFlipMutator,BytesRandSetMutator):
  0000: 97 97 97 00 02 20 00 ff 20 20 20 20 20 20 ef 01   ..... ..      ..
  0010: 0e 00 61 61 61 61 0c 0c 73 6e 2d 48 00 00 e3 0c   ..aaaa..sn-H....
  0020: 00 00 35 0e 00 00 cb 1a 00 00 cb 0e 00 00 cb 1a   ..5.............
  0030: 00 00 cb f8 c2 05 cb 0c 10 00 b1 06 00 ff 35 0e   ..............5.
Seed 2 (id=9a5f3a4fd7f59655, size=101 bytes, fuzzer=naive, trial=1, discovered_at=58163s, mutation_op=BitFlipMutator,CrossoverInsertMutator,DwordInterestingMutator):
  0000: cb 0c 00 00 cb 0b 00 00 02 00 65 7a 68 2d 68 61   ..........ezh-ha
  0010: 20 20 ca ae 07 ae 6e 73 00 08 00 2d e8 03 6e 73     ....ns...-..ns
  0020: 00 06 01 00 34 f9 00 34 34 34 34 6c 00 1a 06 00   ....4..4444l....
  0030: 00 4e 05 00 80 e6 06 ca ca ca ca ca ca 00 00 4e   .N.............N

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0205153660619483, size=58 bytes, fuzzer=cmplog, trial=2, discovered_at=169s, mutation_op=ByteInterestingMutator,TokenInsert,WordAddMutator,ByteDecMutator):
  0000: fb 00 00 1a 00 00 00 00 00 0b 00 00 10 41 41 41   .............AAA
  0010: 41 41 0b 0b 0b 0b 0b 0b 00 7f 7f 7f 0c 0b 0b 0b   AA..............
  0020: 0d 0b 0b f5 0b 0b 01 00 10 01 0a 00 01 00 00 0b   ................
  0030: 1a 2e 20 20 2e 12 01 00 00 0d                     ..  ......
Seed 2 (id=007c63ce736c0eb9, size=43 bytes, fuzzer=cmplog, trial=2, discovered_at=638s, mutation_op=BytesSetMutator,BytesRandInsertMutator,QwordAddMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 08 08 08 08 08 08 08 08 08 08 08   ................
  0010: 08 08 08 08 08 00 53 56 b6 0e 00 00 15 03 00 00   ......SV........
  0020: 00 20 20 20 20 20 20 20 4f 54 90                  .       OT.
Seed 3 (id=0086ef0d21554a5b, size=85 bytes, fuzzer=cmplog, trial=2, discovered_at=673s, mutation_op=ByteFlipMutator,BytesRandSetMutator,BytesCopyMutator,BytesDeleteMutator):
  0000: 20 ff ff ff df 00 01 00 61 67 69 6c 00 ff 02 00    .......agil....
  0010: 20 00 10 00 04 00 00 20 20 00 00 20 00 20 20 12    ......  .. .  .
  0020: 12 12 00 2c 2c 2c 44 44 44 44 44 44 44 44 44 44   ...,,,DDDDDDDDDD
  0030: 44 44 44 00 00 00 00 00 00 00 00 00 00 00 00 00   DDD.............
Seed 4 (id=0011b6b57575fd99, size=77 bytes, fuzzer=cmplog, trial=2, discovered_at=727s, mutation_op=BytesDeleteMutator,WordAddMutator,BytesInsertMutator,ByteInterestingMutator,ByteNegMutator,BytesExpandMutator):
  0000: f8 19 00 0a 00 6b 61 72 20 20 20 01 01 00 80 01   .....kar   .....
  0010: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0020: 00 1e ff ff 02 00 0e 02 00 20 00 02 00 00 04 53   ......... .....S
  0030: 56 47 0e 03 00 00 0e 02 00 20 00 20 02 40 04 53   VG....... . .@.S
Seed 5 (id=01a95adcf2e1f269, size=183 bytes, fuzzer=cmplog, trial=2, discovered_at=1062s, mutation_op=QwordAddMutator,CrossoverReplaceMutator,BytesSetMutator,ByteRandMutator,ByteRandMutator):
  0000: e7 df 20 20 74 00 00 00 00 20 20 78 78 78 78 78   ..  t....  xxxxx
  0010: 78 10 00 20 20 d9 65 72 e7 39 20 00 74 00 20 05   x..  .er.9 .t. .
  0020: e5 20 00 0c 00 1a ff 00 01 00 00 20 00 00 ff ff   . ......... ....
  0030: 06 00 00 09 00 0d 00 1a 73 e1 e1 e1 e1 e1 e1 e1   ........s.......


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  97(.)x1 cb(.)x1                     00(.)x3 31(1)x2 fb(.)x1 20( )x1 +3u  DIFFER
   0x0001  97(.)x1 0c(.)x1                     00(.)x2 0e(.)x2 01(.)x1 ff(.)x1 +4u  DIFFER
   0x0002  97(.)x1 00(.)x1                     00(.)x3 01(.)x2 ff(.)x1 20( )x1 +3u  PARTIAL
   0x0003  00(.)x2                             00(.)x3 1a(.)x2 ff(.)x1 0a(.)x1 +3u  PARTIAL
   0x0004  02(.)x1 cb(.)x1                     00(.)x5 4d(M)x2 df(.)x1 74(t)x1 +1u  DIFFER
   0x0005  20( )x1 0b(.)x1                     00(.)x5 0e(.)x2 08(.)x1 6b(k)x1 +1u  DIFFER
   0x0006  00(.)x2                             00(.)x2 08(.)x1 01(.)x1 61(a)x1 +5u  PARTIAL
   0x0007  ff(.)x1 00(.)x1                     00(.)x6 08(.)x1 72(r)x1 0f(.)x1 +1u  PARTIAL
   0x0008  20( )x1 02(.)x1                     00(.)x3 ff(.)x2 08(.)x1 61(a)x1 +3u  PARTIAL
   0x0009  20( )x1 00(.)x1                     20( )x3 0e(.)x2 0b(.)x1 08(.)x1 +3u  PARTIAL
   0x000a  20( )x1 65(e)x1                     20( )x3 01(.)x2 00(.)x1 08(.)x1 +3u  PARTIAL
   0x000b  20( )x1 7a(z)x1                     00(.)x3 08(.)x2 6c(l)x1 01(.)x1 +3u  PARTIAL
   0x000c  20( )x1 68(h)x1                     10(.)x2 4a(J)x2 08(.)x1 00(.)x1 +4u  PARTIAL
   0x000d  20( )x1 2d(-)x1                     00(.)x3 0e(.)x2 41(A)x1 08(.)x1 +3u  DIFFER
   0x000e  ef(.)x1 68(h)x1                     00(.)x2 41(A)x1 08(.)x1 02(.)x1 +5u  DIFFER
   0x000f  01(.)x1 61(a)x1                     00(.)x3 41(A)x1 08(.)x1 01(.)x1 +4u  PARTIAL
   0x0010  0e(.)x1 20( )x1                     41(A)x1 08(.)x1 20( )x1 00(.)x1 +6u  PARTIAL
   0x0011  00(.)x1 20( )x1                     00(.)x2 20( )x2 41(A)x1 08(.)x1 +4u  PARTIAL
   0x0012  61(a)x1 ca(.)x1                     00(.)x2 02(.)x2 0b(.)x1 08(.)x1 +4u  DIFFER
   0x0013  61(a)x1 ae(.)x1                     00(.)x4 0b(.)x1 08(.)x1 20( )x1 +3u  DIFFER
   0x0014  61(a)x1 07(.)x1                     0b(.)x1 08(.)x1 04(.)x1 00(.)x1 +6u  DIFFER
   0x0015  61(a)x1 ae(.)x1                     00(.)x3 0b(.)x1 d9(.)x1 0e(.)x1 +4u  DIFFER
   0x0016  0c(.)x1 6e(n)x1                     00(.)x4 0b(.)x1 53(S)x1 65(e)x1 +3u  DIFFER
   0x0017  0c(.)x1 73(s)x1                     00(.)x4 0b(.)x1 56(V)x1 20( )x1 +3u  DIFFER
   0x0018  73(s)x1 00(.)x1                     00(.)x3 20( )x2 b6(.)x1 e7(.)x1 +3u  PARTIAL
   0x0019  6e(n)x1 08(.)x1                     0e(.)x3 00(.)x3 7f(.)x1 39(9)x1 +2u  DIFFER
   0x001a  2d(-)x1 00(.)x1                     00(.)x6 7f(.)x1 20( )x1 1a(.)x1 +1u  PARTIAL
   0x001b  48(H)x1 2d(-)x1                     00(.)x5 7f(.)x1 20( )x1 ef(.)x1 +2u  DIFFER
   0x001c  00(.)x1 e8(.)x1                     00(.)x2 0c(.)x1 15(.)x1 74(t)x1 +5u  PARTIAL
   0x001d  00(.)x1 03(.)x1                     00(.)x3 0e(.)x2 0b(.)x1 03(.)x1 +3u  PARTIAL
   0x001e  e3(.)x1 6e(n)x1                     00(.)x3 20( )x2 0b(.)x1 01(.)x1 +3u  DIFFER
   0x001f  0c(.)x1 73(s)x1                     00(.)x4 0b(.)x1 12(.)x1 05(.)x1 +3u  DIFFER
   0x0020  00(.)x2                             00(.)x2 0d(.)x1 12(.)x1 e5(.)x1 +5u  PARTIAL
   0x0021  00(.)x1 06(.)x1                     20( )x2 0e(.)x2 0b(.)x1 12(.)x1 +4u  DIFFER
   0x0022  35(5)x1 01(.)x1                     00(.)x4 0b(.)x1 20( )x1 ff(.)x1 +3u  DIFFER
   0x0023  0e(.)x1 00(.)x1                     00(.)x2 02(.)x2 f5(.)x1 20( )x1 +4u  PARTIAL
   0x0024  00(.)x1 34(4)x1                     00(.)x2 0b(.)x1 20( )x1 2c(,)x1 +5u  PARTIAL
   0x0025  00(.)x1 f9(.)x1                     0e(.)x3 00(.)x2 0b(.)x1 20( )x1 +3u  PARTIAL
   0x0026  cb(.)x1 00(.)x1                     0e(.)x2 01(.)x1 20( )x1 44(D)x1 +4u  DIFFER
   0x0027  1a(.)x1 34(4)x1                     00(.)x3 20( )x1 44(D)x1 02(.)x1 +3u  DIFFER
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
  prompts_b/harfbuzz_5662.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5662,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5662 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5662 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5662 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).