/**
 * opaque_exact_literal_dispatch_gate: parameterized harness for the
 * I2S_pro cluster "single_exact_literal_code_path_unlock".
 *
 * Discovered mechanism (from the brief). Across 12 source branches in
 * harfbuzz / libpng / libxml2 / curl / openthread, a SINGLE all-or-nothing
 * equality / switch CMP tests a contiguous opaque literal of width N bytes
 * (FOURCC table tags 'GDEF'/'GPOS'/'GSUB', PNG chunk types 'eXIf'/'hIST',
 * URL scheme 'file', protocol token 'pop3', attribute name 'xmlns', the
 * UTF-8 BOM 0xEF 0xBB 0xBF, a single switch byte 'q', an IHDR color_type
 * 0x02, an IPv6 next-header enum code). Satisfying that one CMP routes
 * execution into a specific handler / case arm. cmplog and
 * value_profile_cmplog carry I2SRandReplace, which lifts the literal out
 * of the CmpLogObserver buffer and splices it into the input in a single
 * mutation step. naive and value_profile lack I2SRandReplace; naive must
 * brute-force the literal by random havoc and value_profile's Hamming
 * CMP_MAP gradient is flat on an opaque equality (every wrong value is
 * equidistant), so both block.
 *
 * Hypothesis / dose-response. The I2S-vs-blind-search gap is ~1/256^N:
 * negligible at N=1, intractable for the has_axis-lacking arms by N>=4.
 * Effect size grows monotonically with the literal width N.
 *
 * Compile-time parameter (the SOLE knob = the program-feature axis):
 *   GATE_BYTES = width in bytes of the opaque literal the equality gates on.
 *     Swept over {1, 2, 3, 4, 5, 8} — spanning every width seen in the
 *     cluster (1-byte switch/enum/color_type, 3-byte BOM, 4-byte FOURCC/
 *     scheme, 5-byte 'xmlns') plus an 8-byte extreme.
 *
 * Isolation. The gate is a SINGLE exact comparison (memcmp == 0) of the
 * whole width; __builtin_trap() on the gate-true side is the only
 * objective. No partial-match coverage ladder — the literal is opaque,
 * exactly as in the source branches, so no per-byte gradient edge leaks
 * to give the lacks_axis arms a foothold.
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

#ifndef GATE_BYTES
#define GATE_BYTES 4
#endif

#if GATE_BYTES < 1 || GATE_BYTES > 8
#error "GATE_BYTES must be in [1, 8]"
#endif

/* Opaque literal of exactly GATE_BYTES bytes. The values are arbitrary,
 * non-structured constants (an "opaque magic word"): no exploitable
 * sub-structure, mirroring the FOURCC/BOM/scheme literals in the cluster.
 * Only the first GATE_BYTES are compared, so changing the knob changes the
 * compiled comparison width — the knob is live. */
static const uint8_t GATE_LITERAL[8] = {
    0x47, 0x44, 0x45, 0x46, 0x78, 0xEF, 0xBB, 0xBF
};

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < GATE_BYTES) return 0;

    uint8_t buf[GATE_BYTES];
    memcpy(buf, data, GATE_BYTES);

    /* Single all-or-nothing equality on the full GATE_BYTES-wide literal.
     * The compiler lowers this to a fixed-width constant comparison that
     * sancov's trace_const_cmp / weak-hook-memcmp instrumentation logs,
     * so I2SRandReplace can substitute the literal in one step. */
    if (memcmp(buf, GATE_LITERAL, GATE_BYTES) == 0) {
        __builtin_trap();
    }
    return 0;
}
