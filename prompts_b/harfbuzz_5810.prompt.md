==== BLOCKER ====
Target: harfbuzz
Branch ID: 5810
Location: /src/harfbuzz/src/hb-ot-shaper-indic-machine.hh:531:2
Enclosing function: find_syllables_indic(hb_buffer_t*)
Source line: 	case 19:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           1        9          0  loser (I2S vs naive); loser (grimoire_structural vs grimoire)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             7        3          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         8        2          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=0.80h  loser=22.50h
  avg hitcount on branch: winner=87  loser=0
  prob_div=0.90  dur_div=21.70h  hit_div=87
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 20  (grimoire vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=7.60h  loser=22.50h
  avg hitcount on branch: winner=3  loser=0
  prob_div=0.70  dur_div=14.90h  hit_div=2
  subject-level: delta_AUC=45443160.0  p_AUC=0.001  delta_Final=636.4  p_final=0.0006

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5810/{W,L}/branch_coverage_show.txt

--- Enclosing function: find_syllables_indic(hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shaper-indic-machine.hh:458-623) ---
[ ]   456  inline void
[ ]   457  find_syllables_indic (hb_buffer_t *buffer)
[B]   458  {
[B]   459    unsigned int p, pe, eof, ts, te, act;
[B]   460    int cs;
[B]   461    hb_glyph_info_t *info = buffer->info;
[ ]   462    
[B]   463  #line 453 "hb-ot-shaper-indic-machine.hh"
[B]   464  	{
[B]   465  	cs = indic_syllable_machine_start;
[B]   466  	ts = 0;
[B]   467  	te = 0;
[B]   468  	act = 0;
[B]   469  	}
[ ]   470  
[B]   471  #line 138 "hb-ot-shaper-indic-machine.rl"
[ ]   472  
[ ]   473  
[B]   474    p = 0;
[B]   475    pe = eof = buffer->len;
[ ]   476  
[B]   477    unsigned int syllable_serial = 1;
[ ]   478    
[B]   479  #line 465 "hb-ot-shaper-indic-machine.hh"
[B]   480  	{
[B]   481  	int _slen;
[B]   482  	int _trans;
[B]   483  	const unsigned char *_keys;
[B]   484  	const unsigned char *_inds;
[B]   485  	if ( p == pe )
[ ]   486  		goto _test_eof;
[B]   487  _resume:
[B]   488  	switch ( _indic_syllable_machine_from_state_actions[cs] ) {
[B]   489  	case 10:
[B]   490  #line 1 "NONE"
[B]   491  	{ts = p;}
[B]   492  	break;
[B]   493  #line 477 "hb-ot-shaper-indic-machine.hh"
[B]   494  	}
[ ]   495  
[B]   496  	_keys = _indic_syllable_machine_trans_keys + (cs<<1);
[B]   497  	_inds = _indic_syllable_machine_indicies + _indic_syllable_machine_index_offsets[cs];
[ ]   498  
[B]   499  	_slen = _indic_syllable_machine_key_spans[cs];
[B]   500  	_trans = _inds[ _slen > 0 && _keys[0] <=( info[p].indic_category()) &&
[B]   501  		( info[p].indic_category()) <= _keys[1] ?
[B]   502  		( info[p].indic_category()) - _keys[0] : _slen ];
[ ]   503  
[B]   504  _eof_trans:
[B]   505  	cs = _indic_syllable_machine_trans_targs[_trans];
[ ]   506  
[B]   507  	if ( _indic_syllable_machine_trans_actions[_trans] == 0 )
[B]   508  		goto _again;
[ ]   509  
[B]   510  	switch ( _indic_syllable_machine_trans_actions[_trans] ) {
[B]   511  	case 2:
[B]   512  #line 1 "NONE"
[B]   513  	{te = p+1;}
[B]   514  	break;
[B]   515  	case 11:
[B]   516  #line 114 "hb-ot-shaper-indic-machine.rl"
[B]   517  	{te = p+1;{ found_syllable (indic_non_indic_cluster); }}
[B]   518  	break;
[B]   519  	case 13:
[B]   520  #line 109 "hb-ot-shaper-indic-machine.rl"
[B]   521  	{te = p;p--;{ found_syllable (indic_consonant_syllable); }}
[B]   522  	break;
[W]   523  	case 14:
[W]   524  #line 110 "hb-ot-shaper-indic-machine.rl"
[W]   525  	{te = p;p--;{ found_syllable (indic_vowel_syllable); }}
[W]   526  	break;
[B]   527  	case 17:
[B]   528  #line 111 "hb-ot-shaper-indic-machine.rl"
[B]   529  	{te = p;p--;{ found_syllable (indic_standalone_cluster); }}
[B]   530  	break;
[W]   531  	case 19: <-- BLOCKER
[W]   532  #line 112 "hb-ot-shaper-indic-machine.rl"
[W]   533  	{te = p;p--;{ found_syllable (indic_symbol_cluster); }}
[W]   534  	break;
[B]   535  	case 15:
[B]   536  #line 113 "hb-ot-shaper-indic-machine.rl"
[B]   537  	{te = p;p--;{ found_syllable (indic_broken_cluster); buffer->scratch_flags |= HB_BUFFER_SCRATCH_FLAG_HAS_BROKEN_SYLLABLE; }}
[B]   538  	break;
[W]   539  	case 16:
[W]   540  #line 114 "hb-ot-shaper-indic-machine.rl"
[W]   541  	{te = p;p--;{ found_syllable (indic_non_indic_cluster); }}
[W]   542  	break;
[ ]   543  	case 1:
[ ]   544  #line 109 "hb-ot-shaper-indic-machine.rl"
[ ]   545  	{{p = ((te))-1;}{ found_syllable (indic_consonant_syllable); }}
[ ]   546  	break;
[ ]   547  	case 3:
[ ]   548  #line 110 "hb-ot-shaper-indic-machine.rl"
[ ]   549  	{{p = ((te))-1;}{ found_syllable (indic_vowel_syllable); }}
[ ]   550  	break;
[ ]   551  	case 7:
[ ]   552  #line 111 "hb-ot-shaper-indic-machine.rl"
[ ]   553  	{{p = ((te))-1;}{ found_syllable (indic_standalone_cluster); }}
[ ]   554  	break;
[ ]   555  	case 8:
[ ]   556  #line 112 "hb-ot-shaper-indic-machine.rl"
[ ]   557  	{{p = ((te))-1;}{ found_syllable (indic_symbol_cluster); }}
[ ]   558  	break;
[ ]   559  	case 4:
[ ]   560  #line 113 "hb-ot-shaper-indic-machine.rl"
[ ]   561  	{{p = ((te))-1;}{ found_syllable (indic_broken_cluster); buffer->scratch_flags |= HB_BUFFER_SCRATCH_FLAG_HAS_BROKEN_SYLLABLE; }}
[ ]   562  	break;
[ ]   563  	case 6:
[ ]   564  #line 1 "NONE"
[ ]   565  	{	switch( act ) {
[ ]   566  	case 1:
[ ]   567  	{{p = ((te))-1;} found_syllable (indic_consonant_syllable); }
[ ]   568  	break;
[ ]   569  	case 5:
[ ]   570  	{{p = ((te))-1;} found_syllable (indic_broken_cluster); buffer->scratch_flags |= HB_BUFFER_SCRATCH_FLAG_HAS_BROKEN_SYLLABLE; }
[ ]   571  	break;
[ ]   572  	case 6:
[ ]   573  	{{p = ((te))-1;} found_syllable (indic_non_indic_cluster); }
[ ]   574  	break;
[ ]   575  	}
[ ]   576  	}
[ ]   577  	break;
[ ]   578  	case 18:
[ ]   579  #line 1 "NONE"
[ ]   580  	{te = p+1;}
[ ]   581  #line 109 "hb-ot-shaper-indic-machine.rl"
[ ]   582  	{act = 1;}
[ ]   583  	break;
[B]   584  	case 5:
[B]   585  #line 1 "NONE"
[B]   586  	{te = p+1;}
[B]   587  #line 113 "hb-ot-shaper-indic-machine.rl"
[B]   588  	{act = 5;}
[B]   589  	break;
[W]   590  	case 12:
[W]   591  #line 1 "NONE"
[W]   592  	{te = p+1;}
[W]   593  #line 114 "hb-ot-shaper-indic-machine.rl"
[W]   594  	{act = 6;}
[W]   595  	break;
[B]   596  #line 559 "hb-ot-shaper-indic-machine.hh"
[B]   597  	}
[ ]   598  
[B]   599  _again:
[B]   600  	switch ( _indic_syllable_machine_to_state_actions[cs] ) {
[B]   601  	case 9:
[B]   602  #line 1 "NONE"
[B]   603  	{ts = 0;}
[B]   604  	break;
[B]   605  #line 566 "hb-ot-shaper-indic-machine.hh"
[B]   606  	}
[ ]   607  
[B]   608  	if ( ++p != pe )
[B]   609  		goto _resume;
[B]   610  	_test_eof: {}
[B]   611  	if ( p == eof )
[B]   612  	{
[B]   613  	if ( _indic_syllable_machine_eof_trans[cs] > 0 ) {
[B]   614  		_trans = _indic_syllable_machine_eof_trans[cs] - 1;
[B]   615  		goto _eof_trans;
[B]   616  	}
[B]   617  	}
[ ]   618  
[B]   619  	}
[ ]   620  
[B]   621  #line 146 "hb-ot-shaper-indic-machine.rl"
[ ]   622  
[B]   623  }

--- Caller (1 hop): hb-ot-shaper-indic.cc:setup_syllables_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shaper-indic.cc:420-426, calls find_syllables_indic(hb_buffer_t*) at line 422) (full body — short) ---
[B]   420  {
[B]   421    HB_BUFFER_ALLOCATE_VAR (buffer, syllable);
[B]   422    find_syllables_indic (buffer); <-- CALL
[B]   423    foreach_syllable (buffer, start, end)
[B]   424      buffer->unsafe_to_break (start, end);
[B]   425    return false;
[B]   426  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-indic.cc:setup_syllables_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:420-426, calls find_syllables_indic(hb_buffer_t*) at line 422)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0         1  hb-ot-shaper-indic.cc:is_halant(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:86-88)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  find_syllables_indic(hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic-machine.hh:458-623) ---
  d=1   L 501  T=77 F=31  T=18 F=0  ( info[p].indic_category()) <= _keys[1] ?
  d=1   L 523  T=2 F=236  T=0 F=169  case 14:
  d=1   L 531  T=29 F=209  T=0 F=169  case 19:  <-- BLOCKER
  d=1   L 539  T=5 F=233  T=0 F=169  case 16:
  d=1   L 590  T=5 F=233  T=0 F=169  case 12:

[off-chain: 40 additional divergent branches across 5 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=ce09bb2d97eac25b, size=14 bytes, fuzzer=grimoire, trial=1, discovered_at=827s):
  0000: f2 a8 00 00 00 fe 00 00 00 00 00 01 00 06         ..............
Seed 2 (id=68d1ae222de2c678, size=14 bytes, fuzzer=grimoire, trial=1, discovered_at=1173s):
  0000: f2 a8 00 00 f2 a8 00 00 dc 09 00 00 00 06         ..............
Seed 3 (id=0d2bd6067cf33275, size=32 bytes, fuzzer=naive, trial=1, discovered_at=2173s, mutation_op=DwordAddMutator,BytesInsertCopyMutator,ByteFlipMutator,BytesDeleteMutator):
  0000: f3 a8 00 00 f7 1c 00 00 9f a2 a2 a2 a2 a8 00 00   ................
  0010: f7 1c 00 00 a2 a2 a2 a2 a2 a2 a2 a2 5d a2 a2 a2   ............]...
Seed 4 (id=39a78dfab3b51ba9, size=109 bytes, fuzzer=naive, trial=1, discovered_at=2645s, mutation_op=DwordAddMutator,ByteInterestingMutator,BytesRandSetMutator,QwordAddMutator,TokenReplace,BytesDeleteMutator):
  0000: 01 73 69 7a 01 73 69 7a 65 0f 00 00 7a 6f 2d b5   .siz.size...zo-.
  0010: b0 00 10 00 2d 2d 96 00 ec 72 6e 2d 68 61 6e 73   ....--...rn-hans
  0020: 00 6a 40 0c 00 00 00 fe 00 00 e8 f1 f1 0c 0c 00   .j@.............
  0030: 00 00 0c 00 00 00 00 02 00 01 00 64 65 56 10 00   ...........deV..
Seed 5 (id=27cac4a8a08f303f, size=59 bytes, fuzzer=naive, trial=1, discovered_at=14427s, mutation_op=BytesExpandMutator,QwordAddMutator):
  0000: 35 0c 00 ff cb 0c 80 00 4c 0c 00 00 dc 17 00 00   5.......L.......
  0010: 80 0c 00 00 bd 0c 00 00 80 0c 00 00 bd 0c 00 00   ................
  0020: cb ff 80 00 80 0c 00 05 bd 0c 00 00 cb 0c 0c 00   ................
  0030: 00 34 05 05 45 05 1c 1c 1c 1c 0b                  .4..E......

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0237ec581d21f6c0, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=9s, mutation_op=BytesInsertMutator):
  0000: ff 20 20 20 20 6b 65 72 6e 20 df 10 20 0a 00 00   .    kern .. ...
  0010: 1a 20 00 1a 1a 1a 1a 1a 1a 1a 1a 1a 1a 1a 1a 1a   . ..............
  0020: 1a 1a 00 00 00 00 00 7f 20                        ........ 
Seed 2 (id=007e652bc601c59b, size=38 bytes, fuzzer=cmplog, trial=1, discovered_at=21s, mutation_op=TokenInsert,QwordAddMutator,BytesDeleteMutator):
  0000: df 6b 66 20 72 8b 20 20 20 20 0a 01 8a 00 1a fb   .kf r.    ......
  0010: 00 0d 00 00 ef 01 00 72 6d 75 6e 00 01 0d 00 00   .......rmun.....
  0020: ef 01 00 0f e4 20                                 ..... 
Seed 3 (id=00cc7bf7b8cade2f, size=48 bytes, fuzzer=cmplog, trial=1, discovered_at=289s, mutation_op=ByteAddMutator,TokenReplace,ByteRandMutator):
  0000: ff 22 20 20 20 6b 65 00 00 03 e8 10 20 0a 00 00   ."   ke..... ...
  0010: 6a 64 66 6d 5a 20 00 7f 00 00 d2 00 7f 20 00 00   jdfmZ ....... ..
  0020: 36 00 00 00 36 04 00 00 00 00 00 00 d2 00 6b 20   6...6.........k 
Seed 4 (id=0283ed93d64a4a34, size=39 bytes, fuzzer=cmplog, trial=1, discovered_at=297s, mutation_op=BytesRandSetMutator,BytesExpandMutator,BytesDeleteMutator,CrossoverReplaceMutator):
  0000: 17 00 00 00 00 20 20 00 00 01 20 2c 20 00 00 0c   .....  ... , ...
  0010: 00 0d 00 00 00 a0 00 00 00 00 00 00 00 a0 00 00   ................
  0020: 00 00 00 00 00 a0 00                              .......
Seed 5 (id=018af0e4aa381eaa, size=76 bytes, fuzzer=cmplog, trial=1, discovered_at=1353s, mutation_op=ByteDecMutator,WordAddMutator,BytesInsertMutator,WordAddMutator,ByteFlipMutator,WordAddMutator,DwordAddMutator):
  0000: 00 00 00 00 2b 0d 01 10 c0 0a 00 00 bf 0a 00 00   ....+...........
  0010: bf 0a 00 00 bf 0a 00 00 bf 0a 00 00 00 0c 05 05   ................
  0020: 04 f5 05 05 26 05 05 05 ff ff ff ff ff ff ff ff   ....&...........
  0030: ff ff ff 00 ff 05 05 05 05 05 f0 ff 00 30 ff ff   .............0..


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  f2(.)x2 35(5)x2 f3(.)x1 01(.)x1 +6u  00(.)x5 ff(.)x3 df(.)x1 17(.)x1     DIFFER
   0x0002  00(.)x6 69(i)x1 a9(.)x1 c5(.)x1 +3u  00(.)x6 20( )x2 66(f)x1 7f(.)x1     PARTIAL
   0x0003  00(.)x5 64(d)x2 7a(z)x1 ff(.)x1 +3u  00(.)x6 20( )x4                     PARTIAL
   0x000d  06(.)x2 17(.)x2 a8(.)x1 6f(o)x1 +6u  50(P)x4 0a(.)x3 00(.)x3             DIFFER
   0x000e  00(.)x4 2d(-)x1 72(r)x1 c5(.)x1 +3u  00(.)x5 4f(O)x4 1a(.)x1             PARTIAL
   0x0012  00(.)x5 0c(.)x2 10(.)x1 1c(.)x1 +1u  00(.)x9 66(f)x1                     PARTIAL
   0x0013  00(.)x8 6a(j)x1 20( )x1             00(.)x4 0d(.)x2 1a(.)x1 6d(m)x1 +2u  PARTIAL
   0x0016  00(.)x3 a2(.)x1 96(.)x1 1c(.)x1 +4u  00(.)x8 1a(.)x1 20( )x1             PARTIAL
   0x001b  00(.)x4 a2(.)x1 2d(-)x1 ff(.)x1 +3u  00(.)x5 47(G)x3 1a(.)x1 01(.)x1     PARTIAL
   0x0022  00(.)x4 0c(.)x2 40(@)x1 80(.)x1 +1u  00(.)x8 05(.)x1 08(.)x1             PARTIAL
   0x0023  00(.)x6 0c(.)x2 20( )x1             00(.)x3 02(.)x2 0f(.)x1 05(.)x1 +3u  PARTIAL
   0x0025  00(.)x5 0c(.)x2 4c(L)x1 25(%)x1     00(.)x4 20( )x1 04(.)x1 a0(.)x1 +3u  PARTIAL
   0x0026  00(.)x6 0c(.)x2 ec(.)x1             00(.)x6 05(.)x1 1d(.)x1 ff(.)x1     PARTIAL
   0x0029  00(.)x5 0c(.)x2 dc(.)x1             00(.)x4 ff(.)x1 01(.)x1 22(")x1     PARTIAL
   0x002a  00(.)x4 e8(.)x1 bd(.)x1 0c(.)x1 +1u  00(.)x5 ff(.)x1 02(.)x1             PARTIAL
   0x002b  00(.)x3 f1(.)x1 f7(.)x1 bd(.)x1 +2u  10(.)x3 00(.)x2 ff(.)x1 6a(j)x1     PARTIAL
   0x002d  00(.)x4 0c(.)x2 17(.)x1 bd(.)x1     00(.)x2 ff(.)x1 66(f)x1 06(.)x1 +2u  PARTIAL
   0x002e  00(.)x4 0c(.)x3 bd(.)x1             00(.)x3 6b(k)x1 ff(.)x1 6d(m)x1 +1u  PARTIAL
   0x002f  00(.)x5 0c(.)x1 bd(.)x1 20( )x1     20( )x1 ff(.)x1 5a(Z)x1 06(.)x1 +3u  PARTIAL
   0x0030  00(.)x4 61(a)x1 cb(.)x1 bd(.)x1 +1u  00(.)x3 ff(.)x1 20( )x1 0f(.)x1     PARTIAL
   0x0032  00(.)x3 0c(.)x1 05(.)x1 bd(.)x1 +2u  00(.)x3 ff(.)x1 72(r)x1 64(d)x1     PARTIAL
   0x0034  00(.)x3 17(.)x2 45(E)x1 10(.)x1 +1u  00(.)x3 ff(.)x1 6e(n)x1 01(.)x1     PARTIAL
   0x0035  00(.)x6 05(.)x2                     05(.)x1 03(.)x1 00(.)x1 01(.)x1 +2u  PARTIAL
   0x0036  00(.)x4 1c(.)x1 05(.)x1 0c(.)x1 +1u  05(.)x2 00(.)x2 01(.)x1 fa(.)x1     PARTIAL
   0x0038  00(.)x3 1c(.)x1 f4(.)x1 05(.)x1 +2u  00(.)x3 05(.)x1 2a(*)x1 01(.)x1     PARTIAL
   0x0039  00(.)x4 1c(.)x2 01(.)x1 66(f)x1     06(.)x3 05(.)x1 24($)x1 01(.)x1     PARTIAL
   0x003b  64(d)x1 f7(.)x1 1c(.)x1 bd(.)x1 +3u  00(.)x2 10(.)x2 ff(.)x1 04(.)x1     PARTIAL
   0x003c  1c(.)x2 00(.)x2 65(e)x1 e2(.)x1 +1u  00(.)x3 1d(.)x1 01(.)x1 18(.)x1     PARTIAL
   0x003d  00(.)x5 56(V)x1 1c(.)x1             30(0)x1 d2(.)x1 00(.)x1 01(.)x1 +2u  PARTIAL
   0x003e  00(.)x4 10(.)x1 1c(.)x1 0c(.)x1     00(.)x2 ff(.)x1 e9(.)x1 01(.)x1 +1u  PARTIAL
   0x003f  00(.)x3 c2(.)x1 1c(.)x1 cb(.)x1 +1u  ff(.)x3 7f(.)x1 f0(.)x1 01(.)x1     DIFFER
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
  prompts_b/harfbuzz_5810.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5810,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5810 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5810 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5810 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).