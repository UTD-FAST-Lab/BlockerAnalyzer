==== BLOCKER ====
Target: openthread
Branch ID: 13391
Location: /src/openthread/src/core/utils/history_tracker.cpp:131:36
Enclosing function: ot::Utils::HistoryTracker::RecordMessage(ot::Message const&, ot::Mac::Address const&, ot::Utils::HistoryTracker::MessageType)
Source line:     entry->mIcmp6Type            = headers.IsIcmp6() ? headers.GetIcmpHeader().GetType() : 0;
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            9        1          0  winner (I2S vs cmplog)
cmplog                           1        9          0  loser (I2S vs naive)
value_profile                    9        1          0  REFERENCE
value_profile_cmplog             3        7          0  REFERENCE
naive_ctx                        6        4          0  REFERENCE
naive_ngram4                     6        4          0  REFERENCE
mopt                            10        0          0  REFERENCE
minimizer                        8        2          0  REFERENCE
fast                             6        4          0  REFERENCE
grimoire                         4        6          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=3.80h  loser=21.70h
  avg hitcount on branch: winner=1  loser=0
  prob_div=0.80  dur_div=17.90h  hit_div=1
  subject-level: delta_AUC=11709180.0  p_AUC=0.0002  delta_Final=125.3  p_final=0.0007

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/openthread/13391/{W,L}/branch_coverage_show.txt

--- Enclosing function: ot::Utils::HistoryTracker::RecordMessage(ot::Message const&, ot::Mac::Address const&, ot::Utils::HistoryTracker::MessageType) (/src/openthread/src/core/utils/history_tracker.cpp:82-183) ---
[ ]    80  
[ ]    81  void HistoryTracker::RecordMessage(const Message &aMessage, const Mac::Address &aMacAddresss, MessageType aType)
[B]    82  {
[B]    83      MessageInfo *entry = nullptr;
[B]    84      Ip6::Headers headers;
[ ]    85  
[B]    86      VerifyOrExit(aMessage.GetType() == Message::kTypeIp6);
[ ]    87  
[B]    88      SuccessOrExit(headers.ParseFrom(aMessage));
[ ]    89  
[B]    90  #if OPENTHREAD_CONFIG_HISTORY_TRACKER_EXCLUDE_THREAD_CONTROL_MESSAGES
[B]    91      if (headers.IsUdp())
[B]    92      {
[B]    93          uint16_t port = 0;
[ ]    94  
[B]    95          switch (aType)
[B]    96          {
[ ]    97          case kRxMessage:
[ ]    98              port = headers.GetDestinationPort();
[ ]    99              break;
[ ]   100  
[B]   101          case kTxMessage:
[B]   102              port = headers.GetSourcePort();
[B]   103              break;
[B]   104          }
[ ]   105  
[B]   106          VerifyOrExit((port != Mle::kUdpPort) && (port != Tmf::kUdpPort));
[B]   107      }
[B]   108  #endif
[ ]   109  
[B]   110      switch (aType)
[B]   111      {
[ ]   112      case kRxMessage:
[ ]   113          entry = mRxHistory.AddNewEntry();
[ ]   114          break;
[ ]   115  
[B]   116      case kTxMessage:
[B]   117          entry = mTxHistory.AddNewEntry();
[B]   118          break;
[B]   119      }
[ ]   120  
[B]   121      VerifyOrExit(entry != nullptr);
[ ]   122  
[B]   123      entry->mPayloadLength        = headers.GetIp6Header().GetPayloadLength();
[B]   124      entry->mNeighborRloc16       = aMacAddresss.IsShort() ? aMacAddresss.GetShort() : kInvalidRloc16;
[B]   125      entry->mSource.mAddress      = headers.GetSourceAddress();
[B]   126      entry->mSource.mPort         = headers.GetSourcePort();
[B]   127      entry->mDestination.mAddress = headers.GetDestinationAddress();
[B]   128      entry->mDestination.mPort    = headers.GetDestinationPort();
[B]   129      entry->mChecksum             = headers.GetChecksum();
[B]   130      entry->mIpProto              = headers.GetIpProto();
[B]   131      entry->mIcmp6Type            = headers.IsIcmp6() ? headers.GetIcmpHeader().GetType() : 0; <-- BLOCKER
[B]   132      entry->mAveRxRss             = (aType == kRxMessage) ? aMessage.GetRssAverager().GetAverage() : Radio::kInvalidRssi;
[B]   133      entry->mLinkSecurity         = aMessage.IsLinkSecurityEnabled();
[B]   134      entry->mTxSuccess            = (aType == kTxMessage) ? aMessage.GetTxSuccess() : true;
[B]   135      entry->mPriority             = aMessage.GetPriority();
[ ]   136  
[B]   137      if (aMacAddresss.IsExtended())
[B]   138      {
[B]   139          Neighbor *neighbor = Get<NeighborTable>().FindNeighbor(aMacAddresss, Neighbor::kInStateAnyExceptInvalid);
[ ]   140  
[B]   141          if (neighbor != nullptr)
[ ]   142          {
[ ]   143              entry->mNeighborRloc16 = neighbor->GetRloc16();
[ ]   144          }
[B]   145      }
[ ]   146  
[ ]   147  #if OPENTHREAD_CONFIG_MULTI_RADIO
[ ]   148      if (aMessage.IsRadioTypeSet())
[ ]   149      {
[ ]   150          switch (aMessage.GetRadioType())
[ ]   151          {
[ ]   152  #if OPENTHREAD_CONFIG_RADIO_LINK_IEEE_802_15_4_ENABLE
[ ]   153          case Mac::kRadioTypeIeee802154:
[ ]   154              entry->mRadioIeee802154 = true;
[ ]   155              break;
[ ]   156  #endif
[ ]   157  #if OPENTHREAD_CONFIG_RADIO_LINK_TREL_ENABLE
[ ]   158          case Mac::kRadioTypeTrel:
[ ]   159              entry->mRadioTrelUdp6 = true;
[ ]   160              break;
[ ]   161  #endif
[ ]   162          }
[ ]   163  
[ ]   164          // Radio type may not be set on a tx message indicating that it
[ ]   165          // was sent over all radio types (e.g., for broadcast frame).
[ ]   166          // In such a case, we set all supported radios from `else`
[ ]   167          // block below.
[ ]   168      }
[ ]   169      else
[ ]   170  #endif // OPENTHREAD_CONFIG_MULTI_RADIO
[B]   171      {
[B]   172  #if OPENTHREAD_CONFIG_RADIO_LINK_IEEE_802_15_4_ENABLE
[B]   173          entry->mRadioIeee802154 = true;
[B]   174  #endif
[ ]   175  
[ ]   176  #if OPENTHREAD_CONFIG_RADIO_LINK_TREL_ENABLE
[ ]   177          entry->mRadioTrelUdp6 = true;
[ ]   178  #endif
[B]   179      }
[ ]   180  
[B]   181  exit:
[B]   182      return;
[B]   183  }

--- Caller (1 hop): ot::Utils::HistoryTracker::RecordTxMessage(ot::Message const&, ot::Mac::Address const&) (/src/openthread/src/core/utils/history_tracker.hpp:377-379, calls ot::Utils::HistoryTracker::RecordMessage(ot::Message const&, ot::Mac::Address const&, ot::Utils::HistoryTracker::MessageType) at line 378) (full body — short) ---
[B]   377      {
[B]   378          RecordMessage(aMessage, aMacDest, kTxMessage); <-- CALL
[B]   379      }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  ot::Utils::HistoryTracker::RecordRxMessage(ot::Message const&, ot::Mac::Address const&)  (/src/openthread/src/core/utils/history_tracker.hpp:372-374, calls ot::Utils::HistoryTracker::RecordMessage(ot::Message const&, ot::Mac::Address const&, ot::Utils::HistoryTracker::MessageType) at line 373)
hop 2  ot::Utils::HistoryTracker::RecordTxMessage(ot::Message const&, ot::Mac::Address const&)  (/src/openthread/src/core/utils/history_tracker.hpp:377-379, calls ot::Utils::HistoryTracker::RecordMessage(ot::Message const&, ot::Mac::Address const&, ot::Utils::HistoryTracker::MessageType) at line 378)
hop 3  ot::MeshForwarder::HandleDatagram(ot::Message&, ot::ThreadLinkInfo const&, ot::Mac::Address const&)  (/src/openthread/src/core/thread/mesh_forwarder.cpp:1598-1611, calls ot::Utils::HistoryTracker::RecordRxMessage(ot::Message const&, ot::Mac::Address const&) at line 1600)
hop 3  ot::MeshForwarder::UpdateSendMessage(otError, ot::Mac::Address&, ot::Neighbor*)  (/src/openthread/src/core/thread/mesh_forwarder.cpp:1166-1270, calls ot::Utils::HistoryTracker::RecordTxMessage(ot::Message const&, ot::Mac::Address const&) at line 1222)
hop 4  ot::Ip6::Ip6::HandleSendQueue()  (/src/openthread/src/core/net/ip6.cpp:529-537, calls ot::MeshForwarder::HandleDatagram(ot::Message&, ot::ThreadLinkInfo const&, ot::Mac::Address const&) at line 535)
hop 4  ot::Ip6::Ip6::InsertMplOption(ot::Message&, ot::Ip6::Header&)  (/src/openthread/src/core/net/ip6.cpp:244-322, calls ot::MeshForwarder::HandleDatagram(ot::Message&, ot::ThreadLinkInfo const&, ot::Mac::Address const&) at line 307)
hop 4  ot::MeshForwarder::HandleSentFrame(ot::Mac::TxFrame&, otError)  (/src/openthread/src/core/thread/mesh_forwarder.cpp:1130-1163, calls ot::MeshForwarder::UpdateSendMessage(otError, ot::Mac::Address&, ot::Neighbor*) at line 1159)
hop 5  ot::Mac::Mac::HandleTransmitDone(ot::Mac::TxFrame&, ot::Mac::RxFrame*, otError)  (/src/openthread/src/core/mac/mac.cpp:1258-1452, calls ot::MeshForwarder::HandleSentFrame(ot::Mac::TxFrame&, otError) at line 1404)
hop 5  ot::Ip6::Ip6::SendRaw(ot::Message&, bool)  (/src/openthread/src/core/net/ip6.cpp:1132-1160, calls ot::Ip6::Ip6::InsertMplOption(ot::Message&, ot::Ip6::Header&) at line 1142)
hop 6  otIp6Send  (/src/openthread/src/core/api/ip6_api.cpp:134-137, calls ot::Ip6::Ip6::SendRaw(ot::Message&, bool) at line 135)
hop 6  ot::Mac::SubMac::HandleTimer()  (/src/openthread/src/core/mac/sub_mac.cpp:769-800, calls ot::Mac::Mac::HandleTransmitDone(ot::Mac::TxFrame&, ot::Mac::RxFrame*, otError) at line 784)
hop 6  ot::Mac::SubMac::SignalFrameCounterUsed(unsigned int)  (/src/openthread/src/core/mac/sub_mac.cpp:951-967, calls ot::Mac::Mac::HandleTransmitDone(ot::Mac::TxFrame&, ot::Mac::RxFrame*, otError) at line 960)
hop 7  ot::Mac::SubMac::HandleReceiveDone(ot::Mac::RxFrame*, otError)  (/src/openthread/src/core/mac/sub_mac.cpp:280-317, calls ot::Mac::SubMac::SignalFrameCounterUsed(unsigned int) at line 288)
hop 7  ot::Mac::SubMac::ProcessTransmitSecurity()  (/src/openthread/src/core/mac/sub_mac.cpp:369-407, calls ot::Mac::SubMac::SignalFrameCounterUsed(unsigned int) at line 393)
hop 7  ot::MeshCoP::Dtls::HandleTimer(ot::Timer&)  (/src/openthread/src/core/meshcop/dtls.cpp:830-832, calls ot::Mac::SubMac::HandleTimer() at line 831)
hop 7  ot::MeshCoP::JoinerRouter::HandleTimer()  (/src/openthread/src/core/meshcop/joiner_router.cpp:234-234, calls ot::Mac::SubMac::HandleTimer() at line 234)
hop 7  LLVMFuzzerTestOneInput  (/src/openthread/tests/fuzz/ip6_send.cpp:61-112, calls otIp6Send at line 91)
hop 8  ot::Mac::Mac::BeginTransmit()  (/src/openthread/src/core/mac/mac.cpp:920-1109, calls ot::Mac::SubMac::ProcessTransmitSecurity() at line 1055)
hop 8  ot::Mac::SubMac::Send()  (/src/openthread/src/core/mac/sub_mac.cpp:320-366, calls ot::Mac::SubMac::ProcessTransmitSecurity() at line 353)
hop 8  ot::MeshCoP::DatasetManager::HandleTimer()  (/src/openthread/src/core/meshcop/dataset_manager.cpp:241-241, calls ot::MeshCoP::JoinerRouter::HandleTimer() at line 241)
hop 8  otPlatRadioReceiveDone  (/src/openthread/src/core/radio/radio_platform.cpp:49-66, calls ot::Mac::SubMac::HandleReceiveDone(ot::Mac::RxFrame*, otError) at line 62)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      75       272  ot::Utils::HistoryTracker::Timestamp::SetToNow()  (/src/openthread/src/core/utils/history_tracker.cpp:421-431)
      75       272  ot::Utils::HistoryTracker::List::Add(unsigned short, ot::Utils::HistoryTracker::Timestamp*)  (/src/openthread/src/core/utils/history_tracker.cpp:454-468)
      75       272  ot::Utils::HistoryTracker::EntryList<otHistoryTrackerNetworkInfo, (unsigned short)32>::AddNewEntry()  (/src/openthread/src/core/utils/history_tracker.hpp:335-335)
      75       272  ot::Utils::HistoryTracker::EntryList<otHistoryTrackerMessageInfo, (unsigned short)32>::AddNewEntry()  (/src/openthread/src/core/utils/history_tracker.hpp:335-335)
      75       272  ot::Utils::HistoryTracker::EntryList<otHistoryTrackerNeighborInfo, (unsigned short)64>::AddNewEntry()  (/src/openthread/src/core/utils/history_tracker.hpp:335-335)
      75       272  ot::Utils::HistoryTracker::EntryList<otHistoryTrackerUnicastAddressInfo, (unsigned short)20>::AddNewEntry()  (/src/openthread/src/core/utils/history_tracker.hpp:335-335)
      75       272  ot::Utils::HistoryTracker::EntryList<otHistoryTrackerMulticastAddressInfo, (unsigned short)20>::AddNewEntry()  (/src/openthread/src/core/utils/history_tracker.hpp:335-335)
      75       272  ot::Utils::HistoryTracker::EntryList<otHistoryTrackerOnMeshPrefixInfo, (unsigned short)32>::AddNewEntry()  (/src/openthread/src/core/utils/history_tracker.hpp:335-335)
      75       272  ot::Utils::HistoryTracker::EntryList<otHistoryTrackerExternalRouteInfo, (unsigned short)32>::AddNewEntry()  (/src/openthread/src/core/utils/history_tracker.hpp:335-335)
      42       140  ot::Utils::HistoryTracker::RecordAddressEvent(ot::Ip6::Netif::AddressEvent, ot::Ip6::Netif::MulticastAddress const&, ot::Ip6::Netif::AddressOrigin)  (/src/openthread/src/core/utils/history_tracker.cpp:269-280)
      21        92  ot::Utils::HistoryTracker::RecordMessage(ot::Message const&, ot::Mac::Address const&, ot::Utils::HistoryTracker::MessageType)  (/src/openthread/src/core/utils/history_tracker.cpp:82-183)  <-- enclosing
      21        92  ot::Utils::HistoryTracker::RecordTxMessage(ot::Message const&, ot::Mac::Address const&)  (/src/openthread/src/core/utils/history_tracker.hpp:377-379)
      27        90  ot::Utils::HistoryTracker::RecordAddressEvent(ot::Ip6::Netif::AddressEvent, ot::Ip6::Netif::UnicastAddress const&)  (/src/openthread/src/core/utils/history_tracker.cpp:248-264)
      24        80  ot::Utils::HistoryTracker::List::List()  (/src/openthread/src/core/utils/history_tracker.cpp:442-445)
       9        30  ot::Utils::HistoryTracker::HandleNotifierEvents(ot::Events)  (/src/openthread/src/core/utils/history_tracker.cpp:363-376)
... (3 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  ot::Utils::HistoryTracker::RecordMessage(ot::Message const&, ot::Mac::Address const&, ot::Utils::HistoryTracker::MessageType)  (/src/openthread/src/core/utils/history_tracker.cpp:82-183) ---
  d=1   L  91  T=18 F=3  T=60 F=32  if (headers.IsUdp())
  d=1   L  95  T=0 F=18  T=0 F=60  switch (aType)
  d=1   L  97  T=0 F=18  T=0 F=60  case kRxMessage:
  d=1   L 101  T=18 F=0  T=60 F=0  case kTxMessage:
  d=1   L 110  T=0 F=3  T=0 F=32  switch (aType)
  d=1   L 112  T=0 F=3  T=0 F=32  case kRxMessage:
  d=1   L 116  T=3 F=0  T=32 F=0  case kTxMessage:
  d=1   L 124  T=2 F=1  T=26 F=6  entry->mNeighborRloc16       = aMacAddresss.IsShort() ? a...
  d=1   L 131  T=3 F=0  T=0 F=32  entry->mIcmp6Type            = headers.IsIcmp6() ? header...  <-- BLOCKER
  d=1   L 132  T=0 F=3  T=0 F=32  entry->mAveRxRss             = (aType == kRxMessage) ? aM...
  d=1   L 134  T=3 F=0  T=32 F=0  entry->mTxSuccess            = (aType == kTxMessage) ? aM...
  d=1   L 137  T=1 F=2  T=6 F=26  if (aMacAddresss.IsExtended())
  d=1   L 141  T=0 F=1  T=0 F=6  if (neighbor != nullptr)

[off-chain: 11 additional divergent branches across 6 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=d3396de23a76ce4b, size=57 bytes, fuzzer=naive, trial=1, discovered_at=2151s, mutation_op=ByteDecMutator,ByteAddMutator,ByteNegMutator):
  0000: cb 62 5c 02 ff 00 10 3a 3a 33 31 3a 3a 3a 30 00   .b\....::31:::0.
  0010: 00 ff ff 00 ff 00 00 00 7f ff e2 ff ff ff 00 b4   ................
  0020: ff 00 00 00 00 dd ff 00 e8 80 7e aa 83 00 00 6d   ..........~....m
  0030: 00 00 00 ff e7 5c 78 30 30                        .....\x00
Seed 2 (id=3837ed7ffde10735, size=57 bytes, fuzzer=naive, trial=1, discovered_at=2295s, mutation_op=TokenReplace,DwordInterestingMutator):
  0000: cb 62 5c 02 00 00 10 3a 3a 33 3a 3a 3a 3a 30 00   .b\....::3::::0.
  0010: 00 ff ff 00 ff 00 00 00 7f ff 00 01 00 00 00 b4   ................
  0020: ff 00 00 00 00 dd ff 57 92 01 00 00 01 00 00 6d   .......W.......m
  0030: 00 00 00 ff 00 5c 78 30 30                        .....\x00
Seed 3 (id=7e40089c819c75db, size=57 bytes, fuzzer=naive, trial=1, discovered_at=8158s, mutation_op=WordInterestingMutator,TokenReplace,ByteRandMutator,ByteAddMutator,ByteDecMutator):
  0000: cb 62 5c 02 ff 00 10 3a 3a 33 3a 3a 3a 3a 30 00   .b\....::3::::0.
  0010: 00 ff ff 00 ff 00 00 00 7f fe 80 01 ff 48 00 b4   .............H..
  0020: ff 00 00 00 00 dd ff 00 e8 01 00 00 01 00 00 6d   ...............m
  0030: 00 00 00 ff 00 00 01 ff ff                        .........

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0096c8a9856dd0ab, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=101s, mutation_op=CrossoverInsertMutator,DwordAddMutator):
  0000: 78 66 10 01 00 00 00 29 01 00 00 00 00 00 00 00   xf.....)........
  0010: 00 00 00 00 00 a3 78 f8 ff ff 13 01 30 5c 78 30   ......x.....0\x0
  0020: 30 5c 78 30 30 80 78 30 30                        0\x00.x00
Seed 2 (id=0063b6c0f181163b, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=278s, mutation_op=ByteInterestingMutator):
  0000: 78 60 10 ff 01 00 00 29 ff 00 00 00 00 00 00 a0   x`.....)........
  0010: 2c fe 00 18 00 a3 78 f8 ff ff ff ff 30 5c 78 30   ,.....x.....0\x0
  0020: 30 1a 1a 1a 1a 1a f8 1a 1a                        0........
Seed 3 (id=01042de80bf2522a, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=633s, mutation_op=DwordAddMutator):
  0000: 78 66 10 7f 01 00 10 00 7f fd de ad 00 be ef 00   xf..............
  0010: 00 00 00 00 ff fe 00 6c 00 fe 80 9e 01 00 01 00   .......l........
  0020: 00 f8 53 fe f7 c6 58 00 00 07 00 6d 02 40 7f 6d   ..S...X....m.@.m
  0030: 00 07 02 00 fe 00 78 30 30                        ......x00
Seed 4 (id=01042de80bf2522a-2, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=678s, mutation_op=TokenReplace,BytesDeleteMutator,DwordInterestingMutator,DwordInterestingMutator,QwordAddMutator,BytesDeleteMutator,DwordInterestingMutator):
  0000: 78 66 10 7f 01 00 10 00 7f fd de ad 00 be ef 00   xf..............
  0010: 00 00 00 00 ff fe 00 6c 00 fe 80 9e 01 00 01 00   .......l........
  0020: 00 f8 53 fe f7 c6 58 00 00 07 00 6d 02 40 7f 6d   ..S...X....m.@.m
  0030: 00 07 02 00 fe 00 78 30 30                        ......x00
Seed 5 (id=008f597635438ba4, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=725s, mutation_op=CrossoverInsertMutator,DwordInterestingMutator):
  0000: 78 66 10 7f 01 00 10 00 7f 00 b0 00 ff ff ff fc   xf..............
  0010: 03 a0 1a 05 2d a3 07 09 af ff 03 03 07 00 00 40   ....-..........@
  0020: ff ff ff 07 ff af 2c ff 0d 3a 00 6d 02 40 7f 6d   ......,..:.m.@.m
  0030: 00 04 ff ff fe 06 78 30 30                        ......x00


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  cb(.)x3                             78(x)x6 77(w)x3 38(8)x1             DIFFER
   0x0001  62(b)x3                             66(f)x6 67(g)x3 60(`)x1             DIFFER
   0x0002  5c(\)x3                             10(.)x7 ef(.)x2 01(.)x1             DIFFER
   0x0003  02(.)x3                             7f(.)x5 00(.)x3 01(.)x1 ff(.)x1     DIFFER
   0x0004  ff(.)x2 00(.)x1                     01(.)x5 00(.)x4 02(.)x1             PARTIAL
   0x0006  10(.)x3                             10(.)x4 78(x)x3 00(.)x2 29())x1     PARTIAL
   0x0007  3a(:)x3                             00(.)x7 29())x3                     DIFFER
   0x0008  3a(:)x3                             7f(.)x4 40(@)x3 ff(.)x2 01(.)x1     DIFFER
   0x0009  33(3)x3                             00(.)x4 fd(.)x2 bc(.)x2 06(.)x1 +1u  DIFFER
   0x000a  3a(:)x2 31(1)x1                     00(.)x6 de(.)x2 b0(.)x2             DIFFER
   0x000b  3a(:)x3                             00(.)x5 ad(.)x2 bc(.)x2 ff(.)x1     DIFFER
   0x000c  3a(:)x3                             00(.)x5 ff(.)x3 b3(.)x2             DIFFER
   0x000d  3a(:)x3                             ff(.)x4 00(.)x3 be(.)x2 20( )x1     DIFFER
   0x000e  30(0)x3                             00(.)x4 ff(.)x4 ef(.)x2             DIFFER
   0x000f  00(.)x3                             00(.)x5 fe(.)x2 a0(.)x1 fc(.)x1 +1u  PARTIAL
   0x0010  00(.)x3                             00(.)x5 ff(.)x3 2c(,)x1 03(.)x1     PARTIAL
   0x0011  ff(.)x3                             00(.)x4 a0(.)x3 fe(.)x1 10(.)x1 +1u  DIFFER
   0x0012  ff(.)x3                             00(.)x5 ff(.)x3 1a(.)x1 07(.)x1     PARTIAL
   0x0013  00(.)x3                             00(.)x4 af(.)x2 18(.)x1 05(.)x1 +2u  PARTIAL
   0x0014  ff(.)x3                             00(.)x3 ff(.)x3 ea(.)x2 2d(-)x1 +1u  PARTIAL
   0x0015  00(.)x3                             a3(.)x3 ff(.)x3 fe(.)x2 00(.)x2     PARTIAL
   0x0016  00(.)x3                             00(.)x4 ff(.)x3 78(x)x2 07(.)x1     PARTIAL
   0x0017  00(.)x3                             9a(.)x3 f8(.)x2 6c(l)x2 00(.)x2 +1u  PARTIAL
   0x0018  7f(.)x3                             ff(.)x3 00(.)x3 01(.)x2 af(.)x1 +1u  DIFFER
   0x001a  e2(.)x1 00(.)x1 80(.)x1             03(.)x3 80(.)x2 13(.)x1 ff(.)x1 +3u  PARTIAL
   0x001b  01(.)x2 ff(.)x1                     9e(.)x2 c2(.)x2 01(.)x1 ff(.)x1 +4u  PARTIAL
   0x001c  ff(.)x2 00(.)x1                     30(0)x2 01(.)x2 00(.)x2 ff(.)x2 +2u  PARTIAL
   0x001d  ff(.)x1 00(.)x1 48(H)x1             00(.)x3 5c(\)x2 ff(.)x2 06(.)x1 +2u  PARTIAL
   0x001e  00(.)x3                             ff(.)x3 78(x)x2 01(.)x2 00(.)x1 +2u  PARTIAL
   0x001f  b4(.)x3                             00(.)x4 30(0)x2 80(.)x2 40(@)x1 +1u  DIFFER
   0x0020  ff(.)x3                             00(.)x4 30(0)x2 c1(.)x2 ff(.)x1 +1u  PARTIAL
   0x0021  00(.)x3                             ff(.)x3 f8(.)x2 5c(\)x1 1a(.)x1 +3u  PARTIAL
   0x0022  00(.)x3                             ff(.)x3 53(S)x2 78(x)x1 1a(.)x1 +3u  PARTIAL
   0x0023  00(.)x3                             30(0)x2 fe(.)x2 60(`)x2 1a(.)x1 +3u  PARTIAL
   0x0024  00(.)x3                             f7(.)x2 68(h)x2 30(0)x1 1a(.)x1 +4u  PARTIAL
   0x0025  dd(.)x3                             c6(.)x2 10(.)x2 80(.)x1 1a(.)x1 +4u  DIFFER
   0x0026  ff(.)x3                             58(X)x2 0a(.)x2 78(x)x1 f8(.)x1 +4u  PARTIAL
   0x0027  00(.)x2 57(W)x1                     00(.)x4 ff(.)x3 30(0)x1 1a(.)x1 +1u  PARTIAL
   0x0028  e8(.)x2 92(.)x1                     00(.)x3 07(.)x3 30(0)x1 1a(.)x1 +2u  DIFFER
   0x0029  01(.)x2 80(.)x1                     29())x3 07(.)x2 3a(:)x1 00(.)x1 +1u  DIFFER
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
  prompts_b/openthread_13391.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 13391,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 13391 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 13391 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 13391 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).