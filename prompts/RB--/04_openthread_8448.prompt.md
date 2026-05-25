==== BLOCKER ====
Target: openthread
Branch ID: 8448
Location: /src/openthread/src/core/common/linked_list.hpp:218:13
Enclosing function: ot::LinkedList<ot::AddressResolver::CacheEntry>::PopAfter(ot::AddressResolver::CacheEntry*)
Source line:         if (aPrevEntry == nullptr)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           2        8          0  loser (I2S vs naive)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             5        5          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 13  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=0.00h  loser=9.60h
  avg hitcount on branch: winner=1303  loser=0
  prob_div=0.80  dur_div=9.60h  hit_div=1303
  subject-level: delta_AUC=2409450.0  p_AUC=0.0002  delta_Final=145.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/openthread/8448/{W,L}/branch_coverage_show.txt

--- Enclosing function: ot::LinkedList<ot::AddressResolver::CacheEntry>::PopAfter(ot::AddressResolver::CacheEntry*) (/src/openthread/src/core/common/linked_list.hpp:215-233) ---
[ ]   213       */
[ ]   214      Type *PopAfter(Type *aPrevEntry)
[B]   215      {
[B]   216          Type *entry;
[ ]   217  
[B]   218          if (aPrevEntry == nullptr) <-- BLOCKER
[B]   219          {
[B]   220              entry = Pop();
[B]   221          }
[B]   222          else
[B]   223          {
[B]   224              entry = aPrevEntry->GetNext();
[ ]   225  
[B]   226              if (entry != nullptr)
[B]   227              {
[B]   228                  aPrevEntry->SetNext(entry->GetNext());
[B]   229              }
[B]   230          }
[ ]   231  
[B]   232          return entry;
[B]   233      }

--- Caller (1 hop): ot::LinkedList<ot::Timer>::Remove(ot::Timer const&) (/src/openthread/src/core/common/linked_list.hpp:309-319, calls ot::LinkedList<ot::AddressResolver::CacheEntry>::PopAfter(ot::AddressResolver::CacheEntry*) at line 315) (full body — short) ---
[B]   309      {
[B]   310          Type *prev;
[B]   311          Error error = Find(aEntry, prev);
[ ]   312  
[B]   313          if (error == kErrorNone)
[B]   314          {
[B]   315              PopAfter(prev); <-- CALL
[B]   316          }
[ ]   317  
[B]   318          return error;
[B]   319      }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  ot::Ip6::Netif::RemoveExternalUnicastAddress(ot::Ip6::Address const&)  (/src/openthread/src/core/net/netif.cpp:504-525, calls ot::LinkedList<ot::AddressResolver::CacheEntry>::PopAfter(ot::AddressResolver::CacheEntry*) at line 514)
hop 2  ot::Ip6::Netif::UnsubscribeExternalMulticast(ot::Ip6::Address const&)  (/src/openthread/src/core/net/netif.cpp:384-406, calls ot::LinkedList<ot::AddressResolver::CacheEntry>::PopAfter(ot::AddressResolver::CacheEntry*) at line 394)
hop 3  otIp6RemoveUnicastAddress  (/src/openthread/src/core/api/ip6_api.cpp:84-86, calls ot::Ip6::Netif::RemoveExternalUnicastAddress(ot::Ip6::Address const&) at line 85)
hop 3  otIp6UnsubscribeMulticastAddress  (/src/openthread/src/core/api/ip6_api.cpp:99-101, calls ot::Ip6::Netif::UnsubscribeExternalMulticast(ot::Ip6::Address const&) at line 100)
hop 3  ot::Ip6::Netif::RemoveAllExternalUnicastAddresses()  (/src/openthread/src/core/net/netif.cpp:528-540, calls ot::Ip6::Netif::RemoveExternalUnicastAddress(ot::Ip6::Address const&) at line 537)
hop 3  ot::Ip6::Netif::UnsubscribeAllExternalMulticastAddresses()  (/src/openthread/src/core/net/netif.cpp:409-421, calls ot::Ip6::Netif::UnsubscribeExternalMulticast(ot::Ip6::Address const&) at line 418)
hop 4  ot::ThreadNetif::Down()  (/src/openthread/src/core/thread/thread_netif.cpp:88-119, calls ot::Ip6::Netif::UnsubscribeAllExternalMulticastAddresses() at line 106)
hop 5  otIp6SetEnabled  (/src/openthread/src/core/api/ip6_api.cpp:48-69, calls ot::ThreadNetif::Down() at line 62)
hop 6  ot::Instance::Finalize()  (/src/openthread/src/core/common/instance.cpp:337-364, calls otIp6SetEnabled at line 344)
hop 6  LLVMFuzzerTestOneInput  (/src/openthread/tests/fuzz/ip6_send.cpp:61-112, calls otIp6SetEnabled at line 75)
hop 7  ot::Mac::RxFrame::ProcessReceiveAesCcm(ot::Mac::ExtAddress const&, ot::Mac::KeyMaterial const&)  (/src/openthread/src/core/mac/mac_frame.cpp:1387-1432, calls ot::Instance::Finalize() at line 1421)
hop 7  ot::Mac::TxFrame::ProcessTransmitAesCcm(ot::Mac::ExtAddress const&)  (/src/openthread/src/core/mac/mac_frame.cpp:1223-1253, calls ot::Instance::Finalize() at line 1246)
hop 8  ot::Mac::Mac::ProcessEnhAckSecurity(ot::Mac::TxFrame&, ot::Mac::RxFrame&)  (/src/openthread/src/core/mac/mac.cpp:1630-1723, calls ot::Mac::RxFrame::ProcessReceiveAesCcm(ot::Mac::ExtAddress const&, ot::Mac::KeyMaterial const&) at line 1708)
hop 8  ot::Mac::Mac::ProcessReceiveSecurity(ot::Mac::RxFrame&, ot::Mac::Address const&, ot::Neighbor*)  (/src/openthread/src/core/mac/mac.cpp:1495-1626, calls ot::Mac::RxFrame::ProcessReceiveAesCcm(ot::Mac::ExtAddress const&, ot::Mac::KeyMaterial const&) at line 1588)
hop 8  ot::Mac::Mac::ProcessTransmitSecurity(ot::Mac::TxFrame&)  (/src/openthread/src/core/mac/mac.cpp:832-917, calls ot::Mac::TxFrame::ProcessTransmitAesCcm(ot::Mac::ExtAddress const&) at line 913)
hop 8  ot::Mac::SubMac::ProcessTransmitSecurity()  (/src/openthread/src/core/mac/sub_mac.cpp:369-407, calls ot::Mac::TxFrame::ProcessTransmitAesCcm(ot::Mac::ExtAddress const&) at line 403)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      15        75  ot::LinkedList<ot::Ip6::Netif::UnicastAddress>::ConstIterator::Advance()  (/src/openthread/src/core/common/linked_list.hpp:662-662)
      15        75  ot::LinkedList<ot::Srp::Server::Host>::ConstIterator::Advance()  (/src/openthread/src/core/common/linked_list.hpp:662-662)
      15        75  ot::LinkedList<ot::Srp::Server::UpdateMetadata>::ConstIterator::Advance()  (/src/openthread/src/core/common/linked_list.hpp:662-662)
      15        75  ot::LinkedList<ot::Srp::Server::Service>::ConstIterator::Advance()  (/src/openthread/src/core/common/linked_list.hpp:662-662)
      15        75  ot::LinkedList<ot::Ip6::Udp::SocketHandle>::ConstIterator::Advance()  (/src/openthread/src/core/common/linked_list.hpp:662-662)
      72        20  ot::Ip6::Netif::MulticastAddress* ot::LinkedList<ot::Ip6::Netif::MulticastAddress>::FindMatching<ot::Ip6::Address>(ot::Ip6::Address const&, ot::Ip6::Netif::MulticastAddress*&)  (/src/openthread/src/core/common/linked_list.hpp:551-553)
      72        20  ot::Ip6::Netif::UnicastAddress* ot::LinkedList<ot::Ip6::Netif::UnicastAddress>::FindMatching<ot::Ip6::Address>(ot::Ip6::Address const&, ot::Ip6::Netif::UnicastAddress*&)  (/src/openthread/src/core/common/linked_list.hpp:551-553)
      72        20  ot::Ip6::Tcp::Endpoint* ot::LinkedList<ot::Ip6::Tcp::Endpoint>::FindMatching<ot::Ip6::MessageInfo>(ot::Ip6::MessageInfo const&, ot::Ip6::Tcp::Endpoint*&)  (/src/openthread/src/core/common/linked_list.hpp:551-553)
      72        20  ot::Ip6::Tcp::Listener* ot::LinkedList<ot::Ip6::Tcp::Listener>::FindMatching<ot::Ip6::MessageInfo>(ot::Ip6::MessageInfo const&, ot::Ip6::Tcp::Listener*&)  (/src/openthread/src/core/common/linked_list.hpp:551-553)
      72        20  ot::Ip6::Udp::SocketHandle* ot::LinkedList<ot::Ip6::Udp::SocketHandle>::FindMatching<ot::Ip6::MessageInfo>(ot::Ip6::MessageInfo const&, ot::Ip6::Udp::SocketHandle*&)  (/src/openthread/src/core/common/linked_list.hpp:551-553)
      72        20  ot::AddressResolver::CacheEntry* ot::LinkedList<ot::AddressResolver::CacheEntry>::FindMatching<ot::Ip6::Address>(ot::Ip6::Address const&, ot::AddressResolver::CacheEntry*&)  (/src/openthread/src/core/common/linked_list.hpp:551-553)
       6        30  ot::LinkedList<ot::Ip6::Netif::UnicastAddress>::ConstIterator::ConstIterator(ot::Ip6::Netif::UnicastAddress const*)  (/src/openthread/src/core/common/linked_list.hpp:658-660)
       6        30  ot::LinkedList<ot::Srp::Server::Host>::ConstIterator::ConstIterator(ot::Srp::Server::Host const*)  (/src/openthread/src/core/common/linked_list.hpp:658-660)
       6        30  ot::LinkedList<ot::Srp::Server::UpdateMetadata>::ConstIterator::ConstIterator(ot::Srp::Server::UpdateMetadata const*)  (/src/openthread/src/core/common/linked_list.hpp:658-660)
       6        30  ot::LinkedList<ot::Srp::Server::Service>::ConstIterator::ConstIterator(ot::Srp::Server::Service const*)  (/src/openthread/src/core/common/linked_list.hpp:658-660)
... (28 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
  (no divergent branches in chain functions; the split is off-chain)

[off-chain: 24 additional divergent branches across 9 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=000af800f60cb499, size=41 bytes, fuzzer=cmplog, trial=3, discovered_at=101s, mutation_op=ByteDecMutator,ByteInterestingMutator):
  0000: 33 62 a3 00 80 00 00 30 ff 5c 78 30 e0 5c 78 30   3b.....0.\x0.\x0
  0010: 30 7f e0 02 a0 9c ff ff 20 fe 80 07 bc f1 7f ff   0....... .......
  0020: 01 f8 5d 3a 8b a7 88 84 31                        ..]:....1
Seed 2 (id=003eceebc7947160, size=41 bytes, fuzzer=cmplog, trial=3, discovered_at=112s, mutation_op=DwordInterestingMutator,DwordAddMutator,ByteAddMutator,ByteIncMutator):
  0000: 33 62 a3 c4 80 00 00 30 30 0a 10 30 00 02 78 30   3b.....00..0..x0
  0010: d3 d3 d3 d3 d3 d3 d3 d3 d3 ff 6a 00 00 00 00 00   ..........j.....
  0020: 00 00 00 00 00 00 00 00 62                        ........b
Seed 3 (id=00799f76cd714a88, size=41 bytes, fuzzer=cmplog, trial=3, discovered_at=161s, mutation_op=BytesCopyMutator,BytesInsertMutator,BytesInsertCopyMutator,BytesSwapMutator,TokenInsert,WordInterestingMutator,ByteInterestingMutator):
  0000: 33 62 5c 00 80 00 00 30 30 5c 61 30 30 5c 78 30   3b\....00\a00\x0
  0010: 30 5c e0 04 af ff ff ff ff fd de ad 00 be ef 00   0\..............
  0020: 00 00 00 00 ff fe 00 fc 1b                        .........
Seed 4 (id=00561157adb0a1c5, size=105 bytes, fuzzer=cmplog, trial=3, discovered_at=326s, mutation_op=ByteDecMutator,WordAddMutator,CrossoverInsertMutator,DwordAddMutator,BitFlipMutator,BytesCopyMutator):
  0000: 33 62 5c a0 80 00 40 29 5c 07 80 10 4d 30 30 5c   3b\...@)\...M00\
  0010: 88 30 30 7c 78 30 30 03 40 ff 78 30 5c 78 30 5c   .00|x00.@.x0\x0\
  0020: 78 30 30 5c 30 b8 29 0e b4 1a 11 00 00 00 00 00   x00\0.).........
  0030: 00 00 00 43 00 66 00 0f 7f 00 00 20 9d 88 cf 41   ...C.f..... ...A
Seed 5 (id=0075cc5eb561edf4, size=92 bytes, fuzzer=cmplog, trial=3, discovered_at=358s, mutation_op=BytesSwapMutator,ByteFlipMutator,BytesRandInsertMutator,BytesRandSetMutator,ByteRandMutator):
  0000: 33 62 5c a0 80 00 33 00 00 fc 00 00 00 cf 30 5c   3b\...3.......0\
  0010: 30 5c 88 30 30 7c 78 30 30 03 00 ff 78 30 5c 78   0\.00|x00...x0\x
  0020: 30 5c 78 30 30 5c 30 ff ff 01 00 00 00 00 00 00   0\x00\0.........
  0030: 00 00 40 00 00 00 00 00 00 00 00 00 00 00 00 00   ..@.............

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=01cb985683850ad0, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=57s, mutation_op=ByteDecMutator):
  0000: 78 66 65 5c 78 00 00 29 00 78 30 30 5c 78 30 ff   xfe\x..).x00\x0.
  0010: 5c 78 33 62 5c 78 47 3c 5c ff 09 3f 40 a0 dc 00   \x3b\xG<\..?@...
  0020: d6 07 ff 41 ff 68 14 fc 07                        ...A.h...
Seed 2 (id=0178793ca3f2c3a9, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=567s, mutation_op=BytesExpandMutator,BytesDeleteMutator,ByteFlipMutator,DwordInterestingMutator,BytesRandInsertMutator,BytesRandInsertMutator):
  0000: 77 66 65 10 00 00 10 00 be ef 80 ee ff ff 01 dd   wfe.............
  0010: fe 04 fc 30 5c 78 36 30 5d fd de ad 00 be ef 00   ...0\x60].......
  0020: ff ff ff 3a 87 31 d0 5c 78 29 01 6d 01 5c 6d 08   ...:.1.\x).m.\m.
  0030: 5c 78 33 62 5c 78 34 30 71                        \x3b\x40q
Seed 3 (id=00e9dded02369404, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=741s, mutation_op=TokenReplace,WordInterestingMutator,BytesExpandMutator,BytesRandInsertMutator,BytesSetMutator,DwordInterestingMutator):
  0000: 77 66 65 10 00 00 10 00 be 01 00 00 00 00 00 00   wfe.............
  0010: fe 04 fc 30 5c 78 36 30 5d fd de ad 10 be ef fb   ...0\x60].......
  0020: 15 ff 06 3a 87 31 d0 5c 78 29 01 6d 01 5c 6d 01   ...:.1.\x).m.\m.
  0030: 5c 6d 05 74 74 74 74 74 74                        \m.tttttt
Seed 4 (id=025154e64b4f795e, size=406 bytes, fuzzer=cmplog, trial=1, discovered_at=776s, mutation_op=CrossoverInsertMutator):
  0000: 60 60 00 fe bf 00 00 00 01 00 00 00 00 00 00 00   ``..............
  0010: 00 00 78 34 30 5c 78 66 65 5c 78 38 30 00 00 00   ..x40\xfe\x80...
  0020: 10 5c 78 30 30 5c 78 30 30 a4 78 30 30 5c 78 30   .\x00\x00.x00\x0
  0030: 30 5c 78 30 46 5c 78 30 30 5c 78 30 30 5c 78 30   0\x0F\x00\x00\x0
Seed 5 (id=01171ffb01c6abea, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=789s, mutation_op=ByteIncMutator):
  0000: 60 60 00 00 00 00 00 11 ff 00 00 00 00 00 00 00   ``..............
  0010: 00 00 00 00 00 00 00 00 00 ff bf ff ff 3f 19 c0   .............?..
  0020: 0c 0f 4b a0 09 3f 14 fc f8                        ..K..?...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  33(3)x6 32(2)x4                     78(x)x4 77(w)x4 60(`)x2             DIFFER
   0x0001  62(b)x10                            66(f)x8 60(`)x2                     DIFFER
   0x0002  5c(\)x8 a3(.)x2                     65(e)x8 00(.)x2                     DIFFER
   0x0003  a0(.)x7 00(.)x2 c4(.)x1             5c(\)x4 10(.)x3 fe(.)x1 00(.)x1 +1u  PARTIAL
   0x0004  80(.)x10                            00(.)x5 78(x)x3 bf(.)x1 77(w)x1     DIFFER
   0x0006  00(.)x3 33(3)x2 64(d)x2 40(@)x1 +2u  10(.)x6 00(.)x3 28(()x1             PARTIAL
   0x0007  00(.)x6 30(0)x3 29())x1             00(.)x5 11(.)x3 29())x2             PARTIAL
   0x000e  30(0)x6 78(x)x3 ff(.)x1             00(.)x4 ef(.)x2 30(0)x1 01(.)x1 +2u  PARTIAL
   0x0019  ff(.)x5 fe(.)x2 fd(.)x2 03(.)x1     fd(.)x5 ff(.)x3 5c(\)x1 03(.)x1     PARTIAL
   0x001f  ff(.)x4 00(.)x4 5c(\)x1 78(x)x1     00(.)x6 fb(.)x1 c0(.)x1 01(.)x1 +1u  PARTIAL
   0x0029  29())x3 1a(.)x1 01(.)x1 00(.)x1 +1u  29())x4 ff(.)x2 a4(.)x1 64(d)x1     PARTIAL
   0x002a  00(.)x4 11(.)x1 04(.)x1 0b(.)x1     01(.)x4 00(.)x3 78(x)x1             PARTIAL
   0x002b  6d(m)x5 00(.)x2                     6d(m)x4 f0(.)x2 30(0)x1 00(.)x1     PARTIAL
   0x002c  00(.)x6 07(.)x1                     01(.)x4 bf(.)x2 30(0)x1 00(.)x1     PARTIAL
   0x002d  6d(m)x4 00(.)x2 7f(.)x1             5c(\)x5 be(.)x2 29())x1             DIFFER
   0x002e  02(.)x3 00(.)x2 05(.)x1 54(T)x1     6d(m)x4 ef(.)x2 78(x)x1 00(.)x1     PARTIAL
   0x002f  00(.)x2 78(x)x2 64(d)x2 30(0)x1     01(.)x3 07(.)x2 08(.)x1 30(0)x1 +1u  PARTIAL
   0x0030  00(.)x2 09(.)x2 ff(.)x1 50(P)x1 +1u  5c(\)x4 ef(.)x2 30(0)x1 ff(.)x1     PARTIAL
   0x0031  00(.)x2 2a(*)x2 48(H)x1 7f(.)x1 +1u  6d(m)x3 00(.)x3 78(x)x1 5c(\)x1     PARTIAL
   0x0034  00(.)x4 ff(.)x2 6d(m)x1             01(.)x2 5c(\)x1 74(t)x1 46(F)x1 +3u  PARTIAL
   0x0036  00(.)x4 6d(m)x1 20( )x1 05(.)x1     34(4)x1 74(t)x1 78(x)x1 a4(.)x1 +4u  PARTIAL
   0x0039  00(.)x3 fd(.)x2 29())x1 07(.)x1     5c(\)x1 00(.)x1                     PARTIAL
   0x003a  00(.)x3 de(.)x2 78(x)x1 80(.)x1     78(x)x1 00(.)x1                     PARTIAL
   0x003b  00(.)x3 ad(.)x2 20( )x1 33(3)x1     30(0)x1 00(.)x1                     PARTIAL
   0x003c  00(.)x3 9d(.)x1 62(b)x1 a9(.)x1 +1u  30(0)x1 00(.)x1                     PARTIAL
   0x003d  00(.)x3 be(.)x2 88(.)x1 a3(.)x1     5c(\)x1 00(.)x1                     PARTIAL
   0x003e  00(.)x2 ef(.)x2 cf(.)x1 0a(.)x1 +1u  78(x)x1 00(.)x1                     PARTIAL
   0x003f  00(.)x3 41(A)x1 01(.)x1 ff(.)x1 +1u  30(0)x1 00(.)x1                     PARTIAL
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
  prompts/RB--/04_openthread_8448.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 8448,
  "target": "openthread",
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 8448 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 8448 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 8448 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).