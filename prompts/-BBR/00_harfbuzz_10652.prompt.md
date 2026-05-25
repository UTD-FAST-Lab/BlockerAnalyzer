==== BLOCKER ====
Target: harfbuzz
Branch ID: 10652
Location: /src/harfbuzz/src/hb-ot-cff2-table.hh:411:11
Enclosing function: OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*)
Source line:       if (cff2 == &Null (OT::cff2))
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            ?        ?          ?  REFERENCE
cmplog                           0       10          0  loser (value_profile vs value_profile_cmplog)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (value_profile vs cmplog); winner (I2S vs value_profile)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 19  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=6.80h  loser=12.00h
  avg hitcount on branch: winner=5  loser=0
  prob_div=1.00  dur_div=5.20h  hit_div=5
  subject-level: delta_AUC=4469430.0  p_AUC=0.0046  delta_Final=760.0  p_final=0.0008
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 20  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=6.80h  loser=12.00h
  avg hitcount on branch: winner=5  loser=0
  prob_div=1.00  dur_div=5.20h  hit_div=5
  subject-level: delta_AUC=12333210.0  p_AUC=0.0002  delta_Final=1452.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/10652/{W,L}/branch_coverage_show.txt

--- Enclosing function: OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*) (/src/harfbuzz/src/hb-ot-cff2-table.hh:398-475) ---
[ ]   396    {
[ ]   397      accelerator_templ_t (hb_face_t *face)
[B]   398      {
[B]   399        topDict.init ();
[B]   400        fontDicts.init ();
[B]   401        privateDicts.init ();
[ ]   402  
[B]   403        this->blob = sc.reference_table<cff2> (face);
[ ]   404  
[ ]   405        /* setup for run-time santization */
[B]   406        sc.init (this->blob);
[B]   407        sc.start_processing ();
[ ]   408  
[B]   409        const OT::cff2 *cff2 = this->blob->template as<OT::cff2> ();
[ ]   410  
[B]   411        if (cff2 == &Null (OT::cff2)) <-- BLOCKER
[L]   412          goto fail;
[ ]   413  
[W]   414        { /* parse top dict */
[W]   415  	hb_ubytes_t topDictStr = (cff2 + cff2->topDict).as_ubytes (cff2->topDictSize);
[W]   416  	if (unlikely (!topDictStr.sanitize (&sc))) goto fail;
[W]   417  	num_interp_env_t env (topDictStr);
[W]   418  	cff2_top_dict_interpreter_t top_interp (env);
[W]   419  	topDict.init ();
[W]   420  	if (unlikely (!top_interp.interpret (topDict))) goto fail;
[W]   421        }
[ ]   422  
[W]   423        globalSubrs = &StructAtOffset<CFF2Subrs> (cff2, cff2->topDict + cff2->topDictSize);
[W]   424        varStore = &StructAtOffsetOrNull<CFF2VariationStore> (cff2, topDict.vstoreOffset);
[W]   425        charStrings = &StructAtOffsetOrNull<CFF2CharStrings> (cff2, topDict.charStringsOffset);
[W]   426        fdArray = &StructAtOffsetOrNull<CFF2FDArray> (cff2, topDict.FDArrayOffset);
[W]   427        fdSelect = &StructAtOffsetOrNull<CFF2FDSelect> (cff2, topDict.FDSelectOffset);
[ ]   428  
[W]   429        if (((varStore != &Null (CFF2VariationStore)) && unlikely (!varStore->sanitize (&sc))) ||
[W]   430  	  (charStrings == &Null (CFF2CharStrings)) || unlikely (!charStrings->sanitize (&sc)) ||
[W]   431  	  (globalSubrs == &Null (CFF2Subrs)) || unlikely (!globalSubrs->sanitize (&sc)) ||
[W]   432  	  (fdArray == &Null (CFF2FDArray)) || unlikely (!fdArray->sanitize (&sc)) ||
[W]   433  	  (((fdSelect != &Null (CFF2FDSelect)) && unlikely (!fdSelect->sanitize (&sc, fdArray->count)))))
[W]   434          goto fail;
[ ]   435  
[ ]   436        num_glyphs = charStrings->count;
[ ]   437        if (num_glyphs != sc.get_num_glyphs ())
[ ]   438          goto fail;
[ ]   439  
[ ]   440        fdCount = fdArray->count;
[ ]   441        if (!privateDicts.resize (fdCount))
[ ]   442          goto fail;
[ ]   443  
[ ]   444        /* parse font dicts and gather private dicts */
[ ]   445        for (unsigned int i = 0; i < fdCount; i++)
[ ]   446        {
[ ]   447  	const hb_ubytes_t fontDictStr = (*fdArray)[i];
[ ]   448  	if (unlikely (!fontDictStr.sanitize (&sc))) goto fail;
[ ]   449  	cff2_font_dict_values_t  *font;
[ ]   450  	num_interp_env_t env (fontDictStr);
[ ]   451  	cff2_font_dict_interpreter_t font_interp (env);
[ ]   452  	font = fontDicts.push ();
[ ]   453  	if (unlikely (font == &Crap (cff2_font_dict_values_t))) goto fail;
[ ]   454  	font->init ();
[ ]   455  	if (unlikely (!font_interp.interpret (*font))) goto fail;
[ ]   456  
[ ]   457  	const hb_ubytes_t privDictStr = StructAtOffsetOrNull<UnsizedByteStr> (cff2, font->privateDictInfo.offset).as_ubytes (font->privateDictInfo.size);
[ ]   458  	if (unlikely (!privDictStr.sanitize (&sc))) goto fail;
[ ]   459  	cff2_priv_dict_interp_env_t env2 (privDictStr);
[ ]   460  	dict_interpreter_t<PRIVOPSET, PRIVDICTVAL, cff2_priv_dict_interp_env_t> priv_interp (env2);
[ ]   461  	privateDicts[i].init ();
[ ]   462  	if (unlikely (!priv_interp.interpret (privateDicts[i]))) goto fail;
[ ]   463  
[ ]   464  	privateDicts[i].localSubrs = &StructAtOffsetOrNull<CFF2Subrs> (&privDictStr[0], privateDicts[i].subrsOffset);
[ ]   465  	if (privateDicts[i].localSubrs != &Null (CFF2Subrs) &&
[ ]   466  	  unlikely (!privateDicts[i].localSubrs->sanitize (&sc)))
[ ]   467  	  goto fail;
[ ]   468        }
[ ]   469  
[ ]   470  
[ ]   471        return;
[ ]   472  
[B]   473        fail:
[B]   474          _fini ();
[B]   475      }

--- Caller (1 hop): OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::~accelerator_templ_t() (/src/harfbuzz/src/hb-ot-cff2-table.hh:476-476, calls OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*) at line 476) (full body — short) ---
[B]   476      ~accelerator_templ_t () { _fini (); } <-- CALL

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  OT::cff2::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:515-515, calls OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*) at line 515)
hop 2  OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::~accelerator_templ_t()  (/src/harfbuzz/src/hb-ot-cff2-table.hh:476-476, calls OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*) at line 476)
hop 3  OT::cff2_accelerator_t::cff2_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:538-538, calls OT::cff2::accelerator_t::accelerator_t(hb_face_t*) at line 538)
hop 3  OT::hmtx_accelerator_t::hmtx_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:449-449, calls OT::cff2::accelerator_t::accelerator_t(hb_face_t*) at line 449)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      10         0  OT::cff2::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-cff2-table.hh:388-392)
       6         0  CFF::cff2_top_dict_opset_t::process_op(unsigned int, CFF::interp_env_t<CFF::number_t>&, CFF::cff2_top_dict_values_t&)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:157-186)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:398-475) ---
  d=1   L 411  T=0 F=10  T=9 F=0  if (cff2 == &Null (OT::cff2))  <-- BLOCKER
  d=1   L 429  T=0 F=1  T=0 F=0  if (((varStore != &Null (CFF2VariationStore)) && unlikely...
  d=1   L 430  T=1 F=0  T=0 F=0  (charStrings == &Null (CFF2CharStrings)) || unlikely (!ch...

[off-chain: 5 additional divergent branches across 1 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=772f3a6f0978eae1, size=163 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=759s, mutation_op=QwordAddMutator,BytesInsertCopyMutator,ByteNegMutator,CrossoverReplaceMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 43 46 46 32   ......      CFF2
  0010: 20 20 20 20 00 00 00 1a 01 00 02 0c 00 02 00 10       ............
  0020: 00 00 00 20 20 20 20 00 00 00 20 09 20 20 20 20   ...    ... .    
  0030: 00 13 00 20 20 20 20 04 73 70 73 70 2d 68 61 6e   ...    .spsp-han
Seed 2 (id=0e5715354a8b7547, size=181 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=858s, mutation_op=BytesRandInsertMutator,ByteInterestingMutator,BytesCopyMutator,DwordInterestingMutator,ByteRandMutator,BytesExpandMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 43 46 46 32   ......      CFF2
  0010: 20 20 20 20 00 00 00 1a 01 00 02 0c 00 02 00 10       ............
  0020: 00 00 00 20 20 20 20 00 00 00 20 09 20 20 20 20   ...    ... .    
  0030: 00 13 00 20 20 20 20 20 20 20 04 73 70 73 70 2d   ...       .spsp-
Seed 3 (id=1b62d7ce3d875c14, size=170 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=858s, mutation_op=WordAddMutator,ByteInterestingMutator,BytesExpandMutator,ByteFlipMutator,TokenInsert,ByteInterestingMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 43 46 46 32   ......      CFF2
  0010: 20 20 20 20 00 00 00 1a 01 00 02 0c 00 02 00 10       ............
  0020: 00 00 00 20 20 20 20 00 00 00 20 09 20 20 20 20   ...    ... .    
  0030: 00 13 00 20 20 20 20 04 73 70 73 70 2d 68 61 6e   ...    .spsp-han
Seed 4 (id=4153187d785dab16, size=196 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=944s, mutation_op=BytesDeleteMutator,BytesExpandMutator,BytesExpandMutator,DwordAddMutator,BytesInsertCopyMutator,ByteAddMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 43 46 46 32   ......      CFF2
  0010: 20 20 20 20 00 00 00 1a 01 00 02 0c 03 00 01 10       ............
  0020: 00 00 00 20 00 01 00 00 fe 00 00 02 1f df 17 ff   ... ............
  0030: ff 0a 00 80 00 00 01 20 20 6b 9b 72 6e 20 03 00   .......  k.rn ..
Seed 5 (id=010a4f8b7404ab94, size=96 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1022s, mutation_op=ByteInterestingMutator,BytesSetMutator,BytesDeleteMutator,BytesSetMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 43 46 46 32   ......      CFF2
  0010: 20 20 20 20 00 00 00 1a 01 00 02 0c 04 00 10 10       ............
  0020: 10 10 10 10 10 10 10 2a 24 21 40 ff 44 44 44 20   .......*$!@.DDD 
  0030: 2c 20 20 20 20 20 20 20 20 64 20 20 03 06 64 17   ,        d  ..d.

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=0007f1b8131011ce, size=59 bytes, fuzzer=cmplog, trial=1, discovered_at=17s, mutation_op=BytesDeleteMutator,BytesRandInsertMutator,DwordAddMutator,BytesInsertMutator,BytesInsertCopyMutator):
  0000: 01 00 00 00 00 20 20 20 20 06 00 00 00 00 00 00   .....    .......
  0010: 20 20 20 20 06 00 00 00 20 20 20 60 20 20 6b 65       ....   `  ke
  0020: 72 6e 00 64 20 20 00 00 22 ff ff ff 00 00 01 00   rn.d  ..".......
  0030: 00 20 00 00 00 00 00 00 ff 02 00                  . .........
Seed 2 (id=000805815c50d718, size=52 bytes, fuzzer=cmplog, trial=1, discovered_at=1096s, mutation_op=ByteNegMutator,ByteIncMutator):
  0000: b9 17 00 01 9c 1f 10 0f 10 00 00 00 e0 1c 00 00   ................
  0010: c5 17 17 00 e0 1c 00 00 c5 17 06 00 e0 06 00 00   ................
  0020: ce 20 00 00 e0 1c 00 00 c5 17 02 00 e0 1c 00 00   . ..............
  0030: c4 17 00 00                                       ....
Seed 3 (id=00078a6e395420d4, size=319 bytes, fuzzer=cmplog, trial=1, discovered_at=1789s, mutation_op=BytesRandSetMutator,BytesDeleteMutator,WordAddMutator,BytesExpandMutator,BytesRandInsertMutator):
  0000: 00 01 00 00 00 03 20 00 00 7f 00 20 20 20 56 56   ...... ....   VV
  0010: 41 52 b9 b9 53 53 ff ff fe f2 1a 20 47 53 55 42   AR..SS..... GSUB
  0020: 03 00 03 00 00 00 00 00 ff ff ff ff 00 00 20 20   ..............  
  0030: 00 09 f8 00 00 78 78 78 78 78 78 78 78 78 78 78   .....xxxxxxxxxxx
Seed 4 (id=00039e3b8e4285f5, size=281 bytes, fuzzer=cmplog, trial=1, discovered_at=5631s, mutation_op=ByteAddMutator,DwordAddMutator,WordInterestingMutator,BytesRandInsertMutator,TokenReplace,ByteDecMutator,BytesCopyMutator):
  0000: 00 01 00 00 00 04 20 03 00 7f 00 ff ff ff 03 56   ...... ........V
  0010: 41 51 b9 b9 b9 01 ff ff fe f2 1a 20 47 50 4f 53   AQ......... GPOS
  0020: 00 00 03 20 00 00 00 00 ff ff ff 10 00 00 00 80   ... ............
  0030: 04 00 6d 6e 2d 68 61 6e 74 2d 68 6b 00 78 78 78   ..mn-hant-hk.xxx
Seed 5 (id=00035b3a3e1b7ab0, size=749 bytes, fuzzer=cmplog, trial=1, discovered_at=5939s, mutation_op=CrossoverInsertMutator,ByteAddMutator,ByteNegMutator,ByteFlipMutator):
  0000: 00 01 00 00 00 04 20 06 00 7f 00 20 20 20 56 56   ...... ....   VV
  0010: 41 51 b9 b9 b9 00 ff ff fe f2 1a 20 47 50 4f 53   AQ......... GPOS
  0020: 00 00 03 20 00 00 00 00 20 fe 00 10 00 00 00 00   ... .... .......
  0030: 00 00 00 00 00 78 78 78 78 78 00 00 00 51 51 78   .....xxxxx...QQx


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x10                            00(.)x8 01(.)x1 b9(.)x1             PARTIAL
   0x0001  01(.)x10                            01(.)x8 00(.)x1 17(.)x1             PARTIAL
   0x0003  00(.)x10                            00(.)x9 01(.)x1                     PARTIAL
   0x0004  00(.)x10                            00(.)x9 9c(.)x1                     PARTIAL
   0x0005  01(.)x10                            04(.)x7 20( )x1 1f(.)x1 03(.)x1     DIFFER
   0x0006  20( )x9 16(.)x1                     20( )x6 10(.)x1 1f(.)x1 1b(.)x1 +1u  PARTIAL
   0x0007  20( )x10                            06(.)x3 00(.)x2 03(.)x2 20( )x1 +2u  PARTIAL
   0x0008  20( )x10                            00(.)x8 20( )x1 10(.)x1             PARTIAL
   0x0009  20( )x10                            7f(.)x8 06(.)x1 00(.)x1             DIFFER
   0x000a  20( )x10                            00(.)x10                            DIFFER
   0x000b  20( )x10                            20( )x6 00(.)x2 ff(.)x2             PARTIAL
   0x000c  43(C)x10                            20( )x6 ff(.)x2 00(.)x1 e0(.)x1     DIFFER
   0x000d  46(F)x10                            20( )x6 ff(.)x2 00(.)x1 1c(.)x1     DIFFER
   0x000e  46(F)x10                            56(V)x6 00(.)x2 03(.)x2             DIFFER
   0x000f  32(2)x10                            56(V)x8 00(.)x2                     DIFFER
   0x0010  20( )x10                            41(A)x8 20( )x1 c5(.)x1             PARTIAL
   0x0011  20( )x10                            51(Q)x5 20( )x1 17(.)x1 52(R)x1 +2u  PARTIAL
   0x0012  20( )x10                            b9(.)x7 20( )x1 17(.)x1 5f(_)x1     PARTIAL
   0x0013  20( )x10                            b9(.)x8 20( )x1 00(.)x1             PARTIAL
   0x0014  00(.)x10                            b9(.)x7 06(.)x1 e0(.)x1 53(S)x1     DIFFER
   0x0015  00(.)x10                            00(.)x6 01(.)x2 1c(.)x1 53(S)x1     PARTIAL
   0x0016  00(.)x10                            ff(.)x7 00(.)x2 18(.)x1             PARTIAL
   0x0017  1a(.)x10                            ff(.)x8 00(.)x2                     DIFFER
   0x0018  01(.)x10                            fe(.)x8 20( )x1 c5(.)x1             DIFFER
   0x0019  00(.)x10                            f2(.)x8 20( )x1 17(.)x1             DIFFER
   0x001a  02(.)x10                            1a(.)x8 20( )x1 06(.)x1             DIFFER
   0x001b  0c(.)x10                            20( )x7 60(`)x1 00(.)x1 2b(+)x1     DIFFER
   0x001c  00(.)x4 01(.)x3 04(.)x2 03(.)x1     47(G)x8 20( )x1 e0(.)x1             DIFFER
   0x001d  00(.)x6 02(.)x4                     50(P)x6 53(S)x2 20( )x1 06(.)x1     DIFFER
   0x001e  00(.)x5 10(.)x2 01(.)x1 41(A)x1 +1u  4f(O)x6 55(U)x2 6b(k)x1 00(.)x1     PARTIAL
   0x001f  10(.)x9 1d(.)x1                     53(S)x6 42(B)x2 65(e)x1 00(.)x1     DIFFER
   0x0020  00(.)x7 10(.)x2 20( )x1             00(.)x5 02(.)x2 72(r)x1 ce(.)x1 +1u  PARTIAL
   0x0021  00(.)x7 10(.)x2 64(d)x1             00(.)x7 6e(n)x1 20( )x1 03(.)x1     PARTIAL
   0x0022  00(.)x7 10(.)x2 20( )x1             03(.)x7 00(.)x3                     PARTIAL
   0x0023  20( )x7 10(.)x2 8d(.)x1             20( )x6 00(.)x2 64(d)x1 13(.)x1     PARTIAL
   0x0024  20( )x4 10(.)x2 05(.)x2 00(.)x1 +1u  00(.)x8 20( )x1 e0(.)x1             PARTIAL
   0x0025  20( )x4 10(.)x2 00(.)x2 01(.)x1 +1u  00(.)x8 20( )x1 1c(.)x1             PARTIAL
   0x0026  20( )x4 00(.)x3 10(.)x2 12(.)x1     00(.)x10                            PARTIAL
   0x0027  00(.)x6 2a(*)x2 07(.)x1 35(5)x1     00(.)x10                            PARTIAL
   0x0028  00(.)x3 fe(.)x3 24($)x2 13(.)x1 +1u  ff(.)x6 20( )x2 22(")x1 c5(.)x1     DIFFER
   ... (15 more divergent offsets)
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
rows are exclusive to cmplog and value_profile_cmplog; their
presence in a winning seed's ancestor chain is direct (lower-bound)
evidence of I2S contribution.

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
  prompts/-BBR/00_harfbuzz_10652.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 10652,
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
      // pick EXACTLY ONE of:
      //   "I2SRandReplace"     (cmplog / vpc input-to-state substitution)
      //   "CMP_MAP gradient"   (vp / vpc Hamming/prefix-distance feedback)
      //   "havoc-only"         (lucky havoc byte mutation, no CMP introspection)
      //   "token-replace"      (TokenInsert/TokenReplace dictionary mutations)
      //   "other"              (anything that does not fit the four above)
    "verified_in_lineage": true,
      // pick true or false
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 10652 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 10652 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 10652 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).