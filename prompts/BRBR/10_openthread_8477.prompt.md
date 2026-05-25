==== BLOCKER ====
Target: openthread
Branch ID: 8477
Location: /src/openthread/src/core/net/ip6.cpp:981:9
Enclosing function: ot::Ip6::Ip6::HandlePayload(ot::Ip6::Header&, ot::Message&, ot::Ip6::MessageInfo&, unsigned char, ot::Message::Ownership)
Source line:     if (error != kErrorNone)
Globally blocked side: T  (true branch)

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
  avg duration blocked: winner=0.20h  loser=12.00h
  avg hitcount on branch: winner=195  loser=0
  prob_div=1.00  dur_div=11.80h  hit_div=195
  subject-level: delta_AUC=2409450.0  p_AUC=0.0002  delta_Final=145.4  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 16  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.20h  loser=12.00h
  avg hitcount on branch: winner=155  loser=0
  prob_div=1.00  dur_div=11.80h  hit_div=155
  subject-level: delta_AUC=2557680.0  p_AUC=0.0002  delta_Final=165.0  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/openthread/8477/{W,L}/branch_coverage_show.txt

--- Enclosing function: ot::Ip6::Ip6::HandlePayload(ot::Ip6::Header&, ot::Message&, ot::Ip6::MessageInfo&, unsigned char, ot::Message::Ownership) (/src/openthread/src/core/net/ip6.cpp:927-989) ---
[ ]   925                           uint8_t            aIpProto,
[ ]   926                           Message::Ownership aMessageOwnership)
[B]   927  {
[ ]   928  #if !OPENTHREAD_CONFIG_TCP_ENABLE
[ ]   929      OT_UNUSED_VARIABLE(aIp6Header);
[ ]   930  #endif
[ ]   931  
[B]   932      Error    error   = kErrorNone;
[B]   933      Message *message = (aMessageOwnership == Message::kTakeCustody) ? &aMessage : nullptr;
[ ]   934  
[B]   935      switch (aIpProto)
[B]   936      {
[B]   937      case kProtoUdp:
[B]   938      case kProtoIcmp6:
[B]   939          break;
[ ]   940  #if OPENTHREAD_CONFIG_TCP_ENABLE
[ ]   941      case kProtoTcp:
[ ]   942          break;
[ ]   943  #endif
[ ]   944      default:
[ ]   945          ExitNow();
[B]   946      }
[ ]   947  
[B]   948      if (aMessageOwnership == Message::kCopyToUse)
[ ]   949      {
[ ]   950          VerifyOrExit((message = aMessage.Clone()) != nullptr, error = kErrorNoBufs);
[ ]   951      }
[ ]   952  
[B]   953      switch (aIpProto)
[B]   954      {
[ ]   955  #if OPENTHREAD_CONFIG_TCP_ENABLE
[ ]   956      case kProtoTcp:
[ ]   957          error = mTcp.HandleMessage(aIp6Header, *message, aMessageInfo);
[ ]   958          if (error == kErrorDrop)
[ ]   959          {
[ ]   960              LogNote("Error TCP Checksum");
[ ]   961          }
[ ]   962          break;
[ ]   963  #endif
[B]   964      case kProtoUdp:
[B]   965          error = mUdp.HandleMessage(*message, aMessageInfo);
[B]   966          if (error == kErrorDrop)
[W]   967          {
[W]   968              LogNote("Error UDP Checksum");
[W]   969          }
[B]   970          break;
[ ]   971  
[W]   972      case kProtoIcmp6:
[W]   973          error = mIcmp.HandleMessage(*message, aMessageInfo);
[W]   974          break;
[ ]   975  
[ ]   976      default:
[ ]   977          break;
[B]   978      }
[ ]   979  
[B]   980  exit:
[B]   981      if (error != kErrorNone) <-- BLOCKER
[W]   982      {
[W]   983          LogNote("Failed to handle payload: %s", ErrorToString(error));
[W]   984      }
[ ]   985  
[B]   986      FreeMessage(message);
[ ]   987  
[B]   988      return error;
[B]   989  }

--- Caller (1 hop): ot::Ip6::Ip6::HandleDatagram(ot::Message&, ot::Ip6::Ip6::MessageOrigin, void const*, bool) (/src/openthread/src/core/net/ip6.cpp:1163-1364, calls ot::Ip6::Ip6::HandlePayload(ot::Ip6::Header&, ot::Message&, ot::Ip6::MessageInfo&, unsigned char, ot::Message::Ownership) at line 1278) (±10 around call site) ---
[B]  1268          {
[B]  1269              error = PassToHost(aMessage, aOrigin, messageInfo, nextHeader,
[B]  1270                                 /* aApplyFilter */ !forwardHost, Message::kCopyToUse);
[ ]  1271  
[B]  1272              if ((error == kErrorNone || error == kErrorNoRoute) && forwardHost)
[ ]  1273              {
[ ]  1274                  forwardHost = false;
[ ]  1275              }
[B]  1276          }
[ ]  1277  
[B]  1278          error = HandlePayload(header, aMessage, messageInfo, nextHeader, <-- CALL
[B]  1279                                (forwardThread || forwardHost ? Message::kCopyToUse : Message::kTakeCustody));
[ ]  1280  
[ ]  1281          // Need to free the message if we did not pass its
[ ]  1282          // ownership in the call to `HandlePayload()`
[B]  1283          shouldFreeMessage = forwardThread || forwardHost;
[B]  1284      }
[ ]  1285  
[B]  1286      if (forwardHost)
[ ]  1287      {
[ ]  1288          error = PassToHost(aMessage, aOrigin, messageInfo, nextHeader, /* aApplyFilter */ false,

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  ot::Ip6::Ip6::HandleDatagram(ot::Message&, ot::Ip6::Ip6::MessageOrigin, void const*, bool)  (/src/openthread/src/core/net/ip6.cpp:1163-1364, calls ot::Ip6::Ip6::HandlePayload(ot::Ip6::Header&, ot::Message&, ot::Ip6::MessageInfo&, unsigned char, ot::Message::Ownership) at line 1278)
hop 3  ot::Ip6::Ip6::HandleSendQueue()  (/src/openthread/src/core/net/ip6.cpp:529-537, calls ot::Ip6::Ip6::HandleDatagram(ot::Message&, ot::Ip6::Ip6::MessageOrigin, void const*, bool) at line 535)
hop 3  ot::Ip6::Ip6::InsertMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:244-322, calls ot::Ip6::Ip6::HandleDatagram(ot::Message&, ot::Ip6::Ip6::MessageOrigin, void const*, bool) at line 307)
hop 4  ot::Ip6::Ip6::SendRaw(ot::Message&, bool)  (/src/openthread/src/core/net/ip6.cpp:1132-1160, calls ot::Ip6::Ip6::InsertMplOption(ot::Message&, ot::Ip6::Header&) at line 1142)
hop 5  otIp6Send  (/src/openthread/src/core/api/ip6_api.cpp:134-137, calls ot::Ip6::Ip6::SendRaw(ot::Message&, bool) at line 135)
hop 6  LLVMFuzzerTestOneInput  (/src/openthread/tests/fuzz/ip6_send.cpp:61-112, calls otIp6Send at line 91)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0        95  ot::Ip6::Ip6::HandleOptions(ot::Message&, ot::Ip6::Header&, bool, bool&)  (/src/openthread/src/core/net/ip6.cpp:540-597)
       0        38  ot::Ip6::Headers::GetDestinationPort() const  (/src/openthread/src/core/net/ip6.cpp:1727-1745)
       0        38  ot::Ip6::Headers::GetChecksum() const  (/src/openthread/src/core/net/ip6.cpp:1748-1770)
       0         9  ot::Ip6::Ip6::InsertMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:244-322)
       0         8  ot::Ip6::Ip6::ShouldForwardToThread(ot::Ip6::MessageInfo const&, ot::Ip6::Ip6::MessageOrigin) const  (/src/openthread/src/core/net/ip6.cpp:1367-1390)
       0         8  ot::Ip6::Ip6::IsOnLink(ot::Ip6::Address const&) const  (/src/openthread/src/core/net/ip6.cpp:1509-1527)
       0         1  ot::Ip6::Ip6::AddMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:191-216)
       0         1  ot::Ip6::Ip6::AddTunneledMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:219-241)
       1         0  ot::Ip6::Ip6::HandleFragment(ot::Message&, ot::Ip6::Ip6::MessageOrigin, ot::Ip6::MessageInfo&)  (/src/openthread/src/core/net/ip6.cpp:679-791)
       1         0  ot::Ip6::Ip6::HandleTimeTick()  (/src/openthread/src/core/net/ip6.cpp:796-803)
       1         0  ot::Ip6::Ip6::UpdateReassemblyList()  (/src/openthread/src/core/net/ip6.cpp:806-819)
       0         1  ot::Ip6::Ip6::SelectSourceAddress(ot::Ip6::Address const&) const  (/src/openthread/src/core/net/ip6.cpp:1406-1506)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=4  ot::Ip6::Ip6::SendRaw(ot::Message&, bool)  (/src/openthread/src/core/net/ip6.cpp:1132-1160) ---
  d=4   L1140  T=0 F=10  T=9 F=1  if (header.GetDestination().IsMulticast())
--- d=3  ot::Ip6::Ip6::InsertMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:244-322) ---
  d=3   L 250  T=0 F=0  T=8 F=1  if (aHeader.GetDestination().IsRealmLocalMulticast())
  d=3   L 254  T=0 F=0  T=8 F=0  if (aHeader.GetNextHeader() == kProtoHopOpts)
  d=3   L 279  T=0 F=0  T=8 F=0  if (mplOption.GetSize() % 8)
  d=3   L 300  T=0 F=0  T=1 F=0  if (aHeader.GetDestination().IsMulticastLargerThanRealmLo...
  d=3   L 301  T=0 F=0  T=0 F=1  Get<ChildTable>().HasSleepyChildWithAddress(aHeader.GetDe...
--- d=2  ot::Ip6::Ip6::HandleDatagram(ot::Message&, ot::Ip6::Ip6::MessageOrigin, void const*, bool)  (/src/openthread/src/core/net/ip6.cpp:1163-1364) ---
  d=2   L1223  T=31 F=0  T=20 F=8  if (Get<ThreadNetif>().HasUnicastAddress(header.GetDestin...
  d=2   L1227  T=0 F=0  T=8 F=0  else if (!header.GetDestination().IsLinkLocal())
  d=2   L1236  T=0 F=0  T=8 F=0  if (forwardThread && !ShouldForwardToThread(messageInfo, ...
  d=2   L1236  T=0 F=31  T=8 F=20  if (forwardThread && !ShouldForwardToThread(messageInfo, ...
  d=2   L1245  T=1 F=90  T=0 F=136  if (aIsReassembled)
  d=2   L1267  T=29 F=1  T=20 F=0  if (!aIsReassembled)
  d=2   L1311  T=0 F=60  T=18 F=85  if (nextHeader == kProtoIcmp6)
  d=2   L1317  T=0 F=0  T=54 F=0  for (IcmpType type : sForwardICMPTypes)
  d=2   L1319  T=0 F=0  T=18 F=36  if (icmpType == type)
--- d=1  ot::Ip6::Ip6::HandlePayload(ot::Ip6::Header&, ot::Message&, ot::Ip6::MessageInfo&, unsigned char, ot::Message::Ownership)  (/src/openthread/src/core/net/ip6.cpp:927-989) ---
  d=1   L 937  T=29 F=1  T=20 F=0  case kProtoUdp:
  d=1   L 938  T=1 F=29  T=0 F=20  case kProtoIcmp6:
  d=1   L 964  T=29 F=1  T=20 F=0  case kProtoUdp:
  d=1   L 966  T=9 F=20  T=0 F=20  if (error == kErrorDrop)
  d=1   L 972  T=1 F=29  T=0 F=20  case kProtoIcmp6:
  d=1   L 981  T=10 F=20  T=0 F=20  if (error != kErrorNone)  <-- BLOCKER

[off-chain: 62 additional divergent branches across 13 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=0396cf0f608eb8a1, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=744s, mutation_op=BytesDeleteMutator):
  0000: 78 66 65 5c 78 00 10 11 b0 78 01 00 98 7b 30 30   xfe\x....x...{00
  0010: 5c 78 33 62 5c 78 34 30 5c fd de ad 00 be ef 00   \x3b\x40\.......
  0020: 00 00 00 00 ff fe 00 fc 00 00 00 c0 03 be ef 07   ................
  0030: 05 28 57 61 7a 75 eb 18 52                        .(Wazu..R
Seed 2 (id=041877c27f8d3782, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=1194s, mutation_op=BytesDeleteMutator,ByteRandMutator,ByteNegMutator):
  0000: 78 66 65 5c 77 00 10 11 b0 78 da 30 00 00 00 ff   xfe\w....x.0....
  0010: 18 52 33 62 5c 79 34 30 5c fd de ad 00 be ef 00   .R3b\y40\.......
  0020: 00 00 00 00 ff fe 00 fc 00 ff 00 f0 bf be ef 07   ................
  0030: ef 00 7e 09 0a ad 01 18 52                        ..~.....R
Seed 3 (id=106933b64a26f850, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=2523s, mutation_op=ByteFlipMutator):
  0000: 78 66 65 5c 77 00 10 11 00 00 00 00 00 00 00 00   xfe\w...........
  0010: 00 00 00 00 00 00 00 30 5c fd de ad 00 be ef 00   .......0\.......
  0020: 00 00 00 00 ff fe 00 fc 00 ff 00 c0 03 be ef 07   ................
  0030: ef 07 7e 41 56 53 50 18 52                        ..~AVSP.R
Seed 4 (id=0631586c2d8731ee, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=2815s, mutation_op=ByteInterestingMutator,ByteInterestingMutator,BytesInsertCopyMutator):
  0000: 78 66 65 5c 77 00 10 11 b0 fd de ad 00 be ef 00   xfe\w...........
  0010: 00 00 00 01 00 fe 00 fc 10 fd de ad 00 be ef 00   ................
  0020: 00 00 00 00 ff fe 00 fc 00 ff 00 f0 bf be ef 07   ................
  0030: ef 03 01 01 01 01 01 de 00                        .........
Seed 5 (id=0b368eeba9a8f7f9, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=2815s, mutation_op=ByteInterestingMutator,ByteInterestingMutator,BytesInsertCopyMutator):
  0000: 78 66 65 5c 77 00 10 11 b0 fd de ad 00 be ef 00   xfe\w...........
  0010: 00 00 06 01 00 fe a0 fc 10 fd de ad 00 be ef 00   ................
  0020: 00 00 00 00 ff fe 00 fc 00 ff 00 f0 bf be ef 07   ................
  0030: ef 01 01 01 01 01 01 de 00                        .........

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
   0x0000  78(x)x10                            80(.)x5 81(.)x4 7f(.)x1             DIFFER
   0x0001  66(f)x9 67(g)x1                     65(e)x9 6e(n)x1                     DIFFER
   0x0002  65(e)x10                            24($)x2 23(#)x2 40(@)x2 ef(.)x1 +3u  DIFFER
   0x0003  5c(\)x9 01(.)x1                     00(.)x10                            DIFFER
   0x0004  77(w)x6 78(x)x4                     13(.)x6 00(.)x4                     DIFFER
   0x0006  10(.)x10                            64(d)x6 29())x4                     DIFFER
   0x0007  11(.)x9 2c(,)x1                     00(.)x9 29())x1                     DIFFER
   0x0008  b0(.)x9 00(.)x1                     01(.)x4 ff(.)x2 29())x1 5c(\)x1 +2u  DIFFER
   0x0009  fd(.)x5 78(x)x4 00(.)x1             f0(.)x2 80(.)x2 29())x1 10(.)x1 +4u  PARTIAL
   0x000a  de(.)x5 01(.)x2 da(.)x2 00(.)x1     00(.)x3 04(.)x2 29())x1 5c(\)x1 +3u  PARTIAL
   0x000b  ad(.)x5 00(.)x2 30(0)x2 a0(.)x1     00(.)x5 02(.)x2 29())x1 5c(\)x1 +1u  PARTIAL
   0x000c  00(.)x7 98(.)x2 5c(\)x1             00(.)x5 ff(.)x2 29())x1 5c(\)x1 +1u  PARTIAL
   0x000d  be(.)x5 7b({)x2 00(.)x2 78(x)x1     66(f)x4 ff(.)x2 29())x1 5c(\)x1 +2u  PARTIAL
   0x000e  ef(.)x5 30(0)x3 00(.)x2             65(e)x4 40(@)x2 29())x1 5c(\)x1 +2u  PARTIAL
   0x000f  00(.)x6 30(0)x3 ff(.)x1             5c(\)x5 40(@)x2 29())x1 00(.)x1 +1u  PARTIAL
   0x0010  00(.)x6 5c(\)x3 18(.)x1             88(.)x3 41(A)x2 29())x1 81(.)x1 +3u  PARTIAL
   0x0011  00(.)x6 78(x)x3 52(R)x1             87(.)x3 7e(~)x2 40(@)x2 29())x1 +2u  PARTIAL
   0x0012  33(3)x4 00(.)x4 06(.)x1 40(@)x1     87(.)x6 30(0)x2 ff(.)x1 00(.)x1     PARTIAL
   0x0013  01(.)x5 62(b)x4 00(.)x1             87(.)x6 26(&)x2 28(()x1 00(.)x1     PARTIAL
   0x0014  00(.)x6 5c(\)x4                     7c(|)x5 29())x3 87(.)x1 bf(.)x1     DIFFER
   0x0015  fe(.)x5 78(x)x3 79(y)x1 00(.)x1     87(.)x4 29())x2 28(()x2 78(x)x1 +1u  PARTIAL
   0x0016  00(.)x5 34(4)x4 a0(.)x1             87(.)x6 00(.)x2 ff(.)x2             PARTIAL
   0x0017  30(0)x5 fc(.)x4 cf(.)x1             87(.)x6 ff(.)x3 13(.)x1             DIFFER
   0x0018  5c(\)x5 10(.)x5                     7f(.)x6 fd(.)x2 5f(_)x1 80(.)x1     DIFFER
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
   0x0027  fc(.)x10                            00(.)x5 16(.)x2 78(x)x1 6d(m)x1 +1u  DIFFER
   0x0028  00(.)x10                            00(.)x6 16(.)x2 34(4)x1 01(.)x1     PARTIAL
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
  prompts/BRBR/10_openthread_8477.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 8477,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 8477 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 8477 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 8477 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).