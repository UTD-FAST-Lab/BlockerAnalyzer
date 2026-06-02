==== BLOCKER ====
Target: harfbuzz
Branch ID: 5311
Location: /src/harfbuzz/src/hb-buffer.cc:633:25
Enclosing function: hb_buffer_t::delete_glyphs_inplace(bool (*)(hb_glyph_info_t const*))
Source line: 	  for (unsigned k = j; k && info[k - 1].cluster == old_cluster; k--)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           2        8          0  loser (I2S vs naive); loser (grimoire_structural vs grimoire)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             3        7          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         9        1          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=1.30h  loser=18.10h
  avg hitcount on branch: winner=24  loser=1
  prob_div=0.80  dur_div=16.80h  hit_div=24
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 20  (grimoire vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=6.10h  loser=18.10h
  avg hitcount on branch: winner=2  loser=1
  prob_div=0.70  dur_div=12.00h  hit_div=2
  subject-level: delta_AUC=45443160.0  p_AUC=0.001  delta_Final=636.4  p_final=0.0006

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5311/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb_buffer_t::delete_glyphs_inplace(bool (*)(hb_glyph_info_t const*)) (/src/harfbuzz/src/hb-buffer.cc:610-653) ---
[ ]   608  void
[ ]   609  hb_buffer_t::delete_glyphs_inplace (bool (*filter) (const hb_glyph_info_t *info))
[B]   610  {
[ ]   611    /* Merge clusters and delete filtered glyphs.
[ ]   612     * NOTE! We can't use out-buffer as we have positioning data. */
[B]   613    unsigned int j = 0;
[B]   614    unsigned int count = len;
[B]   615    for (unsigned int i = 0; i < count; i++)
[B]   616    {
[B]   617      if (filter (&info[i]))
[B]   618      {
[ ]   619        /* Merge clusters.
[ ]   620         * Same logic as delete_glyph(), but for in-place removal. */
[ ]   621  
[B]   622        unsigned int cluster = info[i].cluster;
[B]   623        if (i + 1 < count && cluster == info[i + 1].cluster)
[W]   624  	continue; /* Cluster survives; do nothing. */
[ ]   625  
[B]   626        if (j)
[B]   627        {
[ ]   628  	/* Merge cluster backward. */
[B]   629  	if (cluster < info[j - 1].cluster)
[B]   630  	{
[B]   631  	  unsigned int mask = info[i].mask;
[B]   632  	  unsigned int old_cluster = info[j - 1].cluster;
[B]   633  	  for (unsigned k = j; k && info[k - 1].cluster == old_cluster; k--) <-- BLOCKER
[B]   634  	    set_cluster (info[k - 1], cluster, mask);
[B]   635  	}
[B]   636  	continue;
[B]   637        }
[ ]   638  
[ ]   639        if (i + 1 < count)
[ ]   640  	merge_clusters (i, i + 2); /* Merge cluster forward. */
[ ]   641  
[ ]   642        continue;
[B]   643      }
[ ]   644  
[B]   645      if (j != i)
[B]   646      {
[B]   647        info[j] = info[i];
[B]   648        pos[j] = pos[i];
[B]   649      }
[B]   650      j++;
[B]   651    }
[B]   652    len = j;
[B]   653  }

--- Caller (1 hop): hb-ot-shape.cc:hb_ot_hide_default_ignorables(hb_buffer_t*, hb_font_t*) (/src/harfbuzz/src/hb-ot-shape.cc:818-839, calls hb_buffer_t::delete_glyphs_inplace(bool (*)(hb_glyph_info_t const*)) at line 838) (full body — short) ---
[B]   818  {
[B]   819    if (!(buffer->scratch_flags & HB_BUFFER_SCRATCH_FLAG_HAS_DEFAULT_IGNORABLES) ||
[B]   820        (buffer->flags & HB_BUFFER_FLAG_PRESERVE_DEFAULT_IGNORABLES))
[B]   821      return;
[ ]   822  
[B]   823    unsigned int count = buffer->len;
[B]   824    hb_glyph_info_t *info = buffer->info;
[ ]   825  
[B]   826    hb_codepoint_t invisible = buffer->invisible;
[B]   827    if (!(buffer->flags & HB_BUFFER_FLAG_REMOVE_DEFAULT_IGNORABLES) &&
[B]   828        (invisible || font->get_nominal_glyph (' ', &invisible)))
[ ]   829    {
[ ]   830      /* Replace default-ignorables with a zero-advance invisible glyph. */
[ ]   831      for (unsigned int i = 0; i < count; i++)
[ ]   832      {
[ ]   833        if (_hb_glyph_info_is_default_ignorable (&info[i]))
[ ]   834  	info[i].codepoint = invisible;
[ ]   835      }
[ ]   836    }
[B]   837    else
[B]   838      buffer->delete_glyphs_inplace (_hb_glyph_info_is_default_ignorable); <-- CALL
[B]   839  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb_aat_layout_remove_deleted_glyphs(hb_buffer_t*)  (/src/harfbuzz/src/hb-aat-layout.cc:299-301, calls hb_buffer_t::delete_glyphs_inplace(bool (*)(hb_glyph_info_t const*)) at line 300)
hop 2  hb-ot-shape.cc:hb_ot_hide_default_ignorables(hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:818-839, calls hb_buffer_t::delete_glyphs_inplace(bool (*)(hb_glyph_info_t const*)) at line 838)
hop 3  hb_buffer_t::delete_glyph()  (/src/harfbuzz/src/hb-buffer.cc:573-606, calls hb-ot-shape.cc:hb_ot_hide_default_ignorables(hb_buffer_t*, hb_font_t*) at line 574)
hop 3  hb-ot-shape.cc:hb_ot_substitute_post(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:938-951, calls hb_aat_layout_remove_deleted_glyphs(hb_buffer_t*) at line 941)
hop 3  hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:923-934, calls hb_aat_layout_remove_deleted_glyphs(hb_buffer_t*) at line 932)
hop 4  OT::Layout::GSUB_impl::Sequence<OT::Layout::SmallTypes>::apply(OT::hb_ot_apply_context_t*) const  (/src/harfbuzz/src/OT/Layout/GSUB/Sequence.hh:35-130, calls hb_buffer_t::delete_glyph() at line 74)
hop 4  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195, calls hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*) at line 1184)
hop 5  AAT::Chain<AAT::ExtendedTypes>::apply(AAT::hb_aat_apply_context_t*) const  (/src/harfbuzz/src/hb-aat-layout-morx-table.hh:1017-1085, calls OT::Layout::GSUB_impl::Sequence<OT::Layout::SmallTypes>::apply(OT::hb_ot_apply_context_t*) const at line 1072)
hop 5  AAT::mortmorx<AAT::ExtendedTypes, 1836020344u>::apply(AAT::hb_aat_apply_context_t*, hb_aat_map_t const&) const  (/src/harfbuzz/src/hb-aat-layout-morx-table.hh:1156-1171, calls OT::Layout::GSUB_impl::Sequence<OT::Layout::SmallTypes>::apply(OT::hb_ot_apply_context_t*) const at line 1167)
hop 5  _hb_ot_shape  (/src/harfbuzz/src/hb-ot-shape.cc:1204-1209, calls hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*) at line 1206)
hop 6  bool AAT::hb_aat_apply_context_t::dispatch<AAT::RearrangementSubtable<AAT::ExtendedTypes> >(AAT::RearrangementSubtable<AAT::ExtendedTypes> const&)  (/src/harfbuzz/src/hb-aat-layout-common.hh:50-50, calls AAT::Chain<AAT::ExtendedTypes>::apply(AAT::hb_aat_apply_context_t*) const at line 50)
hop 7  hb_subset_context_t::return_t OT::AxisValue::dispatch<hb_subset_context_t, hb_array_t<OT::StatAxisRecord const> const&>(hb_subset_context_t*, hb_array_t<OT::StatAxisRecord const> const&) const  (/src/harfbuzz/src/hb-ot-stat-table.hh:392-402, calls bool AAT::hb_aat_apply_context_t::dispatch<AAT::RearrangementSubtable<AAT::ExtendedTypes> >(AAT::RearrangementSubtable<AAT::ExtendedTypes> const&) at line 396)
hop 8  hb_sanitize_context_t::return_t AAT::ChainSubtable<AAT::ExtendedTypes>::dispatch<hb_sanitize_context_t>(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-aat-layout-morx-table.hh:924-935, calls hb_subset_context_t::return_t OT::AxisValue::dispatch<hb_subset_context_t, hb_array_t<OT::StatAxisRecord const> const&>(hb_subset_context_t*, hb_array_t<OT::StatAxisRecord const> const&) const at line 928)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      42         6  hb_buffer_t::merge_clusters_impl(unsigned int, unsigned int)  (/src/harfbuzz/src/hb-buffer.cc:512-539)
      29         7  hb-ot-shape.cc:zero_mark_width(hb_glyph_position_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:967-970)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=4  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195) ---
  d=4   L1177  T=9 F=390  T=3 F=188  if (c->plan->shaper->preprocess_text &&
  d=4   L1178  T=9 F=0  T=3 F=0  c->buffer->message(c->font, "start preprocess-text"))
--- d=3  hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:923-934) ---
  d=3   L 931  T=0 F=399  T=0 F=191  if (c->plan->apply_morx && c->plan->apply_gpos)
--- d=3  hb-ot-shape.cc:hb_ot_substitute_post(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:938-951) ---
  d=3   L 940  T=0 F=399  T=0 F=191  if (c->plan->apply_morx && !c->plan->apply_gpos)
  d=3   L 946  T=9 F=390  T=7 F=184  if (c->plan->shaper->postprocess_glyphs &&
--- d=2  hb-ot-shape.cc:hb_ot_hide_default_ignorables(hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:818-839) ---
  d=2   L 819  T=380 F=19  T=181 F=10  if (!(buffer->scratch_flags & HB_BUFFER_SCRATCH_FLAG_HAS_...
--- d=1  hb_buffer_t::delete_glyphs_inplace(bool (*)(hb_glyph_info_t const*))  (/src/harfbuzz/src/hb-buffer.cc:610-653) ---
  d=1   L 623  T=37 F=1  T=12 F=3  if (i + 1 < count && cluster == info[i + 1].cluster)
  d=1   L 623  T=5 F=32  T=0 F=12  if (i + 1 < count && cluster == info[i + 1].cluster)
  d=1   L 626  T=33 F=0  T=15 F=0  if (j)
  d=1   L 629  T=32 F=1  T=15 F=0  if (cluster < info[j - 1].cluster)
  d=1   L 633  T=54 F=22  T=30 F=0  for (unsigned k = j; k && info[k - 1].cluster == old_clus...  <-- BLOCKER

[off-chain: 104 additional divergent branches across 25 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=493bf2b6bc0e7866, size=101 bytes, fuzzer=naive, trial=1, discovered_at=25s, mutation_op=DwordAddMutator,CrossoverReplaceMutator,ByteIncMutator,QwordAddMutator,BytesInsertMutator,CrossoverInsertMutator,DwordInterestingMutator):
  0000: 73 70 20 20 20 00 01 65 72 91 00 10 00 00 97 97   sp   ..er.......
  0010: 97 97 97 97 7f 20 21 64 66 6c 7f 7f 7f 7f 7f 7f   ..... !dfl......
  0020: 20 20 00 00 00 dc dc dc dc dc dc dc dc dc dc db     ..............
  0030: dc 94 00 ff ff ff 3f ff 20 62 62 62 62 62 00 01   ......?. bbbbb..
Seed 2 (id=5a63c2b460e95e57, size=60 bytes, fuzzer=naive, trial=1, discovered_at=25s, mutation_op=BytesRandSetMutator,ByteInterestingMutator,BytesDeleteMutator,DwordInterestingMutator,TokenReplace,WordAddMutator):
  0000: 72 70 20 f8 f8 6b 9a 72 00 20 1f 00 00 00 00 2d   rp ..k.r. .....-
  0010: 00 1b 00 20 00 06 00 00 3f e3 61 6b 91 4f 6e 6e   ... ....?.ak.Onn
  0020: 7e 6e 55 55 55 05 01 64 ff ff 20 00 9b 9b 9b 00   ~nUUU..d.. .....
  0030: 00 00 2d 68 61 6b 6e 6e 6e 20 00 00               ..-haknnn ..
Seed 3 (id=a732bc5997fb5a04, size=1818 bytes, fuzzer=grimoire, trial=1, discovered_at=142s):
  0000: 74 79 70 31 00 01 20 20 20 20 20 20 66 65 61 74   typ1..      feat
  0010: 73 6e 2d 68 61 6e 73 00 00 01 00 ff e9 00 20 20   sn-hans.......  
  0020: 20 20 20 20 6b 9b 8e 6e ff ff 00 00 4b e9 01 00       k..n....K...
  0030: 73 6e 2d 68 61 6e 74 2d 68 6c 6b 00 4a e8 01 00   sn-hant-hlk.J...
Seed 4 (id=93d6c0dbe8c165e1, size=68 bytes, fuzzer=naive, trial=1, discovered_at=397s, mutation_op=ByteDecMutator,ByteDecMutator,BytesDeleteMutator,BytesSwapMutator,QwordAddMutator,BitFlipMutator,WordInterestingMutator):
  0000: 00 00 de 1d 00 00 6f 74 4b e9 01 00 0e 20 00 00   ......otK.... ..
  0010: 16 00 00 00 01 00 00 00 00 00 00 20 24 20 20 96   ........... $  .
  0020: ff ff ef 20 20 20 20 3a 20 20 20 20 20 20 20 20   ...    :        
  0030: 20 20 de 1d 80 00 6f 74 4b e9 01 00 0e 20 00 00     ....otK.... ..
Seed 5 (id=d1a4223a832b8446, size=468 bytes, fuzzer=grimoire, trial=1, discovered_at=454s):
  0000: 64 6f 2d 00 24 49 92 04 64 61 72 66 68 64 73 63   do-.$I..darfhdsc
  0010: 70 67 6c 68 08 20 74 6c 66 64 1e fa 02 00 00 01   pglh. tlfd......
  0020: 00 00 00 01 20 20 20 20 26 ff 00 ea aa ea ea ea   ....    &.......
  0030: ea ea 76 64 73 63 00 01 00 00 06 01 20 20 20 20   ..vdsc......    

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=697875d93546513f, size=46 bytes, fuzzer=cmplog, trial=1, discovered_at=140s, mutation_op=BytesExpandMutator,BytesInsertMutator,ByteIncMutator):
  0000: 20 6b 65 72 6e 20 20 20 14 06 00 00 00 10 00 00    kern   ........
  0010: 6e 20 65 72 6e 20 20 20 14 06 00 00 00 10 00 00   n ern   ........
  0020: 6f 20 00 00 00 00 20 06 20 35 06 06 06 06         o .... . 5....
Seed 2 (id=54315642c5fbfa8d, size=18 bytes, fuzzer=cmplog, trial=1, discovered_at=163s, mutation_op=BitFlipMutator,ByteNegMutator,ByteInterestingMutator,TokenInsert,BytesSetMutator,BitFlipMutator):
  0000: 64 05 30 12 01 00 01 01 00 0d 01 00 64 20 00 00   d.0.........d ..
  0010: e1 a0                                             ..
Seed 3 (id=47d596c46acd1320, size=22 bytes, fuzzer=cmplog, trial=1, discovered_at=166s, mutation_op=ByteInterestingMutator,BytesDeleteMutator,BytesInsertCopyMutator,BytesDeleteMutator):
  0000: 20 00 7f a3 00 00 e9 20 00 20 00 00 00 e9 01 00    ...... . ......
  0010: 01 0b 4b 20 6e 20                                 ..K n 
Seed 4 (id=6296a3860590d0df, size=27 bytes, fuzzer=cmplog, trial=1, discovered_at=170s, mutation_op=BytesSetMutator,ByteFlipMutator,BytesRandSetMutator,TokenReplace,ByteRandMutator):
  0000: 0f 20 00 00 01 0d 01 00 0f 20 00 00 4b e9 01 00   . ....... ..K...
  0010: 66 20 20 f6 ae 10 00 20 20 20 20                  f  ....    
Seed 5 (id=58c5af3d5e070c14, size=26 bytes, fuzzer=cmplog, trial=1, discovered_at=220s, mutation_op=CrossoverReplaceMutator,BitFlipMutator,BytesDeleteMutator,BytesCopyMutator,ByteDecMutator,BytesCopyMutator,TokenReplace):
  0000: 6b 20 00 00 6b 20 00 00 01 10 ff ff ff 03 00 ff   k ..k ..........
  0010: 00 01 7f 12 00 20 00 00 14 07                     ..... ....


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x000e  00(.)x4 4f(O)x4 61(a)x3 97(.)x1 +7u  00(.)x5 01(.)x2 4d(M)x2 ae(.)x1     PARTIAL
   0x0016  00(.)x8 21(!)x1 73(s)x1 74(t)x1 +8u  00(.)x6 20( )x1 0d(.)x1             PARTIAL
   0x0017  00(.)x5 ff(.)x4 10(.)x2 64(d)x1 +7u  00(.)x6 20( )x2                     PARTIAL
   0x001a  00(.)x5 6f(o)x4 20( )x2 55(U)x2 +6u  00(.)x4 6e(n)x2 20( )x1             PARTIAL
   0x001b  00(.)x5 6d(m)x4 20( )x3 7f(.)x1 +6u  00(.)x3 20( )x1 2d(-)x1 02(.)x1     PARTIAL
   0x001f  00(.)x6 72(r)x4 7f(.)x1 6e(n)x1 +7u  00(.)x3 6e(n)x1 74(t)x1 3a(:)x1     PARTIAL
   0x0022  00(.)x6 fe(.)x3 55(U)x1 20( )x1 +8u  00(.)x3 20( )x1 01(.)x1 6f(o)x1     PARTIAL
   0x0023  00(.)x7 ff(.)x3 20( )x2 55(U)x1 +6u  00(.)x4 20( )x1 0d(.)x1             PARTIAL
   0x0025  00(.)x5 20( )x3 ff(.)x3 dc(.)x1 +7u  00(.)x4 6e(n)x1 06(.)x1             PARTIAL
   0x0026  00(.)x7 20( )x2 b2(.)x2 dc(.)x1 +7u  20( )x2 00(.)x2 1a(.)x1 80(.)x1     PARTIAL
   0x0027  00(.)x4 03(.)x4 20( )x2 05(.)x2 +7u  00(.)x4 06(.)x1 20( )x1             PARTIAL
   0x0028  00(.)x8 ff(.)x2 20( )x2 02(.)x2 +5u  00(.)x3 20( )x1 35(5)x1 04(.)x1     PARTIAL
   0x002a  20( )x6 00(.)x4 dc(.)x1 6b(k)x1 +7u  00(.)x4 06(.)x1 ff(.)x1             PARTIAL
   0x002d  61(a)x4 00(.)x3 20( )x2 dc(.)x1 +9u  02(.)x2 06(.)x1 00(.)x1 20( )x1     PARTIAL
   0x002e  72(r)x5 00(.)x2 dc(.)x1 9b(.)x1 +10u  00(.)x2 f3(.)x1 15(.)x1             PARTIAL
   0x002f  00(.)x4 66(f)x4 20( )x2 db(.)x1 +8u  00(.)x2 6e(n)x1 1f(.)x1             PARTIAL
   0x0030  6a(j)x4 00(.)x3 20( )x2 dc(.)x1 +9u  20( )x2 1f(.)x1 00(.)x1             PARTIAL
   0x0031  79(y)x4 00(.)x3 20( )x3 94(.)x1 +8u  20( )x2 00(.)x1 f7(.)x1             PARTIAL
   0x0032  2d(-)x6 00(.)x2 20( )x2 01(.)x2 +7u  00(.)x1 02(.)x1 6b(k)x1 ff(.)x1     PARTIAL
   0x0033  68(h)x6 00(.)x3 20( )x3 bf(.)x2 +5u  6e(n)x1 00(.)x1 65(e)x1 ff(.)x1     PARTIAL
   0x0034  61(a)x6 20( )x2 4e(N)x2 ff(.)x1 +8u  20( )x2 72(r)x1 ff(.)x1             PARTIAL
   0x0035  6e(n)x5 00(.)x2 20( )x2 ff(.)x1 +9u  00(.)x1 02(.)x1 9c(.)x1 a8(.)x1     PARTIAL
   0x0036  74(t)x5 00(.)x5 3f(?)x1 6e(n)x1 +7u  00(.)x3 03(.)x1                     PARTIAL
   0x0037  00(.)x6 2d(-)x5 ff(.)x1 6e(n)x1 +6u  6e(n)x1 20( )x1 00(.)x1             PARTIAL
   0x0038  68(h)x5 00(.)x2 20( )x1 6e(n)x1 +10u  20( )x1 0f(.)x1 00(.)x1             PARTIAL
   0x0039  6b(k)x4 20( )x3 00(.)x3 62(b)x1 +8u  00(.)x2 0f(.)x1                     PARTIAL
   0x003a  00(.)x9 01(.)x2 61(a)x2 62(b)x1 +5u  00(.)x1 0f(.)x1 fb(.)x1             PARTIAL
   0x003b  00(.)x6 61(a)x4 ff(.)x2 62(b)x1 +5u  00(.)x1 0f(.)x1 ff(.)x1             PARTIAL
   0x003c  6b(k)x4 00(.)x3 62(b)x1 4a(J)x1 +8u  00(.)x1 ff(.)x1                     PARTIAL
   0x003d  2d(-)x4 00(.)x3 20( )x2 62(b)x1 +7u  00(.)x1 a8(.)x1                     PARTIAL
   0x003e  00(.)x9 01(.)x2 20( )x2 5e(^)x1 +3u  6e(n)x1 00(.)x1                     PARTIAL
   0x003f  00(.)x4 80(.)x4 20( )x3 01(.)x1 +5u  20( )x1 00(.)x1                     PARTIAL
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

--- grimoire ---
**Baseline relationship**: grimoire builds on the full cmplog stack —
it includes the `CmpLogObserver`, the `TracingStage`, and the
`I2SRandReplace` (i2s) stage — and ADDS a `GeneralizationStage` plus
Grimoire structural mutators. The single-technique delta is therefore
`grimoire` vs `cmplog` (both have I2S; grimoire adds generalization +
Grimoire mutators), not vs naive.

**Instrumentation**: cmplog's edge counters + per-execution CMP buffer
(`CmpLogObserver`).

**Feedback**: edge-bucket `MaxMapFeedback`.

**Mutators / stages**: stages are
`[generalization, tracing, i2s, havoc, grimoire]`. `GeneralizationStage`
replaces concrete byte runs in a corpus entry with `<GAP>` placeholders
(a generalised input) by repeatedly re-executing and checking that
coverage is preserved. The Grimoire mutators —
`GrimoireExtensionMutator`, `GrimoireRecursiveReplacementMutator`,
`GrimoireStringReplacementMutator`, `GrimoireRandomDeleteMutator` —
splice and recurse on these generalised token/gap structures
(string-based, grammar-free structural mutation). `I2SRandReplace` (the
cmplog i2s stage) also runs.

**Observed `mutation_op` in seed metadata**: all grimoire stages (i2s,
havoc, grimoire) are wrapped in `LineageMutatorWrap` with **no
per-operator name list**, so grimoire seeds appear nameless in lineage
(`mutation_op = -`). As with mopt, nameless rows are NOT an
I2S-exclusive signal here — and grimoire genuinely runs I2S too, so the
two are not separable from lineage names.

**Per-execution cost**: cmplog's per-CMP cost, plus extra executions
during generalization (each candidate gap is validated by a re-run).

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
  prompts_b/harfbuzz_5311.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5311,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S), grimoire>cmplog (grimoire_structural)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5311 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5311 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5311 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).