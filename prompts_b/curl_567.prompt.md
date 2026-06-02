==== BLOCKER ====
Target: curl
Branch ID: 567
Location: /src/curl_fuzzer/curl_fuzzer.cc:385:13
Enclosing function: fuzz_handle_transfer(fuzz_data*)
Source line:     else if(rc == 0) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    2        8          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        2        8          0  REFERENCE
naive_ngram4                     1        9          0  REFERENCE
mopt                             0        9          1  REFERENCE
minimizer                        4        6          0  REFERENCE
fast                             6        4          0  REFERENCE
grimoire                         9        1          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=5.10h  loser=20.30h
  avg hitcount on branch: winner=10  loser=1
  prob_div=0.80  dur_div=15.20h  hit_div=9
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002
--- Pair 2: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=9.10h  loser=11.80h
  avg hitcount on branch: winner=4  loser=1
  prob_div=0.60  dur_div=2.70h  hit_div=3
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/567/{W,L}/branch_coverage_show.txt

--- Enclosing function: fuzz_handle_transfer(fuzz_data*) (/src/curl_fuzzer/curl_fuzzer.cc:309-430) ---
[ ]   307   */
[ ]   308  int fuzz_handle_transfer(FUZZ_DATA *fuzz)
[B]   309  {
[B]   310    int rc = 0;
[B]   311    CURLM *multi_handle;
[B]   312    int still_running; /* keep number of running handles */
[B]   313    CURLMsg *msg; /* for picking up messages with the transfer status */
[B]   314    int msgs_left; /* how many messages are left */
[B]   315    int double_timeout = 0;
[B]   316    fd_set fdread;
[B]   317    fd_set fdwrite;
[B]   318    fd_set fdexcep;
[B]   319    struct timeval timeout;
[B]   320    int select_rc;
[B]   321    CURLMcode mc;
[B]   322    int maxfd = -1;
[B]   323    long curl_timeo = -1;
[B]   324    int ii;
[B]   325    FUZZ_SOCKET_MANAGER *sman[FUZZ_NUM_CONNECTIONS];
[ ]   326  
[B]   327    for(ii = 0; ii < FUZZ_NUM_CONNECTIONS; ii++) {
[B]   328      sman[ii] = &fuzz->sockman[ii];
[ ]   329  
[ ]   330      /* Set up the starting index for responses. */
[B]   331      sman[ii]->response_index = 1;
[B]   332    }
[ ]   333  
[ ]   334    /* init a multi stack */
[B]   335    multi_handle = curl_multi_init();
[ ]   336  
[ ]   337    /* add the individual transfers */
[B]   338    curl_multi_add_handle(multi_handle, fuzz->easy);
[ ]   339  
[ ]   340    /* Do an initial process. This might end the transfer immediately. */
[B]   341    curl_multi_perform(multi_handle, &still_running);
[B]   342    FV_PRINTF(fuzz,
[B]   343              "FUZZ: Initial perform; still running? %d \n",
[B]   344              still_running);
[ ]   345  
[B]   346    while(still_running) {
[ ]   347      /* Reset the sets of file descriptors. */
[B]   348      FD_ZERO(&fdread);
[B]   349      FD_ZERO(&fdwrite);
[B]   350      FD_ZERO(&fdexcep);
[ ]   351  
[ ]   352      /* Set a timeout of 10ms. This is lower than recommended by the multi guide
[ ]   353         but we're not going to any remote servers, so everything should complete
[ ]   354         very quickly. */
[B]   355      timeout.tv_sec = 0;
[B]   356      timeout.tv_usec = 10000;
[ ]   357  
[ ]   358      /* get file descriptors from the transfers */
[B]   359      mc = curl_multi_fdset(multi_handle, &fdread, &fdwrite, &fdexcep, &maxfd);
[B]   360      if(mc != CURLM_OK) {
[ ]   361        fprintf(stderr, "curl_multi_fdset() failed, code %d.\n", mc);
[ ]   362        rc = -1;
[ ]   363        break;
[ ]   364      }
[ ]   365  
[B]   366      for(ii = 0; ii < FUZZ_NUM_CONNECTIONS; ii++) {
[ ]   367        /* Add the socket FD into the readable set if connected. */
[B]   368        if(sman[ii]->fd_state == FUZZ_SOCK_OPEN) {
[B]   369          FD_SET(sman[ii]->fd, &fdread);
[ ]   370  
[ ]   371          /* Work out the maximum FD between the cURL file descriptors and the
[ ]   372             server FD. */
[B]   373          maxfd = FUZZ_MAX(sman[ii]->fd, maxfd);
[B]   374        }
[B]   375      }
[ ]   376  
[ ]   377      /* Work out what file descriptors need work. */
[B]   378      rc = fuzz_select(maxfd + 1, &fdread, &fdwrite, &fdexcep, &timeout);
[ ]   379  
[B]   380      if(rc == -1) {
[ ]   381        /* Had an issue while selecting a file descriptor. Let's just exit. */
[ ]   382        FV_PRINTF(fuzz, "FUZZ: select failed, exiting \n");
[ ]   383        break;
[ ]   384      }
[B]   385      else if(rc == 0) { <-- BLOCKER
[W]   386        FV_PRINTF(fuzz,
[W]   387                  "FUZZ: Timed out; double timeout? %d \n",
[W]   388                  double_timeout);
[ ]   389  
[ ]   390        /* Timed out. */
[W]   391        if(double_timeout == 1) {
[ ]   392          /* We don't expect multiple timeouts in a row. If there are double
[ ]   393             timeouts then exit. */
[W]   394          break;
[W]   395        }
[W]   396        else {
[ ]   397          /* Set the timeout flag for the next time we select(). */
[W]   398          double_timeout = 1;
[W]   399        }
[W]   400      }
[B]   401      else {
[ ]   402        /* There's an active file descriptor. Reset the timeout flag. */
[B]   403        double_timeout = 0;
[B]   404      }
[ ]   405  
[ ]   406      /* Check to see if a server file descriptor is readable. If it is,
[ ]   407         then send the next response from the fuzzing data. */
[B]   408      for(ii = 0; ii < FUZZ_NUM_CONNECTIONS; ii++) {
[B]   409        if(sman[ii]->fd_state == FUZZ_SOCK_OPEN &&
[B]   410           FD_ISSET(sman[ii]->fd, &fdread)) {
[B]   411          rc = fuzz_send_next_response(fuzz, sman[ii]);
[B]   412          if(rc != 0) {
[ ]   413            /* Failed to send a response. Break out here. */
[ ]   414            break;
[ ]   415          }
[B]   416        }
[B]   417      }
[ ]   418  
[B]   419      curl_multi_perform(multi_handle, &still_running);
[B]   420    }
[ ]   421  
[ ]   422    /* Remove the easy handle from the multi stack. */
[B]   423    curl_multi_remove_handle(multi_handle, fuzz->easy);
[ ]   424  
[ ]   425    /* Clean up the multi handle - the top level function will handle the easy
[ ]   426       handle. */
[B]   427    curl_multi_cleanup(multi_handle);
[ ]   428  
[B]   429    return(rc);
[B]   430  }

--- No 1-hop callers of fuzz_handle_transfer(fuzz_data*) fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  fuzz_handle_transfer(fuzz_data*)  (/src/curl_fuzzer/curl_fuzzer.cc:309-430) ---
  d=1   L 346  T=12 F=0  T=7 F=7  while(still_running) {
  d=1   L 385  T=8 F=4  T=0 F=7  else if(rc == 0) {  <-- BLOCKER
  d=1   L 391  T=4 F=4  T=0 F=0  if(double_timeout == 1) {

[off-chain: 3 additional divergent branches across 3 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=5d9ce7f391be0a62, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=7349s, mutation_op=BytesDeleteMutator,BitFlipMutator,TokenReplace,BytesDeleteMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 4b 2f 25 3a 3a 3a   ......pop3K/%:::
  0010: 3a 3a 3a 3a 3a 3a 3a 39 30 30 00 ad 38 35 30 00   :::::::900..850.
  0020: 11 00 00 00 47 48 54 54 50 2f 20 6d 65 40 6c 6f   ....GHTTP/ me@lo
  0030: 6d 65 77 68 65 72 65 0d 0a 54 72 61 6e 32 66 65   mewhere..Tran2fe
Seed 2 (id=faf6b58d07527f1a, size=140 bytes, fuzzer=cmplog, trial=2, discovered_at=32307s, mutation_op=WordInterestingMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 26 2f 2f 70 4d 37   ......pop3&//pM7
  0010: 2e ff 2e 30 2e 31 3a 39 30 30 31 3f 38 35 30 00   ...0.1:9001?850.
  0020: 12 00 00 00 47 00 72 00 6d 3a 20 6d 65 40 37 6f   ....G.r.m: me@7o
  0030: 6d 65 77 68 38 3d 65 00 00 54 00 3a 20 66 61 6b   mewh8=e..T.: fak
Seed 3 (id=7ed01751fe602efb, size=140 bytes, fuzzer=cmplog, trial=2, discovered_at=38842s, mutation_op=ByteIncMutator,QwordAddMutator,TokenReplace):
  0000: 00 01 00 00 00 19 70 6f 70 33 26 2f 2f 70 4d 37   ......pop3&//pM7
  0010: 2e ff 2e 30 2e 31 3a 39 30 30 31 3f 38 35 30 00   ...0.1:9001?850.
  0020: 12 00 00 00 47 00 72 00 6d 3a 20 6d 65 40 37 6f   ....G.r.m: me@7o
  0030: 6d 65 77 68 38 3d 65 00 00 54 00 3a 20 66 61 6b   mewh8=e..T.: fak
Seed 4 (id=be54c16922eb9ce7, size=140 bytes, fuzzer=cmplog, trial=2, discovered_at=60490s, mutation_op=BytesSetMutator,BytesCopyMutator,WordInterestingMutator,DwordInterestingMutator):
  0000: 00 01 00 00 00 19 70 6f 64 00 00 00 2f 70 4d 37   ......pod.../pM7
  0010: 2e ff 2e 30 2e 31 3a 39 30 30 31 3f 38 35 30 00   ...0.1:9001?850.
  0020: 12 00 00 00 47 00 72 00 6d 3a 20 6d 65 40 37 6f   ....G.r.m: me@7o
  0030: 6d 65 77 68 38 3d 65 00 00 54 00 3a 20 66 61 6b   mewh8=e..T.: fak

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0f16f47b53372c37, size=44 bytes, fuzzer=naive, trial=1, discovered_at=2045s, mutation_op=ByteAddMutator):
  0000: 00 11 00 00 00 02 2e 2e 00 01 00 00 00 19 25 41   ..............%A
  0010: 32 25 37 37 25 64 43 44 00 04 41 41 25 44 80 35   2%77%dCD..AA%D.5
  0020: 25 41 43 40 26 00 04 41 bc 64 43 43               %AC@&..A.dCC
Seed 2 (id=ed77400117cda475, size=112 bytes, fuzzer=value_profile, trial=1, discovered_at=2892s, mutation_op=BytesSetMutator,DwordAddMutator):
  0000: 00 01 00 00 00 19 70 00 00 01 00 2f 6f 6f 6f 6f   ......p..../oooo
  0010: 6f 6f 6f 6f 6f 6f 6f 39 30 11 31 2f 38 35 30 00   ooooooo90.1/850.
  0020: 11 00 00 00 47 46 72 6f 6d 3a 20 6d 65 40 1d 6f   ....GFrom: me@.o
  0030: 6d 65 92 68 65 59 65 0d 0a 54 6f 16 20 66 61 6b   me.heYe..To. fak
Seed 3 (id=762994fb53824592, size=52 bytes, fuzzer=naive, trial=1, discovered_at=10311s, mutation_op=BytesExpandMutator,ByteFlipMutator,ByteIncMutator):
  0000: 00 11 00 00 00 02 2e 2e 00 11 00 00 00 02 2e 2e   ................
  0010: 00 01 00 00 00 19 25 41 32 25 37 37 25 64 bc 44   ......%A2%77%d.D
  0020: 00 04 41 41 25 44 80 35 25 41 43 40 27 00 04 41   ..AA%D.5%AC@'..A
  0030: bc 43 43 43                                       .CCC
Seed 4 (id=1a9b0278761b1c37, size=44 bytes, fuzzer=naive, trial=1, discovered_at=17851s, mutation_op=QwordAddMutator):
  0000: 00 11 00 00 00 02 2e 2e 00 01 00 00 00 19 25 41   ..............%A
  0010: 26 25 25 63 45 25 25 63 da 74 43 44 25 36 41 41   &%%cE%%c.tCD%6AA
  0020: 25 41 36 40 26 00 04 41 bc 43 43 43               %A6@&..A.CCC
Seed 5 (id=5553deb89867b5d6, size=39 bytes, fuzzer=value_profile, trial=1, discovered_at=27259s, mutation_op=WordInterestingMutator,BytesRandSetMutator,BytesDeleteMutator,ByteInterestingMutator,DwordAddMutator,BytesInsertCopyMutator,ByteIncMutator):
  0000: 00 11 00 00 00 00 00 01 00 00 00 19 72 72 5a 40   ............rrZ@
  0010: 59 59 59 59 3f 59 59 59 5a 5a 5a 72 2d 2d 2d 00   YYYY?YYYZZZr---.
  0020: 80 e6 72 40 59 65 74                              ..r@Yet


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0001  01(.)x4                             11(.)x4 01(.)x3                     PARTIAL
   0x0005  19(.)x4                             02(.)x3 19(.)x3 00(.)x1             PARTIAL
   0x0006  70(p)x4                             2e(.)x3 70(p)x2 00(.)x1 73(s)x1     PARTIAL
   0x0007  6f(o)x4                             2e(.)x3 00(.)x1 01(.)x1 73(s)x1 +1u  PARTIAL
   0x0008  70(p)x3 64(d)x1                     00(.)x5 6c(l)x1 90(.)x1             DIFFER
   0x0009  33(3)x3 00(.)x1                     01(.)x3 11(.)x1 00(.)x1 76(v)x1 +1u  PARTIAL
   0x000a  26(&)x2 4b(K)x1 00(.)x1             00(.)x5 32(2)x1 3a(:)x1             PARTIAL
   0x000b  2f(/)x3 00(.)x1                     00(.)x3 2f(/)x1 19(.)x1 33(3)x1 +1u  PARTIAL
   0x000c  2f(/)x3 25(%)x1                     00(.)x4 6f(o)x1 72(r)x1 2f(/)x1     PARTIAL
   0x000d  70(p)x3 3a(:)x1                     19(.)x2 31(1)x2 6f(o)x1 02(.)x1 +1u  DIFFER
   0x000e  4d(M)x3 3a(:)x1                     25(%)x2 6f(o)x1 2e(.)x1 5a(Z)x1 +2u  DIFFER
   0x000f  37(7)x3 3a(:)x1                     41(A)x2 6f(o)x1 2e(.)x1 40(@)x1 +2u  PARTIAL
   0x0010  2e(.)x3 3a(:)x1                     32(2)x1 6f(o)x1 00(.)x1 26(&)x1 +3u  PARTIAL
   0x0011  ff(.)x3 3a(:)x1                     25(%)x2 6f(o)x1 01(.)x1 59(Y)x1 +2u  PARTIAL
   0x0012  2e(.)x3 3a(:)x1                     2f(/)x2 37(7)x1 6f(o)x1 00(.)x1 +2u  DIFFER
   0x0013  30(0)x3 3a(:)x1                     30(0)x2 37(7)x1 6f(o)x1 00(.)x1 +2u  PARTIAL
   0x0014  2e(.)x3 3a(:)x1                     2e(.)x2 25(%)x1 6f(o)x1 00(.)x1 +2u  PARTIAL
   0x0015  31(1)x3 3a(:)x1                     64(d)x1 6f(o)x1 19(.)x1 25(%)x1 +3u  PARTIAL
   0x0016  3a(:)x4                             25(%)x2 43(C)x1 6f(o)x1 59(Y)x1 +2u  DIFFER
   0x0017  39(9)x4                             44(D)x1 39(9)x1 41(A)x1 63(c)x1 +3u  PARTIAL
   0x0018  30(0)x4                             30(0)x2 00(.)x1 32(2)x1 da(.)x1 +2u  PARTIAL
   0x0019  30(0)x4                             04(.)x1 11(.)x1 25(%)x1 74(t)x1 +3u  PARTIAL
   0x001a  31(1)x3 00(.)x1                     31(1)x2 41(A)x1 37(7)x1 43(C)x1 +2u  PARTIAL
   0x001b  3f(?)x3 ad(.)x1                     2f(/)x2 41(A)x1 37(7)x1 44(D)x1 +2u  DIFFER
   0x001c  38(8)x4                             25(%)x3 38(8)x3 2d(-)x1             PARTIAL
   0x001d  35(5)x4                             35(5)x3 44(D)x1 64(d)x1 36(6)x1 +1u  PARTIAL
   0x001e  30(0)x4                             30(0)x3 80(.)x1 bc(.)x1 41(A)x1 +1u  PARTIAL
   0x001f  00(.)x4                             00(.)x4 35(5)x1 44(D)x1 41(A)x1     PARTIAL
   0x0020  12(.)x3 11(.)x1                     25(%)x2 11(.)x1 00(.)x1 80(.)x1 +2u  PARTIAL
   0x0021  00(.)x4                             00(.)x3 41(A)x2 04(.)x1 e6(.)x1     PARTIAL
   0x0022  00(.)x4                             00(.)x3 43(C)x1 41(A)x1 36(6)x1 +1u  PARTIAL
   0x0023  00(.)x4                             40(@)x3 00(.)x3 41(A)x1             PARTIAL
   0x0024  47(G)x4                             47(G)x3 26(&)x2 25(%)x1 59(Y)x1     PARTIAL
   0x0025  00(.)x3 48(H)x1                     46(F)x3 00(.)x2 44(D)x1 65(e)x1     PARTIAL
   0x0026  72(r)x3 54(T)x1                     72(r)x3 04(.)x2 80(.)x1 74(t)x1     PARTIAL
   0x0027  00(.)x3 54(T)x1                     41(A)x2 6f(o)x2 35(5)x1 3c(<)x1     DIFFER
   0x0028  6d(m)x3 50(P)x1                     6d(m)x3 bc(.)x2 25(%)x1             PARTIAL
   0x0029  3a(:)x3 2f(/)x1                     3a(:)x3 64(d)x1 41(A)x1 43(C)x1     PARTIAL
   0x002a  20( )x4                             43(C)x3 20( )x3                     PARTIAL
   0x002b  6d(m)x4                             6d(m)x3 43(C)x2 40(@)x1             PARTIAL
   ... (18 more divergent offsets)
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
  prompts_b/curl_567.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 567,
  "target": "curl",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S), cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 567 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 567 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 567 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).