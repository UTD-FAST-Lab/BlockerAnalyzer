==== BLOCKER ====
Target: bloaty
Branch ID: 59
Location: /src/bloaty/src/elf.cc:798:5
Enclosing function: elf.cc:bloaty::(anonymous namespace)::ElfMachineToCapstone(unsigned short, cs_arch*, cs_mode*)
Source line:     case EM_AARCH64:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    5        5          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     2        8          0  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        5        5          0  REFERENCE
fast                             4        6          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=1.60h  loser=23.70h
  avg hitcount on branch: winner=33  loser=0
  prob_div=1.00  dur_div=22.10h  hit_div=33
  subject-level: delta_AUC=26255160.0  p_AUC=0.0002  delta_Final=523.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/bloaty/59/{W,L}/branch_coverage_show.txt

--- Enclosing function: elf.cc:bloaty::(anonymous namespace)::ElfMachineToCapstone(unsigned short, cs_arch*, cs_mode*) (/src/bloaty/src/elf.cc:781-830) ---
[ ]   779  
[ ]   780  static bool ElfMachineToCapstone(Elf64_Half e_machine, cs_arch* arch,
[B]   781                                   cs_mode* mode) {
[B]   782    switch (e_machine) {
[L]   783      case EM_386:
[L]   784        *arch = CS_ARCH_X86;
[L]   785        *mode = CS_MODE_32;
[L]   786        return true;
[ ]   787      case EM_X86_64:
[ ]   788        *arch = CS_ARCH_X86;
[ ]   789        *mode = CS_MODE_64;
[ ]   790        return true;
[ ]   791  
[ ]   792      // These aren't tested, but we include them on the off-chance
[ ]   793      // that it will work.
[ ]   794      case EM_ARM:
[ ]   795        *arch = CS_ARCH_ARM;
[ ]   796        *mode = CS_MODE_LITTLE_ENDIAN;
[ ]   797        return true;
[W]   798      case EM_AARCH64: <-- BLOCKER
[W]   799        *arch = CS_ARCH_ARM64;
[W]   800        *mode = CS_MODE_ARM;
[W]   801        return true;
[ ]   802      case EM_MIPS:
[ ]   803        *arch = CS_ARCH_MIPS;
[ ]   804        return true;
[ ]   805      case EM_PPC:
[ ]   806        *arch = CS_ARCH_PPC;
[ ]   807        *mode = CS_MODE_32;
[ ]   808        return true;
[ ]   809      case EM_PPC64:
[ ]   810        *arch = CS_ARCH_PPC;
[ ]   811        *mode = CS_MODE_64;
[ ]   812        return true;
[ ]   813      case EM_SPARC:
[ ]   814        *arch = CS_ARCH_SPARC;
[ ]   815        *mode = CS_MODE_BIG_ENDIAN;
[ ]   816        return true;
[ ]   817      case EM_SPARCV9:
[ ]   818        *arch = CS_ARCH_SPARC;
[ ]   819        *mode = CS_MODE_V9;
[ ]   820        return true;
[ ]   821  
[L]   822      default:
[L]   823        if (verbose_level > 1) {
[ ]   824          printf(
[ ]   825              "Unable to map to capstone target, disassembly will be "
[ ]   826              "unavailable");
[ ]   827        }
[L]   828        return false;
[B]   829    }
[B]   830  }

--- No 1-hop callers of elf.cc:bloaty::(anonymous namespace)::ElfMachineToCapstone(unsigned short, cs_arch*, cs_mode*) fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0   2130000  elf.cc:bloaty::(anonymous namespace)::ElfFile::Segment::header() const  (/src/bloaty/src/elf.cc:86-86)
     444    858000  elf.cc:bloaty::(anonymous namespace)::ElfFile::GetRegion(unsigned long, unsigned long) const  (/src/bloaty/src/elf.cc:179-181)
      67    856000  elf.cc:bloaty::(anonymous namespace)::ElfFile::header() const  (/src/bloaty/src/elf.cc:79-79)
     222    856000  elf.cc:bloaty::(anonymous namespace)::ElfFile::is_64bit() const  (/src/bloaty/src/elf.cc:165-165)
     222    856000  elf.cc:bloaty::(anonymous namespace)::ElfFile::is_native_endian() const  (/src/bloaty/src/elf.cc:166-166)
     222    856000  elf.cc:void bloaty::(anonymous namespace)::ElfFile::ReadStruct<Elf32_Ehdr, Elf64_Ehdr, bloaty::(anonymous namespace)::EhdrMunger>(std::basic_string_view<char, std::char_traits<char> >, unsigned long, bloaty::(anonymous namespace)::EhdrMunger, std::basic_string_view<char, std::char_traits<char> >*, Elf64_Ehdr*) const  (/src/bloaty/src/elf.cc:170-172)
     222    856000  elf.cc:void bloaty::(anonymous namespace)::ElfFile::ReadStruct<Elf32_Shdr, Elf64_Shdr, bloaty::(anonymous namespace)::ShdrMunger>(std::basic_string_view<char, std::char_traits<char> >, unsigned long, bloaty::(anonymous namespace)::ShdrMunger, std::basic_string_view<char, std::char_traits<char> >*, Elf64_Shdr*) const  (/src/bloaty/src/elf.cc:170-172)
     222    856000  elf.cc:void bloaty::(anonymous namespace)::ElfFile::ReadStruct<Elf_Note, Elf_Note, bloaty::(anonymous namespace)::NoteMunger>(std::basic_string_view<char, std::char_traits<char> >, unsigned long, bloaty::(anonymous namespace)::NoteMunger, std::basic_string_view<char, std::char_traits<char> >*, Elf_Note*) const  (/src/bloaty/src/elf.cc:170-172)
     222    856000  elf.cc:void bloaty::(anonymous namespace)::ElfFile::ReadStruct<Elf32_Phdr, Elf64_Phdr, bloaty::(anonymous namespace)::PhdrMunger>(std::basic_string_view<char, std::char_traits<char> >, unsigned long, bloaty::(anonymous namespace)::PhdrMunger, std::basic_string_view<char, std::char_traits<char> >*, Elf64_Phdr*) const  (/src/bloaty/src/elf.cc:170-172)
     222    856000  elf.cc:void bloaty::(anonymous namespace)::ElfFile::ReadStruct<Elf32_Sym, Elf64_Sym, bloaty::(anonymous namespace)::SymMunger>(std::basic_string_view<char, std::char_traits<char> >, unsigned long, bloaty::(anonymous namespace)::SymMunger, std::basic_string_view<char, std::char_traits<char> >*, Elf64_Sym*) const  (/src/bloaty/src/elf.cc:170-172)
     222    856000  elf.cc:void bloaty::(anonymous namespace)::ElfFile::ReadStruct<Elf32_Chdr, Elf64_Chdr, bloaty::(anonymous namespace)::ChdrMunger>(std::basic_string_view<char, std::char_traits<char> >, unsigned long, bloaty::(anonymous namespace)::ChdrMunger, std::basic_string_view<char, std::char_traits<char> >*, Elf64_Chdr*) const  (/src/bloaty/src/elf.cc:170-172)
     222    856000  elf.cc:void bloaty::(anonymous namespace)::ElfFile::ReadStruct<Elf32_Rela, Elf64_Rela, bloaty::(anonymous namespace)::RelaMunger>(std::basic_string_view<char, std::char_traits<char> >, unsigned long, bloaty::(anonymous namespace)::RelaMunger, std::basic_string_view<char, std::char_traits<char> >*, Elf64_Rela*) const  (/src/bloaty/src/elf.cc:170-172)
     222    856000  elf.cc:void bloaty::(anonymous namespace)::ElfFile::ReadStruct<Elf32_Rel, Elf64_Rel, bloaty::(anonymous namespace)::RelMunger>(std::basic_string_view<char, std::char_traits<char> >, unsigned long, bloaty::(anonymous namespace)::RelMunger, std::basic_string_view<char, std::char_traits<char> >*, Elf64_Rel*) const  (/src/bloaty/src/elf.cc:170-172)
     222    856000  elf.cc:bloaty::(anonymous namespace)::ElfFile::StructReader::StructReader(bloaty::(anonymous namespace)::ElfFile const&, std::basic_string_view<char, std::char_traits<char> >)  (/src/bloaty/src/elf.cc:188-188)
     222    856000  elf.cc:void bloaty::(anonymous namespace)::ElfFile::StructReader::Read<Elf32_Ehdr, Elf64_Ehdr, bloaty::(anonymous namespace)::EhdrMunger>(unsigned long, bloaty::(anonymous namespace)::EhdrMunger, std::basic_string_view<char, std::char_traits<char> >*, Elf64_Ehdr*) const  (/src/bloaty/src/elf.cc:192-198)
... (86 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  elf.cc:bloaty::(anonymous namespace)::ElfMachineToCapstone(unsigned short, cs_arch*, cs_mode*)  (/src/bloaty/src/elf.cc:781-830) ---
  d=1   L 783  T=0 F=3  T=3 F=26  case EM_386:
  d=1   L 787  T=0 F=3  T=0 F=29  case EM_X86_64:
  d=1   L 794  T=0 F=3  T=0 F=29  case EM_ARM:
  d=1   L 798  T=3 F=0  T=0 F=29  case EM_AARCH64:  <-- BLOCKER
  d=1   L 802  T=0 F=3  T=0 F=29  case EM_MIPS:
  d=1   L 805  T=0 F=3  T=0 F=29  case EM_PPC:
  d=1   L 809  T=0 F=3  T=0 F=29  case EM_PPC64:
  d=1   L 813  T=0 F=3  T=0 F=29  case EM_SPARC:
  d=1   L 817  T=0 F=3  T=0 F=29  case EM_SPARCV9:
  d=1   L 822  T=0 F=3  T=26 F=3  default:
  d=1   L 823  T=0 F=0  T=0 F=26  if (verbose_level > 1) {

[off-chain: 62 additional divergent branches across 20 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=86809c70eeb052ac, size=106 bytes, fuzzer=cmplog, trial=1, discovered_at=23533s, mutation_op=BytesCopyMutator):
  0000: 7f 45 4c 46 02 01 00 00 00 00 20 20 20 20 20 00   .ELF......     .
  0010: 01 d5 b7 00 08 00 f5 ff 01 00 20 20 07 90 99 12   ..........  ....
  0020: 54 00 00 00 00 00 00 00 10 00 00 00 00 00 00 00   T...............
  0030: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=43b1a3ff84794b7e, size=76 bytes, fuzzer=naive, trial=1, discovered_at=153s, mutation_op=BytesInsertMutator,CrossoverReplaceMutator):
  0000: 7f 45 4c 46 02 01 01 00 00 00 00 7f ff 20 20 00   .ELF.........  .
  0010: 00 00 00 00 00 00 20 20 20 20 20 20 ff 3c ff ff   ......      .<..
  0020: 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0030: 20 20 20 20 20 00 00 00 00 20 20 00 00 00 00 00        ....  .....
Seed 2 (id=697b917fe1c3c701, size=52 bytes, fuzzer=naive, trial=1, discovered_at=431s, mutation_op=TokenReplace,DwordAddMutator):
  0000: 7f 45 4c 46 01 01 01 00 f2 00 20 20 7f 2e fe ff   .ELF......  ....
  0010: ff ff 03 00 00 00 10 20 20 20 20 00 00 00 00 00   .......    .....
  0020: 00 00 00 00 38 20 00 00 10 00 00 00 00 00 00 ff   ....8 ..........
  0030: 00 00 00 00                                       ....
Seed 3 (id=5d61a88c26233d9d, size=68 bytes, fuzzer=naive, trial=1, discovered_at=2048s, mutation_op=WordAddMutator,BytesCopyMutator,ByteAddMutator):
  0000: 7f 45 4c 46 02 01 01 00 00 00 20 20 20 20 20 00   .ELF......     .
  0010: 00 00 00 00 00 00 20 20 20 20 20 20 ff ff ff ff   ......      ....
  0020: 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0030: 00 00 00 00 00 00 00 00 43 20 20 20 00 00 00 00   ........C   ....
Seed 4 (id=20c31fa3eb44658e, size=64 bytes, fuzzer=naive, trial=1, discovered_at=2388s, mutation_op=CrossoverReplaceMutator,BytesSetMutator):
  0000: 7f 45 4c 46 02 01 01 00 00 00 df 20 20 20 20 00   .ELF.......    .
  0010: 00 00 00 00 00 00 20 20 20 20 20 20 ff ff ff ff   ......      ....
  0020: 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0030: 00 00 00 00 00 00 00 00 00 01 00 20 00 00 20 20   ........... ..  
Seed 5 (id=017a47b9ccdfc684, size=64 bytes, fuzzer=naive, trial=1, discovered_at=2422s, mutation_op=DwordInterestingMutator):
  0000: 7f 45 4c 46 02 01 01 00 00 00 db 20 20 20 20 00   .ELF.......    .
  0010: 00 00 00 00 00 00 20 20 20 20 20 20 ff 3c ff ff   ......      .<..
  0020: 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0030: 20 20 20 20 20 00 00 00 01 00 20 20 00 00 20 20        .....  ..  


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0004  02(.)x1                             02(.)x6 01(.)x4                     PARTIAL
   0x0006  00(.)x1                             01(.)x10                            DIFFER
   0x0007  00(.)x1                             00(.)x7 06(.)x3                     PARTIAL
   0x0008  00(.)x1                             00(.)x6 f2(.)x4                     PARTIAL
   0x000a  20( )x1                             df(.)x5 20( )x2 00(.)x1 db(.)x1 +1u  PARTIAL
   0x000b  20( )x1                             20( )x6 21(!)x2 7f(.)x1 01(.)x1     PARTIAL
   0x000c  20( )x1                             20( )x4 df(.)x3 ff(.)x1 7f(.)x1 +1u  PARTIAL
   0x000d  20( )x1                             20( )x6 df(.)x2 2e(.)x1 23(#)x1     PARTIAL
   0x000e  20( )x1                             20( )x8 fe(.)x1 23(#)x1             PARTIAL
   0x000f  00(.)x1                             00(.)x8 ff(.)x1 03(.)x1             PARTIAL
   0x0010  01(.)x1                             00(.)x6 01(.)x2 ff(.)x1 4c(L)x1     PARTIAL
   0x0011  d5(.)x1                             00(.)x7 ff(.)x1 46(F)x1 01(.)x1     DIFFER
   0x0012  b7(.)x1                             00(.)x8 03(.)x1 01(.)x1             DIFFER
   0x0013  00(.)x1                             00(.)x7 f4(.)x3                     PARTIAL
   0x0014  08(.)x1                             00(.)x10                            DIFFER
   0x0016  f5(.)x1                             20( )x6 f2(.)x3 10(.)x1             DIFFER
   0x0017  ff(.)x1                             20( )x7 00(.)x3                     DIFFER
   0x0018  01(.)x1                             20( )x10                            DIFFER
   0x0019  00(.)x1                             20( )x10                            DIFFER
   0x001a  20( )x1                             20( )x7 df(.)x3                     PARTIAL
   0x001b  20( )x1                             20( )x9 00(.)x1                     PARTIAL
   0x001c  07(.)x1                             ff(.)x6 20( )x3 00(.)x1             DIFFER
   0x001d  90(.)x1                             00(.)x4 ff(.)x4 3c(<)x2             DIFFER
   0x001e  99(.)x1                             ff(.)x6 00(.)x4                     DIFFER
   0x001f  12(.)x1                             ff(.)x6 00(.)x4                     DIFFER
   0x0020  54(T)x1                             06(.)x6 01(.)x3 00(.)x1             DIFFER
   0x0024  00(.)x1                             00(.)x9 38(8)x1                     PARTIAL
   0x0025  00(.)x1                             00(.)x9 20( )x1                     PARTIAL
   0x0028  10(.)x1                             00(.)x7 10(.)x1 08(.)x1 26(&)x1     PARTIAL
   0x002a  00(.)x1                             00(.)x8 01(.)x2                     PARTIAL
   0x002c  00(.)x1                             00(.)x7 01(.)x3                     PARTIAL
   0x002f  00(.)x1                             00(.)x6 1f(.)x3 ff(.)x1             PARTIAL
   0x0030  00(.)x1                             00(.)x7 20( )x3                     PARTIAL
   0x0031  00(.)x1                             00(.)x8 20( )x2                     PARTIAL
   0x0032  00(.)x1                             00(.)x8 20( )x2                     PARTIAL
   0x0033  00(.)x1                             00(.)x7 20( )x2 01(.)x1             PARTIAL
   0x0034  00(.)x1                             00(.)x4 20( )x2 84(.)x2 1f(.)x1     PARTIAL
   0x0035  00(.)x1                             00(.)x7 84(.)x2                     PARTIAL
   0x0036  00(.)x1                             00(.)x7 84(.)x2                     PARTIAL
   0x0037  00(.)x1                             00(.)x7 84(.)x2                     PARTIAL
   ... (8 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/bloaty_59.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 59,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 59 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 59 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 59 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).