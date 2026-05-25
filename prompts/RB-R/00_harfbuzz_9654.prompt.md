==== BLOCKER ====
Target: harfbuzz
Branch ID: 9654
Location: /src/harfbuzz/src/hb-ot-shaper-vowel-constraints.cc:426:5
Enclosing function: _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)
Source line:     case HB_SCRIPT_MODI:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           2        8          0  loser (I2S vs naive); loser (value_profile vs value_profile_cmplog)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             9        1          0  winner (value_profile vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['value_profile']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 17  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=2.40h  loser=9.95h
  avg hitcount on branch: winner=4  loser=1
  prob_div=0.80  dur_div=7.55h  hit_div=3
  subject-level: delta_AUC=9064080.0  p_AUC=0.0002  delta_Final=796.1  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 19  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=2.75h  loser=9.95h
  avg hitcount on branch: winner=3  loser=1
  prob_div=0.70  dur_div=7.20h  hit_div=2
  subject-level: delta_AUC=4469430.0  p_AUC=0.0046  delta_Final=760.0  p_final=0.0008

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/9654/{W,L}/branch_coverage_show.txt

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
[L]    58      case HB_SCRIPT_DEVANAGARI:
[L]    59        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[L]    60        {
[L]    61  	bool matched = false;
[L]    62  	switch (buffer->cur ().codepoint)
[L]    63  	{
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
[L]   103  	}
[L]   104  	(void) buffer->next_glyph ();
[L]   105  	if (matched) _output_with_dotted_circle (buffer);
[L]   106        }
[L]   107        break;
[ ]   108  
[L]   109      case HB_SCRIPT_BENGALI:
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
[L]   222      case HB_SCRIPT_TELUGU:
[L]   223        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[L]   224        {
[L]   225  	bool matched = false;
[L]   226  	switch (buffer->cur ().codepoint)
[L]   227  	{
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
[L]   239  	}
[L]   240  	(void) buffer->next_glyph ();
[L]   241  	if (matched) _output_with_dotted_circle (buffer);
[L]   242        }
[L]   243        break;
[ ]   244  
[L]   245      case HB_SCRIPT_KANNADA:
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
[L]   263      case HB_SCRIPT_MALAYALAM:
[L]   264        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[L]   265        {
[L]   266  	bool matched = false;
[L]   267  	switch (buffer->cur ().codepoint)
[L]   268  	{
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
[L]   283  	}
[L]   284  	(void) buffer->next_glyph ();
[L]   285  	if (matched) _output_with_dotted_circle (buffer);
[L]   286        }
[L]   287        break;
[ ]   288  
[L]   289      case HB_SCRIPT_SINHALA:
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
[W]   426      case HB_SCRIPT_MODI: <-- BLOCKER
[W]   427        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[W]   428        {
[W]   429  	bool matched = false;
[W]   430  	switch (buffer->cur ().codepoint)
[W]   431  	{
[W]   432  	  case 0x11600u: case 0x11601u:
[W]   433  	    switch (buffer->cur (1).codepoint)
[W]   434  	    {
[ ]   435  	      case 0x11639u: case 0x1163Au:
[ ]   436  		matched = true;
[ ]   437  		break;
[W]   438  	    }
[W]   439  	    break;
[W]   440  	}
[W]   441  	(void) buffer->next_glyph ();
[W]   442  	if (matched) _output_with_dotted_circle (buffer);
[W]   443        }
[W]   444        break;
[ ]   445  
[B]   446      case HB_SCRIPT_TAKRI:
[L]   447        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[L]   448        {
[L]   449  	bool matched = false;
[L]   450  	switch (buffer->cur ().codepoint)
[L]   451  	{
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
[L]   463  	}
[L]   464  	(void) buffer->next_glyph ();
[L]   465  	if (matched) _output_with_dotted_circle (buffer);
[L]   466        }
[L]   467        break;
[ ]   468  
[L]   469      default:
[L]   470        break;
[B]   471    }
[B]   472    buffer->sync ();
[B]   473  }

--- Caller (1 hop): hb-ot-shaper-use.cc:preprocess_text_use(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) (/src/harfbuzz/src/hb-ot-shaper-use.cc:474-476, calls _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) at line 475) (full body — short) ---
[B]   474  {
[B]   475    _hb_preprocess_text_vowel_constraints (plan, buffer, font); <-- CALL
[B]   476  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-indic.cc:preprocess_text_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1502-1506, calls _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) at line 1505)
hop 2  hb-ot-shaper-use.cc:preprocess_text_use(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:474-476, calls _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) at line 475)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0        48  hb-ot-shaper-indic.cc:set_indic_properties(hb_glyph_info_t&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:44-50)
       0        48  hb-ot-shaper-indic.cc:decompose_indic(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int*, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1513-1539)
       0        32  hb-ot-shaper-indic.cc:initial_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:968-986)
       0        16  hb-ot-shaper-indic.cc:final_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1017-1474)
       0        15  hb_indic_would_substitute_feature_t::init(hb_ot_map_t const*, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:93-97)
       0         3  hb-ot-shaper-indic.cc:is_one_of(hb_glyph_info_t const&, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:55-59)
       0         3  hb-ot-shaper-indic.cc:collect_features_indic(hb_ot_shape_planner_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:241-265)
       0         3  hb-ot-shaper-indic.cc:override_features_indic(hb_ot_shape_planner_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:269-272)
       0         3  hb-ot-shaper-indic.cc:data_create_indic(hb_ot_shape_plan_t const*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:317-356)
       0         3  hb-ot-shaper-indic.cc:data_destroy_indic(void*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:360-362)
       0         3  hb-ot-shaper-indic.cc:setup_masks_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:403-414)
       0         3  hb-ot-shaper-indic.cc:preprocess_text_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1502-1506)
       0         3  hb-ot-shaper-indic.cc:compose_indic(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1546-1555)
       0         2  hb-ot-shaper-indic.cc:is_consonant(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:72-74)
       0         2  indic_shape_plan_t::load_virama_glyph(hb_font_t*, unsigned int*) const  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:278-294)
... (6 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ot-shaper-indic.cc:preprocess_text_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1502-1506) ---
  d=2   L1504  T=0 F=0  T=3 F=0  if (!indic_plan->uniscribe_bug_compatible)
--- d=1  _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-vowel-constraints.cc:41-473) ---
  d=1   L  58  T=0 F=10  T=1 F=8  case HB_SCRIPT_DEVANAGARI:
  d=1   L  59  T=0 F=0  T=15 F=1  for (buffer->idx = 0; buffer->idx + 1 < count && buffer->...
  d=1   L  59  T=0 F=0  T=15 F=0  for (buffer->idx = 0; buffer->idx + 1 < count && buffer->...
  d=1   L  62  T=0 F=0  T=15 F=0  switch (buffer->cur ().codepoint)
  d=1   L  64  T=0 F=0  T=0 F=15  case 0x0905u:
  d=1   L  74  T=0 F=0  T=0 F=15  case 0x0906u:
  d=1   L  83  T=0 F=0  T=0 F=15  case 0x0909u:
  d=1   L  86  T=0 F=0  T=0 F=15  case 0x090Fu:
  d=1   L  94  T=0 F=0  T=0 F=15  case 0x0930u:
  d=1   L 105  T=0 F=0  T=0 F=15  if (matched) _output_with_dotted_circle (buffer);
  d=1   L 222  T=0 F=10  T=1 F=8  case HB_SCRIPT_TELUGU:
  d=1   L 223  T=0 F=0  T=15 F=1  for (buffer->idx = 0; buffer->idx + 1 < count && buffer->...
  d=1   L 223  T=0 F=0  T=15 F=0  for (buffer->idx = 0; buffer->idx + 1 < count && buffer->...
  d=1   L 226  T=0 F=0  T=15 F=0  switch (buffer->cur ().codepoint)
  d=1   L 228  T=0 F=0  T=0 F=15  case 0x0C12u:
  d=1   L 236  T=0 F=0  T=0 F=15  case 0x0C3Fu: case 0x0C46u: case 0x0C4Au:
  d=1   L 236  T=0 F=0  T=0 F=15  case 0x0C3Fu: case 0x0C46u: case 0x0C4Au:
  d=1   L 236  T=0 F=0  T=0 F=15  case 0x0C3Fu: case 0x0C46u: case 0x0C4Au:
  d=1   L 241  T=0 F=0  T=0 F=15  if (matched) _output_with_dotted_circle (buffer);
  d=1   L 263  T=0 F=10  T=1 F=8  case HB_SCRIPT_MALAYALAM:
  d=1   L 264  T=0 F=0  T=15 F=1  for (buffer->idx = 0; buffer->idx + 1 < count && buffer->...
  d=1   L 264  T=0 F=0  T=15 F=0  for (buffer->idx = 0; buffer->idx + 1 < count && buffer->...
  d=1   L 267  T=0 F=0  T=15 F=0  switch (buffer->cur ().codepoint)
  d=1   L 269  T=0 F=0  T=0 F=15  case 0x0D07u: case 0x0D09u:
  d=1   L 269  T=0 F=0  T=0 F=15  case 0x0D07u: case 0x0D09u:
  d=1   L 272  T=0 F=0  T=0 F=15  case 0x0D0Eu:
  d=1   L 275  T=0 F=0  T=0 F=15  case 0x0D12u:
  d=1   L 285  T=0 F=0  T=0 F=15  if (matched) _output_with_dotted_circle (buffer);
  d=1   L 426  T=10 F=0  T=0 F=9  case HB_SCRIPT_MODI:  <-- BLOCKER
  d=1   L 427  T=150 F=0  T=0 F=0  for (buffer->idx = 0; buffer->idx + 1 < count && buffer->...
  d=1   L 427  T=150 F=10  T=0 F=0  for (buffer->idx = 0; buffer->idx + 1 < count && buffer->...
  d=1   L 430  T=136 F=14  T=0 F=0  switch (buffer->cur ().codepoint)
  d=1   L 432  T=14 F=136  T=0 F=0  case 0x11600u: case 0x11601u:
  d=1   L 432  T=0 F=150  T=0 F=0  case 0x11600u: case 0x11601u:
  d=1   L 433  T=14 F=0  T=0 F=0  switch (buffer->cur (1).codepoint)
  d=1   L 435  T=0 F=14  T=0 F=0  case 0x11639u: case 0x1163Au:
  d=1   L 435  T=0 F=14  T=0 F=0  case 0x11639u: case 0x1163Au:
  d=1   L 442  T=0 F=150  T=0 F=0  if (matched) _output_with_dotted_circle (buffer);
  d=1   L 446  T=0 F=10  T=1 F=8  case HB_SCRIPT_TAKRI:
  d=1   L 447  T=0 F=0  T=15 F=1  for (buffer->idx = 0; buffer->idx + 1 < count && buffer->...
  d=1   L 447  T=0 F=0  T=15 F=0  for (buffer->idx = 0; buffer->idx + 1 < count && buffer->...
  d=1   L 450  T=0 F=0  T=15 F=0  switch (buffer->cur ().codepoint)
  d=1   L 452  T=0 F=0  T=0 F=15  case 0x11680u:
  d=1   L 460  T=0 F=0  T=0 F=15  case 0x11686u:
  d=1   L 465  T=0 F=0  T=0 F=15  if (matched) _output_with_dotted_circle (buffer);
  d=1   L 469  T=0 F=10  T=5 F=4  default:

[off-chain: 92 additional divergent branches across 18 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=7729a7101cb0f296, size=23 bytes, fuzzer=cmplog, trial=2, discovered_at=2s, mutation_op=BytesSwapMutator,BytesDeleteMutator,ByteNegMutator,TokenReplace,ByteInterestingMutator):
  0000: 00 00 df 20 20 6b 4f 52 00 16 01 00 10 00 7f ff   ...  kOR........
  0010: 05 fe 01 00 80 00 00                              .......
Seed 2 (id=5b5ca69be6a83382, size=34 bytes, fuzzer=cmplog, trial=2, discovered_at=13s, mutation_op=BytesRandSetMutator,ByteFlipMutator,BytesDeleteMutator,BytesInsertCopyMutator,BytesSetMutator,TokenReplace,BytesDeleteMutator):
  0000: 4f 54 54 4f 00 01 20 20 20 20 20 20 00 01 48 56   OTTO..      ..HV
  0010: 41 52 20 df 20 20 0a 02 00 16 01 00 20 ff d7 00   AR .  ...... ...
  0020: 00 20                                             . 
Seed 3 (id=0562f3b39cb3dae8, size=46 bytes, fuzzer=cmplog, trial=2, discovered_at=45s, mutation_op=BytesExpandMutator):
  0000: 4f 54 54 4f 00 01 20 20 20 20 20 20 00 01 48 56   OTTO..      ..HV
  0010: 41 52 20 df 20 20 0a 02 00 16 01 00 20 52 20 df   AR .  ...... R .
  0020: 20 20 0a 02 00 16 01 00 20 ff d7 00 00 20           ...... .... 
Seed 4 (id=96db89628c931100, size=136 bytes, fuzzer=cmplog, trial=2, discovered_at=250s, mutation_op=BytesExpandMutator,CrossoverInsertMutator,ByteInterestingMutator,DwordInterestingMutator):
  0000: 00 10 f9 f9 f9 17 ff ff 00 00 00 00 00 21 20 20   .............!  
  0010: 20 20 20 20 20 20 20 0b 20 00 20 20 20 20 20 20          . .      
  0020: 6b 65 72 f9 17 00 00 0a 00 00 00 00 20 20 20 2a   ker.........   *
  0030: 64 20 19 20 20 20 20 6e 20 20 20 0b 20 00 00 6b   d .    n   . ..k
Seed 5 (id=369fd707a65036a2, size=109 bytes, fuzzer=cmplog, trial=2, discovered_at=346s, mutation_op=WordAddMutator,ByteFlipMutator,BytesExpandMutator,BytesDeleteMutator,QwordAddMutator,ByteIncMutator):
  0000: ff 08 08 08 08 08 08 08 08 04 08 01 00 00 0c 18   ................
  0010: 00 00 00 04 ff ff 20 00 00 20 20 20 20 20 20 0a   ...... ..      .
  0020: 01 00 01 20 08 20 21 20 00 00 20 20 20 00 16 01   ... . ! ..   ...
  0030: 00 20 09 03 00 01 00 fe 01 00 01 00 00 01 1e 20   . ............. 

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0068ef8b9292e1cb, size=18 bytes, fuzzer=cmplog, trial=1, discovered_at=4s, mutation_op=TokenInsert,BytesRandInsertMutator,ByteIncMutator):
  0000: 9e 9e 9e 90 90 90 90 90 9e 9e 9e 9f b2 16 01 00   ................
  0010: 9e 9e                                             ..
Seed 2 (id=006d67d4a429fd99, size=19 bytes, fuzzer=cmplog, trial=1, discovered_at=169s, mutation_op=BytesInsertMutator,BitFlipMutator,BytesDeleteMutator):
  0000: 40 a8 00 00 5f 5f 20 28 20 20 20 20 20 20 20 20   @...__ (        
  0010: 20 a9 a8                                           ..
Seed 3 (id=0083da97d7f94a2e, size=19 bytes, fuzzer=cmplog, trial=1, discovered_at=227s, mutation_op=BytesCopyMutator,ByteIncMutator):
  0000: 10 18 00 00 4b e9 01 00 00 0f 0c 0c 0c 0c 0c 0c   ....K...........
  0010: 0c 0c 00                                          ...
Seed 4 (id=0097ed9866a116a9, size=76 bytes, fuzzer=cmplog, trial=1, discovered_at=258s, mutation_op=CrossoverReplaceMutator,CrossoverReplaceMutator,DwordAddMutator):
  0000: 01 00 00 00 01 0c 0c 0c 0c 0c 0c 0c 0c 0c 20 20   ..............  
  0010: 20 0c 04 14 20 20 f3 0c 2f 0c 0c 0c 0c 20 00 00    ...  ../.... ..
  0020: 01 13 01 00 00 20 20 20 20 0c 0c 7f 0c 0c 0b f3   .....    .......
  0030: 0c 0c 0c 0c 20 20 20 0c 00 04 1a 0c f0 01 0e 05   ....   .........
Seed 5 (id=000d2c963873035d, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=765s, mutation_op=BytesDeleteMutator):
  0000: 00 1b 01 00 00 a0 00 00 20 04 0d 6e 00 1b 00 00   ........ ..n....
  0010: 00 a0 00 00 20 09 09 01 00 1b 00 00 7f 03 02 00   .... ...........
  0020: 20 6d 00 00 20 8e 20 20 df                         m.. .  .


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x4 f3(.)x3 4f(O)x2 ff(.)x1     00(.)x5 9e(.)x1 40(@)x1 10(.)x1 +2u  PARTIAL
   0x0002  00(.)x4 54(T)x2 df(.)x1 f9(.)x1 +2u  00(.)x7 9e(.)x1 01(.)x1 7f(.)x1     PARTIAL
   0x0003  00(.)x5 4f(O)x2 20( )x1 f9(.)x1 +1u  00(.)x8 90(.)x1 ff(.)x1             PARTIAL
   0x0004  20( )x4 00(.)x4 f9(.)x1 08(.)x1     00(.)x5 90(.)x1 5f(_)x1 4b(K)x1 +2u  PARTIAL
   0x000c  00(.)x5 10(.)x4 1a(.)x1             20( )x3 0c(.)x2 ff(.)x2 b2(.)x1 +2u  PARTIAL
   0x000d  00(.)x6 01(.)x2 21(!)x1 ff(.)x1     20( )x4 0c(.)x2 ff(.)x2 16(.)x1 +1u  PARTIAL
   0x0010  00(.)x6 41(A)x2 05(.)x1 20( )x1     20( )x4 41(A)x2 9e(.)x1 0c(.)x1 +2u  PARTIAL
   0x0012  01(.)x4 20( )x3 00(.)x3             00(.)x2 20( )x2 b9(.)x2 a8(.)x1 +2u  PARTIAL
   0x0013  00(.)x5 df(.)x2 20( )x1 04(.)x1 +1u  20( )x3 b9(.)x2 14(.)x1 00(.)x1     PARTIAL
   0x0014  20( )x3 0c(.)x3 00(.)x2 80(.)x1 +1u  20( )x3 b9(.)x2 0c(.)x1 be(.)x1     PARTIAL
   0x0015  20( )x7 00(.)x1 ff(.)x1 16(.)x1     20( )x2 01(.)x2 09(.)x1 82(.)x1 +1u  PARTIAL
   0x0017  00(.)x5 02(.)x2 0b(.)x1 ff(.)x1     ff(.)x3 0c(.)x1 01(.)x1 00(.)x1 +1u  PARTIAL
   0x0018  00(.)x7 20( )x1 ff(.)x1             fe(.)x3 2f(/)x1 00(.)x1 a0(.)x1 +1u  PARTIAL
   0x001a  20( )x3 00(.)x3 01(.)x2 df(.)x1     1a(.)x4 0c(.)x1 00(.)x1 20( )x1     PARTIAL
   0x001b  00(.)x6 20( )x2 37(7)x1             20( )x5 0c(.)x1 00(.)x1             PARTIAL
   0x001c  20( )x4 00(.)x3 75(u)x1 43(C)x1     47(G)x3 20( )x2 0c(.)x1 7f(.)x1     PARTIAL
   0x001d  00(.)x3 20( )x2 ff(.)x1 52(R)x1 +2u  20( )x3 50(P)x3 03(.)x1             PARTIAL
   0x001e  20( )x3 00(.)x3 d7(.)x1 66(f)x1 +1u  4f(O)x3 02(.)x2 00(.)x1 20( )x1     PARTIAL
   0x001f  00(.)x5 df(.)x1 20( )x1 0a(.)x1 +1u  53(S)x3 00(.)x2 0a(.)x1 02(.)x1     PARTIAL
   0x0021  00(.)x5 20( )x2 65(e)x1 6c(l)x1     00(.)x3 13(.)x1 6d(m)x1 54(T)x1 +1u  PARTIAL
   0x0022  00(.)x4 0a(.)x1 72(r)x1 01(.)x1 +1u  03(.)x4 01(.)x1 00(.)x1 0e(.)x1     PARTIAL
   0x0023  00(.)x3 02(.)x1 f9(.)x1 20( )x1 +2u  20( )x4 00(.)x2 ff(.)x1             PARTIAL
   0x0024  00(.)x5 17(.)x1 08(.)x1 1a(.)x1     00(.)x5 20( )x1 ff(.)x1             PARTIAL
   0x0025  00(.)x5 16(.)x1 20( )x1 ff(.)x1     00(.)x3 20( )x1 8e(.)x1 0c(.)x1 +1u  PARTIAL
   0x0026  00(.)x5 01(.)x1 21(!)x1 10(.)x1     00(.)x3 20( )x2 0a(.)x1 be(.)x1     PARTIAL
   0x0027  00(.)x6 0a(.)x1 20( )x1             00(.)x4 20( )x2 ab(.)x1             PARTIAL
   0x0028  00(.)x4 0c(.)x3 20( )x1             20( )x2 00(.)x2 df(.)x1 04(.)x1 +1u  PARTIAL
   0x0029  00(.)x4 20( )x3 ff(.)x1             ff(.)x2 0c(.)x1 e1(.)x1 00(.)x1 +1u  PARTIAL
   0x002a  00(.)x5 d7(.)x1 20( )x1 80(.)x1     ff(.)x2 0c(.)x1 e1(.)x1 80(.)x1 +1u  PARTIAL
   0x002b  00(.)x4 20( )x1 80(.)x1 ff(.)x1 +1u  00(.)x2 10(.)x2 7f(.)x1 6f(o)x1     PARTIAL
   0x002c  10(.)x3 00(.)x2 20( )x2 ff(.)x1     4d(M)x2 0c(.)x1 20( )x1 00(.)x1 +1u  PARTIAL
   0x002d  04(.)x3 20( )x2 00(.)x2 16(.)x1     00(.)x2 0c(.)x1 02(.)x1 41(A)x1 +1u  PARTIAL
   0x0030  0c(.)x3 00(.)x2 64(d)x1 02(.)x1     04(.)x2 0c(.)x1 54(T)x1 13(.)x1 +1u  PARTIAL
   0x0031  f0(.)x3 20( )x2 ff(.)x1 00(.)x1     00(.)x3 0c(.)x1 13(.)x1 2d(-)x1     PARTIAL
   0x0034  0c(.)x3 20( )x1 00(.)x1 75(u)x1 +1u  00(.)x4 20( )x1 73(s)x1             PARTIAL
   0x0035  0c(.)x3 20( )x1 01(.)x1 6c(l)x1 +1u  00(.)x2 78(x)x2 20( )x1 66(f)x1     PARTIAL
   0x0036  0c(.)x3 00(.)x2 20( )x1 66(f)x1     78(x)x2 20( )x1 e1(.)x1 00(.)x1 +1u  PARTIAL
   0x0037  00(.)x3 20( )x2 6e(n)x1 fe(.)x1     78(x)x2 0c(.)x1 e1(.)x1 00(.)x1 +1u  PARTIAL
   0x0038  0c(.)x3 20( )x1 01(.)x1 00(.)x1     78(x)x2 00(.)x1 e1(.)x1 06(.)x1 +1u  PARTIAL
   0x0039  20( )x4 00(.)x1 0a(.)x1             78(x)x3 04(.)x1 e1(.)x1 00(.)x1     PARTIAL
   ... (6 more divergent offsets)
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
rows are exclusive to cmplog and value_profile_cmplog; their
presence in a winning seed's ancestor chain is direct (lower-bound)
evidence of I2S contribution.

**Per-execution cost**: edge increment + one callback per intercepted
CMP per execution + post-execution CMP-buffer processing.

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
  prompts/RB-R/00_harfbuzz_9654.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 9654,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S), value_profile_cmplog>cmplog (value_profile)]
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
      // pick EXACTLY ONE of:
      //   "I2SRandReplace"     (cmplog / vpc input-to-state substitution)
      //   "CMP_MAP gradient"   (vp / vpc Hamming/prefix-distance feedback)
      //   "havoc-only"         (lucky havoc byte mutation, no CMP introspection)
      //   "token-replace"      (TokenInsert/TokenReplace dictionary mutations)
      //   "other"              (anything that does not fit the four above)
    "verified_in_lineage": true,
      // pick true or false
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 9654 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 9654 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 9654 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).