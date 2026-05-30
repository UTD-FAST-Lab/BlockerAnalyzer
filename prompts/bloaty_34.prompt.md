==== BLOCKER ====
Target: bloaty
Branch ID: 34
Location: /src/bloaty/src/elf.cc:475:5
Enclosing function: elf.cc:bloaty::(anonymous namespace)::ElfFile::Initialize()
Source line:     default:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    0       10          0  REFERENCE
value_profile_cmplog             5        5          0  REFERENCE
naive_ctx                        0       10          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        3        7          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         5        5          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=7.80h  loser=23.40h
  avg hitcount on branch: winner=19  loser=1
  prob_div=0.70  dur_div=15.60h  hit_div=18
  subject-level: delta_AUC=26255160.0  p_AUC=0.0002  delta_Final=523.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/bloaty/34/{W,L}/branch_coverage_show.txt

--- Enclosing function: elf.cc:bloaty::(anonymous namespace)::ElfFile::Initialize() (/src/bloaty/src/elf.cc:444-520) ---
[ ]   442  }
[ ]   443  
[B]   444  bool ElfFile::Initialize() {
[B]   445    if (data_.size() < EI_NIDENT) {
[ ]   446      return false;
[ ]   447    }
[ ]   448  
[B]   449    unsigned char ident[EI_NIDENT];
[B]   450    memcpy(ident, data_.data(), EI_NIDENT);
[ ]   451  
[B]   452    if (memcmp(ident, "\177ELF", 4) != 0) {
[ ]   453      // Not an ELF file.
[W]   454      return false;
[W]   455    }
[ ]   456  
[B]   457    switch (ident[EI_CLASS]) {
[B]   458      case ELFCLASS32:
[B]   459        is_64bit_ = false;
[B]   460        break;
[B]   461      case ELFCLASS64:
[B]   462        is_64bit_ = true;
[B]   463        break;
[ ]   464      default:
[ ]   465        THROWF("unexpected ELF class: $0", ident[EI_CLASS]);
[B]   466    }
[ ]   467  
[B]   468    switch (ident[EI_DATA]) {
[L]   469      case ELFDATA2LSB:
[L]   470        is_native_endian_ = GetMachineEndian() == Endian::kLittle;
[L]   471        break;
[L]   472      case ELFDATA2MSB:
[L]   473        is_native_endian_ = GetMachineEndian() == Endian::kBig;
[L]   474        break;
[W]   475      default: <-- BLOCKER
[W]   476        THROWF("unexpected ELF data: $0", ident[EI_DATA]);
[B]   477    }
[ ]   478  
[L]   479    absl::string_view range;
[L]   480    ReadStruct<Elf32_Ehdr>(entire_file(), 0, EhdrMunger(), &range, &header_);
[ ]   481  
[L]   482    Section section0;
[L]   483    bool has_section0 = 0;
[ ]   484  
[ ]   485    // ELF extensions: if certain fields overflow, we have to find their true data
[ ]   486    // from elsewhere.  For more info see:
[ ]   487    // https://docs.oracle.com/cd/E19683-01/817-3677/chapter6-94076/index.html
[L]   488    if (header_.e_shoff > 0 &&
[L]   489        data_.size() > (header_.e_shoff + header_.e_shentsize)) {
[L]   490      section_count_ = 1;
[L]   491      ReadSection(0, &section0);
[L]   492      has_section0 = true;
[L]   493    }
[ ]   494  
[L]   495    section_count_ = header_.e_shnum;
[L]   496    section_string_index_ = header_.e_shstrndx;
[ ]   497  
[L]   498    if (section_count_ == 0 && has_section0) {
[L]   499      section_count_ = section0.header().sh_size;
[L]   500    }
[ ]   501  
[L]   502    if (section_string_index_ == SHN_XINDEX && has_section0) {
[L]   503      section_string_index_ = section0.header().sh_link;
[L]   504    }
[ ]   505  
[L]   506    header_region_ = GetRegion(0, header_.e_ehsize);
[L]   507    section_headers_ = GetRegion(header_.e_shoff,
[L]   508                                 CheckedMul(header_.e_shentsize, section_count_));
[L]   509    segment_headers_ = GetRegion(
[L]   510        header_.e_phoff, CheckedMul(header_.e_phentsize, header_.e_phnum));
[ ]   511  
[L]   512    if (section_count_ > 0) {
[L]   513      ReadSection(section_string_index_, &section_name_table_);
[L]   514      if (section_name_table_.header().sh_type != SHT_STRTAB) {
[L]   515        THROW("section string index pointed to non-strtab");
[L]   516      }
[L]   517    }
[ ]   518  
[L]   519    return true;
[L]   520  }

--- No 1-hop callers of elf.cc:bloaty::(anonymous namespace)::ElfFile::Initialize() fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0  23000000  elf.cc:unsigned short bloaty::(anonymous namespace)::NullFunc::operator()<unsigned short>(unsigned short)  (/src/bloaty/src/elf.cc:45-45)
       0  23000000  elf.cc:unsigned int bloaty::(anonymous namespace)::NullFunc::operator()<unsigned int>(unsigned int)  (/src/bloaty/src/elf.cc:45-45)
       0  23000000  elf.cc:unsigned char bloaty::(anonymous namespace)::NullFunc::operator()<unsigned char>(unsigned char)  (/src/bloaty/src/elf.cc:45-45)
       0  23000000  elf.cc:int bloaty::(anonymous namespace)::NullFunc::operator()<int>(int)  (/src/bloaty/src/elf.cc:45-45)
       0   7690000  elf.cc:bloaty::(anonymous namespace)::ElfFile::Segment::header() const  (/src/bloaty/src/elf.cc:86-86)
       0   6340000  elf.cc:bloaty::(anonymous namespace)::ElfFile::is_64bit() const  (/src/bloaty/src/elf.cc:165-165)
       0   3460000  elf.cc:bloaty::(anonymous namespace)::ElfFile::GetRegion(unsigned long, unsigned long) const  (/src/bloaty/src/elf.cc:179-181)
       0   3450000  elf.cc:bloaty::(anonymous namespace)::ElfFile::entire_file() const  (/src/bloaty/src/elf.cc:74-74)
       0   3450000  elf.cc:bloaty::(anonymous namespace)::ElfFile::header() const  (/src/bloaty/src/elf.cc:79-79)
       0   3450000  elf.cc:bloaty::(anonymous namespace)::ElfFile::is_native_endian() const  (/src/bloaty/src/elf.cc:166-166)
       0   3450000  elf.cc:void bloaty::(anonymous namespace)::ElfFile::ReadStruct<Elf32_Ehdr, Elf64_Ehdr, bloaty::(anonymous namespace)::EhdrMunger>(std::basic_string_view<char, std::char_traits<char> >, unsigned long, bloaty::(anonymous namespace)::EhdrMunger, std::basic_string_view<char, std::char_traits<char> >*, Elf64_Ehdr*) const  (/src/bloaty/src/elf.cc:170-172)
       0   3450000  elf.cc:void bloaty::(anonymous namespace)::ElfFile::ReadStruct<Elf32_Shdr, Elf64_Shdr, bloaty::(anonymous namespace)::ShdrMunger>(std::basic_string_view<char, std::char_traits<char> >, unsigned long, bloaty::(anonymous namespace)::ShdrMunger, std::basic_string_view<char, std::char_traits<char> >*, Elf64_Shdr*) const  (/src/bloaty/src/elf.cc:170-172)
       0   3450000  elf.cc:void bloaty::(anonymous namespace)::ElfFile::ReadStruct<Elf_Note, Elf_Note, bloaty::(anonymous namespace)::NoteMunger>(std::basic_string_view<char, std::char_traits<char> >, unsigned long, bloaty::(anonymous namespace)::NoteMunger, std::basic_string_view<char, std::char_traits<char> >*, Elf_Note*) const  (/src/bloaty/src/elf.cc:170-172)
       0   3450000  elf.cc:void bloaty::(anonymous namespace)::ElfFile::ReadStruct<Elf32_Phdr, Elf64_Phdr, bloaty::(anonymous namespace)::PhdrMunger>(std::basic_string_view<char, std::char_traits<char> >, unsigned long, bloaty::(anonymous namespace)::PhdrMunger, std::basic_string_view<char, std::char_traits<char> >*, Elf64_Phdr*) const  (/src/bloaty/src/elf.cc:170-172)
       0   3450000  elf.cc:void bloaty::(anonymous namespace)::ElfFile::ReadStruct<Elf32_Sym, Elf64_Sym, bloaty::(anonymous namespace)::SymMunger>(std::basic_string_view<char, std::char_traits<char> >, unsigned long, bloaty::(anonymous namespace)::SymMunger, std::basic_string_view<char, std::char_traits<char> >*, Elf64_Sym*) const  (/src/bloaty/src/elf.cc:170-172)
... (101 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  elf.cc:bloaty::(anonymous namespace)::ElfFile::Initialize()  (/src/bloaty/src/elf.cc:444-520) ---
  d=1   L 445  T=0 F=240  T=0 F=2220  if (data_.size() < EI_NIDENT) {
  d=1   L 452  T=180 F=60  T=0 F=2220  if (memcmp(ident, "\177ELF", 4) != 0) {
  d=1   L 458  T=24 F=36  T=1540 F=678  case ELFCLASS32:
  d=1   L 461  T=36 F=24  T=678 F=1540  case ELFCLASS64:
  d=1   L 464  T=0 F=60  T=0 F=2220  default:
  d=1   L 469  T=0 F=60  T=1980 F=240  case ELFDATA2LSB:
  d=1   L 472  T=0 F=60  T=240 F=1980  case ELFDATA2MSB:
  d=1   L 475  T=60 F=0  T=0 F=2220  default:  <-- BLOCKER
  d=1   L 488  T=0 F=0  T=905 F=1320  if (header_.e_shoff > 0 &&
  d=1   L 489  T=0 F=0  T=156 F=749  data_.size() > (header_.e_shoff + header_.e_shentsize)) {
  d=1   L 498  T=0 F=0  T=2190 F=36  if (section_count_ == 0 && has_section0) {
  d=1   L 498  T=0 F=0  T=132 F=2050  if (section_count_ == 0 && has_section0) {
  d=1   L 502  T=0 F=0  T=144 F=0  if (section_string_index_ == SHN_XINDEX && has_section0) {
  d=1   L 502  T=0 F=0  T=144 F=2080  if (section_string_index_ == SHN_XINDEX && has_section0) {
  d=1   L 512  T=0 F=0  T=54 F=2170  if (section_count_ > 0) {
  d=1   L 514  T=0 F=0  T=12 F=42  if (section_name_table_.header().sh_type != SHT_STRTAB) {

[off-chain: 75 additional divergent branches across 25 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=0989f57862fb3e41, size=64 bytes, fuzzer=cmplog, trial=1, discovered_at=0s):
  0000: 7f 45 4c 46 02 30 01 00 00 00 20 20 20 20 20 00   .ELF.0....     .
  0010: 00 00 00 00 00 00 20 20 20 20 20 20 ff ff ff ff   ......      ....
  0020: 06 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00   .@..............
  0030: 20 20 20 20 20 00 00 00 20 20 20 20 00 00 20 20        ...    ..  
Seed 2 (id=22d32f722c5c3dc7, size=64 bytes, fuzzer=cmplog, trial=1, discovered_at=0s):
  0000: 7f 45 4c 46 02 00 01 00 00 00 20 20 20 20 20 07   .ELF......     .
  0010: 00 00 00 00 00 00 30 ed 93 b0 00 00 00 00 ff ff   ......0.........
  0020: 06 00 00 00 00 00 00 00 00 00 00 00 07 00 00 00   ................
  0030: 20 20 20 20 20 00 00 00 20 20 20 20 00 00 20 20        ...    ..  
Seed 3 (id=51f1d6d54d767ae6, size=40 bytes, fuzzer=cmplog, trial=1, discovered_at=1s, mutation_op=BytesInsertCopyMutator,TokenInsert,QwordAddMutator,BytesRandInsertMutator,BytesExpandMutator,BytesDeleteMutator):
  0000: 7f 45 4c 46 02 e7 00 00 00 00 20 20 20 20 20 00   .ELF......     .
  0010: 00 00 00 00 00 00 20 25 25 25 25 25 25 25 25 25   ...... %%%%%%%%%
  0020: 25 25 25 25 25 20 20 20                           %%%%%   
Seed 4 (id=b6f55b03dcf5c04e, size=64 bytes, fuzzer=cmplog, trial=1, discovered_at=1s, mutation_op=WordAddMutator,QwordAddMutator,TokenInsert):
  0000: 7f 45 4c 46 01 00 01 00 00 02 20 20 20 20 20 07   .ELF......     .
  0010: 00 00 00 00 00 00 30 ed 93 b0 00 00 00 00 ff ff   ......0.........
  0020: 06 00 00 00 00 00 00 00 00 00 00 07 00 00 00 00   ................
  0030: 20 20 20 20 20 00 00 00 20 20 20 20 00 00 20 20        ...    ..  
Seed 5 (id=4893b768835bc108, size=64 bytes, fuzzer=cmplog, trial=1, discovered_at=12s, mutation_op=CrossoverInsertMutator,WordInterestingMutator,TokenInsert,ByteIncMutator,BytesCopyMutator,CrossoverReplaceMutator,BytesDeleteMutator):
  0000: 7f 45 4c 46 01 ff c9 9a 3b 0a 20 20 20 20 20 09   .ELF....;.     .
  0010: 00 00 00 02 00 00 24 20 20 20 20 20 ff c9 9a 3b   ......$     ...;
  0020: 08 02 02 3e 07 00 00 00 00 00 00 00 00 00 00 00   ...>............
  0030: 00 00 00 ca 9a 3b 00 00 24 24 20 20 40 be 20 20   .....;..$$  @.  

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=01a53df0ebbce533, size=88 bytes, fuzzer=naive, trial=1, discovered_at=31s, mutation_op=BytesInsertCopyMutator,ByteAddMutator,ByteFlipMutator,ByteIncMutator):
  0000: 7f 45 4c 46 01 01 01 00 f2 00 20 21 df 20 00 00   .ELF...... !. ..
  0010: 00 ff 00 00 00 00 00 00 20 20 20 21 20 00 00 00   ........   ! ...
  0020: 00 00 00 00 20 20 00 00 00 00 00 00 00 00 00 00   ....  ..........
  0030: 20 00 20 00 00 00 00 00 00 00 00 00 00 00 00 20    . ............ 
Seed 2 (id=43b1a3ff84794b7e, size=76 bytes, fuzzer=naive, trial=1, discovered_at=153s, mutation_op=BytesInsertMutator,CrossoverReplaceMutator):
  0000: 7f 45 4c 46 02 01 01 00 00 00 00 7f ff 20 20 00   .ELF.........  .
  0010: 00 00 00 00 00 00 20 20 20 20 20 20 ff 3c ff ff   ......      .<..
  0020: 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0030: 20 20 20 20 20 00 00 00 00 20 20 00 00 00 00 00        ....  .....
Seed 3 (id=040ca6fadf614081, size=192 bytes, fuzzer=naive, trial=2, discovered_at=176s, mutation_op=QwordAddMutator,ByteIncMutator,BytesRandSetMutator):
  0000: 7f 45 4c 46 01 01 01 00 00 e2 20 20 29 20 20 20   .ELF......  )   
  0010: 20 20 20 20 20 20 20 20 9c 9c 9c 00 9c 00 00 00           ........
  0020: 01 00 00 00 00 00 69 6e 66 00 00 00 00 11 00 40   ......inf......@
  0030: 00 00 00 00 69 6e 66 00 00 00 00 00 00 00 00 00   ....inf.........
Seed 4 (id=572277f94c864f43, size=111 bytes, fuzzer=naive, trial=1, discovered_at=375s, mutation_op=DwordAddMutator,BytesRandInsertMutator,BytesInsertCopyMutator,BytesCopyMutator,BytesRandSetMutator,DwordAddMutator,BytesRandSetMutator):
  0000: 7f 45 4c 46 01 01 01 06 f2 00 20 21 21 1a 1a 1a   .ELF...... !!...
  0010: 1a 1a 01 f6 00 ed f2 00 20 20 fe 20 20 00 00 00   ........  .  ...
  0020: 11 00 00 00 00 00 00 00 00 00 00 00 ff 00 00 00   ................
  0030: 00 20 df 20 20 00 00 00 11 00 00 00 00 00 00 00   . .  ...........
Seed 5 (id=0051dc042a9f67a8, size=142 bytes, fuzzer=naive, trial=2, discovered_at=758s, mutation_op=BytesExpandMutator,TokenReplace,BytesRandInsertMutator):
  0000: 7f 45 4c 46 02 02 ff 00 00 00 ff 00 00 00 00 00   .ELF............
  0010: 00 40 00 00 00 00 00 00 a1 1d 20 20 20 20 00 01   .@........    ..
  0020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 08   ................
  0030: 20 20 1f 00 00 00 00 ef 00 00 00 00 0e 0e 0e 0e     ..............


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  7f(.)x5 21(!)x5                     7f(.)x32                            PARTIAL
   0x0001  45(E)x5 3c(<)x5                     45(E)x32                            PARTIAL
   0x0002  4c(L)x5 61(a)x5                     4c(L)x32                            PARTIAL
   0x0003  46(F)x5 72(r)x5                     46(F)x32                            PARTIAL
   0x0004  63(c)x5 02(.)x3 01(.)x2             01(.)x24 02(.)x8                    PARTIAL
   0x0005  68(h)x5 00(.)x2 30(0)x1 e7(.)x1 +1u  01(.)x27 02(.)x5                    DIFFER
   0x0006  3e(>)x5 01(.)x3 00(.)x1 c9(.)x1     01(.)x30 ff(.)x1 00(.)x1            PARTIAL
   0x0007  0a(.)x5 00(.)x4 9a(.)x1             00(.)x22 06(.)x6 75(u)x2 01(.)x1 +1u  PARTIAL
   0x0008  20( )x5 00(.)x4 3b(;)x1             00(.)x17 f2(.)x9 75(u)x2 09(.)x2 +2u  PARTIAL
   0x0009  2f(/)x5 00(.)x3 02(.)x1 0a(.)x1     00(.)x19 e2(.)x9 ff(.)x2 75(u)x1 +1u  PARTIAL
   0x000a  20( )x5 6c(l)x5                     20( )x13 df(.)x4 00(.)x3 ff(.)x3 +8u  PARTIAL
   0x000b  20( )x10                            20( )x15 21(!)x6 00(.)x3 ff(.)x2 +6u  PARTIAL
   0x000c  20( )x10                            20( )x9 df(.)x6 ff(.)x2 29())x2 +11u  PARTIAL
   0x000d  20( )x5 c1(.)x5                     20( )x16 00(.)x5 8a(.)x2 df(.)x2 +7u  PARTIAL
   0x000e  20( )x5 88(.)x5                     20( )x18 00(.)x6 1a(.)x1 75(u)x1 +6u  PARTIAL
   0x000f  ff(.)x5 00(.)x2 07(.)x2 09(.)x1     00(.)x16 20( )x6 03(.)x2 1a(.)x1 +7u  PARTIAL
   0x0010  00(.)x5 ff(.)x5                     00(.)x14 20( )x7 01(.)x5 1a(.)x1 +5u  PARTIAL
   0x0011  00(.)x5 ff(.)x5                     00(.)x15 20( )x6 ff(.)x2 46(F)x2 +6u  PARTIAL
   0x0012  00(.)x5 63(c)x5                     00(.)x14 20( )x8 01(.)x5 80(.)x1 +4u  PARTIAL
   0x0013  68(h)x5 00(.)x4 02(.)x1             00(.)x12 20( )x9 f4(.)x4 f6(.)x3 +4u  PARTIAL
   0x0014  00(.)x5 3e(>)x5                     00(.)x21 20( )x8 ff(.)x1 2d(-)x1 +1u  PARTIAL
   0x0015  00(.)x5 71(q)x3 8f(.)x2             00(.)x16 20( )x8 ed(.)x3 ff(.)x2 +3u  PARTIAL
   0x0016  71(q)x5 20( )x2 30(0)x2 24($)x1     20( )x13 00(.)x8 f2(.)x7 2d(-)x1 +3u  PARTIAL
   0x0017  71(q)x5 20( )x2 ed(.)x2 25(%)x1     00(.)x14 20( )x14 2d(-)x1 01(.)x1 +2u  PARTIAL
   0x0018  71(q)x5 20( )x2 93(.)x2 25(%)x1     20( )x13 9c(.)x7 00(.)x5 a1(.)x1 +6u  PARTIAL
   0x0019  71(q)x5 20( )x2 b0(.)x2 25(%)x1     20( )x14 9c(.)x9 00(.)x4 1d(.)x1 +4u  PARTIAL
   0x001a  00(.)x7 20( )x2 25(%)x1             20( )x9 9c(.)x7 df(.)x6 00(.)x6 +4u  PARTIAL
   0x001b  80(.)x5 20( )x2 00(.)x2 25(%)x1     20( )x14 00(.)x12 21(!)x1 7f(.)x1 +4u  PARTIAL
   0x001c  71(q)x5 ff(.)x2 00(.)x2 25(%)x1     20( )x10 9c(.)x8 ff(.)x5 00(.)x5 +4u  PARTIAL
   0x001e  00(.)x5 ff(.)x3 25(%)x1 9a(.)x1     00(.)x26 ff(.)x5 7f(.)x1            PARTIAL
   0x001f  df(.)x5 ff(.)x3 25(%)x1 3b(;)x1     00(.)x25 ff(.)x5 01(.)x1 20( )x1    PARTIAL
   0x0020  df(.)x5 06(.)x3 25(%)x1 08(.)x1     00(.)x12 06(.)x5 01(.)x5 11(.)x4 +6u  PARTIAL
   0x0021  65(e)x5 00(.)x2 40(@)x1 25(%)x1 +1u  00(.)x32                            PARTIAL
   0x0022  6c(l)x5 00(.)x3 25(%)x1 02(.)x1     00(.)x32                            PARTIAL
   0x0023  20( )x5 00(.)x3 25(%)x1 3e(>)x1     00(.)x30 01(.)x2                    PARTIAL
   0x0024  20( )x5 00(.)x3 25(%)x1 07(.)x1     00(.)x27 20( )x2 01(.)x1 08(.)x1 +1u  PARTIAL
   0x0025  2d(-)x5 00(.)x4 20( )x1             00(.)x27 20( )x2 01(.)x2 ff(.)x1    PARTIAL
   0x0026  0a(.)x5 00(.)x4 20( )x1             00(.)x26 69(i)x4 4d(M)x1 ff(.)x1    PARTIAL
   0x0027  d0(.)x5 00(.)x4 20( )x1             00(.)x22 6e(n)x5 10(.)x1 08(.)x1 +3u  PARTIAL
   0x0028  be(.)x5 00(.)x4                     00(.)x21 66(f)x4 0f(.)x1 08(.)x1 +5u  PARTIAL
   ... (23 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/bloaty_34.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 34,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 34 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 34 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 34 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).