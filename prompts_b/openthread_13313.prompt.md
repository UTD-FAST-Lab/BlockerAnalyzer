==== BLOCKER ====
Target: openthread
Branch ID: 13313
Location: /src/openthread/src/core/net/checksum.cpp:154:12
Enclosing function: ot::Checksum::VerifyMessageChecksum(ot::Message const&, ot::Ip6::MessageInfo const&, unsigned char)
Source line:     return (checksum.GetValue() == kValidRxChecksum) ? kErrorNone : kErrorDrop;
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
  avg duration blocked: winner=0.60h  loser=21.50h
  avg hitcount on branch: winner=923  loser=3
  prob_div=0.80  dur_div=20.90h  hit_div=920
  subject-level: delta_AUC=11709180.0  p_AUC=0.0002  delta_Final=125.3  p_final=0.0007

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/openthread/13313/{W,L}/branch_coverage_show.txt

--- Enclosing function: ot::Checksum::VerifyMessageChecksum(ot::Message const&, ot::Ip6::MessageInfo const&, unsigned char) (/src/openthread/src/core/net/checksum.cpp:149-155) ---
[ ]   147  
[ ]   148  Error Checksum::VerifyMessageChecksum(const Message &aMessage, const Ip6::MessageInfo &aMessageInfo, uint8_t aIpProto)
[B]   149  {
[B]   150      Checksum checksum;
[ ]   151  
[B]   152      checksum.Calculate(aMessageInfo.GetPeerAddr(), aMessageInfo.GetSockAddr(), aIpProto, aMessage);
[ ]   153  
[B]   154      return (checksum.GetValue() == kValidRxChecksum) ? kErrorNone : kErrorDrop; <-- BLOCKER
[B]   155  }

--- Caller (1 hop): ot::Ip6::Udp::HandleMessage(ot::Message&, ot::Ip6::MessageInfo&) (/src/openthread/src/core/net/udp6.cpp:454-481, calls ot::Checksum::VerifyMessageChecksum(ot::Message const&, ot::Ip6::MessageInfo const&, unsigned char) at line 461) (full body — short) ---
[B]   454  {
[B]   455      Error  error = kErrorNone;
[B]   456      Header udpHeader;
[ ]   457  
[B]   458      SuccessOrExit(error = aMessage.Read(aMessage.GetOffset(), udpHeader));
[ ]   459  
[B]   460  #ifndef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION
[B]   461      SuccessOrExit(error = Checksum::VerifyMessageChecksum(aMessage, aMessageInfo, kProtoUdp)); <-- CALL
[B]   462  #endif
[ ]   463  
[B]   464      aMessage.MoveOffset(sizeof(udpHeader));
[B]   465      aMessageInfo.mPeerPort = udpHeader.GetSourcePort();
[B]   466      aMessageInfo.mSockPort = udpHeader.GetDestinationPort();
[ ]   467  
[ ]   468  #if OPENTHREAD_CONFIG_PLATFORM_UDP_ENABLE
[ ]   469      VerifyOrExit(!ShouldUsePlatformUdp(aMessageInfo.mSockPort) || IsPortInUse(aMessageInfo.mSockPort));
[ ]   470  #endif
[ ]   471  
[B]   472      for (Receiver &receiver : mReceivers)
[ ]   473      {
[ ]   474          VerifyOrExit(!receiver.HandleMessage(aMessage, aMessageInfo));
[ ]   475      }
[ ]   476  
[B]   477      HandlePayload(aMessage, aMessageInfo);
[ ]   478  
[B]   479  exit:
[B]   480      return error;
[B]   481  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  ot::Ip6::Icmp::HandleMessage(ot::Message&, ot::Ip6::MessageInfo&)  (/src/openthread/src/core/net/icmp6.cpp:132-154, calls ot::Checksum::VerifyMessageChecksum(ot::Message const&, ot::Ip6::MessageInfo const&, unsigned char) at line 138)
hop 2  ot::Ip6::Tcp::HandleMessage(ot::Ip6::Header&, ot::Message&, ot::Ip6::MessageInfo&)  (/src/openthread/src/core/net/tcp6.cpp:596-668, calls ot::Checksum::VerifyMessageChecksum(ot::Message const&, ot::Ip6::MessageInfo const&, unsigned char) at line 624)
hop 3  ot::Ip6::Ip6::HandlePayload(ot::Ip6::Header&, ot::Message&, ot::Ip6::MessageInfo&, unsigned char, ot::Message::Ownership)  (/src/openthread/src/core/net/ip6.cpp:927-989, calls ot::Ip6::Icmp::HandleMessage(ot::Message&, ot::Ip6::MessageInfo&) at line 957)
hop 4  ot::Ip6::Ip6::HandleDatagram(ot::Message&, ot::Ip6::Ip6::MessageOrigin, void const*, bool)  (/src/openthread/src/core/net/ip6.cpp:1163-1364, calls ot::Ip6::Ip6::HandlePayload(ot::Ip6::Header&, ot::Message&, ot::Ip6::MessageInfo&, unsigned char, ot::Message::Ownership) at line 1278)
hop 5  ot::Ip6::Ip6::HandleSendQueue()  (/src/openthread/src/core/net/ip6.cpp:529-537, calls ot::Ip6::Ip6::HandleDatagram(ot::Message&, ot::Ip6::Ip6::MessageOrigin, void const*, bool) at line 535)
hop 5  ot::Ip6::Ip6::InsertMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:244-322, calls ot::Ip6::Ip6::HandleDatagram(ot::Message&, ot::Ip6::Ip6::MessageOrigin, void const*, bool) at line 307)
hop 6  ot::Ip6::Ip6::SendRaw(ot::Message&, bool)  (/src/openthread/src/core/net/ip6.cpp:1132-1160, calls ot::Ip6::Ip6::InsertMplOption(ot::Message&, ot::Ip6::Header&) at line 1142)
hop 7  otIp6Send  (/src/openthread/src/core/api/ip6_api.cpp:134-137, calls ot::Ip6::Ip6::SendRaw(ot::Message&, bool) at line 135)
hop 8  LLVMFuzzerTestOneInput  (/src/openthread/tests/fuzz/ip6_send.cpp:61-112, calls otIp6Send at line 91)

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  ot::Checksum::VerifyMessageChecksum(ot::Message const&, ot::Ip6::MessageInfo const&, unsigned char)  (/src/openthread/src/core/net/checksum.cpp:149-155) ---
  d=1   L 154  T=20 F=10  T=20 F=0  return (checksum.GetValue() == kValidRxChecksum) ? kError...  <-- BLOCKER

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=09b78be3f8e2fbed, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=1864s, mutation_op=ByteRandMutator,WordInterestingMutator,TokenReplace,BytesInsertCopyMutator,BytesInsertMutator,BytesSwapMutator,ByteNegMutator):
  0000: 78 66 10 01 00 00 10 11 7f 00 fc c4 ff ff ff fc   xf..............
  0010: 03 00 07 00 2d a3 07 00 af fd de ad 00 be ef 00   ....-...........
  0020: 00 00 00 00 ff fe 00 fc 00 07 00 f0 bf 40 7f 20   .............@. 
  0030: 00 10 02 00 ff ff 80 00 80                        .........
Seed 2 (id=09f659000b425f03, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=1868s, mutation_op=DwordInterestingMutator,DwordInterestingMutator,ByteRandMutator):
  0000: 78 66 10 00 00 00 10 11 7f 00 fc 01 10 00 00 fd   xf..............
  0010: 04 00 07 00 2d a3 07 00 af fd de ad 00 be ef 00   ....-...........
  0020: 00 00 00 00 ff fe 00 fc 00 07 ff f0 bf 40 7f 00   .............@..
  0030: 00 01 00 00 00 00 00 00 d3                        .........
Seed 3 (id=05bc112c4b8cf7c9, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=2349s, mutation_op=WordAddMutator,BytesRandSetMutator,ByteIncMutator):
  0000: 78 66 10 00 00 00 10 11 7f 00 fc 00 10 00 00 fd   xf..............
  0010: 04 00 07 00 2d a3 fb fb af fd de ad 00 be ef 00   ....-...........
  0020: 00 00 00 00 ff fe 00 fc 00 07 00 f0 bf 40 7f 20   .............@. 
  0030: fa 10 00 de ad 00 be ef 00                        .........
Seed 4 (id=09a48bb9b3051b83, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=2352s, mutation_op=BitFlipMutator,ByteDecMutator,WordInterestingMutator,BitFlipMutator,CrossoverReplaceMutator,ByteNegMutator):
  0000: 78 66 10 00 00 00 10 11 7f 00 fc 03 10 00 00 fd   xf..............
  0010: 01 ff 5a 00 e0 93 04 10 af fd de ad 00 be ef 00   ..Z.............
  0020: 00 00 00 00 ff fe 00 fc 00 07 66 f0 bf 40 81 20   ..........f..@. 
  0030: 00 01 00 6d 6d ff 11 7f 6e                        ...mm...n
Seed 5 (id=02f8ecda52807040, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=2501s, mutation_op=DwordAddMutator,BytesSwapMutator,BytesRandSetMutator,BytesDeleteMutator,CrossoverReplaceMutator):
  0000: 78 66 10 00 00 00 10 11 7f fd de ad 00 be ef 00   xf..............
  0010: 00 00 00 00 ff fe 00 07 af fd de ad 00 be ef 00   ................
  0020: 00 00 00 00 ff fe 00 fc 00 07 00 f0 bf 40 7f 20   .............@. 
  0030: 00 02 10 00 38 80 78 30 30                        ....8.x00

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
   0x0000  78(x)x10                            db(.)x8 dc(.)x1 96(.)x1             DIFFER
   0x0001  66(f)x10                            62(b)x10                            DIFFER
   0x0002  10(.)x10                            5c(\)x9 6f(o)x1                     DIFFER
   0x0004  00(.)x9 f9(.)x1                     00(.)x10                            PARTIAL
   0x0006  10(.)x6 18(.)x3 1d(.)x1             ff(.)x9 6f(o)x1                     DIFFER
   0x0007  11(.)x10                            00(.)x9 fe(.)x1                     DIFFER
   0x0008  7f(.)x10                            64(d)x9 ff(.)x1                     DIFFER
   0x0009  00(.)x7 fd(.)x1 e9(.)x1 01(.)x1     78(x)x8 68(h)x2                     DIFFER
   0x000a  fc(.)x7 de(.)x1 e9(.)x1 00(.)x1     44(D)x7 00(.)x2 30(0)x1             PARTIAL
   0x000b  01(.)x2 0a(.)x2 c4(.)x1 00(.)x1 +4u  44(D)x7 dd(.)x2 30(0)x1             DIFFER
   0x000c  10(.)x8 ff(.)x1 00(.)x1             44(D)x7 6d(m)x2 33(3)x1             DIFFER
   0x000d  00(.)x5 ff(.)x4 be(.)x1             44(D)x7 00(.)x2 62(b)x1             PARTIAL
   0x000e  00(.)x5 ff(.)x4 ef(.)x1             44(D)x7 30(0)x2 5c(\)x1             DIFFER
   0x000f  fd(.)x7 fc(.)x1 00(.)x1 ff(.)x1     44(D)x7 30(0)x2 00(.)x1             PARTIAL
   0x0010  04(.)x5 00(.)x2 03(.)x1 01(.)x1 +1u  44(D)x6 33(3)x2 c1(.)x1 53(S)x1     DIFFER
   0x0011  00(.)x7 01(.)x2 ff(.)x1             44(D)x6 00(.)x1 62(b)x1 9d(.)x1 +1u  PARTIAL
   0x0012  07(.)x8 5a(Z)x1 00(.)x1             44(D)x7 5c(\)x2 00(.)x1             PARTIAL
   0x0013  00(.)x7 01(.)x3                     44(D)x7 00(.)x1 ee(.)x1 30(0)x1     PARTIAL
   0x0014  2d(-)x4 d3(.)x4 e0(.)x1 ff(.)x1     44(D)x5 ff(.)x3 fc(.)x1 30(0)x1     PARTIAL
   0x0015  a3(.)x8 93(.)x1 fe(.)x1             44(D)x5 ff(.)x3 00(.)x1 30(0)x1     DIFFER
   0x0016  fb(.)x5 07(.)x2 04(.)x1 00(.)x1 +1u  30(0)x6 ff(.)x4                     DIFFER
   0x0017  fb(.)x6 00(.)x2 10(.)x1 07(.)x1     ff(.)x4 30(0)x4 fe(.)x1 00(.)x1     PARTIAL
   0x0018  af(.)x10                            ff(.)x3 01(.)x3 fe(.)x2 9e(.)x1 +1u  DIFFER
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
   0x0028  00(.)x10                            00(.)x7 08(.)x2 78(x)x1             PARTIAL
   0x0029  07(.)x10                            00(.)x7 29())x2 30(0)x1             DIFFER
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
  prompts_b/openthread_13313.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 13313,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 13313 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 13313 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 13313 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).