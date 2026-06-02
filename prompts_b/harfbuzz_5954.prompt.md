==== BLOCKER ====
Target: harfbuzz
Branch ID: 5954
Location: /src/harfbuzz/src/hb-ot-shaper-thai.cc:53:39
Enclosing function: hb-ot-shaper-thai.cc:get_consonant_type(unsigned int)
Source line:   if (u == 0x0E1Bu || u == 0x0E1Du || u == 0x0E1Fu/* || u == 0x0E2Cu*/)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           0       10          0  loser (I2S vs naive)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             4        6          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         7        3          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=1.50h  loser=22.00h
  avg hitcount on branch: winner=36  loser=0
  prob_div=1.00  dur_div=20.50h  hit_div=36
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5954/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-thai.cc:get_consonant_type(unsigned int) (/src/harfbuzz/src/hb-ot-shaper-thai.cc:52-62) ---
[ ]    50  static thai_consonant_type_t
[ ]    51  get_consonant_type (hb_codepoint_t u)
[B]    52  {
[B]    53    if (u == 0x0E1Bu || u == 0x0E1Du || u == 0x0E1Fu/* || u == 0x0E2Cu*/) <-- BLOCKER
[W]    54      return AC;
[B]    55    if (u == 0x0E0Du || u == 0x0E10u)
[L]    56      return RC;
[B]    57    if (u == 0x0E0Eu || u == 0x0E0Fu)
[L]    58      return DC;
[B]    59    if (hb_in_range<hb_codepoint_t> (u, 0x0E01u, 0x0E2Eu))
[L]    60      return NC;
[B]    61    return NOT_CONSONANT;
[B]    62  }

--- Caller (1 hop): hb-ot-shaper-thai.cc:do_thai_pua_shaping(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) (/src/harfbuzz/src/hb-ot-shaper-thai.cc:224-261, calls hb-ot-shaper-thai.cc:get_consonant_type(unsigned int) at line 240) (full body — short) ---
[B]   224  {
[ ]   225  #ifdef HB_NO_OT_SHAPER_THAI_FALLBACK
[ ]   226    return;
[ ]   227  #endif
[ ]   228  
[B]   229    thai_above_state_t above_state = thai_above_start_state[NOT_CONSONANT];
[B]   230    thai_below_state_t below_state = thai_below_start_state[NOT_CONSONANT];
[B]   231    unsigned int base = 0;
[ ]   232  
[B]   233    hb_glyph_info_t *info = buffer->info;
[B]   234    unsigned int count = buffer->len;
[B]   235    for (unsigned int i = 0; i < count; i++)
[B]   236    {
[B]   237      thai_mark_type_t mt = get_mark_type (info[i].codepoint);
[ ]   238  
[B]   239      if (mt == NOT_MARK) {
[B]   240        thai_consonant_type_t ct = get_consonant_type (info[i].codepoint); <-- CALL
[B]   241        above_state = thai_above_start_state[ct];
[B]   242        below_state = thai_below_start_state[ct];
[B]   243        base = i;
[B]   244        continue;
[B]   245      }
[ ]   246  
[B]   247      const thai_above_state_machine_edge_t &above_edge = thai_above_state_machine[above_state][mt];
[B]   248      const thai_below_state_machine_edge_t &below_edge = thai_below_state_machine[below_state][mt];
[B]   249      above_state = above_edge.next_state;
[B]   250      below_state = below_edge.next_state;
[ ]   251  
[ ]   252      /* At least one of the above/below actions is NOP. */
[B]   253      thai_action_t action = above_edge.action != NOP ? above_edge.action : below_edge.action;
[ ]   254  
[B]   255      buffer->unsafe_to_break (base, i);
[B]   256      if (action == RD)
[ ]   257        info[base].codepoint = thai_pua_shape (info[base].codepoint, action, font);
[B]   258      else
[B]   259        info[i].codepoint = thai_pua_shape (info[i].codepoint, action, font);
[B]   260    }
[B]   261  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-thai.cc:do_thai_pua_shaping(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-thai.cc:224-261, calls hb-ot-shaper-thai.cc:get_consonant_type(unsigned int) at line 240)
hop 3  hb-ot-shaper-thai.cc:preprocess_text_thai(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-thai.cc:268-372, calls hb-ot-shaper-thai.cc:do_thai_pua_shaping(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) at line 371)

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ot-shaper-thai.cc:do_thai_pua_shaping(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-thai.cc:224-261) ---
  d=2   L 253  T=5 F=28  T=0 F=13  thai_action_t action = above_edge.action != NOP ? above_e...
  d=2   L 256  T=0 F=33  T=0 F=13  if (action == RD)
--- d=1  hb-ot-shaper-thai.cc:get_consonant_type(unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-thai.cc:52-62) ---
  d=1   L  53  T=20 F=108  T=0 F=148  if (u == 0x0E1Bu || u == 0x0E1Du || u == 0x0E1Fu/* || u =...  <-- BLOCKER
  d=1   L  55  T=0 F=108  T=1 F=147  if (u == 0x0E0Du || u == 0x0E10u)
  d=1   L  57  T=0 F=108  T=1 F=146  if (u == 0x0E0Eu || u == 0x0E0Fu)
  d=1   L  59  T=0 F=108  T=3 F=143  if (hb_in_range<hb_codepoint_t> (u, 0x0E01u, 0x0E2Eu))

[off-chain: 12 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=34de298072a6ad88, size=88 bytes, fuzzer=naive, trial=1, discovered_at=337s, mutation_op=ByteRandMutator,BytesCopyMutator):
  0000: 00 00 15 03 00 00 00 e6 ff 00 00 00 00 00 00 00   ................
  0010: 00 00 ff ff ff 68 00 00 e8 c3 01 fd ff ff ff cb   .....h..........
  0020: d3 cb 97 97 00 00 97 00 1f 0e 00 00 48 61 0c 18   ............Ha..
  0030: 00 00 97 00 3a 0e 00 00 48 61 0c 18 00 00 65 72   ....:...Ha....er
Seed 2 (id=3d9a93d4f5d272b7, size=76 bytes, fuzzer=naive, trial=1, discovered_at=485s, mutation_op=BytesInsertCopyMutator,BytesInsertMutator,ByteInterestingMutator):
  0000: ff ff ff 68 14 0c 18 ff ff ff 68 14 0c 18 00 80   ...h......h.....
  0010: 00 00 00 0e 00 00 e8 c3 3a 3a 3a 01 fd ff ff ff   ........:::.....
  0020: cb 00 97 ff ff ff ff ff ff ff ff 00 3a 0e 00 00   ............:...
  0030: 3a 0e 00 00 d3 cb 97 97 00 00 97 40 1f 0e 00 00   :..........@....
Seed 3 (id=37b54b60e3a87fc7, size=107 bytes, fuzzer=naive, trial=1, discovered_at=960s, mutation_op=BytesDeleteMutator):
  0000: 00 ff 00 45 4e 4a 4e 4e 4e 61 4e 65 94 06 65 00   ...ENJNNNaNe..e.
  0010: 4e 4e 4e 4e 1a 4e 00 00 4e 06 00 00 5b 06 4e 4e   NNNN.N..N...[.NN
  0020: 4e 4e 4e 1a 4e 00 00 4e 06 00 00 5b 16 00 65 7a   NNN.N..N...[..ez
  0030: 69 73 00 4e 0e 00 00 cb 06 4e 4e 1a 4e 00 00 4e   is.N.....NN.N..N
Seed 4 (id=6b273bb9c9e1dcf2, size=122 bytes, fuzzer=naive, trial=1, discovered_at=960s, mutation_op=ByteNegMutator,ByteInterestingMutator,ByteNegMutator,BytesRandInsertMutator):
  0000: 00 ff 00 45 4e 4a 4e 4e 4e 61 4e 65 94 fa 65 00   ...ENJNNNaNe..e.
  0010: 4e 4e 4e 4e 1a 4e 00 00 4e 06 00 00 5b 06 4e 4e   NNNN.N..N...[.NN
  0020: 4e 4e 4e 1a 4e 00 00 4e 06 00 00 5b 16 00 65 7a   NNN.N..N...[..ez
  0030: 69 73 00 4e 0e 00 00 cb 06 4e 4e 1a 4e 00 00 4e   is.N.....NN.N..N
Seed 5 (id=58f94c3f9d11aa6c, size=76 bytes, fuzzer=naive, trial=1, discovered_at=2800s, mutation_op=BytesRandSetMutator,BytesExpandMutator):
  0000: df df df df df 06 4e 00 00 00 00 00 1f 0e 00 00   ......N.........
  0010: 4e 06 00 1f 31 0e 00 00 4e 06 00 1f 31 0e 00 00   N...1...N...1...
  0020: 4e 06 00 1f 31 0e 00 00 4e 06 00 1f 31 0e 00 00   N...1...N...1...
  0030: 4e 06 4e 00 00 00 00 00 1f 0e 00 00 4e 06 00 1f   N.N.........N...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=37f8e71ac2ac9677, size=21 bytes, fuzzer=cmplog, trial=1, discovered_at=163s, mutation_op=BytesInsertCopyMutator):
  0000: 05 0d 01 74 05 0d 01 74 ba c0 22 06 38 0e 00 00   ...t...t..".8...
  0010: 00 00 ff 40 20                                    ...@ 
Seed 2 (id=0568144a6b4b248e, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=246s, mutation_op=TokenInsert,QwordAddMutator,BytesSetMutator,ByteInterestingMutator,TokenInsert,WordAddMutator,WordAddMutator):
  0000: 00 01 40 9b 14 01 20 6e 6e 00 1b 1b 1b 1b 1b 1b   ..@... nn.......
  0010: 1b 1b 70 67 6c 73 1b 1b 20 20 20 6b 34 0e 00 00   ..pgls..   k4...
  0020: 05 65 72 6f 25 49 92 04 20 00 1b 1b 1b ff ff fb   .ero%I.. .......
  0030: 01 00 04 dd 0f 0e 00 00 05                        .........
Seed 3 (id=12c176717291bd3c, size=61 bytes, fuzzer=cmplog, trial=1, discovered_at=246s, mutation_op=WordInterestingMutator,ByteAddMutator,BytesRandInsertMutator):
  0000: 00 01 40 9b ff ff ff 1f 6e 1b 1b 1b 1b 1b 1b 1b   ..@.....n.......
  0010: 1b 1b 1b 1b 20 20 20 60 08 0e 00 00 05 65 72 6f   ....   `.....ero
  0020: 20 00 0f 20 cd cd cd cd ea 6e 70 2d 68 61 6e 74    .. .....np-hant
  0030: 00 ff ff fb 00 00 04 00 10 0e 00 00 05            .............
Seed 4 (id=0dbfc616ba80cfe4, size=76 bytes, fuzzer=cmplog, trial=1, discovered_at=972s, mutation_op=BytesDeleteMutator):
  0000: ff fc 00 00 5a 5b 5a 5a 5a 5a 5a 48 00 fe ff 00   ....Z[ZZZZZH....
  0010: 00 01 ff 0f d6 03 1b 20 4d 0e 00 00 34 1d 17 ff   ....... M...4...
  0020: 00 ff fc 00 00 5a 5b 5a 5a 5a 5a 5a 48 00 00 00   .....Z[ZZZZZH...
  0030: 34 0e 4d 0e 00 00 34 20 01 04 4d 0e 4d 0e 00 20   4.M...4 ..M.M.. 
Seed 5 (id=1789cc0d2b4c5f5c, size=78 bytes, fuzzer=cmplog, trial=1, discovered_at=972s, mutation_op=BytesExpandMutator,ByteDecMutator,ByteRandMutator):
  0000: 00 00 00 10 5a 5b 5a 5a 5a 63 5a 48 00 fe ff 00   ....Z[ZZZcZH....
  0010: 00 01 ff 0f 0e 03 1b 20 4d 0e 00 00 34 e2 17 ff   ....... M...4...
  0020: 00 5b 5b 5b 01 00 01 01 20 20 01 04 6b 0e 00 00   .[[[....  ..k...
  0030: 33 0e 4d 0e 00 00 34 20 01 04 4d 0e 00 00 3a 0e   3.M...4 ..M...:.


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x5 ff(.)x1 df(.)x1 5b([)x1 +2u  00(.)x7 05(.)x1 ff(.)x1 4f(O)x1     PARTIAL
   0x0002  00(.)x7 15(.)x1 ff(.)x1 df(.)x1     00(.)x6 40(@)x2 01(.)x1 54(T)x1     PARTIAL
   0x0006  4e(N)x6 00(.)x2 18(.)x1 92(.)x1     20( )x5 5a(Z)x2 01(.)x1 ff(.)x1 +1u  DIFFER
   0x000b  65(e)x5 00(.)x3 14(.)x1 cb(.)x1     20( )x4 1b(.)x3 48(H)x2 06(.)x1     DIFFER
   0x000e  65(e)x5 00(.)x4 cb(.)x1             1b(.)x2 ff(.)x2 54(T)x2 55(U)x2 +2u  PARTIAL
   0x000f  00(.)x8 80(.)x1 cb(.)x1             00(.)x3 1b(.)x2 48(H)x2 42(B)x2 +1u  PARTIAL
   0x0010  4e(N)x5 00(.)x3 cb(.)x2             00(.)x8 1b(.)x2                     PARTIAL
   0x0011  4e(N)x4 00(.)x3 06(.)x2 70(p)x1     01(.)x6 1b(.)x2 00(.)x1 7f(.)x1     PARTIAL
   0x0012  4e(N)x6 00(.)x2 ff(.)x1 6d(m)x1     00(.)x5 ff(.)x3 70(p)x1 1b(.)x1     PARTIAL
   0x0015  4e(N)x4 68(h)x1 00(.)x1 0e(.)x1 +3u  00(.)x5 03(.)x2 73(s)x1 20( )x1     PARTIAL
   0x0016  00(.)x6 e8(.)x1 89(.)x1 cb(.)x1 +1u  00(.)x4 1b(.)x3 20( )x1 ff(.)x1     PARTIAL
   0x001e  4e(N)x4 ff(.)x3 00(.)x3             00(.)x4 17(.)x2 72(r)x1 54(T)x1 +1u  PARTIAL
   0x0020  4e(N)x5 cb(.)x2 d3(.)x1 1f(.)x1 +1u  00(.)x6 05(.)x1 20( )x1 0d(.)x1     DIFFER
   0x0022  4e(N)x5 97(.)x2 00(.)x2 cb(.)x1     00(.)x3 72(r)x1 0f(.)x1 fc(.)x1 +3u  PARTIAL
   0x0026  00(.)x7 97(.)x1 ff(.)x1 1a(.)x1     01(.)x3 00(.)x2 92(.)x1 cd(.)x1 +2u  PARTIAL
   0x002a  00(.)x7 ff(.)x1 0e(.)x1 4e(N)x1     00(.)x2 1b(.)x1 70(p)x1 5a(Z)x1 +4u  PARTIAL
   0x002b  00(.)x4 5b([)x4 1f(.)x1 06(.)x1     04(.)x2 1b(.)x1 2d(-)x1 5a(Z)x1 +4u  DIFFER
   0x002e  00(.)x3 65(e)x2 ff(.)x2 0c(.)x1 +2u  00(.)x6 ff(.)x1 6e(n)x1 6f(o)x1     PARTIAL
   0x0030  69(i)x4 00(.)x2 3a(:)x1 4e(N)x1 +2u  00(.)x6 01(.)x1 34(4)x1 33(3)x1     PARTIAL
   0x0032  00(.)x5 4e(N)x3 97(.)x1 ff(.)x1     00(.)x5 4d(M)x2 04(.)x1 ff(.)x1     PARTIAL
   0x0033  00(.)x4 4e(N)x4 1f(.)x1 69(i)x1     0e(.)x2 dd(.)x1 fb(.)x1 0d(.)x1 +4u  DIFFER
   0x0036  00(.)x7 97(.)x1 4e(N)x1             00(.)x4 34(4)x2 04(.)x1 ff(.)x1 +1u  PARTIAL
   0x003a  4e(N)x4 00(.)x3 0c(.)x1 97(.)x1     00(.)x5 4d(M)x2 02(.)x1             PARTIAL
   0x003b  00(.)x4 1a(.)x2 18(.)x1 40(@)x1 +1u  00(.)x3 0e(.)x2 04(.)x2 14(.)x1     PARTIAL
   0x003c  00(.)x4 4e(N)x3 1f(.)x1 06(.)x1     00(.)x5 05(.)x1 4d(M)x1 1a(.)x1     PARTIAL
   0x003e  00(.)x8 65(e)x1                     00(.)x4 3a(:)x1 20( )x1 01(.)x1     PARTIAL
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
  prompts_b/harfbuzz_5954.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5954,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5954 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5954 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5954 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).