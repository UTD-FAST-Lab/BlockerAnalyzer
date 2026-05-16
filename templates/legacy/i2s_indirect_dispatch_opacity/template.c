/*
 * i2s_indirect_dispatch_opacity — function-pointer-table dispatch is
 * fundamentally invisible to sancov's value-side instrumentation.
 *
 * Replaces the original `i2s_jump_table_opacity` template (refuted on
 * mechanism after disassembly: LibAFL's `__sanitizer_cov_trace_switch`
 * hook iterates over every case literal, so dense switches lowered
 * to jump tables ARE visible to cmp's I2S — they just route through a
 * different sancov entry point. See `templates/legacy/`.
 *
 * Hypothesis. A dispatch implemented as `TABLE[tag](...)` — an array
 * of function pointers indexed by an input-derived tag — emits NO
 * `icmp eq` and NO `switch` at the IR level. The discriminator
 * resolves through an indirect call, not a value comparison. Therefore:
 *   - `__sanitizer_cov_trace_const_cmp{1,2,4,8}` is NOT emitted per arm.
 *   - `__sanitizer_cov_trace_switch` is NOT emitted (no switch in IR).
 *   - cmplog's I2S dictionary never receives a "valid tag" entry.
 *   - value_profile's CMP_MAP gets no Hamming bucket on the dispatch.
 * Only `trace-pc-guard` fires per indirect call — a coverage-only
 * signal with no value-side feedback.
 *
 * Predicted 4-fuzzer signature (decisive shape RBRB):
 *   - naive WINS: throws random bytes at data[0]; hit rate of TARGET = 1/N.
 *     Pays only pc-guard tax.
 *   - cmplog LOSES: same hit rate as naive on the dispatch, BUT pays
 *     extra trace_const_cmp4 hooks emitted in the per-handler noise
 *     compares. cmp's I2S dictionary fills with noise MAGICs that
 *     splice into bytes 4–7 (downstream of the dispatch) — no help.
 *   - value_profile WINS: same as naive (gradient on noise compares
 *     doesn't help reach TARGET; only random walk on data[0] does).
 *   - value_profile_cmplog LOSES: pays both cmp's overhead AND vp's
 *     overhead, no useful signal at the dispatch.
 *
 * Compile-time parameter:
 *   N_HANDLERS ∈ {4, 16, 64, 256} — table size.
 *   Trap rate = 1/N_HANDLERS per execution. cmp/naive ratio should be
 *   roughly FLAT across N (the throughput tax is per-execution, not
 *   per-arm). Absolute crash count falls as 1/N.
 *
 * Real-world instances of this pattern (none in the canonical 5-target
 * DB, but ubiquitous in larger codebases):
 *   - C++ virtual dispatch (vtable lookup, e.g. `obj->parse(...)`).
 *   - C `struct ops`/method tables (Linux VFS, OpenSSL EVP, libuv).
 *   - Computed goto / threaded interpreters (CPython, Lua, V8 fast).
 *   - JIT-emitted code (LuaJIT, V8, eBPF VM after JIT).
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

#ifndef N_HANDLERS
#define N_HANDLERS 64
#endif

#if N_HANDLERS != 4 && N_HANDLERS != 16 && N_HANDLERS != 64 && N_HANDLERS != 256
#error "N_HANDLERS must be one of {4, 16, 64, 256}"
#endif

#define TARGET_TAG (N_HANDLERS / 2)
#define N_NOISE_PER_HANDLER 16

static volatile uint32_t g_sink;

/* Noise MAGICs — these populate cmplog's I2S dictionary when each is
 * compared in handler_noop. They live in input bytes 4–7, NOT byte 0
 * (the dispatch tag), so I2S splice-back never re-pins the dispatch.
 * The point: cmp's instrumentation tax is real (16 trace_const_cmp4
 * hooks per non-target execution) but gives ZERO useful signal toward
 * landing the dispatch on TARGET_TAG. */
static const uint32_t NOISE_MAGICS[16] = {
    0xA0000001u, 0xA0000002u, 0xA0000003u, 0xA0000004u,
    0xA0000005u, 0xA0000006u, 0xA0000007u, 0xA0000008u,
    0xA0000009u, 0xA000000Au, 0xA000000Bu, 0xA000000Cu,
    0xA000000Du, 0xA000000Eu, 0xA000000Fu, 0xA0000010u
};

typedef int (*handler_t)(const uint8_t *, size_t);

/* The non-target handler. Reads bytes 4–7 and runs N_NOISE_PER_HANDLER
 * unhelpful literal-equality compares against the noise table. cmp/vpc
 * pay a trace_const_cmp4 tax per compare; naive/vp don't. */
__attribute__((noinline))
static int handler_noop(const uint8_t *d, size_t s) {
    if (s >= 8) {
        uint32_t v;
        memcpy(&v, d + 4, 4);
        for (int i = 0; i < N_NOISE_PER_HANDLER; i++) {
            if (v == NOISE_MAGICS[i]) g_sink ^= (uint32_t)(i + 1);
        }
    }
    return 0;
}

/* The target handler. Hit only when data[0] % N_HANDLERS == TARGET_TAG.
 * Calls __builtin_trap() unconditionally; no upstream gating. */
__attribute__((noinline))
static int handler_trap(const uint8_t *d, size_t s) {
    (void)d; (void)s;
    __builtin_trap();
    return 0;
}

/* Function-pointer table. Filled at startup via a constructor so the
 * compiler can't statically resolve `TABLE[tag]` — it must remain an
 * indirect call. NO switch, NO icmp on `tag` anywhere. */
static handler_t TABLE[N_HANDLERS];

__attribute__((constructor))
static void init_table(void) {
    for (int i = 0; i < N_HANDLERS; i++) {
        TABLE[i] = (i == TARGET_TAG) ? handler_trap : handler_noop;
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;
    int tag = data[0] % N_HANDLERS;     /* opaque indirect dispatch */
    return TABLE[tag](data, size);
}
