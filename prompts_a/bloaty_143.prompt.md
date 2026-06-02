==== BLOCKER ====
Target: bloaty
Branch ID: 143
Location: /src/bloaty/src/range_map.cc:260:7
Enclosing function: bloaty::RangeMap::AddRangeWithTranslation(unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::RangeMap const&, bool, bloaty::RangeMap*)
Source line:   if (size == kUnknownSize) {
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
  avg duration blocked: winner=3.80h  loser=24.00h
  avg hitcount on branch: winner=22887  loser=0
  prob_div=1.00  dur_div=20.20h  hit_div=22887
  subject-level: delta_AUC=49070700.0  p_AUC=0.0002  delta_Final=792.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/bloaty/143/{W,L}/branch_coverage_show.txt

--- Enclosing function: bloaty::RangeMap::AddRangeWithTranslation(unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::RangeMap const&, bool, bloaty::RangeMap*) (/src/bloaty/src/range_map.cc:257-289) ---
[ ]   255                                         const RangeMap& translator,
[ ]   256                                         bool verbose,
[B]   257                                         RangeMap* other) {
[B]   258    auto it = translator.FindContaining(addr);
[B]   259    uint64_t end;
[B]   260    if (size == kUnknownSize) { <-- BLOCKER
[W]   261      end = addr + 1;
[B]   262    } else {
[B]   263      end = addr + size;
[B]   264      assert(end >= addr);
[B]   265    }
[B]   266    uint64_t total_size = 0;
[ ]   267  
[ ]   268    // TODO: optionally warn about when we span ranges of the translator.  In some
[ ]   269    // cases this would be a bug (ie. symbols VM->file).  In other cases it's
[ ]   270    // totally normal (ie. archive members file->VM).
[B]   271    while (!translator.IterIsEnd(it) && it->first < end) {
[B]   272      uint64_t translated_addr;
[B]   273      uint64_t trimmed_addr;
[B]   274      uint64_t trimmed_size;
[B]   275      if (translator.TranslateAndTrimRangeWithEntry(
[B]   276              it, addr, size, &trimmed_addr, &translated_addr, &trimmed_size)) {
[ ]   277        if (verbose_level > 2 || verbose) {
[ ]   278          printf("  -> translates to: [%" PRIx64 " %" PRIx64 "]\n", translated_addr,
[ ]   279                 trimmed_size);
[ ]   280        }
[ ]   281        other->AddRange(translated_addr, trimmed_size, val);
[ ]   282      }
[B]   283      AddRange(trimmed_addr, trimmed_size, val);
[B]   284      total_size += trimmed_size;
[B]   285      ++it;
[B]   286    }
[ ]   287  
[B]   288    return total_size == size;
[B]   289  }

--- Caller (1 hop): bloaty::RangeSink::AddFileRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long) (/src/bloaty/src/bloaty.cc:1169-1190, calls bloaty::RangeMap::AddRangeWithTranslation(unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::RangeMap const&, bool, bloaty::RangeMap*) at line 1179) (full body — short) ---
[B]  1169                               uint64_t fileoff, uint64_t filesize) {
[B]  1170    bool verbose = IsVerboseForFileRange(fileoff, filesize);
[B]  1171    if (verbose) {
[ ]  1172      printf("[%s, %s] AddFileRange(%.*s, %" PRIx64 ", %" PRIx64 ")\n",
[ ]  1173             GetDataSourceLabel(data_source_), analyzer, (int)name.size(),
[ ]  1174             name.data(), fileoff, filesize);
[ ]  1175    }
[B]  1176    for (auto& pair : outputs_) {
[B]  1177      const std::string label = pair.second->Munge(name);
[B]  1178      if (translator_) {
[B]  1179        bool ok = pair.first->file_map.AddRangeWithTranslation( <-- CALL
[B]  1180            fileoff, filesize, label, translator_->file_map, verbose,
[B]  1181            &pair.first->vm_map);
[B]  1182        if (!ok) {
[W]  1183          WARN("File range ($0, $1) for label $2 extends beyond base map",
[W]  1184               fileoff, filesize, name);
[W]  1185        }
[B]  1186      } else {
[B]  1187        pair.first->file_map.AddRange(fileoff, filesize, label);
[B]  1188      }
[B]  1189    }
[B]  1190  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  bloaty::RangeSink::IsVerboseForFileRange(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1133-1162, calls bloaty::RangeMap::AddRangeWithTranslation(unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::RangeMap const&, bool, bloaty::RangeMap*) at line 1151)
hop 2  bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1102-1131, calls bloaty::RangeMap::AddRangeWithTranslation(unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::RangeMap const&, bool, bloaty::RangeMap*) at line 1119)
hop 3  bloaty::RangeSink::AddFileRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1169-1190, calls bloaty::RangeSink::IsVerboseForFileRange(unsigned long, unsigned long) at line 1170)
hop 3  bloaty::RangeSink::AddFileRangeForVMAddr(char const*, unsigned long, std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/bloaty.cc:1194-1217, calls bloaty::RangeSink::IsVerboseForFileRange(unsigned long, unsigned long) at line 1196)
hop 3  bloaty::RangeSink::AddVMRange(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/bloaty.cc:1278-1296, calls bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long) at line 1279)
hop 3  bloaty::RangeSink::AddVMRangeForVMAddr(char const*, unsigned long, unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1252-1275, calls bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long) at line 1253)
hop 4  bloaty.cc:bloaty::Bloaty::ScanAndRollupFile(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::Rollup*, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*) const::$_1::operator()(unsigned long, unsigned long) const  (/src/bloaty/src/bloaty.cc:1771-1774, calls bloaty::RangeSink::AddFileRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long) at line 1772)
hop 4  bloaty::RangeSink::AddVMRangeAllowAlias(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/bloaty.cc:1299-1303, calls bloaty::RangeSink::AddVMRange(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) at line 1302)
hop 4  bloaty::RangeSink::AddVMRangeIgnoreDuplicate(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/bloaty.cc:1307-1310, calls bloaty::RangeSink::AddVMRange(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) at line 1309)
hop 4  bloaty::RangeSink::AddFileRange(char const*, std::basic_string_view<char, std::char_traits<char> >, std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/bloaty.h:159-170, calls bloaty::RangeSink::AddFileRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long) at line 167)
hop 4  bloaty::DisassembleFindReferences(bloaty::DisassemblyInfo const&, bloaty::RangeSink*)  (/src/bloaty/src/disassemble.cc:43-94, calls bloaty::RangeSink::AddVMRangeForVMAddr(char const*, unsigned long, unsigned long, unsigned long) at line 84)
hop 4  bloaty::ReadEhFrame(std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*)  (/src/bloaty/src/eh_frame.cc:125-226, calls bloaty::RangeSink::AddFileRangeForVMAddr(char const*, unsigned long, std::basic_string_view<char, std::char_traits<char> >) at line 223)
hop 4  bloaty::ReadEhFrameHdr(std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*)  (/src/bloaty/src/eh_frame.cc:230-262, calls bloaty::RangeSink::AddFileRangeForVMAddr(char const*, unsigned long, std::basic_string_view<char, std::char_traits<char> >) at line 254)
hop 5  bloaty.cc:bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::$_0::operator()(bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::PerThreadData*) const  (/src/bloaty/src/bloaty.cc:1822-1831, calls bloaty.cc:bloaty::Bloaty::ScanAndRollupFile(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::Rollup*, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*) const::$_1::operator()(unsigned long, unsigned long) const at line 1826)
hop 5  bloaty::dwarf::ReadRangeList(bloaty::dwarf::CU const&, unsigned long, std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*, std::basic_string_view<char, std::char_traits<char> >*)  (/src/bloaty/src/dwarf.cc:177-194, calls bloaty::RangeSink::AddVMRangeIgnoreDuplicate(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) at line 190)
hop 5  dwarf.cc:bloaty::ReadDWARFAddressRanges(bloaty::dwarf::File const&, bloaty::RangeSink*)  (/src/bloaty/src/dwarf.cc:237-295, calls bloaty::RangeSink::AddVMRangeIgnoreDuplicate(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) at line 287)
hop 5  elf.cc:bloaty::(anonymous namespace)::ReadELFSymbols(bloaty::InputFile const&, bloaty::RangeSink*, std::map<std::basic_string_view<char, std::char_traits<char> >, std::pair<unsigned long, unsigned long>, std::less<std::basic_string_view<char, std::char_traits<char> > >, std::allocator<std::pair<std::basic_string_view<char, std::char_traits<char> > const, std::pair<unsigned long, unsigned long> > > >*, bool)::$_0::operator()(bloaty::(anonymous namespace)::ElfFile const&, std::basic_string_view<char, std::char_traits<char> >, unsigned long) const  (/src/bloaty/src/elf.cc:855-921, calls bloaty::DisassembleFindReferences(bloaty::DisassemblyInfo const&, bloaty::RangeSink*) at line 917)
hop 5  elf.cc:bloaty::(anonymous namespace)::ReadELFTables(bloaty::InputFile const&, bloaty::RangeSink*)::$_0::operator()(bloaty::(anonymous namespace)::ElfFile const&, std::basic_string_view<char, std::char_traits<char> >, unsigned int) const  (/src/bloaty/src/elf.cc:990-1017, calls bloaty::ReadEhFrame(std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*) at line 1012)
hop 6  bloaty::Bloaty::ScanAndRollup(bloaty::Options const&, bloaty::RollupOutput*)  (/src/bloaty/src/bloaty.cc:1854-1911, calls bloaty.cc:bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::$_0::operator()(bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::PerThreadData*) const at line 1869)
hop 6  bloaty::AddDIE(bloaty::dwarf::CU const&, bloaty::GeneralDIE const&, bloaty::DualMap const&, bloaty::RangeSink*)  (/src/bloaty/src/dwarf.cc:406-540, calls bloaty::dwarf::ReadRangeList(bloaty::dwarf::CU const&, unsigned long, std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*, std::basic_string_view<char, std::char_traits<char> >*) at line 529)
hop 6  bloaty::ReadDWARFCompileUnits(bloaty::dwarf::File const&, bloaty::DualMap const&, bloaty::dwarf::CU const*, bloaty::RangeSink*)  (/src/bloaty/src/dwarf.cc:656-674, calls dwarf.cc:bloaty::ReadDWARFAddressRanges(bloaty::dwarf::File const&, bloaty::RangeSink*) at line 662)
hop 7  bloaty::BloatyDoMain(bloaty::Options const&, bloaty::InputFileFactory const&, bloaty::RollupOutput*)  (/src/bloaty/src/bloaty.cc:2233-2278, calls bloaty::Bloaty::ScanAndRollup(bloaty::Options const&, bloaty::RollupOutput*) at line 2274)
hop 7  bloaty::ReadDWARFCompileUnits(bloaty::dwarf::File const&, bloaty::DualMap const&, bloaty::RangeSink*)  (/src/bloaty/src/bloaty.h:303-305, calls bloaty::ReadDWARFCompileUnits(bloaty::dwarf::File const&, bloaty::DualMap const&, bloaty::dwarf::CU const*, bloaty::RangeSink*) at line 304)
hop 7  dwarf.cc:bloaty::ReadDWARFDebugInfo(bloaty::dwarf::InfoReader&, bloaty::dwarf::InfoReader::Section, bloaty::DualMap const&, bloaty::RangeSink*)  (/src/bloaty/src/dwarf.cc:586-653, calls bloaty::AddDIE(bloaty::dwarf::CU const&, bloaty::GeneralDIE const&, bloaty::DualMap const&, bloaty::RangeSink*) at line 628)
hop 8  bloaty::BloatyMain(bloaty::Options const&, bloaty::InputFileFactory const&, bloaty::RollupOutput*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >*)  (/src/bloaty/src/bloaty.cc:2281-2289, calls bloaty::BloatyDoMain(bloaty::Options const&, bloaty::InputFileFactory const&, bloaty::RollupOutput*) at line 2283)
hop 8  elf.cc:bloaty::(anonymous namespace)::ElfObjectFile::ProcessFile(std::vector<bloaty::RangeSink*, std::allocator<bloaty::RangeSink*> > const&) const  (/src/bloaty/src/elf.cc:1297-1359, calls bloaty::ReadDWARFCompileUnits(bloaty::dwarf::File const&, bloaty::DualMap const&, bloaty::RangeSink*) at line 1331)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     140         0  bloaty::RangeSink::AddFileRangeForVMAddr(char const*, unsigned long, std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/bloaty.cc:1194-1217)
     140         0  bloaty::RangeMap::TryGetLabel(unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >*) const  (/src/bloaty/src/range_map.cc:97-105)
      70         0  bloaty::ItaniumDemangle[abi:cxx11](std::basic_string_view<char, std::char_traits<char> >, bloaty::DataSource)  (/src/bloaty/src/bloaty.cc:167-200)
      70         0  bloaty::RangeSink::ContainsVerboseVMAddr(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1090-1094)
      70         0  bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1102-1131)
      70         0  bloaty::RangeSink::AddVMRange(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/bloaty.cc:1278-1296)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  bloaty::RangeSink::AddFileRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1169-1190) ---
  d=3   L1171  T=0 F=620  T=0 F=1380  if (verbose) {
  d=3   L1176  T=620 F=620  T=1380 F=1380  for (auto& pair : outputs_) {
  d=3   L1178  T=200 F=420  T=366 F=1020  if (translator_) {
  d=3   L1182  T=15 F=185  T=0 F=366  if (!ok) {
--- d=3  bloaty::RangeSink::AddFileRangeForVMAddr(char const*, unsigned long, std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/bloaty.cc:1194-1217) ---
  d=3   L1197  T=0 F=140  T=0 F=0  if (verbose) {
  d=3   L1203  T=140 F=140  T=0 F=0  for (auto& pair : outputs_) {
  d=3   L1205  T=0 F=140  T=0 F=0  if (pair.first->vm_map.TryGetLabel(label_from_vmaddr, &la...
  d=3   L1213  T=0 F=140  T=0 F=0  } else if (verbose_level > 1) {
--- d=3  bloaty::RangeSink::AddVMRange(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/bloaty.cc:1278-1296) ---
  d=3   L1280  T=0 F=70  T=0 F=0  if (verbose) {
  d=3   L1286  T=70 F=70  T=0 F=0  for (auto& pair : outputs_) {
  d=3   L1291  T=70 F=0  T=0 F=0  if (!ok) {
--- d=2  bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1102-1131) ---
  d=2   L1103  T=70 F=0  T=0 F=0  if (vmsize == RangeMap::kUnknownSize) {
  d=2   L1107  T=0 F=70  T=0 F=0  if (vmaddr + vmsize < vmaddr) {
  d=2   L1111  T=0 F=70  T=0 F=0  if (ContainsVerboseVMAddr(vmaddr, vmsize)) {
  d=2   L1115  T=0 F=70  T=0 F=0  if (translator_ && options_.has_debug_fileoff()) {
  d=2   L1115  T=70 F=0  T=0 F=0  if (translator_ && options_.has_debug_fileoff()) {
--- d=1  bloaty::RangeMap::AddRangeWithTranslation(unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::RangeMap const&, bool, bloaty::RangeMap*)  (/src/bloaty/src/range_map.cc:257-289) ---
  d=1   L 260  T=70 F=200  T=0 F=366  if (size == kUnknownSize) {  <-- BLOCKER

[off-chain: 12 additional divergent branches across 7 functions (see HIT-COUNT DIVERGENCE for which functions)]

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
Seed 3 (id=002a1e64c96e64b5, size=17 bytes, fuzzer=value_profile, trial=1, discovered_at=765s, mutation_op=WordAddMutator):
  0000: 00 61 73 6d 00 ab 20 00 8a 06 06 02 00 00 ff 00   .asm.. .........
  0010: ff                                                .
Seed 4 (id=000a8607725bb7a8, size=46 bytes, fuzzer=value_profile, trial=1, discovered_at=1239s, mutation_op=ByteIncMutator,BitFlipMutator,ByteNegMutator,ByteAddMutator):
  0000: 00 61 73 6d 00 80 00 00 02 24 e0 04 00 00 01 00   .asm.....$......
  0010: 80 00 00 00 05 01 03 03 03 03 03 03 fe 00 10 00   ................
  0020: 03 03 03 01 00 00 00 02 00 ff 7f 00 00 ff         ..............
Seed 5 (id=0001abf195b2fd72, size=46 bytes, fuzzer=value_profile, trial=1, discovered_at=2013s, mutation_op=ByteRandMutator):
  0000: 00 61 73 6d 00 20 20 ff 02 24 e0 00 00 00 01 00   .asm.  ..$......
  0010: 80 80 00 00 a5 00 00 00 00 04 80 00 f9 00 00 00   ................
  0020: 01 00 00 00 2b 00 00 02 01 00 64 6d fb 00         ....+.....dm..


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  ce(.)x10                            00(.)x10                            DIFFER
   0x0001  fa(.)x10                            61(a)x10                            DIFFER
   0x0002  ed(.)x10                            73(s)x10                            DIFFER
   0x0003  fe(.)x10                            6d(m)x10                            DIFFER
   0x0004  7f(.)x10                            00(.)x8 7b({)x1 ff(.)x1             DIFFER
   0x0005  95(.)x10                            20( )x5 e8(.)x1 ab(.)x1 80(.)x1 +2u  DIFFER
   0x0006  e8(.)x10                            20( )x4 e9(.)x1 00(.)x1 7f(.)x1 +3u  DIFFER
   0x0007  e0(.)x10                            ff(.)x3 00(.)x2 6d(m)x2 2d(-)x1 +2u  DIFFER
   0x0008  0a(.)x10                            02(.)x4 00(.)x3 01(.)x2 8a(.)x1     DIFFER
   0x0009  00(.)x10                            24($)x5 20( )x2 25(%)x1 06(.)x1 +1u  DIFFER
   0x000a  18(.)x10                            e0(.)x3 20( )x2 1f(.)x1 06(.)x1 +3u  DIFFER
   0x000b  24($)x10                            00(.)x7 02(.)x1 04(.)x1 01(.)x1     DIFFER
   0x000c  24($)x10                            00(.)x6 fe(.)x1 01(.)x1 38(8)x1 +1u  DIFFER
   0x000d  20( )x10                            00(.)x6 ff(.)x1 02(.)x1 17(.)x1 +1u  DIFFER
   0x000e  20( )x10                            ff(.)x2 01(.)x2 00(.)x1 24($)x1 +4u  DIFFER
   0x000f  20( )x10                            00(.)x5 ff(.)x1 77(w)x1 05(.)x1 +2u  DIFFER
   0x0010  01(.)x10                            00(.)x3 ff(.)x2 80(.)x2 7f(.)x1 +2u  DIFFER
   0x0011  00(.)x10                            00(.)x3 02(.)x1 80(.)x1 28(()x1 +3u  PARTIAL
   0x0012  00(.)x10                            00(.)x5 24($)x1 20( )x1 f8(.)x1 +1u  PARTIAL
   0x0013  00(.)x10                            00(.)x6 7f(.)x1 07(.)x1 dd(.)x1     PARTIAL
   0x0014  20( )x10                            00(.)x2 c1(.)x1 05(.)x1 a5(.)x1 +4u  DIFFER
   0x0015  ce(.)x9 21(!)x1                     00(.)x4 c1(.)x1 01(.)x1 fe(.)x1 +2u  DIFFER
   0x0016  20( )x10                            00(.)x4 dd(.)x1 03(.)x1 fe(.)x1 +2u  DIFFER
   0x0017  00(.)x10                            00(.)x2 88(.)x1 01(.)x1 03(.)x1 +4u  PARTIAL
   0x0018  00(.)x10                            00(.)x2 88(.)x1 02(.)x1 03(.)x1 +4u  PARTIAL
   0x0019  20( )x10                            00(.)x2 88(.)x1 03(.)x1 04(.)x1 +4u  DIFFER
   0x001a  20( )x10                            88(.)x1 ff(.)x1 03(.)x1 80(.)x1 +5u  DIFFER
   0x001b  00(.)x10                            00(.)x3 03(.)x2 cf(.)x1 02(.)x1 +2u  PARTIAL
   0x001c  02(.)x10                            fe(.)x2 00(.)x1 02(.)x1 f9(.)x1 +4u  PARTIAL
   0x001d  00(.)x10                            00(.)x4 06(.)x2 02(.)x1 ff(.)x1 +1u  PARTIAL
   0x001e  00(.)x10                            10(.)x2 00(.)x2 01(.)x1 02(.)x1 +3u  PARTIAL
   0x001f  00(.)x10                            00(.)x5 02(.)x1 06(.)x1 93(.)x1 +1u  PARTIAL
   0x0020  5f(_)x10                            00(.)x2 0c(.)x1 02(.)x1 03(.)x1 +4u  DIFFER
   0x0021  00(.)x7 01(.)x3                     00(.)x3 20( )x1 02(.)x1 03(.)x1 +3u  PARTIAL
   0x0022  00(.)x10                            02(.)x2 00(.)x2 73(s)x1 03(.)x1 +3u  PARTIAL
   0x0023  00(.)x10                            ff(.)x1 02(.)x1 01(.)x1 00(.)x1 +5u  PARTIAL
   0x0024  00(.)x10                            1a(.)x2 01(.)x1 00(.)x1 2b(+)x1 +4u  PARTIAL
   0x0025  01(.)x10                            00(.)x3 fd(.)x1 04(.)x1 20( )x1 +3u  DIFFER
   0x0026  00(.)x10                            00(.)x4 20( )x2 07(.)x1 82(.)x1 +1u  PARTIAL
   0x0027  00(.)x10                            02(.)x2 b5(.)x1 4a(J)x1 06(.)x1 +4u  DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/bloaty_143.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 143,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 143 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 143 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 143 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).