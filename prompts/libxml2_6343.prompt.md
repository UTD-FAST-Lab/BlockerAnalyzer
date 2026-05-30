==== BLOCKER ====
Target: libxml2
Branch ID: 6343
Location: /src/libxml2/encoding.c:958:25
Enclosing function: xmlDetectCharEncoding
Source line: 	if ((in[0] == 0x00) && (in[1] == 0x00) &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        3          6  REFERENCE
cmplog                           1        9          0  REFERENCE
value_profile                    9        1          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             2        8          0  loser (I2S vs value_profile)
naive_ctx                        5        1          4  REFERENCE
naive_ngram4                     4        3          3  REFERENCE
mopt                             4        3          3  REFERENCE
minimizer                        3        3          4  REFERENCE
fast                             3        4          3  REFERENCE
grimoire                         4        6          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 34  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=2.50h  loser=18.00h
  avg hitcount on branch: winner=5  loser=2
  prob_div=0.70  dur_div=15.50h  hit_div=3
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6343/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlDetectCharEncoding (/src/libxml2/encoding.c:948-999) ---
[ ]   946  xmlCharEncoding
[ ]   947  xmlDetectCharEncoding(const unsigned char* in, int len)
[B]   948  {
[B]   949      if (in == NULL)
[ ]   950          return(XML_CHAR_ENCODING_NONE);
[B]   951      if (len >= 4) {
[B]   952  	if ((in[0] == 0x00) && (in[1] == 0x00) &&
[B]   953  	    (in[2] == 0x00) && (in[3] == 0x3C))
[ ]   954  	    return(XML_CHAR_ENCODING_UCS4BE);
[B]   955  	if ((in[0] == 0x3C) && (in[1] == 0x00) &&
[B]   956  	    (in[2] == 0x00) && (in[3] == 0x00))
[ ]   957  	    return(XML_CHAR_ENCODING_UCS4LE);
[B]   958  	if ((in[0] == 0x00) && (in[1] == 0x00) && <-- BLOCKER
[B]   959  	    (in[2] == 0x3C) && (in[3] == 0x00))
[ ]   960  	    return(XML_CHAR_ENCODING_UCS4_2143);
[B]   961  	if ((in[0] == 0x00) && (in[1] == 0x3C) &&
[B]   962  	    (in[2] == 0x00) && (in[3] == 0x00))
[ ]   963  	    return(XML_CHAR_ENCODING_UCS4_3412);
[B]   964  	if ((in[0] == 0x4C) && (in[1] == 0x6F) &&
[B]   965  	    (in[2] == 0xA7) && (in[3] == 0x94))
[ ]   966  	    return(XML_CHAR_ENCODING_EBCDIC);
[B]   967  	if ((in[0] == 0x3C) && (in[1] == 0x3F) &&
[B]   968  	    (in[2] == 0x78) && (in[3] == 0x6D))
[ ]   969  	    return(XML_CHAR_ENCODING_UTF8);
[ ]   970  	/*
[ ]   971  	 * Although not part of the recommendation, we also
[ ]   972  	 * attempt an "auto-recognition" of UTF-16LE and
[ ]   973  	 * UTF-16BE encodings.
[ ]   974  	 */
[B]   975  	if ((in[0] == 0x3C) && (in[1] == 0x00) &&
[B]   976  	    (in[2] == 0x3F) && (in[3] == 0x00))
[ ]   977  	    return(XML_CHAR_ENCODING_UTF16LE);
[B]   978  	if ((in[0] == 0x00) && (in[1] == 0x3C) &&
[B]   979  	    (in[2] == 0x00) && (in[3] == 0x3F))
[L]   980  	    return(XML_CHAR_ENCODING_UTF16BE);
[B]   981      }
[B]   982      if (len >= 3) {
[ ]   983  	/*
[ ]   984  	 * Errata on XML-1.0 June 20 2001
[ ]   985  	 * We now allow an UTF8 encoded BOM
[ ]   986  	 */
[B]   987  	if ((in[0] == 0xEF) && (in[1] == 0xBB) &&
[B]   988  	    (in[2] == 0xBF))
[ ]   989  	    return(XML_CHAR_ENCODING_UTF8);
[B]   990      }
[ ]   991      /* For UTF-16 we can recognize by the BOM */
[B]   992      if (len >= 2) {
[B]   993  	if ((in[0] == 0xFE) && (in[1] == 0xFF))
[ ]   994  	    return(XML_CHAR_ENCODING_UTF16BE);
[B]   995  	if ((in[0] == 0xFF) && (in[1] == 0xFE))
[ ]   996  	    return(XML_CHAR_ENCODING_UTF16LE);
[B]   997      }
[B]   998      return(XML_CHAR_ENCODING_NONE);
[B]   999  }

--- Caller (1 hop): parser.c:xmlParseTryOrFinish (/src/libxml2/parser.c:11404-12120, calls xmlDetectCharEncoding at line 11530) (±10 around call site) ---
[ ] 11520  		     * Get the 4 first bytes and decode the charset
[ ] 11521  		     * if enc != XML_CHAR_ENCODING_NONE
[ ] 11522  		     * plug some encoding conversion routines,
[ ] 11523  		     * else xmlSwitchEncoding will set to (default)
[ ] 11524  		     * UTF8.
[ ] 11525  		     */
[B] 11526  		    start[0] = RAW;
[B] 11527  		    start[1] = NXT(1);
[B] 11528  		    start[2] = NXT(2);
[B] 11529  		    start[3] = NXT(3);
[B] 11530  		    enc = xmlDetectCharEncoding(start, 4); <-- CALL
[B] 11531  		    xmlSwitchEncoding(ctxt, enc);
[B] 11532  		    break;
[B] 11533  		}
[ ] 11534  
[B] 11535  		if (avail < 2)
[ ] 11536  		    goto done;
[B] 11537  		cur = ctxt->input->cur[0];
[B] 11538  		next = ctxt->input->cur[1];
[B] 11539  		if (cur == 0) {
[B] 11540  		    if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlDetectCharEncoding at line 7108)
hop 2  xmlParsePEReference  (/src/libxml2/parser.c:7999-8146, calls xmlDetectCharEncoding at line 8132)
hop 3  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 3  xmlParserHandlePEReference  (/src/libxml2/parser.c:2529-2585, calls xmlParsePEReference at line 2584)
hop 3  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 3  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217, calls xmlParsePEReference at line 2174)
hop 4  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 5  xmlValidateDocument  (/src/libxml2/valid.c:6896-6954, calls xmlParseDTD at line 6921)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0        61  xmlCharEncInput  (/src/libxml2/encoding.c:2313-2392)
       0        47  encoding.c:UTF16BEToUTF8  (/src/libxml2/encoding.c:748-819)
       0        47  encoding.c:xmlEncInputChunk  (/src/libxml2/encoding.c:2030-2057)
       4        26  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120)
       0        20  parser.c:xmlParseLookupString  (/src/libxml2/parser.c:11137-11161)
       0        16  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
       6        20  parser.c:xmlDetectSAX2  (/src/libxml2/parser.c:1043-1068)
       0        12  parser.c:xmlFatalErrMsgStr  (/src/libxml2/parser.c:632-647)
       2        14  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
       6        18  xmlParseChunk  (/src/libxml2/parser.c:12135-12300)
       0         6  xmlSAX2StartDocument  (/src/libxml2/SAX2.c:958-1013)
       0         6  xmlCharEncCloseFunc  (/src/libxml2/encoding.c:2819-2887)
       0         6  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
       0         6  xmlParseName  (/src/libxml2/parser.c:3368-3412)
       0         6  xmlParsePITarget  (/src/libxml2/parser.c:5123-5155)
... (6 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217) ---
  d=3   L2139  T=0 F=0  T=16 F=0  if (((ctxt->inputNr == 1) && (ctxt->instate != XML_PARSER...
  d=3   L2139  T=0 F=0  T=16 F=0  if (((ctxt->inputNr == 1) && (ctxt->instate != XML_PARSER...
--- d=1  xmlDetectCharEncoding  (/src/libxml2/encoding.c:948-999) ---
  d=1   L 952  T=8 F=0  T=0 F=10  if ((in[0] == 0x00) && (in[1] == 0x00) &&
  d=1   L 953  T=0 F=4  T=0 F=0  (in[2] == 0x00) && (in[3] == 0x3C))
  d=1   L 953  T=4 F=4  T=0 F=0  (in[2] == 0x00) && (in[3] == 0x3C))
  d=1   L 958  T=8 F=0  T=0 F=10  if ((in[0] == 0x00) && (in[1] == 0x00) &&  <-- BLOCKER
  d=1   L 959  T=0 F=8  T=0 F=0  (in[2] == 0x3C) && (in[3] == 0x00))
  d=1   L 961  T=0 F=8  T=6 F=4  if ((in[0] == 0x00) && (in[1] == 0x3C) &&
  d=1   L 962  T=0 F=0  T=0 F=6  (in[2] == 0x00) && (in[3] == 0x00))
  d=1   L 962  T=0 F=0  T=6 F=0  (in[2] == 0x00) && (in[3] == 0x00))
  d=1   L 978  T=0 F=8  T=6 F=4  if ((in[0] == 0x00) && (in[1] == 0x3C) &&
  d=1   L 979  T=0 F=0  T=6 F=0  (in[2] == 0x00) && (in[3] == 0x3F))
  d=1   L 979  T=0 F=0  T=6 F=0  (in[2] == 0x00) && (in[3] == 0x3F))
  d=1   L 982  T=8 F=0  T=4 F=0  if (len >= 3) {
  d=1   L 987  T=0 F=8  T=0 F=4  if ((in[0] == 0xEF) && (in[1] == 0xBB) &&
  d=1   L 992  T=8 F=0  T=4 F=0  if (len >= 2) {
  d=1   L 993  T=0 F=8  T=0 F=4  if ((in[0] == 0xFE) && (in[1] == 0xFF))
  d=1   L 995  T=0 F=8  T=0 F=4  if ((in[0] == 0xFF) && (in[1] == 0xFE))

[off-chain: 397 additional divergent branches across 28 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=d17e8c479b6b27ab, size=380 bytes, fuzzer=value_profile, trial=1, discovered_at=1s, mutation_op=DwordAddMutator,BytesSetMutator,CrossoverInsertMutator,DwordAddMutator):
  0000: 06 54 41 20 20 20 20 20 23 49 4d 50 4c 49 45 44   .TA     #IMPLIED
  0010: 3e 0a 0a 5c 0a 00 00 00 31 32 37 37 37 32 2e 78   >..\....127772.x
  0020: 6d 55 43 53 34 3f 78 6d 6c 20 76 65 72 73 69 6f   mUCS4?xml versio
  0030: 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54   n="1.0"?>.<!DOCT
Seed 2 (id=bac443e768a2dda5, size=129 bytes, fuzzer=value_profile, trial=1, discovered_at=1871s, mutation_op=ByteNegMutator,CrossoverReplaceMutator,BytesInsertMutator,TokenInsert,QwordAddMutator,CrossoverReplaceMutator):
  0000: 54 1f 62 20 28 23 50 44 41 54 45 29 27 27 27 27   T.b (#PDATE)''''
  0010: 27 27 27 27 27 27 5d 5d 5d 5d 5d 5d 5d 5d 5d 5d   '''''']]]]]]]]]]
  0020: 5d 20 62 20 78 6d 94 6e 73 3a 78 6c 49 58 45 fd   ] b xm.ns:xlIXE.
  0030: ff ff ff bf ff ff ff 65 27 0a 20 20 20 20 20 78   .......e'.     x

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=dbb0d112477c5856, size=368 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=2643s, mutation_op=ByteFlipMutator,BytesCopyMutator,QwordAddMutator,ByteNegMutator):
  0000: 75 75 75 75 75 75 70 3a 2f 2f 77 77 77 2e 77 33   uuuuuup://www.w3
  0010: 2e 6f 72 67 26 31 39 39 39 2f 78 6c 69 6e 6b 7e   .org&1999/xlink~
  0020: 0a 2c 20 20 20 a0 20 20 20 20 20 20 20 78 6c 69   .,   .       xli
  0030: 6e 6b 3a 74 79 70 65 2f 5f 20 28 73 69 6d 70 6c   nk:type/_ (simpl
Seed 2 (id=dbd7ffc6491ab3b6, size=667 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=26304s, mutation_op=BytesRandSetMutator,BytesRandInsertMutator,BitFlipMutator,TokenReplace):
  0000: 25 78 6c 69 6e 6b 56 74 78 70 65 26 20 20 28 73   %xlinkVtxpe&  (s
  0010: 06 10 00 00 31 31 37 37 37 32 2e 78 02 6c 5c 0a   ....117772.x.l\.
  0020: 00 3c 00 3f 58 4d 6c 2f 76 25 64 00 69 6f 29 3d   .<.?XMl/v%d.io)=
  0030: 22 31 2e 30 22 20 20 20 20 20 20 88 6c 6b 6e 6b   "1.0"      .lknk
Seed 3 (id=480b02647aec7181, size=145 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=45000s, mutation_op=BytesRandInsertMutator,TokenReplace,ByteDecMutator):
  0000: 37 37 32 2e 64 2c 6c 5c 0a 00 3c 00 3f 59 4d 6c   772.d,l\..<.?YMl
  0010: 2f 76 25 72 95 04 04 03 04 04 04 04 04 04 04 04   /v%r............
  0020: 04 69 6f 7f 0a 0a 0a 0a 0a 0a 0a 5e 0a 69 6f 7f   .io........^.io.
  0030: 0b 0b 0b 0b 0b 0b 0b 0b 0a 0a 7a 0a 0a 0a 0a 0a   ..........z.....


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x1 54(T)x1                     75(u)x1 25(%)x1 37(7)x1             DIFFER
   0x0001  54(T)x1 1f(.)x1                     75(u)x1 78(x)x1 37(7)x1             DIFFER
   0x0002  41(A)x1 62(b)x1                     75(u)x1 6c(l)x1 32(2)x1             DIFFER
   0x0003  20( )x2                             75(u)x1 69(i)x1 2e(.)x1             DIFFER
   0x0004  20( )x1 28(()x1                     75(u)x1 6e(n)x1 64(d)x1             DIFFER
   0x0005  20( )x1 23(#)x1                     75(u)x1 6b(k)x1 2c(,)x1             DIFFER
   0x0006  20( )x1 50(P)x1                     70(p)x1 56(V)x1 6c(l)x1             DIFFER
   0x0007  20( )x1 44(D)x1                     3a(:)x1 74(t)x1 5c(\)x1             DIFFER
   0x0008  23(#)x1 41(A)x1                     2f(/)x1 78(x)x1 0a(.)x1             DIFFER
   0x0009  49(I)x1 54(T)x1                     2f(/)x1 70(p)x1 00(.)x1             DIFFER
   0x000a  4d(M)x1 45(E)x1                     77(w)x1 65(e)x1 3c(<)x1             DIFFER
   0x000b  50(P)x1 29())x1                     77(w)x1 26(&)x1 00(.)x1             DIFFER
   0x000c  4c(L)x1 27(')x1                     77(w)x1 20( )x1 3f(?)x1             DIFFER
   0x000d  49(I)x1 27(')x1                     2e(.)x1 20( )x1 59(Y)x1             DIFFER
   0x000e  45(E)x1 27(')x1                     77(w)x1 28(()x1 4d(M)x1             DIFFER
   0x000f  44(D)x1 27(')x1                     33(3)x1 73(s)x1 6c(l)x1             DIFFER
   0x0010  3e(>)x1 27(')x1                     2e(.)x1 06(.)x1 2f(/)x1             DIFFER
   0x0011  0a(.)x1 27(')x1                     6f(o)x1 10(.)x1 76(v)x1             DIFFER
   0x0012  0a(.)x1 27(')x1                     72(r)x1 00(.)x1 25(%)x1             DIFFER
   0x0013  5c(\)x1 27(')x1                     67(g)x1 00(.)x1 72(r)x1             DIFFER
   0x0014  0a(.)x1 27(')x1                     26(&)x1 31(1)x1 95(.)x1             DIFFER
   0x0015  00(.)x1 27(')x1                     31(1)x2 04(.)x1                     DIFFER
   0x0016  00(.)x1 5d(])x1                     39(9)x1 37(7)x1 04(.)x1             DIFFER
   0x0017  00(.)x1 5d(])x1                     39(9)x1 37(7)x1 03(.)x1             DIFFER
   0x0018  31(1)x1 5d(])x1                     39(9)x1 37(7)x1 04(.)x1             DIFFER
   0x0019  32(2)x1 5d(])x1                     2f(/)x1 32(2)x1 04(.)x1             PARTIAL
   0x001a  37(7)x1 5d(])x1                     78(x)x1 2e(.)x1 04(.)x1             DIFFER
   0x001b  37(7)x1 5d(])x1                     6c(l)x1 78(x)x1 04(.)x1             DIFFER
   0x001c  37(7)x1 5d(])x1                     69(i)x1 02(.)x1 04(.)x1             DIFFER
   0x001d  32(2)x1 5d(])x1                     6e(n)x1 6c(l)x1 04(.)x1             DIFFER
   0x001e  2e(.)x1 5d(])x1                     6b(k)x1 5c(\)x1 04(.)x1             DIFFER
   0x001f  78(x)x1 5d(])x1                     7e(~)x1 0a(.)x1 04(.)x1             DIFFER
   0x0020  6d(m)x1 5d(])x1                     0a(.)x1 00(.)x1 04(.)x1             DIFFER
   0x0021  55(U)x1 20( )x1                     2c(,)x1 3c(<)x1 69(i)x1             DIFFER
   0x0022  43(C)x1 62(b)x1                     20( )x1 00(.)x1 6f(o)x1             DIFFER
   0x0023  53(S)x1 20( )x1                     20( )x1 3f(?)x1 7f(.)x1             PARTIAL
   0x0024  34(4)x1 78(x)x1                     20( )x1 58(X)x1 0a(.)x1             DIFFER
   0x0025  3f(?)x1 6d(m)x1                     a0(.)x1 4d(M)x1 0a(.)x1             DIFFER
   0x0026  78(x)x1 94(.)x1                     20( )x1 6c(l)x1 0a(.)x1             DIFFER
   0x0027  6d(m)x1 6e(n)x1                     20( )x1 2f(/)x1 0a(.)x1             DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6343.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6343,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>value_profile_cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6343 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6343 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6343 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).