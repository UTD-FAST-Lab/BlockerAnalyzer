==== BLOCKER ====
Target: harfbuzz
Branch ID: 9523
Location: /src/harfbuzz/src/hb-ot-shaper-use.cc:394:7
Enclosing function: hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int)
Source line:   if (info[start].use_category() == USE(R) && end - start > 1)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           0       10          0  loser (I2S vs naive)
value_profile                    8        2          0  REFERENCE
value_profile_cmplog             6        4          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 17  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.50h  loser=12.00h
  avg hitcount on branch: winner=5  loser=0
  prob_div=1.00  dur_div=8.50h  hit_div=5
  subject-level: delta_AUC=9064080.0  p_AUC=0.0002  delta_Final=796.1  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/9523/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int) (/src/harfbuzz/src/hb-ot-shaper-use.cc:363-442) ---
[ ]   361  static void
[ ]   362  reorder_syllable_use (hb_buffer_t *buffer, unsigned int start, unsigned int end)
[B]   363  {
[B]   364    use_syllable_type_t syllable_type = (use_syllable_type_t) (buffer->info[start].syllable() & 0x0F);
[ ]   365    /* Only a few syllable types need reordering. */
[B]   366    if (unlikely (!(FLAG_UNSAFE (syllable_type) &
[B]   367  		  (FLAG (use_virama_terminated_cluster) |
[B]   368  		   FLAG (use_sakot_terminated_cluster) |
[B]   369  		   FLAG (use_standard_cluster) |
[B]   370  		   FLAG (use_symbol_cluster) |
[B]   371  		   FLAG (use_broken_cluster) |
[B]   372  		   0))))
[ ]   373      return;
[ ]   374  
[B]   375    hb_glyph_info_t *info = buffer->info;
[ ]   376  
[B]   377  #define POST_BASE_FLAGS64 (FLAG64 (USE(FAbv)) | \
[W]   378  			   FLAG64 (USE(FBlw)) | \
[W]   379  			   FLAG64 (USE(FPst)) | \
[W]   380  			   FLAG64 (USE(MAbv)) | \
[W]   381  			   FLAG64 (USE(MBlw)) | \
[W]   382  			   FLAG64 (USE(MPst)) | \
[W]   383  			   FLAG64 (USE(MPre)) | \
[W]   384  			   FLAG64 (USE(VAbv)) | \
[W]   385  			   FLAG64 (USE(VBlw)) | \
[W]   386  			   FLAG64 (USE(VPst)) | \
[W]   387  			   FLAG64 (USE(VPre)) | \
[W]   388  			   FLAG64 (USE(VMAbv)) | \
[W]   389  			   FLAG64 (USE(VMBlw)) | \
[W]   390  			   FLAG64 (USE(VMPst)) | \
[W]   391  			   FLAG64 (USE(VMPre)))
[ ]   392  
[ ]   393    /* Move things forward. */
[B]   394    if (info[start].use_category() == USE(R) && end - start > 1) <-- BLOCKER
[W]   395    {
[ ]   396      /* Got a repha.  Reorder it towards the end, but before the first post-base
[ ]   397       * glyph. */
[W]   398      for (unsigned int i = start + 1; i < end; i++)
[W]   399      {
[W]   400        bool is_post_base_glyph = (FLAG64_UNSAFE (info[i].use_category()) & POST_BASE_FLAGS64) ||
[W]   401  				is_halant_use (info[i]);
[W]   402        if (is_post_base_glyph || i == end - 1)
[W]   403        {
[ ]   404  	/* If we hit a post-base glyph, move before it; otherwise move to the
[ ]   405  	 * end. Shift things in between backward. */
[ ]   406  
[W]   407  	if (is_post_base_glyph)
[W]   408  	  i--;
[ ]   409  
[W]   410  	buffer->merge_clusters (start, i + 1);
[W]   411  	hb_glyph_info_t t = info[start];
[W]   412  	memmove (&info[start], &info[start + 1], (i - start) * sizeof (info[0]));
[W]   413  	info[i] = t;
[ ]   414  
[W]   415  	break;
[W]   416        }
[W]   417      }
[W]   418    }
[ ]   419  
[ ]   420    /* Move things back. */
[B]   421    unsigned int j = start;
[B]   422    for (unsigned int i = start; i < end; i++)
[B]   423    {
[B]   424      uint32_t flag = FLAG_UNSAFE (info[i].use_category());
[B]   425      if (is_halant_use (info[i]))
[W]   426      {
[ ]   427        /* If we hit a halant, move after it; otherwise move to the beginning, and
[ ]   428         * shift things in between forward. */
[W]   429        j = i + 1;
[W]   430      }
[B]   431      else if (((flag) & (FLAG (USE(VPre)) | FLAG (USE(VMPre)))) &&
[ ]   432  	     /* Only move the first component of a MultipleSubst. */
[B]   433  	     0 == _hb_glyph_info_get_lig_comp (&info[i]) &&
[B]   434  	     j < i)
[W]   435      {
[W]   436        buffer->merge_clusters (j, i + 1);
[W]   437        hb_glyph_info_t t = info[i];
[W]   438        memmove (&info[j + 1], &info[j], (i - j) * sizeof (info[0]));
[W]   439        info[j] = t;
[W]   440      }
[B]   441    }
[B]   442  }

--- No 1-hop callers of hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int) fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:363-442) ---
  d=1   L 394  T=14 F=1  T=0 F=0  if (info[start].use_category() == USE(R) && end - start > 1)  <-- BLOCKER
  d=1   L 394  T=15 F=125  T=0 F=132  if (info[start].use_category() == USE(R) && end - start > 1)  <-- BLOCKER
  d=1   L 398  T=19 F=0  T=0 F=0  for (unsigned int i = start + 1; i < end; i++)
  d=1   L 400  T=3 F=16  T=0 F=0  bool is_post_base_glyph = (FLAG64_UNSAFE (info[i].use_cat...
  d=1   L 401  T=1 F=15  T=0 F=0  is_halant_use (info[i]);
  d=1   L 402  T=10 F=5  T=0 F=0  if (is_post_base_glyph || i == end - 1)
  d=1   L 402  T=4 F=15  T=0 F=0  if (is_post_base_glyph || i == end - 1)
  d=1   L 407  T=4 F=10  T=0 F=0  if (is_post_base_glyph)
  d=1   L 425  T=1 F=159  T=0 F=144  if (is_halant_use (info[i]))
  d=1   L 431  T=3 F=156  T=0 F=144  else if (((flag) & (FLAG (USE(VPre)) | FLAG (USE(VMPre)))...
  d=1   L 433  T=3 F=0  T=0 F=0  0 == _hb_glyph_info_get_lig_comp (&info[i]) &&
  d=1   L 434  T=3 F=0  T=0 F=0  j < i)

[off-chain: 2 additional divergent branches across 1 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=6b27e0030f70e13d, size=16 bytes, fuzzer=naive, trial=1, discovered_at=68s, mutation_op=ByteRandMutator):
  0000: 46 1d 01 00 00 01 0e 00 00 fe 00 00 00 00 00 72   F..............r
Seed 2 (id=26118fa19faf0be5, size=16 bytes, fuzzer=naive, trial=1, discovered_at=105s, mutation_op=BytesCopyMutator):
  0000: 46 1d 01 00 00 01 0e 00 00 fe 00 01 0e 00 00 72   F..............r
Seed 3 (id=3c1e8d834f19e89f, size=40 bytes, fuzzer=naive, trial=1, discovered_at=532s, mutation_op=DwordInterestingMutator,WordAddMutator,ByteDecMutator,BytesInsertCopyMutator,BytesDeleteMutator,ByteRandMutator):
  0000: 4e a8 00 00 4e 0d 00 00 1e 10 00 00 4f 00 00 00   N...N.......O...
  0010: 01 00 9c 89 08 00 00 17 00 00 00 01 0e 00 df fe   ................
  0020: 00 00 7f ff ff ff 00 00                           ........
Seed 4 (id=a05c1e7a7fa09cf6, size=53 bytes, fuzzer=naive, trial=1, discovered_at=1928s, mutation_op=ByteNegMutator,BytesCopyMutator,ByteDecMutator,BytesExpandMutator,TokenInsert):
  0000: 4e 6d e0 0b 09 00 00 1e 10 1e 00 09 4e 08 00 00   Nm..........N...
  0010: 4e 0d 00 00 4e 09 00 00 4e 09 7a 6f 2d 68 61 6e   N...N...N.zo-han
  0020: 73 00 00 00 4e 0d 00 00 4e 09 00 76 66 68 70 00   s...N...N..vfhp.
  0030: 00 68 70 00 00                                    .hp..
Seed 5 (id=8eaca3285d930634, size=114 bytes, fuzzer=naive, trial=1, discovered_at=2238s, mutation_op=CrossoverInsertMutator,BitFlipMutator,WordAddMutator,BytesInsertCopyMutator,CrossoverInsertMutator,BytesSwapMutator):
  0000: 7a 6f 2d 2d 2d 2d 2d 2d 2d 2d 2d 2d 2d b3 2d 00   zo-----------.-.
  0010: 01 20 20 20 6b 65 72 20 20 20 6e 20 20 00 00 2d   .   ker   n  ..-
  0020: 20 00 fe 20 20 2d 40 00 00 20 00 00 64 1a 00 00    ..  -@.. ..d...
  0030: 5a 00 b0 12 01 00 b0 12 01 01 c7 12 01 00 00 00   Z...............

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0068ef8b9292e1cb, size=18 bytes, fuzzer=cmplog, trial=1, discovered_at=4s, mutation_op=TokenInsert,BytesRandInsertMutator,ByteIncMutator):
  0000: 9e 9e 9e 90 90 90 90 90 9e 9e 9e 9f b2 16 01 00   ................
  0010: 9e 9e                                             ..
Seed 2 (id=00b8a45c7e6f196f, size=30 bytes, fuzzer=cmplog, trial=1, discovered_at=6s, mutation_op=ByteRandMutator,BytesInsertCopyMutator,BytesInsertMutator,DwordAddMutator,BytesDeleteMutator,ByteIncMutator):
  0000: 20 20 04 00 72 6e 20 20 20 20 ff 80 00 1a 20 ff     ..rn    .... .
  0010: 20 20 20 00 64 20 20 20 9e ff 00 00 20 17            .d   .... .
Seed 3 (id=006d67d4a429fd99, size=19 bytes, fuzzer=cmplog, trial=1, discovered_at=169s, mutation_op=BytesInsertMutator,BitFlipMutator,BytesDeleteMutator):
  0000: 40 a8 00 00 5f 5f 20 28 20 20 20 20 20 20 20 20   @...__ (        
  0010: 20 a9 a8                                           ..
Seed 4 (id=00ebca8a83a5c915, size=28 bytes, fuzzer=cmplog, trial=1, discovered_at=176s, mutation_op=BytesRandSetMutator,BytesDeleteMutator,TokenReplace,BytesInsertCopyMutator):
  0000: e3 0a 01 00 01 75 65 70 be be be be d7 be 6d 6a   .....uep......mj
  0010: 76 75 00 20 20 be be be be d7 be be               vu.  .......
Seed 5 (id=0083da97d7f94a2e, size=19 bytes, fuzzer=cmplog, trial=1, discovered_at=227s, mutation_op=BytesCopyMutator,ByteIncMutator):
  0000: 10 18 00 00 4b e9 01 00 00 0f 0c 0c 0c 0c 0c 0c   ....K...........
  0010: 0c 0c 00                                          ...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0003  00(.)x5 2d(-)x3 0b(.)x1 10(.)x1     00(.)x8 90(.)x1 ff(.)x1             PARTIAL
   0x0006  00(.)x4 0e(.)x3 2d(-)x2 6b(k)x1     20( )x4 00(.)x2 90(.)x1 65(e)x1 +2u  PARTIAL
   0x000e  00(.)x5 2d(-)x2 10(.)x1 ea(.)x1     20( )x4 01(.)x1 6d(m)x1 0c(.)x1 +3u  DIFFER
   0x0013  00(.)x2 20( )x2 89(.)x1 10(.)x1 +1u  20( )x4 00(.)x1 14(.)x1 02(.)x1     PARTIAL
   0x0015  65(e)x2 00(.)x1 09(.)x1 1f(.)x1 +2u  20( )x3 be(.)x2 02(.)x1 82(.)x1     PARTIAL
   0x0016  00(.)x4 72(r)x2 04(.)x1             20( )x2 be(.)x2 f3(.)x1 04(.)x1 +1u  PARTIAL
   0x0017  00(.)x4 20( )x2 17(.)x1             be(.)x2 00(.)x2 20( )x1 0c(.)x1 +1u  PARTIAL
   0x0019  00(.)x2 09(.)x2 20( )x2 fe(.)x1     ff(.)x1 d7(.)x1 0c(.)x1 6b(k)x1 +3u  PARTIAL
   0x001a  00(.)x3 6e(n)x2 7a(z)x1 6a(j)x1     1a(.)x2 00(.)x1 be(.)x1 0c(.)x1 +2u  PARTIAL
   0x001c  20( )x2 0e(.)x1 2d(-)x1 fe(.)x1 +2u  20( )x3 0c(.)x1 43(C)x1 47(G)x1     PARTIAL
   0x001d  00(.)x4 68(h)x1 12(.)x1 0d(.)x1     20( )x3 17(.)x1 46(F)x1 50(P)x1     DIFFER
   0x0020  20( )x2 00(.)x1 73(s)x1 05(.)x1 +2u  01(.)x2 03(.)x1 bd(.)x1 6e(n)x1     DIFFER
   0x0021  00(.)x5 20( )x1 09(.)x1             13(.)x1 04(.)x1 54(T)x1 00(.)x1 +1u  PARTIAL
   0x0022  00(.)x3 fe(.)x2 7f(.)x1 2d(-)x1     03(.)x2 01(.)x1 64(d)x1 0e(.)x1     DIFFER
   0x0023  20( )x2 ff(.)x1 00(.)x1 04(.)x1 +1u  00(.)x2 20( )x2 ff(.)x1             PARTIAL
   0x0024  20( )x2 ff(.)x1 4e(N)x1 00(.)x1 +1u  00(.)x3 6c(l)x1 ff(.)x1             PARTIAL
   0x0025  2d(-)x3 ff(.)x1 0d(.)x1 10(.)x1     20( )x1 69(i)x1 0c(.)x1 0a(.)x1 +1u  DIFFER
   0x0026  00(.)x3 40(@)x2 2d(-)x1             20( )x1 67(g)x1 0a(.)x1 be(.)x1 +1u  PARTIAL
   0x0027  00(.)x5 5f(_)x1                     00(.)x2 20( )x1 61(a)x1 ab(.)x1     PARTIAL
   0x0028  00(.)x2 4e(N)x1 20( )x1 5f(_)x1     20( )x2 00(.)x2 04(.)x1             PARTIAL
   0x0029  20( )x2 09(.)x1 00(.)x1 5f(_)x1     0c(.)x1 6b(k)x1 e1(.)x1 00(.)x1 +1u  PARTIAL
   0x002a  00(.)x4 10(.)x1                     0c(.)x1 41(A)x1 e1(.)x1 80(.)x1 +1u  DIFFER
   0x002b  00(.)x2 76(v)x1 01(.)x1 5f(_)x1     00(.)x2 7f(.)x1 52(R)x1 6f(o)x1     PARTIAL
   0x002c  64(d)x2 66(f)x1 00(.)x1 5f(_)x1     4d(M)x2 0c(.)x1 04(.)x1 20( )x1     DIFFER
   0x002d  1a(.)x2 68(h)x1 8a(.)x1 5f(_)x1     02(.)x2 0c(.)x1 41(A)x1 56(V)x1     DIFFER
   0x002e  00(.)x2 70(p)x1 8a(.)x1 5f(_)x1     0b(.)x1 03(.)x1 0a(.)x1 54(T)x1 +1u  DIFFER
   0x002f  00(.)x3 8a(.)x1 5f(_)x1             f3(.)x1 02(.)x1 4f(O)x1 48(H)x1 +1u  DIFFER
   0x0030  5a(Z)x2 00(.)x1 8a(.)x1 5f(_)x1     0c(.)x1 00(.)x1 54(T)x1 13(.)x1 +1u  PARTIAL
   0x0031  00(.)x2 68(h)x1 8a(.)x1 20( )x1     0c(.)x1 6d(m)x1 00(.)x1 13(.)x1 +1u  PARTIAL
   0x0032  b0(.)x2 70(p)x1 8a(.)x1 04(.)x1     0c(.)x1 00(.)x1 08(.)x1 ed(.)x1 +1u  DIFFER
   0x0033  00(.)x2 12(.)x2 8a(.)x1             0c(.)x1 00(.)x1 01(.)x1 18(.)x1 +1u  PARTIAL
   0x0034  01(.)x2 00(.)x1 8a(.)x1 63(c)x1     00(.)x3 20( )x1 6b(k)x1             PARTIAL
   0x0035  00(.)x2 8a(.)x1 fe(.)x1             00(.)x2 20( )x1 65(e)x1 78(x)x1     PARTIAL
   0x0036  b0(.)x2 8a(.)x1 6a(j)x1             20( )x1 64(d)x1 e1(.)x1 00(.)x1 +1u  DIFFER
   0x0037  12(.)x2 8a(.)x1 00(.)x1             0c(.)x1 6e(n)x1 e1(.)x1 00(.)x1 +1u  PARTIAL
   0x0038  01(.)x2 8a(.)x1 b0(.)x1             00(.)x2 e1(.)x1 06(.)x1 78(x)x1     DIFFER
   0x0039  01(.)x3 12(.)x1                     04(.)x1 0c(.)x1 e1(.)x1 00(.)x1 +1u  DIFFER
   0x003a  c7(.)x2 4a(J)x1 01(.)x1             1a(.)x1 02(.)x1 e1(.)x1 00(.)x1 +1u  DIFFER
   0x003b  12(.)x2 e9(.)x1 00(.)x1             0c(.)x1 00(.)x1 b0(.)x1 01(.)x1 +1u  PARTIAL
   0x003c  01(.)x3 63(c)x1                     f0(.)x1 20( )x1 12(.)x1 42(B)x1 +1u  DIFFER
   ... (3 more divergent offsets)
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
  prompts/RB--/01_harfbuzz_9523.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 9523,
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
      // pick EXACTLY ONE of:
      //   "I2SRandReplace"     (cmplog / vpc input-to-state substitution)
      //   "CMP_MAP gradient"   (vp / vpc Hamming/prefix-distance feedback)
      //   "havoc-only"         (lucky havoc byte mutation, no CMP introspection)
      //   "token-replace"      (TokenInsert/TokenReplace dictionary mutations)
      //   "other"              (anything that does not fit the four above)
    "verified_in_lineage": true,
      // pick true or false
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 9523 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 9523 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 9523 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).