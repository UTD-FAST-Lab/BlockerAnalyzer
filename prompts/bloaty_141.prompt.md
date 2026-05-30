==== BLOCKER ====
Target: bloaty
Branch ID: 141
Location: /src/bloaty/src/range_map.cc:59:34
Enclosing function: bloaty::RangeMap::FindContaining(unsigned long) const
Source line:   if (it == mappings_.begin() || (--it, !EntryContains(it, addr))) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    1        9          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             3        7          0  REFERENCE
grimoire                         8        2          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=2.30h  loser=22.10h
  avg hitcount on branch: winner=16091  loser=11
  prob_div=0.90  dur_div=19.80h  hit_div=16080
  subject-level: delta_AUC=49070700.0  p_AUC=0.0002  delta_Final=792.5  p_final=0.0002
--- Pair 2: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=8.50h  loser=24.00h
  avg hitcount on branch: winner=23936  loser=0
  prob_div=0.80  dur_div=15.50h  hit_div=23936
  subject-level: delta_AUC=26255160.0  p_AUC=0.0002  delta_Final=523.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/bloaty/141/{W,L}/branch_coverage_show.txt

--- Enclosing function: bloaty::RangeMap::FindContaining(unsigned long) const (/src/bloaty/src/range_map.cc:57-64) ---
[B]    55  }
[ ]    56  
[B]    57  RangeMap::Map::const_iterator RangeMap::FindContaining(uint64_t addr) const {
[B]    58    auto it = mappings_.upper_bound(addr);  // Entry directly after.
[B]    59    if (it == mappings_.begin() || (--it, !EntryContains(it, addr))) { <-- BLOCKER
[W]    60      return mappings_.end();
[B]    61    } else {
[B]    62      return it;
[B]    63    }
[B]    64  }

--- Caller (1 hop): bloaty::RangeMap::CoversRange(unsigned long, unsigned long) const (/src/bloaty/src/range_map.cc:307-321, calls bloaty::RangeMap::FindContaining(unsigned long) const at line 308) (full body — short) ---
[B]   307  bool RangeMap::CoversRange(uint64_t addr, uint64_t size) const {
[B]   308    auto it = FindContaining(addr); <-- CALL
[B]   309    uint64_t end = addr + size;
[B]   310    assert(end >= addr);
[ ]   311  
[B]   312    while (true) {
[B]   313      if (addr >= end) {
[B]   314        return true;
[B]   315      } else if (it == mappings_.end() || !EntryContains(it, addr)) {
[ ]   316        return false;
[ ]   317      }
[B]   318      addr = RangeEnd(it);
[B]   319      it++;
[B]   320    }
[B]   321  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  bloaty::RangeMap::Translate(unsigned long, unsigned long*) const  (/src/bloaty/src/range_map.cc:87-95, calls bloaty::RangeMap::FindContaining(unsigned long) const at line 88)
hop 2  bloaty::RangeMap::TryGetLabel(unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >*) const  (/src/bloaty/src/range_map.cc:97-105, calls bloaty::RangeMap::FindContaining(unsigned long) const at line 98)
hop 3  bloaty::RangeSink::AddFileRangeForVMAddr(char const*, unsigned long, std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/bloaty.cc:1194-1217, calls bloaty::RangeMap::TryGetLabel(unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >*) const at line 1205)
hop 3  bloaty::RangeSink::AddVMRangeForVMAddr(char const*, unsigned long, unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1252-1275, calls bloaty::RangeMap::TryGetLabel(unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >*) const at line 1263)
hop 3  bloaty::RangeSink::TranslateFileToVM(char const*)  (/src/bloaty/src/bloaty.cc:1349-1360, calls bloaty::RangeMap::Translate(unsigned long, unsigned long*) const at line 1354)
hop 3  bloaty::RangeSink::TranslateVMToFile(unsigned long)  (/src/bloaty/src/bloaty.cc:1362-1371, calls bloaty::RangeMap::Translate(unsigned long, unsigned long*) const at line 1365)
hop 4  bloaty::DisassembleFindReferences(bloaty::DisassemblyInfo const&, bloaty::RangeSink*)  (/src/bloaty/src/disassemble.cc:43-94, calls bloaty::RangeSink::AddVMRangeForVMAddr(char const*, unsigned long, unsigned long, unsigned long) at line 84)
hop 4  bloaty::ReadEhFrame(std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*)  (/src/bloaty/src/eh_frame.cc:125-226, calls bloaty::RangeSink::AddFileRangeForVMAddr(char const*, unsigned long, std::basic_string_view<char, std::char_traits<char> >) at line 223)
hop 4  bloaty::ReadEhFrameHdr(std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*)  (/src/bloaty/src/eh_frame.cc:230-262, calls bloaty::RangeSink::AddFileRangeForVMAddr(char const*, unsigned long, std::basic_string_view<char, std::char_traits<char> >) at line 254)
hop 4  bloaty::ReadEncodedPointer(unsigned char, bool, std::basic_string_view<char, std::char_traits<char> >*, char const*, bloaty::RangeSink*)  (/src/bloaty/src/eh_frame.cc:27-100, calls bloaty::RangeSink::TranslateFileToVM(char const*) at line 76)
hop 4  elf.cc:bloaty::(anonymous namespace)::ReadELFSymbols(bloaty::InputFile const&, bloaty::RangeSink*, std::map<std::basic_string_view<char, std::char_traits<char> >, std::pair<unsigned long, unsigned long>, std::less<std::basic_string_view<char, std::char_traits<char> > >, std::allocator<std::pair<std::basic_string_view<char, std::char_traits<char> > const, std::pair<unsigned long, unsigned long> > > >*, bool)::$_0::operator()(bloaty::(anonymous namespace)::ElfFile const&, std::basic_string_view<char, std::char_traits<char> >, unsigned long) const  (/src/bloaty/src/elf.cc:855-921, calls bloaty::RangeSink::TranslateVMToFile(unsigned long) at line 915)
hop 5  elf.cc:bloaty::(anonymous namespace)::ReadELFTables(bloaty::InputFile const&, bloaty::RangeSink*)::$_0::operator()(bloaty::(anonymous namespace)::ElfFile const&, std::basic_string_view<char, std::char_traits<char> >, unsigned int) const  (/src/bloaty/src/elf.cc:990-1017, calls bloaty::ReadEhFrame(std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*) at line 1012)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
    1260      6460  bloaty::RangeMap::FindContainingOrAfter(unsigned long)  (/src/bloaty/src/range_map.cc:66-74)
    1690      6440  bloaty::RangeMap::AddRange(unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/range_map.cc:146-148)
     957      2940  void bloaty::RangeMap::MaybeSetLabel<std::_Rb_tree_iterator<std::pair<unsigned long const, bloaty::RangeMap::Entry> > >(std::_Rb_tree_iterator<std::pair<unsigned long const, bloaty::RangeMap::Entry> >, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long, unsigned long)  (/src/bloaty/src/range_map.cc:152-179)
     252      1700  bloaty::RangeMap::AddRangeWithTranslation(unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::RangeMap const&, bool, bloaty::RangeMap*)  (/src/bloaty/src/range_map.cc:257-289)
     424      1720  bool bloaty::RangeMap::TranslateAndTrimRangeWithEntry<std::_Rb_tree_const_iterator<std::pair<unsigned long const, bloaty::RangeMap::Entry> > >(std::_Rb_tree_const_iterator<std::pair<unsigned long const, bloaty::RangeMap::Entry> >, unsigned long, unsigned long, unsigned long*, unsigned long*, unsigned long*) const  (/src/bloaty/src/range_map.cc:34-55)
     562      1720  bloaty::RangeMap::FindContaining(unsigned long) const  (/src/bloaty/src/range_map.cc:57-64)  <-- enclosing
     310        20  bloaty::RangeMap::CoversRange(unsigned long, unsigned long) const  (/src/bloaty/src/range_map.cc:307-321)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  bloaty::RangeMap::FindContaining(unsigned long) const  (/src/bloaty/src/range_map.cc:57-64) ---
  d=1   L  59  T=101 F=402  T=0 F=1720  if (it == mappings_.begin() || (--it, !EntryContains(it, ...  <-- BLOCKER
  d=1   L  59  T=160 F=402  T=0 F=1720  if (it == mappings_.begin() || (--it, !EntryContains(it, ...  <-- BLOCKER

[off-chain: 32 additional divergent branches across 7 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=0cc6115ee776f4d4, size=373 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=3505s, mutation_op=BytesExpandMutator,DwordInterestingMutator,BitFlipMutator,CrossoverInsertMutator):
  0000: ce fa ed fe 7f 95 e8 00 20 10 18 24 24 20 20 20   ........ ..$$   
  0010: 01 00 00 00 20 20 20 00 00 20 72 00 01 00 00 00   ....   .. r.....
  0020: 0c 01 00 00 ff e9 02 00 1c 00 00 00 5f 01 02 02   ............_...
  0030: 01 00 00 00 00 00 04 00 01 00 00 00 00 00 00 00   ................
Seed 2 (id=0543a304ad99ddc6, size=384 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=3506s, mutation_op=BytesInsertMutator):
  0000: ce fa ed fe 7f 95 e8 00 20 10 18 24 24 20 20 20   ........ ..$$   
  0010: 01 00 00 00 20 20 20 00 00 20 72 00 01 00 00 00   ....   .. r.....
  0020: 0c 01 00 00 ff e9 02 00 1c 00 00 00 5f 01 02 02   ............_...
  0030: 01 00 00 00 00 00 04 00 01 00 00 00 00 00 00 00   ................
Seed 3 (id=53f2923b22c778c6, size=332 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=5611s, mutation_op=ByteFlipMutator,BytesInsertMutator,ByteIncMutator,QwordAddMutator,BytesCopyMutator):
  0000: ce fa ed fe 7f 95 e8 00 20 10 18 24 24 20 20 20   ........ ..$$   
  0010: 01 00 00 00 20 20 20 00 00 20 80 00 01 00 00 00   ....   .. ......
  0020: 0c 01 00 00 ff e9 02 00 1c 00 00 00 5f 01 02 02   ............_...
  0030: 01 00 00 00 00 00 04 00 01 00 00 00 00 00 00 00   ................
Seed 4 (id=50d782f284a13b79, size=411 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=5876s, mutation_op=ByteFlipMutator,BytesExpandMutator,DwordInterestingMutator,TokenInsert):
  0000: ce fa ed fe 7f 95 e8 e0 0a 00 18 24 24 20 20 20   ...........$$   
  0010: 01 00 00 00 20 1f 20 00 00 20 80 00 01 00 00 00   .... . .. ......
  0020: 0c 01 00 00 20 20 20 20 20 02 01 00 00 00 00 00   ....     .......
  0030: 20 20 20 20 12 00 04 20 00 00 00 00 00 00 00 00       ... ........
Seed 5 (id=27a03924d04dc9d3, size=468 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=5881s, mutation_op=ByteNegMutator,ByteDecMutator,BytesDeleteMutator,WordAddMutator,ByteNegMutator):
  0000: ce fa ed fe 7f 95 e8 ec 0a 00 18 24 24 20 20 20   ...........$$   
  0010: 01 00 00 00 20 1f 20 00 00 20 80 00 01 00 00 00   .... . .. ......
  0020: 0c 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0030: 20 20 20 20 00 00 04 20 03 02 00 00 00 00 00 00       ... ........

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=001b86721a62221a, size=59 bytes, fuzzer=value_profile, trial=1, discovered_at=106s, mutation_op=DwordAddMutator,ByteRandMutator,BitFlipMutator):
  0000: 00 61 73 6d 00 e8 e9 2d 00 25 20 00 fe ff ff ff   .asm...-.% .....
  0010: 7f 00 00 00 c1 c1 dd 88 88 88 88 cf 00 00 01 00   ................
  0020: 0c 20 73 ff 01 00 20 b5 b5 20 10 20 00 04 06 88   . s... .. . ....
  0030: 88 00 00 01 06 06 00 00 ff 00 02                  ...........
Seed 2 (id=00165229b536b473, size=54 bytes, fuzzer=value_profile, trial=1, discovered_at=209s, mutation_op=ByteFlipMutator,ByteAddMutator):
  0000: 00 61 73 6d 00 20 20 ff 02 24 1f 00 00 00 00 00   .asm.  ..$......
  0010: 00 02 24 7f 00 00 00 01 02 00 ff 02 02 02 02 02   ..$.............
  0020: 02 02 02 02 1a fd 20 4a b5 25 b6 20 00 04 01 06   ...... J.%. ....
  0030: 06 00 00 ff 00 02                                 ......
Seed 3 (id=00050eebd8570fd9, size=55 bytes, fuzzer=naive, trial=1, discovered_at=274s, mutation_op=BytesDeleteMutator):
  0000: 00 61 73 6d fe 00 6d 00 01 01 01 01 01 01 01 01   .asm..m.........
  0010: 00 80 40 13 07 ff ff c0 c0 c0 a9 c0 c0 c0 13 07   ..@.............
  0020: ff ff c0 c0 e1 ff 01 01 00 07 01 01 01 01 01 01   ................
  0030: 01 01 01 01 00 01 00                              .......
Seed 4 (id=00080a63cb562b4e, size=46 bytes, fuzzer=value_profile, trial=1, discovered_at=348s, mutation_op=QwordAddMutator):
  0000: 00 61 73 6d 01 20 20 08 02 24 e0 e7 ff f0 00 02   .asm.  ..$......
  0010: cc 01 01 01 01 00 02 00 00 01 fb 01 00 00 00 01   ................
  0020: 01 00 02 00 00 34 cc cc cc cc ff ff ff 81         .....4........
Seed 5 (id=4353645200df5442, size=127 bytes, fuzzer=value_profile, trial=4, discovered_at=409s, mutation_op=BytesSetMutator,ByteInterestingMutator,ByteRandMutator):
  0000: 00 61 73 6d 01 01 01 01 01 01 01 02 72 38 00 10   .asm........r8..
  0010: 01 01 fb 00 01 00 ff 01 00 01 ed 00 fe 01 01 01   ................
  0020: 01 01 01 ff ff 00 00 00 00 00 00 00 94 00 01 01   ................
  0030: 01 01 00 00 02 01 01 ff ff ff ff ff ff 7f 7f de   ................


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  7f(.)x10 ce(.)x9 4d(M)x1            00(.)x68 7f(.)x2                    PARTIAL
   0x0001  45(E)x10 fa(.)x9 5a(Z)x1            61(a)x68 45(E)x2                    PARTIAL
   0x0002  4c(L)x10 ed(.)x9 50(P)x1            73(s)x68 4c(L)x2                    PARTIAL
   0x0003  46(F)x10 fe(.)x9 45(E)x1            6d(m)x68 46(F)x2                    PARTIAL
   0x0005  95(.)x9 01(.)x8 02(.)x2 00(.)x1     00(.)x15 01(.)x14 1b(.)x9 20( )x7 +19u  PARTIAL
   0x0006  e8(.)x9 03(.)x8 01(.)x2 ff(.)x1     6d(m)x13 01(.)x11 20( )x7 ff(.)x7 +18u  PARTIAL
   0x0007  0a(.)x8 00(.)x6 e0(.)x3 ec(.)x3     01(.)x22 00(.)x19 02(.)x5 ff(.)x4 +16u  PARTIAL
   0x0008  0a(.)x14 20( )x3 00(.)x3            01(.)x30 02(.)x27 00(.)x9 04(.)x1 +3u  PARTIAL
   0x0009  00(.)x17 10(.)x3                    01(.)x26 24($)x7 1b(.)x6 40(@)x5 +14u  PARTIAL
   0x000d  20( )x9 c9(.)x8 00(.)x2 01(.)x1     00(.)x15 01(.)x8 0f(.)x8 02(.)x7 +19u  PARTIAL
   0x000e  20( )x9 9a(.)x8 00(.)x3             01(.)x20 00(.)x18 03(.)x4 02(.)x4 +17u  PARTIAL
   0x000f  20( )x9 3b(;)x8 03(.)x2 00(.)x1     01(.)x24 00(.)x20 02(.)x5 80(.)x3 +14u  PARTIAL
   0x0010  01(.)x9 03(.)x8 00(.)x3             00(.)x27 01(.)x15 02(.)x7 80(.)x4 +13u  PARTIAL
   0x0011  00(.)x20                            01(.)x21 00(.)x11 02(.)x6 80(.)x6 +16u  PARTIAL
   0x0012  00(.)x20                            01(.)x18 00(.)x17 02(.)x5 03(.)x5 +16u  PARTIAL
   0x0013  00(.)x18 08(.)x2                    00(.)x20 01(.)x17 ff(.)x6 80(.)x4 +15u  PARTIAL
   0x0015  00(.)x11 1f(.)x5 20( )x4            00(.)x21 01(.)x16 80(.)x5 03(.)x5 +16u  PARTIAL
   0x0016  00(.)x11 20( )x9                    00(.)x21 01(.)x9 ff(.)x7 03(.)x5 +20u  PARTIAL
   0x0017  00(.)x18 08(.)x2                    01(.)x17 00(.)x12 02(.)x6 03(.)x4 +20u  PARTIAL
   0x001d  00(.)x18 6f(o)x2                    00(.)x18 01(.)x16 02(.)x6 ff(.)x4 +19u  PARTIAL
   0x001e  00(.)x18 2b(+)x2                    01(.)x17 00(.)x11 02(.)x8 10(.)x3 +25u  PARTIAL
   0x001f  00(.)x18 05(.)x2                    00(.)x16 01(.)x12 02(.)x6 80(.)x4 +22u  PARTIAL
   0x0020  0c(.)x17 00(.)x2 20( )x1            01(.)x16 00(.)x15 02(.)x7 ff(.)x6 +21u  PARTIAL
   0x0021  00(.)x10 01(.)x9 20( )x1            00(.)x16 01(.)x8 02(.)x7 ff(.)x5 +26u  PARTIAL
   0x0022  00(.)x19 42(B)x1                    00(.)x13 01(.)x10 02(.)x9 ff(.)x6 +23u  PARTIAL
   0x0023  00(.)x19 20( )x1                    00(.)x15 01(.)x14 ff(.)x7 02(.)x3 +26u  PARTIAL
   0x0029  00(.)x17 02(.)x1 52(R)x1 20( )x1    00(.)x21 01(.)x12 02(.)x5 a8(.)x3 +20u  PARTIAL
   0x002a  00(.)x18 01(.)x1 46(F)x1            01(.)x13 00(.)x12 ff(.)x6 02(.)x6 +22u  PARTIAL
   0x002b  00(.)x13 fd(.)x6 20( )x1            00(.)x13 01(.)x11 02(.)x6 ff(.)x4 +22u  PARTIAL
   0x002c  00(.)x16 5f(_)x3 fe(.)x1            00(.)x17 01(.)x13 02(.)x5 ff(.)x4 +19u  PARTIAL
   0x002d  00(.)x17 01(.)x3                    01(.)x16 00(.)x7 02(.)x5 04(.)x3 +19u  PARTIAL
   0x002e  00(.)x9 04(.)x8 02(.)x3             01(.)x15 02(.)x9 00(.)x7 06(.)x3 +12u  PARTIAL
   0x002f  00(.)x15 02(.)x3 08(.)x2            01(.)x15 00(.)x6 02(.)x5 06(.)x3 +14u  PARTIAL
   0x0031  00(.)x15 20( )x5                    01(.)x18 00(.)x11 02(.)x5 03(.)x2 +11u  PARTIAL
   0x0032  00(.)x15 20( )x4 2f(/)x1            01(.)x14 00(.)x13 02(.)x3 64(d)x2 +16u  PARTIAL
   0x0033  00(.)x13 20( )x4 5d(])x2 03(.)x1    01(.)x12 00(.)x11 02(.)x6 ff(.)x4 +13u  PARTIAL
   0x0034  00(.)x10 20( )x8 12(.)x1 0b(.)x1    00(.)x10 01(.)x10 02(.)x7 ff(.)x4 +12u  PARTIAL
   0x0036  04(.)x8 20( )x8 00(.)x3 e4(.)x1     00(.)x11 01(.)x10 80(.)x3 02(.)x2 +14u  PARTIAL
   0x0037  20( )x12 00(.)x6 01(.)x1 74(t)x1    01(.)x14 00(.)x8 02(.)x4 ff(.)x3 +10u  PARTIAL
   0x0039  00(.)x17 02(.)x2 7f(.)x1            01(.)x12 00(.)x8 02(.)x4 ff(.)x3 +11u  PARTIAL
   ... (4 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/bloaty_141.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 141,
  "target": "bloaty",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S), cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 141 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 141 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 141 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).