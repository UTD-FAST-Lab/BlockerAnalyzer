==== BLOCKER ====
Target: libxml2
Branch ID: 7326
Location: /src/libxml2/xmlsave.c:988:9
Enclosing function: xmlsave.c:xmlNodeDumpOutputInternal
Source line:         case XML_CDATA_SECTION_NODE:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           1        9          0  loser (value_profile vs value_profile_cmplog)
value_profile                    2        8          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog); winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=14.50h  loser=21.80h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.70  dur_div=7.30h  hit_div=2
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 34  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=14.50h  loser=22.70h
  avg hitcount on branch: winner=2  loser=1
  prob_div=0.60  dur_div=8.20h  hit_div=1
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7326/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlsave.c:xmlNodeDumpOutputInternal (/src/libxml2/xmlsave.c:809-1068) ---
[ ]   807   */
[ ]   808  static void
[B]   809  xmlNodeDumpOutputInternal(xmlSaveCtxtPtr ctxt, xmlNodePtr cur) {
[B]   810      int format = ctxt->format;
[B]   811      xmlNodePtr tmp, root, unformattedNode = NULL, parent;
[B]   812      xmlAttrPtr attr;
[B]   813      xmlChar *start, *end;
[B]   814      xmlOutputBufferPtr buf;
[ ]   815  
[B]   816      if (cur == NULL) return;
[B]   817      buf = ctxt->buf;
[ ]   818  
[B]   819      root = cur;
[B]   820      parent = cur->parent;
[B]   821      while (1) {
[B]   822          switch (cur->type) {
[ ]   823          case XML_DOCUMENT_NODE:
[ ]   824          case XML_HTML_DOCUMENT_NODE:
[ ]   825  	    xmlDocContentDumpOutput(ctxt, (xmlDocPtr) cur);
[ ]   826  	    break;
[ ]   827  
[B]   828          case XML_DTD_NODE:
[B]   829              xmlDtdDumpOutput(ctxt, (xmlDtdPtr) cur);
[B]   830              break;
[ ]   831  
[ ]   832          case XML_DOCUMENT_FRAG_NODE:
[ ]   833              /* Always validate cur->parent when descending. */
[ ]   834              if ((cur->parent == parent) && (cur->children != NULL)) {
[ ]   835                  parent = cur;
[ ]   836                  cur = cur->children;
[ ]   837                  continue;
[ ]   838              }
[ ]   839  	    break;
[ ]   840  
[ ]   841          case XML_ELEMENT_DECL:
[ ]   842              xmlBufDumpElementDecl(buf->buffer, (xmlElementPtr) cur);
[ ]   843              break;
[ ]   844  
[ ]   845          case XML_ATTRIBUTE_DECL:
[ ]   846              xmlBufDumpAttributeDecl(buf->buffer, (xmlAttributePtr) cur);
[ ]   847              break;
[ ]   848  
[ ]   849          case XML_ENTITY_DECL:
[ ]   850              xmlBufDumpEntityDecl(buf->buffer, (xmlEntityPtr) cur);
[ ]   851              break;
[ ]   852  
[B]   853          case XML_ELEMENT_NODE:
[B]   854  	    if ((cur != root) && (ctxt->format == 1) &&
[B]   855                  (xmlIndentTreeOutput))
[ ]   856  		xmlOutputBufferWrite(buf, ctxt->indent_size *
[ ]   857  				     (ctxt->level > ctxt->indent_nr ?
[ ]   858  				      ctxt->indent_nr : ctxt->level),
[ ]   859  				     ctxt->indent);
[ ]   860  
[ ]   861              /*
[ ]   862               * Some users like lxml are known to pass nodes with a corrupted
[ ]   863               * tree structure. Fall back to a recursive call to handle this
[ ]   864               * case.
[ ]   865               */
[B]   866              if ((cur->parent != parent) && (cur->children != NULL)) {
[ ]   867                  xmlNodeDumpOutputInternal(ctxt, cur);
[ ]   868                  break;
[ ]   869              }
[ ]   870  
[B]   871              xmlOutputBufferWrite(buf, 1, "<");
[B]   872              if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) {
[ ]   873                  xmlOutputBufferWriteString(buf, (const char *)cur->ns->prefix);
[ ]   874                  xmlOutputBufferWrite(buf, 1, ":");
[ ]   875              }
[B]   876              xmlOutputBufferWriteString(buf, (const char *)cur->name);
[B]   877              if (cur->nsDef)
[L]   878                  xmlNsListDumpOutputCtxt(ctxt, cur->nsDef);
[B]   879              for (attr = cur->properties; attr != NULL; attr = attr->next)
[L]   880                  xmlAttrDumpOutput(ctxt, attr);
[ ]   881  
[B]   882              if (cur->children == NULL) {
[B]   883                  if ((ctxt->options & XML_SAVE_NO_EMPTY) == 0) {
[B]   884                      if (ctxt->format == 2)
[ ]   885                          xmlOutputBufferWriteWSNonSig(ctxt, 0);
[B]   886                      xmlOutputBufferWrite(buf, 2, "/>");
[B]   887                  } else {
[ ]   888                      if (ctxt->format == 2)
[ ]   889                          xmlOutputBufferWriteWSNonSig(ctxt, 1);
[ ]   890                      xmlOutputBufferWrite(buf, 3, "></");
[ ]   891                      if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) {
[ ]   892                          xmlOutputBufferWriteString(buf,
[ ]   893                                  (const char *)cur->ns->prefix);
[ ]   894                          xmlOutputBufferWrite(buf, 1, ":");
[ ]   895                      }
[ ]   896                      xmlOutputBufferWriteString(buf, (const char *)cur->name);
[ ]   897                      if (ctxt->format == 2)
[ ]   898                          xmlOutputBufferWriteWSNonSig(ctxt, 0);
[ ]   899                      xmlOutputBufferWrite(buf, 1, ">");
[ ]   900                  }
[B]   901              } else {
[B]   902                  if (ctxt->format == 1) {
[ ]   903                      tmp = cur->children;
[ ]   904                      while (tmp != NULL) {
[ ]   905                          if ((tmp->type == XML_TEXT_NODE) ||
[ ]   906                              (tmp->type == XML_CDATA_SECTION_NODE) ||
[ ]   907                              (tmp->type == XML_ENTITY_REF_NODE)) {
[ ]   908                              ctxt->format = 0;
[ ]   909                              unformattedNode = cur;
[ ]   910                              break;
[ ]   911                          }
[ ]   912                          tmp = tmp->next;
[ ]   913                      }
[ ]   914                  }
[B]   915                  if (ctxt->format == 2)
[ ]   916                      xmlOutputBufferWriteWSNonSig(ctxt, 1);
[B]   917                  xmlOutputBufferWrite(buf, 1, ">");
[B]   918                  if (ctxt->format == 1) xmlOutputBufferWrite(buf, 1, "\n");
[B]   919                  if (ctxt->level >= 0) ctxt->level++;
[B]   920                  parent = cur;
[B]   921                  cur = cur->children;
[B]   922                  continue;
[B]   923              }
[ ]   924  
[B]   925              break;
[ ]   926  
[B]   927          case XML_TEXT_NODE:
[B]   928  	    if (cur->content == NULL)
[ ]   929                  break;
[B]   930  	    if (cur->name != xmlStringTextNoenc) {
[B]   931                  xmlOutputBufferWriteEscape(buf, cur->content, ctxt->escape);
[B]   932  	    } else {
[ ]   933  		/*
[ ]   934  		 * Disable escaping, needed for XSLT
[ ]   935  		 */
[ ]   936  		xmlOutputBufferWriteString(buf, (const char *) cur->content);
[ ]   937  	    }
[B]   938  	    break;
[ ]   939  
[ ]   940          case XML_PI_NODE:
[ ]   941  	    if ((cur != root) && (ctxt->format == 1) && (xmlIndentTreeOutput))
[ ]   942  		xmlOutputBufferWrite(buf, ctxt->indent_size *
[ ]   943  				     (ctxt->level > ctxt->indent_nr ?
[ ]   944  				      ctxt->indent_nr : ctxt->level),
[ ]   945  				     ctxt->indent);
[ ]   946  
[ ]   947              if (cur->content != NULL) {
[ ]   948                  xmlOutputBufferWrite(buf, 2, "<?");
[ ]   949                  xmlOutputBufferWriteString(buf, (const char *)cur->name);
[ ]   950                  if (cur->content != NULL) {
[ ]   951                      if (ctxt->format == 2)
[ ]   952                          xmlOutputBufferWriteWSNonSig(ctxt, 0);
[ ]   953                      else
[ ]   954                          xmlOutputBufferWrite(buf, 1, " ");
[ ]   955                      xmlOutputBufferWriteString(buf,
[ ]   956                              (const char *)cur->content);
[ ]   957                  }
[ ]   958                  xmlOutputBufferWrite(buf, 2, "?>");
[ ]   959              } else {
[ ]   960                  xmlOutputBufferWrite(buf, 2, "<?");
[ ]   961                  xmlOutputBufferWriteString(buf, (const char *)cur->name);
[ ]   962                  if (ctxt->format == 2)
[ ]   963                      xmlOutputBufferWriteWSNonSig(ctxt, 0);
[ ]   964                  xmlOutputBufferWrite(buf, 2, "?>");
[ ]   965              }
[ ]   966              break;
[ ]   967  
[ ]   968          case XML_COMMENT_NODE:
[ ]   969  	    if ((cur != root) && (ctxt->format == 1) && (xmlIndentTreeOutput))
[ ]   970  		xmlOutputBufferWrite(buf, ctxt->indent_size *
[ ]   971  				     (ctxt->level > ctxt->indent_nr ?
[ ]   972  				      ctxt->indent_nr : ctxt->level),
[ ]   973  				     ctxt->indent);
[ ]   974  
[ ]   975              if (cur->content != NULL) {
[ ]   976                  xmlOutputBufferWrite(buf, 4, "<!--");
[ ]   977                  xmlOutputBufferWriteString(buf, (const char *)cur->content);
[ ]   978                  xmlOutputBufferWrite(buf, 3, "-->");
[ ]   979              }
[ ]   980              break;
[ ]   981  
[ ]   982          case XML_ENTITY_REF_NODE:
[ ]   983              xmlOutputBufferWrite(buf, 1, "&");
[ ]   984              xmlOutputBufferWriteString(buf, (const char *)cur->name);
[ ]   985              xmlOutputBufferWrite(buf, 1, ";");
[ ]   986              break;
[ ]   987  
[W]   988          case XML_CDATA_SECTION_NODE: <-- BLOCKER
[W]   989              if (cur->content == NULL || *cur->content == '\0') {
[ ]   990                  xmlOutputBufferWrite(buf, 12, "<![CDATA[]]>");
[W]   991              } else {
[W]   992                  start = end = cur->content;
[W]   993                  while (*end != '\0') {
[W]   994                      if ((*end == ']') && (*(end + 1) == ']') &&
[W]   995                          (*(end + 2) == '>')) {
[ ]   996                          end = end + 2;
[ ]   997                          xmlOutputBufferWrite(buf, 9, "<![CDATA[");
[ ]   998                          xmlOutputBufferWrite(buf, end - start,
[ ]   999                                  (const char *)start);
[ ]  1000                          xmlOutputBufferWrite(buf, 3, "]]>");
[ ]  1001                          start = end;
[ ]  1002                      }
[W]  1003                      end++;
[W]  1004                  }
[W]  1005                  if (start != end) {
[W]  1006                      xmlOutputBufferWrite(buf, 9, "<![CDATA[");
[W]  1007                      xmlOutputBufferWriteString(buf, (const char *)start);
[W]  1008                      xmlOutputBufferWrite(buf, 3, "]]>");
[W]  1009                  }
[W]  1010              }
[W]  1011              break;
[ ]  1012  
[ ]  1013          case XML_ATTRIBUTE_NODE:
[ ]  1014              xmlAttrDumpOutput(ctxt, (xmlAttrPtr) cur);
[ ]  1015              break;
[ ]  1016  
[ ]  1017          case XML_NAMESPACE_DECL:
[ ]  1018              xmlNsDumpOutputCtxt(ctxt, (xmlNsPtr) cur);
[ ]  1019              break;
[ ]  1020  
[ ]  1021          default:
[ ]  1022              break;
[B]  1023          }
[ ]  1024  
[B]  1025          while (1) {
[B]  1026              if (cur == root)
[B]  1027                  return;
[B]  1028              if ((ctxt->format == 1) &&
[B]  1029                  (cur->type != XML_XINCLUDE_START) &&
[B]  1030                  (cur->type != XML_XINCLUDE_END))
[ ]  1031                  xmlOutputBufferWrite(buf, 1, "\n");
[B]  1032              if (cur->next != NULL) {
[B]  1033                  cur = cur->next;
[B]  1034                  break;
[B]  1035              }
[ ]  1036  
[B]  1037              cur = parent;
[ ]  1038              /* cur->parent was validated when descending. */
[B]  1039              parent = cur->parent;
[ ]  1040  
[B]  1041              if (cur->type == XML_ELEMENT_NODE) {
[B]  1042                  if (ctxt->level > 0) ctxt->level--;
[B]  1043                  if ((xmlIndentTreeOutput) && (ctxt->format == 1))
[ ]  1044                      xmlOutputBufferWrite(buf, ctxt->indent_size *
[ ]  1045                                           (ctxt->level > ctxt->indent_nr ?
[ ]  1046                                            ctxt->indent_nr : ctxt->level),
[ ]  1047                                           ctxt->indent);
[ ]  1048  
[B]  1049                  xmlOutputBufferWrite(buf, 2, "</");
[B]  1050                  if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) {
[ ]  1051                      xmlOutputBufferWriteString(buf,
[ ]  1052                              (const char *)cur->ns->prefix);
[ ]  1053                      xmlOutputBufferWrite(buf, 1, ":");
[ ]  1054                  }
[ ]  1055  
[B]  1056                  xmlOutputBufferWriteString(buf, (const char *)cur->name);
[B]  1057                  if (ctxt->format == 2)
[ ]  1058                      xmlOutputBufferWriteWSNonSig(ctxt, 0);
[B]  1059                  xmlOutputBufferWrite(buf, 1, ">");
[ ]  1060  
[B]  1061                  if (cur == unformattedNode) {
[ ]  1062                      ctxt->format = format;
[ ]  1063                      unformattedNode = NULL;
[ ]  1064                  }
[B]  1065              }
[B]  1066          }
[B]  1067      }
[B]  1068  }

--- Caller (1 hop): xmlsave.c:xmlDocContentDumpOutput (/src/libxml2/xmlsave.c:1077-1225, calls xmlsave.c:xmlNodeDumpOutputInternal at line 1206) (±10 around call site) ---
[B]  1196  	if (cur->children != NULL) {
[B]  1197  	    xmlNodePtr child = cur->children;
[ ]  1198  
[B]  1199  	    while (child != NULL) {
[B]  1200  		ctxt->level = 0;
[B]  1201  #ifdef LIBXML_HTML_ENABLED
[B]  1202  		if (is_xhtml)
[ ]  1203  		    xhtmlNodeDumpOutput(ctxt, child);
[B]  1204  		else
[B]  1205  #endif
[B]  1206  		    xmlNodeDumpOutputInternal(ctxt, child); <-- CALL
[B]  1207                  if ((child->type != XML_XINCLUDE_START) &&
[B]  1208                      (child->type != XML_XINCLUDE_END))
[B]  1209                      xmlOutputBufferWrite(buf, 1, "\n");
[B]  1210  		child = child->next;
[B]  1211  	    }
[B]  1212  	}
[B]  1213      }
[ ]  1214  
[ ]  1215      /*
[ ]  1216       * Restore the state of the saving context at the end of the document

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlsave.c:xmlDocContentDumpOutput  (/src/libxml2/xmlsave.c:1077-1225, calls xmlsave.c:xmlNodeDumpOutputInternal at line 1206)
hop 2  xmlsave.c:xmlDtdDumpOutput  (/src/libxml2/xmlsave.c:666-712, calls xmlsave.c:xmlNodeDumpOutputInternal at line 707)
hop 3  xmlsave.c:xhtmlNodeDumpOutput  (/src/libxml2/xmlsave.c:1392-1700, calls xmlsave.c:xmlDtdDumpOutput at line 1413)
hop 4  xmlSaveTree  (/src/libxml2/xmlsave.c:1860-1879, calls xmlsave.c:xhtmlNodeDumpOutput at line 1866)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       2        73  xmlsave.c:xmlEscapeEntities  (/src/libxml2/xmlsave.c:166-274)
       2        49  xmlsave.c:xmlNodeDumpOutputInternal  (/src/libxml2/xmlsave.c:809-1068)  <-- enclosing
       1        40  xmlsave.c:xmlSaveCtxtInit  (/src/libxml2/xmlsave.c:289-311)
       1        40  xmlsave.c:xmlDocContentDumpOutput  (/src/libxml2/xmlsave.c:1077-1225)
       1        40  xmlDocDumpFormatMemoryEnc  (/src/libxml2/xmlsave.c:2325-2393)
       1        40  xmlDocDumpMemory  (/src/libxml2/xmlsave.c:2407-2409)
       1        19  xmlsave.c:xmlSaveErr  (/src/libxml2/xmlsave.c:81-101)
       0        15  xmlsave.c:xmlNsDumpOutput  (/src/libxml2/xmlsave.c:591-611)
       0        15  xmlsave.c:xmlNsListDumpOutputCtxt  (/src/libxml2/xmlsave.c:635-640)
       1        10  xmlsave.c:xmlDtdDumpOutput  (/src/libxml2/xmlsave.c:666-712)
       0         7  xmlsave.c:xmlAttrSerializeContent  (/src/libxml2/xmlsave.c:393-415)
       0         7  xmlsave.c:xmlAttrDumpOutput  (/src/libxml2/xmlsave.c:722-740)
       0         7  xmlBufAttrSerializeTxtContent  (/src/libxml2/xmlsave.c:1970-2080)
       0         4  xmlsave.c:xmlSerializeHexCharRef  (/src/libxml2/xmlsave.c:109-147)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  xmlsave.c:xmlDtdDumpOutput  (/src/libxml2/xmlsave.c:666-712) ---
  d=2   L 671  T=0 F=1  T=0 F=10  if (dtd == NULL) return;
  d=2   L 672  T=0 F=1  T=0 F=10  if ((ctxt == NULL) || (ctxt->buf == NULL))
  d=2   L 672  T=0 F=1  T=0 F=10  if ((ctxt == NULL) || (ctxt->buf == NULL))
  d=2   L 677  T=0 F=1  T=0 F=10  if (dtd->ExternalID != NULL) {
  d=2   L 682  T=1 F=0  T=10 F=0  }  else if (dtd->SystemID != NULL) {
  d=2   L 686  T=1 F=0  T=10 F=0  if ((dtd->entities == NULL) && (dtd->elements == NULL) &&
  d=2   L 686  T=1 F=0  T=10 F=0  if ((dtd->entities == NULL) && (dtd->elements == NULL) &&
  d=2   L 687  T=1 F=0  T=10 F=0  (dtd->attributes == NULL) && (dtd->notations == NULL) &&
  d=2   L 687  T=1 F=0  T=10 F=0  (dtd->attributes == NULL) && (dtd->notations == NULL) &&
  d=2   L 688  T=1 F=0  T=10 F=0  (dtd->pentities == NULL)) {
--- d=2  xmlsave.c:xmlDocContentDumpOutput  (/src/libxml2/xmlsave.c:1077-1225) ---
  d=2   L1093  T=1 F=0  T=40 F=0  if ((cur->type != XML_HTML_DOCUMENT_NODE) &&
  d=2   L1094  T=0 F=1  T=0 F=40  (cur->type != XML_DOCUMENT_NODE))
  d=2   L1097  T=0 F=1  T=0 F=40  if (ctxt->encoding != NULL) {
  d=2   L1099  T=0 F=1  T=0 F=40  } else if (cur->encoding != NULL) {
  d=2   L1103  T=0 F=1  T=0 F=40  if (((cur->type == XML_HTML_DOCUMENT_NODE) &&
  d=2   L1106  T=0 F=1  T=0 F=40  (ctxt->options & XML_SAVE_AS_HTML)) {
  d=2   L1133  T=1 F=0  T=40 F=0  } else if ((cur->type == XML_DOCUMENT_NODE) ||
  d=2   L1137  T=0 F=1  T=0 F=40  if ((encoding != NULL) && (oldctxtenc == NULL) &&
  d=2   L1164  T=1 F=0  T=40 F=0  if ((ctxt->options & XML_SAVE_NO_DECL) == 0) {
  d=2   L1166  T=1 F=0  T=40 F=0  if (cur->version != NULL)
  d=2   L1170  T=0 F=1  T=0 F=40  if (encoding != NULL) {
  d=2   L1174  T=1 F=0  T=40 F=0  switch (cur->standalone) {
  d=2   L1175  T=0 F=1  T=0 F=40  case 0:
  d=2   L1178  T=0 F=1  T=0 F=40  case 1:
  d=2   L1186  T=0 F=1  T=0 F=40  if (ctxt->options & XML_SAVE_XHTML)
  d=2   L1188  T=1 F=0  T=40 F=0  if ((ctxt->options & XML_SAVE_NO_XHTML) == 0) {
  d=2   L1190  T=1 F=0  T=10 F=30  if (dtd != NULL) {
  d=2   L1192  T=0 F=1  T=0 F=10  if (is_xhtml < 0) is_xhtml = 0;
  d=2   L1196  T=1 F=0  T=40 F=0  if (cur->children != NULL) {
  d=2   L1199  T=2 F=1  T=49 F=40  while (child != NULL) {
  d=2   L1202  T=0 F=2  T=0 F=49  if (is_xhtml)
  d=2   L1207  T=2 F=0  T=49 F=0  if ((child->type != XML_XINCLUDE_START) &&
  d=2   L1208  T=2 F=0  T=49 F=0  (child->type != XML_XINCLUDE_END))
  d=2   L1218  T=0 F=1  T=0 F=40  if ((switched_encoding) && (oldctxtenc == NULL)) {
--- d=1  xmlsave.c:xmlNodeDumpOutputInternal  (/src/libxml2/xmlsave.c:809-1068) ---
  d=1   L 816  T=0 F=2  T=0 F=49  if (cur == NULL) return;
  d=1   L 823  T=0 F=6  T=0 F=194  case XML_DOCUMENT_NODE:
  d=1   L 824  T=0 F=6  T=0 F=194  case XML_HTML_DOCUMENT_NODE:
  d=1   L 828  T=1 F=5  T=10 F=184  case XML_DTD_NODE:
  d=1   L 832  T=0 F=6  T=0 F=194  case XML_DOCUMENT_FRAG_NODE:
  d=1   L 841  T=0 F=6  T=0 F=194  case XML_ELEMENT_DECL:
  d=1   L 845  T=0 F=6  T=0 F=194  case XML_ATTRIBUTE_DECL:
  d=1   L 849  T=0 F=6  T=0 F=194  case XML_ENTITY_DECL:
  d=1   L 853  T=2 F=4  T=120 F=74  case XML_ELEMENT_NODE:
  d=1   L 854  T=1 F=1  T=81 F=39  if ((cur != root) && (ctxt->format == 1) &&
  d=1   L 854  T=0 F=1  T=0 F=81  if ((cur != root) && (ctxt->format == 1) &&
  d=1   L 866  T=0 F=2  T=0 F=120  if ((cur->parent != parent) && (cur->children != NULL)) {
  d=1   L 872  T=0 F=2  T=0 F=120  if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) {
  d=1   L 877  T=0 F=2  T=15 F=105  if (cur->nsDef)
  d=1   L 879  T=0 F=2  T=7 F=120  for (attr = cur->properties; attr != NULL; attr = attr->n...
  d=1   L 882  T=1 F=1  T=62 F=58  if (cur->children == NULL) {
  d=1   L 883  T=1 F=0  T=62 F=0  if ((ctxt->options & XML_SAVE_NO_EMPTY) == 0) {
  d=1   L 884  T=0 F=1  T=0 F=62  if (ctxt->format == 2)
  d=1   L 902  T=0 F=1  T=0 F=58  if (ctxt->format == 1) {
  d=1   L 915  T=0 F=1  T=0 F=58  if (ctxt->format == 2)
  d=1   L 918  T=0 F=1  T=0 F=58  if (ctxt->format == 1) xmlOutputBufferWrite(buf, 1, "\n");
  d=1   L 919  T=1 F=0  T=58 F=0  if (ctxt->level >= 0) ctxt->level++;
  d=1   L 927  T=2 F=4  T=64 F=130  case XML_TEXT_NODE:
  d=1   L 928  T=0 F=2  T=0 F=64  if (cur->content == NULL)
  d=1   L 930  T=2 F=0  T=64 F=0  if (cur->name != xmlStringTextNoenc) {
  d=1   L 940  T=0 F=6  T=0 F=194  case XML_PI_NODE:
  d=1   L 968  T=0 F=6  T=0 F=194  case XML_COMMENT_NODE:
  d=1   L 982  T=0 F=6  T=0 F=194  case XML_ENTITY_REF_NODE:
  d=1   L 988  T=1 F=5  T=0 F=194  case XML_CDATA_SECTION_NODE:  <-- BLOCKER
  d=1   L 989  T=0 F=1  T=0 F=0  if (cur->content == NULL || *cur->content == '\0') {
  d=1   L 989  T=0 F=1  T=0 F=0  if (cur->content == NULL || *cur->content == '\0') {
  d=1   L 993  T=54 F=1  T=0 F=0  while (*end != '\0') {
  d=1   L 994  T=0 F=54  T=0 F=0  if ((*end == ']') && (*(end + 1) == ']') &&
  d=1   L1005  T=1 F=0  T=0 F=0  if (start != end) {
  d=1   L1013  T=0 F=6  T=0 F=194  case XML_ATTRIBUTE_NODE:
  d=1   L1017  T=0 F=6  T=0 F=194  case XML_NAMESPACE_DECL:
  d=1   L1021  T=0 F=6  T=0 F=194  default:
  d=1   L1026  T=2 F=4  T=49 F=145  if (cur == root)
  d=1   L1028  T=0 F=4  T=0 F=145  if ((ctxt->format == 1) &&
  d=1   L1032  T=3 F=1  T=87 F=58  if (cur->next != NULL) {
  d=1   L1041  T=1 F=0  T=58 F=0  if (cur->type == XML_ELEMENT_NODE) {
  d=1   L1042  T=1 F=0  T=58 F=0  if (ctxt->level > 0) ctxt->level--;
  d=1   L1043  T=1 F=0  T=58 F=0  if ((xmlIndentTreeOutput) && (ctxt->format == 1))
  d=1   L1043  T=0 F=1  T=0 F=58  if ((xmlIndentTreeOutput) && (ctxt->format == 1))
  d=1   L1050  T=0 F=1  T=0 F=58  if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) {
  d=1   L1057  T=0 F=1  T=0 F=58  if (ctxt->format == 2)
  d=1   L1061  T=0 F=1  T=0 F=58  if (cur == unformattedNode) {

[off-chain: 94 additional divergent branches across 10 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=008ff29e17e42a70, size=339 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=63057s, mutation_op=QwordAddMutator,ByteIncMutator,BytesDeleteMutator):
  0000: cb 00 00 00 31 32 37 37 37 32 6e 78 6d 6c 5c 0a   ....127772nxml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 0a   .0"?>.<!DOCTYPE.
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 29 cf   a SYSTEM "dtds).

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00f7af173db700b0, size=368 bytes, fuzzer=cmplog, trial=2, discovered_at=0s, mutation_op=BytesExpandMutator,DwordAddMutator,ByteRandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=027913052b5d6b70, size=141 bytes, fuzzer=cmplog, trial=2, discovered_at=28s, mutation_op=ByteFlipMutator,BytesCopyMutator,ByteDecMutator,ByteRandMutator,BytesRandSetMutator,BytesDeleteMutator):
  0000: 6b 27 0a 20 20 20 20 20 20 20 20 20 20 20 20 78   k'.            x
  0010: 6c 69 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c   li....127772.xml
  0020: 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d   \.<?xml version=
  0030: 22 31 2e 30 22 3f 3e 0a 3c 6e 6b 3a 74 79 70 1f   "1.0"?>.<nk:typ.
Seed 3 (id=0146b95b93cf0ce2, size=372 bytes, fuzzer=cmplog, trial=2, discovered_at=265s, mutation_op=ByteAddMutator,TokenInsert,BytesSwapMutator):
  0000: 4d 45 4e 54 20 62 20 28 23 50 43 44 41 54 41 29   MENT b (#PCDATA)
  0010: 3e 0a 3c 21 41 54 54 4c 49 3e 54 20 62 20 78 6d   >.<!ATTLI>T b xm
  0020: 6c 6e 73 3a 78 6c 69 6e 37 20 20 43 44 41 54 41   lns:xlin7  CDATA
  0030: 20 20 20 20 20 23 46 49 58 45 44 20 27 68 25 74        #FIXED 'h%t
Seed 4 (id=001c8c9d4510710d, size=248 bytes, fuzzer=cmplog, trial=1, discovered_at=411s, mutation_op=ByteNegMutator,BytesCopyMutator,BytesInsertMutator,ByteIncMutator,BytesSwapMutator,BytesDeleteMutator,TokenReplace):
  0000: 5f 5f 5f 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ___.127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=00ebab469d057524, size=371 bytes, fuzzer=cmplog, trial=1, discovered_at=573s, mutation_op=ByteFlipMutator,ByteNegMutator,BitFlipMutator,CrossoverReplaceMutator):
  0000: 37 58 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20   7X72.xml\.<?xml 
  0010: 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a   version="1.0"?>.
  0020: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST
  0030: 45 4d 20 22 64 74 64 73 2a 31 32 37 37 37 32 2e   EM "dtds*127772.


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  cb(.)x1                             4d(M)x4 43(C)x4 45(E)x4 37(7)x3 +22u  DIFFER
   0x0001  00(.)x1                             44(D)x4 00(.)x2 27(')x2 37(7)x2 +28u  PARTIAL
   0x0002  00(.)x1                             20( )x4 00(.)x3 32(2)x2 68(h)x2 +27u  PARTIAL
   0x0003  00(.)x1                             00(.)x5 27(')x4 74(t)x3 54(T)x2 +23u  PARTIAL
   0x0004  31(1)x1                             68(h)x5 31(1)x4 00(.)x3 20( )x2 +22u  PARTIAL
   0x0005  32(2)x1                             74(t)x5 00(.)x5 32(2)x4 78(x)x2 +21u  PARTIAL
   0x0006  37(7)x1                             37(7)x5 74(t)x5 20( )x4 00(.)x4 +17u  PARTIAL
   0x0007  37(7)x1                             37(7)x6 20( )x5 70(p)x5 6c(l)x3 +15u  PARTIAL
   0x0008  37(7)x1                             37(7)x9 3a(:)x5 20( )x4 5c(\)x4 +17u  PARTIAL
   0x0009  32(2)x1                             32(2)x7 20( )x4 0a(.)x4 2f(/)x4 +15u  PARTIAL
   0x000a  6e(n)x1                             2e(.)x7 20( )x4 77(w)x4 2f(/)x4 +15u  DIFFER
   0x000b  78(x)x1                             78(x)x7 77(w)x6 20( )x5 3f(?)x3 +15u  PARTIAL
   0x000c  6d(m)x1                             6d(m)x7 20( )x5 78(x)x4 77(w)x4 +17u  PARTIAL
   0x000d  6c(l)x1                             6c(l)x7 20( )x6 77(w)x5 6d(m)x3 +16u  PARTIAL
   0x000e  5c(\)x1                             5c(\)x6 20( )x6 6c(l)x3 6d(m)x3 +18u  PARTIAL
   0x000f  0a(.)x1                             0a(.)x8 20( )x6 6c(l)x4 37(7)x2 +17u  PARTIAL
   0x0010  3c(<)x1                             3c(<)x6 0a(.)x6 20( )x3 5c(\)x3 +19u  PARTIAL
   0x0011  3f(?)x1                             0a(.)x6 3f(?)x4 20( )x4 2f(/)x3 +19u  PARTIAL
   0x0012  78(x)x1                             78(x)x5 3c(<)x4 0a(.)x3 20( )x2 +22u  PARTIAL
   0x0013  6d(m)x1                             6d(m)x4 20( )x4 2f(/)x2 6c(l)x2 +23u  PARTIAL
   0x0014  6c(l)x1                             6c(l)x4 78(x)x4 69(i)x3 20( )x3 +20u  PARTIAL
   0x0015  20( )x1                             20( )x8 00(.)x3 2f(/)x3 6d(m)x3 +18u  PARTIAL
   0x0016  76(v)x1                             76(v)x4 31(1)x3 20( )x3 6c(l)x3 +22u  PARTIAL
   0x0017  65(e)x1                             65(e)x4 3c(<)x4 39(9)x3 2f(/)x3 +22u  PARTIAL
   0x0018  72(r)x1                             72(r)x4 37(7)x3 62(b)x3 2f(/)x3 +21u  PARTIAL
   0x0019  73(s)x1                             73(s)x3 37(7)x2 64(d)x2 3f(?)x2 +24u  PARTIAL
   0x001a  69(i)x1                             69(i)x5 2f(/)x4 78(x)x3 2e(.)x2 +22u  PARTIAL
   0x001b  6f(o)x1                             6f(o)x4 20( )x4 69(i)x3 78(x)x3 +22u  PARTIAL
   0x001c  6e(n)x1                             6e(n)x5 20( )x4 2e(.)x3 6c(l)x3 +20u  PARTIAL
   0x001d  3d(=)x1                             20( )x5 3d(=)x4 78(x)x3 6c(l)x3 +20u  PARTIAL
   0x001e  22(")x1                             20( )x7 0a(.)x4 22(")x3 6d(m)x2 +20u  PARTIAL
   0x001f  31(1)x1                             0a(.)x5 31(1)x3 3c(<)x3 3a(:)x3 +22u  PARTIAL
   0x0020  2e(.)x1                             2e(.)x5 3c(<)x4 6c(l)x3 5c(\)x2 +22u  PARTIAL
   0x0021  30(0)x1                             30(0)x4 0a(.)x4 21(!)x3 2e(.)x3 +20u  PARTIAL
   0x0022  22(")x1                             22(")x4 3c(<)x4 0a(.)x3 73(s)x2 +23u  PARTIAL
   0x0023  3f(?)x1                             3f(?)x6 20( )x3 45(E)x3 0a(.)x2 +25u  PARTIAL
   0x0024  3e(>)x1                             20( )x5 3e(>)x4 78(x)x3 54(T)x2 +26u  PARTIAL
   0x0025  0a(.)x1                             0a(.)x4 20( )x4 6d(m)x3 3e(>)x3 +23u  PARTIAL
   0x0026  3c(<)x1                             3c(<)x6 0a(.)x3 20( )x3 6c(l)x2 +24u  PARTIAL
   0x0027  21(!)x1                             21(!)x4 20( )x4 45(E)x2 0a(.)x2 +26u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7326.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7326,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>cmplog (value_profile), value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7326 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7326 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7326 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).