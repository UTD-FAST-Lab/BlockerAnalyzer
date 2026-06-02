==== BLOCKER ====
Target: openthread
Branch ID: 13333
Location: /src/openthread/src/core/net/ip6.cpp:972:5
Enclosing function: ot::Ip6::Ip6::HandlePayload(ot::Ip6::Header&, ot::Message&, ot::Ip6::MessageInfo&, unsigned char, ot::Message::Ownership)
Source line:     case kProtoIcmp6:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    5        5          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     1        9          0  REFERENCE
mopt                             2        8          0  REFERENCE
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
  avg duration blocked: winner=0.20h  loser=21.90h
  avg hitcount on branch: winner=13  loser=2
  prob_div=0.80  dur_div=21.70h  hit_div=11
  subject-level: delta_AUC=11709180.0  p_AUC=0.0002  delta_Final=125.3  p_final=0.0007

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/openthread/13333/{W,L}/branch_coverage_show.txt

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
[ ]   967          {
[ ]   968              LogNote("Error UDP Checksum");
[ ]   969          }
[B]   970          break;
[ ]   971  
[W]   972      case kProtoIcmp6: <-- BLOCKER
[W]   973          error = mIcmp.HandleMessage(*message, aMessageInfo);
[W]   974          break;
[ ]   975  
[ ]   976      default:
[ ]   977          break;
[B]   978      }
[ ]   979  
[B]   980  exit:
[B]   981      if (error != kErrorNone)
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
[L]  1287      {
[L]  1288          error = PassToHost(aMessage, aOrigin, messageInfo, nextHeader, /* aApplyFilter */ false,

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
      11       179  ot::Ip6::Ip6::HandleOptions(ot::Message&, ot::Ip6::Header&, bool, bool&)  (/src/openthread/src/core/net/ip6.cpp:540-597)
       0        28  ot::Ip6::Ip6::ShouldForwardToThread(ot::Ip6::MessageInfo const&, ot::Ip6::Ip6::MessageOrigin) const  (/src/openthread/src/core/net/ip6.cpp:1367-1390)
       0        13  ot::Ip6::Headers::GetDestinationPort() const  (/src/openthread/src/core/net/ip6.cpp:1727-1745)
       0        13  ot::Ip6::Headers::GetChecksum() const  (/src/openthread/src/core/net/ip6.cpp:1748-1770)
       6         0  ot::Ip6::Ip6::HandleFragment(ot::Message&, ot::Ip6::Ip6::MessageOrigin, ot::Ip6::MessageInfo&)  (/src/openthread/src/core/net/ip6.cpp:679-791)
       0         5  ot::Ip6::Ip6::InsertMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:244-322)
       4         0  ot::Ip6::Ip6::HandleTimeTick()  (/src/openthread/src/core/net/ip6.cpp:796-803)
       4         0  ot::Ip6::Ip6::UpdateReassemblyList()  (/src/openthread/src/core/net/ip6.cpp:806-819)
       0         3  ot::Ip6::Ip6::AddMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:191-216)
       0         2  ot::Ip6::Ip6::AddTunneledMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:219-241)
       0         2  ot::Ip6::Ip6::SelectSourceAddress(ot::Ip6::Address const&) const  (/src/openthread/src/core/net/ip6.cpp:1406-1506)
       0         2  ot::Ip6::Ip6::IsOnLink(ot::Ip6::Address const&) const  (/src/openthread/src/core/net/ip6.cpp:1509-1527)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=4  ot::Ip6::Ip6::SendRaw(ot::Message&, bool)  (/src/openthread/src/core/net/ip6.cpp:1132-1160) ---
  d=4   L1140  T=0 F=10  T=5 F=5  if (header.GetDestination().IsMulticast())
--- d=3  ot::Ip6::Ip6::InsertMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:244-322) ---
  d=3   L 250  T=0 F=0  T=3 F=2  if (aHeader.GetDestination().IsRealmLocalMulticast())
  d=3   L 254  T=0 F=0  T=2 F=1  if (aHeader.GetNextHeader() == kProtoHopOpts)
  d=3   L 279  T=0 F=0  T=2 F=0  if (mplOption.GetSize() % 8)
  d=3   L 300  T=0 F=0  T=2 F=0  if (aHeader.GetDestination().IsMulticastLargerThanRealmLo...
  d=3   L 301  T=0 F=0  T=0 F=2  Get<ChildTable>().HasSleepyChildWithAddress(aHeader.GetDe...
--- d=2  ot::Ip6::Ip6::HandleDatagram(ot::Message&, ot::Ip6::Ip6::MessageOrigin, void const*, bool)  (/src/openthread/src/core/net/ip6.cpp:1163-1364) ---
  d=2   L1223  T=43 F=0  T=20 F=28  if (Get<ThreadNetif>().HasUnicastAddress(header.GetDestin...
  d=2   L1227  T=0 F=0  T=2 F=26  else if (!header.GetDestination().IsLinkLocal())
  d=2   L1231  T=0 F=0  T=26 F=0  else if (aOrigin != kFromThreadNetif)
  d=2   L1236  T=0 F=0  T=2 F=26  if (forwardThread && !ShouldForwardToThread(messageInfo, ...
  d=2   L1236  T=0 F=43  T=28 F=20  if (forwardThread && !ShouldForwardToThread(messageInfo, ...
  d=2   L1245  T=4 F=99  T=0 F=139  if (aIsReassembled)
  d=2   L1267  T=26 F=4  T=20 F=0  if (!aIsReassembled)
  d=2   L1286  T=0 F=99  T=2 F=111  if (forwardHost)
  d=2   L1289  T=0 F=0  T=0 F=2  forwardThread ? Message::kCopyToUse : Message::kTakeCusto...
  d=2   L1311  T=0 F=60  T=13 F=78  if (nextHeader == kProtoIcmp6)
  d=2   L1317  T=0 F=0  T=78 F=13  for (IcmpType type : sForwardICMPTypes)
  d=2   L1319  T=0 F=0  T=0 F=78  if (icmpType == type)
--- d=1  ot::Ip6::Ip6::HandlePayload(ot::Ip6::Header&, ot::Message&, ot::Ip6::MessageInfo&, unsigned char, ot::Message::Ownership)  (/src/openthread/src/core/net/ip6.cpp:927-989) ---
  d=1   L 937  T=20 F=10  T=20 F=0  case kProtoUdp:
  d=1   L 938  T=10 F=20  T=0 F=20  case kProtoIcmp6:
  d=1   L 964  T=20 F=10  T=20 F=0  case kProtoUdp:
  d=1   L 972  T=10 F=20  T=0 F=20  case kProtoIcmp6:  <-- BLOCKER
  d=1   L 981  T=10 F=20  T=0 F=20  if (error != kErrorNone)

[off-chain: 64 additional divergent branches across 14 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=4f1af37e9d5867a4, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=387s, mutation_op=ByteRandMutator,BytesCopyMutator,TokenInsert):
  0000: 77 66 20 11 00 00 10 3a 7f 02 b0 07 ff ff ff fc   wf ....:........
  0010: 0a a0 07 0d 2d a3 07 c0 af fd de ad 00 be ef 00   ....-...........
  0020: 00 00 00 00 ff fe 00 fc 00 02 02 00 07 40 7f 20   .............@. 
  0030: 03 10 09 07 07 07 07 07 07                        .........
Seed 2 (id=3280d8d2781fbeb1, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=1245s, mutation_op=CrossoverReplaceMutator,WordInterestingMutator):
  0000: 78 66 10 00 00 00 10 2c 00 00 b0 07 ff ff fe fc   xf.....,........
  0010: 03 a0 07 ff 2d a3 07 b1 af fd de ad 00 be ef 00   ....-...........
  0020: 00 00 00 00 ff fe 00 fc 10 3a 06 04 24 ff 00 64   .........:..$..d
  0030: 78 30 e3 55 ff 06 09 00 2e                        x0.U.....
Seed 3 (id=3c12fb482290a3a5, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=1245s, mutation_op=BytesSetMutator,CrossoverReplaceMutator):
  0000: 78 66 10 00 00 00 10 2c 00 00 b0 07 ff ff fe fc   xf.....,........
  0010: 03 a0 07 ff 2d a3 07 b1 af fd de ad 00 be ef 00   ....-...........
  0020: 00 00 00 00 ff fe 00 fc 10 3a 00 00 00 00 00 00   .........:......
  0030: ff fe 00 ff 00 29 09 00 00                        .....)...
Seed 4 (id=74dbd15e33aabeb0, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=1245s, mutation_op=ByteNegMutator):
  0000: 78 66 10 00 00 00 10 2c 00 00 b0 07 ff ff fe fc   xf.....,........
  0010: 03 a0 07 ff 2d a3 07 b1 af fd de ad 00 be ef 00   ....-...........
  0020: 00 00 00 00 ff fe 00 fc 10 3a 06 01 24 ff 00 64   .........:..$..d
  0030: 78 30 e3 55 ff 06 09 00 2e                        x0.U.....
Seed 5 (id=4b13bfa42a3d3d57, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=1302s, mutation_op=ByteFlipMutator,BytesInsertCopyMutator,ByteNegMutator):
  0000: 78 66 10 00 00 00 10 2c 00 00 b0 07 ff ff fe fc   xf.....,........
  0010: 03 a0 07 ff 2d a3 07 b1 af fd de ad 00 be ef 00   ....-...........
  0020: 00 00 00 00 ff fe 00 fc 10 3a 06 07 24 ff 00 64   .........:..$..d
  0030: 78 30 e3 55 ff 06 09 00 00                        x0.U.....

==== Loser-blocking seeds (take false branch) ====
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
Seed 4 (id=006f860b208405fe, size=296 bytes, fuzzer=naive, trial=1, discovered_at=7404s, mutation_op=DwordInterestingMutator,ByteDecMutator,ByteRandMutator):
  0000: db 62 5c 00 00 00 ff 00 64 78 44 44 44 44 44 44   .b\.....dxDDDDDD
  0010: 44 44 44 44 44 44 30 30 01 fe b4 30 30 30 30 30   DDDDDD00...00000
  0020: 2f 34 34 34 34 34 34 34 00 00 01 6d 05 67 20 9e   /4444444...m.g .
  0030: 30 dd 6d 05 67 78 ff 15 15 15 15 38 5c 78 30 cf   0.m.gx.....8\x0.
Seed 5 (id=005f073b0be48440, size=296 bytes, fuzzer=naive, trial=1, discovered_at=10802s, mutation_op=DwordAddMutator,ByteIncMutator):
  0000: db 62 5c 00 00 00 ff 00 64 78 44 44 44 44 44 44   .b\.....dxDDDDDD
  0010: 44 44 44 44 44 44 30 00 9e fd de ad 00 be ef 00   DDDDDD0.........
  0020: 01 00 79 78 30 08 08 08 08 29 08 08 08 01 00 ff   ..yx0....)......
  0030: 00 64 68 00 dd 6d 05 67 67 67 30 30 10 30 30 30   .dh..m.ggg00.000


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  78(x)x7 77(w)x2 c6(.)x1             db(.)x8 dc(.)x1 96(.)x1             DIFFER
   0x0001  66(f)x8 67(g)x2                     62(b)x10                            DIFFER
   0x0002  10(.)x9 20( )x1                     5c(\)x9 6f(o)x1                     DIFFER
   0x0003  00(.)x8 11(.)x1 02(.)x1             00(.)x9 01(.)x1                     PARTIAL
   0x0006  10(.)x6 78(x)x2 11(.)x1 06(.)x1     ff(.)x9 6f(o)x1                     DIFFER
   0x0007  2c(,)x6 3a(:)x2 00(.)x1 3c(<)x1     00(.)x9 fe(.)x1                     PARTIAL
   0x0008  00(.)x7 7f(.)x2 ff(.)x1             64(d)x9 ff(.)x1                     PARTIAL
   0x0009  00(.)x7 fe(.)x2 02(.)x1             78(x)x8 68(h)x2                     DIFFER
   0x000a  b0(.)x7 fc(.)x1 b4(.)x1 00(.)x1     44(D)x7 00(.)x2 30(0)x1             PARTIAL
   0x000b  07(.)x7 01(.)x1 ff(.)x1 03(.)x1     44(D)x7 dd(.)x2 30(0)x1             DIFFER
   0x000c  ff(.)x7 b3(.)x2 10(.)x1             44(D)x7 6d(m)x2 33(3)x1             DIFFER
   0x000d  ff(.)x8 00(.)x1 0b(.)x1             44(D)x7 00(.)x2 62(b)x1             PARTIAL
   0x000e  fe(.)x6 ff(.)x2 00(.)x1 0b(.)x1     44(D)x7 30(0)x2 5c(\)x1             DIFFER
   0x000f  fc(.)x7 fd(.)x1 0b(.)x1 fe(.)x1     44(D)x7 30(0)x2 00(.)x1             DIFFER
   0x0010  03(.)x6 0a(.)x1 04(.)x1 0b(.)x1 +1u  44(D)x6 33(3)x2 c1(.)x1 53(S)x1     DIFFER
   0x0011  a0(.)x7 00(.)x1 0b(.)x1 ff(.)x1     44(D)x6 00(.)x1 62(b)x1 9d(.)x1 +1u  PARTIAL
   0x0012  07(.)x8 0b(.)x1 ff(.)x1             44(D)x7 5c(\)x2 00(.)x1             DIFFER
   0x0013  ff(.)x7 0d(.)x1 00(.)x1 0b(.)x1     44(D)x7 00(.)x1 ee(.)x1 30(0)x1     PARTIAL
   0x0014  2d(-)x8 0b(.)x1 ff(.)x1             44(D)x5 ff(.)x3 fc(.)x1 30(0)x1     PARTIAL
   0x0015  a3(.)x8 ff(.)x2                     44(D)x5 ff(.)x3 00(.)x1 30(0)x1     PARTIAL
   0x0016  07(.)x8 ff(.)x2                     30(0)x6 ff(.)x4                     PARTIAL
   0x0017  b1(.)x6 9a(.)x2 c0(.)x1 00(.)x1     ff(.)x4 30(0)x4 fe(.)x1 00(.)x1     PARTIAL
   0x0018  af(.)x8 5c(\)x2                     ff(.)x3 01(.)x3 fe(.)x2 9e(.)x1 +1u  DIFFER
   0x0019  fd(.)x10                            ff(.)x5 fe(.)x4 fd(.)x1             PARTIAL
   0x001a  de(.)x10                            b4(.)x4 e3(.)x2 03(.)x1 ff(.)x1 +2u  PARTIAL
   0x001b  ad(.)x10                            ff(.)x3 30(0)x2 25(%)x2 5d(])x1 +2u  PARTIAL
   0x001c  00(.)x10                            00(.)x3 30(0)x2 ef(.)x2 78(x)x1 +2u  PARTIAL
   0x001d  be(.)x10                            30(0)x3 00(.)x2 ff(.)x2 da(.)x1 +2u  PARTIAL
   0x001e  ef(.)x10                            00(.)x4 30(0)x3 da(.)x1 ef(.)x1 +1u  PARTIAL
   0x001f  00(.)x10                            30(0)x4 00(.)x3 b4(.)x2 ff(.)x1     PARTIAL
   0x0020  00(.)x10                            30(0)x2 00(.)x2 ff(.)x2 80(.)x1 +3u  PARTIAL
   0x0021  00(.)x10                            34(4)x6 00(.)x3 30(0)x1             PARTIAL
   0x0022  00(.)x10                            34(4)x5 00(.)x2 30(0)x1 79(y)x1 +1u  PARTIAL
   0x0023  00(.)x10                            34(4)x5 78(x)x2 1c(.)x2 5c(\)x1     DIFFER
   0x0024  ff(.)x10                            34(4)x7 30(0)x2 76(v)x1             DIFFER
   0x0025  fe(.)x10                            34(4)x7 08(.)x2 30(0)x1             DIFFER
   0x0026  00(.)x10                            34(4)x5 08(.)x2 30(0)x1 33(3)x1 +1u  DIFFER
   0x0027  fc(.)x10                            34(4)x7 08(.)x2 5c(\)x1             DIFFER
   0x0028  10(.)x6 00(.)x4                     00(.)x7 08(.)x2 78(x)x1             PARTIAL
   0x0029  3a(:)x8 02(.)x1 24($)x1             00(.)x7 29())x2 30(0)x1             DIFFER
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
  prompts_b/openthread_13333.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 13333,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 13333 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 13333 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 13333 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).