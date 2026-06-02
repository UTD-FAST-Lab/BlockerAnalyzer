==== BLOCKER ====
Target: harfbuzz
Branch ID: 5998
Location: /src/harfbuzz/src/hb-ot-shaper-use.cc:425:9
Enclosing function: hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int)
Source line:     if (is_halant_use (info[i]))
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           0       10          0  loser (I2S vs naive); loser (value_profile vs value_profile_cmplog)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             9        1          0  winner (value_profile vs cmplog)
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
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.60h  loser=23.60h
  avg hitcount on branch: winner=45  loser=0
  prob_div=1.00  dur_div=23.00h  hit_div=45
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=8.50h  loser=23.60h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.90  dur_div=15.10h  hit_div=2
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5998/{W,L}/branch_coverage_show.txt

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
[ ]   378  			   FLAG64 (USE(FBlw)) | \
[ ]   379  			   FLAG64 (USE(FPst)) | \
[ ]   380  			   FLAG64 (USE(MAbv)) | \
[ ]   381  			   FLAG64 (USE(MBlw)) | \
[ ]   382  			   FLAG64 (USE(MPst)) | \
[ ]   383  			   FLAG64 (USE(MPre)) | \
[ ]   384  			   FLAG64 (USE(VAbv)) | \
[ ]   385  			   FLAG64 (USE(VBlw)) | \
[ ]   386  			   FLAG64 (USE(VPst)) | \
[ ]   387  			   FLAG64 (USE(VPre)) | \
[ ]   388  			   FLAG64 (USE(VMAbv)) | \
[ ]   389  			   FLAG64 (USE(VMBlw)) | \
[ ]   390  			   FLAG64 (USE(VMPst)) | \
[ ]   391  			   FLAG64 (USE(VMPre)))
[ ]   392  
[ ]   393    /* Move things forward. */
[B]   394    if (info[start].use_category() == USE(R) && end - start > 1)
[ ]   395    {
[ ]   396      /* Got a repha.  Reorder it towards the end, but before the first post-base
[ ]   397       * glyph. */
[ ]   398      for (unsigned int i = start + 1; i < end; i++)
[ ]   399      {
[ ]   400        bool is_post_base_glyph = (FLAG64_UNSAFE (info[i].use_category()) & POST_BASE_FLAGS64) ||
[ ]   401  				is_halant_use (info[i]);
[ ]   402        if (is_post_base_glyph || i == end - 1)
[ ]   403        {
[ ]   404  	/* If we hit a post-base glyph, move before it; otherwise move to the
[ ]   405  	 * end. Shift things in between backward. */
[ ]   406  
[ ]   407  	if (is_post_base_glyph)
[ ]   408  	  i--;
[ ]   409  
[ ]   410  	buffer->merge_clusters (start, i + 1);
[ ]   411  	hb_glyph_info_t t = info[start];
[ ]   412  	memmove (&info[start], &info[start + 1], (i - start) * sizeof (info[0]));
[ ]   413  	info[i] = t;
[ ]   414  
[ ]   415  	break;
[ ]   416        }
[ ]   417      }
[ ]   418    }
[ ]   419  
[ ]   420    /* Move things back. */
[B]   421    unsigned int j = start;
[B]   422    for (unsigned int i = start; i < end; i++)
[B]   423    {
[B]   424      uint32_t flag = FLAG_UNSAFE (info[i].use_category());
[B]   425      if (is_halant_use (info[i])) <-- BLOCKER
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

--- Caller (1 hop): hb-ot-shaper-use.cc:reorder_use(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shaper-use.cc:448-467, calls hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int) at line 459) (full body — short) ---
[B]   448  {
[B]   449    bool ret = false;
[B]   450    if (buffer->message (font, "start reordering USE"))
[B]   451    {
[B]   452      if (hb_syllabic_insert_dotted_circles (font, buffer,
[B]   453  					   use_broken_cluster,
[B]   454  					   USE(B),
[B]   455  					   USE(R)))
[ ]   456        ret = true;
[ ]   457  
[B]   458      foreach_syllable (buffer, start, end)
[B]   459        reorder_syllable_use (buffer, start, end); <-- CALL
[ ]   460  
[B]   461      (void) buffer->message (font, "end reordering USE");
[B]   462    }
[ ]   463  
[B]   464    HB_BUFFER_DEALLOCATE_VAR (buffer, use_category);
[ ]   465  
[B]   466    return ret;
[B]   467  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-use.cc:reorder_use(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:448-467, calls hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int) at line 459)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      39        10  hb-ot-shaper-use.cc:compose_use(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:483-489)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:363-442) ---
  d=1   L 425  T=25 F=247  T=0 F=144  if (is_halant_use (info[i]))  <-- BLOCKER
  d=1   L 431  T=3 F=244  T=0 F=144  else if (((flag) & (FLAG (USE(VPre)) | FLAG (USE(VMPre)))...
  d=1   L 433  T=3 F=0  T=0 F=0  0 == _hb_glyph_info_get_lig_comp (&info[i]) &&
  d=1   L 434  T=3 F=0  T=0 F=0  j < i)

[off-chain: 7 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=281d4d26e9abb8d7, size=20 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=87s, mutation_op=BytesSetMutator,BytesDeleteMutator,ByteIncMutator):
  0000: 35 12 01 00 00 c0 01 04 00 00 00 ba 45 45 ff ff   5...........EE..
  0010: ff ff ff ff                                       ....
Seed 2 (id=890855f856f6ca42, size=2 bytes, fuzzer=naive, trial=1, discovered_at=150s, mutation_op=ByteInterestingMutator,ByteRandMutator,ByteRandMutator,BytesDeleteMutator):
  0000: 7f 2d                                             .-
Seed 3 (id=94baf643047e5047, size=53 bytes, fuzzer=naive, trial=1, discovered_at=281s, mutation_op=QwordAddMutator,BytesDeleteMutator):
  0000: 4b e9 01 00 ee 1f 00 00 3f 16 01 00 ee 54 54 fd   K.......?....TT.
  0010: ff ff ff 54 54 73 73 73 73 77 03 03 54 54 54 54   ...TTssssw..TTTT
  0020: 54 3a 54 54 54 54 54 50 73 73 73 73 77 03 ff 64   T:TTTTTPssssw..d
  0030: 00 00 03 03 03                                    .....
Seed 4 (id=017a673c0fdcee2c, size=98 bytes, fuzzer=naive, trial=1, discovered_at=333s, mutation_op=ByteIncMutator,BytesInsertCopyMutator,CrossoverReplaceMutator,BytesRandInsertMutator,BytesSetMutator,QwordAddMutator):
  0000: 0c 0c 0c 0c 00 00 00 97 97 97 97 97 ff 08 00 00   ................
  0010: 00 00 0c 0c 00 11 00 00 80 00 15 00 01 ff 00 7b   ...............{
  0020: 7b 7b 7b 7b 7b 7b 7b 7b 7b 00 02 00 00 03 00 00   {{{{{{{{{.......
  0030: 80 00 00 00 10 00 0a 4a 0f 01 00 ff f0 0e fd 10   .......J........
Seed 5 (id=7a9f1edb9a47ab4a, size=40 bytes, fuzzer=naive, trial=1, discovered_at=1333s, mutation_op=BytesSwapMutator,ByteInterestingMutator,ByteInterestingMutator,BytesSwapMutator):
  0000: 7f 2d 00 00 40 08 00 00 00 ff 03 64 20 00 97 97   .-..@......d ...
  0010: 00 01 fb 00 00 00 01 fe 10 f4 07 00 00 00 00 00   ................
  0020: ff 21 ec 66 ff 00 ff 00                           .!.f....

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
   0x0000  00(.)x5 7f(.)x2 80(.)x2 b4(.)x2 +6u  00(.)x7 74(t)x1 86(.)x1 4f(O)x1     PARTIAL
   0x0004  00(.)x8 fe(.)x2 ee(.)x1 40(@)x1 +4u  00(.)x9 20( )x1                     PARTIAL
   0x0008  00(.)x4 20( )x4 e7(.)x2 3f(?)x1 +5u  00(.)x3 20( )x3 21(!)x3 65(e)x1     PARTIAL
   0x0016  00(.)x10 73(s)x1 01(.)x1 03(.)x1 +2u  00(.)x7 97(.)x1 01(.)x1 02(.)x1     PARTIAL
   0x0018  00(.)x8 73(s)x1 80(.)x1 10(.)x1 +4u  00(.)x7 20( )x1 fd(.)x1 17(.)x1     PARTIAL
   0x0026  00(.)x6 ff(.)x2 54(T)x1 7b({)x1 +5u  00(.)x7 3b(;)x1 80(.)x1             PARTIAL
   0x0027  00(.)x5 50(P)x1 7b({)x1 10(.)x1 +7u  10(.)x3 02(.)x2 20( )x2 00(.)x2     PARTIAL
   0x002a  00(.)x4 17(.)x2 73(s)x1 02(.)x1 +5u  00(.)x4 72(r)x2 0d(.)x1 10(.)x1     PARTIAL
   0x002c  00(.)x4 77(w)x2 0d(.)x1 ff(.)x1 +5u  00(.)x6 11(.)x1 20( )x1             PARTIAL
   0x0034  00(.)x4 1f(.)x2 03(.)x1 10(.)x1 +3u  00(.)x6 0c(.)x1 01(.)x1             PARTIAL
   0x0036  00(.)x3 20( )x2 0a(.)x1 02(.)x1 +3u  00(.)x4 01(.)x1 0c(.)x1 20( )x1     PARTIAL
   0x003a  00(.)x6 84(.)x1 04(.)x1 ff(.)x1 +1u  00(.)x4 ec(.)x1 20( )x1             PARTIAL
   0x003c  00(.)x5 01(.)x2 f0(.)x1 ec(.)x1 +1u  00(.)x5 22(")x1                     PARTIAL
   0x003d  00(.)x8 0e(.)x1 6b(k)x1             22(")x1 00(.)x1 06(.)x1 01(.)x1 +2u  PARTIAL
   0x003e  00(.)x6 fd(.)x1 0a(.)x1 65(e)x1 +1u  00(.)x4 e2(.)x1                     PARTIAL
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
  prompts_b/harfbuzz_5998.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5998,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5998 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5998 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5998 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).