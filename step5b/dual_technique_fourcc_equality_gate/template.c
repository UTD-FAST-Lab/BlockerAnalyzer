/*
 * dual_technique_fourcc_equality_gate
 *
 * Cluster (independent family): a single contiguous N-byte FOURCC equality
 * gate that BOTH I2S (cmplog direct operand substitution) AND value_profile
 * (Hamming-gradient ascent) independently clear, while naive cannot.
 *
 * Models the libpng_7254 sPLT blocker: `chunk_name == png_sPLT`, the exact
 * 32-bit equality `if (read_u32(input+4) == 0x73504c54) trap;` sketched in the
 * member's falsifiability.would_be_refuted_by.
 *
 * The sole objective is the equality gate. There are NO partial-match coverage
 * edges (no per-byte ladder): naive must hit the full constant by blind chance
 * (~1/256^GATE_BYTES), while cmplog substitutes the logged operand directly and
 * value_profile's CMP_MAP buckets the wide compare's operand distance — so it
 * climbs the gradient. Both winners clear it via distinct mechanisms.
 *
 * ONE compile-time knob:
 *   GATE_BYTES = width of the magic constant in bytes (the program-feature axis).
 *                The I2S/VP-vs-naive gap is ~1/256^GATE_BYTES.
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

/* --- single compile-time knob: constant width in bytes --- */
#ifndef GATE_BYTES
#define GATE_BYTES 4
#endif

/*
 * Magic constant truncated/extended to GATE_BYTES.
 * Low bytes are the png_sPLT FOURCC 0x73504c54 ('s','P','L','T' in stream
 * order 0x73 0x50 0x4c 0x54); higher bytes pad the value out to 8 bytes so any
 * GATE_BYTES in {1,2,4,8} compiles. We compare the low GATE_BYTES bytes.
 */
#define MAGIC_FULL 0x4847464573504c54ULL  /* low 4 bytes = 0x73504c54 (sPLT) */

/* Offset of the gate operand in the input (mimics 4-byte length prefix). */
#define GATE_OFFSET 4

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    /* Need the length-prefix offset plus the full constant width. */
    if (size < GATE_OFFSET + GATE_BYTES)
        return 0;

    /* Load GATE_BYTES contiguous bytes from the input into a wide integer. */
    uint64_t got = 0;
    memcpy(&got, data + GATE_OFFSET, GATE_BYTES);

    /* Mask the magic constant down to GATE_BYTES so the comparison width
     * scales with the knob — the single source of difficulty. */
#if GATE_BYTES >= 8
    uint64_t magic = (uint64_t)MAGIC_FULL;
#else
    uint64_t magic = ((uint64_t)MAGIC_FULL) & (((uint64_t)1 << (GATE_BYTES * 8)) - 1);
#endif

    /* The sole objective: one exact equality gate, no partial-match edges. */
    if (got == magic) {
        __builtin_trap();
    }

    return 0;
}
