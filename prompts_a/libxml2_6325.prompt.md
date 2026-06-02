==== BLOCKER ====
Target: libxml2
Branch ID: 6325
Location: /src/libxml2/encoding.c:533:13
Enclosing function: encoding.c:UTF16LEToUTF8
Source line:         if ((c & 0xFC00) == 0xD800) {    /* surrogates */
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        8          1  loser (ngram_coverage vs naive_ngram4); loser (value_profile vs value_profile)
cmplog                           4        6          0  REFERENCE
value_profile                    9        1          0  winner (value_profile vs naive)
value_profile_cmplog             7        3          0  REFERENCE
naive_ctx                        1        6          3  REFERENCE
naive_ngram4                    10        0          0  winner (ngram_coverage vs naive)
mopt                             7        3          0  REFERENCE
minimizer                        5        5          0  REFERENCE
fast                             7        3          0  REFERENCE
grimoire                         3        7          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ngram4', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile_cmplog', 'naive_ctx', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive_ngram4 > naive  [delta: ngram_coverage] ---
  subject 36  (naive_ngram4 vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=8  unreached=1
  avg duration blocked: winner=6.10h  loser=15.44h
  avg hitcount on branch: winner=50  loser=4
  prob_div=0.89  dur_div=9.34h  hit_div=46
  subject-level: delta_AUC=-26852220.0  p_AUC=0.0173  delta_Final=-260.4  p_final=0.0312
--- Pair 2: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=8  unreached=1
  avg duration blocked: winner=5.20h  loser=15.44h
  avg hitcount on branch: winner=96  loser=4
  prob_div=0.79  dur_div=10.24h  hit_div=93
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6325/{W,L}/branch_coverage_show.txt

--- Enclosing function: encoding.c:UTF16LEToUTF8 (/src/libxml2/encoding.c:505-576) ---
[ ]   503  UTF16LEToUTF8(unsigned char* out, int *outlen,
[ ]   504              const unsigned char* inb, int *inlenb)
[B]   505  {
[B]   506      unsigned char* outstart = out;
[B]   507      const unsigned char* processed = inb;
[B]   508      unsigned char* outend;
[B]   509      unsigned short* in = (unsigned short*) inb;
[B]   510      unsigned short* inend;
[B]   511      unsigned int c, d, inlen;
[B]   512      unsigned char *tmp;
[B]   513      int bits;
[ ]   514  
[B]   515      if (*outlen == 0) {
[ ]   516          *inlenb = 0;
[ ]   517          return(0);
[ ]   518      }
[B]   519      outend = out + *outlen;
[B]   520      if ((*inlenb % 2) == 1)
[W]   521          (*inlenb)--;
[B]   522      inlen = *inlenb / 2;
[B]   523      inend = in + inlen;
[B]   524      while ((in < inend) && (out - outstart + 5 < *outlen)) {
[B]   525          if (xmlLittleEndian) {
[B]   526  	    c= *in++;
[B]   527  	} else {
[ ]   528  	    tmp = (unsigned char *) in;
[ ]   529  	    c = *tmp++;
[ ]   530  	    c = c | (*tmp << 8);
[ ]   531  	    in++;
[ ]   532  	}
[B]   533          if ((c & 0xFC00) == 0xD800) {    /* surrogates */ <-- BLOCKER
[W]   534  	    if (in >= inend) {           /* handle split mutli-byte characters */
[W]   535  		break;
[W]   536  	    }
[W]   537  	    if (xmlLittleEndian) {
[W]   538  		d = *in++;
[W]   539  	    } else {
[ ]   540  		tmp = (unsigned char *) in;
[ ]   541  		d = *tmp++;
[ ]   542  		d = d | (*tmp << 8);
[ ]   543  		in++;
[ ]   544  	    }
[W]   545              if ((d & 0xFC00) == 0xDC00) {
[ ]   546                  c &= 0x03FF;
[ ]   547                  c <<= 10;
[ ]   548                  c |= d & 0x03FF;
[ ]   549                  c += 0x10000;
[ ]   550              }
[W]   551              else {
[W]   552  		*outlen = out - outstart;
[W]   553  		*inlenb = processed - inb;
[W]   554  	        return(-2);
[W]   555  	    }
[W]   556          }
[ ]   557  
[ ]   558  	/* assertion: c is a single UTF-4 value */
[B]   559          if (out >= outend)
[ ]   560  	    break;
[B]   561          if      (c <    0x80) {  *out++=  c;                bits= -6; }
[B]   562          else if (c <   0x800) {  *out++= ((c >>  6) & 0x1F) | 0xC0;  bits=  0; }
[B]   563          else if (c < 0x10000) {  *out++= ((c >> 12) & 0x0F) | 0xE0;  bits=  6; }
[ ]   564          else                  {  *out++= ((c >> 18) & 0x07) | 0xF0;  bits= 12; }
[ ]   565  
[B]   566          for ( ; bits >= 0; bits-= 6) {
[B]   567              if (out >= outend)
[ ]   568  	        break;
[B]   569              *out++= ((c >> bits) & 0x3F) | 0x80;
[B]   570          }
[B]   571  	processed = (const unsigned char*) in;
[B]   572      }
[B]   573      *outlen = out - outstart;
[B]   574      *inlenb = processed - inb;
[B]   575      return(*outlen);
[B]   576  }

--- No 1-hop callers of encoding.c:UTF16LEToUTF8 fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      54         6  encoding.c:UTF16LEToUTF8  (/src/libxml2/encoding.c:505-576)  <-- enclosing
      54         6  encoding.c:xmlEncInputChunk  (/src/libxml2/encoding.c:2030-2057)
      46         6  xmlCharEncInput  (/src/libxml2/encoding.c:2313-2392)
      28         7  xmlGetCharEncodingHandler  (/src/libxml2/encoding.c:1590-1712)
      12         0  encoding.c:xmlEncodingErr  (/src/libxml2/encoding.c:102-106)
      12         3  xmlDetectCharEncoding  (/src/libxml2/encoding.c:948-999)
      12         3  xmlCharEncCloseFunc  (/src/libxml2/encoding.c:2819-2887)
       8         2  xmlCharEncFirstLineInput  (/src/libxml2/encoding.c:2206-2297)
       2         0  xmlParseCharEncoding  (/src/libxml2/encoding.c:1166-1235)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  encoding.c:UTF16LEToUTF8  (/src/libxml2/encoding.c:505-576) ---
  d=1   L 515  T=0 F=54  T=0 F=6  if (*outlen == 0) {
  d=1   L 520  T=29 F=25  T=0 F=6  if ((*inlenb % 2) == 1)
  d=1   L 524  T=772 F=0  T=149 F=0  while ((in < inend) && (out - outstart + 5 < *outlen)) {
  d=1   L 524  T=772 F=17  T=149 F=6  while ((in < inend) && (out - outstart + 5 < *outlen)) {
  d=1   L 525  T=772 F=0  T=149 F=0  if (xmlLittleEndian) {
  d=1   L 533  T=37 F=735  T=0 F=149  if ((c & 0xFC00) == 0xD800) {    /* surrogates */  <-- BLOCKER
  d=1   L 534  T=25 F=12  T=0 F=0  if (in >= inend) {           /* handle split mutli-byte c...
  d=1   L 537  T=12 F=0  T=0 F=0  if (xmlLittleEndian) {
  d=1   L 545  T=0 F=12  T=0 F=0  if ((d & 0xFC00) == 0xDC00) {
  d=1   L 559  T=0 F=735  T=0 F=149  if (out >= outend)
  d=1   L 561  T=65 F=670  T=19 F=130  if      (c <    0x80) {  *out++=  c;                bits=...
  d=1   L 562  T=64 F=606  T=3 F=127  else if (c <   0x800) {  *out++= ((c >>  6) & 0x1F) | 0xC...
  d=1   L 563  T=606 F=0  T=127 F=0  else if (c < 0x10000) {  *out++= ((c >> 12) & 0x0F) | 0xE...
  d=1   L 566  T=1270 F=735  T=257 F=149  for ( ; bits >= 0; bits-= 6) {
  d=1   L 567  T=0 F=1270  T=0 F=257  if (out >= outend)

[off-chain: 87 additional divergent branches across 7 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=6b5fd2ed3f5a7285, size=358 bytes, fuzzer=naive_ngram4, trial=1):
  0000: 4d 50 4c 49 45 44 3e 0a 0a 5c 0a ff fe ff 43 53   MPLIED>..\....CS
  0010: 59 50 40 20 61 78 78 78 78 78 6d 6c 02 02 02 02   YP@ axxxxxml....
  0020: 02 00 00 00 00 00 02 6e c3 22 31 2e 30 22 3f 3e   .......n."1.0"?>
  0030: 41 73 69 6f 6e 3d 02 02 02 02 00 00 00 00 00 02   Asion=..........
Seed 2 (id=8c438cb94d27e127, size=247 bytes, fuzzer=naive_ngram4, trial=1):
  0000: 4d 50 4c 49 45 44 3e 0a 0a 5c 0a ff fe ff 43 53   MPLIED>..\....CS
  0010: 59 50 40 20 61 78 78 78 78 78 6d 6c 02 02 02 02   YP@ axxxxxml....
  0020: 02 00 00 00 00 00 02 6e 3d 22 31 2e 30 22 3f 3e   .......n="1.0"?>
  0030: 41 73 69 6f 6e 3d 54 41 20 20 20 20 13 23 49 72   Asion=TA    .#Ir
Seed 3 (id=8d6a9da46e8ede7d, size=502 bytes, fuzzer=naive_ngram4, trial=1):
  0000: 3c 61 3e f5 20 20 3c 64 74 64 73 2f 31 20 20 20   <a>.  <dtds/1   
  0010: 23 49 4d 25 1e 1e 1e 10 10 10 10 10 10 10 1e 1e   #IM%............
  0020: 1d 1e 1e 1e 1e 1e 1e 1e 1e 1e 1e 53 48 69 9c 9c   ...........SHi..
  0030: 9c 9c 80 9c 9c 73 73 73 46 54 5f 4a 49 53 3a 00   .....sssFT_JIS:.
Seed 4 (id=991dd70f7b9ba189, size=149 bytes, fuzzer=naive_ngram4, trial=1):
  0000: ce f1 f1 68 31 40 40 80 80 ff 5c 0a 3c 00 3f 00   ...h1@@...\.<.?.
  0010: 34 69 69 e5 e5 e5 e5 e5 e5 e5 e5 e5 e5 e5 e5 69   4ii............i
  0020: 69 20 c8 00 3c 61 3e f5 20 20 3c 64 74 64 73 2f   i ..<a>.  <dtds/
  0030: 31 20 20 20 23 49 4d 25 1e 1e 1e 10 10 10 10 10   1   #IM%........

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=98e939dda23e141f, size=183 bytes, fuzzer=naive, trial=1, discovered_at=6597s, mutation_op=ByteAddMutator,ByteAddMutator,BytesDeleteMutator,WordInterestingMutator,BytesExpandMutator,BytesExpandMutator):
  0000: 6e 6b 27 14 14 14 14 10 14 02 14 0a 59 ae ff ff   nk'.........Y...
  0010: 20 20 20 20 20 20 20 20 20 20 20 78 6c 69 6e 6b              xlink
  0020: 3a 74 79 2c 2c 2c 2c 2c 2c 2c 2c 2c 38 2c 2c 2c   :ty,,,,,,,,,8,,,
  0030: 2c 29 20 20 23 46 49 64 74 77 68 54 10 10 10 10   ,)  #FIdtwhT....


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  4d(M)x2 3c(<)x1 ce(.)x1             6e(n)x1                             DIFFER
   0x0001  50(P)x2 61(a)x1 f1(.)x1             6b(k)x1                             DIFFER
   0x0002  4c(L)x2 3e(>)x1 f1(.)x1             27(')x1                             DIFFER
   0x0003  49(I)x2 f5(.)x1 68(h)x1             14(.)x1                             DIFFER
   0x0004  45(E)x2 20( )x1 31(1)x1             14(.)x1                             DIFFER
   0x0005  44(D)x2 20( )x1 40(@)x1             14(.)x1                             DIFFER
   0x0006  3e(>)x2 3c(<)x1 40(@)x1             14(.)x1                             DIFFER
   0x0007  0a(.)x2 64(d)x1 80(.)x1             10(.)x1                             DIFFER
   0x0008  0a(.)x2 74(t)x1 80(.)x1             14(.)x1                             DIFFER
   0x0009  5c(\)x2 64(d)x1 ff(.)x1             02(.)x1                             DIFFER
   0x000a  0a(.)x2 73(s)x1 5c(\)x1             14(.)x1                             DIFFER
   0x000b  ff(.)x2 2f(/)x1 0a(.)x1             0a(.)x1                             PARTIAL
   0x000c  fe(.)x2 31(1)x1 3c(<)x1             59(Y)x1                             DIFFER
   0x000d  ff(.)x2 20( )x1 00(.)x1             ae(.)x1                             DIFFER
   0x000e  43(C)x2 20( )x1 3f(?)x1             ff(.)x1                             DIFFER
   0x000f  53(S)x2 20( )x1 00(.)x1             ff(.)x1                             DIFFER
   0x0010  59(Y)x2 23(#)x1 34(4)x1             20( )x1                             DIFFER
   0x0011  50(P)x2 49(I)x1 69(i)x1             20( )x1                             DIFFER
   0x0012  40(@)x2 4d(M)x1 69(i)x1             20( )x1                             DIFFER
   0x0013  20( )x2 25(%)x1 e5(.)x1             20( )x1                             PARTIAL
   0x0014  61(a)x2 1e(.)x1 e5(.)x1             20( )x1                             DIFFER
   0x0015  78(x)x2 1e(.)x1 e5(.)x1             20( )x1                             DIFFER
   0x0016  78(x)x2 1e(.)x1 e5(.)x1             20( )x1                             DIFFER
   0x0017  78(x)x2 10(.)x1 e5(.)x1             20( )x1                             DIFFER
   0x0018  78(x)x2 10(.)x1 e5(.)x1             20( )x1                             DIFFER
   0x0019  78(x)x2 10(.)x1 e5(.)x1             20( )x1                             DIFFER
   0x001a  6d(m)x2 10(.)x1 e5(.)x1             20( )x1                             DIFFER
   0x001b  6c(l)x2 10(.)x1 e5(.)x1             78(x)x1                             DIFFER
   0x001c  02(.)x2 10(.)x1 e5(.)x1             6c(l)x1                             DIFFER
   0x001d  02(.)x2 10(.)x1 e5(.)x1             69(i)x1                             DIFFER
   0x001e  02(.)x2 1e(.)x1 e5(.)x1             6e(n)x1                             DIFFER
   0x001f  02(.)x2 1e(.)x1 69(i)x1             6b(k)x1                             DIFFER
   0x0020  02(.)x2 1d(.)x1 69(i)x1             3a(:)x1                             DIFFER
   0x0021  00(.)x2 1e(.)x1 20( )x1             74(t)x1                             DIFFER
   0x0022  00(.)x2 1e(.)x1 c8(.)x1             79(y)x1                             DIFFER
   0x0023  00(.)x3 1e(.)x1                     2c(,)x1                             DIFFER
   0x0024  00(.)x2 1e(.)x1 3c(<)x1             2c(,)x1                             DIFFER
   0x0025  00(.)x2 1e(.)x1 61(a)x1             2c(,)x1                             DIFFER
   0x0026  02(.)x2 1e(.)x1 3e(>)x1             2c(,)x1                             DIFFER
   0x0027  6e(n)x2 1e(.)x1 f5(.)x1             2c(,)x1                             DIFFER
   ... (24 more divergent offsets)
==== MECHANISM CONTEXT (involved fuzzers only) ====
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

--- naive_ngram4 ---
**Instrumentation**: naive's edge counters, but the executor installs
an `NgramHook` (`HookableInProcessExecutor`) that folds a rolling
history of the last 4 edge IDs into the map index. A map slot
therefore encodes a length-4 edge path (an n-gram of N=4) rather than
a single edge.

**Feedback**: `MaxMapFeedback` over the n-gram-indexed map — a "new
bucket" is a previously-unseen 4-edge path tuple.

**Mutators**: naive's havoc + token stack. No I2S, no CMP_MAP. Stages
are `[mutator]` (`LineageMutator`, names captured).

**Observed `mutation_op` in seed metadata**: havoc/token names only;
no dash rows.

**Per-execution cost**: edge increment plus a rolling 4-edge-history
update per executed edge.

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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_6325.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6325,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive_ngram4>naive (ngram_coverage), value_profile>naive (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6325 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6325 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6325 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).