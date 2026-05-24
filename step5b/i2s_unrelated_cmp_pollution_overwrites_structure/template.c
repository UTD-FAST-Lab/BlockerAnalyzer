/*
 * Synthetic harness for cluster: i2s_unrelated_cmp_pollution_overwrites_structure
 * Family: I2S_anti  (the I2S technique HURTS)
 *
 * Mechanism under test
 * --------------------
 * The target objective is a *structural* byte gate: a fixed window of the input
 * (the STRUCTURE_WINDOW) must equal a precise reference sequence. Reaching it is
 * pure byte search, equally available to every fuzzer.
 *
 * Surrounding it are POLLUTION_SOURCES *unrelated* exact-equality comparisons,
 * each over its own disjoint operand and each gated to NEVER reach the trap
 * (their bodies do nothing). Their only purpose is to feed the CmpLogObserver
 * with many distinct operand literals. An I2S-carrying fuzzer (cmplog / vpc)
 * runs I2SRandReplace: it scans the WHOLE input for byte runs matching a logged
 * operand and substitutes the paired operand at those offsets. Because the
 * pollution operands are short, common byte runs, I2S frequently lands a splice
 * *inside the STRUCTURE_WINDOW*, overwriting structural bytes the target gate
 * needs. The more pollution sources there are, the more often I2S corrupts the
 * window per execution, so the I2S-carrying fuzzers degrade.
 *
 * The lacks-I2S fuzzers (naive, value_profile) never run the substitution stage,
 * so their havoc/gradient exploration of the structure window is undisturbed and
 * they win; the win margin grows with the knob.
 *
 * One compile-time knob
 * ---------------------
 *   POLLUTION_SOURCES = number of unrelated literal CMPs competing for input bytes.
 * Larger value => more I2S splice pressure on the structural window.
 *
 * Self-contained: stdint/stddef/string only. The trap on the structural gate is
 * the SOLE objective; the pollution arms have empty bodies (no coverage edge that
 * is itself an objective). They still emit a CMP, which is the entire point.
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

/* ---- the one program-feature knob -------------------------------------- */
#ifndef POLLUTION_SOURCES
#define POLLUTION_SOURCES 8
#endif

/* Structural window: an 8-byte precise reference the target gate requires.
 * Width is fixed; only the number of competing pollution CMPs varies. */
#define STRUCT_OFF   0
#define STRUCT_LEN   8
static const uint8_t STRUCT_REF[STRUCT_LEN] = {
    0x53, 0x54, 0x52, 0x55, 0x43, 0x54, 0x21, 0x00  /* "STRUCT!\0" */
};

/* Pollution operands live in a region the I2S scanner reads from. Each is a
 * short literal an I2S-carrying fuzzer will harvest and try to splice anywhere
 * in the input -- including over STRUCT_REF's window. */
#define POLL_OFF    8
#define POLL_STRIDE 2          /* each pollution CMP consumes 2 input bytes */

/* Enough distinct literals to cover the max scan value. Kept as 16-bit values
 * so each pollution arm is a 2-byte exact compare. */
static const uint16_t POLL_LIT[16] = {
    0x4142, 0x4344, 0x4546, 0x4748, 0x494a, 0x4b4c, 0x4d4e, 0x4f50,
    0x5152, 0x5354, 0x5556, 0x5758, 0x595a, 0x6162, 0x6364, 0x6566
};

/* Volatile sink so the pollution comparisons cannot be optimized away. */
static volatile uint32_t g_sink = 0;

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    /* Need the structural window plus all pollution operand bytes present. */
    size_t need = POLL_OFF + (size_t)POLLUTION_SOURCES * POLL_STRIDE;
    if (need < (STRUCT_OFF + STRUCT_LEN))
        need = STRUCT_OFF + STRUCT_LEN;
    if (size < need)
        return 0;

    uint8_t window[STRUCT_LEN];
    memcpy(window, data + STRUCT_OFF, STRUCT_LEN);

#if POLLUTION_SOURCES > 0
    /* Unrelated literal CMPs. Each compares a distinct 2-byte input slice to a
     * distinct literal. The CmpLogObserver records these operands; I2S then
     * splices them across the input, frequently corrupting the window above.
     * Bodies are empty -- these are NOT objectives, only operand sources. */
    for (int i = 0; i < POLLUTION_SOURCES; i++) {
        uint16_t v;
        memcpy(&v, data + POLL_OFF + (size_t)i * POLL_STRIDE, sizeof(v));
        if (v == POLL_LIT[i & 15]) {
            g_sink += (uint32_t)v;   /* no trap, no new objective edge */
        }
    }
#endif

    /* SOLE objective: the structural window must equal the precise reference. */
    if (memcmp(window, STRUCT_REF, STRUCT_LEN) == 0) {
        __builtin_trap();
    }

    return 0;
}
