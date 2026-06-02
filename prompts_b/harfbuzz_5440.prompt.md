==== BLOCKER ====
Target: harfbuzz
Branch ID: 5440
Location: /src/harfbuzz/src/hb-ot-font.cc:390:7
Enclosing function: hb-ot-font.cc:hb_ot_get_glyph_extents(hb_font_t*, void*, unsigned int, hb_glyph_extents_t*, void*)
Source line:   if (ot_face->glyf->get_extents (font, glyph, extents)) return true;
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           1        9          0  loser (value_profile vs value_profile_cmplog); loser (grimoire_structural vs grimoire)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile); winner (value_profile vs cmplog)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         9        1          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (3) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.20h  loser=24.00h
  avg hitcount on branch: winner=8  loser=0
  prob_div=1.00  dur_div=20.80h  hit_div=8
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=3.20h  loser=21.90h
  avg hitcount on branch: winner=8  loser=0
  prob_div=0.90  dur_div=18.70h  hit_div=7
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002
--- Pair 3: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 20  (grimoire vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=7.80h  loser=21.90h
  avg hitcount on branch: winner=30  loser=0
  prob_div=0.80  dur_div=14.10h  hit_div=30
  subject-level: delta_AUC=45443160.0  p_AUC=0.001  delta_Final=636.4  p_final=0.0006

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5440/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-font.cc:hb_ot_get_glyph_extents(hb_font_t*, void*, unsigned int, hb_glyph_extents_t*, void*) (/src/harfbuzz/src/hb-ot-font.cc:379-397) ---
[ ]   377  			 hb_glyph_extents_t *extents,
[ ]   378  			 void *user_data HB_UNUSED)
[B]   379  {
[B]   380    const hb_ot_font_t *ot_font = (const hb_ot_font_t *) font_data;
[B]   381    const hb_ot_face_t *ot_face = ot_font->ot_face;
[ ]   382  
[B]   383  #if !defined(HB_NO_OT_FONT_BITMAP) && !defined(HB_NO_COLOR)
[B]   384    if (ot_face->sbix->get_extents (font, glyph, extents)) return true;
[B]   385    if (ot_face->CBDT->get_extents (font, glyph, extents)) return true;
[B]   386  #endif
[B]   387  #if !defined(HB_NO_COLOR)
[B]   388    if (ot_face->COLR->get_extents (font, glyph, extents)) return true;
[B]   389  #endif
[B]   390    if (ot_face->glyf->get_extents (font, glyph, extents)) return true; <-- BLOCKER
[B]   391  #ifndef HB_NO_OT_FONT_CFF
[B]   392    if (ot_face->cff1->get_extents (font, glyph, extents)) return true;
[B]   393    if (ot_face->cff2->get_extents (font, glyph, extents)) return true;
[B]   394  #endif
[ ]   395  
[B]   396    return false;
[B]   397  }

--- No 1-hop callers of hb-ot-font.cc:hb_ot_get_glyph_extents(hb_font_t*, void*, unsigned int, hb_glyph_extents_t*, void*) fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-font.cc:hb_ot_get_glyph_extents(hb_font_t*, void*, unsigned int, hb_glyph_extents_t*, void*)  (/src/harfbuzz/src/hb-ot-font.cc:379-397) ---
  d=1   L 390  T=51 F=8  T=0 F=31  if (ot_face->glyf->get_extents (font, glyph, extents)) re...  <-- BLOCKER
  d=1   L 392  T=0 F=8  T=0 F=31  if (ot_face->cff1->get_extents (font, glyph, extents)) re...
  d=1   L 393  T=0 F=8  T=0 F=31  if (ot_face->cff2->get_extents (font, glyph, extents)) re...

[off-chain: 5 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=d862f87dd0cadddf, size=90 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=891s, mutation_op=CrossoverInsertMutator,DwordInterestingMutator,QwordAddMutator):
  0000: 74 79 70 31 00 02 20 20 00 01 00 01 6c 6f 63 61   typ1..  ....loca
  0010: 06 20 02 0a 00 00 00 1f 00 00 00 ff 00 00 00 03   . ..............
  0020: 00 00 6f ff fe ff 23 67 01 a0 01 ff ff ff de 00   ..o...#g........
  0030: 76 62 61 20 02 02 20 20 01 00 dc 09 0d 7a 20 20   vba ..  .....z  
Seed 2 (id=7b66038eb6fb00ba, size=126 bytes, fuzzer=grimoire, trial=1, discovered_at=1252s):
  0000: 74 72 75 65 00 01 20 20 20 20 20 20 6c 6f 63 61   true..      loca
  0010: 70 6d 6a 74 00 00 00 01 01 0b 00 00 01 20 20 20   pmjt.........   
  0020: 20 20 6d 6e 2d 00 7f 65 72 6e 20 20 20 20 2d 6c     mn-..ern    -l
  0030: 75 78 00 00 70 70 70 00 00 10 00 00 1d 75 78 00   ux..ppp......ux.
Seed 3 (id=a9643cacbc8916b3, size=126 bytes, fuzzer=grimoire, trial=1, discovered_at=1252s):
  0000: 74 72 75 65 00 01 20 20 20 20 20 20 6c 6f 63 61   true..      loca
  0010: 70 6d 6a 74 00 00 00 01 01 0b 00 00 01 20 20 20   pmjt.........   
  0020: 20 20 6d 6e 2d 00 7f 65 72 6e 20 20 20 20 2d 6c     mn-..ern    -l
  0030: 75 78 00 00 70 70 70 00 00 10 00 00 1d 75 78 00   ux..ppp......ux.
Seed 4 (id=7d2d06308fa478eb, size=136 bytes, fuzzer=grimoire, trial=1, discovered_at=1702s):
  0000: 74 72 75 65 00 01 20 20 20 20 20 20 6c 6f 63 61   true..      loca
  0010: 70 6d 6a 74 00 00 00 00 cc 00 00 00 80 70 78 2d   pmjt.........px-
  0020: 00 00 01 20 20 08 00 00 00 20 cc 0c 2f 12 00 00   ...  .... ../...
  0030: ff ff 7f 00 01 00 1d fa 02 00 00 03 00 00 11 00   ................
Seed 5 (id=00e7c22b71956844, size=123 bytes, fuzzer=grimoire, trial=1, discovered_at=2069s):
  0000: 74 72 75 65 00 01 20 20 20 20 20 20 6c 6f 63 61   true..      loca
  0010: 6d 6a 74 00 00 00 00 4b 01 00 18 a0 00 00 00 00   mjt....K........
  0020: 00 00 74 74 63 66 00 01 00 01 00 00 00 01 4a e9   ..ttcf........J.
  0030: 01 00 00 00 80 00 0f 0b 00 00 00 20 6d 6e 2d 00   ........... mn-.

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00546490999c9c0b, size=57 bytes, fuzzer=value_profile, trial=1, discovered_at=13s, mutation_op=DwordAddMutator,BytesDeleteMutator,ByteInterestingMutator,TokenInsert,BytesCopyMutator,ByteNegMutator):
  0000: fe ff ff ff f4 01 e0 e0 20 00 00 00 01 20 e0 6a   ........ .... .j
  0010: 79 2d 68 61 6e 74 2d 68 6b 00 20 00 00 00 ff 01   y-hant-hk. .....
  0020: 00 07 00 00 01 20 20 20 01 5b 00 00 00 e0 20 00   .....   .[.... .
  0030: 00 00 01 20 ff 09 fd 20 ff                        ... ... .
Seed 2 (id=0003cbd2b6f5fff8, size=13 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=BitFlipMutator,BytesDeleteMutator,WordAddMutator):
  0000: e0 17 00 00 1a 20 00 00 29 2b 29 29 2c            ..... ..)+)),
Seed 3 (id=00280212c7547f95, size=27 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=WordInterestingMutator,WordAddMutator,ByteAddMutator):
  0000: e0 e8 ff ff 20 00 00 55 e0 17 00 00 2b 20 00 fa   .... ..U....+ ..
  0010: 20 00 00 55 e0 17 00 00 61 2e 69                   ..U....a.i
Seed 4 (id=00167ff70704a0e0, size=23 bytes, fuzzer=value_profile, trial=1, discovered_at=120s, mutation_op=BytesInsertCopyMutator,CrossoverInsertMutator,ByteDecMutator):
  0000: 4c 0e 00 00 4c 0e 00 00 4c 16 00 00 00 18 18 00   L...L...L.......
  0010: 00 42 18 65 0e 00 ff                              .B.e...
Seed 5 (id=0059bffc70552fa0, size=62 bytes, fuzzer=value_profile, trial=1, discovered_at=197s, mutation_op=DwordInterestingMutator,BytesRandInsertMutator,BytesInsertMutator):
  0000: 00 01 0e 00 df 20 00 00 00 00 aa 13 df 20 3d 3d   ..... ....... ==
  0010: 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 00 ff   ==============..
  0020: df 20 00 00 00 00 00 20 20 20 20 20 20 20 20 20   . .....         
  0030: 2c 00 00 00 64 55 55 55 df 20 00 00 00 00         ,...dUUU. ....


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  74(t)x12                            00(.)x11 e0(.)x2 fe(.)x1 4c(L)x1 +5u  DIFFER
   0x0001  72(r)x10 79(y)x2                    01(.)x11 ff(.)x1 17(.)x1 e8(.)x1 +6u  DIFFER
   0x0002  75(u)x10 70(p)x2                    00(.)x15 ff(.)x2 0e(.)x1 8a(.)x1 +1u  DIFFER
   0x0003  65(e)x10 31(1)x2                    00(.)x16 ff(.)x2 8a(.)x1 b7(.)x1    DIFFER
   0x0004  00(.)x12                            00(.)x10 df(.)x2 f4(.)x1 1a(.)x1 +6u  PARTIAL
   0x0005  01(.)x10 02(.)x2                    01(.)x11 20( )x3 00(.)x3 0e(.)x2 +1u  PARTIAL
   0x0006  20( )x12                            00(.)x8 07(.)x6 20( )x3 e0(.)x1 +2u  PARTIAL
   0x0007  20( )x12                            00(.)x8 20( )x8 e0(.)x1 55(U)x1 +2u  PARTIAL
   0x0008  20( )x8 00(.)x2 21(!)x2             21(!)x9 20( )x3 00(.)x2 29())x1 +5u  PARTIAL
   0x0009  20( )x10 01(.)x2                    20( )x9 00(.)x2 2b(+)x1 17(.)x1 +7u  PARTIAL
   0x000a  20( )x10 00(.)x2                    1e(.)x7 00(.)x5 20( )x3 29())x1 +4u  PARTIAL
   0x000b  20( )x10 01(.)x2                    20( )x10 00(.)x7 29())x1 13(.)x1 +1u  PARTIAL
   0x000c  6c(l)x12                            47(G)x9 00(.)x2 01(.)x1 2c(,)x1 +7u  DIFFER
   0x000d  6f(o)x12                            50(P)x7 20( )x4 53(S)x2 18(.)x1 +5u  DIFFER
   0x000e  63(c)x12                            4f(O)x7 00(.)x3 55(U)x2 e0(.)x1 +6u  DIFFER
   0x000f  61(a)x12                            53(S)x7 00(.)x3 42(B)x2 6a(j)x1 +6u  DIFFER
   0x0010  70(p)x9 06(.)x2 6d(m)x1             00(.)x12 20( )x2 79(y)x1 3d(=)x1 +3u  DIFFER
   0x0011  6d(m)x9 20( )x2 6a(j)x1             01(.)x10 20( )x2 2d(-)x1 00(.)x1 +5u  PARTIAL
   0x0012  6a(j)x9 02(.)x2 74(t)x1             00(.)x14 68(h)x1 18(.)x1 3d(=)x1 +2u  DIFFER
   0x0013  74(t)x9 0a(.)x2 00(.)x1             0d(.)x8 00(.)x3 61(a)x1 55(U)x1 +6u  PARTIAL
   0x0014  00(.)x12                            00(.)x11 6e(n)x1 e0(.)x1 0e(.)x1 +5u  PARTIAL
   0x0015  00(.)x12                            00(.)x11 74(t)x1 17(.)x1 3d(=)x1 +5u  PARTIAL
   0x0016  00(.)x12                            00(.)x14 2d(-)x1 ff(.)x1 3d(=)x1 +2u  PARTIAL
   0x001a  00(.)x9 18(.)x1 6e(n)x1 02(.)x1     00(.)x12 20( )x2 69(i)x1 3d(=)x1 +2u  PARTIAL
   0x0022  00(.)x3 6d(m)x2 01(.)x2 6f(o)x1 +4u  00(.)x15 1b(.)x1 01(.)x1            PARTIAL
   0x0033  00(.)x8 20( )x2 49(I)x1 b3(.)x1     01(.)x5 20( )x2 02(.)x2 03(.)x2 +5u  PARTIAL
   0x003a  00(.)x9 dc(.)x1 55(U)x1 20( )x1     00(.)x9 9f(.)x1 e3(.)x1 ff(.)x1 +3u  PARTIAL
   0x003f  00(.)x10 20( )x1 12(.)x1            00(.)x2 10(.)x2 06(.)x2 91(.)x1 +6u  PARTIAL
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

--- grimoire ---
**Baseline relationship**: grimoire builds on the full cmplog stack —
it includes the `CmpLogObserver`, the `TracingStage`, and the
`I2SRandReplace` (i2s) stage — and ADDS a `GeneralizationStage` plus
Grimoire structural mutators. The single-technique delta is therefore
`grimoire` vs `cmplog` (both have I2S; grimoire adds generalization +
Grimoire mutators), not vs naive.

**Instrumentation**: cmplog's edge counters + per-execution CMP buffer
(`CmpLogObserver`).

**Feedback**: edge-bucket `MaxMapFeedback`.

**Mutators / stages**: stages are
`[generalization, tracing, i2s, havoc, grimoire]`. `GeneralizationStage`
replaces concrete byte runs in a corpus entry with `<GAP>` placeholders
(a generalised input) by repeatedly re-executing and checking that
coverage is preserved. The Grimoire mutators —
`GrimoireExtensionMutator`, `GrimoireRecursiveReplacementMutator`,
`GrimoireStringReplacementMutator`, `GrimoireRandomDeleteMutator` —
splice and recurse on these generalised token/gap structures
(string-based, grammar-free structural mutation). `I2SRandReplace` (the
cmplog i2s stage) also runs.

**Observed `mutation_op` in seed metadata**: all grimoire stages (i2s,
havoc, grimoire) are wrapped in `LineageMutatorWrap` with **no
per-operator name list**, so grimoire seeds appear nameless in lineage
(`mutation_op = -`). As with mopt, nameless rows are NOT an
I2S-exclusive signal here — and grimoire genuinely runs I2S too, so the
two are not separable from lineage names.

**Per-execution cost**: cmplog's per-CMP cost, plus extra executions
during generalization (each candidate gap is validated by a re-run).

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
  prompts_b/harfbuzz_5440.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5440,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S), value_profile_cmplog>cmplog (value_profile), grimoire>cmplog (grimoire_structural)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5440 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5440 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5440 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).