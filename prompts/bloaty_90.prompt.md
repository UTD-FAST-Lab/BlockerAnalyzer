==== BLOCKER ====
Target: bloaty
Branch ID: 90
Location: /src/bloaty/src/elf.cc:1279:29
Enclosing function: elf.cc:bloaty::(anonymous namespace)::ElfObjectFile::GetBuildId[abi:cxx11]() const
Source line:     for (Elf64_Xword i = 1; i < elf.section_count(); i++) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    6        4          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     2        8          0  REFERENCE
mopt                             5        5          0  REFERENCE
minimizer                        5        5          0  REFERENCE
fast                             6        4          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.60h  loser=23.60h
  avg hitcount on branch: winner=14015000  loser=0
  prob_div=1.00  dur_div=23.00h  hit_div=14015000
  subject-level: delta_AUC=26255160.0  p_AUC=0.0002  delta_Final=523.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/bloaty/90/{W,L}/branch_coverage_show.txt

--- Enclosing function: elf.cc:bloaty::(anonymous namespace)::ElfObjectFile::GetBuildId[abi:cxx11]() const (/src/bloaty/src/elf.cc:1271-1295) ---
[B]  1269        : ObjectFile(std::move(file)) {}
[ ]  1270  
[B]  1271    std::string GetBuildId() const override {
[B]  1272      if (IsObjectFile(file_data().data())) {
[ ]  1273        // Object files don't have a build ID.
[ ]  1274        return std::string();
[ ]  1275      }
[ ]  1276  
[B]  1277      ElfFile elf(file_data().data());
[B]  1278      assert(elf.IsOpen());
[B]  1279      for (Elf64_Xword i = 1; i < elf.section_count(); i++) { <-- BLOCKER
[W]  1280        ElfFile::Section section;
[W]  1281        elf.ReadSection(i, &section);
[W]  1282        if (section.header().sh_type != SHT_NOTE) {
[W]  1283          continue;
[W]  1284        }
[ ]  1285  
[W]  1286        for (ElfFile::NoteIter notes(section); !notes.IsDone(); notes.Next()) {
[ ]  1287          if (notes.name() == "GNU" && notes.type() == NT_GNU_BUILD_ID) {
[ ]  1288            return std::string(notes.descriptor());
[ ]  1289          }
[ ]  1290        }
[W]  1291      }
[ ]  1292  
[ ]  1293      // No build id section found.
[B]  1294      return std::string();
[B]  1295    }

--- No 1-hop callers of elf.cc:bloaty::(anonymous namespace)::ElfObjectFile::GetBuildId[abi:cxx11]() const fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
 2840000         0  elf.cc:unsigned short bloaty::(anonymous namespace)::ByteSwapFunc::operator()<unsigned short>(unsigned short)  (/src/bloaty/src/elf.cc:38-40)
 2840000         0  elf.cc:unsigned int bloaty::(anonymous namespace)::ByteSwapFunc::operator()<unsigned int>(unsigned int)  (/src/bloaty/src/elf.cc:38-40)
 2840000         0  elf.cc:unsigned long bloaty::(anonymous namespace)::ByteSwapFunc::operator()<unsigned long>(unsigned long)  (/src/bloaty/src/elf.cc:38-40)
 2840000         0  elf.cc:unsigned char bloaty::(anonymous namespace)::ByteSwapFunc::operator()<unsigned char>(unsigned char)  (/src/bloaty/src/elf.cc:38-40)
 2840000         0  elf.cc:long bloaty::(anonymous namespace)::ByteSwapFunc::operator()<long>(long)  (/src/bloaty/src/elf.cc:38-40)
 2840000         0  elf.cc:int bloaty::(anonymous namespace)::ByteSwapFunc::operator()<int>(int)  (/src/bloaty/src/elf.cc:38-40)
       0   2130000  elf.cc:bloaty::(anonymous namespace)::ElfFile::Segment::header() const  (/src/bloaty/src/elf.cc:86-86)
     402    856000  elf.cc:bloaty::(anonymous namespace)::ElfFile::header() const  (/src/bloaty/src/elf.cc:79-79)
       6    855000  elf.cc:bloaty::(anonymous namespace)::ElfFile::ReadSegment(unsigned int, bloaty::(anonymous namespace)::ElfFile::Segment*) const  (/src/bloaty/src/elf.cc:522-534)
       0    427000  elf.cc:bloaty::(anonymous namespace)::ElfFile::Segment::contents() const  (/src/bloaty/src/elf.cc:87-87)
       0    427000  elf.cc:bloaty::(anonymous namespace)::GetSegmentName[abi:cxx11](bloaty::(anonymous namespace)::ElfFile::Segment const&, unsigned long, bloaty::(anonymous namespace)::ReportSegmentsBy)  (/src/bloaty/src/elf.cc:1097-1134)
  287000         0  elf.cc:bloaty::(anonymous namespace)::ElfFile::Section::header() const  (/src/bloaty/src/elf.cc:100-100)
  287000         0  elf.cc:bloaty::(anonymous namespace)::ElfFile::ReadSection(unsigned int, bloaty::(anonymous namespace)::ElfFile::Section*) const  (/src/bloaty/src/elf.cc:536-555)
  286000       230  elf.cc:bloaty::(anonymous namespace)::ElfFile::section_count() const  (/src/bloaty/src/elf.cc:80-80)
  284000       546  elf.cc:void bloaty::(anonymous namespace)::ElfFile::StructReader::ReadFallback<Elf32_Ehdr, Elf64_Ehdr, bloaty::(anonymous namespace)::EhdrMunger>(unsigned long, std::basic_string_view<char, std::char_traits<char> >*, Elf64_Ehdr*) const  (/src/bloaty/src/elf.cc:342-357)
... (17 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  elf.cc:bloaty::(anonymous namespace)::ElfObjectFile::GetBuildId[abi:cxx11]() const  (/src/bloaty/src/elf.cc:1271-1295) ---
  d=1   L1279  T=228000 F=90  T=0 F=120  for (Elf64_Xword i = 1; i < elf.section_count(); i++) {  <-- BLOCKER
  d=1   L1282  T=228000 F=6  T=0 F=0  if (section.header().sh_type != SHT_NOTE) {
  d=1   L1286  T=0 F=6  T=0 F=0  for (ElfFile::NoteIter notes(section); !notes.IsDone(); n...

[off-chain: 64 additional divergent branches across 19 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=ecb713059f708e8e, size=73 bytes, fuzzer=cmplog, trial=1, discovered_at=10802s, mutation_op=CrossoverInsertMutator,BytesRandInsertMutator,TokenInsert,CrossoverInsertMutator,BytesRandSetMutator,ByteDecMutator):
  0000: 7f 45 4c 46 01 02 00 00 00 03 20 20 20 20 20 00   .ELF......     .
  0010: 00 00 00 00 00 00 00 00 00 03 07 00 00 00 00 0a   ................
  0020: 00 00 00 02 24 24 20 20 00 00 00 00 01 08 00 00   ....$$  ........
  0030: 00 00 00 00 00 00 24 20 0a 00 00 20 00 20 20 20   ......$ ... .   
Seed 2 (id=e97c8a45eb376ae4, size=52 bytes, fuzzer=cmplog, trial=1, discovered_at=19879s, mutation_op=BytesDeleteMutator,ByteNegMutator):
  0000: 7f 45 4c 46 01 02 00 00 00 03 20 20 00 00 00 08   .ELF......  ....
  0010: ff 00 00 00 00 00 00 00 00 03 07 00 00 00 00 0a   ................
  0020: 00 00 00 02 24 24 20 20 00 00 00 00 00 00 00 06   ....$$  ........
  0030: 00 00 00 00                                       ....
Seed 3 (id=ac3ba2cbb00192e0, size=117 bytes, fuzzer=cmplog, trial=1, discovered_at=56923s, mutation_op=BytesSwapMutator,ByteNegMutator,BytesDeleteMutator):
  0000: 7f 45 4c 46 01 01 00 00 00 00 24 20 20 20 20 00   .ELF......$    .
  0010: 00 00 00 00 03 00 00 00 24 20 20 20 07 00 00 00   ........$   ....
  0020: 10 00 00 00 08 00 00 00 00 00 07 00 00 00 10 00   ................
  0030: 02 00 00 00 00 00 00 00 ff 00 00 00 00 00 03 00   ................
Seed 4 (id=8aaeeb3b8eacf665, size=94 bytes, fuzzer=cmplog, trial=1, discovered_at=56956s, mutation_op=DwordInterestingMutator,QwordAddMutator):
  0000: 7f 45 4c 46 02 02 03 00 7f 00 00 00 00 00 00 03   .ELF............
  0010: 00 00 00 00 ff 00 00 07 20 20 20 20 00 00 00 08   ........    ....
  0020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 08   ................
  0030: 00 00 00 00 00 00 00 00 00 00 00 08 00 03 00 00   ................
Seed 5 (id=3ab8422648b69481, size=74 bytes, fuzzer=cmplog, trial=1, discovered_at=60421s, mutation_op=BytesSwapMutator,WordAddMutator):
  0000: 7f 45 4c 46 02 02 03 00 00 22 01 00 00 00 00 03   .ELF....."......
  0010: 00 00 00 28 00 00 20 21 20 20 20 20 98 38 10 00   ...(.. !    .8..
  0020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 08   ................
  0030: 00 00 00 00 00 00 00 00 00 00 00 00 49 9a ff ff   ............I...

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
   0x0005  02(.)x6 01(.)x2                     01(.)x10                            PARTIAL
   0x0006  00(.)x5 03(.)x3                     01(.)x10                            DIFFER
   0x0007  00(.)x8                             00(.)x7 06(.)x3                     PARTIAL
   0x0008  00(.)x6 7f(.)x2                     00(.)x6 f2(.)x4                     PARTIAL
   0x0009  00(.)x4 03(.)x3 22(")x1             00(.)x10                            PARTIAL
   0x000a  20( )x4 00(.)x2 24($)x1 01(.)x1     df(.)x5 20( )x2 00(.)x1 db(.)x1 +1u  PARTIAL
   0x000b  00(.)x5 20( )x3                     20( )x6 21(!)x3 7f(.)x1             PARTIAL
   0x000c  00(.)x6 20( )x2                     20( )x4 df(.)x3 ff(.)x1 7f(.)x1 +1u  PARTIAL
   0x000d  00(.)x6 20( )x2                     20( )x6 23(#)x2 2e(.)x1 df(.)x1     PARTIAL
   0x000e  00(.)x6 20( )x2                     20( )x7 23(#)x2 fe(.)x1             PARTIAL
   0x000f  00(.)x4 03(.)x3 08(.)x1             00(.)x7 03(.)x2 ff(.)x1             PARTIAL
   0x0010  00(.)x5 ff(.)x2 05(.)x1             00(.)x6 4c(L)x2 ff(.)x1 01(.)x1     PARTIAL
   0x0011  00(.)x7 02(.)x1                     00(.)x6 46(F)x2 ff(.)x1 01(.)x1     PARTIAL
   0x0012  00(.)x8                             00(.)x7 01(.)x2 03(.)x1             PARTIAL
   0x0013  00(.)x6 28(()x1 01(.)x1             00(.)x7 f4(.)x3                     PARTIAL
   0x0014  00(.)x5 03(.)x2 ff(.)x1             00(.)x10                            PARTIAL
   0x0016  00(.)x7 20( )x1                     20( )x6 f2(.)x3 10(.)x1             PARTIAL
   0x0017  00(.)x5 07(.)x1 21(!)x1 66(f)x1     20( )x7 00(.)x3                     PARTIAL
   0x0018  00(.)x4 20( )x2 24($)x1 61(a)x1     20( )x10                            PARTIAL
   0x0019  20( )x3 03(.)x2 6c(l)x1 7f(.)x1 +1u  20( )x10                            PARTIAL
   0x001a  07(.)x3 20( )x3 73(s)x1 00(.)x1     20( )x7 df(.)x3                     PARTIAL
   0x001b  00(.)x4 20( )x3 65(e)x1             20( )x9 00(.)x1                     PARTIAL
   0x001c  00(.)x6 07(.)x1 98(.)x1             ff(.)x6 20( )x3 00(.)x1             PARTIAL
   0x001d  00(.)x6 38(8)x1 90(.)x1             00(.)x4 ff(.)x4 3c(<)x2             PARTIAL
   0x001e  00(.)x6 10(.)x1 99(.)x1             ff(.)x6 00(.)x4                     PARTIAL
   0x001f  0a(.)x2 00(.)x2 08(.)x2 12(.)x1 +1u  ff(.)x6 00(.)x4                     PARTIAL
   0x0020  00(.)x6 10(.)x1 12(.)x1             06(.)x6 01(.)x3 00(.)x1             PARTIAL
   0x0023  00(.)x5 02(.)x3                     00(.)x10                            PARTIAL
   0x0024  00(.)x4 24($)x3 08(.)x1             00(.)x9 38(8)x1                     PARTIAL
   0x0025  00(.)x5 24($)x3                     00(.)x9 20( )x1                     PARTIAL
   0x0026  00(.)x5 20( )x3                     00(.)x10                            PARTIAL
   0x0027  00(.)x5 20( )x3                     00(.)x10                            PARTIAL
   0x0028  00(.)x7 10(.)x1                     00(.)x6 08(.)x2 10(.)x1 26(&)x1     PARTIAL
   0x0029  00(.)x7 03(.)x1                     00(.)x10                            PARTIAL
   0x002a  00(.)x6 07(.)x2                     00(.)x8 01(.)x2                     PARTIAL
   0x002d  00(.)x7 08(.)x1                     00(.)x10                            PARTIAL
   0x002e  00(.)x7 10(.)x1                     00(.)x10                            PARTIAL
   0x002f  00(.)x3 08(.)x3 06(.)x1 0a(.)x1     00(.)x6 1f(.)x3 ff(.)x1             PARTIAL
   0x0030  00(.)x6 02(.)x1 10(.)x1             00(.)x7 20( )x3                     PARTIAL
   0x0031  00(.)x8                             00(.)x8 20( )x2                     PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/bloaty_90.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 90,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 90 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 90 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 90 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).