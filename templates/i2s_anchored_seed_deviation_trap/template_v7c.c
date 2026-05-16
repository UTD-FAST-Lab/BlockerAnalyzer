/*
 * i2s_anchored_seed_deviation_trap v7c — SUB-TYPE C trap shape verification.
 *
 * Companion to v6 (sub-type B threshold trap) and v7a (sub-type A length-
 * fail trap). v7c tests the third sub-type: SWITCH-DEFAULT-ARM trap
 * where input class field must match one of K valid literals.
 *
 * Trap shape:
 *   if (cls != L0 && cls != L1 && ... && cls != L_{K-1}) trap();
 * Each `==` CMP logs L_i as an I2S dict entry. cmp/vpc's I2S can
 * substitute any of the K valid literals into bytes 128-131.
 *
 * vpc's queue concentrates at one of the K valid values (I2SRandReplace
 * substitution pressure); vp's queue has random bytes 128-131. Trap
 * fires when bytes 128-131 are OUTSIDE the K-element valid set.
 *
 * Mirrors lcms cmsio0.c:758 br67 trap (validDeviceClass switch default
 * arm; K=7 valid FOURCCs: scnr/mntr/prtr/link/abst/spac/nmcl).
 *
 * Compile-time parameter:
 *   N_ARMS_PER_OFFSET ∈ {1, 7, 56, 224} — same knob as v6, controls
 *   upstream I2S dictionary breadth.
 *
 * Mechanism prediction:
 *   - Low N: vpc wins. Small upstream dictionary; high I2SRandReplace
 *     hit rate on the K class literals; vpc's bytes 128-131 stay in
 *     valid set; vpc rarely trips trap.
 *   - High N: vp wins. Upstream dictionary saturates with 16*N entries;
 *     I2SRandReplace's K class entries are diluted to K/(K+16*N) of
 *     mutator budget; vpc's bytes 128-131 drift OUT of valid set;
 *     vpc trips trap MORE often. vp's behavior is independent of N
 *     (no I2S — random bytes 128-131 are always outside the K=7 set).
 *
 * Predicted curve mirrors v6: vp/vpc ratio monotone-increasing in N,
 * direction-flip somewhere in the middle of the dose range.
 */

#include <stdint.h>
#include <stddef.h>

#ifndef N_ARMS_PER_OFFSET
#define N_ARMS_PER_OFFSET 7
#endif

#if N_ARMS_PER_OFFSET != 1   && N_ARMS_PER_OFFSET != 7   && \
    N_ARMS_PER_OFFSET != 56  && N_ARMS_PER_OFFSET != 224
#error "N_ARMS_PER_OFFSET must be one of {1, 7, 56, 224}"
#endif

#define MAGIC_OFFSET 36
#define MAGIC_VALUE  0x61637370U  /* 'acsp' */
#define TRAP_OFFSET  128          /* class field — past the anchor zone */
#define K_VALID      7
#define N_SITES      16
#define MAX_ARMS     224

static const size_t SITE_OFFSETS[N_SITES] = {
    0,  4,  8,  12, 16, 20, 24, 28,
    32, 40, 44, 48, 52, 56, 60, 64
};

/* K=7 class literals — modeled directly on lcms cmsSig*Class FOURCCs. */
static const uint32_t CLASS_LITERALS[K_VALID] = {
    0x73636E72u,  /* 'scnr' — cmsSigInputClass */
    0x6D6E7472u,  /* 'mntr' — cmsSigDisplayClass */
    0x70727472u,  /* 'prtr' — cmsSigOutputClass */
    0x6C696E6Bu,  /* 'link' — cmsSigLinkClass */
    0x61627374u,  /* 'abst' — cmsSigAbstractClass */
    0x73706163u,  /* 'spac' — cmsSigColorSpaceClass */
    0x6E6D636Cu   /* 'nmcl' — cmsSigNamedColorClass */
};

static uint32_t SIGS_TABLE[N_SITES * MAX_ARMS];

static void setup_sigs(void) {
    static int initialized = 0;
    if (initialized) return;
    for (size_t i = 0; i < (size_t)N_SITES * MAX_ARMS; i++) {
        SIGS_TABLE[i] = 0x10000000U + (uint32_t)i;
    }
    initialized = 1;
}

static inline uint32_t read_be32(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] << 8)  |  (uint32_t)p[3];
}

__attribute__((noinline))
static int valid_at_site(int site, uint32_t v) {
    int found = 0;
    for (int i = 0; i < N_ARMS_PER_OFFSET; i++) {
        if (v == SIGS_TABLE[site * MAX_ARMS + i]) found = 1;
    }
    return found;
}

/* Sub-type C trap: switch-default arm. Each `cls == L_i` CMP logs
 * L_i as an I2S dict entry — vpc accumulates K=7 valid class literals
 * to substitute into bytes 128-131. vp has no such substitution. */
__attribute__((noinline))
static int valid_class(uint32_t cls) {
    int found = 0;
    for (int i = 0; i < K_VALID; i++) {
        if (cls == CLASS_LITERALS[i]) found = 1;
    }
    return found;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    setup_sigs();

    /* Fixed minimum input: 132 bytes (header + class field). */
    if (size < TRAP_OFFSET + 4) return 0;

    /* === UPSTREAM ANCHOR BLOCK === (same as v6) */
    if (read_be32(data + MAGIC_OFFSET) != MAGIC_VALUE) return 0;
    for (int s = 0; s < N_SITES; s++) {
        if (!valid_at_site(s, read_be32(data + SITE_OFFSETS[s]))) return 0;
    }

    /* === SUB-TYPE C TRAP === */
    /* Trap fires when class field at offset 128 is NOT in valid set.
     * vpc's I2S substitutes one of K=7 valid literals; vp's bytes 128
     * are random. */
    uint32_t cls = read_be32(data + TRAP_OFFSET);
    if (!valid_class(cls)) {
        __builtin_trap();
    }
    return 0;
}
