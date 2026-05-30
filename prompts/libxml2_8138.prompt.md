==== BLOCKER ====
Target: libxml2
Branch ID: 8138
Location: /src/libxml2/parserInternals.c:764:17
Enclosing function: xmlStringCurrentChar
Source line:             if (!IS_CHAR(val)) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0        5          5  REFERENCE
cmplog                           0        6          4  REFERENCE
value_profile                    1        9          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        2          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             1        3          6  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 34  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=5.70h  loser=10.80h
  avg hitcount on branch: winner=4  loser=1
  prob_div=0.70  dur_div=5.10h  hit_div=3
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/8138/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlStringCurrentChar (/src/libxml2/parserInternals.c:717-813) ---
[ ]   715  int
[ ]   716  xmlStringCurrentChar(xmlParserCtxtPtr ctxt, const xmlChar * cur, int *len)
[B]   717  {
[B]   718      if ((len == NULL) || (cur == NULL)) return(0);
[B]   719      if ((ctxt == NULL) || (ctxt->charset == XML_CHAR_ENCODING_UTF8)) {
[ ]   720          /*
[ ]   721           * We are supposed to handle UTF8, check it's valid
[ ]   722           * From rfc2044: encoding of the Unicode values on UTF-8:
[ ]   723           *
[ ]   724           * UCS-4 range (hex.)           UTF-8 octet sequence (binary)
[ ]   725           * 0000 0000-0000 007F   0xxxxxxx
[ ]   726           * 0000 0080-0000 07FF   110xxxxx 10xxxxxx
[ ]   727           * 0000 0800-0000 FFFF   1110xxxx 10xxxxxx 10xxxxxx
[ ]   728           *
[ ]   729           * Check for the 0x110000 limit too
[ ]   730           */
[B]   731          unsigned char c;
[B]   732          unsigned int val;
[ ]   733  
[B]   734          c = *cur;
[B]   735          if (c & 0x80) {
[B]   736              if ((cur[1] & 0xc0) != 0x80)
[W]   737                  goto encoding_error;
[B]   738              if ((c & 0xe0) == 0xe0) {
[ ]   739  
[ ]   740                  if ((cur[2] & 0xc0) != 0x80)
[ ]   741                      goto encoding_error;
[ ]   742                  if ((c & 0xf0) == 0xf0) {
[ ]   743                      if (((c & 0xf8) != 0xf0) || ((cur[3] & 0xc0) != 0x80))
[ ]   744                          goto encoding_error;
[ ]   745                      /* 4-byte code */
[ ]   746                      *len = 4;
[ ]   747                      val = (cur[0] & 0x7) << 18;
[ ]   748                      val |= (cur[1] & 0x3f) << 12;
[ ]   749                      val |= (cur[2] & 0x3f) << 6;
[ ]   750                      val |= cur[3] & 0x3f;
[ ]   751                  } else {
[ ]   752                      /* 3-byte code */
[ ]   753                      *len = 3;
[ ]   754                      val = (cur[0] & 0xf) << 12;
[ ]   755                      val |= (cur[1] & 0x3f) << 6;
[ ]   756                      val |= cur[2] & 0x3f;
[ ]   757                  }
[B]   758              } else {
[ ]   759                  /* 2-byte code */
[B]   760                  *len = 2;
[B]   761                  val = (cur[0] & 0x1f) << 6;
[B]   762                  val |= cur[1] & 0x3f;
[B]   763              }
[B]   764              if (!IS_CHAR(val)) { <-- BLOCKER
[W]   765  	        xmlErrEncodingInt(ctxt, XML_ERR_INVALID_CHAR,
[W]   766  				  "Char 0x%X out of allowed range\n", val);
[W]   767              }
[B]   768              return (val);
[B]   769          } else {
[ ]   770              /* 1-byte code */
[W]   771              *len = 1;
[W]   772              return (*cur);
[W]   773          }
[B]   774      }
[ ]   775      /*
[ ]   776       * Assume it's a fixed length encoding (1) with
[ ]   777       * a compatible encoding for the ASCII set, since
[ ]   778       * XML constructs only use < 128 chars
[ ]   779       */
[ ]   780      *len = 1;
[ ]   781      return (*cur);
[W]   782  encoding_error:
[ ]   783  
[ ]   784      /*
[ ]   785       * An encoding problem may arise from a truncated input buffer
[ ]   786       * splitting a character in the middle. In that case do not raise
[ ]   787       * an error but return 0 to indicate an end of stream problem
[ ]   788       */
[W]   789      if ((ctxt == NULL) || (ctxt->input == NULL) ||
[W]   790          (ctxt->input->end - ctxt->input->cur < 4)) {
[ ]   791  	*len = 0;
[ ]   792  	return(0);
[ ]   793      }
[ ]   794      /*
[ ]   795       * If we detect an UTF8 error that probably mean that the
[ ]   796       * input encoding didn't get properly advertised in the
[ ]   797       * declaration header. Report the error and switch the encoding
[ ]   798       * to ISO-Latin-1 (if you don't like this policy, just declare the
[ ]   799       * encoding !)
[ ]   800       */
[W]   801      {
[W]   802          char buffer[150];
[ ]   803  
[W]   804  	snprintf(buffer, 149, "Bytes: 0x%02X 0x%02X 0x%02X 0x%02X\n",
[W]   805  			ctxt->input->cur[0], ctxt->input->cur[1],
[W]   806  			ctxt->input->cur[2], ctxt->input->cur[3]);
[W]   807  	__xmlErrEncoding(ctxt, XML_ERR_INVALID_CHAR,
[W]   808  		     "Input is not proper UTF-8, indicate encoding !\n%s",
[W]   809  		     BAD_CAST buffer, NULL);
[W]   810      }
[W]   811      *len = 1;
[W]   812      return (*cur);
[W]   813  }

--- Caller (1 hop): valid.c:xmlValidateNmtokensValueInternal (/src/libxml2/valid.c:3765-3810, calls xmlStringCurrentChar at line 3771) (±10 around call site) ---
[W]  3765  xmlValidateNmtokensValueInternal(xmlDocPtr doc, const xmlChar *value) {
[W]  3766      const xmlChar *cur;
[W]  3767      int val, len;
[ ]  3768  
[W]  3769      if (value == NULL) return(0);
[W]  3770      cur = value;
[W]  3771      val = xmlStringCurrentChar(NULL, cur, &len); <-- CALL
[W]  3772      cur += len;
[ ]  3773  
[W]  3774      while (IS_BLANK(val)) {
[ ]  3775  	val = xmlStringCurrentChar(NULL, cur, &len);
[ ]  3776  	cur += len;
[ ]  3777      }
[ ]  3778  
[W]  3779      if (!xmlIsDocNameChar(doc, val))
[ ]  3780  	return(0);
[ ]  3781  

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  pattern.c:xmlPatScanName  (/src/libxml2/pattern.c:813-839, calls xmlStringCurrentChar at line 821)
hop 3  pattern.c:xmlCompileAttributeTest  (/src/libxml2/pattern.c:912-991, calls pattern.c:xmlPatScanName at line 945)
hop 3  pattern.c:xmlCompileStepPattern  (/src/libxml2/pattern.c:1005-1212, calls pattern.c:xmlPatScanName at line 1067)
hop 4  pattern.c:xmlCompilePathPattern  (/src/libxml2/pattern.c:1224-1309, calls pattern.c:xmlCompileStepPattern at line 1256)
hop 5  xmlPatterncompile  (/src/libxml2/pattern.c:2351-2443, calls pattern.c:xmlCompilePathPattern at line 2398)
hop 6  xmlTextReaderPreservePattern  (/src/libxml2/xmlreader.c:3917-3951, calls xmlPatterncompile at line 3923)
hop 6  xmlschemas.c:xmlSchemaCheckCSelectorXPath  (/src/libxml2/xmlschemas.c:8091-8181, calls xmlPatterncompile at line 8162)
hop 7  xmlschemas.c:xmlSchemaParseIDCSelectorAndField  (/src/libxml2/xmlschemas.c:8307-8387, calls xmlschemas.c:xmlSchemaCheckCSelectorXPath at line 8355)
hop 8  xmlschemas.c:xmlSchemaParseIDC  (/src/libxml2/xmlschemas.c:8405-8534, calls xmlschemas.c:xmlSchemaParseIDCSelectorAndField at line 8498)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     250         3  xmlNextChar  (/src/libxml2/parserInternals.c:397-537)
     243        13  xmlParserInputGrow  (/src/libxml2/parserInternals.c:289-330)
     153         3  xmlStringCurrentChar  (/src/libxml2/parserInternals.c:717-813)  <-- enclosing
      21         0  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581)
      12         0  xmlGetDtdElementDesc  (/src/libxml2/valid.c:3250-3267)
      12         0  xmlGetDtdQElementDesc  (/src/libxml2/valid.c:3349-3357)
      12         0  xmlGetDtdAttrDesc  (/src/libxml2/valid.c:3372-3393)
       9         0  valid.c:xmlFreeAttribute  (/src/libxml2/valid.c:1907-1939)
       9         0  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172)
       9         0  valid.c:xmlFreeAttributeTableEntry  (/src/libxml2/valid.c:2175-2177)
       9         0  valid.c:xmlGetDtdElementDesc2  (/src/libxml2/valid.c:3280-3334)
       9         0  valid.c:xmlValidateAttributeCallback  (/src/libxml2/valid.c:6762-6830)
       9         1  __xmlErrEncoding  (/src/libxml2/parserInternals.c:134-149)
       6         0  xmlNewDocElementContent  (/src/libxml2/valid.c:902-961)
       6         0  xmlFreeDocElementContent  (/src/libxml2/valid.c:1082-1138)
... (16 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  xmlStringCurrentChar  (/src/libxml2/parserInternals.c:717-813) ---
  d=1   L 718  T=0 F=153  T=0 F=3  if ((len == NULL) || (cur == NULL)) return(0);
  d=1   L 718  T=0 F=153  T=0 F=3  if ((len == NULL) || (cur == NULL)) return(0);
  d=1   L 719  T=18 F=135  T=0 F=3  if ((ctxt == NULL) || (ctxt->charset == XML_CHAR_ENCODING...
  d=1   L 719  T=135 F=0  T=3 F=0  if ((ctxt == NULL) || (ctxt->charset == XML_CHAR_ENCODING...
  d=1   L 735  T=6 F=147  T=3 F=0  if (c & 0x80) {
  d=1   L 736  T=3 F=3  T=0 F=3  if ((cur[1] & 0xc0) != 0x80)
  d=1   L 764  T=3 F=0  T=0 F=3  if (!IS_CHAR(val)) {  <-- BLOCKER
  d=1   L 789  T=0 F=3  T=0 F=0  if ((ctxt == NULL) || (ctxt->input == NULL) ||
  d=1   L 789  T=0 F=3  T=0 F=0  if ((ctxt == NULL) || (ctxt->input == NULL) ||
  d=1   L 790  T=0 F=3  T=0 F=0  (ctxt->input->end - ctxt->input->cur < 4)) {

[off-chain: 265 additional divergent branches across 31 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=e77944c783da000c, size=381 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=46283s, mutation_op=ByteAddMutator,ByteAddMutator):
  0000: f5 ff ff ff ff ff ff ff 06 5f 00 00 31 32 37 37   ........._..1277
  0010: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0020: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0030: 44 4f 43 54 59 50 45 0a 61 20 53 59 53 54 45 4d   DOCTYPE.a SYSTEM

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=54cdbfa4a80d9f79, size=147 bytes, fuzzer=value_profile, trial=1, discovered_at=22946s, mutation_op=ByteIncMutator,ByteRandMutator,BytesRandInsertMutator,QwordAddMutator,ByteAddMutator,ByteNegMutator,BytesSwapMutator):
  0000: 49 53 54 20 84 84 84 84 84 54 4c 0a b3 21 54 43   IST .....TL..!TC
  0010: 44 6e 6b 3a 68 30 30 30 30 30 30 30 30 30 30 30   Dnk:h00000000000
  0020: 00 20 61 6e 73 3a 78 6c 69 6e 49 53 4f 2d 45 ad   . ans:xlinISO-E.
  0030: 36 ef 53 5c 32 04 31 30 26 cb 36 2d 55 43 37 2d   6.S\2.10&.6-UC7-


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  f5(.)x1                             49(I)x1                             DIFFER
   0x0001  ff(.)x1                             53(S)x1                             DIFFER
   0x0002  ff(.)x1                             54(T)x1                             DIFFER
   0x0003  ff(.)x1                             20( )x1                             DIFFER
   0x0004  ff(.)x1                             84(.)x1                             DIFFER
   0x0005  ff(.)x1                             84(.)x1                             DIFFER
   0x0006  ff(.)x1                             84(.)x1                             DIFFER
   0x0007  ff(.)x1                             84(.)x1                             DIFFER
   0x0008  06(.)x1                             84(.)x1                             DIFFER
   0x0009  5f(_)x1                             54(T)x1                             DIFFER
   0x000a  00(.)x1                             4c(L)x1                             DIFFER
   0x000b  00(.)x1                             0a(.)x1                             DIFFER
   0x000c  31(1)x1                             b3(.)x1                             DIFFER
   0x000d  32(2)x1                             21(!)x1                             DIFFER
   0x000e  37(7)x1                             54(T)x1                             DIFFER
   0x000f  37(7)x1                             43(C)x1                             DIFFER
   0x0010  37(7)x1                             44(D)x1                             DIFFER
   0x0011  32(2)x1                             6e(n)x1                             DIFFER
   0x0012  2e(.)x1                             6b(k)x1                             DIFFER
   0x0013  78(x)x1                             3a(:)x1                             DIFFER
   0x0014  6d(m)x1                             68(h)x1                             DIFFER
   0x0015  6c(l)x1                             30(0)x1                             DIFFER
   0x0016  5c(\)x1                             30(0)x1                             DIFFER
   0x0017  0a(.)x1                             30(0)x1                             DIFFER
   0x0018  3c(<)x1                             30(0)x1                             DIFFER
   0x0019  3f(?)x1                             30(0)x1                             DIFFER
   0x001a  78(x)x1                             30(0)x1                             DIFFER
   0x001b  6d(m)x1                             30(0)x1                             DIFFER
   0x001c  6c(l)x1                             30(0)x1                             DIFFER
   0x001d  20( )x1                             30(0)x1                             DIFFER
   0x001e  76(v)x1                             30(0)x1                             DIFFER
   0x001f  65(e)x1                             30(0)x1                             DIFFER
   0x0020  72(r)x1                             00(.)x1                             DIFFER
   0x0021  73(s)x1                             20( )x1                             DIFFER
   0x0022  69(i)x1                             61(a)x1                             DIFFER
   0x0023  6f(o)x1                             6e(n)x1                             DIFFER
   0x0024  6e(n)x1                             73(s)x1                             DIFFER
   0x0025  3d(=)x1                             3a(:)x1                             DIFFER
   0x0026  22(")x1                             78(x)x1                             DIFFER
   0x0027  31(1)x1                             6c(l)x1                             DIFFER
   ... (24 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_8138.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 8138,
  "target": "libxml2",
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 8138 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 8138 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 8138 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).