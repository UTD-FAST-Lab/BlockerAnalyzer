==== BLOCKER ====
Target: bloaty
Branch ID: 145
Location: /src/bloaty/src/range_map.cc:315:16
Enclosing function: bloaty::RangeMap::CoversRange(unsigned long, unsigned long) const
Source line:     } else if (it == mappings_.end() || !EntryContains(it, addr)) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    4        6          0  REFERENCE
value_profile_cmplog             8        2          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     2        8          0  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        4        4          2  REFERENCE
fast                             2        8          0  REFERENCE
grimoire                         7        3          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=4.00h  loser=22.40h
  avg hitcount on branch: winner=26  loser=0
  prob_div=1.00  dur_div=18.40h  hit_div=26
  subject-level: delta_AUC=26255160.0  p_AUC=0.0002  delta_Final=523.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/bloaty/145/{W,L}/branch_coverage_show.txt

--- Enclosing function: bloaty::RangeMap::CoversRange(unsigned long, unsigned long) const (/src/bloaty/src/range_map.cc:307-321) ---
[B]   305  }
[ ]   306  
[B]   307  bool RangeMap::CoversRange(uint64_t addr, uint64_t size) const {
[B]   308    auto it = FindContaining(addr);
[B]   309    uint64_t end = addr + size;
[B]   310    assert(end >= addr);
[ ]   311  
[B]   312    while (true) {
[B]   313      if (addr >= end) {
[L]   314        return true;
[B]   315      } else if (it == mappings_.end() || !EntryContains(it, addr)) { <-- BLOCKER
[W]   316        return false;
[W]   317      }
[L]   318      addr = RangeEnd(it);
[L]   319      it++;
[L]   320    }
[B]   321  }

--- Caller (1 hop): bloaty::RangeSink::AddRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long, unsigned long, unsigned long) (/src/bloaty/src/bloaty.cc:1314-1347, calls bloaty::RangeMap::CoversRange(unsigned long, unsigned long) const at line 1331) (full body — short) ---
[B]  1314                           uint64_t filesize) {
[B]  1315    if (vmsize == RangeMap::kUnknownSize || filesize == RangeMap::kUnknownSize) {
[ ]  1316      // AddRange() is used for segments and sections; the mappings that establish
[ ]  1317      // the file <-> vm mapping.  The size should always be known.  Moreover it
[ ]  1318      // would be unclear how the logic should work if the size was *not* known.
[ ]  1319      THROW("AddRange() does not allow unknown size.");
[ ]  1320    }
[ ]  1321  
[B]  1322    if (IsVerboseForVMRange(vmaddr, vmsize) ||
[B]  1323        IsVerboseForFileRange(fileoff, filesize)) {
[ ]  1324      printf("[%s, %s] AddRange(%.*s, %" PRIx64 ", %" PRIx64 ", %" PRIx64
[ ]  1325             ", %" PRIx64 ")\n",
[ ]  1326             GetDataSourceLabel(data_source_), analyzer, (int)name.size(),
[ ]  1327             name.data(), vmaddr, vmsize, fileoff, filesize);
[ ]  1328    }
[ ]  1329  
[B]  1330    if (translator_) {
[B]  1331      if (!translator_->vm_map.CoversRange(vmaddr, vmsize) || <-- CALL
[B]  1332          !translator_->file_map.CoversRange(fileoff, filesize)) {
[W]  1333        THROW("Tried to add range that is not covered by base map.");
[W]  1334      }
[B]  1335    }
[ ]  1336  
[L]  1337    for (auto& pair : outputs_) {
[L]  1338      const std::string label = pair.second->Munge(name);
[L]  1339      uint64_t common = std::min(vmsize, filesize);
[ ]  1340  
[L]  1341      pair.first->vm_map.AddDualRange(vmaddr, common, fileoff, label);
[L]  1342      pair.first->file_map.AddDualRange(fileoff, common, vmaddr, label);
[ ]  1343  
[L]  1344      pair.first->vm_map.AddRange(vmaddr + common, vmsize - common, label);
[L]  1345      pair.first->file_map.AddRange(fileoff + common, filesize - common, label);
[L]  1346    }
[L]  1347  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  bloaty::RangeSink::AddRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long, unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1314-1347, calls bloaty::RangeMap::CoversRange(unsigned long, unsigned long) const at line 1331)
hop 3  bloaty::RangeMap::AddRange(unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/range_map.cc:146-148, calls bloaty::RangeSink::AddRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long, unsigned long, unsigned long) at line 146)
hop 3  bloaty::RangeMap::AddRangeWithTranslation(unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::RangeMap const&, bool, bloaty::RangeMap*)  (/src/bloaty/src/range_map.cc:257-289, calls bloaty::RangeSink::AddRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long, unsigned long, unsigned long) at line 281)
hop 4  bloaty::RangeSink::IsVerboseForFileRange(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1133-1162, calls bloaty::RangeMap::AddRangeWithTranslation(unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::RangeMap const&, bool, bloaty::RangeMap*) at line 1151)
hop 4  bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1102-1131, calls bloaty::RangeMap::AddRangeWithTranslation(unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::RangeMap const&, bool, bloaty::RangeMap*) at line 1119)
hop 5  bloaty::RangeSink::AddFileRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1169-1190, calls bloaty::RangeSink::IsVerboseForFileRange(unsigned long, unsigned long) at line 1170)
hop 5  bloaty::RangeSink::AddFileRangeForVMAddr(char const*, unsigned long, std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/bloaty.cc:1194-1217, calls bloaty::RangeSink::IsVerboseForFileRange(unsigned long, unsigned long) at line 1196)
hop 5  bloaty::RangeSink::AddVMRange(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/bloaty.cc:1278-1296, calls bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long) at line 1279)
hop 5  bloaty::RangeSink::AddVMRangeForVMAddr(char const*, unsigned long, unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1252-1275, calls bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long) at line 1253)
hop 6  bloaty.cc:bloaty::Bloaty::ScanAndRollupFile(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::Rollup*, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*) const::$_1::operator()(unsigned long, unsigned long) const  (/src/bloaty/src/bloaty.cc:1771-1774, calls bloaty::RangeSink::AddFileRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long) at line 1772)
hop 6  bloaty::RangeSink::AddVMRangeAllowAlias(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/bloaty.cc:1299-1303, calls bloaty::RangeSink::AddVMRange(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) at line 1302)
hop 6  bloaty::RangeSink::AddVMRangeIgnoreDuplicate(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/bloaty.cc:1307-1310, calls bloaty::RangeSink::AddVMRange(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) at line 1309)
hop 6  bloaty::RangeSink::AddFileRange(char const*, std::basic_string_view<char, std::char_traits<char> >, std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/bloaty.h:159-170, calls bloaty::RangeSink::AddFileRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long) at line 167)
hop 6  bloaty::DisassembleFindReferences(bloaty::DisassemblyInfo const&, bloaty::RangeSink*)  (/src/bloaty/src/disassemble.cc:43-94, calls bloaty::RangeSink::AddVMRangeForVMAddr(char const*, unsigned long, unsigned long, unsigned long) at line 84)
hop 6  bloaty::ReadEhFrame(std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*)  (/src/bloaty/src/eh_frame.cc:125-226, calls bloaty::RangeSink::AddFileRangeForVMAddr(char const*, unsigned long, std::basic_string_view<char, std::char_traits<char> >) at line 223)
hop 6  bloaty::ReadEhFrameHdr(std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*)  (/src/bloaty/src/eh_frame.cc:230-262, calls bloaty::RangeSink::AddFileRangeForVMAddr(char const*, unsigned long, std::basic_string_view<char, std::char_traits<char> >) at line 254)
hop 7  bloaty.cc:bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::$_0::operator()(bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::PerThreadData*) const  (/src/bloaty/src/bloaty.cc:1822-1831, calls bloaty.cc:bloaty::Bloaty::ScanAndRollupFile(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::Rollup*, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*) const::$_1::operator()(unsigned long, unsigned long) const at line 1826)
hop 7  bloaty::dwarf::ReadRangeList(bloaty::dwarf::CU const&, unsigned long, std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*, std::basic_string_view<char, std::char_traits<char> >*)  (/src/bloaty/src/dwarf.cc:177-194, calls bloaty::RangeSink::AddVMRangeIgnoreDuplicate(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) at line 190)
hop 7  dwarf.cc:bloaty::ReadDWARFAddressRanges(bloaty::dwarf::File const&, bloaty::RangeSink*)  (/src/bloaty/src/dwarf.cc:237-295, calls bloaty::RangeSink::AddVMRangeIgnoreDuplicate(char const*, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) at line 287)
hop 7  elf.cc:bloaty::(anonymous namespace)::ReadELFSymbols(bloaty::InputFile const&, bloaty::RangeSink*, std::map<std::basic_string_view<char, std::char_traits<char> >, std::pair<unsigned long, unsigned long>, std::less<std::basic_string_view<char, std::char_traits<char> > >, std::allocator<std::pair<std::basic_string_view<char, std::char_traits<char> > const, std::pair<unsigned long, unsigned long> > > >*, bool)::$_0::operator()(bloaty::(anonymous namespace)::ElfFile const&, std::basic_string_view<char, std::char_traits<char> >, unsigned long) const  (/src/bloaty/src/elf.cc:855-921, calls bloaty::DisassembleFindReferences(bloaty::DisassemblyInfo const&, bloaty::RangeSink*) at line 917)
hop 7  elf.cc:bloaty::(anonymous namespace)::ReadELFTables(bloaty::InputFile const&, bloaty::RangeSink*)::$_0::operator()(bloaty::(anonymous namespace)::ElfFile const&, std::basic_string_view<char, std::char_traits<char> >, unsigned int) const  (/src/bloaty/src/elf.cc:990-1017, calls bloaty::ReadEhFrame(std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*) at line 1012)
hop 8  bloaty::Bloaty::ScanAndRollup(bloaty::Options const&, bloaty::RollupOutput*)  (/src/bloaty/src/bloaty.cc:1854-1911, calls bloaty.cc:bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::$_0::operator()(bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::PerThreadData*) const at line 1869)
hop 8  bloaty::AddDIE(bloaty::dwarf::CU const&, bloaty::GeneralDIE const&, bloaty::DualMap const&, bloaty::RangeSink*)  (/src/bloaty/src/dwarf.cc:406-540, calls bloaty::dwarf::ReadRangeList(bloaty::dwarf::CU const&, unsigned long, std::basic_string_view<char, std::char_traits<char> >, bloaty::RangeSink*, std::basic_string_view<char, std::char_traits<char> >*) at line 529)
hop 8  bloaty::ReadDWARFCompileUnits(bloaty::dwarf::File const&, bloaty::DualMap const&, bloaty::dwarf::CU const*, bloaty::RangeSink*)  (/src/bloaty/src/dwarf.cc:656-674, calls dwarf.cc:bloaty::ReadDWARFAddressRanges(bloaty::dwarf::File const&, bloaty::RangeSink*) at line 662)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      50   6900000  bloaty::RangeMap::AddDualRange(unsigned long, unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/range_map.cc:182-243)
       0   4440000  void bloaty::RangeMap::MaybeSetLabel<std::_Rb_tree_iterator<std::pair<unsigned long const, bloaty::RangeMap::Entry> > >(std::_Rb_tree_iterator<std::pair<unsigned long const, bloaty::RangeMap::Entry> >, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long, unsigned long)  (/src/bloaty/src/range_map.cc:152-179)
      14   4310000  bloaty::RangeMap::FindContainingOrAfter(unsigned long)  (/src/bloaty/src/range_map.cc:66-74)
      50   3450000  bloaty::RangeMap::AddRange(unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/src/range_map.cc:146-148)
       6   1720000  bloaty::RangeSink::ContainsVerboseVMAddr(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1090-1094)
       6   1720000  bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1102-1131)
       6   1720000  bloaty::RangeSink::AddRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long, unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1314-1347)
      50   1720000  bloaty::NameMunger::Munge[abi:cxx11](std::basic_string_view<char, std::char_traits<char> >) const  (/src/bloaty/src/bloaty.cc:210-221)
      56   1720000  bloaty::RangeSink::ContainsVerboseFileOffset(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1096-1100)
      56   1720000  bloaty::RangeSink::IsVerboseForFileRange(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1133-1162)
       6   1010000  bloaty::RangeMap::CoversRange(unsigned long, unsigned long) const  (/src/bloaty/src/range_map.cc:307-321)  <-- enclosing
       8   1010000  bloaty::RangeMap::FindContaining(unsigned long) const  (/src/bloaty/src/range_map.cc:57-64)
     120      1020  bloaty::ConfiguredDataSource::ConfiguredDataSource(bloaty::DataSourceDefinition const&)  (/src/bloaty/src/bloaty.cc:1445-1447)
      50       646  bloaty::RangeSink::AddFileRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1169-1190)
      30       493  bloaty::Rollup::Rollup()  (/src/bloaty/src/bloaty.cc:251-251)
... (43 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=8  bloaty::Bloaty::ScanAndRollup(bloaty::Options const&, bloaty::RollupOutput*)  (/src/bloaty/src/bloaty.cc:1854-1911) ---
  d=8   L1855  T=0 F=12  T=0 F=102  if (input_files_.empty()) {
  d=8   L1859  T=12 F=12  T=102 F=102  for (const auto& name : source_names_) {
  d=8   L1866  T=12 F=12  T=102 F=102  for (const auto& file_info : input_files_) {
  d=8   L1871  T=0 F=12  T=0 F=102  if (!base_files_.empty()) {
  d=8   L1884  T=0 F=12  T=0 F=102  for (const auto& build_id : build_ids) {
  d=8   L1889  T=0 F=12  T=0 F=102  if (!debug_files_.empty()) {
--- d=7  bloaty.cc:bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::$_0::operator()(bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::PerThreadData*) const  (/src/bloaty/src/bloaty.cc:1822-1831) ---
  d=7   L1825  T=12 F=12  T=102 F=102  while (index.TryGetNext(&j)) {
--- d=5  bloaty::RangeSink::AddFileRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1169-1190) ---
  d=5   L1171  T=0 F=50  T=0 F=646  if (verbose) {
  d=5   L1176  T=50 F=50  T=646 F=646  for (auto& pair : outputs_) {
  d=5   L1178  T=2 F=48  T=238 F=408  if (translator_) {
  d=5   L1182  T=0 F=2  T=9 F=229  if (!ok) {
--- d=4  bloaty::RangeSink::IsVerboseForVMRange(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1102-1131) ---
  d=4   L1103  T=0 F=6  T=0 F=1720000  if (vmsize == RangeMap::kUnknownSize) {
  d=4   L1107  T=0 F=6  T=0 F=1720000  if (vmaddr + vmsize < vmaddr) {
  d=4   L1111  T=0 F=6  T=0 F=1720000  if (ContainsVerboseVMAddr(vmaddr, vmsize)) {
  d=4   L1115  T=0 F=6  T=0 F=507000  if (translator_ && options_.has_debug_fileoff()) {
  d=4   L1115  T=6 F=0  T=507000 F=1210000  if (translator_ && options_.has_debug_fileoff()) {
--- d=4  bloaty::RangeSink::IsVerboseForFileRange(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1133-1162) ---
  d=4   L1134  T=0 F=56  T=0 F=1720000  if (filesize == RangeMap::kUnknownSize) {
  d=4   L1138  T=0 F=56  T=0 F=1720000  if (fileoff + filesize < fileoff) {
  d=4   L1143  T=0 F=56  T=0 F=1720000  if (ContainsVerboseFileOffset(fileoff, filesize)) {
  d=4   L1147  T=8 F=48  T=508000 F=1210000  if (translator_ && options_.has_debug_vmaddr()) {
  d=4   L1147  T=0 F=8  T=0 F=508000  if (translator_ && options_.has_debug_vmaddr()) {
--- d=3  bloaty::RangeMap::AddRangeWithTranslation(unsigned long, unsigned long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::RangeMap const&, bool, bloaty::RangeMap*)  (/src/bloaty/src/range_map.cc:257-289) ---
  d=3   L 260  T=0 F=2  T=0 F=238  if (size == kUnknownSize) {
  d=3   L 271  T=2 F=0  T=311 F=117  while (!translator.IterIsEnd(it) && it->first < end) {
  d=3   L 271  T=2 F=2  T=428 F=121  while (!translator.IterIsEnd(it) && it->first < end) {
  d=3   L 275  T=0 F=2  T=42 F=269  if (translator.TranslateAndTrimRangeWithEntry(
  d=3   L 277  T=0 F=0  T=0 F=42  if (verbose_level > 2 || verbose) {
  d=3   L 277  T=0 F=0  T=0 F=42  if (verbose_level > 2 || verbose) {
--- d=2  bloaty::RangeSink::AddRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long, unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1314-1347) ---
  d=2   L1315  T=0 F=6  T=0 F=1720000  if (vmsize == RangeMap::kUnknownSize || filesize == Range...
  d=2   L1315  T=0 F=6  T=0 F=1720000  if (vmsize == RangeMap::kUnknownSize || filesize == Range...
  d=2   L1322  T=0 F=6  T=0 F=1720000  if (IsVerboseForVMRange(vmaddr, vmsize) ||
  d=2   L1323  T=0 F=6  T=0 F=1720000  IsVerboseForFileRange(fileoff, filesize)) {
  d=2   L1330  T=6 F=0  T=507000 F=1210000  if (translator_) {
  d=2   L1331  T=6 F=0  T=0 F=507000  if (!translator_->vm_map.CoversRange(vmaddr, vmsize) ||
  d=2   L1332  T=0 F=0  T=0 F=507000  !translator_->file_map.CoversRange(fileoff, filesize)) {
  d=2   L1337  T=0 F=0  T=1720000 F=1720000  for (auto& pair : outputs_) {
--- d=1  bloaty::RangeMap::CoversRange(unsigned long, unsigned long) const  (/src/bloaty/src/range_map.cc:307-321) ---
  d=1   L 313  T=0 F=6  T=1010000 F=1260000  if (addr >= end) {
  d=1   L 315  T=6 F=0  T=0 F=1260000  } else if (it == mappings_.end() || !EntryContains(it, ad...  <-- BLOCKER
  d=1   L 315  T=0 F=0  T=0 F=1260000  } else if (it == mappings_.end() || !EntryContains(it, ad...  <-- BLOCKER

[off-chain: 105 additional divergent branches across 27 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=05a56c847ffbf4de, size=86 bytes, fuzzer=cmplog, trial=2, discovered_at=4769s, mutation_op=DwordInterestingMutator):
  0000: 7f 45 4c 46 01 02 0a 0a 0a ff ff ff 7f 24 20 0a   .ELF.........$ .
  0010: 00 00 00 09 00 00 00 03 50 55 ff ff 00 00 00 00   ........PU......
  0020: 00 00 00 10 00 00 00 10 00 00 00 00 00 00 00 00   ................
  0030: 00 00 00 00 0a 0a 0a ff ff ff 7f 24 20 0a 0a 02   ...........$ ...
Seed 2 (id=bf6ba209e9cab437, size=86 bytes, fuzzer=cmplog, trial=2, discovered_at=4789s, mutation_op=ByteInterestingMutator,ByteRandMutator,ByteDecMutator,ByteInterestingMutator):
  0000: 7f 45 4c 46 01 02 0a 0a 0a ff ff ff 7f 24 20 0a   .ELF.........$ .
  0010: 00 00 00 08 00 00 00 03 50 55 ff ff 00 00 00 00   ........PU......
  0020: 00 00 00 10 00 00 00 10 00 00 3e 00 00 00 00 00   ..........>.....
  0030: 00 00 00 00 0a 0a 0a ff ff ff 7f 24 20 0a 0a 02   ...........$ ...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=43b1a3ff84794b7e, size=76 bytes, fuzzer=naive, trial=1, discovered_at=153s, mutation_op=BytesInsertMutator,CrossoverReplaceMutator):
  0000: 7f 45 4c 46 02 01 01 00 00 00 00 7f ff 20 20 00   .ELF.........  .
  0010: 00 00 00 00 00 00 20 20 20 20 20 20 ff 3c ff ff   ......      .<..
  0020: 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0030: 20 20 20 20 20 00 00 00 00 20 20 00 00 00 00 00        ....  .....
Seed 2 (id=040ca6fadf614081, size=192 bytes, fuzzer=naive, trial=2, discovered_at=176s, mutation_op=QwordAddMutator,ByteIncMutator,BytesRandSetMutator):
  0000: 7f 45 4c 46 01 01 01 00 00 e2 20 20 29 20 20 20   .ELF......  )   
  0010: 20 20 20 20 20 20 20 20 9c 9c 9c 00 9c 00 00 00           ........
  0020: 01 00 00 00 00 00 69 6e 66 00 00 00 00 11 00 40   ......inf......@
  0030: 00 00 00 00 69 6e 66 00 00 00 00 00 00 00 00 00   ....inf.........
Seed 3 (id=2510a93ad5db03cb, size=210 bytes, fuzzer=naive, trial=2, discovered_at=262s, mutation_op=DwordInterestingMutator,ByteNegMutator,BytesInsertCopyMutator,QwordAddMutator,TokenReplace,ByteAddMutator):
  0000: 7f 45 4c 46 01 01 01 00 00 e2 20 20 07 20 e5 20   .ELF......  . . 
  0010: 20 20 20 20 20 20 20 20 ae 9c 9b 00 9c 00 00 00           ........
  0020: 00 00 00 00 00 00 69 6e 00 00 00 00 40 00 00 00   ......in....@...
  0030: 00 00 00 00 69 81 66 00 00 00 00 00 00 00 00 00   ....i.f.........
Seed 4 (id=27c4344e01ef1c7a, size=198 bytes, fuzzer=naive, trial=2, discovered_at=730s, mutation_op=ByteInterestingMutator,BytesSetMutator):
  0000: 7f 45 4c 46 01 01 01 00 00 e2 20 20 07 20 e5 20   .ELF......  . . 
  0010: 20 20 20 20 20 20 20 20 9c 9c 9b 00 9c 00 00 00           ........
  0020: 00 00 00 00 00 00 69 6e 00 00 00 00 40 00 00 00   ......in....@...
  0030: 00 00 00 00 69 6e 66 00 00 00 00 00 00 00 00 00   ....inf.........
Seed 5 (id=017a47b9ccdfc684, size=64 bytes, fuzzer=naive, trial=1, discovered_at=2422s, mutation_op=DwordInterestingMutator):
  0000: 7f 45 4c 46 02 01 01 00 00 00 db 20 20 20 20 00   .ELF.......    .
  0010: 00 00 00 00 00 00 20 20 20 20 20 20 ff 3c ff ff   ......      .<..
  0020: 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0030: 20 20 20 20 20 00 00 00 01 00 20 20 00 00 20 20        .....  ..  


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0004  01(.)x2                             01(.)x14 02(.)x3                    PARTIAL
   0x0005  02(.)x2                             01(.)x17                            DIFFER
   0x0006  0a(.)x2                             01(.)x17                            DIFFER
   0x0007  0a(.)x2                             00(.)x12 06(.)x4 01(.)x1            DIFFER
   0x0008  0a(.)x2                             00(.)x13 f2(.)x4                    DIFFER
   0x0009  ff(.)x2                             e2(.)x10 00(.)x7                    DIFFER
   0x000a  ff(.)x2                             20( )x8 df(.)x5 00(.)x1 db(.)x1 +2u  DIFFER
   0x000b  ff(.)x2                             20( )x10 21(!)x3 7f(.)x1 45(E)x1 +2u  DIFFER
   0x000c  7f(.)x2                             20( )x5 df(.)x4 29())x2 07(.)x2 +4u  DIFFER
   0x000d  24($)x2                             20( )x11 23(#)x2 df(.)x2 46(F)x1 +1u  DIFFER
   0x000e  20( )x2                             20( )x11 e5(.)x2 23(#)x2 01(.)x1 +1u  PARTIAL
   0x000f  0a(.)x2                             20( )x8 00(.)x5 03(.)x2 01(.)x1 +1u  DIFFER
   0x0010  00(.)x2                             20( )x9 00(.)x3 01(.)x3 4c(L)x2     PARTIAL
   0x0011  00(.)x2                             20( )x8 00(.)x5 46(F)x2 01(.)x1 +1u  PARTIAL
   0x0012  00(.)x2                             20( )x10 00(.)x5 01(.)x2            PARTIAL
   0x0013  09(.)x1 08(.)x1                     20( )x10 f4(.)x4 00(.)x3            DIFFER
   0x0014  00(.)x2                             20( )x10 00(.)x7                    PARTIAL
   0x0015  00(.)x2                             20( )x10 00(.)x7                    PARTIAL
   0x0016  00(.)x2                             20( )x13 f2(.)x4                    DIFFER
   0x0017  03(.)x2                             20( )x13 00(.)x4                    DIFFER
   0x0018  50(P)x2                             9c(.)x8 20( )x7 ae(.)x1 35(5)x1     DIFFER
   0x0019  55(U)x2                             9c(.)x10 20( )x7                    DIFFER
   0x001a  ff(.)x2                             9c(.)x7 df(.)x4 20( )x3 9b(.)x3     DIFFER
   0x001b  ff(.)x2                             00(.)x10 20( )x7                    DIFFER
   0x001c  00(.)x2                             9c(.)x10 20( )x4 ff(.)x3            DIFFER
   0x001d  00(.)x2                             00(.)x14 3c(<)x2 ff(.)x1            PARTIAL
   0x001e  00(.)x2                             00(.)x14 ff(.)x3                    PARTIAL
   0x001f  00(.)x2                             00(.)x14 ff(.)x3                    PARTIAL
   0x0020  00(.)x2                             00(.)x8 01(.)x6 06(.)x3             PARTIAL
   0x0023  10(.)x2                             00(.)x17                            DIFFER
   0x0026  00(.)x2                             00(.)x10 69(i)x6 4d(M)x1            PARTIAL
   0x0027  10(.)x2                             00(.)x9 6e(n)x7 10(.)x1             PARTIAL
   0x0028  00(.)x2                             00(.)x9 66(f)x4 08(.)x2 26(&)x1 +1u  PARTIAL
   0x002a  00(.)x1 3e(>)x1                     00(.)x14 01(.)x3                    PARTIAL
   0x002c  00(.)x2                             00(.)x8 01(.)x4 40(@)x3 f2(.)x1 +1u  PARTIAL
   0x002d  00(.)x2                             00(.)x10 11(.)x2 20( )x2 6c(l)x2 +1u  PARTIAL
   0x002e  00(.)x2                             00(.)x13 6f(o)x4                    PARTIAL
   0x002f  00(.)x2                             00(.)x6 63(c)x4 1f(.)x4 40(@)x3     PARTIAL
   0x0030  00(.)x2                             00(.)x14 20( )x3                    PARTIAL
   0x0031  00(.)x2                             00(.)x15 20( )x2                    PARTIAL
   ... (14 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/bloaty_145.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 145,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 145 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 145 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 145 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).