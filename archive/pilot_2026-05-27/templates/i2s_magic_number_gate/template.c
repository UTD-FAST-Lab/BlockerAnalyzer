/**
 * i2s_magic_number_gate: parameterized harness for the (cmplog, naive)
 * source pair.
 *
 * Hypothesis. cmp's input-to-state (I2S) substitution uses sancov's
 * trace_const_cmp* hooks to log the constant operand of every integer
 * comparison; the mutator then directly substitutes the constant into
 * candidate input positions. naive's random havoc must brute-force the
 * constant byte-by-byte. As constant width grows, naive's hit rate
 * drops geometrically (1/256^N) while cmp's stays ~constant.
 *
 * Predicted dose-response. Effect size grows monotonically in the
 * width of the magic equality check.
 *
 * Compile-time parameter:
 *   MAGIC_BYTES in {1, 2, 4, 8}
 *     1: ~1/256       — trivial for both
 *     2: ~1/65k       — both find but cmp instant
 *     4: ~1/4e9       — naive at edge, cmp instant
 *     8: ~1/1.8e19    — naive impossible, cmp instant
 *
 * The harness emits a single inline integer comparison of width
 * MAGIC_BYTES so the compiler generates exactly one trace_const_cmp
 * hook of that width. No partial-match coverage edges — keeps the
 * mechanism isolated to "I2S substitutes the full constant in one
 * mutation step."
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

#ifndef MAGIC_BYTES
#define MAGIC_BYTES 4
#endif

#if MAGIC_BYTES != 1 && MAGIC_BYTES != 2 && MAGIC_BYTES != 4 && MAGIC_BYTES != 8
#error "MAGIC_BYTES must be one of {1, 2, 4, 8}"
#endif

#if   MAGIC_BYTES == 1
typedef uint8_t  magic_t;
static const magic_t MAGIC = 0xDEu;
#elif MAGIC_BYTES == 2
typedef uint16_t magic_t;
static const magic_t MAGIC = 0xDEADu;
#elif MAGIC_BYTES == 4
typedef uint32_t magic_t;
static const magic_t MAGIC = 0xDEADBEEFu;
#elif MAGIC_BYTES == 8
typedef uint64_t magic_t;
static const magic_t MAGIC = 0xDEADBEEFCAFEBABEull;
#endif

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < MAGIC_BYTES) return 0;

    magic_t v;
    memcpy(&v, data, MAGIC_BYTES);

    if (v == MAGIC) {
        __builtin_trap();
    }
    return 0;
}
