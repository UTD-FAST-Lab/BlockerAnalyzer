==== BLOCKER ====
Target: harfbuzz
Branch ID: 5251
Location: /src/harfbuzz/src/OT/name/name.hh:504:32
Enclosing function: OT::name::accelerator_t::accelerator_t(hb_face_t*)
Source line:       for (unsigned int i = 0; i < this->names.length; i++)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           1        9          0  loser (value_profile vs value_profile_cmplog)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             9        1          0  winner (I2S vs value_profile); winner (value_profile vs cmplog)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         2        8          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=7.50h  loser=24.00h
  avg hitcount on branch: winner=12  loser=0
  prob_div=0.90  dur_div=16.50h  hit_div=12
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=7.50h  loser=21.90h
  avg hitcount on branch: winner=12  loser=2
  prob_div=0.80  dur_div=14.40h  hit_div=11
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5251/{W,L}/branch_coverage_show.txt

--- Enclosing function: OT::name::accelerator_t::accelerator_t(hb_face_t*) (/src/harfbuzz/src/OT/name/name.hh:480-516) ---
[ ]   478    {
[ ]   479      accelerator_t (hb_face_t *face)
[B]   480      {
[B]   481        this->table = hb_sanitize_context_t ().reference_table<name> (face);
[B]   482        assert (this->table.get_length () >= this->table->stringOffset);
[B]   483        this->pool = (const char *) (const void *) (this->table+this->table->stringOffset);
[B]   484        this->pool_len = this->table.get_length () - this->table->stringOffset;
[B]   485        const hb_array_t<const NameRecord> all_names (this->table->nameRecordZ.arrayZ,
[B]   486  						    this->table->count);
[ ]   487  
[B]   488        this->names.alloc (all_names.length, true);
[ ]   489  
[B]   490        for (unsigned int i = 0; i < all_names.length; i++)
[W]   491        {
[W]   492  	hb_ot_name_entry_t *entry = this->names.push ();
[ ]   493  
[W]   494  	entry->name_id = all_names[i].nameID;
[W]   495  	entry->language = all_names[i].language (face);
[W]   496  	entry->entry_score =  all_names[i].score ();
[W]   497  	entry->entry_index = i;
[W]   498        }
[ ]   499  
[B]   500        this->names.qsort (_hb_ot_name_entry_cmp);
[ ]   501        /* Walk and pick best only for each name_id,language pair,
[ ]   502         * while dropping unsupported encodings. */
[B]   503        unsigned int j = 0;
[B]   504        for (unsigned int i = 0; i < this->names.length; i++) <-- BLOCKER
[W]   505        {
[W]   506  	if (this->names[i].entry_score == UNSUPPORTED ||
[W]   507  	    this->names[i].language == HB_LANGUAGE_INVALID)
[W]   508  	  continue;
[W]   509  	if (i &&
[W]   510  	    this->names[i - 1].name_id  == this->names[i].name_id &&
[W]   511  	    this->names[i - 1].language == this->names[i].language)
[ ]   512  	  continue;
[W]   513  	this->names[j++] = this->names[i];
[W]   514        }
[B]   515        this->names.resize (j);
[B]   516      }

--- Caller (1 hop): OT::CBDT_accelerator_t::CBDT_accelerator_t(hb_face_t*) (/src/harfbuzz/src/OT/Color/CBDT/CBDT.hh:1024-1024, calls OT::name::accelerator_t::accelerator_t(hb_face_t*) at line 1024) (full body — short) ---
[B]  1024    CBDT_accelerator_t (hb_face_t *face) : CBDT::accelerator_t (face) {} <-- CALL

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  OT::cff2::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:515-515, calls OT::name::accelerator_t::accelerator_t(hb_face_t*) at line 515)
hop 2  OT::cff2_accelerator_t::cff2_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:538-538, calls OT::name::accelerator_t::accelerator_t(hb_face_t*) at line 538)
hop 3  OT::hmtx_accelerator_t::hmtx_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:449-449, calls OT::cff2::accelerator_t::accelerator_t(hb_face_t*) at line 449)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      57      2180  OT::hmtxvmtx<OT::vmtx, OT::vhea, OT::VVAR>::accelerator_t::get_advance_without_var_unscaled(unsigned int) const  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:326-354)
      57      2180  OT::hmtxvmtx<OT::hmtx, OT::hhea, OT::HVAR>::accelerator_t::get_advance_without_var_unscaled(unsigned int) const  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:326-354)
      57      2180  OT::hmtxvmtx<OT::hmtx, OT::hhea, OT::HVAR>::accelerator_t::get_advance_with_var_unscaled(unsigned int, hb_font_t*, float*) const  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:359-375)
      57      2180  OT::hmtxvmtx<OT::vmtx, OT::vhea, OT::VVAR>::accelerator_t::get_advance_with_var_unscaled(unsigned int, hb_font_t*, float*) const  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:359-375)
       4       188  OT::cff1::accelerator_templ_t<CFF::cff1_private_dict_opset_t, CFF::cff1_private_dict_values_base_t<CFF::dict_val_t> >::is_valid() const  (/src/harfbuzz/src/hb-ot-cff1-table.hh:1189-1189)
       3       120  OT::name::accelerator_t::get_index(unsigned int, hb_language_impl_t const*, unsigned int*) const  (/src/harfbuzz/src/OT/name/name.hh:525-549)
       2       108  OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::is_valid() const  (/src/harfbuzz/src/hb-ot-cff2-table.hh:492-492)
       2        80  OT::CBDT::accelerator_t::has_data() const  (/src/harfbuzz/src/OT/Color/CBDT/CBDT.hh:942-942)
       2        80  CFF::cff1_top_dict_values_t::fini()  (/src/harfbuzz/src/hb-ot-cff1-table.hh:724-724)
       2        80  OT::cff1::accelerator_templ_t<CFF::cff1_private_dict_opset_t, CFF::cff1_private_dict_values_base_t<CFF::dict_val_t> >::fini()  (/src/harfbuzz/src/hb-ot-cff1-table.hh:1180-1187)
       2        79  OT::hmtxvmtx<OT::hmtx, OT::hhea, OT::HVAR>::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:236-277)
       2        79  OT::hmtxvmtx<OT::vmtx, OT::vhea, OT::VVAR>::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:236-277)
       2        79  OT::hmtxvmtx<OT::hmtx, OT::hhea, OT::HVAR>::accelerator_t::~accelerator_t()  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:279-282)
       2        79  OT::hmtxvmtx<OT::vmtx, OT::vhea, OT::VVAR>::accelerator_t::~accelerator_t()  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:279-282)
       2        76  CFF::cff2_top_dict_values_t::fini()  (/src/harfbuzz/src/hb-ot-cff2-table.hh:148-148)
... (66 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OT::name::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/OT/name/name.hh:480-516) ---
  d=1   L 490  T=2 F=1  T=0 F=39  for (unsigned int i = 0; i < all_names.length; i++)
  d=1   L 504  T=2 F=1  T=0 F=39  for (unsigned int i = 0; i < this->names.length; i++)  <-- BLOCKER
  d=1   L 506  T=1 F=1  T=0 F=0  if (this->names[i].entry_score == UNSUPPORTED ||
  d=1   L 507  T=0 F=1  T=0 F=0  this->names[i].language == HB_LANGUAGE_INVALID)
  d=1   L 509  T=1 F=0  T=0 F=0  if (i &&
  d=1   L 510  T=0 F=1  T=0 F=0  this->names[i - 1].name_id  == this->names[i].name_id &&

[off-chain: 36 additional divergent branches across 18 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=55e02621633263d5, size=184 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=61717s, mutation_op=WordAddMutator,ByteFlipMutator,BytesInsertCopyMutator):
  0000: 74 79 70 31 00 02 20 20 20 3f 21 20 6e 61 6d 65   typ1..   ?! name
  0010: b2 b2 2d b2 00 00 00 21 20 6b 20 47 ac 47 42 20   ..-....! k G.GB 
  0020: 00 00 00 00 02 00 2c 00 01 00 00 00 00 20 20 00   ......,......  .
  0030: 00 00 06 00 04 00 0c 00 03 00 01 00 00 00 10 00   ................

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00546490999c9c0b, size=57 bytes, fuzzer=value_profile, trial=1, discovered_at=13s, mutation_op=DwordAddMutator,BytesDeleteMutator,ByteInterestingMutator,TokenInsert,BytesCopyMutator,ByteNegMutator):
  0000: fe ff ff ff f4 01 e0 e0 20 00 00 00 01 20 e0 6a   ........ .... .j
  0010: 79 2d 68 61 6e 74 2d 68 6b 00 20 00 00 00 ff 01   y-hant-hk. .....
  0020: 00 07 00 00 01 20 20 20 01 5b 00 00 00 e0 20 00   .....   .[.... .
  0030: 00 00 01 20 ff 09 fd 20 ff                        ... ... .
Seed 2 (id=002a5b2b8b5c414d, size=54 bytes, fuzzer=value_profile, trial=2, discovered_at=70s, mutation_op=TokenReplace,BytesCopyMutator,ByteAddMutator,BytesSetMutator):
  0000: 92 92 92 df 68 2d 68 81 6e 74 00 9a 9a 20 8e 8e   ....h-h.nt... ..
  0010: 8e 8e 79 8e 9a 17 00 00 00 01 20 20 44 46 ff 54   ..y.......  DF.T
  0020: 70 7f 70 70 70 70 70 52 9a 9a ff df 68 2d 68 61   p.pppppR....h-ha
  0030: 6e 74 00 9a 9a 74                                 nt...t
Seed 3 (id=0003cbd2b6f5fff8, size=13 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=BitFlipMutator,BytesDeleteMutator,WordAddMutator):
  0000: e0 17 00 00 1a 20 00 00 29 2b 29 29 2c            ..... ..)+)),
Seed 4 (id=00280212c7547f95, size=27 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=WordInterestingMutator,WordAddMutator,ByteAddMutator):
  0000: e0 e8 ff ff 20 00 00 55 e0 17 00 00 2b 20 00 fa   .... ..U....+ ..
  0010: 20 00 00 55 e0 17 00 00 61 2e 69                   ..U....a.i
Seed 5 (id=005256bf1b5bc04f, size=28 bytes, fuzzer=cmplog, trial=3, discovered_at=108s, mutation_op=BytesRandSetMutator):
  0000: 49 49 49 49 49 49 49 49 49 49 49 49 49 07 00 00   IIIIIIIIIIIII...
  0010: 00 0d 00 00 0a 00 0a 00 00 21 20 20               .........!  


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  74(t)x1                             00(.)x10 74(t)x9 e0(.)x2 2d(-)x2 +17u  PARTIAL
   0x0001  79(y)x1                             72(r)x9 01(.)x8 08(.)x2 00(.)x2 +19u  DIFFER
   0x0002  70(p)x1                             00(.)x16 75(u)x9 ff(.)x2 0e(.)x2 +10u  DIFFER
   0x0003  31(1)x1                             00(.)x16 65(e)x9 ff(.)x2 df(.)x1 +12u  DIFFER
   0x0004  00(.)x1                             00(.)x19 df(.)x2 f4(.)x1 68(h)x1 +17u  PARTIAL
   0x0005  02(.)x1                             01(.)x15 00(.)x6 20( )x3 0e(.)x2 +12u  PARTIAL
   0x0006  20( )x1                             00(.)x17 a0(.)x7 20( )x4 e0(.)x1 +11u  PARTIAL
   0x0007  20( )x1                             00(.)x14 20( )x9 04(.)x3 01(.)x2 +10u  PARTIAL
   0x0008  20( )x1                             20( )x14 00(.)x9 10(.)x2 6e(n)x1 +14u  PARTIAL
   0x0009  3f(?)x1                             20( )x12 00(.)x5 7b({)x3 21(!)x2 +17u  DIFFER
   0x000a  21(!)x1                             00(.)x11 df(.)x7 ff(.)x7 20( )x3 +11u  DIFFER
   0x000b  20( )x1                             00(.)x18 20( )x6 01(.)x2 9a(.)x1 +13u  PARTIAL
   0x000c  6e(n)x1                             47(G)x14 00(.)x4 20( )x3 4d(M)x3 +15u  DIFFER
   0x000d  61(a)x1                             50(P)x10 20( )x6 00(.)x6 53(S)x4 +10u  DIFFER
   0x000e  6d(m)x1                             00(.)x10 4f(O)x10 55(U)x4 54(T)x2 +13u  DIFFER
   0x000f  65(e)x1                             53(S)x10 00(.)x8 42(B)x4 48(H)x2 +15u  DIFFER
   0x0010  b2(.)x1                             00(.)x10 20( )x8 df(.)x4 01(.)x3 +13u  DIFFER
   0x0011  b2(.)x1                             20( )x12 00(.)x8 01(.)x3 a9(.)x2 +14u  DIFFER
   0x0012  2d(-)x1                             00(.)x14 20( )x9 03(.)x3 80(.)x3 +10u  DIFFER
   0x0013  b2(.)x1                             00(.)x11 07(.)x7 8e(.)x2 0a(.)x2 +16u  DIFFER
   0x0014  00(.)x1                             00(.)x22 6e(n)x1 9a(.)x1 e0(.)x1 +14u  PARTIAL
   0x0015  00(.)x1                             00(.)x24 17(.)x2 20( )x2 74(t)x1 +10u  PARTIAL
   0x0016  00(.)x1                             00(.)x29 20( )x2 2d(-)x1 0a(.)x1 +6u  PARTIAL
   0x0017  21(!)x1                             00(.)x19 20( )x11 10(.)x2 68(h)x1 +5u  DIFFER
   0x0018  20( )x1                             00(.)x12 02(.)x8 20( )x4 6b(k)x1 +13u  PARTIAL
   0x0019  6b(k)x1                             00(.)x18 20( )x3 61(a)x2 1d(.)x2 +12u  DIFFER
   0x001a  20( )x1                             00(.)x13 71(q)x8 20( )x4 69(i)x1 +12u  PARTIAL
   0x001b  47(G)x1                             00(.)x14 f8(.)x5 20( )x4 01(.)x3 +10u  DIFFER
   0x001c  ac(.)x1                             00(.)x9 02(.)x4 17(.)x4 43(C)x2 +17u  DIFFER
   0x001d  47(G)x1                             00(.)x18 20( )x3 46(F)x2 3d(=)x1 +12u  DIFFER
   0x001e  42(B)x1                             00(.)x14 10(.)x5 20( )x3 ff(.)x2 +11u  DIFFER
   0x001f  20( )x1                             00(.)x10 04(.)x8 02(.)x4 54(T)x2 +11u  DIFFER
   0x0020  00(.)x1                             00(.)x20 70(p)x1 df(.)x1 39(9)x1 +13u  PARTIAL
   0x0021  00(.)x1                             01(.)x9 00(.)x4 ff(.)x3 07(.)x2 +17u  PARTIAL
   0x0022  00(.)x1                             00(.)x13 6e(n)x5 ff(.)x4 02(.)x3 +11u  PARTIAL
   0x0023  00(.)x1                             00(.)x13 20( )x5 01(.)x3 02(.)x2 +12u  PARTIAL
   0x0024  02(.)x1                             00(.)x10 20( )x10 01(.)x1 70(p)x1 +14u  PARTIAL
   0x0025  00(.)x1                             20( )x7 00(.)x6 03(.)x3 0e(.)x3 +14u  PARTIAL
   0x0026  2c(,)x1                             00(.)x11 20( )x5 10(.)x3 0e(.)x2 +14u  DIFFER
   0x0027  00(.)x1                             00(.)x12 04(.)x4 20( )x3 02(.)x3 +12u  PARTIAL
   ... (24 more divergent offsets)
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
  prompts_b/harfbuzz_5251.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5251,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S), value_profile_cmplog>cmplog (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5251 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5251 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5251 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).