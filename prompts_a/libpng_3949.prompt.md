==== BLOCKER ====
Target: libpng
Branch ID: 3949
Location: /src/libpng/pngrutil.c:847:8
Enclosing function: OSS_FUZZ_png_handle_IHDR
Source line:    if ((png_ptr->mode & PNG_HAVE_IHDR) != 0)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            4        6          0  REFERENCE
cmplog                           9        1          0  REFERENCE
value_profile                    1        9          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                       10        0          0  REFERENCE
naive_ngram4                     4        6          0  REFERENCE
mopt                             5        5          0  REFERENCE
minimizer                        6        4          0  REFERENCE
fast                             4        6          0  REFERENCE
grimoire                         5        5          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 24  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=3.00h  loser=21.60h
  avg hitcount on branch: winner=20  loser=0
  prob_div=0.90  dur_div=18.60h  hit_div=19
  subject-level: delta_AUC=13087800.0  p_AUC=0.0002  delta_Final=135.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3949/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_handle_IHDR (/src/libpng/pngrutil.c:839-908) ---
[ ]   837  void /* PRIVATE */
[ ]   838  png_handle_IHDR(png_structrp png_ptr, png_inforp info_ptr, png_uint_32 length)
[B]   839  {
[B]   840     png_byte buf[13];
[B]   841     png_uint_32 width, height;
[B]   842     int bit_depth, color_type, compression_type, filter_type;
[B]   843     int interlace_type;
[ ]   844  
[B]   845     png_debug(1, "in png_handle_IHDR");
[ ]   846  
[B]   847     if ((png_ptr->mode & PNG_HAVE_IHDR) != 0) <-- BLOCKER
[W]   848        png_chunk_error(png_ptr, "out of place");
[ ]   849  
[ ]   850     /* Check the length */
[B]   851     if (length != 13)
[ ]   852        png_chunk_error(png_ptr, "invalid");
[ ]   853  
[B]   854     png_ptr->mode |= PNG_HAVE_IHDR;
[ ]   855  
[B]   856     png_crc_read(png_ptr, buf, 13);
[B]   857     png_crc_finish(png_ptr, 0);
[ ]   858  
[B]   859     width = png_get_uint_31(png_ptr, buf);
[B]   860     height = png_get_uint_31(png_ptr, buf + 4);
[B]   861     bit_depth = buf[8];
[B]   862     color_type = buf[9];
[B]   863     compression_type = buf[10];
[B]   864     filter_type = buf[11];
[B]   865     interlace_type = buf[12];
[ ]   866  
[ ]   867     /* Set internal variables */
[B]   868     png_ptr->width = width;
[B]   869     png_ptr->height = height;
[B]   870     png_ptr->bit_depth = (png_byte)bit_depth;
[B]   871     png_ptr->interlaced = (png_byte)interlace_type;
[B]   872     png_ptr->color_type = (png_byte)color_type;
[B]   873  #ifdef PNG_MNG_FEATURES_SUPPORTED
[B]   874     png_ptr->filter_type = (png_byte)filter_type;
[B]   875  #endif
[B]   876     png_ptr->compression_type = (png_byte)compression_type;
[ ]   877  
[ ]   878     /* Find number of channels */
[B]   879     switch (png_ptr->color_type)
[B]   880     {
[ ]   881        default: /* invalid, png_set_IHDR calls png_error */
[B]   882        case PNG_COLOR_TYPE_GRAY:
[B]   883        case PNG_COLOR_TYPE_PALETTE:
[B]   884           png_ptr->channels = 1;
[B]   885           break;
[ ]   886  
[ ]   887        case PNG_COLOR_TYPE_RGB:
[ ]   888           png_ptr->channels = 3;
[ ]   889           break;
[ ]   890  
[ ]   891        case PNG_COLOR_TYPE_GRAY_ALPHA:
[ ]   892           png_ptr->channels = 2;
[ ]   893           break;
[ ]   894  
[B]   895        case PNG_COLOR_TYPE_RGB_ALPHA:
[B]   896           png_ptr->channels = 4;
[B]   897           break;
[B]   898     }
[ ]   899  
[ ]   900     /* Set up other useful info */
[B]   901     png_ptr->pixel_depth = (png_byte)(png_ptr->bit_depth * png_ptr->channels);
[B]   902     png_ptr->rowbytes = PNG_ROWBYTES(png_ptr->pixel_depth, png_ptr->width);
[B]   903     png_debug1(3, "bit_depth = %d", png_ptr->bit_depth);
[B]   904     png_debug1(3, "channels = %d", png_ptr->channels);
[B]   905     png_debug1(3, "rowbytes = %lu", (unsigned long)png_ptr->rowbytes);
[B]   906     png_set_IHDR(png_ptr, info_ptr, width, height, bit_depth,
[B]   907         color_type, interlace_type, compression_type, filter_type);
[B]   908  }

--- No 1-hop callers of OSS_FUZZ_png_handle_IHDR fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     110         0  OSS_FUZZ_png_read_filter_row  (/src/libpng/pngrutil.c:4134-4146)
      52         0  pngrutil.c:png_read_filter_row_up  (/src/libpng/pngrutil.c:3952-3963)
      33         0  pngrutil.c:png_read_filter_row_paeth_multibyte_pixel  (/src/libpng/pngrutil.c:4046-4092)
      15         0  pngrutil.c:png_read_filter_row_sub  (/src/libpng/pngrutil.c:3934-3947)
      10         0  pngrutil.c:png_read_filter_row_avg  (/src/libpng/pngrutil.c:3968-3990)
       6         2  OSS_FUZZ_png_read_finish_IDAT  (/src/libpng/pngrutil.c:4280-4324)
       2         0  OSS_FUZZ_png_handle_sPLT  (/src/libpng/pngrutil.c:1641-1811)
       2         0  OSS_FUZZ_png_handle_iTXt  (/src/libpng/pngrutil.c:2715-2858)
       1         0  OSS_FUZZ_png_handle_hIST  (/src/libpng/pngrutil.c:2103-2150)
       1         0  pngrutil.c:png_init_filter_functions  (/src/libpng/pngrutil.c:4105-4129)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_handle_IHDR  (/src/libpng/pngrutil.c:839-908) ---
  d=1   L 847  T=10 F=10  T=0 F=10  if ((png_ptr->mode & PNG_HAVE_IHDR) != 0)  <-- BLOCKER

[off-chain: 136 additional divergent branches across 31 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=0bb540212fef4c2a, size=1564 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=5s, mutation_op=BytesCopyMutator,ByteFlipMutator,ByteFlipMutator,ByteFlipMutator,BytesInsertCopyMutator,BytesRandInsertMutator,ByteAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=5197665af4970fae, size=1111 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=32s, mutation_op=BytesDeleteMutator,BytesRandInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 73 52 47 42 00 00 b1 8f 0b fc 61   .....sRGB......a
  0030: 05 00 00 00 01 6f 46 46 73 01 d9 c9 2c 7f 00 00   .....oFFs...,...
Seed 3 (id=689f01263c448879, size=8759 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=52s, mutation_op=BytesInsertCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=2dda2e4f022d63c3, size=8759 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=135s, mutation_op=BytesRandSetMutator,WordInterestingMutator,BytesSwapMutator,BytesSetMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 04 00 00 00 0b 08 00 00 00 01 52 ed aa   .............R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 04 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=9093cd3302d76c9e, size=8759 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=224s, mutation_op=BytesInsertCopyMutator,WordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 00 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00c64a8985930929, size=433 bytes, fuzzer=value_profile, trial=1, discovered_at=0s, mutation_op=BytesSetMutator,QwordAddMutator,BytesCopyMutator,ByteFlipMutator,TokenReplace):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 74 52 47 42 01 d9 c9 2c 7f 00 00   .....tRGB...,...
Seed 2 (id=00793532ef09f446, size=269 bytes, fuzzer=value_profile, trial=1, discovered_at=14s, mutation_op=CrossoverReplaceMutator,ByteDecMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 0f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 41 01 f5 c9 2c 7f 00 00   .....sRGA...,...
Seed 3 (id=009a34a8f7375590, size=2610 bytes, fuzzer=value_profile, trial=1, discovered_at=15s, mutation_op=DwordAddMutator,QwordAddMutator,CrossoverInsertMutator,BytesDeleteMutator,ByteInterestingMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=00240036e293ba45, size=8818 bytes, fuzzer=value_profile, trial=1, discovered_at=562s, mutation_op=DwordInterestingMutator,BytesInsertMutator,ByteIncMutator,TokenInsert,WordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 20 00 00 00 01 08 06 00 00 01 52 ed aa   ... .........R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=005d3e4b5b80440b, size=9099 bytes, fuzzer=value_profile, trial=1, discovered_at=4461s, mutation_op=BytesSetMutator,QwordAddMutator,BytesCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 22 00 00 a1 86 02 00 00 00 01 52 ed aa   ...".........R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0013  5b([)x8 04(.)x2                     5b([)x6 51(Q)x2 20( )x1 22(")x1     PARTIAL
   0x0016  00(.)x10                            00(.)x7 a1(.)x2 80(.)x1             PARTIAL
   0x0017  45(E)x8 0b(.)x2                     45(E)x6 86(.)x2 01(.)x1 00(.)x1     PARTIAL
   0x0018  08(.)x10                            08(.)x7 02(.)x2 04(.)x1             PARTIAL
   0x001c  01(.)x7 00(.)x3                     01(.)x10                            PARTIAL
   0x0025  67(g)x9 73(s)x1                     67(g)x10                            PARTIAL
   0x0026  41(A)x9 52(R)x1                     41(A)x10                            PARTIAL
   0x0027  4d(M)x9 47(G)x1                     4d(M)x10                            PARTIAL
   0x0028  41(A)x9 42(B)x1                     41(A)x10                            PARTIAL
   0x002a  00(.)x9 86(.)x1                     00(.)x10                            PARTIAL
   0x002b  b1(.)x9 86(.)x1                     b1(.)x9 b2(.)x1                     PARTIAL
   0x002c  8f(.)x9 86(.)x1                     8f(.)x9 0f(.)x1                     PARTIAL
   0x002d  0b(.)x9 86(.)x1                     0b(.)x10                            PARTIAL
   0x002e  fc(.)x9 86(.)x1                     fc(.)x10                            PARTIAL
   0x002f  61(a)x9 86(.)x1                     61(a)x10                            PARTIAL
   0x0030  05(.)x7 04(.)x2 86(.)x1             05(.)x10                            PARTIAL
   0x0035  73(s)x8 6f(o)x1 74(t)x1             73(s)x9 74(t)x1                     PARTIAL
   0x0036  52(R)x8 46(F)x1 49(I)x1             52(R)x10                            PARTIAL
   0x0037  47(G)x8 46(F)x1 4d(M)x1             47(G)x9 64(d)x1                     PARTIAL
   0x0038  42(B)x8 73(s)x1 45(E)x1             42(B)x9 41(A)x1                     PARTIAL
   0x003a  d9(.)x10                            d9(.)x9 f5(.)x1                     PARTIAL
==== MECHANISM CONTEXT (involved fuzzers only) ====
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
  /home/miao/BlockerAnalyzer/prompts/libpng_3949.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3949,
  "target": "libpng",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3949 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3949 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3949 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).