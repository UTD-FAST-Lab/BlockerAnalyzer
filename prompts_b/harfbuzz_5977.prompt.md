==== BLOCKER ====
Target: harfbuzz
Branch ID: 5977
Location: /src/harfbuzz/src/hb-ot-shaper-use-machine.hh:917:39
Enclosing function: hb-ot-shaper-use.cc:find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}::operator()(hb_pair_t<unsigned int, hb_glyph_info_t const&>) const
Source line: 		     for (unsigned i = p.first + 1; i < buffer->len; ++i)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           1        9          0  loser (I2S vs naive); loser (value_profile vs value_profile_cmplog)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         6        4          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=1.10h  loser=18.80h
  avg hitcount on branch: winner=125  loser=1
  prob_div=0.90  dur_div=17.70h  hit_div=124
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=6.40h  loser=18.80h
  avg hitcount on branch: winner=10  loser=1
  prob_div=0.70  dur_div=12.40h  hit_div=9
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5977/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-use.cc:find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}::operator()(hb_pair_t<unsigned int, hb_glyph_info_t const&>) const (/src/harfbuzz/src/hb-ot-shaper-use-machine.hh:915-921) ---
[B]   913  		 hb_second)
[B]   914      | hb_filter ([&] (const hb_pair_t<unsigned, const hb_glyph_info_t &> p)
[B]   915  		 {
[B]   916  		   if (p.second.use_category() == USE(ZWNJ))
[B]   917  		     for (unsigned i = p.first + 1; i < buffer->len; ++i) <-- BLOCKER
[B]   918  		       if (not_ccs_default_ignorable (info[i]))
[B]   919  			 return !_hb_glyph_info_is_unicode_mark (&info[i]);
[B]   920  		   return true;
[B]   921  		 })

--- Caller (1 hop): hb-ot-shaper-use.cc:setup_syllables_use(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shaper-use.cc:300-308, calls hb-ot-shaper-use.cc:find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}::operator()(hb_pair_t<unsigned int, hb_glyph_info_t const&>) const at line 302) (full body — short) ---
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
hop 2  hb-ot-shaper-use.cc:setup_syllables_use(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:300-308, calls hb-ot-shaper-use.cc:find_syllables_use(hb_buffer_t*)::{lambda(hb_pair_t<unsigned int, hb_glyph_info_t const&>)#1}::operator()(hb_pair_t<unsigned int, hb_glyph_info_t const&>) const at line 302)

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
  (no divergent branches in chain functions; the split is off-chain)

[off-chain: 4 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=f481295249a6092a, size=69 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=448s, mutation_op=BytesDeleteMutator,BytesRandInsertMutator,TokenInsert):
  0000: 74 72 75 03 00 00 00 00 00 1c 1c 1c 1c 1c 1c 1c   tru.............
  0010: ff 0c 20 00 00 00 00 18 18 18 18 18 18 58 73 72   .. ..........Xsr
  0020: 63 68 18 18 18 18 18 00 00 00 00 00 1a 0d 20 00   ch............ .
  0030: 00 00 00 18 18 18 18 18 18 75 03 00 00 00 00 00   .........u......
Seed 2 (id=7d8b777e7e7a8de7, size=95 bytes, fuzzer=naive, trial=1, discovered_at=798s, mutation_op=WordAddMutator,ByteFlipMutator,ByteIncMutator,BytesInsertMutator,BytesDeleteMutator,ByteRandMutator,BytesInsertCopyMutator):
  0000: 00 27 07 00 30 01 00 00 0c 00 00 00 00 16 01 00   .'..0...........
  0010: 00 00 00 10 20 00 65 79 6e df 20 0c 0c 00 00 65   .... .eyn. ....e
  0020: 97 20 20 20 df 00 e7 19 19 19 19 19 19 00 00 00   .   ............
  0030: 0c e5 00 00 00 0d 00 f7 1c 01 00 00 00 00 00 0c   ................
Seed 3 (id=46ddf1aa401bfab3, size=117 bytes, fuzzer=naive, trial=1, discovered_at=5089s, mutation_op=WordInterestingMutator,BytesInsertMutator,BytesSetMutator):
  0000: ff 6e 74 2d 68 6b 00 75 6e 12 ff 00 75 74 4d 4d   .nt-hk.un...utMM
  0010: 4d 00 85 85 85 85 85 85 85 85 85 85 85 85 74 7f   M.............t.
  0020: 75 8a 00 ff ff 85 85 85 85 74 7f 75 8a f9 f9 f9   u........t.u....
  0030: f9 f9 f9 f9 f9 f9 f9 f9 f9 01 10 01 00 00 ff ff   ................
Seed 4 (id=2e4a22672f7de1e4, size=72 bytes, fuzzer=naive, trial=1, discovered_at=5470s, mutation_op=CrossoverReplaceMutator,BytesRandSetMutator):
  0000: 6a 79 2d 68 61 6e 74 00 00 66 66 00 0c 00 0c 00   jy-hant..ff.....
  0010: 97 66 8b 8b 00 00 00 00 00 1b 00 00 15 03 00 61   .f.............a
  0020: 6e 2d 68 61 6e 74 00 00 00 0c 0c 0c 0c 0c 0c 0c   n-hant..........
  0030: 0c 0c 00 00 d4 d4 d4 d4 d4 d4 d4 20 0c 20 00 00   ........... . ..
Seed 5 (id=1a191f11c5d15c02, size=106 bytes, fuzzer=naive, trial=1, discovered_at=10287s, mutation_op=ByteIncMutator):
  0000: ff 6e 74 2d 68 6b 00 75 6e 12 ff 00 75 74 00 85   .nt-hk.un...ut..
  0010: 85 85 85 85 85 85 85 85 85 85 85 74 7f 75 8a 00   ...........t.u..
  0020: ff ff 85 85 85 85 74 7f 75 8a b2 1f 01 00 04 00   ......t.u.......
  0030: 00 00 03 00 00 00 01 10 01 00 00 ff ff ff 7f 00   ................

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=b99d80be1530c37f, size=37 bytes, fuzzer=cmplog, trial=1, discovered_at=283s, mutation_op=BytesDeleteMutator,ByteIncMutator):
  0000: 00 72 10 02 00 72 10 00 00 72 10 00 00 72 10 00   .r...r...r...r..
  0010: 0c 18 00 00 0c 20 00 00 00 0c 00 00 20 8e 74 6c   ..... ...... .tl
  0020: 7b 20 20 20 20                                    {    
Seed 2 (id=daab4b510ad7ac5b, size=62 bytes, fuzzer=cmplog, trial=1, discovered_at=283s, mutation_op=ByteDecMutator,BytesSwapMutator):
  0000: 6c 62 10 0f 0c 20 00 00 0c 20 00 00 ff 00 00 04   lb... ... ......
  0010: 00 20 00 66 77 10 10 10 10 10 10 10 17 10 01 00   . .fw...........
  0020: 00 00 e6 00 00 01 20 20 20 9f 9f 20 6b 65 8e 6e   ......   .. ke.n
  0030: df 28 20 13 ff 7f 00 00 30 7b 7b 0d 00 00         .( .....0{{...
Seed 3 (id=3571be0118d8671b, size=22 bytes, fuzzer=cmplog, trial=1, discovered_at=483s, mutation_op=BytesExpandMutator,BytesRandInsertMutator,BytesInsertCopyMutator,BytesDeleteMutator,ByteAddMutator):
  0000: aa 14 01 00 aa 14 01 00 ff 06 f1 f1 f1 f1 f1 f1   ................
  0010: f1 25 20 00 0c 20                                 .% .. 
Seed 4 (id=39b1e0ba4eefcc06, size=63 bytes, fuzzer=cmplog, trial=1, discovered_at=1370s, mutation_op=CrossoverInsertMutator,BytesRandInsertMutator,ByteNegMutator,BytesDeleteMutator):
  0000: 00 01 10 6f 0c 18 00 00 0c 20 fe ff 02 00 10 6f   ...o..... .....o
  0010: 0c 18 0f 00 0c 17 ff ff 01 03 04 00 ff 0b 18 01   ................
  0020: 0e 0c 18 01 00 0c 32 00 f2 02 00 ff 0b 18 00 00   ......2.........
  0030: 0c 18 01 00 0c 20 00 00 1e fa 02 00 0c fe 00      ..... .........
Seed 5 (id=7dda68d0a67a5a1b, size=63 bytes, fuzzer=cmplog, trial=1, discovered_at=1370s, mutation_op=BytesInsertCopyMutator,ByteRandMutator,TokenInsert,BytesExpandMutator):
  0000: 00 01 10 6f 0c 18 00 00 0c 20 00 00 00 01 10 6f   ...o..... .....o
  0010: 0c 18 00 00 0c 20 00 00 00 00 00 00 ff 0b 18 01   ..... ..........
  0020: 00 0c 18 01 00 0c 32 00 f2 01 00 ff 0b 18 01 00   ......2.........
  0030: 0c 18 02 00 0c 18 00 00 0f 18 00 00 0c 20 00      ............. .


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0004  68(h)x3 00(.)x2 61(a)x2 fa(.)x2 +2u  00(.)x4 0c(.)x4 aa(.)x1 72(r)x1     PARTIAL
   0x0006  00(.)x7 0d(.)x2 74(t)x1 61(a)x1     00(.)x4 20( )x3 10(.)x1 01(.)x1 +1u  PARTIAL
   0x0007  00(.)x5 75(u)x3 08(.)x2 6a(j)x1     00(.)x6 20( )x3 72(r)x1             PARTIAL
   0x0009  12(.)x3 00(.)x2 08(.)x2 1c(.)x1 +3u  20( )x6 72(r)x2 06(.)x1 18(.)x1     DIFFER
   0x000a  00(.)x3 ff(.)x3 08(.)x2 1c(.)x1 +2u  00(.)x6 10(.)x2 f1(.)x1 fe(.)x1     PARTIAL
   0x000e  00(.)x3 08(.)x3 0c(.)x2 1c(.)x1 +2u  10(.)x3 dc(.)x3 00(.)x2 f1(.)x1     PARTIAL
   0x0010  08(.)x3 00(.)x2 85(.)x2 ff(.)x1 +3u  0c(.)x4 00(.)x4 f1(.)x1             PARTIAL
   0x0011  08(.)x3 0c(.)x2 00(.)x2 85(.)x2 +2u  18(.)x3 7f(.)x3 20( )x2 25(%)x1     PARTIAL
   0x0012  85(.)x3 08(.)x3 20( )x2 00(.)x2 +1u  00(.)x4 ff(.)x3 20( )x1 0f(.)x1     PARTIAL
   0x0013  00(.)x3 85(.)x3 08(.)x3 10(.)x1 +1u  00(.)x4 1b(.)x3 66(f)x1 ff(.)x1     PARTIAL
   0x0014  85(.)x3 00(.)x2 08(.)x2 20( )x1 +3u  0c(.)x4 04(.)x3 77(w)x1 0b(.)x1     PARTIAL
   0x0016  00(.)x5 85(.)x3 65(e)x1 20( )x1 +1u  00(.)x3 02(.)x3 10(.)x1 ff(.)x1     PARTIAL
   0x0017  00(.)x5 85(.)x3 18(.)x1 79(y)x1 +1u  00(.)x3 02(.)x3 10(.)x1 ff(.)x1     PARTIAL
   0x0018  85(.)x3 00(.)x2 ab(.)x2 18(.)x1 +3u  00(.)x5 10(.)x1 01(.)x1 0f(.)x1     PARTIAL
   0x001a  85(.)x3 00(.)x2 0b(.)x2 18(.)x1 +3u  00(.)x6 10(.)x1 04(.)x1             PARTIAL
   0x001b  18(.)x3 00(.)x3 74(t)x2 0c(.)x1 +2u  00(.)x4 1b(.)x3 10(.)x1             PARTIAL
   0x001f  00(.)x3 20( )x2 72(r)x1 65(e)x1 +4u  48(H)x3 00(.)x2 01(.)x2 6c(l)x1     PARTIAL
   0x0020  00(.)x3 ff(.)x2 63(c)x1 97(.)x1 +4u  00(.)x5 7b({)x1 0e(.)x1 0f(.)x1     PARTIAL
   0x0023  18(.)x3 20( )x2 85(.)x2 00(.)x2 +2u  40(@)x3 00(.)x2 01(.)x2 20( )x1     PARTIAL
   0x0024  00(.)x3 85(.)x2 18(.)x1 df(.)x1 +4u  00(.)x6 20( )x1 72(r)x1             PARTIAL
   0x0025  00(.)x4 85(.)x3 18(.)x1 74(t)x1 +2u  00(.)x3 0c(.)x2 01(.)x1 72(r)x1     PARTIAL
   0x0026  00(.)x3 74(t)x2 0c(.)x2 18(.)x1 +3u  00(.)x4 32(2)x2 20( )x1             PARTIAL
   0x0027  00(.)x3 7f(.)x2 20( )x2 19(.)x1 +3u  20( )x4 00(.)x3                     PARTIAL
   0x0028  00(.)x5 75(u)x2 19(.)x1 85(.)x1 +2u  6a(j)x3 f2(.)x2 20( )x1 0b(.)x1     DIFFER
   0x002a  0c(.)x3 00(.)x2 b2(.)x2 0b(.)x2 +2u  00(.)x3 72(r)x3 9f(.)x1             PARTIAL
   0x002b  00(.)x3 1f(.)x2 18(.)x2 19(.)x1 +3u  6c(l)x3 ff(.)x2 20( )x1 00(.)x1     PARTIAL
   0x002c  00(.)x4 01(.)x3 1a(.)x1 19(.)x1 +2u  20( )x3 0b(.)x2 6b(k)x1 45(E)x1     DIFFER
   0x002d  00(.)x5 0c(.)x3 0d(.)x1 f9(.)x1 +1u  00(.)x3 18(.)x2 65(e)x1 20( )x1     PARTIAL
   0x002f  00(.)x5 0c(.)x2 20( )x2 f9(.)x1 +1u  00(.)x3 02(.)x2 6e(n)x1 ff(.)x1     PARTIAL
   0x0030  00(.)x7 0c(.)x2 f9(.)x1 0b(.)x1     00(.)x3 0c(.)x2 df(.)x1 2d(-)x1     PARTIAL
   0x0031  00(.)x6 e5(.)x1 f9(.)x1 0c(.)x1 +2u  7f(.)x3 18(.)x2 28(()x1 68(h)x1     DIFFER
   0x0033  00(.)x6 18(.)x3 f9(.)x1 0c(.)x1     00(.)x3 ab(.)x3 13(.)x1             PARTIAL
   0x0034  00(.)x6 18(.)x2 f9(.)x1 d4(.)x1 +1u  00(.)x4 0c(.)x2 ff(.)x1             PARTIAL
   0x0035  00(.)x4 18(.)x1 0d(.)x1 f9(.)x1 +4u  20( )x4 7f(.)x1 18(.)x1 00(.)x1     PARTIAL
   0x0036  00(.)x3 18(.)x1 f9(.)x1 d4(.)x1 +5u  00(.)x4 20( )x3                     PARTIAL
   0x0037  00(.)x3 18(.)x2 20( )x2 f7(.)x1 +3u  00(.)x4 20( )x3                     PARTIAL
   0x003a  00(.)x5 03(.)x1 10(.)x1 d4(.)x1 +3u  20( )x3 02(.)x2 7b({)x1 00(.)x1     PARTIAL
   0x003b  00(.)x5 20( )x2 01(.)x1 ff(.)x1 +2u  00(.)x4 04(.)x2 0d(.)x1             PARTIAL
   0x003c  00(.)x6 0c(.)x3 ff(.)x1 0a(.)x1     00(.)x4 0c(.)x3                     PARTIAL
   0x003d  00(.)x6 20( )x2 ff(.)x1 0c(.)x1 +1u  80(.)x3 20( )x2 00(.)x1 fe(.)x1     PARTIAL
   ... (2 more divergent offsets)
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
  prompts_b/harfbuzz_5977.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5977,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5977 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5977 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5977 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).