==== BLOCKER ====
Target: harfbuzz
Branch ID: 6025
Location: /src/harfbuzz/src/hb-ot-shaper-vowel-constraints.cc:94:4
Enclosing function: _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)
Source line: 	  case 0x0930u:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            4        6          0  REFERENCE
cmplog                           2        8          0  loser (value_profile vs value_profile_cmplog)
value_profile                    8        2          0  REFERENCE
value_profile_cmplog            10        0          0  winner (value_profile vs cmplog)
naive_ctx                       10        0          0  REFERENCE
naive_ngram4                     5        5          0  REFERENCE
mopt                             4        6          0  REFERENCE
minimizer                       10        0          0  REFERENCE
fast                             7        3          0  REFERENCE
grimoire                         6        4          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=2.20h  loser=18.80h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.80  dur_div=16.60h  hit_div=2
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/6025/{W,L}/branch_coverage_show.txt

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
[L]    64  	  case 0x0905u:
[L]    65  	    switch (buffer->cur (1).codepoint)
[L]    66  	    {
[ ]    67  	      case 0x093Au: case 0x093Bu: case 0x093Eu: case 0x0945u:
[ ]    68  	      case 0x0946u: case 0x0949u: case 0x094Au: case 0x094Bu:
[L]    69  	      case 0x094Cu: case 0x094Fu: case 0x0956u: case 0x0957u:
[L]    70  		matched = true;
[L]    71  		break;
[L]    72  	    }
[L]    73  	    break;
[L]    74  	  case 0x0906u:
[L]    75  	    switch (buffer->cur (1).codepoint)
[L]    76  	    {
[ ]    77  	      case 0x093Au: case 0x0945u: case 0x0946u: case 0x0947u:
[ ]    78  	      case 0x0948u:
[ ]    79  		matched = true;
[ ]    80  		break;
[L]    81  	    }
[L]    82  	    break;
[L]    83  	  case 0x0909u:
[ ]    84  	    matched = 0x0941u == buffer->cur (1).codepoint;
[ ]    85  	    break;
[L]    86  	  case 0x090Fu:
[L]    87  	    switch (buffer->cur (1).codepoint)
[L]    88  	    {
[ ]    89  	      case 0x0945u: case 0x0946u: case 0x0947u:
[ ]    90  		matched = true;
[ ]    91  		break;
[L]    92  	    }
[L]    93  	    break;
[B]    94  	  case 0x0930u: <-- BLOCKER
[W]    95  	    if (0x094Du == buffer->cur (1).codepoint &&
[W]    96  		buffer->idx + 2 < count &&
[W]    97  		0x0907u == buffer->cur (2).codepoint)
[ ]    98  	    {
[ ]    99  	      (void) buffer->next_glyph ();
[ ]   100  	      matched = true;
[ ]   101  	    }
[W]   102  	    break;
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
      16       161  hb-ot-shaper-indic.cc:set_indic_properties(hb_glyph_info_t&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:44-50)
      15       154  hb-ot-shaper-indic.cc:initial_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:968-986)
      15       154  hb-ot-shaper-indic.cc:final_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1017-1474)
      16       147  hb-ot-shaper-indic.cc:decompose_indic(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int*, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1513-1539)
       4        62  hb-ot-shaper-indic.cc:is_one_of(hb_glyph_info_t const&, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:55-59)
       5        50  hb_indic_would_substitute_feature_t::init(hb_ot_map_t const*, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:93-97)
       3        42  hb-ot-shaper-indic.cc:is_consonant(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:72-74)
       1        28  hb-ot-shaper-indic.cc:initial_reordering_consonant_syllable(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:470-939)
       1        27  hb-ot-shaper-indic.cc:compose_indic(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1546-1555)
       0        20  hb-ot-shaper-indic.cc:initial_reordering_standalone_cluster(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:946-961)
       1        10  hb-ot-shaper-indic.cc:collect_features_indic(hb_ot_shape_planner_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:241-265)
       1        10  hb-ot-shaper-indic.cc:override_features_indic(hb_ot_shape_planner_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:269-272)
       1        10  indic_shape_plan_t::load_virama_glyph(hb_font_t*, unsigned int*) const  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:278-294)
       1        10  hb-ot-shaper-indic.cc:data_create_indic(hb_ot_shape_plan_t const*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:317-356)
       1        10  hb-ot-shaper-indic.cc:data_destroy_indic(void*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:360-362)
... (11 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ot-shaper-indic.cc:preprocess_text_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1502-1506) ---
  d=2   L1504  T=1 F=0  T=10 F=0  if (!indic_plan->uniscribe_bug_compatible)
--- d=1  _hb_preprocess_text_vowel_constraints(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-vowel-constraints.cc:41-473) ---
  d=1   L  45  T=0 F=1  T=0 F=10  if (buffer->flags & HB_BUFFER_FLAG_DO_NOT_INSERT_DOTTED_C...
  d=1   L  58  T=1 F=0  T=10 F=0  case HB_SCRIPT_DEVANAGARI:
  d=1   L  59  T=15 F=1  T=149 F=10  for (buffer->idx = 0; buffer->idx + 1 < count && buffer->...
  d=1   L  59  T=15 F=0  T=149 F=0  for (buffer->idx = 0; buffer->idx + 1 < count && buffer->...
  d=1   L  62  T=14 F=1  T=146 F=3  switch (buffer->cur ().codepoint)
  d=1   L  64  T=0 F=15  T=1 F=148  case 0x0905u:
  d=1   L  65  T=0 F=0  T=0 F=1  switch (buffer->cur (1).codepoint)
  d=1   L  67  T=0 F=0  T=0 F=1  case 0x093Au: case 0x093Bu: case 0x093Eu: case 0x0945u:
  d=1   L  67  T=0 F=0  T=0 F=1  case 0x093Au: case 0x093Bu: case 0x093Eu: case 0x0945u:
  d=1   L  67  T=0 F=0  T=0 F=1  case 0x093Au: case 0x093Bu: case 0x093Eu: case 0x0945u:
  d=1   L  67  T=0 F=0  T=0 F=1  case 0x093Au: case 0x093Bu: case 0x093Eu: case 0x0945u:
  d=1   L  68  T=0 F=0  T=0 F=1  case 0x0946u: case 0x0949u: case 0x094Au: case 0x094Bu:
  d=1   L  68  T=0 F=0  T=0 F=1  case 0x0946u: case 0x0949u: case 0x094Au: case 0x094Bu:
  d=1   L  68  T=0 F=0  T=0 F=1  case 0x0946u: case 0x0949u: case 0x094Au: case 0x094Bu:
  d=1   L  68  T=0 F=0  T=0 F=1  case 0x0946u: case 0x0949u: case 0x094Au: case 0x094Bu:
  d=1   L  69  T=0 F=0  T=0 F=1  case 0x094Cu: case 0x094Fu: case 0x0956u: case 0x0957u:
  d=1   L  69  T=0 F=0  T=1 F=0  case 0x094Cu: case 0x094Fu: case 0x0956u: case 0x0957u:
  d=1   L  69  T=0 F=0  T=0 F=1  case 0x094Cu: case 0x094Fu: case 0x0956u: case 0x0957u:
  d=1   L  69  T=0 F=0  T=0 F=1  case 0x094Cu: case 0x094Fu: case 0x0956u: case 0x0957u:
  d=1   L  74  T=0 F=15  T=1 F=148  case 0x0906u:
  d=1   L  75  T=0 F=0  T=1 F=0  switch (buffer->cur (1).codepoint)
  d=1   L  77  T=0 F=0  T=0 F=1  case 0x093Au: case 0x0945u: case 0x0946u: case 0x0947u:
  d=1   L  77  T=0 F=0  T=0 F=1  case 0x093Au: case 0x0945u: case 0x0946u: case 0x0947u:
  d=1   L  77  T=0 F=0  T=0 F=1  case 0x093Au: case 0x0945u: case 0x0946u: case 0x0947u:
  d=1   L  77  T=0 F=0  T=0 F=1  case 0x093Au: case 0x0945u: case 0x0946u: case 0x0947u:
  d=1   L  78  T=0 F=0  T=0 F=1  case 0x0948u:
  d=1   L  83  T=0 F=15  T=0 F=149  case 0x0909u:
  d=1   L  86  T=0 F=15  T=1 F=148  case 0x090Fu:
  d=1   L  87  T=0 F=0  T=1 F=0  switch (buffer->cur (1).codepoint)
  d=1   L  89  T=0 F=0  T=0 F=1  case 0x0945u: case 0x0946u: case 0x0947u:
  d=1   L  89  T=0 F=0  T=0 F=1  case 0x0945u: case 0x0946u: case 0x0947u:
  d=1   L  89  T=0 F=0  T=0 F=1  case 0x0945u: case 0x0946u: case 0x0947u:
  d=1   L  94  T=1 F=14  T=0 F=149  case 0x0930u:  <-- BLOCKER
  d=1   L  95  T=1 F=0  T=0 F=0  if (0x094Du == buffer->cur (1).codepoint &&
  d=1   L  96  T=1 F=0  T=0 F=0  buffer->idx + 2 < count &&
  d=1   L  97  T=0 F=1  T=0 F=0  0x0907u == buffer->cur (2).codepoint)
  d=1   L 105  T=0 F=15  T=1 F=148  if (matched) _output_with_dotted_circle (buffer);
  d=1   L 109  T=0 F=1  T=0 F=10  case HB_SCRIPT_BENGALI:
  d=1   L 130  T=0 F=1  T=0 F=10  case HB_SCRIPT_GURMUKHI:
  d=1   L 166  T=0 F=1  T=0 F=10  case HB_SCRIPT_GUJARATI:
  d=1   L 190  T=0 F=1  T=0 F=10  case HB_SCRIPT_ORIYA:
  d=1   L 208  T=0 F=1  T=0 F=10  case HB_SCRIPT_TAMIL:
  d=1   L 222  T=0 F=1  T=0 F=10  case HB_SCRIPT_TELUGU:
  d=1   L 245  T=0 F=1  T=0 F=10  case HB_SCRIPT_KANNADA:
  d=1   L 263  T=0 F=1  T=0 F=10  case HB_SCRIPT_MALAYALAM:
  d=1   L 289  T=0 F=1  T=0 F=10  case HB_SCRIPT_SINHALA:
  d=1   L 324  T=0 F=1  T=0 F=10  case HB_SCRIPT_BRAHMI:
  d=1   L 345  T=0 F=1  T=0 F=10  case HB_SCRIPT_KHOJKI:
  d=1   L 379  T=0 F=1  T=0 F=10  case HB_SCRIPT_KHUDAWADI:
  d=1   L 400  T=0 F=1  T=0 F=10  case HB_SCRIPT_TIRHUTA:
  d=1   L 426  T=0 F=1  T=0 F=10  case HB_SCRIPT_MODI:
  d=1   L 446  T=0 F=1  T=0 F=10  case HB_SCRIPT_TAKRI:
  d=1   L 469  T=0 F=1  T=0 F=10  default:

[off-chain: 93 additional divergent branches across 14 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=b59f70477fb60424, size=28 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=72297s, mutation_op=DwordAddMutator,WordAddMutator,QwordAddMutator,CrossoverReplaceMutator):
  0000: 30 09 00 00 4d 09 00 00 06 00 00 00 10 00 10 34   0...M..........4
  0010: 34 3c c9 4d 34 34 c0 52 4d 34 34 0c               4<.M44.RM44.

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0cc973685868d14f, size=55 bytes, fuzzer=cmplog, trial=2, discovered_at=18s, mutation_op=CrossoverInsertMutator,DwordInterestingMutator):
  0000: 19 09 00 00 72 1b 1b 1b 1b 00 00 40 20 20 20 6e   ....r......@   n
  0010: 20 20 20 20 20 00 ff ff ff ff 68 61 6e 74 2d 6d        .....hant-m
  0020: 6f 00 00 1a 20 20 00 04 00 01 00 1b 1b 1b 1b 1b   o...  ..........
  0030: 1b 1b 03 00 40 20 00                              ....@ .
Seed 2 (id=00f73a27abba075d, size=58 bytes, fuzzer=cmplog, trial=2, discovered_at=650s, mutation_op=DwordAddMutator,BytesExpandMutator):
  0000: 00 00 00 00 00 00 00 bf 17 09 00 00 bf 17 00 00   ................
  0010: 17 00 00 bf 17 09 00 00 bf 17 00 00 17 00 00 00   ................
  0020: 00 00 00 00 02 e1 0e 00 00 00 00 00 21 00 62 00   ............!.b.
  0030: 11 20 00 00 ef 17 00 00 ef 17                     . ........
Seed 3 (id=0b9c9d613fc4f47d, size=64 bytes, fuzzer=cmplog, trial=2, discovered_at=888s, mutation_op=WordInterestingMutator,DwordAddMutator,BytesInsertMutator,ByteAddMutator,ByteRandMutator,ByteDecMutator):
  0000: 00 fe 00 00 00 09 2c 00 00 01 00 02 00 09 00 00   ......,.........
  0010: 00 fe 00 00 00 09 00 00 00 fe 00 02 00 09 00 00   ................
  0020: 00 fe ff 00 00 00 00 00 00 00 09 00 00 09 00 00   ................
  0030: 00 fe 19 00 e7 00 fc ff ff 00 00 00 00 09 00 00   ................
Seed 4 (id=158d79bf644e1c91, size=62 bytes, fuzzer=cmplog, trial=2, discovered_at=925s, mutation_op=TokenInsert,DwordInterestingMutator):
  0000: 00 73 6e 2d 68 61 6e 74 00 00 00 00 02 00 09 c4   .sn-hant........
  0010: 16 09 00 00 bf 17 00 00 00 09 bf 16 09 ff 00 00   ................
  0020: 00 00 80 00 00 00 00 00 ff 20 01 6f 9c 65 93 01   ......... .o.e..
  0030: 00 00 02 00 80 20 00 00 f0 17 7a 68 2d 00         ..... ....zh-.
Seed 5 (id=09e6802506d6d807, size=119 bytes, fuzzer=cmplog, trial=2, discovered_at=1161s, mutation_op=TokenInsert,BitFlipMutator,CrossoverReplaceMutator,WordAddMutator):
  0000: 00 00 fb 6a 79 2d 68 61 6e 74 00 20 51 00 b6 22   ...jy-hant. Q.."
  0010: 00 64 10 00 00 12 06 00 00 ff 3f 00 72 6e 20 18   .d........?.rn .
  0020: 00 00 ff 20 0c 20 75 6e 69 00 20 00 00 72 0c 00   ... . uni. ..r..
  0030: 0e 0d 00 00 46 0d 00 00 09 00 00 25 0e 0d 00 00   ....F......%....


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  30(0)x1                             00(.)x7 19(.)x1 09(.)x1 e7(.)x1     DIFFER
   0x0001  09(.)x1                             01(.)x3 09(.)x2 00(.)x2 fe(.)x1 +2u  PARTIAL
   0x0002  00(.)x1                             00(.)x6 6e(n)x1 fb(.)x1 09(.)x1 +1u  PARTIAL
   0x0003  00(.)x1                             00(.)x7 2d(-)x1 6a(j)x1 20( )x1     PARTIAL
   0x0004  4d(M)x1                             00(.)x6 72(r)x1 68(h)x1 79(y)x1 +1u  DIFFER
   0x0005  09(.)x1                             01(.)x2 1b(.)x1 00(.)x1 09(.)x1 +5u  PARTIAL
   0x0006  00(.)x1                             00(.)x4 1b(.)x1 2c(,)x1 6e(n)x1 +3u  PARTIAL
   0x0007  00(.)x1                             00(.)x2 1b(.)x1 bf(.)x1 74(t)x1 +5u  PARTIAL
   0x0008  06(.)x1                             00(.)x5 1b(.)x1 17(.)x1 6e(n)x1 +2u  DIFFER
   0x0009  00(.)x1                             00(.)x3 09(.)x2 01(.)x1 74(t)x1 +3u  PARTIAL
   0x000a  00(.)x1                             00(.)x6 df(.)x3 59(Y)x1             PARTIAL
   0x000b  00(.)x1                             20( )x4 00(.)x3 40(@)x1 02(.)x1 +1u  PARTIAL
   0x000c  10(.)x1                             47(G)x3 20( )x1 bf(.)x1 00(.)x1 +4u  DIFFER
   0x000d  00(.)x1                             50(P)x3 00(.)x2 20( )x1 17(.)x1 +3u  PARTIAL
   0x000e  10(.)x1                             4f(O)x3 00(.)x2 20( )x1 09(.)x1 +3u  DIFFER
   0x000f  34(4)x1                             53(S)x3 00(.)x2 6e(n)x1 c4(.)x1 +3u  DIFFER
   0x0010  34(4)x1                             00(.)x4 20( )x1 17(.)x1 16(.)x1 +3u  DIFFER
   0x0011  3c(<)x1                             00(.)x3 fe(.)x2 20( )x1 09(.)x1 +3u  DIFFER
   0x0012  c9(.)x1                             00(.)x4 20( )x1 10(.)x1 22(")x1 +3u  DIFFER
   0x0013  4d(M)x1                             00(.)x6 20( )x1 bf(.)x1 09(.)x1 +1u  DIFFER
   0x0014  34(4)x1                             00(.)x6 20( )x1 17(.)x1 bf(.)x1 +1u  DIFFER
   0x0015  34(4)x1                             00(.)x5 09(.)x3 17(.)x1 12(.)x1     DIFFER
   0x0016  c0(.)x1                             00(.)x8 ff(.)x1 06(.)x1             DIFFER
   0x0017  52(R)x1                             00(.)x7 ff(.)x1 fe(.)x1 10(.)x1     DIFFER
   0x0018  4d(M)x1                             00(.)x4 ff(.)x1 bf(.)x1 0b(.)x1 +3u  DIFFER
   0x0019  34(4)x1                             ff(.)x2 fe(.)x2 00(.)x2 17(.)x1 +3u  DIFFER
   0x001a  34(4)x1                             00(.)x6 68(h)x1 bf(.)x1 3f(?)x1 +1u  DIFFER
   0x001b  0c(.)x1                             00(.)x3 02(.)x2 f8(.)x2 61(a)x1 +2u  DIFFER
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
  prompts_b/harfbuzz_6025.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6025,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6025 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6025 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6025 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).