==== BLOCKER ====
Target: libxml2
Branch ID: 6809
Location: /src/libxml2/parser.c:11351:29
Enclosing function: parser.c:xmlCheckCdataPush
Source line: 	    else if ((c == 0xA) || (c == 0xD) || (c == 0x9))
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0        9          1  REFERENCE
cmplog                           2        6          2  REFERENCE
value_profile                    2        8          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        0          2  winner (I2S vs value_profile)
naive_ctx                        3        5          2  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        3        7          0  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                         6        4          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 34  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=0  unreached=2
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=4.12h  loser=16.20h
  avg hitcount on branch: winner=9  loser=11
  prob_div=0.80  dur_div=12.07h  hit_div=2
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6809/{W,L}/branch_coverage_show.txt

--- Enclosing function: parser.c:xmlCheckCdataPush (/src/libxml2/parser.c:11338-11392) ---
[ ] 11336   */
[ ] 11337  static int
[B] 11338  xmlCheckCdataPush(const xmlChar *utf, int len, int complete) {
[B] 11339      int ix;
[B] 11340      unsigned char c;
[B] 11341      int codepoint;
[ ] 11342  
[B] 11343      if ((utf == NULL) || (len <= 0))
[ ] 11344          return(0);
[ ] 11345  
[B] 11346      for (ix = 0; ix < len;) {      /* string is 0-terminated */
[B] 11347          c = utf[ix];
[B] 11348          if ((c & 0x80) == 0x00) {	/* 1-byte code, starts with 10 */
[B] 11349  	    if (c >= 0x20)
[B] 11350  		ix++;
[B] 11351  	    else if ((c == 0xA) || (c == 0xD) || (c == 0x9)) <-- BLOCKER
[B] 11352  	        ix++;
[L] 11353  	    else
[L] 11354  	        return(-ix);
[B] 11355  	} else if ((c & 0xe0) == 0xc0) {/* 2-byte code, starts with 110 */
[ ] 11356  	    if (ix + 2 > len) return(complete ? -ix : ix);
[ ] 11357  	    if ((utf[ix+1] & 0xc0 ) != 0x80)
[ ] 11358  	        return(-ix);
[ ] 11359  	    codepoint = (utf[ix] & 0x1f) << 6;
[ ] 11360  	    codepoint |= utf[ix+1] & 0x3f;
[ ] 11361  	    if (!xmlIsCharQ(codepoint))
[ ] 11362  	        return(-ix);
[ ] 11363  	    ix += 2;
[B] 11364  	} else if ((c & 0xf0) == 0xe0) {/* 3-byte code, starts with 1110 */
[ ] 11365  	    if (ix + 3 > len) return(complete ? -ix : ix);
[ ] 11366  	    if (((utf[ix+1] & 0xc0) != 0x80) ||
[ ] 11367  	        ((utf[ix+2] & 0xc0) != 0x80))
[ ] 11368  		    return(-ix);
[ ] 11369  	    codepoint = (utf[ix] & 0xf) << 12;
[ ] 11370  	    codepoint |= (utf[ix+1] & 0x3f) << 6;
[ ] 11371  	    codepoint |= utf[ix+2] & 0x3f;
[ ] 11372  	    if (!xmlIsCharQ(codepoint))
[ ] 11373  	        return(-ix);
[ ] 11374  	    ix += 3;
[B] 11375  	} else if ((c & 0xf8) == 0xf0) {/* 4-byte code, starts with 11110 */
[ ] 11376  	    if (ix + 4 > len) return(complete ? -ix : ix);
[ ] 11377  	    if (((utf[ix+1] & 0xc0) != 0x80) ||
[ ] 11378  	        ((utf[ix+2] & 0xc0) != 0x80) ||
[ ] 11379  		((utf[ix+3] & 0xc0) != 0x80))
[ ] 11380  		    return(-ix);
[ ] 11381  	    codepoint = (utf[ix] & 0x7) << 18;
[ ] 11382  	    codepoint |= (utf[ix+1] & 0x3f) << 12;
[ ] 11383  	    codepoint |= (utf[ix+2] & 0x3f) << 6;
[ ] 11384  	    codepoint |= utf[ix+3] & 0x3f;
[ ] 11385  	    if (!xmlIsCharQ(codepoint))
[ ] 11386  	        return(-ix);
[ ] 11387  	    ix += 4;
[ ] 11388  	} else				/* unknown encoding */
[B] 11389  	    return(-ix);
[B] 11390        }
[ ] 11391        return(ix);
[B] 11392  }

--- Caller (1 hop): parser.c:xmlParseTryOrFinish (/src/libxml2/parser.c:11404-12120, calls parser.c:xmlCheckCdataPush at line 11865) (±10 around call site) ---
[ ] 11855                              ctxt->sax->characters(ctxt->userData,
[ ] 11856                                                    ctxt->input->cur, tmp);
[ ] 11857                      }
[ ] 11858                      if (ctxt->instate == XML_PARSER_EOF)
[ ] 11859                          goto done;
[ ] 11860                      SKIPL(tmp);
[W] 11861  		} else {
[W] 11862                      int base = term - CUR_PTR;
[W] 11863  		    int tmp;
[ ] 11864  
[W] 11865  		    tmp = xmlCheckCdataPush(ctxt->input->cur, base, 1); <-- CALL
[W] 11866  		    if ((tmp < 0) || (tmp != base)) {
[W] 11867  			tmp = -tmp;
[W] 11868  			ctxt->input->cur += tmp;
[W] 11869  			goto encoding_error;
[W] 11870  		    }
[ ] 11871  		    if ((ctxt->sax != NULL) && (base == 0) &&
[ ] 11872  		        (ctxt->sax->cdataBlock != NULL) &&
[ ] 11873  		        (!ctxt->disableSAX)) {
[ ] 11874  			/*
[ ] 11875  			 * Special case to provide identical behaviour

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls parser.c:xmlCheckCdataPush at line 11844)
hop 3  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 4  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0        15  xmlSplitQName  (/src/libxml2/parser.c:2970-3118)
       3        18  xmlParseName  (/src/libxml2/parser.c:3368-3412)
      10         0  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
      10         0  parser.c:xmlParseQName  (/src/libxml2/parser.c:8884-8953)
       0         9  xmlParseStartTag  (/src/libxml2/parser.c:8632-8752)
       7         0  parser.c:xmlParseStartTag2  (/src/libxml2/parser.c:9355-9774)
       0         6  parser.c:xmlParseAttValueComplex  (/src/libxml2/parser.c:3948-4190)
       0         6  xmlParseAttValue  (/src/libxml2/parser.c:4229-4232)
       0         6  xmlParseAttribute  (/src/libxml2/parser.c:8542-8600)
       6         0  parser.c:xmlGetNamespace  (/src/libxml2/parser.c:8856-8867)
       0         6  parser.c:xmlParseAttValueInternal  (/src/libxml2/parser.c:9058-9203)
       3         0  parser.c:areBlanks  (/src/libxml2/parser.c:2889-2942)
       0         3  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
       3         0  parser.c:xmlParseAttribute2  (/src/libxml2/parser.c:9225-9323)
       1         0  parser.c:xmlIsNameStartChar  (/src/libxml2/parser.c:3152-3180)
... (1 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=3   L12170  T=2 F=0  T=4 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=3   L12171  T=2 F=0  T=4 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=3   L12171  T=0 F=2  T=0 F=4  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=3   L12211  T=1 F=0  T=2 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=3   L12212  T=1 F=0  T=2 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=3   L12212  T=1 F=0  T=2 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=3   L12214  T=0 F=1  T=0 F=2  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=3   L12274  T=1 F=0  T=2 F=0  if (ctxt->input != NULL) {
  d=3   L12275  T=0 F=1  T=0 F=2  if (ctxt->input->buf == NULL)
  d=3   L12283  T=1 F=0  T=2 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=3   L12284  T=1 F=0  T=2 F=0  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=3   L12287  T=0 F=1  T=0 F=2  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=3   L12290  T=1 F=0  T=2 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=3   L12291  T=1 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L12291  T=1 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
--- d=2  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=2   L11509  T=1 F=2  T=3 F=4  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=2   L11516  T=0 F=1  T=0 F=3  if (avail < 4)
  d=2   L11535  T=0 F=2  T=0 F=4  if (avail < 2)
  d=2   L11539  T=0 F=2  T=0 F=4  if (cur == 0) {
  d=2   L11553  T=2 F=0  T=2 F=2  if ((cur == '<') && (next == '?')) {
  d=2   L11553  T=2 F=0  T=4 F=0  if ((cur == '<') && (next == '?')) {
  d=2   L11604  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=2   L11604  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=2   L11608  T=0 F=0  T=0 F=2  if (ctxt->version == NULL) {
  d=2   L11612  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11612  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11613  T=0 F=0  T=2 F=0  (!ctxt->disableSAX))
  d=2   L11648  T=4 F=0  T=0 F=6  if (ctxt->sax2)
  d=2   L11748  T=2 F=2  T=4 F=0  (ctxt->input->cur[2] == '[') &&
  d=2   L11749  T=2 F=0  T=4 F=0  (ctxt->input->cur[3] == 'C') &&
  d=2   L11750  T=2 F=0  T=4 F=0  (ctxt->input->cur[4] == 'D') &&
  d=2   L11751  T=2 F=0  T=4 F=0  (ctxt->input->cur[5] == 'A') &&
  d=2   L11752  T=2 F=0  T=4 F=0  (ctxt->input->cur[6] == 'T') &&
  d=2   L11753  T=2 F=0  T=4 F=0  (ctxt->input->cur[7] == 'A') &&
  d=2   L11754  T=2 F=0  T=4 F=0  (ctxt->input->cur[8] == '[')) {
  d=2   L11758  T=2 F=9  T=0 F=10  } else if ((cur == '<') && (next == '!') &&
  d=2   L11758  T=2 F=0  T=0 F=0  } else if ((cur == '<') && (next == '!') &&
  d=2   L11759  T=0 F=2  T=0 F=0  (avail < 9)) {
  d=2   L11761  T=2 F=9  T=0 F=10  } else if (cur == '<') {
  d=2   L11783  T=9 F=0  T=7 F=3  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=2   L11784  T=1 F=8  T=0 F=7  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=2   L11820  T=1 F=3  T=2 F=7  if (terminate) {
  d=2   L11831  T=0 F=4  T=9 F=0  if (term == NULL) {
  d=2   L11834  T=0 F=0  T=2 F=7  if (terminate) {
  d=2   L11838  T=0 F=0  T=5 F=2  if (avail < XML_PARSER_BIG_BUFFER_SIZE + 2)
  d=2   L11845  T=0 F=0  T=4 F=0  if (tmp <= 0) {
  d=2   L11866  T=2 F=2  T=0 F=0  if ((tmp < 0) || (tmp != base)) {
  d=2   L11866  T=2 F=0  T=0 F=0  if ((tmp < 0) || (tmp != base)) {
  d=2   L11943  T=2 F=0  T=2 F=2  (cur == '<') && (next == '!') &&
  d=2   L11943  T=2 F=0  T=4 F=0  (cur == '<') && (next == '!') &&
  d=2   L11985  T=0 F=2  T=0 F=4  } else if ((cur == '<') && (next == '!') &&
  d=2   L11985  T=2 F=0  T=4 F=0  } else if ((cur == '<') && (next == '!') &&
  d=2   L11989  T=0 F=2  T=0 F=4  } else if (ctxt->instate == XML_PARSER_EPILOG) {
--- d=1  parser.c:xmlCheckCdataPush  (/src/libxml2/parser.c:11338-11392) ---
  d=1   L11351  T=2 F=0  T=11 F=4  else if ((c == 0xA) || (c == 0xD) || (c == 0x9))  <-- BLOCKER
  d=1   L11351  T=2 F=2  T=3 F=15  else if ((c == 0xA) || (c == 0xD) || (c == 0x9))  <-- BLOCKER
  d=1   L11351  T=0 F=0  T=1 F=3  else if ((c == 0xA) || (c == 0xD) || (c == 0x9))  <-- BLOCKER
  d=1   L11355  T=0 F=4  T=0 F=1  } else if ((c & 0xe0) == 0xc0) {/* 2-byte code, starts wi...
  d=1   L11364  T=0 F=4  T=0 F=1  } else if ((c & 0xf0) == 0xe0) {/* 3-byte code, starts wi...
  d=1   L11375  T=0 F=4  T=0 F=1  } else if ((c & 0xf8) == 0xf0) {/* 4-byte code, starts wi...

[off-chain: 429 additional divergent branches across 43 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=008ff29e17e42a70, size=339 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=63057s, mutation_op=QwordAddMutator,ByteIncMutator,BytesDeleteMutator):
  0000: cb 00 00 00 31 32 37 37 37 32 6e 78 6d 6c 5c 0a   ....127772nxml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 0a   .0"?>.<!DOCTYPE.
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 29 cf   a SYSTEM "dtds).

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=2901866335121450, size=142 bytes, fuzzer=value_profile, trial=3, discovered_at=7368s, mutation_op=ByteRandMutator,DwordInterestingMutator,ByteAddMutator,DwordAddMutator):
  0000: fd fe 10 00 06 00 00 00 31 32 37 37 37 32 2e 78   ........127772.x
  0010: 6d 6c 5c 0a 3c c1 78 6d 6d 20 76 65 72 73 69 6f   ml\.<.xmm versio
  0020: 6e 3d 22 31 2e 0d 0d 27 37 32 2e e8 03 6c 3c 21   n="1...'72...l<!
  0030: 5b 43 44 41 54 41 5b 0d 0d 0d 09 0d 0d 0d 0d 0d   [CDATA[.........
Seed 2 (id=291ed3a730d7bd94, size=486 bytes, fuzzer=value_profile, trial=3, discovered_at=9126s, mutation_op=ByteIncMutator,BitFlipMutator,ByteDecMutator,ByteNegMutator,ByteRandMutator):
  0000: 31 32 37 37 37 32 3f 3f 22 22 22 22 22 22 22 22   127772??""""""""
  0010: 22 22 74 64 22 5c 5c 5c 00 31 32 37 37 37 32 2e   ""td"\\\.127772.
  0020: 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69   xml\.<?xml versi
  0030: 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43   on="1.0"?>.<!DOC


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  cb(.)x1                             fd(.)x1 31(1)x1                     DIFFER
   0x0001  00(.)x1                             fe(.)x1 32(2)x1                     DIFFER
   0x0002  00(.)x1                             10(.)x1 37(7)x1                     DIFFER
   0x0003  00(.)x1                             00(.)x1 37(7)x1                     PARTIAL
   0x0004  31(1)x1                             06(.)x1 37(7)x1                     DIFFER
   0x0005  32(2)x1                             00(.)x1 32(2)x1                     PARTIAL
   0x0006  37(7)x1                             00(.)x1 3f(?)x1                     DIFFER
   0x0007  37(7)x1                             00(.)x1 3f(?)x1                     DIFFER
   0x0008  37(7)x1                             31(1)x1 22(")x1                     DIFFER
   0x0009  32(2)x1                             32(2)x1 22(")x1                     PARTIAL
   0x000a  6e(n)x1                             37(7)x1 22(")x1                     DIFFER
   0x000b  78(x)x1                             37(7)x1 22(")x1                     DIFFER
   0x000c  6d(m)x1                             37(7)x1 22(")x1                     DIFFER
   0x000d  6c(l)x1                             32(2)x1 22(")x1                     DIFFER
   0x000e  5c(\)x1                             2e(.)x1 22(")x1                     DIFFER
   0x000f  0a(.)x1                             78(x)x1 22(")x1                     DIFFER
   0x0010  3c(<)x1                             6d(m)x1 22(")x1                     DIFFER
   0x0011  3f(?)x1                             6c(l)x1 22(")x1                     DIFFER
   0x0012  78(x)x1                             5c(\)x1 74(t)x1                     DIFFER
   0x0013  6d(m)x1                             0a(.)x1 64(d)x1                     DIFFER
   0x0014  6c(l)x1                             3c(<)x1 22(")x1                     DIFFER
   0x0015  20( )x1                             c1(.)x1 5c(\)x1                     DIFFER
   0x0016  76(v)x1                             78(x)x1 5c(\)x1                     DIFFER
   0x0017  65(e)x1                             6d(m)x1 5c(\)x1                     DIFFER
   0x0018  72(r)x1                             6d(m)x1 00(.)x1                     DIFFER
   0x0019  73(s)x1                             20( )x1 31(1)x1                     DIFFER
   0x001a  69(i)x1                             76(v)x1 32(2)x1                     DIFFER
   0x001b  6f(o)x1                             65(e)x1 37(7)x1                     DIFFER
   0x001c  6e(n)x1                             72(r)x1 37(7)x1                     DIFFER
   0x001d  3d(=)x1                             73(s)x1 37(7)x1                     DIFFER
   0x001e  22(")x1                             69(i)x1 32(2)x1                     DIFFER
   0x001f  31(1)x1                             6f(o)x1 2e(.)x1                     DIFFER
   0x0020  2e(.)x1                             6e(n)x1 78(x)x1                     DIFFER
   0x0021  30(0)x1                             3d(=)x1 6d(m)x1                     DIFFER
   0x0022  22(")x1                             22(")x1 6c(l)x1                     PARTIAL
   0x0023  3f(?)x1                             31(1)x1 5c(\)x1                     DIFFER
   0x0024  3e(>)x1                             2e(.)x1 0a(.)x1                     DIFFER
   0x0025  0a(.)x1                             0d(.)x1 3c(<)x1                     DIFFER
   0x0026  3c(<)x1                             0d(.)x1 3f(?)x1                     DIFFER
   0x0027  21(!)x1                             27(')x1 78(x)x1                     DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6809.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6809,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6809 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6809 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6809 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).