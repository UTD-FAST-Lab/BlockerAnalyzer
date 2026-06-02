==== BLOCKER ====
Target: libpng
Branch ID: 4020
Location: /src/libpng/pngrutil.c:2180:8
Enclosing function: OSS_FUZZ_png_handle_pHYs
Source line:    if (length != 9)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            4        6          0  REFERENCE
cmplog                          10        0          0  REFERENCE
value_profile                    1        9          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                       10        0          0  REFERENCE
naive_ngram4                     2        8          0  REFERENCE
mopt                             4        6          0  REFERENCE
minimizer                        2        8          0  REFERENCE
fast                             3        7          0  REFERENCE
grimoire                         9        1          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 24  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=0.30h  loser=21.70h
  avg hitcount on branch: winner=103  loser=0
  prob_div=0.90  dur_div=21.40h  hit_div=103
  subject-level: delta_AUC=13087800.0  p_AUC=0.0002  delta_Final=135.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/4020/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_handle_pHYs (/src/libpng/pngrutil.c:2156-2196) ---
[ ]  2154  void /* PRIVATE */
[ ]  2155  png_handle_pHYs(png_structrp png_ptr, png_inforp info_ptr, png_uint_32 length)
[B]  2156  {
[B]  2157     png_byte buf[9];
[B]  2158     png_uint_32 res_x, res_y;
[B]  2159     int unit_type;
[ ]  2160  
[B]  2161     png_debug(1, "in png_handle_pHYs");
[ ]  2162  
[B]  2163     if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
[ ]  2164        png_chunk_error(png_ptr, "missing IHDR");
[ ]  2165  
[B]  2166     else if ((png_ptr->mode & PNG_HAVE_IDAT) != 0)
[ ]  2167     {
[ ]  2168        png_crc_finish(png_ptr, length);
[ ]  2169        png_chunk_benign_error(png_ptr, "out of place");
[ ]  2170        return;
[ ]  2171     }
[ ]  2172  
[B]  2173     else if (info_ptr != NULL && (info_ptr->valid & PNG_INFO_pHYs) != 0)
[L]  2174     {
[L]  2175        png_crc_finish(png_ptr, length);
[L]  2176        png_chunk_benign_error(png_ptr, "duplicate");
[L]  2177        return;
[L]  2178     }
[ ]  2179  
[B]  2180     if (length != 9) <-- BLOCKER
[W]  2181     {
[W]  2182        png_crc_finish(png_ptr, length);
[W]  2183        png_chunk_benign_error(png_ptr, "invalid");
[W]  2184        return;
[W]  2185     }
[ ]  2186  
[B]  2187     png_crc_read(png_ptr, buf, 9);
[ ]  2188  
[B]  2189     if (png_crc_finish(png_ptr, 0) != 0)
[ ]  2190        return;
[ ]  2191  
[B]  2192     res_x = png_get_uint_32(buf);
[B]  2193     res_y = png_get_uint_32(buf + 4);
[B]  2194     unit_type = buf[8];
[B]  2195     png_set_pHYs(png_ptr, info_ptr, res_x, res_y, unit_type);
[B]  2196  }

--- No 1-hop callers of OSS_FUZZ_png_handle_pHYs fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0      4270  OSS_FUZZ_png_read_finish_row  (/src/libpng/pngrutil.c:4328-4388)
       0       597  OSS_FUZZ_png_zlib_inflate  (/src/libpng/pngrutil.c:454-467)
       0       571  OSS_FUZZ_png_read_IDAT_data  (/src/libpng/pngrutil.c:4152-4276)
       0       560  OSS_FUZZ_png_combine_row  (/src/libpng/pngrutil.c:3202-3681)
       0       560  OSS_FUZZ_png_do_read_interlace  (/src/libpng/pngrutil.c:3687-3928)
       0        54  OSS_FUZZ_png_read_filter_row  (/src/libpng/pngrutil.c:4134-4146)
       0        34  pngrutil.c:png_read_filter_row_avg  (/src/libpng/pngrutil.c:3968-3990)
      14        47  OSS_FUZZ_png_handle_unknown  (/src/libpng/pngrutil.c:2925-3120)
      22         0  OSS_FUZZ_png_handle_sPLT  (/src/libpng/pngrutil.c:1641-1811)
       2        18  OSS_FUZZ_png_handle_bKGD  (/src/libpng/pngrutil.c:1921-2033)
       6        22  OSS_FUZZ_png_handle_pCAL  (/src/libpng/pngrutil.c:2249-2371)
       0        16  pngrutil.c:png_read_filter_row_paeth_1byte_pixel  (/src/libpng/pngrutil.c:3995-4041)
       0        12  pngrutil.c:png_inflate_claim  (/src/libpng/pngrutil.c:342-443)
      11         0  OSS_FUZZ_png_handle_hIST  (/src/libpng/pngrutil.c:2103-2150)
       0        11  OSS_FUZZ_png_read_start_row  (/src/libpng/pngrutil.c:4393-4680)
... (13 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_handle_pHYs  (/src/libpng/pngrutil.c:2156-2196) ---
  d=1   L2173  T=0 F=21  T=1 F=13  else if (info_ptr != NULL && (info_ptr->valid & PNG_INFO_...
  d=1   L2180  T=15 F=6  T=0 F=13  if (length != 9)  <-- BLOCKER
  d=1   L2189  T=0 F=6  T=0 F=13  if (png_crc_finish(png_ptr, 0) != 0)

[off-chain: 321 additional divergent branches across 39 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=60e9d782d27cdf4b, size=1111 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=6s, mutation_op=BitFlipMutator,BytesDeleteMutator,BytesCopyMutator,TokenInsert,BytesSetMutator,BytesDeleteMutator,ByteFlipMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=0997284f41d33d90, size=6629 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=8s, mutation_op=ByteNegMutator,QwordAddMutator,CrossoverReplaceMutator,BytesRandSetMutator,BytesExpandMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 70 48 59 73 00 00 b1 8f 0b fc 61   .....pHYs......a
  0030: 05 00 00 00 01 69 54 58 74 01 d9 c9 2c 7f 00 00   .....iTXt...,...
Seed 3 (id=1ace8e9e5c39d6f1, size=1111 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=9s, mutation_op=BitFlipMutator,BytesCopyMutator,BytesDeleteMutator,BytesDeleteMutator,BytesSetMutator,BytesExpandMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=2662b8644a55512f, size=1111 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=9s, mutation_op=BitFlipMutator,BytesCopyMutator,BytesDeleteMutator,BytesDeleteMutator,BytesSetMutator,BytesExpandMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 00   .....gAMA.......
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=1880c3d2372fd21a, size=6629 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=18s, mutation_op=DwordInterestingMutator,TokenReplace,BytesSetMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=024188c1a0b8a2c2, size=9727 bytes, fuzzer=value_profile, trial=1, discovered_at=15s, mutation_op=ByteNegMutator,ByteAddMutator,ByteNegMutator,BytesSetMutator,TokenReplace):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 10 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 3a 3a 3a   .....gAMA....:::
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=012870f9afb207c8, size=8759 bytes, fuzzer=value_profile, trial=1, discovered_at=65s, mutation_op=TokenReplace,ByteFlipMutator,WordInterestingMutator,ByteFlipMutator,ByteNegMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 01 08 06 00 00 01 52 ed aa   ...[.........R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=00240036e293ba45, size=8818 bytes, fuzzer=value_profile, trial=1, discovered_at=562s, mutation_op=DwordInterestingMutator,BytesInsertMutator,ByteIncMutator,TokenInsert,WordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 20 00 00 00 01 08 06 00 00 01 52 ed aa   ... .........R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=012c5d33511f6e6b, size=9304 bytes, fuzzer=value_profile, trial=1, discovered_at=2703s, mutation_op=QwordAddMutator,BytesInsertCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 52 00 00 80 00 04 00 00 00 01 52 ed aa   ...R.........R..
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
   0x0013  5b([)x15                            5b([)x4 51(Q)x2 20( )x1 52(R)x1 +5u  PARTIAL
   0x0016  00(.)x15                            00(.)x6 80(.)x4 a1(.)x2 01(.)x1     PARTIAL
   0x0017  45(E)x15                            00(.)x4 45(E)x3 01(.)x3 86(.)x2 +1u  PARTIAL
   0x0018  08(.)x14 01(.)x1                    08(.)x5 04(.)x3 10(.)x2 02(.)x2 +1u  PARTIAL
   0x0025  67(g)x14 70(p)x1                    67(g)x12 66(f)x1                    PARTIAL
   0x0026  41(A)x14 48(H)x1                    41(A)x13                            PARTIAL
   0x0027  4d(M)x14 59(Y)x1                    4d(M)x13                            PARTIAL
   0x0028  41(A)x14 73(s)x1                    41(A)x13                            PARTIAL
   0x002d  0b(.)x15                            0b(.)x12 3a(:)x1                    PARTIAL
   0x002e  fc(.)x15                            fc(.)x12 3a(:)x1                    PARTIAL
   0x002f  61(a)x8 00(.)x7                     61(a)x12 3a(:)x1                    PARTIAL
   0x0030  05(.)x15                            05(.)x12 fb(.)x1                    PARTIAL
   0x0035  73(s)x14 69(i)x1                    73(s)x13                            PARTIAL
   0x0036  52(R)x14 54(T)x1                    52(R)x13                            PARTIAL
   0x0037  47(G)x14 58(X)x1                    47(G)x13                            PARTIAL
   0x0038  42(B)x14 74(t)x1                    42(B)x13                            PARTIAL
   0x003b  c9(.)x14 d9(.)x1                    c9(.)x13                            PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_4020.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 4020,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 4020 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 4020 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 4020 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).