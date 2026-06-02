==== BLOCKER ====
Target: libxml2
Branch ID: 7327
Location: /src/libxml2/xmlsave.c:1050:21
Enclosing function: xmlsave.c:xmlNodeDumpOutputInternal
Source line:                 if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  REFERENCE
cmplog                           2        8          0  loser (grimoire_structural vs grimoire)
value_profile                    5        5          0  REFERENCE
value_profile_cmplog             6        4          0  REFERENCE
naive_ctx                        4        6          0  REFERENCE
naive_ngram4                     1        9          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        2        8          0  REFERENCE
fast                             5        5          0  REFERENCE
grimoire                         8        2          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=13.00h  loser=20.30h
  avg hitcount on branch: winner=606  loser=0
  prob_div=0.60  dur_div=7.30h  hit_div=605
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7327/{W,L}/branch_coverage_show.txt

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
[B]   878                  xmlNsListDumpOutputCtxt(ctxt, cur->nsDef);
[B]   879              for (attr = cur->properties; attr != NULL; attr = attr->next)
[B]   880                  xmlAttrDumpOutput(ctxt, attr);
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
[W]   940          case XML_PI_NODE:
[W]   941  	    if ((cur != root) && (ctxt->format == 1) && (xmlIndentTreeOutput))
[ ]   942  		xmlOutputBufferWrite(buf, ctxt->indent_size *
[ ]   943  				     (ctxt->level > ctxt->indent_nr ?
[ ]   944  				      ctxt->indent_nr : ctxt->level),
[ ]   945  				     ctxt->indent);
[ ]   946  
[W]   947              if (cur->content != NULL) {
[W]   948                  xmlOutputBufferWrite(buf, 2, "<?");
[W]   949                  xmlOutputBufferWriteString(buf, (const char *)cur->name);
[W]   950                  if (cur->content != NULL) {
[W]   951                      if (ctxt->format == 2)
[ ]   952                          xmlOutputBufferWriteWSNonSig(ctxt, 0);
[W]   953                      else
[W]   954                          xmlOutputBufferWrite(buf, 1, " ");
[W]   955                      xmlOutputBufferWriteString(buf,
[W]   956                              (const char *)cur->content);
[W]   957                  }
[W]   958                  xmlOutputBufferWrite(buf, 2, "?>");
[W]   959              } else {
[ ]   960                  xmlOutputBufferWrite(buf, 2, "<?");
[ ]   961                  xmlOutputBufferWriteString(buf, (const char *)cur->name);
[ ]   962                  if (ctxt->format == 2)
[ ]   963                      xmlOutputBufferWriteWSNonSig(ctxt, 0);
[ ]   964                  xmlOutputBufferWrite(buf, 2, "?>");
[ ]   965              }
[W]   966              break;
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
[ ]   988          case XML_CDATA_SECTION_NODE:
[ ]   989              if (cur->content == NULL || *cur->content == '\0') {
[ ]   990                  xmlOutputBufferWrite(buf, 12, "<![CDATA[]]>");
[ ]   991              } else {
[ ]   992                  start = end = cur->content;
[ ]   993                  while (*end != '\0') {
[ ]   994                      if ((*end == ']') && (*(end + 1) == ']') &&
[ ]   995                          (*(end + 2) == '>')) {
[ ]   996                          end = end + 2;
[ ]   997                          xmlOutputBufferWrite(buf, 9, "<![CDATA[");
[ ]   998                          xmlOutputBufferWrite(buf, end - start,
[ ]   999                                  (const char *)start);
[ ]  1000                          xmlOutputBufferWrite(buf, 3, "]]>");
[ ]  1001                          start = end;
[ ]  1002                      }
[ ]  1003                      end++;
[ ]  1004                  }
[ ]  1005                  if (start != end) {
[ ]  1006                      xmlOutputBufferWrite(buf, 9, "<![CDATA[");
[ ]  1007                      xmlOutputBufferWriteString(buf, (const char *)start);
[ ]  1008                      xmlOutputBufferWrite(buf, 3, "]]>");
[ ]  1009                  }
[ ]  1010              }
[ ]  1011              break;
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
[B]  1050                  if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) { <-- BLOCKER
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
      11        57  xmlsave.c:xmlEscapeEntities  (/src/libxml2/xmlsave.c:166-274)
       0        24  xmlsave.c:xmlSaveErr  (/src/libxml2/xmlsave.c:81-101)
       3        10  xmlsave.c:xmlSaveCtxtInit  (/src/libxml2/xmlsave.c:289-311)
       3        10  xmlsave.c:xmlDocContentDumpOutput  (/src/libxml2/xmlsave.c:1077-1225)
       3        10  xmlDocDumpFormatMemoryEnc  (/src/libxml2/xmlsave.c:2325-2393)
       3        10  xmlDocDumpMemory  (/src/libxml2/xmlsave.c:2407-2409)
       0         6  xmlsave.c:xmlSerializeHexCharRef  (/src/libxml2/xmlsave.c:109-147)
       7         1  xmlsave.c:xmlNsDumpOutput  (/src/libxml2/xmlsave.c:591-611)
       7         1  xmlsave.c:xmlNsListDumpOutputCtxt  (/src/libxml2/xmlsave.c:635-640)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  xmlsave.c:xmlDtdDumpOutput  (/src/libxml2/xmlsave.c:666-712) ---
  d=2   L 671  T=0 F=3  T=0 F=7  if (dtd == NULL) return;
  d=2   L 672  T=0 F=3  T=0 F=7  if ((ctxt == NULL) || (ctxt->buf == NULL))
  d=2   L 672  T=0 F=3  T=0 F=7  if ((ctxt == NULL) || (ctxt->buf == NULL))
  d=2   L 677  T=0 F=3  T=0 F=7  if (dtd->ExternalID != NULL) {
  d=2   L 682  T=3 F=0  T=7 F=0  }  else if (dtd->SystemID != NULL) {
  d=2   L 686  T=3 F=0  T=7 F=0  if ((dtd->entities == NULL) && (dtd->elements == NULL) &&
  d=2   L 686  T=3 F=0  T=7 F=0  if ((dtd->entities == NULL) && (dtd->elements == NULL) &&
  d=2   L 687  T=3 F=0  T=7 F=0  (dtd->attributes == NULL) && (dtd->notations == NULL) &&
  d=2   L 687  T=3 F=0  T=7 F=0  (dtd->attributes == NULL) && (dtd->notations == NULL) &&
  d=2   L 688  T=3 F=0  T=7 F=0  (dtd->pentities == NULL)) {
--- d=2  xmlsave.c:xmlDocContentDumpOutput  (/src/libxml2/xmlsave.c:1077-1225) ---
  d=2   L1093  T=3 F=0  T=10 F=0  if ((cur->type != XML_HTML_DOCUMENT_NODE) &&
  d=2   L1094  T=0 F=3  T=0 F=10  (cur->type != XML_DOCUMENT_NODE))
  d=2   L1097  T=0 F=3  T=0 F=10  if (ctxt->encoding != NULL) {
  d=2   L1099  T=0 F=3  T=0 F=10  } else if (cur->encoding != NULL) {
  d=2   L1103  T=0 F=3  T=0 F=10  if (((cur->type == XML_HTML_DOCUMENT_NODE) &&
  d=2   L1106  T=0 F=3  T=0 F=10  (ctxt->options & XML_SAVE_AS_HTML)) {
  d=2   L1133  T=3 F=0  T=10 F=0  } else if ((cur->type == XML_DOCUMENT_NODE) ||
  d=2   L1137  T=0 F=3  T=0 F=10  if ((encoding != NULL) && (oldctxtenc == NULL) &&
  d=2   L1164  T=3 F=0  T=10 F=0  if ((ctxt->options & XML_SAVE_NO_DECL) == 0) {
  d=2   L1166  T=3 F=0  T=10 F=0  if (cur->version != NULL)
  d=2   L1170  T=0 F=3  T=0 F=10  if (encoding != NULL) {
  d=2   L1174  T=3 F=0  T=10 F=0  switch (cur->standalone) {
  d=2   L1175  T=0 F=3  T=0 F=10  case 0:
  d=2   L1178  T=0 F=3  T=0 F=10  case 1:
  d=2   L1186  T=0 F=3  T=0 F=10  if (ctxt->options & XML_SAVE_XHTML)
  d=2   L1188  T=3 F=0  T=10 F=0  if ((ctxt->options & XML_SAVE_NO_XHTML) == 0) {
  d=2   L1190  T=3 F=0  T=7 F=3  if (dtd != NULL) {
  d=2   L1192  T=0 F=3  T=0 F=7  if (is_xhtml < 0) is_xhtml = 0;
  d=2   L1196  T=3 F=0  T=10 F=0  if (cur->children != NULL) {
  d=2   L1199  T=8 F=3  T=17 F=10  while (child != NULL) {
  d=2   L1202  T=0 F=8  T=0 F=17  if (is_xhtml)
  d=2   L1207  T=8 F=0  T=17 F=0  if ((child->type != XML_XINCLUDE_START) &&
  d=2   L1208  T=8 F=0  T=17 F=0  (child->type != XML_XINCLUDE_END))
  d=2   L1218  T=0 F=3  T=0 F=10  if ((switched_encoding) && (oldctxtenc == NULL)) {
--- d=1  xmlsave.c:xmlNodeDumpOutputInternal  (/src/libxml2/xmlsave.c:809-1068) ---
  d=1   L 816  T=0 F=8  T=0 F=17  if (cur == NULL) return;
  d=1   L 823  T=0 F=27  T=0 F=137  case XML_DOCUMENT_NODE:
  d=1   L 824  T=0 F=27  T=0 F=137  case XML_HTML_DOCUMENT_NODE:
  d=1   L 828  T=3 F=24  T=7 F=130  case XML_DTD_NODE:
  d=1   L 832  T=0 F=27  T=0 F=137  case XML_DOCUMENT_FRAG_NODE:
  d=1   L 841  T=0 F=27  T=0 F=137  case XML_ELEMENT_DECL:
  d=1   L 845  T=0 F=27  T=0 F=137  case XML_ATTRIBUTE_DECL:
  d=1   L 849  T=0 F=27  T=0 F=137  case XML_ENTITY_DECL:
  d=1   L 853  T=11 F=16  T=73 F=64  case XML_ELEMENT_NODE:
  d=1   L 854  T=8 F=3  T=63 F=10  if ((cur != root) && (ctxt->format == 1) &&
  d=1   L 854  T=0 F=8  T=0 F=63  if ((cur != root) && (ctxt->format == 1) &&
  d=1   L 866  T=0 F=11  T=0 F=73  if ((cur->parent != parent) && (cur->children != NULL)) {
  d=1   L 872  T=7 F=4  T=0 F=73  if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) {
  d=1   L 872  T=0 F=7  T=0 F=0  if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) {
  d=1   L 877  T=7 F=4  T=1 F=72  if (cur->nsDef)
  d=1   L 879  T=3 F=11  T=4 F=73  for (attr = cur->properties; attr != NULL; attr = attr->n...
  d=1   L 882  T=3 F=8  T=58 F=15  if (cur->children == NULL) {
  d=1   L 883  T=3 F=0  T=58 F=0  if ((ctxt->options & XML_SAVE_NO_EMPTY) == 0) {
  d=1   L 884  T=0 F=3  T=0 F=58  if (ctxt->format == 2)
  d=1   L 927  T=11 F=16  T=57 F=80  case XML_TEXT_NODE:
  d=1   L 928  T=0 F=11  T=0 F=57  if (cur->content == NULL)
  d=1   L 930  T=11 F=0  T=57 F=0  if (cur->name != xmlStringTextNoenc) {
  d=1   L 940  T=2 F=25  T=0 F=137  case XML_PI_NODE:
  d=1   L 941  T=0 F=2  T=0 F=0  if ((cur != root) && (ctxt->format == 1) && (xmlIndentTre...
  d=1   L 947  T=2 F=0  T=0 F=0  if (cur->content != NULL) {
  d=1   L 950  T=2 F=0  T=0 F=0  if (cur->content != NULL) {
  d=1   L 951  T=0 F=2  T=0 F=0  if (ctxt->format == 2)
  d=1   L 968  T=0 F=27  T=0 F=137  case XML_COMMENT_NODE:
  d=1   L 982  T=0 F=27  T=0 F=137  case XML_ENTITY_REF_NODE:
  d=1   L 988  T=0 F=27  T=0 F=137  case XML_CDATA_SECTION_NODE:
  d=1   L1013  T=0 F=27  T=0 F=137  case XML_ATTRIBUTE_NODE:
  d=1   L1017  T=0 F=27  T=0 F=137  case XML_NAMESPACE_DECL:
  d=1   L1021  T=0 F=27  T=0 F=137  default:
  d=1   L1026  T=8 F=19  T=17 F=120  if (cur == root)
  d=1   L1028  T=0 F=19  T=0 F=120  if ((ctxt->format == 1) &&
  d=1   L1032  T=11 F=8  T=105 F=15  if (cur->next != NULL) {
  d=1   L1050  T=0 F=4  T=0 F=0  if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) {  <-- BLOCKER
  d=1   L1050  T=4 F=4  T=0 F=15  if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) {  <-- BLOCKER

[off-chain: 71 additional divergent branches across 8 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=ed9377be9621bf39, size=189 bytes, fuzzer=grimoire, trial=1, discovered_at=1816s, mutation_op=GrimoireExtensionMutator):
  0000: 55 54 46 38 06 00 5c 0a 3c 3f 6c 20 3f 3e 3c 21   UTF8..\.<?l ?><!
  0010: 44 4f 43 54 59 50 45 61 20 53 59 53 54 45 4d 20   DOCTYPEa SYSTEM 
  0020: 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64   "dtds/127772.dtd
  0030: 22 3e 3c 61 3e 20 3c 62 20 6b 3a 66 3d 22 22 3e   "><a> <b k:f="">
Seed 2 (id=f953abe6839324e8, size=234 bytes, fuzzer=grimoire, trial=1, discovered_at=6863s, mutation_op=ByteInterestingMutator,ByteNegMutator):
  0000: 55 54 46 38 06 00 37 37 32 2e 78 6d 6c 5c 0a 3c   UTF8..772.xml\.<
  0010: 3f 6c 20 3f 3e 3c 21 44 4f 43 54 59 50 45 61 20   ?l ?><!DOCTYPEa 
  0020: 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37   SYSTEM "dtds/127
  0030: 37 37 32 2e 64 74 64 22 3e 3c 61 3e 0a 20 20 3c   772.dtd"><a>.  <
Seed 3 (id=c23096ec9dae2ed4, size=389 bytes, fuzzer=grimoire, trial=1, discovered_at=18912s, mutation_op=ByteNegMutator,BytesExpandMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM
  0030: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=001c8c9d4510710d, size=248 bytes, fuzzer=cmplog, trial=1, discovered_at=411s, mutation_op=ByteNegMutator,BytesCopyMutator,BytesInsertMutator,ByteIncMutator,BytesSwapMutator,BytesDeleteMutator,TokenReplace):
  0000: 5f 5f 5f 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ___.127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=00ebab469d057524, size=371 bytes, fuzzer=cmplog, trial=1, discovered_at=573s, mutation_op=ByteFlipMutator,ByteNegMutator,BitFlipMutator,CrossoverReplaceMutator):
  0000: 37 58 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20   7X72.xml\.<?xml 
  0010: 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a   version="1.0"?>.
  0020: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST
  0030: 45 4d 20 22 64 74 64 73 2a 31 32 37 37 37 32 2e   EM "dtds*127772.
Seed 3 (id=01f8661e47872c51, size=437 bytes, fuzzer=cmplog, trial=1, discovered_at=1510s, mutation_op=CrossoverInsertMutator,ByteInterestingMutator):
  0000: 65 65 65 65 65 54 54 4c 49 53 54 20 62 20 78 6d   eeeeeTTLIST b xm
  0010: 6c 6e 73 3a 78 6c 69 6e 6b 28 2a 43 44 41 54 41   lns:xlink(*CDATA
  0020: 9f 20 20 20 20 23 06 00 00 00 31 32 37 37 37 32   .    #....127772
  0030: 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73   .xml\.<?xml vers
Seed 4 (id=00b887d5dd27fa7e, size=192 bytes, fuzzer=cmplog, trial=1, discovered_at=2184s, mutation_op=CrossoverReplaceMutator,BytesRandInsertMutator,ByteIncMutator,BytesExpandMutator,ByteFlipMutator):
  0000: 2f 2f 66 61 54 41 20 20 06 00 00 00 31 32 37 37   //faTA  ....1277
  0010: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0020: 72 2e 64 74 64 22 3e 0a 0a 3c 61 3e 0a 20 20 3c   r.dtd">..<a>.  <
  0030: 62 20 78 2f 77 77 77 2e 77 33 2e 6f 72 67 68 74   b x/www.w3.orght
Seed 5 (id=01ce8fc7df8498a7, size=389 bytes, fuzzer=cmplog, trial=1, discovered_at=4075s, mutation_op=TokenReplace,CrossoverInsertMutator,BytesCopyMutator,ByteDecMutator,ByteAddMutator):
  0000: 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76   772.xml\.<?xml v
  0010: 65 72 73 69 6f 6e 3d 22 31 2e 30 22 47 3e 0a 3c   ersion="1.0"G>.<
  0020: 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45   !DOCTYPE a SYSTE
  0030: 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64   M "dtds/127772.d


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  55(U)x2 37(7)x1                     37(7)x3 5f(_)x1 65(e)x1 2f(/)x1 +4u  PARTIAL
   0x0001  54(T)x2 32(2)x1                     37(7)x2 5f(_)x1 58(X)x1 65(e)x1 +5u  PARTIAL
   0x0002  46(F)x2 2e(.)x1                     5f(_)x1 37(7)x1 65(e)x1 66(f)x1 +6u  PARTIAL
   0x0003  38(8)x2 78(x)x1                     00(.)x2 2e(.)x2 32(2)x1 65(e)x1 +4u  DIFFER
   0x0004  06(.)x2 6d(m)x1                     31(1)x3 78(x)x2 2e(.)x1 65(e)x1 +3u  DIFFER
   0x0005  00(.)x2 6c(l)x1                     32(2)x4 78(x)x1 54(T)x1 41(A)x1 +3u  DIFFER
   0x0006  5c(\)x2 37(7)x1                     37(7)x3 6c(l)x2 6d(m)x1 54(T)x1 +3u  PARTIAL
   0x0007  0a(.)x2 37(7)x1                     37(7)x3 5c(\)x2 6c(l)x1 4c(L)x1 +3u  PARTIAL
   0x0008  3c(<)x2 32(2)x1                     37(7)x3 0a(.)x2 5c(\)x1 49(I)x1 +3u  DIFFER
   0x0009  3f(?)x2 2e(.)x1                     32(2)x3 3c(<)x2 0a(.)x1 53(S)x1 +3u  DIFFER
   0x000a  78(x)x2 6c(l)x1                     2e(.)x3 3f(?)x2 3c(<)x1 54(T)x1 +3u  DIFFER
   0x000b  6d(m)x2 20( )x1                     78(x)x5 3f(?)x1 20( )x1 00(.)x1 +2u  PARTIAL
   0x000c  6c(l)x2 3f(?)x1                     6d(m)x5 78(x)x1 62(b)x1 31(1)x1 +2u  DIFFER
   0x000d  3e(>)x1 5c(\)x1 20( )x1             6c(l)x5 6d(m)x1 20( )x1 32(2)x1 +2u  PARTIAL
   0x000e  3c(<)x1 0a(.)x1 76(v)x1             5c(\)x3 20( )x2 6c(l)x1 78(x)x1 +3u  DIFFER
   0x000f  21(!)x1 3c(<)x1 65(e)x1             0a(.)x3 76(v)x2 20( )x1 6d(m)x1 +3u  DIFFER
   0x0010  44(D)x1 3f(?)x1 72(r)x1             3c(<)x3 65(e)x2 76(v)x1 6c(l)x1 +3u  DIFFER
   0x0011  4f(O)x1 6c(l)x1 73(s)x1             3f(?)x3 72(r)x2 65(e)x1 6e(n)x1 +3u  DIFFER
   0x0012  43(C)x1 20( )x1 69(i)x1             78(x)x3 73(s)x2 72(r)x1 2e(.)x1 +3u  DIFFER
   0x0013  54(T)x1 3f(?)x1 6f(o)x1             6d(m)x3 73(s)x1 3a(:)x1 78(x)x1 +4u  DIFFER
   0x0014  59(Y)x1 3e(>)x1 6e(n)x1             6c(l)x3 69(i)x1 78(x)x1 6d(m)x1 +4u  DIFFER
   0x0015  50(P)x1 3c(<)x1 3d(=)x1             20( )x3 6c(l)x2 6f(o)x1 6e(n)x1 +3u  DIFFER
   0x0016  45(E)x1 21(!)x1 22(")x1             76(v)x3 3d(=)x2 6e(n)x1 69(i)x1 +3u  DIFFER
   0x0017  61(a)x1 44(D)x1 31(1)x1             65(e)x3 3d(=)x1 6e(n)x1 0a(.)x1 +4u  DIFFER
   0x0018  20( )x1 4f(O)x1 2e(.)x1             72(r)x3 22(")x1 6b(k)x1 3c(<)x1 +4u  PARTIAL
   0x0019  53(S)x1 43(C)x1 30(0)x1             73(s)x3 28(()x2 31(1)x1 3f(?)x1 +3u  DIFFER
   0x001a  59(Y)x1 54(T)x1 22(")x1             69(i)x3 2e(.)x1 2a(*)x1 78(x)x1 +4u  DIFFER
   0x001b  53(S)x1 59(Y)x1 3f(?)x1             6f(o)x3 22(")x2 30(0)x1 43(C)x1 +3u  DIFFER
   0x001c  54(T)x1 50(P)x1 3e(>)x1             6e(n)x3 22(")x1 44(D)x1 6c(l)x1 +4u  PARTIAL
   0x001d  45(E)x2 0a(.)x1                     3d(=)x3 3f(?)x1 41(A)x1 20( )x1 +4u  PARTIAL
   0x001e  4d(M)x1 61(a)x1 3c(<)x1             22(")x3 0a(.)x2 41(A)x2 3e(>)x1 +2u  DIFFER
   0x001f  20( )x2 21(!)x1                     31(1)x3 3c(<)x2 54(T)x2 0a(.)x1 +2u  DIFFER
   0x0020  22(")x1 53(S)x1 44(D)x1             2e(.)x3 72(r)x2 3c(<)x1 9f(.)x1 +3u  DIFFER
   0x0021  64(d)x1 59(Y)x1 4f(O)x1             30(0)x3 21(!)x1 20( )x1 2e(.)x1 +4u  DIFFER
   0x0022  74(t)x1 53(S)x1 43(C)x1             22(")x3 44(D)x1 20( )x1 64(d)x1 +4u  DIFFER
   0x0023  54(T)x2 64(d)x1                     3f(?)x3 20( )x2 4f(O)x1 74(t)x1 +3u  DIFFER
   0x0024  73(s)x1 45(E)x1 59(Y)x1             3e(>)x3 20( )x2 54(T)x2 43(C)x1 +2u  DIFFER
   0x0025  2f(/)x1 4d(M)x1 50(P)x1             0a(.)x3 54(T)x1 23(#)x1 22(")x1 +4u  DIFFER
   0x0026  31(1)x1 20( )x1 45(E)x1             3c(<)x3 62(b)x2 59(Y)x1 06(.)x1 +3u  DIFFER
   0x0027  32(2)x1 22(")x1 20( )x1             21(!)x3 20( )x2 50(P)x1 00(.)x1 +3u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7327.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7327,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [grimoire>cmplog (grimoire_structural)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7327 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7327 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7327 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).