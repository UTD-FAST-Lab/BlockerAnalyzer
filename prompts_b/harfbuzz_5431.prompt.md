==== BLOCKER ====
Target: harfbuzz
Branch ID: 5431
Location: /src/harfbuzz/src/hb-ot-cmap-table.hh:1883:2
Enclosing function: OT::cmap::accelerator_t::accelerator_t(hb_face_t*)
Source line: 	default:
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           3        7          0  REFERENCE
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             9        1          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         8        2          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=10.00h  loser=24.00h
  avg hitcount on branch: winner=62  loser=0
  prob_div=0.90  dur_div=14.00h  hit_div=62
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5431/{W,L}/branch_coverage_show.txt

--- Enclosing function: OT::cmap::accelerator_t::accelerator_t(hb_face_t*) (/src/harfbuzz/src/hb-ot-cmap-table.hh:1848-1898) ---
[ ]  1846  
[ ]  1847      accelerator_t (hb_face_t *face)
[B]  1848      {
[B]  1849        this->table = hb_sanitize_context_t ().reference_table<cmap> (face);
[B]  1850        bool symbol;
[B]  1851        this->subtable = table->find_best_subtable (&symbol);
[B]  1852        this->subtable_uvs = &Null (CmapSubtableFormat14);
[B]  1853        {
[B]  1854  	const CmapSubtable *st = table->find_subtable (0, 5);
[B]  1855  	if (st && st->u.format == 14)
[ ]  1856  	  subtable_uvs = &st->u.format14;
[B]  1857        }
[ ]  1858  
[B]  1859        this->get_glyph_data = subtable;
[B]  1860        if (unlikely (symbol))
[ ]  1861        {
[ ]  1862  	switch ((unsigned) face->table.OS2->get_font_page ()) {
[ ]  1863  	case OS2::font_page_t::FONT_PAGE_NONE:
[ ]  1864  	  this->get_glyph_funcZ = get_glyph_from_symbol<CmapSubtable, _hb_symbol_pua_map>;
[ ]  1865  	  break;
[ ]  1866  #ifndef HB_NO_OT_SHAPER_ARABIC_FALLBACK
[ ]  1867  	case OS2::font_page_t::FONT_PAGE_SIMP_ARABIC:
[ ]  1868  	  this->get_glyph_funcZ = get_glyph_from_symbol<CmapSubtable, _hb_arabic_pua_simp_map>;
[ ]  1869  	  break;
[ ]  1870  	case OS2::font_page_t::FONT_PAGE_TRAD_ARABIC:
[ ]  1871  	  this->get_glyph_funcZ = get_glyph_from_symbol<CmapSubtable, _hb_arabic_pua_trad_map>;
[ ]  1872  	  break;
[ ]  1873  #endif
[ ]  1874  	default:
[ ]  1875  	  this->get_glyph_funcZ = get_glyph_from<CmapSubtable>;
[ ]  1876  	  break;
[ ]  1877  	}
[ ]  1878        }
[B]  1879        else
[B]  1880        {
[B]  1881  	switch (subtable->u.format) {
[ ]  1882  	/* Accelerate format 4 and format 12. */
[L]  1883  	default: <-- BLOCKER
[L]  1884  	  this->get_glyph_funcZ = get_glyph_from<CmapSubtable>;
[L]  1885  	  break;
[ ]  1886  	case 12:
[ ]  1887  	  this->get_glyph_funcZ = get_glyph_from<CmapSubtableFormat12>;
[ ]  1888  	  break;
[W]  1889  	case  4:
[W]  1890  	{
[W]  1891  	  this->format4_accel.init (&subtable->u.format4);
[W]  1892  	  this->get_glyph_data = &this->format4_accel;
[W]  1893  	  this->get_glyph_funcZ = this->format4_accel.get_glyph_func;
[W]  1894  	  break;
[ ]  1895  	}
[B]  1896  	}
[B]  1897        }
[B]  1898      }

--- Caller (1 hop): OT::CBDT_accelerator_t::CBDT_accelerator_t(hb_face_t*) (/src/harfbuzz/src/OT/Color/CBDT/CBDT.hh:1024-1024, calls OT::cmap::accelerator_t::accelerator_t(hb_face_t*) at line 1024) (full body — short) ---
[B]  1024    CBDT_accelerator_t (hb_face_t *face) : CBDT::accelerator_t (face) {} <-- CALL

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  OT::cff2::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:515-515, calls OT::cmap::accelerator_t::accelerator_t(hb_face_t*) at line 515)
hop 2  OT::cff2_accelerator_t::cff2_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:538-538, calls OT::cmap::accelerator_t::accelerator_t(hb_face_t*) at line 538)
hop 3  OT::hmtx_accelerator_t::hmtx_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:449-449, calls OT::cff2::accelerator_t::accelerator_t(hb_face_t*) at line 449)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0      1240  OT::CmapSubtableFormat0::get_glyph(unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:48-54)
       0      1240  OT::CmapSubtable::get_glyph(unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:1351-1362)
       0      1240  bool OT::cmap::accelerator_t::get_glyph_from<OT::CmapSubtable>(void const*, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-cmap-table.hh:1984-1987)
       0      1240  bool OT::cmap::accelerator_t::get_glyph_from<OT::CmapSubtableFormat12>(void const*, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-cmap-table.hh:1984-1987)
      77      1240  OT::cmap::accelerator_t::_cached_get(unsigned int, unsigned int*, hb_cache_t<21u, 16u, 8u, true>*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:1904-1916)
      56      1050  OT::cmap::accelerator_t::get_nominal_glyph(unsigned int, unsigned int*, hb_cache_t<21u, 16u, 8u, true>*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:1921-1924)
      57       532  OT::hmtxvmtx<OT::vmtx, OT::vhea, OT::VVAR>::accelerator_t::get_advance_without_var_unscaled(unsigned int) const  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:326-354)
      57       532  OT::hmtxvmtx<OT::hmtx, OT::hhea, OT::HVAR>::accelerator_t::get_advance_without_var_unscaled(unsigned int) const  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:326-354)
      57       532  OT::hmtxvmtx<OT::hmtx, OT::hhea, OT::HVAR>::accelerator_t::get_advance_with_var_unscaled(unsigned int, hb_font_t*, float*) const  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:359-375)
      57       532  OT::hmtxvmtx<OT::vmtx, OT::vhea, OT::VVAR>::accelerator_t::get_advance_with_var_unscaled(unsigned int, hb_font_t*, float*) const  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:359-375)
      21       204  OT::cmap::accelerator_t::get_nominal_glyphs(unsigned int, unsigned int const*, unsigned int, unsigned int*, unsigned int, hb_cache_t<21u, 16u, 8u, true>*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:1932-1944)
       5       100  OT::cmap::find_subtable(unsigned int, unsigned int) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:2021-2031)
      77         0  OT::CmapSubtableFormat4::accelerator_t::get_glyph(unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:400-443)
      77         0  OT::CmapSubtableFormat4::accelerator_t::get_glyph(unsigned int, unsigned int*) const::CustomRange::cmp(unsigned int, unsigned int) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:405-409)
      77         0  OT::CmapSubtableFormat4::accelerator_t::get_glyph_func(void const*, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-cmap-table.hh:446-446)
... (81 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OT::cmap::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cmap-table.hh:1848-1898) ---
  d=1   L1855  T=0 F=1  T=0 F=10  if (st && st->u.format == 14)
  d=1   L1883  T=0 F=1  T=10 F=0  default:  <-- BLOCKER
  d=1   L1886  T=0 F=1  T=0 F=10  case 12:
  d=1   L1889  T=1 F=0  T=0 F=10  case  4:

[off-chain: 76 additional divergent branches across 29 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=f95aab45df7ef054, size=415 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=85027s, mutation_op=BytesSwapMutator,DwordAddMutator,BytesDeleteMutator,TokenReplace,ByteNegMutator):
  0000: 00 01 00 00 00 0c 02 ff 00 30 00 1f 63 6d 61 70   .........0..cmap
  0010: 20 20 20 20 00 00 00 02 74 74 6c 66 00 01 15 15       ....ttlf....
  0020: 15 15 15 15 15 15 15 15 15 15 20 20 20 20 00 00   ..........    ..
  0030: 00 04 00 00 00 ff ff ff ff 03 02 00 00 00 20 20   ..............  

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=0003cbd2b6f5fff8, size=13 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=BitFlipMutator,BytesDeleteMutator,WordAddMutator):
  0000: e0 17 00 00 1a 20 00 00 29 2b 29 29 2c            ..... ..)+)),
Seed 2 (id=00280212c7547f95, size=27 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=WordInterestingMutator,WordAddMutator,ByteAddMutator):
  0000: e0 e8 ff ff 20 00 00 55 e0 17 00 00 2b 20 00 fa   .... ..U....+ ..
  0010: 20 00 00 55 e0 17 00 00 61 2e 69                   ..U....a.i
Seed 3 (id=00167ff70704a0e0, size=23 bytes, fuzzer=value_profile, trial=1, discovered_at=120s, mutation_op=BytesInsertCopyMutator,CrossoverInsertMutator,ByteDecMutator):
  0000: 4c 0e 00 00 4c 0e 00 00 4c 16 00 00 00 18 18 00   L...L...L.......
  0010: 00 42 18 65 0e 00 ff                              .B.e...
Seed 4 (id=0059bffc70552fa0, size=62 bytes, fuzzer=value_profile, trial=1, discovered_at=197s, mutation_op=DwordInterestingMutator,BytesRandInsertMutator,BytesInsertMutator):
  0000: 00 01 0e 00 df 20 00 00 00 00 aa 13 df 20 3d 3d   ..... ....... ==
  0010: 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 00 ff   ==============..
  0020: df 20 00 00 00 00 00 20 20 20 20 20 20 20 20 20   . .....         
  0030: 2c 00 00 00 64 55 55 55 df 20 00 00 00 00         ,...dUUU. ....
Seed 5 (id=000502d87c3cfa20, size=68 bytes, fuzzer=value_profile, trial=1, discovered_at=915s, mutation_op=BytesRandSetMutator):
  0000: f1 08 00 00 10 06 00 00 37 1c 00 00 f1 08 3b 3b   ........7.....;;
  0010: 3b 06 00 00 37 1c 00 00 4c 9f 9f 9f 4c 06 00 00   ;...7...L...L...
  0020: 37 0e 00 00 4c 9f 9f 9f 0e 17 00 36 0e 00 00 4c   7...L......6...L
  0030: 0e 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 91   ................


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x1                             e0(.)x2 20( )x2 4c(L)x1 00(.)x1 +4u  PARTIAL
   0x0001  01(.)x1                             17(.)x1 e8(.)x1 0e(.)x1 01(.)x1 +6u  PARTIAL
   0x0002  00(.)x1                             00(.)x5 ff(.)x1 0e(.)x1 8a(.)x1 +2u  PARTIAL
   0x0003  00(.)x1                             00(.)x7 ff(.)x1 8a(.)x1 b7(.)x1     PARTIAL
   0x0004  00(.)x1                             df(.)x2 1a(.)x1 20( )x1 4c(L)x1 +5u  PARTIAL
   0x0005  0c(.)x1                             00(.)x4 20( )x3 0e(.)x2 06(.)x1     DIFFER
   0x0006  02(.)x1                             00(.)x8 e5(.)x1 20( )x1             DIFFER
   0x0007  ff(.)x1                             00(.)x7 55(U)x1 01(.)x1 0d(.)x1     DIFFER
   0x0008  00(.)x1                             00(.)x2 29())x1 e0(.)x1 4c(L)x1 +5u  PARTIAL
   0x0009  30(0)x1                             00(.)x2 2b(+)x1 17(.)x1 16(.)x1 +5u  DIFFER
   0x000a  00(.)x1                             00(.)x4 29())x1 aa(.)x1 89(.)x1 +3u  PARTIAL
   0x000b  1f(.)x1                             00(.)x6 29())x1 13(.)x1 15(.)x1 +1u  DIFFER
   0x000c  63(c)x1                             00(.)x3 2c(,)x1 2b(+)x1 df(.)x1 +4u  DIFFER
   0x000d  6d(m)x1                             20( )x3 00(.)x2 18(.)x1 08(.)x1 +2u  DIFFER
   0x000e  61(a)x1                             00(.)x3 18(.)x1 3d(=)x1 3b(;)x1 +3u  DIFFER
   0x000f  70(p)x1                             00(.)x3 fa(.)x1 3d(=)x1 3b(;)x1 +3u  DIFFER
   0x0010  20( )x1                             20( )x2 00(.)x2 3d(=)x1 3b(;)x1 +3u  PARTIAL
   0x0011  20( )x1                             20( )x2 00(.)x1 42(B)x1 3d(=)x1 +4u  PARTIAL
   0x0012  20( )x1                             00(.)x4 18(.)x1 3d(=)x1 20( )x1 +2u  PARTIAL
   0x0013  20( )x1                             00(.)x2 55(U)x1 65(e)x1 3d(=)x1 +4u  PARTIAL
   0x0014  00(.)x1                             e0(.)x1 0e(.)x1 3d(=)x1 37(7)x1 +5u  PARTIAL
   0x0015  00(.)x1                             20( )x2 17(.)x1 00(.)x1 3d(=)x1 +4u  PARTIAL
   0x0016  00(.)x1                             00(.)x4 20( )x2 ff(.)x1 3d(=)x1 +1u  PARTIAL
   0x0017  02(.)x1                             00(.)x5 20( )x2 3d(=)x1             DIFFER
   0x0018  74(t)x1                             20( )x3 61(a)x1 3d(=)x1 4c(L)x1 +2u  DIFFER
   0x0019  74(t)x1                             20( )x2 2e(.)x1 3d(=)x1 9f(.)x1 +3u  DIFFER
   0x001a  6c(l)x1                             00(.)x2 69(i)x1 3d(=)x1 9f(.)x1 +3u  DIFFER
   0x001b  66(f)x1                             00(.)x3 20( )x2 3d(=)x1 9f(.)x1     DIFFER
   0x001c  00(.)x1                             3d(=)x1 4c(L)x1 20( )x1 df(.)x1 +3u  PARTIAL
   0x001d  01(.)x1                             3d(=)x1 06(.)x1 7f(.)x1 20( )x1 +3u  DIFFER
   0x001e  15(.)x1                             00(.)x4 80(.)x1 13(.)x1 ff(.)x1     DIFFER
   0x001f  15(.)x1                             00(.)x3 ff(.)x1 54(T)x1 10(.)x1 +1u  DIFFER
   0x0020  15(.)x1                             00(.)x2 df(.)x1 37(7)x1 54(T)x1 +2u  DIFFER
   0x0021  15(.)x1                             0e(.)x2 00(.)x2 20( )x1 6f(o)x1 +1u  DIFFER
   0x0022  15(.)x1                             00(.)x5 1b(.)x1 0f(.)x1             DIFFER
   0x0023  15(.)x1                             00(.)x4 6d(m)x1 2d(-)x1 fd(.)x1     DIFFER
   0x0024  15(.)x1                             00(.)x3 4c(L)x1 20( )x1 b9(.)x1 +1u  DIFFER
   0x0025  15(.)x1                             00(.)x3 9f(.)x1 43(C)x1 11(.)x1 +1u  DIFFER
   0x0026  15(.)x1                             00(.)x2 9f(.)x1 09(.)x1 2d(-)x1 +2u  DIFFER
   0x0027  15(.)x1                             20( )x2 9f(.)x1 68(h)x1 61(a)x1 +2u  DIFFER
   ... (24 more divergent offsets)
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
  prompts_b/harfbuzz_5431.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5431,
  "target": "harfbuzz",
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5431 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5431 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5431 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).