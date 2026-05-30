==== BLOCKER ====
Target: libpng
Branch ID: 4072
Location: /src/libpng/pngrutil.c:4245:47
Enclosing function: OSS_FUZZ_png_read_IDAT_data
Source line:          if (png_ptr->zstream.avail_in > 0 || png_ptr->idat_size > 0)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (ctx_coverage vs naive_ctx)
cmplog                           0        7          3  REFERENCE
value_profile                    8        2          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             0       10          0  loser (I2S vs value_profile)
naive_ctx                        1        9          0  loser (ctx_coverage vs naive)
naive_ngram4                     8        2          0  REFERENCE
mopt                             6        4          0  REFERENCE
minimizer                        3        4          3  REFERENCE
fast                             2        5          3  REFERENCE
grimoire                         2        8          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > naive_ctx  [delta: ctx_coverage] ---
  subject 25  (naive_ctx vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=2.70h  loser=21.80h
  avg hitcount on branch: winner=1  loser=0
  prob_div=0.90  dur_div=19.10h  hit_div=1
  subject-level: delta_AUC=6413040.0  p_AUC=0.0003  delta_Final=91.4  p_final=0.0002
--- Pair 2: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 24  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=10.70h  loser=23.10h
  avg hitcount on branch: winner=1  loser=0
  prob_div=0.80  dur_div=12.40h  hit_div=1
  subject-level: delta_AUC=13087800.0  p_AUC=0.0002  delta_Final=135.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/4072/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_read_IDAT_data (/src/libpng/pngrutil.c:4152-4276) ---
[ ]  4150  png_read_IDAT_data(png_structrp png_ptr, png_bytep output,
[ ]  4151      png_alloc_size_t avail_out)
[B]  4152  {
[ ]  4153     /* Loop reading IDATs and decompressing the result into output[avail_out] */
[B]  4154     png_ptr->zstream.next_out = output;
[B]  4155     png_ptr->zstream.avail_out = 0; /* safety: set below */
[ ]  4156  
[B]  4157     if (output == NULL)
[B]  4158        avail_out = 0;
[ ]  4159  
[B]  4160     do
[B]  4161     {
[B]  4162        int ret;
[B]  4163        png_byte tmpbuf[PNG_INFLATE_BUF_SIZE];
[ ]  4164  
[B]  4165        if (png_ptr->zstream.avail_in == 0)
[B]  4166        {
[B]  4167           uInt avail_in;
[B]  4168           png_bytep buffer;
[ ]  4169  
[B]  4170           while (png_ptr->idat_size == 0)
[ ]  4171           {
[ ]  4172              png_crc_finish(png_ptr, 0);
[ ]  4173  
[ ]  4174              png_ptr->idat_size = png_read_chunk_header(png_ptr);
[ ]  4175              /* This is an error even in the 'check' case because the code just
[ ]  4176               * consumed a non-IDAT header.
[ ]  4177               */
[ ]  4178              if (png_ptr->chunk_name != png_IDAT)
[ ]  4179                 png_error(png_ptr, "Not enough image data");
[ ]  4180           }
[ ]  4181  
[B]  4182           avail_in = png_ptr->IDAT_read_size;
[ ]  4183  
[B]  4184           if (avail_in > png_ptr->idat_size)
[L]  4185              avail_in = (uInt)png_ptr->idat_size;
[ ]  4186  
[ ]  4187           /* A PNG with a gradually increasing IDAT size will defeat this attempt
[ ]  4188            * to minimize memory usage by causing lots of re-allocs, but
[ ]  4189            * realistically doing IDAT_read_size re-allocs is not likely to be a
[ ]  4190            * big problem.
[ ]  4191            */
[B]  4192           buffer = png_read_buffer(png_ptr, avail_in, 0/*error*/);
[ ]  4193  
[B]  4194           png_crc_read(png_ptr, buffer, avail_in);
[B]  4195           png_ptr->idat_size -= avail_in;
[ ]  4196  
[B]  4197           png_ptr->zstream.next_in = buffer;
[B]  4198           png_ptr->zstream.avail_in = avail_in;
[B]  4199        }
[ ]  4200  
[ ]  4201        /* And set up the output side. */
[B]  4202        if (output != NULL) /* standard read */
[B]  4203        {
[B]  4204           uInt out = ZLIB_IO_MAX;
[ ]  4205  
[B]  4206           if (out > avail_out)
[B]  4207              out = (uInt)avail_out;
[ ]  4208  
[B]  4209           avail_out -= out;
[B]  4210           png_ptr->zstream.avail_out = out;
[B]  4211        }
[ ]  4212  
[B]  4213        else /* after last row, checking for end */
[B]  4214        {
[B]  4215           png_ptr->zstream.next_out = tmpbuf;
[B]  4216           png_ptr->zstream.avail_out = (sizeof tmpbuf);
[B]  4217        }
[ ]  4218  
[ ]  4219        /* Use NO_FLUSH; this gives zlib the maximum opportunity to optimize the
[ ]  4220         * process.  If the LZ stream is truncated the sequential reader will
[ ]  4221         * terminally damage the stream, above, by reading the chunk header of the
[ ]  4222         * following chunk (it then exits with png_error).
[ ]  4223         *
[ ]  4224         * TODO: deal more elegantly with truncated IDAT lists.
[ ]  4225         */
[B]  4226        ret = PNG_INFLATE(png_ptr, Z_NO_FLUSH);
[ ]  4227  
[ ]  4228        /* Take the unconsumed output back. */
[B]  4229        if (output != NULL)
[B]  4230           avail_out += png_ptr->zstream.avail_out;
[ ]  4231  
[B]  4232        else /* avail_out counts the extra bytes */
[B]  4233           avail_out += (sizeof tmpbuf) - png_ptr->zstream.avail_out;
[ ]  4234  
[B]  4235        png_ptr->zstream.avail_out = 0;
[ ]  4236  
[B]  4237        if (ret == Z_STREAM_END)
[B]  4238        {
[ ]  4239           /* Do this for safety; we won't read any more into this row. */
[B]  4240           png_ptr->zstream.next_out = NULL;
[ ]  4241  
[B]  4242           png_ptr->mode |= PNG_AFTER_IDAT;
[B]  4243           png_ptr->flags |= PNG_FLAG_ZSTREAM_ENDED;
[ ]  4244  
[B]  4245           if (png_ptr->zstream.avail_in > 0 || png_ptr->idat_size > 0) <-- BLOCKER
[W]  4246              png_chunk_benign_error(png_ptr, "Extra compressed data");
[B]  4247           break;
[B]  4248        }
[ ]  4249  
[B]  4250        if (ret != Z_OK)
[ ]  4251        {
[ ]  4252           png_zstream_error(png_ptr, ret);
[ ]  4253  
[ ]  4254           if (output != NULL)
[ ]  4255              png_chunk_error(png_ptr, png_ptr->zstream.msg);
[ ]  4256  
[ ]  4257           else /* checking */
[ ]  4258           {
[ ]  4259              png_chunk_benign_error(png_ptr, png_ptr->zstream.msg);
[ ]  4260              return;
[ ]  4261           }
[ ]  4262        }
[B]  4263     } while (avail_out > 0);
[ ]  4264  
[B]  4265     if (avail_out > 0)
[B]  4266     {
[ ]  4267        /* The stream ended before the image; this is the same as too few IDATs so
[ ]  4268         * should be handled the same way.
[ ]  4269         */
[B]  4270        if (output != NULL)
[B]  4271           png_error(png_ptr, "Not enough image data");
[ ]  4272  
[B]  4273        else /* the deflate stream contained extra data */
[B]  4274           png_chunk_benign_error(png_ptr, "Too much image data");
[B]  4275     }
[B]  4276  }

--- No 1-hop callers of OSS_FUZZ_png_read_IDAT_data fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     490     10100  OSS_FUZZ_png_read_finish_row  (/src/libpng/pngrutil.c:4328-4388)
     137      2760  OSS_FUZZ_png_zlib_inflate  (/src/libpng/pngrutil.c:454-467)
     136      2750  OSS_FUZZ_png_read_IDAT_data  (/src/libpng/pngrutil.c:4152-4276)  <-- enclosing
     132      2740  OSS_FUZZ_png_combine_row  (/src/libpng/pngrutil.c:3202-3681)
     106      2190  OSS_FUZZ_png_read_filter_row  (/src/libpng/pngrutil.c:4134-4146)
      97      2029  OSS_FUZZ_png_do_read_interlace  (/src/libpng/pngrutil.c:3687-3928)
      50      1040  pngrutil.c:png_read_filter_row_up  (/src/libpng/pngrutil.c:3952-3963)
      36       660  pngrutil.c:png_read_filter_row_paeth_multibyte_pixel  (/src/libpng/pngrutil.c:4046-4092)
      62       627  OSS_FUZZ_png_crc_read  (/src/libpng/pngrutil.c:197-203)
      68       398  OSS_FUZZ_png_get_uint_31  (/src/libpng/pngrutil.c:23-30)
      60       358  OSS_FUZZ_png_read_chunk_header  (/src/libpng/pngrutil.c:157-192)
      60       354  OSS_FUZZ_png_check_chunk_name  (/src/libpng/pngrutil.c:3136-3151)
      60       350  OSS_FUZZ_png_check_chunk_length  (/src/libpng/pngrutil.c:3155-3191)
      57       345  OSS_FUZZ_png_crc_finish  (/src/libpng/pngrutil.c:212-245)
      56       342  OSS_FUZZ_png_crc_error  (/src/libpng/pngrutil.c:252-285)
... (30 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_read_IDAT_data  (/src/libpng/pngrutil.c:4152-4276) ---
  d=1   L4157  T=1 F=135  T=1 F=2750  if (output == NULL)
  d=1   L4165  T=5 F=132  T=21 F=2730  if (png_ptr->zstream.avail_in == 0)
  d=1   L4170  T=0 F=5  T=0 F=21  while (png_ptr->idat_size == 0)
  d=1   L4184  T=0 F=5  T=21 F=0  if (avail_in > png_ptr->idat_size)
  d=1   L4202  T=136 F=1  T=2750 F=1  if (output != NULL) /* standard read */
  d=1   L4206  T=136 F=0  T=2750 F=0  if (out > avail_out)
  d=1   L4229  T=136 F=1  T=2750 F=1  if (output != NULL)
  d=1   L4237  T=4 F=133  T=21 F=2730  if (ret == Z_STREAM_END)
  d=1   L4245  T=4 F=0  T=0 F=21  if (png_ptr->zstream.avail_in > 0 || png_ptr->idat_size > 0)  <-- BLOCKER
  d=1   L4245  T=0 F=4  T=0 F=21  if (png_ptr->zstream.avail_in > 0 || png_ptr->idat_size > 0)  <-- BLOCKER
  d=1   L4250  T=0 F=133  T=0 F=2730  if (ret != Z_OK)
  d=1   L4263  T=1 F=132  T=0 F=2730  } while (avail_out > 0);
  d=1   L4265  T=4 F=132  T=3 F=2740  if (avail_out > 0)

[off-chain: 322 additional divergent branches across 43 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=7bc940e72a5dbe0c, size=8832 bytes, fuzzer=naive, trial=1, discovered_at=12240s, mutation_op=BytesDeleteMutator,BytesRandInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 01 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=7bd9db8c471916c1, size=8832 bytes, fuzzer=value_profile, trial=1, discovered_at=17155s, mutation_op=BytesDeleteMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 02 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=6aec768cba0b78a6, size=8832 bytes, fuzzer=value_profile, trial=1, discovered_at=38780s, mutation_op=ByteDecMutator,CrossoverInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 46 08 06 00 00 01 52 ed aa   ...[...F.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=6ee6e91083da0412, size=17024 bytes, fuzzer=value_profile, trial=1, discovered_at=40848s, mutation_op=BytesInsertCopyMutator,BytesDeleteMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 02 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=044467da0a43d8a1, size=8555 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=05ad30e9130d1008, size=8759 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=146cf13dbd444ee9, size=8700 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=2436ea06f9c62bfc, size=8555 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=4869be6b690aecbf, size=8763 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0011  02(.)x2 01(.)x1 00(.)x1             00(.)x21                            PARTIAL
   0x0017  45(E)x3 46(F)x1                     45(E)x21                            PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_4072.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 4072,
  "target": "libpng",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>naive_ctx (ctx_coverage), value_profile>value_profile_cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 4072 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 4072 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 4072 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).