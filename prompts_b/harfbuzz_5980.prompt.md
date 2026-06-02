==== BLOCKER ====
Target: harfbuzz
Branch ID: 5980
Location: /src/harfbuzz/src/hb-ot-shaper-use-machine.hh:981:2
Enclosing function: hb-ot-shaper-use.cc:find_syllables_use(hb_buffer_t*)
Source line: 	case 10:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  REFERENCE
cmplog                           0       10          0  loser (value_profile vs value_profile_cmplog)
value_profile                    1        9          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             9        1          0  winner (value_profile vs cmplog); winner (I2S vs value_profile)
naive_ctx                        0       10          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=12.70h  loser=23.60h
  avg hitcount on branch: winner=1  loser=0
  prob_div=0.90  dur_div=10.90h  hit_div=1
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=12.70h  loser=23.80h
  avg hitcount on branch: winner=1  loser=0
  prob_div=0.80  dur_div=11.10h  hit_div=1
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5980/{W,L}/branch_coverage_show.txt

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
[W]   981  	case 10: <-- BLOCKER
[W]   982  #line 171 "hb-ot-shaper-use-machine.rl"
[W]   983  	{te = p+1;{ found_syllable (use_sakot_terminated_cluster); }}
[W]   984  	break;
[L]   985  	case 8:
[L]   986  #line 172 "hb-ot-shaper-use-machine.rl"
[L]   987  	{te = p+1;{ found_syllable (use_standard_cluster); }}
[L]   988  	break;
[ ]   989  	case 16:
[ ]   990  #line 173 "hb-ot-shaper-use-machine.rl"
[ ]   991  	{te = p+1;{ found_syllable (use_number_joiner_terminated_cluster); }}
[ ]   992  	break;
[ ]   993  	case 14:
[ ]   994  #line 174 "hb-ot-shaper-use-machine.rl"
[ ]   995  	{te = p+1;{ found_syllable (use_numeral_cluster); }}
[ ]   996  	break;
[L]   997  	case 6:
[L]   998  #line 175 "hb-ot-shaper-use-machine.rl"
[L]   999  	{te = p+1;{ found_syllable (use_symbol_cluster); }}
[L]  1000  	break;
[ ]  1001  	case 20:
[ ]  1002  #line 176 "hb-ot-shaper-use-machine.rl"
[ ]  1003  	{te = p+1;{ found_syllable (use_hieroglyph_cluster); }}
[ ]  1004  	break;
[L]  1005  	case 4:
[L]  1006  #line 177 "hb-ot-shaper-use-machine.rl"
[L]  1007  	{te = p+1;{ found_syllable (use_broken_cluster); buffer->scratch_flags |= HB_BUFFER_SCRATCH_FLAG_HAS_BROKEN_SYLLABLE; }}
[L]  1008  	break;
[L]  1009  	case 3:
[L]  1010  #line 178 "hb-ot-shaper-use-machine.rl"
[L]  1011  	{te = p+1;{ found_syllable (use_non_cluster); }}
[L]  1012  	break;
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
[L]  1029  	case 13:
[L]  1030  #line 174 "hb-ot-shaper-use-machine.rl"
[L]  1031  	{te = p;p--;{ found_syllable (use_numeral_cluster); }}
[L]  1032  	break;
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
     428     10100  hb-ot-shaper-use.cc:not_ccs_default_ignorable(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:903-903)
     408     10000  hb-ot-shaper-use.cc:find_syllables_use(hb_buffer_t*)::{lambda(hb_glyph_info_t const&)#1}::operator()(hb_glyph_info_t const&) const  (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:912-912)
     416      9860  hb-ot-shaper-use.cc:machine_index_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_filter_iter_t<hb_filter_iter_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_array_t<hb_glyph_info_t> >, find_syllables_use(hb_buffer_t*)::{lambda(hb_glyph_info_t const&)#1}, $_31 const&, (void*)0>, find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}, $_9 const&, (void*)0> > >::__item__() const  (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:859-859)
     408      9460  hb-ot-shaper-use.cc:find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}::operator()(hb_pair_t<unsigned int, hb_glyph_info_t const&>) const  (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:915-921)
     128      3080  hb-ot-shaper-use.cc:machine_index_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_filter_iter_t<hb_filter_iter_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_array_t<hb_glyph_info_t> >, find_syllables_use(hb_buffer_t*)::{lambda(hb_glyph_info_t const&)#1}, $_31 const&, (void*)0>, find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}, $_9 const&, (void*)0> > >::operator==(machine_index_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_filter_iter_t<hb_filter_iter_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_array_t<hb_glyph_info_t> >, find_syllables_use(hb_buffer_t*)::{lambda(hb_glyph_info_t const&)#1}, $_31 const&, (void*)0>, find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}, $_9 const&, (void*)0> > > const&) const  (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:882-882)
     116      2790  hb-ot-shaper-use.cc:machine_index_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_filter_iter_t<hb_filter_iter_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_array_t<hb_glyph_info_t> >, find_syllables_use(hb_buffer_t*)::{lambda(hb_glyph_info_t const&)#1}, $_31 const&, (void*)0>, find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}, $_9 const&, (void*)0> > >::__next__()  (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:862-862)
     116      2790  hb-ot-shaper-use.cc:machine_index_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_filter_iter_t<hb_filter_iter_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_array_t<hb_glyph_info_t> >, find_syllables_use(hb_buffer_t*)::{lambda(hb_glyph_info_t const&)#1}, $_31 const&, (void*)0>, find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}, $_9 const&, (void*)0> > >::operator!=(machine_index_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_filter_iter_t<hb_filter_iter_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_array_t<hb_glyph_info_t> >, find_syllables_use(hb_buffer_t*)::{lambda(hb_glyph_info_t const&)#1}, $_31 const&, (void*)0>, find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}, $_9 const&, (void*)0> > > const&) const  (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:883-883)
     112      2740  hb-ot-shaper-use.cc:machine_index_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_filter_iter_t<hb_filter_iter_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_array_t<hb_glyph_info_t> >, find_syllables_use(hb_buffer_t*)::{lambda(hb_glyph_info_t const&)#1}, $_31 const&, (void*)0>, find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}, $_9 const&, (void*)0> > >::operator=(machine_index_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_filter_iter_t<hb_filter_iter_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_array_t<hb_glyph_info_t> >, find_syllables_use(hb_buffer_t*)::{lambda(hb_glyph_info_t const&)#1}, $_31 const&, (void*)0>, find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}, $_9 const&, (void*)0> > > const&)  (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:875-880)
      72      1750  hb-ot-shaper-use.cc:machine_index_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_filter_iter_t<hb_filter_iter_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_array_t<hb_glyph_info_t> >, find_syllables_use(hb_buffer_t*)::{lambda(hb_glyph_info_t const&)#1}, $_31 const&, (void*)0>, find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}, $_9 const&, (void*)0> > >::machine_index_t(machine_index_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_filter_iter_t<hb_filter_iter_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_array_t<hb_glyph_info_t> >, find_syllables_use(hb_buffer_t*)::{lambda(hb_glyph_info_t const&)#1}, $_31 const&, (void*)0>, find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}, $_9 const&, (void*)0> > > const&)  (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:852-854)
      64      1560  hb-ot-shaper-use.cc:machine_index_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_filter_iter_t<hb_filter_iter_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_array_t<hb_glyph_info_t> >, find_syllables_use(hb_buffer_t*)::{lambda(hb_glyph_info_t const&)#1}, $_31 const&, (void*)0>, find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}, $_9 const&, (void*)0> > >::operator=(unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:868-871)
      64      1530  hb-ot-shaper-use.cc:is_halant_use(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:356-359)
      56      1370  hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:363-442)
      52      1350  hb-ot-shaper-use.cc:machine_index_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_filter_iter_t<hb_filter_iter_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_array_t<hb_glyph_info_t> >, find_syllables_use(hb_buffer_t*)::{lambda(hb_glyph_info_t const&)#1}, $_31 const&, (void*)0>, find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}, $_9 const&, (void*)0> > >::__prev__()  (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:864-864)
       5       176  hb-ot-shaper-use.cc:compose_use(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:483-489)
       8       112  hb-ot-shaper-use.cc:machine_index_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_filter_iter_t<hb_filter_iter_t<hb_zip_iter_t<hb_iota_iter_t<unsigned int, unsigned int>, hb_array_t<hb_glyph_info_t> >, find_syllables_use(hb_buffer_t*)::{lambda(hb_glyph_info_t const&)#1}, $_31 const&, (void*)0>, find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}, $_9 const&, (void*)0> > >::__forward__(unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:863-863)
... (15 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-shaper-use.cc:find_syllables_use(hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:907-1076) ---
  d=1   L 951  T=0 F=4  T=0 F=96  if ( p == pe )
  d=1   L 954  T=56 F=56  T=1330 F=1370  switch ( _use_syllable_machine_from_state_actions[cs] ) {
  d=1   L 955  T=56 F=56  T=1370 F=1330  case 2:
  d=1   L 966  T=64 F=48  T=1440 F=1250  _trans = _inds[ _slen > 0 && _keys[0] <=( (*p).second.sec...
  d=1   L 966  T=112 F=0  T=2700 F=0  _trans = _inds[ _slen > 0 && _keys[0] <=( (*p).second.sec...
  d=1   L 967  T=64 F=0  T=1440 F=0  ( (*p).second.second.use_category()) <= _keys[1] ?
  d=1   L 973  T=60 F=56  T=1420 F=1370  if ( _use_syllable_machine_trans_actions[_trans] == 0 )
  d=1   L 976  T=0 F=56  T=0 F=1370  switch ( _use_syllable_machine_trans_actions[_trans] ) {
  d=1   L 977  T=0 F=56  T=0 F=1370  case 12:
  d=1   L 981  T=4 F=52  T=0 F=1370  case 10:  <-- BLOCKER
  d=1   L 985  T=0 F=56  T=5 F=1360  case 8:
  d=1   L 989  T=0 F=56  T=0 F=1370  case 16:
  d=1   L 993  T=0 F=56  T=0 F=1370  case 14:
  d=1   L 997  T=0 F=56  T=3 F=1360  case 6:
  d=1   L1001  T=0 F=56  T=0 F=1370  case 20:
  d=1   L1005  T=0 F=56  T=3 F=1360  case 4:
  d=1   L1009  T=0 F=56  T=5 F=1360  case 3:
  d=1   L1013  T=0 F=56  T=0 F=1370  case 11:
  d=1   L1017  T=0 F=56  T=0 F=1370  case 9:
  d=1   L1021  T=1 F=55  T=109 F=1260  case 7:
  d=1   L1025  T=0 F=56  T=0 F=1370  case 15:
  d=1   L1029  T=0 F=56  T=1 F=1360  case 13:
  d=1   L1033  T=51 F=5  T=1230 F=135  case 5:
  d=1   L1037  T=0 F=56  T=0 F=1370  case 19:
  d=1   L1041  T=0 F=56  T=9 F=1360  case 17:
  d=1   L1045  T=0 F=56  T=0 F=1370  case 18:
  d=1   L1053  T=60 F=56  T=1420 F=1370  switch ( _use_syllable_machine_to_state_actions[cs] ) {
  d=1   L1054  T=56 F=60  T=1370 F=1420  case 1:
  d=1   L1061  T=108 F=8  T=2600 F=191  if ( ++p != pe )
  d=1   L1064  T=8 F=0  T=191 F=0  if ( p == eof )
  d=1   L1066  T=4 F=4  T=95 F=96  if ( _use_syllable_machine_eof_trans[cs] > 0 ) {

[off-chain: 34 additional divergent branches across 14 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=5542b009878a902b, size=96 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=11610s, mutation_op=BytesRandSetMutator,DwordInterestingMutator,DwordInterestingMutator,BytesExpandMutator,BytesRandSetMutator,ByteRandMutator,CrossoverReplaceMutator):
  0000: 06 05 01 19 b9 05 00 d3 d3 d3 16 16 16 16 16 06   ................
  0010: 25 25 25 26 25 16 25 25 25 25 25 25 25 25 25 25   %%%&%.%%%%%%%%%%
  0020: 25 25 25 25 05 0c 00 20 02 0a 00 be 0c 00 17 0a   %%%%... ........
  0030: 00 b4 05 17 a0 00 00 00 60 1a 00 00 0c 20 00 00   ........`.... ..
Seed 2 (id=27d2b3dce8bac64b, size=92 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=18696s, mutation_op=BitFlipMutator,BytesDeleteMutator):
  0000: 06 05 01 19 b9 05 00 d3 d3 d3 16 16 16 16 16 06   ................
  0010: 25 25 25 26 25 16 25 25 25 25 25 25 05 25 25 25   %%%&%.%%%%%%.%%%
  0020: 25 25 25 25 05 0c 00 20 02 0a 00 be 0c 00 17 0a   %%%%... ........
  0030: 00 b4 05 17 a0 00 00 00 60 1a 00 00 0c 20 00 00   ........`.... ..
Seed 3 (id=be6f6394815703a9, size=72 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=18696s, mutation_op=ByteIncMutator,ByteAddMutator,ByteAddMutator,TokenInsert,ByteRandMutator,BytesDeleteMutator,BytesDeleteMutator):
  0000: 25 25 25 25 25 26 b8 25 05 0c 00 20 02 0a 00 be   %%%%%&.%... ....
  0010: 0c 00 17 0a 00 b4 05 17 a0 00 00 00 60 1a 00 00   ............`...
  0020: 0c 20 00 00 b4 b4 05 00 00 dd b4 05 00 00 05 0a   . ..............
  0030: 00 00 00 b4 00 00 00 00 04 00 4f 54 54 4f 30 25   ..........OTTO0%
Seed 4 (id=7c811dce95cb5654, size=97 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=59703s, mutation_op=BytesDeleteMutator,BytesRandSetMutator,BytesExpandMutator,BytesExpandMutator,TokenReplace,TokenInsert):
  0000: 06 05 01 19 b9 05 00 d3 d3 d3 16 0f 0f 0f 0f 0f   ................
  0010: 0f 0f 0f 0f 25 16 25 25 25 25 25 17 0a 00 b4 05   ....%.%%%%%.....
  0020: 17 a0 00 00 00 60 1a 00 00 0c 20 00 00 b4 b4 05   .....`.... .....
  0030: 20 00 00 b4 b4 05 00 00 00 b4 05 00 00 05 0a 00    ...............

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00a59872e91590a9, size=70 bytes, fuzzer=value_profile, trial=1, discovered_at=11s, mutation_op=ByteNegMutator,BytesInsertMutator,CrossoverReplaceMutator,QwordAddMutator,ByteAddMutator):
  0000: 6e 6e 01 00 00 1f 00 00 00 80 20 00 00 1a 20 20   nn........ ...  
  0010: 20 20 72 01 0b 01 01 01 01 01 b2 16 01 00 01 00     r.............
  0020: 00 00 b2 16 20 74 20 20 22 20 00 00 00 00 00 01   .... t  " ......
  0030: 00 ff 20 00 7f 00 00 80 00 00 00 20 01 00 00 00   .. ........ ....
Seed 2 (id=0254d9f4dd404f17, size=62 bytes, fuzzer=cmplog, trial=2, discovered_at=15s, mutation_op=BytesSetMutator,BytesInsertCopyMutator,BytesInsertCopyMutator,DwordInterestingMutator):
  0000: 04 18 00 00 00 01 0c 00 20 20 20 20 43 50 00 a9   ........    CP..
  0010: 20 20 2a 4c 43 50 00 a9 20 a9 a9 a9 a9 a9 00 00     *LCP.. .......
  0020: 00 00 00 18 20 20 20 20 00 00 64 00 00 00 00 00   ....    ..d.....
  0030: 00 a9 20 20 20 20 02 01 00 18 20 20 20 20         ..    ....    
Seed 3 (id=0120cc83e7ef9ff2, size=18 bytes, fuzzer=cmplog, trial=3, discovered_at=22s, mutation_op=TokenInsert,ByteIncMutator,BytesDeleteMutator,BytesInsertMutator,BytesInsertCopyMutator,WordAddMutator,ByteAddMutator):
  0000: 20 1f 20 20 72 6e 20 20 7f 00 00 00 01 1a 01 00    .  rn  ........
  0010: 00 fe                                             ..
Seed 4 (id=004933ca7f4dadea, size=19 bytes, fuzzer=value_profile, trial=5, discovered_at=23s, mutation_op=ByteFlipMutator,ByteRandMutator,ByteInterestingMutator,TokenInsert):
  0000: 00 ff 64 55 30 12 01 00 00 10 01 00 24 0f df 20   ..dU0.......$.. 
  0010: 1f 20 97                                          . .
Seed 5 (id=0084cd793cb69c13, size=5 bytes, fuzzer=value_profile, trial=1, discovered_at=40s, mutation_op=ByteNegMutator,WordAddMutator,ByteRandMutator,BytesExpandMutator,BytesDeleteMutator,BytesDeleteMutator,TokenReplace):
  0000: e0 0a 01 00 68                                    ....h


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x3 25(%)x1                     00(.)x39 0d(.)x7 20( )x4 74(t)x3 +38u  PARTIAL
   0x0001  05(.)x3 25(%)x1                     01(.)x22 18(.)x15 00(.)x9 20( )x6 +30u  DIFFER
   0x0002  01(.)x3 25(%)x1                     00(.)x47 01(.)x10 20( )x5 10(.)x5 +25u  PARTIAL
   0x0003  19(.)x3 25(%)x1                     00(.)x58 20( )x8 65(e)x2 ff(.)x2 +26u  DIFFER
   0x0004  b9(.)x3 25(%)x1                     00(.)x37 20( )x6 0c(.)x6 4a(J)x4 +37u  DIFFER
   0x0005  05(.)x3 26(&)x1                     01(.)x25 00(.)x11 18(.)x11 20( )x8 +26u  DIFFER
   0x0006  00(.)x3 b8(.)x1                     00(.)x34 01(.)x18 20( )x13 02(.)x6 +20u  PARTIAL
   0x0007  d3(.)x3 25(%)x1                     00(.)x55 20( )x14 02(.)x6 01(.)x3 +18u  DIFFER
   0x0008  d3(.)x3 05(.)x1                     00(.)x32 20( )x10 0c(.)x6 0d(.)x5 +36u  DIFFER
   0x0009  d3(.)x3 0c(.)x1                     20( )x19 00(.)x12 18(.)x11 1a(.)x9 +32u  PARTIAL
   0x000a  16(.)x3 00(.)x1                     00(.)x36 20( )x14 01(.)x10 ff(.)x4 +25u  PARTIAL
   0x000b  16(.)x2 20( )x1 0f(.)x1             00(.)x46 20( )x20 18(.)x2 ff(.)x2 +24u  PARTIAL
   0x000c  16(.)x2 02(.)x1 0f(.)x1             00(.)x23 47(G)x16 0d(.)x6 01(.)x4 +35u  PARTIAL
   0x000d  16(.)x2 0a(.)x1 0f(.)x1             00(.)x16 50(P)x11 18(.)x10 20( )x6 +35u  PARTIAL
   0x000e  16(.)x2 00(.)x1 0f(.)x1             00(.)x29 4f(O)x10 01(.)x9 ff(.)x6 +27u  PARTIAL
   0x000f  06(.)x2 be(.)x1 0f(.)x1             00(.)x35 53(S)x10 20( )x6 42(B)x6 +26u  PARTIAL
   0x0010  25(%)x2 0c(.)x1 0f(.)x1             00(.)x28 20( )x11 82(.)x6 0d(.)x5 +33u  PARTIAL
   0x0011  25(%)x2 00(.)x1 0f(.)x1             00(.)x18 20( )x16 01(.)x10 18(.)x6 +26u  PARTIAL
   0x0012  25(%)x2 17(.)x1 0f(.)x1             00(.)x35 01(.)x11 20( )x6 e0(.)x5 +29u  PARTIAL
   0x0013  26(&)x2 0a(.)x1 0f(.)x1             00(.)x44 20( )x7 0d(.)x3 18(.)x3 +30u  PARTIAL
   0x0014  25(%)x3 00(.)x1                     00(.)x34 0c(.)x6 20( )x4 0b(.)x3 +37u  PARTIAL
   0x0015  16(.)x3 b4(.)x1                     00(.)x27 18(.)x13 20( )x8 01(.)x6 +30u  DIFFER
   0x0016  25(%)x3 05(.)x1                     00(.)x50 01(.)x12 20( )x5 02(.)x3 +20u  DIFFER
   0x0017  25(%)x3 17(.)x1                     00(.)x43 10(.)x7 01(.)x6 20( )x4 +25u  DIFFER
   0x0018  25(%)x3 a0(.)x1                     00(.)x34 20( )x9 0d(.)x6 80(.)x5 +30u  DIFFER
   0x0019  25(%)x3 00(.)x1                     00(.)x20 20( )x7 18(.)x7 02(.)x6 +35u  PARTIAL
   0x001a  25(%)x3 00(.)x1                     00(.)x45 01(.)x4 20( )x3 04(.)x2 +31u  PARTIAL
   0x001b  25(%)x2 00(.)x1 17(.)x1             00(.)x28 20( )x8 47(G)x5 ff(.)x4 +35u  PARTIAL
   0x001c  25(%)x1 05(.)x1 60(`)x1 0a(.)x1     00(.)x19 20( )x8 0d(.)x7 01(.)x5 +40u  PARTIAL
   0x001d  25(%)x2 1a(.)x1 00(.)x1             00(.)x18 20( )x12 18(.)x8 01(.)x5 +32u  PARTIAL
   0x001e  25(%)x2 00(.)x1 b4(.)x1             00(.)x33 01(.)x9 20( )x5 02(.)x3 +27u  PARTIAL
   0x001f  25(%)x2 00(.)x1 05(.)x1             00(.)x35 03(.)x5 01(.)x3 20( )x3 +30u  PARTIAL
   0x0020  25(%)x2 0c(.)x1 17(.)x1             00(.)x29 20( )x5 0c(.)x5 01(.)x3 +33u  PARTIAL
   0x0021  25(%)x2 20( )x1 a0(.)x1             00(.)x21 20( )x8 18(.)x5 0c(.)x3 +37u  PARTIAL
   0x0022  25(%)x2 00(.)x2                     00(.)x38 01(.)x4 02(.)x3 53(S)x3 +32u  PARTIAL
   0x0023  25(%)x2 00(.)x2                     00(.)x30 20( )x5 02(.)x5 ff(.)x3 +36u  PARTIAL
   0x0024  05(.)x2 b4(.)x1 00(.)x1             00(.)x24 20( )x8 4f(O)x5 01(.)x3 +36u  PARTIAL
   0x0025  0c(.)x2 b4(.)x1 60(`)x1             00(.)x32 20( )x4 18(.)x3 0c(.)x3 +36u  PARTIAL
   0x0026  00(.)x2 05(.)x1 1a(.)x1             00(.)x29 20( )x6 01(.)x6 32(2)x3 +30u  PARTIAL
   0x0027  20( )x2 00(.)x2                     00(.)x26 20( )x6 01(.)x5 10(.)x5 +28u  PARTIAL
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
  prompts_b/harfbuzz_5980.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5980,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5980 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5980 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5980 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).