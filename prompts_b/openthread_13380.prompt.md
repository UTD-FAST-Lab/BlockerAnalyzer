==== BLOCKER ====
Target: openthread
Branch ID: 13380
Location: /src/openthread/src/core/thread/mesh_forwarder_ftd.cpp:82:21
Enclosing function: ot::MeshForwarder::SendMessage(ot::Message&)
Source line:                     ip6Header.GetDestination() == mle.GetRealmLocalAllThreadNodesAddress())
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             9        1          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=1.00h  loser=24.00h
  avg hitcount on branch: winner=6  loser=0
  prob_div=1.00  dur_div=23.00h  hit_div=6
  subject-level: delta_AUC=11709180.0  p_AUC=0.0002  delta_Final=125.3  p_final=0.0007
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 24  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=6.90h  loser=24.00h
  avg hitcount on branch: winner=6  loser=0
  prob_div=0.90  dur_div=17.10h  hit_div=6
  subject-level: delta_AUC=8206200.0  p_AUC=0.0006  delta_Final=65.8  p_final=0.0884

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/openthread/13380/{W,L}/branch_coverage_show.txt

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
[B]    81                  if (ip6Header.GetDestination() == mle.GetLinkLocalAllThreadNodesAddress() ||
[B]    82                      ip6Header.GetDestination() == mle.GetRealmLocalAllThreadNodesAddress()) <-- BLOCKER
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
       0        18  ot::MeshForwarder::UpdateIp6RouteFtd(ot::Ip6::Header&, ot::Message&)  (/src/openthread/src/core/thread/mesh_forwarder_ftd.cpp:504-594)
       0         1  ot::MeshForwarder::HandleResolved(ot::Ip6::Address const&, otError)  (/src/openthread/src/core/thread/mesh_forwarder_ftd.cpp:150-203)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  ot::MeshForwarder::SendMessage(ot::Message&)  (/src/openthread/src/core/thread/mesh_forwarder_ftd.cpp:50-147) ---
  d=1   L  67  T=192 F=0  T=162 F=30  if (ip6Header.GetDestination().IsMulticast())
  d=1   L  82  T=19 F=114  T=0 F=129  ip6Header.GetDestination() == mle.GetRealmLocalAllThreadN...  <-- BLOCKER
  d=1   L  85  T=0 F=19  T=0 F=0  for (Child &child : Get<ChildTable>().Iterate(Child::kInS...
  d=1   L 110  T=0 F=0  T=0 F=30  if ((neighbor != nullptr) && !neighbor->IsRxOnWhenIdle() ...

[off-chain: 10 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=28b9b7bce2f851cb, size=133 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=37s, mutation_op=ByteFlipMutator,BytesRandSetMutator,BytesDeleteMutator,ByteFlipMutator):
  0000: 34 65 00 00 00 00 5c 78 ff 5b 26 85 30 30 5c 78   4e....\x.[&.00\x
  0010: 30 62 5c 78 ca 30 5c 78 66 ff 33 00 40 fd de ad   0b\x.0\xf.3.@...
  0020: 00 be ef 00 00 00 00 00 01 30 5c 30 5c 78 30 30   .........0\0\x00
  0030: 5c 78 30 30 5c 78 30 78 78 bd bd bd bd bd 31 5c   \x00\x0xx.....1\
Seed 2 (id=8b0111a41b7191d5, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=63s, mutation_op=BitFlipMutator):
  0000: 78 66 10 00 00 00 00 09 0a 7d 00 c5 ff ff 04 00   xf.......}......
  0010: 00 00 00 00 00 a3 78 00 00 ff 33 00 40 fd de ad   ......x...3.@...
  0020: 00 be ef 00 00 00 00 00 01                        .........
Seed 3 (id=911216effe059c36, size=133 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=76s, mutation_op=BytesInsertCopyMutator,BytesDeleteMutator,TokenInsert,DwordInterestingMutator,TokenInsert,WordAddMutator,ByteInterestingMutator):
  0000: 34 65 30 00 00 00 5c 29 40 30 5c 40 30 30 5c 79   4e0...\)@0\@00\y
  0010: 30 9d 5c 78 ca 30 5c 78 66 ff 33 00 40 fd de ad   0.\x.0\xf.3.@...
  0020: 00 be ef 00 00 00 00 00 01 b4 00 00 00 01 5c 00   ..............\.
  0030: 40 30 55 30 5c 78 30 78 78 bd bd bd bd bd 31 5c   @0U0\x0xx.....1\
Seed 4 (id=2cd86711c9395aea, size=133 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=227s, mutation_op=ByteDecMutator):
  0000: 34 65 5a 2a 00 00 5c 29 40 30 5c 78 30 30 5c 79   4eZ*..\)@0\x00\y
  0010: 30 9d 5c 78 ca 30 5c 78 30 ff 33 00 40 fd de ad   0.\x.0\x0.3.@...
  0020: 00 be ef 00 00 00 00 00 01 07 70 00 00 00 5c 29   ..........p...\)
  0030: 40 30 fd a0 be 56 be 98 34 00 03 00 00 00 5c 29   @0...V..4.....\)
Seed 5 (id=0cdd1302c0011792, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=1732s, mutation_op=ByteInterestingMutator,BytesDeleteMutator,TokenReplace,BytesSetMutator):
  0000: 78 66 10 7f 01 00 10 00 7f fd de ad 00 be ef 00   xf..............
  0010: 00 00 00 00 ff fe 29 6c 00 ff 33 00 40 fd de ad   ......)l..3.@...
  0020: 00 be ef 00 00 00 00 00 01 29 00 6d 02 59 7f 6d   .........).m.Y.m
  0030: 00 07 02 00 fe 00 78 30 30                        ......x00

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00ada06cb8766ab8, size=160 bytes, fuzzer=value_profile, trial=1, discovered_at=0s, mutation_op=ByteAddMutator):
  0000: 5c 78 36 30 5c 78 30 30 5c 78 30 30 5c 78 30 30   \x60\x00\x00\x00
  0010: 5c 78 30 30 5c 78 30 30 5c 78 33 62 5c 78 34 30   \x00\x00\x3b\x40
  0020: 5c 78 66 65 5c 78 38 30 5c 78 30 30 5c 78 30 30   \xfe\x80\x00\x00
  0030: 5c 78 30 30 5c 78 30 30 5c 78 30 30 5c 78 30 30   \x00\x00\x00\x00
Seed 2 (id=00123255f0c0a666, size=296 bytes, fuzzer=naive, trial=1, discovered_at=58s, mutation_op=BytesSetMutator,ByteInterestingMutator):
  0000: dc 62 5c 00 00 00 ff fe ff 78 30 30 33 62 5c 00   .b\......x003b\.
  0010: c1 00 00 00 fc 00 ff fe ff ff 03 5d 78 30 30 ff   ...........]x00.
  0020: 80 30 30 5c 76 30 30 5c 78 30 40 5c 78 30 30 5c   .00\v00\x0@\x00\
  0030: 78 30 30 5c 78 30 31 5c 78 9a 65 5c 78 38 30 5c   x00\x01\x.e\x80\
Seed 3 (id=003f512ca5e5af05, size=296 bytes, fuzzer=naive, trial=1, discovered_at=575s, mutation_op=TokenReplace,ByteDecMutator):
  0000: db 62 5c 00 00 00 ff 00 64 68 00 dd 6d 00 30 30   .b\.....dh..m.00
  0010: 33 62 5c ee ff ff ff ff ff ff ff da da da da 30   3b\............0
  0020: 30 34 34 34 34 34 33 34 00 00 01 20 00 00 00 01   04444434... ....
  0030: 08 df ff ff ff ff ff ff ff 19 19 19 19 19 30 30   ..............00
Seed 4 (id=0054cafd1d2ce9d3, size=296 bytes, fuzzer=naive, trial=1, discovered_at=927s, mutation_op=WordInterestingMutator,ByteFlipMutator,ByteAddMutator,ByteFlipMutator):
  0000: db 62 6f 01 00 00 ff 00 64 68 00 dd 6d 00 30 30   .bo.....dh..m.00
  0010: 33 9d 5c 30 30 30 30 ff ff ff fe 30 30 30 30 30   3.\0000....00000
  0020: 30 34 34 34 34 34 21 34 00 00 01 08 00 00 00 01   044444!4........
  0030: 08 08 3b df ff 87 ff 15 15 00 00 00 00 00 00 00   ..;.............
Seed 5 (id=00b2f880b76b28a5, size=57 bytes, fuzzer=value_profile, trial=1, discovered_at=1069s, mutation_op=DwordAddMutator,ByteRandMutator,BytesSetMutator,WordInterestingMutator):
  0000: 78 60 00 00 00 00 10 3a ff cc 02 ff 5d 35 5c 5d   x`.....:....]5\]
  0010: 5d 5d 7f 01 ff ff e8 81 ff ff e3 1b ff 5d 5d 5d   ]]...........]]]
  0020: 5d 5d 5d 5d 5d ff e1 01 21 03 02 cc 02 c9 5d 5d   ]]]]]...!.....]]
  0030: 72 e8 03 5d 5d 65 00 5d 4f                        r..]]e.]O


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  34(4)x10 78(x)x5 77(w)x4            db(.)x8 78(x)x7 5c(\)x1 dc(.)x1 +3u  PARTIAL
   0x0001  65(e)x10 66(f)x8 67(g)x1            62(b)x10 66(f)x7 78(x)x1 60(`)x1 +1u  PARTIAL
   0x0004  01(.)x12 00(.)x7                    00(.)x12 ff(.)x4 f7(.)x2 5c(\)x1 +1u  PARTIAL
   0x0005  00(.)x19                            00(.)x19 78(x)x1                    PARTIAL
   0x0007  00(.)x13 78(x)x2 29())x2 09(.)x1 +1u  00(.)x17 30(0)x1 fe(.)x1 3a(:)x1    PARTIAL
   0x000a  fc(.)x5 5c(\)x3 de(.)x3 26(&)x2 +4u  00(.)x10 44(D)x7 30(0)x2 02(.)x1    PARTIAL
   0x000c  30(0)x10 00(.)x5 ff(.)x3 01(.)x1    44(D)x7 ff(.)x6 6d(m)x2 5c(\)x1 +4u  PARTIAL
   0x000e  00(.)x7 5c(\)x5 ef(.)x3 ff(.)x3 +1u  00(.)x8 44(D)x7 30(0)x3 5c(\)x2     PARTIAL
   0x0010  00(.)x7 30(0)x5 ff(.)x5 03(.)x2     44(D)x6 33(3)x2 7f(.)x2 45(E)x2 +7u  DIFFER
   0x0012  00(.)x6 30(0)x6 5c(\)x4 07(.)x3     44(D)x7 30(0)x3 00(.)x3 5c(\)x2 +5u  PARTIAL
   0x0019  ff(.)x19                            ff(.)x11 fe(.)x4 fd(.)x2 00(.)x2 +1u  PARTIAL
   0x001a  33(3)x19                            e3(.)x6 b4(.)x4 03(.)x3 de(.)x2 +4u  PARTIAL
   0x001b  00(.)x19                            64(d)x3 ff(.)x3 30(0)x2 00(.)x2 +7u  PARTIAL
   0x001c  40(@)x19                            00(.)x5 78(x)x4 30(0)x2 c4(.)x2 +6u  DIFFER
   0x001d  fd(.)x19                            30(0)x8 be(.)x2 00(.)x2 c4(.)x2 +5u  DIFFER
   0x001e  de(.)x19                            5c(\)x5 00(.)x4 30(0)x3 ef(.)x2 +5u  DIFFER
   0x001f  ad(.)x19                            30(0)x5 78(x)x5 00(.)x4 c4(.)x2 +3u  DIFFER
   0x0020  00(.)x19                            00(.)x6 30(0)x3 ff(.)x3 c4(.)x2 +6u  PARTIAL
   0x0021  be(.)x19                            00(.)x7 34(4)x6 c4(.)x3 78(x)x1 +3u  DIFFER
   0x0022  ef(.)x19                            34(4)x5 c4(.)x4 00(.)x3 ff(.)x3 +5u  DIFFER
   0x0023  00(.)x19                            34(4)x5 1a(.)x3 ff(.)x2 78(x)x2 +6u  PARTIAL
   0x0024  00(.)x19                            34(4)x7 00(.)x4 80(.)x3 30(0)x2 +4u  PARTIAL
   0x0025  00(.)x19                            34(4)x7 00(.)x4 0f(.)x3 08(.)x2 +4u  PARTIAL
   0x0026  00(.)x19                            34(4)x5 38(8)x4 7f(.)x2 08(.)x2 +6u  DIFFER
   0x0027  00(.)x19                            34(4)x7 00(.)x7 08(.)x2 30(0)x1 +3u  PARTIAL
   0x0028  01(.)x19                            00(.)x12 08(.)x2 5c(\)x1 78(x)x1 +4u  PARTIAL
   0x0029  29())x13 30(0)x3 b4(.)x1 07(.)x1    00(.)x11 29())x5 78(x)x1 30(0)x1 +2u  PARTIAL
   0x002b  6d(m)x13 30(0)x2 00(.)x2 78(x)x1    6d(m)x9 00(.)x5 08(.)x2 30(0)x1 +3u  PARTIAL
   0x002c  00(.)x11 02(.)x4 5c(\)x2 30(0)x1    00(.)x10 05(.)x5 5c(\)x1 78(x)x1 +3u  PARTIAL
   0x002e  20( )x6 5c(\)x3 7f(.)x3 00(.)x3 +3u  00(.)x12 20( )x5 30(0)x2 5d(])x1    PARTIAL
   0x0039  bd(.)x8 30(0)x2 00(.)x1             00(.)x6 6d(m)x4 78(x)x1 9a(.)x1 +7u  PARTIAL
   0x003b  bd(.)x8 00(.)x1 30(0)x1 62(b)x1     6d(m)x8 00(.)x3 30(0)x2 5c(\)x1 +5u  PARTIAL
   0x003c  a0(.)x5 bd(.)x3 5c(\)x2 00(.)x1     00(.)x6 05(.)x4 5c(\)x2 78(x)x1 +6u  PARTIAL
   0x003d  d9(.)x5 bd(.)x3 78(x)x2 00(.)x1     6d(m)x4 67(g)x4 00(.)x3 78(x)x2 +5u  PARTIAL
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
  prompts_b/openthread_13380.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 13380,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 13380 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 13380 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 13380 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).