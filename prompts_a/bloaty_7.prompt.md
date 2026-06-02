==== BLOCKER ====
Target: bloaty
Branch ID: 7
Location: /src/bloaty/src/bloaty.cc:1103:7
Enclosing function: bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long)
Source line:   if (vmsize == RangeMap::kUnknownSize) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           7        3          0  REFERENCE
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         4        6          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.80h  loser=23.60h
  avg hitcount on branch: winner=22887  loser=0
  prob_div=1.00  dur_div=19.80h  hit_div=22887
  subject-level: delta_AUC=49070700.0  p_AUC=0.0002  delta_Final=792.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/bloaty/7/{W,L}/branch_coverage_show.txt

--- Enclosing function: bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long) (/src/bloaty/src/bloaty.cc:1102-1131) ---
[B]  1100  }
[ ]  1101  
[B]  1102  bool RangeSink::IsVerboseForVMRange(uint64_t vmaddr, uint64_t vmsize) {
[B]  1103    if (vmsize == RangeMap::kUnknownSize) { <-- BLOCKER
[W]  1104      vmsize = UINT64_MAX - vmaddr;
[W]  1105    }
[ ]  1106  
[B]  1107    if (vmaddr + vmsize < vmaddr) {
[ ]  1108      THROWF("Overflow in vm range, vmaddr=$0, vmsize=$1", vmaddr, vmsize);
[ ]  1109    }
[ ]  1110  
[B]  1111    if (ContainsVerboseVMAddr(vmaddr, vmsize)) {
[ ]  1112      return true;
[ ]  1113    }
[ ]  1114  
[B]  1115    if (translator_ && options_.has_debug_fileoff()) {
[ ]  1116      RangeMap vm_map;
[ ]  1117      RangeMap file_map;
[ ]  1118      bool contains = false;
[ ]  1119      vm_map.AddRangeWithTranslation(vmaddr, vmsize, "", translator_->vm_map,
[ ]  1120                                     false, &file_map);
[ ]  1121      file_map.ForEachRange(
[ ]  1122          [this, &contains](uint64_t fileoff, uint64_t filesize) {
[ ]  1123            if (ContainsVerboseFileOffset(fileoff, filesize)) {
[ ]  1124              contains = true;
[ ]  1125            }
[ ]  1126          });
[ ]  1127      return contains;
[ ]  1128    }
[ ]  1129  
[B]  1130    return false;
[B]  1131  }

--- Caller (1 hop): bloaty::RangeSink::AddVMRange(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) (/src/bloaty/src/bloaty.cc:1278-1296, calls bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long) at line 1279) (full body — short) ---
[W]  1278                             uint64_t vmsize, const std::string& name) {
[W]  1279    bool verbose = IsVerboseForVMRange(vmaddr, vmsize); <-- CALL
[W]  1280    if (verbose) {
[ ]  1281      printf("[%s, %s] AddVMRange(%.*s, %" PRIx64 ", %" PRIx64 ")\n",
[ ]  1282             GetDataSourceLabel(data_source_), analyzer, (int)name.size(),
[ ]  1283             name.data(), vmaddr, vmsize);
[ ]  1284    }
[W]  1285    assert(translator_);
[W]  1286    for (auto& pair : outputs_) {
[W]  1287      const std::string label = pair.second->Munge(name);
[W]  1288      bool ok = pair.first->vm_map.AddRangeWithTranslation(
[W]  1289          vmaddr, vmsize, label, translator_->vm_map, verbose,
[W]  1290          &pair.first->file_map);
[W]  1291      if (!ok) {
[W]  1292        WARN("VM range ($0, $1) for label $2 extends beyond base map", vmaddr,
[W]  1293             vmsize, name);
[W]  1294      }
[W]  1295    }
[W]  1296  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  bloaty::RangeSink::AddVMRange(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/bloaty.cc:1278-1296, calls bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long) at line 1279)
hop 2  bloaty::RangeSink::AddVMRangeForVMAddr(char const*, unsigned long, unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1252-1275, calls bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long) at line 1253)
hop 3  bloaty::RangeSink::AddVMRangeAllowAlias(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/bloaty.cc:1299-1303, calls bloaty::RangeSink::AddVMRange(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) at line 1302)
hop 3  bloaty::RangeSink::AddVMRangeIgnoreDuplicate(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/bloaty.cc:1307-1310, calls bloaty::RangeSink::AddVMRange(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) at line 1309)
hop 3  bloaty::DisassembleFindReferences(bloaty::DisassemblyInfo const&, bloaty::RangeSink*)  (/src/bloaty/src/disassemble.cc:43-94, calls bloaty::RangeSink::AddVMRangeForVMAddr(char const*, unsigned long, unsigned long, unsigned long) at line 84)
hop 4  bloaty::dwarf::ReadRangeList(bloaty::dwarf::CU const&, unsigned long, std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*, std::basic_string_view<char, std::char_traits<char> >*)  (/src/bloaty/src/dwarf.cc:177-194, calls bloaty::RangeSink::AddVMRangeIgnoreDuplicate(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) at line 190)
hop 4  dwarf.cc:bloaty::ReadDWARFAddressRanges(bloaty::dwarf::File const&, bloaty::RangeSink*)  (/src/bloaty/src/dwarf.cc:237-295, calls bloaty::RangeSink::AddVMRangeIgnoreDuplicate(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) at line 287)
hop 4  elf.cc:bloaty::(anonymous namespace)::ReadELFSymbols(bloaty::InputFile const&, bloaty::RangeSink*, std::map<std::basic_string_view<char, std::char_traits<char> >, std::pair<unsigned long, unsigned long>, std::less<std::basic_string_view<char, std::char_traits<char> > >, std::allocator<std::pair<std::basic_string_view<char, std::char_traits<char> > const, std::pair<unsigned long, unsigned long> > > >*, bool)::$_0::operator()(bloaty::(anonymous namespace)::ElfFile const&, std::basic_string_view<char, std::char_traits<char> >, unsigned long) const  (/src/bloaty/src/elf.cc:855-921, calls bloaty::DisassembleFindReferences(bloaty::DisassemblyInfo const&, bloaty::RangeSink*) at line 917)
hop 5  bloaty::AddDIE(bloaty::dwarf::CU const&, bloaty::GeneralDIE const&, bloaty::DualMap const&, bloaty::RangeSink*)  (/src/bloaty/src/dwarf.cc:406-540, calls bloaty::dwarf::ReadRangeList(bloaty::dwarf::CU const&, unsigned long, std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*, std::basic_string_view<char, std::char_traits<char> >*) at line 529)
hop 5  bloaty::ReadDWARFCompileUnits(bloaty::dwarf::File const&, bloaty::DualMap const&, bloaty::dwarf::CU const*, bloaty::RangeSink*)  (/src/bloaty/src/dwarf.cc:656-674, calls dwarf.cc:bloaty::ReadDWARFAddressRanges(bloaty::dwarf::File const&, bloaty::RangeSink*) at line 662)
hop 6  bloaty::ReadDWARFCompileUnits(bloaty::dwarf::File const&, bloaty::DualMap const&, bloaty::RangeSink*)  (/src/bloaty/src/bloaty.h:303-305, calls bloaty::ReadDWARFCompileUnits(bloaty::dwarf::File const&, bloaty::DualMap const&, bloaty::dwarf::CU const*, bloaty::RangeSink*) at line 304)
hop 6  dwarf.cc:bloaty::ReadDWARFDebugInfo(bloaty::dwarf::InfoReader&, bloaty::dwarf::InfoReader::Section, bloaty::DualMap const&, bloaty::RangeSink*)  (/src/bloaty/src/dwarf.cc:586-653, calls bloaty::AddDIE(bloaty::dwarf::CU const&, bloaty::GeneralDIE const&, bloaty::DualMap const&, bloaty::RangeSink*) at line 628)
hop 7  elf.cc:bloaty::(anonymous namespace)::ElfObjectFile::ProcessFile(std::vector<bloaty::RangeSink*, std::allocator<bloaty::RangeSink*> > const&) const  (/src/bloaty/src/elf.cc:1297-1359, calls bloaty::ReadDWARFCompileUnits(bloaty::dwarf::File const&, bloaty::DualMap const&, bloaty::RangeSink*) at line 1331)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0      2170  bloaty::RangeSink::AddRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long, unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1314-1347)
      70      2170  bloaty::RangeSink::ContainsVerboseVMAddr(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1090-1094)
      70      2170  bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1102-1131)  <-- enclosing
     690      2210  bloaty::NameMunger::Munge[abi:cxx11](std::basic_string_view<char, std::char_traits<char> >) const  (/src/bloaty/src/bloaty.cc:210-221)
     620        38  bloaty::RangeSink::AddFileRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1169-1190)
     600        60  bloaty::ConfiguredDataSource::ConfiguredDataSource(bloaty::DataSourceDefinition const&)  (/src/bloaty/src/bloaty.cc:1445-1447)
     310        16  bloaty::CheckedAdd(long*, long)  (/src/bloaty/src/bloaty.cc:122-136)
     310        16  bloaty::Rollup::AddInternal(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, unsigned long, unsigned long, bool)  (/src/bloaty/src/bloaty.cc:337-375)
     272        28  bloaty::Rollup::Rollup()  (/src/bloaty/src/bloaty.cc:251-251)
     192        16  bloaty::Rollup::Percent(long, long)  (/src/bloaty/src/bloaty.cc:377-389)
     155         4  bloaty::DualMaps::ComputeRollup(bloaty::Rollup*)::{lambda(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, unsigned long, unsigned long)#2}::operator()(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, unsigned long, unsigned long) const  (/src/bloaty/src/bloaty.cc:1651-1653)
     155         8  bloaty::Rollup::AddSizes(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, unsigned long, bool)  (/src/bloaty/src/bloaty.cc:259-262)
     140         0  bloaty::RangeSink::AddFileRangeForVMAddr(char const*, unsigned long, std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/bloaty.cc:1194-1217)
     130        13  bloaty::RangeSink::RangeSink(bloaty::InputFile const*, bloaty::Options const&, bloaty::DataSource, bloaty::DualMap const*, google::protobuf::Arena*)  (/src/bloaty/src/bloaty.cc:1079-1083)
     130        13  bloaty::RangeSink::~RangeSink()  (/src/bloaty/src/bloaty.cc:1085-1085)
... (34 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  bloaty::RangeSink::AddVMRange(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/bloaty.cc:1278-1296) ---
  d=2   L1280  T=0 F=70  T=0 F=0  if (verbose) {
  d=2   L1286  T=70 F=70  T=0 F=0  for (auto& pair : outputs_) {
  d=2   L1291  T=70 F=0  T=0 F=0  if (!ok) {
--- d=1  bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1102-1131) ---
  d=1   L1103  T=70 F=0  T=0 F=2170  if (vmsize == RangeMap::kUnknownSize) {  <-- BLOCKER
  d=1   L1107  T=0 F=70  T=0 F=2170  if (vmaddr + vmsize < vmaddr) {
  d=1   L1111  T=0 F=70  T=0 F=2170  if (ContainsVerboseVMAddr(vmaddr, vmsize)) {
  d=1   L1115  T=0 F=70  T=0 F=640  if (translator_ && options_.has_debug_fileoff()) {
  d=1   L1115  T=70 F=0  T=640 F=1530  if (translator_ && options_.has_debug_fileoff()) {

[off-chain: 111 additional divergent branches across 28 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=007b5827d861c66f, size=481 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=44890s, mutation_op=BytesDeleteMutator,TokenInsert,BytesDeleteMutator):
  0000: ce fa ed fe 7f 95 e8 e0 0a 00 18 24 24 20 20 20   ...........$$   
  0010: 01 00 00 00 20 ce 20 00 00 20 20 00 02 00 00 00   .... . ..  .....
  0020: 5f 00 00 00 00 01 00 00 07 00 00 00 80 00 00 00   _...............
  0030: 00 01 00 00 ff 00 00 00 20 00 1b 00 00 00 18 88   ........ .......
Seed 2 (id=00543fe52d18cbcf, size=481 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=44985s, mutation_op=ByteNegMutator,DwordAddMutator,BytesRandSetMutator,ByteDecMutator,BytesExpandMutator,BytesSetMutator):
  0000: ce fa ed fe 7f 95 e8 e0 0a 00 18 24 24 20 20 20   ...........$$   
  0010: 01 00 00 00 20 ce 20 00 00 20 20 00 02 00 00 00   .... . ..  .....
  0020: 5f 00 00 00 00 01 00 00 07 00 00 00 80 00 00 00   _...............
  0030: 00 01 00 00 ff 00 00 00 20 00 1b 00 00 00 18 88   ........ .......
Seed 3 (id=007c2cba25c7ebe1, size=521 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=45026s, mutation_op=DwordAddMutator):
  0000: ce fa ed fe 7f 95 e8 e0 0a 00 18 24 24 20 20 20   ...........$$   
  0010: 01 00 00 00 20 ce 20 00 00 20 20 00 02 00 00 00   .... . ..  .....
  0020: 5f 00 00 00 00 01 00 00 07 00 00 00 80 00 00 00   _...............
  0030: 00 01 00 00 80 00 00 00 20 00 1b 00 00 00 18 88   ........ .......
Seed 4 (id=003dc3258ece2f1a, size=493 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=45427s, mutation_op=WordInterestingMutator,DwordAddMutator,BytesDeleteMutator,BytesSetMutator,BytesRandInsertMutator):
  0000: ce fa ed fe 7f 95 e8 e0 0a 00 18 24 24 20 20 20   ...........$$   
  0010: 01 00 00 00 20 21 20 00 00 20 20 00 02 00 00 00   .... ! ..  .....
  0020: 5f 00 00 00 00 01 00 00 07 00 00 00 80 00 00 00   _...............
  0030: 00 01 00 00 ff 00 00 00 20 00 1b 00 00 00 18 88   ........ .......
Seed 5 (id=000e28b08e64f97d, size=555 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=45567s, mutation_op=BytesInsertMutator,ByteAddMutator):
  0000: ce fa ed fe 7f 95 e8 e0 0a 00 18 24 24 20 20 20   ...........$$   
  0010: 01 00 00 00 20 ce 20 00 00 20 20 00 02 00 00 00   .... . ..  .....
  0020: 5f 01 00 00 00 01 00 00 07 00 00 00 80 00 00 00   _...............
  0030: 00 01 00 00 80 00 00 00 20 00 1b 00 00 00 18 88   ........ .......

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=51265bea2d00b019, size=106 bytes, fuzzer=value_profile, trial=1, discovered_at=71310s, mutation_op=TokenReplace,DwordInterestingMutator,ByteInterestingMutator):
  0000: 7f 45 4c 46 01 01 01 00 00 00 00 00 00 00 00 00   .ELF............
  0010: 00 00 08 08 08 00 00 00 00 00 ff ff 06 00 00 00   ................
  0020: 00 00 00 00 00 00 10 00 00 00 00 00 80 00 00 00   ................
  0030: 00 00 00 20 01 00 00 00 20 20 20 20 20 20 ff 1e   ... ....      ..


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  ce(.)x10                            7f(.)x1                             DIFFER
   0x0001  fa(.)x10                            45(E)x1                             DIFFER
   0x0002  ed(.)x10                            4c(L)x1                             DIFFER
   0x0003  fe(.)x10                            46(F)x1                             DIFFER
   0x0004  7f(.)x10                            01(.)x1                             DIFFER
   0x0005  95(.)x10                            01(.)x1                             DIFFER
   0x0006  e8(.)x10                            01(.)x1                             DIFFER
   0x0007  e0(.)x10                            00(.)x1                             DIFFER
   0x0008  0a(.)x10                            00(.)x1                             DIFFER
   0x000a  18(.)x10                            00(.)x1                             DIFFER
   0x000b  24($)x10                            00(.)x1                             DIFFER
   0x000c  24($)x10                            00(.)x1                             DIFFER
   0x000d  20( )x10                            00(.)x1                             DIFFER
   0x000e  20( )x10                            00(.)x1                             DIFFER
   0x000f  20( )x10                            00(.)x1                             DIFFER
   0x0010  01(.)x10                            00(.)x1                             DIFFER
   0x0012  00(.)x10                            08(.)x1                             DIFFER
   0x0013  00(.)x10                            08(.)x1                             DIFFER
   0x0014  20( )x10                            08(.)x1                             DIFFER
   0x0015  ce(.)x9 21(!)x1                     00(.)x1                             DIFFER
   0x0016  20( )x10                            00(.)x1                             DIFFER
   0x0019  20( )x10                            00(.)x1                             DIFFER
   0x001a  20( )x10                            ff(.)x1                             DIFFER
   0x001b  00(.)x10                            ff(.)x1                             DIFFER
   0x001c  02(.)x10                            06(.)x1                             DIFFER
   0x0020  5f(_)x10                            00(.)x1                             DIFFER
   0x0021  00(.)x7 01(.)x3                     00(.)x1                             PARTIAL
   0x0025  01(.)x10                            00(.)x1                             DIFFER
   0x0026  00(.)x10                            10(.)x1                             DIFFER
   0x0028  07(.)x10                            00(.)x1                             DIFFER
   0x0031  01(.)x10                            00(.)x1                             DIFFER
   0x0033  00(.)x10                            20( )x1                             DIFFER
   0x0034  ff(.)x6 80(.)x4                     01(.)x1                             DIFFER
   0x0039  00(.)x10                            20( )x1                             DIFFER
   0x003a  1b(.)x10                            20( )x1                             DIFFER
   0x003b  00(.)x10                            20( )x1                             DIFFER
   0x003c  00(.)x10                            20( )x1                             DIFFER
   0x003d  00(.)x10                            20( )x1                             DIFFER
   0x003e  18(.)x10                            ff(.)x1                             DIFFER
   0x003f  88(.)x10                            1e(.)x1                             DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/bloaty_7.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7,
  "target": "bloaty",
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).