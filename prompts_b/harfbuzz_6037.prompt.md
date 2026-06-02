==== BLOCKER ====
Target: harfbuzz
Branch ID: 6037
Location: /src/harfbuzz/src/hb-ot-shaper-vowel-constraints.cc:144:4
Enclosing function: _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)
Source line: 	  case 0x0A72u:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            7        3          0  REFERENCE
cmplog                           2        8          0  loser (value_profile vs value_profile_cmplog)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog            10        0          0  winner (value_profile vs cmplog)
naive_ctx                       10        0          0  REFERENCE
naive_ngram4                     7        3          0  REFERENCE
mopt                             7        3          0  REFERENCE
minimizer                        9        1          0  REFERENCE
fast                             5        5          0  REFERENCE
grimoire                         2        8          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=3.70h  loser=20.10h
  avg hitcount on branch: winner=3  loser=0
  prob_div=0.80  dur_div=16.40h  hit_div=3
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/6037/{W,L}/branch_coverage_show.txt

--- Enclosing function: _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) (/src/harfbuzz/src/hb-ot-shaper-vowel-constraints.cc:41-473) ---
[ ]    39  				       hb_buffer_t              *buffer,
[ ]    40  				       hb_font_t                *font HB_UNUSED)
[B]    41  {
[ ]    42  #ifdef HB_NO_OT_SHAPER_VOWEL_CONSTRAINTS
[ ]    43    return;
[ ]    44  #endif
[B]    45    if (buffer->flags & HB_BUFFER_FLAG_DO_NOT_INSERT_DOTTED_CIRCLE)
[ ]    46      return;
[ ]    47  
[ ]    48    /* UGLY UGLY UGLY business of adding dotted-circle in the middle of
[ ]    49     * vowel-sequences that look like another vowel.  Data for each script
[ ]    50     * collected from the USE script development spec.
[ ]    51     *
[ ]    52     * https://github.com/harfbuzz/harfbuzz/issues/1019
[ ]    53     */
[B]    54    buffer->clear_output ();
[B]    55    unsigned int count = buffer->len;
[B]    56    switch ((unsigned) buffer->props.script)
[B]    57    {
[ ]    58      case HB_SCRIPT_DEVANAGARI:
[ ]    59        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[ ]    60        {
[ ]    61  	bool matched = false;
[ ]    62  	switch (buffer->cur ().codepoint)
[ ]    63  	{
[ ]    64  	  case 0x0905u:
[ ]    65  	    switch (buffer->cur (1).codepoint)
[ ]    66  	    {
[ ]    67  	      case 0x093Au: case 0x093Bu: case 0x093Eu: case 0x0945u:
[ ]    68  	      case 0x0946u: case 0x0949u: case 0x094Au: case 0x094Bu:
[ ]    69  	      case 0x094Cu: case 0x094Fu: case 0x0956u: case 0x0957u:
[ ]    70  		matched = true;
[ ]    71  		break;
[ ]    72  	    }
[ ]    73  	    break;
[ ]    74  	  case 0x0906u:
[ ]    75  	    switch (buffer->cur (1).codepoint)
[ ]    76  	    {
[ ]    77  	      case 0x093Au: case 0x0945u: case 0x0946u: case 0x0947u:
[ ]    78  	      case 0x0948u:
[ ]    79  		matched = true;
[ ]    80  		break;
[ ]    81  	    }
[ ]    82  	    break;
[ ]    83  	  case 0x0909u:
[ ]    84  	    matched = 0x0941u == buffer->cur (1).codepoint;
[ ]    85  	    break;
[ ]    86  	  case 0x090Fu:
[ ]    87  	    switch (buffer->cur (1).codepoint)
[ ]    88  	    {
[ ]    89  	      case 0x0945u: case 0x0946u: case 0x0947u:
[ ]    90  		matched = true;
[ ]    91  		break;
[ ]    92  	    }
[ ]    93  	    break;
[ ]    94  	  case 0x0930u:
[ ]    95  	    if (0x094Du == buffer->cur (1).codepoint &&
[ ]    96  		buffer->idx + 2 < count &&
[ ]    97  		0x0907u == buffer->cur (2).codepoint)
[ ]    98  	    {
[ ]    99  	      (void) buffer->next_glyph ();
[ ]   100  	      matched = true;
[ ]   101  	    }
[ ]   102  	    break;
[ ]   103  	}
[ ]   104  	(void) buffer->next_glyph ();
[ ]   105  	if (matched) _output_with_dotted_circle (buffer);
[ ]   106        }
[ ]   107        break;
[ ]   108  
[ ]   109      case HB_SCRIPT_BENGALI:
[ ]   110        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[ ]   111        {
[ ]   112  	bool matched = false;
[ ]   113  	switch (buffer->cur ().codepoint)
[ ]   114  	{
[ ]   115  	  case 0x0985u:
[ ]   116  	    matched = 0x09BEu == buffer->cur (1).codepoint;
[ ]   117  	    break;
[ ]   118  	  case 0x098Bu:
[ ]   119  	    matched = 0x09C3u == buffer->cur (1).codepoint;
[ ]   120  	    break;
[ ]   121  	  case 0x098Cu:
[ ]   122  	    matched = 0x09E2u == buffer->cur (1).codepoint;
[ ]   123  	    break;
[ ]   124  	}
[ ]   125  	(void) buffer->next_glyph ();
[ ]   126  	if (matched) _output_with_dotted_circle (buffer);
[ ]   127        }
[ ]   128        break;
[ ]   129  
[B]   130      case HB_SCRIPT_GURMUKHI:
[B]   131        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[B]   132        {
[B]   133  	bool matched = false;
[B]   134  	switch (buffer->cur ().codepoint)
[B]   135  	{
[ ]   136  	  case 0x0A05u:
[ ]   137  	    switch (buffer->cur (1).codepoint)
[ ]   138  	    {
[ ]   139  	      case 0x0A3Eu: case 0x0A48u: case 0x0A4Cu:
[ ]   140  		matched = true;
[ ]   141  		break;
[ ]   142  	    }
[ ]   143  	    break;
[B]   144  	  case 0x0A72u: <-- BLOCKER
[B]   145  	    switch (buffer->cur (1).codepoint)
[B]   146  	    {
[ ]   147  	      case 0x0A3Fu: case 0x0A40u: case 0x0A47u:
[ ]   148  		matched = true;
[ ]   149  		break;
[B]   150  	    }
[B]   151  	    break;
[B]   152  	  case 0x0A73u:
[B]   153  	    switch (buffer->cur (1).codepoint)
[B]   154  	    {
[ ]   155  	      case 0x0A41u: case 0x0A42u: case 0x0A4Bu:
[ ]   156  		matched = true;
[ ]   157  		break;
[B]   158  	    }
[B]   159  	    break;
[B]   160  	}
[B]   161  	(void) buffer->next_glyph ();
[B]   162  	if (matched) _output_with_dotted_circle (buffer);
[B]   163        }
[B]   164        break;
[ ]   165  
[B]   166      case HB_SCRIPT_GUJARATI:
[ ]   167        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[ ]   168        {
[ ]   169  	bool matched = false;
[ ]   170  	switch (buffer->cur ().codepoint)
[ ]   171  	{
[ ]   172  	  case 0x0A85u:
[ ]   173  	    switch (buffer->cur (1).codepoint)
[ ]   174  	    {
[ ]   175  	      case 0x0ABEu: case 0x0AC5u: case 0x0AC7u: case 0x0AC8u:
[ ]   176  	      case 0x0AC9u: case 0x0ACBu: case 0x0ACCu:
[ ]   177  		matched = true;
[ ]   178  		break;
[ ]   179  	    }
[ ]   180  	    break;
[ ]   181  	  case 0x0AC5u:
[ ]   182  	    matched = 0x0ABEu == buffer->cur (1).codepoint;
[ ]   183  	    break;
[ ]   184  	}
[ ]   185  	(void) buffer->next_glyph ();
[ ]   186  	if (matched) _output_with_dotted_circle (buffer);
[ ]   187        }
[ ]   188        break;
[ ]   189  
[ ]   190      case HB_SCRIPT_ORIYA:
[ ]   191        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[ ]   192        {
[ ]   193  	bool matched = false;
[ ]   194  	switch (buffer->cur ().codepoint)
[ ]   195  	{
[ ]   196  	  case 0x0B05u:
[ ]   197  	    matched = 0x0B3Eu == buffer->cur (1).codepoint;
[ ]   198  	    break;
[ ]   199  	  case 0x0B0Fu: case 0x0B13u:
[ ]   200  	    matched = 0x0B57u == buffer->cur (1).codepoint;
[ ]   201  	    break;
[ ]   202  	}
[ ]   203  	(void) buffer->next_glyph ();
[ ]   204  	if (matched) _output_with_dotted_circle (buffer);
[ ]   205        }
[ ]   206        break;
[ ]   207  
[ ]   208      case HB_SCRIPT_TAMIL:
[ ]   209        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[ ]   210        {
[ ]   211  	bool matched = false;
[ ]   212  	if (0x0B85u == buffer->cur ().codepoint &&
[ ]   213  	    0x0BC2u == buffer->cur (1).codepoint)
[ ]   214  	{
[ ]   215  	  matched = true;
[ ]   216  	}
[ ]   217  	(void) buffer->next_glyph ();
[ ]   218  	if (matched) _output_with_dotted_circle (buffer);
[ ]   219        }
[ ]   220        break;
[ ]   221  
[ ]   222      case HB_SCRIPT_TELUGU:
[ ]   223        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[ ]   224        {
[ ]   225  	bool matched = false;
[ ]   226  	switch (buffer->cur ().codepoint)
[ ]   227  	{
[ ]   228  	  case 0x0C12u:
[ ]   229  	    switch (buffer->cur (1).codepoint)
[ ]   230  	    {
[ ]   231  	      case 0x0C4Cu: case 0x0C55u:
[ ]   232  		matched = true;
[ ]   233  		break;
[ ]   234  	    }
[ ]   235  	    break;
[ ]   236  	  case 0x0C3Fu: case 0x0C46u: case 0x0C4Au:
[ ]   237  	    matched = 0x0C55u == buffer->cur (1).codepoint;
[ ]   238  	    break;
[ ]   239  	}
[ ]   240  	(void) buffer->next_glyph ();
[ ]   241  	if (matched) _output_with_dotted_circle (buffer);
[ ]   242        }
[ ]   243        break;
[ ]   244  
[ ]   245      case HB_SCRIPT_KANNADA:
[ ]   246        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[ ]   247        {
[ ]   248  	bool matched = false;
[ ]   249  	switch (buffer->cur ().codepoint)
[ ]   250  	{
[ ]   251  	  case 0x0C89u: case 0x0C8Bu:
[ ]   252  	    matched = 0x0CBEu == buffer->cur (1).codepoint;
[ ]   253  	    break;
[ ]   254  	  case 0x0C92u:
[ ]   255  	    matched = 0x0CCCu == buffer->cur (1).codepoint;
[ ]   256  	    break;
[ ]   257  	}
[ ]   258  	(void) buffer->next_glyph ();
[ ]   259  	if (matched) _output_with_dotted_circle (buffer);
[ ]   260        }
[ ]   261        break;
[ ]   262  
[ ]   263      case HB_SCRIPT_MALAYALAM:
[ ]   264        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[ ]   265        {
[ ]   266  	bool matched = false;
[ ]   267  	switch (buffer->cur ().codepoint)
[ ]   268  	{
[ ]   269  	  case 0x0D07u: case 0x0D09u:
[ ]   270  	    matched = 0x0D57u == buffer->cur (1).codepoint;
[ ]   271  	    break;
[ ]   272  	  case 0x0D0Eu:
[ ]   273  	    matched = 0x0D46u == buffer->cur (1).codepoint;
[ ]   274  	    break;
[ ]   275  	  case 0x0D12u:
[ ]   276  	    switch (buffer->cur (1).codepoint)
[ ]   277  	    {
[ ]   278  	      case 0x0D3Eu: case 0x0D57u:
[ ]   279  		matched = true;
[ ]   280  		break;
[ ]   281  	    }
[ ]   282  	    break;
[ ]   283  	}
[ ]   284  	(void) buffer->next_glyph ();
[ ]   285  	if (matched) _output_with_dotted_circle (buffer);
[ ]   286        }
[ ]   287        break;
[ ]   288  
[ ]   289      case HB_SCRIPT_SINHALA:
[ ]   290        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[ ]   291        {
[ ]   292  	bool matched = false;
[ ]   293  	switch (buffer->cur ().codepoint)
[ ]   294  	{
[ ]   295  	  case 0x0D85u:
[ ]   296  	    switch (buffer->cur (1).codepoint)
[ ]   297  	    {
[ ]   298  	      case 0x0DCFu: case 0x0DD0u: case 0x0DD1u:
[ ]   299  		matched = true;
[ ]   300  		break;
[ ]   301  	    }
[ ]   302  	    break;
[ ]   303  	  case 0x0D8Bu: case 0x0D8Fu: case 0x0D94u:
[ ]   304  	    matched = 0x0DDFu == buffer->cur (1).codepoint;
[ ]   305  	    break;
[ ]   306  	  case 0x0D8Du:
[ ]   307  	    matched = 0x0DD8u == buffer->cur (1).codepoint;
[ ]   308  	    break;
[ ]   309  	  case 0x0D91u:
[ ]   310  	    switch (buffer->cur (1).codepoint)
[ ]   311  	    {
[ ]   312  	      case 0x0DCAu: case 0x0DD9u: case 0x0DDAu: case 0x0DDCu:
[ ]   313  	      case 0x0DDDu: case 0x0DDEu:
[ ]   314  		matched = true;
[ ]   315  		break;
[ ]   316  	    }
[ ]   317  	    break;
[ ]   318  	}
[ ]   319  	(void) buffer->next_glyph ();
[ ]   320  	if (matched) _output_with_dotted_circle (buffer);
[ ]   321        }
[ ]   322        break;
[ ]   323  
[ ]   324      case HB_SCRIPT_BRAHMI:
[ ]   325        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[ ]   326        {
[ ]   327  	bool matched = false;
[ ]   328  	switch (buffer->cur ().codepoint)
[ ]   329  	{
[ ]   330  	  case 0x11005u:
[ ]   331  	    matched = 0x11038u == buffer->cur (1).codepoint;
[ ]   332  	    break;
[ ]   333  	  case 0x1100Bu:
[ ]   334  	    matched = 0x1103Eu == buffer->cur (1).codepoint;
[ ]   335  	    break;
[ ]   336  	  case 0x1100Fu:
[ ]   337  	    matched = 0x11042u == buffer->cur (1).codepoint;
[ ]   338  	    break;
[ ]   339  	}
[ ]   340  	(void) buffer->next_glyph ();
[ ]   341  	if (matched) _output_with_dotted_circle (buffer);
[ ]   342        }
[ ]   343        break;
[ ]   344  
[ ]   345      case HB_SCRIPT_KHOJKI:
[ ]   346        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[ ]   347        {
[ ]   348  	bool matched = false;
[ ]   349  	switch (buffer->cur ().codepoint)
[ ]   350  	{
[ ]   351  	  case 0x11200u:
[ ]   352  	    switch (buffer->cur (1).codepoint)
[ ]   353  	    {
[ ]   354  	      case 0x1122Cu: case 0x11231u: case 0x11233u:
[ ]   355  		matched = true;
[ ]   356  		break;
[ ]   357  	    }
[ ]   358  	    break;
[ ]   359  	  case 0x11206u:
[ ]   360  	    matched = 0x1122Cu == buffer->cur (1).codepoint;
[ ]   361  	    break;
[ ]   362  	  case 0x1122Cu:
[ ]   363  	    switch (buffer->cur (1).codepoint)
[ ]   364  	    {
[ ]   365  	      case 0x11230u: case 0x11231u:
[ ]   366  		matched = true;
[ ]   367  		break;
[ ]   368  	    }
[ ]   369  	    break;
[ ]   370  	  case 0x11240u:
[ ]   371  	    matched = 0x1122Eu == buffer->cur (1).codepoint;
[ ]   372  	    break;
[ ]   373  	}
[ ]   374  	(void) buffer->next_glyph ();
[ ]   375  	if (matched) _output_with_dotted_circle (buffer);
[ ]   376        }
[ ]   377        break;
[ ]   378  
[ ]   379      case HB_SCRIPT_KHUDAWADI:
[ ]   380        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[ ]   381        {
[ ]   382  	bool matched = false;
[ ]   383  	switch (buffer->cur ().codepoint)
[ ]   384  	{
[ ]   385  	  case 0x112B0u:
[ ]   386  	    switch (buffer->cur (1).codepoint)
[ ]   387  	    {
[ ]   388  	      case 0x112E0u: case 0x112E5u: case 0x112E6u: case 0x112E7u:
[ ]   389  	      case 0x112E8u:
[ ]   390  		matched = true;
[ ]   391  		break;
[ ]   392  	    }
[ ]   393  	    break;
[ ]   394  	}
[ ]   395  	(void) buffer->next_glyph ();
[ ]   396  	if (matched) _output_with_dotted_circle (buffer);
[ ]   397        }
[ ]   398        break;
[ ]   399  
[ ]   400      case HB_SCRIPT_TIRHUTA:
[ ]   401        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[ ]   402        {
[ ]   403  	bool matched = false;
[ ]   404  	switch (buffer->cur ().codepoint)
[ ]   405  	{
[ ]   406  	  case 0x11481u:
[ ]   407  	    matched = 0x114B0u == buffer->cur (1).codepoint;
[ ]   408  	    break;
[ ]   409  	  case 0x1148Bu: case 0x1148Du:
[ ]   410  	    matched = 0x114BAu == buffer->cur (1).codepoint;
[ ]   411  	    break;
[ ]   412  	  case 0x114AAu:
[ ]   413  	    switch (buffer->cur (1).codepoint)
[ ]   414  	    {
[ ]   415  	      case 0x114B5u: case 0x114B6u:
[ ]   416  		matched = true;
[ ]   417  		break;
[ ]   418  	    }
[ ]   419  	    break;
[ ]   420  	}
[ ]   421  	(void) buffer->next_glyph ();
[ ]   422  	if (matched) _output_with_dotted_circle (buffer);
[ ]   423        }
[ ]   424        break;
[ ]   425  
[ ]   426      case HB_SCRIPT_MODI:
[ ]   427        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[ ]   428        {
[ ]   429  	bool matched = false;
[ ]   430  	switch (buffer->cur ().codepoint)
[ ]   431  	{
[ ]   432  	  case 0x11600u: case 0x11601u:
[ ]   433  	    switch (buffer->cur (1).codepoint)
[ ]   434  	    {
[ ]   435  	      case 0x11639u: case 0x1163Au:
[ ]   436  		matched = true;
[ ]   437  		break;
[ ]   438  	    }
[ ]   439  	    break;
[ ]   440  	}
[ ]   441  	(void) buffer->next_glyph ();
[ ]   442  	if (matched) _output_with_dotted_circle (buffer);
[ ]   443        }
[ ]   444        break;
[ ]   445  
[ ]   446      case HB_SCRIPT_TAKRI:
[ ]   447        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[ ]   448        {
[ ]   449  	bool matched = false;
[ ]   450  	switch (buffer->cur ().codepoint)
[ ]   451  	{
[ ]   452  	  case 0x11680u:
[ ]   453  	    switch (buffer->cur (1).codepoint)
[ ]   454  	    {
[ ]   455  	      case 0x116ADu: case 0x116B4u: case 0x116B5u:
[ ]   456  		matched = true;
[ ]   457  		break;
[ ]   458  	    }
[ ]   459  	    break;
[ ]   460  	  case 0x11686u:
[ ]   461  	    matched = 0x116B2u == buffer->cur (1).codepoint;
[ ]   462  	    break;
[ ]   463  	}
[ ]   464  	(void) buffer->next_glyph ();
[ ]   465  	if (matched) _output_with_dotted_circle (buffer);
[ ]   466        }
[ ]   467        break;
[ ]   468  
[ ]   469      default:
[ ]   470        break;
[B]   471    }
[B]   472    buffer->sync ();
[B]   473  }

--- Caller (1 hop): hb-ot-shaper-indic.cc:preprocess_text_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1502-1506, calls _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) at line 1505) (full body — short) ---
[B]  1502  {
[B]  1503    const indic_shape_plan_t *indic_plan = (const indic_shape_plan_t *) plan->data;
[B]  1504    if (!indic_plan->uniscribe_bug_compatible)
[B]  1505      _hb_preprocess_text_vowel_constraints (plan, buffer, font); <-- CALL
[B]  1506  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-indic.cc:preprocess_text_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1502-1506, calls _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) at line 1505)
hop 2  hb-ot-shaper-use.cc:preprocess_text_use(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:474-476, calls _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) at line 475)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       1         9  hb-ot-shaper-indic.cc:initial_reordering_standalone_cluster(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:946-961)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-vowel-constraints.cc:41-473) ---
  d=1   L 145  T=7 F=0  T=1 F=0  switch (buffer->cur (1).codepoint)
  d=1   L 147  T=0 F=7  T=0 F=1  case 0x0A3Fu: case 0x0A40u: case 0x0A47u:
  d=1   L 147  T=0 F=7  T=0 F=1  case 0x0A3Fu: case 0x0A40u: case 0x0A47u:
  d=1   L 147  T=0 F=7  T=0 F=1  case 0x0A3Fu: case 0x0A40u: case 0x0A47u:

[off-chain: 50 additional divergent branches across 5 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=2051614ec8111e65, size=61 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=190s, mutation_op=ByteNegMutator,TokenInsert,BytesInsertCopyMutator,ByteNegMutator,BytesCopyMutator,BytesDeleteMutator,BytesInsertCopyMutator):
  0000: 20 20 20 20 20 6b 65 8d 20 20 20 6b 65 72 6e 20        ke.   kern 
  0010: 20 fb 00 ff 0f 20 7a 6f 2d 68 61 92 72 0a 00 00    .... zo-ha.r...
  0020: 00 0c 00 00 00 20 62 6e 53 00 00 02 00 ff 7f 0d   ..... bnS.......
  0030: 00 0a 02 00 20 00 00 00 73 0a 00 00 00            .... ...s....
Seed 2 (id=cf3af040d155a60a, size=65 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=809s, mutation_op=ByteInterestingMutator,ByteRandMutator,DwordAddMutator,CrossoverInsertMutator,BytesDeleteMutator):
  0000: 62 aa 00 00 61 72 0a 00 00 fe 00 00 02 a9 de 00   b...ar..........
  0010: 62 aa 00 00 00 00 fe 00 00 02 aa 00 a9 62 aa 00   b............b..
  0020: 00 00 00 00 61 72 09 6e 01 0c 00 00 06 06 00 18   ....ar.n........
  0030: 20 20 20 20 00 00 20 00 00 20 0c 00 00 73 80 7f       .. .. ...s..
Seed 3 (id=a2a12ce0dcc04bd4, size=116 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=899s, mutation_op=ByteIncMutator,BytesSetMutator,QwordAddMutator,QwordAddMutator,WordAddMutator,WordInterestingMutator,BytesSwapMutator):
  0000: 00 03 00 1a 20 e0 20 20 20 20 20 20 02 20 20 20   .... .      .   
  0010: 20 20 0d 20 20 20 20 20 20 35 20 01 00 1a 20 20     .      5 ...  
  0020: 20 20 20 20 20 20 20 27 6c 6c ba 6c ba 14 01 20          'll.l... 
  0030: e0 20 20 80 20 00 64 22 6b 0a 00 00 00 00 00 00   .  . .d"k.......
Seed 4 (id=53e30e91602afc12, size=436 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=9299s, mutation_op=BytesDeleteMutator):
  0000: 00 01 00 00 00 05 12 ff 00 46 00 20 47 50 4f 53   .........F. GPOS
  0010: 20 20 20 20 00 00 00 00 ff ff 00 ec ec ec ec ec       ............
  0020: ec ec ec ec ec ec ed 18 18 18 0b 03 0a 00 fd ff   ................
  0030: 00 11 00 80 94 00 04 10 1d 41 20 20 28 a0 10 0d   .........A  (...
Seed 5 (id=8f41738c9d970f06, size=385 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=18450s, mutation_op=BytesDeleteMutator,ByteFlipMutator):
  0000: 00 01 00 00 00 02 ee ff 00 30 00 20 47 50 4f 53   .........0. GPOS
  0010: 20 20 20 20 00 00 00 00 ff ff 00 ec 4d 56 41 52       ........MVAR
  0020: ff ff ff 00 7a 6f 2d 68 61 6e 73 00 00 00 fd ff   ....zo-hans.....
  0030: 00 11 00 00 94 00 2a 24 1d 43 20 20 28 a0 01 00   ......*$.C  (...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0cf0d8ffcee25b69, size=51 bytes, fuzzer=cmplog, trial=2, discovered_at=116s, mutation_op=BytesDeleteMutator,TokenInsert,TokenInsert,BytesSwapMutator,DwordAddMutator):
  0000: 29 2d 00 00 72 0a 00 00 01 1f 20 e0 20 20 05 00   )-..r..... .  ..
  0010: 10 00 20 ff 2d 00 22 00 00 20 20 20 20 7f 00 80   .. .-."..    ...
  0020: 20 20 01 00 01 0a 02 00 01 20 20 20 20 7f 00 00     .......    ...
  0030: 20 20 20                                             
Seed 2 (id=068910d63bd66f21, size=63 bytes, fuzzer=cmplog, trial=2, discovered_at=363s, mutation_op=DwordInterestingMutator,BytesSetMutator,CrossoverInsertMutator,ByteNegMutator):
  0000: 19 0a 00 00 72 1b 1b 1b 1b 02 00 40 20 20 20 6e   ....r......@   n
  0010: 20 20 20 20 20 01 73 6e 2d 68 61 6e 73 00 2d 6d        .sn-hans.-m
  0020: 6f 02 00 04 20 20 00 1e 01 01 00 1b 1b 1b 70 78   o...  ........px
  0030: 2d 68 61 6e 74 0c 00 00 73 0a 00 00 00 20 00      -hant...s.... .
Seed 3 (id=04a53b14e796e969, size=59 bytes, fuzzer=cmplog, trial=2, discovered_at=697s, mutation_op=BytesSwapMutator):
  0000: 00 00 e6 17 00 00 00 00 00 e6 17 00 00 01 0c 00   ................
  0010: 20 00 20 64 80 20 00 00 00 00 00 01 01 0a 00 00    . d. ..........
  0020: 00 02 00 00 00 0c 02 20 7f 20 00 00 00 10 00 00   ....... . ......
  0030: 00 00 00 00 00 00 00 00 f8 25 00                  .........%.
Seed 4 (id=01d6436c2d229f52, size=81 bytes, fuzzer=cmplog, trial=2, discovered_at=829s, mutation_op=ByteNegMutator,WordAddMutator,BytesDeleteMutator):
  0000: 74 74 63 66 00 01 04 00 00 00 00 04 20 72 6e 04   ttcf........ rn.
  0010: 00 00 00 04 00 00 00 20 04 72 6e 2a f8 17 00 00   ....... .rn*....
  0020: 0f 00 0c 00 20 20 13 0d 00 00 0c 00 20 20 df 30   ....  ......  .0
  0030: 01 02 0a 00 00 ff 03 00 00 00 00 00 00 00 00 e6   ................
Seed 5 (id=07027b43fe645249, size=140 bytes, fuzzer=cmplog, trial=2, discovered_at=1834s, mutation_op=BytesDeleteMutator,BytesExpandMutator,ByteAddMutator,BytesRandSetMutator,BytesSetMutator,BytesSetMutator):
  0000: 1f 01 00 02 02 02 02 02 02 02 02 02 02 02 02 02   ................
  0010: 02 02 00 c9 c9 00 00 01 c9 c9 c9 0a 01 03 00 00   ................
  0020: 1d 01 00 00 00 ff 00 ff 03 1d 00 00 02 0a 04 fd   ................
  0030: ff 00 00 fe 10 00 1d dd 09 0c 00 00 f8 04 00 e5   ................


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x4 20( )x1 62(b)x1             00(.)x6 29())x1 19(.)x1 74(t)x1 +1u  PARTIAL
   0x0001  01(.)x3 20( )x1 aa(.)x1 03(.)x1     01(.)x6 2d(-)x1 0a(.)x1 00(.)x1 +1u  PARTIAL
   0x0002  00(.)x5 20( )x1                     00(.)x7 e6(.)x1 63(c)x1 c9(.)x1     PARTIAL
   0x0003  00(.)x4 20( )x1 1a(.)x1             00(.)x6 17(.)x1 66(f)x1 02(.)x1 +1u  PARTIAL
   0x0004  00(.)x3 20( )x2 61(a)x1             00(.)x6 72(r)x2 02(.)x1 c9(.)x1     PARTIAL
   0x0006  ee(.)x2 65(e)x1 0a(.)x1 20( )x1 +1u  00(.)x6 02(.)x2 1b(.)x1 04(.)x1     DIFFER
   0x0007  ff(.)x3 8d(.)x1 00(.)x1 20( )x1     00(.)x6 04(.)x2 1b(.)x1 02(.)x1     PARTIAL
   0x0008  00(.)x4 20( )x2                     00(.)x6 01(.)x1 1b(.)x1 02(.)x1 +1u  PARTIAL
   0x0009  20( )x2 30(0)x2 fe(.)x1 46(F)x1     02(.)x3 7b({)x2 18(.)x2 1f(.)x1 +2u  DIFFER
   0x000a  00(.)x4 20( )x2                     df(.)x4 00(.)x3 20( )x1 17(.)x1 +1u  PARTIAL
   0x000b  20( )x4 6b(k)x1 00(.)x1             20( )x4 e0(.)x1 40(@)x1 00(.)x1 +3u  PARTIAL
   0x000c  47(G)x3 02(.)x2 65(e)x1             47(G)x4 20( )x3 00(.)x1 02(.)x1 +1u  PARTIAL
   0x000d  50(P)x3 72(r)x1 a9(.)x1 20( )x1     50(P)x4 20( )x2 01(.)x1 72(r)x1 +2u  PARTIAL
   0x000e  4f(O)x3 6e(n)x1 de(.)x1 20( )x1     4f(O)x4 05(.)x1 20( )x1 0c(.)x1 +3u  PARTIAL
   0x000f  53(S)x3 20( )x2 00(.)x1             53(S)x4 00(.)x3 6e(n)x1 04(.)x1 +1u  PARTIAL
   0x0010  20( )x5 62(b)x1                     02(.)x4 20( )x2 00(.)x2 10(.)x1 +1u  PARTIAL
   0x0011  20( )x4 fb(.)x1 aa(.)x1             00(.)x6 20( )x1 02(.)x1 0a(.)x1 +1u  PARTIAL
   0x0012  20( )x3 00(.)x2 0d(.)x1             00(.)x5 20( )x3 01(.)x1 80(.)x1     PARTIAL
   0x0013  20( )x4 ff(.)x1 00(.)x1             04(.)x2 00(.)x2 06(.)x2 ff(.)x1 +3u  PARTIAL
   0x0014  00(.)x4 0f(.)x1 20( )x1             00(.)x5 2d(-)x1 20( )x1 80(.)x1 +2u  PARTIAL
   0x0015  00(.)x4 20( )x2                     00(.)x7 01(.)x1 20( )x1 10(.)x1     PARTIAL
   0x0016  00(.)x3 7a(z)x1 fe(.)x1 20( )x1     00(.)x7 22(")x1 73(s)x1 02(.)x1     PARTIAL
   0x0017  00(.)x4 6f(o)x1 20( )x1             00(.)x7 6e(n)x1 20( )x1 01(.)x1     PARTIAL
   0x0018  ff(.)x3 2d(-)x1 00(.)x1 20( )x1     00(.)x5 2d(-)x1 04(.)x1 c9(.)x1 +2u  PARTIAL
   0x0019  ff(.)x3 68(h)x1 02(.)x1 35(5)x1     00(.)x3 1d(.)x2 20( )x1 68(h)x1 +3u  PARTIAL
   0x001a  00(.)x3 61(a)x1 aa(.)x1 20( )x1     00(.)x6 20( )x1 61(a)x1 6e(n)x1 +1u  PARTIAL
   0x001b  ec(.)x3 92(.)x1 00(.)x1 01(.)x1     f8(.)x4 20( )x2 6e(n)x1 01(.)x1 +2u  PARTIAL
   0x001f  00(.)x2 52(R)x2 20( )x1 ec(.)x1     00(.)x5 61(a)x2 80(.)x1 6d(m)x1 +1u  PARTIAL
   0x0020  00(.)x2 ff(.)x2 20( )x1 ec(.)x1     00(.)x2 53(S)x2 20( )x1 6f(o)x1 +4u  PARTIAL
   0x0022  00(.)x2 ff(.)x2 20( )x1 ec(.)x1     00(.)x4 ff(.)x2 53(S)x2 01(.)x1 +1u  PARTIAL
   0x0023  00(.)x4 20( )x1 ec(.)x1             00(.)x5 53(S)x2 04(.)x1 a0(.)x1 +1u  PARTIAL
   0x0025  20( )x2 6f(o)x2 72(r)x1 ec(.)x1     20( )x2 53(S)x2 0a(.)x1 0c(.)x1 +4u  PARTIAL
   0x0027  6e(n)x2 68(h)x2 27(')x1 18(.)x1     00(.)x3 53(S)x2 1e(.)x1 20( )x1 +3u  DIFFER
   0x002a  00(.)x2 73(s)x2 ba(.)x1 0b(.)x1     00(.)x5 20( )x2 0c(.)x1 01(.)x1 +1u  PARTIAL
   0x002b  00(.)x3 02(.)x1 6c(l)x1 03(.)x1     00(.)x4 02(.)x2 20( )x1 1b(.)x1 +2u  PARTIAL
   0x002c  00(.)x3 06(.)x1 ba(.)x1 0a(.)x1     00(.)x4 20( )x2 1b(.)x1 02(.)x1 +2u  PARTIAL
   0x002d  00(.)x3 ff(.)x1 06(.)x1 14(.)x1     20( )x3 7f(.)x2 00(.)x2 1b(.)x1 +2u  PARTIAL
   0x002e  fd(.)x3 7f(.)x1 00(.)x1 01(.)x1     00(.)x3 7f(.)x2 70(p)x1 df(.)x1 +3u  PARTIAL
   0x002f  ff(.)x3 0d(.)x1 18(.)x1 20( )x1     00(.)x2 20( )x2 24($)x2 78(x)x1 +3u  PARTIAL
   0x0030  00(.)x4 20( )x1 e0(.)x1             b6(.)x2 20( )x1 2d(-)x1 00(.)x1 +5u  PARTIAL
   ... (15 more divergent offsets)
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
  prompts_b/harfbuzz_6037.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6037,
  "target": "harfbuzz",
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6037 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6037 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6037 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).