==== BLOCKER ====
Target: curl
Branch ID: 399
Location: /src/curl/lib/strcase.c:126:30
Enclosing function: Curl_strncasecompare
Source line:   while(*first && *second && max) {
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=4.50h  loser=24.00h
  avg hitcount on branch: winner=66  loser=0
  prob_div=1.00  dur_div=19.50h  hit_div=66
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.40h  loser=24.00h
  avg hitcount on branch: winner=76  loser=0
  prob_div=1.00  dur_div=20.60h  hit_div=76
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/399/{W,L}/branch_coverage_show.txt

--- Enclosing function: Curl_strncasecompare (/src/curl/lib/strcase.c:125-138) ---
[ ]   123   */
[ ]   124  int Curl_strncasecompare(const char *first, const char *second, size_t max)
[B]   125  {
[B]   126    while(*first && *second && max) { <-- BLOCKER
[B]   127      if(Curl_raw_toupper(*first) != Curl_raw_toupper(*second)) {
[B]   128        break;
[B]   129      }
[B]   130      max--;
[B]   131      first++;
[B]   132      second++;
[B]   133    }
[B]   134    if(0 == max)
[B]   135      return 1; /* they are equal this far */
[ ]   136  
[B]   137    return Curl_raw_toupper(*first) == Curl_raw_toupper(*second);
[B]   138  }

--- Caller (1 hop): curl_strnequal (/src/curl/lib/strcase.c:209-211, calls Curl_strncasecompare at line 210) (full body — short) ---
[B]   209  {
[B]   210    return Curl_strncasecompare(first, second, max); <-- CALL
[B]   211  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  Curl_hsts_parse  (/src/curl/lib/hsts.c:144-240, calls Curl_strncasecompare at line 161)
hop 2  openssl.c:ossl_version  (/src/curl/lib/vtls/openssl.c:4360-4433, calls Curl_strncasecompare at line 4367)
hop 3  Curl_http_header  (/src/curl/lib/http.c:3451-3765, calls Curl_hsts_parse at line 3727)
hop 3  openssl.c:ossl_send  (/src/curl/lib/vtls/openssl.c:4189-4266, calls openssl.c:ossl_version at line 4249)
hop 4  Curl_http_readwrite_headers  (/src/curl/lib/http.c:3904-4466, calls Curl_http_header at line 4434)
hop 5  transfer.c:readwrite_data  (/src/curl/lib/transfer.c:520-878, calls Curl_http_readwrite_headers at line 633)
hop 6  Curl_readwrite  (/src/curl/lib/transfer.c:1167-1340, calls transfer.c:readwrite_data at line 1219)
hop 7  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661, calls Curl_readwrite at line 2405)
hop 8  curl_multi_perform  (/src/curl/lib/multi.c:2665-2716, calls multi.c:multi_runsingle at line 2683)
hop 8  multi.c:multi_socket  (/src/curl/lib/multi.c:3101-3208, calls multi.c:multi_runsingle at line 3158)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
    6640      1940  Curl_raw_toupper  (/src/curl/lib/strcase.c:73-75)
    1040       209  Curl_strncasecompare  (/src/curl/lib/strcase.c:125-138)  <-- enclosing
     460        91  curl_strnequal  (/src/curl/lib/strcase.c:209-211)
       2         0  openssl.c:ossl_seed  (/src/curl/lib/vtls/openssl.c:807-883)
       2         0  openssl.c:ossl_random  (/src/curl/lib/vtls/openssl.c:4438-4451)
       1         0  openssl.c:rand_enough  (/src/curl/lib/vtls/openssl.c:802-804)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  Curl_strncasecompare  (/src/curl/lib/strcase.c:125-138) ---
  d=1   L 126  T=2140 F=101  T=551 F=72  while(*first && *second && max) {  <-- BLOCKER
  d=1   L 126  T=2240 F=129  T=623 F=59  while(*first && *second && max) {  <-- BLOCKER
  d=1   L 126  T=2120 F=25  T=551 F=0  while(*first && *second && max) {  <-- BLOCKER
  d=1   L 127  T=792 F=1320  T=78 F=473  if(Curl_raw_toupper(*first) != Curl_raw_toupper(*second)) {
  d=1   L 134  T=247 F=800  T=131 F=78  if(0 == max)

[off-chain: 11 additional divergent branches across 5 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=095209cade8bf193, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=8093s, mutation_op=CrossoverReplaceMutator,WordInterestingMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 4b 2f 3a 3a 00 10   ......pop3K/::..
  0010: 3a 3a 3a 3a 3a 3a 3a 39 30 30 31 ad 38 35 30 00   :::::::9001.850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 40 6c 25   ....GHTTP/ me@l%
  0030: 6d 65 54 68 65 72 65 0d 0a 54 72 61 6e 73 66 65   meThere..Transfe
Seed 2 (id=017423e94c217ba2, size=113 bytes, fuzzer=cmplog, trial=1, discovered_at=8397s, mutation_op=BytesInsertCopyMutator,ByteFlipMutator,ByteDecMutator,ByteIncMutator,BitFlipMutator,BytesDeleteMutator,ByteInterestingMutator):
  0000: 00 01 00 00 00 19 70 6f 70 00 3a 25 2f 31 32 00   ......pop.:%/12.
  0010: 00 30 7f 28 2e 00 00 04 9c 30 31 72 38 35 30 00   .0.(.....01r850.
  0020: 02 00 00 00 48 48 54 54 50 2f 23 6d 65 61 06 24   ....HHTTP/#mea.$
  0030: 65 2c 8e 65 74 72 87 09 0a 54 72 61 6e 53 66 65   e,.etr...TranSfe
Seed 3 (id=1d9d678b6253009f, size=114 bytes, fuzzer=cmplog, trial=1, discovered_at=8401s, mutation_op=ByteAddMutator,ByteNegMutator):
  0000: 00 01 00 00 00 19 70 6f 70 00 3a 2f 2f 31 32 00   ......pop.://12.
  0010: 00 30 28 28 2e 00 3a 39 64 30 31 72 38 35 30 00   .0((..:9d01r850.
  0020: 02 00 00 00 48 48 54 54 50 2f 23 6d 65 61 06 24   ....HHTTP/#mea.$
  0030: 65 63 8e 65 74 72 87 09 0a 54 72 61 6e 53 66 65   ec.etr...TranSfe
Seed 4 (id=054a689b9dd21854, size=114 bytes, fuzzer=cmplog, trial=1, discovered_at=8473s, mutation_op=BytesDeleteMutator,ByteAddMutator,ByteIncMutator,BytesInsertMutator):
  0000: 00 01 00 00 00 19 70 70 70 00 3a 2f 2f 80 32 00   ......ppp.://.2.
  0010: 00 30 28 28 2e 00 3a 39 9c 30 31 72 00 02 30 00   .0((..:9.01r..0.
  0020: 02 00 00 00 48 48 54 54 50 2f 23 6d 65 56 06 24   ....HHTTP/#meV.$
  0030: 65 63 8e 65 74 72 44 17 0a 54 72 61 6e 53 66 65   ec.etrD..TranSfe
Seed 5 (id=0429edfc621de054, size=114 bytes, fuzzer=cmplog, trial=1, discovered_at=8485s, mutation_op=ByteIncMutator,BytesCopyMutator,ByteInterestingMutator,BitFlipMutator,BytesDeleteMutator,ByteDecMutator,BytesInsertCopyMutator):
  0000: 00 01 00 00 00 19 70 6f 70 00 3a 2f 2e 00 32 ad   ......pop.:/..2.
  0010: db 30 28 28 00 07 3a 39 9c 30 31 72 38 35 30 00   .0((..:9.01r850.
  0020: 02 00 00 00 48 48 54 54 50 2f 23 6d 65 61 06 24   ....HHTTP/#mea.$
  0030: 65 63 8e 65 74 72 87 09 0a 54 72 61 6e 53 66 65   ec.etr...TranSfe

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=00182ecc311b5f0b, size=32 bytes, fuzzer=naive, trial=1, discovered_at=3s, mutation_op=BitFlipMutator,BytesRandSetMutator,ByteDecMutator,ByteDecMutator,QwordAddMutator,ByteAddMutator):
  0000: 00 01 00 00 00 19 70 6b 2b 2b 2b 2b 2b 2a 2b 2b   ......pk+++++*++
  0010: 2b 2b 4b 2b 1f 1f 1e 1f 1f 40 2f 2f 2f 14 00 00   ++K+.....@///...
Seed 2 (id=0024e5972fc0b2e0, size=35 bytes, fuzzer=naive, trial=1, discovered_at=88s, mutation_op=WordAddMutator):
  0000: 00 01 00 00 00 19 25 60 25 61 3e 66 9f 9f 63 25   ......%`%a>f..c%
  0010: 2b 5d 25 41 bf 41 41 41 41 40 41 41 5a 70 65 72   +]%A.AAAA@AAZper
  0020: 6d 69 74                                          mit
Seed 3 (id=00225bc4819174d2, size=73 bytes, fuzzer=value_profile, trial=1, discovered_at=152s, mutation_op=BytesInsertMutator,ByteAddMutator,ByteIncMutator,BytesDeleteMutator,ByteDecMutator):
  0000: 00 01 00 00 00 43 64 55 43 25 25 25 25 21 25 65   .....CdUC%%%%!%e
  0010: 26 25 65 24 25 64 45 72 46 25 41 27 25 31 25 25   &%e$%dErF%A'%1%%
  0020: 65 25 44 d6 42 64 45 72 33 25 65 4b 25 43 25 25   e%D.BdEr3%eK%C%%
  0030: 25 25 25 25 25 25 25 25 25 25 25 25 26 25 40 e8   %%%%%%%%%%%%&%@.
Seed 4 (id=00078b9eb464eef9, size=33 bytes, fuzzer=naive, trial=1, discovered_at=190s, mutation_op=ByteDecMutator,ByteFlipMutator):
  0000: 00 01 00 00 00 19 2e 2e 2b 2d 2e 2b 2b d4 2b 2c   ........+-.++.+,
  0010: 2f 2f 02 2f 2f 2f d1 00 00 56 28 6d 7e ad 80 72   //.///...V(m~..r
  0020: 56                                                V
Seed 5 (id=00180f1c833e1ad6, size=36 bytes, fuzzer=naive, trial=1, discovered_at=641s, mutation_op=BytesRandSetMutator,DwordAddMutator,ByteFlipMutator):
  0000: 00 01 00 00 00 19 25 61 45 25 61 45 25 25 25 25   ......%aE%aE%%%%
  0010: 65 25 31 42 42 42 42 25 41 45 25 62 eb 00 00 00   e%1BBBB%AE%b....
  0020: 7e 00 00 00                                       ~...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0005  19(.)x20                            19(.)x8 43(C)x4 44(D)x1 23(#)x1 +6u  PARTIAL
   0x0006  70(p)x10 9a(.)x9 9f(.)x1            25(%)x6 64(d)x3 2e(.)x3 70(p)x1 +7u  PARTIAL
   0x0007  6f(o)x9 9a(.)x9 70(p)x1 53(S)x1     55(U)x2 2e(.)x2 25(%)x2 62(b)x2 +12u  PARTIAL
   0x0008  70(p)x18 25(%)x1 00(.)x1            43(C)x5 2b(+)x3 25(%)x2 2e(.)x2 +8u  PARTIAL
   0x0009  33(3)x9 00(.)x9 cd(.)x1 54(T)x1     25(%)x4 2b(+)x2 41(A)x2 46(F)x2 +10u  DIFFER
   0x000a  3a(:)x10 cb(.)x9 4b(K)x1            25(%)x6 2e(.)x3 2b(+)x2 3e(>)x1 +8u  DIFFER
   0x000b  2f(/)x17 43(C)x2 25(%)x1            25(%)x4 2b(+)x3 2d(-)x2 63(c)x2 +9u  PARTIAL
   0x000c  3a(:)x10 2f(/)x9 2e(.)x1            25(%)x5 2b(+)x3 2e(.)x3 45(E)x2 +7u  PARTIAL
   0x000d  3a(:)x10 00(.)x5 31(1)x4 80(.)x1    2e(.)x3 25(%)x2 64(d)x2 2a(*)x1 +12u  PARTIAL
   0x000e  00(.)x10 32(2)x10                   25(%)x7 2b(+)x2 2d(-)x2 63(c)x1 +8u  DIFFER
   0x000f  10(.)x10 00(.)x5 ad(.)x5            25(%)x4 45(E)x2 42(B)x2 2b(+)x1 +11u  DIFFER
   0x0013  28(()x9 3a(:)x7 09(.)x3 00(.)x1     2e(.)x3 41(A)x2 42(B)x2 62(b)x2 +9u  DIFFER
   0x0017  39(9)x16 09(.)x3 04(.)x1            41(A)x3 25(%)x2 2e(.)x2 1f(.)x1 +12u  DIFFER
   0x0018  30(0)x9 9c(.)x9 64(d)x1 10(.)x1     41(A)x3 43(C)x3 00(.)x2 25(%)x2 +10u  PARTIAL
   0x0019  30(0)x20                            25(%)x3 40(@)x2 45(E)x2 2e(.)x2 +10u  DIFFER
   0x001a  31(1)x18 00(.)x1 5b([)x1            25(%)x5 41(A)x3 2f(/)x2 66(f)x2 +8u  PARTIAL
   0x001b  72(r)x10 ad(.)x7 00(.)x2 2d(-)x1    2e(.)x3 25(%)x3 2d(-)x2 2f(/)x1 +11u  PARTIAL
   0x001c  38(8)x14 e8(.)x4 00(.)x2            2f(/)x2 2e(.)x2 45(E)x2 5a(Z)x1 +13u  PARTIAL
   0x001d  35(5)x14 03(.)x4 02(.)x1 04(.)x1    2e(.)x2 2d(-)x2 25(%)x2 62(b)x2 +12u  PARTIAL
   0x001e  30(0)x19 28(()x1                    25(%)x4 00(.)x2 65(e)x2 44(D)x2 +10u  DIFFER
   0x001f  00(.)x20                            2e(.)x4 25(%)x3 00(.)x2 72(r)x2 +8u  PARTIAL
   0x0020  02(.)x20                            65(e)x2 2e(.)x2 42(B)x2 6d(m)x1 +12u  DIFFER
   0x0021  00(.)x20                            2d(-)x3 25(%)x2 00(.)x2 62(b)x2 +8u  PARTIAL
   0x0022  00(.)x20                            44(D)x2 00(.)x2 2e(.)x2 74(t)x1 +10u  PARTIAL
   0x0023  00(.)x20                            2e(.)x3 62(b)x2 25(%)x2 d6(.)x1 +7u  PARTIAL
   0x0024  47(G)x10 48(H)x10                   50(P)x2 42(B)x1 9e(.)x1 2f(/)x1 +7u  DIFFER
   0x0025  48(H)x20                            25(%)x3 2e(.)x2 41(A)x2 64(d)x1 +4u  DIFFER
   0x0026  54(T)x20                            45(E)x2 41(A)x1 2f(/)x1 25(%)x1 +7u  DIFFER
   0x0027  54(T)x20                            72(r)x1 27(')x1 00(.)x1 40(@)x1 +8u  DIFFER
   0x0028  50(P)x20                            25(%)x5 33(3)x1 db(.)x1 2f(/)x1 +4u  PARTIAL
   0x0029  2f(/)x20                            25(%)x2 41(A)x2 31(1)x1 2f(/)x1 +6u  PARTIAL
   0x002a  20( )x10 23(#)x10                   25(%)x4 65(e)x1 2e(.)x1 42(B)x1 +4u  DIFFER
   0x002b  6d(m)x20                            25(%)x5 2e(.)x2 4b(K)x1 66(f)x1 +2u  DIFFER
   0x002c  65(e)x11 98(.)x9                    25(%)x3 65(e)x2 d2(.)x1 2e(.)x1 +4u  PARTIAL
   0x002d  61(a)x9 a1(.)x9 40(@)x1 56(V)x1     25(%)x2 43(C)x1 ff(.)x1 2e(.)x1 +6u  PARTIAL
   0x002f  24($)x10 25(%)x9 2c(,)x1            25(%)x2 55(U)x1 2e(.)x1 44(D)x1 +5u  PARTIAL
   0x0030  6d(m)x10 65(e)x10                   25(%)x2 62(b)x2 43(C)x1 2e(.)x1 +4u  DIFFER
   0x0032  8e(.)x10 54(T)x8 43(C)x2            25(%)x3 b5(.)x1 2e(.)x1 42(B)x1 +3u  DIFFER
   0x0033  68(h)x10 65(e)x10                   25(%)x3 2e(.)x2 41(A)x2 bd(.)x1 +1u  DIFFER
   0x0034  65(e)x10 74(t)x10                   25(%)x4 45(E)x2 2e(.)x1 e2(.)x1 +1u  PARTIAL
   ... (10 more divergent offsets)
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
  prompts_b/curl_399.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 399,
  "target": "curl",
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 399 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 399 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 399 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).