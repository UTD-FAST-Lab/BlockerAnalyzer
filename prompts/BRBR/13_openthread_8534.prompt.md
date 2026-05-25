==== BLOCKER ====
Target: openthread
Branch ID: 8534
Location: /src/openthread/src/core/thread/mle.cpp:3835:44
Enclosing function: ot::Mle::Mle::IsRoutingLocator(ot::Ip6::Address const&) const
Source line:     return IsMeshLocalAddress(aAddress) && aAddress.GetIid().IsRoutingLocator();
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
  avg duration blocked: winner=0.15h  loser=12.00h
  avg hitcount on branch: winner=134  loser=0
  prob_div=1.00  dur_div=11.85h  hit_div=134
  subject-level: delta_AUC=2557680.0  p_AUC=0.0002  delta_Final=165.0  p_final=0.0002
--- Pair 2: cmplog > naive  [delta: I2S] ---
  subject 13  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=0.20h  loser=11.75h
  avg hitcount on branch: winner=167  loser=0
  prob_div=0.90  dur_div=11.55h  hit_div=167
  subject-level: delta_AUC=2409450.0  p_AUC=0.0002  delta_Final=145.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/openthread/8534/{W,L}/branch_coverage_show.txt

--- Enclosing function: ot::Mle::Mle::IsRoutingLocator(ot::Ip6::Address const&) const (/src/openthread/src/core/thread/mle.cpp:3834-3836) ---
[ ]  3832  
[ ]  3833  bool Mle::IsRoutingLocator(const Ip6::Address &aAddress) const
[B]  3834  {
[B]  3835      return IsMeshLocalAddress(aAddress) && aAddress.GetIid().IsRoutingLocator(); <-- BLOCKER
[B]  3836  }

--- Caller (1 hop): ot::NeighborTable::FindNeighbor(ot::Ip6::Address const&, ot::Neighbor::StateFilter) (/src/openthread/src/core/thread/neighbor_table.cpp:138-168, calls ot::Mle::Mle::IsRoutingLocator(ot::Ip6::Address const&) const at line 147) (full body — short) ---
[B]   138  {
[B]   139      Neighbor    *neighbor = nullptr;
[B]   140      Mac::Address macAddress;
[ ]   141  
[B]   142      if (aIp6Address.IsLinkLocal())
[ ]   143      {
[ ]   144          aIp6Address.GetIid().ConvertToMacAddress(macAddress);
[ ]   145      }
[ ]   146  
[B]   147      if (Get<Mle::Mle>().IsRoutingLocator(aIp6Address)) <-- CALL
[W]   148      {
[W]   149          macAddress.SetShort(aIp6Address.GetIid().GetLocator());
[W]   150      }
[ ]   151  
[B]   152      if (!macAddress.IsNone())
[W]   153      {
[W]   154          neighbor = FindNeighbor(Neighbor::AddressMatcher(macAddress, aFilter));
[W]   155          ExitNow();
[W]   156      }
[ ]   157  
[B]   158      for (Child &child : Get<ChildTable>().Iterate(aFilter))
[ ]   159      {
[ ]   160          if (child.HasIp6Address(aIp6Address))
[ ]   161          {
[ ]   162              ExitNow(neighbor = &child);
[ ]   163          }
[ ]   164      }
[ ]   165  
[B]   166  exit:
[B]   167      return neighbor;
[B]   168  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  void ot::MeshCoP::Leader::HandleTmf<(ot::Uri)23>(ot::Coap::Message&, ot::Ip6::MessageInfo const&)  (/src/openthread/src/core/meshcop/meshcop_leader.cpp:67-113, calls ot::Mle::Mle::IsRoutingLocator(ot::Ip6::Address const&) const at line 76)
hop 2  ot::Ip6::Ip6::SelectSourceAddress(ot::Ip6::Address const&) const  (/src/openthread/src/core/net/ip6.cpp:1406-1506, calls ot::Mle::Mle::IsRoutingLocator(ot::Ip6::Address const&) const at line 1408)
hop 3  otIp6SelectSourceAddress  (/src/openthread/src/core/api/ip6_api.cpp:225-227, calls ot::Ip6::Ip6::SelectSourceAddress(ot::Ip6::Address const&) const at line 226)
hop 3  ot::Ip6::Ip6::AddTunneledMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:219-241, calls ot::Ip6::Ip6::SelectSourceAddress(ot::Ip6::Address const&) const at line 231)
hop 4  ot::Ip6::Ip6::InsertMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:244-322, calls ot::Ip6::Ip6::AddTunneledMplOption(ot::Message&, ot::Ip6::Header&) at line 317)
hop 4  ot::Ip6::Ip6::SendDatagram(ot::Message&, ot::Ip6::MessageInfo&, unsigned char)  (/src/openthread/src/core/net/ip6.cpp:447-526, calls ot::Ip6::Ip6::AddTunneledMplOption(ot::Message&, ot::Ip6::Header&) at line 509)
hop 5  void ot::MeshCoP::BorderAgent::HandleTmf<(ot::Uri)31>(ot::Coap::Message&, ot::Ip6::MessageInfo const&)  (/src/openthread/src/core/meshcop/border_agent.cpp:254-291, calls ot::Ip6::Ip6::SendDatagram(ot::Message&, ot::Ip6::MessageInfo&, unsigned char) at line 283)
hop 5  ot::Ip6::Icmp::SendEchoRequest(ot::Message&, ot::Ip6::MessageInfo const&, unsigned short)  (/src/openthread/src/core/net/icmp6.cpp:62-82, calls ot::Ip6::Ip6::SendDatagram(ot::Message&, ot::Ip6::MessageInfo&, unsigned char) at line 76)
hop 5  ot::Ip6::Ip6::SendRaw(ot::Message&, bool)  (/src/openthread/src/core/net/ip6.cpp:1132-1160, calls ot::Ip6::Ip6::InsertMplOption(ot::Message&, ot::Ip6::Header&) at line 1142)
hop 6  otIp6Send  (/src/openthread/src/core/api/ip6_api.cpp:134-137, calls ot::Ip6::Ip6::SendRaw(ot::Message&, bool) at line 135)
hop 6  ot::Utils::PingSender::SendPing()  (/src/openthread/src/core/utils/ping_sender.cpp:128-170, calls ot::Ip6::Icmp::SendEchoRequest(ot::Message&, ot::Ip6::MessageInfo const&, unsigned short) at line 149)
hop 7  ot::Utils::PingSender::HandleTimer()  (/src/openthread/src/core/utils/ping_sender.cpp:173-182, calls ot::Utils::PingSender::SendPing() at line 176)
hop 7  ot::Utils::PingSender::Ping(ot::Utils::PingSender::Config const&)  (/src/openthread/src/core/utils/ping_sender.cpp:101-119, calls ot::Utils::PingSender::SendPing() at line 115)
hop 7  LLVMFuzzerTestOneInput  (/src/openthread/tests/fuzz/ip6_send.cpp:61-112, calls otIp6Send at line 91)
hop 8  ot::MeshCoP::Dtls::HandleTimer(ot::Timer&)  (/src/openthread/src/core/meshcop/dtls.cpp:830-832, calls ot::Utils::PingSender::HandleTimer() at line 831)
hop 8  ot::MeshCoP::JoinerRouter::HandleTimer()  (/src/openthread/src/core/meshcop/joiner_router.cpp:234-234, calls ot::Utils::PingSender::HandleTimer() at line 234)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0        50  ot::Mle::Mle::IsAnycastLocator(ot::Ip6::Address const&) const  (/src/openthread/src/core/thread/mle.cpp:3839-3841)
      21         0  ot::Ip6::Ip6::ShouldForwardToThread(ot::Ip6::MessageInfo const&, ot::Ip6::Ip6::MessageOrigin) const  (/src/openthread/src/core/net/ip6.cpp:1367-1390)
      21         0  ot::Ip6::Ip6::IsOnLink(ot::Ip6::Address const&) const  (/src/openthread/src/core/net/ip6.cpp:1509-1527)
      21         0  ot::MeshForwarder::UpdateIp6RouteFtd(ot::Ip6::Header&, ot::Message&)  (/src/openthread/src/core/thread/mesh_forwarder_ftd.cpp:504-594)
       0        20  ot::Ip6::Headers::GetDestinationPort() const  (/src/openthread/src/core/net/ip6.cpp:1727-1745)
       0        20  ot::Ip6::Headers::GetChecksum() const  (/src/openthread/src/core/net/ip6.cpp:1748-1770)
       0        10  ot::Ip6::Ip6::AddMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:191-216)
       0        10  ot::Ip6::Ip6::AddTunneledMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:219-241)
       0        10  ot::Ip6::Ip6::InsertMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:244-322)
       0        10  ot::Ip6::Ip6::SelectSourceAddress(ot::Ip6::Address const&) const  (/src/openthread/src/core/net/ip6.cpp:1406-1506)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=5  ot::Ip6::Ip6::SendRaw(ot::Message&, bool)  (/src/openthread/src/core/net/ip6.cpp:1132-1160) ---
  d=5   L1140  T=0 F=10  T=10 F=0  if (header.GetDestination().IsMulticast())
--- d=4  ot::Ip6::Ip6::InsertMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:244-322) ---
  d=4   L 250  T=0 F=0  T=0 F=10  if (aHeader.GetDestination().IsRealmLocalMulticast())
  d=4   L 300  T=0 F=0  T=10 F=0  if (aHeader.GetDestination().IsMulticastLargerThanRealmLo...
  d=4   L 301  T=0 F=0  T=0 F=10  Get<ChildTable>().HasSleepyChildWithAddress(aHeader.GetDe...
--- d=2  ot::Ip6::Ip6::SelectSourceAddress(ot::Ip6::Address const&) const  (/src/openthread/src/core/net/ip6.cpp:1406-1506) ---
  d=2   L1412  T=0 F=0  T=50 F=10  for (const Netif::UnicastAddress &addr : Get<ThreadNetif>...
  d=2   L1417  T=0 F=0  T=20 F=30  if (Get<Mle::Mle>().IsAnycastLocator(addr.GetAddress()))
  d=2   L1425  T=0 F=0  T=0 F=30  if (matchLen >= addr.mPrefixLength)
  d=2   L1435  T=0 F=0  T=10 F=20  if (bestAddr == nullptr)
  d=2   L1441  T=0 F=0  T=0 F=20  else if (addr.GetAddress() == aDestination)
  d=2   L1447  T=0 F=0  T=10 F=10  else if (addr.GetScope() < bestAddr->GetScope())
  d=2   L1450  T=0 F=0  T=0 F=10  if (addr.GetScope() >= overrideScope)
  d=2   L1460  T=0 F=0  T=0 F=10  else if (addr.GetScope() > bestAddr->GetScope())
  d=2   L1472  T=0 F=0  T=0 F=10  else if (addr.mPreferred && !bestAddr->mPreferred)
  d=2   L1478  T=0 F=0  T=0 F=10  else if (matchLen > bestMatchLen)
  d=2   L1486  T=0 F=0  T=10 F=0  else if ((matchLen == bestMatchLen) && (destIsRloc == Get...
  d=2   L1486  T=0 F=0  T=10 F=0  else if ((matchLen == bestMatchLen) && (destIsRloc == Get...
  d=2   L1498  T=0 F=0  T=0 F=20  if (bestMatchLen >= bestAddr->mPrefixLength)
  d=2   L1505  T=0 F=0  T=10 F=0  return (bestAddr != nullptr) ? &bestAddr->GetAddress() : ...
--- d=1  ot::Mle::Mle::IsRoutingLocator(ot::Ip6::Address const&) const  (/src/openthread/src/core/thread/mle.cpp:3834-3836) ---
  d=1   L3835  T=42 F=0  T=0 F=10  return IsMeshLocalAddress(aAddress) && aAddress.GetIid()....  <-- BLOCKER

[off-chain: 57 additional divergent branches across 20 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=2d0d9b87803c3479, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=52s, mutation_op=TokenInsert,BytesRandSetMutator,WordAddMutator):
  0000: 78 66 65 5c 78 00 00 80 5c 78 30 30 5c 78 30 30   xfe\x...\x00\x00
  0010: 5c 78 33 62 5c 78 34 30 5c fd de ad 00 be ef 00   \x3b\x40\.......
  0020: 00 00 00 00 ff fe 00 80 00                        .........
Seed 2 (id=437431defc4c318e, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=358s, mutation_op=WordInterestingMutator):
  0000: 77 66 65 5c 7e 00 10 00 be ef 00 80 c3 ff ff ff   wfe\~...........
  0010: fe 00 fc 30 5c 78 30 30 5c fd de ad 00 be ef 00   ...0\x00\.......
  0020: 00 00 00 00 ff fe 00 9c 00 3a 00 6d 03 5c 78 13   .........:.m.\x.
  0030: 00 80 5c 47 3c 66 66 66 66                        ..\G<ffff
Seed 3 (id=c0e04b0c7e03f1fa, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=487s, mutation_op=ByteFlipMutator,ByteIncMutator):
  0000: 77 66 65 5c 81 00 10 00 be ef 00 80 c3 ff ff ff   wfe\............
  0010: fe 00 fc 30 5c 78 30 30 5c fd de ad 00 be ef 00   ...0\x00\.......
  0020: 00 00 00 00 ff fe 00 9c 00 3a 00 6d 03 5c 78 13   .........:.m.\x.
  0030: 00 81 5c 47 3c 66 66 66 66                        ..\G<ffff
Seed 4 (id=2da935a6ae5165e2, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=489s, mutation_op=BytesSwapMutator,ByteDecMutator):
  0000: 77 66 65 5c 7e 00 10 00 be 06 00 80 c3 ff ff ff   wfe\~...........
  0010: fe 00 fc 30 5c 78 30 30 5c fd de ad 00 be ef 00   ...0\x00\.......
  0020: 00 00 00 00 ff fe 00 9c 00 3a 00 6d 03 5c 78 13   .........:.m.\x.
  0030: 00 04 5c 47 3c 66 66 66 66                        ..\G<ffff
Seed 5 (id=86172622ecc367bf, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=686s, mutation_op=ByteDecMutator):
  0000: 77 66 65 5c 7e 00 10 00 be ef 59 f4 00 00 00 1f   wfe\~.....Y.....
  0010: fe 00 fc 30 5c 78 30 30 5c fd de ad 00 be ef 00   ...0\x00\.......
  0020: 00 00 00 00 ff fe 00 6c 00 29 00 6d 02 5c 78 6d   .......l.).m.\xm
  0030: 00 40 ff ff 3c ff 71 65 70                        .@..<.qep

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=086f19fd342c6071, size=82 bytes, fuzzer=naive, trial=1, discovered_at=28s, mutation_op=BytesCopyMutator,ByteFlipMutator,DwordAddMutator,ByteIncMutator,WordAddMutator,ByteInterestingMutator):
  0000: 80 65 10 00 00 00 29 29 29 29 29 29 29 29 29 29   .e....))))))))))
  0010: 29 29 ff 28 29 29 ff ff e6 ff ff ff 78 13 30 00   )).())......x.0.
  0020: 00 29 4b 29 29 29 29 29 29 29 29 29 29 29 28 29   .)K)))))))))))()
  0030: 29 ff ff fd ff ff ff 79 13 30 5c 78 cf 30 5c 78   )......y.0\x.0\x
Seed 2 (id=022dbf2ad819a43f, size=82 bytes, fuzzer=naive, trial=1, discovered_at=36s, mutation_op=ByteFlipMutator,TokenReplace):
  0000: 80 65 ef 00 00 00 29 29 29 29 29 29 29 29 29 29   .e....))))))))))
  0010: 29 29 ff 28 29 29 ff ff e6 ff ff ff 78 13 30 00   )).())......x.0.
  0020: 00 29 4b 29 90 5f 01 00 29 29 29 29 29 29 28 29   .)K)._..))))))()
  0030: 29 ff ff fd ff ff ff 79 13 30 5c 78 cf 30 5c 78   )......y.0\x.0\x
Seed 3 (id=01c40ea81ac69e68, size=82 bytes, fuzzer=naive, trial=1, discovered_at=43s, mutation_op=BitFlipMutator,WordAddMutator):
  0000: a2 65 10 00 00 00 29 29 29 29 29 29 29 29 29 29   .e....))))))))))
  0010: aa 29 30 32 29 29 ff ff ff ff ff 00 00 00 00 00   .)02))..........
  0020: 00 00 00 00 0e 00 00 78 30 5d 00 30 5c 78 30 30   .......x0].0\x00
  0030: 5c 78 30 30 a7 78 30 30 30 30 16 16 16 16 00 5c   \x00.x0000.....\
Seed 4 (id=030074e8185bf59d, size=133 bytes, fuzzer=naive, trial=1, discovered_at=51s, mutation_op=ByteNegMutator,BytesSwapMutator):
  0000: 80 65 10 00 00 00 5c 00 ff 30 5c 78 66 65 5c 78   .e....\..0\xfe\x
  0010: f0 fc ff ff ef 30 31 30 ff ff ff ff 78 30 30 5c   .....010....x00\
  0020: 30 30 5c 77 30 c0 04 00 00 00 00 00 00 25 5c 78   00\w0........%\x
  0030: 30 31 5c 88 ff 00 00 ff 38 30 30 30 30 5c 78 66   01\.....80000\xf
Seed 5 (id=0853ed435965a069, size=82 bytes, fuzzer=naive, trial=1, discovered_at=157s, mutation_op=ByteRandMutator,ByteNegMutator):
  0000: 7f 65 ef 00 00 00 29 29 29 29 29 29 29 29 29 29   .e....))))))))))
  0010: 29 29 ff 28 29 29 00 ff 7f ff ff ff 40 13 20 5c   )).())......@. \
  0020: 5c 5c 5c 5c 30 30 a4 78 34 30 00 a0 00 02 00 00   \\\\00.x40......
  0030: ff 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  77(w)x6 78(x)x2 74(t)x2             7f(.)x4 80(.)x3 a2(.)x1 68(h)x1 +1u  DIFFER
   0x0001  66(f)x10                            65(e)x10                            DIFFER
   0x0002  65(e)x10                            ef(.)x6 10(.)x4                     DIFFER
   0x0003  5c(\)x6 10(.)x4                     00(.)x9 b9(.)x1                     DIFFER
   0x0004  00(.)x4 7e(~)x3 78(x)x1 81(.)x1 +1u  00(.)x10                            PARTIAL
   0x0006  10(.)x7 80(.)x2 00(.)x1             29())x8 5c(\)x1 31(1)x1             DIFFER
   0x0007  00(.)x6 07(.)x2 80(.)x1 11(.)x1     29())x9 00(.)x1                     PARTIAL
   0x0008  be(.)x8 5c(\)x1 b0(.)x1             29())x7 2a(*)x2 ff(.)x1             DIFFER
   0x0009  ef(.)x7 78(x)x1 06(.)x1 fd(.)x1     29())x8 30(0)x1 4a(J)x1             DIFFER
   0x000a  00(.)x5 01(.)x2 30(0)x1 59(Y)x1 +1u  29())x9 5c(\)x1                     DIFFER
   0x000b  80(.)x3 15(.)x2 30(0)x1 f4(.)x1 +3u  29())x9 78(x)x1                     DIFFER
   0x000c  c3(.)x3 00(.)x3 ff(.)x3 5c(\)x1     29())x9 66(f)x1                     DIFFER
   0x000d  ff(.)x4 00(.)x2 06(.)x2 78(x)x1 +1u  29())x6 32(2)x2 65(e)x1 31(1)x1     DIFFER
   0x000e  ff(.)x3 00(.)x3 3a(:)x2 30(0)x1 +1u  29())x8 5c(\)x1 01(.)x1             DIFFER
   0x0010  fe(.)x6 31(1)x2 5c(\)x1 00(.)x1     29())x7 aa(.)x1 f0(.)x1 90(.)x1     DIFFER
   0x0011  00(.)x5 04(.)x2 d0(.)x2 78(x)x1     29())x8 fc(.)x1 90(.)x1             DIFFER
   0x0012  fc(.)x6 5c(\)x2 33(3)x1 00(.)x1     ff(.)x7 30(0)x1 90(.)x1 10(.)x1     DIFFER
   0x0013  30(0)x6 78(x)x2 62(b)x1 00(.)x1     28(()x8 32(2)x1 ff(.)x1             DIFFER
   0x0014  5c(\)x7 29())x2 ff(.)x1             29())x9 ef(.)x1                     PARTIAL
   0x0015  78(x)x7 01(.)x2 fe(.)x1             29())x9 30(0)x1                     DIFFER
   0x0016  30(0)x4 36(6)x2 6d(m)x2 34(4)x1 +1u  ff(.)x6 00(.)x3 31(1)x1             DIFFER
   0x0017  30(0)x7 01(.)x2 fc(.)x1             ff(.)x8 30(0)x1 0e(.)x1             PARTIAL
   0x0018  5c(\)x5 5d(])x2 80(.)x2 10(.)x1     7f(.)x6 e6(.)x2 ff(.)x2             DIFFER
   0x0019  fd(.)x10                            ff(.)x10                            DIFFER
   0x001a  de(.)x10                            ff(.)x8 16(.)x1 5d(])x1             DIFFER
   0x001b  ad(.)x10                            ff(.)x8 00(.)x1 16(.)x1             DIFFER
   0x001c  00(.)x10                            78(x)x3 40(@)x2 00(.)x1 41(A)x1 +3u  PARTIAL
   0x001d  be(.)x10                            13(.)x5 00(.)x3 30(0)x1 65(e)x1     DIFFER
   0x001e  ef(.)x10                            20( )x4 30(0)x3 00(.)x1 10(.)x1 +1u  PARTIAL
   0x001f  00(.)x10                            5c(\)x5 00(.)x4 10(.)x1             PARTIAL
   0x0020  00(.)x10                            00(.)x4 5c(\)x4 30(0)x1 21(!)x1     PARTIAL
   0x0021  00(.)x10                            5c(\)x4 29())x2 00(.)x2 30(0)x1 +1u  PARTIAL
   0x0022  00(.)x10                            5c(\)x5 4b(K)x2 00(.)x1 18(.)x1 +1u  PARTIAL
   0x0023  00(.)x10                            5c(\)x4 29())x3 00(.)x1 77(w)x1 +1u  PARTIAL
   0x0024  ff(.)x10                            30(0)x5 29())x1 90(.)x1 0e(.)x1 +2u  PARTIAL
   0x0025  fe(.)x10                            30(0)x3 29())x2 5f(_)x1 00(.)x1 +3u  DIFFER
   0x0026  00(.)x10                            29())x2 5c(\)x2 01(.)x1 00(.)x1 +4u  PARTIAL
   0x0027  9c(.)x3 30(0)x2 00(.)x2 80(.)x1 +2u  29())x3 00(.)x3 78(x)x3 ef(.)x1     PARTIAL
   0x0028  00(.)x9 01(.)x1                     29())x4 00(.)x3 34(4)x2 30(0)x1     PARTIAL
   0x0029  3a(:)x3 29())x3 5c(\)x2 ff(.)x1     00(.)x3 29())x2 5d(])x1 30(0)x1 +3u  PARTIAL
   ... (18 more divergent offsets)
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
  prompts/BRBR/13_openthread_8534.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 8534,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 8534 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 8534 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 8534 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).