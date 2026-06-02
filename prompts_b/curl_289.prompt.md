==== BLOCKER ====
Target: curl
Branch ID: 289
Location: /src/curl/lib/mprintf.c:735:16
Enclosing function: mprintf.c:dprintf_formatf
Source line:       is_neg = (p->data.num.as_signed < (mp_intmax_t)0) ? 1 : 0;
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    2        8          0  REFERENCE
value_profile_cmplog             7        3          0  REFERENCE
naive_ctx                        2        8          0  REFERENCE
naive_ngram4                     1        9          0  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        7        3          0  REFERENCE
fast                             7        3          0  REFERENCE
grimoire                        10        0          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=8.40h  loser=23.10h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.70  dur_div=14.70h  hit_div=2
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/289/{W,L}/branch_coverage_show.txt

--- Enclosing function: mprintf.c:dprintf_formatf (/src/curl/lib/mprintf.c:576-1008) ---
[ ]   574    const char *format,    /* %-formatted string */
[ ]   575    va_list ap_save) /* list of parameters */
[B]   576  {
[ ]   577    /* Base-36 digits for numbers.  */
[B]   578    const char *digits = lower_digits;
[ ]   579  
[ ]   580    /* Pointer into the format string.  */
[B]   581    char *f;
[ ]   582  
[ ]   583    /* Number of characters written.  */
[B]   584    int done = 0;
[ ]   585  
[B]   586    long param; /* current parameter to read */
[B]   587    long param_num = 0; /* parameter counter */
[ ]   588  
[B]   589    struct va_stack vto[MAX_PARAMETERS];
[B]   590    char *endpos[MAX_PARAMETERS];
[B]   591    char **end;
[B]   592    char work[BUFFSIZE];
[B]   593    struct va_stack *p;
[ ]   594  
[ ]   595    /* 'workend' points to the final buffer byte position, but with an extra
[ ]   596       byte as margin to avoid the (false?) warning Coverity gives us
[ ]   597       otherwise */
[B]   598    char *workend = &work[sizeof(work) - 2];
[ ]   599  
[ ]   600    /* Do the actual %-code parsing */
[B]   601    if(dprintf_Pass1(format, vto, endpos, ap_save))
[ ]   602      return 0;
[ ]   603  
[B]   604    end = &endpos[0]; /* the initial end-position from the list dprintf_Pass1()
[ ]   605                         created for us */
[ ]   606  
[B]   607    f = (char *)format;
[B]   608    while(*f != '\0') {
[ ]   609      /* Format spec modifiers.  */
[B]   610      int is_alt;
[ ]   611  
[ ]   612      /* Width of a field.  */
[B]   613      long width;
[ ]   614  
[ ]   615      /* Precision of a field.  */
[B]   616      long prec;
[ ]   617  
[ ]   618      /* Decimal integer is negative.  */
[B]   619      int is_neg;
[ ]   620  
[ ]   621      /* Base of a number to be written.  */
[B]   622      unsigned long base;
[ ]   623  
[ ]   624      /* Integral values to be written.  */
[B]   625      mp_uintmax_t num;
[ ]   626  
[ ]   627      /* Used to convert negative in positive.  */
[B]   628      mp_intmax_t signed_num;
[ ]   629  
[B]   630      char *w;
[ ]   631  
[B]   632      if(*f != '%') {
[ ]   633        /* This isn't a format spec, so write everything out until the next one
[ ]   634           OR end of string is reached.  */
[B]   635        do {
[B]   636          OUTCHAR(*f);
[B]   637        } while(*++f && ('%' != *f));
[B]   638        continue;
[B]   639      }
[ ]   640  
[B]   641      ++f;
[ ]   642  
[ ]   643      /* Check for "%%".  Note that although the ANSI standard lists
[ ]   644         '%' as a conversion specifier, it says "The complete format
[ ]   645         specification shall be `%%'," so we can avoid all the width
[ ]   646         and precision processing.  */
[B]   647      if(*f == '%') {
[L]   648        ++f;
[L]   649        OUTCHAR('%');
[L]   650        continue;
[L]   651      }
[ ]   652  
[ ]   653      /* If this is a positional parameter, the position must follow immediately
[ ]   654         after the %, thus create a %<num>$ sequence */
[B]   655      param = dprintf_DollarString(f, &f);
[ ]   656  
[B]   657      if(!param)
[B]   658        param = param_num;
[ ]   659      else
[ ]   660        --param;
[ ]   661  
[B]   662      param_num++; /* increase this always to allow "%2$s %1$s %s" and then the
[ ]   663                      third %s will pick the 3rd argument */
[ ]   664  
[B]   665      p = &vto[param];
[ ]   666  
[ ]   667      /* pick up the specified width */
[B]   668      if(p->flags & FLAGS_WIDTHPARAM) {
[ ]   669        width = (long)vto[p->width].data.num.as_signed;
[ ]   670        param_num++; /* since the width is extracted from a parameter, we
[ ]   671                        must skip that to get to the next one properly */
[ ]   672        if(width < 0) {
[ ]   673          /* "A negative field width is taken as a '-' flag followed by a
[ ]   674             positive field width." */
[ ]   675          width = -width;
[ ]   676          p->flags |= FLAGS_LEFT;
[ ]   677          p->flags &= ~FLAGS_PAD_NIL;
[ ]   678        }
[ ]   679      }
[B]   680      else
[B]   681        width = p->width;
[ ]   682  
[ ]   683      /* pick up the specified precision */
[B]   684      if(p->flags & FLAGS_PRECPARAM) {
[ ]   685        prec = (long)vto[p->precision].data.num.as_signed;
[ ]   686        param_num++; /* since the precision is extracted from a parameter, we
[ ]   687                        must skip that to get to the next one properly */
[ ]   688        if(prec < 0)
[ ]   689          /* "A negative precision is taken as if the precision were
[ ]   690             omitted." */
[ ]   691          prec = -1;
[ ]   692      }
[B]   693      else if(p->flags & FLAGS_PREC)
[ ]   694        prec = p->precision;
[B]   695      else
[B]   696        prec = -1;
[ ]   697  
[B]   698      is_alt = (p->flags & FLAGS_ALT) ? 1 : 0;
[ ]   699  
[B]   700      switch(p->type) {
[B]   701      case FORMAT_INT:
[B]   702        num = p->data.num.as_unsigned;
[B]   703        if(p->flags & FLAGS_CHAR) {
[ ]   704          /* Character.  */
[L]   705          if(!(p->flags & FLAGS_LEFT))
[L]   706            while(--width > 0)
[ ]   707              OUTCHAR(' ');
[L]   708          OUTCHAR((char) num);
[L]   709          if(p->flags & FLAGS_LEFT)
[ ]   710            while(--width > 0)
[ ]   711              OUTCHAR(' ');
[L]   712          break;
[L]   713        }
[B]   714        if(p->flags & FLAGS_OCTAL) {
[ ]   715          /* Octal unsigned integer.  */
[ ]   716          base = 8;
[ ]   717          goto unsigned_number;
[ ]   718        }
[B]   719        else if(p->flags & FLAGS_HEX) {
[ ]   720          /* Hexadecimal unsigned integer.  */
[ ]   721  
[L]   722          digits = (p->flags & FLAGS_UPPER)? upper_digits : lower_digits;
[L]   723          base = 16;
[L]   724          goto unsigned_number;
[L]   725        }
[B]   726        else if(p->flags & FLAGS_UNSIGNED) {
[ ]   727          /* Decimal unsigned integer.  */
[B]   728          base = 10;
[B]   729          goto unsigned_number;
[B]   730        }
[ ]   731  
[ ]   732        /* Decimal integer.  */
[B]   733        base = 10;
[ ]   734  
[B]   735        is_neg = (p->data.num.as_signed < (mp_intmax_t)0) ? 1 : 0; <-- BLOCKER
[B]   736        if(is_neg) {
[ ]   737          /* signed_num might fail to hold absolute negative minimum by 1 */
[W]   738          signed_num = p->data.num.as_signed + (mp_intmax_t)1;
[W]   739          signed_num = -signed_num;
[W]   740          num = (mp_uintmax_t)signed_num;
[W]   741          num += (mp_uintmax_t)1;
[W]   742        }
[ ]   743  
[B]   744        goto number;
[ ]   745  
[B]   746        unsigned_number:
[ ]   747        /* Unsigned number of base BASE.  */
[B]   748        is_neg = 0;
[ ]   749  
[B]   750        number:
[ ]   751        /* Number of base BASE.  */
[ ]   752  
[ ]   753        /* Supply a default precision if none was given.  */
[B]   754        if(prec == -1)
[B]   755          prec = 1;
[ ]   756  
[ ]   757        /* Put the number in WORK.  */
[B]   758        w = workend;
[B]   759        while(num > 0) {
[B]   760          *w-- = digits[num % base];
[B]   761          num /= base;
[B]   762        }
[B]   763        width -= (long)(workend - w);
[B]   764        prec -= (long)(workend - w);
[ ]   765  
[B]   766        if(is_alt && base == 8 && prec <= 0) {
[ ]   767          *w-- = '0';
[ ]   768          --width;
[ ]   769        }
[ ]   770  
[B]   771        if(prec > 0) {
[B]   772          width -= prec;
[B]   773          while(prec-- > 0 && w >= work)
[B]   774            *w-- = '0';
[B]   775        }
[ ]   776  
[B]   777        if(is_alt && base == 16)
[ ]   778          width -= 2;
[ ]   779  
[B]   780        if(is_neg || (p->flags & FLAGS_SHOWSIGN) || (p->flags & FLAGS_SPACE))
[W]   781          --width;
[ ]   782  
[B]   783        if(!(p->flags & FLAGS_LEFT) && !(p->flags & FLAGS_PAD_NIL))
[B]   784          while(width-- > 0)
[ ]   785            OUTCHAR(' ');
[ ]   786  
[B]   787        if(is_neg)
[W]   788          OUTCHAR('-');
[B]   789        else if(p->flags & FLAGS_SHOWSIGN)
[ ]   790          OUTCHAR('+');
[B]   791        else if(p->flags & FLAGS_SPACE)
[ ]   792          OUTCHAR(' ');
[ ]   793  
[B]   794        if(is_alt && base == 16) {
[ ]   795          OUTCHAR('0');
[ ]   796          if(p->flags & FLAGS_UPPER)
[ ]   797            OUTCHAR('X');
[ ]   798          else
[ ]   799            OUTCHAR('x');
[ ]   800        }
[ ]   801  
[B]   802        if(!(p->flags & FLAGS_LEFT) && (p->flags & FLAGS_PAD_NIL))
[L]   803          while(width-- > 0)
[ ]   804            OUTCHAR('0');
[ ]   805  
[ ]   806        /* Write the number.  */
[B]   807        while(++w <= workend) {
[B]   808          OUTCHAR(*w);
[B]   809        }
[ ]   810  
[B]   811        if(p->flags & FLAGS_LEFT)
[ ]   812          while(width-- > 0)
[ ]   813            OUTCHAR(' ');
[B]   814        break;
[ ]   815  
[B]   816      case FORMAT_STRING:
[ ]   817              /* String.  */
[B]   818        {
[B]   819          static const char null[] = "(nil)";
[B]   820          const char *str;
[B]   821          size_t len;
[ ]   822  
[B]   823          str = (char *) p->data.str;
[B]   824          if(!str) {
[ ]   825            /* Write null[] if there's space.  */
[ ]   826            if(prec == -1 || prec >= (long) sizeof(null) - 1) {
[ ]   827              str = null;
[ ]   828              len = sizeof(null) - 1;
[ ]   829              /* Disable quotes around (nil) */
[ ]   830              p->flags &= (~FLAGS_ALT);
[ ]   831            }
[ ]   832            else {
[ ]   833              str = "";
[ ]   834              len = 0;
[ ]   835            }
[ ]   836          }
[B]   837          else if(prec != -1)
[ ]   838            len = (size_t)prec;
[B]   839          else if(*str == '\0')
[B]   840            len = 0;
[B]   841          else
[B]   842            len = strlen(str);
[ ]   843  
[B]   844          width -= (len > LONG_MAX) ? LONG_MAX : (long)len;
[ ]   845  
[B]   846          if(p->flags & FLAGS_ALT)
[ ]   847            OUTCHAR('"');
[ ]   848  
[B]   849          if(!(p->flags&FLAGS_LEFT))
[B]   850            while(width-- > 0)
[ ]   851              OUTCHAR(' ');
[ ]   852  
[B]   853          for(; len && *str; len--)
[B]   854            OUTCHAR(*str++);
[B]   855          if(p->flags&FLAGS_LEFT)
[ ]   856            while(width-- > 0)
[ ]   857              OUTCHAR(' ');
[ ]   858  
[B]   859          if(p->flags & FLAGS_ALT)
[ ]   860            OUTCHAR('"');
[B]   861        }
[B]   862        break;
[ ]   863  
[B]   864      case FORMAT_PTR:
[ ]   865        /* Generic pointer.  */
[ ]   866        {
[ ]   867          void *ptr;
[ ]   868          ptr = (void *) p->data.ptr;
[ ]   869          if(ptr) {
[ ]   870            /* If the pointer is not NULL, write it as a %#x spec.  */
[ ]   871            base = 16;
[ ]   872            digits = (p->flags & FLAGS_UPPER)? upper_digits : lower_digits;
[ ]   873            is_alt = 1;
[ ]   874            num = (size_t) ptr;
[ ]   875            is_neg = 0;
[ ]   876            goto number;
[ ]   877          }
[ ]   878          else {
[ ]   879            /* Write "(nil)" for a nil pointer.  */
[ ]   880            static const char strnil[] = "(nil)";
[ ]   881            const char *point;
[ ]   882  
[ ]   883            width -= (long)(sizeof(strnil) - 1);
[ ]   884            if(p->flags & FLAGS_LEFT)
[ ]   885              while(width-- > 0)
[ ]   886                OUTCHAR(' ');
[ ]   887            for(point = strnil; *point != '\0'; ++point)
[ ]   888              OUTCHAR(*point);
[ ]   889            if(!(p->flags & FLAGS_LEFT))
[ ]   890              while(width-- > 0)
[ ]   891                OUTCHAR(' ');
[ ]   892          }
[ ]   893        }
[ ]   894        break;
[ ]   895  
[ ]   896      case FORMAT_DOUBLE:
[ ]   897        {
[ ]   898          char formatbuf[32]="%";
[ ]   899          char *fptr = &formatbuf[1];
[ ]   900          size_t left = sizeof(formatbuf)-strlen(formatbuf);
[ ]   901          int len;
[ ]   902  
[ ]   903          width = -1;
[ ]   904          if(p->flags & FLAGS_WIDTH)
[ ]   905            width = p->width;
[ ]   906          else if(p->flags & FLAGS_WIDTHPARAM)
[ ]   907            width = (long)vto[p->width].data.num.as_signed;
[ ]   908  
[ ]   909          prec = -1;
[ ]   910          if(p->flags & FLAGS_PREC)
[ ]   911            prec = p->precision;
[ ]   912          else if(p->flags & FLAGS_PRECPARAM)
[ ]   913            prec = (long)vto[p->precision].data.num.as_signed;
[ ]   914  
[ ]   915          if(p->flags & FLAGS_LEFT)
[ ]   916            *fptr++ = '-';
[ ]   917          if(p->flags & FLAGS_SHOWSIGN)
[ ]   918            *fptr++ = '+';
[ ]   919          if(p->flags & FLAGS_SPACE)
[ ]   920            *fptr++ = ' ';
[ ]   921          if(p->flags & FLAGS_ALT)
[ ]   922            *fptr++ = '#';
[ ]   923  
[ ]   924          *fptr = 0;
[ ]   925  
[ ]   926          if(width >= 0) {
[ ]   927            if(width >= (long)sizeof(work))
[ ]   928              width = sizeof(work)-1;
[ ]   929            /* RECURSIVE USAGE */
[ ]   930            len = curl_msnprintf(fptr, left, "%ld", width);
[ ]   931            fptr += len;
[ ]   932            left -= len;
[ ]   933          }
[ ]   934          if(prec >= 0) {
[ ]   935            /* for each digit in the integer part, we can have one less
[ ]   936               precision */
[ ]   937            size_t maxprec = sizeof(work) - 2;
[ ]   938            double val = p->data.dnum;
[ ]   939            if(width > 0 && prec <= width)
[ ]   940              maxprec -= width;
[ ]   941            while(val >= 10.0) {
[ ]   942              val /= 10;
[ ]   943              maxprec--;
[ ]   944            }
[ ]   945  
[ ]   946            if(prec > (long)maxprec)
[ ]   947              prec = (long)maxprec-1;
[ ]   948            if(prec < 0)
[ ]   949              prec = 0;
[ ]   950            /* RECURSIVE USAGE */
[ ]   951            len = curl_msnprintf(fptr, left, ".%ld", prec);
[ ]   952            fptr += len;
[ ]   953          }
[ ]   954          if(p->flags & FLAGS_LONG)
[ ]   955            *fptr++ = 'l';
[ ]   956  
[ ]   957          if(p->flags & FLAGS_FLOATE)
[ ]   958            *fptr++ = (char)((p->flags & FLAGS_UPPER) ? 'E':'e');
[ ]   959          else if(p->flags & FLAGS_FLOATG)
[ ]   960            *fptr++ = (char)((p->flags & FLAGS_UPPER) ? 'G' : 'g');
[ ]   961          else
[ ]   962            *fptr++ = 'f';
[ ]   963  
[ ]   964          *fptr = 0; /* and a final null-termination */
[ ]   965  
[ ]   966  #ifdef __clang__
[ ]   967  #pragma clang diagnostic push
[ ]   968  #pragma clang diagnostic ignored "-Wformat-nonliteral"
[ ]   969  #endif
[ ]   970          /* NOTE NOTE NOTE!! Not all sprintf implementations return number of
[ ]   971             output characters */
[ ]   972  #ifdef HAVE_SNPRINTF
[ ]   973          (snprintf)(work, sizeof(work), formatbuf, p->data.dnum);
[ ]   974  #else
[ ]   975          (sprintf)(work, formatbuf, p->data.dnum);
[ ]   976  #endif
[ ]   977  #ifdef __clang__
[ ]   978  #pragma clang diagnostic pop
[ ]   979  #endif
[ ]   980          DEBUGASSERT(strlen(work) <= sizeof(work));
[ ]   981          for(fptr = work; *fptr; fptr++)
[ ]   982            OUTCHAR(*fptr);
[ ]   983        }
[ ]   984        break;
[ ]   985  
[ ]   986      case FORMAT_INTPTR:
[ ]   987        /* Answer the count of characters written.  */
[ ]   988  #ifdef HAVE_LONG_LONG_TYPE
[ ]   989        if(p->flags & FLAGS_LONGLONG)
[ ]   990          *(LONG_LONG_TYPE *) p->data.ptr = (LONG_LONG_TYPE)done;
[ ]   991        else
[ ]   992  #endif
[ ]   993          if(p->flags & FLAGS_LONG)
[ ]   994            *(long *) p->data.ptr = (long)done;
[ ]   995        else if(!(p->flags & FLAGS_SHORT))
[ ]   996          *(int *) p->data.ptr = (int)done;
[ ]   997        else
[ ]   998          *(short *) p->data.ptr = (short)done;
[ ]   999        break;
[ ]  1000  
[ ]  1001      default:
[ ]  1002        break;
[B]  1003      }
[B]  1004      f = *end++; /* goto end of %-code */
[ ]  1005  
[B]  1006    }
[B]  1007    return done;
[B]  1008  }

--- Caller (1 hop): curl_mvsnprintf (/src/curl/lib/mprintf.c:1028-1049, calls mprintf.c:dprintf_formatf at line 1036) (full body — short) ---
[B]  1028  {
[B]  1029    int retcode;
[B]  1030    struct nsprintf info;
[ ]  1031  
[B]  1032    info.buffer = buffer;
[B]  1033    info.length = 0;
[B]  1034    info.max = maxlength;
[ ]  1035  
[B]  1036    retcode = dprintf_formatf(&info, addbyter, format, ap_save); <-- CALL
[B]  1037    if(info.max) {
[ ]  1038      /* we terminate this with a zero byte */
[B]  1039      if(info.max == info.length) {
[ ]  1040        /* we're at maximum, scrap the last letter */
[ ]  1041        info.buffer[-1] = 0;
[ ]  1042        DEBUGASSERT(retcode);
[ ]  1043        retcode--; /* don't count the nul byte */
[ ]  1044      }
[B]  1045      else
[B]  1046        info.buffer[0] = 0;
[B]  1047    }
[B]  1048    return retcode;
[B]  1049  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  Curl_dyn_vprintf  (/src/curl/lib/mprintf.c:1079-1090, calls mprintf.c:dprintf_formatf at line 1084)
hop 2  curl_mvsnprintf  (/src/curl/lib/mprintf.c:1028-1049, calls mprintf.c:dprintf_formatf at line 1036)
hop 3  Curl_dyn_vaddf  (/src/curl/lib/dynbuf.c:183-206, calls Curl_dyn_vprintf at line 189)
hop 3  curl_msnprintf  (/src/curl/lib/mprintf.c:1052-1059, calls curl_mvsnprintf at line 1056)
hop 4  Curl_dyn_addf  (/src/curl/lib/dynbuf.c:212-222, calls Curl_dyn_vaddf at line 219)
hop 4  Curl_pp_vsendf  (/src/curl/lib/pingpong.c:170-231, calls Curl_dyn_vaddf at line 190)
hop 5  curl_easy_escape  (/src/curl/lib/escape.c:85-116, calls Curl_dyn_addf at line 109)
hop 5  http.c:add_haproxy_protocol_header  (/src/curl/lib/http.c:1601-1632, calls Curl_dyn_addf at line 1617)
hop 5  imap.c:imap_sendf  (/src/curl/lib/imap.c:1768-1791, calls Curl_pp_vsendf at line 1787)
hop 5  Curl_pp_sendf  (/src/curl/lib/pingpong.c:246-256, calls Curl_pp_vsendf at line 251)
hop 6  curl_escape  (/src/curl/lib/escape.c:70-72, calls curl_easy_escape at line 71)
hop 6  Curl_http_connect  (/src/curl/lib/http.c:1541-1584, calls http.c:add_haproxy_protocol_header at line 1568)
hop 6  imap.c:imap_perform_capability  (/src/curl/lib/imap.c:438-452, calls imap.c:imap_sendf at line 446)
hop 6  imap.c:imap_perform_starttls  (/src/curl/lib/imap.c:461-469, calls imap.c:imap_sendf at line 463)
hop 6  smtp.c:smtp_perform_ehlo  (/src/curl/lib/smtp.c:329-347, calls Curl_pp_sendf at line 341)
hop 6  smtp.c:smtp_perform_helo  (/src/curl/lib/smtp.c:357-371, calls Curl_pp_sendf at line 365)
hop 6  curl_url_get  (/src/curl/lib/urlapi.c:1377-1620, calls curl_easy_escape at line 1514)
hop 7  imap.c:imap_perform_upgrade_tls  (/src/curl/lib/imap.c:479-496, calls imap.c:imap_perform_capability at line 491)
hop 7  imap.c:imap_state_capability_resp  (/src/curl/lib/imap.c:894-971, calls imap.c:imap_perform_starttls at line 958)
hop 7  imap.c:imap_state_servergreet_resp  (/src/curl/lib/imap.c:872-888, calls imap.c:imap_perform_capability at line 887)
hop 7  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661, calls Curl_http_connect at line 2027)
hop 7  rtsp.c:rtsp_connect  (/src/curl/lib/rtsp.c:186-200, calls Curl_http_connect at line 189)
hop 7  smtp.c:smtp_perform_upgrade_tls  (/src/curl/lib/smtp.c:399-418, calls smtp.c:smtp_perform_ehlo at line 413)
hop 7  smtp.c:smtp_state_ehlo_resp  (/src/curl/lib/smtp.c:882-979, calls smtp.c:smtp_perform_helo at line 892)
hop 7  smtp.c:smtp_state_servergreet_resp  (/src/curl/lib/smtp.c:838-850, calls smtp.c:smtp_perform_ehlo at line 847)
hop 7  Curl_follow  (/src/curl/lib/transfer.c:1568-1849, calls curl_url_get at line 1625)
hop 7  Curl_pretransfer  (/src/curl/lib/transfer.c:1403-1541, calls curl_url_get at line 1422)
hop 8  imap.c:imap_state_starttls_resp  (/src/curl/lib/imap.c:977-999, calls imap.c:imap_perform_upgrade_tls at line 996)
hop 8  imap.c:imap_statemachine  (/src/curl/lib/imap.c:1291-1378, calls imap.c:imap_perform_upgrade_tls at line 1302)
hop 8  curl_multi_perform  (/src/curl/lib/multi.c:2665-2716, calls multi.c:multi_runsingle at line 2683)
hop 8  multi.c:multi_socket  (/src/curl/lib/multi.c:3101-3208, calls multi.c:multi_runsingle at line 3158)
hop 8  smtp.c:smtp_state_starttls_resp  (/src/curl/lib/smtp.c:856-876, calls smtp.c:smtp_perform_upgrade_tls at line 873)
hop 8  smtp.c:smtp_statemachine  (/src/curl/lib/smtp.c:1197-1278, calls smtp.c:smtp_perform_upgrade_tls at line 1207)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     276       830  mprintf.c:dprintf_IsQualifierNoDollar  (/src/curl/lib/mprintf.c:196-217)
      61       223  mprintf.c:dprintf_Pass1  (/src/curl/lib/mprintf.c:231-567)
      61       223  mprintf.c:dprintf_formatf  (/src/curl/lib/mprintf.c:576-1008)  <-- enclosing
      35       112  curl_mvsnprintf  (/src/curl/lib/mprintf.c:1028-1049)
      35       112  curl_msnprintf  (/src/curl/lib/mprintf.c:1052-1059)
      11        77  Curl_dyn_vprintf  (/src/curl/lib/mprintf.c:1079-1090)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  curl_mvsnprintf  (/src/curl/lib/mprintf.c:1028-1049) ---
  d=2   L1037  T=35 F=0  T=112 F=0  if(info.max) {
  d=2   L1039  T=0 F=35  T=0 F=112  if(info.max == info.length) {
--- d=2  Curl_dyn_vprintf  (/src/curl/lib/mprintf.c:1079-1090) ---
  d=2   L1085  T=0 F=11  T=0 F=77  if(info.fail) {
--- d=1  mprintf.c:dprintf_formatf  (/src/curl/lib/mprintf.c:576-1008) ---
  d=1   L 601  T=0 F=61  T=0 F=223  if(dprintf_Pass1(format, vto, endpos, ap_save))
  d=1   L 608  T=347 F=61  T=971 F=223  while(*f != '\0') {
  d=1   L 632  T=96 F=251  T=181 F=790  if(*f != '%') {
  d=1   L 647  T=0 F=251  T=57 F=733  if(*f == '%') {
  d=1   L 657  T=251 F=0  T=733 F=0  if(!param)
  d=1   L 668  T=0 F=251  T=0 F=733  if(p->flags & FLAGS_WIDTHPARAM) {
  d=1   L 684  T=0 F=251  T=0 F=733  if(p->flags & FLAGS_PRECPARAM) {
  d=1   L 693  T=0 F=251  T=0 F=733  else if(p->flags & FLAGS_PREC)
  d=1   L 698  T=0 F=251  T=0 F=733  is_alt = (p->flags & FLAGS_ALT) ? 1 : 0;
  d=1   L 701  T=60 F=191  T=330 F=403  case FORMAT_INT:
  d=1   L 703  T=0 F=60  T=163 F=167  if(p->flags & FLAGS_CHAR) {
  d=1   L 705  T=0 F=0  T=163 F=0  if(!(p->flags & FLAGS_LEFT))
  d=1   L 706  T=0 F=0  T=0 F=163  while(--width > 0)
  d=1   L 709  T=0 F=0  T=0 F=163  if(p->flags & FLAGS_LEFT)
  d=1   L 714  T=0 F=60  T=0 F=167  if(p->flags & FLAGS_OCTAL) {
  d=1   L 719  T=0 F=60  T=57 F=110  else if(p->flags & FLAGS_HEX) {
  d=1   L 722  T=0 F=0  T=0 F=57  digits = (p->flags & FLAGS_UPPER)? upper_digits : lower_d...
  d=1   L 735  T=5 F=20  T=0 F=40  is_neg = (p->data.num.as_signed < (mp_intmax_t)0) ? 1 : 0;  <-- BLOCKER
  d=1   L 736  T=5 F=20  T=0 F=40  if(is_neg) {
  d=1   L 754  T=60 F=0  T=167 F=0  if(prec == -1)
  d=1   L 759  T=75 F=60  T=254 F=167  while(num > 0) {
  d=1   L 766  T=0 F=60  T=0 F=167  if(is_alt && base == 8 && prec <= 0) {
  d=1   L 771  T=20 F=40  T=40 F=127  if(prec > 0) {
  d=1   L 773  T=20 F=0  T=40 F=0  while(prec-- > 0 && w >= work)
  d=1   L 773  T=20 F=20  T=40 F=40  while(prec-- > 0 && w >= work)
  d=1   L 777  T=0 F=60  T=0 F=167  if(is_alt && base == 16)
  d=1   L 780  T=0 F=55  T=0 F=167  if(is_neg || (p->flags & FLAGS_SHOWSIGN) || (p->flags & F...
  d=1   L 780  T=0 F=55  T=0 F=167  if(is_neg || (p->flags & FLAGS_SHOWSIGN) || (p->flags & F...
  d=1   L 780  T=5 F=55  T=0 F=167  if(is_neg || (p->flags & FLAGS_SHOWSIGN) || (p->flags & F...
  d=1   L 783  T=60 F=0  T=110 F=57  if(!(p->flags & FLAGS_LEFT) && !(p->flags & FLAGS_PAD_NIL))
  d=1   L 783  T=60 F=0  T=167 F=0  if(!(p->flags & FLAGS_LEFT) && !(p->flags & FLAGS_PAD_NIL))
  d=1   L 787  T=5 F=55  T=0 F=167  if(is_neg)
  d=1   L 789  T=0 F=55  T=0 F=167  else if(p->flags & FLAGS_SHOWSIGN)
  d=1   L 791  T=0 F=55  T=0 F=167  else if(p->flags & FLAGS_SPACE)
  d=1   L 794  T=0 F=60  T=0 F=167  if(is_alt && base == 16) {
  d=1   L 802  T=0 F=60  T=57 F=110  if(!(p->flags & FLAGS_LEFT) && (p->flags & FLAGS_PAD_NIL))
  d=1   L 802  T=60 F=0  T=167 F=0  if(!(p->flags & FLAGS_LEFT) && (p->flags & FLAGS_PAD_NIL))
  d=1   L 803  T=0 F=0  T=0 F=57  while(width-- > 0)
  d=1   L 807  T=95 F=60  T=294 F=167  while(++w <= workend) {
  d=1   L 811  T=0 F=60  T=0 F=167  if(p->flags & FLAGS_LEFT)
  d=1   L 816  T=191 F=60  T=403 F=330  case FORMAT_STRING:
  d=1   L 824  T=0 F=191  T=0 F=403  if(!str) {
  d=1   L 837  T=0 F=191  T=0 F=403  else if(prec != -1)
  d=1   L 839  T=117 F=74  T=243 F=160  else if(*str == '\0')
  d=1   L 844  T=0 F=191  T=0 F=403  width -= (len > LONG_MAX) ? LONG_MAX : (long)len;
  d=1   L 846  T=0 F=191  T=0 F=403  if(p->flags & FLAGS_ALT)
  d=1   L 849  T=191 F=0  T=403 F=0  if(!(p->flags&FLAGS_LEFT))
  d=1   L 850  T=0 F=191  T=0 F=403  while(width-- > 0)
  d=1   L 853  T=726 F=0  T=1960 F=0  for(; len && *str; len--)
  d=1   L 853  T=726 F=191  T=1960 F=403  for(; len && *str; len--)
  d=1   L 855  T=0 F=191  T=0 F=403  if(p->flags&FLAGS_LEFT)
  d=1   L 859  T=0 F=191  T=0 F=403  if(p->flags & FLAGS_ALT)
  d=1   L 864  T=0 F=251  T=0 F=733  case FORMAT_PTR:
  d=1   L 896  T=0 F=251  T=0 F=733  case FORMAT_DOUBLE:
  d=1   L 986  T=0 F=251  T=0 F=733  case FORMAT_INTPTR:
  d=1   L1001  T=0 F=251  T=0 F=733  default:

[off-chain: 99 additional divergent branches across 6 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=6543e87c49a8de08, size=130 bytes, fuzzer=cmplog, trial=1, discovered_at=451s, mutation_op=ByteAddMutator,ByteAddMutator):
  0000: 00 01 00 00 00 19 57 53 00 54 3a 2f af 31 32 37   ......WS.T:/.127
  0010: 2e 30 23 30 2e 31 3a 39 30 30 31 2f 38 35 30 00   .0#0.1:9001/850.
  0020: 06 00 00 00 47 00 00 6f 6d 3a 20 6d 71 40 23 6f   ....G..om: mq@#o
  0030: 6d 65 77 68 65 72 65 25 0a 54 6f 3a 20 66 61 6b   mewhere%.To: fak
Seed 2 (id=d33356af10a98c7b, size=142 bytes, fuzzer=cmplog, trial=1, discovered_at=864s, mutation_op=BytesDeleteMutator,ByteIncMutator,WordInterestingMutator,BytesCopyMutator):
  0000: 00 01 00 00 00 19 70 6f 00 33 3a 2f 2f 50 cd 37   ......po.3://P.7
  0010: 2e 30 2e 30 6f 64 00 01 0a 00 75 75 38 35 30 00   .0.0od....uu850.
  0020: 09 00 00 00 47 6c 72 6f 6d 00 25 80 65 40 30 6f   ....Glrom.%.e@0o
  0030: 6d 65 77 68 65 72 65 00 00 05 6f 3a 20 66 61 6b   mewhere...o: fak
Seed 3 (id=d6a8509f695a5fee, size=142 bytes, fuzzer=cmplog, trial=1, discovered_at=928s, mutation_op=BitFlipMutator):
  0000: 00 01 00 00 00 19 70 6f 00 33 3a 7f 2f 31 cd c8   ......po.3:./1..
  0010: 00 30 2e ff 7f 00 00 01 0a 00 75 75 38 35 30 00   .0........uu850.
  0020: 06 00 00 00 47 43 50 48 3a 2f 2e 00 25 62 30 25   ....GCPH:/..%b0%
  0030: 63 a7 77 68 65 72 65 00 00 01 6f 00 25 66 61 00   c.where...o.%fa.
Seed 4 (id=c8217ad1a7ebff7b, size=142 bytes, fuzzer=cmplog, trial=1, discovered_at=931s, mutation_op=BytesCopyMutator,ByteDecMutator):
  0000: 00 01 00 00 00 19 70 6f 00 33 3a 7f 2f 31 cd c8   ......po.3:./1..
  0010: 00 30 2e ff 7f 00 00 01 0a 00 75 75 38 35 30 00   .0........uu850.
  0020: 06 00 00 00 47 43 50 48 3a 00 04 6e 25 65 72 00   ....GCPH:..n%er.
  0030: 09 00 00 00 05 00 00 6e 25 ad 72 00 06 00 00 00   .......n%.r.....
Seed 5 (id=2b297e9d5e12f897, size=144 bytes, fuzzer=cmplog, trial=1, discovered_at=7547s, mutation_op=ByteDecMutator,CrossoverReplaceMutator,ByteInterestingMutator,BytesSetMutator):
  0000: 00 01 00 00 00 19 70 6f 00 33 3a 2f 2f ad cd c8   ......po.3://...
  0010: 80 00 2e ff 7f 00 00 22 ad 00 35 2a 38 35 30 00   ......."..5*850.
  0020: 09 00 00 00 47 0a 50 68 3b 20 20 0a 20 5a 00 3b   ....G.Ph;  . Z.;
  0030: df ff 0d cd cd cd cd cd cd cd cd cd cd cd d9 cd   ................

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0024e5972fc0b2e0, size=35 bytes, fuzzer=naive, trial=1, discovered_at=88s, mutation_op=WordAddMutator):
  0000: 00 01 00 00 00 19 25 60 25 61 3e 66 9f 9f 63 25   ......%`%a>f..c%
  0010: 2b 5d 25 41 bf 41 41 41 41 40 41 41 5a 70 65 72   +]%A.AAAA@AAZper
  0020: 6d 69 74                                          mit
Seed 2 (id=00430153b42aa78b, size=35 bytes, fuzzer=naive, trial=1, discovered_at=175s, mutation_op=BytesDeleteMutator,ByteAddMutator):
  0000: 00 01 00 00 00 19 70 6b 73 65 2e 2e 2e 45 2e 41   ......pkse...E.A
  0010: 2e 2b 6b 73 65 4d 2e 2e 45 2b 2b 2b 2b 2b 2b 2b   .+kseM..E+++++++
  0020: 2b 55 6b                                          +Uk
Seed 3 (id=0036ed920052a1c1, size=35 bytes, fuzzer=naive, trial=1, discovered_at=626s, mutation_op=ByteIncMutator,ByteInterestingMutator):
  0000: 00 01 00 00 00 19 43 41 25 64 61 25 41 25 64 61   ......CA%da%A%da
  0010: 25 43 66 25 25 43 40 25 00 19 70 6b 2e 44 43 43   %Cf%%C@%..pk.DCC
  0020: 01 43 44                                          .CD
Seed 4 (id=004f868e7ea91716, size=36 bytes, fuzzer=naive, trial=1, discovered_at=3286s, mutation_op=ByteDecMutator,CrossoverInsertMutator,DwordInterestingMutator,BytesCopyMutator,BytesDeleteMutator,ByteNegMutator):
  0000: 00 01 00 00 00 19 26 41 41 25 25 29 25 62 25 29   ......&AA%%)%b%)
  0010: 25 62 2d 2d 2e 41 4b db 44 40 25 44 45 45 45 bb   %b--.AK.D@%DEEE.
  0020: 25 25 2a bb                                       %%*.
Seed 5 (id=003aec9151c3fdc7, size=34 bytes, fuzzer=naive, trial=1, discovered_at=6410s, mutation_op=ByteDecMutator):
  0000: 00 01 00 00 00 19 25 25 43 62 25 63 61 25 25 61   ......%%Cb%ca%%a
  0010: 25 42 25 61 25 40 42 25 94 00 00 00 64 64 ff 6c   %B%a%@B%....dd.l
  0020: 39 39                                             99


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0005  19(.)x5                             19(.)x7 25(%)x1 27(')x1 2d(-)x1     PARTIAL
   0x0006  70(p)x4 57(W)x1                     25(%)x3 43(C)x2 70(p)x1 26(&)x1 +3u  PARTIAL
   0x0007  6f(o)x4 53(S)x1                     41(A)x2 25(%)x2 60(`)x1 6b(k)x1 +4u  DIFFER
   0x0008  00(.)x5                             43(C)x3 25(%)x2 41(A)x2 73(s)x1 +2u  DIFFER
   0x0009  33(3)x4 54(T)x1                     25(%)x2 61(a)x1 65(e)x1 64(d)x1 +5u  DIFFER
   0x000a  3a(:)x5                             25(%)x5 3e(>)x1 2e(.)x1 61(a)x1 +2u  DIFFER
   0x000b  2f(/)x3 7f(.)x2                     25(%)x2 63(c)x2 66(f)x1 2e(.)x1 +4u  DIFFER
   0x000c  2f(/)x4 af(.)x1                     2e(.)x2 25(%)x2 9f(.)x1 41(A)x1 +4u  DIFFER
   0x000d  31(1)x3 50(P)x1 ad(.)x1             25(%)x2 9f(.)x1 45(E)x1 62(b)x1 +5u  DIFFER
   0x000e  cd(.)x4 32(2)x1                     25(%)x2 63(c)x1 2e(.)x1 64(d)x1 +5u  DIFFER
   0x000f  c8(.)x3 37(7)x2                     25(%)x2 41(A)x2 61(a)x2 29())x1 +3u  DIFFER
   0x0010  2e(.)x2 00(.)x2 80(.)x1             25(%)x4 2b(+)x1 2e(.)x1 52(R)x1 +3u  PARTIAL
   0x0011  30(0)x4 00(.)x1                     25(%)x2 5d(])x1 2b(+)x1 43(C)x1 +5u  DIFFER
   0x0012  2e(.)x4 23(#)x1                     25(%)x3 66(f)x2 6b(k)x1 2d(-)x1 +3u  DIFFER
   0x0013  ff(.)x3 30(0)x2                     25(%)x3 41(A)x2 2d(-)x2 73(s)x1 +2u  DIFFER
   0x0014  7f(.)x3 2e(.)x1 6f(o)x1             25(%)x2 bf(.)x1 65(e)x1 2e(.)x1 +5u  PARTIAL
   0x0015  00(.)x3 31(1)x1 64(d)x1             41(A)x3 25(%)x3 4d(M)x1 43(C)x1 +2u  DIFFER
   0x0016  00(.)x4 3a(:)x1                     41(A)x2 25(%)x2 2e(.)x1 40(@)x1 +4u  DIFFER
   0x0017  01(.)x3 39(9)x1 22(")x1             25(%)x3 41(A)x2 2e(.)x1 db(.)x1 +3u  DIFFER
   0x0018  0a(.)x3 30(0)x1 ad(.)x1             45(E)x2 43(C)x2 41(A)x1 00(.)x1 +4u  DIFFER
   0x0019  00(.)x4 30(0)x1                     40(@)x2 2b(+)x1 19(.)x1 00(.)x1 +5u  PARTIAL
   0x001a  75(u)x3 31(1)x1 35(5)x1             25(%)x5 41(A)x1 2b(+)x1 70(p)x1 +2u  DIFFER
   0x001b  75(u)x3 2f(/)x1 2a(*)x1             00(.)x2 41(A)x1 2b(+)x1 6b(k)x1 +5u  DIFFER
   0x001c  38(8)x5                             45(E)x2 5a(Z)x1 2b(+)x1 2e(.)x1 +5u  DIFFER
   0x001d  35(5)x5                             70(p)x1 2b(+)x1 44(D)x1 45(E)x1 +6u  DIFFER
   0x001e  30(0)x5                             65(e)x1 2b(+)x1 43(C)x1 45(E)x1 +6u  DIFFER
   0x001f  00(.)x5                             41(A)x2 72(r)x1 2b(+)x1 43(C)x1 +5u  DIFFER
   0x0020  06(.)x3 09(.)x2                     6d(m)x1 2b(+)x1 01(.)x1 25(%)x1 +6u  DIFFER
   0x0021  00(.)x5                             25(%)x2 2d(-)x2 69(i)x1 55(U)x1 +3u  DIFFER
   0x0022  00(.)x5                             44(D)x2 74(t)x1 6b(k)x1 2a(*)x1 +3u  DIFFER
   0x0023  00(.)x5                             bb(.)x1 4c(L)x1 25(%)x1 2d(-)x1     DIFFER
   0x0024  47(G)x5                             50(P)x2 25(%)x1                     DIFFER
   0x0025  43(C)x2 00(.)x1 6c(l)x1 0a(.)x1     25(%)x1 41(A)x1 2e(.)x1             DIFFER
   0x0026  50(P)x3 00(.)x1 72(r)x1             25(%)x1 66(f)x1 67(g)x1             DIFFER
   0x0027  6f(o)x2 48(H)x2 68(h)x1             40(@)x1 25(%)x1 2d(-)x1             DIFFER
   0x0028  6d(m)x2 3a(:)x2 3b(;)x1             25(%)x1 44(D)x1 50(P)x1             DIFFER
   0x0029  00(.)x2 3a(:)x1 2f(/)x1 20( )x1     25(%)x1 66(f)x1 2d(-)x1             DIFFER
   0x002a  20( )x2 25(%)x1 2e(.)x1 04(.)x1     25(%)x2 44(D)x1                     PARTIAL
   0x002b  6d(m)x1 80(.)x1 00(.)x1 6e(n)x1 +1u  25(%)x2 2e(.)x1                     DIFFER
   0x002c  25(%)x2 71(q)x1 65(e)x1 20( )x1     d2(.)x1 43(C)x1 65(e)x1             PARTIAL
   ... (9 more divergent offsets)
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  prompts_b/curl_289.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 289,
  "target": "curl",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 289 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 289 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 289 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).