// Template: i2s_multi_arm_dictionary_roulette_crowds_target
// Family: I2S_anti  (the I2S technique HURTS here)
//
// Cluster mechanism (from brief, member harfbuzz_9459 / Myanmar Ragel switch):
//   A K-way dispatch (switch) selects an arm by matching a 4-byte selector word
//   against one of K distinct case constants. Exactly ONE arm (the TARGET) traps;
//   the other K-1 are "sister" arms that just consume the input and return.
//
//   * value_profile (WINNER): its CMP_MAP records a per-comparison Hamming-distance
//     bucket. Each input whose selector word is closer (in value) to the TARGET
//     constant than any previously seen input is preserved as corpus, giving a
//     monotone gradient that climbs to the target arm regardless of K.
//
//   * value_profile_cmplog (LOSER): it has the SAME CMP_MAP gradient, but ALSO logs
//     every one of the K case constants into its input-to-state (I2S) substitution
//     dictionary. Per-mutation I2S draws uniformly across that K-entry dictionary
//     and splices a (usually wrong) sister-arm constant straight into the selector
//     bytes. Whichever sister arm gains corpus residency first then monocultures the
//     queue. The chance any single I2S draw is the TARGET constant is ~1/K, so the
//     larger K is, the more the dictionary roulette overrides the working gradient
//     and crowds the search away from the target arm. Pure loss on top of vp.
//
// Knob = K = ARM_COUNT = number of competing case constants / switch arms.
//   Larger K  =>  vpc's I2S roulette degrades more relative to vp's gradient.
//   Predicted: value_profile > value_profile_cmplog, gap grows with ARM_COUNT.
//
// Honesty caveat: the vp-vs-vpc roulette dynamic is an emergent corpus-scheduling
// effect; a micro-harness can populate the K-entry I2S dictionary and provide the
// per-arm CMP_MAP gradient, but it cannot guarantee the scheduler actually
// monocultures into a sister arm. See feature_spec.json:hypothesis.tradeoff_observation.

#include <stdint.h>
#include <stddef.h>
#include <string.h>

// ---- the single program-feature knob ----------------------------------------
// K = number of competing switch arms (= number of distinct 4-byte case
// constants the I2S dictionary gets loaded with). Exactly one of them traps.
#ifndef ARM_COUNT
#define ARM_COUNT 4
#endif

#if (ARM_COUNT) < 2
#error "ARM_COUNT must be >= 2 (need at least one sister arm to compete with the target)"
#endif

// Distinct, well-separated 32-bit case constants, one per arm. Index 0 is the
// TARGET arm; indices 1..K-1 are sister arms that the I2S dictionary also carries.
// Spacing the constants by a large stride keeps each arm's CMP_MAP comparison an
// independent gradient bucket (no accidental partial-match edges between arms).
static const uint32_t ARM_CONST[16] = {
    0x5A6B7C8Du, // arm 0  = TARGET (the trap)
    0x11223344u, // arm 1
    0x22446688u, // arm 2
    0x3366AACCu, // arm 3
    0x4488CC00u, // arm 4
    0x55AA0055u, // arm 5
    0x66CC1166u, // arm 6
    0x77EE2277u, // arm 7
    0x18293A4Bu, // arm 8
    0x29304152u, // arm 9
    0x3A4B5C6Du, // arm 10
    0x4B5C6D7Eu, // arm 11
    0x5C6D7E8Fu, // arm 12
    0x6D7E8F90u, // arm 13
    0x7E8F90A1u, // arm 14
    0x0F1E2D3Cu, // arm 15
};

static volatile uint32_t g_sink;

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // selector word (4 bytes) chooses the arm; this is the operand the CMP_MAP
    // gradient climbs and the slot the I2S dictionary substitutes into.
    if (size < 4)
        return 0;

    uint32_t sel;
    memcpy(&sel, data, 4);

    // K-way dispatch. The switch makes all K case constants visible to the
    // CmpLog instrumentation, so value_profile_cmplog loads all K into its I2S
    // dictionary and draws uniformly across them (~1/K target probability).
    // value_profile sees each comparison as an independent CMP_MAP bucket and
    // climbs the per-arm gradient toward the target.
    switch (sel) {
        case 0x5A6B7C8Du: // == ARM_CONST[0], the TARGET arm
            __builtin_trap();          // SOLE objective
            break;
#if (ARM_COUNT) > 1
        case 0x11223344u: g_sink += 1; break;
#endif
#if (ARM_COUNT) > 2
        case 0x22446688u: g_sink += 2; break;
#endif
#if (ARM_COUNT) > 3
        case 0x3366AACCu: g_sink += 3; break;
#endif
#if (ARM_COUNT) > 4
        case 0x4488CC00u: g_sink += 4; break;
#endif
#if (ARM_COUNT) > 5
        case 0x55AA0055u: g_sink += 5; break;
#endif
#if (ARM_COUNT) > 6
        case 0x66CC1166u: g_sink += 6; break;
#endif
#if (ARM_COUNT) > 7
        case 0x77EE2277u: g_sink += 7; break;
#endif
#if (ARM_COUNT) > 8
        case 0x18293A4Bu: g_sink += 8; break;
#endif
#if (ARM_COUNT) > 9
        case 0x29304152u: g_sink += 9; break;
#endif
#if (ARM_COUNT) > 10
        case 0x3A4B5C6Du: g_sink += 10; break;
#endif
#if (ARM_COUNT) > 11
        case 0x4B5C6D7Eu: g_sink += 11; break;
#endif
#if (ARM_COUNT) > 12
        case 0x5C6D7E8Fu: g_sink += 12; break;
#endif
#if (ARM_COUNT) > 13
        case 0x6D7E8F90u: g_sink += 13; break;
#endif
#if (ARM_COUNT) > 14
        case 0x7E8F90A1u: g_sink += 14; break;
#endif
#if (ARM_COUNT) > 15
        case 0x0F1E2D3Cu: g_sink += 15; break;
#endif
        default:
            g_sink += sel; // non-matching selector: no arm, just churn
            break;
    }

    return 0;
}
