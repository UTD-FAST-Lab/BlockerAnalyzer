==== BLOCKER ====
Target: bloaty
Branch ID: 147
Location: /src/bloaty/src/webassembly.cc:77:7
Enclosing function: bloaty::wasm::ReadMagic(std::basic_string_view<char, std::char_traits<char> >*)
Source line:   if (magic != wasm_magic) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (value_profile vs value_profile)
cmplog                           7        3          0  REFERENCE
value_profile                    8        2          0  winner (value_profile vs naive)
value_profile_cmplog             7        3          0  REFERENCE
naive_ctx                        3        7          0  REFERENCE
naive_ngram4                     6        4          0  REFERENCE
mopt                             3        7          0  REFERENCE
minimizer                        7        3          0  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                         0       10          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile > naive  [delta: value_profile] ---
  subject 2  (value_profile vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=10.20h  loser=21.10h
  avg hitcount on branch: winner=17  loser=2
  prob_div=0.60  dur_div=10.90h  hit_div=16
  subject-level: delta_AUC=4000860.0  p_AUC=0.014  delta_Final=74.3  p_final=0.014

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/bloaty/147/{W,L}/branch_coverage_show.txt

--- Enclosing function: bloaty::wasm::ReadMagic(std::basic_string_view<char, std::char_traits<char> >*) (/src/bloaty/src/webassembly.cc:73-86) ---
[L]    71  }
[ ]    72  
[B]    73  bool ReadMagic(string_view* data) {
[B]    74    const uint32_t wasm_magic = 0x6d736100;
[B]    75    auto magic = ReadFixed<uint32_t>(data);
[ ]    76  
[B]    77    if (magic != wasm_magic) { <-- BLOCKER
[W]    78      return false;
[W]    79    }
[ ]    80  
[ ]    81    // TODO(haberman): do we need to fail if this is >1?
[L]    82    auto version = ReadFixed<uint32_t>(data);
[L]    83    (void)version;
[ ]    84  
[L]    85    return true;
[B]    86  }

--- Caller (1 hop): bloaty::macho::ReadMagic(std::basic_string_view<char, std::char_traits<char> >) (/src/bloaty/src/macho.cc:42-49, calls bloaty::wasm::ReadMagic(std::basic_string_view<char, std::char_traits<char> >*) at line 42) (full body — short) ---
[B]    42  uint32_t ReadMagic(string_view data) { <-- CALL
[B]    43    if (data.size() < sizeof(uint32_t)) {
[ ]    44      THROW("Malformed Mach-O file");
[ ]    45    }
[B]    46    uint32_t magic;
[B]    47    memcpy(&magic, data.data(), sizeof(magic));
[B]    48    return magic;
[B]    49  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  bloaty::macho::ReadMagic(std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/macho.cc:42-49, calls bloaty::wasm::ReadMagic(std::basic_string_view<char, std::char_traits<char> >*) at line 42)
hop 2  void bloaty::macho::ParseMachOHeader<bloaty::macho::MachOObjectFile::GetBuildId[abi:cxx11]() const::{lambda(bloaty::macho::LoadCommand)#1}>(std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*, bloaty::macho::MachOObjectFile::GetBuildId[abi:cxx11]() const::{lambda(bloaty::macho::LoadCommand)#1}&&)  (/src/bloaty/src/macho.cc:119-155, calls bloaty::wasm::ReadMagic(std::basic_string_view<char, std::char_traits<char> >*) at line 120)
hop 3  void bloaty::macho::ForEachLoadCommand<bloaty::macho::MachOObjectFile::GetBuildId[abi:cxx11]() const::{lambda(bloaty::macho::LoadCommand)#1}>(std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*, bloaty::macho::MachOObjectFile::GetBuildId[abi:cxx11]() const::{lambda(bloaty::macho::LoadCommand)#1}&&)  (/src/bloaty/src/macho.cc:177-192, calls bloaty::macho::ReadMagic(std::basic_string_view<char, std::char_traits<char> >) at line 178)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0      2070  bloaty::wasm::ReadLEB128Internal(bool, unsigned long, std::basic_string_view<char, std::char_traits<char> >*)  (/src/bloaty/src/webassembly.cc:25-46)
       0      1990  bloaty::wasm::ReadPiece(unsigned long, std::basic_string_view<char, std::char_traits<char> >*)  (/src/bloaty/src/webassembly.cc:64-71)
       0      1150  bloaty::wasm::ReadVarUInt32(std::basic_string_view<char, std::char_traits<char> >*)  (/src/bloaty/src/webassembly.cc:56-58)
       0       898  bloaty::wasm::ReadVarUInt7(std::basic_string_view<char, std::char_traits<char> >*)  (/src/bloaty/src/webassembly.cc:52-54)
       0       898  bloaty::wasm::Section::Read(std::basic_string_view<char, std::char_traits<char> >*)  (/src/bloaty/src/webassembly.cc:95-117)
       0       414  webassembly.cc:bloaty::wasm::AddWebAssemblyFallback(bloaty::RangeSink*)::$_0::operator()(bloaty::wasm::Section const&) const  (/src/bloaty/src/webassembly.cc:374-378)
       0       400  webassembly.cc:bloaty::wasm::ParseSections(bloaty::RangeSink*)::$_0::operator()(bloaty::wasm::Section const&) const  (/src/bloaty/src/webassembly.cc:176-178)
      60       302  bloaty::wasm::ReadMagic(std::basic_string_view<char, std::char_traits<char> >*)  (/src/bloaty/src/webassembly.cc:73-86)  <-- enclosing
       0       182  webassembly.cc:void bloaty::wasm::ForEachSection<bloaty::wasm::ParseSections(bloaty::RangeSink*)::$_0>(std::basic_string_view<char, std::char_traits<char> >, bloaty::wasm::ParseSections(bloaty::RangeSink*)::$_0&&)  (/src/bloaty/src/webassembly.cc:165-173)
       0       182  webassembly.cc:void bloaty::wasm::ForEachSection<bloaty::wasm::ParseSymbols(bloaty::RangeSink*)::$_0>(std::basic_string_view<char, std::char_traits<char> >, bloaty::wasm::ParseSymbols(bloaty::RangeSink*)::$_0&&)  (/src/bloaty/src/webassembly.cc:165-173)
       0       182  webassembly.cc:void bloaty::wasm::ForEachSection<bloaty::wasm::ParseSymbols(bloaty::RangeSink*)::$_1>(std::basic_string_view<char, std::char_traits<char> >, bloaty::wasm::ParseSymbols(bloaty::RangeSink*)::$_1&&)  (/src/bloaty/src/webassembly.cc:165-173)
       0       182  webassembly.cc:void bloaty::wasm::ForEachSection<bloaty::wasm::AddWebAssemblyFallback(bloaty::RangeSink*)::$_0>(std::basic_string_view<char, std::char_traits<char> >, bloaty::wasm::AddWebAssemblyFallback(bloaty::RangeSink*)::$_0&&)  (/src/bloaty/src/webassembly.cc:165-173)
       0       120  bloaty::wasm::WebAssemblyObjectFile::WebAssemblyObjectFile(std::unique_ptr<bloaty::InputFile, std::default_delete<bloaty::InputFile> >)  (/src/bloaty/src/webassembly.cc:386-386)
       0       120  bloaty::wasm::WebAssemblyObjectFile::GetBuildId[abi:cxx11]() const  (/src/bloaty/src/webassembly.cc:388-391)
       0        82  bloaty::wasm::AddWebAssemblyFallback(bloaty::RangeSink*)  (/src/bloaty/src/webassembly.cc:373-381)
... (17 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  bloaty::macho::ReadMagic(std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/macho.cc:42-49) ---
  d=2   L  43  T=0 F=60  T=0 F=120  if (data.size() < sizeof(uint32_t)) {
--- d=1  bloaty::wasm::ReadMagic(std::basic_string_view<char, std::char_traits<char> >*)  (/src/bloaty/src/webassembly.cc:73-86) ---
  d=1   L  77  T=60 F=0  T=0 F=302  if (magic != wasm_magic) {  <-- BLOCKER

[off-chain: 39 additional divergent branches across 14 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=0898eeac49002255, size=36 bytes, fuzzer=value_profile, trial=1, discovered_at=0s, mutation_op=ByteFlipMutator,BytesDeleteMutator,BytesDeleteMutator,ByteInterestingMutator,WordAddMutator):
  0000: 01 01 00 00 06 00 00 00 00 00 00 00 00 00 00 00   ................
  0010: 00 00 00 00 20 20 20 20 20 00 00 40 18 20 20 20   ....     ..@.   
  0020: 00 00 20 20                                       ..  
Seed 2 (id=6d85f36146aa65e0, size=78 bytes, fuzzer=value_profile, trial=1, discovered_at=0s, mutation_op=ByteIncMutator,BytesSetMutator,WordInterestingMutator,CrossoverReplaceMutator,WordAddMutator,BytesSetMutator):
  0000: 7f 7f 7f ff ff ff ff 00 04 ff ff ff 00 00 00 00   ................
  0010: 00 00 00 00 00 00 00 00 00 20 20 20 20 00 00 00   .........    ...
  0020: 00 00 00 00 00 00 00 00 00 00 00 20 20 20 20 00   ...........    .
  0030: 00 00 00 00 01 00 00 00 00 00 00 00 00 00 20 20   ..............  
Seed 3 (id=910e13b56385fb5c, size=75 bytes, fuzzer=value_profile, trial=1, discovered_at=0s, mutation_op=TokenInsert,ByteRandMutator,BytesInsertCopyMutator,DwordAddMutator,BytesRandSetMutator,QwordAddMutator,DwordAddMutator):
  0000: 4c 46 02 04 01 00 00 00 20 20 20 20 20 00 20 20   LF......     .  
  0010: fe ff dd 00 00 00 00 20 20 20 45 7f 20 e6 20 ff   .......   E. . .
  0020: ff ff ff 06 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0030: 00 00 20 20 20 20 00 20 20 20 28 20 00 00 cb cc   ..    .   ( ....
Seed 4 (id=9c1e72a398133265, size=78 bytes, fuzzer=value_profile, trial=1, discovered_at=0s, mutation_op=ByteRandMutator,BitFlipMutator,CrossoverReplaceMutator,BytesInsertMutator):
  0000: 7f 45 4c 4c 46 02 01 01 00 00 00 00 00 00 00 00   .ELLF...........
  0010: 00 00 00 00 00 00 00 00 00 20 20 20 20 00 00 00   .........    ...
  0020: 00 00 00 00 20 20 20 20 20 20 ff ff ff ff 04 00   ....      ......
  0030: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 20 20   ..............  
Seed 5 (id=f1abc1ad5ae20705, size=53 bytes, fuzzer=value_profile, trial=1, discovered_at=0s, mutation_op=BytesDeleteMutator,WordAddMutator,BytesSwapMutator,ByteAddMutator,ByteNegMutator,BytesCopyMutator):
  0000: 00 00 00 00 00 00 00 20 20 20 20 00 00 00 20 20   .......    ...  
  0010: 20 20 20 20 ff ff ff ff 06 00 00 00 00 20 20 20       .........   
  0020: 20 20 20 ff ff ff ff 06 00 00 00 00 00 00 00 20      ............ 
  0030: 20 00 00 20 20                                     ..  

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00050eebd8570fd9, size=55 bytes, fuzzer=naive, trial=1, discovered_at=274s, mutation_op=BytesDeleteMutator):
  0000: 00 61 73 6d fe 00 6d 00 01 01 01 01 01 01 01 01   .asm..m.........
  0010: 00 80 40 13 07 ff ff c0 c0 c0 a9 c0 c0 c0 13 07   ..@.............
  0020: ff ff c0 c0 e1 ff 01 01 00 07 01 01 01 01 01 01   ................
  0030: 01 01 01 01 00 01 00                              .......
Seed 2 (id=0048a2ae493af0f5, size=71 bytes, fuzzer=naive, trial=1, discovered_at=498s, mutation_op=DwordInterestingMutator,BytesExpandMutator,ByteIncMutator,DwordInterestingMutator):
  0000: 00 61 73 6d fe 00 6d 01 01 01 ff 02 20 19 01 01   .asm..m..... ...
  0010: 00 01 02 01 00 01 00 01 01 01 01 00 02 01 00 80   ................
  0020: ff ff f8 00 01 08 01 01 00 00 00 00 01 01 00 02   ................
  0030: 01 00 05 00 00 02 00 00 00 01 00 01 07 ff ff 01   ................
Seed 3 (id=004787abb6df541c, size=45 bytes, fuzzer=naive, trial=1, discovered_at=503s, mutation_op=QwordAddMutator,TokenReplace,CrossoverReplaceMutator,ByteDecMutator,DwordInterestingMutator):
  0000: 00 61 73 6d fe 00 6d 01 01 01 ff 02 20 e8 03 00   .asm..m..... ...
  0010: 00 01 01 01 7f ff ff ff 01 01 01 01 01 01 01 01   ................
  0020: 01 fe ff ff ff ff ff ff 3f 00 00 00 00            ........?....
Seed 4 (id=0038691782d6e2c5, size=54 bytes, fuzzer=naive, trial=1, discovered_at=660s, mutation_op=ByteIncMutator,WordInterestingMutator,ByteRandMutator):
  0000: 00 61 73 6d fe 04 6d 01 01 01 ff 02 20 d5 ff 01   .asm..m..... ...
  0010: 00 05 01 00 40 00 00 01 fe f1 f1 f1 f1 f1 f1 f1   ....@...........
  0020: 00 7f ff 01 01 01 01 01 20 00 01 01 01 01 01 d8   ........ .......
  0030: 01 01 01 01 01 02                                 ......
Seed 5 (id=000ab8cc8de317fd, size=45 bytes, fuzzer=naive, trial=1, discovered_at=1783s, mutation_op=BytesSwapMutator):
  0000: 00 61 73 6d fe 00 6d 01 01 01 ff 02 20 0f 01 ff   .asm..m..... ...
  0010: 00 01 01 ff ff 0b 00 00 80 00 00 00 00 00 10 f8   ................
  0020: f8 01 aa fe ff ff 66 01 01 01 fb 2d 69            ......f....-i


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  7f(.)x2 4c(L)x2 ce(.)x2 01(.)x1 +3u  00(.)x10                            PARTIAL
   0x0001  46(F)x2 fe(.)x2 01(.)x1 7f(.)x1 +4u  61(a)x10                            DIFFER
   0x0002  00(.)x2 02(.)x2 ff(.)x2 cd(.)x2 +2u  73(s)x10                            DIFFER
   0x0003  fe(.)x3 00(.)x2 ff(.)x2 04(.)x1 +2u  6d(m)x10                            DIFFER
   0x0004  ff(.)x4 01(.)x3 06(.)x1 46(F)x1 +1u  fe(.)x8 be(.)x2                     DIFFER
   0x0005  00(.)x4 ff(.)x4 02(.)x1 61(a)x1     00(.)x8 04(.)x1 40(@)x1             PARTIAL
   0x0006  00(.)x4 ff(.)x2 3f(?)x2 01(.)x1 +1u  6d(m)x7 d5(.)x1 00(.)x1 20( )x1     PARTIAL
   0x0007  00(.)x4 08(.)x2 01(.)x1 20( )x1 +2u  01(.)x8 00(.)x1 02(.)x1             PARTIAL
   0x0008  00(.)x3 20( )x3 24($)x2 04(.)x1 +1u  01(.)x10                            DIFFER
   0x0009  20( )x4 00(.)x3 0f(.)x2 ff(.)x1     01(.)x8 80(.)x2                     DIFFER
   0x000a  00(.)x5 20( )x4 ff(.)x1             ff(.)x7 00(.)x2 01(.)x1             PARTIAL
   0x000b  00(.)x5 ff(.)x3 20( )x2             02(.)x7 01(.)x1 0a(.)x1 03(.)x1     DIFFER
   0x000c  00(.)x5 20( )x2 01(.)x2 02(.)x1     20( )x7 01(.)x1 38(8)x1 21(!)x1     PARTIAL
   0x000d  00(.)x7 ff(.)x2 24($)x1             0f(.)x4 01(.)x1 19(.)x1 e8(.)x1 +3u  DIFFER
   0x000e  00(.)x4 20( )x3 e4(.)x2 c7(.)x1     01(.)x8 03(.)x1 ff(.)x1             DIFFER
   0x000f  20( )x5 00(.)x4 17(.)x1             01(.)x8 00(.)x1 ff(.)x1             PARTIAL
   0x0010  00(.)x5 20( )x2 fe(.)x1 ff(.)x1 +1u  00(.)x8 02(.)x1 01(.)x1             PARTIAL
   0x0011  00(.)x6 20( )x2 ff(.)x1 0b(.)x1     01(.)x7 80(.)x1 05(.)x1 02(.)x1     DIFFER
   0x0012  00(.)x7 dd(.)x1 20( )x1 80(.)x1     01(.)x6 02(.)x2 40(@)x1 03(.)x1     DIFFER
   0x0013  00(.)x9 20( )x1                     01(.)x3 ff(.)x2 0b(.)x2 13(.)x1 +2u  PARTIAL
   0x0015  00(.)x8 20( )x1 ff(.)x1             ff(.)x3 00(.)x3 01(.)x1 0b(.)x1 +2u  PARTIAL
   0x0016  00(.)x7 20( )x1 ff(.)x1 e3(.)x1     00(.)x5 ff(.)x4 01(.)x1             PARTIAL
   0x0017  20( )x5 00(.)x3 ff(.)x1 0a(.)x1     01(.)x2 ff(.)x2 00(.)x2 c0(.)x1 +3u  PARTIAL
   0x0019  20( )x6 00(.)x3 17(.)x1             01(.)x2 00(.)x2 08(.)x2 80(.)x2 +2u  PARTIAL
   0x001a  00(.)x5 20( )x2 45(E)x2 01(.)x1     00(.)x5 01(.)x3 a9(.)x1 f1(.)x1     PARTIAL
   0x001d  00(.)x5 20( )x3 e6(.)x1 c1(.)x1     01(.)x3 00(.)x3 c0(.)x1 f1(.)x1 +2u  PARTIAL
   0x001e  00(.)x5 20( )x4 01(.)x1             01(.)x3 13(.)x1 00(.)x1 f1(.)x1 +4u  PARTIAL
   0x0020  00(.)x6 ff(.)x2 20( )x1 f8(.)x1     01(.)x3 00(.)x3 ff(.)x2 f8(.)x1 +1u  PARTIAL
   0x0021  00(.)x5 ff(.)x2 02(.)x2 20( )x1     ff(.)x2 01(.)x2 00(.)x2 fe(.)x1 +3u  PARTIAL
   0x0022  00(.)x5 20( )x2 ff(.)x2 01(.)x1     ff(.)x3 01(.)x2 00(.)x2 c0(.)x1 +2u  PARTIAL
   0x0024  00(.)x6 20( )x1 ff(.)x1 01(.)x1     01(.)x5 ff(.)x2 e1(.)x1 05(.)x1 +1u  PARTIAL
   0x0025  00(.)x4 20( )x2 ff(.)x1 01(.)x1 +1u  ff(.)x4 01(.)x3 00(.)x2 08(.)x1     PARTIAL
   0x0026  00(.)x4 20( )x3 ff(.)x1 2d(-)x1     01(.)x3 ff(.)x1 66(f)x1 00(.)x1 +4u  PARTIAL
   0x0027  00(.)x5 20( )x2 06(.)x1 63(c)x1     01(.)x6 00(.)x2 ff(.)x1 8a(.)x1     PARTIAL
   0x0028  00(.)x5 20( )x2 23(#)x1 73(s)x1     00(.)x4 01(.)x2 3f(?)x1 20( )x1 +2u  PARTIAL
   0x0029  00(.)x5 20( )x2 06(.)x1 76(v)x1     00(.)x6 01(.)x2 07(.)x1 a8(.)x1     PARTIAL
   0x002a  00(.)x5 20( )x2 ff(.)x1 fa(.)x1     01(.)x5 00(.)x2 fb(.)x1 a8(.)x1 +1u  PARTIAL
   0x002b  00(.)x4 20( )x3 ff(.)x1 eb(.)x1     01(.)x3 00(.)x2 2d(-)x1 3e(>)x1 +3u  PARTIAL
   0x002c  00(.)x4 20( )x3 ff(.)x1 10(.)x1     01(.)x5 00(.)x3 69(i)x1 57(W)x1     PARTIAL
   0x002d  00(.)x4 20( )x2 ff(.)x1 01(.)x1 +1u  01(.)x5 80(.)x1 05(.)x1             PARTIAL
   ... (18 more divergent offsets)
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/bloaty_147.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 147,
  "target": "bloaty",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>naive (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 147 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 147 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 147 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).