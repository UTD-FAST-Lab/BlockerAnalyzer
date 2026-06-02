==== BLOCKER ====
Target: openthread
Branch ID: 13302
Location: /src/openthread/src/core/common/linked_list.hpp:472:17
Enclosing function: ot::AddressResolver::CacheEntry const* ot::LinkedList<ot::AddressResolver::CacheEntry>::FindMatching<ot::Ip6::Address>(ot::AddressResolver::CacheEntry const*, ot::AddressResolver::CacheEntry const*, ot::Ip6::Address const&, ot::AddressResolver::CacheEntry const*&) const
Source line:             if (entry->Matches(aIndicator))
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            9        1          0  winner (I2S vs cmplog)
cmplog                           2        8          0  loser (I2S vs naive)
value_profile                    8        2          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             2        8          0  loser (I2S vs value_profile)
naive_ctx                       10        0          0  REFERENCE
naive_ngram4                    10        0          0  REFERENCE
mopt                            10        0          0  REFERENCE
minimizer                        5        5          0  REFERENCE
fast                             7        3          0  REFERENCE
grimoire                         3        7          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=2.30h  loser=19.20h
  avg hitcount on branch: winner=1140  loser=0
  prob_div=0.70  dur_div=16.90h  hit_div=1140
  subject-level: delta_AUC=11709180.0  p_AUC=0.0002  delta_Final=125.3  p_final=0.0007
--- Pair 2: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 24  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=4.70h  loser=19.20h
  avg hitcount on branch: winner=0  loser=0
  prob_div=0.60  dur_div=14.50h  hit_div=0
  subject-level: delta_AUC=8206200.0  p_AUC=0.0006  delta_Final=65.8  p_final=0.0884

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/openthread/13302/{W,L}/branch_coverage_show.txt

--- Enclosing function: ot::AddressResolver::CacheEntry const* ot::LinkedList<ot::AddressResolver::CacheEntry>::FindMatching<ot::Ip6::Address>(ot::AddressResolver::CacheEntry const*, ot::AddressResolver::CacheEntry const*, ot::Ip6::Address const&, ot::AddressResolver::CacheEntry const*&) const (/src/openthread/src/core/common/linked_list.hpp:465-479) ---
[ ]   463                               const Indicator &aIndicator,
[ ]   464                               const Type     *&aPrevEntry) const
[B]   465      {
[B]   466          const Type *entry;
[ ]   467  
[B]   468          aPrevEntry = nullptr;
[ ]   469  
[B]   470          for (entry = aBegin; entry != aEnd; aPrevEntry = entry, entry = entry->GetNext())
[B]   471          {
[B]   472              if (entry->Matches(aIndicator)) <-- BLOCKER
[B]   473              {
[B]   474                  break;
[B]   475              }
[B]   476          }
[ ]   477  
[B]   478          return entry;
[B]   479      }

--- Caller (1 hop): ot::RouterTable::FindRouter(ot::Neighbor::AddressMatcher const&) const (/src/openthread/src/core/thread/router_table.cpp:249-251, calls ot::AddressResolver::CacheEntry const* ot::LinkedList<ot::AddressResolver::CacheEntry>::FindMatching<ot::Ip6::Address>(ot::AddressResolver::CacheEntry const*, ot::AddressResolver::CacheEntry const*, ot::Ip6::Address const&, ot::AddressResolver::CacheEntry const*&) const at line 250) (full body — short) ---
[B]   249  {
[B]   250      return mRouters.FindMatching(aMatcher); <-- CALL
[B]   251  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  ot::Srp::Server::AddHost(ot::Srp::Server::Host&)  (/src/openthread/src/core/net/srp_server.cpp:313-318, calls ot::AddressResolver::CacheEntry const* ot::LinkedList<ot::AddressResolver::CacheEntry>::FindMatching<ot::Ip6::Address>(ot::AddressResolver::CacheEntry const*, ot::AddressResolver::CacheEntry const*, ot::Ip6::Address const&, ot::AddressResolver::CacheEntry const*&) const at line 316)
hop 2  ot::Srp::Server::HasNameConflictsWith(ot::Srp::Server::Host&) const  (/src/openthread/src/core/net/srp_server.cpp:360-389, calls ot::AddressResolver::CacheEntry const* ot::LinkedList<ot::AddressResolver::CacheEntry>::FindMatching<ot::Ip6::Address>(ot::AddressResolver::CacheEntry const*, ot::AddressResolver::CacheEntry const*, ot::Ip6::Address const&, ot::AddressResolver::CacheEntry const*&) const at line 362)
hop 3  ot::Srp::Server::CommitSrpUpdate(otError, ot::Srp::Server::Host&, ot::Dns::UpdateHeader const&, ot::Ip6::MessageInfo const*, ot::Srp::Server::TtlConfig const&, ot::Srp::Server::LeaseConfig const&)  (/src/openthread/src/core/net/srp_server.cpp:443-538, calls ot::Srp::Server::AddHost(ot::Srp::Server::Host&) at line 497)
hop 3  ot::Srp::Server::ProcessUpdateSection(ot::Srp::Server::Host&, ot::Message const&, ot::Srp::Server::MessageMetadata&) const  (/src/openthread/src/core/net/srp_server.cpp:794-821, calls ot::Srp::Server::HasNameConflictsWith(ot::Srp::Server::Host&) const at line 812)
hop 4  ot::Srp::Server::CommitSrpUpdate(otError, ot::Srp::Server::Host&, ot::Srp::Server::MessageMetadata const&)  (/src/openthread/src/core/net/srp_server.cpp:425-428, calls ot::Srp::Server::CommitSrpUpdate(otError, ot::Srp::Server::Host&, ot::Dns::UpdateHeader const&, ot::Ip6::MessageInfo const*, ot::Srp::Server::TtlConfig const&, ot::Srp::Server::LeaseConfig const&) at line 426)
hop 4  ot::Srp::Server::HandleServiceUpdateResult(ot::Srp::Server::UpdateMetadata*, otError)  (/src/openthread/src/core/net/srp_server.cpp:406-422, calls ot::Srp::Server::CommitSrpUpdate(otError, ot::Srp::Server::Host&, ot::Dns::UpdateHeader const&, ot::Ip6::MessageInfo const*, ot::Srp::Server::TtlConfig const&, ot::Srp::Server::LeaseConfig const&) at line 411)
hop 4  ot::Srp::Server::ProcessDnsUpdate(ot::Message&, ot::Srp::Server::MessageMetadata&)  (/src/openthread/src/core/net/srp_server.cpp:718-765, calls ot::Srp::Server::ProcessUpdateSection(ot::Srp::Server::Host&, ot::Message const&, ot::Srp::Server::MessageMetadata&) const at line 743)
hop 5  otSrpServerHandleServiceUpdateResult  (/src/openthread/src/core/api/srp_server_api.cpp:124-126, calls ot::Srp::Server::HandleServiceUpdateResult(ot::Srp::Server::UpdateMetadata*, otError) at line 125)
hop 5  ot::Srp::Server::CommitSrpUpdate(otError, ot::Srp::Server::UpdateMetadata&)  (/src/openthread/src/core/net/srp_server.cpp:431-435, calls ot::Srp::Server::CommitSrpUpdate(otError, ot::Srp::Server::Host&, ot::Srp::Server::MessageMetadata const&) at line 432)
hop 5  ot::Srp::Server::HandleServiceUpdateResult(unsigned int, otError)  (/src/openthread/src/core/net/srp_server.cpp:392-403, calls ot::Srp::Server::HandleServiceUpdateResult(ot::Srp::Server::UpdateMetadata*, otError) at line 397)
hop 5  ot::Srp::Server::ProcessMessage(ot::Message&, ot::Time, ot::Srp::Server::TtlConfig const&, ot::Srp::Server::LeaseConfig const&, ot::Ip6::MessageInfo const*)  (/src/openthread/src/core/net/srp_server.cpp:1503-1523, calls ot::Srp::Server::ProcessDnsUpdate(ot::Message&, ot::Srp::Server::MessageMetadata&) at line 1519)
hop 6  ot::Srp::Server::HandleOutstandingUpdatesTimer()  (/src/openthread/src/core/net/srp_server.cpp:1640-1646, calls ot::Srp::Server::HandleServiceUpdateResult(unsigned int, otError) at line 1644)
hop 6  ot::Srp::Server::HandleUdpReceive(ot::Message&, ot::Ip6::MessageInfo const&)  (/src/openthread/src/core/net/srp_server.cpp:1484-1491, calls ot::Srp::Server::ProcessMessage(ot::Message&, ot::Time, ot::Srp::Server::TtlConfig const&, ot::Srp::Server::LeaseConfig const&, ot::Ip6::MessageInfo const*) at line 1485)
hop 6  ot::Srp::Server::ProcessMessage(ot::Message&, ot::Ip6::MessageInfo const&)  (/src/openthread/src/core/net/srp_server.cpp:1494-1496, calls ot::Srp::Server::ProcessMessage(ot::Message&, ot::Time, ot::Srp::Server::TtlConfig const&, ot::Srp::Server::LeaseConfig const&, ot::Ip6::MessageInfo const*) at line 1495)
hop 7  ot::MeshCoP::Dtls::HandleUdpReceive(void*, otMessage*, otMessageInfo const*)  (/src/openthread/src/core/meshcop/dtls.cpp:169-171, calls ot::Srp::Server::HandleUdpReceive(ot::Message&, ot::Ip6::MessageInfo const&) at line 170)
hop 7  ot::MeshCoP::JoinerRouter::HandleUdpReceive(void*, otMessage*, otMessageInfo const*)  (/src/openthread/src/core/meshcop/joiner_router.cpp:126-128, calls ot::Srp::Server::HandleUdpReceive(ot::Message&, ot::Ip6::MessageInfo const&) at line 127)
hop 8  void ot::MeshCoP::Commissioner::HandleTmf<(ot::Uri)28>(ot::Coap::Message&, ot::Ip6::MessageInfo const&)  (/src/openthread/src/core/meshcop/commissioner.cpp:943-1003, calls ot::MeshCoP::JoinerRouter::HandleUdpReceive(void*, otMessage*, otMessageInfo const*) at line 999)

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
[no branches with W/L direction or count divergence in the cov dump — execution split is at the blocker itself, or in code outside the dumped files]


==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=00123255f0c0a666, size=296 bytes, fuzzer=naive, trial=1, discovered_at=58s, mutation_op=BytesSetMutator,ByteInterestingMutator):
  0000: dc 62 5c 00 00 00 ff fe ff 78 30 30 33 62 5c 00   .b\......x003b\.
  0010: c1 00 00 00 fc 00 ff fe ff ff 03 5d 78 30 30 ff   ...........]x00.
  0020: 80 30 30 5c 76 30 30 5c 78 30 40 5c 78 30 30 5c   .00\v00\x0@\x00\
  0030: 78 30 30 5c 78 30 31 5c 78 9a 65 5c 78 38 30 5c   x00\x01\x.e\x80\
Seed 2 (id=00901525a2acfd44, size=41 bytes, fuzzer=value_profile, trial=2, discovered_at=96s, mutation_op=TokenReplace):
  0000: 93 6c 6c 94 00 00 00 00 00 5c 00 80 ff ff 10 00   .ll......\......
  0010: 64 30 5c 78 30 df ff ff ff fd de 93 04 00 30 30   d0\x0.........00
  0020: 30 30 30 30 ff f1 7b 36 30                        0000..{60
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
Seed 5 (id=00acdf46cf74675d, size=57 bytes, fuzzer=value_profile, trial=2, discovered_at=2762s, mutation_op=BytesCopyMutator):
  0000: 93 6c 95 6c 5b 00 10 00 e6 00 ff dc 6d 61 00 17   .l.l[.......ma..
  0010: 00 1c fd 00 ff ff ff ff ff ff f3 00 e8 6d 00 00   .............m..
  0020: 78 4f df 48 45 5c 5c 7e aa 83 01 00 6d 00 6d 00   xO.HE\\~....m.m.
  0030: 6d 00 6d 01 7d 10 00 6d 00                        m.m.}..m.

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=004413684432e458, size=92 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=0s, mutation_op=BytesDeleteMutator,BytesSetMutator,BytesSwapMutator,BytesRandSetMutator,BytesDeleteMutator):
  0000: f5 f5 f5 38 30 5c 78 30 30 5c 78 30 30 5c 78 30   ...80\x00\x00\x0
  0010: 30 5c 78 78 30 30 5c 78 30 30 5c 78 30 30 5c 78   0\xx00\x00\x00\x
  0020: c9 30 5c 78 30 30 5c 78 30 30 5c 78 36 30 5c 78   .0\x00\x00\x60\x
  0030: 30 30 5c 78 30 30 5c 78 30 30 5c 78 5c 5c 5c 5c   00\x00\x00\x\\\\
Seed 2 (id=006c5730c281e21c, size=160 bytes, fuzzer=cmplog, trial=1, discovered_at=0s):
  0000: 5c 78 36 30 5c 78 30 30 5c 78 30 30 5c 78 54 30   \x60\x00\x00\xT0
  0010: 5c 78 30 30 5c 78 30 30 5c 78 33 62 5c 78 34 30   \x00\x00\x3b\x40
  0020: 5c 78 66 ff 5c 78 38 30 5c 78 30 30 5c 78 30 30   \xf.\x80\x00\x00
  0030: 5c 78 30 30 5c 78 30 30 5c 78 30 30 5c 78 30 30   \x00\x00\x00\x00
Seed 3 (id=0096c8a9856dd0ab, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=101s, mutation_op=CrossoverInsertMutator,DwordAddMutator):
  0000: 78 66 10 01 00 00 00 29 01 00 00 00 00 00 00 00   xf.....)........
  0010: 00 00 00 00 00 a3 78 f8 ff ff 13 01 30 5c 78 30   ......x.....0\x0
  0020: 30 5c 78 30 30 80 78 30 30                        0\x00.x00
Seed 4 (id=0063b6c0f181163b, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=278s, mutation_op=ByteInterestingMutator):
  0000: 78 60 10 ff 01 00 00 29 ff 00 00 00 00 00 00 a0   x`.....)........
  0010: 2c fe 00 18 00 a3 78 f8 ff ff ff ff 30 5c 78 30   ,.....x.....0\x0
  0020: 30 1a 1a 1a 1a 1a f8 1a 1a                        0........
Seed 5 (id=008f597635438ba4, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=725s, mutation_op=CrossoverInsertMutator,DwordInterestingMutator):
  0000: 78 66 10 7f 01 00 10 00 7f 00 b0 00 ff ff ff fc   xf..............
  0010: 03 a0 1a 05 2d a3 07 09 af ff 03 03 07 00 00 40   ....-..........@
  0020: ff ff ff 07 ff af 2c ff 0d 3a 00 6d 02 40 7f 6d   ......,..:.m.@.m
  0030: 00 04 ff ff fe 06 78 30 30                        ......x00


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0001  62(b)x10 65(e)x6 6c(l)x3 63(c)x1    6c(l)x8 66(f)x6 67(g)x2 f5(.)x1 +3u  PARTIAL
   0x0004  00(.)x16 1d(.)x2 5b([)x1 6c(l)x1    00(.)x8 01(.)x2 45(E)x2 ff(.)x2 +6u  PARTIAL
   0x0005  00(.)x20                            00(.)x10 02(.)x6 01(.)x2 5c(\)x1 +1u  PARTIAL
   0x0007  00(.)x19 fe(.)x1                    00(.)x12 29())x5 30(0)x2 2c(,)x1    PARTIAL
   0x0016  ff(.)x7 30(0)x6 00(.)x5 41(A)x2     30(0)x4 00(.)x4 07(.)x3 f4(.)x3 +4u  PARTIAL
   0x0019  ff(.)x10 fe(.)x6 fd(.)x4            ff(.)x12 fd(.)x6 30(0)x1 78(x)x1    PARTIAL
   0x0029  00(.)x14 29())x3 30(0)x1 83(.)x1    00(.)x4 11(.)x4 30(0)x3 29())x2 +5u  PARTIAL
   0x002a  01(.)x10 00(.)x7 40(@)x1 08(.)x1    00(.)x6 5c(\)x3 01(.)x3 0b(.)x3 +3u  PARTIAL
   0x002e  00(.)x11 20( )x5 6d(m)x2 30(0)x1    00(.)x3 18(.)x3 07(.)x2 78(x)x2 +7u  PARTIAL
   0x003e  00(.)x8 30(0)x4 20( )x4 33(3)x1     30(0)x3 00(.)x3 78(x)x3 ff(.)x2 +2u  PARTIAL
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
  prompts_b/openthread_13302.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 13302,
  "target": "openthread",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S), value_profile>value_profile_cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 13302 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 13302 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 13302 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).