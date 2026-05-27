==== BLOCKER ====
Target: harfbuzz
Branch ID: 9459
Location: /src/harfbuzz/src/hb-ot-shaper-myanmar-machine.hh:518:2
Enclosing function: find_syllables_myanmar(hb_buffer_t*)
Source line: 	case 9:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            8        2          0  REFERENCE
cmplog                           3        7          0  REFERENCE
value_profile                   10        0          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             0       10          0  loser (I2S vs value_profile)

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 20  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=2.70h  loser=11.95h
  avg hitcount on branch: winner=8  loser=0
  prob_div=1.00  dur_div=9.25h  hit_div=8
  subject-level: delta_AUC=12333210.0  p_AUC=0.0002  delta_Final=1452.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/9459/{W,L}/branch_coverage_show.txt

--- Enclosing function: find_syllables_myanmar(hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shaper-myanmar-machine.hh:441-549) ---
[ ]   439  inline void
[ ]   440  find_syllables_myanmar (hb_buffer_t *buffer)
[B]   441  {
[B]   442    unsigned int p, pe, eof, ts, te, act HB_UNUSED;
[B]   443    int cs;
[B]   444    hb_glyph_info_t *info = buffer->info;
[ ]   445    
[B]   446  #line 436 "hb-ot-shaper-myanmar-machine.hh"
[B]   447  	{
[B]   448  	cs = myanmar_syllable_machine_start;
[B]   449  	ts = 0;
[B]   450  	te = 0;
[B]   451  	act = 0;
[B]   452  	}
[ ]   453  
[B]   454  #line 137 "hb-ot-shaper-myanmar-machine.rl"
[ ]   455  
[ ]   456  
[B]   457    p = 0;
[B]   458    pe = eof = buffer->len;
[ ]   459  
[B]   460    unsigned int syllable_serial = 1;
[ ]   461    
[B]   462  #line 448 "hb-ot-shaper-myanmar-machine.hh"
[B]   463  	{
[B]   464  	int _slen;
[B]   465  	int _trans;
[B]   466  	const unsigned char *_keys;
[B]   467  	const char *_inds;
[B]   468  	if ( p == pe )
[ ]   469  		goto _test_eof;
[B]   470  _resume:
[B]   471  	switch ( _myanmar_syllable_machine_from_state_actions[cs] ) {
[B]   472  	case 2:
[B]   473  #line 1 "NONE"
[B]   474  	{ts = p;}
[B]   475  	break;
[B]   476  #line 460 "hb-ot-shaper-myanmar-machine.hh"
[B]   477  	}
[ ]   478  
[B]   479  	_keys = _myanmar_syllable_machine_trans_keys + (cs<<1);
[B]   480  	_inds = _myanmar_syllable_machine_indicies + _myanmar_syllable_machine_index_offsets[cs];
[ ]   481  
[B]   482  	_slen = _myanmar_syllable_machine_key_spans[cs];
[B]   483  	_trans = _inds[ _slen > 0 && _keys[0] <=( info[p].myanmar_category()) &&
[B]   484  		( info[p].myanmar_category()) <= _keys[1] ?
[B]   485  		( info[p].myanmar_category()) - _keys[0] : _slen ];
[ ]   486  
[B]   487  _eof_trans:
[B]   488  	cs = _myanmar_syllable_machine_trans_targs[_trans];
[ ]   489  
[B]   490  	if ( _myanmar_syllable_machine_trans_actions[_trans] == 0 )
[B]   491  		goto _again;
[ ]   492  
[B]   493  	switch ( _myanmar_syllable_machine_trans_actions[_trans] ) {
[ ]   494  	case 6:
[ ]   495  #line 110 "hb-ot-shaper-myanmar-machine.rl"
[ ]   496  	{te = p+1;{ found_syllable (myanmar_consonant_syllable); }}
[ ]   497  	break;
[ ]   498  	case 4:
[ ]   499  #line 111 "hb-ot-shaper-myanmar-machine.rl"
[ ]   500  	{te = p+1;{ found_syllable (myanmar_non_myanmar_cluster); }}
[ ]   501  	break;
[ ]   502  	case 8:
[ ]   503  #line 112 "hb-ot-shaper-myanmar-machine.rl"
[ ]   504  	{te = p+1;{ found_syllable (myanmar_broken_cluster); buffer->scratch_flags |= HB_BUFFER_SCRATCH_FLAG_HAS_BROKEN_SYLLABLE; }}
[ ]   505  	break;
[B]   506  	case 3:
[B]   507  #line 113 "hb-ot-shaper-myanmar-machine.rl"
[B]   508  	{te = p+1;{ found_syllable (myanmar_non_myanmar_cluster); }}
[B]   509  	break;
[B]   510  	case 5:
[B]   511  #line 110 "hb-ot-shaper-myanmar-machine.rl"
[B]   512  	{te = p;p--;{ found_syllable (myanmar_consonant_syllable); }}
[B]   513  	break;
[ ]   514  	case 7:
[ ]   515  #line 112 "hb-ot-shaper-myanmar-machine.rl"
[ ]   516  	{te = p;p--;{ found_syllable (myanmar_broken_cluster); buffer->scratch_flags |= HB_BUFFER_SCRATCH_FLAG_HAS_BROKEN_SYLLABLE; }}
[ ]   517  	break;
[W]   518  	case 9: <-- BLOCKER
[W]   519  #line 113 "hb-ot-shaper-myanmar-machine.rl"
[W]   520  	{te = p;p--;{ found_syllable (myanmar_non_myanmar_cluster); }}
[W]   521  	break;
[B]   522  #line 498 "hb-ot-shaper-myanmar-machine.hh"
[B]   523  	}
[ ]   524  
[B]   525  _again:
[B]   526  	switch ( _myanmar_syllable_machine_to_state_actions[cs] ) {
[B]   527  	case 1:
[B]   528  #line 1 "NONE"
[B]   529  	{ts = 0;}
[B]   530  	break;
[B]   531  #line 505 "hb-ot-shaper-myanmar-machine.hh"
[B]   532  	}
[ ]   533  
[B]   534  	if ( ++p != pe )
[B]   535  		goto _resume;
[B]   536  	_test_eof: {}
[B]   537  	if ( p == eof )
[B]   538  	{
[B]   539  	if ( _myanmar_syllable_machine_eof_trans[cs] > 0 ) {
[B]   540  		_trans = _myanmar_syllable_machine_eof_trans[cs] - 1;
[B]   541  		goto _eof_trans;
[B]   542  	}
[B]   543  	}
[ ]   544  
[B]   545  	}
[ ]   546  
[B]   547  #line 145 "hb-ot-shaper-myanmar-machine.rl"
[ ]   548  
[B]   549  }

--- Caller (1 hop): hb-ot-shaper-myanmar.cc:setup_syllables_myanmar(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:157-163, calls find_syllables_myanmar(hb_buffer_t*) at line 159) (full body — short) ---
[B]   157  {
[B]   158    HB_BUFFER_ALLOCATE_VAR (buffer, syllable);
[B]   159    find_syllables_myanmar (buffer); <-- CALL
[B]   160    foreach_syllable (buffer, start, end)
[B]   161      buffer->unsafe_to_break (start, end);
[B]   162    return false;
[B]   163  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-myanmar.cc:setup_syllables_myanmar(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:157-163, calls find_syllables_myanmar(hb_buffer_t*) at line 159)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       6        21  hb-ot-shaper-myanmar.cc:is_one_of_myanmar(hb_glyph_info_t const&, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:79-83)
       6        21  hb-ot-shaper-myanmar.cc:is_consonant_myanmar(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:96-98)
       6        21  hb-ot-shaper-myanmar.cc:initial_reordering_consonant_syllable(hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:181-301)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  find_syllables_myanmar(hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-myanmar-machine.hh:441-549) ---
  d=1   L 518  T=14 F=82  T=0 F=160  case 9:  <-- BLOCKER

[off-chain: 13 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=590665959e0a28b0, size=139 bytes, fuzzer=cmplog, trial=2, discovered_at=929s, mutation_op=BytesRandInsertMutator,BytesSwapMutator,TokenInsert,BytesSetMutator,BytesCopyMutator,ByteDecMutator):
  0000: 00 ff 01 20 49 0c 00 00 00 04 20 00 ff 01 20 4a   ... I..... ... J
  0010: 0c 00 00 00 7c 69 61 68 54 7c 7c 7c 7c 7c 7c 7c   ....|iahT|||||||
  0020: 20 0d 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ...............
  0030: 80 00 00 00 00 00 00 6f 2d 53 61 01 06 00 00 00   .......o-Sa.....
Seed 2 (id=90af32e3a407d8da, size=161 bytes, fuzzer=cmplog, trial=2, discovered_at=1002s, mutation_op=CrossoverInsertMutator,BytesExpandMutator,CrossoverInsertMutator,BytesExpandMutator,ByteIncMutator):
  0000: 00 ff 01 20 49 0c 00 ff 01 20 49 0c 00 00 00 04   ... I.... I.....
  0010: 20 00 ff 01 20 4a 0c 00 00 00 7c 69 61 68 54 7c    ... J....|iahT|
  0020: 7c 7c 7c 7c 7c 7c 20 0d 00 00 00 01 0b 00 00 00   |||||| .........
  0030: 00 00 00 00 00 00 00 00 80 00 00 01 00 00 00 6f   ...............o
Seed 3 (id=e23eae58b496d643, size=125 bytes, fuzzer=cmplog, trial=2, discovered_at=1074s, mutation_op=ByteDecMutator,BitFlipMutator,ByteAddMutator,BytesDeleteMutator,BytesCopyMutator):
  0000: 00 ff 01 20 49 0c 00 ff 01 20 49 0c 00 00 00 04   ... I.... I.....
  0010: 20 00 ff 01 20 4a 0c 00 00 00 7c 69 61 68 54 7c    ... J....|iahT|
  0020: 7c 7c 7c 7c 98 7c 00 00 00 00 00 2f 00 20 00 1f   ||||.|...../. ..
  0030: 01 a9 00 00 00 00 00 a8 00 00 00 a8 00 00 00 a8   ................
Seed 4 (id=9d7b0b123ca6b5b9, size=125 bytes, fuzzer=cmplog, trial=2, discovered_at=1152s, mutation_op=WordAddMutator,WordAddMutator,DwordAddMutator,BytesSwapMutator,CrossoverInsertMutator,BytesSwapMutator):
  0000: 00 ff 01 20 49 0c 00 ff 01 20 49 0c 00 00 00 04   ... I.... I.....
  0010: 20 74 79 70 31 4a 0c 00 00 00 7c 69 61 68 54 7c    typ1J....|iahT|
  0020: 7c 7c 7c 7c 98 7c 02 67 69 6c 72 2f 00 20 00 1f   ||||.|.gilr/. ..
  0030: 01 a9 73 77 6c 62 00 a8 00 00 00 a8 00 00 00 a8   ..swlb..........
Seed 5 (id=28eb0bc2edabfc7a, size=151 bytes, fuzzer=cmplog, trial=2, discovered_at=3573s, mutation_op=CrossoverInsertMutator,BytesSwapMutator):
  0000: ff 10 01 00 72 00 00 02 00 f2 0c 00 00 80 fe 00   ....r...........
  0010: 00 ff 01 20 49 0c 00 ff 01 20 49 0c 00 00 fe 00   ... I.... I.....
  0020: 20 00 ff 01 20 4a 0c 00 00 00 7c 69 61 68 54 7c    ... J....|iahT|
  0030: 7c 7c 7c 7c 98 7c 00 00 00 00 00 2f 00 20 00 1f   ||||.|...../. ..

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00293b686680cdda, size=66 bytes, fuzzer=cmplog, trial=1, discovered_at=5s, mutation_op=BytesRandSetMutator,BytesCopyMutator,TokenInsert):
  0000: 00 00 01 10 00 00 00 20 20 20 20 20 20 6b 00 08   .......      k..
  0010: 00 00 01 20 20 20 04 00 00 01 00 7f 20 6b 65 7a   ...   ...... kez
  0020: 68 2d 68 61 6e 74 2d 6d 6f 00 72 6e 20 20 20 20   h-hant-mo.rn    
  0030: 00 02 00 20 00 02 00 20 20 20 20 60 00 1a 20 23   ... ...    `.. #
Seed 2 (id=0078665cd55688d0, size=23 bytes, fuzzer=cmplog, trial=1, discovered_at=93s, mutation_op=BytesDeleteMutator,ByteRandMutator,ByteNegMutator,BytesDeleteMutator):
  0000: 00 10 00 00 00 00 20 20 10 0a 00 00 00 00 00 20   ......  ....... 
  0010: 20 10 00 00 00 00 20                               ..... 
Seed 3 (id=012fd22e30076039, size=45 bytes, fuzzer=cmplog, trial=1, discovered_at=359s, mutation_op=BytesCopyMutator,ByteRandMutator,BytesInsertCopyMutator,ByteRandMutator,ByteDecMutator,WordAddMutator):
  0000: 74 70 78 2d 00 10 00 00 00 1f 16 01 00 a0 00 00   tpx-............
  0010: 00 a0 00 00 20 ff 00 00 00 26 00 00 74 70 20 2d   .... ....&..tp -
  0020: 00 10 20 05 64 6e c1 20 00 20 20 20 20            .. .dn. .    
Seed 4 (id=0045c9404813a29a, size=38 bytes, fuzzer=cmplog, trial=1, discovered_at=493s, mutation_op=ByteRandMutator,BytesDeleteMutator,TokenInsert,QwordAddMutator,BytesDeleteMutator,BytesDeleteMutator):
  0000: 00 00 00 01 00 00 b1 b1 b1 00 00 00 00 10 00 00   ................
  0010: 00 00 00 00 00 20 20 20 20 00 b1 b1 b1 00 00 00   .....    .......
  0020: 00 10 00 00 00 00                                 ......
Seed 5 (id=002242b926005ecd, size=98 bytes, fuzzer=cmplog, trial=1, discovered_at=514s, mutation_op=WordAddMutator,BytesExpandMutator,CrossoverReplaceMutator):
  0000: 01 00 01 00 01 20 20 20 20 03 02 00 01 75 72 00   .....    ....ur.
  0010: 76 30 6c 6c 6c 6c 00 64 20 20 10 02 fb fb fb fb   v0llll.d  ......
  0020: fb 7f 06 00 00 00 80 10 00 00 00 02 00 00 80 10   ................
  0030: 00 00 00 02 00 00 20 10 01 00 01 00 00 00 20 10   ...... ....... .


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x5 ff(.)x1                     00(.)x7 74(t)x1 01(.)x1 0a(.)x1     PARTIAL
   0x0001  ff(.)x5 10(.)x1                     00(.)x4 01(.)x3 10(.)x1 70(p)x1 +1u  PARTIAL
   0x0002  01(.)x6                             00(.)x6 01(.)x3 78(x)x1             PARTIAL
   0x0003  20( )x5 00(.)x1                     00(.)x7 10(.)x1 2d(-)x1 01(.)x1     PARTIAL
   0x0004  49(I)x5 72(r)x1                     00(.)x8 01(.)x1 64(d)x1             DIFFER
   0x0005  0c(.)x5 00(.)x1                     00(.)x3 04(.)x2 10(.)x1 20( )x1 +3u  PARTIAL
   0x0006  00(.)x6                             20( )x5 00(.)x3 b1(.)x1 0d(.)x1     PARTIAL
   0x0007  ff(.)x4 00(.)x1 02(.)x1             00(.)x4 20( )x3 b1(.)x1 06(.)x1 +1u  PARTIAL
   0x0008  01(.)x4 00(.)x2                     00(.)x5 20( )x2 10(.)x1 b1(.)x1 +1u  PARTIAL
   0x0009  20( )x4 04(.)x1 f2(.)x1             7f(.)x3 00(.)x2 20( )x1 0a(.)x1 +3u  PARTIAL
   0x000a  49(I)x4 20( )x1 0c(.)x1             00(.)x7 20( )x1 16(.)x1 02(.)x1     PARTIAL
   0x000b  0c(.)x4 00(.)x2                     00(.)x5 20( )x3 01(.)x1 ff(.)x1     PARTIAL
   0x000c  00(.)x5 ff(.)x1                     00(.)x5 20( )x3 01(.)x1 ff(.)x1     PARTIAL
   0x000d  00(.)x4 01(.)x1 80(.)x1             00(.)x2 20( )x2 6b(k)x1 a0(.)x1 +4u  PARTIAL
   0x000e  00(.)x4 20( )x1 fe(.)x1             00(.)x4 56(V)x2 72(r)x1 c7(.)x1 +2u  PARTIAL
   0x000f  04(.)x4 4a(J)x1 00(.)x1             00(.)x4 20( )x2 56(V)x2 08(.)x1 +1u  PARTIAL
   0x0010  20( )x3 0c(.)x1 00(.)x1 08(.)x1     00(.)x3 20( )x3 41(A)x2 76(v)x1 +1u  PARTIAL
   0x0011  00(.)x4 74(t)x1 ff(.)x1             00(.)x3 10(.)x1 a0(.)x1 30(0)x1 +4u  PARTIAL
   0x0012  ff(.)x3 00(.)x1 79(y)x1 01(.)x1     00(.)x3 b9(.)x2 01(.)x1 6c(l)x1 +2u  PARTIAL
   0x0013  01(.)x3 00(.)x1 70(p)x1 20( )x1     00(.)x3 20( )x2 b9(.)x2 6c(l)x1 +1u  PARTIAL
   0x0014  20( )x3 7c(|)x1 31(1)x1 49(I)x1     20( )x3 00(.)x2 b9(.)x2 6c(l)x1 +1u  PARTIAL
   0x0015  4a(J)x4 69(i)x1 0c(.)x1             20( )x3 01(.)x2 00(.)x1 ff(.)x1 +2u  DIFFER
   0x0016  0c(.)x4 61(a)x1 00(.)x1             20( )x3 00(.)x2 ff(.)x2 04(.)x1 +1u  PARTIAL
   0x0017  00(.)x4 68(h)x1 ff(.)x1             00(.)x3 ff(.)x3 20( )x1 64(d)x1     PARTIAL
   0x0018  00(.)x4 54(T)x1 01(.)x1             00(.)x3 fe(.)x3 20( )x2             PARTIAL
   0x0019  00(.)x4 7c(|)x1 20( )x1             f2(.)x3 01(.)x2 26(&)x1 00(.)x1 +1u  PARTIAL
   0x001a  7c(|)x5 49(I)x1                     1a(.)x3 00(.)x2 b1(.)x1 10(.)x1 +1u  DIFFER
   0x001b  69(i)x4 7c(|)x1 0c(.)x1             20( )x3 7f(.)x1 00(.)x1 b1(.)x1 +2u  DIFFER
   0x001c  61(a)x4 7c(|)x1 00(.)x1             47(G)x3 20( )x1 74(t)x1 b1(.)x1 +2u  DIFFER
   0x001d  68(h)x4 7c(|)x1 00(.)x1             50(P)x3 6b(k)x1 70(p)x1 00(.)x1 +2u  PARTIAL
   0x001e  54(T)x4 7c(|)x1 fe(.)x1             4f(O)x3 65(e)x1 20( )x1 00(.)x1 +2u  DIFFER
   0x001f  7c(|)x5 00(.)x1                     53(S)x3 7a(z)x1 2d(-)x1 00(.)x1 +2u  PARTIAL
   0x0020  7c(|)x4 20( )x2                     00(.)x4 68(h)x1 fb(.)x1 02(.)x1 +1u  DIFFER
   0x0021  7c(|)x4 0d(.)x1 00(.)x1             00(.)x3 10(.)x2 2d(-)x1 7f(.)x1 +1u  PARTIAL
   0x0022  7c(|)x4 00(.)x1 ff(.)x1             03(.)x3 20( )x2 68(h)x1 00(.)x1 +1u  PARTIAL
   0x0023  7c(|)x4 00(.)x1 01(.)x1             00(.)x4 20( )x2 61(a)x1 05(.)x1     PARTIAL
   0x0024  98(.)x3 00(.)x1 7c(|)x1 20( )x1     00(.)x5 6e(n)x1 64(d)x1 80(.)x1     PARTIAL
   0x0025  7c(|)x4 00(.)x1 4a(J)x1             00(.)x5 74(t)x1 6e(n)x1 11(.)x1     PARTIAL
   0x0026  00(.)x3 20( )x1 02(.)x1 0c(.)x1     00(.)x3 2d(-)x1 c1(.)x1 80(.)x1 +1u  PARTIAL
   0x0027  00(.)x4 0d(.)x1 67(g)x1             00(.)x3 10(.)x2 6d(m)x1 20( )x1     PARTIAL
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
  prompts/--RB/00_harfbuzz_9459.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 9459,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>value_profile_cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 9459 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 9459 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 9459 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).