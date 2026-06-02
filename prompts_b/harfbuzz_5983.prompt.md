==== BLOCKER ====
Target: harfbuzz
Branch ID: 5983
Location: /src/harfbuzz/src/hb-ot-shaper-use-machine.hh:993:2
Enclosing function: hb-ot-shaper-use.cc:find_syllables_use(hb_buffer_t*)
Source line: 	case 14:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            8        2          0  winner (I2S vs cmplog)
cmplog                           0       10          0  loser (I2S vs naive); loser (value_profile vs value_profile_cmplog)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog)
naive_ctx                        7        3          0  REFERENCE
naive_ngram4                     5        5          0  REFERENCE
mopt                             5        5          0  REFERENCE
minimizer                        7        3          0  REFERENCE
fast                             6        4          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=12.60h  loser=23.60h
  avg hitcount on branch: winner=5  loser=0
  prob_div=0.80  dur_div=11.00h  hit_div=5
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=11.90h  loser=23.60h
  avg hitcount on branch: winner=1  loser=0
  prob_div=0.80  dur_div=11.70h  hit_div=1
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5983/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-use.cc:find_syllables_use(hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:907-1076) ---
[ ]   905  static inline void
[ ]   906  find_syllables_use (hb_buffer_t *buffer)
[B]   907  {
[B]   908    hb_glyph_info_t *info = buffer->info;
[B]   909    auto p =
[B]   910      + hb_iter (info, buffer->len)
[B]   911      | hb_enumerate
[B]   912      | hb_filter ([] (const hb_glyph_info_t &i) { return not_ccs_default_ignorable (i); },
[B]   913  		 hb_second)
[B]   914      | hb_filter ([&] (const hb_pair_t<unsigned, const hb_glyph_info_t &> p)
[B]   915  		 {
[B]   916  		   if (p.second.use_category() == USE(ZWNJ))
[B]   917  		     for (unsigned i = p.first + 1; i < buffer->len; ++i)
[B]   918  		       if (not_ccs_default_ignorable (info[i]))
[B]   919  			 return !_hb_glyph_info_is_unicode_mark (&info[i]);
[B]   920  		   return true;
[B]   921  		 })
[B]   922      | hb_enumerate
[B]   923      | machine_index
[B]   924      ;
[B]   925    auto pe = p + p.len ();
[B]   926    auto eof = +pe;
[B]   927    auto ts = +p;
[B]   928    auto te = +p;
[B]   929    unsigned int act HB_UNUSED;
[B]   930    int cs;
[ ]   931    
[B]   932  #line 922 "hb-ot-shaper-use-machine.hh"
[B]   933  	{
[B]   934  	cs = use_syllable_machine_start;
[B]   935  	ts = 0;
[B]   936  	te = 0;
[B]   937  	act = 0;
[B]   938  	}
[ ]   939  
[B]   940  #line 282 "hb-ot-shaper-use-machine.rl"
[ ]   941  
[ ]   942  
[B]   943    unsigned int syllable_serial = 1;
[ ]   944    
[B]   945  #line 931 "hb-ot-shaper-use-machine.hh"
[B]   946  	{
[B]   947  	int _slen;
[B]   948  	int _trans;
[B]   949  	const unsigned char *_keys;
[B]   950  	const unsigned char *_inds;
[B]   951  	if ( p == pe )
[ ]   952  		goto _test_eof;
[B]   953  _resume:
[B]   954  	switch ( _use_syllable_machine_from_state_actions[cs] ) {
[B]   955  	case 2:
[B]   956  #line 1 "NONE"
[B]   957  	{ts = p;}
[B]   958  	break;
[B]   959  #line 943 "hb-ot-shaper-use-machine.hh"
[B]   960  	}
[ ]   961  
[B]   962  	_keys = _use_syllable_machine_trans_keys + (cs<<1);
[B]   963  	_inds = _use_syllable_machine_indicies + _use_syllable_machine_index_offsets[cs];
[ ]   964  
[B]   965  	_slen = _use_syllable_machine_key_spans[cs];
[B]   966  	_trans = _inds[ _slen > 0 && _keys[0] <=( (*p).second.second.use_category()) &&
[B]   967  		( (*p).second.second.use_category()) <= _keys[1] ?
[B]   968  		( (*p).second.second.use_category()) - _keys[0] : _slen ];
[ ]   969  
[B]   970  _eof_trans:
[B]   971  	cs = _use_syllable_machine_trans_targs[_trans];
[ ]   972  
[B]   973  	if ( _use_syllable_machine_trans_actions[_trans] == 0 )
[B]   974  		goto _again;
[ ]   975  
[B]   976  	switch ( _use_syllable_machine_trans_actions[_trans] ) {
[ ]   977  	case 12:
[ ]   978  #line 170 "hb-ot-shaper-use-machine.rl"
[ ]   979  	{te = p+1;{ found_syllable (use_virama_terminated_cluster); }}
[ ]   980  	break;
[ ]   981  	case 10:
[ ]   982  #line 171 "hb-ot-shaper-use-machine.rl"
[ ]   983  	{te = p+1;{ found_syllable (use_sakot_terminated_cluster); }}
[ ]   984  	break;
[ ]   985  	case 8:
[ ]   986  #line 172 "hb-ot-shaper-use-machine.rl"
[ ]   987  	{te = p+1;{ found_syllable (use_standard_cluster); }}
[ ]   988  	break;
[ ]   989  	case 16:
[ ]   990  #line 173 "hb-ot-shaper-use-machine.rl"
[ ]   991  	{te = p+1;{ found_syllable (use_number_joiner_terminated_cluster); }}
[ ]   992  	break;
[W]   993  	case 14: <-- BLOCKER
[W]   994  #line 174 "hb-ot-shaper-use-machine.rl"
[W]   995  	{te = p+1;{ found_syllable (use_numeral_cluster); }}
[W]   996  	break;
[ ]   997  	case 6:
[ ]   998  #line 175 "hb-ot-shaper-use-machine.rl"
[ ]   999  	{te = p+1;{ found_syllable (use_symbol_cluster); }}
[ ]  1000  	break;
[ ]  1001  	case 20:
[ ]  1002  #line 176 "hb-ot-shaper-use-machine.rl"
[ ]  1003  	{te = p+1;{ found_syllable (use_hieroglyph_cluster); }}
[ ]  1004  	break;
[L]  1005  	case 4:
[L]  1006  #line 177 "hb-ot-shaper-use-machine.rl"
[L]  1007  	{te = p+1;{ found_syllable (use_broken_cluster); buffer->scratch_flags |= HB_BUFFER_SCRATCH_FLAG_HAS_BROKEN_SYLLABLE; }}
[L]  1008  	break;
[W]  1009  	case 3:
[W]  1010  #line 178 "hb-ot-shaper-use-machine.rl"
[W]  1011  	{te = p+1;{ found_syllable (use_non_cluster); }}
[W]  1012  	break;
[ ]  1013  	case 11:
[ ]  1014  #line 170 "hb-ot-shaper-use-machine.rl"
[ ]  1015  	{te = p;p--;{ found_syllable (use_virama_terminated_cluster); }}
[ ]  1016  	break;
[ ]  1017  	case 9:
[ ]  1018  #line 171 "hb-ot-shaper-use-machine.rl"
[ ]  1019  	{te = p;p--;{ found_syllable (use_sakot_terminated_cluster); }}
[ ]  1020  	break;
[B]  1021  	case 7:
[B]  1022  #line 172 "hb-ot-shaper-use-machine.rl"
[B]  1023  	{te = p;p--;{ found_syllable (use_standard_cluster); }}
[B]  1024  	break;
[ ]  1025  	case 15:
[ ]  1026  #line 173 "hb-ot-shaper-use-machine.rl"
[ ]  1027  	{te = p;p--;{ found_syllable (use_number_joiner_terminated_cluster); }}
[ ]  1028  	break;
[ ]  1029  	case 13:
[ ]  1030  #line 174 "hb-ot-shaper-use-machine.rl"
[ ]  1031  	{te = p;p--;{ found_syllable (use_numeral_cluster); }}
[ ]  1032  	break;
[B]  1033  	case 5:
[B]  1034  #line 175 "hb-ot-shaper-use-machine.rl"
[B]  1035  	{te = p;p--;{ found_syllable (use_symbol_cluster); }}
[B]  1036  	break;
[ ]  1037  	case 19:
[ ]  1038  #line 176 "hb-ot-shaper-use-machine.rl"
[ ]  1039  	{te = p;p--;{ found_syllable (use_hieroglyph_cluster); }}
[ ]  1040  	break;
[L]  1041  	case 17:
[L]  1042  #line 177 "hb-ot-shaper-use-machine.rl"
[L]  1043  	{te = p;p--;{ found_syllable (use_broken_cluster); buffer->scratch_flags |= HB_BUFFER_SCRATCH_FLAG_HAS_BROKEN_SYLLABLE; }}
[L]  1044  	break;
[ ]  1045  	case 18:
[ ]  1046  #line 178 "hb-ot-shaper-use-machine.rl"
[ ]  1047  	{te = p;p--;{ found_syllable (use_non_cluster); }}
[ ]  1048  	break;
[B]  1049  #line 1014 "hb-ot-shaper-use-machine.hh"
[B]  1050  	}
[ ]  1051  
[B]  1052  _again:
[B]  1053  	switch ( _use_syllable_machine_to_state_actions[cs] ) {
[B]  1054  	case 1:
[B]  1055  #line 1 "NONE"
[B]  1056  	{ts = 0;}
[B]  1057  	break;
[B]  1058  #line 1021 "hb-ot-shaper-use-machine.hh"
[B]  1059  	}
[ ]  1060  
[B]  1061  	if ( ++p != pe )
[B]  1062  		goto _resume;
[B]  1063  	_test_eof: {}
[B]  1064  	if ( p == eof )
[B]  1065  	{
[B]  1066  	if ( _use_syllable_machine_eof_trans[cs] > 0 ) {
[B]  1067  		_trans = _use_syllable_machine_eof_trans[cs] - 1;
[B]  1068  		goto _eof_trans;
[B]  1069  	}
[B]  1070  	}
[ ]  1071  
[B]  1072  	}
[ ]  1073  
[B]  1074  #line 287 "hb-ot-shaper-use-machine.rl"
[ ]  1075  
[B]  1076  }

--- Caller (1 hop): hb-ot-shaper-use.cc:setup_syllables_use(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shaper-use.cc:300-308, calls hb-ot-shaper-use.cc:find_syllables_use(hb_buffer_t*) at line 302) (full body — short) ---
[B]   300  {
[B]   301    HB_BUFFER_ALLOCATE_VAR (buffer, syllable);
[B]   302    find_syllables_use (buffer); <-- CALL
[B]   303    foreach_syllable (buffer, start, end)
[B]   304      buffer->unsafe_to_break (start, end);
[B]   305    setup_rphf_mask (plan, buffer);
[B]   306    setup_topographical_masks (plan, buffer);
[B]   307    return false;
[B]   308  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-use.cc:setup_syllables_use(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:300-308, calls hb-ot-shaper-use.cc:find_syllables_use(hb_buffer_t*) at line 302)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      47       144  hb-ot-shaper-use.cc:is_halant_use(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:356-359)
      43       134  hb-ot-shaper-use.cc:machine_index_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_filter_iter_t<hb_filter_iter_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_array_t<hb_glyph_info_t> >, find_syllables_use(hb_buffer_t*)::{lambda(hb_glyph_info_t const&)#1}, $_31 const&, (void*)0>, find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}, $_9 const&, (void*)0> > >::__prev__()  (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:864-864)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-shaper-use.cc:find_syllables_use(hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:907-1076) ---
  d=1   L 951  T=0 F=4  T=0 F=9  if ( p == pe )
  d=1   L 954  T=44 F=48  T=126 F=135  switch ( _use_syllable_machine_from_state_actions[cs] ) {
  d=1   L 955  T=48 F=44  T=135 F=126  case 2:
  d=1   L 966  T=54 F=38  T=136 F=125  _trans = _inds[ _slen > 0 && _keys[0] <=( (*p).second.sec...
  d=1   L 966  T=92 F=0  T=261 F=0  _trans = _inds[ _slen > 0 && _keys[0] <=( (*p).second.sec...
  d=1   L 967  T=54 F=0  T=136 F=0  ( (*p).second.second.use_category()) <= _keys[1] ?
  d=1   L 973  T=48 F=48  T=135 F=135  if ( _use_syllable_machine_trans_actions[_trans] == 0 )
  d=1   L 976  T=0 F=48  T=0 F=135  switch ( _use_syllable_machine_trans_actions[_trans] ) {
  d=1   L 977  T=0 F=48  T=0 F=135  case 12:
  d=1   L 981  T=0 F=48  T=0 F=135  case 10:
  d=1   L 985  T=0 F=48  T=0 F=135  case 8:
  d=1   L 989  T=0 F=48  T=0 F=135  case 16:
  d=1   L 993  T=4 F=44  T=0 F=135  case 14:  <-- BLOCKER
  d=1   L 997  T=0 F=48  T=0 F=135  case 6:
  d=1   L1001  T=0 F=48  T=0 F=135  case 20:
  d=1   L1005  T=0 F=48  T=1 F=134  case 4:
  d=1   L1009  T=1 F=47  T=0 F=135  case 3:
  d=1   L1013  T=0 F=48  T=0 F=135  case 11:
  d=1   L1017  T=0 F=48  T=0 F=135  case 9:
  d=1   L1021  T=1 F=47  T=10 F=125  case 7:
  d=1   L1025  T=0 F=48  T=0 F=135  case 15:
  d=1   L1029  T=0 F=48  T=0 F=135  case 13:
  d=1   L1033  T=42 F=6  T=123 F=12  case 5:
  d=1   L1037  T=0 F=48  T=0 F=135  case 19:
  d=1   L1041  T=0 F=48  T=1 F=134  case 17:
  d=1   L1045  T=0 F=48  T=0 F=135  case 18:
  d=1   L1053  T=48 F=48  T=135 F=135  switch ( _use_syllable_machine_to_state_actions[cs] ) {
  d=1   L1054  T=48 F=48  T=135 F=135  case 1:
  d=1   L1061  T=88 F=8  T=252 F=18  if ( ++p != pe )
  d=1   L1064  T=8 F=0  T=18 F=0  if ( p == eof )
  d=1   L1066  T=4 F=4  T=9 F=9  if ( _use_syllable_machine_eof_trans[cs] > 0 ) {

[off-chain: 32 additional divergent branches across 14 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=45860a463b0d0161, size=59 bytes, fuzzer=naive, trial=1, discovered_at=5235s, mutation_op=BytesInsertCopyMutator):
  0000: 93 93 a9 00 ef 6c 00 02 ab aa aa 0a 2d 25 00 00   .....l......-%..
  0010: 20 7f dd ff 64 10 01 00 0c 20 00 00 00 6c 00 02    ...d.... ...l..
  0020: ab aa aa 0a 2d 25 00 00 20 7f 0c 00 00 0c 20 00   ....-%.. ..... .
  0030: 00 0c 20 ff fe 02 ff 2d 00 64 03                  .. ....-.d.
Seed 2 (id=da1a7cfae5091572, size=50 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=20545s, mutation_op=QwordAddMutator):
  0000: 00 18 00 00 35 10 00 00 0d 18 00 00 0e 18 00 00   ....5...........
  0010: 00 18 04 00 52 10 01 00 0d 18 00 00 0c 20 00 00   ....R........ ..
  0020: 20 20 6b 12 72 6e 20 20 20 20 0b 0e 06 1a 20 20     k.rn    ....  
  0030: 20 20                                               
Seed 3 (id=c679dc1de8b970bd, size=44 bytes, fuzzer=naive, trial=1, discovered_at=40599s, mutation_op=WordAddMutator,BytesSwapMutator,WordAddMutator,ByteRandMutator):
  0000: 01 02 0c 00 00 21 00 0c 00 00 fe 00 00 0c 20 00   .....!........ .
  0010: 00 00 fe 00 53 10 01 00 0b fe 00 00 00 fe 00 00   ....S...........
  0020: 0c 20 00 00 00 fe 00 00 0c 21 00 00               . .......!..
Seed 4 (id=2d751de852068a11, size=110 bytes, fuzzer=naive, trial=1, discovered_at=78061s, mutation_op=TokenInsert,QwordAddMutator,ByteInterestingMutator):
  0000: 93 93 a9 00 ef 6c 00 02 00 00 00 40 2d 25 00 00   .....l.....@-%..
  0010: 20 02 ab aa aa 0a 2d 25 00 00 20 7f dd ff 83 10    .....-%.. .....
  0020: 01 00 0c 20 00 00 20 7f dd ff 64 10 01 00 0c 18   ... .. ...d.....
  0030: 00 00 0b 18 00 00 0b 18 dd ff 64 10 01 00 0c 18   ..........d.....

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0170cbbd7538578d, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=151s, mutation_op=BytesSetMutator,DwordAddMutator,BytesDeleteMutator,BytesDeleteMutator,WordInterestingMutator,TokenInsert):
  0000: 00 20 97 97 00 00 20 20 00 00 00 00 0c 00 00 02   . ....  ........
  0010: 00 0d 01 00 20 97 97 01 00 3b 3b 3b 3b 3b 73 6e   .... ....;;;;;sn
  0020: 2d 00 3b 3b 3b 3b 3b 02 09 61 72 74 00 01 03 00   -.;;;;;..art....
  0030: 0c 0a 01 02 00 0d 01 00 20                        ........ 
Seed 2 (id=02e04c9299b6e4e1, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=172s, mutation_op=BytesDeleteMutator,BytesDeleteMutator,ByteAddMutator,TokenReplace):
  0000: 00 95 6b 95 20 24 01 03 00 01 00 40 00 03 00 00   ..k. $.....@....
  0010: e0 20 00 00 00 18 00 00 20 b8 48 b8 b8 b8 b8 b8   . ...... .H.....
  0020: b8 b8 b8 06 02 00 80 20 b8                        ....... .
Seed 3 (id=034b3a94b7d5b64d, size=62 bytes, fuzzer=cmplog, trial=1, discovered_at=199s, mutation_op=QwordAddMutator):
  0000: 74 72 75 65 00 00 04 02 65 7f 64 6f 2d 0c 04 02   true....e.do-...
  0010: 02 00 ec 03 03 01 00 02 00 ec ed 1f 20 70 78 2d   ............ px-
  0020: 0e 7c 65 72 20 18 00 00 00 00 0d 06 00 02 02 ff   .|er ...........
  0030: ec 0c 0c 0c 0c 0c 0c 0c 0c 0c ec 22 22 22         ..........."""
Seed 4 (id=02b51d5c1a8c70da, size=53 bytes, fuzzer=cmplog, trial=1, discovered_at=413s, mutation_op=ByteRandMutator,TokenReplace,ByteNegMutator,ByteAddMutator):
  0000: 00 ff 01 00 00 01 00 1a 00 01 00 70 77 63 66 63   ...........pwcfc
  0010: 10 0d 01 00 21 0d 01 00 fd 06 00 00 60 10 00 00   ....!.......`...
  0020: 06 18 00 00 20 10 00 00 52 06 10 00 00 06 20 00   .... ...R..... .
  0030: 00 06 20 00 00                                    .. ..
Seed 5 (id=0335bf1465b48090, size=28 bytes, fuzzer=cmplog, trial=1, discovered_at=859s, mutation_op=BytesSwapMutator,BytesRandInsertMutator):
  0000: 86 18 00 00 00 a6 a6 10 20 10 7f ff ff ff 01 00   ........ .......
  0010: 6e 70 1c c5 17 01 00 16 17 00 80 ff               np..........


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  93(.)x2 00(.)x1 01(.)x1             00(.)x7 74(t)x1 86(.)x1 4f(O)x1     PARTIAL
   0x0001  93(.)x2 18(.)x1 02(.)x1             01(.)x4 20( )x1 95(.)x1 72(r)x1 +3u  PARTIAL
   0x0002  a9(.)x2 00(.)x1 0c(.)x1             00(.)x5 97(.)x1 6b(k)x1 75(u)x1 +2u  PARTIAL
   0x0003  00(.)x4                             00(.)x6 97(.)x1 95(.)x1 65(e)x1 +1u  PARTIAL
   0x0004  ef(.)x2 35(5)x1 00(.)x1             00(.)x9 20( )x1                     PARTIAL
   0x0005  6c(l)x2 10(.)x1 21(!)x1             01(.)x5 00(.)x2 24($)x1 a6(.)x1 +1u  DIFFER
   0x0006  00(.)x4                             20( )x3 07(.)x2 01(.)x1 04(.)x1 +3u  PARTIAL
   0x0007  02(.)x2 00(.)x1 0c(.)x1             20( )x5 03(.)x1 02(.)x1 1a(.)x1 +2u  PARTIAL
   0x0008  00(.)x2 ab(.)x1 0d(.)x1             00(.)x3 20( )x3 21(!)x3 65(e)x1     PARTIAL
   0x0009  00(.)x2 aa(.)x1 18(.)x1             20( )x4 01(.)x2 00(.)x1 7f(.)x1 +2u  PARTIAL
   0x000a  00(.)x2 aa(.)x1 fe(.)x1             00(.)x4 64(d)x1 7f(.)x1 20( )x1 +3u  PARTIAL
   0x000b  00(.)x2 0a(.)x1 40(@)x1             20( )x4 00(.)x1 40(@)x1 6f(o)x1 +3u  PARTIAL
   0x000c  2d(-)x2 0e(.)x1 00(.)x1             47(G)x3 0c(.)x1 00(.)x1 2d(-)x1 +4u  PARTIAL
   0x000d  25(%)x2 18(.)x1 0c(.)x1             00(.)x2 50(P)x2 03(.)x1 0c(.)x1 +4u  PARTIAL
   0x000e  00(.)x3 20( )x1                     00(.)x2 4f(O)x2 04(.)x1 66(f)x1 +4u  PARTIAL
   0x000f  00(.)x4                             02(.)x2 00(.)x2 53(S)x2 63(c)x1 +3u  PARTIAL
   0x0010  20( )x2 00(.)x2                     00(.)x6 e0(.)x1 02(.)x1 10(.)x1 +1u  PARTIAL
   0x0011  7f(.)x1 18(.)x1 00(.)x1 02(.)x1     01(.)x4 0d(.)x2 20( )x1 00(.)x1 +2u  PARTIAL
   0x0012  dd(.)x1 04(.)x1 fe(.)x1 ab(.)x1     00(.)x5 01(.)x2 ec(.)x1 1c(.)x1 +1u  DIFFER
   0x0013  00(.)x2 ff(.)x1 aa(.)x1             00(.)x4 03(.)x1 c5(.)x1 0d(.)x1 +3u  PARTIAL
   0x0014  64(d)x1 52(R)x1 53(S)x1 aa(.)x1     00(.)x5 20( )x1 03(.)x1 21(!)x1 +2u  DIFFER
   0x0015  10(.)x3 0a(.)x1                     00(.)x5 01(.)x2 97(.)x1 18(.)x1 +1u  DIFFER
   0x0016  01(.)x3 2d(-)x1                     00(.)x7 97(.)x1 01(.)x1 02(.)x1     PARTIAL
   0x0017  00(.)x3 25(%)x1                     10(.)x4 00(.)x2 02(.)x2 01(.)x1 +1u  PARTIAL
   0x0018  0c(.)x1 0d(.)x1 0b(.)x1 00(.)x1     00(.)x7 20( )x1 fd(.)x1 17(.)x1     PARTIAL
   0x0019  20( )x1 18(.)x1 fe(.)x1 00(.)x1     02(.)x3 00(.)x2 3b(;)x1 b8(.)x1 +3u  PARTIAL
   0x001a  00(.)x3 20( )x1                     00(.)x6 3b(;)x1 48(H)x1 ed(.)x1 +1u  PARTIAL
   0x001b  00(.)x3 7f(.)x1                     47(G)x3 3b(;)x1 b8(.)x1 1f(.)x1 +4u  PARTIAL
   0x001c  00(.)x2 0c(.)x1 dd(.)x1             00(.)x3 3b(;)x1 b8(.)x1 20( )x1 +3u  PARTIAL
   0x001d  6c(l)x1 20( )x1 fe(.)x1 ff(.)x1     01(.)x2 00(.)x2 3b(;)x1 b8(.)x1 +3u  DIFFER
   0x001e  00(.)x3 83(.)x1                     00(.)x3 73(s)x1 b8(.)x1 78(x)x1 +3u  PARTIAL
   0x001f  00(.)x2 02(.)x1 10(.)x1             00(.)x2 03(.)x2 6e(n)x1 b8(.)x1 +3u  PARTIAL
   0x0020  ab(.)x1 20( )x1 0c(.)x1 01(.)x1     00(.)x3 2d(-)x1 b8(.)x1 0e(.)x1 +3u  PARTIAL
   0x0021  20( )x2 aa(.)x1 00(.)x1             00(.)x5 b8(.)x1 7c(|)x1 18(.)x1 +1u  PARTIAL
   0x0022  aa(.)x1 6b(k)x1 00(.)x1 0c(.)x1     00(.)x5 3b(;)x1 b8(.)x1 65(e)x1 +1u  PARTIAL
   0x0023  0a(.)x1 12(.)x1 00(.)x1 20( )x1     02(.)x3 06(.)x2 3b(;)x1 72(r)x1 +2u  PARTIAL
   0x0024  00(.)x2 2d(-)x1 72(r)x1             4f(O)x3 20( )x2 00(.)x2 3b(;)x1 +1u  PARTIAL
   0x0025  25(%)x1 6e(n)x1 fe(.)x1 00(.)x1     00(.)x5 3b(;)x1 18(.)x1 10(.)x1 +1u  PARTIAL
   0x0026  00(.)x2 20( )x2                     00(.)x7 3b(;)x1 80(.)x1             PARTIAL
   0x0027  00(.)x2 20( )x1 7f(.)x1             10(.)x3 02(.)x2 20( )x2 00(.)x2     PARTIAL
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
  prompts_b/harfbuzz_5983.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5983,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S), value_profile_cmplog>cmplog (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5983 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5983 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5983 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).