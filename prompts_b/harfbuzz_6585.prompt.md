==== BLOCKER ====
Target: harfbuzz
Branch ID: 6585
Location: /src/harfbuzz/src/hb-ot-shaper-vowel-constraints.cc:199:18
Enclosing function: _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)
Source line: 	  case 0x0B0Fu: case 0x0B13u:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (ctx_coverage vs naive_ctx)
cmplog                           0        7          3  REFERENCE
value_profile                    3        7          0  REFERENCE
value_profile_cmplog             0        9          1  REFERENCE
naive_ctx                       10        0          0  winner (ctx_coverage vs naive)
naive_ngram4                     2        8          0  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        2        8          0  REFERENCE
fast                             5        5          0  REFERENCE
grimoire                         3        6          1  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 15  (naive_ctx vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=4.00h  loser=23.00h
  avg hitcount on branch: winner=36  loser=0
  prob_div=1.00  dur_div=19.00h  hit_div=36
  subject-level: delta_AUC=15634800.0  p_AUC=0.0003  delta_Final=258.3  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/6585/{W,L}/branch_coverage_show.txt

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
[ ]   130      case HB_SCRIPT_GURMUKHI:
[ ]   131        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[ ]   132        {
[ ]   133  	bool matched = false;
[ ]   134  	switch (buffer->cur ().codepoint)
[ ]   135  	{
[ ]   136  	  case 0x0A05u:
[ ]   137  	    switch (buffer->cur (1).codepoint)
[ ]   138  	    {
[ ]   139  	      case 0x0A3Eu: case 0x0A48u: case 0x0A4Cu:
[ ]   140  		matched = true;
[ ]   141  		break;
[ ]   142  	    }
[ ]   143  	    break;
[ ]   144  	  case 0x0A72u:
[ ]   145  	    switch (buffer->cur (1).codepoint)
[ ]   146  	    {
[ ]   147  	      case 0x0A3Fu: case 0x0A40u: case 0x0A47u:
[ ]   148  		matched = true;
[ ]   149  		break;
[ ]   150  	    }
[ ]   151  	    break;
[ ]   152  	  case 0x0A73u:
[ ]   153  	    switch (buffer->cur (1).codepoint)
[ ]   154  	    {
[ ]   155  	      case 0x0A41u: case 0x0A42u: case 0x0A4Bu:
[ ]   156  		matched = true;
[ ]   157  		break;
[ ]   158  	    }
[ ]   159  	    break;
[ ]   160  	}
[ ]   161  	(void) buffer->next_glyph ();
[ ]   162  	if (matched) _output_with_dotted_circle (buffer);
[ ]   163        }
[ ]   164        break;
[ ]   165  
[ ]   166      case HB_SCRIPT_GUJARATI:
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
[B]   190      case HB_SCRIPT_ORIYA:
[B]   191        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[B]   192        {
[B]   193  	bool matched = false;
[B]   194  	switch (buffer->cur ().codepoint)
[B]   195  	{
[ ]   196  	  case 0x0B05u:
[ ]   197  	    matched = 0x0B3Eu == buffer->cur (1).codepoint;
[ ]   198  	    break;
[B]   199  	  case 0x0B0Fu: case 0x0B13u: <-- BLOCKER
[B]   200  	    matched = 0x0B57u == buffer->cur (1).codepoint;
[B]   201  	    break;
[B]   202  	}
[B]   203  	(void) buffer->next_glyph ();
[B]   204  	if (matched) _output_with_dotted_circle (buffer);
[B]   205        }
[B]   206        break;
[ ]   207  
[B]   208      case HB_SCRIPT_TAMIL:
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
      23       248  hb-ot-shaper-indic.cc:is_one_of(hb_glyph_info_t const&, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:55-59)
      19       167  hb-ot-shaper-indic.cc:is_consonant(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:72-74)
       0        95  hb-ot-shaper-indic.cc:compare_indic_order(hb_glyph_info_t const*, hb_glyph_info_t const*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:430-435)
       0        45  hb-ot-shaper-indic.cc:is_joiner(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:80-82)
       4        47  hb-ot-shaper-indic.cc:compose_indic(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1546-1555)
       0        12  hb-ot-shaper-indic.cc:is_halant(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:86-88)
       4        15  hb-ot-shaper-indic.cc:initial_reordering_standalone_cluster(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:946-961)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ot-shaper-indic.cc:preprocess_text_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1502-1506) ---
  d=2   L1504  T=5 F=0  T=10 F=0  if (!indic_plan->uniscribe_bug_compatible)
--- d=1  _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-vowel-constraints.cc:41-473) ---
  d=1   L  45  T=0 F=5  T=0 F=10  if (buffer->flags & HB_BUFFER_FLAG_DO_NOT_INSERT_DOTTED_C...
  d=1   L  58  T=0 F=5  T=0 F=10  case HB_SCRIPT_DEVANAGARI:
  d=1   L 109  T=0 F=5  T=0 F=10  case HB_SCRIPT_BENGALI:
  d=1   L 130  T=0 F=5  T=0 F=10  case HB_SCRIPT_GURMUKHI:
  d=1   L 166  T=0 F=5  T=0 F=10  case HB_SCRIPT_GUJARATI:
  d=1   L 190  T=5 F=0  T=10 F=0  case HB_SCRIPT_ORIYA:
  d=1   L 191  T=75 F=0  T=150 F=0  for (buffer->idx = 0; buffer->idx + 1 < count && buffer->...
  d=1   L 191  T=75 F=5  T=150 F=10  for (buffer->idx = 0; buffer->idx + 1 < count && buffer->...
  d=1   L 194  T=60 F=15  T=148 F=2  switch (buffer->cur ().codepoint)
  d=1   L 196  T=0 F=75  T=0 F=150  case 0x0B05u:
  d=1   L 199  T=15 F=60  T=0 F=150  case 0x0B0Fu: case 0x0B13u:  <-- BLOCKER
  d=1   L 199  T=0 F=75  T=2 F=148  case 0x0B0Fu: case 0x0B13u:  <-- BLOCKER
  d=1   L 204  T=0 F=75  T=0 F=150  if (matched) _output_with_dotted_circle (buffer);
  d=1   L 208  T=0 F=5  T=0 F=10  case HB_SCRIPT_TAMIL:
  d=1   L 222  T=0 F=5  T=0 F=10  case HB_SCRIPT_TELUGU:
  d=1   L 245  T=0 F=5  T=0 F=10  case HB_SCRIPT_KANNADA:
  d=1   L 263  T=0 F=5  T=0 F=10  case HB_SCRIPT_MALAYALAM:
  d=1   L 289  T=0 F=5  T=0 F=10  case HB_SCRIPT_SINHALA:
  d=1   L 324  T=0 F=5  T=0 F=10  case HB_SCRIPT_BRAHMI:
  d=1   L 345  T=0 F=5  T=0 F=10  case HB_SCRIPT_KHOJKI:
  d=1   L 379  T=0 F=5  T=0 F=10  case HB_SCRIPT_KHUDAWADI:
  d=1   L 400  T=0 F=5  T=0 F=10  case HB_SCRIPT_TIRHUTA:
  d=1   L 426  T=0 F=5  T=0 F=10  case HB_SCRIPT_MODI:
  d=1   L 446  T=0 F=5  T=0 F=10  case HB_SCRIPT_TAKRI:
  d=1   L 469  T=0 F=5  T=0 F=10  default:

[off-chain: 81 additional divergent branches across 14 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=2be3a676a011a1f2, size=56 bytes, fuzzer=naive_ctx, trial=1, discovered_at=8941s, mutation_op=TokenInsert,ByteFlipMutator):
  0000: 00 61 6b 2d 68 61 6e 74 00 0d 00 ff 00 0d 00 ff   .ak-hant........
  0010: 00 0d 8e 14 13 0b 00 00 00 0d 00 ff 00 f2 8e 12   ................
  0020: 00 00 00 00 00 00 00 00 00 00 00 00 13 0b 00 00   ................
  0030: 00 0d 8e 12 40 0d 00 00                           ....@...
Seed 2 (id=06c7833b0e154f65, size=28 bytes, fuzzer=naive_ctx, trial=1, discovered_at=16444s, mutation_op=BytesRandInsertMutator,BytesDeleteMutator):
  0000: 00 0d 00 ff 00 0d 00 ff 00 0d 8e 14 13 0b 00 00   ................
  0010: 13 0b 00 00 00 0d 8e 12 40 0d 00 00               ........@...
Seed 3 (id=89dfff878e1186bc, size=32 bytes, fuzzer=naive_ctx, trial=1, discovered_at=25039s, mutation_op=BytesDeleteMutator):
  0000: 13 0b 00 00 ff 0d 8e 12 13 0b 00 00 00 0d 00 ff   ................
  0010: 00 0d 8e 12 13 0b 00 00 00 0d 8e 12 40 0d 00 00   ............@...
Seed 4 (id=61a1738ca6c821b1, size=60 bytes, fuzzer=naive_ctx, trial=1, discovered_at=31709s, mutation_op=ByteInterestingMutator,BytesInsertCopyMutator,BytesInsertCopyMutator):
  0000: 13 0b 00 00 ff 0d 8e 12 13 0b 00 00 00 0d 8e 12   ................
  0010: 13 0b 00 00 00 0d 00 ff 20 0d 13 0b 00 00 00 0d   ........ .......
  0020: 00 ff 20 0d 8e 12 0d 8e 12 0d 00 ff 20 0d 8e 12   .. ......... ...
  0030: 13 0b 00 00 00 0d 8e 12 40 0d 00 00               ........@...
Seed 5 (id=41f753b477b1a92c, size=44 bytes, fuzzer=naive_ctx, trial=1, discovered_at=38120s, mutation_op=BytesExpandMutator,DwordAddMutator):
  0000: 00 0d 00 ff 00 0d 00 ff 00 0d af 14 13 0b 00 00   ................
  0010: 13 0b 00 00 00 0d 00 ff 00 0d 8e 14 13 0b 00 00   ................
  0020: 13 0b 00 00 00 0d 8e 12 40 0d 00 00               ........@...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=404dbac1e8824ff4, size=38 bytes, fuzzer=naive, trial=1, discovered_at=361s, mutation_op=BytesRandInsertMutator,ByteNegMutator,BytesExpandMutator,TokenInsert,BitFlipMutator,DwordInterestingMutator):
  0000: 0f 0b 00 00 10 00 40 00 00 00 00 00 10 00 00 20   ......@........ 
  0010: c5 00 00 00 00 10 00 00 80 3d 3d 00 00 00 51 ff   .........==...Q.
  0020: 64 61 72 66 ff e2                                 darf..
Seed 2 (id=5f6449c19536d749, size=71 bytes, fuzzer=naive, trial=1, discovered_at=14213s, mutation_op=BytesRandInsertMutator):
  0000: c8 20 0b 0b 0b 0b 0b 0b 0b 00 00 d2 17 00 00 e2   . ..............
  0010: 27 00 00 d2 17 00 00 e2 20 00 00 de 17 00 00 e2   '....... .......
  0020: 20 00 00 d2 17 00 00 e2 20 00 00 d2 17 00 00 e2    ....... .......
  0030: 6f 6f 6f 6f 6f 6f 6f 6f 6f 6f 6f 6f 6f 6f 20 00   oooooooooooooo .
Seed 3 (id=6f30fd62dd63099f, size=81 bytes, fuzzer=naive, trial=1, discovered_at=17717s, mutation_op=DwordAddMutator,WordAddMutator):
  0000: 65 65 65 65 10 00 00 59 10 00 00 59 10 fe 00 00   eeee...Y...Y....
  0010: 00 01 0b 00 00 00 21 00 00 49 10 00 00 6c 02 00   ......!..I...l..
  0020: 00 59 10 00 00 98 10 00 00 59 10 00 00 00 00 00   .Y.......Y......
  0030: 00 59 28 00 00 67 10 00 00 59 10 00 00 49 10 00   .Y(..g...Y...I..
Seed 4 (id=09e6326f07745c9b, size=131 bytes, fuzzer=naive, trial=1, discovered_at=21508s, mutation_op=ByteIncMutator):
  0000: 15 bd cb cb cb cb cb 00 0c 72 61 66 63 ff 00 01   .........rafc...
  0010: 00 ff 7f 00 7f 10 00 ff dd 20 00 10 00 00 00 cb   ......... ......
  0020: 00 ff 7f 00 7f 10 00 ff dd 20 00 10 00 fe ff 7f   ......... ......
  0030: 00 00 0c 00 ff e3 00 cb 84 0c 00 00 0c 0c 0c 0c   ................
Seed 5 (id=44dc2643908bb1ca, size=131 bytes, fuzzer=naive, trial=1, discovered_at=21509s, mutation_op=TokenReplace,ByteIncMutator,BytesCopyMutator):
  0000: 15 bd cb cb cb cb cb 00 0c 72 61 66 63 ff 00 01   .........rafc...
  0010: 00 ff 7f 00 7f 10 00 ff dd 20 00 10 00 00 00 cb   ......... ......
  0020: 00 c8 0b 00 00 cb 7f ff 00 20 00 10 00 fe ff 7f   ......... ......
  0030: 00 00 0c 00 ff e3 01 cb 84 0c 00 00 0c 0c 0c 0c   ................


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x3 13(.)x2                     0f(.)x2 15(.)x2 00(.)x2 cb(.)x2 +2u  PARTIAL
   0x0001  0d(.)x2 0b(.)x2 61(a)x1             0b(.)x2 bd(.)x2 00(.)x2 cb(.)x2 +2u  PARTIAL
   0x0002  00(.)x4 6b(k)x1                     00(.)x5 cb(.)x2 0b(.)x1 65(e)x1 +1u  PARTIAL
   0x0003  ff(.)x2 00(.)x2 2d(-)x1             00(.)x3 cb(.)x2 0c(.)x2 0b(.)x1 +2u  PARTIAL
   0x0004  00(.)x2 ff(.)x2 68(h)x1             10(.)x3 cb(.)x2 72(r)x2 0b(.)x1 +2u  PARTIAL
   0x0005  0d(.)x4 61(a)x1                     00(.)x4 cb(.)x2 61(a)x2 0b(.)x1 +1u  PARTIAL
   0x0006  00(.)x2 8e(.)x2 6e(n)x1             40(@)x2 00(.)x2 cb(.)x2 66(f)x2 +2u  PARTIAL
   0x0007  ff(.)x2 12(.)x2 74(t)x1             00(.)x4 63(c)x2 0b(.)x1 59(Y)x1 +2u  PARTIAL
   0x0008  00(.)x3 13(.)x2                     00(.)x3 0c(.)x2 ff(.)x2 0b(.)x1 +2u  PARTIAL
   0x0009  0d(.)x3 0b(.)x2                     00(.)x6 72(r)x2 10(.)x1 c8(.)x1     DIFFER
   0x000a  00(.)x3 8e(.)x1 af(.)x1             00(.)x5 61(a)x2 01(.)x2 c8(.)x1     PARTIAL
   0x000b  14(.)x2 00(.)x2 ff(.)x1             00(.)x5 66(f)x2 d2(.)x1 59(Y)x1 +1u  PARTIAL
   0x000c  00(.)x3 13(.)x2                     10(.)x2 63(c)x2 00(.)x2 17(.)x1 +3u  PARTIAL
   0x000d  0d(.)x3 0b(.)x2                     00(.)x4 ff(.)x2 20( )x2 fe(.)x1 +1u  DIFFER
   0x000e  00(.)x4 8e(.)x1                     00(.)x9 c8(.)x1                     PARTIAL
   0x000f  ff(.)x2 00(.)x2 12(.)x1             00(.)x3 01(.)x2 7f(.)x2 20( )x1 +2u  PARTIAL
   0x0010  13(.)x3 00(.)x2                     00(.)x5 10(.)x2 c5(.)x1 27(')x1 +1u  PARTIAL
   0x0011  0b(.)x3 0d(.)x2                     00(.)x5 ff(.)x3 01(.)x1 10(.)x1     DIFFER
   0x0012  00(.)x3 8e(.)x2                     00(.)x3 7f(.)x2 ff(.)x2 0b(.)x1 +2u  PARTIAL
   0x0013  00(.)x3 14(.)x1 12(.)x1             00(.)x6 01(.)x2 d2(.)x1 20( )x1     PARTIAL
   0x0014  00(.)x3 13(.)x2                     00(.)x5 7f(.)x2 17(.)x1 0b(.)x1 +1u  PARTIAL
   0x0015  0d(.)x3 0b(.)x2                     00(.)x6 10(.)x3 0b(.)x1             PARTIAL
   0x0016  00(.)x4 8e(.)x1                     00(.)x6 21(!)x1 ff(.)x1 cb(.)x1 +1u  PARTIAL
   0x0017  00(.)x2 ff(.)x2 12(.)x1             00(.)x3 ff(.)x2 cb(.)x2 e2(.)x1 +2u  PARTIAL
   0x0018  00(.)x3 40(@)x1 20( )x1             00(.)x2 dd(.)x2 cb(.)x2 80(.)x1 +3u  PARTIAL
   0x0019  0d(.)x5                             00(.)x2 20( )x2 cb(.)x2 3d(=)x1 +3u  DIFFER
   0x001a  00(.)x2 8e(.)x2 13(.)x1             00(.)x5 cb(.)x2 3d(=)x1 10(.)x1 +1u  PARTIAL
   0x001c  00(.)x2 40(@)x1 13(.)x1             00(.)x6 17(.)x1 34(4)x1 10(.)x1 +1u  PARTIAL
   0x001d  f2(.)x1 0d(.)x1 00(.)x1 0b(.)x1     00(.)x6 10(.)x2 6c(l)x1 0c(.)x1     PARTIAL
   0x001e  00(.)x3 8e(.)x1                     00(.)x6 cb(.)x2 51(Q)x1 02(.)x1     PARTIAL
   0x001f  00(.)x2 12(.)x1 0d(.)x1             00(.)x4 cb(.)x2 ff(.)x1 e2(.)x1 +2u  PARTIAL
   0x0020  00(.)x2 13(.)x1                     00(.)x5 64(d)x1 20( )x1 0c(.)x1 +2u  PARTIAL
   0x0021  00(.)x1 ff(.)x1 0b(.)x1             00(.)x5 61(a)x1 59(Y)x1 ff(.)x1 +2u  PARTIAL
   0x0022  00(.)x2 20( )x1                     00(.)x5 72(r)x1 10(.)x1 7f(.)x1 +2u  PARTIAL
   0x0023  00(.)x2 0d(.)x1                     00(.)x6 66(f)x1 d2(.)x1 0c(.)x1 +1u  PARTIAL
   0x0024  00(.)x2 8e(.)x1                     00(.)x4 ff(.)x1 17(.)x1 7f(.)x1 +3u  PARTIAL
   0x0025  00(.)x1 12(.)x1 0d(.)x1             00(.)x2 ff(.)x2 e2(.)x1 98(.)x1 +4u  PARTIAL
   0x0026  00(.)x1 0d(.)x1 8e(.)x1             00(.)x4 10(.)x1 7f(.)x1 64(d)x1 +2u  PARTIAL
   0x0027  00(.)x1 8e(.)x1 12(.)x1             00(.)x4 ff(.)x2 e2(.)x1 75(u)x1 +1u  PARTIAL
   0x0028  00(.)x1 12(.)x1 40(@)x1             00(.)x3 20( )x1 dd(.)x1 b1(.)x1 +3u  PARTIAL
   ... (19 more divergent offsets)
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
  prompts_b/harfbuzz_6585.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6585,
  "target": "harfbuzz",
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6585 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6585 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6585 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).