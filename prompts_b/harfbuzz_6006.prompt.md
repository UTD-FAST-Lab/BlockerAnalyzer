==== BLOCKER ====
Target: harfbuzz
Branch ID: 6006
Location: /src/harfbuzz/src/hb-ot-shaper-vowel-constraints.cc:67:22
Enclosing function: _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)
Source line: 	      case 0x093Au: case 0x093Bu: case 0x093Eu: case 0x0945u:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        8          1  loser (value_profile vs value_profile)
cmplog                           1        6          3  REFERENCE
value_profile                    9        1          0  winner (value_profile vs naive)
value_profile_cmplog             3        7          0  REFERENCE
naive_ctx                        4        6          0  REFERENCE
naive_ngram4                     1        7          2  REFERENCE
mopt                             1        6          3  REFERENCE
minimizer                        4        6          0  REFERENCE
fast                             6        3          1  REFERENCE
grimoire                         0        6          4  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile > naive  [delta: value_profile] ---
  subject 12  (value_profile vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=8  unreached=1
  avg duration blocked: winner=9.10h  loser=16.78h
  avg hitcount on branch: winner=4  loser=2
  prob_div=0.79  dur_div=7.68h  hit_div=2
  subject-level: delta_AUC=17795340.0  p_AUC=0.0002  delta_Final=285.0  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/6006/{W,L}/branch_coverage_show.txt

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
[B]    58      case HB_SCRIPT_DEVANAGARI:
[B]    59        for (buffer->idx = 0; buffer->idx + 1 < count && buffer->successful;)
[B]    60        {
[B]    61  	bool matched = false;
[B]    62  	switch (buffer->cur ().codepoint)
[B]    63  	{
[B]    64  	  case 0x0905u:
[B]    65  	    switch (buffer->cur (1).codepoint)
[B]    66  	    {
[W]    67  	      case 0x093Au: case 0x093Bu: case 0x093Eu: case 0x0945u: <-- BLOCKER
[W]    68  	      case 0x0946u: case 0x0949u: case 0x094Au: case 0x094Bu:
[W]    69  	      case 0x094Cu: case 0x094Fu: case 0x0956u: case 0x0957u:
[W]    70  		matched = true;
[W]    71  		break;
[B]    72  	    }
[B]    73  	    break;
[B]    74  	  case 0x0906u:
[ ]    75  	    switch (buffer->cur (1).codepoint)
[ ]    76  	    {
[ ]    77  	      case 0x093Au: case 0x0945u: case 0x0946u: case 0x0947u:
[ ]    78  	      case 0x0948u:
[ ]    79  		matched = true;
[ ]    80  		break;
[ ]    81  	    }
[ ]    82  	    break;
[L]    83  	  case 0x0909u:
[L]    84  	    matched = 0x0941u == buffer->cur (1).codepoint;
[L]    85  	    break;
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
[B]   103  	}
[B]   104  	(void) buffer->next_glyph ();
[B]   105  	if (matched) _output_with_dotted_circle (buffer);
[B]   106        }
[B]   107        break;
[ ]   108  
[B]   109      case HB_SCRIPT_BENGALI:
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
       0        47  hb-ot-shaper-indic.cc:initial_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:968-986)
       0        47  hb-ot-shaper-indic.cc:final_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1017-1474)
       0        15  hb-ot-shaper-indic.cc:is_one_of(hb_glyph_info_t const&, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:55-59)
       0        13  hb-ot-shaper-indic.cc:is_consonant(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:72-74)
       5        15  hb_indic_would_substitute_feature_t::init(hb_ot_map_t const*, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:93-97)
       0         9  hb-ot-shaper-indic.cc:initial_reordering_consonant_syllable(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:470-939)
       0         3  indic_shape_plan_t::load_virama_glyph(hb_font_t*, unsigned int*) const  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:278-294)
       0         3  hb-ot-shaper-indic.cc:setup_syllables_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:420-426)
       0         3  hb-ot-shaper-indic.cc:update_consonant_positions_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:443-459)
       0         3  hb-ot-shaper-indic.cc:initial_reordering_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:992-1011)
       0         3  hb-ot-shaper-indic.cc:final_reordering_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1481-1495)
       0         2  hb-ot-shaper-indic.cc:is_joiner(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:80-82)
       1         3  hb-ot-shaper-indic.cc:collect_features_indic(hb_ot_shape_planner_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:241-265)
       1         3  hb-ot-shaper-indic.cc:override_features_indic(hb_ot_shape_planner_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:269-272)
       1         3  hb-ot-shaper-indic.cc:data_create_indic(hb_ot_shape_plan_t const*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:317-356)
... (6 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ot-shaper-indic.cc:preprocess_text_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1502-1506) ---
  d=2   L1504  T=1 F=0  T=3 F=0  if (!indic_plan->uniscribe_bug_compatible)
--- d=1  _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-vowel-constraints.cc:41-473) ---
  d=1   L  45  T=0 F=1  T=0 F=3  if (buffer->flags & HB_BUFFER_FLAG_DO_NOT_INSERT_DOTTED_C...
  d=1   L  58  T=1 F=0  T=3 F=0  case HB_SCRIPT_DEVANAGARI:
  d=1   L  59  T=14 F=1  T=44 F=3  for (buffer->idx = 0; buffer->idx + 1 < count && buffer->...
  d=1   L  59  T=14 F=0  T=44 F=0  for (buffer->idx = 0; buffer->idx + 1 < count && buffer->...
  d=1   L  62  T=13 F=1  T=36 F=8  switch (buffer->cur ().codepoint)
  d=1   L  64  T=1 F=13  T=6 F=38  case 0x0905u:
  d=1   L  65  T=0 F=1  T=6 F=0  switch (buffer->cur (1).codepoint)
  d=1   L  67  T=0 F=1  T=0 F=6  case 0x093Au: case 0x093Bu: case 0x093Eu: case 0x0945u:  <-- BLOCKER
  d=1   L  67  T=1 F=0  T=0 F=6  case 0x093Au: case 0x093Bu: case 0x093Eu: case 0x0945u:  <-- BLOCKER
  d=1   L  67  T=0 F=1  T=0 F=6  case 0x093Au: case 0x093Bu: case 0x093Eu: case 0x0945u:  <-- BLOCKER
  d=1   L  67  T=0 F=1  T=0 F=6  case 0x093Au: case 0x093Bu: case 0x093Eu: case 0x0945u:  <-- BLOCKER
  d=1   L  68  T=0 F=1  T=0 F=6  case 0x0946u: case 0x0949u: case 0x094Au: case 0x094Bu:
  d=1   L  68  T=0 F=1  T=0 F=6  case 0x0946u: case 0x0949u: case 0x094Au: case 0x094Bu:
  d=1   L  68  T=0 F=1  T=0 F=6  case 0x0946u: case 0x0949u: case 0x094Au: case 0x094Bu:
  d=1   L  68  T=0 F=1  T=0 F=6  case 0x0946u: case 0x0949u: case 0x094Au: case 0x094Bu:
  d=1   L  69  T=0 F=1  T=0 F=6  case 0x094Cu: case 0x094Fu: case 0x0956u: case 0x0957u:
  d=1   L  69  T=0 F=1  T=0 F=6  case 0x094Cu: case 0x094Fu: case 0x0956u: case 0x0957u:
  d=1   L  69  T=0 F=1  T=0 F=6  case 0x094Cu: case 0x094Fu: case 0x0956u: case 0x0957u:
  d=1   L  69  T=0 F=1  T=0 F=6  case 0x094Cu: case 0x094Fu: case 0x0956u: case 0x0957u:
  d=1   L  74  T=0 F=14  T=0 F=44  case 0x0906u:
  d=1   L  83  T=0 F=14  T=2 F=42  case 0x0909u:
  d=1   L  86  T=0 F=14  T=0 F=44  case 0x090Fu:
  d=1   L  94  T=0 F=14  T=0 F=44  case 0x0930u:
  d=1   L 105  T=1 F=13  T=1 F=43  if (matched) _output_with_dotted_circle (buffer);
  d=1   L 109  T=0 F=1  T=0 F=3  case HB_SCRIPT_BENGALI:
  d=1   L 130  T=0 F=1  T=0 F=3  case HB_SCRIPT_GURMUKHI:
  d=1   L 166  T=0 F=1  T=0 F=3  case HB_SCRIPT_GUJARATI:
  d=1   L 190  T=0 F=1  T=0 F=3  case HB_SCRIPT_ORIYA:
  d=1   L 208  T=0 F=1  T=0 F=3  case HB_SCRIPT_TAMIL:
  d=1   L 222  T=0 F=1  T=0 F=3  case HB_SCRIPT_TELUGU:
  d=1   L 245  T=0 F=1  T=0 F=3  case HB_SCRIPT_KANNADA:
  d=1   L 263  T=0 F=1  T=0 F=3  case HB_SCRIPT_MALAYALAM:
  d=1   L 289  T=0 F=1  T=0 F=3  case HB_SCRIPT_SINHALA:
  d=1   L 324  T=0 F=1  T=0 F=3  case HB_SCRIPT_BRAHMI:
  d=1   L 345  T=0 F=1  T=0 F=3  case HB_SCRIPT_KHOJKI:
  d=1   L 379  T=0 F=1  T=0 F=3  case HB_SCRIPT_KHUDAWADI:
  d=1   L 400  T=0 F=1  T=0 F=3  case HB_SCRIPT_TIRHUTA:
  d=1   L 426  T=0 F=1  T=0 F=3  case HB_SCRIPT_MODI:
  d=1   L 446  T=0 F=1  T=0 F=3  case HB_SCRIPT_TAKRI:
  d=1   L 469  T=0 F=1  T=0 F=3  default:

[off-chain: 87 additional divergent branches across 13 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=e064052b51cec676, size=64 bytes, fuzzer=value_profile, trial=1, discovered_at=58282s, mutation_op=CrossoverInsertMutator,ByteNegMutator,ByteIncMutator,ByteDecMutator):
  0000: 05 09 00 00 3b 09 00 00 ff 00 01 f1 f4 fc 01 5a   ....;..........Z
  0010: ff ff 00 09 00 00 e0 20 20 00 3b 09 00 00 00 09   .......  .;.....
  0020: 00 00 01 9c 0f 00 75 6e 20 00 20 20 80 00 00 20   ......un .  ... 
  0030: 00 cd cc cc 0c 18 ff ff ff 00 ff ff ff ff ff ff   ................

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=38fb33a510e8fc0d, size=81 bytes, fuzzer=naive, trial=2, discovered_at=213s, mutation_op=CrossoverInsertMutator):
  0000: 20 fe ff ff 7f 00 01 00 f3 17 00 00 00 30 66 66    ............0ff
  0010: 66 05 09 00 00 00 fe 00 df fe 98 98 98 98 98 97   f...............
  0020: 03 00 00 37 c7 17 17 17 17 17 17 17 17 17 17 f3   ...7............
  0030: 17 17 e8 17 17 17 71 1c 07 70 17 17 17 17 17 00   ......q..p......
Seed 2 (id=09f7ba78ff908139, size=13 bytes, fuzzer=naive, trial=2, discovered_at=921s, mutation_op=BytesDeleteMutator,BytesDeleteMutator,WordInterestingMutator,WordInterestingMutator,ByteFlipMutator,BytesCopyMutator):
  0000: 05 09 00 00 05 09 00 00 0e ff 00 00 04            .............
Seed 3 (id=8e6a71378ff190f4, size=84 bytes, fuzzer=naive, trial=2, discovered_at=59552s, mutation_op=BytesExpandMutator,TokenInsert,ByteDecMutator,TokenInsert,ByteIncMutator):
  0000: 03 00 01 00 90 f4 00 00 40 09 3a 3a 3a 3a 3a 3a   ........@.::::::
  0010: 3a 3a 09 19 09 09 00 00 41 09 00 00 bf 09 09 09   ::......A.......
  0020: 09 05 66 66 05 09 00 00 40 09 00 00 bf 09 09 09   ..ff....@.......
  0030: 09 05 66 66 05 09 00 00 bf 09 09 75 72 65 76 0a   ..ff.......urev.


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  05(.)x1                             20( )x1 05(.)x1 03(.)x1             PARTIAL
   0x0001  09(.)x1                             fe(.)x1 09(.)x1 00(.)x1             PARTIAL
   0x0002  00(.)x1                             ff(.)x1 00(.)x1 01(.)x1             PARTIAL
   0x0003  00(.)x1                             00(.)x2 ff(.)x1                     PARTIAL
   0x0004  3b(;)x1                             7f(.)x1 05(.)x1 90(.)x1             DIFFER
   0x0005  09(.)x1                             00(.)x1 09(.)x1 f4(.)x1             PARTIAL
   0x0006  00(.)x1                             00(.)x2 01(.)x1                     PARTIAL
   0x0008  ff(.)x1                             f3(.)x1 0e(.)x1 40(@)x1             DIFFER
   0x0009  00(.)x1                             17(.)x1 ff(.)x1 09(.)x1             DIFFER
   0x000a  01(.)x1                             00(.)x2 3a(:)x1                     DIFFER
   0x000b  f1(.)x1                             00(.)x2 3a(:)x1                     DIFFER
   0x000c  f4(.)x1                             00(.)x1 04(.)x1 3a(:)x1             DIFFER
   0x000d  fc(.)x1                             30(0)x1 3a(:)x1                     DIFFER
   0x000e  01(.)x1                             66(f)x1 3a(:)x1                     DIFFER
   0x000f  5a(Z)x1                             66(f)x1 3a(:)x1                     DIFFER
   0x0010  ff(.)x1                             66(f)x1 3a(:)x1                     DIFFER
   0x0011  ff(.)x1                             05(.)x1 3a(:)x1                     DIFFER
   0x0012  00(.)x1                             09(.)x2                             DIFFER
   0x0013  09(.)x1                             00(.)x1 19(.)x1                     DIFFER
   0x0014  00(.)x1                             00(.)x1 09(.)x1                     PARTIAL
   0x0015  00(.)x1                             00(.)x1 09(.)x1                     PARTIAL
   0x0016  e0(.)x1                             fe(.)x1 00(.)x1                     DIFFER
   0x0017  20( )x1                             00(.)x2                             DIFFER
   0x0018  20( )x1                             df(.)x1 41(A)x1                     DIFFER
   0x0019  00(.)x1                             fe(.)x1 09(.)x1                     DIFFER
   0x001a  3b(;)x1                             98(.)x1 00(.)x1                     DIFFER
   0x001b  09(.)x1                             98(.)x1 00(.)x1                     DIFFER
   0x001c  00(.)x1                             98(.)x1 bf(.)x1                     DIFFER
   0x001d  00(.)x1                             98(.)x1 09(.)x1                     DIFFER
   0x001e  00(.)x1                             98(.)x1 09(.)x1                     DIFFER
   0x001f  09(.)x1                             97(.)x1 09(.)x1                     PARTIAL
   0x0020  00(.)x1                             03(.)x1 09(.)x1                     DIFFER
   0x0021  00(.)x1                             00(.)x1 05(.)x1                     PARTIAL
   0x0022  01(.)x1                             00(.)x1 66(f)x1                     DIFFER
   0x0023  9c(.)x1                             37(7)x1 66(f)x1                     DIFFER
   0x0024  0f(.)x1                             c7(.)x1 05(.)x1                     DIFFER
   0x0025  00(.)x1                             17(.)x1 09(.)x1                     DIFFER
   0x0026  75(u)x1                             17(.)x1 00(.)x1                     DIFFER
   0x0027  6e(n)x1                             17(.)x1 00(.)x1                     DIFFER
   0x0028  20( )x1                             17(.)x1 40(@)x1                     DIFFER
   ... (23 more divergent offsets)
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
  prompts_b/harfbuzz_6006.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6006,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>naive (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6006 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6006 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6006 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).