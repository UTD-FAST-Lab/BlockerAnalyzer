==== BLOCKER ====
Target: curl
Branch ID: 527
Location: /src/curl/lib/urlapi.c:600:12
Enclosing function: urlapi.c:hostname_check
Source line:         if(!strncmp(h, "25", 2) && h[2] && (h[2] != ']'))
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           2        6          2  REFERENCE
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        1          1  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     1        9          0  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        1        8          1  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                         3        6          1  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=1  unreached=1
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.78h  loser=19.70h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.89  dur_div=15.92h  hit_div=2
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/527/{W,L}/branch_coverage_show.txt

--- Enclosing function: urlapi.c:hostname_check (/src/curl/lib/urlapi.c:574-645) ---
[ ]   572  static CURLUcode hostname_check(struct Curl_URL *u, char *hostname,
[ ]   573                                  size_t hlen) /* length of hostname */
[B]   574  {
[B]   575    size_t len;
[B]   576    DEBUGASSERT(hostname);
[ ]   577  
[B]   578    if(!hostname[0])
[ ]   579      return CURLUE_NO_HOST;
[B]   580    else if(hostname[0] == '[') {
[B]   581      const char *l = "0123456789abcdefABCDEF:.";
[B]   582      if(hlen < 4) /* '[::]' is the shortest possible valid string */
[ ]   583        return CURLUE_BAD_IPV6;
[B]   584      hostname++;
[B]   585      hlen -= 2;
[ ]   586  
[B]   587      if(hostname[hlen] != ']')
[ ]   588        return CURLUE_BAD_IPV6;
[ ]   589  
[ ]   590      /* only valid letters are ok */
[B]   591      len = strspn(hostname, l);
[B]   592      if(hlen != len) {
[B]   593        hlen = len;
[B]   594        if(hostname[len] == '%') {
[ ]   595          /* this could now be '%[zone id]' */
[B]   596          char zoneid[16];
[B]   597          int i = 0;
[B]   598          char *h = &hostname[len + 1];
[ ]   599          /* pass '25' if present and is a url encoded percent sign */
[B]   600          if(!strncmp(h, "25", 2) && h[2] && (h[2] != ']')) <-- BLOCKER
[W]   601            h += 2;
[B]   602          while(*h && (*h != ']') && (i < 15))
[B]   603            zoneid[i++] = *h++;
[B]   604          if(!i || (']' != *h))
[ ]   605            /* impossible to reach? */
[ ]   606            return CURLUE_MALFORMED_INPUT;
[B]   607          zoneid[i] = 0;
[B]   608          u->zoneid = strdup(zoneid);
[B]   609          if(!u->zoneid)
[ ]   610            return CURLUE_OUT_OF_MEMORY;
[B]   611          hostname[len] = ']'; /* insert end bracket */
[B]   612          hostname[len + 1] = 0; /* terminate the hostname */
[B]   613        }
[ ]   614        else
[ ]   615          return CURLUE_BAD_IPV6;
[ ]   616        /* hostname is fine */
[B]   617      }
[B]   618  #ifdef ENABLE_IPV6
[B]   619      {
[B]   620        char dest[16]; /* fits a binary IPv6 address */
[B]   621        char norm[MAX_IPADR_LEN];
[B]   622        hostname[hlen] = 0; /* end the address there */
[B]   623        if(1 != Curl_inet_pton(AF_INET6, hostname, dest))
[B]   624          return CURLUE_BAD_IPV6;
[ ]   625  
[ ]   626        /* check if it can be done shorter */
[L]   627        if(Curl_inet_ntop(AF_INET6, dest, norm, sizeof(norm)) &&
[L]   628           (strlen(norm) < hlen)) {
[ ]   629          strcpy(hostname, norm);
[ ]   630          hlen = strlen(norm);
[ ]   631          hostname[hlen + 1] = 0;
[ ]   632        }
[L]   633        hostname[hlen] = ']'; /* restore ending bracket */
[L]   634      }
[L]   635  #endif
[L]   636    }
[ ]   637    else {
[ ]   638      /* letters from the second string are not ok */
[ ]   639      len = strcspn(hostname, " \r\n\t/:#?!@{}[]\\$\'\"^`*<>=;,");
[ ]   640      if(hlen != len)
[ ]   641        /* hostname with bad content */
[ ]   642        return CURLUE_BAD_HOSTNAME;
[ ]   643    }
[L]   644    return CURLUE_OK;
[B]   645  }

--- Caller (1 hop): urlapi.c:parseurl (/src/curl/lib/urlapi.c:912-1311, calls urlapi.c:hostname_check at line 1266) (±10 around call site) ---
[B]  1256                        normalized_ipv4, sizeof(normalized_ipv4))) {
[ ]  1257        Curl_dyn_reset(&host);
[ ]  1258        if(Curl_dyn_add(&host, normalized_ipv4)) {
[ ]  1259          result = CURLUE_OUT_OF_MEMORY;
[ ]  1260          goto fail;
[ ]  1261        }
[ ]  1262      }
[B]  1263      else {
[B]  1264        result = decode_host(&host);
[B]  1265        if(!result)
[B]  1266          result = hostname_check(u, Curl_dyn_ptr(&host), Curl_dyn_len(&host)); <-- CALL
[B]  1267        if(result)
[B]  1268          goto fail;
[B]  1269      }
[ ]  1270  
[L]  1271      if((flags & CURLU_GUESS_SCHEME) && !schemep) {
[L]  1272        const char *hostname = Curl_dyn_ptr(&host);
[ ]  1273        /* legacy curl-style guess based on host name */
[L]  1274        if(checkprefix("ftp.", hostname))
[ ]  1275          schemep = "ftp";
[L]  1276        else if(checkprefix("dict.", hostname))

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  curl_url_set  (/src/curl/lib/urlapi.c:1624-1887, calls urlapi.c:hostname_check at line 1872)
hop 2  urlapi.c:parseurl  (/src/curl/lib/urlapi.c:912-1311, calls urlapi.c:hostname_check at line 1266)
hop 3  Curl_follow  (/src/curl/lib/transfer.c:1568-1849, calls curl_url_set at line 1617)
hop 3  urlapi.c:parseurl_and_replace  (/src/curl/lib/urlapi.c:1318-1328, calls urlapi.c:parseurl at line 1322)
hop 4  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661, calls Curl_follow at line 2222)
hop 5  curl_multi_perform  (/src/curl/lib/multi.c:2665-2716, calls multi.c:multi_runsingle at line 2683)
hop 5  multi.c:multi_socket  (/src/curl/lib/multi.c:3101-3208, calls multi.c:multi_runsingle at line 3158)
hop 6  curl_multi_socket  (/src/curl/lib/multi.c:3288-3296, calls multi.c:multi_socket at line 3292)
hop 6  curl_multi_socket_action  (/src/curl/lib/multi.c:3300-3308, calls multi.c:multi_socket at line 3304)
hop 6  curl_multi_strerror  (/src/curl/lib/strerror.c:364-420, calls curl_multi_perform at line 368)
hop 7  easy.c:wait_or_timeout  (/src/curl/lib/easy.c:541-628, calls curl_multi_socket_action at line 582)
hop 7  curl_multi_add_handle  (/src/curl/lib/multi.c:464-590, calls curl_multi_socket at line 509)
hop 8  easy.c:easy_events  (/src/curl/lib/easy.c:636-645, calls easy.c:wait_or_timeout at line 644)
hop 8  easy.c:easy_perform  (/src/curl/lib/easy.c:706-763, calls curl_multi_add_handle at line 741)
hop 8  Curl_multi_add_perform  (/src/curl/lib/multi.c:1574-1594, calls curl_multi_add_handle at line 1580)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       3        27  curl_url_cleanup  (/src/curl/lib/urlapi.c:1338-1343)
       1        19  curl_url_get  (/src/curl/lib/urlapi.c:1377-1620)
       2        18  urlapi.c:free_urlhandle  (/src/curl/lib/urlapi.c:77-88)
       2        18  Curl_is_absolute_url  (/src/curl/lib/urlapi.c:192-229)
       1         9  urlapi.c:junkscan  (/src/curl/lib/urlapi.c:370-389)
       1         9  urlapi.c:parse_hostname_login  (/src/curl/lib/urlapi.c:401-490)
       1         9  Curl_parse_port  (/src/curl/lib/urlapi.c:494-570)
       1         9  urlapi.c:hostname_check  (/src/curl/lib/urlapi.c:574-645)  <-- enclosing
       1         9  urlapi.c:ipv4_normalize  (/src/curl/lib/urlapi.c:660-735)
       1         9  urlapi.c:decode_host  (/src/curl/lib/urlapi.c:739-765)
       1         9  urlapi.c:parseurl  (/src/curl/lib/urlapi.c:912-1311)
       1         9  urlapi.c:parseurl_and_replace  (/src/curl/lib/urlapi.c:1318-1328)
       1         9  curl_url  (/src/curl/lib/urlapi.c:1333-1335)
       1         9  curl_url_set  (/src/curl/lib/urlapi.c:1624-1887)
       0         1  urlapi.c:urlchar_needs_escaping  (/src/curl/lib/urlapi.c:123-125)
... (1 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  urlapi.c:parseurl_and_replace  (/src/curl/lib/urlapi.c:1318-1328) ---
  d=3   L1323  T=0 F=1  T=1 F=8  if(!result) {
--- d=2  urlapi.c:parseurl  (/src/curl/lib/urlapi.c:912-1311) ---
  d=2   L 935  T=0 F=1  T=0 F=9  if(urllen > CURL_MAX_INPUT_LENGTH) {
  d=2   L 946  T=0 F=1  T=0 F=9  if(schemelen && !strcmp(schemebuf, "file")) {
  d=2   L1061  T=0 F=1  T=0 F=9  if(schemelen) {
  d=2   L1089  T=0 F=1  T=0 F=9  if(!(flags & (CURLU_DEFAULT_SCHEME|CURLU_GUESS_SCHEME))) {
  d=2   L1093  T=0 F=1  T=0 F=9  if(flags & CURLU_DEFAULT_SCHEME)
  d=2   L1104  T=7 F=1  T=89 F=9  while(*p && !HOSTNAME_END(*p))
  d=2   L1108  T=1 F=0  T=9 F=0  if(len) {
  d=2   L1109  T=0 F=1  T=0 F=9  if(Curl_dyn_addn(&host, hostp, len)) {
  d=2   L1123  T=0 F=1  T=0 F=9  if(schemep) {
  d=2   L1133  T=0 F=1  T=0 F=9  if(fragment) {
  d=2   L1151  T=0 F=1  T=0 F=9  if(query && (!fragment || (query < fragment))) {
  d=2   L1192  T=0 F=1  T=0 F=9  if(pathlen && (flags & CURLU_URLENCODE)) {
  d=2   L1203  T=1 F=0  T=9 F=0  if(!pathlen) {
  d=2   L1238  T=1 F=0  T=9 F=0  if(Curl_dyn_len(&host)) {
  d=2   L1245  T=1 F=0  T=9 F=0  if(!result)
  d=2   L1247  T=0 F=1  T=0 F=9  if(result)
  d=2   L1250  T=0 F=1  T=0 F=9  if(junkscan(Curl_dyn_ptr(&host), flags)) {
  d=2   L1255  T=0 F=1  T=0 F=9  if(ipv4_normalize(Curl_dyn_ptr(&host),
  d=2   L1265  T=1 F=0  T=9 F=0  if(!result)
  d=2   L1267  T=1 F=0  T=8 F=1  if(result)
  d=2   L1271  T=0 F=0  T=1 F=0  if((flags & CURLU_GUESS_SCHEME) && !schemep) {
  d=2   L1271  T=0 F=0  T=1 F=0  if((flags & CURLU_GUESS_SCHEME) && !schemep) {
  d=2   L1290  T=0 F=0  T=0 F=1  if(!u->scheme) {
--- d=2  curl_url_set  (/src/curl/lib/urlapi.c:1624-1887) ---
  d=2   L1627  T=0 F=1  T=0 F=9  bool urlencode = (flags & CURLU_URLENCODE)? 1 : 0;
  d=2   L1633  T=0 F=1  T=0 F=9  if(!u)
  d=2   L1635  T=0 F=1  T=0 F=9  if(!part) {
  d=2   L1685  T=0 F=1  T=0 F=9  case CURLUPART_SCHEME:
  d=2   L1696  T=0 F=1  T=0 F=9  case CURLUPART_USER:
  d=2   L1699  T=0 F=1  T=0 F=9  case CURLUPART_PASSWORD:
  d=2   L1702  T=0 F=1  T=0 F=9  case CURLUPART_OPTIONS:
  d=2   L1705  T=0 F=1  T=0 F=9  case CURLUPART_HOST: {
  d=2   L1714  T=0 F=1  T=0 F=9  case CURLUPART_ZONEID:
  d=2   L1717  T=0 F=1  T=0 F=9  case CURLUPART_PORT:
  d=2   L1730  T=0 F=1  T=0 F=9  case CURLUPART_PATH:
  d=2   L1734  T=0 F=1  T=0 F=9  case CURLUPART_QUERY:
  d=2   L1740  T=0 F=1  T=0 F=9  case CURLUPART_FRAGMENT:
  d=2   L1743  T=1 F=0  T=9 F=0  case CURLUPART_URL: {
  d=2   L1757  T=0 F=1  T=0 F=9  if(Curl_is_absolute_url(part, NULL, 0,
  d=2   L1760  T=1 F=0  T=9 F=0  || curl_url_get(u, CURLUPART_URL, &oldurl, flags)) {
  d=2   L1775  T=0 F=1  T=0 F=9  default:
--- d=1  urlapi.c:hostname_check  (/src/curl/lib/urlapi.c:574-645) ---
  d=1   L 578  T=0 F=1  T=0 F=9  if(!hostname[0])
  d=1   L 580  T=1 F=0  T=9 F=0  else if(hostname[0] == '[') {
  d=1   L 582  T=0 F=1  T=0 F=9  if(hlen < 4) /* '[::]' is the shortest possible valid str...
  d=1   L 587  T=0 F=1  T=0 F=9  if(hostname[hlen] != ']')
  d=1   L 592  T=1 F=0  T=9 F=0  if(hlen != len) {
  d=1   L 594  T=1 F=0  T=9 F=0  if(hostname[len] == '%') {
  d=1   L 600  T=1 F=0  T=0 F=0  if(!strncmp(h, "25", 2) && h[2] && (h[2] != ']'))  <-- BLOCKER
  d=1   L 600  T=1 F=0  T=0 F=0  if(!strncmp(h, "25", 2) && h[2] && (h[2] != ']'))  <-- BLOCKER
  d=1   L 600  T=1 F=0  T=0 F=9  if(!strncmp(h, "25", 2) && h[2] && (h[2] != ']'))  <-- BLOCKER
  d=1   L 602  T=2 F=0  T=47 F=0  while(*h && (*h != ']') && (i < 15))
  d=1   L 602  T=2 F=1  T=47 F=9  while(*h && (*h != ']') && (i < 15))
  d=1   L 602  T=3 F=0  T=56 F=0  while(*h && (*h != ']') && (i < 15))
  d=1   L 604  T=0 F=1  T=0 F=9  if(!i || (']' != *h))
  d=1   L 604  T=0 F=1  T=0 F=9  if(!i || (']' != *h))
  d=1   L 609  T=0 F=1  T=0 F=9  if(!u->zoneid)
  d=1   L 623  T=1 F=0  T=8 F=1  if(1 != Curl_inet_pton(AF_INET6, hostname, dest))
  d=1   L 628  T=0 F=0  T=0 F=1  (strlen(norm) < hlen)) {

[off-chain: 92 additional divergent branches across 9 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=a6c98d560acaad26, size=35 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=10193s, mutation_op=BytesDeleteMutator,BytesDeleteMutator,DwordAddMutator,BitFlipMutator):
  0000: 00 01 00 00 00 19 5b 25 32 35 2e 2e 5d 00 2e 00   ......[%25..]...
  0010: 2f 2e 2f 2f 2e 69 61 35 6f 72 67 5b 2e ad db 77   /.//.ia5org[...w
  0020: 2f f7 f7                                          /..

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=c4ac2ace49d41647, size=34 bytes, fuzzer=value_profile, trial=1, discovered_at=1141s, mutation_op=CrossoverReplaceMutator,TokenReplace,BytesDeleteMutator):
  0000: 00 01 00 00 00 19 5b 25 31 31 5d 00 40 25 72 73   ......[%11].@%rs
  0010: 61 5f 70 61 64 64 69 6e 67 5f 6d 6f 64 65 00 20   a_padding_mode. 
  0020: 00 2d                                             .-
Seed 2 (id=3a543e2e4626141e, size=33 bytes, fuzzer=value_profile, trial=1, discovered_at=1164s, mutation_op=ByteDecMutator,BytesDeleteMutator,ByteAddMutator):
  0000: 00 01 00 00 00 19 5b 25 30 31 5d 00 40 25 5b 73   ......[%01].@%[s
  0010: 61 5f 70 61 64 64 69 67 5f 6d 6f 64 65 00 20 00   a_paddig_mode. .
  0020: 2d                                                -
Seed 3 (id=062b09c23493a9cb, size=34 bytes, fuzzer=value_profile, trial=1, discovered_at=1969s, mutation_op=ByteRandMutator):
  0000: 00 01 00 00 00 19 5b 25 e7 31 5d 00 40 5d 5d a3   ......[%.1].@]].
  0010: 5d 5d 5d 40 5d 5d a3 5d 5d 5d 5d 5d 64 69 00 20   ]]]@]].]]]]]di. 
  0020: 00 2d                                             .-
Seed 4 (id=dcdc4f60d0b9795e, size=36 bytes, fuzzer=value_profile, trial=1, discovered_at=14361s, mutation_op=ByteInterestingMutator,BytesExpandMutator):
  0000: 00 01 00 00 00 19 5b 25 31 25 31 31 5d 00 40 25   ......[%1%11].@%
  0010: 72 ff 61 5f 70 61 64 64 69 6e 67 5f 6d 6f 64 65   r.a_padding_mode
  0020: 00 20 00 2d                                       . .-
Seed 5 (id=d778c78162551018, size=35 bytes, fuzzer=value_profile, trial=1, discovered_at=15168s, mutation_op=CrossoverInsertMutator):
  0000: 00 01 00 00 00 19 5b 25 33 31 cc 5d 00 40 5d 5d   ......[%31.].@]]
  0010: a3 5d 5d 5d 40 5d 5d a3 5d 5d 5d 5d 5d 64 69 00   .]]]@]].]]]]]di.
  0020: 20 00 2d                                           .-


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0006  5b([)x1                             5b([)x8 25(%)x1                     PARTIAL
   0x0007  25(%)x1                             25(%)x6 35(5)x1 31(1)x1 3a(:)x1     PARTIAL
   0x0008  32(2)x1                             31(1)x4 30(0)x1 e7(.)x1 33(3)x1 +2u  DIFFER
   0x0009  35(5)x1                             31(1)x5 25(%)x3 44(D)x1             DIFFER
   0x000a  2e(.)x1                             5d(])x3 31(1)x2 cc(.)x1 25(%)x1 +2u  DIFFER
   0x000b  2e(.)x1                             00(.)x3 31(1)x3 5d(])x1 62(b)x1 +1u  DIFFER
   0x000c  5d(])x1                             40(@)x3 5d(])x2 00(.)x1 5b([)x1 +2u  PARTIAL
   0x000d  00(.)x1                             25(%)x4 5d(])x2 00(.)x2 40(@)x1     PARTIAL
   0x000e  2e(.)x1                             5d(])x2 40(@)x2 72(r)x1 5b([)x1 +3u  DIFFER
   0x000f  00(.)x1                             25(%)x3 73(s)x2 a3(.)x1 5d(])x1 +2u  DIFFER
   0x0010  2f(/)x1                             61(a)x2 72(r)x2 5d(])x1 a3(.)x1 +3u  DIFFER
   0x0011  2e(.)x1                             5f(_)x2 5d(])x2 ff(.)x2 41(A)x1 +2u  DIFFER
   0x0012  2f(/)x1                             70(p)x2 5d(])x2 61(a)x2 25(%)x1 +2u  DIFFER
   0x0013  2f(/)x1                             61(a)x2 5f(_)x2 40(@)x1 5d(])x1 +3u  DIFFER
   0x0014  2e(.)x1                             64(d)x2 70(p)x2 5d(])x1 40(@)x1 +3u  DIFFER
   0x0015  69(i)x1                             64(d)x2 5d(])x2 61(a)x2 25(%)x1 +2u  DIFFER
   0x0016  61(a)x1                             69(i)x2 64(d)x2 a3(.)x1 5d(])x1 +3u  DIFFER
   0x0017  35(5)x1                             64(d)x2 6e(n)x1 67(g)x1 5d(])x1 +4u  DIFFER
   0x0018  6f(o)x1                             5d(])x2 69(i)x2 67(g)x1 5f(_)x1 +3u  DIFFER
   0x0019  72(r)x1                             5d(])x2 6e(n)x2 5f(_)x1 6d(m)x1 +3u  DIFFER
   0x001a  67(g)x1                             5d(])x3 67(g)x2 6d(m)x1 6f(o)x1 +2u  PARTIAL
   0x001b  5b([)x1                             5d(])x2 5f(_)x2 6f(o)x1 64(d)x1 +3u  DIFFER
   0x001c  2e(.)x1                             64(d)x3 6d(m)x2 65(e)x1 5d(])x1 +2u  DIFFER
   0x001d  ad(.)x1                             65(e)x2 6f(o)x2 00(.)x1 69(i)x1 +3u  DIFFER
   0x001e  db(.)x1                             00(.)x3 64(d)x2 20( )x1 69(i)x1 +2u  DIFFER
   0x001f  77(w)x1                             20( )x3 00(.)x3 65(e)x2             DIFFER
   0x0020  2f(/)x1                             00(.)x5 2d(-)x1 20( )x1 41(A)x1     DIFFER
   0x0021  f7(.)x1                             2d(-)x3 20( )x2 00(.)x1 25(%)x1     DIFFER
   0x0022  f7(.)x1                             00(.)x2 2d(-)x1 45(E)x1             DIFFER
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
  prompts_b/curl_527.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 527,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 527 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 527 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 527 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).