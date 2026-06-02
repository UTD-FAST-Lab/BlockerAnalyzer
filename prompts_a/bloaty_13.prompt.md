==== BLOCKER ====
Target: bloaty
Branch ID: 13
Location: /src/bloaty/src/bloaty.cc:1750:7
Enclosing function: bloaty::Bloaty::ScanAndRollupFile(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::Rollup*, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*) const
Source line:   if (!build_id.empty()) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         6        4          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=5.50h  loser=24.00h
  avg hitcount on branch: winner=498  loser=0
  prob_div=1.00  dur_div=18.50h  hit_div=498
  subject-level: delta_AUC=26255160.0  p_AUC=0.0002  delta_Final=523.6  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.30h  loser=24.00h
  avg hitcount on branch: winner=177  loser=0
  prob_div=1.00  dur_div=20.70h  hit_div=177
  subject-level: delta_AUC=49070700.0  p_AUC=0.0002  delta_Final=792.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/bloaty/13/{W,L}/branch_coverage_show.txt

--- Enclosing function: bloaty::Bloaty::ScanAndRollupFile(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::Rollup*, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*) const (/src/bloaty/src/bloaty.cc:1718-1796) ---
[ ]  1716  
[ ]  1717  void Bloaty::ScanAndRollupFile(const std::string& filename, Rollup* rollup,
[B]  1718                                 std::vector<std::string>* out_build_ids) const {
[B]  1719    auto file = GetObjectFile(filename);
[ ]  1720  
[B]  1721    DualMaps maps;
[B]  1722    std::vector<std::unique_ptr<RangeSink>> sinks;
[B]  1723    std::vector<RangeSink*> sink_ptrs;
[B]  1724    std::vector<RangeSink*> filename_sink_ptrs;
[ ]  1725  
[ ]  1726    // Base map always goes first.
[B]  1727    sinks.push_back(absl::make_unique<RangeSink>(
[B]  1728        &file->file_data(), options_, DataSource::kSegments, nullptr, nullptr));
[B]  1729    NameMunger empty_munger;
[B]  1730    sinks.back()->AddOutput(maps.base_map(), &empty_munger);
[B]  1731    sink_ptrs.push_back(sinks.back().get());
[ ]  1732  
[B]  1733    for (auto source : sources_) {
[B]  1734      sinks.push_back(absl::make_unique<RangeSink>(
[B]  1735          &file->file_data(), options_, source->effective_source, maps.base_map(),
[B]  1736          arena_.get()));
[B]  1737      sinks.back()->AddOutput(maps.AppendMap(), source->munger.get());
[ ]  1738      // We handle the kInputFiles data source internally, without handing it off
[ ]  1739      // to the file format implementation.  This seems slightly simpler, since
[ ]  1740      // the file format has to deal with armembers too.
[B]  1741      if (source->effective_source == DataSource::kInputFiles) {
[ ]  1742        filename_sink_ptrs.push_back(sinks.back().get());
[B]  1743      } else {
[B]  1744        sink_ptrs.push_back(sinks.back().get());
[B]  1745      }
[B]  1746    }
[ ]  1747  
[B]  1748    std::unique_ptr<ObjectFile> debug_file;
[B]  1749    std::string build_id = file->GetBuildId();
[B]  1750    if (!build_id.empty()) { <-- BLOCKER
[W]  1751      auto iter = debug_files_.find(build_id);
[W]  1752      if (iter != debug_files_.end()) {
[ ]  1753        debug_file = GetObjectFile(iter->second);
[ ]  1754        file->set_debug_file(debug_file.get());
[ ]  1755        out_build_ids->push_back(build_id);
[ ]  1756      }
[W]  1757    }
[ ]  1758  
[B]  1759    int64_t filesize_before =
[B]  1760        rollup->file_total() + rollup->filtered_file_total();
[B]  1761    file->ProcessFile(sink_ptrs);
[ ]  1762  
[ ]  1763    // kInputFile source: Copy the base map to the filename sink(s).
[B]  1764    for (auto sink : filename_sink_ptrs) {
[ ]  1765      maps.base_map()->vm_map.ForEachRange(
[ ]  1766          [sink](uint64_t start, uint64_t length) {
[ ]  1767            sink->AddVMRange("inputfile_vmcopier", start, length,
[ ]  1768                             sink->input_file().filename());
[ ]  1769          });
[ ]  1770      maps.base_map()->file_map.ForEachRange(
[ ]  1771          [sink](uint64_t start, uint64_t length) {
[ ]  1772            sink->AddFileRange("inputfile_filecopier",
[ ]  1773                               sink->input_file().filename(), start, length);
[ ]  1774          });
[ ]  1775    }
[ ]  1776  
[B]  1777    maps.ComputeRollup(rollup);
[ ]  1778  
[ ]  1779    // The ObjectFile implementation must guarantee this.
[B]  1780    int64_t filesize =
[B]  1781        rollup->file_total() + rollup->filtered_file_total() - filesize_before;
[B]  1782    (void)filesize;
[B]  1783    assert(filesize == file->file_data().data().size());
[ ]  1784  
[B]  1785    if (verbose_level > 0 || options_.dump_raw_map()) {
[ ]  1786      printf("Maps for %s:\n\n", filename.c_str());
[ ]  1787      if (show != ShowDomain::kShowVM) {
[ ]  1788        printf("FILE MAP:\n");
[ ]  1789        maps.PrintFileMaps();
[ ]  1790      }
[ ]  1791      if (show != ShowDomain::kShowFile) {
[ ]  1792        printf("VM MAP:\n");
[ ]  1793        maps.PrintVMMaps();
[ ]  1794      }
[ ]  1795    }
[B]  1796  }

--- Caller (1 hop): bloaty.cc:bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::$_0::operator()(bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::PerThreadData*) const (/src/bloaty/src/bloaty.cc:1822-1831, calls bloaty::Bloaty::ScanAndRollupFile(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::Rollup*, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*) const at line 1826) (full body — short) ---
[B]  1822          [this, &index, &filenames](PerThreadData* data) {
[B]  1823            try {
[B]  1824              int j;
[B]  1825              while (index.TryGetNext(&j)) {
[B]  1826                ScanAndRollupFile(filenames[j], &data->rollup, &data->build_ids); <-- CALL
[B]  1827              }
[B]  1828            } catch (const bloaty::Error& e) {
[B]  1829              index.Abort(e.what());
[B]  1830            }
[B]  1831          },

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  bloaty.cc:bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::$_0::operator()(bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::PerThreadData*) const  (/src/bloaty/src/bloaty.cc:1822-1831, calls bloaty::Bloaty::ScanAndRollupFile(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::Rollup*, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*) const at line 1826)
hop 3  bloaty::Bloaty::ScanAndRollup(bloaty::Options const&, bloaty::RollupOutput*)  (/src/bloaty/src/bloaty.cc:1854-1911, calls bloaty.cc:bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::$_0::operator()(bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::PerThreadData*) const at line 1869)
hop 4  bloaty::BloatyDoMain(bloaty::Options const&, bloaty::InputFileFactory const&, bloaty::RollupOutput*)  (/src/bloaty/src/bloaty.cc:2233-2278, calls bloaty::Bloaty::ScanAndRollup(bloaty::Options const&, bloaty::RollupOutput*) at line 2274)
hop 5  bloaty::BloatyMain(bloaty::Options const&, bloaty::InputFileFactory const&, bloaty::RollupOutput*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >*)  (/src/bloaty/src/bloaty.cc:2281-2289, calls bloaty::BloatyDoMain(bloaty::Options const&, bloaty::InputFileFactory const&, bloaty::RollupOutput*) at line 2283)
hop 6  bloaty::RunBloaty(bloaty::InputFileFactory const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)  (/src/bloaty/tests/fuzz_target.cc:51-58, calls bloaty::BloatyMain(bloaty::Options const&, bloaty::InputFileFactory const&, bloaty::RollupOutput*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >*) at line 57)
hop 7  LLVMFuzzerTestOneInput  (/src/bloaty/tests/fuzz_target.cc:62-75, calls bloaty::RunBloaty(bloaty::InputFileFactory const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) at line 67)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     305      1560  bloaty::NameMunger::Munge[abi:cxx11](std::basic_string_view<char, std::char_traits<char> >) const  (/src/bloaty/src/bloaty.cc:210-221)
     305      1560  bloaty::RangeSink::ContainsVerboseFileOffset(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1096-1100)
     305      1560  bloaty::RangeSink::IsVerboseForFileRange(unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1133-1162)
     305      1560  bloaty::RangeSink::AddFileRange(char const*, std::basic_string_view<char, std::char_traits<char> >, unsigned long, unsigned long)  (/src/bloaty/src/bloaty.cc:1169-1190)
      42       444  bloaty::CheckedAdd(long*, long)  (/src/bloaty/src/bloaty.cc:122-136)
      42       444  bloaty::Rollup::AddInternal(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, unsigned long, unsigned long, bool)  (/src/bloaty/src/bloaty.cc:337-375)
     153       502  bloaty::Rollup::Rollup()  (/src/bloaty/src/bloaty.cc:251-251)
      42       356  bloaty::Rollup::Percent(long, long)  (/src/bloaty/src/bloaty.cc:377-389)
      21       222  bloaty::Rollup::AddSizes(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, unsigned long, bool)  (/src/bloaty/src/bloaty.cc:259-262)
      21       222  bloaty::DualMaps::ComputeRollup(bloaty::Rollup*)::{lambda(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, unsigned long, unsigned long)#2}::operator()(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, unsigned long, unsigned long) const  (/src/bloaty/src/bloaty.cc:1651-1653)
      33       220  bloaty::Rollup::CreateRows(bloaty::RollupRow*, bloaty::Rollup const*, bloaty::Options const&, bool) const  (/src/bloaty/src/bloaty.cc:398-438)
      33       220  bloaty::Rollup::SortAndAggregateRows(bloaty::RollupRow*, bloaty::Rollup const*, bloaty::Options const&, bool) const  (/src/bloaty/src/bloaty.cc:444-575)
      12        42  bloaty::Rollup::CreateRollupOutput(bloaty::Options const&, bloaty::RollupOutput*) const  (/src/bloaty/src/bloaty.cc:265-268)
      12        42  bloaty::Rollup::CreateDiffModeRollupOutput(bloaty::Rollup*, bloaty::Options const&, bloaty::RollupOutput*) const  (/src/bloaty/src/bloaty.cc:271-281)
      12        42  bloaty::DualMaps::ComputeRollup(bloaty::Rollup*)  (/src/bloaty/src/bloaty.cc:1640-1654)
... (3 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=4  bloaty::BloatyDoMain(bloaty::Options const&, bloaty::InputFileFactory const&, bloaty::RollupOutput*)  (/src/bloaty/src/bloaty.cc:2233-2278) ---
  d=4   L2236  T=0 F=54  T=0 F=120  if (options.filename_size() == 0) {
  d=4   L2240  T=0 F=54  T=0 F=120  if (options.max_rows_per_level() < 1) {
  d=4   L2244  T=54 F=54  T=120 F=120  for (auto& filename : options.filename()) {
  d=4   L2248  T=0 F=54  T=0 F=120  for (auto& base_filename : options.base_filename()) {
  d=4   L2252  T=0 F=54  T=0 F=120  for (auto& debug_filename : options.debug_filename()) {
  d=4   L2256  T=0 F=54  T=0 F=120  for (const auto& custom_data_source : options.custom_data...
  d=4   L2260  T=54 F=54  T=120 F=120  for (const auto& data_source : options.data_source()) {
  d=4   L2264  T=0 F=54  T=0 F=120  if (options.has_source_filter()) {
  d=4   L2273  T=54 F=0  T=120 F=0  if (options.data_source_size() > 0) {
--- d=3  bloaty::Bloaty::ScanAndRollup(bloaty::Options const&, bloaty::RollupOutput*)  (/src/bloaty/src/bloaty.cc:1854-1911) ---
  d=3   L1855  T=0 F=54  T=0 F=120  if (input_files_.empty()) {
  d=3   L1859  T=54 F=54  T=120 F=120  for (const auto& name : source_names_) {
  d=3   L1866  T=54 F=54  T=120 F=120  for (const auto& file_info : input_files_) {
  d=3   L1871  T=0 F=54  T=0 F=120  if (!base_files_.empty()) {
  d=3   L1884  T=0 F=54  T=0 F=120  for (const auto& build_id : build_ids) {
  d=3   L1889  T=0 F=54  T=0 F=120  if (!debug_files_.empty()) {
--- d=2  bloaty.cc:bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::$_0::operator()(bloaty::Bloaty::ScanAndRollupFiles(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bloaty::Rollup*) const::PerThreadData*) const  (/src/bloaty/src/bloaty.cc:1822-1831) ---
  d=2   L1825  T=54 F=54  T=120 F=120  while (index.TryGetNext(&j)) {
--- d=1  bloaty::Bloaty::ScanAndRollupFile(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bloaty::Rollup*, std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*) const  (/src/bloaty/src/bloaty.cc:1718-1796) ---
  d=1   L1733  T=54 F=54  T=120 F=120  for (auto source : sources_) {
  d=1   L1741  T=0 F=54  T=0 F=120  if (source->effective_source == DataSource::kInputFiles) {
  d=1   L1750  T=54 F=0  T=0 F=120  if (!build_id.empty()) {  <-- BLOCKER
  d=1   L1752  T=0 F=54  T=0 F=0  if (iter != debug_files_.end()) {
  d=1   L1764  T=0 F=54  T=0 F=120  for (auto sink : filename_sink_ptrs) {
  d=1   L1785  T=0 F=12  T=0 F=42  if (verbose_level > 0 || options_.dump_raw_map()) {
  d=1   L1785  T=0 F=12  T=0 F=42  if (verbose_level > 0 || options_.dump_raw_map()) {

[off-chain: 72 additional divergent branches across 20 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=dcb7ff92fe9d1ffa, size=111 bytes, fuzzer=cmplog, trial=1, discovered_at=239s, mutation_op=BytesDeleteMutator,DwordAddMutator):
  0000: ce fa ed fe 02 01 01 20 20 20 01 b0 48 13 5f 5f   .......   ..H.__
  0010: 02 00 00 00 30 30 01 13 5f 5f 01 00 22 00 00 00   ....00..__.."...
  0020: 2b 00 00 00 ff f9 01 00 00 21 3c 69 6e 66 68 3e   +........!<infh>
  0030: 0a 00 63 73 69 2e 49 73 07 01 4b 07 00 00 20 16   ..csi.Is..K... .
Seed 2 (id=eca8ca75a45aa03b, size=111 bytes, fuzzer=cmplog, trial=1, discovered_at=1827s, mutation_op=TokenReplace):
  0000: ce fa ed fe 02 01 01 20 20 20 01 b0 48 13 5f 5f   .......   ..H.__
  0010: 01 00 00 00 30 30 01 13 5f 5f 01 00 1b 00 00 00   ....00..__......
  0020: 18 00 00 00 ff f9 01 00 00 21 3c 72 61 63 68 3e   .........!<rach>
  0030: 0a 00 61 73 66 2e 49 73 07 01 4b 07 00 00 20 16   ..asf.Is..K... .
Seed 3 (id=6ac11a9dca2495f8, size=123 bytes, fuzzer=cmplog, trial=1, discovered_at=6701s, mutation_op=TokenReplace,ByteAddMutator,ByteInterestingMutator,BytesInsertMutator,BytesDeleteMutator,QwordAddMutator):
  0000: cf fa ed fe 48 13 5f 5f 02 00 00 00 02 01 01 20   ....H.__....... 
  0010: 01 00 00 00 48 13 00 20 20 03 07 00 00 30 01 13   ....H..  ....0..
  0020: 1b 00 00 00 18 00 00 00 00 00 64 00 ff 00 64 00   ..........d...d.
  0030: ff f9 01 00 00 ce fa 72 68 24 68 3e 1b 07 00 00   .......rh$h>....
Seed 4 (id=80d8c7d46eca304a, size=127 bytes, fuzzer=cmplog, trial=1, discovered_at=10818s, mutation_op=DwordAddMutator,ByteIncMutator,ByteFlipMutator,ByteAddMutator,ByteInterestingMutator):
  0000: ce fa ed fe 02 01 01 20 20 20 01 b0 48 13 5f 5f   .......   ..H.__
  0010: 03 00 00 00 30 30 01 13 5f 5f 01 00 1b 00 00 00   ....00..__......
  0020: 18 00 00 00 ff f9 01 90 99 21 5d 72 61 77 68 3e   .........!]rawh>
  0030: 0a 0a 61 63 1e 00 00 00 18 00 00 00 00 90 24 16   ..ac..........$.
Seed 5 (id=40a17ee7fff2f42d, size=125 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=11236s, mutation_op=ByteFlipMutator,CrossoverInsertMutator,ByteNegMutator,BytesSetMutator,ByteRandMutator,BytesExpandMutator,BytesExpandMutator):
  0000: ce fa ed fe 7f 95 e8 e0 0a 16 18 24 24 20 20 20   ...........$$   
  0010: 03 00 00 00 00 00 00 00 ff ff ff 00 1b 00 00 00   ................
  0020: 18 00 00 00 07 03 1b 00 00 24 dc 20 20 00 00 18   .........$.  ...
  0030: 20 01 00 20 20 20 20 20 20 00 00 00 00 00 00 00    ..      .......

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0002812e1528da92, size=101 bytes, fuzzer=value_profile, trial=1, discovered_at=82s, mutation_op=BytesRandSetMutator,BytesSetMutator):
  0000: 00 61 73 6d 7b 45 4c 46 01 01 46 01 01 17 04 00   .asm{ELF..F.....
  0010: 00 28 20 00 00 00 00 00 00 00 20 23 20 00 00 61   .( ....... # ..a
  0020: 00 00 00 00 00 1f 20 a5 20 20 00 00 00 20 00 00   ...... .  ... ..
  0030: 00 00 00 00 00 00 00 00 00 00 00 20 01 01 01 01   ........... ....
Seed 2 (id=001b86721a62221a, size=59 bytes, fuzzer=value_profile, trial=1, discovered_at=106s, mutation_op=DwordAddMutator,ByteRandMutator,BitFlipMutator):
  0000: 00 61 73 6d 00 e8 e9 2d 00 25 20 00 fe ff ff ff   .asm...-.% .....
  0010: 7f 00 00 00 c1 c1 dd 88 88 88 88 cf 00 00 01 00   ................
  0020: 0c 20 73 ff 01 00 20 b5 b5 20 10 20 00 04 06 88   . s... .. . ....
  0030: 88 00 00 01 06 06 00 00 ff 00 02                  ...........
Seed 3 (id=00165229b536b473, size=54 bytes, fuzzer=value_profile, trial=1, discovered_at=209s, mutation_op=ByteFlipMutator,ByteAddMutator):
  0000: 00 61 73 6d 00 20 20 ff 02 24 1f 00 00 00 00 00   .asm.  ..$......
  0010: 00 02 24 7f 00 00 00 01 02 00 ff 02 02 02 02 02   ..$.............
  0020: 02 02 02 02 1a fd 20 4a b5 25 b6 20 00 04 01 06   ...... J.%. ....
  0030: 06 00 00 ff 00 02                                 ......
Seed 4 (id=00050eebd8570fd9, size=55 bytes, fuzzer=naive, trial=1, discovered_at=274s, mutation_op=BytesDeleteMutator):
  0000: 00 61 73 6d fe 00 6d 00 01 01 01 01 01 01 01 01   .asm..m.........
  0010: 00 80 40 13 07 ff ff c0 c0 c0 a9 c0 c0 c0 13 07   ..@.............
  0020: ff ff c0 c0 e1 ff 01 01 00 07 01 01 01 01 01 01   ................
  0030: 01 01 01 01 00 01 00                              .......
Seed 5 (id=004787abb6df541c, size=45 bytes, fuzzer=naive, trial=1, discovered_at=503s, mutation_op=QwordAddMutator,TokenReplace,CrossoverReplaceMutator,ByteDecMutator,DwordInterestingMutator):
  0000: 00 61 73 6d fe 00 6d 01 01 01 ff 02 20 e8 03 00   .asm..m..... ...
  0010: 00 01 01 01 7f ff ff ff 01 01 01 01 01 01 01 01   ................
  0020: 01 fe ff ff ff ff ff ff 3f 00 00 00 00            ........?....


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  ce(.)x7 cf(.)x2                     00(.)x19 21(!)x1                    DIFFER
   0x0001  fa(.)x9                             61(a)x19 3c(<)x1                    DIFFER
   0x0002  ed(.)x9                             73(s)x19 61(a)x1                    DIFFER
   0x0003  fe(.)x9                             6d(m)x19 72(r)x1                    DIFFER
   0x0004  02(.)x6 48(H)x2 7f(.)x1             00(.)x8 fe(.)x7 7b({)x2 be(.)x2 +1u  DIFFER
   0x0005  01(.)x5 13(.)x2 95(.)x1 02(.)x1     00(.)x7 20( )x4 45(E)x2 e8(.)x1 +6u  DIFFER
   0x0006  01(.)x5 5f(_)x2 e8(.)x1 02(.)x1     6d(m)x6 20( )x4 4c(L)x2 00(.)x2 +6u  DIFFER
   0x0007  20( )x5 5f(_)x2 e0(.)x1 02(.)x1     01(.)x7 ff(.)x3 00(.)x3 46(F)x2 +5u  PARTIAL
   0x0008  20( )x5 02(.)x3 0a(.)x1             01(.)x13 02(.)x4 00(.)x2 8a(.)x1    PARTIAL
   0x0009  20( )x5 00(.)x2 16(.)x1 02(.)x1     01(.)x10 24($)x5 80(.)x2 25(%)x1 +2u  PARTIAL
   0x000a  01(.)x5 00(.)x2 18(.)x1 02(.)x1     ff(.)x6 e0(.)x3 46(F)x2 20( )x2 +6u  PARTIAL
   0x000b  b0(.)x5 00(.)x2 24($)x1 02(.)x1     02(.)x7 00(.)x6 01(.)x3 04(.)x1 +3u  PARTIAL
   0x000c  48(H)x5 02(.)x3 24($)x1             00(.)x6 20( )x6 01(.)x3 38(8)x2 +3u  DIFFER
   0x000d  13(.)x5 01(.)x2 20( )x1 02(.)x1     00(.)x6 0f(.)x4 17(.)x2 01(.)x2 +6u  PARTIAL
   0x000f  5f(_)x3 20( )x3 00(.)x2 02(.)x1     00(.)x7 01(.)x7 ff(.)x2 77(w)x1 +3u  PARTIAL
   0x0010  01(.)x3 02(.)x2 03(.)x2 04(.)x2     00(.)x11 80(.)x2 01(.)x2 7f(.)x1 +4u  PARTIAL
   0x0011  00(.)x9                             01(.)x7 00(.)x3 28(()x2 02(.)x2 +4u  PARTIAL
   0x0012  00(.)x9                             01(.)x6 00(.)x5 20( )x2 24($)x1 +5u  PARTIAL
   0x0013  00(.)x9                             00(.)x8 ff(.)x3 01(.)x2 0b(.)x2 +4u  PARTIAL
   0x0014  30(0)x6 48(H)x2 00(.)x1             00(.)x4 7f(.)x3 40(@)x2 01(.)x2 +8u  PARTIAL
   0x0015  30(0)x6 13(.)x2 00(.)x1             00(.)x8 ff(.)x4 c1(.)x1 01(.)x1 +5u  PARTIAL
   0x0016  01(.)x6 00(.)x3                     00(.)x10 ff(.)x4 dd(.)x1 03(.)x1 +3u  PARTIAL
   0x0017  13(.)x6 20( )x2 00(.)x1             00(.)x5 01(.)x3 ff(.)x2 02(.)x2 +7u  PARTIAL
   0x0018  5f(_)x5 20( )x2 ff(.)x1 00(.)x1     00(.)x5 01(.)x3 fe(.)x2 88(.)x1 +8u  PARTIAL
   0x0019  5f(_)x5 03(.)x2 ff(.)x1 00(.)x1     00(.)x5 08(.)x2 80(.)x2 ff(.)x2 +8u  PARTIAL
   0x001a  01(.)x5 07(.)x2 ff(.)x1 00(.)x1     00(.)x6 ff(.)x2 01(.)x2 20( )x1 +8u  PARTIAL
   0x001b  00(.)x9                             00(.)x5 01(.)x4 02(.)x2 03(.)x2 +6u  PARTIAL
   0x001c  1b(.)x6 00(.)x2 22(")x1             00(.)x4 01(.)x4 fe(.)x2 ff(.)x2 +7u  PARTIAL
   0x001d  00(.)x6 30(0)x2 13(.)x1             00(.)x9 01(.)x2 06(.)x2 ff(.)x2 +4u  PARTIAL
   0x001e  00(.)x6 01(.)x2 1f(.)x1             00(.)x4 01(.)x4 10(.)x3 02(.)x2 +6u  PARTIAL
   0x001f  00(.)x6 13(.)x2 ad(.)x1             00(.)x6 02(.)x3 01(.)x2 61(a)x1 +7u  PARTIAL
   0x0020  18(.)x6 1b(.)x2 2b(+)x1             00(.)x7 01(.)x4 0c(.)x1 02(.)x1 +6u  DIFFER
   0x0021  00(.)x9                             00(.)x7 03(.)x2 01(.)x2 20( )x1 +7u  PARTIAL
   0x0022  00(.)x9                             00(.)x6 ff(.)x3 01(.)x2 73(s)x1 +7u  PARTIAL
   0x0023  00(.)x9                             00(.)x6 01(.)x3 ff(.)x2 02(.)x1 +7u  PARTIAL
   0x0024  ff(.)x6 18(.)x2 07(.)x1             01(.)x6 00(.)x3 1a(.)x2 ff(.)x2 +6u  PARTIAL
   0x0025  f9(.)x6 00(.)x2 03(.)x1             00(.)x6 ff(.)x4 01(.)x3 1f(.)x1 +5u  PARTIAL
   0x0026  01(.)x6 00(.)x2 1b(.)x1             00(.)x5 20( )x3 01(.)x2 ff(.)x1 +8u  PARTIAL
   0x0027  00(.)x8 90(.)x1                     01(.)x5 00(.)x3 02(.)x2 a5(.)x1 +8u  PARTIAL
   0x0028  00(.)x8 99(.)x1                     00(.)x4 01(.)x3 20( )x2 b5(.)x2 +7u  PARTIAL
   ... (17 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/bloaty_13.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 13,
  "target": "bloaty",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S), value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 13 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 13 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 13 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).