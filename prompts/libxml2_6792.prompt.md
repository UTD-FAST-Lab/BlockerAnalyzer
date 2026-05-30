==== BLOCKER ====
Target: libxml2
Branch ID: 6792
Location: /src/libxml2/parser.c:11261:18
Enclosing function: parser.c:xmlParseLookupInternalSubset
Source line:         else if (state == ']') {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0        7          3  REFERENCE
cmplog                           1        8          1  loser (value_profile vs value_profile_cmplog)
value_profile                    9        1          0  REFERENCE
value_profile_cmplog             9        1          0  winner (value_profile vs cmplog)
naive_ctx                        9        1          0  REFERENCE
naive_ngram4                     1        3          6  REFERENCE
mopt                             2        3          5  REFERENCE
minimizer                        1        4          5  REFERENCE
fast                             0        7          3  REFERENCE
grimoire                         0       10          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=8  unreached=1
  avg duration blocked: winner=4.00h  loser=15.44h
  avg hitcount on branch: winner=5  loser=0
  prob_div=0.79  dur_div=11.44h  hit_div=5
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6792/{W,L}/branch_coverage_show.txt

--- Enclosing function: parser.c:xmlParseLookupInternalSubset (/src/libxml2/parser.c:11231-11324) ---
[ ] 11229   */
[ ] 11230  static int
[B] 11231  xmlParseLookupInternalSubset(xmlParserCtxtPtr ctxt) {
[ ] 11232      /*
[ ] 11233       * Sorry, but progressive parsing of the internal subset is not
[ ] 11234       * supported. We first check that the full content of the internal
[ ] 11235       * subset is available and parsing is launched only at that point.
[ ] 11236       * Internal subset ends with "']' S? '>'" in an unescaped section and
[ ] 11237       * not in a ']]>' sequence which are conditional sections.
[ ] 11238       */
[B] 11239      const xmlChar *cur, *start;
[B] 11240      const xmlChar *end = ctxt->input->end;
[B] 11241      int state = ctxt->endCheckState;
[ ] 11242  
[B] 11243      if (ctxt->checkIndex == 0) {
[B] 11244          cur = ctxt->input->cur + 1;
[B] 11245      } else {
[W] 11246          cur = ctxt->input->cur + ctxt->checkIndex;
[W] 11247      }
[B] 11248      start = cur;
[ ] 11249  
[B] 11250      while (cur < end) {
[B] 11251          if (state == '-') {
[ ] 11252              if ((*cur == '-') &&
[ ] 11253                  (cur[1] == '-') &&
[ ] 11254                  (cur[2] == '>')) {
[ ] 11255                  state = 0;
[ ] 11256                  cur += 3;
[ ] 11257                  start = cur;
[ ] 11258                  continue;
[ ] 11259              }
[ ] 11260          }
[B] 11261          else if (state == ']') { <-- BLOCKER
[W] 11262              if (*cur == '>') {
[ ] 11263                  ctxt->checkIndex = 0;
[ ] 11264                  ctxt->endCheckState = 0;
[ ] 11265                  return(1);
[ ] 11266              }
[W] 11267              if (IS_BLANK_CH(*cur)) {
[W] 11268                  state = ' ';
[W] 11269              } else if (*cur != ']') {
[ ] 11270                  state = 0;
[ ] 11271                  start = cur;
[ ] 11272                  continue;
[ ] 11273              }
[W] 11274          }
[B] 11275          else if (state == ' ') {
[W] 11276              if (*cur == '>') {
[ ] 11277                  ctxt->checkIndex = 0;
[ ] 11278                  ctxt->endCheckState = 0;
[ ] 11279                  return(1);
[ ] 11280              }
[W] 11281              if (!IS_BLANK_CH(*cur)) {
[W] 11282                  state = 0;
[W] 11283                  start = cur;
[W] 11284                  continue;
[W] 11285              }
[W] 11286          }
[B] 11287          else if (state != 0) {
[B] 11288              if (*cur == state) {
[B] 11289                  state = 0;
[B] 11290                  start = cur + 1;
[B] 11291              }
[B] 11292          }
[B] 11293          else if (*cur == '<') {
[B] 11294              if ((cur[1] == '!') &&
[B] 11295                  (cur[2] == '-') &&
[B] 11296                  (cur[3] == '-')) {
[ ] 11297                  state = '-';
[ ] 11298                  cur += 4;
[ ] 11299                  /* Don't treat <!--> as comment */
[ ] 11300                  start = cur;
[ ] 11301                  continue;
[ ] 11302              }
[B] 11303          }
[B] 11304          else if ((*cur == '"') || (*cur == '\'') || (*cur == ']')) {
[B] 11305              state = *cur;
[B] 11306          }
[ ] 11307  
[B] 11308          cur++;
[B] 11309      }
[ ] 11310  
[ ] 11311      /*
[ ] 11312       * Rescan the three last characters to detect "<!--" and "-->"
[ ] 11313       * split across chunks.
[ ] 11314       */
[B] 11315      if ((state == 0) || (state == '-')) {
[B] 11316          if (cur - start < 3)
[ ] 11317              cur = start;
[B] 11318          else
[B] 11319              cur -= 3;
[B] 11320      }
[B] 11321      ctxt->checkIndex = cur - ctxt->input->cur;
[B] 11322      ctxt->endCheckState = state;
[B] 11323      return(0);
[B] 11324  }

--- Caller (1 hop): parser.c:xmlParseTryOrFinish (/src/libxml2/parser.c:11404-12120, calls parser.c:xmlParseLookupInternalSubset at line 12008) (±10 around call site) ---
[ ] 11998  		    goto done;
[ ] 11999                  } else {
[ ] 12000  		    ctxt->instate = XML_PARSER_START_TAG;
[ ] 12001  #ifdef DEBUG_PUSH
[ ] 12002  		    xmlGenericError(xmlGenericErrorContext,
[ ] 12003  			    "PP: entering START_TAG\n");
[ ] 12004  #endif
[ ] 12005  		}
[B] 12006  		break;
[B] 12007              case XML_PARSER_DTD: {
[B] 12008                  if ((!terminate) && (!xmlParseLookupInternalSubset(ctxt))) <-- CALL
[B] 12009                      goto done;
[B] 12010  		xmlParseInternalSubset(ctxt);
[B] 12011  		if (ctxt->instate == XML_PARSER_EOF)
[B] 12012  		    goto done;
[ ] 12013  		ctxt->inSubset = 2;
[ ] 12014  		if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
[ ] 12015  		    (ctxt->sax->externalSubset != NULL))
[ ] 12016  		    ctxt->sax->externalSubset(ctxt->userData, ctxt->intSubName,
[ ] 12017  			    ctxt->extSubSystem, ctxt->extSubURI);
[ ] 12018  		ctxt->inSubset = 0;

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls parser.c:xmlParseLookupInternalSubset at line 12008)
hop 3  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 4  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       3         0  xmlParseSystemLiteral  (/src/libxml2/parser.c:4248-4326)
       3         0  xmlParseElementMixedContentDecl  (/src/libxml2/parser.c:6193-6284)
       3         0  xmlParseElementContentDecl  (/src/libxml2/parser.c:6647-6675)
       3         0  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788)
       3         0  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=3   L12139  T=0 F=6  T=0 F=3  if (ctxt == NULL)
  d=3   L12141  T=0 F=0  T=0 F=1  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12141  T=0 F=6  T=1 F=2  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12143  T=0 F=6  T=0 F=3  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L12145  T=0 F=6  T=0 F=3  if (ctxt->input == NULL)
  d=3   L12149  T=2 F=4  T=2 F=1  if (ctxt->instate == XML_PARSER_START)
  d=3   L12151  T=3 F=3  T=2 F=1  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=3   L12159  T=3 F=3  T=2 F=1  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=3   L12170  T=2 F=1  T=2 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=3   L12211  T=3 F=0  T=1 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=3   L12212  T=3 F=0  T=1 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=3   L12212  T=3 F=0  T=1 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=3   L12214  T=0 F=3  T=0 F=1  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=3   L12233  T=0 F=6  T=0 F=3  if (remain != 0) {
  d=3   L12238  T=2 F=4  T=1 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L12241  T=4 F=0  T=2 F=0  if ((ctxt->input != NULL) &&
  d=3   L12242  T=0 F=4  T=0 F=2  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=3   L12243  T=0 F=4  T=0 F=2  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=3   L12248  T=0 F=0  T=0 F=2  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12248  T=0 F=4  T=2 F=0  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12251  T=0 F=4  T=0 F=2  if (remain != 0) {
  d=3   L12257  T=0 F=4  T=0 F=2  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=3   L12268  T=0 F=4  T=0 F=2  if (terminate) {
  d=3   L12296  T=0 F=4  T=2 F=0  if (ctxt->wellFormed == 0)
--- d=2  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=2   L11409  T=0 F=6  T=0 F=3  if (ctxt->input == NULL)
  d=2   L11465  T=6 F=0  T=3 F=0  if ((ctxt->input != NULL) &&
  d=2   L11466  T=0 F=6  T=0 F=3  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=2   L11471  T=0 F=0  T=0 F=3  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L11471  T=0 F=11  T=3 F=5  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L12008  T=4 F=2  T=2 F=1  if ((!terminate) && (!xmlParseLookupInternalSubset(ctxt)))
  d=2   L12008  T=4 F=0  T=2 F=0  if ((!terminate) && (!xmlParseLookupInternalSubset(ctxt)))
  d=2   L12011  T=2 F=0  T=1 F=0  if (ctxt->instate == XML_PARSER_EOF)
--- d=1  parser.c:xmlParseLookupInternalSubset  (/src/libxml2/parser.c:11231-11324) ---
  d=1   L11243  T=2 F=2  T=2 F=0  if (ctxt->checkIndex == 0) {
  d=1   L11250  T=401 F=4  T=166 F=2  while (cur < end) {
  d=1   L11251  T=0 F=401  T=0 F=166  if (state == '-') {
  d=1   L11261  T=4 F=397  T=0 F=166  else if (state == ']') {  <-- BLOCKER
  d=1   L11262  T=0 F=4  T=0 F=0  if (*cur == '>') {
  d=1   L11275  T=12 F=385  T=0 F=166  else if (state == ' ') {
  d=1   L11276  T=0 F=12  T=0 F=0  if (*cur == '>') {
  d=1   L11287  T=60 F=325  T=70 F=96  else if (state != 0) {
  d=1   L11293  T=2 F=323  T=8 F=88  else if (*cur == '<') {
  d=1   L11294  T=2 F=0  T=0 F=8  if ((cur[1] == '!') &&
  d=1   L11295  T=0 F=2  T=0 F=0  (cur[2] == '-') &&
  d=1   L11304  T=4 F=319  T=0 F=84  else if ((*cur == '"') || (*cur == '\'') || (*cur == ']')) {
  d=1   L11304  T=0 F=323  T=4 F=84  else if ((*cur == '"') || (*cur == '\'') || (*cur == ']')) {
  d=1   L11304  T=4 F=315  T=0 F=84  else if ((*cur == '"') || (*cur == '\'') || (*cur == ']')) {
  d=1   L11315  T=0 F=1  T=0 F=0  if ((state == 0) || (state == '-')) {
  d=1   L11315  T=3 F=1  T=2 F=0  if ((state == 0) || (state == '-')) {

[off-chain: 92 additional divergent branches across 14 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=81e56072f992fc6e, size=280 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=81019s, mutation_op=BytesInsertCopyMutator,BytesSwapMutator):
  0000: 25 39 39 39 2f 78 06 00 00 00 31 32 37 37 37 32   %999/x....127772
  0010: 2e 01 00 00 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73   ....\.<?xml vers
  0020: 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f   ion="1.0"?>.<!DO
  0030: 43 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22   CTYPE a SYSTEM "

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=3b3da00795bdfae9, size=384 bytes, fuzzer=cmplog, trial=1, discovered_at=13s, mutation_op=ByteFlipMutator,BytesInsertMutator,BitFlipMutator):
  0000: 07 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 5b 53 54 45 4d 20 22 64 74 64 73 2f 31   a S[STEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  25(%)x1                             07(.)x1                             DIFFER
   0x0001  39(9)x1                             00(.)x1                             DIFFER
   0x0002  39(9)x1                             00(.)x1                             DIFFER
   0x0003  39(9)x1                             00(.)x1                             DIFFER
   0x0004  2f(/)x1                             31(1)x1                             DIFFER
   0x0005  78(x)x1                             32(2)x1                             DIFFER
   0x0006  06(.)x1                             37(7)x1                             DIFFER
   0x0007  00(.)x1                             37(7)x1                             DIFFER
   0x0008  00(.)x1                             37(7)x1                             DIFFER
   0x0009  00(.)x1                             32(2)x1                             DIFFER
   0x000a  31(1)x1                             2e(.)x1                             DIFFER
   0x000b  32(2)x1                             78(x)x1                             DIFFER
   0x000c  37(7)x1                             6d(m)x1                             DIFFER
   0x000d  37(7)x1                             6c(l)x1                             DIFFER
   0x000e  37(7)x1                             5c(\)x1                             DIFFER
   0x000f  32(2)x1                             0a(.)x1                             DIFFER
   0x0010  2e(.)x1                             3c(<)x1                             DIFFER
   0x0011  01(.)x1                             3f(?)x1                             DIFFER
   0x0012  00(.)x1                             78(x)x1                             DIFFER
   0x0013  00(.)x1                             6d(m)x1                             DIFFER
   0x0014  5c(\)x1                             6c(l)x1                             DIFFER
   0x0015  0a(.)x1                             20( )x1                             DIFFER
   0x0016  3c(<)x1                             76(v)x1                             DIFFER
   0x0017  3f(?)x1                             65(e)x1                             DIFFER
   0x0018  78(x)x1                             72(r)x1                             DIFFER
   0x0019  6d(m)x1                             73(s)x1                             DIFFER
   0x001a  6c(l)x1                             69(i)x1                             DIFFER
   0x001b  20( )x1                             6f(o)x1                             DIFFER
   0x001c  76(v)x1                             6e(n)x1                             DIFFER
   0x001d  65(e)x1                             3d(=)x1                             DIFFER
   0x001e  72(r)x1                             22(")x1                             DIFFER
   0x001f  73(s)x1                             31(1)x1                             DIFFER
   0x0020  69(i)x1                             2e(.)x1                             DIFFER
   0x0021  6f(o)x1                             30(0)x1                             DIFFER
   0x0022  6e(n)x1                             22(")x1                             DIFFER
   0x0023  3d(=)x1                             3f(?)x1                             DIFFER
   0x0024  22(")x1                             3e(>)x1                             DIFFER
   0x0025  31(1)x1                             0a(.)x1                             DIFFER
   0x0026  2e(.)x1                             3c(<)x1                             DIFFER
   0x0027  30(0)x1                             21(!)x1                             DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6792.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6792,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>cmplog (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6792 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6792 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6792 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).