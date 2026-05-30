==== BLOCKER ====
Target: libxml2
Branch ID: 6597
Location: /src/libxml2/parser.c:4985:9
Enclosing function: xmlParseComment
Source line: 	       (*in == 0x09)) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (ctx_coverage vs naive_ctx); loser (I2S vs cmplog)
cmplog                           8        2          0  winner (grimoire_structural vs grimoire); winner (I2S vs naive)
value_profile                    5        5          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                       10        0          0  winner (ctx_coverage vs naive)
naive_ngram4                     4        6          0  REFERENCE
mopt                             6        4          0  REFERENCE
minimizer                        2        8          0  REFERENCE
fast                             6        4          0  REFERENCE
grimoire                         1        9          0  loser (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire', 'naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (3) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 35  (naive_ctx vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=1.80h  loser=19.60h
  avg hitcount on branch: winner=3618  loser=8
  prob_div=0.80  dur_div=17.80h  hit_div=3610
  subject-level: delta_AUC=21345840.0  p_AUC=0.0452  delta_Final=464.2  p_final=0.001
--- Pair 2: cmplog > grimoire  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=8.70h  loser=19.40h
  avg hitcount on branch: winner=6  loser=1
  prob_div=0.70  dur_div=10.70h  hit_div=5
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002
--- Pair 3: cmplog > naive  [delta: I2S] ---
  subject 31  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=8.70h  loser=19.60h
  avg hitcount on branch: winner=6  loser=8
  prob_div=0.60  dur_div=10.90h  hit_div=2
  subject-level: delta_AUC=23254200.0  p_AUC=0.0452  delta_Final=447.3  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6597/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlParseComment (/src/libxml2/parser.c:4941-5106) ---
[ ]  4939   */
[ ]  4940  void
[B]  4941  xmlParseComment(xmlParserCtxtPtr ctxt) {
[B]  4942      xmlChar *buf = NULL;
[B]  4943      size_t size = XML_PARSER_BUFFER_SIZE;
[B]  4944      size_t len = 0;
[B]  4945      size_t maxLength = (ctxt->options & XML_PARSE_HUGE) ?
[B]  4946                         XML_MAX_HUGE_LENGTH :
[B]  4947                         XML_MAX_TEXT_LENGTH;
[B]  4948      xmlParserInputState state;
[B]  4949      const xmlChar *in;
[B]  4950      size_t nbchar = 0;
[B]  4951      int ccol;
[B]  4952      int inputid;
[ ]  4953  
[ ]  4954      /*
[ ]  4955       * Check that there is a comment right here.
[ ]  4956       */
[B]  4957      if ((RAW != '<') || (NXT(1) != '!'))
[ ]  4958          return;
[B]  4959      SKIP(2);
[B]  4960      if ((RAW != '-') || (NXT(1) != '-'))
[ ]  4961          return;
[B]  4962      state = ctxt->instate;
[B]  4963      ctxt->instate = XML_PARSER_COMMENT;
[B]  4964      inputid = ctxt->input->id;
[B]  4965      SKIP(2);
[B]  4966      SHRINK;
[B]  4967      GROW;
[ ]  4968  
[ ]  4969      /*
[ ]  4970       * Accelerated common case where input don't need to be
[ ]  4971       * modified before passing it to the handler.
[ ]  4972       */
[B]  4973      in = ctxt->input->cur;
[B]  4974      do {
[B]  4975  	if (*in == 0xA) {
[ ]  4976  	    do {
[ ]  4977  		ctxt->input->line++; ctxt->input->col = 1;
[ ]  4978  		in++;
[ ]  4979  	    } while (*in == 0xA);
[ ]  4980  	}
[B]  4981  get_more:
[B]  4982          ccol = ctxt->input->col;
[B]  4983  	while (((*in > '-') && (*in <= 0x7F)) ||
[B]  4984  	       ((*in >= 0x20) && (*in < '-')) ||
[B]  4985  	       (*in == 0x09)) { <-- BLOCKER
[B]  4986  		    in++;
[B]  4987  		    ccol++;
[B]  4988  	}
[B]  4989  	ctxt->input->col = ccol;
[B]  4990  	if (*in == 0xA) {
[B]  4991  	    do {
[B]  4992  		ctxt->input->line++; ctxt->input->col = 1;
[B]  4993  		in++;
[B]  4994  	    } while (*in == 0xA);
[B]  4995  	    goto get_more;
[B]  4996  	}
[B]  4997  	nbchar = in - ctxt->input->cur;
[ ]  4998  	/*
[ ]  4999  	 * save current set of data
[ ]  5000  	 */
[B]  5001  	if (nbchar > 0) {
[B]  5002  	    if ((ctxt->sax != NULL) &&
[B]  5003  		(ctxt->sax->comment != NULL)) {
[B]  5004  		if (buf == NULL) {
[B]  5005  		    if ((*in == '-') && (in[1] == '-'))
[B]  5006  		        size = nbchar + 1;
[L]  5007  		    else
[L]  5008  		        size = XML_PARSER_BUFFER_SIZE + nbchar;
[B]  5009  		    buf = (xmlChar *) xmlMallocAtomic(size);
[B]  5010  		    if (buf == NULL) {
[ ]  5011  		        xmlErrMemory(ctxt, NULL);
[ ]  5012  			ctxt->instate = state;
[ ]  5013  			return;
[ ]  5014  		    }
[B]  5015  		    len = 0;
[B]  5016  		} else if (len + nbchar + 1 >= size) {
[B]  5017  		    xmlChar *new_buf;
[B]  5018  		    size  += len + nbchar + XML_PARSER_BUFFER_SIZE;
[B]  5019  		    new_buf = (xmlChar *) xmlRealloc(buf, size);
[B]  5020  		    if (new_buf == NULL) {
[ ]  5021  		        xmlFree (buf);
[ ]  5022  			xmlErrMemory(ctxt, NULL);
[ ]  5023  			ctxt->instate = state;
[ ]  5024  			return;
[ ]  5025  		    }
[B]  5026  		    buf = new_buf;
[B]  5027  		}
[B]  5028  		memcpy(&buf[len], ctxt->input->cur, nbchar);
[B]  5029  		len += nbchar;
[B]  5030  		buf[len] = 0;
[B]  5031  	    }
[B]  5032  	}
[B]  5033          if (len > maxLength) {
[ ]  5034              xmlFatalErrMsgStr(ctxt, XML_ERR_COMMENT_NOT_FINISHED,
[ ]  5035                           "Comment too big found", NULL);
[ ]  5036              xmlFree (buf);
[ ]  5037              return;
[ ]  5038          }
[B]  5039  	ctxt->input->cur = in;
[B]  5040  	if (*in == 0xA) {
[ ]  5041  	    in++;
[ ]  5042  	    ctxt->input->line++; ctxt->input->col = 1;
[ ]  5043  	}
[B]  5044  	if (*in == 0xD) {
[ ]  5045  	    in++;
[ ]  5046  	    if (*in == 0xA) {
[ ]  5047  		ctxt->input->cur = in;
[ ]  5048  		in++;
[ ]  5049  		ctxt->input->line++; ctxt->input->col = 1;
[ ]  5050  		goto get_more;
[ ]  5051  	    }
[ ]  5052  	    in--;
[ ]  5053  	}
[B]  5054  	SHRINK;
[B]  5055  	GROW;
[B]  5056          if (ctxt->instate == XML_PARSER_EOF) {
[ ]  5057              xmlFree(buf);
[ ]  5058              return;
[ ]  5059          }
[B]  5060  	in = ctxt->input->cur;
[B]  5061  	if (*in == '-') {
[B]  5062  	    if (in[1] == '-') {
[B]  5063  	        if (in[2] == '>') {
[ ]  5064  		    if (ctxt->input->id != inputid) {
[ ]  5065  			xmlFatalErrMsg(ctxt, XML_ERR_ENTITY_BOUNDARY,
[ ]  5066  			               "comment doesn't start and stop in the"
[ ]  5067                                         " same entity\n");
[ ]  5068  		    }
[ ]  5069  		    SKIP(3);
[ ]  5070  		    if ((ctxt->sax != NULL) && (ctxt->sax->comment != NULL) &&
[ ]  5071  		        (!ctxt->disableSAX)) {
[ ]  5072  			if (buf != NULL)
[ ]  5073  			    ctxt->sax->comment(ctxt->userData, buf);
[ ]  5074  			else
[ ]  5075  			    ctxt->sax->comment(ctxt->userData, BAD_CAST "");
[ ]  5076  		    }
[ ]  5077  		    if (buf != NULL)
[ ]  5078  		        xmlFree(buf);
[ ]  5079  		    if (ctxt->instate != XML_PARSER_EOF)
[ ]  5080  			ctxt->instate = state;
[ ]  5081  		    return;
[ ]  5082  		}
[B]  5083  		if (buf != NULL) {
[B]  5084  		    xmlFatalErrMsgStr(ctxt, XML_ERR_HYPHEN_IN_COMMENT,
[B]  5085  		                      "Double hyphen within comment: "
[B]  5086                                        "<!--%.50s\n",
[B]  5087  				      buf);
[B]  5088  		} else
[B]  5089  		    xmlFatalErrMsgStr(ctxt, XML_ERR_HYPHEN_IN_COMMENT,
[B]  5090  		                      "Double hyphen within comment\n", NULL);
[B]  5091                  if (ctxt->instate == XML_PARSER_EOF) {
[ ]  5092                      xmlFree(buf);
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
[B]  5103      xmlParseCommentComplex(ctxt, buf, len, size);
[B]  5104      ctxt->instate = state;
[B]  5105      return;
[B]  5106  }

--- Caller (1 hop): parser.c:xmlParseTryOrFinish (/src/libxml2/parser.c:11404-12120, calls xmlParseComment at line 11745) (±10 around call site) ---
[ ] 11735  		    ctxt->instate = XML_PARSER_CONTENT;
[B] 11736  		} else if ((cur == '<') && (next != '!')) {
[W] 11737  		    ctxt->instate = XML_PARSER_START_TAG;
[W] 11738  		    break;
[B] 11739  		} else if ((cur == '<') && (next == '!') &&
[B] 11740  		           (ctxt->input->cur[2] == '-') &&
[B] 11741  			   (ctxt->input->cur[3] == '-')) {
[B] 11742  		    if ((!terminate) &&
[B] 11743  		        (!xmlParseLookupString(ctxt, 4, "-->", 3)))
[W] 11744  			goto done;
[B] 11745  		    xmlParseComment(ctxt); <-- CALL
[B] 11746  		    ctxt->instate = XML_PARSER_CONTENT;
[B] 11747  		} else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
[B] 11748  		    (ctxt->input->cur[2] == '[') &&
[B] 11749  		    (ctxt->input->cur[3] == 'C') &&
[B] 11750  		    (ctxt->input->cur[4] == 'D') &&
[B] 11751  		    (ctxt->input->cur[5] == 'A') &&
[B] 11752  		    (ctxt->input->cur[6] == 'T') &&
[B] 11753  		    (ctxt->input->cur[7] == 'A') &&
[B] 11754  		    (ctxt->input->cur[8] == '[')) {
[ ] 11755  		    SKIP(9);

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033, calls xmlParseComment at line 9997)
hop 2  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParseComment at line 6970)
hop 3  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 3  xmlParseContent  (/src/libxml2/parser.c:10045-10057, calls parser.c:xmlParseContentInternal at line 10048)
hop 3  xmlParseElement  (/src/libxml2/parser.c:10076-10094, calls parser.c:xmlParseContentInternal at line 10080)
hop 3  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 4  parser.c:xmlParseExternalEntityPrivate  (/src/libxml2/parser.c:12831-13042, calls xmlParseContent at line 12969)
hop 4  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503, calls parser.c:xmlParseConditionalSections at line 8475)
hop 4  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 4  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls xmlParseElement at line 10941)
hop 4  xmlParseExtParsedEnt  (/src/libxml2/parser.c:11002-11091, calls xmlParseContent at line 11073)
hop 4  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 5  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 5  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440, calls parser.c:xmlParseInternalSubset at line 8428)
hop 5  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls parser.c:xmlParseExternalEntityPrivate at line 7303)
hop 5  xmlSAXParseEntity  (/src/libxml2/parser.c:13716-13745, calls xmlParseExtParsedEnt at line 13731)
hop 5  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 5  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 6  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseDocTypeDecl at line 11958)
hop 6  xmlParseEntity  (/src/libxml2/parser.c:13761-13763, calls xmlSAXParseEntity at line 13762)
hop 6  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)
hop 6  xmlValidateDocument  (/src/libxml2/valid.c:6896-6954, calls xmlParseDTD at line 6921)
hop 7  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 7  xmlParseFile  (/src/libxml2/parser.c:14048-14050, calls xmlSAXParseFile at line 14049)
hop 7  xmlRecoverFile  (/src/libxml2/parser.c:14067-14069, calls xmlSAXParseFile at line 14068)
hop 8  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     300        77  parser.c:xmlFatalErrMsgStr  (/src/libxml2/parser.c:632-647)
      29         0  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
      29         0  parser.c:xmlParseQName  (/src/libxml2/parser.c:8884-8953)
      18         0  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      17         0  parser.c:xmlIsNameStartChar  (/src/libxml2/parser.c:3152-3180)
      17         0  parser.c:xmlParseNCNameComplex  (/src/libxml2/parser.c:3415-3471)
      15         0  parser.c:xmlParseStartTag2  (/src/libxml2/parser.c:9355-9774)
      14         0  parser.c:xmlGetNamespace  (/src/libxml2/parser.c:8856-8867)
      14         0  parser.c:xmlParseAttribute2  (/src/libxml2/parser.c:9225-9323)
      10         0  xmlParseReference  (/src/libxml2/parser.c:7173-7586)
      10         0  xmlParseEntityRef  (/src/libxml2/parser.c:7619-7769)
       0         9  xmlParseAttribute  (/src/libxml2/parser.c:8542-8600)
       0         9  xmlParseStartTag  (/src/libxml2/parser.c:8632-8752)
       7         0  xmlParseElementMixedContentDecl  (/src/libxml2/parser.c:6193-6284)
       7         0  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503)
... (12 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=7  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=7   L12141  T=0 F=6  T=2 F=0  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L12238  T=5 F=34  T=0 F=39  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L12248  T=0 F=15  T=12 F=4  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
--- d=6  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=6   L11471  T=0 F=131  T=12 F=50  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L11555  T=0 F=11  T=0 F=4  if (avail < 5) goto done;
  d=6   L11556  T=9 F=2  T=4 F=0  if ((!terminate) &&
  d=6   L11557  T=5 F=4  T=0 F=4  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=6   L11562  T=6 F=0  T=0 F=4  if ((ctxt->input->cur[2] == 'x') &&
  d=6   L11563  T=6 F=0  T=0 F=0  (ctxt->input->cur[3] == 'm') &&
  d=6   L11564  T=4 F=2  T=0 F=0  (ctxt->input->cur[4] == 'l') &&
  d=6   L11572  T=0 F=4  T=0 F=0  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=6   L11581  T=4 F=0  T=0 F=0  if ((ctxt->encoding == NULL) &&
  d=6   L11582  T=0 F=4  T=0 F=0  (ctxt->input->encoding != NULL))
  d=6   L11584  T=4 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11584  T=4 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11585  T=4 F=0  T=0 F=0  (!ctxt->disableSAX))
  d=6   L11594  T=2 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11594  T=2 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11595  T=2 F=0  T=4 F=0  (!ctxt->disableSAX))
  d=6   L11639  T=14 F=2  T=11 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=6   L11648  T=11 F=0  T=0 F=6  if (ctxt->sax2)
  d=6   L11657  T=1 F=10  T=0 F=6  if (name == NULL) {
  d=6   L11660  T=1 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L11660  T=1 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L11722  T=0 F=105  T=0 F=46  if ((avail < 2) && (ctxt->inputNr == 1))
  d=6   L11727  T=16 F=89  T=10 F=36  if ((cur == '<') && (next == '/')) {
  d=6   L11730  T=16 F=89  T=10 F=36  } else if ((cur == '<') && (next == '?')) {
  d=6   L11736  T=3 F=13  T=0 F=10  } else if ((cur == '<') && (next != '!')) {
  d=6   L11736  T=16 F=89  T=10 F=36  } else if ((cur == '<') && (next != '!')) {
  d=6   L11739  T=13 F=89  T=10 F=36  } else if ((cur == '<') && (next == '!') &&
  d=6   L11740  T=13 F=0  T=4 F=6  (ctxt->input->cur[2] == '-') &&
  d=6   L11741  T=13 F=0  T=4 F=0  (ctxt->input->cur[3] == '-')) {
  d=6   L11742  T=2 F=11  T=0 F=4  if ((!terminate) &&
  d=6   L11743  T=2 F=0  T=0 F=0  (!xmlParseLookupString(ctxt, 4, "-->", 3)))
  d=6   L11747  T=0 F=0  T=6 F=0  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=6   L11747  T=0 F=89  T=6 F=36  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=6   L11748  T=0 F=0  T=0 F=6  (ctxt->input->cur[2] == '[') &&
  d=6   L11758  T=0 F=89  T=6 F=36  } else if ((cur == '<') && (next == '!') &&
  d=6   L11758  T=0 F=0  T=6 F=0  } else if ((cur == '<') && (next == '!') &&
  d=6   L11759  T=0 F=0  T=0 F=6  (avail < 9)) {
  d=6   L11761  T=0 F=89  T=6 F=36  } else if (cur == '<') {
  d=6   L11765  T=10 F=79  T=0 F=36  } else if (cur == '&') {
  d=6   L11766  T=0 F=10  T=0 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=6   L11782  T=79 F=0  T=36 F=0  if ((ctxt->inputNr == 1) &&
  d=6   L11783  T=79 F=0  T=36 F=0  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=6   L11784  T=0 F=2  T=0 F=0  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=6   L11784  T=2 F=77  T=0 F=36  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=6   L11908  T=0 F=16  T=0 F=32  if (ctxt->input->buf == NULL)
  d=6   L11914  T=0 F=16  T=0 F=32  if (avail < 2)
  d=6   L11918  T=16 F=0  T=32 F=0  if ((cur == '<') && (next == '?')) {
  d=6   L11918  T=2 F=14  T=4 F=28  if ((cur == '<') && (next == '?')) {
  d=6   L11919  T=2 F=0  T=4 F=0  if ((!terminate) &&
  d=6   L11920  T=0 F=2  T=0 F=4  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=6   L11927  T=0 F=2  T=0 F=4  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L11929  T=6 F=8  T=22 F=6  } else if ((cur == '<') && (next == '!') &&
  d=6   L11929  T=14 F=0  T=28 F=0  } else if ((cur == '<') && (next == '!') &&
  d=6   L11930  T=0 F=6  T=18 F=4  (ctxt->input->cur[2] == '-') &&
  d=6   L11931  T=0 F=0  T=18 F=0  (ctxt->input->cur[3] == '-')) {
  d=6   L11932  T=0 F=0  T=12 F=6  if ((!terminate) &&
  d=6   L11933  T=0 F=0  T=12 F=0  (!xmlParseLookupString(ctxt, 4, "-->", 3)))
  d=6   L11940  T=0 F=0  T=0 F=6  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L11951  T=4 F=2  T=4 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=6   L11961  T=6 F=0  T=0 F=4  if (RAW == '[') {
  d=6   L11972  T=0 F=0  T=4 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=6   L11972  T=0 F=0  T=4 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=6   L11973  T=0 F=0  T=4 F=0  (ctxt->sax->externalSubset != NULL))
  d=6   L12007  T=11 F=176  T=0 F=127  case XML_PARSER_DTD: {
  d=6   L12008  T=7 F=4  T=0 F=0  if ((!terminate) && (!xmlParseLookupInternalSubset(ctxt)))
  d=6   L12008  T=7 F=0  T=0 F=0  if ((!terminate) && (!xmlParseLookupInternalSubset(ctxt)))
  d=6   L12011  T=4 F=0  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF)
--- d=5  xmlParseReference  (/src/libxml2/parser.c:7173-7586) ---
  d=5   L7181  T=0 F=10  T=0 F=0  if (RAW != '&')
  d=5   L7187  T=0 F=10  T=0 F=0  if (NXT(1) == '#') {
  d=5   L7233  T=10 F=0  T=0 F=0  if (ent == NULL) return;
--- d=5  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440) ---
  d=5   L8409  T=0 F=9  T=6 F=0  if ((URI != NULL) || (ExternalID != NULL)) {
  d=5   L8409  T=0 F=9  T=0 F=0  if ((URI != NULL) || (ExternalID != NULL)) {
  d=5   L8436  T=9 F=0  T=0 F=6  if (RAW != '>') {
--- d=4  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503) ---
  d=4   L8456  T=7 F=0  T=0 F=0  if (RAW == '[') {
  d=4   L8466  T=21 F=0  T=0 F=0  while (((RAW != ']') || (ctxt->inputNr > baseInputNr)) &&
  d=4   L8467  T=21 F=0  T=0 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=4   L8473  T=0 F=21  T=0 F=0  if ((ctxt->inputNr > 1) && (ctxt->input->filename != NULL...
  d=4   L8476  T=14 F=7  T=0 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=4   L8476  T=14 F=0  T=0 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=4   L8478  T=0 F=7  T=0 F=0  } else if (RAW == '%') {
--- d=4  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=4   L10846  T=3 F=4  T=0 F=8  if (enc != XML_CHAR_ENCODING_NONE) {
  d=4   L10872  T=0 F=2  T=0 F=0  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=4   L10873  T=0 F=2  T=0 F=0  (ctxt->instate == XML_PARSER_EOF)) {
  d=4   L10907  T=3 F=0  T=0 F=2  if (RAW == '[') {
  d=4   L10910  T=3 F=0  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10918  T=0 F=0  T=2 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=4   L10918  T=0 F=0  T=2 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=4   L10919  T=0 F=0  T=2 F=0  (!ctxt->disableSAX))
  d=4   L10922  T=0 F=0  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10936  T=0 F=4  T=5 F=3  if (RAW != '<') {
  d=4   L10959  T=4 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L10959  T=4 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L10965  T=4 F=0  T=8 F=0  if ((ctxt->myDoc != NULL) &&
  d=4   L10966  T=0 F=4  T=0 F=8  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=4   L10971  T=0 F=4  T=0 F=8  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=4   L10980  T=4 F=0  T=8 F=0  if (! ctxt->wellFormed) {
--- d=3  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155) ---
  d=3   L7099  T=0 F=0  T=6 F=0  if ((ctxt->encoding == NULL) &&
  d=3   L7100  T=0 F=0  T=6 F=0  (ctxt->input->end - ctxt->input->cur >= 4)) {
  d=3   L7109  T=0 F=0  T=0 F=6  if (enc != XML_CHAR_ENCODING_NONE)
  d=3   L7123  T=0 F=0  T=0 F=6  if (ctxt->myDoc == NULL) {
  d=3   L7131  T=0 F=0  T=0 F=6  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=3   L7131  T=0 F=0  T=6 F=0  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=3   L7137  T=0 F=0  T=18 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=3   L7137  T=0 F=0  T=12 F=6  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=3   L7139  T=0 F=0  T=12 F=0  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=3   L7139  T=0 F=0  T=12 F=0  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=3   L7139  T=0 F=0  T=0 F=12  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=3   L7141  T=0 F=0  T=12 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=3   L7141  T=0 F=0  T=12 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=3   L7151  T=0 F=0  T=0 F=6  if (RAW != 0) {
--- d=1  xmlParseComment  (/src/libxml2/parser.c:4941-5106) ---
  d=1   L4983  T=563 F=540  T=227 F=137  while (((*in > '-') && (*in <= 0x7F)) ||
  d=1   L4983  T=554 F=9  T=210 F=17  while (((*in > '-') && (*in <= 0x7F)) ||
  d=1   L4984  T=460 F=89  T=141 F=13  ((*in >= 0x20) && (*in < '-')) ||
  d=1   L4984  T=107 F=353  T=46 F=95  ((*in >= 0x20) && (*in < '-')) ||
  d=1   L4985  T=76 F=366  T=0 F=108  (*in == 0x09)) {  <-- BLOCKER
  d=1   L4990  T=4 F=362  T=10 F=98  if (*in == 0xA) {
  d=1   L4994  T=0 F=4  T=0 F=10  } while (*in == 0xA);
  d=1   L5001  T=344 F=18  T=78 F=20  if (nbchar > 0) {
  d=1   L5002  T=344 F=0  T=78 F=0  if ((ctxt->sax != NULL) &&
  d=1   L5003  T=344 F=0  T=78 F=0  (ctxt->sax->comment != NULL)) {
  d=1   L5004  T=18 F=326  T=17 F=61  if (buf == NULL) {
  d=1   L5005  T=18 F=0  T=15 F=2  if ((*in == '-') && (in[1] == '-'))
  d=1   L5005  T=18 F=0  T=6 F=9  if ((*in == '-') && (in[1] == '-'))
  d=1   L5016  T=25 F=301  T=6 F=55  } else if (len + nbchar + 1 >= size) {
  d=1   L5020  T=0 F=25  T=0 F=6  if (new_buf == NULL) {
  d=1   L5033  T=0 F=362  T=0 F=98  if (len > maxLength) {
  d=1   L5040  T=0 F=362  T=0 F=98  if (*in == 0xA) {
  d=1   L5044  T=0 F=362  T=0 F=98  if (*in == 0xD) {
  d=1   L5056  T=0 F=362  T=0 F=98  if (ctxt->instate == XML_PARSER_EOF) {
  d=1   L5061  T=344 F=18  T=78 F=20  if (*in == '-') {
  d=1   L5062  T=280 F=64  T=50 F=28  if (in[1] == '-') {
  d=1   L5063  T=0 F=280  T=0 F=50  if (in[2] == '>') {
  d=1   L5083  T=262 F=18  T=35 F=15  if (buf != NULL) {
  d=1   L5091  T=0 F=280  T=0 F=50  if (ctxt->instate == XML_PARSER_EOF) {

[off-chain: 428 additional divergent branches across 47 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=eaa7695e5f1f4385, size=270 bytes, fuzzer=naive_ctx, trial=1, discovered_at=11139s, mutation_op=BytesInsertMutator,WordAddMutator,ByteInterestingMutator,BytesSetMutator,ByteNegMutator,WordAddMutator):
  0000: 41 54 41 20 ee ee 96 09 09 98 00 20 20 3c 62 20   ATA .......  <b 
  0010: 78 c1 0a 7d 96 98 00 20 84 84 84 84 84 84 84 84   x..}... ........
  0020: 84 84 20 3c 0a ff ff 0a 5c 0a 3c 41 54 41 20 09   .. <....\.<ATA .
  0030: 20 38 3c 21 2d 2d 2d 2d 2d 2d 2d 2d 09 09 09 21    8<!--------...!
Seed 2 (id=4a80f044763015fa, size=344 bytes, fuzzer=naive_ctx, trial=1, discovered_at=18974s, mutation_op=ByteNegMutator,TokenInsert,DwordInterestingMutator,BytesSwapMutator,BytesDeleteMutator,ByteDecMutator,BytesRandInsertMutator):
  0000: 41 54 41 20 ee ee 96 98 00 20 20 37 62 34 78 c1   ATA .....  7b4x.
  0010: 0a 7d 96 98 00 20 84 84 84 84 84 84 84 84 84 84   .}... ..........
  0020: 20 3c 0a ff ff 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 0a    <...==========.
  0030: 5c 0a 3c 41 54 41 20 ee 11 96 98 00 20 20 3c ff   \.<ATA .....  <.
Seed 3 (id=fbb662a1a4d6f7ed, size=195 bytes, fuzzer=naive_ctx, trial=1, discovered_at=21709s, mutation_op=ByteRandMutator,BitFlipMutator,BytesCopyMutator,BytesDeleteMutator,BytesCopyMutator,BytesDeleteMutator,WordAddMutator):
  0000: 41 54 41 20 ee ee 96 97 ea 20 20 3c 62 20 78 c1   ATA .....  <b x.
  0010: 0a 7d 83 84 84 84 84 20 3c 0a ff ff 0a 5c 0a 3c   .}..... <....\.<
  0020: 41 54 41 20 09 20 38 3c 21 2d 2d 2d 2d 2d 2d 2d   ATA . 8<!-------
  0030: 2d 09 09 09 09 09 20 38 09 20 3b 3b 3b 3b 3b 3b   -..... 8. ;;;;;;
Seed 4 (id=34f2310e21fd75b1, size=227 bytes, fuzzer=naive_ctx, trial=1, discovered_at=35162s, mutation_op=BytesDeleteMutator,TokenReplace):
  0000: 41 20 20 20 41 54 41 20 20 20 21 20 00 d0 01 18   A   ATA   ! ....
  0010: 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e   l\.<?xml version
  0020: 3c 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59   <"1.0"?>.<!DOCTY
  0030: 50 45 20 61 20 53 5b 3c 21 45 4c 45 4d 45 4e 54   PE a S[<!ELEMENT
Seed 5 (id=4fa372c99ea89938, size=178 bytes, fuzzer=naive_ctx, trial=1, discovered_at=37714s, mutation_op=ByteDecMutator,BytesInsertMutator,BitFlipMutator,BitFlipMutator,CrossoverInsertMutator,BytesDeleteMutator):
  0000: 41 54 41 20 ee ee 96 98 00 20 20 3c 66 20 78 c1   ATA .....  <f x.
  0010: 0b 7d 96 98 00 1f 84 84 20 84 84 84 84 84 84 84   .}...... .......
  0020: 84 20 3c 0a ff ff 0a 5c 0a 3c 41 54 41 20 09 20   . <....\.<ATA . 
  0030: 38 3c 21 2d 2d 2d 2d 2d 2d 2d 2d 09 2d 2d 09 09   8<!--------.--..

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=65e3697d6e827111, size=198 bytes, fuzzer=naive, trial=1, discovered_at=5013s, mutation_op=BytesCopyMutator,TokenReplace,ByteFlipMutator,BytesInsertCopyMutator,DwordAddMutator,BytesDeleteMutator):
  0000: 65 72 73 7f 6f 6e 3d 35 29 20 20 06 00 00 00 31   ers.on=5)  ....1
  0010: 44 4f 43 54 74 50 45 20 61 20 32 37 33 7f 6d 6c   DOCTtPE a 273.ml
  0020: 5c 0a 3c c0 20 20 20 20 20 20 20 78 6d 6c 10 76   \.<.       xml.v
  0030: 65 72 73 69 6f 6e c2 22 31 2e 05 ff ff 05 0a 3c   ersion."1......<
Seed 2 (id=9d9938cca0652438, size=117 bytes, fuzzer=grimoire, trial=1, discovered_at=6800s, mutation_op=GrimoireExtensionMutator):
  0000: 06 78 6d 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44 4f   .xml\.<?l ?><!DO
  0010: 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64   CTYPEa SYSTEM "d
  0020: 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e   tds/127772.dtd">
  0030: 5c 0a 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74   \.dtds/127772.dt
Seed 3 (id=2a575047f30d3eb8, size=320 bytes, fuzzer=naive, trial=1, discovered_at=6812s, mutation_op=ByteFlipMutator):
  0000: 65 72 73 7f 6f 6e 3d 35 29 20 20 06 00 00 00 31   ers.on=5)  ....1
  0010: 44 4f 43 54 59 50 45 20 61 20 32 37 33 7f 6d 6c   DOCTYPE a 273.ml
  0020: 5c 0a 3c c0 20 20 20 20 20 20 20 78 6d 6c 10 76   \.<.       xml.v
  0030: 65 72 73 69 6f 6e 3d 22 31 2e 05 ff ff 05 0a 3c   ersion="1......<
Seed 4 (id=040e4a058943b780, size=163 bytes, fuzzer=naive, trial=1, discovered_at=8913s, mutation_op=DwordInterestingMutator,TokenReplace,WordInterestingMutator,WordInterestingMutator,BytesInsertCopyMutator):
  0000: 8e 8e 8e 8e 8e 73 69 6f 00 00 00 d8 ff ff ff ff   .....sio........
  0010: ff ff ff 78 6c 69 6e 6b 3a 68 72 01 00 00 00 00   ...xlink:hr.....
  0020: 20 44 60 54 41 20 21 20 20 20 22 45 4e 01 00 00    D`TA !   "EN...
  0030: f4 2d 2d 45 4c 45 4d 2f 2f 3d 2d 3d 31 2d 2d ff   .--ELEM//=-=1--.
Seed 5 (id=7432a9a1bcec6e63, size=224 bytes, fuzzer=naive, trial=1, discovered_at=9527s, mutation_op=BytesSwapMutator,BytesDeleteMutator,WordAddMutator,TokenInsert,BytesDeleteMutator):
  0000: 20 32 37 33 7f 6d 2d 2d 2d 6c 65 27 0a 20 20 20    273.m---le'.   
  0010: 2d 2d 2d 2d 2d 8e 62 20 2d 2d 2d 2d 2d 2d 2d 2d   -----.b --------
  0020: 2d 47 65 78 3e 0a 3c 21 74 22 3e 62 20 2d 2d 41   -Gex>.<!t">b --A
  0030: 54 54 4c 4d 20 20 20 20 20 20 20 20 2d 2d 2d 2d   TTLM        ----


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  41(A)x5 49(I)x1 27(')x1             65(e)x2 06(.)x2 8e(.)x1 20( )x1 +2u  DIFFER
   0x0001  54(T)x4 20( )x1 58(X)x1 09(.)x1     72(r)x2 78(x)x2 8e(.)x1 32(2)x1 +2u  DIFFER
   0x0002  41(A)x4 20( )x1 45(E)x1 09(.)x1     73(s)x2 6d(m)x2 8e(.)x1 37(7)x1 +2u  DIFFER
   0x0003  20( )x5 44(D)x1 09(.)x1             7f(.)x2 6c(l)x2 8e(.)x1 33(3)x1 +2u  DIFFER
   0x0004  ee(.)x4 41(A)x1 27(')x1 00(.)x1     6f(o)x2 5c(\)x2 8e(.)x1 7f(.)x1 +2u  DIFFER
   0x0005  ee(.)x4 54(T)x1 68(h)x1 08(.)x1     6e(n)x2 0a(.)x2 73(s)x1 6d(m)x1 +2u  DIFFER
   0x0006  96(.)x4 41(A)x1 74(t)x1 01(.)x1     3d(=)x2 3c(<)x2 69(i)x1 2d(-)x1 +2u  DIFFER
   0x0009  20( )x4 98(.)x1 01(.)x1 78(x)x1     20( )x3 00(.)x1 6c(l)x1 3f(?)x1 +2u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6597.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6597,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive_ctx>naive (ctx_coverage), cmplog>grimoire (grimoire_structural), cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6597 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6597 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6597 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).