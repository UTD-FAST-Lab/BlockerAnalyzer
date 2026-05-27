==== BLOCKER ====
Target: openthread
Branch ID: 8453
Location: /src/openthread/src/core/common/message.cpp:523:13
Enclosing function: ot::Message::GetFirstChunk(unsigned short, unsigned short&, ot::Message::Chunk&) const
Source line:         if (aOffset < kBufferDataSize)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            5        5          0  REFERENCE
cmplog                          10        0          0  REFERENCE
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 16  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.35h  loser=11.05h
  avg hitcount on branch: winner=36243  loser=0
  prob_div=1.00  dur_div=10.70h  hit_div=36243
  subject-level: delta_AUC=2557680.0  p_AUC=0.0002  delta_Final=165.0  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/openthread/8453/{W,L}/branch_coverage_show.txt

--- Enclosing function: ot::Message::GetFirstChunk(unsigned short, unsigned short&, ot::Message::Chunk&) const (/src/openthread/src/core/common/message.cpp:486-539) ---
[ ]   484  
[ ]   485  void Message::GetFirstChunk(uint16_t aOffset, uint16_t &aLength, Chunk &aChunk) const
[B]   486  {
[ ]   487      // This method gets the first message chunk (contiguous data
[ ]   488      // buffer) corresponding to a given offset and length. On exit
[ ]   489      // `aChunk` is updated such that `aChunk.GetBytes()` gives the
[ ]   490      // pointer to the start of chunk and `aChunk.GetLength()` gives
[ ]   491      // its length. The `aLength` is also decreased by the chunk
[ ]   492      // length.
[ ]   493  
[B]   494      VerifyOrExit(aOffset < GetLength(), aChunk.SetLength(0));
[ ]   495  
[B]   496      if (aOffset + aLength >= GetLength())
[B]   497      {
[B]   498          aLength = GetLength() - aOffset;
[B]   499      }
[ ]   500  
[B]   501      aOffset += GetReserved();
[ ]   502  
[B]   503      aChunk.SetBuffer(this);
[ ]   504  
[ ]   505      // Special case for the first buffer
[ ]   506  
[B]   507      if (aOffset < kHeadBufferDataSize)
[B]   508      {
[B]   509          aChunk.Init(GetFirstData() + aOffset, kHeadBufferDataSize - aOffset);
[B]   510          ExitNow();
[B]   511      }
[ ]   512  
[B]   513      aOffset -= kHeadBufferDataSize;
[ ]   514  
[ ]   515      // Find the `Buffer` matching the offset
[ ]   516  
[B]   517      while (true)
[B]   518      {
[B]   519          aChunk.SetBuffer(aChunk.GetBuffer()->GetNextBuffer());
[ ]   520  
[B]   521          OT_ASSERT(aChunk.GetBuffer() != nullptr);
[ ]   522  
[B]   523          if (aOffset < kBufferDataSize) <-- BLOCKER
[B]   524          {
[B]   525              aChunk.Init(aChunk.GetBuffer()->GetData() + aOffset, kBufferDataSize - aOffset);
[B]   526              ExitNow();
[B]   527          }
[ ]   528  
[W]   529          aOffset -= kBufferDataSize;
[W]   530      }
[ ]   531  
[B]   532  exit:
[B]   533      if (aChunk.GetLength() > aLength)
[B]   534      {
[B]   535          aChunk.SetLength(aLength);
[B]   536      }
[ ]   537  
[B]   538      aLength -= aChunk.GetLength();
[B]   539  }

--- Caller (1 hop): ot::Message::ReadBytes(unsigned short, void*, unsigned short) const (/src/openthread/src/core/common/message.cpp:569-583, calls ot::Message::GetFirstChunk(unsigned short, unsigned short&, ot::Message::Chunk&) const at line 573) (full body — short) ---
[B]   569  {
[B]   570      uint8_t *bufPtr = reinterpret_cast<uint8_t *>(aBuf);
[B]   571      Chunk    chunk;
[ ]   572  
[B]   573      GetFirstChunk(aOffset, aLength, chunk); <-- CALL
[ ]   574  
[B]   575      while (chunk.GetLength() > 0)
[B]   576      {
[B]   577          chunk.CopyBytesTo(bufPtr);
[B]   578          bufPtr += chunk.GetLength();
[B]   579          GetNextChunk(aLength, chunk);
[B]   580      }
[ ]   581  
[B]   582      return static_cast<uint16_t>(bufPtr - reinterpret_cast<uint8_t *>(aBuf));
[B]   583  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  ot::Checksum::Calculate(ot::Ip4::Address const&, ot::Ip4::Address const&, unsigned char, ot::Message const&)  (/src/openthread/src/core/net/checksum.cpp:123-146, calls ot::Message::GetFirstChunk(unsigned short, unsigned short&, ot::Message::Chunk&) const at line 139)
hop 2  ot::Checksum::Calculate(ot::Ip6::Address const&, ot::Ip6::Address const&, unsigned char, ot::Message const&)  (/src/openthread/src/core/net/checksum.cpp:97-117, calls ot::Message::GetFirstChunk(unsigned short, unsigned short&, ot::Message::Chunk&) const at line 110)
hop 3  ot::Checksum::UpdateMessageChecksum(ot::Message&, ot::Ip6::Address const&, ot::Ip6::Address const&, unsigned char)  (/src/openthread/src/core/net/checksum.cpp:161-190, calls ot::Checksum::Calculate(ot::Ip6::Address const&, ot::Ip6::Address const&, unsigned char, ot::Message const&) at line 185)
hop 3  ot::Checksum::VerifyMessageChecksum(ot::Message const&, ot::Ip6::MessageInfo const&, unsigned char)  (/src/openthread/src/core/net/checksum.cpp:149-155, calls ot::Checksum::Calculate(ot::Ip6::Address const&, ot::Ip6::Address const&, unsigned char, ot::Message const&) at line 152)
hop 4  ot::Ip6::Icmp::HandleMessage(ot::Message&, ot::Ip6::MessageInfo&)  (/src/openthread/src/core/net/icmp6.cpp:132-154, calls ot::Checksum::VerifyMessageChecksum(ot::Message const&, ot::Ip6::MessageInfo const&, unsigned char) at line 138)
hop 4  ot::Ip6::Ip6::SendDatagram(ot::Message&, ot::Ip6::MessageInfo&, unsigned char)  (/src/openthread/src/core/net/ip6.cpp:447-526, calls ot::Checksum::UpdateMessageChecksum(ot::Message&, ot::Ip6::Address const&, ot::Ip6::Address const&, unsigned char) at line 488)
hop 4  ot::Ip6::Tcp::HandleMessage(ot::Ip6::Header&, ot::Message&, ot::Ip6::MessageInfo&)  (/src/openthread/src/core/net/tcp6.cpp:596-668, calls ot::Checksum::VerifyMessageChecksum(ot::Message const&, ot::Ip6::MessageInfo const&, unsigned char) at line 624)
hop 5  void ot::MeshCoP::BorderAgent::HandleTmf<(ot::Uri)31>(ot::Coap::Message&, ot::Ip6::MessageInfo const&)  (/src/openthread/src/core/meshcop/border_agent.cpp:254-291, calls ot::Ip6::Ip6::SendDatagram(ot::Message&, ot::Ip6::MessageInfo&, unsigned char) at line 283)
hop 5  ot::Ip6::Icmp::SendEchoRequest(ot::Message&, ot::Ip6::MessageInfo const&, unsigned short)  (/src/openthread/src/core/net/icmp6.cpp:62-82, calls ot::Ip6::Ip6::SendDatagram(ot::Message&, ot::Ip6::MessageInfo&, unsigned char) at line 76)
hop 5  ot::Ip6::Ip6::HandlePayload(ot::Ip6::Header&, ot::Message&, ot::Ip6::MessageInfo&, unsigned char, ot::Message::Ownership)  (/src/openthread/src/core/net/ip6.cpp:927-989, calls ot::Ip6::Icmp::HandleMessage(ot::Message&, ot::Ip6::MessageInfo&) at line 957)
hop 6  ot::Ip6::Ip6::HandleDatagram(ot::Message&, ot::Ip6::Ip6::MessageOrigin, void const*, bool)  (/src/openthread/src/core/net/ip6.cpp:1163-1364, calls ot::Ip6::Ip6::HandlePayload(ot::Ip6::Header&, ot::Message&, ot::Ip6::MessageInfo&, unsigned char, ot::Message::Ownership) at line 1278)
hop 6  ot::Utils::PingSender::SendPing()  (/src/openthread/src/core/utils/ping_sender.cpp:128-170, calls ot::Ip6::Icmp::SendEchoRequest(ot::Message&, ot::Ip6::MessageInfo const&, unsigned short) at line 149)
hop 7  ot::Ip6::Ip6::HandleSendQueue()  (/src/openthread/src/core/net/ip6.cpp:529-537, calls ot::Ip6::Ip6::HandleDatagram(ot::Message&, ot::Ip6::Ip6::MessageOrigin, void const*, bool) at line 535)
hop 7  ot::Ip6::Ip6::InsertMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:244-322, calls ot::Ip6::Ip6::HandleDatagram(ot::Message&, ot::Ip6::Ip6::MessageOrigin, void const*, bool) at line 307)
hop 7  ot::Utils::PingSender::HandleTimer()  (/src/openthread/src/core/utils/ping_sender.cpp:173-182, calls ot::Utils::PingSender::SendPing() at line 176)
hop 7  ot::Utils::PingSender::Ping(ot::Utils::PingSender::Config const&)  (/src/openthread/src/core/utils/ping_sender.cpp:101-119, calls ot::Utils::PingSender::SendPing() at line 115)
hop 8  ot::MeshCoP::Dtls::HandleTimer(ot::Timer&)  (/src/openthread/src/core/meshcop/dtls.cpp:830-832, calls ot::Utils::PingSender::HandleTimer() at line 831)
hop 8  ot::MeshCoP::JoinerRouter::HandleTimer()  (/src/openthread/src/core/meshcop/joiner_router.cpp:234-234, calls ot::Utils::PingSender::HandleTimer() at line 234)
hop 8  ot::Ip6::Ip6::SendRaw(ot::Message&, bool)  (/src/openthread/src/core/net/ip6.cpp:1132-1160, calls ot::Ip6::Ip6::InsertMplOption(ot::Message&, ot::Ip6::Header&) at line 1142)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      84       253  ot::Buffer::GetData() const  (/src/openthread/src/core/common/message.hpp:242-242)
      40       129  ot::Message::GetMessageQueue() const  (/src/openthread/src/core/common/message.hpp:1186-1188)
       0        68  ot::Message::Iterator::Advance()  (/src/openthread/src/core/common/message.cpp:216-219)
       0        39  ot::Message::GetDatagramTag() const  (/src/openthread/src/core/common/message.hpp:898-898)
       0        31  ot::Message::Clone() const  (/src/openthread/src/core/common/message.hpp:889-889)
      10        31  ot::MessageQueue::Enqueue(ot::Message&)  (/src/openthread/src/core/common/message.hpp:1437-1437)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  ot::Checksum::VerifyMessageChecksum(ot::Message const&, ot::Ip6::MessageInfo const&, unsigned char)  (/src/openthread/src/core/net/checksum.cpp:149-155) ---
  d=3   L 154  T=20 F=4  T=20 F=0  return (checksum.GetValue() == kValidRxChecksum) ? kError...
--- d=1  ot::Message::GetFirstChunk(unsigned short, unsigned short&, ot::Message::Chunk&) const  (/src/openthread/src/core/common/message.cpp:486-539) ---
  d=1   L 523  T=47 F=35  T=176 F=0  if (aOffset < kBufferDataSize)  <-- BLOCKER

[off-chain: 25 additional divergent branches across 14 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=27e3a6c597f95b0d, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=2385s, mutation_op=BytesDeleteMutator,ByteDecMutator,DwordInterestingMutator):
  0000: 78 66 65 5c 78 00 10 2c b0 78 da 30 5c 78 30 30   xfe\x..,.x.0\x00
  0010: 5c 78 33 62 5c 78 34 30 5c fd de ad 00 be ef 00   \x3b\x40\.......
  0020: 00 00 00 00 ff fe 00 fc 00 05 06 07 1a ff 80 00   ................
  0030: c7 ff ff 07 00 00 92 06 02                        .........
Seed 2 (id=6af1cac90f1e693f, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=2454s, mutation_op=CrossoverInsertMutator,ByteIncMutator):
  0000: 78 66 65 5c 78 00 10 2c b0 78 da 30 5c 78 30 30   xfe\x..,.x.0\x00
  0010: 5c 78 33 62 5c 78 34 30 5c fd de ad 00 be ef 00   \x3b\x40\.......
  0020: 00 00 00 00 ff fe 00 fc 00 7f 06 03 1a ff 00 00   ................
  0030: c7 ff ff 00 00 00 92 06 02                        .........
Seed 3 (id=57f58893e9527e4e, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=2525s, mutation_op=BytesDeleteMutator):
  0000: 78 66 65 5c 78 00 10 2c b0 78 da 30 5c 78 30 30   xfe\x..,.x.0\x00
  0010: 5c 78 33 62 5c 78 34 30 5c fd de ad 00 be ef 00   \x3b\x40\.......
  0020: 00 00 00 00 ff fe 00 fc 00 00 06 03 1a ff 80 00   ................
  0030: c7 ff ff 00 00 00 92 06 01                        .........
Seed 4 (id=451d31b7b7277e15, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=2884s, mutation_op=BytesSetMutator,WordInterestingMutator):
  0000: 78 66 65 5c 78 00 10 2c b0 78 da 30 5c 78 30 30   xfe\x..,.x.0\x00
  0010: 5c 78 00 10 5c 78 34 30 5c fd de ad 00 be ef 00   \x..\x40\.......
  0020: 00 00 00 00 ff fe 00 fc 00 00 06 07 92 92 92 92   ................
  0030: 92 92 92 92 92 92 92 06 01                        .........
Seed 5 (id=27a8a44f1158252d, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=2885s, mutation_op=ByteIncMutator,BitFlipMutator):
  0000: 78 66 65 5c 78 00 10 2c 90 78 da 30 5c 78 30 30   xfe\x..,.x.0\x00
  0010: 5c 78 33 62 5c 78 34 30 5c fd de ad 00 be ef 00   \x3b\x40\.......
  0020: 00 00 00 00 ff fe 00 fc 00 06 06 07 1a ff 80 00   ................
  0030: c7 ff ff 07 00 00 92 06 02                        .........

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=023f811fa394f34b, size=141 bytes, fuzzer=naive, trial=1, discovered_at=2416s, mutation_op=BitFlipMutator):
  0000: 81 65 10 00 13 00 64 00 01 f0 04 00 00 66 65 5c   .e....d......fe\
  0010: 88 87 87 87 87 87 87 87 7f ff 53 ff ff ff ff ff   ..........S.....
  0020: 00 08 30 9c c4 20 00 00 00 00 00 00 00 00 00 6d   ..0.. .........m
  0030: 00 79 00 02 00 08 00 6d 00 42 16 5f 17 00 a4 00   .y.....m.B._....
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
   0x0000  78(x)x10                            81(.)x5 80(.)x5                     DIFFER
   0x0001  66(f)x10                            65(e)x10                            DIFFER
   0x0002  65(e)x10                            24($)x3 23(#)x3 10(.)x2 2e(.)x2     DIFFER
   0x0003  5c(\)x10                            00(.)x10                            DIFFER
   0x0004  78(x)x10                            13(.)x10                            DIFFER
   0x0006  10(.)x10                            64(d)x9 9b(.)x1                     DIFFER
   0x0007  2c(,)x10                            00(.)x10                            DIFFER
   0x0008  b0(.)x9 90(.)x1                     01(.)x7 fe(.)x2 5c(\)x1             DIFFER
   0x0009  78(x)x10                            f0(.)x5 c3(.)x2 10(.)x1 5c(\)x1 +1u  DIFFER
   0x000a  da(.)x10                            04(.)x5 09(.)x2 5c(\)x1 00(.)x1 +1u  DIFFER
   0x000b  30(0)x10                            00(.)x8 5c(\)x1 e0(.)x1             DIFFER
   0x000c  5c(\)x10                            00(.)x9 5c(\)x1                     PARTIAL
   0x000d  78(x)x10                            66(f)x8 5c(\)x1 00(.)x1             DIFFER
   0x000e  30(0)x10                            65(e)x8 5c(\)x1 00(.)x1             DIFFER
   0x000f  30(0)x10                            5c(\)x9 00(.)x1                     DIFFER
   0x0010  5c(\)x10                            88(.)x6 81(.)x2 01(.)x1 87(.)x1     DIFFER
   0x0011  78(x)x10                            87(.)x5 7e(~)x4 64(d)x1             DIFFER
   0x0012  33(3)x9 00(.)x1                     87(.)x10                            DIFFER
   0x0013  62(b)x9 10(.)x1                     87(.)x10                            DIFFER
   0x0014  5c(\)x10                            7c(|)x8 87(.)x2                     DIFFER
   0x0015  78(x)x10                            87(.)x7 78(x)x2 17(.)x1             PARTIAL
   0x0016  34(4)x10                            87(.)x10                            DIFFER
   0x0017  30(0)x10                            87(.)x10                            DIFFER
   0x0018  5c(\)x10                            7f(.)x6 5f(_)x2 80(.)x2             DIFFER
   0x0019  fd(.)x10                            ff(.)x10                            DIFFER
   0x001a  de(.)x10                            53(S)x10                            DIFFER
   0x001b  ad(.)x10                            ff(.)x5 00(.)x5                     DIFFER
   0x001c  00(.)x10                            ff(.)x5 00(.)x5                     PARTIAL
   0x001d  be(.)x10                            ff(.)x5 00(.)x5                     DIFFER
   0x001e  ef(.)x10                            ff(.)x5 00(.)x5                     DIFFER
   0x001f  00(.)x10                            ff(.)x5 00(.)x5                     PARTIAL
   0x0021  00(.)x10                            08(.)x5 00(.)x5                     PARTIAL
   0x0022  00(.)x10                            30(0)x5 00(.)x5                     PARTIAL
   0x0023  00(.)x10                            00(.)x5 9c(.)x4 9b(.)x1             PARTIAL
   0x0024  ff(.)x10                            00(.)x5 c4(.)x3 a1(.)x2             DIFFER
   0x0025  fe(.)x10                            20( )x5 00(.)x5                     DIFFER
   0x0027  fc(.)x10                            00(.)x8 6d(m)x1 0d(.)x1             DIFFER
   0x0028  00(.)x10                            00(.)x8 0d(.)x1 01(.)x1             PARTIAL
   0x0029  3a(:)x4 00(.)x2 05(.)x1 7f(.)x1 +2u  00(.)x8 d7(.)x1 0d(.)x1             PARTIAL
   0x002a  06(.)x10                            00(.)x8 02(.)x1 0d(.)x1             DIFFER
   ... (14 more divergent offsets)
==== MECHANISM CONTEXT (involved fuzzers only) ====
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
  prompts/--BR/04_openthread_8453.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 8453,
  "target": "openthread",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 8453 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 8453 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 8453 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).