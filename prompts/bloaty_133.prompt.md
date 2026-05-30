==== BLOCKER ====
Target: bloaty
Branch ID: 133
Location: /src/bloaty/src/macho.cc:618:28
Enclosing function: bloaty::TryOpenMachOFile(std::unique_ptr<bloaty::InputFile, std::default_delete<bloaty::InputFile> >&)
Source line:   if (magic == MH_MAGIC || magic == MH_MAGIC_64 || magic == FAT_CIGAM) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    6        4          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=1.10h  loser=24.00h
  avg hitcount on branch: winner=6719  loser=0
  prob_div=1.00  dur_div=22.90h  hit_div=6719
  subject-level: delta_AUC=26255160.0  p_AUC=0.0002  delta_Final=523.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/bloaty/133/{W,L}/branch_coverage_show.txt

--- Enclosing function: bloaty::TryOpenMachOFile(std::unique_ptr<bloaty::InputFile, std::default_delete<bloaty::InputFile> >&) (/src/bloaty/src/macho.cc:612-624) ---
[ ]   610  }  // namespace macho
[ ]   611  
[B]   612  std::unique_ptr<ObjectFile> TryOpenMachOFile(std::unique_ptr<InputFile> &file) {
[B]   613    uint32_t magic = macho::ReadMagic(file->data());
[ ]   614  
[ ]   615    // We only support little-endian host and little endian binaries (see
[ ]   616    // ParseMachOHeader() for more rationale).  Fat headers are always on disk as
[ ]   617    // big-endian.
[B]   618    if (magic == MH_MAGIC || magic == MH_MAGIC_64 || magic == FAT_CIGAM) { <-- BLOCKER
[W]   619      return std::unique_ptr<ObjectFile>(
[W]   620          new macho::MachOObjectFile(std::move(file)));
[W]   621    }
[ ]   622  
[L]   623    return nullptr;
[B]   624  }

--- Caller (1 hop): bloaty::Bloaty::GetObjectFile(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) const (/src/bloaty/src/bloaty.cc:1544-1565, calls bloaty::TryOpenMachOFile(std::unique_ptr<bloaty::InputFile, std::default_delete<bloaty::InputFile> >&) at line 1549) (full body — short) ---
[B]  1544      const std::string& filename) const {
[B]  1545    std::unique_ptr<InputFile> file(file_factory_.OpenFile(filename));
[B]  1546    auto object_file = TryOpenELFFile(file);
[ ]  1547  
[B]  1548    if (!object_file.get()) {
[B]  1549      object_file = TryOpenMachOFile(file); <-- CALL
[B]  1550    }
[ ]  1551  
[B]  1552    if (!object_file.get()) {
[L]  1553      object_file = TryOpenWebAssemblyFile(file);
[L]  1554    }
[ ]  1555  
[B]  1556    if (!object_file.get()) {
[ ]  1557      object_file = TryOpenPEFile(file);
[ ]  1558    }
[ ]  1559  
[B]  1560    if (!object_file.get()) {
[ ]  1561      THROWF("unknown file type for file '$0'", filename.c_str());
[ ]  1562    }
[ ]  1563  
[B]  1564    return object_file;
[B]  1565  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  bloaty::Bloaty::GetObjectFile(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) const  (/src/bloaty/src/bloaty.cc:1544-1565, calls bloaty::TryOpenMachOFile(std::unique_ptr<bloaty::InputFile, std::default_delete<bloaty::InputFile> >&) at line 1549)
hop 3  bloaty::Bloaty::AddDebugFilename(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/bloaty.cc:1578-1586, calls bloaty::Bloaty::GetObjectFile(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) const at line 1579)
hop 3  bloaty::Bloaty::AddFilename(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bool)  (/src/bloaty/src/bloaty.cc:1567-1576, calls bloaty::Bloaty::GetObjectFile(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) const at line 1568)
hop 4  bloaty::BloatyDoMain(bloaty::Options const&, bloaty::InputFileFactory const&, bloaty::RollupOutput*)  (/src/bloaty/src/bloaty.cc:2233-2278, calls bloaty::Bloaty::AddFilename(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bool) at line 2245)
hop 5  bloaty::BloatyMain(bloaty::Options const&, bloaty::InputFileFactory const&, bloaty::RollupOutput*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >*)  (/src/bloaty/src/bloaty.cc:2281-2289, calls bloaty::BloatyDoMain(bloaty::Options const&, bloaty::InputFileFactory const&, bloaty::RollupOutput*) at line 2283)
hop 6  bloaty::RunBloaty(bloaty::InputFileFactory const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/tests/fuzz_target.cc:51-58, calls bloaty::BloatyMain(bloaty::Options const&, bloaty::InputFileFactory const&, bloaty::RollupOutput*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >*) at line 57)
hop 7  LLVMFuzzerTestOneInput  (/src/bloaty/tests/fuzz_target.cc:62-75, calls bloaty::RunBloaty(bloaty::InputFileFactory const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) at line 67)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     201       911  bloaty::NameMunger::Munge[abi:cxx11](std::basic_string_view<char, std::char_traits<char> >) const  (/src/bloaty/src/bloaty.cc:210-221)
     201       911  bloaty::RangeSink::ContainsVerboseFileOffset(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1096-1100)
     201       911  bloaty::RangeSink::IsVerboseForFileRange(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1133-1162)
     201       911  bloaty::RangeSink::AddFileRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1169-1190)
     526         0  dyld_info_command const* bloaty::macho::GetStructPointer<dyld_info_command>(std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/macho.cc:52-57)
     526         0  symtab_command const* bloaty::macho::GetStructPointer<symtab_command>(std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/macho.cc:52-57)
     526         0  dysymtab_command const* bloaty::macho::GetStructPointer<dysymtab_command>(std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/macho.cc:52-57)
     526         0  linkedit_data_command const* bloaty::macho::GetStructPointer<linkedit_data_command>(std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/macho.cc:52-57)
     526         0  mach_header const* bloaty::macho::GetStructPointer<mach_header>(std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/macho.cc:52-57)
     526         0  load_command const* bloaty::macho::GetStructPointer<load_command>(std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/macho.cc:52-57)
     526         0  uuid_command const* bloaty::macho::GetStructPointer<uuid_command>(std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/macho.cc:52-57)
     526         0  mach_header_64 const* bloaty::macho::GetStructPointer<mach_header_64>(std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/macho.cc:52-57)
     526         0  fat_header const* bloaty::macho::GetStructPointer<fat_header>(std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/macho.cc:52-57)
     526         0  fat_arch const* bloaty::macho::GetStructPointer<fat_arch>(std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/macho.cc:52-57)
     526         0  segment_command_64 const* bloaty::macho::GetStructPointer<segment_command_64>(std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/macho.cc:52-57)
... (60 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=4  bloaty::BloatyDoMain(bloaty::Options const&, bloaty::InputFileFactory const&, bloaty::RollupOutput*)  (/src/bloaty/src/bloaty.cc:2233-2278) ---
  d=4   L2273  T=36 F=24  T=60 F=0  if (options.data_source_size() > 0) {
  d=4   L2275  T=0 F=24  T=0 F=0  } else if (options.has_disassemble_function()) {
--- d=2  bloaty::Bloaty::GetObjectFile(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) const  (/src/bloaty/src/bloaty.cc:1544-1565) ---
  d=2   L1552  T=0 F=96  T=120 F=0  if (!object_file.get()) {
--- d=1  bloaty::TryOpenMachOFile(std::unique_ptr<bloaty::InputFile, std::default_delete<bloaty::InputFile> >&)  (/src/bloaty/src/macho.cc:612-624) ---
  d=1   L 618  T=96 F=0  T=0 F=120  if (magic == MH_MAGIC || magic == MH_MAGIC_64 || magic ==...  <-- BLOCKER
  d=1   L 618  T=0 F=0  T=0 F=120  if (magic == MH_MAGIC || magic == MH_MAGIC_64 || magic ==...  <-- BLOCKER

[off-chain: 99 additional divergent branches across 22 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=492ed499061ee540, size=59 bytes, fuzzer=cmplog, trial=1, discovered_at=36s, mutation_op=ByteInterestingMutator,BytesExpandMutator,WordInterestingMutator,BytesDeleteMutator,BytesDeleteMutator,ByteRandMutator,ByteRandMutator):
  0000: cf fa ed fe 00 20 20 20 20 20 00 00 00 00 00 00   .....     ......
  0010: 00 00 00 00 74 74 74 74 74 74 74 74 74 74 74 74   ....tttttttttttt
  0020: 74 74 74 00 00 00 00 00 00 00 00 20 20 20 20 20   ttt........     
  0030: 00 00 00 20 20 20 20 00 00 20 20                  ...    ..  
Seed 2 (id=ac3fa571f1153219, size=123 bytes, fuzzer=cmplog, trial=1, discovered_at=3886s, mutation_op=ByteInterestingMutator,ByteRandMutator):
  0000: cf fa ed fe 48 13 3c 5f 02 00 00 00 02 01 01 20   ....H.<_....... 
  0010: 02 00 00 00 48 13 5f 5f 02 00 00 00 30 30 01 13   ....H.__....00..
  0020: 1d 00 10 00 2b 00 00 00 2b 00 00 00 ff f9 01 00   ....+...+.......
  0030: 00 ce fa 61 72 63 68 2d 2d 63 73 76 69 2e 49 73   ...arch--csvi.Is
Seed 3 (id=2a3d619b60c7dca8, size=123 bytes, fuzzer=cmplog, trial=1, discovered_at=3896s, mutation_op=CrossoverReplaceMutator,BitFlipMutator,CrossoverInsertMutator,ByteDecMutator):
  0000: cf fa ed fe 48 13 3c 5f 02 00 00 00 02 01 01 10   ....H.<_........
  0010: 02 00 00 00 48 13 5f 5f 02 00 00 00 30 30 01 13   ....H.__....00..
  0020: 5f 5f 01 00 2b 00 00 00 2b 00 00 00 ff f9 01 00   __..+...+.......
  0030: 00 ce fa 63 6f 63 68 2d 2d 63 73 76 69 2e 49 73   ...coch--csvi.Is
Seed 4 (id=c9afa8b2add562c1, size=119 bytes, fuzzer=cmplog, trial=1, discovered_at=6628s, mutation_op=CrossoverInsertMutator,ByteNegMutator,BytesInsertMutator,BytesDeleteMutator,QwordAddMutator,BytesDeleteMutator):
  0000: cf fa ed fe 48 13 5f 5f 02 00 00 00 02 01 01 20   ....H.__....... 
  0010: 20 20 01 b0 48 13 5f 5f 03 00 00 00 30 30 01 13     ..H.__....00..
  0020: 1b 00 00 00 18 00 00 00 2b 00 00 00 ff f9 01 01   ........+.......
  0030: 00 ce fa 72 61 24 68 3e 0a 01 72 73 01 00 00 00   ...ra$h>..rs....
Seed 5 (id=3ae92f8da472b228, size=123 bytes, fuzzer=cmplog, trial=1, discovered_at=6701s, mutation_op=QwordAddMutator):
  0000: cf fa ed fe 48 13 5f 5f 02 00 00 00 02 01 01 20   ....H.__....... 
  0010: 20 20 01 b0 48 13 00 20 20 03 07 00 00 30 01 13     ..H..  ....0..
  0020: 1b 00 00 00 18 00 00 00 00 00 64 00 ff 00 64 00   ..........d...d.
  0030: ff f9 01 00 00 ce fa 73 68 24 68 3e 1b 00 00 00   .......sh$h>....

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
   0x0000  cf(.)x10                            00(.)x10                            DIFFER
   0x0001  fa(.)x10                            61(a)x10                            DIFFER
   0x0002  ed(.)x10                            73(s)x10                            DIFFER
   0x0003  fe(.)x10                            6d(m)x10                            DIFFER
   0x0004  48(H)x8 00(.)x1 02(.)x1             fe(.)x8 be(.)x2                     DIFFER
   0x0005  13(.)x8 20( )x1 01(.)x1             00(.)x8 04(.)x1 40(@)x1             DIFFER
   0x0006  5f(_)x6 3c(<)x2 20( )x1 01(.)x1     6d(m)x7 d5(.)x1 00(.)x1 20( )x1     PARTIAL
   0x0007  5f(_)x8 20( )x2                     01(.)x8 00(.)x1 02(.)x1             DIFFER
   0x0008  02(.)x8 20( )x1 df(.)x1             01(.)x10                            DIFFER
   0x0009  00(.)x8 20( )x2                     01(.)x8 80(.)x2                     DIFFER
   0x000a  00(.)x9 01(.)x1                     ff(.)x7 00(.)x2 01(.)x1             PARTIAL
   0x000b  00(.)x9 b0(.)x1                     02(.)x7 01(.)x1 0a(.)x1 03(.)x1     DIFFER
   0x000c  02(.)x8 00(.)x1 48(H)x1             20( )x7 01(.)x1 38(8)x1 21(!)x1     DIFFER
   0x000d  01(.)x8 00(.)x1 13(.)x1             0f(.)x4 01(.)x1 19(.)x1 e8(.)x1 +3u  PARTIAL
   0x000e  01(.)x8 00(.)x1 5f(_)x1             01(.)x8 03(.)x1 ff(.)x1             PARTIAL
   0x000f  20( )x7 00(.)x1 10(.)x1 5f(_)x1     01(.)x8 00(.)x1 ff(.)x1             PARTIAL
   0x0010  20( )x4 01(.)x3 02(.)x2 00(.)x1     00(.)x8 02(.)x1 01(.)x1             PARTIAL
   0x0011  00(.)x6 20( )x4                     01(.)x7 80(.)x1 05(.)x1 02(.)x1     DIFFER
   0x0012  00(.)x6 01(.)x4                     01(.)x6 02(.)x2 40(@)x1 03(.)x1     PARTIAL
   0x0013  00(.)x6 b0(.)x4                     01(.)x3 ff(.)x2 0b(.)x2 13(.)x1 +2u  PARTIAL
   0x0014  48(H)x8 74(t)x1 30(0)x1             00(.)x2 01(.)x2 07(.)x1 7f(.)x1 +4u  DIFFER
   0x0015  13(.)x8 74(t)x1 30(0)x1             ff(.)x3 00(.)x3 01(.)x1 0b(.)x1 +2u  DIFFER
   0x0016  5f(_)x4 00(.)x4 74(t)x1 01(.)x1     00(.)x5 ff(.)x4 01(.)x1             PARTIAL
   0x0017  5f(_)x4 20( )x4 74(t)x1 13(.)x1     01(.)x2 ff(.)x2 00(.)x2 c0(.)x1 +3u  DIFFER
   0x0019  00(.)x4 03(.)x4 74(t)x1 5f(_)x1     01(.)x2 00(.)x2 08(.)x2 80(.)x2 +2u  PARTIAL
   0x001a  00(.)x4 07(.)x4 74(t)x1 01(.)x1     00(.)x5 01(.)x3 a9(.)x1 f1(.)x1     PARTIAL
   0x001b  00(.)x9 74(t)x1                     00(.)x3 01(.)x3 c0(.)x1 f1(.)x1 +2u  PARTIAL
   0x001c  30(0)x4 00(.)x4 74(t)x1 29())x1     01(.)x4 00(.)x2 c0(.)x1 02(.)x1 +2u  PARTIAL
   0x001d  30(0)x8 74(t)x1 00(.)x1             01(.)x3 00(.)x3 c0(.)x1 f1(.)x1 +2u  PARTIAL
   0x001e  01(.)x8 74(t)x1 00(.)x1             01(.)x3 13(.)x1 00(.)x1 f1(.)x1 +4u  PARTIAL
   0x001f  13(.)x8 74(t)x1 00(.)x1             80(.)x2 01(.)x2 07(.)x1 f1(.)x1 +4u  PARTIAL
   0x0021  00(.)x8 74(t)x1 5f(_)x1             ff(.)x2 01(.)x2 00(.)x2 fe(.)x1 +3u  PARTIAL
   0x0022  00(.)x7 74(t)x1 10(.)x1 01(.)x1     ff(.)x3 01(.)x2 00(.)x2 c0(.)x1 +2u  PARTIAL
   0x0023  00(.)x10                            00(.)x4 01(.)x2 c0(.)x1 ff(.)x1 +2u  PARTIAL
   0x0024  18(.)x6 2b(+)x2 00(.)x1 20( )x1     01(.)x5 ff(.)x2 e1(.)x1 05(.)x1 +1u  PARTIAL
   0x0025  00(.)x10                            ff(.)x4 01(.)x3 00(.)x2 08(.)x1     PARTIAL
   0x0026  00(.)x10                            01(.)x3 ff(.)x1 66(f)x1 00(.)x1 +4u  PARTIAL
   0x0027  00(.)x10                            01(.)x6 00(.)x2 ff(.)x1 8a(.)x1     PARTIAL
   0x0028  00(.)x5 2b(+)x4 53(S)x1             00(.)x4 01(.)x2 3f(?)x1 20( )x1 +2u  PARTIAL
   0x0029  00(.)x10                            00(.)x6 01(.)x2 07(.)x1 a8(.)x1     PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/bloaty_133.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 133,
  "target": "bloaty",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 133 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 133 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 133 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).