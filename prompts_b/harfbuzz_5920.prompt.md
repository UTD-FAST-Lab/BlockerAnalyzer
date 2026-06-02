==== BLOCKER ====
Target: harfbuzz
Branch ID: 5920
Location: /src/harfbuzz/src/hb-ot-shaper-khmer.cc:245:9
Enclosing function: hb-ot-shaper-khmer.cc:reorder_consonant_syllable(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)
Source line:     if (info[i].khmer_category() == K_Cat(H) && num_coengs <= 2 && i + 1 < end)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           0       10          0  loser (I2S vs naive)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             5        5          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.90h  loser=20.00h
  avg hitcount on branch: winner=203  loser=0
  prob_div=1.00  dur_div=19.10h  hit_div=203
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5920/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-khmer.cc:reorder_consonant_syllable(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) (/src/harfbuzz/src/hb-ot-shaper-khmer.cc:216-286) ---
[ ]   214  			    hb_buffer_t *buffer,
[ ]   215  			    unsigned int start, unsigned int end)
[B]   216  {
[B]   217    const khmer_shape_plan_t *khmer_plan = (const khmer_shape_plan_t *) plan->data;
[B]   218    hb_glyph_info_t *info = buffer->info;
[ ]   219  
[ ]   220    /* Setup masks. */
[B]   221    {
[ ]   222      /* Post-base */
[B]   223      hb_mask_t mask = khmer_plan->mask_array[KHMER_BLWF] |
[B]   224  		     khmer_plan->mask_array[KHMER_ABVF] |
[B]   225  		     khmer_plan->mask_array[KHMER_PSTF];
[B]   226      for (unsigned int i = start + 1; i < end; i++)
[B]   227        info[i].mask  |= mask;
[B]   228    }
[ ]   229  
[B]   230    unsigned int num_coengs = 0;
[B]   231    for (unsigned int i = start + 1; i < end; i++)
[B]   232    {
[ ]   233      /* """
[ ]   234       * When a COENG + (Cons | IndV) combination are found (and subscript count
[ ]   235       * is less than two) the character combination is handled according to the
[ ]   236       * subscript type of the character following the COENG.
[ ]   237       *
[ ]   238       * ...
[ ]   239       *
[ ]   240       * Subscript Type 2 - The COENG + RO characters are reordered to immediately
[ ]   241       * before the base glyph. Then the COENG + RO characters are assigned to have
[ ]   242       * the 'pref' OpenType feature applied to them.
[ ]   243       * """
[ ]   244       */
[B]   245      if (info[i].khmer_category() == K_Cat(H) && num_coengs <= 2 && i + 1 < end) <-- BLOCKER
[W]   246      {
[W]   247        num_coengs++;
[ ]   248  
[W]   249        if (info[i + 1].khmer_category() == K_Cat(Ra))
[ ]   250        {
[ ]   251  	for (unsigned int j = 0; j < 2; j++)
[ ]   252  	  info[i + j].mask |= khmer_plan->mask_array[KHMER_PREF];
[ ]   253  
[ ]   254  	/* Move the Coeng,Ro sequence to the start. */
[ ]   255  	buffer->merge_clusters (start, i + 2);
[ ]   256  	hb_glyph_info_t t0 = info[i];
[ ]   257  	hb_glyph_info_t t1 = info[i + 1];
[ ]   258  	memmove (&info[start + 2], &info[start], (i - start) * sizeof (info[0]));
[ ]   259  	info[start] = t0;
[ ]   260  	info[start + 1] = t1;
[ ]   261  
[ ]   262  	/* Mark the subsequent stuff with 'cfar'.  Used in Khmer.
[ ]   263  	 * Read the feature spec.
[ ]   264  	 * This allows distinguishing the following cases with MS Khmer fonts:
[ ]   265  	 * U+1784,U+17D2,U+179A,U+17D2,U+1782
[ ]   266  	 * U+1784,U+17D2,U+1782,U+17D2,U+179A
[ ]   267  	 */
[ ]   268  	if (khmer_plan->mask_array[KHMER_CFAR])
[ ]   269  	  for (unsigned int j = i + 2; j < end; j++)
[ ]   270  	    info[j].mask |= khmer_plan->mask_array[KHMER_CFAR];
[ ]   271  
[ ]   272  	num_coengs = 2; /* Done. */
[ ]   273        }
[W]   274      }
[ ]   275  
[ ]   276      /* Reorder left matra piece. */
[B]   277      else if (info[i].khmer_category() == K_Cat(VPre))
[L]   278      {
[ ]   279        /* Move to the start. */
[L]   280        buffer->merge_clusters (start, i + 1);
[L]   281        hb_glyph_info_t t = info[i];
[L]   282        memmove (&info[start + 1], &info[start], (i - start) * sizeof (info[0]));
[L]   283        info[start] = t;
[L]   284      }
[B]   285    }
[B]   286  }

--- Caller (1 hop): hb-ot-shaper-khmer.cc:reorder_syllable_khmer(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) (/src/harfbuzz/src/hb-ot-shaper-khmer.cc:293-305, calls hb-ot-shaper-khmer.cc:reorder_consonant_syllable(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) at line 299) (full body — short) ---
[B]   293  {
[B]   294    khmer_syllable_type_t syllable_type = (khmer_syllable_type_t) (buffer->info[start].syllable() & 0x0F);
[B]   295    switch (syllable_type)
[B]   296    {
[B]   297      case khmer_broken_cluster: /* We already inserted dotted-circles, so just call the consonant_syllable. */
[B]   298      case khmer_consonant_syllable:
[B]   299       reorder_consonant_syllable (plan, face, buffer, start, end); <-- CALL
[B]   300       break;
[ ]   301  
[B]   302      case khmer_non_khmer_cluster:
[B]   303        break;
[B]   304    }
[B]   305  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-khmer.cc:reorder_syllable_khmer(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-khmer.cc:293-305, calls hb-ot-shaper-khmer.cc:reorder_consonant_syllable(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) at line 299)
hop 3  hb-ot-shaper-khmer.cc:reorder_khmer(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-khmer.cc:311-328, calls hb-ot-shaper-khmer.cc:reorder_syllable_khmer(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) at line 322)

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-shaper-khmer.cc:reorder_consonant_syllable(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-khmer.cc:216-286) ---
  d=1   L 226  T=55 F=45  T=20 F=27  for (unsigned int i = start + 1; i < end; i++)
  d=1   L 231  T=55 F=45  T=20 F=27  for (unsigned int i = start + 1; i < end; i++)
  d=1   L 245  T=13 F=15  T=0 F=0  if (info[i].khmer_category() == K_Cat(H) && num_coengs <=...  <-- BLOCKER
  d=1   L 245  T=28 F=0  T=0 F=0  if (info[i].khmer_category() == K_Cat(H) && num_coengs <=...  <-- BLOCKER
  d=1   L 245  T=28 F=27  T=0 F=20  if (info[i].khmer_category() == K_Cat(H) && num_coengs <=...  <-- BLOCKER
  d=1   L 249  T=0 F=13  T=0 F=0  if (info[i + 1].khmer_category() == K_Cat(Ra))
  d=1   L 277  T=0 F=42  T=2 F=18  else if (info[i].khmer_category() == K_Cat(VPre))

[off-chain: 6 additional divergent branches across 1 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=0d431e94a78d2b78, size=52 bytes, fuzzer=naive, trial=1, discovered_at=3599s, mutation_op=BytesExpandMutator):
  0000: 00 00 04 00 e9 17 00 00 01 00 00 00 2d 00 00 00   ............-...
  0010: e9 17 00 00 d2 17 00 00 80 00 00 00 2d 00 00 00   ............-...
  0020: e9 17 00 00 d2 17 00 00 80 32 00 00 d2 00 1a 17   .........2......
  0030: 00 00 1d 20                                       ... 
Seed 2 (id=114e911adf815ef0, size=102 bytes, fuzzer=naive, trial=1, discovered_at=8260s, mutation_op=CrossoverInsertMutator,BytesInsertCopyMutator,WordAddMutator,ByteRandMutator):
  0000: b4 00 1a e8 ff ff 00 01 0f 7f c1 05 00 19 00 00   ................
  0010: d2 d2 00 d2 d2 d2 bc bc d2 d2 0c 69 61 68 54 d2   ...........iahT.
  0020: ed d2 d2 00 0c 00 00 00 18 18 18 f7 0f 00 00 00   ................
  0030: fe 00 00 0c 20 00 21 00 00 00 00 fe 00 00 0c 20   .... .!........ 
Seed 3 (id=0dbe20c7b23ed0dc, size=101 bytes, fuzzer=naive, trial=1, discovered_at=11037s, mutation_op=BitFlipMutator,ByteDecMutator,ByteNegMutator,ByteInterestingMutator):
  0000: b4 00 1a 06 00 00 00 00 00 20 00 10 80 00 d2 17   ......... ......
  0010: 00 00 b6 16 00 00 01 01 0f 18 18 00 10 00 00 00   ................
  0020: 00 00 20 00 10 80 00 d2 17 00 00 b6 17 00 00 00   .. .............
  0030: 10 00 00 00 00 d2 17 00 00 00 10 00 00 00 10 00   ................
Seed 4 (id=006b5b05dac229fd, size=86 bytes, fuzzer=naive, trial=1, discovered_at=11221s, mutation_op=QwordAddMutator):
  0000: dc dc dc dc dc dc dc dc dc dc dc 0f ff e4 ff ff   ................
  0010: ff b6 b6 10 80 00 d2 17 00 00 b6 16 e7 00 00 10   ................
  0020: 00 00 d2 17 00 00 00 0f 00 00 00 10 00 00 d2 17   ................
  0030: 00 00 00 0f 00 00 00 10 00 00 d2 17 00 00 00 01   ................
Seed 5 (id=06efaf123de39528, size=185 bytes, fuzzer=naive, trial=1, discovered_at=14444s, mutation_op=BytesCopyMutator):
  0000: b4 00 1a e8 ff ff 00 01 0f 7f c1 05 00 19 00 00   ................
  0010: d2 d2 00 d2 d2 d2 bc 00 1a 06 00 00 4e d2 d2 d2   ............N...
  0020: bc 00 1a 06 00 00 4e 06 00 00 1a 80 00 00 00 06   ......N.........
  0030: 00 00 1a 06 00 00 04 00 cb 0c 00 00 00 00 1a 06   ................

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=6f605517948f68a7, size=100 bytes, fuzzer=cmplog, trial=1, discovered_at=584s, mutation_op=TokenReplace,BytesCopyMutator):
  0000: 20 20 20 20 ff 0f 0e 00 20 ff 0f 0e 00 20 df 6b       .... .... .k
  0010: 65 72 6e 02 02 02 7f 00 ff ff ff 7f 0d 01 9c 01   ern.............
  0020: e2 17 01 01 00 01 00 e5 e2 17 00 00 00 20 e2 9c   ............. ..
  0030: 20 40 0c 00 00 7f 20 12 00 1d 01 00 cc 25 00 00    @.... ......%..
Seed 2 (id=722bbd9afe1477c7, size=61 bytes, fuzzer=cmplog, trial=1, discovered_at=670s, mutation_op=WordAddMutator,BytesRandInsertMutator,DwordInterestingMutator,DwordAddMutator,ByteAddMutator,WordInterestingMutator,ByteInterestingMutator):
  0000: e2 17 00 00 be 17 00 00 c4 17 00 00 e2 17 00 10   ................
  0010: 00 e2 04 00 c4 17 04 e0 01 0a 00 01 10 00 ff 0a   ................
  0020: 00 17 0a 00 04 04 04 2d 20 03 00 20 20 00 02 00   .......- ..  ...
  0030: 20 2c 04 00 1a 20 e0 00 04 00 1a 20 e0             ,... ..... .
Seed 3 (id=2eb2c9d8a3cc389c, size=59 bytes, fuzzer=cmplog, trial=1, discovered_at=672s, mutation_op=BytesSetMutator,ByteDecMutator):
  0000: e0 17 00 00 c3 17 00 00 f0 16 00 00 01 e2 c4 c4   ................
  0010: c4 c4 c4 c4 c4 c4 c4 c4 c4 c4 c4 00 f0 16 00 00   ................
  0020: 01 e2 00 00 00 64 00 00 19 01 20 d4 66 68 70 72   .....d.... .fhpr
  0030: b6 b6 00 f1 00 00 04 00 1a 38 10                  .........8.
Seed 4 (id=20577f3ccd47ddf3, size=59 bytes, fuzzer=cmplog, trial=1, discovered_at=869s, mutation_op=ByteAddMutator,BytesInsertCopyMutator,BytesDeleteMutator,BytesInsertCopyMutator):
  0000: e0 17 00 00 c3 17 00 00 c5 17 00 00 01 e2 c4 c4   ................
  0010: c4 c4 c4 c4 c4 c4 c4 c4 c4 c4 c4 00 f0 16 00 80   ................
  0020: 7f 10 03 04 00 64 00 00 19 00 20 d4 66 68 70 72   .....d.... .fhpr
  0030: b6 b6 00 f1 04 00 04 00 1a 38 10                  .........8.
Seed 5 (id=02909d65a0dade40, size=64 bytes, fuzzer=cmplog, trial=1, discovered_at=954s, mutation_op=ByteAddMutator,BytesInsertCopyMutator,ByteIncMutator,WordAddMutator,TokenReplace,ByteIncMutator):
  0000: bf 17 00 00 01 00 e2 d5 00 00 00 00 17 00 00 01   ................
  0010: 01 20 20 a2 a2 a2 f0 e7 80 99 01 00 20 00 01 20   .  ......... .. 
  0020: ad f6 f6 f6 10 f6 f6 20 18 01 00 68 61 6e 73 00   ....... ...hans.
  0030: 6e 20 20 7f a0 00 00 00 c5 17 00 00 00 00 01 00   n  .............


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x4 b4(.)x4 dc(.)x1 5b([)x1     00(.)x3 e0(.)x2 20( )x1 e2(.)x1 +3u  PARTIAL
   0x0001  00(.)x7 dc(.)x1 4e(N)x1 06(.)x1     17(.)x4 6e(n)x3 00(.)x2 20( )x1     PARTIAL
   0x0002  1a(.)x4 04(.)x2 00(.)x2 dc(.)x1 +1u  00(.)x5 70(p)x3 20( )x1 01(.)x1     PARTIAL
   0x0003  00(.)x4 e8(.)x2 06(.)x1 dc(.)x1 +2u  00(.)x5 1c(.)x3 20( )x2             PARTIAL
   0x0006  00(.)x8 dc(.)x1 04(.)x1             00(.)x7 0e(.)x1 e2(.)x1 17(.)x1     PARTIAL
   0x0007  00(.)x4 01(.)x2 dc(.)x1 19(.)x1 +2u  00(.)x7 d5(.)x1 0a(.)x1 01(.)x1     PARTIAL
   0x000a  00(.)x7 c1(.)x2 dc(.)x1             00(.)x7 0f(.)x1 0a(.)x1 02(.)x1     PARTIAL
   0x000b  00(.)x3 05(.)x2 10(.)x1 0f(.)x1 +3u  00(.)x8 0e(.)x1 04(.)x1             PARTIAL
   0x000e  00(.)x7 d2(.)x1 ff(.)x1 e8(.)x1     00(.)x6 c4(.)x2 df(.)x1 0d(.)x1     PARTIAL
   0x0014  00(.)x5 d2(.)x3 80(.)x1 7f(.)x1     c4(.)x3 c5(.)x2 02(.)x1 a2(.)x1 +3u  DIFFER
   0x001b  00(.)x5 69(i)x1 16(.)x1 d2(.)x1 +2u  00(.)x7 7f(.)x1 01(.)x1 76(v)x1     PARTIAL
   0x001f  00(.)x5 d2(.)x4 10(.)x1             00(.)x4 01(.)x1 0a(.)x1 80(.)x1 +3u  PARTIAL
   0x0026  00(.)x7 4e(N)x1 69(i)x1 b4(.)x1     00(.)x5 04(.)x1 f6(.)x1 c5(.)x1 +2u  PARTIAL
   0x002d  00(.)x10                            00(.)x3 68(h)x2 a1(.)x2 20( )x1 +2u  PARTIAL
   0x0031  00(.)x8 10(.)x1 06(.)x1             b6(.)x2 00(.)x2 40(@)x1 2c(,)x1 +3u  PARTIAL
   0x0032  00(.)x8 1d(.)x1 1a(.)x1             00(.)x2 0c(.)x1 04(.)x1 20( )x1 +4u  PARTIAL
   0x0034  00(.)x6 20( )x2 4e(N)x1             00(.)x4 1a(.)x1 04(.)x1 a0(.)x1 +2u  PARTIAL
   0x0035  00(.)x6 d2(.)x1 01(.)x1 06(.)x1     00(.)x4 7f(.)x1 20( )x1 01(.)x1 +1u  PARTIAL
   0x0037  00(.)x6 10(.)x2 0f(.)x1             00(.)x4 10(.)x2 12(.)x1 31(1)x1     PARTIAL
   0x003c  00(.)x7 2d(-)x1 ff(.)x1             00(.)x2 cc(.)x1 e0(.)x1 55(U)x1 +1u  PARTIAL
   0x003d  00(.)x6 68(h)x1 05(.)x1 d2(.)x1     00(.)x2 25(%)x1 f5(.)x1             PARTIAL
   0x003e  1a(.)x2 0c(.)x1 10(.)x1 00(.)x1 +4u  00(.)x1 01(.)x1 f5(.)x1 20( )x1     PARTIAL
   0x003f  00(.)x3 06(.)x2 20( )x1 01(.)x1 +2u  00(.)x3 10(.)x1                     PARTIAL
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
  prompts_b/harfbuzz_5920.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5920,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5920 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5920 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5920 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).