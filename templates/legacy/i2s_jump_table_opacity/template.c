/*
 * jump_table_opacity v2 — switch-table dispatch makes cmplog's I2S blind.
 *
 * v1 had an unintended leak: a post-dispatch `if (m == TARGET_CASE)`
 * check exposed TARGET_CASE to cmplog's I2S as a regular integer
 * comparison, letting cmp substitute it directly into bytes 0-3
 * regardless of dispatch shape. cmp dominated at every N (not because
 * I2S actually saw the dispatch, but because it bypassed the dispatch
 * entirely via the post-check).
 *
 * v2 fix: the trap fires from INSIDE the target case body. There is NO
 * post-dispatch comparison. Reaching the trap requires the dispatch
 * itself to land on case TARGET_CASE. The case body uses a compile-
 * time-folded conditional (`(I) == TARGET_CASE` where I is the case
 * label literal) so non-target cases compile to just the sink and the
 * target case compiles to just `__builtin_trap()`. The runtime
 * comparison is fully eliminated by the compiler.
 *
 * Real-target origin: libpcap gen_linktype() switch on cstate->linktype
 * (60+ contiguous DLT case values, gencode.c lines 3218-3623). At -O2
 * clang lowers dense contiguous switches to JUMP TABLES — a single
 * indirect-branch instruction indexed by the dispatch value, plus a
 * .rodata table of jump targets. NO per-case CMP is emitted, so
 * CmpLogObserver registers no hooks, the case literals never enter the
 * I2S dictionary, and I2SRandReplace has no entries to substitute.
 *
 * RCA-cataloged at 39 of 148 libpcap blockers as
 * jump_table_opacity_I2S_lock_in family.
 *
 * Compile-time parameter:
 *   N_CASES ∈ {4, 16, 64, 256} — number of contiguous switch cases.
 *   At N=4, clang typically emits a comparison chain (per-case CMP
 *   visible to I2S). At N≥16, clang emits a jump table (no per-case
 *   CMP, I2S blind). The dose-response transitions cmp from "I2S helps"
 *   regime to "I2S blind" regime.
 *
 * Trap: only the case TARGET_CASE = N_CASES/2 triggers __builtin_trap.
 *
 * Predicted dose-response (4 fuzzers):
 *   N=4 (compare chain, I2S sees per-case CMPs):
 *     cmp ≫ naive — I2S substitutes TARGET_CASE directly into v
 *     vpc ≳ cmp — VP gradient adds little at small case set
 *     vp ≈ naive — gradient saturated, no I2S
 *
 *   N=16 (clang threshold, may emit hybrid):
 *     direction-transition zone
 *
 *   N=64 (definitive jump table, I2S blind):
 *     cmp ≤ naive — I2S provides nothing; cmplog tracing-stage
 *       throughput tax (~10-20%) puts cmp BELOW naive
 *     vp ≈ vpc ≈ naive — random hit rate 1/N; gradient on case-body
 *       arithmetic is too weak to differentiate
 *
 *   N=256 (deeply jump table):
 *     cmp ≪ naive — same mechanism as N=64, hit rate 1/256, throughput
 *       tax dominates
 */

#include <stdint.h>
#include <stddef.h>

#ifndef N_CASES
#define N_CASES 64
#endif

#if N_CASES != 4 && N_CASES != 16 && N_CASES != 64 && N_CASES != 256
#error "N_CASES must be one of {4, 16, 64, 256}"
#endif

#define TARGET_CASE  (N_CASES / 2)

static volatile uint32_t g_sink;

/* Compile-time-folded case body: for case I where I is the case label
 * literal, the conditional ((I) == TARGET_CASE) folds at compile time.
 * Non-target cases compile to just `g_sink ^= ...; break;`.
 * The target case compiles to just `__builtin_trap();`. No runtime
 * comparison survives — the only path to the trap is the dispatch
 * landing on case TARGET_CASE. */
#define CASE_BODY(I) case I: \
    if ((I) == TARGET_CASE) __builtin_trap(); \
    g_sink ^= (uint32_t)((I) + 1); \
    break;

#define CASES_4(start) \
    CASE_BODY((start)+0) CASE_BODY((start)+1) \
    CASE_BODY((start)+2) CASE_BODY((start)+3)

#define CASES_16(start) \
    CASES_4((start)+0)  CASES_4((start)+4) \
    CASES_4((start)+8)  CASES_4((start)+12)

#define CASES_64(start) \
    CASES_16((start)+0)  CASES_16((start)+16) \
    CASES_16((start)+32) CASES_16((start)+48)

#define CASES_256(start) \
    CASES_64((start)+0)   CASES_64((start)+64) \
    CASES_64((start)+128) CASES_64((start)+192)

__attribute__((noinline))
static void dispatch(uint32_t v) {
    uint32_t m = v % (uint32_t)N_CASES;
    /* The dispatch itself selects the case. At small N, clang emits a
     * comparison chain (per-case CMP visible to I2S). At large N, clang
     * emits a jump table (no per-case CMP, I2S blind). The trap fires
     * only when the dispatch lands on case TARGET_CASE. */
    switch (m) {
#if N_CASES == 4
        CASES_4(0)
#elif N_CASES == 16
        CASES_16(0)
#elif N_CASES == 64
        CASES_64(0)
#elif N_CASES == 256
        CASES_256(0)
#endif
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;
    uint32_t v = ((uint32_t)data[0] << 24) | ((uint32_t)data[1] << 16) |
                 ((uint32_t)data[2] << 8)  |  (uint32_t)data[3];
    dispatch(v);
    return 0;
}
