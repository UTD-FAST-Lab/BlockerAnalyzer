==== BLOCKER ====
Target: harfbuzz
Branch ID: 5931
Location: /src/harfbuzz/src/hb-ot-shaper-myanmar-machine.hh:502:2
Enclosing function: find_syllables_myanmar(hb_buffer_t*)
Source line: 	case 8:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           2        8          0  loser (I2S vs naive)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             4        6          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         3        7          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=1.80h  loser=19.40h
  avg hitcount on branch: winner=38  loser=0
  prob_div=0.80  dur_div=17.60h  hit_div=38
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5931/{W,L}/branch_coverage_show.txt

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
[W]   494  	case 6:
[W]   495  #line 110 "hb-ot-shaper-myanmar-machine.rl"
[W]   496  	{te = p+1;{ found_syllable (myanmar_consonant_syllable); }}
[W]   497  	break;
[W]   498  	case 4:
[W]   499  #line 111 "hb-ot-shaper-myanmar-machine.rl"
[W]   500  	{te = p+1;{ found_syllable (myanmar_non_myanmar_cluster); }}
[W]   501  	break;
[W]   502  	case 8: <-- BLOCKER
[W]   503  #line 112 "hb-ot-shaper-myanmar-machine.rl"
[W]   504  	{te = p+1;{ found_syllable (myanmar_broken_cluster); buffer->scratch_flags |= HB_BUFFER_SCRATCH_FLAG_HAS_BROKEN_SYLLABLE; }}
[W]   505  	break;
[B]   506  	case 3:
[B]   507  #line 113 "hb-ot-shaper-myanmar-machine.rl"
[B]   508  	{te = p+1;{ found_syllable (myanmar_non_myanmar_cluster); }}
[B]   509  	break;
[B]   510  	case 5:
[B]   511  #line 110 "hb-ot-shaper-myanmar-machine.rl"
[B]   512  	{te = p;p--;{ found_syllable (myanmar_consonant_syllable); }}
[B]   513  	break;
[B]   514  	case 7:
[B]   515  #line 112 "hb-ot-shaper-myanmar-machine.rl"
[B]   516  	{te = p;p--;{ found_syllable (myanmar_broken_cluster); buffer->scratch_flags |= HB_BUFFER_SCRATCH_FLAG_HAS_BROKEN_SYLLABLE; }}
[B]   517  	break;
[ ]   518  	case 9:
[ ]   519  #line 113 "hb-ot-shaper-myanmar-machine.rl"
[ ]   520  	{te = p;p--;{ found_syllable (myanmar_non_myanmar_cluster); }}
[ ]   521  	break;
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
[W]   540  		_trans = _myanmar_syllable_machine_eof_trans[cs] - 1;
[W]   541  		goto _eof_trans;
[W]   542  	}
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
      69        20  hb-ot-shaper-myanmar.cc:is_one_of_myanmar(hb_glyph_info_t const&, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:79-83)
      69        20  hb-ot-shaper-myanmar.cc:is_consonant_myanmar(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:96-98)
      32         3  hb-ot-shaper-myanmar.cc:compare_myanmar_order(hb_glyph_info_t const*, hb_glyph_info_t const*)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:167-172)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  find_syllables_myanmar(hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-myanmar-machine.hh:441-549) ---
  d=1   L 484  T=83 F=0  T=20 F=2  ( info[p].myanmar_category()) <= _keys[1] ?
  d=1   L 494  T=3 F=125  T=0 F=157  case 6:
  d=1   L 498  T=3 F=125  T=0 F=157  case 4:
  d=1   L 502  T=21 F=107  T=0 F=157  case 8:  <-- BLOCKER
  d=1   L 539  T=2 F=10  T=0 F=10  if ( _myanmar_syllable_machine_eof_trans[cs] > 0 ) {

[off-chain: 22 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=a1568bfee9e19ce4, size=24 bytes, fuzzer=naive, trial=1, discovered_at=475s, mutation_op=BytesCopyMutator):
  0000: 10 10 00 00 0c 0c 0c 00 00 fe 00 00 0c 20 00 00   ............. ..
  0010: 00 fe 00 00 0c 20 00 00                           ..... ..
Seed 2 (id=9ae21f4b51d39044, size=36 bytes, fuzzer=naive, trial=1, discovered_at=515s, mutation_op=BytesInsertMutator,BytesExpandMutator):
  0000: 10 10 00 00 0c 0c 00 00 00 00 0c 00 00 fe 00 00   ................
  0010: 0c 20 00 00 00 fe 00 00 0c 20 00 00 00 fe 00 00   . ....... ......
  0020: 0c 20 00 00                                       . ..
Seed 3 (id=02ac2652bb45c395, size=82 bytes, fuzzer=naive, trial=1, discovered_at=630s, mutation_op=BytesInsertMutator):
  0000: ca 0f 00 10 00 68 2d 00 20 1f f0 a9 00 00 21 23   .....h-. .....!#
  0010: 00 aa aa aa 1f 1f 00 00 00 00 00 00 00 00 00 00   ................
  0020: 00 00 f0 a9 00 00 00 00 7f 00 00 00 00 00 0b 0c   ................
  0030: 00 00 00 14 ef ff ff fd 00 00 0c 20 00 00 80 00   ........... ....
Seed 4 (id=7dd71e91d2115b62, size=36 bytes, fuzzer=naive, trial=1, discovered_at=4842s, mutation_op=ByteNegMutator,ByteDecMutator,ByteAddMutator):
  0000: 10 10 00 00 0c 0c ff 00 00 00 0c 00 00 fe 00 00   ................
  0010: 0c 20 00 00 00 fe 09 00 1d 20 00 00 00 fe 00 00   . ....... ......
  0020: 0c 20 00 00                                       . ..
Seed 5 (id=0dca411b21920a58, size=44 bytes, fuzzer=naive, trial=1, discovered_at=5228s, mutation_op=ByteIncMutator,ByteAddMutator):
  0000: 10 10 00 00 0c 0c 00 00 00 00 0c 00 00 fe 00 00   ................
  0010: 0c 20 00 00 00 fe 00 00 0c 20 00 11 00 fe 00 00   . ....... ......
  0020: 0c 20 00 00 00 fe 00 00 0d 21 00 00               . .......!..

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=04d8571de170df2e, size=77 bytes, fuzzer=cmplog, trial=1, discovered_at=28s, mutation_op=ByteInterestingMutator,TokenReplace,BytesDeleteMutator):
  0000: 00 01 02 00 01 00 f9 f9 f9 00 01 00 f9 f9 f9 f9   ................
  0010: f9 f0 00 10 00 00 20 f9 f9 f9 f9 f0 f9 f9 f9 f9   ...... .........
  0020: f9 00 10 00 00 20 06 00 00 02 08 01 01 01 01 01   ..... ..........
  0030: 01 00 01 00 00 00 01 20 00 1a 20 20 20 39 39 39   ....... ..   999
Seed 2 (id=02a49f927f1125e3, size=25 bytes, fuzzer=cmplog, trial=1, discovered_at=130s, mutation_op=DwordAddMutator,WordInterestingMutator,ByteRandMutator,TokenInsert,BytesDeleteMutator):
  0000: 6b 20 00 00 01 10 00 00 68 61 73 63 12 16 01 00   k ......hasc....
  0010: 00 80 00 00 0e 01 00 00 65                        ........e
Seed 3 (id=031a883624e0ba3f, size=40 bytes, fuzzer=cmplog, trial=1, discovered_at=384s, mutation_op=BytesInsertCopyMutator,BytesSetMutator,BytesCopyMutator,BitFlipMutator,BytesDeleteMutator,BytesInsertCopyMutator,BytesRandSetMutator):
  0000: a4 a4 a4 a4 a4 63 66 63 10 0d 0b 00 21 0d 10 00   .....cfc....!...
  0010: fd a9 00 00 60 20 63 73 61 68 ff ff ff 03 f0 00   ....` csah......
  0020: 71 0e 00 ff 03 f0 11 00                           q.......
Seed 4 (id=051c163734ad5d08, size=35 bytes, fuzzer=cmplog, trial=1, discovered_at=506s, mutation_op=ByteFlipMutator,BytesInsertMutator,BytesDeleteMutator,BytesInsertCopyMutator,BytesCopyMutator):
  0000: 1e 03 80 00 00 00 6b 67 10 00 71 0f 72 10 00 00   ......kg..q.r...
  0010: 8d 10 00 00 8d 10 00 00 73 10 00 00 8d 10 00 00   ........s.......
  0020: 73 10 00                                          s..
Seed 5 (id=04223d85d25f4e4e, size=76 bytes, fuzzer=cmplog, trial=1, discovered_at=987s, mutation_op=ByteDecMutator,ByteNegMutator,BytesRandInsertMutator,BytesSwapMutator,TokenReplace,BytesInsertMutator,BytesSwapMutator):
  0000: fa fa 00 6f 77 0d aa 00 00 00 00 9b fd a9 00 00   ...ow...........
  0010: 60 00 00 00 00 00 00 00 00 00 00 00 fd a9 00 00   `...............
  0020: 60 00 16 a9 00 22 60 aa aa 00 cd cd cd cd cd 00   `...."`.........
  0030: 00 60 21 0d 01 20 00 00 fd a9 00 00 f8 25 cd cd   .`!.. .......%..


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0002  00(.)x8 03(.)x1 85(.)x1             00(.)x7 02(.)x1 a4(.)x1 80(.)x1     PARTIAL
   0x0003  00(.)x6 0c(.)x2 10(.)x1 85(.)x1     00(.)x8 a4(.)x1 6f(o)x1             PARTIAL
   0x0004  0c(.)x4 00(.)x3 20( )x1 fe(.)x1 +1u  00(.)x6 01(.)x2 a4(.)x1 77(w)x1     PARTIAL
   0x0006  00(.)x5 0c(.)x2 ff(.)x2 2d(-)x1     20( )x2 07(.)x2 f9(.)x1 00(.)x1 +4u  PARTIAL
   0x0007  00(.)x8 20( )x1 7f(.)x1             20( )x4 00(.)x3 f9(.)x1 63(c)x1 +1u  PARTIAL
   0x0008  00(.)x7 20( )x1 0c(.)x1 61(a)x1     21(!)x3 10(.)x2 00(.)x2 f9(.)x1 +2u  PARTIAL
   0x0009  00(.)x6 fe(.)x2 1f(.)x1 6e(n)x1     00(.)x4 20( )x4 61(a)x1 0d(.)x1     PARTIAL
   0x000a  00(.)x5 0c(.)x3 f0(.)x1 2d(-)x1     20( )x3 1e(.)x2 01(.)x1 73(s)x1 +3u  PARTIAL
   0x000b  00(.)x7 a9(.)x1 fe(.)x1 0b(.)x1     20( )x5 00(.)x2 63(c)x1 0f(.)x1 +1u  PARTIAL
   0x000d  00(.)x4 fe(.)x3 20( )x2 74(t)x1     50(P)x3 41(A)x2 f9(.)x1 16(.)x1 +3u  DIFFER
   0x000e  00(.)x7 21(!)x1 01(.)x1 2d(-)x1     4f(O)x3 00(.)x2 54(T)x2 f9(.)x1 +2u  PARTIAL
   0x000f  00(.)x7 23(#)x1 0c(.)x1 68(h)x1     00(.)x4 53(S)x3 48(H)x2 f9(.)x1     PARTIAL
   0x0010  00(.)x5 0c(.)x3 20( )x1 6b(k)x1     00(.)x6 f9(.)x1 fd(.)x1 8d(.)x1 +1u  PARTIAL
   0x0012  00(.)x7 aa(.)x1 97(.)x1 75(u)x1     00(.)x10                            PARTIAL
   0x0013  00(.)x7 aa(.)x1 0b(.)x1 6e(n)x1     00(.)x4 80(.)x2 0d(.)x2 10(.)x1 +1u  PARTIAL
   0x0014  00(.)x3 0c(.)x1 1f(.)x1 2d(-)x1 +4u  00(.)x7 0e(.)x1 60(`)x1 8d(.)x1     PARTIAL
   0x0015  fe(.)x3 00(.)x3 20( )x1 1f(.)x1 +2u  00(.)x7 01(.)x1 20( )x1 10(.)x1     PARTIAL
   0x0016  00(.)x8 09(.)x1 1a(.)x1             00(.)x8 20( )x1 63(c)x1             PARTIAL
   0x0017  00(.)x9 d4(.)x1                     10(.)x5 00(.)x3 f9(.)x1 73(s)x1     PARTIAL
   0x001a  00(.)x9                             00(.)x4 03(.)x2 f9(.)x1 ff(.)x1 +1u  PARTIAL
   0x001b  00(.)x6 11(.)x1 01(.)x1 ff(.)x1     00(.)x3 03(.)x2 47(G)x2 f0(.)x1 +1u  PARTIAL
   0x001d  fe(.)x4 00(.)x3 7f(.)x1 10(.)x1     10(.)x3 00(.)x2 f9(.)x1 03(.)x1 +2u  PARTIAL
   0x001e  00(.)x8 79(y)x1                     00(.)x6 f9(.)x1 f0(.)x1 30(0)x1     PARTIAL
   0x001f  00(.)x6 79(y)x1 97(.)x1 15(.)x1     00(.)x5 03(.)x2 f9(.)x1 30(0)x1     PARTIAL
   0x0020  0c(.)x4 00(.)x3 79(y)x1 7f(.)x1     20( )x2 00(.)x2 f9(.)x1 71(q)x1 +3u  PARTIAL
   0x0021  20( )x4 00(.)x3 79(y)x1 01(.)x1     00(.)x5 0e(.)x1 10(.)x1 04(.)x1 +1u  PARTIAL
   0x0023  00(.)x6 a9(.)x1 79(y)x1 03(.)x1     06(.)x2 00(.)x1 ff(.)x1 a9(.)x1 +3u  PARTIAL
   0x0024  00(.)x5 79(y)x1 0b(.)x1             00(.)x4 4f(O)x2 03(.)x1 01(.)x1     PARTIAL
   0x0025  00(.)x3 fe(.)x2 18(.)x1 0f(.)x1     00(.)x2 20( )x1 f0(.)x1 22(")x1 +3u  PARTIAL
   0x0027  00(.)x5 79(y)x1 0e(.)x1             00(.)x3 10(.)x2 aa(.)x1 02(.)x1 +1u  PARTIAL
   0x0028  00(.)x3 7f(.)x1 0d(.)x1 de(.)x1 +1u  00(.)x4 aa(.)x1 ff(.)x1 03(.)x1     PARTIAL
   0x0029  00(.)x3 21(!)x1 0c(.)x1 fd(.)x1 +1u  00(.)x3 01(.)x2 02(.)x1 10(.)x1     PARTIAL
   0x002a  00(.)x6 7f(.)x1                     00(.)x2 08(.)x1 cd(.)x1 6b(k)x1 +2u  PARTIAL
   0x002b  00(.)x7                             01(.)x3 10(.)x2 cd(.)x1 61(a)x1     DIFFER
   0x002c  00(.)x4 79(y)x1 0c(.)x1             00(.)x3 01(.)x2 cd(.)x1 72(r)x1     PARTIAL
   0x002e  00(.)x3 0b(.)x1 79(y)x1 20( )x1     01(.)x1 cd(.)x1 7f(.)x1 20( )x1 +3u  PARTIAL
   0x0030  00(.)x4 79(y)x1 0c(.)x1             00(.)x5 01(.)x1 20( )x1             PARTIAL
   0x0032  00(.)x4 79(y)x1 0c(.)x1             00(.)x3 01(.)x1 21(!)x1 e3(.)x1 +1u  PARTIAL
   0x0033  00(.)x3 14(.)x1 79(y)x1 20( )x1     00(.)x3 0d(.)x1 e3(.)x1 01(.)x1 +1u  PARTIAL
   0x0034  00(.)x2 ef(.)x1 fe(.)x1 20( )x1     00(.)x3 01(.)x2 e3(.)x1 73(s)x1     PARTIAL
   ... (10 more divergent offsets)
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
  prompts_b/harfbuzz_5931.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5931,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5931 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5931 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5931 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).