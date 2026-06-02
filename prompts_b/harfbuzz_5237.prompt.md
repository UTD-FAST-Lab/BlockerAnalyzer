==== BLOCKER ====
Target: harfbuzz
Branch ID: 5237
Location: /src/harfbuzz/src/OT/Layout/GPOS/GPOS.hh:151:7
Enclosing function: OT::Layout::GPOS::position_finish_offsets(hb_font_t*, hb_buffer_t*)
Source line:   if (buffer->scratch_flags & HB_BUFFER_SCRATCH_FLAG_HAS_GPOS_ATTACHMENT)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (value_profile vs value_profile); loser (calibrated_energy vs minimizer); loser (ctx_coverage vs naive_ctx)
cmplog                           1        9          0  REFERENCE
value_profile                    9        1          0  winner (value_profile vs naive); winner (I2S vs value_profile_cmplog)
value_profile_cmplog             2        8          0  loser (I2S vs value_profile)
naive_ctx                        8        2          0  winner (ctx_coverage vs naive)
naive_ngram4                     2        8          0  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        9        1          0  winner (calibrated_energy vs naive)
fast                             9        1          0  REFERENCE
grimoire                         3        7          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['minimizer', 'naive', 'naive_ctx', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'naive_ngram4', 'mopt', 'fast', 'grimoire']

==== DECISIVE PAIRS (4) ====
--- Pair 1: value_profile > naive  [delta: value_profile] ---
  subject 12  (value_profile vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.90h  loser=21.80h
  avg hitcount on branch: winner=105  loser=15
  prob_div=0.70  dur_div=9.90h  hit_div=90
  subject-level: delta_AUC=17795340.0  p_AUC=0.0002  delta_Final=285.0  p_final=0.0002
--- Pair 2: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.90h  loser=21.50h
  avg hitcount on branch: winner=105  loser=6
  prob_div=0.70  dur_div=9.60h  hit_div=99
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002
--- Pair 3: minimizer > naive  [delta: calibrated_energy] ---
  subject 18  (minimizer vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=7.30h  loser=21.80h
  avg hitcount on branch: winner=208  loser=15
  prob_div=0.70  dur_div=14.50h  hit_div=193
  subject-level: delta_AUC=13277160.0  p_AUC=0.001  delta_Final=189.1  p_final=0.001
--- Pair 4: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 15  (naive_ctx vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=13.20h  loser=21.80h
  avg hitcount on branch: winner=166  loser=15
  prob_div=0.60  dur_div=8.60h  hit_div=151
  subject-level: delta_AUC=15634800.0  p_AUC=0.0003  delta_Final=258.3  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5237/{W,L}/branch_coverage_show.txt

--- Enclosing function: OT::Layout::GPOS::position_finish_offsets(hb_font_t*, hb_buffer_t*) (/src/harfbuzz/src/OT/Layout/GPOS/GPOS.hh:143-161) ---
[ ]   141  void
[ ]   142  GPOS::position_finish_offsets (hb_font_t *font, hb_buffer_t *buffer)
[B]   143  {
[B]   144    _hb_buffer_assert_gsubgpos_vars (buffer);
[ ]   145  
[B]   146    unsigned int len;
[B]   147    hb_glyph_position_t *pos = hb_buffer_get_glyph_positions (buffer, &len);
[B]   148    hb_direction_t direction = buffer->props.direction;
[ ]   149  
[ ]   150    /* Handle attachments */
[B]   151    if (buffer->scratch_flags & HB_BUFFER_SCRATCH_FLAG_HAS_GPOS_ATTACHMENT) <-- BLOCKER
[W]   152      for (unsigned i = 0; i < len; i++)
[W]   153        propagate_attachment_offsets (pos, len, i, direction);
[ ]   154  
[B]   155    if (unlikely (font->slant))
[ ]   156    {
[ ]   157      for (unsigned i = 0; i < len; i++)
[ ]   158        if (unlikely (pos[i].y_offset))
[ ]   159          pos[i].x_offset += _hb_roundf (font->slant_xy * pos[i].y_offset);
[ ]   160    }
[B]   161  }

--- Caller (1 hop): hb_ot_layout_position_finish_offsets(hb_font_t*, hb_buffer_t*) (/src/harfbuzz/src/hb-ot-layout.cc:1640-1642, calls OT::Layout::GPOS::position_finish_offsets(hb_font_t*, hb_buffer_t*) at line 1641) (full body — short) ---
[B]  1640  {
[B]  1641    GPOS::position_finish_offsets (font, buffer); <-- CALL
[B]  1642  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb_ot_layout_position_finish_offsets(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1640-1642, calls OT::Layout::GPOS::position_finish_offsets(hb_font_t*, hb_buffer_t*) at line 1641)
hop 3  hb-ot-shape.cc:hb_ot_position_plan(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:1022-1097, calls hb_ot_layout_position_finish_offsets(hb_font_t*, hb_buffer_t*) at line 1085)
hop 4  hb-ot-shape.cc:hb_ot_position(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:1101-1112, calls hb-ot-shape.cc:hb_ot_position_plan(hb_ot_shape_context_t const*) at line 1106)
hop 5  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195, calls hb-ot-shape.cc:hb_ot_position(hb_ot_shape_context_t const*) at line 1185)
hop 6  _hb_ot_shape  (/src/harfbuzz/src/hb-ot-shape.cc:1204-1209, calls hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*) at line 1206)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
    3150         0  hb-aat-layout.cc:OT::Layout::propagate_attachment_offsets(hb_glyph_position_t*, unsigned int, unsigned int, hb_direction_t, unsigned int)  (/src/harfbuzz/src/OT/Layout/GPOS/GPOS.hh:80-125)
    3150         0  hb-ot-face.cc:OT::Layout::propagate_attachment_offsets(hb_glyph_position_t*, unsigned int, unsigned int, hb_direction_t, unsigned int)  (/src/harfbuzz/src/OT/Layout/GPOS/GPOS.hh:80-125)
    3150         0  hb-ot-layout.cc:OT::Layout::propagate_attachment_offsets(hb_glyph_position_t*, unsigned int, unsigned int, hb_direction_t, unsigned int)  (/src/harfbuzz/src/OT/Layout/GPOS/GPOS.hh:80-125)
    3150         0  hb-ot-shape-fallback.cc:OT::Layout::propagate_attachment_offsets(hb_glyph_position_t*, unsigned int, unsigned int, hb_direction_t, unsigned int)  (/src/harfbuzz/src/OT/Layout/GPOS/GPOS.hh:80-125)
      90       483  void hb_ot_map_t::apply<GSUBProxy>(GSUBProxy const&, hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) const  (/src/harfbuzz/src/hb-ot-layout.cc:1948-1998)
      90       483  void hb_ot_map_t::apply<GPOSProxy>(GPOSProxy const&, hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) const  (/src/harfbuzz/src/hb-ot-layout.cc:1948-1998)
      90       399  OT::Layout::GPOS::position_start(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/OT/Layout/GPOS/GPOS.hh:129-133)
      90       399  OT::Layout::GPOS::position_finish_advances(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/OT/Layout/GPOS/GPOS.hh:137-139)
      90       399  OT::Layout::GPOS::position_finish_offsets(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/OT/Layout/GPOS/GPOS.hh:143-161)  <-- enclosing
      90       399  hb-ot-layout.cc:_hb_ot_layout_set_glyph_props(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:255-265)
      90       399  hb_ot_layout_substitute_start(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1510-1512)
      90       399  hb_ot_layout_position_start(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1611-1613)
      90       399  hb_ot_layout_position_finish_advances(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1626-1628)
      90       399  hb_ot_layout_position_finish_offsets(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1640-1642)
      90       399  GSUBProxy::GSUBProxy(hb_face_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1833-1834)
... (8 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OT::Layout::GPOS::position_finish_offsets(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/OT/Layout/GPOS/GPOS.hh:143-161) ---
  d=1   L 151  T=89 F=1  T=0 F=399  if (buffer->scratch_flags & HB_BUFFER_SCRATCH_FLAG_HAS_GP...  <-- BLOCKER
  d=1   L 152  T=1620 F=89  T=0 F=0  for (unsigned i = 0; i < len; i++)

[off-chain: 10 additional divergent branches across 5 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=4d132b760aa030c6, size=183 bytes, fuzzer=minimizer, trial=1, discovered_at=2659s, mutation_op=BytesInsertMutator):
  0000: 00 01 00 00 00 01 46 20 20 e0 28 f6 6b 65 72 6e   ......F  .(.kern
  0010: 00 00 00 01 00 00 00 10 00 7f 00 10 00 00 10 00   ................
  0020: 7f 00 00 20 02 40 00 01 00 00 16 01 2c 20 20 2d   ... .@......,  -
  0030: 68 61 6e 73 00 00 00 00 00 1a 65 72 6e 20 00 00   hans......ern ..
Seed 2 (id=449fa4ce94fc559a, size=116 bytes, fuzzer=minimizer, trial=1, discovered_at=3240s, mutation_op=DwordInterestingMutator,ByteDecMutator,ByteAddMutator):
  0000: 00 01 00 00 00 01 4d 20 20 20 00 64 6b 65 72 6e   ......M   .dkern
  0010: 00 00 00 01 00 00 00 10 00 7f 00 02 00 00 00 00   ................
  0020: 00 00 00 00 00 00 00 ff 00 00 ef 00 05 f9 00 00   ................
  0030: e8 00 00 e8 0d 00 00 7f 18 64 00 80 80 80 80 80   .........d......
Seed 3 (id=1fcad0f16ec207ea, size=140 bytes, fuzzer=minimizer, trial=1, discovered_at=3241s, mutation_op=ByteIncMutator):
  0000: 00 01 00 00 00 01 4d 20 20 20 00 64 6b 65 72 6e   ......M   .dkern
  0010: 00 00 00 01 00 00 00 10 00 7f 00 03 00 00 00 00   ................
  0020: 00 00 00 00 00 00 ff 00 00 00 ef 00 18 00 00 00   ................
  0030: e8 00 00 e8 0d 00 00 7f 18 64 00 80 80 80 80 80   .........d......
Seed 4 (id=2f8b0304762c6b0e, size=145 bytes, fuzzer=minimizer, trial=1, discovered_at=3953s, mutation_op=ByteAddMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 01 46 20 20 0b 28 0a 6b 65 72 6e   ......F  .(.kern
  0010: 00 00 00 01 00 00 00 10 02 05 00 00 00 40 00 1a   .............@..
  0020: 00 00 00 03 00 00 00 03 00 00 00 fe 00 00 e0 1c   ................
  0030: 00 00 01 00 0d 00 b5 b4 b4 b4 b4 b4 4c b4 b4 b4   ............L...
Seed 5 (id=4c02e66d520468b0, size=293 bytes, fuzzer=minimizer, trial=1, discovered_at=8386s, mutation_op=CrossoverInsertMutator,ByteNegMutator,DwordInterestingMutator,ByteNegMutator,ByteDecMutator,CrossoverInsertMutator,ByteAddMutator):
  0000: 00 01 00 00 00 01 46 20 20 e0 28 f6 6b 65 72 6e   ......F  .(.kern
  0010: 00 00 00 01 00 00 00 10 00 7f 00 10 00 00 10 00   ................
  0020: 7f 00 00 20 02 40 00 0a 00 00 16 01 2c 10 00 00   ... .@......,...
  0030: 00 db db 00 35 00 00 00 00 f5 00 2c 10 00 00 68   ....5......,...h

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=003817559785f774, size=6 bytes, fuzzer=naive, trial=1, discovered_at=0s, mutation_op=ByteDecMutator,WordAddMutator):
  0000: 87 0e 0d 0e 22 0e                                 ....".
Seed 2 (id=002edec370c771cf, size=35 bytes, fuzzer=naive, trial=1, discovered_at=47s, mutation_op=BytesExpandMutator,BytesDeleteMutator,ByteNegMutator,TokenInsert,ByteIncMutator,ByteRandMutator):
  0000: 00 00 00 00 00 00 00 00 00 00 00 00 20 00 64 6f   ............ .do
  0010: 2d 68 0a 6f 74 00 0e 00 20 00 0c 00 0c 09 00 00   -h.ot... .......
  0020: 00 0c 00                                          ...
Seed 3 (id=0016e7ecc5a956f6, size=64 bytes, fuzzer=naive, trial=1, discovered_at=308s, mutation_op=BytesRandInsertMutator,ByteRandMutator):
  0000: 00 75 fe 2d 68 67 68 77 72 75 75 75 80 17 00 00   .u.-hghwruuu....
  0010: 00 20 00 00 23 91 01 9f 9f 9f 9f f3 00 00 00 00   . ..#...........
  0020: 00 00 02 02 02 02 02 02 02 02 00 00 00 00 00 00   ................
  0030: fe fc fe ff 01 20 00 00 00 00 10 00 00 a7 00 00   ..... ..........
Seed 4 (id=0024e76787b8341b, size=25 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=313s, mutation_op=BytesExpandMutator,TokenInsert,TokenInsert,CrossoverInsertMutator):
  0000: 01 e9 01 00 e0 1f 01 00 7f ff ff ff ff ff 01 00   ................
  0010: 00 00 02 fd ff ff ff 2d 06                        .......-.
Seed 5 (id=0002ee9aae2b9bef, size=54 bytes, fuzzer=naive, trial=1, discovered_at=470s, mutation_op=WordInterestingMutator,TokenInsert,BytesExpandMutator,ByteInterestingMutator):
  0000: 00 ff 00 00 1d 20 00 00 c8 0a 01 00 70 78 2d 68   ..... ......px-h
  0010: 61 6e 74 2d 68 6b 00 74 40 01 00 00 00 20 01 00   ant-hk.t@.... ..
  0020: c8 0a 01 00 40 62 91 6d 00 00 00 20 01 00 c8 7f   ....@b.m... ....
  0030: 01 00 40 62 91 6d                                 ..@b.m


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x30                            00(.)x12 05(.)x2 87(.)x1 01(.)x1 +4u  PARTIAL
   0x0001  01(.)x30                            01(.)x9 00(.)x2 07(.)x2 0e(.)x1 +6u  PARTIAL
   0x0002  00(.)x30                            00(.)x14 0d(.)x1 fe(.)x1 01(.)x1 +3u  PARTIAL
   0x0003  00(.)x30                            00(.)x15 2d(-)x2 0e(.)x1 cb(.)x1 +1u  PARTIAL
   0x0004  00(.)x30                            00(.)x11 68(h)x2 70(p)x2 22(")x1 +4u  PARTIAL
   0x0005  01(.)x16 04(.)x8 03(.)x5 02(.)x1    02(.)x9 0e(.)x1 00(.)x1 67(g)x1 +8u  PARTIAL
   0x000c  6b(k)x30                            47(G)x8 ff(.)x2 20( )x1 80(.)x1 +7u  DIFFER
   0x000d  65(e)x30                            50(P)x5 00(.)x3 53(S)x3 17(.)x1 +7u  DIFFER
   0x000e  72(r)x30                            4f(O)x5 55(U)x3 00(.)x2 01(.)x2 +7u  DIFFER
   0x000f  6e(n)x30                            53(S)x5 00(.)x3 42(B)x3 6f(o)x1 +7u  DIFFER
   0x0011  00(.)x10 df(.)x10 20( )x9 fd(.)x1   20( )x8 0f(.)x3 00(.)x2 68(h)x1 +5u  PARTIAL
   0x0014  00(.)x30                            00(.)x10 68(h)x3 74(t)x1 23(#)x1 +4u  PARTIAL
   0x0015  00(.)x30                            00(.)x12 91(.)x1 ff(.)x1 6b(k)x1 +4u  PARTIAL
   0x0016  00(.)x30                            00(.)x13 0e(.)x1 01(.)x1 ff(.)x1 +3u  PARTIAL
   0x0017  10(.)x10 1a(.)x10 35(5)x10          21(!)x9 00(.)x2 74(t)x2 9f(.)x1 +5u  DIFFER
   0x001a  00(.)x18 35(5)x7 56(V)x3 2d(-)x2    20( )x8 00(.)x3 0c(.)x1 9f(.)x1 +5u  PARTIAL
   0x0022  00(.)x20 80(.)x7 56(V)x2 2d(-)x1    01(.)x11 00(.)x2 02(.)x1 61(a)x1 +1u  PARTIAL
   0x0033  00(.)x13 08(.)x4 10(.)x4 66(f)x3 +5u  00(.)x11 ff(.)x2 62(b)x1 b6(.)x1    PARTIAL
   0x0037  00(.)x10 69(i)x5 10(.)x4 04(.)x3 +6u  00(.)x12 ff(.)x1 57(W)x1            PARTIAL
==== MECHANISM CONTEXT (involved fuzzers only) ====
--- minimizer ---
**Instrumentation**: naive's edge counters only.

**Feedback**: naive's edge-bucket `MaxMapFeedback`, plus a
`CalibrationStage` that measures each new corpus entry's execution
time, edge-map fill, and stability into `SchedulerMetadata`/testcase
metadata.

**Mutators / stages**: havoc + token mutator (`LineageMutator`, names
captured) run inside a `StdPowerMutationalStage` rather than naive's
plain `StdMutationalStage`. Stages are `[calibration, power]`. The
power stage derives the number of havoc mutations per seed visit (the
"energy") from a calibration-based `perf_score` — faster, smaller,
more-stable seeds earn more mutations. PowerSchedule is `None`, so the
energy uses ONLY intrinsic calibration and is NOT weighted by how often
a region has been hit. Corpus selection is plain FIFO `QueueScheduler`
(same order as naive).

**Observed `mutation_op` in seed metadata**: havoc/token names
(captured); no dash rows.

**Per-execution cost**: one edge increment per edge, plus a one-time
calibration burst per new corpus entry.

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

--- naive_ctx ---
**Instrumentation**: naive's SanitizerCoverage edge counters, but the
executor installs a `CtxHook` (`HookableInProcessExecutor`). The hook
keeps a running hash of the current call context (caller chain) and
folds it into the edge-map index, so the same basic-block edge is
recorded at different map slots depending on the call path that
reached it.

**Feedback**: the same `MaxMapFeedback` edge-bucket signal as naive,
computed over the context-indexed map — a "new bucket" is a new
(call-context, edge) pair rather than a bare edge.

**Mutators**: naive's havoc + token stack. No `I2SRandReplace`, no
CMP_MAP. Stages are `[mutator]` (`LineageMutator`, names captured).

**Observed `mutation_op` in seed metadata**: havoc/token names only;
no ParentInfo-only / dash rows.

**Per-execution cost**: one edge-counter increment per executed edge
plus a context-hash update per call/return.

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
  prompts_b/harfbuzz_5237.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5237,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>naive (value_profile), value_profile>value_profile_cmplog (I2S), minimizer>naive (calibrated_energy), naive_ctx>naive (ctx_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5237 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5237 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5237 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).