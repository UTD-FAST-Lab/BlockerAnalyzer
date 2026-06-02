==== BLOCKER ====
Target: harfbuzz
Branch ID: 5913
Location: /src/harfbuzz/src/hb-ot-shaper-khmer-machine.hh:369:2
Enclosing function: find_syllables_khmer(hb_buffer_t*)
Source line: 	case 3:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           2        8          0  loser (I2S vs naive)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             5        5          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=1.10h  loser=19.60h
  avg hitcount on branch: winner=50  loser=0
  prob_div=0.80  dur_div=18.50h  hit_div=50
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5913/{W,L}/branch_coverage_show.txt

--- Enclosing function: find_syllables_khmer(hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shaper-khmer-machine.hh:292-424) ---
[ ]   290  inline void
[ ]   291  find_syllables_khmer (hb_buffer_t *buffer)
[B]   292  {
[B]   293    unsigned int p, pe, eof, ts, te, act HB_UNUSED;
[B]   294    int cs;
[B]   295    hb_glyph_info_t *info = buffer->info;
[ ]   296    
[B]   297  #line 287 "hb-ot-shaper-khmer-machine.hh"
[B]   298  	{
[B]   299  	cs = khmer_syllable_machine_start;
[B]   300  	ts = 0;
[B]   301  	te = 0;
[B]   302  	act = 0;
[B]   303  	}
[ ]   304  
[B]   305  #line 122 "hb-ot-shaper-khmer-machine.rl"
[ ]   306  
[ ]   307  
[B]   308    p = 0;
[B]   309    pe = eof = buffer->len;
[ ]   310  
[B]   311    unsigned int syllable_serial = 1;
[ ]   312    
[B]   313  #line 299 "hb-ot-shaper-khmer-machine.hh"
[B]   314  	{
[B]   315  	int _slen;
[B]   316  	int _trans;
[B]   317  	const unsigned char *_keys;
[B]   318  	const char *_inds;
[B]   319  	if ( p == pe )
[ ]   320  		goto _test_eof;
[B]   321  _resume:
[B]   322  	switch ( _khmer_syllable_machine_from_state_actions[cs] ) {
[B]   323  	case 7:
[B]   324  #line 1 "NONE"
[B]   325  	{ts = p;}
[B]   326  	break;
[B]   327  #line 311 "hb-ot-shaper-khmer-machine.hh"
[B]   328  	}
[ ]   329  
[B]   330  	_keys = _khmer_syllable_machine_trans_keys + (cs<<1);
[B]   331  	_inds = _khmer_syllable_machine_indicies + _khmer_syllable_machine_index_offsets[cs];
[ ]   332  
[B]   333  	_slen = _khmer_syllable_machine_key_spans[cs];
[B]   334  	_trans = _inds[ _slen > 0 && _keys[0] <=( info[p].khmer_category()) &&
[B]   335  		( info[p].khmer_category()) <= _keys[1] ?
[B]   336  		( info[p].khmer_category()) - _keys[0] : _slen ];
[ ]   337  
[B]   338  _eof_trans:
[B]   339  	cs = _khmer_syllable_machine_trans_targs[_trans];
[ ]   340  
[B]   341  	if ( _khmer_syllable_machine_trans_actions[_trans] == 0 )
[W]   342  		goto _again;
[ ]   343  
[B]   344  	switch ( _khmer_syllable_machine_trans_actions[_trans] ) {
[B]   345  	case 2:
[B]   346  #line 1 "NONE"
[B]   347  	{te = p+1;}
[B]   348  	break;
[B]   349  	case 8:
[B]   350  #line 98 "hb-ot-shaper-khmer-machine.rl"
[B]   351  	{te = p+1;{ found_syllable (khmer_non_khmer_cluster); }}
[B]   352  	break;
[B]   353  	case 10:
[B]   354  #line 96 "hb-ot-shaper-khmer-machine.rl"
[B]   355  	{te = p;p--;{ found_syllable (khmer_consonant_syllable); }}
[B]   356  	break;
[B]   357  	case 11:
[B]   358  #line 97 "hb-ot-shaper-khmer-machine.rl"
[B]   359  	{te = p;p--;{ found_syllable (khmer_broken_cluster); buffer->scratch_flags |= HB_BUFFER_SCRATCH_FLAG_HAS_BROKEN_SYLLABLE; }}
[B]   360  	break;
[ ]   361  	case 12:
[ ]   362  #line 98 "hb-ot-shaper-khmer-machine.rl"
[ ]   363  	{te = p;p--;{ found_syllable (khmer_non_khmer_cluster); }}
[ ]   364  	break;
[W]   365  	case 1:
[W]   366  #line 96 "hb-ot-shaper-khmer-machine.rl"
[W]   367  	{{p = ((te))-1;}{ found_syllable (khmer_consonant_syllable); }}
[W]   368  	break;
[W]   369  	case 3: <-- BLOCKER
[W]   370  #line 97 "hb-ot-shaper-khmer-machine.rl"
[W]   371  	{{p = ((te))-1;}{ found_syllable (khmer_broken_cluster); buffer->scratch_flags |= HB_BUFFER_SCRATCH_FLAG_HAS_BROKEN_SYLLABLE; }}
[W]   372  	break;
[ ]   373  	case 5:
[ ]   374  #line 1 "NONE"
[ ]   375  	{	switch( act ) {
[ ]   376  	case 2:
[ ]   377  	{{p = ((te))-1;} found_syllable (khmer_broken_cluster); buffer->scratch_flags |= HB_BUFFER_SCRATCH_FLAG_HAS_BROKEN_SYLLABLE; }
[ ]   378  	break;
[ ]   379  	case 3:
[ ]   380  	{{p = ((te))-1;} found_syllable (khmer_non_khmer_cluster); }
[ ]   381  	break;
[ ]   382  	}
[ ]   383  	}
[ ]   384  	break;
[W]   385  	case 4:
[W]   386  #line 1 "NONE"
[W]   387  	{te = p+1;}
[W]   388  #line 97 "hb-ot-shaper-khmer-machine.rl"
[W]   389  	{act = 2;}
[W]   390  	break;
[ ]   391  	case 9:
[ ]   392  #line 1 "NONE"
[ ]   393  	{te = p+1;}
[ ]   394  #line 98 "hb-ot-shaper-khmer-machine.rl"
[ ]   395  	{act = 3;}
[ ]   396  	break;
[B]   397  #line 368 "hb-ot-shaper-khmer-machine.hh"
[B]   398  	}
[ ]   399  
[B]   400  _again:
[B]   401  	switch ( _khmer_syllable_machine_to_state_actions[cs] ) {
[B]   402  	case 6:
[B]   403  #line 1 "NONE"
[B]   404  	{ts = 0;}
[B]   405  	break;
[B]   406  #line 375 "hb-ot-shaper-khmer-machine.hh"
[B]   407  	}
[ ]   408  
[B]   409  	if ( ++p != pe )
[B]   410  		goto _resume;
[B]   411  	_test_eof: {}
[B]   412  	if ( p == eof )
[B]   413  	{
[B]   414  	if ( _khmer_syllable_machine_eof_trans[cs] > 0 ) {
[B]   415  		_trans = _khmer_syllable_machine_eof_trans[cs] - 1;
[B]   416  		goto _eof_trans;
[B]   417  	}
[B]   418  	}
[ ]   419  
[B]   420  	}
[ ]   421  
[B]   422  #line 130 "hb-ot-shaper-khmer-machine.rl"
[ ]   423  
[B]   424  }

--- Caller (1 hop): hb-ot-shaper-khmer.cc:setup_syllables_khmer(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shaper-khmer.cc:199-205, calls find_syllables_khmer(hb_buffer_t*) at line 201) (full body — short) ---
[B]   199  {
[B]   200    HB_BUFFER_ALLOCATE_VAR (buffer, syllable);
[B]   201    find_syllables_khmer (buffer); <-- CALL
[B]   202    foreach_syllable (buffer, start, end)
[B]   203      buffer->unsafe_to_break (start, end);
[B]   204    return false;
[B]   205  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-khmer.cc:setup_syllables_khmer(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-khmer.cc:199-205, calls find_syllables_khmer(hb_buffer_t*) at line 201)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      75         7  hb-ot-shaper-khmer.cc:compose_khmer(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-khmer.cc:359-365)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  find_syllables_khmer(hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-khmer-machine.hh:292-424) ---
  d=1   L 335  T=95 F=0  T=18 F=2  ( info[p].khmer_category()) <= _keys[1] ?
  d=1   L 341  T=31 F=181  T=0 F=177  if ( _khmer_syllable_machine_trans_actions[_trans] == 0 )
  d=1   L 365  T=1 F=180  T=0 F=177  case 1:
  d=1   L 369  T=12 F=169  T=0 F=177  case 3:  <-- BLOCKER
  d=1   L 385  T=18 F=163  T=0 F=177  case 4:

[off-chain: 8 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=5b7de4009fc79bde, size=155 bytes, fuzzer=naive, trial=1, discovered_at=2265s, mutation_op=DwordAddMutator,BytesRandSetMutator,ByteAddMutator):
  0000: cb 0c 00 00 cb 0b 1d 00 16 66 65 7a 68 2d 68 61   .........fezh-ha
  0010: 6e 73 00 00 00 20 57 96 97 20 20 20 7a 5f 7c 7c   ns... W..   z_||
  0020: 7c 8b 7c 7c 7c 7c 7c 7c 7c 7c 7c 9b 7c 68 00 00   |.|||||||||.|h..
  0030: cb 0e 00 bf cc 05 00 00 00 0c 00 00 cc 0e 03 00   ................
Seed 2 (id=b6733a80ed4f929d, size=155 bytes, fuzzer=naive, trial=1, discovered_at=2289s, mutation_op=TokenReplace,BitFlipMutator,ByteAddMutator):
  0000: cb 0c 00 00 cb 0b 00 00 16 66 65 7a 68 2d 68 61   .........fezh-ha
  0010: 6e 73 00 00 00 20 57 96 97 20 20 20 7a 5f 7c 7c   ns... W..   z_||
  0020: 7c 8b 7c 7c 7c 7c 7c 7c 7c 7c 7c 9b 7c 68 00 00   |.|||||||||.|h..
  0030: cb 0e 00 bf cc 05 00 00 00 0c 00 00 cc 0e 03 00   ................
Seed 3 (id=21cb30c974bc60a2, size=139 bytes, fuzzer=naive, trial=1, discovered_at=2312s, mutation_op=BitFlipMutator,BytesRandSetMutator,TokenInsert,TokenReplace):
  0000: 8b 7c 7c 7c 7c 7c 7c 7c 7c 7c 9b 7c 00 00 00 fe   .|||||||||.|....
  0010: fe fe fe 00 05 00 00 00 0c 00 01 cc 0e 03 00 16   ................
  0020: 66 65 ff 00 bf cc 05 00 00 00 0c 00 01 cc ed 02   fe..............
  0030: 00 16 66 65 75 75 2d 68 61 6e 74 2d 68 6b 00 0c   ..feuu-hant-hk..
Seed 4 (id=692a9706769fdc4b, size=102 bytes, fuzzer=naive, trial=1, discovered_at=10802s, mutation_op=BytesDeleteMutator):
  0000: 00 59 00 59 10 00 00 59 6b 72 61 6d 10 00 00 24   .Y.Y...Ykram...$
  0010: 49 92 04 59 10 00 00 59 10 00 00 59 10 00 00 59   I..Y...Y...Y...Y
  0020: 10 0e 03 0e 00 00 1a 05 ff e6 cf 17 00 00 d2 17   ................
  0030: 00 00 4e 7f ff 00 b8 b8 00 00 00 00 00 00 00 00   ..N.............
Seed 5 (id=7e8aa711252f145b, size=202 bytes, fuzzer=naive, trial=1, discovered_at=12728s, mutation_op=ByteDecMutator,BytesRandInsertMutator,BytesRandInsertMutator,BytesSwapMutator,ByteDecMutator):
  0000: cb 0c 00 00 cb 0b 00 00 16 66 65 7a 68 2d 67 61   .........fezh-ga
  0010: 6e 73 00 00 00 20 a9 96 97 20 20 20 7a 5f f0 3c   ns... ...   z_.<
  0020: f5 e0 20 00 bf 72 00 e7 99 99 99 99 99 61 61 61   .. ..r.......aaa
  0030: 61 61 61 61 61 61 61 61 99 99 99 99 99 99 99 e7   aaaaaaaa........

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0509f37188b3277c, size=45 bytes, fuzzer=cmplog, trial=1, discovered_at=57s, mutation_op=DwordAddMutator,CrossoverReplaceMutator):
  0000: e2 17 00 00 01 e2 17 00 00 00 04 20 23 00 00 01   ........... #...
  0010: 20 2c 20 20 20 f6 e2 e2 e2 e2 e2 e2 e2 00 00 00    ,   ...........
  0020: 1e 0d 00 00 01 21 04 00 1a 20 e0 a0 20            .....!... .. 
Seed 2 (id=0218f5a2fd89b4cc, size=76 bytes, fuzzer=cmplog, trial=1, discovered_at=138s, mutation_op=TokenReplace,WordInterestingMutator):
  0000: 00 00 00 16 00 7f 20 00 00 16 00 7f 20 01 00 80   ...... ..... ...
  0010: 1a 00 01 20 38 20 20 20 20 6b 20 20 6b 65 72 6e   ... 8    k  kern
  0020: 20 20 00 00 00 01 20 20 20 20 ff ff 9e 17 00 00     ....    ......
  0030: 00 01 20 38 20 20 20 20 6b 20 6d 6e 2d 00 6e 20   .. 8    k mn-.n 
Seed 3 (id=06c512ef6289de25, size=40 bytes, fuzzer=cmplog, trial=1, discovered_at=209s, mutation_op=BytesDeleteMutator,BytesInsertCopyMutator,ByteDecMutator,BytesSetMutator,BytesInsertMutator,DwordInterestingMutator,BytesInsertMutator):
  0000: f6 17 00 00 2c 00 00 00 00 00 00 00 f6 17 00 00   ....,...........
  0010: 2c 2c 2c 2c 2c 2c 20 23 03 00 00 20 2c 20 20 20   ,,,,,, #... ,   
  0020: f6 00 80 ff ff e2 e1 e2                           ........
Seed 4 (id=0c3654af6740e537, size=47 bytes, fuzzer=cmplog, trial=1, discovered_at=308s, mutation_op=ByteDecMutator,DwordAddMutator,ByteInterestingMutator,ByteIncMutator,BytesSetMutator,BytesInsertCopyMutator):
  0000: e2 17 00 00 01 e2 00 00 00 28 00 00 0a 00 01 00   .........(......
  0010: 01 00 ff 00 00 17 00 00 01 01 20 20 00 ff 01 20   ..........  ... 
  0020: 2c 00 00 00 00 00 00 00 00 00 00 00 00 00 00      ,..............
Seed 5 (id=014331d1dcf5dc8a, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=318s, mutation_op=ByteIncMutator,BytesRandInsertMutator,ByteDecMutator):
  0000: e2 17 00 00 01 4f 54 54 4f 00 04 20 23 00 00 01   .....OTTO.. #...
  0010: 20 2c 20 20 20 f6 e2 e2 e2 e2 e2 e1 e2 1d 00 22    ,   .........."
  0020: 30 30 30 30 30 30 30 30 30 30 30 30 a0 00 00 00   000000000000....
  0030: 00 21 04 00 1b 20 e0 a0 20                        .!... .. 


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x5 cb(.)x3 8b(.)x1 b4(.)x1     e2(.)x3 00(.)x2 f6(.)x1 13(.)x1 +3u  PARTIAL
   0x0001  00(.)x5 0c(.)x3 7c(|)x1 59(Y)x1     17(.)x6 00(.)x1 20( )x1 de(.)x1 +1u  PARTIAL
   0x0002  00(.)x4 cc(.)x3 7c(|)x1 eb(.)x1 +1u  00(.)x8 13(.)x1 20( )x1             PARTIAL
   0x0003  00(.)x3 0e(.)x3 7c(|)x1 59(Y)x1 +2u  00(.)x7 16(.)x1 9e(.)x1 10(.)x1     PARTIAL
   0x0006  00(.)x6 20( )x2 1d(.)x1 7c(|)x1     00(.)x3 17(.)x2 20( )x2 54(T)x1 +2u  PARTIAL
   0x0008  16(.)x3 65(e)x3 7c(|)x1 6b(k)x1 +2u  00(.)x5 20( )x3 4f(O)x1 12(.)x1     PARTIAL
   0x000b  7a(z)x3 00(.)x3 7c(|)x1 6d(m)x1 +2u  20( )x5 00(.)x4 7f(.)x1             PARTIAL
   0x000f  61(a)x3 00(.)x2 fe(.)x1 24($)x1 +3u  00(.)x5 01(.)x3 80(.)x1 48(H)x1     PARTIAL
   0x0013  00(.)x6 61(a)x2 59(Y)x1 4e(N)x1     00(.)x4 20( )x3 2c(,)x1 a2(.)x1 +1u  PARTIAL
   0x0027  00(.)x3 7c(|)x2 05(.)x1 e7(.)x1 +3u  00(.)x5 20( )x3 e2(.)x1 30(0)x1     PARTIAL
   0x002f  00(.)x3 02(.)x1 17(.)x1 61(a)x1 +4u  00(.)x5 0c(.)x1 ff(.)x1             PARTIAL
   0x0035  05(.)x2 75(u)x1 00(.)x1 61(a)x1 +5u  20( )x3 00(.)x2 26(&)x1             PARTIAL
   0x0039  0c(.)x2 00(.)x2 6e(n)x1 99(.)x1 +4u  20( )x3 26(&)x1 17(.)x1             PARTIAL
   0x003b  00(.)x4 2d(-)x1 99(.)x1 61(a)x1 +3u  00(.)x2 6e(n)x1 20( )x1 0c(.)x1     PARTIAL
   0x003c  cc(.)x2 68(h)x1 00(.)x1 99(.)x1 +5u  00(.)x3 2d(-)x1 4d(M)x1             PARTIAL
   0x003d  0e(.)x2 17(.)x2 6b(k)x1 00(.)x1 +4u  00(.)x3 65(e)x1 c5(.)x1             PARTIAL
   0x003f  00(.)x6 0c(.)x1 e7(.)x1 4e(N)x1     20( )x1 6e(n)x1 00(.)x1 03(.)x1 +1u  PARTIAL
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
  prompts_b/harfbuzz_5913.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5913,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5913 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5913 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5913 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).