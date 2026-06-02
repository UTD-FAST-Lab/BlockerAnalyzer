==== BLOCKER ====
Target: curl
Branch ID: 505
Location: /src/curl/lib/url.c:4271:8
Enclosing function: Curl_init_do
Source line:     if(data->state.wildcardmatch &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            3        7          0  REFERENCE
cmplog                          10        0          0  REFERENCE
value_profile                    1        9          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             9        1          0  winner (I2S vs value_profile)
naive_ctx                        8        2          0  REFERENCE
naive_ngram4                     5        5          0  REFERENCE
mopt                             4        6          0  REFERENCE
minimizer                        7        3          0  REFERENCE
fast                             8        2          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=7.20h  loser=22.90h
  avg hitcount on branch: winner=7  loser=0
  prob_div=0.80  dur_div=15.70h  hit_div=7
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/505/{W,L}/branch_coverage_show.txt

--- Enclosing function: Curl_init_do (/src/curl/lib/url.c:4259-4294) ---
[ ]  4257  
[ ]  4258  CURLcode Curl_init_do(struct Curl_easy *data, struct connectdata *conn)
[B]  4259  {
[B]  4260    struct SingleRequest *k = &data->req;
[ ]  4261  
[ ]  4262    /* if this is a pushed stream, we need this: */
[B]  4263    CURLcode result = Curl_preconnect(data);
[B]  4264    if(result)
[ ]  4265      return result;
[ ]  4266  
[B]  4267    if(conn) {
[B]  4268      conn->bits.do_more = FALSE; /* by default there's no curl_do_more() to
[ ]  4269                                     use */
[ ]  4270      /* if the protocol used doesn't support wildcards, switch it off */
[B]  4271      if(data->state.wildcardmatch && <-- BLOCKER
[B]  4272         !(conn->handler->flags & PROTOPT_WILDCARD))
[W]  4273        data->state.wildcardmatch = FALSE;
[B]  4274    }
[ ]  4275  
[B]  4276    data->state.done = FALSE; /* *_done() is not called yet */
[B]  4277    data->state.expect100header = FALSE;
[ ]  4278  
[B]  4279    if(data->set.opt_no_body)
[ ]  4280      /* in HTTP lingo, no body means using the HEAD request... */
[ ]  4281      data->state.httpreq = HTTPREQ_HEAD;
[ ]  4282  
[B]  4283    k->start = Curl_now(); /* start time */
[B]  4284    k->now = k->start;   /* current time is now */
[B]  4285    k->header = TRUE; /* assume header */
[B]  4286    k->bytecount = 0;
[B]  4287    k->ignorebody = FALSE;
[ ]  4288  
[B]  4289    Curl_speedinit(data);
[B]  4290    Curl_pgrsSetUploadCounter(data, 0);
[B]  4291    Curl_pgrsSetDownloadCounter(data, 0);
[ ]  4292  
[B]  4293    return CURLE_OK;
[B]  4294  }

--- Caller (1 hop): url.c:create_conn (/src/curl/lib/url.c:3683-4145, calls Curl_init_do at line 4120) (±10 around call site) ---
[B]  4110      if((data->state.authproxy.picked & (CURLAUTH_NTLM | CURLAUTH_NTLM_WB)) &&
[B]  4111         data->state.authproxy.done) {
[ ]  4112        infof(data, "NTLM-proxy picked AND auth done set, clear picked");
[ ]  4113        data->state.authproxy.picked = CURLAUTH_NONE;
[ ]  4114        data->state.authproxy.done = FALSE;
[ ]  4115      }
[B]  4116  #endif
[B]  4117    }
[ ]  4118  
[ ]  4119    /* Setup and init stuff before DO starts, in preparing for the transfer. */
[B]  4120    Curl_init_do(data, conn); <-- CALL
[ ]  4121  
[ ]  4122    /*
[ ]  4123     * Setup whatever necessary for a resumed transfer
[ ]  4124     */
[B]  4125    result = setup_range(data);
[B]  4126    if(result)
[ ]  4127      goto out;
[ ]  4128  
[ ]  4129    /* Continue connectdata initialization here. */
[ ]  4130  

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  url.c:create_conn  (/src/curl/lib/url.c:3683-4145, calls Curl_init_do at line 3893)
hop 3  url.c:findprotocol  (/src/curl/lib/url.c:1864-1893, calls url.c:create_conn at line 1888)
hop 3  url.c:resolve_server  (/src/curl/lib/url.c:3572-3586, calls url.c:create_conn at line 3579)
hop 4  url.c:parseurlandfillconn  (/src/curl/lib/url.c:1969-2174, calls url.c:findprotocol at line 2066)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       5         0  curl_multi_fdset  (/src/curl/lib/multi.c:1099-1154)
       5         0  multi.c:add_next_timeout  (/src/curl/lib/multi.c:3055-3094)
       1         4  Curl_parse_login_details  (/src/curl/lib/url.c:2861-2960)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=4  url.c:parseurlandfillconn  (/src/curl/lib/url.c:1969-2174) ---
  d=4   L2074  T=5 F=1  T=10 F=0  if(!data->state.aptr.passwd) {
  d=4   L2076  T=0 F=5  T=0 F=10  if(!uc) {
  d=4   L2088  T=0 F=5  T=0 F=10  else if(uc != CURLUE_NO_PASSWORD)
  d=4   L2100  T=1 F=0  T=4 F=0  conn->handler->flags&PROTOPT_USERPWDCTRL ?
  d=4   L2102  T=0 F=1  T=0 F=4  if(result)
--- d=1  Curl_init_do  (/src/curl/lib/url.c:4259-4294) ---
  d=1   L4271  T=6 F=0  T=0 F=10  if(data->state.wildcardmatch &&  <-- BLOCKER
  d=1   L4272  T=6 F=0  T=0 F=0  !(conn->handler->flags & PROTOPT_WILDCARD))

[off-chain: 66 additional divergent branches across 13 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=7bcbae710a7130dd, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=7946s, mutation_op=BytesDeleteMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 4b 2f 3f 3a 3a 3a   ......pop3K/?:::
  0010: 3a 3a 3a 3a 3a 3a 3a 39 30 30 31 ad 38 35 30 00   :::::::9001.850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 40 6c 6f   ....GHTTP/ me@lo
  0030: 6d 65 77 68 65 72 65 0d 0a 54 72 e0 6e 63 66 65   mewhere..Tr.ncfe
Seed 2 (id=6d700d2eb9984aee, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=11569s, mutation_op=BytesDeleteMutator,ByteNegMutator,BytesDeleteMutator,BytesRandSetMutator,ByteAddMutator,BytesExpandMutator):
  0000: 00 01 00 00 00 19 4d 6f 70 33 40 2e 2f 3f 32 37   ......Mop3@./?27
  0010: 3e 30 2e 30 2e 31 3a 39 30 30 31 2f 56 35 30 00   >0.0.1:9001/V50.
  0020: 16 00 00 00 47 46 42 54 6d 3a 20 6d 65 40 24 6f   ....GFBTm: me@$o
  0030: 6d 65 77 68 65 48 65 0d 0a 54 6f 3a 20 66 61 6b   mewheHe..To: fak
Seed 3 (id=e33ac9c77ad5dd6a, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=15535s, mutation_op=BytesRandInsertMutator,BytesSwapMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 4b 2e 2f 3f 32 37   ......pop3K./?27
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 31 ad 38 35 30 00   .0.0.1:9001.850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 40 6c 6f   ....GHTTP/ me@lo
  0030: 6d 65 77 66 65 72 65 0d 0a 41 6f 3a 05 66 61 6b   mewfere..Ao:.fak
Seed 4 (id=a166388f57a3006b, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=30071s, mutation_op=BytesSetMutator,BitFlipMutator,QwordAddMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 4b 2e 2f 3f 32 37   ......pop3K./?27
  0010: 26 30 2e 30 2e 31 3a 39 30 30 31 ad 38 35 30 00   &0.0.1:9001.850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 40 6c 6f   ....GHTTP/ me@lo
  0030: 6d 65 77 66 65 72 65 0d 0a 52 65 74 72 79 2d 41   mewfere..Retry-A
Seed 5 (id=9dd25f376ba10b2e, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=34595s, mutation_op=ByteAddMutator,ByteFlipMutator,TokenInsert,BitFlipMutator,CrossoverInsertMutator,CrossoverReplaceMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 4b 2e 2f 3f 32 37   ......pop3K./?27
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 31 ad 38 35 30 00   .0.0.1:9001.850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 40 6c 6f   ....GHTTP/ me@lo
  0030: 6d 65 77 66 65 72 65 0d 0a 41 6c 74 2d 53 76 63   mewfere..Alt-Svc

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=003e4994f2c65fcf, size=35 bytes, fuzzer=value_profile, trial=1, discovered_at=22s, mutation_op=QwordAddMutator,WordAddMutator):
  0000: 00 01 00 00 00 19 30 49 2e 2e 51 2e 47 48 2e 2b   ......0I..Q.GH.+
  0010: 80 00 21 47 47 46 0f 00 00 00 f9 ff ff ff 49 62   ..!GGF........Ib
  0020: 7e 05 61                                          ~.a
Seed 2 (id=00225bc4819174d2, size=73 bytes, fuzzer=value_profile, trial=1, discovered_at=152s, mutation_op=BytesInsertMutator,ByteAddMutator,ByteIncMutator,BytesDeleteMutator,ByteDecMutator):
  0000: 00 01 00 00 00 43 64 55 43 25 25 25 25 21 25 65   .....CdUC%%%%!%e
  0010: 26 25 65 24 25 64 45 72 46 25 41 27 25 31 25 25   &%e$%dErF%A'%1%%
  0020: 65 25 44 d6 42 64 45 72 33 25 65 4b 25 43 25 25   e%D.BdEr3%eK%C%%
  0030: 25 25 25 25 25 25 25 25 25 25 25 25 26 25 40 e8   %%%%%%%%%%%%&%@.
Seed 3 (id=001607afc7f08ce7, size=74 bytes, fuzzer=value_profile, trial=1, discovered_at=3913s, mutation_op=BytesCopyMutator):
  0000: 00 01 00 00 00 44 64 55 43 db b5 25 45 66 25 66   .....DdUC..%Ef%f
  0010: 42 62 9e 62 9e 44 64 55 43 db b5 25 45 66 25 66   Bb.b.DdUC..%Ef%f
  0020: 42 62 9e 62 9e 43 41 27 db 31 25 25 25 25 26 55   Bb.b.CA'.1%%%%&U
  0030: 43 db b5 25 45 66 25 65 42 62 9e 66 52 66 25 65   C..%Ef%eBb.fRf%e
Seed 4 (id=00412fff2cf16b82, size=34 bytes, fuzzer=value_profile, trial=1, discovered_at=3918s, mutation_op=BitFlipMutator):
  0000: 00 01 00 00 00 19 71 6e 2f 2f 2f 2e 2e 2f 2e 2f   ......qn///.././
  0010: 2e 2f 2f 2f 2f 2f 2f 2f 2e 2f 21 2e 2f 75 75 75   .///////./!./uuu
  0020: ff 35                                             .5
Seed 5 (id=00224975860e7d7e, size=36 bytes, fuzzer=value_profile, trial=1, discovered_at=4107s, mutation_op=DwordAddMutator,QwordAddMutator,CrossoverReplaceMutator):
  0000: 00 01 00 00 00 19 2e 2d 2b 47 2b 2b 2b 2e 4e 51   .......-+G+++.NQ
  0010: 37 2b 2b 2d 2b 2e 4e 41 59 2b 38 2d 2b 2e 46 25   7++-+.NAY+8-+.F%
  0020: 21 00 00 8d                                       !...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0005  19(.)x6                             19(.)x3 43(C)x3 2e(.)x2 44(D)x1 +1u  PARTIAL
   0x0006  70(p)x5 4d(M)x1                     64(d)x3 2e(.)x3 30(0)x1 71(q)x1 +2u  DIFFER
   0x0007  6f(o)x6                             55(U)x2 2e(.)x2 49(I)x1 6e(n)x1 +4u  DIFFER
   0x0008  70(p)x6                             2e(.)x3 43(C)x2 2f(/)x1 2b(+)x1 +3u  DIFFER
   0x0009  33(3)x6                             25(%)x2 2b(+)x2 2e(.)x1 db(.)x1 +4u  DIFFER
   0x000a  4b(K)x5 40(@)x1                     25(%)x2 2e(.)x2 51(Q)x1 b5(.)x1 +4u  DIFFER
   0x000b  2e(.)x5 2f(/)x1                     25(%)x3 2e(.)x2 2b(+)x1 2d(-)x1 +3u  PARTIAL
   0x000c  2f(/)x5 3f(?)x1                     2e(.)x3 25(%)x2 47(G)x1 45(E)x1 +3u  DIFFER
   0x000d  3f(?)x5 3a(:)x1                     2e(.)x3 48(H)x1 21(!)x1 66(f)x1 +4u  DIFFER
   0x000e  32(2)x5 3a(:)x1                     25(%)x5 2e(.)x4 4e(N)x1             DIFFER
   0x000f  37(7)x5 3a(:)x1                     2e(.)x2 2b(+)x1 65(e)x1 66(f)x1 +5u  DIFFER
   0x0010  2e(.)x3 3a(:)x1 3e(>)x1 26(&)x1     2e(.)x3 42(B)x2 80(.)x1 26(&)x1 +3u  PARTIAL
   0x0011  30(0)x5 3a(:)x1                     25(%)x4 00(.)x1 62(b)x1 2f(/)x1 +3u  DIFFER
   0x0012  2e(.)x5 3a(:)x1                     21(!)x1 65(e)x1 9e(.)x1 2f(/)x1 +6u  PARTIAL
   0x0013  30(0)x5 3a(:)x1                     62(b)x2 47(G)x1 24($)x1 2f(/)x1 +5u  DIFFER
   0x0014  2e(.)x5 3a(:)x1                     25(%)x2 2e(.)x2 47(G)x1 9e(.)x1 +4u  PARTIAL
   0x0015  31(1)x5 3a(:)x1                     46(F)x2 25(%)x2 64(d)x1 44(D)x1 +4u  DIFFER
   0x0016  3a(:)x6                             64(d)x2 0f(.)x1 45(E)x1 2f(/)x1 +5u  DIFFER
   0x0017  39(9)x6                             2e(.)x2 00(.)x1 72(r)x1 55(U)x1 +5u  DIFFER
   0x0018  30(0)x6                             2e(.)x3 00(.)x1 46(F)x1 43(C)x1 +4u  DIFFER
   0x0019  30(0)x6                             25(%)x2 2b(+)x2 00(.)x1 db(.)x1 +4u  DIFFER
   0x001a  31(1)x6                             41(A)x2 f9(.)x1 b5(.)x1 21(!)x1 +5u  DIFFER
   0x001b  ad(.)x5 2f(/)x1                     25(%)x3 2e(.)x2 ff(.)x1 27(')x1 +3u  DIFFER
   0x001c  38(8)x5 56(V)x1                     2e(.)x2 ff(.)x1 25(%)x1 45(E)x1 +5u  DIFFER
   0x001d  35(5)x6                             2e(.)x2 ff(.)x1 31(1)x1 66(f)x1 +5u  DIFFER
   0x001e  30(0)x6                             25(%)x3 49(I)x1 75(u)x1 46(F)x1 +4u  DIFFER
   0x001f  00(.)x6                             25(%)x3 2e(.)x2 62(b)x1 66(f)x1 +3u  DIFFER
   0x0020  02(.)x5 16(.)x1                     42(B)x2 2e(.)x2 7e(~)x1 65(e)x1 +4u  DIFFER
   0x0021  00(.)x6                             05(.)x1 25(%)x1 62(b)x1 35(5)x1 +6u  PARTIAL
   0x0022  00(.)x6                             2e(.)x2 61(a)x1 44(D)x1 9e(.)x1 +4u  PARTIAL
   0x0023  00(.)x6                             2e(.)x2 d6(.)x1 62(b)x1 8d(.)x1 +3u  DIFFER
   0x0024  47(G)x6                             42(B)x1 9e(.)x1 2e(.)x1 44(D)x1 +3u  DIFFER
   0x0025  48(H)x5 46(F)x1                     2e(.)x2 25(%)x2 64(d)x1 43(C)x1 +1u  DIFFER
   0x0026  54(T)x5 42(B)x1                     2e(.)x2 45(E)x1 41(A)x1 42(B)x1 +2u  PARTIAL
   0x0027  54(T)x6                             72(r)x1 27(')x1 2e(.)x1 42(B)x1 +3u  DIFFER
   0x0028  50(P)x5 6d(m)x1                     25(%)x3 2e(.)x2 33(3)x1 db(.)x1     DIFFER
   0x0029  2f(/)x5 3a(:)x1                     25(%)x1 31(1)x1 2e(.)x1 42(B)x1 +3u  DIFFER
   0x002a  20( )x6                             65(e)x1 25(%)x1 2e(.)x1 42(B)x1 +3u  DIFFER
   0x002b  6d(m)x6                             25(%)x2 4b(K)x1 2e(.)x1 66(f)x1 +2u  DIFFER
   0x002c  65(e)x6                             25(%)x2 2e(.)x2 6e(n)x1 45(E)x1 +1u  PARTIAL
   ... (19 more divergent offsets)
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
  prompts_b/curl_505.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 505,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 505 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 505 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 505 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).