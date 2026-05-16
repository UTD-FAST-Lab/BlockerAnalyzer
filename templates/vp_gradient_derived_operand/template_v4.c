/**
 * vp_gradient_derived_operand v4: canonical demonstrator of VP's CMP_MAP
 * gradient on a single literal-equality CMP whose operand is read directly
 * from input bytes (no transform, no chain).
 *
 * Why v4. v1 (32-bit equality + bijective XOR derivation) refuted because
 * single-CMP gradient too narrow at 32-bit. v2 (chain of K narrow CMPs)
 * reproduced but tests a structurally different feature (chain compounding)
 * — promoted to its own template. v3 (64-bit equality + bijective XOR
 * derivation) refuted: even ONE XOR layer destroys VP's gradient
 * empirically in LibAFL despite the math saying it should propagate.
 *
 * v4 returns the synthetic to the actual mechanism the 13 real-target
 * branches in branch_index.json share: a literal-equality CMP whose
 * operand is a plain bytewise read of input bytes, with NO derivation
 * layer between the read and the CMP. This matches:
 *   - mbedtls ssl_tls12_client.c:1266 br 378 (LEADER) — 2-byte tls_version
 *     range check; vp 8/10 vs naive 0/10 at n=10
 *   - mbedtls ssl_msg.c:5824 br 371 — `tls_version == 0x0302` equality
 *   - lcms cmsio0.c:752/753/754 br 62/63/65 — validDeviceClass() 7-arm
 *     FOURCC switch (each arm is a 4-byte literal-equality CMP)
 *   - lcms cmsxform.c:1025 br 349 — `cls == cmsSigNamedColorClass` FOURCC
 *   - sqlite3 br 1898/1754/1808/1572 — VDBE opcode-dispatch switch arms
 *   - libpcap grammar.c:1922 br 660 — bison yyparse reduction case
 *   - 13 branches total across 4 targets; ALL plain read-then-compare.
 *
 * None of these branches have any bijective transform between the input
 * read and the CMP. The "derived via XOR-mask / base64 / ASN.1 DER"
 * framing in v1's spec was a theoretical extrapolation that v3 empirically
 * refuted — at any depth ≥ 1, even bijective XOR layers destroy VP's
 * gradient in LibAFL's actual implementation. The actual mechanism is
 * simpler: VP's per-CMP Hamming-distance bucket retains seeds that get
 * progressively closer to the literal operand via byte-level mutations
 * — but the input bytes must reach the CMP without intervening transforms.
 *
 * Knob: WIDTH ∈ {1, 2, 4, 8} bytes — width of the equality CMP operand.
 *   Real-target regimes:
 *     mbedtls br378/br371: WIDTH=2 (16-bit version field)
 *     lcms br62/63/65/349, sqlite VDBE arms: WIDTH=4 (32-bit FOURCC / opcode)
 *     no real branch with WIDTH=1 or WIDTH=8 — included to bracket the
 *     dose-response curve and find where VP's gradient bites cleanly.
 *
 * Predicted dose-response (vp vs naive):
 *   - WIDTH=1: BOTH high. naive 1/256 per random attempt → ~9k crashes/600s.
 *     vp not much faster — gradient has only 9 buckets, naive's random hit
 *     rate competes. vp/naive ≈ 1-3×.
 *   - WIDTH=2: vp WINS BIG. naive 1/65536 → ~36 crashes/trial. vp gradient
 *     walks 17 buckets cleanly → expect 1000s of crashes. vp/naive ~30-100×.
 *     This is the mbedtls br378 corroborating dose.
 *   - WIDTH=4: vp WINS but absolute count drops. naive 1/2^32 → ~0. vp
 *     gradient walks 33 buckets — borderline. Either reproduces (vp wins
 *     decisively) or refutes (gradient too narrow at 32-bit, which would
 *     repeat v1's diagnosis but on read-then-compare instead of derivation).
 *     This is the lcms FOURCC / VDBE opcode regime.
 *   - WIDTH=8: tests the limits. naive 1/2^64 → 0. vp 65 buckets — v3 d=0
 *     showed only ~2× advantage at this width; v4 should reproduce that or
 *     do slightly better (no derivation overhead).
 *
 * Verdict criteria:
 *   - reproduced_v4: vp/naive ratio > 10× at WIDTH=2 AND vp resolves at
 *     WIDTH ∈ {2, 4} consistently (≥3 of 5 trials with crashes > 0).
 *   - reproduced_v4_in_part: vp wins at WIDTH=2 only; degrades at WIDTH=4.
 *   - refuted_v4: vp ≈ naive at WIDTH=2 (would mean even the canonical
 *     mechanism fails — surprising given mbedtls br378's 8/10 vs 0/10 real-
 *     target evidence; would point to some libafl_fuzzbench-specific config
 *     issue rather than a fundamental gradient failure).
 */

#include <stdint.h>
#include <stddef.h>

#ifndef WIDTH
#define WIDTH 2
#endif

#if WIDTH == 1
typedef uint8_t  cmp_t;
#define TARGET ((cmp_t)0x42u)
#elif WIDTH == 2
typedef uint16_t cmp_t;
#define TARGET ((cmp_t)0x0342u)
#elif WIDTH == 4
typedef uint32_t cmp_t;
#define TARGET ((cmp_t)0xCDB60342u)
#elif WIDTH == 8
typedef uint64_t cmp_t;
#define TARGET ((cmp_t)0xF52E7A91CDB60342ULL)
#else
#error "WIDTH must be one of {1, 2, 4, 8}"
#endif

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < WIDTH) return 0;

    /* Plain bytewise little-endian read. clang -O2 collapses this to a
     * single load instruction at WIDTH ∈ {1,2,4,8}. NO derivation. */
    cmp_t v = 0;
    for (int i = 0; i < WIDTH; i++) {
        v |= ((cmp_t)data[i]) << (8 * i);
    }

    /* Single literal-equality CMP at the trap. One trace_const_cmp_N
     * hook fires here per execution (where N matches WIDTH). VP's
     * CMP_MAP records the smallest Hamming distance ever seen between
     * v and TARGET, retaining the seed achieving each new best-distance
     * bucket. The gradient walks input bytes toward TARGET byte-by-byte. */
    if (v == TARGET) {
        __builtin_trap();
    }

    return 0;
}
