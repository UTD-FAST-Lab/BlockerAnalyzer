==== BLOCKER ====
Target: curl
Branch ID: 263
Location: /src/curl/lib/mime.c:321:26
Enclosing function: mime.c:escape_string
Source line:     for(p = table; *p && **p != *src; p++)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           4        6          0  REFERENCE
value_profile                    1        9          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             9        1          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     1        9          0  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        2        8          0  REFERENCE
fast                             4        6          0  REFERENCE
grimoire                         8        2          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=10.80h  loser=19.60h
  avg hitcount on branch: winner=35  loser=0
  prob_div=0.80  dur_div=8.80h  hit_div=34
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/263/{W,L}/branch_coverage_show.txt

--- Enclosing function: mime.c:escape_string (/src/curl/lib/mime.c:287-331) ---
[ ]   285  static char *escape_string(struct Curl_easy *data,
[ ]   286                             const char *src, enum mimestrategy strategy)
[B]   287  {
[B]   288    CURLcode result;
[B]   289    struct dynbuf db;
[B]   290    const char * const *table;
[B]   291    const char * const *p;
[ ]   292    /* replace first character by rest of string. */
[B]   293    static const char * const mimetable[] = {
[B]   294      "\\\\\\",
[B]   295      "\"\\\"",
[B]   296      NULL
[B]   297    };
[ ]   298    /* WHATWG HTML living standard 4.10.21.8 2 specifies:
[ ]   299       For field names and filenames for file fields, the result of the
[ ]   300       encoding in the previous bullet point must be escaped by replacing
[ ]   301       any 0x0A (LF) bytes with the byte sequence `%0A`, 0x0D (CR) with `%0D`
[ ]   302       and 0x22 (") with `%22`.
[ ]   303       The user agent must not perform any other escapes. */
[B]   304    static const char * const formtable[] = {
[B]   305      "\"%22",
[B]   306      "\r%0D",
[B]   307      "\n%0A",
[B]   308      NULL
[B]   309    };
[ ]   310  
[B]   311    table = formtable;
[ ]   312    /* data can be NULL when this function is called indirectly from
[ ]   313       curl_formget(). */
[B]   314    if(strategy == MIMESTRATEGY_MAIL ||
[B]   315       (data && (data->set.mime_options & CURLMIMEOPT_FORMESCAPE)))
[ ]   316      table = mimetable;
[ ]   317  
[B]   318    Curl_dyn_init(&db, CURL_MAX_INPUT_LENGTH);
[ ]   319  
[B]   320    for(result = Curl_dyn_addn(&db, STRCONST("")); !result && *src; src++) {
[B]   321      for(p = table; *p && **p != *src; p++) <-- BLOCKER
[B]   322        ;
[ ]   323  
[B]   324      if(*p)
[W]   325        result = Curl_dyn_add(&db, *p + 1);
[B]   326      else
[B]   327        result = Curl_dyn_addn(&db, src, 1);
[B]   328    }
[ ]   329  
[B]   330    return Curl_dyn_ptr(&db);
[B]   331  }

--- Caller (1 hop): Curl_mime_prepare_headers (/src/curl/lib/mime.c:1773-1906, calls mime.c:escape_string at line 1838) (±10 around call site) ---
[B]  1828          (contenttype && !strncasecompare(contenttype, "multipart/", 10)))
[ ]  1829            disposition = DISPOSITION_DEFAULT;
[B]  1830      if(disposition && curl_strequal(disposition, "attachment") &&
[B]  1831       !part->name && !part->filename)
[ ]  1832        disposition = NULL;
[B]  1833      if(disposition) {
[B]  1834        char *name = NULL;
[B]  1835        char *filename = NULL;
[ ]  1836  
[B]  1837        if(part->name) {
[B]  1838          name = escape_string(part->easy, part->name, strategy); <-- CALL
[B]  1839          if(!name)
[ ]  1840            ret = CURLE_OUT_OF_MEMORY;
[B]  1841        }
[B]  1842        if(!ret && part->filename) {
[ ]  1843          filename = escape_string(part->easy, part->filename, strategy);
[ ]  1844          if(!filename)
[ ]  1845            ret = CURLE_OUT_OF_MEMORY;
[ ]  1846        }
[B]  1847        if(!ret)
[B]  1848          ret = Curl_mime_add_header(&part->curlheaders,

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  Curl_mime_prepare_headers  (/src/curl/lib/mime.c:1773-1906, calls mime.c:escape_string at line 1838)
hop 3  Curl_http_body  (/src/curl/lib/http.c:2348-2433, calls Curl_mime_prepare_headers at line 2387)
hop 3  smtp.c:smtp_perform_mail  (/src/curl/lib/smtp.c:597-773, calls Curl_mime_prepare_headers at line 699)
hop 4  Curl_http  (/src/curl/lib/http.c:3088-3372, calls Curl_http_body at line 3202)
hop 4  smtp.c:smtp_perform  (/src/curl/lib/smtp.c:1479-1528, calls smtp.c:smtp_perform_mail at line 1511)
hop 5  smtp.c:smtp_regular_transfer  (/src/curl/lib/smtp.c:1630-1651, calls smtp.c:smtp_perform at line 1644)
hop 6  smtp.c:smtp_do  (/src/curl/lib/smtp.c:1540-1552, calls smtp.c:smtp_regular_transfer at line 1549)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      26       420  mime.c:mimesetstate  (/src/curl/lib/mime.c:277-281)
      15       225  mime.c:readback_bytes  (/src/curl/lib/mime.c:765-787)
       9       195  mime.c:cleanup_encoder_state  (/src/curl/lib/mime.c:373-377)
       6       150  mime.c:cleanup_part_content  (/src/curl/lib/mime.c:1127-1143)
       8       150  Curl_mime_initpart  (/src/curl/lib/mime.c:1306-1311)
       4        90  Curl_mime_cleanpart  (/src/curl/lib/mime.c:1170-1179)
       6        90  mime.c:search_header  (/src/curl/lib/mime.c:347-354)
       3        48  mime.c:read_part_content  (/src/curl/lib/mime.c:792-852)
       2        45  curl_mime_headers  (/src/curl/lib/mime.c:1500-1513)
       3        45  mime.c:readback_part  (/src/curl/lib/mime.c:917-996)
       0        30  mime.c:match_header  (/src/curl/lib/mime.c:335-342)
       2        30  mime.c:slist_size  (/src/curl/lib/mime.c:1626-1633)
       2        30  Curl_mime_size  (/src/curl/lib/mime.c:1663-1681)
       2        30  Curl_mime_add_header  (/src/curl/lib/mime.c:1686-1704)
       2        30  Curl_mime_prepare_headers  (/src/curl/lib/mime.c:1773-1906)
... (20 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  Curl_mime_prepare_headers  (/src/curl/lib/mime.c:1773-1906) ---
  d=2   L1785  T=0 F=2  T=0 F=30  if(part->state.state == MIMESTATE_CURLHEADERS)
  d=2   L1790  T=2 F=0  T=30 F=0  if(!customct)
  d=2   L1792  T=0 F=2  T=0 F=30  if(customct)
  d=2   L1796  T=1 F=1  T=15 F=15  if(!contenttype) {
  d=2   L1798  T=0 F=1  T=0 F=15  case MIMEKIND_MULTIPART:
  d=2   L1801  T=0 F=1  T=0 F=15  case MIMEKIND_FILE:
  d=2   L1808  T=1 F=0  T=15 F=0  default:
  d=2   L1814  T=1 F=1  T=15 F=15  if(part->kind == MIMEKIND_MULTIPART) {
  d=2   L1816  T=1 F=0  T=15 F=0  if(mime)
  d=2   L1819  T=0 F=1  T=0 F=15  else if(contenttype && !customct &&
  d=2   L1825  T=2 F=0  T=30 F=0  if(!search_header(part->userheaders, STRCONST("Content-Di...
  d=2   L1826  T=1 F=1  T=15 F=15  if(!disposition)
  d=2   L1827  T=0 F=1  T=0 F=15  if(part->filename || part->name ||
  d=2   L1827  T=0 F=1  T=0 F=15  if(part->filename || part->name ||
  d=2   L1828  T=1 F=0  T=15 F=0  (contenttype && !strncasecompare(contenttype, "multipart/...
  d=2   L1828  T=0 F=1  T=0 F=15  (contenttype && !strncasecompare(contenttype, "multipart/...
  d=2   L1830  T=0 F=1  T=0 F=15  if(disposition && curl_strequal(disposition, "attachment"...
  d=2   L1830  T=1 F=1  T=15 F=15  if(disposition && curl_strequal(disposition, "attachment"...
  d=2   L1833  T=1 F=1  T=15 F=15  if(disposition) {
  d=2   L1837  T=1 F=0  T=15 F=0  if(part->name) {
  d=2   L1839  T=0 F=1  T=0 F=15  if(!name)
  d=2   L1842  T=1 F=0  T=15 F=0  if(!ret && part->filename) {
  d=2   L1842  T=0 F=1  T=0 F=15  if(!ret && part->filename) {
  d=2   L1847  T=1 F=0  T=15 F=0  if(!ret)
  d=2   L1851  T=1 F=0  T=15 F=0  name? "; name=\"": "",
  d=2   L1852  T=1 F=0  T=15 F=0  name? name: "",
  d=2   L1853  T=1 F=0  T=15 F=0  name? "\"": "",
  d=2   L1854  T=0 F=1  T=0 F=15  filename? "; filename=\"": "",
  d=2   L1855  T=0 F=1  T=0 F=15  filename? filename: "",
  d=2   L1856  T=0 F=1  T=0 F=15  filename? "\"": "");
  d=2   L1859  T=0 F=1  T=0 F=15  if(ret)
  d=2   L1865  T=1 F=1  T=15 F=15  if(contenttype) {
  d=2   L1867  T=0 F=1  T=0 F=15  if(ret)
  d=2   L1872  T=2 F=0  T=30 F=0  if(!search_header(part->userheaders,
  d=2   L1874  T=0 F=2  T=0 F=30  if(part->encoder)
  d=2   L1876  T=1 F=1  T=15 F=15  else if(contenttype && strategy == MIMESTRATEGY_MAIL &&
  d=2   L1876  T=0 F=1  T=0 F=15  else if(contenttype && strategy == MIMESTRATEGY_MAIL &&
  d=2   L1879  T=0 F=2  T=0 F=30  if(cte) {
  d=2   L1889  T=0 F=2  T=0 F=30  if(part->state.state == MIMESTATE_CURLHEADERS)
  d=2   L1893  T=1 F=0  T=15 F=0  if(part->kind == MIMEKIND_MULTIPART && mime) {
  d=2   L1893  T=1 F=1  T=15 F=15  if(part->kind == MIMEKIND_MULTIPART && mime) {
  d=2   L1897  T=1 F=0  T=15 F=0  if(content_type_match(contenttype, STRCONST("multipart/fo...
  d=2   L1899  T=1 F=1  T=15 F=15  for(subpart = mime->firstpart; subpart; subpart = subpart...
  d=2   L1901  T=0 F=1  T=0 F=15  if(ret)
--- d=1  mime.c:escape_string  (/src/curl/lib/mime.c:287-331) ---
  d=1   L 314  T=0 F=1  T=0 F=15  if(strategy == MIMESTRATEGY_MAIL ||
  d=1   L 315  T=1 F=0  T=15 F=0  (data && (data->set.mime_options & CURLMIMEOPT_FORMESCAPE)))
  d=1   L 315  T=0 F=1  T=0 F=15  (data && (data->set.mime_options & CURLMIMEOPT_FORMESCAPE)))
  d=1   L 320  T=4 F=1  T=60 F=15  for(result = Curl_dyn_addn(&db, STRCONST("")); !result &&...
  d=1   L 320  T=5 F=0  T=75 F=0  for(result = Curl_dyn_addn(&db, STRCONST("")); !result &&...
  d=1   L 321  T=10 F=2  T=180 F=0  for(p = table; *p && **p != *src; p++)  <-- BLOCKER
  d=1   L 321  T=12 F=2  T=180 F=60  for(p = table; *p && **p != *src; p++)  <-- BLOCKER
  d=1   L 324  T=2 F=2  T=0 F=60  if(*p)

[off-chain: 130 additional divergent branches across 27 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=0a01b9b5d382aecb, size=113 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=64635s, mutation_op=BytesInsertMutator,TokenReplace):
  0000: 00 01 00 00 00 19 70 00 70 33 3a 00 01 31 32 37   ......p.p3:..127
  0010: 2e 4c 2e 30 2e 31 3a 39 30 30 31 2f 38 35 30 00   .L.0.1:9001/850.
  0020: 0d 00 00 00 47 00 0e 00 00 00 04 0a 0a 75 73 65   ....G........use
  0030: 72 00 fc 00 1d 00 06 73 65 63 72 65 74 f1 ff ff   r......secret...

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=5672884cecc4db29, size=38 bytes, fuzzer=value_profile, trial=1, discovered_at=22s, mutation_op=BytesInsertMutator):
  0000: 00 34 00 00 00 00 00 01 00 00 00 19 72 65 65 65   .4..........reee
  0010: 65 65 6f 00 00 06 64 dd dd 72 9b 63 72 65 74 cd   eeo...d..r.cret.
  0020: 41 ff e6 72 65 74                                 A..ret
Seed 2 (id=08fbf9f64a7c35c9, size=39 bytes, fuzzer=value_profile, trial=1, discovered_at=221s, mutation_op=BytesSwapMutator,BytesExpandMutator):
  0000: 00 01 00 00 00 19 4e 00 01 00 00 00 19 4e 2d 2b   ......N......N-+
  0010: 43 2e 2e 2b 2e 2e 2e 2e 1d ff 2e 32 2e 30 2e 00   C..+.......2.0..
  0020: 34 00 00 00 00 66 66                              4....ff
Seed 3 (id=15b9bbc304e3dba1, size=38 bytes, fuzzer=value_profile, trial=1, discovered_at=1993s, mutation_op=QwordAddMutator,BitFlipMutator):
  0000: 00 34 00 00 00 00 00 01 00 00 00 19 72 65 65 65   .4..........reee
  0010: 2f 72 72 72 7a 72 72 b7 a0 b7 b7 b7 70 65 74 cd   /rrrzrr.....pet.
  0020: 40 ff e6 55 65 74                                 @..Uet
Seed 4 (id=28f4a216f2a41873, size=39 bytes, fuzzer=value_profile, trial=1, discovered_at=3942s, mutation_op=BytesInsertCopyMutator,ByteDecMutator,ByteFlipMutator,BytesSwapMutator):
  0000: 00 34 00 00 00 00 00 01 00 00 00 19 72 65 65 b7   .4..........ree.
  0010: b7 48 70 65 74 b7 b7 65 2e 72 72 72 7a b7 b7 cd   .Hpet..e.rrrz...
  0020: 3f ff e6 55 55 65 74                              ?..UUet
Seed 5 (id=57d10adc7ff1313d, size=40 bytes, fuzzer=value_profile, trial=1, discovered_at=9197s, mutation_op=BitFlipMutator,ByteDecMutator,ByteInterestingMutator):
  0000: 00 34 00 00 00 00 00 01 00 00 00 19 72 72 72 72   .4..........rrrr
  0010: 72 72 72 72 6f 34 30 34 34 34 34 34 34 34 34 3a   rrrro4044444444:
  0020: 40 34 34 34 34 72 65 73                           @4444res


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0001  01(.)x1                             34(4)x9 01(.)x6                     PARTIAL
   0x0005  19(.)x1                             00(.)x9 19(.)x6                     PARTIAL
   0x0006  70(p)x1                             00(.)x9 73(s)x3 4e(N)x1 70(p)x1 +1u  PARTIAL
   0x0007  00(.)x1                             01(.)x9 73(s)x3 6f(o)x2 00(.)x1     PARTIAL
   0x0008  70(p)x1                             00(.)x9 6c(l)x3 70(p)x2 01(.)x1     PARTIAL
   0x0009  33(3)x1                             00(.)x10 76(v)x2 33(3)x2 8b(.)x1    PARTIAL
   0x000a  3a(:)x1                             00(.)x10 32(2)x3 40(@)x2            DIFFER
   0x000b  00(.)x1                             19(.)x9 33(3)x3 30(0)x2 00(.)x1     PARTIAL
   0x000c  01(.)x1                             72(r)x6 00(.)x5 19(.)x1 53(S)x1 +2u  DIFFER
   0x000d  31(1)x1                             65(e)x4 31(1)x3 72(r)x2 00(.)x2 +4u  PARTIAL
   0x000e  32(2)x1                             65(e)x3 32(2)x3 2d(-)x2 2b(+)x2 +4u  PARTIAL
   0x000f  37(7)x1                             37(7)x3 00(.)x3 65(e)x2 b7(.)x2 +4u  PARTIAL
   0x0010  2e(.)x1                             2e(.)x4 00(.)x2 65(e)x1 43(C)x1 +7u  PARTIAL
   0x0011  4c(L)x1                             00(.)x4 30(0)x3 2e(.)x2 72(r)x2 +3u  DIFFER
   0x0012  2e(.)x1                             2e(.)x3 72(r)x3 2f(/)x3 70(p)x2 +3u  PARTIAL
   0x0013  30(0)x1                             00(.)x3 72(r)x3 30(0)x3 65(e)x2 +3u  PARTIAL
   0x0014  2e(.)x1                             2e(.)x5 00(.)x3 6f(o)x2 7a(z)x1 +4u  PARTIAL
   0x0015  31(1)x1                             31(1)x3 34(4)x2 00(.)x2 2d(-)x2 +6u  PARTIAL
   0x0016  3a(:)x1                             c6(.)x3 00(.)x2 2d(-)x2 64(d)x1 +7u  DIFFER
   0x0017  39(9)x1                             8a(.)x3 65(e)x2 34(4)x2 00(.)x2 +6u  DIFFER
   0x0018  30(0)x1                             30(0)x3 34(4)x2 65(e)x2 00(.)x2 +6u  PARTIAL
   0x0019  30(0)x1                             30(0)x3 72(r)x2 34(4)x2 00(.)x2 +6u  PARTIAL
   0x001a  31(1)x1                             31(1)x3 34(4)x2 00(.)x2 9b(.)x1 +7u  PARTIAL
   0x001b  2f(/)x1                             2f(/)x3 b7(.)x2 34(4)x2 20( )x2 +6u  PARTIAL
   0x001c  38(8)x1                             38(8)x3 2e(.)x2 34(4)x2 0f(.)x2 +6u  PARTIAL
   0x001d  35(5)x1                             35(5)x3 00(.)x3 65(e)x2 34(4)x2 +5u  PARTIAL
   0x001e  30(0)x1                             30(0)x5 74(t)x3 34(4)x2 2e(.)x1 +4u  PARTIAL
   0x001f  00(.)x1                             00(.)x6 cd(.)x4 3a(:)x1 34(4)x1 +3u  PARTIAL
   0x0020  0d(.)x1                             34(4)x7 41(A)x2 40(@)x2 3f(?)x1 +3u  DIFFER
   0x0021  00(.)x1                             00(.)x6 ff(.)x4 34(4)x1 3a(:)x1 +3u  PARTIAL
   0x0022  00(.)x1                             00(.)x6 e6(.)x4 34(4)x2 ff(.)x1 +2u  PARTIAL
   0x0023  00(.)x1                             00(.)x6 55(U)x3 34(4)x2 72(r)x1 +3u  PARTIAL
   0x0024  47(G)x1                             65(e)x3 00(.)x3 47(G)x3 55(U)x1 +5u  PARTIAL
   0x0025  00(.)x1                             74(t)x3 46(F)x3 65(e)x2 00(.)x2 +4u  PARTIAL
   0x0026  0e(.)x1                             74(t)x2 72(r)x2 06(.)x2 66(f)x1 +4u  DIFFER
   0x0027  00(.)x1                             6f(o)x3 00(.)x2 73(s)x1 72(r)x1 +1u  PARTIAL
   0x0028  00(.)x1                             6d(m)x3 00(.)x2 65(e)x1 73(s)x1     PARTIAL
   0x0029  00(.)x1                             3a(:)x2 00(.)x2 74(t)x1 01(.)x1     PARTIAL
   0x002a  04(.)x1                             00(.)x3 20( )x2                     DIFFER
   0x002b  0a(.)x1                             00(.)x3 6d(m)x2                     DIFFER
   ... (20 more divergent offsets)
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
  prompts_b/curl_263.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 263,
  "target": "curl",
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 263 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 263 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 263 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).