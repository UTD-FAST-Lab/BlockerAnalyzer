==== BLOCKER ====
Target: harfbuzz
Branch ID: 5391
Location: /src/harfbuzz/src/hb-open-file.hh:490:5
Enclosing function: OT::OpenTypeFontFile::get_face(unsigned int, unsigned int*) const
Source line:     case DFontTag:	return u.rfHeader.get_face (i, base_offset);
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            9        1          0  winner (I2S vs cmplog)
cmplog                           0       10          0  loser (I2S vs naive)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             7        3          0  REFERENCE
naive_ctx                       10        0          0  REFERENCE
naive_ngram4                    10        0          0  REFERENCE
mopt                             9        1          0  REFERENCE
minimizer                        7        3          0  REFERENCE
fast                            10        0          0  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=6.50h  loser=24.00h
  avg hitcount on branch: winner=72  loser=0
  prob_div=0.90  dur_div=17.50h  hit_div=72
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5391/{W,L}/branch_coverage_show.txt

--- Enclosing function: OT::OpenTypeFontFile::get_face(unsigned int, unsigned int*) const (/src/harfbuzz/src/hb-open-file.hh:478-493) ---
[ ]   476    }
[ ]   477    const OpenTypeFontFace& get_face (unsigned int i, unsigned int *base_offset = nullptr) const
[B]   478    {
[B]   479      if (base_offset)
[B]   480        *base_offset = 0;
[B]   481      switch (u.tag) {
[ ]   482      /* Note: for non-collection SFNT data we ignore index.  This is because
[ ]   483       * Apple dfont container is a container of SFNT's.  So each SFNT is a
[ ]   484       * non-TTC, but the index is more than zero. */
[ ]   485      case CFFTag:	/* All the non-collection tags */
[ ]   486      case TrueTag:
[ ]   487      case Typ1Tag:
[L]   488      case TrueTypeTag:	return u.fontFace;
[ ]   489      case TTCTag:	return u.ttcHeader.get_face (i);
[W]   490      case DFontTag:	return u.rfHeader.get_face (i, base_offset); <-- BLOCKER
[ ]   491      default:		return Null (OpenTypeFontFace);
[B]   492      }
[B]   493    }

--- Caller (1 hop): hb-face.cc:_hb_face_for_data_reference_table(hb_face_t*, unsigned int, void*) (/src/harfbuzz/src/hb-face.cc:174-189, calls OT::OpenTypeFontFile::get_face(unsigned int, unsigned int*) const at line 182) (full body — short) ---
[B]   174  {
[B]   175    hb_face_for_data_closure_t *data = (hb_face_for_data_closure_t *) user_data;
[ ]   176  
[B]   177    if (tag == HB_TAG_NONE)
[ ]   178      return hb_blob_reference (data->blob);
[ ]   179  
[B]   180    const OT::OpenTypeFontFile &ot_file = *data->blob->as<OT::OpenTypeFontFile> ();
[B]   181    unsigned int base_offset;
[B]   182    const OT::OpenTypeFontFace &ot_face = ot_file.get_face (data->index, &base_offset); <-- CALL
[ ]   183  
[B]   184    const OT::OpenTypeTable &table = ot_face.get_table_by_tag (tag);
[ ]   185  
[B]   186    hb_blob_t *blob = hb_blob_create_sub_blob (data->blob, base_offset + table.offset, table.length);
[ ]   187  
[B]   188    return blob;
[B]   189  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  OT::TTCHeader::get_face(unsigned int) const  (/src/harfbuzz/src/hb-open-file.hh:258-264, calls OT::OpenTypeFontFile::get_face(unsigned int, unsigned int*) const at line 261)
hop 2  OT::TTCHeaderVersion1::get_face(unsigned int) const  (/src/harfbuzz/src/hb-open-file.hh:224-224, calls OT::OpenTypeFontFile::get_face(unsigned int, unsigned int*) const at line 224)
hop 3  OT::ResourceRecord::sanitize(hb_sanitize_context_t*, void const*) const  (/src/harfbuzz/src/hb-open-file.hh:301-306, calls OT::TTCHeaderVersion1::get_face(unsigned int) const at line 305)
hop 4  CFF::CFF2FDSelect::sanitize(hb_sanitize_context_t*, unsigned int) const  (/src/harfbuzz/src/hb-ot-cff2-table.hh:90-102, calls OT::ResourceRecord::sanitize(hb_sanitize_context_t*, void const*) const at line 97)
hop 5  CFF::CFF2VariationStore::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-cff2-table.hh:117-120, calls CFF::CFF2FDSelect::sanitize(hb_sanitize_context_t*, unsigned int) const at line 119)
hop 5  OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:398-475, calls CFF::CFF2FDSelect::sanitize(hb_sanitize_context_t*, unsigned int) const at line 416)
hop 6  OT::cff2::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:515-515, calls OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*) at line 515)
hop 6  OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::~accelerator_templ_t()  (/src/harfbuzz/src/hb-ot-cff2-table.hh:476-476, calls OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*) at line 476)
hop 7  OT::cff2_accelerator_t::cff2_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:538-538, calls OT::cff2::accelerator_t::accelerator_t(hb_face_t*) at line 538)
hop 7  OT::hmtx_accelerator_t::hmtx_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:449-449, calls OT::cff2::accelerator_t::accelerator_t(hb_face_t*) at line 449)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0       384  OT::TableRecord::cmp(OT::Tag) const  (/src/harfbuzz/src/hb-open-file.hh:56-56)
     232         0  OT::ResourceTypeRecord::is_sfnt() const  (/src/harfbuzz/src/hb-open-file.hh:328-328)
     232         0  OT::ResourceMap::get_type_record(unsigned int) const  (/src/harfbuzz/src/hb-open-file.hh:397-397)
     154         0  OT::ResourceMap::get_face(unsigned int, void const*) const  (/src/harfbuzz/src/hb-open-file.hh:371-382)
     154         0  OT::ResourceMap::get_type_count() const  (/src/harfbuzz/src/hb-open-file.hh:394-394)
     154         0  OT::ResourceForkHeader::get_face(unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-open-file.hh:420-425)
       0        10  OT::OpenTypeOffsetTable::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-open-file.hh:201-204)
       6         0  OT::ResourceTypeRecord::get_resource_count() const  (/src/harfbuzz/src/hb-open-file.hh:326-326)
       6         0  OT::ResourceTypeRecord::sanitize(hb_sanitize_context_t*, void const*, void const*) const  (/src/harfbuzz/src/hb-open-file.hh:337-343)
       4         0  OT::ResourceMap::sanitize(hb_sanitize_context_t*, void const*) const  (/src/harfbuzz/src/hb-open-file.hh:385-391)
       4         0  OT::ResourceForkHeader::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-open-file.hh:428-433)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OT::OpenTypeFontFile::get_face(unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-open-file.hh:478-493) ---
  d=1   L 479  T=154 F=0  T=384 F=0  if (base_offset)
  d=1   L 485  T=0 F=154  T=0 F=384  case CFFTag:	/* All the non-collection tags */
  d=1   L 486  T=0 F=154  T=0 F=384  case TrueTag:
  d=1   L 487  T=0 F=154  T=0 F=384  case Typ1Tag:
  d=1   L 488  T=0 F=154  T=384 F=0  case TrueTypeTag:	return u.fontFace;
  d=1   L 489  T=0 F=154  T=0 F=384  case TTCTag:	return u.ttcHeader.get_face (i);
  d=1   L 490  T=154 F=0  T=0 F=384  case DFontTag:	return u.rfHeader.get_face (i, base_offset);  <-- BLOCKER
  d=1   L 491  T=0 F=154  T=0 F=384  default:		return Null (OpenTypeFontFace);

[off-chain: 19 additional divergent branches across 9 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=b2a2493cc4390501, size=41 bytes, fuzzer=naive, trial=1, discovered_at=201s, mutation_op=BytesExpandMutator,ByteRandMutator,BytesDeleteMutator):
  0000: 00 00 01 00 00 00 00 00 00 00 00 00 00 00 1a 00   ................
  0010: 00 00 00 00 1a 00 95 01 00 00 00 00 e3 38 8e 03   .............8..
  0020: 01 00 00 00 00 95 cc 95 95                        .........
Seed 2 (id=b992070cb47a232a, size=79 bytes, fuzzer=naive, trial=1, discovered_at=4393s, mutation_op=BytesCopyMutator,BytesDeleteMutator,ByteIncMutator):
  0000: 00 00 01 00 00 00 00 01 00 00 00 00 06 00 00 34   ...............4
  0010: 07 00 00 cc 0e 00 00 cb 0c 00 00 00 0c 00 00 cb   ................
  0020: ff 00 00 00 00 00 10 1a 06 00 f6 4e 06 00 69 68   ...........N..ih
  0030: 0e 00 00 cb 0c 00 00 cb 0c 00 00 cb 0c 00 00 cc   ................
Seed 3 (id=abcfbc1efd39322f, size=75 bytes, fuzzer=naive, trial=1, discovered_at=13082s, mutation_op=BitFlipMutator,ByteFlipMutator):
  0000: 00 00 01 00 00 00 00 00 00 00 00 00 00 00 1a 00   ................
  0010: 00 00 e3 38 8e 03 01 00 00 00 69 2d 68 61 6e 74   ...8......i-hant
  0020: 2d 00 00 40 00 00 74 2c 0e f6 00 0c 18 00 00 65   -..@..t,.......e
  0030: 6d 00 5c 0f 18 00 00 7d 14 14 01 00 00 2d 00 31   m.\....}.....-.1
Seed 4 (id=09f42ea6e02325fe, size=136 bytes, fuzzer=naive, trial=1, discovered_at=19332s, mutation_op=BitFlipMutator,CrossoverReplaceMutator,BytesSetMutator,ByteRandMutator,BytesExpandMutator):
  0000: 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0010: 00 00 00 11 20 0c 0c 00 00 01 1a 00 a6 41 a6 a6   .... ........A..
  0020: a6 5a a6 80 61 e9 17 00 00 e9 17 00 66 a6 5a a6   .Z..a.......f.Z.
  0030: 80 61 e9 17 00 00 e9 17 00 66 10 18 1d 20 10 00   .a.......f... ..

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=000abe48ad9847bd, size=86 bytes, fuzzer=cmplog, trial=1, discovered_at=2302s, mutation_op=TokenReplace,CrossoverInsertMutator,ByteInterestingMutator,ByteNegMutator,ByteNegMutator,BytesRandInsertMutator):
  0000: 00 01 00 00 00 01 20 00 20 ff 20 20 4d 41 54 48   ...... . .  MATH
  0010: 00 01 00 00 00 00 00 10 00 10 00 22 01 01 01 00   ..........."....
  0020: 00 00 00 02 00 02 00 02 00 02 00 00 00 10 00 73   ...............s
  0030: 6e 2d 00 01 01 01 00 ff ff 00 00 17 00 00 e2 17   n-..............
Seed 2 (id=002c9ad92acce91b, size=171 bytes, fuzzer=cmplog, trial=1, discovered_at=2579s, mutation_op=BytesInsertMutator,ByteFlipMutator):
  0000: 00 01 00 00 00 01 20 19 21 20 20 20 47 50 4f 53   ...... .!   GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 47 50 4f 00 00   ...........GPO..
  0020: 10 00 01 01 04 53 00 01 00 0d 00 14 01 ff fb 13   .....S..........
  0030: 72 f9 f0 01 4f 53 03 03 00 04 00 1a 43 22 55 41   r...OS......C"UA
Seed 3 (id=003bfa8ebe690138, size=144 bytes, fuzzer=cmplog, trial=1, discovered_at=2770s, mutation_op=BytesInsertCopyMutator,TokenReplace,WordInterestingMutator,TokenInsert):
  0000: 00 01 00 00 00 01 07 20 21 20 1e 20 47 50 4f 53   ....... ! . GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 47 03 01 0c 00   ...........G....
  0020: 00 00 00 07 4f 00 00 10 ff 7a 68 2d 68 61 6e 74   ....O....zh-hant
  0030: 00 00 00 02 00 44 00 10 00 ff ff ff 3f 0d 02 00   .....D......?...
Seed 4 (id=002e1500bcab55a2, size=174 bytes, fuzzer=cmplog, trial=1, discovered_at=3377s, mutation_op=BytesCopyMutator,ByteAddMutator):
  0000: 00 01 00 00 00 01 07 20 21 20 1e 20 47 50 4f 53   ....... ! . GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 47 00 00 00 03   ...........G....
  0020: ff de 00 02 4f 00 00 10 00 01 00 10 00 06 00 06   ....O...........
  0030: 00 10 00 01 00 00 00 06 00 06 03 00 1d 00 e9 ff   ................
Seed 5 (id=000d6a0375e6457c, size=135 bytes, fuzzer=cmplog, trial=1, discovered_at=3730s, mutation_op=ByteInterestingMutator,BytesExpandMutator):
  0000: 00 01 00 00 00 01 20 20 21 20 20 20 47 53 55 42   ......  !   GSUB
  0010: 00 01 00 27 00 00 00 10 00 02 00 00 00 00 00 00   ...'............
  0020: 10 00 00 04 00 01 00 10 00 02 00 00 00 00 00 00   ................
  0030: 00 00 20 27 00 00 00 10 00 02 00 03 02 00 20 04   .. '.......... .


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0001  00(.)x4                             01(.)x10                            DIFFER
   0x0002  01(.)x4                             00(.)x10                            DIFFER
   0x0005  00(.)x4                             01(.)x10                            DIFFER
   0x0006  00(.)x4                             07(.)x6 20( )x3 ff(.)x1             DIFFER
   0x0007  00(.)x3 01(.)x1                     20( )x8 00(.)x1 19(.)x1             PARTIAL
   0x0008  00(.)x4                             21(!)x9 20( )x1                     DIFFER
   0x0009  00(.)x4                             20( )x9 ff(.)x1                     DIFFER
   0x000a  00(.)x4                             1e(.)x7 20( )x3                     DIFFER
   0x000b  00(.)x4                             20( )x10                            DIFFER
   0x000c  00(.)x3 06(.)x1                     47(G)x9 4d(M)x1                     DIFFER
   0x000d  00(.)x4                             50(P)x7 53(S)x2 41(A)x1             DIFFER
   0x000e  1a(.)x2 00(.)x2                     4f(O)x7 55(U)x2 54(T)x1             DIFFER
   0x000f  00(.)x3 34(4)x1                     53(S)x7 42(B)x2 48(H)x1             DIFFER
   0x0010  00(.)x3 07(.)x1                     00(.)x10                            PARTIAL
   0x0011  00(.)x4                             01(.)x10                            DIFFER
   0x0012  00(.)x3 e3(.)x1                     00(.)x10                            PARTIAL
   0x0013  00(.)x1 cc(.)x1 38(8)x1 11(.)x1     0d(.)x8 00(.)x1 27(')x1             PARTIAL
   0x0014  1a(.)x1 0e(.)x1 8e(.)x1 20( )x1     00(.)x10                            DIFFER
   0x0015  00(.)x2 03(.)x1 0c(.)x1             00(.)x10                            PARTIAL
   0x0016  95(.)x1 00(.)x1 01(.)x1 0c(.)x1     00(.)x10                            PARTIAL
   0x0017  00(.)x2 01(.)x1 cb(.)x1             10(.)x10                            DIFFER
   0x0018  00(.)x3 0c(.)x1                     00(.)x10                            PARTIAL
   0x0019  00(.)x3 01(.)x1                     02(.)x9 10(.)x1                     DIFFER
   0x001a  00(.)x2 69(i)x1 1a(.)x1             00(.)x10                            PARTIAL
   0x001b  00(.)x3 2d(-)x1                     47(G)x8 22(")x1 00(.)x1             PARTIAL
   0x001c  e3(.)x1 0c(.)x1 68(h)x1 a6(.)x1     00(.)x3 01(.)x2 02(.)x2 50(P)x1 +2u  DIFFER
   0x001d  38(8)x1 00(.)x1 61(a)x1 41(A)x1     00(.)x6 01(.)x2 4f(O)x1 0c(.)x1     PARTIAL
   0x001e  8e(.)x1 00(.)x1 6e(n)x1 a6(.)x1     00(.)x8 01(.)x1 0c(.)x1             PARTIAL
   0x001f  03(.)x1 cb(.)x1 74(t)x1 a6(.)x1     00(.)x7 03(.)x2 06(.)x1             PARTIAL
   0x0020  01(.)x1 ff(.)x1 2d(-)x1 a6(.)x1     00(.)x7 10(.)x2 ff(.)x1             PARTIAL
   0x0021  00(.)x3 5a(Z)x1                     00(.)x8 de(.)x1 02(.)x1             PARTIAL
   0x0022  00(.)x3 a6(.)x1                     00(.)x9 01(.)x1                     PARTIAL
   0x0023  00(.)x2 40(@)x1 80(.)x1             02(.)x3 08(.)x3 04(.)x2 01(.)x1 +1u  DIFFER
   0x0024  00(.)x3 61(a)x1                     4f(O)x6 00(.)x3 04(.)x1             PARTIAL
   0x0025  00(.)x2 95(.)x1 e9(.)x1             02(.)x4 00(.)x3 53(S)x1 01(.)x1 +1u  PARTIAL
   0x0026  cc(.)x1 10(.)x1 74(t)x1 17(.)x1     00(.)x10                            DIFFER
   0x0027  95(.)x1 1a(.)x1 2c(,)x1 00(.)x1     10(.)x7 02(.)x1 01(.)x1 40(@)x1     DIFFER
   0x0028  95(.)x1 06(.)x1 0e(.)x1 00(.)x1     00(.)x9 ff(.)x1                     PARTIAL
   0x0029  00(.)x1 f6(.)x1 e9(.)x1             02(.)x4 01(.)x2 10(.)x2 0d(.)x1 +1u  DIFFER
   0x002a  f6(.)x1 00(.)x1 17(.)x1             00(.)x8 68(h)x1 19(.)x1             PARTIAL
   ... (21 more divergent offsets)
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
  prompts_b/harfbuzz_5391.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5391,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5391 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5391 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5391 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).