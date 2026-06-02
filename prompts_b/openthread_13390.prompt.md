==== BLOCKER ====
Target: openthread
Branch ID: 13390
Location: /src/openthread/src/core/thread/network_data_leader.cpp:177:9
Enclosing function: ot::NetworkData::LeaderBase::GetContext(unsigned char, ot::Lowpan::Context&) const
Source line:     if (aContextId == Mle::kMeshLocalPrefixContextId)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    5        5          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     2        8          0  REFERENCE
mopt                             3        7          0  REFERENCE
minimizer                        6        4          0  REFERENCE
fast                             7        3          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=0.30h  loser=21.30h
  avg hitcount on branch: winner=127  loser=12
  prob_div=0.80  dur_div=21.00h  hit_div=115
  subject-level: delta_AUC=11709180.0  p_AUC=0.0002  delta_Final=125.3  p_final=0.0007

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/openthread/13390/{W,L}/branch_coverage_show.txt

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
       0        47  ot::NetworkData::LeaderBase::GetContextForMeshLocalPrefix(ot::Lowpan::Context&) const  (/src/openthread/src/core/thread/network_data_leader.cpp:204-209)
      45         0  ot::NetworkData::LeaderBase::IsOnMesh(ot::Ip6::Address const&) const  (/src/openthread/src/core/thread/network_data_leader.cpp:212-238)
       0        44  ot::Lowpan::Lowpan::CompressExtensionHeader(ot::Message&, ot::FrameBuilder&, unsigned char&)  (/src/openthread/src/core/thread/lowpan.cpp:436-520)
       0        31  ot::Lowpan::Lowpan::FindContextForId(unsigned char, ot::Lowpan::Context&) const  (/src/openthread/src/core/thread/lowpan.cpp:58-63)
       0         2  ot::Lowpan::Lowpan::CompressDestinationIid(ot::Mac::Address const&, ot::Ip6::Address const&, ot::Lowpan::Context const&, unsigned short&, ot::FrameBuilder&)  (/src/openthread/src/core/thread/lowpan.cpp:133-155)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  ot::NetworkData::LeaderBase::GetContext(unsigned char, ot::Lowpan::Context&) const  (/src/openthread/src/core/thread/network_data_leader.cpp:172-201) ---
  d=1   L 177  T=0 F=45  T=31 F=0  if (aContextId == Mle::kMeshLocalPrefixContextId)  <-- BLOCKER
  d=1   L 183  T=0 F=45  T=0 F=0  while ((prefixTlv = tlvIterator.Iterate<PrefixTlv>()) != ...

[off-chain: 50 additional divergent branches across 11 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=09d1aa462b9734c9, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=150s, mutation_op=ByteRandMutator,BytesCopyMutator,WordInterestingMutator,BytesDeleteMutator,BytesRandSetMutator):
  0000: 78 66 10 02 00 00 00 01 32 07 00 00 09 0b 80 b1   xf......2.......
  0010: ff ff 07 00 ff a3 00 9c 57 fd de ad 00 be ef 00   ........W.......
  0020: 00 00 00 00 ff fe 00 fc 0d                        .........
Seed 2 (id=59dd6f6c79a8b94e, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=2060s, mutation_op=ByteRandMutator):
  0000: 78 66 10 04 c2 00 10 00 01 00 50 04 ff 78 66 10   xf........P..xf.
  0010: 02 ff 10 00 11 b2 01 81 18 fd de ad 00 be ef 00   ................
  0020: 00 00 00 00 ff fe 00 fc 4b 7f 01 6d 03 40 7f 68   ........K..m.@.h
  0030: 6d 07 40 ff 0a 80 78 30 30                        m.@...x00
Seed 3 (id=4bc44abe688c6b28, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=2721s, mutation_op=BytesSwapMutator,ByteIncMutator,ByteAddMutator,WordInterestingMutator):
  0000: 78 66 10 04 c2 00 10 00 01 00 50 04 ff 78 66 10   xf........P..xf.
  0010: 02 ff 10 00 06 b2 01 81 18 fd de ad 00 be ef 00   ................
  0020: 00 00 00 00 ff fe 00 fc 4b 7f 01 6d 03 40 7f 68   ........K..m.@.h
  0030: 6d 07 40 ff 0a 80 78 30 30                        m.@...x00
Seed 4 (id=450f357a2cfe6806, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=2791s, mutation_op=ByteDecMutator,ByteIncMutator,BytesDeleteMutator,BytesInsertMutator):
  0000: 80 66 ff 0d 01 00 10 00 7f 0a b0 00 ff e3 14 14   .f..............
  0010: 20 00 14 14 14 15 14 14 ec fd de ad 00 be ef 00    ...............
  0020: 00 00 00 00 ff fe 00 fc 48 00 00 6d 02 40 ff 6d   ........H..m.@.m
  0030: 00 7f 00 6d 04 40 78 a1 30                        ...m.@x.0
Seed 5 (id=450f357a2cfe6806-2, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=8211s, mutation_op=BitFlipMutator,BytesDeleteMutator,ByteFlipMutator,WordInterestingMutator,BytesInsertMutator,BytesSetMutator):
  0000: 80 66 ff 0d 01 00 10 00 7f 0a b0 00 ff e3 14 14   .f..............
  0010: 20 00 14 14 14 15 14 14 ec fd de ad 00 be ef 00    ...............
  0020: 00 00 00 00 ff fe 00 fc 48 00 00 6d 02 40 ff 6d   ........H..m.@.m
  0030: 00 7f 00 6d 04 40 78 a1 30                        ...m.@x.0

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=00123255f0c0a666, size=296 bytes, fuzzer=naive, trial=1, discovered_at=58s, mutation_op=BytesSetMutator,ByteInterestingMutator):
  0000: dc 62 5c 00 00 00 ff fe ff 78 30 30 33 62 5c 00   .b\......x003b\.
  0010: c1 00 00 00 fc 00 ff fe ff ff 03 5d 78 30 30 ff   ...........]x00.
  0020: 80 30 30 5c 76 30 30 5c 78 30 40 5c 78 30 30 5c   .00\v00\x0@\x00\
  0030: 78 30 30 5c 78 30 31 5c 78 9a 65 5c 78 38 30 5c   x00\x01\x.e\x80\
Seed 2 (id=003f512ca5e5af05, size=296 bytes, fuzzer=naive, trial=1, discovered_at=575s, mutation_op=TokenReplace,ByteDecMutator):
  0000: db 62 5c 00 00 00 ff 00 64 68 00 dd 6d 00 30 30   .b\.....dh..m.00
  0010: 33 62 5c ee ff ff ff ff ff ff ff da da da da 30   3b\............0
  0020: 30 34 34 34 34 34 33 34 00 00 01 20 00 00 00 01   04444434... ....
  0030: 08 df ff ff ff ff ff ff ff 19 19 19 19 19 30 30   ..............00
Seed 3 (id=0054cafd1d2ce9d3, size=296 bytes, fuzzer=naive, trial=1, discovered_at=927s, mutation_op=WordInterestingMutator,ByteFlipMutator,ByteAddMutator,ByteFlipMutator):
  0000: db 62 6f 01 00 00 ff 00 64 68 00 dd 6d 00 30 30   .bo.....dh..m.00
  0010: 33 9d 5c 30 30 30 30 ff ff ff fe 30 30 30 30 30   3.\0000....00000
  0020: 30 34 34 34 34 34 21 34 00 00 01 08 00 00 00 01   044444!4........
  0030: 08 08 3b df ff 87 ff 15 15 00 00 00 00 00 00 00   ..;.............
Seed 4 (id=016b5060aed712e0, size=41 bytes, fuzzer=naive, trial=1, discovered_at=1027s, mutation_op=DwordInterestingMutator,ByteDecMutator):
  0000: db 62 10 2a 00 00 00 29 40 00 00 00 00 00 00 00   .b.*...)@.......
  0010: 00 00 00 00 00 00 00 00 14 ff dc 5c e2 e3 e3 e3   ...........\....
  0020: e2 7a fc ff ff e7 ff 20 ff                        .z..... .
Seed 5 (id=00a2056a8d3290d7, size=41 bytes, fuzzer=naive, trial=1, discovered_at=1322s, mutation_op=ByteNegMutator,BytesCopyMutator):
  0000: db 60 00 80 00 00 00 11 ff 00 00 00 00 00 00 00   .`..............
  0010: 00 00 00 00 00 ff ff ff 00 ff ff ff ff 00 ff e3   ................
  0020: e3 e3 e3 e3 e3 e3 e2 00 30                        ........0


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  77(w)x5 78(x)x3 80(.)x2             db(.)x8 dc(.)x2                     DIFFER
   0x0001  66(f)x5 67(g)x5                     62(b)x9 60(`)x1                     DIFFER
   0x0002  10(.)x8 ff(.)x2                     5c(\)x6 6f(o)x1 10(.)x1 00(.)x1 +1u  PARTIAL
   0x0003  01(.)x5 04(.)x2 0d(.)x2 02(.)x1     00(.)x7 01(.)x1 2a(*)x1 80(.)x1     PARTIAL
   0x0004  00(.)x3 01(.)x3 c2(.)x2 07(.)x2     00(.)x9 08(.)x1                     PARTIAL
   0x0005  00(.)x10                            00(.)x9 02(.)x1                     PARTIAL
   0x0006  78(x)x5 10(.)x4 00(.)x1             ff(.)x5 00(.)x2 02(.)x1 10(.)x1 +1u  PARTIAL
   0x0007  00(.)x8 01(.)x1 66(f)x1             00(.)x5 29())x2 fe(.)x1 11(.)x1 +1u  PARTIAL
   0x000e  ff(.)x4 14(.)x3 66(f)x2 80(.)x1     00(.)x3 30(0)x2 5c(\)x1 33(3)x1 +3u  DIFFER
   0x0010  ff(.)x4 20( )x3 02(.)x2 0e(.)x1     00(.)x3 33(3)x2 c1(.)x1 7f(.)x1 +3u  DIFFER
   0x0011  00(.)x7 ff(.)x3                     00(.)x5 62(b)x2 9d(.)x1 e4(.)x1 +1u  PARTIAL
   0x0012  14(.)x3 10(.)x2 01(.)x2 07(.)x1 +2u  00(.)x4 5c(\)x4 e4(.)x1 29())x1     DIFFER
   0x0013  ff(.)x4 00(.)x3 14(.)x3             00(.)x6 ee(.)x1 30(0)x1 e4(.)x1 +1u  PARTIAL
   0x0014  ff(.)x5 14(.)x3 11(.)x1 06(.)x1     00(.)x5 ff(.)x2 fc(.)x1 30(0)x1 +1u  PARTIAL
   0x0015  15(.)x3 ff(.)x3 b2(.)x2 a3(.)x1 +1u  00(.)x4 ff(.)x4 30(0)x1 e4(.)x1     PARTIAL
   0x0019  fd(.)x10                            ff(.)x10                            DIFFER
   0x001a  de(.)x10                            ff(.)x4 03(.)x1 fe(.)x1 dc(.)x1 +3u  DIFFER
   0x001b  ad(.)x10                            ff(.)x3 30(0)x2 5d(])x1 da(.)x1 +3u  DIFFER
   0x001c  00(.)x10                            78(x)x2 30(0)x2 ff(.)x2 da(.)x1 +3u  PARTIAL
   0x001d  be(.)x10                            30(0)x3 00(.)x3 da(.)x1 e3(.)x1 +2u  DIFFER
   0x001e  ef(.)x10                            00(.)x4 30(0)x3 da(.)x1 e3(.)x1 +1u  DIFFER
   0x001f  00(.)x10                            30(0)x3 e3(.)x2 ff(.)x1 5b([)x1 +3u  PARTIAL
   0x0020  00(.)x10                            30(0)x3 00(.)x2 80(.)x1 e2(.)x1 +3u  PARTIAL
   0x0021  00(.)x10                            30(0)x2 34(4)x2 00(.)x2 7a(z)x1 +3u  PARTIAL
   0x0022  00(.)x10                            30(0)x2 34(4)x2 fc(.)x1 e3(.)x1 +4u  PARTIAL
   0x0023  00(.)x10                            ff(.)x3 34(4)x2 5c(\)x1 e3(.)x1 +3u  PARTIAL
   0x0024  ff(.)x10                            34(4)x2 00(.)x2 76(v)x1 ff(.)x1 +4u  PARTIAL
   0x0025  fe(.)x10                            30(0)x2 34(4)x2 e7(.)x1 e3(.)x1 +4u  DIFFER
   0x0026  00(.)x10                            30(0)x3 33(3)x1 21(!)x1 ff(.)x1 +4u  PARTIAL
   0x0027  fc(.)x10                            5c(\)x2 34(4)x2 20( )x1 00(.)x1 +4u  DIFFER
   0x0029  00(.)x5 7f(.)x2 30(0)x1 23(#)x1     30(0)x2 00(.)x2 29())x2 3a(:)x1 +1u  PARTIAL
   0x002a  00(.)x3 0b(.)x3 01(.)x2 5c(\)x1     01(.)x2 00(.)x2 40(@)x1 11(.)x1 +2u  PARTIAL
   0x002b  6d(m)x8 78(x)x1                     00(.)x3 5c(\)x1 20( )x1 08(.)x1 +1u  DIFFER
   0x002c  02(.)x3 00(.)x3 03(.)x2 30(0)x1     00(.)x5 78(x)x1 30(0)x1             PARTIAL
   0x002d  40(@)x5 6d(m)x3 30(0)x1             00(.)x3 30(0)x1 6d(m)x1 db(.)x1 +1u  PARTIAL
   0x002e  ff(.)x3 00(.)x3 7f(.)x2 5c(\)x1     00(.)x5 30(0)x1 62(b)x1             PARTIAL
   0x002f  6d(m)x6 68(h)x2 78(x)x1             5c(\)x2 01(.)x2 6d(m)x1 11(.)x1 +1u  PARTIAL
   0x0030  00(.)x3 02(.)x3 6d(m)x2 30(0)x1     00(.)x3 08(.)x2 78(x)x1 90(.)x1     PARTIAL
   0x0031  7f(.)x3 40(@)x3 07(.)x2 fd(.)x1     00(.)x2 30(0)x1 df(.)x1 08(.)x1 +2u  DIFFER
   0x0032  00(.)x5 40(@)x2 a9(.)x1 0b(.)x1     ff(.)x2 30(0)x1 3b(;)x1 08(.)x1 +2u  PARTIAL
   ... (12 more divergent offsets)
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
  prompts_b/openthread_13390.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 13390,
  "target": "openthread",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 13390 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 13390 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 13390 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).