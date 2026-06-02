==== BLOCKER ====
Target: curl
Branch ID: 266
Location: /src/curl/lib/mime.c:350:9
Enclosing function: mime.c:search_header
Source line:   for(; !value && hdrlist; hdrlist = hdrlist->next)
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
  avg duration blocked: winner=6.20h  loser=22.50h
  avg hitcount on branch: winner=7  loser=0
  prob_div=1.00  dur_div=16.30h  hit_div=7
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=2.90h  loser=21.70h
  avg hitcount on branch: winner=10  loser=0
  prob_div=1.00  dur_div=18.80h  hit_div=10
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/266/{W,L}/branch_coverage_show.txt

--- Enclosing function: mime.c:search_header (/src/curl/lib/mime.c:347-354) ---
[ ]   345  static char *search_header(struct curl_slist *hdrlist,
[ ]   346                             const char *hdr, size_t len)
[B]   347  {
[B]   348    char *value = NULL;
[ ]   349  
[B]   350    for(; !value && hdrlist; hdrlist = hdrlist->next) <-- BLOCKER
[B]   351      value = match_header(hdrlist, hdr, len);
[ ]   352  
[B]   353    return value;
[B]   354  }

--- Caller (1 hop): Curl_mime_prepare_headers (/src/curl/lib/mime.c:1773-1906, calls mime.c:search_header at line 1791) (±10 around call site) ---
[B]  1781    curl_slist_free_all(part->curlheaders);
[B]  1782    part->curlheaders = NULL;
[ ]  1783  
[ ]  1784    /* Be sure we won't access old headers later. */
[B]  1785    if(part->state.state == MIMESTATE_CURLHEADERS)
[ ]  1786      mimesetstate(&part->state, MIMESTATE_CURLHEADERS, NULL);
[ ]  1787  
[ ]  1788    /* Check if content type is specified. */
[B]  1789    customct = part->mimetype;
[B]  1790    if(!customct)
[B]  1791      customct = search_header(part->userheaders, STRCONST("Content-Type")); <-- CALL
[B]  1792    if(customct)
[W]  1793      contenttype = customct;
[ ]  1794  
[ ]  1795    /* If content type is not specified, try to determine it. */
[B]  1796    if(!contenttype) {
[B]  1797      switch(part->kind) {
[ ]  1798      case MIMEKIND_MULTIPART:
[ ]  1799        contenttype = MULTIPART_CONTENTTYPE_DEFAULT;
[ ]  1800        break;
[ ]  1801      case MIMEKIND_FILE:

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  Curl_mime_prepare_headers  (/src/curl/lib/mime.c:1773-1906, calls mime.c:search_header at line 1791)
hop 3  Curl_http_body  (/src/curl/lib/http.c:2348-2433, calls Curl_mime_prepare_headers at line 2387)
hop 3  smtp.c:smtp_perform_mail  (/src/curl/lib/smtp.c:597-773, calls Curl_mime_prepare_headers at line 699)
hop 4  Curl_http  (/src/curl/lib/http.c:3088-3372, calls Curl_http_body at line 3202)
hop 4  smtp.c:smtp_perform  (/src/curl/lib/smtp.c:1479-1528, calls smtp.c:smtp_perform_mail at line 1511)
hop 5  smtp.c:smtp_regular_transfer  (/src/curl/lib/smtp.c:1630-1651, calls smtp.c:smtp_perform at line 1644)
hop 6  smtp.c:smtp_do  (/src/curl/lib/smtp.c:1540-1552, calls smtp.c:smtp_regular_transfer at line 1549)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       7         2  mime.c:mime_mem_read  (/src/curl/lib/mime.c:661-676)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  Curl_mime_prepare_headers  (/src/curl/lib/mime.c:1773-1906) ---
  d=2   L1792  T=20 F=21  T=0 F=41  if(customct)
  d=2   L1826  T=41 F=0  T=20 F=21  if(!disposition)
  d=2   L1827  T=0 F=41  T=0 F=20  if(part->filename || part->name ||
  d=2   L1827  T=8 F=33  T=0 F=20  if(part->filename || part->name ||
  d=2   L1828  T=20 F=13  T=20 F=0  (contenttype && !strncasecompare(contenttype, "multipart/...
  d=2   L1828  T=20 F=0  T=0 F=20  (contenttype && !strncasecompare(contenttype, "multipart/...
  d=2   L1830  T=28 F=0  T=0 F=21  if(disposition && curl_strequal(disposition, "attachment"...
  d=2   L1831  T=20 F=8  T=0 F=0  !part->name && !part->filename)
  d=2   L1831  T=20 F=0  T=0 F=0  !part->name && !part->filename)
  d=2   L1837  T=8 F=0  T=13 F=8  if(part->name) {
  d=2   L1842  T=8 F=0  T=21 F=0  if(!ret && part->filename) {
  d=2   L1842  T=0 F=8  T=0 F=21  if(!ret && part->filename) {
  d=2   L1847  T=8 F=0  T=21 F=0  if(!ret)
  d=2   L1851  T=8 F=0  T=13 F=8  name? "; name=\"": "",
  d=2   L1852  T=8 F=0  T=13 F=8  name? name: "",
  d=2   L1853  T=8 F=0  T=13 F=8  name? "\"": "",
  d=2   L1854  T=0 F=8  T=0 F=21  filename? "; filename=\"": "",
  d=2   L1855  T=0 F=8  T=0 F=21  filename? filename: "",
  d=2   L1856  T=0 F=8  T=0 F=21  filename? "\"": "");
  d=2   L1859  T=0 F=8  T=0 F=21  if(ret)
  d=2   L1897  T=0 F=20  T=20 F=0  if(content_type_match(contenttype, STRCONST("multipart/fo...
--- d=1  mime.c:search_header  (/src/curl/lib/mime.c:347-354) ---
  d=1   L 350  T=195 F=20  T=165 F=0  for(; !value && hdrlist; hdrlist = hdrlist->next)  <-- BLOCKER

[off-chain: 17 additional divergent branches across 7 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=3ada62fdafca01cd, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=4595s, mutation_op=ByteInterestingMutator,BytesDeleteMutator,BitFlipMutator,WordAddMutator,BitFlipMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 4b 2f 2f 3f 32 37   ......pop3K//?27
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 00 20 38 35 30 00   .0.0.1:900. 850.
  0020: 06 00 00 00 47 43 6f 6e 74 65 6e 74 2d 54 79 70   ....GContent-Typ
  0030: 65 3a 77 68 65 72 65 00 0a 54 6f 3a 20 66 61 6b   e:where..To: fak
Seed 2 (id=64421f7fa17f9e92, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=4631s, mutation_op=DwordInterestingMutator,BytesSetMutator,BytesInsertCopyMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 4b 00 2f 3f 32 37   ......pop3K./?27
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 00 20 38 35 30 00   .0.0.1:900. 850.
  0020: 06 00 00 00 47 43 6f 6e 74 65 6e 74 2d 54 79 70   ....GContent-Typ
  0030: 65 3a 77 68 65 72 65 0d 0a 54 6f 3a 20 66 61 6b   e:where..To: fak
Seed 3 (id=705a0fa0ecdc55d4, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=4639s, mutation_op=BytesDeleteMutator,BytesInsertCopyMutator,CrossoverInsertMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 4b 2f 2f 3f 32 37   ......pop3K//?27
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 00 20 38 35 30 00   .0.0.1:900. 850.
  0020: 06 00 00 00 47 43 6f 6e 74 65 6e 74 2d 54 79 70   ....GContent-Typ
  0030: 65 3a 6d 69 6c 74 69 70 0a 54 6f 3a 20 66 61 6b   e:miltip.To: fak
Seed 4 (id=0d635c8dfd81a1f9, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=7482s, mutation_op=ByteFlipMutator,CrossoverReplaceMutator):
  0000: 00 01 00 00 00 19 70 6f 00 01 00 00 00 19 25 35   ......po......%5
  0010: 65 25 65 64 4e 35 3a 39 30 30 00 20 38 35 30 00   e%edN5:900. 850.
  0020: 06 00 00 00 47 43 6f 6e 74 65 6e 74 2d 54 79 70   ....GContent-Typ
  0030: 65 3a 77 68 65 72 65 0d 0a 54 6f 3a 20 66 61 6b   e:where..To: fak
Seed 5 (id=acb98175a6d3d5c3, size=130 bytes, fuzzer=cmplog, trial=1, discovered_at=7598s, mutation_op=ByteInterestingMutator,BytesSetMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 c5 77 2f ad 32 37   ......pop3.w/.27
  0010: 2f 3f 2e 30 2e 31 3a 39 30 30 31 00 38 00 30 00   /?.0.1:9001.8.0.
  0020: 06 00 00 00 47 43 6f 6e 74 65 6e 74 2d 54 79 70   ....GContent-Typ
  0030: 65 3a 77 68 65 37 65 0d 0a 04 6f 3a 20 66 00 6b   e:whe7e...o: f.k

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=18d48c8a6b6d8917, size=42 bytes, fuzzer=naive, trial=1, discovered_at=35s, mutation_op=WordInterestingMutator):
  0000: 00 01 00 00 00 19 41 2e 2d 2d 2d 2d 2d 2d 64 00   ......A.------d.
  0010: 10 00 01 00 00 00 19 64 2e 2e 69 7f f7 00 00 00   .......d..i.....
  0020: 34 00 00 00 00 80 2e fe eb ff                     4.........
Seed 2 (id=11a70e50c05da388, size=42 bytes, fuzzer=naive, trial=1, discovered_at=181s, mutation_op=CrossoverReplaceMutator,ByteNegMutator):
  0000: 00 01 00 00 00 19 41 2e 2d 2d 2d 2d 2d 2d 64 2d   ......A.------d-
  0010: 65 00 01 00 00 00 19 64 2e 2e 69 81 f7 00 00 00   e......d..i.....
  0020: 34 00 00 00 00 80 2e fe eb ff                     4.........
Seed 3 (id=0f647baa03cf861d, size=42 bytes, fuzzer=naive, trial=1, discovered_at=930s, mutation_op=CrossoverReplaceMutator,ByteNegMutator):
  0000: 00 01 00 00 00 19 41 2e 2d 40 72 73 2d d3 64 2d   ......A.-@rs-.d-
  0010: 65 00 01 00 00 00 19 64 2e 2e 69 8f f7 00 00 00   e......d..i.....
  0020: 34 00 00 00 01 80 2e fe eb ff                     4.........
Seed 4 (id=09bb327a47e9cad2, size=44 bytes, fuzzer=naive, trial=1, discovered_at=1220s, mutation_op=ByteNegMutator,WordInterestingMutator,DwordAddMutator):
  0000: 00 0d 00 00 00 02 2e 2e 00 01 00 00 00 19 25 41   ..............%A
  0010: 26 25 25 63 25 64 43 00 02 36 41 26 25 25 63 25   &%%c%dC..6A&%%c%
  0020: 64 43 94 25 36 41 41 25 bc 43 43 43               dC.%6AA%.CCC
Seed 5 (id=15b9bbc304e3dba1, size=38 bytes, fuzzer=value_profile, trial=1, discovered_at=1993s, mutation_op=QwordAddMutator,BitFlipMutator):
  0000: 00 34 00 00 00 00 00 01 00 00 00 19 72 65 65 65   .4..........reee
  0010: 2f 72 72 72 7a 72 72 b7 a0 b7 b7 b7 70 65 74 cd   /rrrzrr.....pet.
  0020: 40 ff e6 55 65 74                                 @..Uet


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0001  01(.)x20                            01(.)x14 34(4)x3 0d(.)x1 03(.)x1 +1u  PARTIAL
   0x0005  19(.)x20                            19(.)x14 00(.)x4 02(.)x1 01(.)x1    PARTIAL
   0x0006  70(p)x20                            41(A)x7 00(.)x4 70(p)x2 8f(.)x2 +5u  PARTIAL
   0x0007  6f(o)x20                            2e(.)x5 6f(o)x4 01(.)x3 d6(.)x2 +5u  PARTIAL
   0x0008  70(p)x14 00(.)x6                    00(.)x6 2d(-)x4 70(p)x3 d6(.)x2 +4u  PARTIAL
   0x0009  33(3)x18 01(.)x1 00(.)x1            00(.)x6 2d(-)x3 33(3)x3 d6(.)x2 +6u  PARTIAL
   0x000a  4b(K)x9 c5(.)x5 3a(:)x5 00(.)x1     00(.)x7 2d(-)x3 d6(.)x2 3a(:)x2 +5u  PARTIAL
   0x000b  2f(/)x13 77(w)x5 00(.)x2            30(0)x4 2d(-)x3 00(.)x3 19(.)x3 +6u  PARTIAL
   0x000c  2f(/)x15 00(.)x5                    00(.)x6 2d(-)x5 72(r)x2 d6(.)x2 +4u  PARTIAL
   0x000d  ad(.)x10 3f(?)x9 19(.)x1            2d(-)x4 65(e)x3 31(1)x3 00(.)x3 +6u  PARTIAL
   0x000e  32(2)x13 cd(.)x5 25(%)x1 00(.)x1    64(d)x8 00(.)x5 65(e)x2 61(a)x2 +3u  PARTIAL
   0x000f  37(7)x14 c8(.)x5 35(5)x1            00(.)x7 2d(-)x3 61(a)x2 41(A)x1 +7u  PARTIAL
   0x0011  30(0)x9 3f(?)x5 00(.)x5 25(%)x1     00(.)x10 25(%)x2 45(E)x2 72(r)x1 +5u  PARTIAL
   0x0012  2e(.)x19 65(e)x1                    00(.)x4 01(.)x3 42(B)x2 2e(.)x2 +9u  PARTIAL
   0x0013  30(0)x14 ff(.)x5 64(d)x1            00(.)x5 30(0)x3 72(r)x2 63(c)x1 +9u  PARTIAL
   0x0014  2e(.)x14 7f(.)x5 4e(N)x1            00(.)x6 2e(.)x4 43(C)x2 25(%)x1 +7u  PARTIAL
   0x0015  31(1)x13 00(.)x6 35(5)x1            00(.)x8 43(C)x2 31(1)x2 30(0)x2 +6u  PARTIAL
   0x0016  3a(:)x15 00(.)x5                    19(.)x4 3a(:)x4 00(.)x3 5b([)x2 +7u  PARTIAL
   0x0017  39(9)x15 22(")x4 34(4)x1            00(.)x4 8a(.)x4 64(d)x3 25(%)x3 +6u  PARTIAL
   0x0018  30(0)x15 ad(.)x5                    30(0)x5 2e(.)x4 00(.)x3 40(@)x2 +6u  PARTIAL
   0x0019  30(0)x15 00(.)x5                    30(0)x5 2e(.)x3 25(%)x3 00(.)x2 +7u  PARTIAL
   0x001a  00(.)x14 31(1)x5 35(5)x1            00(.)x6 69(i)x3 64(d)x2 ff(.)x2 +6u  PARTIAL
   0x001b  20( )x10 00(.)x5 ff(.)x4 2a(*)x1    04(.)x3 2f(/)x2 20( )x2 7f(.)x1 +12u  PARTIAL
   0x001c  38(8)x14 ff(.)x4 00(.)x1 01(.)x1    f7(.)x4 38(8)x4 0f(.)x2 25(%)x1 +9u  PARTIAL
   0x001d  35(5)x10 00(.)x5 ff(.)x4 1c(.)x1    00(.)x6 35(5)x4 ff(.)x2 2d(-)x2 +6u  PARTIAL
   0x001e  30(0)x20                            30(0)x7 00(.)x5 74(t)x2 ff(.)x2 +4u  PARTIAL
   0x001f  00(.)x20                            00(.)x15 cd(.)x3 25(%)x1 2e(.)x1    PARTIAL
   0x0020  06(.)x20                            34(4)x10 06(.)x3 64(d)x1 40(@)x1 +5u  PARTIAL
   0x0021  00(.)x20                            00(.)x15 ff(.)x3 43(C)x1 01(.)x1    PARTIAL
   0x0022  00(.)x20                            00(.)x16 e6(.)x3 94(.)x1            PARTIAL
   0x0023  00(.)x20                            00(.)x16 55(U)x3 25(%)x1            PARTIAL
   0x0024  47(G)x20                            00(.)x9 47(G)x6 65(e)x2 01(.)x1 +2u  PARTIAL
   0x0025  43(C)x20                            80(.)x7 00(.)x3 41(A)x2 74(t)x2 +5u  DIFFER
   0x0026  6f(o)x20                            2e(.)x5 72(r)x3 06(.)x2 41(A)x1 +7u  DIFFER
   0x0027  6e(n)x20                            fe(.)x6 6f(o)x3 00(.)x3 25(%)x1 +4u  DIFFER
   0x0028  74(t)x20                            eb(.)x7 6d(m)x3 00(.)x3 bc(.)x1 +3u  DIFFER
   0x0029  65(e)x20                            ff(.)x7 00(.)x4 3a(:)x2 43(C)x1 +3u  DIFFER
   0x002a  6e(n)x20                            00(.)x4 20( )x2 43(C)x1 33(3)x1 +2u  DIFFER
   0x002b  74(t)x20                            00(.)x5 43(C)x1 2d(-)x1 ff(.)x1 +2u  DIFFER
   0x002c  2d(-)x20                            00(.)x2 06(.)x2 ef(.)x1 02(.)x1 +3u  DIFFER
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
  prompts_b/curl_266.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 266,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 266 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 266 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 266 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).