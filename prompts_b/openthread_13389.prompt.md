==== BLOCKER ====
Target: openthread
Branch ID: 13389
Location: /src/openthread/src/core/thread/network_data.cpp:259:25
Enclosing function: ot::NetworkData::NetworkData::Iterate(unsigned int&, unsigned short, ot::NetworkData::NetworkData::Config&) const
Source line:                     if ((aRloc16 == Mac::kShortAddrBroadcast) || (server->GetServer16() == aRloc16))
Globally blocked side: T  (true branch)

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
  avg duration blocked: winner=2.70h  loser=21.30h
  avg hitcount on branch: winner=16  loser=2
  prob_div=0.80  dur_div=18.60h  hit_div=14
  subject-level: delta_AUC=11709180.0  p_AUC=0.0002  delta_Final=125.3  p_final=0.0007

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/openthread/13389/{W,L}/branch_coverage_show.txt

--- Enclosing function: ot::NetworkData::NetworkData::Iterate(unsigned int&, unsigned short, ot::NetworkData::NetworkData::Config&) const (/src/openthread/src/core/thread/network_data.cpp:132-276) ---
[ ]   130  
[ ]   131  Error NetworkData::Iterate(Iterator &aIterator, uint16_t aRloc16, Config &aConfig) const
[B]   132  {
[ ]   133      // Iterate to the next entry in Network Data matching `aRloc16`
[ ]   134      // (can be set to `Mac::kShortAddrBroadcast` to allow any RLOC).
[ ]   135      // The `aIterator` is used to track and save the current position.
[ ]   136      // On input, the non-`nullptr` pointer members in `aConfig` specify
[ ]   137      // the Network Data entry types (`mOnMeshPrefix`, `mExternalRoute`,
[ ]   138      // `mService`) to iterate over. On successful exit, the `aConfig`
[ ]   139      // is updated such that only one member pointer is not `nullptr`
[ ]   140      // indicating the type of entry and the non-`nullptr` config is
[ ]   141      // updated with the entry info.
[ ]   142  
[B]   143      Error               error = kErrorNotFound;
[B]   144      NetworkDataIterator iterator(aIterator);
[ ]   145  
[B]   146      for (const NetworkDataTlv *cur;
[B]   147           cur = iterator.GetTlv(mTlvs), (cur + 1 <= GetTlvsEnd()) && (cur->GetNext() <= GetTlvsEnd());
[B]   148           iterator.AdvanceTlv(mTlvs))
[B]   149      {
[B]   150          const NetworkDataTlv *subTlvs = nullptr;
[ ]   151  
[B]   152          switch (cur->GetType())
[B]   153          {
[ ]   154          case NetworkDataTlv::kTypePrefix:
[ ]   155              if ((aConfig.mOnMeshPrefix != nullptr) || (aConfig.mExternalRoute != nullptr))
[ ]   156              {
[ ]   157                  subTlvs = As<PrefixTlv>(cur)->GetSubTlvs();
[ ]   158              }
[ ]   159              break;
[B]   160          case NetworkDataTlv::kTypeService:
[B]   161              if (aConfig.mService != nullptr)
[B]   162              {
[B]   163                  subTlvs = As<ServiceTlv>(cur)->GetSubTlvs();
[B]   164              }
[B]   165              break;
[B]   166          default:
[B]   167              break;
[B]   168          }
[ ]   169  
[B]   170          if (subTlvs == nullptr)
[B]   171          {
[B]   172              continue;
[B]   173          }
[ ]   174  
[B]   175          for (const NetworkDataTlv *subCur; subCur = iterator.GetSubTlv(subTlvs),
[B]   176                                             (subCur + 1 <= cur->GetNext()) && (subCur->GetNext() <= cur->GetNext());
[B]   177               iterator.AdvaceSubTlv(subTlvs))
[B]   178          {
[B]   179              if (cur->GetType() == NetworkDataTlv::kTypePrefix)
[ ]   180              {
[ ]   181                  const PrefixTlv *prefixTlv = As<PrefixTlv>(cur);
[ ]   182  
[ ]   183                  switch (subCur->GetType())
[ ]   184                  {
[ ]   185                  case NetworkDataTlv::kTypeBorderRouter:
[ ]   186                  {
[ ]   187                      const BorderRouterTlv *borderRouter = As<BorderRouterTlv>(subCur);
[ ]   188  
[ ]   189                      if (aConfig.mOnMeshPrefix == nullptr)
[ ]   190                      {
[ ]   191                          continue;
[ ]   192                      }
[ ]   193  
[ ]   194                      for (uint8_t index; (index = iterator.GetAndAdvanceIndex()) < borderRouter->GetNumEntries();)
[ ]   195                      {
[ ]   196                          if (aRloc16 == Mac::kShortAddrBroadcast || borderRouter->GetEntry(index)->GetRloc() == aRloc16)
[ ]   197                          {
[ ]   198                              const BorderRouterEntry *borderRouterEntry = borderRouter->GetEntry(index);
[ ]   199  
[ ]   200                              aConfig.mExternalRoute = nullptr;
[ ]   201                              aConfig.mService       = nullptr;
[ ]   202                              aConfig.mOnMeshPrefix->SetFrom(*prefixTlv, *borderRouter, *borderRouterEntry);
[ ]   203  
[ ]   204                              ExitNow(error = kErrorNone);
[ ]   205                          }
[ ]   206                      }
[ ]   207  
[ ]   208                      break;
[ ]   209                  }
[ ]   210  
[ ]   211                  case NetworkDataTlv::kTypeHasRoute:
[ ]   212                  {
[ ]   213                      const HasRouteTlv *hasRoute = As<HasRouteTlv>(subCur);
[ ]   214  
[ ]   215                      if (aConfig.mExternalRoute == nullptr)
[ ]   216                      {
[ ]   217                          continue;
[ ]   218                      }
[ ]   219  
[ ]   220                      for (uint8_t index; (index = iterator.GetAndAdvanceIndex()) < hasRoute->GetNumEntries();)
[ ]   221                      {
[ ]   222                          if (aRloc16 == Mac::kShortAddrBroadcast || hasRoute->GetEntry(index)->GetRloc() == aRloc16)
[ ]   223                          {
[ ]   224                              const HasRouteEntry *hasRouteEntry = hasRoute->GetEntry(index);
[ ]   225  
[ ]   226                              aConfig.mOnMeshPrefix = nullptr;
[ ]   227                              aConfig.mService      = nullptr;
[ ]   228                              aConfig.mExternalRoute->SetFrom(GetInstance(), *prefixTlv, *hasRoute, *hasRouteEntry);
[ ]   229  
[ ]   230                              ExitNow(error = kErrorNone);
[ ]   231                          }
[ ]   232                      }
[ ]   233  
[ ]   234                      break;
[ ]   235                  }
[ ]   236  
[ ]   237                  default:
[ ]   238                      break;
[ ]   239                  }
[ ]   240              }
[B]   241              else // cur is `ServiceTLv`
[B]   242              {
[B]   243                  const ServiceTlv *service = As<ServiceTlv>(cur);
[ ]   244  
[B]   245                  if (aConfig.mService == nullptr)
[ ]   246                  {
[ ]   247                      continue;
[ ]   248                  }
[ ]   249  
[B]   250                  if (subCur->GetType() == NetworkDataTlv::kTypeServer)
[B]   251                  {
[B]   252                      const ServerTlv *server = As<ServerTlv>(subCur);
[ ]   253  
[B]   254                      if (!iterator.IsNewEntry())
[B]   255                      {
[B]   256                          continue;
[B]   257                      }
[ ]   258  
[B]   259                      if ((aRloc16 == Mac::kShortAddrBroadcast) || (server->GetServer16() == aRloc16)) <-- BLOCKER
[B]   260                      {
[B]   261                          aConfig.mOnMeshPrefix  = nullptr;
[B]   262                          aConfig.mExternalRoute = nullptr;
[B]   263                          aConfig.mService->SetFrom(*service, *server);
[ ]   264  
[B]   265                          iterator.MarkEntryAsNotNew();
[ ]   266  
[B]   267                          ExitNow(error = kErrorNone);
[B]   268                      }
[B]   269                  }
[B]   270              }
[B]   271          }
[B]   272      }
[ ]   273  
[B]   274  exit:
[B]   275      return error;
[B]   276  }

--- Caller (1 hop): ot::ChildTable::Iterate(ot::Neighbor::StateFilter) (/src/openthread/src/core/thread/child_table.hpp:250-250, calls ot::NetworkData::NetworkData::Iterate(unsigned int&, unsigned short, ot::NetworkData::NetworkData::Config&) const at line 250) (full body — short) ---
[B]   250      IteratorBuilder Iterate(Child::StateFilter aFilter) { return IteratorBuilder(GetInstance(), aFilter); } <-- CALL

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  ot::DataPollHandler::Clear()  (/src/openthread/src/core/mac/data_poll_handler.cpp:83-93, calls ot::NetworkData::NetworkData::Iterate(unsigned int&, unsigned short, ot::NetworkData::NetworkData::Config&) const at line 84)
hop 2  ot::DataPollHandler::ProcessPendingPolls()  (/src/openthread/src/core/mac/data_poll_handler.cpp:306-327, calls ot::NetworkData::NetworkData::Iterate(unsigned int&, unsigned short, ot::NetworkData::NetworkData::Config&) const at line 307)
hop 3  ot::Mac::ChannelMask::Clear()  (/src/openthread/src/core/mac/channel_mask.hpp:106-106, calls ot::DataPollHandler::Clear() at line 106)
hop 3  ot::DataPollHandler::HandleSentFrame(ot::Mac::TxFrame const&, otError)  (/src/openthread/src/core/mac/data_poll_handler.cpp:216-226, calls ot::DataPollHandler::ProcessPendingPolls() at line 225)
hop 3  ot::Mac::SubMac::Init()  (/src/openthread/src/core/mac/sub_mac.cpp:73-107, calls ot::DataPollHandler::Clear() at line 78)
hop 4  ot::Mac::Mac::HandleTransmitDone(ot::Mac::TxFrame&, ot::Mac::RxFrame*, otError)  (/src/openthread/src/core/mac/mac.cpp:1258-1452, calls ot::DataPollHandler::HandleSentFrame(ot::Mac::TxFrame const&, otError) at line 1404)
hop 4  ot::Mac::SubMac::SubMac(ot::Instance&)  (/src/openthread/src/core/mac/sub_mac.cpp:56-70, calls ot::Mac::SubMac::Init() at line 66)
hop 5  ot::Mac::SubMac::HandleTimer()  (/src/openthread/src/core/mac/sub_mac.cpp:769-800, calls ot::Mac::Mac::HandleTransmitDone(ot::Mac::TxFrame&, ot::Mac::RxFrame*, otError) at line 784)
hop 5  ot::Mac::SubMac::SignalFrameCounterUsed(unsigned int)  (/src/openthread/src/core/mac/sub_mac.cpp:951-967, calls ot::Mac::Mac::HandleTransmitDone(ot::Mac::TxFrame&, ot::Mac::RxFrame*, otError) at line 960)
hop 6  ot::Mac::SubMac::HandleReceiveDone(ot::Mac::RxFrame*, otError)  (/src/openthread/src/core/mac/sub_mac.cpp:280-317, calls ot::Mac::SubMac::SignalFrameCounterUsed(unsigned int) at line 288)
hop 6  ot::Mac::SubMac::ProcessTransmitSecurity()  (/src/openthread/src/core/mac/sub_mac.cpp:369-407, calls ot::Mac::SubMac::SignalFrameCounterUsed(unsigned int) at line 393)
hop 6  ot::MeshCoP::Dtls::HandleTimer(ot::Timer&)  (/src/openthread/src/core/meshcop/dtls.cpp:830-832, calls ot::Mac::SubMac::HandleTimer() at line 831)
hop 6  ot::MeshCoP::JoinerRouter::HandleTimer()  (/src/openthread/src/core/meshcop/joiner_router.cpp:234-234, calls ot::Mac::SubMac::HandleTimer() at line 234)
hop 7  ot::Mac::Mac::BeginTransmit()  (/src/openthread/src/core/mac/mac.cpp:920-1109, calls ot::Mac::SubMac::ProcessTransmitSecurity() at line 1055)
hop 7  ot::Mac::SubMac::Send()  (/src/openthread/src/core/mac/sub_mac.cpp:320-366, calls ot::Mac::SubMac::ProcessTransmitSecurity() at line 353)
hop 7  ot::MeshCoP::DatasetManager::HandleTimer()  (/src/openthread/src/core/meshcop/dataset_manager.cpp:241-241, calls ot::MeshCoP::JoinerRouter::HandleTimer() at line 241)
hop 7  otPlatRadioReceiveDone  (/src/openthread/src/core/radio/radio_platform.cpp:49-66, calls ot::Mac::SubMac::HandleReceiveDone(ot::Mac::RxFrame*, otError) at line 62)
hop 8  ot::Mac::LinkRaw::Transmit(void (*)(otInstance*, otRadioFrame*, otRadioFrame*, otError))  (/src/openthread/src/core/mac/link_raw.cpp:193-203, calls ot::Mac::SubMac::Send() at line 198)
hop 8  ot::Mac::SubMac::StartCsmaBackoff()  (/src/openthread/src/core/mac/sub_mac.cpp:410-454, calls ot::Mac::Mac::BeginTransmit() at line 429)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     183       567  ot::ChildTable::Iterator::Iterator(ot::Instance&)  (/src/openthread/src/core/thread/child_table.hpp:94-97)
     183       567  ot::ChildTable::Iterate(ot::Neighbor::StateFilter)  (/src/openthread/src/core/thread/child_table.hpp:250-250)
     183       567  ot::ChildTable::IteratorBuilder::IteratorBuilder(ot::Instance&, ot::Neighbor::StateFilter)  (/src/openthread/src/core/thread/child_table.hpp:330-333)
     183       567  ot::ChildTable::IteratorBuilder::begin()  (/src/openthread/src/core/thread/child_table.hpp:335-335)
     183       567  ot::ChildTable::IteratorBuilder::end()  (/src/openthread/src/core/thread/child_table.hpp:336-336)
      54       304  ot::ChildTable::FindChild(ot::Neighbor::AddressMatcher const&)  (/src/openthread/src/core/thread/child_table.hpp:342-342)
      72       253  ot::Utils::HistoryTracker::EntryList<otHistoryTrackerNetworkInfo, (unsigned short)32>::AddNewEntry()  (/src/openthread/src/core/utils/history_tracker.hpp:335-335)
      72       253  ot::Utils::HistoryTracker::EntryList<otHistoryTrackerMessageInfo, (unsigned short)32>::AddNewEntry()  (/src/openthread/src/core/utils/history_tracker.hpp:335-335)
      72       253  ot::Utils::HistoryTracker::EntryList<otHistoryTrackerNeighborInfo, (unsigned short)64>::AddNewEntry()  (/src/openthread/src/core/utils/history_tracker.hpp:335-335)
      72       253  ot::Utils::HistoryTracker::EntryList<otHistoryTrackerUnicastAddressInfo, (unsigned short)20>::AddNewEntry()  (/src/openthread/src/core/utils/history_tracker.hpp:335-335)
      72       253  ot::Utils::HistoryTracker::EntryList<otHistoryTrackerMulticastAddressInfo, (unsigned short)20>::AddNewEntry()  (/src/openthread/src/core/utils/history_tracker.hpp:335-335)
      72       253  ot::Utils::HistoryTracker::EntryList<otHistoryTrackerOnMeshPrefixInfo, (unsigned short)32>::AddNewEntry()  (/src/openthread/src/core/utils/history_tracker.hpp:335-335)
      72       253  ot::Utils::HistoryTracker::EntryList<otHistoryTrackerExternalRouteInfo, (unsigned short)32>::AddNewEntry()  (/src/openthread/src/core/utils/history_tracker.hpp:335-335)
      36       120  ot::NetworkData::NetworkData::GetNextOnMeshPrefix(unsigned int&, unsigned short, ot::NetworkData::OnMeshPrefixConfig&) const  (/src/openthread/src/core/thread/network_data.cpp:89-97)
      30       100  ot::NetworkData::NetworkData::GetNextOnMeshPrefix(unsigned int&, ot::NetworkData::OnMeshPrefixConfig&) const  (/src/openthread/src/core/thread/network_data.cpp:84-86)
... (44 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  ot::DataPollHandler::Clear()  (/src/openthread/src/core/mac/data_poll_handler.cpp:83-93) ---
  d=2   L  84  T=0 F=3  T=0 F=10  for (Child &child : Get<ChildTable>().Iterate(Child::kInS...
--- d=1  ot::NetworkData::NetworkData::Iterate(unsigned int&, unsigned short, ot::NetworkData::NetworkData::Config&) const  (/src/openthread/src/core/thread/network_data.cpp:132-276) ---
  d=1   L 147  T=132 F=84  T=290 F=230  cur = iterator.GetTlv(mTlvs), (cur + 1 <= GetTlvsEnd()) &...
  d=1   L 147  T=132 F=84  T=290 F=230  cur = iterator.GetTlv(mTlvs), (cur + 1 <= GetTlvsEnd()) &...
  d=1   L 147  T=132 F=0  T=290 F=0  cur = iterator.GetTlv(mTlvs), (cur + 1 <= GetTlvsEnd()) &...
  d=1   L 154  T=0 F=132  T=0 F=290  case NetworkDataTlv::kTypePrefix:
  d=1   L 160  T=57 F=75  T=90 F=200  case NetworkDataTlv::kTypeService:
  d=1   L 166  T=75 F=57  T=200 F=90  default:
  d=1   L 170  T=93 F=39  T=260 F=30  if (subTlvs == nullptr)
  d=1   L 259  T=6 F=0  T=20 F=0  if ((aRloc16 == Mac::kShortAddrBroadcast) || (server->Get...  <-- BLOCKER
  d=1   L 259  T=15 F=6  T=0 F=20  if ((aRloc16 == Mac::kShortAddrBroadcast) || (server->Get...  <-- BLOCKER

[off-chain: 35 additional divergent branches across 15 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=29c3bac95a89ef85, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=287s, mutation_op=ByteRandMutator,BytesInsertMutator,DwordInterestingMutator,CrossoverReplaceMutator):
  0000: 78 66 10 00 00 00 10 00 7f 00 b0 00 ff ff ff fc   xf..............
  0010: 00 a0 07 02 2d a3 07 07 af fd de ad 00 be ef 00   ....-...........
  0020: 00 00 00 00 ff fe 00 fc 19 07 00 6d 04 40 7f 20   ...........m.@. 
  0030: 00 ff 09 00 fe 80 78 30 30                        ......x00
Seed 2 (id=5b356d105fc8479e, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=1670s, mutation_op=CrossoverReplaceMutator,ByteRandMutator):
  0000: 80 66 ff 0d 01 00 10 00 7f 0a b0 00 ff e3 14 14   .f..............
  0010: 10 00 14 14 14 15 14 14 ec fd de ad 00 be ef 00   ................
  0020: 00 00 00 00 ff fe 00 fc 28 00 00 6d 02 40 ff 6d   ........(..m.@.m
  0030: 00 7f 00 6d 04 40 78 a1 30                        ...m.@x.0
Seed 3 (id=0d6f85bfb5f3cd14, size=161 bytes, fuzzer=cmplog, trial=1, discovered_at=19790s, mutation_op=QwordAddMutator):
  0000: 77 67 10 01 00 00 78 00 ff fe 00 ff b3 ff ff fe   wg....x.........
  0010: ff 00 01 ff ff ff ff 9a 5c fd de ad 00 be ef 00   ........\.......
  0020: 00 00 00 00 ff fe 00 fc 17 00 0b 6d 00 6d 00 6d   ...........m.m.m
  0030: 02 40 00 6d 00 6d 02 40 08 6d 4d 72 76 66 ff 0d   .@.m.m.@.mMrvf..

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
   0x0000  78(x)x1 80(.)x1 77(w)x1             db(.)x8 dc(.)x1 96(.)x1             DIFFER
   0x0001  66(f)x2 67(g)x1                     62(b)x10                            DIFFER
   0x0002  10(.)x2 ff(.)x1                     5c(\)x9 6f(o)x1                     DIFFER
   0x0003  00(.)x1 0d(.)x1 01(.)x1             00(.)x9 01(.)x1                     PARTIAL
   0x0004  00(.)x2 01(.)x1                     00(.)x10                            PARTIAL
   0x0006  10(.)x2 78(x)x1                     ff(.)x9 6f(o)x1                     DIFFER
   0x0007  00(.)x3                             00(.)x9 fe(.)x1                     PARTIAL
   0x0008  7f(.)x2 ff(.)x1                     64(d)x9 ff(.)x1                     PARTIAL
   0x0009  00(.)x1 0a(.)x1 fe(.)x1             78(x)x8 68(h)x2                     DIFFER
   0x000a  b0(.)x2 00(.)x1                     44(D)x7 00(.)x2 30(0)x1             PARTIAL
   0x000b  00(.)x2 ff(.)x1                     44(D)x7 dd(.)x2 30(0)x1             DIFFER
   0x000c  ff(.)x2 b3(.)x1                     44(D)x7 6d(m)x2 33(3)x1             DIFFER
   0x000d  ff(.)x2 e3(.)x1                     44(D)x7 00(.)x2 62(b)x1             DIFFER
   0x000e  ff(.)x2 14(.)x1                     44(D)x7 30(0)x2 5c(\)x1             DIFFER
   0x000f  fc(.)x1 14(.)x1 fe(.)x1             44(D)x7 30(0)x2 00(.)x1             DIFFER
   0x0010  00(.)x1 10(.)x1 ff(.)x1             44(D)x6 33(3)x2 c1(.)x1 53(S)x1     DIFFER
   0x0011  00(.)x2 a0(.)x1                     44(D)x6 00(.)x1 62(b)x1 9d(.)x1 +1u  PARTIAL
   0x0012  07(.)x1 14(.)x1 01(.)x1             44(D)x7 5c(\)x2 00(.)x1             DIFFER
   0x0013  02(.)x1 14(.)x1 ff(.)x1             44(D)x7 00(.)x1 ee(.)x1 30(0)x1     DIFFER
   0x0014  2d(-)x1 14(.)x1 ff(.)x1             44(D)x5 ff(.)x3 fc(.)x1 30(0)x1     PARTIAL
   0x0015  a3(.)x1 15(.)x1 ff(.)x1             44(D)x5 ff(.)x3 00(.)x1 30(0)x1     PARTIAL
   0x0016  07(.)x1 14(.)x1 ff(.)x1             30(0)x6 ff(.)x4                     PARTIAL
   0x0017  07(.)x1 14(.)x1 9a(.)x1             ff(.)x4 30(0)x4 fe(.)x1 00(.)x1     DIFFER
   0x0018  af(.)x1 ec(.)x1 5c(\)x1             ff(.)x3 01(.)x3 fe(.)x2 9e(.)x1 +1u  DIFFER
   0x0019  fd(.)x3                             ff(.)x5 fe(.)x4 fd(.)x1             PARTIAL
   0x001a  de(.)x3                             b4(.)x4 e3(.)x2 03(.)x1 ff(.)x1 +2u  PARTIAL
   0x001b  ad(.)x3                             ff(.)x3 30(0)x2 25(%)x2 5d(])x1 +2u  PARTIAL
   0x001c  00(.)x3                             00(.)x3 30(0)x2 ef(.)x2 78(x)x1 +2u  PARTIAL
   0x001d  be(.)x3                             30(0)x3 00(.)x2 ff(.)x2 da(.)x1 +2u  PARTIAL
   0x001e  ef(.)x3                             00(.)x4 30(0)x3 da(.)x1 ef(.)x1 +1u  PARTIAL
   0x001f  00(.)x3                             30(0)x4 00(.)x3 b4(.)x2 ff(.)x1     PARTIAL
   0x0020  00(.)x3                             30(0)x2 00(.)x2 ff(.)x2 80(.)x1 +3u  PARTIAL
   0x0021  00(.)x3                             34(4)x6 00(.)x3 30(0)x1             PARTIAL
   0x0022  00(.)x3                             34(4)x5 00(.)x2 30(0)x1 79(y)x1 +1u  PARTIAL
   0x0023  00(.)x3                             34(4)x5 78(x)x2 1c(.)x2 5c(\)x1     DIFFER
   0x0024  ff(.)x3                             34(4)x7 30(0)x2 76(v)x1             DIFFER
   0x0025  fe(.)x3                             34(4)x7 08(.)x2 30(0)x1             DIFFER
   0x0026  00(.)x3                             34(4)x5 08(.)x2 30(0)x1 33(3)x1 +1u  DIFFER
   0x0027  fc(.)x3                             34(4)x7 08(.)x2 5c(\)x1             DIFFER
   0x0028  19(.)x1 28(()x1 17(.)x1             00(.)x7 08(.)x2 78(x)x1             DIFFER
   ... (23 more divergent offsets)
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
  prompts_b/openthread_13389.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 13389,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 13389 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 13389 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 13389 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).