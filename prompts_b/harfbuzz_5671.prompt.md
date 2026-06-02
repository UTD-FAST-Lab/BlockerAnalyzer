==== BLOCKER ====
Target: harfbuzz
Branch ID: 5671
Location: /src/harfbuzz/src/hb-ot-shape-fallback.cc:328:7
Enclosing function: hb-ot-shape-fallback.cc:position_around_base(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)
Source line:   if (!font->get_glyph_extents (buffer->info[base].codepoint,
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           4        6          0  REFERENCE
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                        10        0          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=2.10h  loser=24.00h
  avg hitcount on branch: winner=681  loser=0
  prob_div=1.00  dur_div=21.90h  hit_div=681
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5671/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shape-fallback.cc:position_around_base(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool) (/src/harfbuzz/src/hb-ot-shape-fallback.cc:322-409) ---
[ ]   320  		      unsigned int end,
[ ]   321  		      bool adjust_offsets_when_zeroing)
[B]   322  {
[B]   323    hb_direction_t horiz_dir = HB_DIRECTION_INVALID;
[ ]   324  
[B]   325    buffer->unsafe_to_break (base, end);
[ ]   326  
[B]   327    hb_glyph_extents_t base_extents;
[B]   328    if (!font->get_glyph_extents (buffer->info[base].codepoint, <-- BLOCKER
[B]   329  				&base_extents))
[L]   330    {
[ ]   331      /* If extents don't work, zero marks and go home. */
[L]   332      zero_mark_advances (buffer, base + 1, end, adjust_offsets_when_zeroing);
[L]   333      return;
[L]   334    }
[W]   335    base_extents.y_bearing += buffer->pos[base].y_offset;
[ ]   336    /* Use horizontal advance for horizontal positioning.
[ ]   337     * Generally a better idea.  Also works for zero-ink glyphs.  See:
[ ]   338     * https://github.com/harfbuzz/harfbuzz/issues/1532 */
[W]   339    base_extents.x_bearing = 0;
[W]   340    base_extents.width = font->get_glyph_h_advance (buffer->info[base].codepoint);
[ ]   341  
[W]   342    unsigned int lig_id = _hb_glyph_info_get_lig_id (&buffer->info[base]);
[ ]   343    /* Use integer for num_lig_components such that it doesn't convert to unsigned
[ ]   344     * when we divide or multiply by it. */
[W]   345    int num_lig_components = _hb_glyph_info_get_lig_num_comps (&buffer->info[base]);
[ ]   346  
[W]   347    hb_position_t x_offset = 0, y_offset = 0;
[W]   348    if (HB_DIRECTION_IS_FORWARD (buffer->props.direction)) {
[W]   349      x_offset -= buffer->pos[base].x_advance;
[W]   350      y_offset -= buffer->pos[base].y_advance;
[W]   351    }
[ ]   352  
[W]   353    hb_glyph_extents_t component_extents = base_extents;
[W]   354    int last_lig_component = -1;
[W]   355    unsigned int last_combining_class = 255;
[W]   356    hb_glyph_extents_t cluster_extents = base_extents; /* Initialization is just to shut gcc up. */
[W]   357    hb_glyph_info_t *info = buffer->info;
[W]   358    for (unsigned int i = base + 1; i < end; i++)
[W]   359      if (_hb_glyph_info_get_modified_combining_class (&info[i]))
[W]   360      {
[W]   361        if (num_lig_components > 1) {
[ ]   362  	unsigned int this_lig_id = _hb_glyph_info_get_lig_id (&info[i]);
[ ]   363  	int this_lig_component = _hb_glyph_info_get_lig_comp (&info[i]) - 1;
[ ]   364  	/* Conditions for attaching to the last component. */
[ ]   365  	if (!lig_id || lig_id != this_lig_id || this_lig_component >= num_lig_components)
[ ]   366  	  this_lig_component = num_lig_components - 1;
[ ]   367  	if (last_lig_component != this_lig_component)
[ ]   368  	{
[ ]   369  	  last_lig_component = this_lig_component;
[ ]   370  	  last_combining_class = 255;
[ ]   371  	  component_extents = base_extents;
[ ]   372  	  if (unlikely (horiz_dir == HB_DIRECTION_INVALID)) {
[ ]   373  	    if (HB_DIRECTION_IS_HORIZONTAL (plan->props.direction))
[ ]   374  	      horiz_dir = plan->props.direction;
[ ]   375  	    else
[ ]   376  	      horiz_dir = hb_script_get_horizontal_direction (plan->props.script);
[ ]   377  	  }
[ ]   378  	  if (horiz_dir == HB_DIRECTION_LTR)
[ ]   379  	    component_extents.x_bearing += (this_lig_component * component_extents.width) / num_lig_components;
[ ]   380  	  else
[ ]   381  	    component_extents.x_bearing += ((num_lig_components - 1 - this_lig_component) * component_extents.width) / num_lig_components;
[ ]   382  	  component_extents.width /= num_lig_components;
[ ]   383  	}
[ ]   384        }
[ ]   385  
[W]   386        unsigned int this_combining_class = _hb_glyph_info_get_modified_combining_class (&info[i]);
[W]   387        if (last_combining_class != this_combining_class)
[W]   388        {
[W]   389  	last_combining_class = this_combining_class;
[W]   390  	cluster_extents = component_extents;
[W]   391        }
[ ]   392  
[W]   393        position_mark (plan, font, buffer, cluster_extents, i, this_combining_class);
[ ]   394  
[W]   395        buffer->pos[i].x_advance = 0;
[W]   396        buffer->pos[i].y_advance = 0;
[W]   397        buffer->pos[i].x_offset += x_offset;
[W]   398        buffer->pos[i].y_offset += y_offset;
[ ]   399  
[W]   400      } else {
[ ]   401        if (HB_DIRECTION_IS_FORWARD (buffer->props.direction)) {
[ ]   402  	x_offset -= buffer->pos[i].x_advance;
[ ]   403  	y_offset -= buffer->pos[i].y_advance;
[ ]   404        } else {
[ ]   405  	x_offset += buffer->pos[i].x_advance;
[ ]   406  	y_offset += buffer->pos[i].y_advance;
[ ]   407        }
[ ]   408      }
[W]   409  }

--- Caller (1 hop): hb-ot-shape-fallback.cc:position_cluster(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool) (/src/harfbuzz/src/hb-ot-shape-fallback.cc:418-437, calls hb-ot-shape-fallback.cc:position_around_base(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool) at line 433) (full body — short) ---
[B]   418  {
[B]   419    if (end - start < 2)
[B]   420      return;
[ ]   421  
[ ]   422    /* Find the base glyph */
[B]   423    hb_glyph_info_t *info = buffer->info;
[B]   424    for (unsigned int i = start; i < end; i++)
[B]   425      if (!_hb_glyph_info_is_unicode_mark (&info[i]))
[B]   426      {
[ ]   427        /* Find mark glyphs */
[B]   428        unsigned int j;
[B]   429        for (j = i + 1; j < end; j++)
[B]   430  	if (!_hb_glyph_info_is_unicode_mark (&info[j]))
[ ]   431  	  break;
[ ]   432  
[B]   433        position_around_base (plan, font, buffer, i, j, adjust_offsets_when_zeroing); <-- CALL
[ ]   434  
[B]   435        i = j - 1;
[B]   436      }
[B]   437  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shape-fallback.cc:position_cluster(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:418-437, calls hb-ot-shape-fallback.cc:position_around_base(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool) at line 433)
hop 3  _hb_ot_shape_fallback_mark_position(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:444-465, calls hb-ot-shape-fallback.cc:position_cluster(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool) at line 459)
hop 4  hb-ot-shape.cc:hb_ot_position_plan(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:1022-1097, calls _hb_ot_shape_fallback_mark_position(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, bool) at line 1095)
hop 5  hb-ot-shape.cc:hb_ot_position(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:1101-1112, calls hb-ot-shape.cc:hb_ot_position_plan(hb_ot_shape_context_t const*) at line 1106)
hop 6  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195, calls hb-ot-shape.cc:hb_ot_position(hb_ot_shape_context_t const*) at line 1185)
hop 7  _hb_ot_shape  (/src/harfbuzz/src/hb-ot-shape.cc:1204-1209, calls hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*) at line 1206)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0        27  hb-ot-shape-fallback.cc:zero_mark_advances(hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:193-206)
      20         0  hb-ot-shape-fallback.cc:position_mark(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, hb_glyph_extents_t&, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:215-313)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ot-shape-fallback.cc:position_cluster(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:418-437) ---
  d=2   L 425  T=20 F=0  T=27 F=4  if (!_hb_glyph_info_is_unicode_mark (&info[i]))
  d=2   L 430  T=0 F=20  T=0 F=48  if (!_hb_glyph_info_is_unicode_mark (&info[j]))
--- d=1  hb-ot-shape-fallback.cc:position_around_base(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:322-409) ---
  d=1   L 328  T=0 F=20  T=27 F=0  if (!font->get_glyph_extents (buffer->info[base].codepoint,  <-- BLOCKER
  d=1   L 358  T=20 F=20  T=0 F=0  for (unsigned int i = base + 1; i < end; i++)
  d=1   L 359  T=20 F=0  T=0 F=0  if (_hb_glyph_info_get_modified_combining_class (&info[i]))
  d=1   L 361  T=0 F=20  T=0 F=0  if (num_lig_components > 1) {
  d=1   L 387  T=20 F=0  T=0 F=0  if (last_combining_class != this_combining_class)

[off-chain: 89 additional divergent branches across 3 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=00722b1acd0aaeac, size=258 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=6538s, mutation_op=CrossoverReplaceMutator,DwordInterestingMutator,QwordAddMutator,ByteFlipMutator,ByteRandMutator,BytesExpandMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 43 4f 4c 52   ......      COLR
  0010: 20 ff 1f 20 00 00 00 18 00 01 00 00 01 ee 7f 0a    .. ............
  0020: 00 00 00 02 00 00 00 00 00 08 00 00 00 00 00 2e   ................
  0030: 2e 00 2e 2e 2e 20 72 01 24 01 00 01 00 0c 00 00   ..... r.$.......
Seed 2 (id=07a219e126f35230, size=226 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=6838s, mutation_op=ByteNegMutator,CrossoverReplaceMutator,BytesExpandMutator,ByteAddMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 0d 20 43 4f 4c 52   ......    . COLR
  0010: 20 ff 1f 20 00 00 00 18 00 01 00 00 01 ee 7f 0a    .. ............
  0020: 00 00 00 02 00 00 00 00 00 08 00 00 00 00 00 2e   ................
  0030: 2e 2e 2e 2e 20 72 01 24 02 00 03 00 00 00 00 00   .... r.$........
Seed 3 (id=37aac5d41d0361da, size=172 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=16842s, mutation_op=BytesExpandMutator,BitFlipMutator,ByteDecMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 43 4f 4c 52   ......      COLR
  0010: 20 ff 1f 20 00 00 00 18 00 01 00 00 01 ee 7f 0a    .. ............
  0020: 00 00 00 02 00 01 00 00 00 08 00 00 00 00 00 2e   ................
  0030: 2e 00 2e 2e 2e 20 72 01 24 01 00 01 00 0c 16 bf   ..... r.$.......
Seed 4 (id=2f14766fa42ed50c, size=258 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=27390s, mutation_op=BytesRandSetMutator,BytesCopyMutator,BytesCopyMutator,BytesDeleteMutator,DwordAddMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 43 4f 4c 52   ......      COLR
  0010: 20 ff 1f 20 00 00 00 18 00 01 00 00 01 ee 7f 0a    .. ............
  0020: 00 00 00 02 00 2d 00 00 00 08 ff ff 00 00 00 2e   .....-..........
  0030: 2e 00 2e 2e 2e 20 72 01 24 02 00 10 00 0c 01 02   ..... r.$.......
Seed 5 (id=1bd0264732bd59b2, size=343 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=31042s, mutation_op=CrossoverReplaceMutator,ByteAddMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 43 4f 4c 52   ......      COLR
  0010: 20 ff 1f 20 00 00 00 18 00 01 00 00 64 73 64 76    .. ........dsdv
  0020: 00 00 00 21 00 00 00 00 00 08 00 00 01 00 00 2e   ...!............
  0030: 2e 2e 2e 2e 20 72 00 24 00 00 01 00 0c 5f 25 a5   .... r.$....._%.

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=0059bffc70552fa0, size=62 bytes, fuzzer=value_profile, trial=1, discovered_at=197s, mutation_op=DwordInterestingMutator,BytesRandInsertMutator,BytesInsertMutator):
  0000: 00 01 0e 00 df 20 00 00 00 00 aa 13 df 20 3d 3d   ..... ....... ==
  0010: 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 00 ff   ==============..
  0020: df 20 00 00 00 00 00 20 20 20 20 20 20 20 20 20   . .....         
  0030: 2c 00 00 00 64 55 55 55 df 20 00 00 00 00         ,...dUUU. ....
Seed 2 (id=006ae19c29c5da15, size=122 bytes, fuzzer=value_profile, trial=1, discovered_at=707s, mutation_op=TokenInsert,WordAddMutator,QwordAddMutator,ByteDecMutator,BytesInsertMutator,TokenInsert):
  0000: bf bf bf bf bf bf bf bf bf bf 00 00 00 00 00 00   ................
  0010: 00 00 00 64 73 64 76 00 bf bf bf b4 00 10 cb 0e   ...dsdv.........
  0020: 10 00 b4 00 00 b4 0e 00 00 b4 0e 00 00 4b 00 00   .............K..
  0030: 00 00 00 00 00 00 00 0e ff 7f 6c 61 72 74 00 01   ..........lart..
Seed 3 (id=000502d87c3cfa20, size=68 bytes, fuzzer=value_profile, trial=1, discovered_at=915s, mutation_op=BytesRandSetMutator):
  0000: f1 08 00 00 10 06 00 00 37 1c 00 00 f1 08 3b 3b   ........7.....;;
  0010: 3b 06 00 00 37 1c 00 00 4c 9f 9f 9f 4c 06 00 00   ;...7...L...L...
  0020: 37 0e 00 00 4c 9f 9f 9f 0e 17 00 36 0e 00 00 4c   7...L......6...L
  0030: 0e 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 91   ................
Seed 4 (id=001d239360d6d616, size=136 bytes, fuzzer=value_profile, trial=1, discovered_at=958s, mutation_op=BytesDeleteMutator):
  0000: 32 8a 8a 8a 8a 00 e5 01 20 e7 89 15 00 fb 20 20   2....... .....  
  0010: 20 20 20 20 20 20 20 20 20 20 20 20 20 7f 80 54                ..T
  0020: 54 6f 1b 6d 20 43 09 20 00 09 00 1b 6d 6d 6d 20   To.m C. ....mmm 
  0030: 2d 09 20 20 20 00 1b 6d 6d e3 e3 e3 e3 e3 20 20   -.   ..mm.....  
Seed 5 (id=007fc926cc3fda81, size=41 bytes, fuzzer=value_profile, trial=1, discovered_at=2290s, mutation_op=WordInterestingMutator,ByteNegMutator):
  0000: d6 08 00 00 4c 37 37 37 37 37 37 37 37 37 37 37   ....L77777777777
  0010: c9 0e 00 00 47 0e 00 00 37 0e 00 00 00 00 ff ff   ....G...7.......
  0020: 01 37 0d ff 10 ff ff f3 0e                        .7.......


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x10                            00(.)x1 bf(.)x1 f1(.)x1 32(2)x1 +6u  PARTIAL
   0x0001  01(.)x10                            08(.)x3 01(.)x1 bf(.)x1 8a(.)x1 +4u  PARTIAL
   0x0002  00(.)x10                            00(.)x6 0e(.)x1 bf(.)x1 8a(.)x1 +1u  PARTIAL
   0x0003  00(.)x10                            00(.)x7 bf(.)x1 8a(.)x1 40(@)x1     PARTIAL
   0x0004  00(.)x10                            00(.)x2 df(.)x1 bf(.)x1 10(.)x1 +5u  PARTIAL
   0x0005  01(.)x10                            00(.)x3 20( )x1 bf(.)x1 06(.)x1 +4u  DIFFER
   0x0006  20( )x10                            00(.)x5 bf(.)x1 e5(.)x1 37(7)x1 +2u  PARTIAL
   0x0007  20( )x10                            00(.)x5 bf(.)x1 01(.)x1 37(7)x1 +2u  DIFFER
   0x0008  20( )x10                            00(.)x3 37(7)x2 bf(.)x1 20( )x1 +3u  PARTIAL
   0x0009  20( )x10                            00(.)x3 bf(.)x1 1c(.)x1 e7(.)x1 +4u  DIFFER
   0x000a  20( )x9 0d(.)x1                     00(.)x5 aa(.)x1 89(.)x1 37(7)x1 +2u  DIFFER
   0x000b  20( )x10                            00(.)x4 13(.)x1 15(.)x1 37(7)x1 +3u  DIFFER
   0x000c  43(C)x10                            00(.)x4 df(.)x1 f1(.)x1 37(7)x1 +3u  DIFFER
   0x000d  4f(O)x10                            00(.)x2 0e(.)x2 20( )x1 08(.)x1 +4u  DIFFER
   0x000e  4c(L)x10                            00(.)x4 3d(=)x1 3b(;)x1 20( )x1 +3u  DIFFER
   0x000f  52(R)x10                            00(.)x4 3d(=)x1 3b(;)x1 20( )x1 +3u  DIFFER
   0x0010  20( )x10                            3d(=)x1 00(.)x1 3b(;)x1 20( )x1 +6u  PARTIAL
   0x0011  ff(.)x9 06(.)x1                     3d(=)x1 00(.)x1 06(.)x1 20( )x1 +6u  PARTIAL
   0x0012  1f(.)x10                            00(.)x3 3d(=)x1 20( )x1 97(.)x1 +4u  DIFFER
   0x0013  20( )x10                            00(.)x2 3d(=)x1 64(d)x1 20( )x1 +5u  PARTIAL
   0x0014  00(.)x10                            3d(=)x1 73(s)x1 37(7)x1 20( )x1 +6u  DIFFER
   0x0015  00(.)x10                            20( )x2 3d(=)x1 64(d)x1 1c(.)x1 +5u  DIFFER
   0x0016  00(.)x10                            00(.)x3 20( )x2 3d(=)x1 76(v)x1 +3u  PARTIAL
   0x0017  18(.)x10                            00(.)x4 20( )x2 3d(=)x1 97(.)x1 +2u  DIFFER
   0x0018  00(.)x10                            20( )x2 3d(=)x1 bf(.)x1 4c(L)x1 +5u  PARTIAL
   0x0019  01(.)x10                            0e(.)x2 3d(=)x1 bf(.)x1 9f(.)x1 +5u  DIFFER
   0x001a  00(.)x10                            00(.)x4 3d(=)x1 bf(.)x1 9f(.)x1 +3u  PARTIAL
   0x001b  00(.)x10                            00(.)x3 20( )x2 3d(=)x1 b4(.)x1 +3u  PARTIAL
   0x001c  01(.)x6 64(d)x4                     00(.)x3 3d(=)x1 4c(L)x1 20( )x1 +4u  DIFFER
   0x001d  ee(.)x6 73(s)x4                     00(.)x3 3d(=)x1 10(.)x1 06(.)x1 +4u  DIFFER
   0x001e  7f(.)x6 64(d)x4                     00(.)x3 ff(.)x2 cb(.)x1 80(.)x1 +3u  DIFFER
   0x001f  0a(.)x6 76(v)x4                     00(.)x3 ff(.)x2 0e(.)x1 54(T)x1 +3u  DIFFER
   0x0020  00(.)x10                            01(.)x2 00(.)x2 df(.)x1 10(.)x1 +4u  PARTIAL
   0x0021  00(.)x10                            00(.)x3 0e(.)x2 20( )x1 6f(o)x1 +3u  PARTIAL
   0x0022  00(.)x10                            00(.)x3 b4(.)x1 1b(.)x1 0d(.)x1 +4u  PARTIAL
   0x0023  02(.)x6 21(!)x4                     00(.)x4 6d(m)x1 ff(.)x1 4c(L)x1 +3u  DIFFER
   0x0024  00(.)x10                            00(.)x2 4c(L)x1 20( )x1 10(.)x1 +5u  PARTIAL
   0x0025  00(.)x6 01(.)x2 2d(-)x1 03(.)x1     00(.)x1 b4(.)x1 9f(.)x1 43(C)x1 +6u  PARTIAL
   0x0026  00(.)x10                            00(.)x1 0e(.)x1 9f(.)x1 09(.)x1 +6u  PARTIAL
   0x0027  00(.)x10                            20( )x2 00(.)x2 9f(.)x1 f3(.)x1 +4u  PARTIAL
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
  prompts_b/harfbuzz_5671.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5671,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5671 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5671 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5671 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).