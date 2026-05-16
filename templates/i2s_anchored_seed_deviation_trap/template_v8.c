/*
 * i2s_anchored_seed_deviation_trap v8 — sub-type C via DICTIONARY POLLUTION.
 *
 * v7c and v7c2 failed to reproduce the v6 mechanism at sub-type C trap
 * shape. Diagnosis (post-hoc): at sub-type C the trap CMP literals
 * themselves are I2S substitution targets — vpc's I2S anchors the
 * trap-region bytes INTO the valid set, not outside it. The v6
 * "queue-monoculture-OUTSIDE-anchor-zone" mechanism is structurally
 * inapplicable.
 *
 * v8 tests the alternative mechanism that should fit sub-type C: I2S
 * DICTIONARY POLLUTION. The hypothesis:
 *
 *   Predicted mechanism (v8):
 *   - At low N_POLLUTE, vpc's I2S dictionary contains only the K=7
 *     valid class literals. I2SRandReplace at offset 128 substitutes
 *     one of K class literals at near-100% rate; vpc's bytes 128-131
 *     stay IN valid set; vpc rarely trips trap. vp without I2S has
 *     random bytes 128-131; trips trap often (random ∉ 7-element set
 *     with prob ≈ 1).
 *     → vp >>> vpc on crash count.
 *
 *   - At high N_POLLUTE, vpc's I2S dictionary contains K + N_POLLUTE
 *     entries. I2SRandReplace's class-substitution rate at offset 128
 *     dilutes to K/(K + N_POLLUTE). At N=4096, dilution to 7/4103 ≈
 *     0.17%. vpc's bytes 128-131 get OVERWRITTEN with non-class
 *     literals from elsewhere in the dictionary (the pollution
 *     literals, which appear at unrelated offsets in the input but
 *     whose 4-byte windows can be substituted into bytes 128-131).
 *     → vpc trips trap MORE often. vp's behavior unchanged.
 *     → vp/vpc gap NARROWS or REVERSES.
 *
 * If the predicted dose-response holds, this corroborates the
 * "sub-type C divergence at lcms is corpus-pollution-driven, not
 * anchor-monoculture-driven" interpretation.
 *
 * Compile-time parameter: N_POLLUTE ∈ {0, 64, 512, 4096}.
 *
 * Design choices vs v7c/v7c2:
 *   - NO upstream anchor block (trivial size gate only) — both fuzzers
 *     reach the trap.
 *   - K=7 class FOURCCs at trap (same as v7c) — modeled on lcms.
 *   - N_POLLUTE noise CMPs at offsets 16..127, each emits cmplog hook
 *     but does NOT gate the trap (XOR result into volatile sink).
 */

#include <stdint.h>
#include <stddef.h>

#ifndef N_POLLUTE
#define N_POLLUTE 0
#endif

#if N_POLLUTE != 0  && N_POLLUTE != 64 && \
    N_POLLUTE != 512 && N_POLLUTE != 4096
#error "N_POLLUTE must be one of {0, 64, 512, 4096}"
#endif

#define TRAP_OFFSET 128
#define K_VALID     7
#define MAX_POLLUTE 4096

static const uint32_t CLASS_LITERALS[K_VALID] = {
    0x73636E72u,  /* 'scnr' */
    0x6D6E7472u,  /* 'mntr' */
    0x70727472u,  /* 'prtr' */
    0x6C696E6Bu,  /* 'link' */
    0x61627374u,  /* 'abst' */
    0x73706163u,  /* 'spac' */
    0x6E6D636Cu   /* 'nmcl' */
};

/* Pollution table: 4096 distinct 4-byte literals, runtime-initialized
 * to discourage compile-time fold. Each pollution CMP fires every
 * execution but does NOT affect trap reachability. */
static uint32_t POLLUTE_TABLE[MAX_POLLUTE];

static void setup_pollute(void) {
    static int initialized = 0;
    if (initialized) return;
    for (int i = 0; i < MAX_POLLUTE; i++) {
        POLLUTE_TABLE[i] = 0xDEAD0000u + (uint32_t)i;
    }
    initialized = 1;
}

static volatile uint32_t g_pollute_sink;

static inline uint32_t read_be32(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] << 8)  |  (uint32_t)p[3];
}

/* Pollution: N_POLLUTE noise literal CMPs at varying offsets in [16,
 * 127]. Each call hits the cmplog __sanitizer_cov_trace_const_cmp_4
 * hook, populating vpc's I2S dictionary with one entry. The match
 * outcome XORs into a volatile sink so the compiler cannot eliminate
 * the CMPs as dead code. The CMPs do NOT gate the trap — they are
 * "soft" pressure on dictionary breadth. */
__attribute__((noinline))
static void pollute(const uint8_t *data, size_t size) {
    uint32_t s = 0;
    for (int i = 0; i < N_POLLUTE; i++) {
        size_t off = 16 + (size_t)((i * 4) % 112);  /* offsets 16..127, wrap */
        if (off + 4 > size) continue;
        uint32_t v = read_be32(data + off);
        if (v == POLLUTE_TABLE[i]) s++;
    }
    g_pollute_sink ^= s;
}

__attribute__((noinline))
static int valid_class(uint32_t cls) {
    int found = 0;
    for (int i = 0; i < K_VALID; i++) {
        if (cls == CLASS_LITERALS[i]) found = 1;
    }
    return found;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    setup_pollute();

    /* Trivial length gate — both fuzzers easily pass. */
    if (size < TRAP_OFFSET + 4) return 0;

    /* Dictionary pollution block. Doesn't gate the trap; just populates
     * the I2S dictionary with N_POLLUTE noise literals. */
    pollute(data, size);

    /* Sub-type C trap. Trap CMP literals (K=7 valid FOURCCs) are
     * I2S-substitutable. CMP_MAP records Hamming distance per class
     * literal — vp's gradient channel can retain near-class seeds.
     *
     * Exclude cls == 0 so the all-zero seed-zero doesn't auto-trip the
     * trap on startup. (Without this guard, both fuzzers find a
     * deterministic 3-crash floor at startup with no differentiation.) */
    uint32_t cls = read_be32(data + TRAP_OFFSET);
    if (cls != 0 && !valid_class(cls)) {
        __builtin_trap();
    }
    return 0;
}
