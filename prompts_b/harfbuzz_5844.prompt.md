==== BLOCKER ====
Target: harfbuzz
Branch ID: 5844
Location: /src/harfbuzz/src/hb-ot-shaper-indic.cc:678:11
Enclosing function: hb-ot-shaper-indic.cc:initial_reordering_consonant_syllable(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)
Source line:       if (info[i].indic_category() == I_Cat(H))
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           1        9          0  loser (I2S vs naive); loser (value_profile vs value_profile_cmplog)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             9        1          0  winner (value_profile vs cmplog)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             9        1          0  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=5.10h  loser=22.20h
  avg hitcount on branch: winner=34  loser=0
  prob_div=0.90  dur_div=17.10h  hit_div=34
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=4.00h  loser=22.20h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.80  dur_div=18.20h  hit_div=2
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5844/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-indic.cc:initial_reordering_consonant_syllable(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) (/src/harfbuzz/src/hb-ot-shaper-indic.cc:470-939) ---
[ ]   468  				       hb_buffer_t *buffer,
[ ]   469  				       unsigned int start, unsigned int end)
[B]   470  {
[B]   471    const indic_shape_plan_t *indic_plan = (const indic_shape_plan_t *) plan->data;
[B]   472    hb_glyph_info_t *info = buffer->info;
[ ]   473  
[ ]   474    /* https://github.com/harfbuzz/harfbuzz/issues/435#issuecomment-335560167
[ ]   475     * // For compatibility with legacy usage in Kannada,
[ ]   476     * // Ra+h+ZWJ must behave like Ra+ZWJ+h...
[ ]   477     */
[B]   478    if (buffer->props.script == HB_SCRIPT_KANNADA &&
[B]   479        start + 3 <= end &&
[B]   480        is_one_of (info[start  ], FLAG (I_Cat(Ra))) &&
[B]   481        is_one_of (info[start+1], FLAG (I_Cat(H))) &&
[B]   482        is_one_of (info[start+2], FLAG (I_Cat(ZWJ))))
[ ]   483    {
[ ]   484      buffer->merge_clusters (start+1, start+3);
[ ]   485      hb_glyph_info_t tmp = info[start+1];
[ ]   486      info[start+1] = info[start+2];
[ ]   487      info[start+2] = tmp;
[ ]   488    }
[ ]   489  
[ ]   490    /* 1. Find base consonant:
[ ]   491     *
[ ]   492     * The shaping engine finds the base consonant of the syllable, using the
[ ]   493     * following algorithm: starting from the end of the syllable, move backwards
[ ]   494     * until a consonant is found that does not have a below-base or post-base
[ ]   495     * form (post-base forms have to follow below-base forms), or that is not a
[ ]   496     * pre-base-reordering Ra, or arrive at the first consonant. The consonant
[ ]   497     * stopped at will be the base.
[ ]   498     *
[ ]   499     *   o If the syllable starts with Ra + Halant (in a script that has Reph)
[ ]   500     *     and has more than one consonant, Ra is excluded from candidates for
[ ]   501     *     base consonants.
[ ]   502     */
[ ]   503  
[B]   504    unsigned int base = end;
[B]   505    bool has_reph = false;
[ ]   506  
[B]   507    {
[ ]   508      /* -> If the syllable starts with Ra + Halant (in a script that has Reph)
[ ]   509       *    and has more than one consonant, Ra is excluded from candidates for
[ ]   510       *    base consonants. */
[B]   511      unsigned int limit = start;
[B]   512      if (indic_plan->mask_array[INDIC_RPHF] &&
[B]   513  	start + 3 <= end &&
[B]   514  	(
[ ]   515  	 (indic_plan->config->reph_mode == REPH_MODE_IMPLICIT && !is_joiner (info[start + 2])) ||
[ ]   516  	 (indic_plan->config->reph_mode == REPH_MODE_EXPLICIT && info[start + 2].indic_category() == I_Cat(ZWJ))
[ ]   517  	))
[ ]   518      {
[ ]   519        /* See if it matches the 'rphf' feature. */
[ ]   520        hb_codepoint_t glyphs[3] = {info[start].codepoint,
[ ]   521  				  info[start + 1].codepoint,
[ ]   522  				  indic_plan->config->reph_mode == REPH_MODE_EXPLICIT ?
[ ]   523  				    info[start + 2].codepoint : 0};
[ ]   524        if (indic_plan->rphf.would_substitute (glyphs, 2, face) ||
[ ]   525  	  (indic_plan->config->reph_mode == REPH_MODE_EXPLICIT &&
[ ]   526  	   indic_plan->rphf.would_substitute (glyphs, 3, face)))
[ ]   527        {
[ ]   528  	limit += 2;
[ ]   529  	while (limit < end && is_joiner (info[limit]))
[ ]   530  	  limit++;
[ ]   531  	base = start;
[ ]   532  	has_reph = true;
[ ]   533        }
[B]   534      } else if (indic_plan->config->reph_mode == REPH_MODE_LOG_REPHA && info[start].indic_category() == I_Cat(Repha))
[ ]   535      {
[ ]   536  	limit += 1;
[ ]   537  	while (limit < end && is_joiner (info[limit]))
[ ]   538  	  limit++;
[ ]   539  	base = start;
[ ]   540  	has_reph = true;
[ ]   541      }
[ ]   542  
[B]   543      {
[ ]   544        /* -> starting from the end of the syllable, move backwards */
[B]   545        unsigned int i = end;
[B]   546        bool seen_below = false;
[B]   547        do {
[B]   548  	i--;
[ ]   549  	/* -> until a consonant is found */
[B]   550  	if (is_consonant (info[i]))
[B]   551  	{
[ ]   552  	  /* -> that does not have a below-base or post-base form
[ ]   553  	   * (post-base forms have to follow below-base forms), */
[B]   554  	  if (info[i].indic_position() != POS_BELOW_C &&
[B]   555  	      (info[i].indic_position() != POS_POST_C || seen_below))
[B]   556  	  {
[B]   557  	    base = i;
[B]   558  	    break;
[B]   559  	  }
[ ]   560  	  if (info[i].indic_position() == POS_BELOW_C)
[ ]   561  	    seen_below = true;
[ ]   562  
[ ]   563  	  /* -> or that is not a pre-base-reordering Ra,
[ ]   564  	   *
[ ]   565  	   * IMPLEMENTATION NOTES:
[ ]   566  	   *
[ ]   567  	   * Our pre-base-reordering Ra's are marked POS_POST_C, so will be skipped
[ ]   568  	   * by the logic above already.
[ ]   569  	   */
[ ]   570  
[ ]   571  	  /* -> or arrive at the first consonant. The consonant stopped at will
[ ]   572  	   * be the base. */
[ ]   573  	  base = i;
[ ]   574  	}
[B]   575  	else
[B]   576  	{
[ ]   577  	  /* A ZWJ after a Halant stops the base search, and requests an explicit
[ ]   578  	   * half form.
[ ]   579  	   * A ZWJ before a Halant, requests a subjoined form instead, and hence
[ ]   580  	   * search continues.  This is particularly important for Bengali
[ ]   581  	   * sequence Ra,H,Ya that should form Ya-Phalaa by subjoining Ya. */
[B]   582  	  if (start < i &&
[B]   583  	      info[i].indic_category() == I_Cat(ZWJ) &&
[B]   584  	      info[i - 1].indic_category() == I_Cat(H))
[ ]   585  	    break;
[B]   586  	}
[B]   587        } while (i > limit);
[B]   588      }
[ ]   589  
[ ]   590      /* -> If the syllable starts with Ra + Halant (in a script that has Reph)
[ ]   591       *    and has more than one consonant, Ra is excluded from candidates for
[ ]   592       *    base consonants.
[ ]   593       *
[ ]   594       *  Only do this for unforced Reph. (ie. not for Ra,H,ZWJ. */
[B]   595      if (has_reph && base == start && limit - base <= 2) {
[ ]   596        /* Have no other consonant, so Reph is not formed and Ra becomes base. */
[ ]   597        has_reph = false;
[ ]   598      }
[B]   599    }
[ ]   600  
[ ]   601  
[ ]   602    /* 2. Decompose and reorder Matras:
[ ]   603     *
[ ]   604     * Each matra and any syllable modifier sign in the syllable are moved to the
[ ]   605     * appropriate position relative to the consonant(s) in the syllable. The
[ ]   606     * shaping engine decomposes two- or three-part matras into their constituent
[ ]   607     * parts before any repositioning. Matra characters are classified by which
[ ]   608     * consonant in a conjunct they have affinity for and are reordered to the
[ ]   609     * following positions:
[ ]   610     *
[ ]   611     *   o Before first half form in the syllable
[ ]   612     *   o After subjoined consonants
[ ]   613     *   o After post-form consonant
[ ]   614     *   o After main consonant (for above marks)
[ ]   615     *
[ ]   616     * IMPLEMENTATION NOTES:
[ ]   617     *
[ ]   618     * The normalize() routine has already decomposed matras for us, so we don't
[ ]   619     * need to worry about that.
[ ]   620     */
[ ]   621  
[ ]   622  
[ ]   623    /* 3.  Reorder marks to canonical order:
[ ]   624     *
[ ]   625     * Adjacent nukta and halant or nukta and vedic sign are always repositioned
[ ]   626     * if necessary, so that the nukta is first.
[ ]   627     *
[ ]   628     * IMPLEMENTATION NOTES:
[ ]   629     *
[ ]   630     * We don't need to do this: the normalize() routine already did this for us.
[ ]   631     */
[ ]   632  
[ ]   633  
[ ]   634    /* Reorder characters */
[ ]   635  
[B]   636    for (unsigned int i = start; i < base; i++)
[B]   637      info[i].indic_position() = hb_min (POS_PRE_C, (indic_position_t) info[i].indic_position());
[ ]   638  
[B]   639    if (base < end)
[B]   640      info[base].indic_position() = POS_BASE_C;
[ ]   641  
[ ]   642    /* Handle beginning Ra */
[B]   643    if (has_reph)
[ ]   644      info[start].indic_position() = POS_RA_TO_BECOME_REPH;
[ ]   645  
[ ]   646    /* For old-style Indic script tags, move the first post-base Halant after
[ ]   647     * last consonant.
[ ]   648     *
[ ]   649     * Reports suggest that in some scripts Uniscribe does this only if there
[ ]   650     * is *not* a Halant after last consonant already.  We know that is the
[ ]   651     * case for Kannada, while it reorders unconditionally in other scripts,
[ ]   652     * eg. Malayalam, Bengali, and Devanagari.  We don't currently know about
[ ]   653     * other scripts, so we block Kannada.
[ ]   654     *
[ ]   655     * Kannada test case:
[ ]   656     * U+0C9A,U+0CCD,U+0C9A,U+0CCD
[ ]   657     * With some versions of Lohit Kannada.
[ ]   658     * https://bugs.freedesktop.org/show_bug.cgi?id=59118
[ ]   659     *
[ ]   660     * Malayalam test case:
[ ]   661     * U+0D38,U+0D4D,U+0D31,U+0D4D,U+0D31,U+0D4D
[ ]   662     * With lohit-ttf-20121122/Lohit-Malayalam.ttf
[ ]   663     *
[ ]   664     * Bengali test case:
[ ]   665     * U+0998,U+09CD,U+09AF,U+09CD
[ ]   666     * With Windows XP vrinda.ttf
[ ]   667     * https://github.com/harfbuzz/harfbuzz/issues/1073
[ ]   668     *
[ ]   669     * Devanagari test case:
[ ]   670     * U+091F,U+094D,U+0930,U+094D
[ ]   671     * With chandas.ttf
[ ]   672     * https://github.com/harfbuzz/harfbuzz/issues/1071
[ ]   673     */
[B]   674    if (indic_plan->is_old_spec)
[B]   675    {
[B]   676      bool disallow_double_halants = buffer->props.script == HB_SCRIPT_KANNADA;
[B]   677      for (unsigned int i = base + 1; i < end; i++)
[B]   678        if (info[i].indic_category() == I_Cat(H)) <-- BLOCKER
[W]   679        {
[W]   680  	unsigned int j;
[W]   681  	for (j = end - 1; j > i; j--)
[W]   682  	  if (is_consonant (info[j]) ||
[W]   683  	      (disallow_double_halants && info[j].indic_category() == I_Cat(H)))
[ ]   684  	    break;
[W]   685  	if (info[j].indic_category() != I_Cat(H) && j > i) {
[ ]   686  	  /* Move Halant to after last consonant. */
[ ]   687  	  hb_glyph_info_t t = info[i];
[ ]   688  	  memmove (&info[i], &info[i + 1], (j - i) * sizeof (info[0]));
[ ]   689  	  info[j] = t;
[ ]   690  	}
[W]   691  	break;
[W]   692        }
[B]   693    }
[ ]   694  
[ ]   695    /* Attach misc marks to previous char to move with them. */
[B]   696    {
[B]   697      indic_position_t last_pos = POS_START;
[B]   698      for (unsigned int i = start; i < end; i++)
[B]   699      {
[B]   700        if ((FLAG_UNSAFE (info[i].indic_category()) & (JOINER_FLAGS | FLAG (I_Cat(N)) | FLAG (I_Cat(RS)) | FLAG (I_Cat(CM)) | FLAG (I_Cat(H)))))
[B]   701        {
[B]   702  	info[i].indic_position() = last_pos;
[B]   703  	if (unlikely (info[i].indic_category() == I_Cat(H) &&
[B]   704  		      info[i].indic_position() == POS_PRE_M))
[ ]   705  	{
[ ]   706  	  /*
[ ]   707  	   * Uniscribe doesn't move the Halant with Left Matra.
[ ]   708  	   * TEST: U+092B,U+093F,U+094D
[ ]   709  	   * We follow.
[ ]   710  	   */
[ ]   711  	  for (unsigned int j = i; j > start; j--)
[ ]   712  	    if (info[j - 1].indic_position() != POS_PRE_M) {
[ ]   713  	      info[i].indic_position() = info[j - 1].indic_position();
[ ]   714  	      break;
[ ]   715  	    }
[ ]   716  	}
[B]   717        } else if (info[i].indic_position() != POS_SMVD) {
[B]   718  	if (info[i].indic_category() == I_Cat(MPst) &&
[B]   719  	    i > start && info[i - 1].indic_category() == I_Cat(SM))
[ ]   720  	  info[i - 1].indic_position() = info[i].indic_position();
[B]   721  	last_pos = (indic_position_t) info[i].indic_position();
[B]   722        }
[B]   723      }
[B]   724    }
[ ]   725    /* For post-base consonants let them own anything before them
[ ]   726     * since the last consonant or matra. */
[B]   727    {
[B]   728      unsigned int last = base;
[B]   729      for (unsigned int i = base + 1; i < end; i++)
[B]   730        if (is_consonant (info[i]))
[ ]   731        {
[ ]   732  	for (unsigned int j = last + 1; j < i; j++)
[ ]   733  	  if (info[j].indic_position() < POS_SMVD)
[ ]   734  	    info[j].indic_position() = info[i].indic_position();
[ ]   735  	last = i;
[B]   736        } else if (FLAG_UNSAFE (info[i].indic_category()) & (FLAG (I_Cat(M)) | FLAG (I_Cat(MPst))))
[L]   737  	last = i;
[B]   738    }
[ ]   739  
[ ]   740  
[B]   741    {
[ ]   742      /* Use syllable() for sort accounting temporarily. */
[B]   743      unsigned int syllable = info[start].syllable();
[B]   744      for (unsigned int i = start; i < end; i++)
[B]   745        info[i].syllable() = i - start;
[ ]   746  
[ ]   747      /* Sit tight, rock 'n roll! */
[B]   748      hb_stable_sort (info + start, end - start, compare_indic_order);
[ ]   749  
[ ]   750      /* Find base again; also flip left-matra sequence. */
[B]   751      unsigned first_left_matra = end;
[B]   752      unsigned last_left_matra = end;
[B]   753      base = end;
[B]   754      for (unsigned int i = start; i < end; i++)
[B]   755      {
[B]   756        if (info[i].indic_position() == POS_BASE_C)
[B]   757        {
[B]   758  	base = i;
[B]   759  	break;
[B]   760        }
[B]   761        else if (info[i].indic_position() == POS_PRE_M)
[L]   762        {
[L]   763          if (first_left_matra == end)
[L]   764  	  first_left_matra = i;
[L]   765  	last_left_matra = i;
[L]   766        }
[B]   767      }
[ ]   768      /* https://github.com/harfbuzz/harfbuzz/issues/3863 */
[B]   769      if (first_left_matra < last_left_matra)
[L]   770      {
[ ]   771        /* No need to merge clusters, handled later. */
[L]   772        buffer->reverse_range (first_left_matra, last_left_matra + 1);
[ ]   773        /* Reverse back nuktas, etc. */
[L]   774        unsigned i = first_left_matra;
[L]   775        for (unsigned j = i; j <= last_left_matra; j++)
[L]   776  	if (FLAG_UNSAFE (info[j].indic_category()) & (FLAG (I_Cat(M)) | FLAG (I_Cat(MPst))))
[L]   777  	{
[L]   778  	  buffer->reverse_range (i, j + 1);
[L]   779  	  i = j + 1;
[L]   780  	}
[L]   781      }
[ ]   782  
[ ]   783      /* Things are out-of-control for post base positions, they may shuffle
[ ]   784       * around like crazy.  In old-spec mode, we move halants around, so in
[ ]   785       * that case merge all clusters after base.  Otherwise, check the sort
[ ]   786       * order and merge as needed.
[ ]   787       * For pre-base stuff, we handle cluster issues in final reordering.
[ ]   788       *
[ ]   789       * We could use buffer->sort() for this, if there was no special
[ ]   790       * reordering of pre-base stuff happening later...
[ ]   791       * We don't want to merge_clusters all of that, which buffer->sort()
[ ]   792       * would.  Here's a concrete example:
[ ]   793       *
[ ]   794       * Assume there's a pre-base consonant and explicit Halant before base,
[ ]   795       * followed by a prebase-reordering (left) Matra:
[ ]   796       *
[ ]   797       *   C,H,ZWNJ,B,M
[ ]   798       *
[ ]   799       * At this point in reordering we would have:
[ ]   800       *
[ ]   801       *   M,C,H,ZWNJ,B
[ ]   802       *
[ ]   803       * whereas in final reordering we will bring the Matra closer to Base:
[ ]   804       *
[ ]   805       *   C,H,ZWNJ,M,B
[ ]   806       *
[ ]   807       * That's why we don't want to merge-clusters anything before the Base
[ ]   808       * at this point.  But if something moved from after Base to before it,
[ ]   809       * we should merge clusters from base to them.  In final-reordering, we
[ ]   810       * only move things around before base, and merge-clusters up to base.
[ ]   811       * These two merge-clusters from the two sides of base will interlock
[ ]   812       * to merge things correctly.  See:
[ ]   813       * https://github.com/harfbuzz/harfbuzz/issues/2272
[ ]   814       */
[B]   815      if (indic_plan->is_old_spec || end - start > 127)
[B]   816        buffer->merge_clusters (base, end);
[ ]   817      else
[ ]   818      {
[ ]   819        /* Note!  syllable() is a one-byte field. */
[ ]   820        for (unsigned int i = base; i < end; i++)
[ ]   821  	if (info[i].syllable() != 255)
[ ]   822  	{
[ ]   823  	  unsigned int min = i;
[ ]   824  	  unsigned int max = i;
[ ]   825  	  unsigned int j = start + info[i].syllable();
[ ]   826  	  while (j != i)
[ ]   827  	  {
[ ]   828  	    min = hb_min (min, j);
[ ]   829  	    max = hb_max (max, j);
[ ]   830  	    unsigned int next = start + info[j].syllable();
[ ]   831  	    info[j].syllable() = 255; /* So we don't process j later again. */
[ ]   832  	    j = next;
[ ]   833  	  }
[ ]   834  	  buffer->merge_clusters (hb_max (base, min), max + 1);
[ ]   835  	}
[ ]   836      }
[ ]   837  
[ ]   838      /* Put syllable back in. */
[B]   839      for (unsigned int i = start; i < end; i++)
[B]   840        info[i].syllable() = syllable;
[B]   841    }
[ ]   842  
[ ]   843    /* Setup masks now */
[ ]   844  
[B]   845    {
[B]   846      hb_mask_t mask;
[ ]   847  
[ ]   848      /* Reph */
[B]   849      for (unsigned int i = start; i < end && info[i].indic_position() == POS_RA_TO_BECOME_REPH; i++)
[ ]   850        info[i].mask |= indic_plan->mask_array[INDIC_RPHF];
[ ]   851  
[ ]   852      /* Pre-base */
[B]   853      mask = indic_plan->mask_array[INDIC_HALF];
[B]   854      if (!indic_plan->is_old_spec &&
[B]   855  	indic_plan->config->blwf_mode == BLWF_MODE_PRE_AND_POST)
[ ]   856        mask |= indic_plan->mask_array[INDIC_BLWF];
[B]   857      for (unsigned int i = start; i < base; i++)
[B]   858        info[i].mask  |= mask;
[ ]   859      /* Base */
[B]   860      mask = 0;
[B]   861      if (base < end)
[B]   862        info[base].mask |= mask;
[ ]   863      /* Post-base */
[B]   864      mask = indic_plan->mask_array[INDIC_BLWF] |
[B]   865  	   indic_plan->mask_array[INDIC_ABVF] |
[B]   866  	   indic_plan->mask_array[INDIC_PSTF];
[B]   867      for (unsigned int i = base + 1; i < end; i++)
[B]   868        info[i].mask  |= mask;
[B]   869    }
[ ]   870  
[B]   871    if (indic_plan->is_old_spec &&
[B]   872        buffer->props.script == HB_SCRIPT_DEVANAGARI)
[B]   873    {
[ ]   874      /* Old-spec eye-lash Ra needs special handling.  From the
[ ]   875       * spec:
[ ]   876       *
[ ]   877       * "The feature 'below-base form' is applied to consonants
[ ]   878       * having below-base forms and following the base consonant.
[ ]   879       * The exception is vattu, which may appear below half forms
[ ]   880       * as well as below the base glyph. The feature 'below-base
[ ]   881       * form' will be applied to all such occurrences of Ra as well."
[ ]   882       *
[ ]   883       * Test case: U+0924,U+094D,U+0930,U+094d,U+0915
[ ]   884       * with Sanskrit 2003 font.
[ ]   885       *
[ ]   886       * However, note that Ra,Halant,ZWJ is the correct way to
[ ]   887       * request eyelash form of Ra, so we wouldbn't inhibit it
[ ]   888       * in that sequence.
[ ]   889       *
[ ]   890       * Test case: U+0924,U+094D,U+0930,U+094d,U+200D,U+0915
[ ]   891       */
[B]   892      for (unsigned int i = start; i + 1 < base; i++)
[ ]   893        if (info[i  ].indic_category() == I_Cat(Ra) &&
[ ]   894  	  info[i+1].indic_category() == I_Cat(H)  &&
[ ]   895  	  (i + 2 == base ||
[ ]   896  	   info[i+2].indic_category() != I_Cat(ZWJ)))
[ ]   897        {
[ ]   898  	info[i  ].mask |= indic_plan->mask_array[INDIC_BLWF];
[ ]   899  	info[i+1].mask |= indic_plan->mask_array[INDIC_BLWF];
[ ]   900        }
[B]   901    }
[ ]   902  
[B]   903    unsigned int pref_len = 2;
[B]   904    if (indic_plan->mask_array[INDIC_PREF] && base + pref_len < end)
[ ]   905    {
[ ]   906      /* Find a Halant,Ra sequence and mark it for pre-base-reordering processing. */
[ ]   907      for (unsigned int i = base + 1; i + pref_len - 1 < end; i++) {
[ ]   908        hb_codepoint_t glyphs[2];
[ ]   909        for (unsigned int j = 0; j < pref_len; j++)
[ ]   910  	glyphs[j] = info[i + j].codepoint;
[ ]   911        if (indic_plan->pref.would_substitute (glyphs, pref_len, face))
[ ]   912        {
[ ]   913  	for (unsigned int j = 0; j < pref_len; j++)
[ ]   914  	  info[i++].mask |= indic_plan->mask_array[INDIC_PREF];
[ ]   915  	break;
[ ]   916        }
[ ]   917      }
[ ]   918    }
[ ]   919  
[ ]   920    /* Apply ZWJ/ZWNJ effects */
[B]   921    for (unsigned int i = start + 1; i < end; i++)
[B]   922      if (is_joiner (info[i])) {
[B]   923        bool non_joiner = info[i].indic_category() == I_Cat(ZWNJ);
[B]   924        unsigned int j = i;
[ ]   925  
[B]   926        do {
[B]   927  	j--;
[ ]   928  
[ ]   929  	/* ZWJ/ZWNJ should disable CJCT.  They do that by simply
[ ]   930  	 * being there, since we don't skip them for the CJCT
[ ]   931  	 * feature (ie. F_MANUAL_ZWJ) */
[ ]   932  
[ ]   933  	/* A ZWNJ disables HALF. */
[B]   934  	if (non_joiner)
[B]   935  	  info[j].mask &= ~indic_plan->mask_array[INDIC_HALF];
[ ]   936  
[B]   937        } while (j > start && !is_consonant (info[j]));
[B]   938      }
[B]   939  }

--- Caller (1 hop): hb-ot-shaper-indic.cc:initial_reordering_standalone_cluster(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) (/src/harfbuzz/src/hb-ot-shaper-indic.cc:946-961, calls hb-ot-shaper-indic.cc:initial_reordering_consonant_syllable(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) at line 960) (full body — short) ---
[B]   946  {
[ ]   947    /* We treat placeholder/dotted-circle as if they are consonants, so we
[ ]   948     * should just chain.  Only if not in compatibility mode that is... */
[ ]   949  
[B]   950    const indic_shape_plan_t *indic_plan = (const indic_shape_plan_t *) plan->data;
[B]   951    if (indic_plan->uniscribe_bug_compatible)
[ ]   952    {
[ ]   953      /* For dotted-circle, this is what Uniscribe does:
[ ]   954       * If dotted-circle is the last glyph, it just does nothing.
[ ]   955       * Ie. It doesn't form Reph. */
[ ]   956      if (buffer->info[end - 1].indic_category() == I_Cat(DOTTEDCIRCLE))
[ ]   957        return;
[ ]   958    }
[ ]   959  
[B]   960    initial_reordering_consonant_syllable (plan, face, buffer, start, end); <-- CALL
[B]   961  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-indic.cc:initial_reordering_standalone_cluster(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:946-961, calls hb-ot-shaper-indic.cc:initial_reordering_consonant_syllable(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) at line 960)
hop 2  hb-ot-shaper-myanmar.cc:reorder_syllable_myanmar(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:308-320, calls hb-ot-shaper-indic.cc:initial_reordering_consonant_syllable(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) at line 314)
hop 3  hb-ot-shaper-indic.cc:initial_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:968-986, calls hb-ot-shaper-indic.cc:initial_reordering_standalone_cluster(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) at line 979)
hop 3  hb-ot-shaper-myanmar.cc:reorder_myanmar(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:326-344, calls hb-ot-shaper-myanmar.cc:reorder_syllable_myanmar(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) at line 336)
hop 4  hb-ot-shaper-indic.cc:initial_reordering_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:992-1011, calls hb-ot-shaper-indic.cc:initial_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) at line 1006)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      10         3  hb-ot-shaper-indic.cc:is_halant(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:86-88)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ot-shaper-indic.cc:initial_reordering_standalone_cluster(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:946-961) ---
  d=2   L 951  T=0 F=22  T=0 F=10  if (indic_plan->uniscribe_bug_compatible)
--- d=1  hb-ot-shaper-indic.cc:initial_reordering_consonant_syllable(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:470-939) ---
  d=1   L 478  T=4 F=34  T=0 F=25  if (buffer->props.script == HB_SCRIPT_KANNADA &&
  d=1   L 479  T=3 F=1  T=0 F=0  start + 3 <= end &&
  d=1   L 480  T=0 F=3  T=0 F=0  is_one_of (info[start  ], FLAG (I_Cat(Ra))) &&
  d=1   L 678  T=15 F=0  T=0 F=17  if (info[i].indic_category() == I_Cat(H))  <-- BLOCKER
  d=1   L 681  T=2 F=15  T=0 F=0  for (j = end - 1; j > i; j--)
  d=1   L 682  T=0 F=2  T=0 F=0  if (is_consonant (info[j]) ||
  d=1   L 683  T=0 F=2  T=0 F=0  (disallow_double_halants && info[j].indic_category() == I...
  d=1   L 685  T=0 F=15  T=0 F=0  if (info[j].indic_category() != I_Cat(H) && j > i) {
  d=1   L 736  T=0 F=17  T=7 F=10  } else if (FLAG_UNSAFE (info[i].indic_category()) & (FLAG...
  d=1   L 761  T=0 F=24  T=9 F=8  else if (info[i].indic_position() == POS_PRE_M)
  d=1   L 763  T=0 F=0  T=5 F=4  if (first_left_matra == end)
  d=1   L 769  T=0 F=38  T=3 F=22  if (first_left_matra < last_left_matra)
  d=1   L 775  T=0 F=0  T=7 F=3  for (unsigned j = i; j <= last_left_matra; j++)
  d=1   L 776  T=0 F=0  T=7 F=0  if (FLAG_UNSAFE (info[j].indic_category()) & (FLAG (I_Cat...
  d=1   L 892  T=0 F=9  T=0 F=4  for (unsigned int i = start; i + 1 < base; i++)
  d=1   L 934  T=2 F=0  T=1 F=0  if (non_joiner)
  d=1   L 937  T=1 F=1  T=0 F=1  } while (j > start && !is_consonant (info[j]));
  d=1   L 937  T=1 F=0  T=0 F=0  } while (j > start && !is_consonant (info[j]));

[off-chain: 29 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=c336d304b7510992, size=76 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1928s, mutation_op=ByteFlipMutator,WordInterestingMutator,BytesCopyMutator,BytesCopyMutator):
  0000: 0b 0b 04 00 30 32 02 00 02 00 02 04 0c 10 00 31   ....02.........1
  0010: 10 0d 00 00 39 10 00 00 0c 20 00 00 00 10 0e 35   ....9.... .....5
  0020: 7c 10 03 00 31 10 0d 00 84 0f ff ef 19 03 00 80   |...1...........
  0030: 00 fe ff 0f 84 10 05 72 b4 0b 02 0c 52 52 02 02   .......r....RR..
Seed 2 (id=bd95f0d91464d9e7, size=104 bytes, fuzzer=naive, trial=1, discovered_at=2872s, mutation_op=CrossoverReplaceMutator,BytesDeleteMutator,ByteNegMutator,BytesInsertMutator,BitFlipMutator):
  0000: 00 00 00 20 00 00 e7 19 00 00 64 e6 e6 00 30 00   ... ......d...0.
  0010: 00 00 0c 0c 64 6f 2d 68 61 6e 74 2d 6d 6f 00 00   ....do-hant-mo..
  0020: 00 00 01 61 6e 74 64 80 00 0c 00 00 00 00 00 0c   ...antd.........
  0030: 00 00 00 00 00 e9 17 00 00 00 e9 17 00 00 d0 17   ................
Seed 3 (id=3b0b8905e23e3695, size=88 bytes, fuzzer=naive, trial=1, discovered_at=5427s, mutation_op=ByteIncMutator,TokenInsert,DwordInterestingMutator,ByteInterestingMutator,BitFlipMutator):
  0000: b4 00 00 ff ff ff 7f 64 00 0c 00 00 00 18 18 18   .......d........
  0010: 18 10 00 00 d2 17 4a 92 24 09 00 00 00 10 00 00   ......J.$.......
  0020: d2 17 00 00 00 fe 00 00 00 00 00 00 01 fe 00 00   ................
  0030: 00 00 01 03 e8 2d 68 00 00 00 00 00 00 00 10 00   .....-h.........
Seed 4 (id=549dd0df4b551ea3, size=92 bytes, fuzzer=naive, trial=1, discovered_at=7606s, mutation_op=CrossoverInsertMutator,ByteRandMutator,TokenInsert,BytesDeleteMutator,ByteRandMutator,BytesCopyMutator,ByteAddMutator):
  0000: 80 00 2a 2a 6f 8c 62 7b 6b 00 00 20 5f 5f 5f 5f   ..**o.b{k.. ____
  0010: 00 00 5f 00 f7 1b 00 00 f7 1c 00 00 02 0c 00 00   .._.............
  0020: 00 0c 00 00 02 61 6e 74 64 80 80 00 2a 2a 6f 8c   .....antd...**o.
  0030: 62 7b 6b 00 00 20 5f 5f 5f 5f 00 00 5f 00 00 00   b{k.. ____.._...
Seed 5 (id=aa1db95df2e2f405, size=57 bytes, fuzzer=naive, trial=1, discovered_at=13782s, mutation_op=DwordInterestingMutator,ByteInterestingMutator):
  0000: b4 00 d2 d2 7f ff b5 d2 00 0c 00 00 00 18 18 18   ................
  0010: e7 17 00 00 d2 17 00 00 00 10 00 00 d2 17 00 00   ................
  0020: d2 17 00 00 86 1e 00 01 d2 17 00 00 00 10 e8 03   ................
  0030: 00 00 c0 00 00 00 00 00 00                        .........

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=2c1530bd7ce01cdf, size=62 bytes, fuzzer=cmplog, trial=1, discovered_at=176s, mutation_op=BitFlipMutator,BytesRandSetMutator,CrossoverReplaceMutator,ByteNegMutator):
  0000: 0c 0c 00 00 00 00 00 20 20 20 00 00 00 08 00 64   .......   .....d
  0010: 6f 2d 00 16 00 74 6c 6d 20 20 20 20 20 20 00 00   o-...tlm      ..
  0020: f9 01 0d df 20 20 20 20 20 20 20 20 00 64 0a 00   ....        .d..
  0030: 00 1a 72 74 6c 6d 20 20 31 09 00 00 74 20         ..rtlm  1...t 
Seed 2 (id=3675fdf17ec49db6, size=29 bytes, fuzzer=cmplog, trial=1, discovered_at=282s, mutation_op=ByteAddMutator,BytesDeleteMutator,CrossoverInsertMutator,ByteIncMutator,BytesDeleteMutator,CrossoverReplaceMutator,BytesSetMutator):
  0000: 0c 20 00 00 11 20 00 00 0c 20 00 00 00 0c 00 00   . ... ... ......
  0010: 20 8d 74 6c 7b 20 20 20 20 74 6c 7b 20             .tl{    tl{ 
Seed 3 (id=1ab7b55624217b8c, size=38 bytes, fuzzer=cmplog, trial=1, discovered_at=328s, mutation_op=ByteIncMutator,DwordAddMutator):
  0000: 04 00 80 00 dc 09 00 00 03 0d 00 00 00 ff 00 00   ................
  0010: ff 0a 00 80 dc 09 00 00 8b 09 00 00 00 ff 00 00   ................
  0020: ff 00 00 06 00 20                                 ..... 
Seed 4 (id=0e87a4f703257081, size=54 bytes, fuzzer=cmplog, trial=1, discovered_at=577s, mutation_op=WordAddMutator):
  0000: 00 00 0a 00 dc 09 00 00 03 0d 00 00 00 fe 02 00   ................
  0010: ff 0a 00 00 dc 09 00 00 03 00 00 00 00 ff 02 00   ................
  0020: ff 0a 00 00 dc 09 00 00 03 01 00 00 00 ff 00 00   ................
  0030: ff 0a 00 00 07 20                                 ..... 
Seed 5 (id=423f5ff5db868dfb, size=68 bytes, fuzzer=cmplog, trial=1, discovered_at=616s, mutation_op=CrossoverReplaceMutator,BytesSetMutator,BytesDeleteMutator,WordAddMutator,DwordInterestingMutator):
  0000: 34 34 34 34 34 00 00 00 01 0d 00 00 01 0d 00 00   44444...........
  0010: 57 6e 2d 68 61 6e 74 fb 00 0c ee 00 ef 01 00 00   Wn-hant.........
  0020: 01 0d 00 00 ef 01 00 10 01 20 20 20 20 20 20 00   .........      .
  0030: 1a 2d 6d 20 6f 0d 0d 0d 0d 0d 0d 0d 00 00 01 00   .-m o...........


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0006  00(.)x3 d2(.)x2 02(.)x1 e7(.)x1 +5u  00(.)x8 02(.)x1 01(.)x1             PARTIAL
   0x0007  00(.)x3 d2(.)x3 19(.)x1 64(d)x1 +4u  00(.)x8 20( )x1 bc(.)x1             PARTIAL
   0x0009  00(.)x6 0c(.)x3 7f(.)x1 d2(.)x1 +1u  0d(.)x4 20( )x2 0a(.)x2 00(.)x2     PARTIAL
   0x000a  00(.)x6 02(.)x1 64(d)x1 c1(.)x1 +3u  00(.)x8 09(.)x1 21(!)x1             PARTIAL
   0x000b  00(.)x4 04(.)x1 e6(.)x1 20( )x1 +5u  00(.)x9 36(6)x1                     PARTIAL
   0x000e  00(.)x4 18(.)x3 05(.)x2 30(0)x1 +2u  00(.)x9 02(.)x1                     PARTIAL
   0x000f  18(.)x4 00(.)x2 31(1)x1 5f(_)x1 +4u  00(.)x8 64(d)x1 36(6)x1             PARTIAL
   0x001c  00(.)x4 d2(.)x2 6d(m)x1 02(.)x1 +3u  00(.)x3 bf(.)x3 20( )x2 ef(.)x1     PARTIAL
   0x001e  00(.)x7 0e(.)x1 54(T)x1 0d(.)x1 +1u  00(.)x6 02(.)x1 e9(.)x1             PARTIAL
   0x001f  00(.)x7 35(5)x1 e2(.)x1 d2(.)x1 +1u  00(.)x7 10(.)x1                     PARTIAL
   0x0022  00(.)x6 03(.)x1 01(.)x1 d2(.)x1 +2u  00(.)x7 0d(.)x1                     PARTIAL
   0x0023  00(.)x7 61(a)x1 d2(.)x1 f5(.)x1 +1u  00(.)x4 df(.)x1 06(.)x1 36(6)x1     PARTIAL
   0x0026  00(.)x4 64(d)x2 0d(.)x1 6e(n)x1 +3u  00(.)x4 20( )x1 1d(.)x1             PARTIAL
   0x0027  00(.)x6 80(.)x1 74(t)x1 01(.)x1 +2u  00(.)x3 20( )x1 10(.)x1 31(1)x1     PARTIAL
   0x002a  00(.)x6 ff(.)x1 80(.)x1 18(.)x1 +2u  00(.)x3 20( )x2 06(.)x1             PARTIAL
   0x002b  00(.)x8 ef(.)x1 d2(.)x1 e6(.)x1     00(.)x3 20( )x2 6a(j)x1             PARTIAL
   0x002f  00(.)x3 10(.)x2 80(.)x1 0c(.)x1 +4u  00(.)x4 5a(Z)x1                     PARTIAL
   0x0030  00(.)x8 62(b)x1 6f(o)x1 49(I)x1     00(.)x1 ff(.)x1 1a(.)x1 20( )x1 +1u  PARTIAL
   0x0032  00(.)x3 ff(.)x1 01(.)x1 6b(k)x1 +5u  72(r)x2 00(.)x2 6d(m)x1             PARTIAL
   0x0033  00(.)x5 0f(.)x1 03(.)x1 6f(o)x1 +3u  74(t)x1 00(.)x1 20( )x1 61(a)x1     PARTIAL
   0x0034  00(.)x7 84(.)x1 e8(.)x1 6f(o)x1 +1u  6c(l)x1 07(.)x1 6f(o)x1 6e(n)x1     PARTIAL
   0x0035  00(.)x5 10(.)x1 e9(.)x1 2d(-)x1 +3u  6d(m)x1 20( )x1 0d(.)x1 03(.)x1     PARTIAL
   0x0036  00(.)x3 05(.)x1 17(.)x1 68(h)x1 +5u  20( )x1 0d(.)x1 05(.)x1             PARTIAL
   0x0037  00(.)x6 72(r)x1 5f(_)x1 6f(o)x1 +2u  20( )x1 0d(.)x1 29())x1             DIFFER
   0x0038  00(.)x7 b4(.)x1 5f(_)x1 6f(o)x1 +1u  31(1)x1 0d(.)x1 2a(*)x1             DIFFER
   0x0039  00(.)x4 0b(.)x1 5f(_)x1 6f(o)x1 +3u  09(.)x1 0d(.)x1 24($)x1             DIFFER
   0x003a  00(.)x5 02(.)x1 e9(.)x1 6f(o)x1 +2u  00(.)x1 0d(.)x1 7f(.)x1             PARTIAL
   0x003b  00(.)x5 0c(.)x1 17(.)x1 6f(o)x1 +2u  00(.)x2 0d(.)x1                     PARTIAL
   0x003c  00(.)x6 52(R)x1 5f(_)x1 6f(o)x1 +1u  00(.)x2 74(t)x1                     PARTIAL
   0x003d  00(.)x6 52(R)x1 6f(o)x1 1c(.)x1 +1u  20( )x1 00(.)x1 d2(.)x1             PARTIAL
   0x003e  00(.)x4 20( )x2 02(.)x1 d0(.)x1 +2u  01(.)x1 00(.)x1                     PARTIAL
   0x003f  00(.)x6 17(.)x2 02(.)x1 e7(.)x1     00(.)x1 7f(.)x1                     PARTIAL
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
  prompts_b/harfbuzz_5844.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5844,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5844 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5844 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5844 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).