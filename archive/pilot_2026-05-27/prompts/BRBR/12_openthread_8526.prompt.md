==== BLOCKER ====
Target: openthread
Branch ID: 8526
Location: /src/openthread/src/core/thread/mesh_forwarder.cpp:582:9
Enclosing function: ot::MeshForwarder::PrepareNextDirectTransmission()
Source line:         default:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     []

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 16  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.20h  loser=12.00h
  avg hitcount on branch: winner=166  loser=0
  prob_div=1.00  dur_div=11.80h  hit_div=166
  subject-level: delta_AUC=2557680.0  p_AUC=0.0002  delta_Final=165.0  p_final=0.0002
--- Pair 2: cmplog > naive  [delta: I2S] ---
  subject 13  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=0.05h  loser=11.75h
  avg hitcount on branch: winner=240  loser=0
  prob_div=0.90  dur_div=11.70h  hit_div=240
  subject-level: delta_AUC=2409450.0  p_AUC=0.0002  delta_Final=145.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/openthread/8526/{W,L}/branch_coverage_show.txt

--- Enclosing function: ot::MeshForwarder::PrepareNextDirectTransmission() (/src/openthread/src/core/thread/mesh_forwarder.cpp:515-591) ---
[ ]   513  
[ ]   514  Message *MeshForwarder::PrepareNextDirectTransmission(void)
[B]   515  {
[B]   516      Message *curMessage, *nextMessage;
[B]   517      Error    error = kErrorNone;
[ ]   518  
[B]   519      for (curMessage = mSendQueue.GetHead(); curMessage; curMessage = nextMessage)
[B]   520      {
[ ]   521          // We set the `nextMessage` here but it can be updated again
[ ]   522          // after the `switch(message.GetType())` since it may be
[ ]   523          // evicted during message processing (e.g., from the call to
[ ]   524          // `UpdateIp6Route()` due to Address Solicit).
[ ]   525  
[B]   526          nextMessage = curMessage->GetNext();
[ ]   527  
[B]   528          if (!curMessage->IsDirectTransmission() || curMessage->IsResolvingAddress())
[ ]   529          {
[ ]   530              continue;
[ ]   531          }
[ ]   532  
[B]   533  #if OPENTHREAD_CONFIG_DELAY_AWARE_QUEUE_MANAGEMENT_ENABLE
[B]   534          if (UpdateEcnOrDrop(*curMessage) == kErrorDrop)
[L]   535          {
[L]   536              continue;
[L]   537          }
[B]   538  #endif
[B]   539          curMessage->SetDoNotEvict(true);
[ ]   540  
[B]   541          switch (curMessage->GetType())
[B]   542          {
[B]   543          case Message::kTypeIp6:
[B]   544              error = UpdateIp6Route(*curMessage);
[B]   545              break;
[ ]   546  
[ ]   547  #if OPENTHREAD_FTD
[ ]   548  
[ ]   549          case Message::kType6lowpan:
[ ]   550              error = UpdateMeshRoute(*curMessage);
[ ]   551              break;
[ ]   552  
[ ]   553  #endif
[ ]   554  
[ ]   555  #if OPENTHREAD_CONFIG_REFERENCE_DEVICE_ENABLE
[ ]   556          case Message::kTypeMacEmptyData:
[ ]   557              error = kErrorNone;
[ ]   558              break;
[ ]   559  #endif
[ ]   560  
[ ]   561          default:
[ ]   562              error = kErrorDrop;
[ ]   563              break;
[B]   564          }
[ ]   565  
[B]   566          curMessage->SetDoNotEvict(false);
[ ]   567  
[ ]   568          // the next message may have been evicted during processing (e.g. due to Address Solicit)
[B]   569          nextMessage = curMessage->GetNext();
[ ]   570  
[B]   571          switch (error)
[B]   572          {
[B]   573          case kErrorNone:
[B]   574              ExitNow();
[ ]   575  
[ ]   576  #if OPENTHREAD_FTD
[ ]   577          case kErrorAddressQuery:
[ ]   578              curMessage->SetResolvingAddress(true);
[ ]   579              continue;
[ ]   580  #endif
[ ]   581  
[W]   582          default: <-- BLOCKER
[W]   583              LogMessage(kMessageDrop, *curMessage, error);
[W]   584              mSendQueue.DequeueAndFree(*curMessage);
[W]   585              continue;
[B]   586          }
[B]   587      }
[ ]   588  
[B]   589  exit:
[B]   590      return curMessage;
[B]   591  }

--- Caller (1 hop): ot::MeshForwarder::ScheduleTransmissionTask() (/src/openthread/src/core/thread/mesh_forwarder.cpp:493-512, calls ot::MeshForwarder::PrepareNextDirectTransmission() at line 500) (full body — short) ---
[B]   493  {
[B]   494      VerifyOrExit(!mSendBusy && !mTxPaused);
[ ]   495  
[B]   496  #if OPENTHREAD_FTD && OPENTHREAD_CONFIG_MAC_COLLISION_AVOIDANCE_DELAY_ENABLE
[B]   497      VerifyOrExit(!mDelayNextTx);
[B]   498  #endif
[ ]   499  
[B]   500      mSendMessage = PrepareNextDirectTransmission(); <-- CALL
[B]   501      VerifyOrExit(mSendMessage != nullptr);
[ ]   502  
[B]   503      if (mSendMessage->GetOffset() == 0)
[B]   504      {
[B]   505          mSendMessage->SetTxSuccess(true);
[B]   506      }
[ ]   507  
[B]   508      Get<Mac::Mac>().RequestDirectFrameTransmission();
[ ]   509  
[B]   510  exit:
[B]   511      return;
[B]   512  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  ot::MeshForwarder::ScheduleTransmissionTask()  (/src/openthread/src/core/thread/mesh_forwarder.cpp:493-512, calls ot::MeshForwarder::PrepareNextDirectTransmission() at line 500)

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  ot::MeshForwarder::ScheduleTransmissionTask()  (/src/openthread/src/core/thread/mesh_forwarder.cpp:493-512) ---
  d=2   L 503  T=60 F=0  T=98 F=7  if (mSendMessage->GetOffset() == 0)
--- d=1  ot::MeshForwarder::PrepareNextDirectTransmission()  (/src/openthread/src/core/thread/mesh_forwarder.cpp:515-591) ---
  d=1   L 534  T=0 F=79  T=5 F=105  if (UpdateEcnOrDrop(*curMessage) == kErrorDrop)
  d=1   L 573  T=60 F=19  T=105 F=0  case kErrorNone:
  d=1   L 582  T=19 F=60  T=0 F=105  default:  <-- BLOCKER

[off-chain: 27 additional divergent branches across 6 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=2d0d9b87803c3479, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=52s, mutation_op=TokenInsert,BytesRandSetMutator,WordAddMutator):
  0000: 78 66 65 5c 78 00 00 80 5c 78 30 30 5c 78 30 30   xfe\x...\x00\x00
  0010: 5c 78 33 62 5c 78 34 30 5c fd de ad 00 be ef 00   \x3b\x40\.......
  0020: 00 00 00 00 ff fe 00 80 00                        .........
Seed 2 (id=23ef6000356aac6c, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=73s, mutation_op=TokenInsert):
  0000: 78 66 65 5c 78 00 00 0f ff 78 30 30 5c 78 30 01   xfe\x....x00\x0.
  0010: 5c 78 33 62 5c 78 47 3c 5c fd de ad 00 be ef 00   \x3b\xG<\.......
  0020: 00 00 00 00 ff fe 00 fc 30                        ........0
Seed 3 (id=2da935a6ae5165e2, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=489s, mutation_op=BytesSwapMutator,ByteDecMutator):
  0000: 77 66 65 5c 7e 00 10 00 be 06 00 80 c3 ff ff ff   wfe\~...........
  0010: fe 00 fc 30 5c 78 30 30 5c fd de ad 00 be ef 00   ...0\x00\.......
  0020: 00 00 00 00 ff fe 00 9c 00 3a 00 6d 03 5c 78 13   .........:.m.\x.
  0030: 00 04 5c 47 3c 66 66 66 66                        ..\G<ffff
Seed 4 (id=29fb4468872247c9, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=1011s, mutation_op=ByteInterestingMutator,BytesSetMutator):
  0000: 77 66 65 10 00 00 10 00 be ef 00 d9 ff ff 00 00   wfe.............
  0010: fe 04 fc 30 5c 78 36 30 5d fd de ad 00 be ef 00   ...0\x60].......
  0020: 00 00 00 00 ff fe 00 30 01 29 01 6d 01 5c 6d 01   .......0.).m.\m.
  0030: 5c 6d 06 5c 78 33 34 30 71                        \m.\x340q
Seed 5 (id=03da72304f643e8f, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=1447s, mutation_op=BitFlipMutator):
  0000: 77 66 65 5c 7e 00 10 00 be ef 59 f4 00 00 00 1f   wfe\~.....Y.....
  0010: fe 00 fe 30 5c 78 30 30 00 fd de ad 00 be ef 00   ...0\x00........
  0020: 00 00 00 00 ff fe 00 fc 40 07 00 6d 02 5c 78 6d   ........@..m.\xm
  0030: 00 40 ff ff 3c ff 71 93 70                        .@..<.q.p

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=003de3dead0e140f, size=82 bytes, fuzzer=naive, trial=1, discovered_at=164s, mutation_op=ByteFlipMutator):
  0000: 7f 65 ef 00 00 00 29 29 29 29 29 29 29 29 29 29   .e....))))))))))
  0010: 29 29 ff 28 29 29 00 ff 7f ff ff ff 40 13 20 5c   )).())......@. \
  0020: 5c 5c 5c 5c 30 30 5c 78 34 cf 00 00 00 02 00 00   \\\\00\x4.......
  0030: ff 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
Seed 2 (id=011d58e917a7cca6, size=141 bytes, fuzzer=naive, trial=1, discovered_at=3472s, mutation_op=DwordInterestingMutator):
  0000: 81 65 10 00 13 00 64 00 01 10 04 00 00 66 65 5c   .e....d......fe\
  0010: 88 64 87 87 87 87 87 87 7f ff 53 ff ff ff ff ff   .d........S.....
  0020: 00 08 30 9c c4 20 00 00 00 00 00 00 00 00 00 6d   ..0.. .........m
  0030: 00 00 01 02 02 00 10 00 00 00 6d 00 6d 00 6d 00   ..........m.m.m.
Seed 3 (id=002b6399f7108e3c, size=141 bytes, fuzzer=naive, trial=1, discovered_at=4045s, mutation_op=BytesSetMutator):
  0000: 81 65 24 00 13 00 64 00 5c 5c 5c 5c 5c 5c 5c 5c   .e$...d.\\\\\\\\
  0010: 88 87 87 87 7c 87 87 87 7f ff 53 ff ff ff ff ff   ....|.....S.....
  0020: 00 08 30 9b c4 20 00 6d 00 d7 02 00 10 00 08 00   ..0.. .m........
  0030: 6d 00 6d 00 6d 03 6d 00 7f 00 6d 00 6d 03 6d f2   m.m.m.m...m.m.m.
Seed 4 (id=00ac3d97d5418009, size=141 bytes, fuzzer=naive, trial=1, discovered_at=4802s, mutation_op=ByteFlipMutator,ByteFlipMutator,WordAddMutator,WordAddMutator):
  0000: 81 65 2e 00 13 00 64 00 fe c3 09 00 00 66 65 5c   .e....d......fe\
  0010: 81 87 87 87 7c 78 87 87 5f ff 53 ff ff ff ff ff   ....|x.._.S.....
  0020: 00 08 30 9c a1 20 00 00 00 00 00 00 00 00 00 6d   ..0.. .........m
  0030: 00 29 00 02 00 08 00 6d 00 40 7f ff 00 71 00 11   .).....m.@...q..
Seed 5 (id=00a7c40b3a8bf88e, size=141 bytes, fuzzer=naive, trial=1, discovered_at=5904s, mutation_op=BytesCopyMutator):
  0000: 80 65 24 00 13 00 64 00 01 00 00 00 00 00 00 00   .e$...d.........
  0010: 01 87 87 87 7c 17 87 87 7f ff 53 00 00 00 00 00   ....|.....S.....
  0020: 00 00 00 00 00 00 00 00 00 00 00 00 0e 00 00 6d   ...............m
  0030: 00 29 00 02 00 08 00 6d 00 64 15 5f 57 1b 43 29   .).....m.d._W.C)


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  77(w)x4 78(x)x3 74(t)x3             80(.)x5 81(.)x4 7f(.)x1             DIFFER
   0x0001  66(f)x10                            65(e)x9 6e(n)x1                     DIFFER
   0x0002  65(e)x10                            24($)x2 23(#)x2 40(@)x2 ef(.)x1 +3u  DIFFER
   0x0003  5c(\)x5 10(.)x4 0a(.)x1             00(.)x10                            DIFFER
   0x0004  00(.)x5 78(x)x2 7e(~)x2 77(w)x1     13(.)x6 00(.)x4                     PARTIAL
   0x0006  10(.)x5 80(.)x3 00(.)x2             64(d)x6 29())x4                     DIFFER
   0x0007  00(.)x4 07(.)x2 80(.)x1 0f(.)x1 +2u  00(.)x9 29())x1                     PARTIAL
   0x0008  be(.)x7 5c(\)x1 ff(.)x1 b0(.)x1     01(.)x4 ff(.)x2 29())x1 5c(\)x1 +2u  PARTIAL
   0x0009  ef(.)x6 78(x)x2 06(.)x1 fd(.)x1     f0(.)x2 80(.)x2 29())x1 10(.)x1 +4u  DIFFER
   0x0011  00(.)x3 d0(.)x3 78(x)x2 04(.)x2     87(.)x3 7e(~)x2 40(@)x2 29())x1 +2u  PARTIAL
   0x0012  fc(.)x3 5c(\)x3 33(3)x2 fe(.)x1 +1u  87(.)x6 30(0)x2 ff(.)x1 00(.)x1     PARTIAL
   0x0013  30(0)x4 78(x)x3 62(b)x2 00(.)x1     87(.)x6 26(&)x2 28(()x1 00(.)x1     PARTIAL
   0x0014  5c(\)x5 29())x3 58(X)x1 ff(.)x1     7c(|)x5 29())x3 87(.)x1 bf(.)x1     PARTIAL
   0x0015  78(x)x6 01(.)x2 fe(.)x1 00(.)x1     87(.)x4 29())x2 28(()x2 78(x)x1 +1u  PARTIAL
   0x0016  6d(m)x3 30(0)x2 36(6)x2 34(4)x1 +2u  87(.)x6 00(.)x2 ff(.)x2             DIFFER
   0x0017  30(0)x5 01(.)x3 3c(<)x1 fc(.)x1     87(.)x6 ff(.)x3 13(.)x1             DIFFER
   0x0018  5c(\)x3 80(.)x3 5d(])x2 00(.)x1 +1u  7f(.)x6 fd(.)x2 5f(_)x1 80(.)x1     PARTIAL
   0x0019  fd(.)x10                            ff(.)x9 fd(.)x1                     PARTIAL
   0x001a  de(.)x10                            53(S)x6 c3(.)x2 ff(.)x1 de(.)x1     PARTIAL
   0x001b  ad(.)x10                            ff(.)x6 00(.)x3 ad(.)x1             PARTIAL
   0x001c  00(.)x10                            00(.)x4 40(@)x3 ff(.)x3             PARTIAL
   0x001d  be(.)x10                            ff(.)x3 00(.)x3 01(.)x2 13(.)x1 +1u  PARTIAL
   0x001e  ef(.)x10                            ff(.)x3 00(.)x3 78(x)x2 20( )x1 +1u  DIFFER
   0x001f  00(.)x10                            ff(.)x3 00(.)x3 11(.)x2 5c(\)x1 +1u  PARTIAL
   0x0020  00(.)x10                            00(.)x6 30(0)x2 5c(\)x1 ad(.)x1     PARTIAL
   0x0021  00(.)x10                            5c(\)x3 08(.)x3 00(.)x3 ad(.)x1     PARTIAL
   0x0022  00(.)x10                            30(0)x3 00(.)x3 78(x)x2 5c(\)x1 +1u  PARTIAL
   0x0023  00(.)x10                            00(.)x3 9c(.)x2 30(0)x2 5c(\)x1 +2u  PARTIAL
   0x0024  ff(.)x10                            00(.)x3 c4(.)x2 16(.)x2 30(0)x1 +2u  DIFFER
   0x0025  fe(.)x10                            20( )x3 00(.)x3 16(.)x2 30(0)x1 +1u  DIFFER
   0x0026  00(.)x10                            00(.)x7 16(.)x2 5c(\)x1             PARTIAL
   0x0028  00(.)x5 30(0)x2 01(.)x2 40(@)x1     00(.)x6 16(.)x2 34(4)x1 01(.)x1     PARTIAL
   0x0029  5c(\)x3 29())x2 3a(:)x1 07(.)x1 +1u  00(.)x7 cf(.)x1 d7(.)x1 6d(m)x1     DIFFER
   0x002a  00(.)x3 78(x)x3 01(.)x2             00(.)x8 02(.)x1 03(.)x1             PARTIAL
   0x002b  6d(m)x4 30(0)x3 f0(.)x1             00(.)x7 6d(m)x3                     PARTIAL
   0x002c  30(0)x3 01(.)x2 03(.)x1 02(.)x1 +1u  00(.)x6 0e(.)x3 10(.)x1             DIFFER
   0x002d  5c(\)x7 be(.)x1                     00(.)x6 6d(m)x3 02(.)x1             DIFFER
   0x002e  78(x)x5 6d(m)x2 ef(.)x1             00(.)x9 08(.)x1                     DIFFER
   0x002f  31(1)x3 01(.)x2 13(.)x1 6d(m)x1 +1u  6d(m)x8 00(.)x2                     PARTIAL
   0x0030  30(0)x3 00(.)x2 5c(\)x2 ef(.)x1     00(.)x8 ff(.)x1 6d(m)x1             PARTIAL
   ... (15 more divergent offsets)
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
  prompts/BRBR/12_openthread_8526.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 8526,
  "target": "openthread",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S), cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 8526 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 8526 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 8526 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).