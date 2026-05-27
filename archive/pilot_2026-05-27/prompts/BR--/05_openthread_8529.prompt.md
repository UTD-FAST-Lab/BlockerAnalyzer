==== BLOCKER ====
Target: openthread
Branch ID: 8529
Location: /src/openthread/src/core/thread/mesh_forwarder_ftd.cpp:81:21
Enclosing function: ot::MeshForwarder::SendMessage(ot::Message&)
Source line:                 if (ip6Header.GetDestination() == mle.GetLinkLocalAllThreadNodesAddress() ||
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    0       10          0  REFERENCE
value_profile_cmplog             4        6          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 13  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.05h  loser=12.00h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.80  dur_div=8.95h  hit_div=2
  subject-level: delta_AUC=2409450.0  p_AUC=0.0002  delta_Final=145.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/openthread/8529/{W,L}/branch_coverage_show.txt

--- Enclosing function: ot::MeshForwarder::SendMessage(ot::Message&) (/src/openthread/src/core/thread/mesh_forwarder_ftd.cpp:50-147) ---
[ ]    48  
[ ]    49  Error MeshForwarder::SendMessage(Message &aMessage)
[B]    50  {
[B]    51      Mle::MleRouter &mle   = Get<Mle::MleRouter>();
[B]    52      Error           error = kErrorNone;
[ ]    53  
[B]    54      aMessage.SetOffset(0);
[B]    55      aMessage.SetDatagramTag(0);
[B]    56      aMessage.SetTimestampToNow();
[B]    57      mSendQueue.Enqueue(aMessage);
[ ]    58  
[B]    59      switch (aMessage.GetType())
[B]    60      {
[B]    61      case Message::kTypeIp6:
[B]    62      {
[B]    63          Ip6::Header ip6Header;
[ ]    64  
[B]    65          IgnoreError(aMessage.Read(0, ip6Header));
[ ]    66  
[B]    67          if (ip6Header.GetDestination().IsMulticast())
[B]    68          {
[ ]    69              // For traffic destined to multicast address larger than realm local, generally it uses IP-in-IP
[ ]    70              // encapsulation (RFC2473), with outer destination as ALL_MPL_FORWARDERS. So here if the destination
[ ]    71              // is multicast address larger than realm local, it should be for indirection transmission for the
[ ]    72              // device's sleepy child, thus there should be no direct transmission.
[B]    73              if (!ip6Header.GetDestination().IsMulticastLargerThanRealmLocal())
[B]    74              {
[ ]    75                  // schedule direct transmission
[B]    76                  aMessage.SetDirectTransmission();
[B]    77              }
[ ]    78  
[B]    79              if (aMessage.GetSubType() != Message::kSubTypeMplRetransmission)
[B]    80              {
[B]    81                  if (ip6Header.GetDestination() == mle.GetLinkLocalAllThreadNodesAddress() || <-- BLOCKER
[B]    82                      ip6Header.GetDestination() == mle.GetRealmLocalAllThreadNodesAddress())
[W]    83                  {
[ ]    84                      // destined for all sleepy children
[W]    85                      for (Child &child : Get<ChildTable>().Iterate(Child::kInStateValidOrRestoring))
[ ]    86                      {
[ ]    87                          if (!child.IsRxOnWhenIdle())
[ ]    88                          {
[ ]    89                              mIndirectSender.AddMessageForSleepyChild(aMessage, child);
[ ]    90                          }
[ ]    91                      }
[W]    92                  }
[B]    93                  else
[B]    94                  {
[ ]    95                      // destined for some sleepy children which subscribed the multicast address.
[B]    96                      for (Child &child : Get<ChildTable>().Iterate(Child::kInStateValidOrRestoring))
[ ]    97                      {
[ ]    98                          if (!child.IsRxOnWhenIdle() && child.HasIp6Address(ip6Header.GetDestination()))
[ ]    99                          {
[ ]   100                              mIndirectSender.AddMessageForSleepyChild(aMessage, child);
[ ]   101                          }
[ ]   102                      }
[B]   103                  }
[B]   104              }
[B]   105          }
[L]   106          else // Destination is unicast
[L]   107          {
[L]   108              Neighbor *neighbor = Get<NeighborTable>().FindNeighbor(ip6Header.GetDestination());
[ ]   109  
[L]   110              if ((neighbor != nullptr) && !neighbor->IsRxOnWhenIdle() && !aMessage.IsDirectTransmission() &&
[L]   111                  Get<ChildTable>().Contains(*neighbor))
[ ]   112              {
[ ]   113                  // Destined for a sleepy child
[ ]   114                  mIndirectSender.AddMessageForSleepyChild(aMessage, *static_cast<Child *>(neighbor));
[ ]   115              }
[L]   116              else
[L]   117              {
[L]   118                  aMessage.SetDirectTransmission();
[L]   119              }
[L]   120          }
[ ]   121  
[B]   122          break;
[ ]   123      }
[ ]   124  
[ ]   125  #if OPENTHREAD_CONFIG_CHILD_SUPERVISION_ENABLE
[ ]   126      case Message::kTypeSupervision:
[ ]   127      {
[ ]   128          Child *child = Get<Utils::ChildSupervisor>().GetDestination(aMessage);
[ ]   129          OT_ASSERT((child != nullptr) && !child->IsRxOnWhenIdle());
[ ]   130          mIndirectSender.AddMessageForSleepyChild(aMessage, *child);
[ ]   131          break;
[ ]   132      }
[ ]   133  #endif
[ ]   134  
[ ]   135      default:
[ ]   136          aMessage.SetDirectTransmission();
[ ]   137          break;
[B]   138      }
[ ]   139  
[B]   140  #if (OPENTHREAD_CONFIG_MAX_FRAMES_IN_DIRECT_TX_QUEUE > 0)
[B]   141      ApplyDirectTxQueueLimit(aMessage);
[B]   142  #endif
[ ]   143  
[B]   144      mScheduleTransmissionTask.Post();
[ ]   145  
[B]   146      return error;
[B]   147  }

--- No 1-hop callers of ot::MeshForwarder::SendMessage(ot::Message&) fired in W (callers index present but none matched) ---

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  ot::MeshCoP::Leader::SendKeepAliveResponse(ot::Coap::Message const&, ot::Ip6::MessageInfo const&, ot::MeshCoP::StateTlv::State)  (/src/openthread/src/core/meshcop/meshcop_leader.cpp:194-210, calls ot::MeshForwarder::SendMessage(ot::Message&) at line 203)
hop 2  ot::MeshCoP::Leader::SendPetitionResponse(ot::Coap::Message const&, ot::Ip6::MessageInfo const&, ot::MeshCoP::StateTlv::State)  (/src/openthread/src/core/meshcop/meshcop_leader.cpp:118-144, calls ot::MeshForwarder::SendMessage(ot::Message&) at line 137)
hop 3  void ot::MeshCoP::Leader::HandleTmf<(ot::Uri)22>(ot::Coap::Message&, ot::Ip6::MessageInfo const&)  (/src/openthread/src/core/meshcop/meshcop_leader.cpp:147-189, calls ot::MeshCoP::Leader::SendKeepAliveResponse(ot::Coap::Message const&, ot::Ip6::MessageInfo const&, ot::MeshCoP::StateTlv::State) at line 185)
hop 3  void ot::MeshCoP::Leader::HandleTmf<(ot::Uri)23>(ot::Coap::Message&, ot::Ip6::MessageInfo const&)  (/src/openthread/src/core/meshcop/meshcop_leader.cpp:67-113, calls ot::MeshCoP::Leader::SendPetitionResponse(ot::Coap::Message const&, ot::Ip6::MessageInfo const&, ot::MeshCoP::StateTlv::State) at line 112)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      14        82  ot::MeshForwarder::SendMessage(ot::Message&)  (/src/openthread/src/core/thread/mesh_forwarder_ftd.cpp:50-147)  <-- enclosing
      16        80  ot::MeshCoP::DatasetManager::Restore()  (/src/openthread/src/core/meshcop/dataset_manager.cpp:69-90)
       8        40  ot::MeshCoP::DatasetManager::GetTimestamp() const  (/src/openthread/src/core/meshcop/dataset_manager.cpp:66-66)
       6        30  ot::MeshCoP::BorderAgent::HandleNotifierEvents(ot::Events)  (/src/openthread/src/core/meshcop/border_agent.cpp:233-251)
       6        30  ot::MeshCoP::JoinerRouter::HandleNotifierEvents(ot::Events)  (/src/openthread/src/core/meshcop/joiner_router.cpp:67-72)
       4        20  ot::MeshCoP::DatasetManager::DatasetManager(ot::Instance&, ot::MeshCoP::Dataset::Type, void (&)(ot::Timer&))  (/src/openthread/src/core/meshcop/dataset_manager.cpp:57-64)
       4        20  ot::MeshCoP::DatasetManager::Clear()  (/src/openthread/src/core/meshcop/dataset_manager.cpp:105-111)
       4        20  ot::MeshCoP::DatasetManager::HandleDetach()  (/src/openthread/src/core/meshcop/dataset_manager.cpp:113-113)
       4        20  ot::MeshCoP::DatasetManager::SignalDatasetChange() const  (/src/openthread/src/core/meshcop/dataset_manager.cpp:215-218)
       4        20  ot::MeshCoP::JoinerRouter::Start()  (/src/openthread/src/core/meshcop/joiner_router.cpp:75-100)
       2        10  ot::AnnounceBeginClient::AnnounceBeginClient(ot::Instance&)  (/src/openthread/src/core/meshcop/announce_begin_client.cpp:54-56)
       2        10  ot::MeshCoP::BorderAgent::BorderAgent(ot::Instance&)  (/src/openthread/src/core/meshcop/border_agent.cpp:223-230)
       2        10  ot::MeshCoP::BorderAgent::Start()  (/src/openthread/src/core/meshcop/border_agent.cpp:555-578)
       2        10  ot::MeshCoP::BorderAgent::ApplyMeshLocalPrefix()  (/src/openthread/src/core/meshcop/border_agent.cpp:606-618)
       2        10  ot::MeshCoP::DatasetManager::GetChannelMask(ot::Mac::ChannelMask&) const  (/src/openthread/src/core/meshcop/dataset_manager.cpp:221-239)
... (15 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  ot::MeshForwarder::SendMessage(ot::Message&)  (/src/openthread/src/core/thread/mesh_forwarder_ftd.cpp:50-147) ---
  d=1   L  61  T=14 F=0  T=82 F=0  case Message::kTypeIp6:
  d=1   L  67  T=14 F=0  T=76 F=6  if (ip6Header.GetDestination().IsMulticast())
  d=1   L  73  T=14 F=0  T=76 F=0  if (!ip6Header.GetDestination().IsMulticastLargerThanReal...
  d=1   L  79  T=14 F=0  T=67 F=9  if (aMessage.GetSubType() != Message::kSubTypeMplRetransm...
  d=1   L  81  T=2 F=12  T=0 F=67  if (ip6Header.GetDestination() == mle.GetLinkLocalAllThre...  <-- BLOCKER
  d=1   L  82  T=0 F=12  T=0 F=67  ip6Header.GetDestination() == mle.GetRealmLocalAllThreadN...
  d=1   L  85  T=0 F=2  T=0 F=0  for (Child &child : Get<ChildTable>().Iterate(Child::kInS...
  d=1   L  96  T=0 F=12  T=0 F=67  for (Child &child : Get<ChildTable>().Iterate(Child::kInS...
  d=1   L 110  T=0 F=0  T=0 F=6  if ((neighbor != nullptr) && !neighbor->IsRxOnWhenIdle() ...
  d=1   L 126  T=0 F=14  T=0 F=82  case Message::kTypeSupervision:
  d=1   L 135  T=0 F=14  T=0 F=82  default:

[off-chain: 29 additional divergent branches across 11 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=dfad99a60a0fc48e, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=104s, mutation_op=TokenReplace,BytesInsertCopyMutator,CrossoverReplaceMutator,ByteInterestingMutator):
  0000: 78 66 65 5c 78 00 00 29 ff 78 30 30 5c 78 30 40   xfe\x..).x00\x0@
  0010: 5c 78 33 62 5c 78 47 c4 5c ff 32 00 40 fd de ad   \x3b\xG.\.2.@...
  0020: 00 be ef 00 00 00 00 00 01                        .........
Seed 2 (id=ca90f41f741f4e23, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=419s, mutation_op=BytesSetMutator):
  0000: 78 66 65 5c 78 00 10 3c 5c fe 80 00 00 00 00 00   xfe\x..<\.......
  0010: 00 9c 56 46 bc 24 06 fc 30 ff 32 00 40 fd de ad   ..VF.$..0.2.@...
  0020: 00 be ef 00 00 00 00 00 01 ff 03 bc dc be ef 07   ................
  0030: 03 28 57 61 7f ff eb 18 52                        .(Wa....R

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=003cb3d1dc671c0a, size=46 bytes, fuzzer=cmplog, trial=4, discovered_at=139s, mutation_op=ByteInterestingMutator,TokenReplace,ByteDecMutator):
  0000: 66 65 5c 78 38 00 05 11 ff fd de ad 00 be ef 00   fe\x8...........
  0010: 00 fd ff 06 ff c4 c4 c4 c4 ff a9 0c 30 30 78 e9   ............00x.
  0020: 30 5c 78 30 06 06 06 1d 06 30 5c 78 30 30         0\x0.....0\x00
Seed 2 (id=009333ba20c255f4, size=46 bytes, fuzzer=cmplog, trial=4, discovered_at=187s, mutation_op=TokenReplace):
  0000: 65 65 5c 77 38 00 05 00 00 00 00 00 00 00 00 00   ee\w8...........
  0010: 00 00 00 00 00 00 00 00 00 ff 0c 00 00 00 00 00   ................
  0020: 00 00 00 00 00 00 00 00 00 00 00 00 48 30         ............H0
Seed 3 (id=016264a30146f1e5, size=46 bytes, fuzzer=cmplog, trial=4, discovered_at=221s, mutation_op=TokenReplace,WordInterestingMutator,TokenReplace,WordAddMutator,CrossoverReplaceMutator):
  0000: 66 65 5c 77 38 00 05 29 01 0d 00 ff ff ff ff 06   fe\w8..)........
  0010: 00 00 ff 00 00 00 f8 1a c1 ff 0e 00 00 00 00 00   ................
  0020: 00 00 00 00 00 00 00 4c 4d 00 00 00 48 30         .......LM...H0
Seed 4 (id=00a36d0cbdc5b59f, size=67 bytes, fuzzer=cmplog, trial=4, discovered_at=354s, mutation_op=QwordAddMutator,DwordAddMutator):
  0000: 66 65 5c 77 e6 00 1a 00 00 00 4f 07 00 00 00 00   fe\w......O.....
  0010: 99 99 00 d6 00 00 7f ff ff ff 07 00 00 00 00 00   ................
  0020: 00 00 00 00 00 00 00 ff 00 00 00 61 2f 73 64 00   ...........a/sd.
  0030: ea 00 00 a9 a9 a9 99 99 64 00 00 c5 ff ff 07 00   ........d.......
Seed 5 (id=0046682ff92d57af, size=67 bytes, fuzzer=cmplog, trial=4, discovered_at=538s, mutation_op=CrossoverReplaceMutator,BytesRandSetMutator):
  0000: 66 65 5c 77 42 00 1a 00 7b fc ff 0f ff df 00 00   fe\wB...{.......
  0010: 41 99 99 99 99 81 11 c4 ff ff 03 00 02 00 2d ef   A.............-.
  0020: 69 57 fa de 07 15 00 00 00 00 00 00 00 00 00 6d   iW.............m
  0030: 00 ff 00 00 6d 03 66 ff 53 06 a9 a9 a9 00 bc 9f   ....m.f.S.......


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  78(x)x2                             66(f)x8 65(e)x1 99(.)x1             DIFFER
   0x0001  66(f)x2                             65(e)x10                            DIFFER
   0x0002  65(e)x2                             5c(\)x9 00(.)x1                     DIFFER
   0x0003  5c(\)x2                             77(w)x8 78(x)x1 00(.)x1             DIFFER
   0x0004  78(x)x2                             38(8)x4 42(B)x3 e6(.)x1 00(.)x1 +1u  DIFFER
   0x0006  00(.)x1 10(.)x1                     1a(.)x5 05(.)x4 66(f)x1             DIFFER
   0x0007  29())x1 3c(<)x1                     00(.)x5 11(.)x2 29())x1 2c(,)x1 +1u  PARTIAL
   0x0008  ff(.)x1 5c(\)x1                     00(.)x3 6b(k)x2 ff(.)x1 01(.)x1 +3u  PARTIAL
   0x0009  78(x)x1 fe(.)x1                     00(.)x4 fc(.)x3 fd(.)x1 0d(.)x1 +1u  PARTIAL
   0x000a  30(0)x1 80(.)x1                     00(.)x4 ff(.)x2 de(.)x1 4f(O)x1 +2u  DIFFER
   0x000b  30(0)x1 00(.)x1                     00(.)x3 0f(.)x2 ad(.)x1 ff(.)x1 +3u  PARTIAL
   0x000c  5c(\)x1 00(.)x1                     00(.)x4 ff(.)x3 79(y)x1 99(.)x1 +1u  PARTIAL
   0x000d  78(x)x1 00(.)x1                     00(.)x3 ff(.)x2 be(.)x1 df(.)x1 +3u  PARTIAL
   0x000e  30(0)x1 00(.)x1                     00(.)x4 ef(.)x1 ff(.)x1 0b(.)x1 +3u  PARTIAL
   0x000f  40(@)x1 00(.)x1                     00(.)x5 06(.)x1 13(.)x1 ff(.)x1 +2u  PARTIAL
   0x0010  5c(\)x1 00(.)x1                     00(.)x4 99(.)x3 41(A)x1 ff(.)x1 +1u  PARTIAL
   0x0011  78(x)x1 9c(.)x1                     99(.)x4 00(.)x3 fd(.)x1 04(.)x1 +1u  DIFFER
   0x0012  33(3)x1 56(V)x1                     00(.)x4 99(.)x3 ff(.)x2 bc(.)x1     DIFFER
   0x0013  62(b)x1 46(F)x1                     00(.)x3 99(.)x3 06(.)x1 d6(.)x1 +2u  DIFFER
   0x0014  5c(\)x1 bc(.)x1                     00(.)x4 99(.)x3 ff(.)x2 01(.)x1     DIFFER
   0x0015  78(x)x1 24($)x1                     00(.)x4 99(.)x2 c4(.)x1 81(.)x1 +2u  DIFFER
   0x0016  47(G)x1 06(.)x1                     00(.)x3 c4(.)x1 f8(.)x1 7f(.)x1 +4u  DIFFER
   0x0017  c4(.)x1 fc(.)x1                     c4(.)x3 00(.)x2 1a(.)x1 ff(.)x1 +3u  PARTIAL
   0x0018  5c(\)x1 30(0)x1                     ff(.)x3 00(.)x2 c4(.)x1 c1(.)x1 +3u  DIFFER
   0x0019  ff(.)x2                             ff(.)x7 fd(.)x2 fe(.)x1             PARTIAL
   0x001a  32(2)x2                             a9(.)x2 03(.)x2 de(.)x2 0c(.)x1 +3u  DIFFER
   0x001b  00(.)x2                             00(.)x5 ad(.)x2 0c(.)x1 c2(.)x1 +1u  PARTIAL
   0x001c  40(@)x2                             00(.)x5 30(0)x1 02(.)x1 ff(.)x1 +2u  DIFFER
   0x001d  fd(.)x2                             00(.)x6 be(.)x2 30(0)x1 ff(.)x1     DIFFER
   0x001e  de(.)x2                             00(.)x4 ef(.)x2 78(x)x1 2d(-)x1 +2u  DIFFER
   0x001f  ad(.)x2                             00(.)x7 ef(.)x2 e9(.)x1             DIFFER
   0x0020  00(.)x2                             00(.)x6 69(i)x2 30(0)x1 29())x1     PARTIAL
   0x0021  be(.)x2                             00(.)x6 57(W)x2 5c(\)x1 d0(.)x1     DIFFER
   0x0022  ef(.)x2                             00(.)x5 fa(.)x2 78(x)x1 40(@)x1 +1u  PARTIAL
   0x0023  00(.)x2                             00(.)x5 30(0)x1 de(.)x1 03(.)x1 +2u  PARTIAL
   0x0024  00(.)x2                             00(.)x4 bf(.)x2 ff(.)x2 06(.)x1 +1u  PARTIAL
   0x0025  00(.)x2                             00(.)x4 fe(.)x2 06(.)x1 15(.)x1 +2u  PARTIAL
   0x0026  00(.)x2                             00(.)x8 06(.)x1 7f(.)x1             PARTIAL
   0x0027  00(.)x2                             00(.)x4 1d(.)x1 4c(L)x1 ff(.)x1 +3u  PARTIAL
   0x0028  01(.)x2                             00(.)x4 ff(.)x2 06(.)x1 4d(M)x1 +2u  DIFFER
   ... (16 more divergent offsets)
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
  prompts/BR--/05_openthread_8529.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 8529,
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
      // pick EXACTLY ONE of:
      //   "I2SRandReplace"     (cmplog / vpc input-to-state substitution)
      //   "CMP_MAP gradient"   (vp / vpc Hamming/prefix-distance feedback)
      //   "havoc-only"         (lucky havoc byte mutation, no CMP introspection)
      //   "token-replace"      (TokenInsert/TokenReplace dictionary mutations)
      //   "other"              (anything that does not fit the four above)
    "verified_in_lineage": true,
      // pick true or false
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 8529 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 8529 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 8529 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).