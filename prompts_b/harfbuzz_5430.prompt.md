==== BLOCKER ====
Target: harfbuzz
Branch ID: 5430
Location: /src/harfbuzz/src/hb-ot-cmap-table.hh:1837:9
Enclosing function: OT::cmap::find_best_subtable(bool*) const
Source line:     if ((subtable = this->find_subtable (0, 0))) return subtable;
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           3        7          0  REFERENCE
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
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
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=6.60h  loser=24.00h
  avg hitcount on branch: winner=51  loser=0
  prob_div=1.00  dur_div=17.40h  hit_div=51
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5430/{W,L}/branch_coverage_show.txt

--- Enclosing function: OT::cmap::find_best_subtable(bool*) const (/src/harfbuzz/src/hb-ot-cmap-table.hh:1813-1841) ---
[ ]  1811  
[ ]  1812    const CmapSubtable *find_best_subtable (bool *symbol = nullptr) const
[B]  1813    {
[B]  1814      if (symbol) *symbol = false;
[ ]  1815  
[B]  1816      const CmapSubtable *subtable;
[ ]  1817  
[ ]  1818      /* Symbol subtable.
[ ]  1819       * Prefer symbol if available.
[ ]  1820       * https://github.com/harfbuzz/harfbuzz/issues/1918 */
[B]  1821      if ((subtable = this->find_subtable (3, 0)))
[ ]  1822      {
[ ]  1823        if (symbol) *symbol = true;
[ ]  1824        return subtable;
[ ]  1825      }
[ ]  1826  
[ ]  1827      /* 32-bit subtables. */
[B]  1828      if ((subtable = this->find_subtable (3, 10))) return subtable;
[B]  1829      if ((subtable = this->find_subtable (0, 6))) return subtable;
[B]  1830      if ((subtable = this->find_subtable (0, 4))) return subtable;
[ ]  1831  
[ ]  1832      /* 16-bit subtables. */
[B]  1833      if ((subtable = this->find_subtable (3, 1))) return subtable;
[B]  1834      if ((subtable = this->find_subtable (0, 3))) return subtable;
[B]  1835      if ((subtable = this->find_subtable (0, 2))) return subtable;
[B]  1836      if ((subtable = this->find_subtable (0, 1))) return subtable;
[B]  1837      if ((subtable = this->find_subtable (0, 0))) return subtable; <-- BLOCKER
[ ]  1838  
[ ]  1839      /* Meh. */
[L]  1840      return &Null (CmapSubtable);
[B]  1841    }

--- Caller (1 hop): OT::cmap::accelerator_t::accelerator_t(hb_face_t*) (/src/harfbuzz/src/hb-ot-cmap-table.hh:1848-1898, calls OT::cmap::find_best_subtable(bool*) const at line 1851) (±10 around call site) ---
[B]  1848      {
[B]  1849        this->table = hb_sanitize_context_t ().reference_table<cmap> (face);
[B]  1850        bool symbol;
[B]  1851        this->subtable = table->find_best_subtable (&symbol); <-- CALL
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

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  OT::NameRecord::score() const  (/src/harfbuzz/src/OT/name/name.hh:119-143, calls OT::cmap::find_best_subtable(bool*) const at line 120)
hop 2  OT::cmap::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cmap-table.hh:1848-1898, calls OT::cmap::find_best_subtable(bool*) const at line 1851)
hop 3  OT::name::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/OT/name/name.hh:480-516, calls OT::NameRecord::score() const at line 496)
hop 3  OT::cff2::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:515-515, calls OT::cmap::accelerator_t::accelerator_t(hb_face_t*) at line 515)
hop 3  OT::cff2_accelerator_t::cff2_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:538-538, calls OT::cmap::accelerator_t::accelerator_t(hb_face_t*) at line 538)
hop 4  OT::hmtx_accelerator_t::hmtx_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:449-449, calls OT::cff2::accelerator_t::accelerator_t(hb_face_t*) at line 449)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     207      2240  OT::CmapSubtableFormat0::get_glyph(unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:48-54)
     534         0  OT::CmapSubtableTrimmed<OT::IntType<unsigned short, 2u> >::get_glyph(unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:639-646)
     534         0  OT::CmapSubtableTrimmed<OT::IntType<unsigned int, 4u> >::get_glyph(unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:639-646)
     306         0  OT::EncodingRecord::cmp(OT::EncodingRecord const&) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:1458-1465)
     234         0  OT::EncodingRecord::sanitize(hb_sanitize_context_t*, void const*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:1468-1472)
     158         0  OT::CmapSubtableLongSegmented<OT::CmapSubtableFormat12>::get_glyph(unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:704-710)
     158         0  OT::CmapSubtableLongSegmented<OT::CmapSubtableFormat13>::get_glyph(unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:704-710)
     119         0  OT::CmapSubtable::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:1424-1437)
      81         0  OT::CmapSubtableFormat13::group_get_glyph(OT::CmapSubtableLongGroup const&, unsigned int)  (/src/harfbuzz/src/hb-ot-cmap-table.hh:871-871)
      77         0  OT::CmapSubtableFormat12::group_get_glyph(OT::CmapSubtableLongGroup const&, unsigned int)  (/src/harfbuzz/src/hb-ot-cmap-table.hh:799-800)
      30         0  OT::cmap::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:2058-2063)
       3        20  OT::CmapSubtableFormat0::collect_unicodes(hb_set_t*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:62-66)
      14         0  OT::CmapSubtableFormat0::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:81-84)
      12         0  OT::CmapSubtableTrimmed<OT::IntType<unsigned short, 2u> >::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:678-681)
      12         0  OT::CmapSubtableTrimmed<OT::IntType<unsigned int, 4u> >::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:678-681)
... (6 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  OT::cmap::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cmap-table.hh:1848-1898) ---
  d=2   L1855  T=0 F=10  T=0 F=20  if (st && st->u.format == 14)
  d=2   L1883  T=9 F=1  T=20 F=0  default:
  d=2   L1886  T=1 F=9  T=0 F=20  case 12:
  d=2   L1889  T=0 F=10  T=0 F=20  case  4:
--- d=1  OT::cmap::find_best_subtable(bool*) const  (/src/harfbuzz/src/hb-ot-cmap-table.hh:1813-1841) ---
  d=1   L1814  T=10 F=0  T=20 F=0  if (symbol) *symbol = false;
  d=1   L1821  T=0 F=10  T=0 F=20  if ((subtable = this->find_subtable (3, 0)))
  d=1   L1828  T=0 F=10  T=0 F=20  if ((subtable = this->find_subtable (3, 10))) return subt...
  d=1   L1829  T=0 F=10  T=0 F=20  if ((subtable = this->find_subtable (0, 6))) return subta...
  d=1   L1830  T=0 F=10  T=0 F=20  if ((subtable = this->find_subtable (0, 4))) return subta...
  d=1   L1833  T=0 F=10  T=0 F=20  if ((subtable = this->find_subtable (3, 1))) return subta...
  d=1   L1834  T=0 F=10  T=0 F=20  if ((subtable = this->find_subtable (0, 3))) return subta...
  d=1   L1835  T=0 F=10  T=0 F=20  if ((subtable = this->find_subtable (0, 2))) return subta...
  d=1   L1836  T=0 F=10  T=0 F=20  if ((subtable = this->find_subtable (0, 1))) return subta...
  d=1   L1837  T=10 F=0  T=0 F=20  if ((subtable = this->find_subtable (0, 0))) return subta...  <-- BLOCKER

[off-chain: 50 additional divergent branches across 17 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=9b29484356b4664e, size=80 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=1865s, mutation_op=BytesRandSetMutator,BytesSwapMutator,BytesRandInsertMutator,CrossoverInsertMutator,QwordAddMutator):
  0000: 00 01 00 00 00 02 20 20 20 3f 21 20 63 6d 61 70   ......   ?! cmap
  0010: 20 20 00 06 00 00 00 21 20 6b 20 47 53 55 42 1f     .....! k GSUB.
  0020: 20 00 00 00 03 00 00 00 00 00 00 00 21 20 6b 65    ...........! ke
  0030: 72 6e 20 20 df 8e 84 84 7a 84 61 70 20 20 00 06   rn  ....z.ap  ..
Seed 2 (id=14a27d1d9974c46e, size=86 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=2208s, mutation_op=BytesDeleteMutator,BytesDeleteMutator,BytesDeleteMutator,BytesInsertCopyMutator,TokenReplace,BytesExpandMutator,BytesRandSetMutator):
  0000: 00 01 00 00 00 02 20 20 20 3f 21 20 63 6d 61 70   ......   ?! cmap
  0010: 20 20 00 06 00 00 00 21 20 6b 20 47 53 55 42 1f     .....! k GSUB.
  0020: 20 00 00 00 03 00 00 00 00 00 00 00 21 20 6b 65    ...........! ke
  0030: 72 6e 20 20 df 8e 84 84 7a 84 61 70 20 20 00 06   rn  ....z.ap  ..
Seed 3 (id=a27e1294281af760, size=321 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=3895s, mutation_op=ByteAddMutator,ByteRandMutator,DwordInterestingMutator):
  0000: 00 01 00 00 00 02 20 20 e0 3f 21 20 63 6d 61 70   ......  .?! cmap
  0010: 20 20 00 06 00 00 00 21 20 6b 20 47 53 55 42 20     .....! k GSUB 
  0020: 20 00 00 00 0e 00 02 00 06 00 00 01 00 00 00 00    ...............
  0030: 00 00 00 00 00 00 00 00 00 00 00 00 01 00 1d 00   ................
Seed 4 (id=ad28ac4555050a6f, size=321 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=4103s, mutation_op=ByteInterestingMutator,QwordAddMutator,DwordInterestingMutator):
  0000: 00 01 00 00 00 02 20 20 e0 3f 21 20 63 6d 61 70   ......  .?! cmap
  0010: 20 20 00 06 00 00 00 21 20 6b 20 47 53 55 42 20     .....! k GSUB 
  0020: 20 00 00 00 0e 00 0a 00 06 00 00 00 00 00 00 00    ...............
  0030: 00 00 00 00 00 00 00 00 00 00 00 00 04 00 1d 00   ................
Seed 5 (id=887a39b289ccfd49, size=301 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=4104s, mutation_op=BytesSetMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 02 20 20 e0 3f 21 20 63 6d 61 70   ......  .?! cmap
  0010: 20 20 00 06 00 00 00 21 20 6b 20 47 53 55 42 20     .....! k GSUB 
  0020: 20 00 00 00 0e 00 02 00 06 00 00 01 00 00 00 00    ...............
  0030: 00 00 00 00 00 00 00 00 00 00 00 00 01 00 1d 00   ................

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=002a5b2b8b5c414d, size=54 bytes, fuzzer=value_profile, trial=2, discovered_at=70s, mutation_op=TokenReplace,BytesCopyMutator,ByteAddMutator,BytesSetMutator):
  0000: 92 92 92 df 68 2d 68 81 6e 74 00 9a 9a 20 8e 8e   ....h-h.nt... ..
  0010: 8e 8e 79 8e 9a 17 00 00 00 01 20 20 44 46 ff 54   ..y.......  DF.T
  0020: 70 7f 70 70 70 70 70 52 9a 9a ff df 68 2d 68 61   p.pppppR....h-ha
  0030: 6e 74 00 9a 9a 74                                 nt...t
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
   0x0000  00(.)x10                            00(.)x3 e0(.)x2 20( )x2 92(.)x1 +12u  PARTIAL
   0x0001  01(.)x10                            00(.)x2 92(.)x1 17(.)x1 e8(.)x1 +15u  PARTIAL
   0x0002  00(.)x10                            00(.)x8 6e(n)x2 92(.)x1 ff(.)x1 +8u  PARTIAL
   0x0003  00(.)x10                            00(.)x10 df(.)x1 ff(.)x1 6c(l)x1 +7u  PARTIAL
   0x0004  00(.)x10                            df(.)x2 00(.)x2 68(h)x1 1a(.)x1 +14u  PARTIAL
   0x0005  02(.)x10                            00(.)x5 20( )x3 0e(.)x2 2d(-)x1 +9u  DIFFER
   0x0006  20( )x10                            00(.)x11 20( )x2 68(h)x1 73(s)x1 +5u  PARTIAL
   0x0007  20( )x10                            00(.)x11 39(9)x2 81(.)x1 55(U)x1 +5u  PARTIAL
   0x0008  e0(.)x8 20( )x2                     00(.)x4 20( )x2 10(.)x2 6e(n)x1 +11u  PARTIAL
   0x0009  3f(?)x10                            00(.)x4 20( )x2 74(t)x1 2b(+)x1 +12u  DIFFER
   0x000a  21(!)x10                            00(.)x9 29())x1 aa(.)x1 61(a)x1 +8u  DIFFER
   0x000b  20( )x10                            00(.)x8 9a(.)x1 29())x1 13(.)x1 +9u  DIFFER
   0x000c  63(c)x10                            00(.)x5 9a(.)x1 2c(,)x1 2b(+)x1 +12u  DIFFER
   0x000d  6d(m)x10                            00(.)x6 20( )x4 18(.)x3 01(.)x1 +5u  DIFFER
   0x000e  61(a)x10                            00(.)x8 8e(.)x1 18(.)x1 3d(=)x1 +8u  DIFFER
   0x000f  70(p)x10                            00(.)x7 8e(.)x1 fa(.)x1 3d(=)x1 +9u  DIFFER
   0x0010  20( )x10                            00(.)x5 20( )x2 8e(.)x1 3d(=)x1 +10u  PARTIAL
   0x0011  20( )x5 18(.)x5                     00(.)x3 a9(.)x2 20( )x2 8e(.)x1 +11u  PARTIAL
   0x0012  00(.)x9 f0(.)x1                     00(.)x10 79(y)x1 18(.)x1 3d(=)x1 +6u  PARTIAL
   0x0013  06(.)x10                            00(.)x7 8e(.)x1 55(U)x1 65(e)x1 +9u  DIFFER
   0x0014  00(.)x10                            00(.)x5 9a(.)x1 e0(.)x1 0e(.)x1 +11u  PARTIAL
   0x0015  00(.)x10                            00(.)x5 20( )x3 17(.)x2 3d(=)x1 +8u  PARTIAL
   0x0016  00(.)x10                            00(.)x12 20( )x2 ff(.)x1 3d(=)x1 +3u  PARTIAL
   0x0017  21(!)x10                            00(.)x11 20( )x2 3d(=)x1 2d(-)x1 +3u  DIFFER
   0x0018  20( )x10                            00(.)x4 20( )x3 61(a)x1 3d(=)x1 +9u  PARTIAL
   0x0019  6b(k)x10                            00(.)x3 20( )x2 a8(.)x2 01(.)x1 +10u  DIFFER
   0x001a  20( )x10                            00(.)x8 20( )x2 69(i)x1 3d(=)x1 +6u  PARTIAL
   0x001b  47(G)x10                            00(.)x7 20( )x3 3d(=)x1 74(t)x1 +5u  DIFFER
   0x001c  53(S)x7 76(v)x2 43(C)x1             00(.)x4 44(D)x1 3d(=)x1 e3(.)x1 +10u  DIFFER
   0x001d  55(U)x7 68(h)x2 46(F)x1             20( )x3 00(.)x3 46(F)x1 3d(=)x1 +9u  PARTIAL
   0x001e  42(B)x6 65(e)x2 43(C)x1 46(F)x1     00(.)x11 ff(.)x2 80(.)x1 6a(j)x1 +2u  DIFFER
   0x001f  20( )x5 1f(.)x2 61(a)x2 32(2)x1     00(.)x9 54(T)x2 ff(.)x1 95(.)x1 +4u  DIFFER
   0x0020  20( )x10                            00(.)x5 70(p)x1 df(.)x1 39(9)x1 +9u  DIFFER
   0x0021  00(.)x10                            00(.)x3 0e(.)x2 7f(.)x1 20( )x1 +10u  PARTIAL
   0x0022  00(.)x10                            00(.)x9 70(p)x1 64(d)x1 1b(.)x1 +5u  PARTIAL
   0x0023  00(.)x10                            00(.)x8 70(p)x1 73(s)x1 6d(m)x1 +6u  PARTIAL
   0x0025  00(.)x9 fa(.)x1                     00(.)x4 03(.)x2 0e(.)x2 70(p)x1 +8u  PARTIAL
   0x0026  00(.)x5 02(.)x4 0a(.)x1             00(.)x9 70(p)x1 ff(.)x1 9f(.)x1 +5u  PARTIAL
   0x0027  00(.)x9 0d(.)x1                     00(.)x6 20( )x2 61(a)x2 52(R)x1 +6u  PARTIAL
   0x0028  06(.)x5 00(.)x4 ff(.)x1             00(.)x8 9a(.)x1 20( )x1 6b(k)x1 +6u  PARTIAL
   ... (22 more divergent offsets)
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
  prompts_b/harfbuzz_5430.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5430,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5430 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5430 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5430 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).