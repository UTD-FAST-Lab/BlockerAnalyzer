==== BLOCKER ====
Target: openthread
Branch ID: 8538
Location: /src/openthread/src/core/thread/network_data_leader.cpp:177:9
Enclosing function: ot::NetworkData::LeaderBase::GetContext(unsigned char, ot::Lowpan::Context&) const
Source line:     if (aContextId == Mle::kMeshLocalPrefixContextId)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     []

==== DECISIVE PAIRS (2) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 13  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.10h  loser=12.00h
  avg hitcount on branch: winner=76  loser=0
  prob_div=1.00  dur_div=11.90h  hit_div=76
  subject-level: delta_AUC=2409450.0  p_AUC=0.0002  delta_Final=145.4  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 16  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.80h  loser=12.00h
  avg hitcount on branch: winner=42  loser=0
  prob_div=1.00  dur_div=11.20h  hit_div=42
  subject-level: delta_AUC=2557680.0  p_AUC=0.0002  delta_Final=165.0  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/openthread/8538/{W,L}/branch_coverage_show.txt

--- Enclosing function: ot::NetworkData::LeaderBase::GetContext(unsigned char, ot::Lowpan::Context&) const (/src/openthread/src/core/thread/network_data_leader.cpp:172-201) ---
[ ]   170  
[ ]   171  Error LeaderBase::GetContext(uint8_t aContextId, Lowpan::Context &aContext) const
[B]   172  {
[B]   173      Error            error = kErrorNotFound;
[B]   174      TlvIterator      tlvIterator(GetTlvsStart(), GetTlvsEnd());
[B]   175      const PrefixTlv *prefixTlv;
[ ]   176  
[B]   177      if (aContextId == Mle::kMeshLocalPrefixContextId) <-- BLOCKER
[L]   178      {
[L]   179          GetContextForMeshLocalPrefix(aContext);
[L]   180          ExitNow(error = kErrorNone);
[L]   181      }
[ ]   182  
[W]   183      while ((prefixTlv = tlvIterator.Iterate<PrefixTlv>()) != nullptr)
[ ]   184      {
[ ]   185          const ContextTlv *contextTlv = prefixTlv->FindSubTlv<ContextTlv>();
[ ]   186  
[ ]   187          if ((contextTlv == nullptr) || (contextTlv->GetContextId() != aContextId))
[ ]   188          {
[ ]   189              continue;
[ ]   190          }
[ ]   191  
[ ]   192          prefixTlv->CopyPrefixTo(aContext.mPrefix);
[ ]   193          aContext.mContextId    = contextTlv->GetContextId();
[ ]   194          aContext.mCompressFlag = contextTlv->IsCompress();
[ ]   195          aContext.mIsValid      = true;
[ ]   196          ExitNow(error = kErrorNone);
[ ]   197      }
[ ]   198  
[B]   199  exit:
[B]   200      return error;
[W]   201  }

--- Caller (1 hop): ot::Lowpan::Lowpan::FindContextToCompressAddress(ot::Ip6::Address const&, ot::Lowpan::Context&) const (/src/openthread/src/core/thread/lowpan.cpp:66-73, calls ot::NetworkData::LeaderBase::GetContext(unsigned char, ot::Lowpan::Context&) const at line 67) (full body — short) ---
[B]    66  {
[B]    67      Error error = Get<NetworkData::Leader>().GetContext(aIp6Address, aContext); <-- CALL
[ ]    68  
[B]    69      if ((error != kErrorNone) || !aContext.mCompressFlag)
[B]    70      {
[B]    71          aContext.Clear();
[B]    72      }
[B]    73  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  ot::Coap::CoapBase::HandleRetransmissionTimer(ot::Timer&)  (/src/openthread/src/core/coap/coap.cpp:439-441, calls ot::NetworkData::LeaderBase::GetContext(unsigned char, ot::Lowpan::Context&) const at line 440)
hop 2  ot::MeshCoP::Dtls::HandleTimer(ot::Timer&)  (/src/openthread/src/core/meshcop/dtls.cpp:830-832, calls ot::NetworkData::LeaderBase::GetContext(unsigned char, ot::Lowpan::Context&) const at line 831)
hop 3  ot::MeshCoP::DatasetManager::HandleTimer()  (/src/openthread/src/core/meshcop/dataset_manager.cpp:241-241, calls ot::MeshCoP::Dtls::HandleTimer(ot::Timer&) at line 241)
hop 3  ot::MeshCoP::JoinerRouter::HandleTimer()  (/src/openthread/src/core/meshcop/joiner_router.cpp:234-234, calls ot::MeshCoP::Dtls::HandleTimer(ot::Timer&) at line 234)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0        72  ot::Lowpan::Lowpan::CompressExtensionHeader(ot::Message&, ot::FrameBuilder&, unsigned char&)  (/src/openthread/src/core/thread/lowpan.cpp:436-520)
       0        55  ot::NetworkData::LeaderBase::GetContextForMeshLocalPrefix(ot::Lowpan::Context&) const  (/src/openthread/src/core/thread/network_data_leader.cpp:204-209)
       0        47  ot::Lowpan::Lowpan::FindContextForId(unsigned char, ot::Lowpan::Context&) const  (/src/openthread/src/core/thread/lowpan.cpp:58-63)
      25         0  ot::NetworkData::LeaderBase::IsOnMesh(ot::Ip6::Address const&) const  (/src/openthread/src/core/thread/network_data_leader.cpp:212-238)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  ot::NetworkData::LeaderBase::GetContext(unsigned char, ot::Lowpan::Context&) const  (/src/openthread/src/core/thread/network_data_leader.cpp:172-201) ---
  d=1   L 177  T=0 F=25  T=47 F=0  if (aContextId == Mle::kMeshLocalPrefixContextId)  <-- BLOCKER
  d=1   L 183  T=0 F=25  T=0 F=0  while ((prefixTlv = tlvIterator.Iterate<PrefixTlv>()) != ...

[off-chain: 55 additional divergent branches across 11 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=42f0755109cd79b2, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=64s, mutation_op=DwordInterestingMutator,ByteIncMutator):
  0000: 78 66 65 5c 78 00 00 0f ff 78 30 30 5c 78 00 00   xfe\x....x00\x..
  0010: 01 00 33 62 5c 78 47 3c 5c fd de ad 00 be ef 00   ..3b\xG<\.......
  0020: 00 00 00 00 ff fe 00 fc 01                        .........
Seed 2 (id=8a4323d6185a6d11, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=91s, mutation_op=BytesRandSetMutator,ByteRandMutator,DwordInterestingMutator,ByteAddMutator):
  0000: 78 66 65 5c 78 00 00 0f ff 78 30 30 fa 00 00 fa   xfe\x....x00....
  0010: 17 17 17 17 17 17 47 3c 5c fd de ad 00 be ef 00   ......G<\.......
  0020: 00 00 00 00 ff fe 00 fc 43                        ........C
Seed 3 (id=79f0a9e708add6b2, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=423s, mutation_op=BytesRandInsertMutator,BytesExpandMutator,BytesRandSetMutator):
  0000: 77 66 e5 5c 7e 00 10 00 be ef 00 00 00 00 01 01   wf.\~...........
  0010: fe 00 fc 30 5c 78 30 30 5c fd de ad 00 be ef 00   ...0\x00\.......
  0020: 00 00 00 00 ff fe 00 fc 01 29 00 6d 02 5c 78 00   .........).m.\x.
  0030: 00 80 5c 47 3c ff 71 71 71                        ..\G<.qqq
Seed 4 (id=588b308108bd6154, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=794s, mutation_op=BytesSetMutator,WordAddMutator,BytesRandInsertMutator,BytesCopyMutator):
  0000: 77 66 65 5c 7e 00 10 00 be ef 59 f4 00 00 00 1f   wfe\~.....Y.....
  0010: fe 00 fc 30 5c 78 30 30 04 fd de ad 00 be ef 00   ...0\x00........
  0020: 00 00 00 00 ff fe 00 fc 01 07 00 6d 02 5c 78 6d   ...........m.\xm
  0030: 00 40 ff ff 3c ff 71 93 70                        .@..<.q.p
Seed 5 (id=4bc957df85d3ce9f, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=846s, mutation_op=ByteFlipMutator,CrossoverReplaceMutator,DwordAddMutator,BytesDeleteMutator,DwordAddMutator,BytesDeleteMutator):
  0000: 77 66 65 5c 7e 00 10 00 be ef 59 f4 5a 00 00 1f   wfe\~.....Y.Z...
  0010: fe 00 fc 30 5c 78 30 30 04 fd de ad 00 be ef 00   ...0\x00........
  0020: 00 00 00 00 ff fe 00 fc 01 07 00 6d 02 5c 78 6d   ...........m.\xm
  0030: 00 40 ff ff 3c ff 71 93 70                        .@..<.q.p

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=022dbf2ad819a43f, size=82 bytes, fuzzer=naive, trial=1, discovered_at=36s, mutation_op=ByteFlipMutator,TokenReplace):
  0000: 80 65 ef 00 00 00 29 29 29 29 29 29 29 29 29 29   .e....))))))))))
  0010: 29 29 ff 28 29 29 ff ff e6 ff ff ff 78 13 30 00   )).())......x.0.
  0020: 00 29 4b 29 90 5f 01 00 29 29 29 29 29 29 28 29   .)K)._..))))))()
  0030: 29 ff ff fd ff ff ff 79 13 30 5c 78 cf 30 5c 78   )......y.0\x.0\x
Seed 2 (id=003de3dead0e140f, size=82 bytes, fuzzer=naive, trial=1, discovered_at=164s, mutation_op=ByteFlipMutator):
  0000: 7f 65 ef 00 00 00 29 29 29 29 29 29 29 29 29 29   .e....))))))))))
  0010: 29 29 ff 28 29 29 00 ff 7f ff ff ff 40 13 20 5c   )).())......@. \
  0020: 5c 5c 5c 5c 30 30 5c 78 34 cf 00 00 00 02 00 00   \\\\00\x4.......
  0030: ff 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
Seed 3 (id=0192e8b18c01cf0c, size=82 bytes, fuzzer=naive, trial=1, discovered_at=352s, mutation_op=ByteNegMutator,QwordAddMutator,WordAddMutator):
  0000: 68 65 ef 00 00 00 29 29 2a 4a 29 29 29 31 29 01   he....))*J)))1).
  0010: 29 29 ff 28 29 29 ff 0e 7f ff 16 16 16 00 10 10   )).())..........
  0020: 21 d7 18 05 ff ff 05 29 29 00 40 00 00 29 29 29   !......)).@..)))
  0030: 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
Seed 4 (id=01720237e52d2b80, size=82 bytes, fuzzer=naive, trial=1, discovered_at=457s, mutation_op=BytesSetMutator):
  0000: 7f 65 ef 00 00 00 29 29 2a 29 29 29 29 32 29 8f   .e....))*))))2).
  0010: 90 90 90 28 29 29 ff ff 7f ff ff ff 7f 65 ef 00   ...()).......e..
  0020: 00 00 29 29 2a 29 29 29 29 32 00 00 00 00 00 29   ..))*))))2.....)
  0030: 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   @...............
Seed 5 (id=002b6399f7108e3c, size=141 bytes, fuzzer=naive, trial=1, discovered_at=4045s, mutation_op=BytesSetMutator):
  0000: 81 65 24 00 13 00 64 00 5c 5c 5c 5c 5c 5c 5c 5c   .e$...d.\\\\\\\\
  0010: 88 87 87 87 7c 87 87 87 7f ff 53 ff ff ff ff ff   ....|.....S.....
  0020: 00 08 30 9b c4 20 00 6d 00 d7 02 00 10 00 08 00   ..0.. .m........
  0030: 6d 00 6d 00 6d 03 6d 00 7f 00 6d 00 6d 03 6d f2   m.m.m.m...m.m.m.


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  77(w)x7 78(x)x2 74(t)x1             80(.)x4 81(.)x3 7f(.)x2 68(h)x1     DIFFER
   0x0001  66(f)x10                            65(e)x10                            DIFFER
   0x0002  65(e)x9 e5(.)x1                     ef(.)x4 24($)x2 2e(.)x2 40(@)x2     DIFFER
   0x0003  5c(\)x7 10(.)x2 0a(.)x1             00(.)x10                            DIFFER
   0x0004  7e(~)x5 00(.)x3 78(x)x2             00(.)x6 13(.)x4                     PARTIAL
   0x0006  10(.)x7 00(.)x2 80(.)x1             29())x6 64(d)x4                     DIFFER
   0x0007  00(.)x7 0f(.)x2 06(.)x1             00(.)x6 29())x4                     PARTIAL
   0x0008  be(.)x8 ff(.)x2                     29())x2 2a(*)x2 fe(.)x2 ff(.)x2 +2u  PARTIAL
   0x0009  ef(.)x8 78(x)x2                     29())x3 c3(.)x2 80(.)x2 4a(J)x1 +2u  DIFFER
   0x000a  00(.)x4 59(Y)x4 30(0)x2             29())x4 00(.)x3 09(.)x2 5c(\)x1     PARTIAL
   0x000b  f4(.)x4 30(0)x2 72(r)x2 00(.)x1 +1u  29())x4 00(.)x3 02(.)x2 5c(\)x1     PARTIAL
   0x000c  00(.)x4 72(r)x2 5c(\)x1 fa(.)x1 +2u  29())x4 00(.)x3 ff(.)x2 5c(\)x1     PARTIAL
   0x000d  00(.)x6 72(r)x2 78(x)x1 06(.)x1     29())x2 66(f)x2 ff(.)x2 31(1)x1 +3u  PARTIAL
   0x000e  00(.)x6 72(r)x2 01(.)x1 3a(:)x1     29())x4 65(e)x2 40(@)x2 5c(\)x1 +1u  PARTIAL
   0x0011  00(.)x6 04(.)x2 17(.)x1 d0(.)x1     87(.)x4 29())x3 40(@)x2 90(.)x1     DIFFER
   0x0012  fc(.)x6 33(3)x1 17(.)x1 fe(.)x1 +1u  87(.)x4 ff(.)x3 30(0)x2 90(.)x1     DIFFER
   0x0013  30(0)x7 62(b)x1 17(.)x1 78(x)x1     28(()x4 87(.)x4 26(&)x2             DIFFER
   0x0014  5c(\)x7 17(.)x1 58(X)x1 29())x1     29())x6 7c(|)x4                     PARTIAL
   0x0015  78(x)x8 17(.)x1 00(.)x1             29())x4 78(x)x2 28(()x2 87(.)x1 +1u  PARTIAL
   0x0016  30(0)x5 47(G)x2 36(6)x2 6d(m)x1     ff(.)x5 87(.)x4 00(.)x1             DIFFER
   0x0017  30(0)x7 3c(<)x2 01(.)x1             ff(.)x5 87(.)x4 0e(.)x1             DIFFER
   0x0018  5c(\)x3 04(.)x2 00(.)x2 5d(])x2 +1u  7f(.)x5 5f(_)x2 fd(.)x2 e6(.)x1     DIFFER
   0x0019  fd(.)x10                            ff(.)x10                            DIFFER
   0x001a  de(.)x10                            53(S)x4 ff(.)x3 c3(.)x2 16(.)x1     DIFFER
   0x001b  ad(.)x10                            ff(.)x8 16(.)x1 00(.)x1             DIFFER
   0x001c  00(.)x10                            40(@)x3 ff(.)x3 78(x)x1 16(.)x1 +2u  PARTIAL
   0x001d  be(.)x10                            ff(.)x3 13(.)x2 00(.)x2 01(.)x2 +1u  DIFFER
   0x001e  ef(.)x10                            ff(.)x3 78(x)x2 30(0)x1 20( )x1 +3u  PARTIAL
   0x001f  00(.)x10                            00(.)x3 ff(.)x3 11(.)x2 5c(\)x1 +1u  PARTIAL
   0x0020  00(.)x10                            00(.)x6 30(0)x2 5c(\)x1 21(!)x1     PARTIAL
   0x0021  00(.)x10                            5c(\)x3 08(.)x3 00(.)x2 29())x1 +1u  PARTIAL
   0x0022  00(.)x10                            30(0)x3 78(x)x2 4b(K)x1 5c(\)x1 +3u  PARTIAL
   0x0023  00(.)x10                            29())x2 9c(.)x2 30(0)x2 5c(\)x1 +3u  PARTIAL
   0x0024  ff(.)x10                            a1(.)x2 16(.)x2 90(.)x1 30(0)x1 +4u  PARTIAL
   0x0025  fe(.)x10                            20( )x3 16(.)x2 5f(_)x1 30(0)x1 +3u  DIFFER
   0x0026  00(.)x10                            00(.)x4 16(.)x2 01(.)x1 5c(\)x1 +2u  PARTIAL
   0x0027  fc(.)x10                            00(.)x4 29())x2 16(.)x2 78(x)x1 +1u  DIFFER
   0x0028  01(.)x5 40(@)x3 43(C)x1 0b(.)x1     00(.)x4 29())x3 16(.)x2 34(4)x1     DIFFER
   0x0029  07(.)x4 29())x3 5c(\)x1             00(.)x6 29())x1 cf(.)x1 32(2)x1 +1u  PARTIAL
   0x002a  00(.)x5 01(.)x2 78(x)x1             00(.)x7 29())x1 40(@)x1 02(.)x1     PARTIAL
   ... (21 more divergent offsets)
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
  prompts/BRBR/14_openthread_8538.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 8538,
  "target": "openthread",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S), value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 8538 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 8538 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 8538 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).