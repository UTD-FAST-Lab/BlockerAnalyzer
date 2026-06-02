==== BLOCKER ====
Target: curl
Branch ID: 42
Location: /src/curl/lib/cookie.c:404:11
Enclosing function: cookie.c:remove_expired
Source line:     while(co) {
Globally blocked side: T  (true branch)

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
  avg duration blocked: winner=4.20h  loser=24.00h
  avg hitcount on branch: winner=249  loser=0
  prob_div=1.00  dur_div=19.80h  hit_div=249
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.40h  loser=24.00h
  avg hitcount on branch: winner=237  loser=0
  prob_div=1.00  dur_div=20.60h  hit_div=237
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/42/{W,L}/branch_coverage_show.txt

--- Enclosing function: cookie.c:remove_expired (/src/curl/lib/cookie.c:382-428) ---
[ ]   380   */
[ ]   381  static void remove_expired(struct CookieInfo *cookies)
[B]   382  {
[B]   383    struct Cookie *co, *nx;
[B]   384    curl_off_t now = (curl_off_t)time(NULL);
[B]   385    unsigned int i;
[ ]   386  
[ ]   387    /*
[ ]   388     * If the earliest expiration timestamp in the jar is in the future we can
[ ]   389     * skip scanning the whole jar and instead exit early as there won't be any
[ ]   390     * cookies to evict.  If we need to evict however, reset the next_expiration
[ ]   391     * counter in order to track the next one. In case the recorded first
[ ]   392     * expiration is the max offset, then perform the safe fallback of checking
[ ]   393     * all cookies.
[ ]   394     */
[B]   395    if(now < cookies->next_expiration &&
[B]   396        cookies->next_expiration != CURL_OFF_T_MAX)
[ ]   397      return;
[B]   398    else
[B]   399      cookies->next_expiration = CURL_OFF_T_MAX;
[ ]   400  
[B]   401    for(i = 0; i < COOKIE_HASH_SIZE; i++) {
[B]   402      struct Cookie *pv = NULL;
[B]   403      co = cookies->cookies[i];
[B]   404      while(co) { <-- BLOCKER
[W]   405        nx = co->next;
[W]   406        if(co->expires && co->expires < now) {
[ ]   407          if(!pv) {
[ ]   408            cookies->cookies[i] = co->next;
[ ]   409          }
[ ]   410          else {
[ ]   411            pv->next = co->next;
[ ]   412          }
[ ]   413          cookies->numcookies--;
[ ]   414          freecookie(co);
[ ]   415        }
[W]   416        else {
[ ]   417          /*
[ ]   418           * If this cookie has an expiration timestamp earlier than what we've
[ ]   419           * seen so far then record it for the next round of expirations.
[ ]   420           */
[W]   421          if(co->expires && co->expires < cookies->next_expiration)
[ ]   422            cookies->next_expiration = co->expires;
[W]   423          pv = co;
[W]   424        }
[W]   425        co = nx;
[W]   426      }
[B]   427    }
[B]   428  }

--- Caller (1 hop): Curl_cookie_add (/src/curl/lib/cookie.c:494-1207, calls cookie.c:remove_expired at line 1040) (±10 around call site) ---
[W]  1030    co->creationtime = ++c->lastct;
[ ]  1031  
[ ]  1032    /*
[ ]  1033     * Now we have parsed the incoming line, we must now check if this supersedes
[ ]  1034     * an already existing cookie, which it may if the previous have the same
[ ]  1035     * domain and path as this.
[ ]  1036     */
[ ]  1037  
[ ]  1038    /* at first, remove expired cookies */
[W]  1039    if(!noexpire)
[W]  1040      remove_expired(c); <-- CALL
[ ]  1041  
[ ]  1042  #ifdef USE_LIBPSL
[ ]  1043    /*
[ ]  1044     * Check if the domain is a Public Suffix and if yes, ignore the cookie. We
[ ]  1045     * must also check that the data handle isn't NULL since the psl code will
[ ]  1046     * dereference it.
[ ]  1047     */
[ ]  1048    if(data && (domain && co->domain && !Curl_host_is_ipnum(co->domain))) {
[ ]  1049      const psl_ctx_t *psl = Curl_psl_use(data);
[ ]  1050      int acceptable;

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  Curl_cookie_add  (/src/curl/lib/cookie.c:494-1207, calls cookie.c:remove_expired at line 1040)
hop 2  Curl_cookie_init  (/src/curl/lib/cookie.c:1227-1320, calls cookie.c:remove_expired at line 1297)
hop 3  Curl_http_header  (/src/curl/lib/http.c:3451-3765, calls Curl_cookie_add at line 3641)
hop 3  Curl_vsetopt  (/src/curl/lib/setopt.c:190-3117, calls Curl_cookie_add at line 863)
hop 4  Curl_http_readwrite_headers  (/src/curl/lib/http.c:3904-4466, calls Curl_http_header at line 4434)
hop 4  curl_easy_setopt  (/src/curl/lib/setopt.c:3129-3142, calls Curl_vsetopt at line 3138)
hop 5  doh.c:dohprobe  (/src/curl/lib/doh.c:219-354, calls curl_easy_setopt at line 330)
hop 5  transfer.c:readwrite_data  (/src/curl/lib/transfer.c:520-878, calls Curl_http_readwrite_headers at line 633)
hop 6  Curl_doh  (/src/curl/lib/doh.c:365-418, calls doh.c:dohprobe at line 392)
hop 6  Curl_readwrite  (/src/curl/lib/transfer.c:1167-1340, calls transfer.c:readwrite_data at line 1219)
hop 7  Curl_resolv  (/src/curl/lib/hostip.c:648-814, calls Curl_doh at line 766)
hop 7  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661, calls Curl_readwrite at line 2405)
hop 8  curl_multi_perform  (/src/curl/lib/multi.c:2665-2716, calls multi.c:multi_runsingle at line 2683)
hop 8  multi.c:multi_socket  (/src/curl/lib/multi.c:3101-3208, calls multi.c:multi_runsingle at line 3158)
hop 8  Curl_SOCKS4  (/src/curl/lib/socks.c:197-483, calls Curl_resolv at line 244)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      40         0  cookie.c:invalid_octets  (/src/curl/lib/cookie.c:454-466)
      40        13  cookie.c:cookiehash  (/src/curl/lib/cookie.c:279-288)
      20         0  cookie.c:freecookie  (/src/curl/lib/cookie.c:113-123)
      20         0  cookie.c:sanitize_cookie_path  (/src/curl/lib/cookie.c:294-324)
      20         0  Curl_cookie_add  (/src/curl/lib/cookie.c:494-1207)
      20         0  cookie.c:get_netscape_format  (/src/curl/lib/cookie.c:1625-1648)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  Curl_cookie_add  (/src/curl/lib/cookie.c:494-1207) ---
  d=2   L 510  T=0 F=20  T=0 F=0  if(data->req.setcookies >= MAX_SET_COOKIE_AMOUNT)
  d=2   L 515  T=0 F=20  T=0 F=0  if(!co)
  d=2   L 518  T=20 F=0  T=0 F=0  if(httpheader) {
  d=2   L 526  T=0 F=20  T=0 F=0  if(linelength > MAX_COOKIE_LINE) {
  d=2   L 534  T=28 F=0  T=0 F=0  while(*lineptr && ISBLANK(*lineptr))
  d=2   L 541  T=33 F=10  T=0 F=0  if(1 <= sscanf(ptr, "%" MAX_NAME_TXT "[^;\t\r\n=] =%"
  d=2   L 561  T=0 F=33  T=0 F=0  if(nlen >= (MAX_NAME-1) || len >= (MAX_NAME-1) ||
  d=2   L 561  T=0 F=33  T=0 F=0  if(nlen >= (MAX_NAME-1) || len >= (MAX_NAME-1) ||
  d=2   L 562  T=0 F=33  T=0 F=0  ((nlen + len) > MAX_NAME)) {
  d=2   L 570  T=21 F=12  T=0 F=0  sep = (*endofn == '=')?TRUE:FALSE;
  d=2   L 572  T=33 F=0  T=0 F=0  if(nlen) {
  d=2   L 576  T=14 F=0  T=0 F=0  while(*endofn && ISBLANK(*endofn) && nlen) {
  d=2   L 576  T=27 F=0  T=0 F=0  while(*endofn && ISBLANK(*endofn) && nlen) {
  d=2   L 585  T=31 F=12  T=0 F=0  while(len && ISBLANK(what[len-1])) {
  d=2   L 592  T=28 F=12  T=0 F=0  while(*whatptr && ISBLANK(*whatptr))
  d=2   L 596  T=0 F=33  T=0 F=0  if(strchr(whatptr, '\t')) {
  d=2   L 608  T=1 F=28  T=0 F=0  if(nlen > 3 && name[0] == '_' && name[1] == '_') {
  d=2   L 608  T=0 F=1  T=0 F=0  if(nlen > 3 && name[0] == '_' && name[1] == '_') {
  d=2   L 608  T=29 F=4  T=0 F=0  if(nlen > 3 && name[0] == '_' && name[1] == '_') {
  d=2   L 615  T=20 F=13  T=0 F=0  if(!co->name) {
  d=2   L 617  T=0 F=20  T=0 F=0  if(!sep) {
  d=2   L 625  T=0 F=20  T=0 F=0  if(!co->name || !co->value) {
  d=2   L 625  T=0 F=20  T=0 F=0  if(!co->name || !co->value) {
  d=2   L 629  T=0 F=20  T=0 F=0  if(invalid_octets(whatptr) || invalid_octets(name)) {
  d=2   L 629  T=0 F=20  T=0 F=0  if(invalid_octets(whatptr) || invalid_octets(name)) {
  d=2   L 635  T=12 F=1  T=0 F=0  else if(!len) {
  d=2   L 657  T=0 F=12  T=0 F=0  else if(sep)
  d=2   L 661  T=32 F=1  T=0 F=0  if(done)
  d=2   L 760  T=12 F=31  T=0 F=0  if(!semiptr || !*semiptr) {
  d=2   L 760  T=8 F=23  T=0 F=0  if(!semiptr || !*semiptr) {
  d=2   L 767  T=29 F=0  T=0 F=0  while(*ptr && ISBLANK(*ptr))
  d=2   L 771  T=8 F=0  T=0 F=0  if(!semiptr && *ptr)
  d=2   L 771  T=8 F=15  T=0 F=0  if(!semiptr && *ptr)
  d=2   L 777  T=23 F=20  T=0 F=0  } while(semiptr);
  d=2   L 779  T=0 F=20  T=0 F=0  if(co->maxage) {
  d=2   L 798  T=0 F=20  T=0 F=0  else if(co->expirestr) {
  d=2   L 815  T=20 F=0  T=0 F=0  if(!badcookie && !co->domain) {
  d=2   L 815  T=20 F=0  T=0 F=0  if(!badcookie && !co->domain) {
  d=2   L 816  T=20 F=0  T=0 F=0  if(domain) {
  d=2   L 819  T=0 F=20  T=0 F=0  if(!co->domain)
  d=2   L 824  T=20 F=0  T=0 F=0  if(!badcookie && !co->path && path) {
  d=2   L 824  T=20 F=0  T=0 F=0  if(!badcookie && !co->path && path) {
  d=2   L 824  T=20 F=0  T=0 F=0  if(!badcookie && !co->path && path) {
  d=2   L 837  T=20 F=0  T=0 F=0  if(!queryp)
  d=2   L 841  T=20 F=0  T=0 F=0  if(endslash) {
  d=2   L 844  T=20 F=0  T=0 F=0  if(co->path) {
  d=2   L 848  T=0 F=20  T=0 F=0  if(!co->spath)
  d=2   L 860  T=0 F=20  T=0 F=0  if(badcookie || !co->name) {
  d=2   L 860  T=0 F=20  T=0 F=0  if(badcookie || !co->name) {
  d=2   L1002  T=0 F=20  T=0 F=0  if(co->prefix & COOKIE_PREFIX__SECURE) {
  d=2   L1009  T=0 F=20  T=0 F=0  if(co->prefix & COOKIE_PREFIX__HOST) {
  d=2   L1022  T=0 F=20  T=0 F=0  if(!c->running &&    /* read from a file */
  d=2   L1039  T=20 F=0  T=0 F=0  if(!noexpire)
  d=2   L1071  T=0 F=20  T=0 F=0  while(clist) {
  d=2   L1159  T=0 F=20  T=0 F=0  if(replace_co) {
  d=2   L1183  T=20 F=0  T=0 F=0  if(c->running)
  d=2   L1187  T=0 F=20  T=0 F=0  replace_old?"Replaced":"Added", co->name, co->value,
  d=2   L1190  T=20 F=0  T=0 F=0  if(!replace_old) {
  d=2   L1192  T=0 F=20  T=0 F=0  if(lastc)
  d=2   L1203  T=0 F=20  T=0 F=0  if(co->expires && (co->expires < c->next_expiration))
--- d=1  cookie.c:remove_expired  (/src/curl/lib/cookie.c:382-428) ---
  d=1   L 404  T=20 F=15300  T=0 F=10200  while(co) {  <-- BLOCKER
  d=1   L 406  T=0 F=20  T=0 F=0  if(co->expires && co->expires < now) {
  d=1   L 421  T=0 F=20  T=0 F=0  if(co->expires && co->expires < cookies->next_expiration)

[off-chain: 28 additional divergent branches across 6 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=2b428b2993f47feb, size=109 bytes, fuzzer=cmplog, trial=1, discovered_at=7643s, mutation_op=ByteAddMutator,BytesSetMutator,DwordInterestingMutator,BytesRandInsertMutator,DwordAddMutator,ByteInterestingMutator,BytesInsertCopyMutator):
  0000: 00 01 00 00 00 19 70 6f 70 00 3a 2f 2f 31 32 00   ......pop.://12.
  0010: 00 30 28 28 2e 31 3a 39 30 30 31 72 38 35 30 00   .0((.1:9001r850.
  0020: 02 00 00 00 47 48 54 54 50 2f 09 6d 65 40 06 24   ....GHTTP/.me@.$
  0030: 65 63 8e 65 74 72 65 0d 0a 53 65 74 2d 43 6f 6f   ec.etre..Set-Coo
Seed 2 (id=577566704525e25b, size=123 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=14217s, mutation_op=BytesDeleteMutator,ByteRandMutator):
  0000: 00 01 00 00 00 19 70 6f 70 71 4b 2f 3a 3a 3a 3a   ......popqK/::::
  0010: 3a 3a 3a 3a 3a 3a 3a 39 30 30 31 ad 38 35 30 00   :::::::9001.850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 40 6c 6f   ....GHTTP/ me@lo
  0030: 6d 65 77 68 65 23 65 0d 0a 53 65 74 2d 43 6f 6f   mewhe#e..Set-Coo
Seed 3 (id=206d29fa3555ad49, size=109 bytes, fuzzer=cmplog, trial=1, discovered_at=22580s, mutation_op=ByteIncMutator):
  0000: 00 01 00 00 00 19 70 6f 70 00 3a 2f 2f 31 32 00   ......pop.://12.
  0010: 00 30 28 28 2e 31 3a 39 30 30 31 72 38 35 30 00   .0((.1:9001r850.
  0020: 02 00 00 00 47 48 54 54 50 2f 09 6d 65 40 06 24   ....GHTTP/.me@.$
  0030: 65 63 8e 65 74 72 65 0d 0a 53 65 74 2d 43 6f 6f   ec.etre..Set-Coo
Seed 4 (id=312f8211efce9c2c, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=29272s, mutation_op=BytesDeleteMutator,TokenInsert,ByteIncMutator,BytesInsertCopyMutator):
  0000: 00 01 00 00 00 19 70 6f 70 71 94 94 94 94 94 94   ......popq......
  0010: 94 94 94 3a c5 3a 3a 39 30 30 31 ad 38 40 30 00   ...:.::9001.8@0.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 40 6c 6f   ....GHTTP/ me@lo
  0030: 6d 65 77 68 65 23 65 0d 0a 53 65 74 2d 43 6f 6f   mewhe#e..Set-Coo
Seed 5 (id=6820d797c493b782, size=123 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=29768s, mutation_op=BytesDeleteMutator,CrossoverInsertMutator,BytesInsertCopyMutator):
  0000: 00 01 00 00 00 19 71 6f 70 71 4b 2f 3a 3a 3a 3a   ......qopqK/::::
  0010: 3a 3a 3a 3a 3a 3a 3a 39 30 30 31 ad 38 35 30 00   :::::::9001.850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 40 6c 6f   ....GHTTP/ me@lo
  0030: 6d 65 77 68 65 23 65 0d 0a 53 65 74 2d 43 6f 6f   mewhe#e..Set-Coo

==== Loser-blocking seeds (take false branch) ====
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
   0x0007  6f(o)x16 00(.)x2 db(.)x1 2e(.)x1    55(U)x2 2e(.)x2 25(%)x2 62(b)x2 +12u  PARTIAL
   0x0012  3a(:)x12 28(()x4 94(.)x3 69(i)x1    25(%)x3 41(A)x2 4b(K)x1 65(e)x1 +13u  DIFFER
   0x0015  3a(:)x10 54(T)x6 31(1)x3 e6(.)x1    25(%)x5 41(A)x2 1f(.)x1 64(d)x1 +11u  DIFFER
   0x0016  3a(:)x19 e6(.)x1                    41(A)x3 64(d)x3 42(B)x2 25(%)x2 +10u  DIFFER
   0x0017  39(9)x19 e6(.)x1                    41(A)x3 25(%)x2 2e(.)x2 1f(.)x1 +12u  DIFFER
   0x0018  30(0)x19 e6(.)x1                    41(A)x3 43(C)x3 00(.)x2 25(%)x2 +10u  DIFFER
   0x0019  30(0)x19 e6(.)x1                    25(%)x3 40(@)x2 45(E)x2 2e(.)x2 +10u  DIFFER
   0x001a  31(1)x18 e6(.)x1 50(P)x1            25(%)x5 41(A)x3 2f(/)x2 66(f)x2 +8u  DIFFER
   0x001b  72(r)x9 ad(.)x9 e6(.)x1 00(.)x1     2e(.)x3 25(%)x3 2d(-)x2 2f(/)x1 +11u  PARTIAL
   0x001c  38(8)x20                            2f(/)x2 2e(.)x2 45(E)x2 5a(Z)x1 +13u  DIFFER
   0x001d  35(5)x17 40(@)x3                    2e(.)x2 2d(-)x2 25(%)x2 62(b)x2 +12u  DIFFER
   0x001e  30(0)x19 7a(z)x1                    25(%)x4 00(.)x2 65(e)x2 44(D)x2 +10u  DIFFER
   0x001f  00(.)x20                            2e(.)x4 25(%)x3 00(.)x2 72(r)x2 +8u  PARTIAL
   0x0020  02(.)x20                            65(e)x2 2e(.)x2 42(B)x2 6d(m)x1 +12u  DIFFER
   0x0021  00(.)x20                            2d(-)x3 25(%)x2 00(.)x2 62(b)x2 +8u  PARTIAL
   0x0022  00(.)x20                            44(D)x2 00(.)x2 2e(.)x2 74(t)x1 +10u  PARTIAL
   0x0023  00(.)x20                            2e(.)x3 62(b)x2 25(%)x2 d6(.)x1 +7u  PARTIAL
   0x0024  47(G)x20                            50(P)x2 42(B)x1 9e(.)x1 2f(/)x1 +7u  DIFFER
   0x0025  48(H)x19 68(h)x1                    25(%)x3 2e(.)x2 41(A)x2 64(d)x1 +4u  DIFFER
   0x0026  54(T)x19 74(t)x1                    45(E)x2 41(A)x1 2f(/)x1 25(%)x1 +7u  DIFFER
   0x0027  54(T)x19 74(t)x1                    72(r)x1 27(')x1 00(.)x1 40(@)x1 +8u  DIFFER
   0x0028  50(P)x19 70(p)x1                    25(%)x5 33(3)x1 db(.)x1 2f(/)x1 +4u  PARTIAL
   0x0029  2f(/)x20                            25(%)x2 41(A)x2 31(1)x1 2f(/)x1 +6u  PARTIAL
   0x002a  20( )x16 09(.)x3 98(.)x1            25(%)x4 65(e)x1 2e(.)x1 42(B)x1 +4u  DIFFER
   0x002b  6d(m)x19 98(.)x1                    25(%)x5 2e(.)x2 4b(K)x1 66(f)x1 +2u  DIFFER
   0x002c  65(e)x20                            25(%)x3 65(e)x2 d2(.)x1 2e(.)x1 +4u  PARTIAL
   0x002d  40(@)x20                            25(%)x2 43(C)x1 ff(.)x1 2e(.)x1 +6u  PARTIAL
   0x002e  06(.)x10 6c(l)x8 2d(-)x2            25(%)x4 26(&)x1 2e(.)x1 45(E)x1 +3u  DIFFER
   0x002f  24($)x10 6f(o)x10                   25(%)x2 55(U)x1 2e(.)x1 44(D)x1 +5u  DIFFER
   0x0030  65(e)x10 6d(m)x10                   25(%)x2 62(b)x2 43(C)x1 2e(.)x1 +4u  DIFFER
   0x0031  63(c)x10 65(e)x10                   62(b)x2 25(%)x1 db(.)x1 2e(.)x1 +4u  DIFFER
   0x0032  8e(.)x10 77(w)x10                   25(%)x3 b5(.)x1 2e(.)x1 42(B)x1 +3u  DIFFER
   0x0033  65(e)x10 68(h)x10                   25(%)x3 2e(.)x2 41(A)x2 bd(.)x1 +1u  DIFFER
   0x0034  74(t)x10 65(e)x10                   25(%)x4 45(E)x2 2e(.)x1 e2(.)x1 +1u  PARTIAL
   0x0035  72(r)x10 23(#)x10                   25(%)x3 66(f)x2 4f(O)x1 44(D)x1 +2u  DIFFER
   0x0036  65(e)x20                            25(%)x6 4e(N)x1 45(E)x1             DIFFER
   0x0037  0d(.)x20                            25(%)x2 65(e)x2 11(.)x1 42(B)x1 +2u  DIFFER
   0x0038  0a(.)x20                            25(%)x3 42(B)x2 80(.)x1 45(E)x1 +1u  DIFFER
   0x0039  53(S)x20                            25(%)x4 62(b)x2 58(X)x1             DIFFER
   ... (6 more divergent offsets)
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
  prompts_b/curl_42.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 42,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 42 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 42 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 42 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).