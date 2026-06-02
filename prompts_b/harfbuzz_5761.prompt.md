==== BLOCKER ====
Target: harfbuzz
Branch ID: 5761
Location: /src/harfbuzz/src/hb-ot-shaper-arabic-joining-list.hh:32:5
Enclosing function: hb-ot-shaper-use.cc:has_arabic_joining(hb_script_t)
Source line:     case HB_SCRIPT_OLD_UYGHUR:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  REFERENCE
cmplog                           4        6          0  REFERENCE
value_profile                   10        0          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             1        9          0  loser (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         7        3          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=0.70h  loser=22.00h
  avg hitcount on branch: winner=26  loser=0
  prob_div=0.90  dur_div=21.30h  hit_div=26
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5761/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-use.cc:has_arabic_joining(hb_script_t) (/src/harfbuzz/src/hb-ot-shaper-arabic-joining-list.hh:20-42) ---
[ ]    18  static bool
[ ]    19  has_arabic_joining (hb_script_t script)
[B]    20  {
[ ]    21    /* List of scripts that have data in arabic-table. */
[B]    22    switch ((int) script)
[B]    23    {
[ ]    24      case HB_SCRIPT_ADLAM:
[ ]    25      case HB_SCRIPT_ARABIC:
[ ]    26      case HB_SCRIPT_CHORASMIAN:
[ ]    27      case HB_SCRIPT_HANIFI_ROHINGYA:
[ ]    28      case HB_SCRIPT_MANDAIC:
[ ]    29      case HB_SCRIPT_MANICHAEAN:
[L]    30      case HB_SCRIPT_MONGOLIAN:
[L]    31      case HB_SCRIPT_NKO:
[B]    32      case HB_SCRIPT_OLD_UYGHUR: <-- BLOCKER
[B]    33      case HB_SCRIPT_PHAGS_PA:
[B]    34      case HB_SCRIPT_PSALTER_PAHLAVI:
[B]    35      case HB_SCRIPT_SOGDIAN:
[B]    36      case HB_SCRIPT_SYRIAC:
[B]    37        return true;
[ ]    38  
[L]    39      default:
[L]    40        return false;
[B]    41    }
[B]    42  }

--- Caller (1 hop): hb-ot-shaper-use.cc:data_create_use(hb_ot_shape_plan_t const*) (/src/harfbuzz/src/hb-ot-shaper-use.cc:157-175, calls hb-ot-shaper-use.cc:has_arabic_joining(hb_script_t) at line 164) (full body — short) ---
[B]   157  {
[B]   158    use_shape_plan_t *use_plan = (use_shape_plan_t *) hb_calloc (1, sizeof (use_shape_plan_t));
[B]   159    if (unlikely (!use_plan))
[ ]   160      return nullptr;
[ ]   161  
[B]   162    use_plan->rphf_mask = plan->map.get_1_mask (HB_TAG('r','p','h','f'));
[ ]   163  
[B]   164    if (has_arabic_joining (plan->props.script)) <-- CALL
[B]   165    {
[B]   166      use_plan->arabic_plan = (arabic_shape_plan_t *) data_create_arabic (plan);
[B]   167      if (unlikely (!use_plan->arabic_plan))
[L]   168      {
[L]   169        hb_free (use_plan);
[L]   170        return nullptr;
[L]   171      }
[B]   172    }
[ ]   173  
[B]   174    return use_plan;
[B]   175  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-use.cc:data_create_use(hb_ot_shape_plan_t const*)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:157-175, calls hb-ot-shaper-use.cc:has_arabic_joining(hb_script_t) at line 164)

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ot-shaper-use.cc:data_create_use(hb_ot_shape_plan_t const*)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:157-175) ---
  d=2   L 164  T=10 F=0  T=4 F=6  if (has_arabic_joining (plan->props.script))
--- d=1  hb-ot-shaper-use.cc:has_arabic_joining(hb_script_t)  (/src/harfbuzz/src/hb-ot-shaper-arabic-joining-list.hh:20-42) ---
  d=1   L  30  T=0 F=10  T=3 F=7  case HB_SCRIPT_MONGOLIAN:
  d=1   L  32  T=10 F=0  T=0 F=10  case HB_SCRIPT_OLD_UYGHUR:  <-- BLOCKER
  d=1   L  33  T=0 F=10  T=1 F=9  case HB_SCRIPT_PHAGS_PA:
  d=1   L  39  T=0 F=10  T=6 F=4  default:

[off-chain: 9 additional divergent branches across 5 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=1390ee63592e3e2f, size=19 bytes, fuzzer=value_profile, trial=1, discovered_at=28s, mutation_op=ByteAddMutator,BytesDeleteMutator,ByteNegMutator):
  0000: 75 0f 01 00 00 00 00 01 20 20 e0 ed 5a 1a 20 39   u.......  ..Z. 9
  0010: 20 1e ff                                           ..
Seed 2 (id=040f38ebb4b5b1fb, size=10 bytes, fuzzer=value_profile, trial=1, discovered_at=68s, mutation_op=CrossoverReplaceMutator):
  0000: 88 0f 01 00 2d 20 00 00 00 20                     ....- ... 
Seed 3 (id=149c5dae05145ccf, size=26 bytes, fuzzer=value_profile, trial=1, discovered_at=119s, mutation_op=ByteDecMutator):
  0000: 75 0f 01 00 00 00 00 00 8a 0e 01 00 00 00 00 00   u...............
  0010: 00 00 00 00 24 09 4a 4a 3d 3d                     ....$.JJ==
Seed 4 (id=1ced7236f1cec3c8, size=73 bytes, fuzzer=value_profile, trial=1, discovered_at=525s, mutation_op=BytesExpandMutator,WordAddMutator,WordInterestingMutator,ByteIncMutator,ByteIncMutator,CrossoverInsertMutator,DwordInterestingMutator):
  0000: 00 e6 d2 08 80 00 01 20 20 01 00 00 00 00 00 00   .......  .......
  0010: 21 21 00 28 0d 0d 0d 0d 0d 0d 0d 0d 00 75 0f 01   !!.(.........u..
  0020: 00 00 00 00 01 20 20 e0 ed 5a 1a 20 39 d7 08 00   .....  ..Z. 9...
  0030: 00 00 fe 00 00 d7 08 00 00 01 00 00 00 d6 08 00   ................
Seed 5 (id=1fed305655293d8a, size=55 bytes, fuzzer=value_profile, trial=1, discovered_at=1411s, mutation_op=BitFlipMutator,BytesRandInsertMutator):
  0000: 80 0f 01 00 80 00 01 00 00 00 00 00 00 eb 01 00   ................
  0010: c0 0f 01 00 00 00 01 00 64 57 57 57 57 57 57 57   ........dWWWWWWW
  0020: 57 57 57 01 2d 68 61 6e 74 00 00 00 00 7b cc cc   WWW.-hant....{..
  0030: cb 0c 00 01 4a d6 3d                              ....J.=

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0406343f1fc9d531, size=19 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=5s, mutation_op=WordAddMutator,BytesDeleteMutator,QwordAddMutator,TokenInsert,BytesSwapMutator):
  0000: 00 01 02 22 00 10 0e 00 20 1f 01 00 1a 20 02 00   ...".... .... ..
  0010: 20 20 89                                            .
Seed 2 (id=044f6bc4804646ac, size=45 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=18s, mutation_op=QwordAddMutator,BytesSwapMutator,BytesCopyMutator,BytesDeleteMutator,BytesInsertMutator,TokenInsert):
  0000: 00 01 ff 73 6e 2d 00 00 18 18 00 00 1a 20 20 20   ...sn-.......   
  0010: 20 00 01 20 20 20 20 20 20 20 20 20 6b e8 20 20    ..         k.  
  0020: 20 00 20 20 20 00 01 20 20 20 2c 20 20             .   ..   ,  
Seed 3 (id=02f1a7a097f2fc04, size=19 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=66s, mutation_op=BytesDeleteMutator):
  0000: 4a a8 00 00 00 01 20 28 20 20 20 20 67 6c 79 66   J..... (    glyf
  0010: ff ff dd                                          ...
Seed 4 (id=0456e276e0605002, size=45 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=198s, mutation_op=BytesDeleteMutator,ByteNegMutator,QwordAddMutator,ByteNegMutator,CrossoverReplaceMutator):
  0000: f3 f3 f3 f3 f3 20 20 20 00 18 00 00 00 0e 00 00   .....   ........
  0010: 01 0a 01 00 20 20 00 0f 20 20 01 00 01 0a 01 0d   ....  ..  ......
  0020: 20 20 00 00 00 fd 00 00 01 20 20 20 20              .......    
Seed 5 (id=0192d19cb57126d5, size=74 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=922s, mutation_op=BytesDeleteMutator,WordAddMutator,DwordInterestingMutator):
  0000: 68 61 72 6e df 06 00 00 00 80 00 68 61 72 6e df   harn.......harn.
  0010: 06 00 00 00 80 00 e0 70 aa aa aa aa aa aa aa aa   .......p........
  0020: aa aa aa 68 61 72 00 12 01 00 00 12 01 00 2c 12   ...har........,.
  0030: 01 00 00 12 01 00 2c 12 01 00 2c 12 00 00 0e 12   ......,...,.....


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0001  0f(.)x7 e6(.)x1 e0(.)x1 0c(.)x1     01(.)x5 a8(.)x1 f3(.)x1 61(a)x1 +2u  DIFFER
   0x0002  01(.)x7 00(.)x2 d2(.)x1             00(.)x5 02(.)x1 ff(.)x1 f3(.)x1 +2u  PARTIAL
   0x0003  00(.)x7 08(.)x1 ed(.)x1 a4(.)x1     00(.)x5 22(")x1 73(s)x1 f3(.)x1 +2u  PARTIAL
   0x0006  00(.)x5 01(.)x3 0e(.)x1 92(.)x1     00(.)x4 20( )x3 ee(.)x2 0e(.)x1     PARTIAL
   0x0007  00(.)x7 01(.)x1 20( )x1 04(.)x1     00(.)x5 20( )x2 ff(.)x2 28(()x1     PARTIAL
   0x0008  00(.)x5 20( )x2 8a(.)x1 75(u)x1 +1u  00(.)x4 20( )x3 18(.)x2 01(.)x1     PARTIAL
   0x000a  01(.)x5 00(.)x3 e0(.)x1             00(.)x6 01(.)x2 20( )x2             PARTIAL
   0x000b  00(.)x8 ed(.)x1                     00(.)x4 20( )x4 68(h)x1 09(.)x1     PARTIAL
   0x000c  00(.)x5 76(v)x2 5a(Z)x1 11(.)x1     47(G)x3 1a(.)x2 00(.)x2 67(g)x1 +2u  PARTIAL
   0x000e  01(.)x4 00(.)x3 20( )x1 ff(.)x1     00(.)x2 55(U)x2 02(.)x1 20( )x1 +4u  PARTIAL
   0x000f  00(.)x6 39(9)x1 20( )x1 a4(.)x1     00(.)x3 42(B)x2 20( )x1 66(f)x1 +3u  PARTIAL
   0x0011  0f(.)x3 1e(.)x1 00(.)x1 21(!)x1 +3u  20( )x3 00(.)x3 ff(.)x3 0a(.)x1     PARTIAL
   0x0013  00(.)x7 28(()x1                     20( )x4 00(.)x3 10(.)x1             PARTIAL
   0x0014  00(.)x4 24($)x1 0d(.)x1 75(u)x1 +1u  00(.)x4 20( )x2 80(.)x1 01(.)x1     PARTIAL
   0x0015  09(.)x1 0d(.)x1 00(.)x1 10(.)x1 +4u  00(.)x5 20( )x3                     PARTIAL
   0x0016  01(.)x4 00(.)x2 4a(J)x1 0d(.)x1     00(.)x4 20( )x2 e0(.)x1 03(.)x1     PARTIAL
   0x0017  00(.)x6 4a(J)x1 0d(.)x1             20( )x2 00(.)x2 0f(.)x1 70(p)x1 +2u  PARTIAL
   0x001e  01(.)x3 0e(.)x2 0f(.)x1 57(W)x1     00(.)x2 20( )x1 01(.)x1 aa(.)x1 +3u  PARTIAL
   0x0020  00(.)x3 57(W)x1 75(u)x1 4b(K)x1     00(.)x4 20( )x2 aa(.)x1 3e(>)x1     PARTIAL
   0x0022  00(.)x3 01(.)x2 57(W)x1             00(.)x2 18(.)x2 20( )x1 aa(.)x1 +2u  PARTIAL
   0x0023  00(.)x5 01(.)x1                     20( )x2 e0(.)x2 00(.)x1 68(h)x1 +2u  PARTIAL
   0x0025  00(.)x2 20( )x1 68(h)x1 10(.)x1     00(.)x3 fd(.)x1 72(r)x1 3d(=)x1 +2u  PARTIAL
   0x0026  20( )x1 61(a)x1 01(.)x1 24($)x1     00(.)x2 ab(.)x2 01(.)x1 20( )x1 +2u  PARTIAL
   0x0027  e0(.)x1 6e(n)x1 00(.)x1             42(B)x3 20( )x1 00(.)x1 12(.)x1 +2u  PARTIAL
   0x0028  ed(.)x1 74(t)x1                     20( )x4 01(.)x2 f3(.)x1 03(.)x1     DIFFER
   0x0029  5a(Z)x1 00(.)x1                     20( )x3 00(.)x2 3c(<)x2 63(c)x1     PARTIAL
   0x002a  1a(.)x1 00(.)x1                     20( )x3 2c(,)x1 00(.)x1 67(g)x1 +2u  PARTIAL
   0x002b  20( )x1 00(.)x1                     20( )x3 12(.)x1 67(g)x1 10(.)x1 +2u  PARTIAL
   0x002c  39(9)x1 00(.)x1                     00(.)x3 20( )x2 01(.)x1 67(g)x1 +1u  PARTIAL
   0x002d  d7(.)x1 7b({)x1                     00(.)x4 e1(.)x1 80(.)x1             DIFFER
   0x002e  08(.)x1 cc(.)x1                     2c(,)x1 20( )x1 84(.)x1 00(.)x1 +2u  DIFFER
   0x002f  00(.)x1 cc(.)x1                     ff(.)x2 12(.)x1 0d(.)x1 b0(.)x1 +1u  DIFFER
   0x0030  00(.)x1 cb(.)x1                     00(.)x4 01(.)x1 12(.)x1             PARTIAL
   0x0031  00(.)x1 0c(.)x1                     00(.)x1 4f(O)x1 01(.)x1 10(.)x1 +2u  PARTIAL
   0x0032  fe(.)x1 00(.)x1                     00(.)x3 03(.)x1 09(.)x1 08(.)x1     PARTIAL
   0x0033  00(.)x1 01(.)x1                     00(.)x2 12(.)x1 03(.)x1 0c(.)x1 +1u  PARTIAL
   0x0034  00(.)x1 4a(J)x1                     00(.)x2 94(.)x2 01(.)x1 04(.)x1     PARTIAL
   0x0035  d7(.)x1 d6(.)x1                     00(.)x1 20( )x1 80(.)x1 10(.)x1 +2u  DIFFER
   0x0036  08(.)x1 3d(=)x1                     00(.)x3 2c(,)x1 20( )x1 04(.)x1     DIFFER
   0x0037  00(.)x1                             00(.)x4 12(.)x1 fe(.)x1             PARTIAL
   ... (8 more divergent offsets)
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
  prompts_b/harfbuzz_5761.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5761,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>value_profile_cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5761 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5761 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5761 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).