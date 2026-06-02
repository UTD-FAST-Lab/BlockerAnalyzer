==== BLOCKER ====
Target: libxml2
Branch ID: 7783
Location: /src/libxml2/parser.c:4846:9
Enclosing function: parser.c:xmlParseCommentComplex
Source line:     if (cur == 0)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (ctx_coverage vs naive_ctx)
cmplog                           0       10          0  REFERENCE
value_profile                    4        6          0  REFERENCE
value_profile_cmplog             1        9          0  REFERENCE
naive_ctx                       10        0          0  winner (ctx_coverage vs naive)
naive_ngram4                     3        7          0  REFERENCE
mopt                             2        8          0  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             5        5          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 35  (naive_ctx vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=8.60h  loser=20.50h
  avg hitcount on branch: winner=9  loser=0
  prob_div=1.00  dur_div=11.90h  hit_div=9
  subject-level: delta_AUC=21345840.0  p_AUC=0.0452  delta_Final=464.2  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7783/{W,L}/branch_coverage_show.txt

--- Enclosing function: parser.c:xmlParseCommentComplex (/src/libxml2/parser.c:4801-4925) ---
[ ]  4799  static void
[ ]  4800  xmlParseCommentComplex(xmlParserCtxtPtr ctxt, xmlChar *buf,
[B]  4801                         size_t len, size_t size) {
[B]  4802      int q, ql;
[B]  4803      int r, rl;
[B]  4804      int cur, l;
[B]  4805      size_t count = 0;
[B]  4806      size_t maxLength = (ctxt->options & XML_PARSE_HUGE) ?
[B]  4807                         XML_MAX_HUGE_LENGTH :
[B]  4808                         XML_MAX_TEXT_LENGTH;
[B]  4809      int inputid;
[ ]  4810  
[B]  4811      inputid = ctxt->input->id;
[ ]  4812  
[B]  4813      if (buf == NULL) {
[L]  4814          len = 0;
[L]  4815  	size = XML_PARSER_BUFFER_SIZE;
[L]  4816  	buf = (xmlChar *) xmlMallocAtomic(size);
[L]  4817  	if (buf == NULL) {
[ ]  4818  	    xmlErrMemory(ctxt, NULL);
[ ]  4819  	    return;
[ ]  4820  	}
[L]  4821      }
[B]  4822      GROW;	/* Assure there's enough input data */
[B]  4823      q = CUR_CHAR(ql);
[B]  4824      if (q == 0)
[W]  4825          goto not_terminated;
[B]  4826      if (!IS_CHAR(q)) {
[ ]  4827          xmlFatalErrMsgInt(ctxt, XML_ERR_INVALID_CHAR,
[ ]  4828                            "xmlParseComment: invalid xmlChar value %d\n",
[ ]  4829  	                  q);
[ ]  4830  	xmlFree (buf);
[ ]  4831  	return;
[ ]  4832      }
[B]  4833      NEXTL(ql);
[B]  4834      r = CUR_CHAR(rl);
[B]  4835      if (r == 0)
[ ]  4836          goto not_terminated;
[B]  4837      if (!IS_CHAR(r)) {
[ ]  4838          xmlFatalErrMsgInt(ctxt, XML_ERR_INVALID_CHAR,
[ ]  4839                            "xmlParseComment: invalid xmlChar value %d\n",
[ ]  4840  	                  r);
[ ]  4841  	xmlFree (buf);
[ ]  4842  	return;
[ ]  4843      }
[B]  4844      NEXTL(rl);
[B]  4845      cur = CUR_CHAR(l);
[B]  4846      if (cur == 0) <-- BLOCKER
[W]  4847          goto not_terminated;
[B]  4848      while (IS_CHAR(cur) && /* checked */
[B]  4849             ((cur != '>') ||
[B]  4850  	    (r != '-') || (q != '-'))) {
[B]  4851  	if ((r == '-') && (q == '-')) {
[B]  4852  	    xmlFatalErr(ctxt, XML_ERR_HYPHEN_IN_COMMENT, NULL);
[B]  4853  	}
[B]  4854  	if (len + 5 >= size) {
[L]  4855  	    xmlChar *new_buf;
[L]  4856              size_t new_size;
[ ]  4857  
[L]  4858  	    new_size = size * 2;
[L]  4859  	    new_buf = (xmlChar *) xmlRealloc(buf, new_size);
[L]  4860  	    if (new_buf == NULL) {
[ ]  4861  		xmlFree (buf);
[ ]  4862  		xmlErrMemory(ctxt, NULL);
[ ]  4863  		return;
[ ]  4864  	    }
[L]  4865  	    buf = new_buf;
[L]  4866              size = new_size;
[L]  4867  	}
[B]  4868  	COPY_BUF(ql,buf,len,q);
[B]  4869  	q = r;
[B]  4870  	ql = rl;
[B]  4871  	r = cur;
[B]  4872  	rl = l;
[ ]  4873  
[B]  4874  	count++;
[B]  4875  	if (count > 50) {
[L]  4876  	    SHRINK;
[L]  4877  	    GROW;
[L]  4878  	    count = 0;
[L]  4879              if (ctxt->instate == XML_PARSER_EOF) {
[ ]  4880  		xmlFree(buf);
[ ]  4881  		return;
[ ]  4882              }
[L]  4883  	}
[B]  4884  	NEXTL(l);
[B]  4885  	cur = CUR_CHAR(l);
[B]  4886  	if (cur == 0) {
[B]  4887  	    SHRINK;
[B]  4888  	    GROW;
[B]  4889  	    cur = CUR_CHAR(l);
[B]  4890  	}
[ ]  4891  
[B]  4892          if (len > maxLength) {
[ ]  4893              xmlFatalErrMsgStr(ctxt, XML_ERR_COMMENT_NOT_FINISHED,
[ ]  4894                           "Comment too big found", NULL);
[ ]  4895              xmlFree (buf);
[ ]  4896              return;
[ ]  4897          }
[B]  4898      }
[B]  4899      buf[len] = 0;
[B]  4900      if (cur == 0) {
[B]  4901  	xmlFatalErrMsgStr(ctxt, XML_ERR_COMMENT_NOT_FINISHED,
[B]  4902  	                     "Comment not terminated \n<!--%.50s\n", buf);
[B]  4903      } else if (!IS_CHAR(cur)) {
[B]  4904          xmlFatalErrMsgInt(ctxt, XML_ERR_INVALID_CHAR,
[B]  4905                            "xmlParseComment: invalid xmlChar value %d\n",
[B]  4906  	                  cur);
[B]  4907      } else {
[ ]  4908  	if (inputid != ctxt->input->id) {
[ ]  4909  	    xmlFatalErrMsg(ctxt, XML_ERR_ENTITY_BOUNDARY,
[ ]  4910  		           "Comment doesn't start and stop in the same"
[ ]  4911                             " entity\n");
[ ]  4912  	}
[ ]  4913          NEXT;
[ ]  4914  	if ((ctxt->sax != NULL) && (ctxt->sax->comment != NULL) &&
[ ]  4915  	    (!ctxt->disableSAX))
[ ]  4916  	    ctxt->sax->comment(ctxt->userData, buf);
[ ]  4917      }
[B]  4918      xmlFree(buf);
[B]  4919      return;
[W]  4920  not_terminated:
[W]  4921      xmlFatalErrMsgStr(ctxt, XML_ERR_COMMENT_NOT_FINISHED,
[W]  4922  			 "Comment not terminated\n", NULL);
[W]  4923      xmlFree(buf);
[W]  4924      return;
[B]  4925  }

--- Caller (1 hop): xmlParseComment (/src/libxml2/parser.c:4941-5106, calls parser.c:xmlParseCommentComplex at line 5103) (±10 around call site) ---
[ ]  5093                      return;
[ ]  5094                  }
[B]  5095  		in++;
[B]  5096  		ctxt->input->col++;
[B]  5097  	    }
[B]  5098  	    in++;
[B]  5099  	    ctxt->input->col++;
[B]  5100  	    goto get_more;
[B]  5101  	}
[B]  5102      } while (((*in >= 0x20) && (*in <= 0x7F)) || (*in == 0x09) || (*in == 0x0a));
[B]  5103      xmlParseCommentComplex(ctxt, buf, len, size); <-- CALL
[B]  5104      ctxt->instate = state;
[B]  5105      return;
[B]  5106  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlParseComment  (/src/libxml2/parser.c:4941-5106, calls parser.c:xmlParseCommentComplex at line 5103)
hop 3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033, calls xmlParseComment at line 9997)
hop 3  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParseComment at line 6970)
hop 4  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 4  xmlParseContent  (/src/libxml2/parser.c:10045-10057, calls parser.c:xmlParseContentInternal at line 10048)
hop 4  xmlParseElement  (/src/libxml2/parser.c:10076-10094, calls parser.c:xmlParseContentInternal at line 10080)
hop 4  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 5  parser.c:xmlParseExternalEntityPrivate  (/src/libxml2/parser.c:12831-13042, calls xmlParseContent at line 12969)
hop 5  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503, calls parser.c:xmlParseConditionalSections at line 8475)
hop 5  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls xmlParseElement at line 10941)
hop 5  xmlParseExtParsedEnt  (/src/libxml2/parser.c:11002-11091, calls xmlParseContent at line 11073)
hop 5  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 6  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 6  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440, calls parser.c:xmlParseInternalSubset at line 8428)
hop 6  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls parser.c:xmlParseExternalEntityPrivate at line 7303)
hop 6  xmlSAXParseEntity  (/src/libxml2/parser.c:13716-13745, calls xmlParseExtParsedEnt at line 13731)
hop 6  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 6  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 7  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseDocTypeDecl at line 11958)
hop 7  xmlParseEntity  (/src/libxml2/parser.c:13761-13763, calls xmlSAXParseEntity at line 13762)
hop 7  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)
hop 7  xmlValidateDocument  (/src/libxml2/valid.c:6896-6954, calls xmlParseDTD at line 6921)
hop 8  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 8  xmlParseFile  (/src/libxml2/parser.c:14048-14050, calls xmlSAXParseFile at line 14049)
hop 8  xmlRecoverFile  (/src/libxml2/parser.c:14067-14069, calls xmlSAXParseFile at line 14068)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      68       993  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)
     543       177  parser.c:xmlFatalErrMsgStr  (/src/libxml2/parser.c:632-647)
      73       229  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      10        48  parser.c:xmlParseLookupString  (/src/libxml2/parser.c:11137-11161)
       0        36  xmlParsePITarget  (/src/libxml2/parser.c:5123-5155)
       0        36  xmlParsePI  (/src/libxml2/parser.c:5233-5371)
      28         0  xmlParseReference  (/src/libxml2/parser.c:7173-7586)
      28         0  xmlParseEntityRef  (/src/libxml2/parser.c:7619-7769)
       7        29  parser.c:xmlParseElementStart  (/src/libxml2/parser.c:10106-10226)
       0        15  xmlParseStartTag  (/src/libxml2/parser.c:8632-8752)
       0        12  xmlSplitQName  (/src/libxml2/parser.c:2970-3118)
       0         9  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
       0         9  xmlParseAttribute  (/src/libxml2/parser.c:8542-8600)
       0         6  xmlParseVersionInfo  (/src/libxml2/parser.c:10347-10378)
       0         6  xmlParseXMLDecl  (/src/libxml2/parser.c:10658-10766)
... (15 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=8  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=8   L12141  T=0 F=0  T=15 F=0  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=8   L12141  T=0 F=59  T=15 F=97  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=8   L12238  T=10 F=49  T=0 F=97  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L12248  T=4 F=6  T=28 F=6  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
--- d=7  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=7   L11471  T=4 F=302  T=28 F=70  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L11553  T=0 F=20  T=4 F=28  if ((cur == '<') && (next == '?')) {
  d=7   L11553  T=20 F=0  T=32 F=2  if ((cur == '<') && (next == '?')) {
  d=7   L11555  T=0 F=0  T=0 F=4  if (avail < 5) goto done;
  d=7   L11556  T=0 F=0  T=4 F=0  if ((!terminate) &&
  d=7   L11557  T=0 F=0  T=0 F=4  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=7   L11559  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=7   L11559  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=7   L11562  T=0 F=0  T=4 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=7   L11563  T=0 F=0  T=4 F=0  (ctxt->input->cur[3] == 'm') &&
  d=7   L11564  T=0 F=0  T=4 F=0  (ctxt->input->cur[4] == 'l') &&
  d=7   L11572  T=0 F=0  T=0 F=4  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=7   L11581  T=0 F=0  T=4 F=0  if ((ctxt->encoding == NULL) &&
  d=7   L11582  T=0 F=0  T=0 F=4  (ctxt->input->encoding != NULL))
  d=7   L11584  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=7   L11584  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=7   L11585  T=0 F=0  T=2 F=2  (!ctxt->disableSAX))
  d=7   L11632  T=2 F=51  T=0 F=35  if (cur != '<') {
  d=7   L11635  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L11635  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L11639  T=29 F=0  T=19 F=6  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=7   L11648  T=22 F=0  T=6 F=10  if (ctxt->sax2)
  d=7   L11657  T=8 F=14  T=0 F=16  if (name == NULL) {
  d=7   L11660  T=8 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L11660  T=8 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L11670  T=0 F=0  T=0 F=2  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=7   L11670  T=0 F=14  T=2 F=14  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=7   L11707  T=0 F=14  T=6 F=10  if (RAW == '>') {
  d=7   L11722  T=2 F=284  T=2 F=82  if ((avail < 2) && (ctxt->inputNr == 1))
  d=7   L11727  T=36 F=248  T=26 F=56  if ((cur == '<') && (next == '/')) {
  d=7   L11730  T=36 F=248  T=26 F=56  } else if ((cur == '<') && (next == '?')) {
  d=7   L11736  T=8 F=28  T=0 F=26  } else if ((cur == '<') && (next != '!')) {
  d=7   L11736  T=36 F=248  T=26 F=56  } else if ((cur == '<') && (next != '!')) {
  d=7   L11739  T=28 F=248  T=26 F=56  } else if ((cur == '<') && (next == '!') &&
  d=7   L11740  T=28 F=0  T=18 F=8  (ctxt->input->cur[2] == '-') &&
  d=7   L11742  T=0 F=28  T=8 F=10  if ((!terminate) &&
  d=7   L11743  T=0 F=0  T=8 F=0  (!xmlParseLookupString(ctxt, 4, "-->", 3)))
  d=7   L11747  T=0 F=0  T=8 F=0  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=7   L11747  T=0 F=248  T=8 F=56  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=7   L11748  T=0 F=0  T=0 F=8  (ctxt->input->cur[2] == '[') &&
  d=7   L11758  T=0 F=248  T=8 F=56  } else if ((cur == '<') && (next == '!') &&
  d=7   L11758  T=0 F=0  T=8 F=0  } else if ((cur == '<') && (next == '!') &&
  d=7   L11759  T=0 F=0  T=0 F=8  (avail < 9)) {
  d=7   L11761  T=0 F=248  T=8 F=56  } else if (cur == '<') {
  d=7   L11765  T=28 F=220  T=0 F=56  } else if (cur == '&') {
  d=7   L11766  T=0 F=28  T=0 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=7   L11782  T=220 F=0  T=56 F=0  if ((ctxt->inputNr == 1) &&
  d=7   L11783  T=218 F=2  T=55 F=1  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=7   L11784  T=0 F=0  T=0 F=5  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=7   L11784  T=0 F=218  T=5 F=50  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=7   L11905  T=0 F=411  T=2 F=253  case XML_PARSER_PROLOG:
  d=7   L11908  T=0 F=32  T=0 F=70  if (ctxt->input->buf == NULL)
  d=7   L11914  T=0 F=32  T=0 F=70  if (avail < 2)
  d=7   L11918  T=30 F=2  T=70 F=0  if ((cur == '<') && (next == '?')) {
  d=7   L11918  T=0 F=30  T=0 F=70  if ((cur == '<') && (next == '?')) {
  d=7   L11929  T=16 F=14  T=54 F=16  } else if ((cur == '<') && (next == '!') &&
  d=7   L11929  T=30 F=2  T=70 F=0  } else if ((cur == '<') && (next == '!') &&
  d=7   L11930  T=16 F=0  T=52 F=2  (ctxt->input->cur[2] == '-') &&
  d=7   L11931  T=16 F=0  T=52 F=0  (ctxt->input->cur[3] == '-')) {
  d=7   L11932  T=10 F=6  T=36 F=16  if ((!terminate) &&
  d=7   L11933  T=10 F=0  T=36 F=0  (!xmlParseLookupString(ctxt, 4, "-->", 3)))
  d=7   L11940  T=0 F=6  T=0 F=16  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L11942  T=16 F=0  T=16 F=2  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=7   L11943  T=0 F=14  T=2 F=14  (cur == '<') && (next == '!') &&
  d=7   L11943  T=14 F=2  T=16 F=0  (cur == '<') && (next == '!') &&
  d=7   L11944  T=0 F=0  T=2 F=0  (ctxt->input->cur[2] == 'D') &&
  d=7   L11945  T=0 F=0  T=2 F=0  (ctxt->input->cur[3] == 'O') &&
  d=7   L11946  T=0 F=0  T=2 F=0  (ctxt->input->cur[4] == 'C') &&
  d=7   L11947  T=0 F=0  T=2 F=0  (ctxt->input->cur[5] == 'T') &&
  d=7   L11948  T=0 F=0  T=2 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=7   L11949  T=0 F=0  T=2 F=0  (ctxt->input->cur[7] == 'P') &&
  d=7   L11950  T=0 F=0  T=2 F=0  (ctxt->input->cur[8] == 'E')) {
  d=7   L11951  T=0 F=0  T=2 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=7   L11951  T=0 F=0  T=0 F=2  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=7   L11959  T=0 F=0  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L11961  T=0 F=0  T=0 F=2  if (RAW == '[') {
  d=7   L11972  T=0 F=0  T=2 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=7   L11972  T=0 F=0  T=2 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=7   L11973  T=0 F=0  T=2 F=0  (ctxt->sax->externalSubset != NULL))
  d=7   L11985  T=14 F=2  T=16 F=0  } else if ((cur == '<') && (next == '!') &&
--- d=6  xmlParseReference  (/src/libxml2/parser.c:7173-7586) ---
  d=6   L7181  T=0 F=28  T=0 F=0  if (RAW != '&')
  d=6   L7187  T=0 F=28  T=0 F=0  if (NXT(1) == '#') {
  d=6   L7233  T=28 F=0  T=0 F=0  if (ent == NULL) return;
--- d=6  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440) ---
  d=6   L8396  T=0 F=0  T=0 F=4  if (name == NULL) {
  d=6   L8409  T=0 F=0  T=4 F=0  if ((URI != NULL) || (ExternalID != NULL)) {
  d=6   L8420  T=0 F=0  T=4 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=6   L8420  T=0 F=0  T=4 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=6   L8421  T=0 F=0  T=3 F=1  (!ctxt->disableSAX))
  d=6   L8423  T=0 F=0  T=0 F=4  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L8430  T=0 F=0  T=0 F=4  if (RAW == '[')
  d=6   L8436  T=0 F=0  T=0 F=4  if (RAW != '>') {
--- d=5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=5   L10846  T=0 F=10  T=2 F=15  if (enc != XML_CHAR_ENCODING_NONE) {
  d=5   L10872  T=0 F=0  T=0 F=2  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=5   L10873  T=0 F=0  T=0 F=2  (ctxt->instate == XML_PARSER_EOF)) {
  d=5   L10884  T=10 F=0  T=16 F=1  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10888  T=10 F=0  T=16 F=1  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=5   L10907  T=0 F=0  T=0 F=2  if (RAW == '[') {
  d=5   L10918  T=0 F=0  T=2 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=5   L10918  T=0 F=0  T=2 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=5   L10919  T=0 F=0  T=1 F=1  (!ctxt->disableSAX))
  d=5   L10922  T=0 F=0  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10950  T=7 F=0  T=4 F=5  if (RAW != 0) {
  d=5   L10965  T=10 F=0  T=16 F=1  if ((ctxt->myDoc != NULL) &&
--- d=4  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=4   L10077  T=7 F=0  T=5 F=4  if (xmlParseElementStart(ctxt) != 0)
  d=4   L10081  T=0 F=0  T=0 F=4  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10084  T=0 F=0  T=4 F=0  if (CUR == 0) {
--- d=3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=3   L9973  T=0 F=0  T=112 F=4  while ((RAW != 0) &&
  d=3   L9974  T=0 F=0  T=112 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=3   L9980  T=0 F=0  T=61 F=51  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9980  T=0 F=0  T=36 F=25  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9995  T=0 F=0  T=25 F=51  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9995  T=0 F=0  T=9 F=16  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9996  T=0 F=0  T=4 F=0  (NXT(2) == '-') && (NXT(3) == '-')) {
  d=3   L9996  T=0 F=0  T=4 F=5  (NXT(2) == '-') && (NXT(3) == '-')) {
  d=3   L10004  T=0 F=0  T=21 F=51  else if (*cur == '<') {
  d=3   L10005  T=0 F=0  T=1 F=20  if (NXT(1) == '/') {
  d=3   L10006  T=0 F=0  T=0 F=1  if (ctxt->nameNr <= nameNr)
  d=3   L10019  T=0 F=0  T=0 F=51  else if (*cur == '&') {
--- d=2  xmlParseComment  (/src/libxml2/parser.c:4941-5106) ---
  d=2   L4984  T=1050 F=154  T=307 F=18  ((*in >= 0x20) && (*in < '-')) ||
  d=2   L4984  T=481 F=569  T=97 F=210  ((*in >= 0x20) && (*in < '-')) ||
  d=2   L4985  T=135 F=588  T=0 F=228  (*in == 0x09)) {
  d=2   L4990  T=11 F=577  T=18 F=210  if (*in == 0xA) {
  d=2   L4994  T=0 F=11  T=6 F=18  } while (*in == 0xA);
  d=2   L5001  T=540 F=37  T=173 F=37  if (nbchar > 0) {
  d=2   L5002  T=540 F=0  T=173 F=0  if ((ctxt->sax != NULL) &&
  d=2   L5003  T=540 F=0  T=173 F=0  (ctxt->sax->comment != NULL)) {
  d=2   L5004  T=37 F=503  T=32 F=141  if (buf == NULL) {
  d=2   L5005  T=35 F=0  T=6 F=18  if ((*in == '-') && (in[1] == '-'))
  d=2   L5016  T=35 F=468  T=6 F=135  } else if (len + nbchar + 1 >= size) {
  d=2   L5020  T=0 F=35  T=0 F=6  if (new_buf == NULL) {
  d=2   L5033  T=0 F=577  T=0 F=210  if (len > maxLength) {
  d=2   L5040  T=0 F=577  T=0 F=210  if (*in == 0xA) {
  d=2   L5044  T=0 F=577  T=0 F=210  if (*in == 0xD) {
  d=2   L5056  T=0 F=577  T=0 F=210  if (ctxt->instate == XML_PARSER_EOF) {
  d=2   L5061  T=540 F=37  T=170 F=40  if (*in == '-') {
  d=2   L5062  T=494 F=46  T=112 F=58  if (in[1] == '-') {
  d=2   L5063  T=0 F=494  T=0 F=112  if (in[2] == '>') {
  d=2   L5083  T=457 F=37  T=85 F=27  if (buf != NULL) {
  d=2   L5091  T=0 F=494  T=0 F=112  if (ctxt->instate == XML_PARSER_EOF) {
  d=2   L5102  T=29 F=8  T=40 F=0  } while (((*in >= 0x20) && (*in <= 0x7F)) || (*in == 0x09...
--- d=1  parser.c:xmlParseCommentComplex  (/src/libxml2/parser.c:4801-4925) ---
  d=1   L4813  T=0 F=37  T=8 F=32  if (buf == NULL) {
  d=1   L4817  T=0 F=0  T=0 F=8  if (buf == NULL) {
  d=1   L4824  T=8 F=29  T=0 F=40  if (q == 0)
  d=1   L4846  T=23 F=6  T=0 F=40  if (cur == 0)  <-- BLOCKER
  d=1   L4849  T=176 F=0  T=5560 F=94  ((cur != '>') ||
  d=1   L4850  T=0 F=0  T=94 F=0  (r != '-') || (q != '-'))) {
  d=1   L4851  T=48 F=128  T=1390 F=4260  if ((r == '-') && (q == '-')) {
  d=1   L4851  T=32 F=16  T=956 F=443  if ((r == '-') && (q == '-')) {
  d=1   L4854  T=0 F=176  T=34 F=5620  if (len + 5 >= size) {
  d=1   L4860  T=0 F=0  T=0 F=34  if (new_buf == NULL) {
  d=1   L4875  T=0 F=176  T=86 F=5570  if (count > 50) {
  d=1   L4879  T=0 F=0  T=0 F=86  if (ctxt->instate == XML_PARSER_EOF) {
  d=1   L4886  T=4 F=172  T=17 F=5640  if (cur == 0) {
  d=1   L4892  T=0 F=176  T=0 F=5660  if (len > maxLength) {
  d=1   L4900  T=4 F=2  T=17 F=23  if (cur == 0) {
  d=1   L4903  T=2 F=0  T=23 F=0  } else if (!IS_CHAR(cur)) {

[off-chain: 464 additional divergent branches across 49 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=109dbd12cddec189, size=247 bytes, fuzzer=naive_ctx, trial=1, discovered_at=11157s, mutation_op=WordInterestingMutator):
  0000: 41 54 41 20 ee ee 96 98 00 20 20 3c 62 20 78 c1   ATA .....  <b x.
  0010: 0a 1a 96 98 00 20 84 84 84 84 84 84 84 84 84 84   ..... ..........
  0020: 20 3c 0a ff ff 0a 5c 0a 3c 41 54 41 20 09 20 38    <....\.<ATA . 8
  0030: 3c 21 2d 2d 2d 2d 2d 2d 2d 2d 09 00 01 09 09 20   <!--------..... 
Seed 2 (id=935a637b473a8f52, size=216 bytes, fuzzer=naive_ctx, trial=1, discovered_at=11160s, mutation_op=BytesDeleteMutator,ByteInterestingMutator,BitFlipMutator,WordAddMutator,ByteDecMutator,BytesInsertCopyMutator):
  0000: 41 54 41 28 ee ee 96 98 00 20 20 3c 62 20 78 c1   ATA(.....  <b x.
  0010: 0a 1a 96 98 00 20 84 84 84 84 84 84 84 84 84 84   ..... ..........
  0020: 20 3c 0a ff ff 0a 5c 0a 3c 41 54 41 20 09 20 38    <....\.<ATA . 8
  0030: 3c 21 2d 2d 2d 2d 2d 2d 2d 2d 09 00 01 09 09 20   <!--------..... 
Seed 3 (id=83133e7eae273e81, size=256 bytes, fuzzer=naive_ctx, trial=1, discovered_at=13671s, mutation_op=ByteDecMutator,CrossoverReplaceMutator,CrossoverInsertMutator,QwordAddMutator,TokenInsert):
  0000: 41 54 41 20 ee ee 96 98 00 20 20 3c 62 20 78 c1   ATA .....  <b x.
  0010: 0a 1a 96 98 00 20 84 84 84 84 84 84 84 84 84 84   ..... ..........
  0020: 20 3c 0a ff ff 0a 5c 0a 3c 41 54 41 20 09 20 38    <....\.<ATA . 8
  0030: 3c 21 2d 2d 2d 2d 2d 2d 2d 2d 09 09 09 3a 78 6c   <!--------...:xl
Seed 4 (id=3433a29bf1a4db87, size=252 bytes, fuzzer=naive_ctx, trial=1, discovered_at=16187s, mutation_op=ByteInterestingMutator,BytesRandInsertMutator,DwordInterestingMutator):
  0000: 41 54 41 20 ee ee 96 98 00 20 20 3c 62 20 78 c1   ATA .....  <b x.
  0010: 00 00 03 e8 00 20 84 84 84 84 84 84 84 84 84 84   ..... ..........
  0020: 20 3c 0a ff ff 0a 5c 0a 3c 41 54 41 20 09 20 38    <....\.<ATA . 8
  0030: 3c 21 2d 2d 2d 2d 2d 2d 2d 2d 09 09 09 09 09 20   <!--------..... 
Seed 5 (id=644fa0231c345262, size=139 bytes, fuzzer=naive_ctx, trial=1, discovered_at=21858s, mutation_op=BytesInsertCopyMutator,TokenInsert,BytesDeleteMutator,BytesSetMutator,ByteRandMutator):
  0000: 96 98 00 28 20 3c 4a ff 00 0a 5c 0a 3c 21 2d 2d   ...( <J...\.<!--
  0010: 2d 2d 2d 2d 2d 2d 20 20 3c 64 3e 0a 20 20 09 09   ------  <d>.  ..
  0020: 20 2d 2d 2d 2d 2d 2d 2d 2d 2d 2d 2d 2d 20 09 09    ------------ ..
  0030: 20 2d 2d 2d 2d 2d 2d 20 09 09 20 2d 2d 2d 2d 2d    ------ .. -----

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=65e3697d6e827111, size=198 bytes, fuzzer=naive, trial=1, discovered_at=5013s, mutation_op=BytesCopyMutator,TokenReplace,ByteFlipMutator,BytesInsertCopyMutator,DwordAddMutator,BytesDeleteMutator):
  0000: 65 72 73 7f 6f 6e 3d 35 29 20 20 06 00 00 00 31   ers.on=5)  ....1
  0010: 44 4f 43 54 74 50 45 20 61 20 32 37 33 7f 6d 6c   DOCTtPE a 273.ml
  0020: 5c 0a 3c c0 20 20 20 20 20 20 20 78 6d 6c 10 76   \.<.       xml.v
  0030: 65 72 73 69 6f 6e c2 22 31 2e 05 ff ff 05 0a 3c   ersion."1......<
Seed 2 (id=2a575047f30d3eb8, size=320 bytes, fuzzer=naive, trial=1, discovered_at=6812s, mutation_op=ByteFlipMutator):
  0000: 65 72 73 7f 6f 6e 3d 35 29 20 20 06 00 00 00 31   ers.on=5)  ....1
  0010: 44 4f 43 54 59 50 45 20 61 20 32 37 33 7f 6d 6c   DOCTYPE a 273.ml
  0020: 5c 0a 3c c0 20 20 20 20 20 20 20 78 6d 6c 10 76   \.<.       xml.v
  0030: 65 72 73 69 6f 6e 3d 22 31 2e 05 ff ff 05 0a 3c   ersion="1......<
Seed 3 (id=08b75ca85d4cdd43, size=212 bytes, fuzzer=naive, trial=1, discovered_at=7812s, mutation_op=BytesExpandMutator,BytesRandInsertMutator):
  0000: 2e 64 74 64 5c 0a 3c 21 2d 2d 2d 2d 2d f7 f7 f7   .dtd\.<!-----...
  0010: f7 f7 f7 f6 f7 f7 f7 f7 f7 f7 45 4c 45 0d 0d 0d   ..........ELE...
  0020: 0d 3c 21 45 4c 45 4d 20 62 20 28 23 50 43 44 41   .<!ELEM b (#PCDA
  0030: 54 41 29 3e 0a 3c 4d 20 62 20 28 23 50 43 44 41   TA)>.<M b (#PCDA
Seed 4 (id=adc2631e2b97be93, size=507 bytes, fuzzer=naive, trial=2, discovered_at=8049s, mutation_op=BytesDeleteMutator,ByteDecMutator,BytesInsertMutator,ByteRandMutator,BytesInsertCopyMutator,ByteFlipMutator):
  0000: 2e 64 74 64 5c 0a 3c 21 2d 2d 2d 2d 2d 2d 2d 2d   .dtd\.<!--------
  0010: 2d 2d 2d 62 2a 29 3e 0a 0a 3c 21 45 4c 45 4d 45   ---b*)>..<!ELEME
  0020: 4e 54 20 62 20 4b 23 50 bc 44 41 54 41 29 3e 0a   NT b K#P.DATA)>.
  0030: 3c 21 41 54 54 4b 49 53 44 41 54 41 29 3e 0a 3c   <!ATTKISDATA)>.<
Seed 5 (id=a19dc961552da126, size=59 bytes, fuzzer=naive, trial=4, discovered_at=8318s, mutation_op=ByteRandMutator,DwordInterestingMutator,BytesExpandMutator,CrossoverReplaceMutator,QwordAddMutator,BytesRandSetMutator,ByteDecMutator):
  0000: de cc ff ff ff ff 74 64 5c 0a 3c 21 2d 2d d3 2d   ......td\.<!--.-
  0010: 65 66 3d 22 67 74 74 70 3a 2f 2f 66 61 6b 0a 0a   ef="gttp://fak..
  0020: 0a 0a 0a b3 0a 0a 2d 2d 2d 2d 2d 2d 2d 2d 2e 64   ......--------.d
  0030: 74 64 70 0a 3c 21 54 20 cb cc 62                  tdp.<!T ..b


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  41(A)x8 96(.)x2                     65(e)x2 2e(.)x2 c6(.)x2 cc(.)x2 +8u  DIFFER
   0x0001  54(T)x8 98(.)x2                     cc(.)x3 72(r)x2 64(d)x2 20( )x2 +7u  DIFFER
   0x0002  41(A)x6 00(.)x2 bf(.)x1 43(C)x1     74(t)x3 73(s)x2 78(x)x2 cc(.)x2 +8u  PARTIAL
   0x0003  20( )x7 28(()x3                     7f(.)x2 64(d)x2 6d(m)x2 cc(.)x2 +9u  PARTIAL
   0x0004  ee(.)x8 20( )x2                     6f(o)x2 5c(\)x2 20( )x2 6c(l)x2 +8u  PARTIAL
   0x0005  ee(.)x8 3c(<)x2                     6e(n)x2 0a(.)x2 20( )x2 5c(\)x2 +8u  DIFFER
   0x0006  96(.)x7 4a(J)x2 49(I)x1             3d(=)x2 3c(<)x2 0a(.)x2 2b(+)x2 +9u  DIFFER
   0x0007  98(.)x7 ff(.)x2 53(S)x1             35(5)x2 21(!)x2 3c(<)x2 2b(+)x2 +9u  DIFFER
   0x0008  00(.)x9 4f(O)x1                     2d(-)x3 29())x2 00(.)x2 49(I)x2 +7u  PARTIAL
   0x0009  20( )x7 0a(.)x2 2d(-)x1             20( )x3 2d(-)x2 00(.)x2 70(p)x2 +7u  PARTIAL
   0x000a  20( )x7 5c(\)x2 38(8)x1             20( )x3 6c(l)x3 2d(-)x2 68(h)x2 +7u  PARTIAL
   0x000b  3c(<)x7 0a(.)x2 38(8)x1             2d(-)x3 06(.)x2 65(e)x2 74(t)x2 +8u  DIFFER
   0x000c  62(b)x7 3c(<)x2 35(5)x1             2d(-)x4 00(.)x2 0a(.)x2 3e(>)x2 +6u  DIFFER
   0x000d  20( )x7 21(!)x2 39(9)x1             2d(-)x3 00(.)x2 0a(.)x2 70(p)x2 +8u  PARTIAL
   0x000e  78(x)x7 2d(-)x3                     00(.)x2 2d(-)x2 3c(<)x2 3a(:)x2 +9u  PARTIAL
   0x000f  c1(.)x7 2d(-)x2 37(7)x1             2d(-)x3 31(1)x2 21(!)x2 2f(/)x2 +8u  PARTIAL
   0x0010  0a(.)x5 00(.)x2 2d(-)x2 96(.)x1     2d(-)x4 44(D)x2 2f(/)x2 f7(.)x1 +8u  PARTIAL
   0x0011  1a(.)x5 00(.)x2 2d(-)x2 98(.)x1     2d(-)x5 4f(O)x2 23(#)x2 f7(.)x1 +7u  PARTIAL
   0x0012  96(.)x5 03(.)x2 2d(-)x2 00(.)x1     2d(-)x5 43(C)x2 2f(/)x2 f7(.)x1 +7u  PARTIAL
   0x0013  98(.)x5 e8(.)x2 2d(-)x2 20( )x1     2d(-)x3 54(T)x2 27(')x2 f6(.)x1 +9u  PARTIAL
   0x0014  00(.)x7 2d(-)x2 20( )x1             6c(l)x2 2d(-)x2 d2(.)x2 2e(.)x2 +9u  PARTIAL
   0x0015  20( )x7 2d(-)x2 3c(<)x1             2d(-)x3 50(P)x2 2e(.)x2 f7(.)x1 +9u  PARTIAL
   0x0016  84(.)x7 20( )x2 62(b)x1             2d(-)x3 45(E)x2 2e(.)x2 f7(.)x1 +9u  PARTIAL
   0x0017  84(.)x7 20( )x3                     2d(-)x5 20( )x3 0a(.)x2 f7(.)x1 +6u  PARTIAL
   0x0018  84(.)x7 3c(<)x2 78(x)x1             0a(.)x4 2d(-)x3 61(a)x2 3a(:)x2 +6u  DIFFER
   0x0019  84(.)x7 64(d)x2 c1(.)x1             2d(-)x3 20( )x2 3c(<)x2 0a(.)x2 +8u  DIFFER
   0x001a  84(.)x7 3e(>)x2 0a(.)x1             2d(-)x3 32(2)x2 0a(.)x2 45(E)x1 +9u  PARTIAL
   0x001b  84(.)x7 0a(.)x2 1a(.)x1             2d(-)x3 37(7)x2 0a(.)x2 4c(L)x1 +9u  PARTIAL
   0x001c  84(.)x7 20( )x2 96(.)x1             0a(.)x3 2d(-)x3 33(3)x2 45(E)x1 +8u  DIFFER
   0x001d  84(.)x7 20( )x2 98(.)x1             2d(-)x4 7f(.)x2 0a(.)x2 0d(.)x1 +8u  PARTIAL
   0x001e  84(.)x7 09(.)x2 00(.)x1             0a(.)x4 2d(-)x3 6d(m)x2 0d(.)x1 +7u  PARTIAL
   0x001f  84(.)x7 09(.)x1 20( )x1 55(U)x1     0a(.)x3 2d(-)x3 6c(l)x2 0d(.)x1 +8u  PARTIAL
   0x0020  20( )x8 84(.)x1 53(S)x1             0a(.)x3 5c(\)x2 20( )x2 2d(-)x2 +7u  PARTIAL
   0x0021  3c(<)x7 2d(-)x2 84(.)x1             0a(.)x5 72(r)x2 3c(<)x1 54(T)x1 +8u  PARTIAL
   0x0022  0a(.)x7 2d(-)x1 84(.)x1 41(A)x1     20( )x3 3c(<)x2 0a(.)x2 2d(-)x2 +7u  PARTIAL
   0x0023  ff(.)x7 2d(-)x1 84(.)x1 53(S)x1     c0(.)x2 20( )x2 2d(-)x2 2e(.)x2 +8u  PARTIAL
   0x0024  ff(.)x7 2d(-)x1 84(.)x1 43(C)x1     20( )x4 0a(.)x2 3e(>)x2 2d(-)x2 +6u  PARTIAL
   0x0025  0a(.)x7 2d(-)x1 84(.)x1 49(I)x1     20( )x4 0a(.)x3 2d(-)x2 2e(.)x2 +6u  PARTIAL
   0x0026  5c(\)x7 2d(-)x1 84(.)x1 49(I)x1     2d(-)x3 20( )x2 21(!)x2 3c(<)x2 +6u  PARTIAL
   0x0027  0a(.)x7 2d(-)x1 84(.)x1 09(.)x1     2d(-)x5 20( )x4 21(!)x2 62(b)x2 +4u  PARTIAL
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

--- naive_ctx ---
**Instrumentation**: naive's SanitizerCoverage edge counters, but the
executor installs a `CtxHook` (`HookableInProcessExecutor`). The hook
keeps a running hash of the current call context (caller chain) and
folds it into the edge-map index, so the same basic-block edge is
recorded at different map slots depending on the call path that
reached it.

**Feedback**: the same `MaxMapFeedback` edge-bucket signal as naive,
computed over the context-indexed map — a "new bucket" is a new
(call-context, edge) pair rather than a bare edge.

**Mutators**: naive's havoc + token stack. No `I2SRandReplace`, no
CMP_MAP. Stages are `[mutator]` (`LineageMutator`, names captured).

**Observed `mutation_op` in seed metadata**: havoc/token names only;
no ParentInfo-only / dash rows.

**Per-execution cost**: one edge-counter increment per executed edge
plus a context-hash update per call/return.

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_7783.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7783,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive_ctx>naive (ctx_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7783 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7783 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7783 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).