==== BLOCKER ====
Target: libxml2
Branch ID: 6869
Location: /src/libxml2/parserInternals.c:309:9
Enclosing function: xmlParserInputGrow
Source line:     if (xmlBufUse(in->buf->buffer) > (unsigned int) indx + INPUT_CHUNK) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            7        3          0  REFERENCE
cmplog                           9        1          0  winner (grimoire_structural vs grimoire)
value_profile                    9        1          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        7        3          0  REFERENCE
naive_ngram4                     9        1          0  REFERENCE
mopt                            10        0          0  REFERENCE
minimizer                        9        1          0  REFERENCE
fast                            10        0          0  REFERENCE
grimoire                         1        9          0  loser (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > grimoire  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=10.30h  loser=22.10h
  avg hitcount on branch: winner=56  loser=45
  prob_div=0.80  dur_div=11.80h  hit_div=10
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6869/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlParserInputGrow (/src/libxml2/parserInternals.c:289-330) ---
[ ]   287   */
[ ]   288  int
[B]   289  xmlParserInputGrow(xmlParserInputPtr in, int len) {
[B]   290      int ret;
[B]   291      size_t indx;
[ ]   292  
[B]   293      if ((in == NULL) || (len < 0)) return(-1);
[ ]   294  #ifdef DEBUG_INPUT
[ ]   295      xmlGenericError(xmlGenericErrorContext, "Grow\n");
[ ]   296  #endif
[B]   297      if (in->buf == NULL) return(-1);
[B]   298      if (in->base == NULL) return(-1);
[B]   299      if (in->cur == NULL) return(-1);
[B]   300      if (in->buf->buffer == NULL) return(-1);
[ ]   301  
[ ]   302      /* Don't grow memory buffers. */
[B]   303      if ((in->buf->encoder == NULL) && (in->buf->readcallback == NULL))
[L]   304          return(0);
[ ]   305  
[B]   306      CHECK_BUFFER(in);
[ ]   307  
[B]   308      indx = in->cur - in->base;
[B]   309      if (xmlBufUse(in->buf->buffer) > (unsigned int) indx + INPUT_CHUNK) { <-- BLOCKER
[ ]   310  
[W]   311  	CHECK_BUFFER(in);
[ ]   312  
[W]   313          return(0);
[W]   314      }
[B]   315      ret = xmlParserInputBufferGrow(in->buf, len);
[ ]   316  
[B]   317      in->base = xmlBufContent(in->buf->buffer);
[B]   318      if (in->base == NULL) {
[ ]   319          in->base = BAD_CAST "";
[ ]   320          in->cur = in->base;
[ ]   321          in->end = in->base;
[ ]   322          return(-1);
[ ]   323      }
[B]   324      in->cur = in->base + indx;
[B]   325      in->end = xmlBufEnd(in->buf->buffer);
[ ]   326  
[B]   327      CHECK_BUFFER(in);
[ ]   328  
[B]   329      return(ret);
[B]   330  }

--- Caller (1 hop): xmlCurrentChar (/src/libxml2/parserInternals.c:558-701, calls xmlParserInputGrow at line 642) (±10 around call site) ---
[W]   632  	    }
[W]   633  	    if (!IS_CHAR(val)) {
[ ]   634  	        xmlErrEncodingInt(ctxt, XML_ERR_INVALID_CHAR,
[ ]   635  				  "Char 0x%X out of allowed range\n", val);
[ ]   636  	    }
[W]   637  	    return(val);
[W]   638  	} else {
[ ]   639  	    /* 1-byte code */
[W]   640  	    *len = 1;
[W]   641  	    if (*ctxt->input->cur == 0)
[W]   642  		xmlParserInputGrow(ctxt->input, INPUT_CHUNK); <-- CALL
[W]   643  	    if ((*ctxt->input->cur == 0) &&
[W]   644  	        (ctxt->input->end > ctxt->input->cur)) {
[W]   645  	        xmlErrEncodingInt(ctxt, XML_ERR_INVALID_CHAR,
[W]   646  				  "Char 0x0 out of allowed range\n", 0);
[W]   647  	    }
[W]   648  	    if (*ctxt->input->cur == 0xD) {
[ ]   649  		if (ctxt->input->cur[1] == 0xA) {
[ ]   650  		    ctxt->input->cur++;
[ ]   651  		}
[ ]   652  		return(0xA);

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094, calls xmlParserInputGrow at line 2085)
hop 2  parser.c:xmlSHRINK  (/src/libxml2/parser.c:2059-2066, calls xmlParserInputGrow at line 2065)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     178      1220  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
     351         0  xmlCurrentChar  (/src/libxml2/parserInternals.c:558-701)
     309         0  xmlCopyCharMultiByte  (/src/libxml2/parserInternals.c:825-854)
       9       108  inputPop  (/src/libxml2/parser.c:1723-1738)
       1        60  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
       7        60  xmlParserInputGrow  (/src/libxml2/parserInternals.c:289-330)  <-- enclosing
       3        36  inputPush  (/src/libxml2/parser.c:1693-1712)
       8        41  xmlParseChunk  (/src/libxml2/parser.c:12135-12300)
       3        36  parser.c:xmlHaltParser  (/src/libxml2/parser.c:12416-12441)
       3        36  parser.c:xmlCtxtUseOptionsInternal  (/src/libxml2/parser.c:14842-14969)
       3        36  xmlSwitchEncoding  (/src/libxml2/parserInternals.c:899-1015)
       3        36  parserInternals.c:xmlSwitchInputEncodingInt  (/src/libxml2/parserInternals.c:1032-1153)
       3        36  xmlFreeInputStream  (/src/libxml2/parserInternals.c:1205-1217)
       3        36  xmlNewInputStream  (/src/libxml2/parserInternals.c:1228-1255)
       3        36  parserInternals.c:xmlInitSAXParserCtxt  (/src/libxml2/parserInternals.c:1477-1659)
... (23 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094) ---
  d=2   L2076  T=0 F=1  T=0 F=60  if (((curEnd > XML_MAX_LOOKUP_LIMIT) ||
  d=2   L2077  T=0 F=1  T=0 F=60  (curBase > XML_MAX_LOOKUP_LIMIT)) &&
  d=2   L2086  T=0 F=1  T=0 F=60  if ((ctxt->input->cur > ctxt->input->end) ||
  d=2   L2087  T=0 F=1  T=0 F=60  (ctxt->input->cur < ctxt->input->base)) {
  d=2   L2092  T=1 F=0  T=60 F=0  if ((ctxt->input->cur != NULL) && (*ctxt->input->cur == 0))
  d=2   L2092  T=0 F=1  T=0 F=60  if ((ctxt->input->cur != NULL) && (*ctxt->input->cur == 0))
--- d=1  xmlParserInputGrow  (/src/libxml2/parserInternals.c:289-330) ---
  d=1   L 293  T=0 F=7  T=0 F=60  if ((in == NULL) || (len < 0)) return(-1);
  d=1   L 293  T=0 F=7  T=0 F=60  if ((in == NULL) || (len < 0)) return(-1);
  d=1   L 297  T=0 F=7  T=0 F=60  if (in->buf == NULL) return(-1);
  d=1   L 298  T=0 F=7  T=0 F=60  if (in->base == NULL) return(-1);
  d=1   L 299  T=0 F=7  T=0 F=60  if (in->cur == NULL) return(-1);
  d=1   L 300  T=0 F=7  T=0 F=60  if (in->buf->buffer == NULL) return(-1);
  d=1   L 303  T=0 F=7  T=12 F=48  if ((in->buf->encoder == NULL) && (in->buf->readcallback ...
  d=1   L 303  T=0 F=0  T=12 F=0  if ((in->buf->encoder == NULL) && (in->buf->readcallback ...
  d=1   L 309  T=6 F=1  T=0 F=48  if (xmlBufUse(in->buf->buffer) > (unsigned int) indx + IN...  <-- BLOCKER
  d=1   L 318  T=0 F=1  T=0 F=48  if (in->base == NULL) {

[off-chain: 511 additional divergent branches across 35 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=9c2cb638eada1a5c, size=458 bytes, fuzzer=cmplog, trial=3, discovered_at=17874s, mutation_op=TokenInsert,BitFlipMutator,BytesCopyMutator,ByteFlipMutator,BytesDeleteMutator):
  0000: 2f 2f 2d 2f 2f 2d 27 2e 3f 3a 5f 5f 28 2c 27 25   //-//-'.?:__(,'%
  0010: 23 5c 5b 61 23 23 9f 2e 40 2e 7e 28 41 3c 37 37   #\[a##..@.~(A<77
  0020: 37 32 56 78 02 6c 5c 0a 3c 00 3f 00 8e 1a 1a 1a   72Vx.l\.<.?.....
  0030: 1a 8e 40 62 3f 78 6d 6c 6e 73 74 78 6c 69 6e 6b   ..@b?xmlnstxlink

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=072de3970265e315, size=13 bytes, fuzzer=grimoire, trial=1, discovered_at=8816s, mutation_op=I2SRandReplace):
  0000: 4c 49 45 44 24 7e 7e 5c 0a fe ff ff 3f            LIED$~~\....?
Seed 2 (id=03d3f32d703e68ad, size=47 bytes, fuzzer=grimoire, trial=1, discovered_at=9682s, mutation_op=GrimoireRecursiveReplacementMutator):
  0000: 3f 42 0f 00 2f 2f 2f 2f 2f 2f 2f 2f 44 24 1c 0a   ?B..////////D$..
  0010: 5c 0a fe ff ff 3f 9b ff ff ff 02 02 5c 0a 53 48   \....?......\.SH
  0020: 49 46 54 5f 4a 49 53 00 00 d0 01 00 5c 0a 3c      IFT_JIS.....\.<
Seed 3 (id=07761326db68c9e4, size=52 bytes, fuzzer=grimoire, trial=1, discovered_at=12000s, mutation_op=I2SRandReplace,I2SRandReplace):
  0000: 27 68 74 74 70 3a 2c 27 23 27 68 74 74 70 3a 2f   'http:,'#'http:/
  0010: 2f 2f 77 2e 77 3e 20 23 3a 2f 2f 77 77 77 2b 77   //w.w> #://www+w
  0020: 33 2e 25 67 5c 0a fe ff ff 7f 3c 20 27 73 20 62   3.%g\.....< 's b
  0030: 20 5c 0a 20                                        \. 
Seed 4 (id=106c8087154f07e6, size=33 bytes, fuzzer=grimoire, trial=1, discovered_at=12306s, mutation_op=BytesExpandMutator):
  0000: 27 68 74 74 70 3a 2f 2f 7e 74 70 3a 2f 2f 7e 20   'http://~tp://~ 
  0010: 27 8d 69 6d 70 6c 65 01 20 78 3c 5c 0a fe ff 10   '.imple. x<\....
  0020: 00                                                .
Seed 5 (id=074a75b4270c7ea0, size=27 bytes, fuzzer=grimoire, trial=1, discovered_at=16152s, mutation_op=I2SRandReplace):
  0000: 27 68 74 74 70 3a 2f 2f 23 6d 70 6c 65 5f 2d 2d   'http://#mple_--
  0010: 20 20 20 23 5c 0a fe ff ff 7f 4d                     #\.....M


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  2f(/)x1                             27(')x5 5f(_)x2 2f(/)x2 4c(L)x1 +2u  PARTIAL
   0x0001  2f(/)x1                             68(h)x5 42(B)x2 2f(/)x2 49(I)x1 +2u  PARTIAL
   0x0002  2d(-)x1                             74(t)x5 2f(/)x2 45(E)x1 0f(.)x1 +3u  PARTIAL
   0x0003  2f(/)x1                             74(t)x5 44(D)x1 00(.)x1 5f(_)x1 +4u  DIFFER
   0x0004  2f(/)x1                             70(p)x5 2f(/)x4 24($)x1 5f(_)x1 +1u  PARTIAL
   0x0005  2d(-)x1                             3a(:)x5 2f(/)x3 7e(~)x1 5f(_)x1 +2u  DIFFER
   0x0006  27(')x1                             2f(/)x8 7e(~)x1 2c(,)x1 2d(-)x1 +1u  DIFFER
   0x0007  2e(.)x1                             2f(/)x7 5c(\)x1 27(')x1 5f(_)x1 +2u  DIFFER
   0x0008  3f(?)x1                             2f(/)x4 23(#)x2 0a(.)x1 7e(~)x1 +4u  DIFFER
   0x0009  3a(:)x1                             2f(/)x4 fe(.)x1 27(')x1 74(t)x1 +5u  DIFFER
   0x000a  5f(_)x1                             2f(/)x4 70(p)x3 ff(.)x1 68(h)x1 +3u  PARTIAL
   0x000b  5f(_)x1                             2f(/)x2 3a(:)x2 5f(_)x2 ff(.)x1 +5u  PARTIAL
   0x000c  28(()x1                             44(D)x2 2f(/)x2 3f(?)x1 74(t)x1 +6u  DIFFER
   0x000d  2c(,)x1                             2f(/)x3 70(p)x2 5f(_)x2 24($)x1 +3u  DIFFER
   0x000e  27(')x1                             7e(~)x2 1c(.)x1 3a(:)x1 2d(-)x1 +6u  PARTIAL
   0x000f  25(%)x1                             2f(/)x2 20( )x2 5f(_)x2 0a(.)x1 +4u  DIFFER
   0x0010  23(#)x1                             2f(/)x2 5f(_)x2 70(p)x2 5c(\)x1 +4u  DIFFER
   0x0011  5c(\)x1                             2f(/)x3 5f(_)x2 0a(.)x1 8d(.)x1 +4u  DIFFER
   0x0012  5b([)x1                             2f(/)x2 fe(.)x1 77(w)x1 69(i)x1 +6u  DIFFER
   0x0013  61(a)x1                             2f(/)x2 ff(.)x1 2e(.)x1 6d(m)x1 +6u  DIFFER
   0x0014  23(#)x1                             5f(_)x2 ff(.)x1 77(w)x1 70(p)x1 +6u  DIFFER
   0x0015  23(#)x1                             3f(?)x1 3e(>)x1 6c(l)x1 0a(.)x1 +7u  DIFFER
   0x0016  9f(.)x1                             20( )x2 2f(/)x2 9b(.)x1 65(e)x1 +5u  DIFFER
   0x0017  2e(.)x1                             ff(.)x2 23(#)x2 01(.)x1 5f(_)x1 +5u  PARTIAL
   0x0018  40(@)x1                             ff(.)x2 3a(:)x2 20( )x1 23(#)x1 +5u  DIFFER
   0x0019  2e(.)x1                             2f(/)x2 ff(.)x1 78(x)x1 7f(.)x1 +6u  DIFFER
   0x001a  7e(~)x1                             5f(_)x2 02(.)x1 2f(/)x1 3c(<)x1 +6u  DIFFER
   0x001b  28(()x1                             2f(/)x3 5f(_)x2 02(.)x1 77(w)x1 +3u  DIFFER
   0x001c  41(A)x1                             2b(+)x2 25(%)x2 5c(\)x1 77(w)x1 +4u  DIFFER
   0x001d  3c(<)x1                             5f(_)x2 0a(.)x1 77(w)x1 fe(.)x1 +5u  DIFFER
   0x001e  37(7)x1                             53(S)x1 2b(+)x1 ff(.)x1 a9(.)x1 +6u  DIFFER
   0x001f  37(7)x1                             48(H)x1 77(w)x1 10(.)x1 05(.)x1 +6u  DIFFER
   0x0020  37(7)x1                             5f(_)x2 49(I)x1 33(3)x1 00(.)x1 +4u  DIFFER
   0x0021  32(2)x1                             5f(_)x2 46(F)x1 2e(.)x1 29())x1 +3u  DIFFER
   0x0022  56(V)x1                             25(%)x3 54(T)x1 2d(-)x1 5f(_)x1 +2u  DIFFER
   0x0023  78(x)x1                             5f(_)x2 67(g)x1 21(!)x1 44(D)x1 +3u  DIFFER
   0x0024  02(.)x1                             4a(J)x1 5c(\)x1 5f(_)x1 2d(-)x1 +4u  DIFFER
   0x0025  6c(l)x1                             5f(_)x2 70(p)x2 2f(/)x2 49(I)x1 +1u  DIFFER
   0x0026  5c(\)x1                             2f(/)x2 53(S)x1 fe(.)x1 2d(-)x1 +3u  DIFFER
   0x0027  0a(.)x1                             2b(+)x2 00(.)x1 ff(.)x1 28(()x1 +3u  DIFFER
   ... (24 more divergent offsets)
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

--- grimoire ---
**Baseline relationship**: grimoire builds on the full cmplog stack —
it includes the `CmpLogObserver`, the `TracingStage`, and the
`I2SRandReplace` (i2s) stage — and ADDS a `GeneralizationStage` plus
Grimoire structural mutators. The single-technique delta is therefore
`grimoire` vs `cmplog` (both have I2S; grimoire adds generalization +
Grimoire mutators), not vs naive.

**Instrumentation**: cmplog's edge counters + per-execution CMP buffer
(`CmpLogObserver`).

**Feedback**: edge-bucket `MaxMapFeedback`.

**Mutators / stages**: stages are
`[generalization, tracing, i2s, havoc, grimoire]`. `GeneralizationStage`
replaces concrete byte runs in a corpus entry with `<GAP>` placeholders
(a generalised input) by repeatedly re-executing and checking that
coverage is preserved. The Grimoire mutators —
`GrimoireExtensionMutator`, `GrimoireRecursiveReplacementMutator`,
`GrimoireStringReplacementMutator`, `GrimoireRandomDeleteMutator` —
splice and recurse on these generalised token/gap structures
(string-based, grammar-free structural mutation). `I2SRandReplace` (the
cmplog i2s stage) also runs.

**Observed `mutation_op` in seed metadata**: all grimoire stages (i2s,
havoc, grimoire) are wrapped in `LineageMutatorWrap` with **no
per-operator name list**, so grimoire seeds appear nameless in lineage
(`mutation_op = -`). As with mopt, nameless rows are NOT an
I2S-exclusive signal here — and grimoire genuinely runs I2S too, so the
two are not separable from lineage names.

**Per-execution cost**: cmplog's per-CMP cost, plus extra executions
during generalization (each candidate gap is validated by a re-run).

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_6869.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6869,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>grimoire (grimoire_structural)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6869 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6869 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6869 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).