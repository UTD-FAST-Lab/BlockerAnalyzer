/*
 * network_address_protocol_template_gate  (family: I2S_pro)
 *
 * Synthetic isolation of the cluster's shared mechanism:
 *   I2S (I2SRandReplace) materializes a CONTIGUOUS multi-byte protocol-header
 *   / network-address literal into specific input byte positions in ONE
 *   mutation step, satisfying a single wide equality gate. Fuzzers WITHOUT
 *   I2S (naive, value_profile) must synthesize the same TEMPLATE_BYTES-wide
 *   literal by blind havoc, whose probability of success is ~1/256^N per
 *   exec — so the I2S-vs-blind-search advantage grows as ~1/256^N with the
 *   literal width.
 *
 * Mechanism mapped from the cluster: a Thread/IPv6 fixed address/header
 * template (mesh-local prefix, routing-locator IID anchor, multicast
 * address, next-header template) is the runtime CMP operand; cmplog reads
 * it out of the CmpLogObserver buffer and pastes it into the input. We model
 * that as a single memcmp against a fixed multi-byte constant.
 *
 * ONE compile-time knob:
 *   TEMPLATE_BYTES = width (in bytes) of the contiguous address/template
 *   literal the equality gates on. This is the program-feature axis.
 *
 * Sole objective: __builtin_trap() on the gate-true (full-match) side.
 * No partial-match coverage ladder — the equality is checked as one memcmp,
 * so there are no intermediate edges that would give naive a gradient.
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

#ifndef TEMPLATE_BYTES
#define TEMPLATE_BYTES 8
#endif

/*
 * A fixed multi-byte protocol/address template (32 bytes available). The gate
 * compares the first TEMPLATE_BYTES of it. Bytes are a representative
 * Thread/IPv6-flavoured constant run (mesh-local ULA prefix + FF:FE routing
 * locator IID anchor) so the literal looks like the real runtime operand,
 * but the exact values are immaterial — only the WIDTH that must match is the
 * axis under test.
 */
static const uint8_t kTemplate[32] = {
    0xfd, 0xde, 0xad, 0x00, 0xbe, 0xef, 0x00, 0x00,
    0xff, 0x32, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0xff, 0xfe, 0x00, 0xfc,
    0x78, 0x66, 0x65, 0x5c, 0x77, 0x00, 0x10, 0x11,
};

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < TEMPLATE_BYTES) {
        return 0;
    }

    uint8_t buf[TEMPLATE_BYTES];
    memcpy(buf, data, TEMPLATE_BYTES);

    /* Single wide equality gate — the I2S substitution target. */
    if (memcmp(buf, kTemplate, TEMPLATE_BYTES) == 0) {
        __builtin_trap();
    }

    return 0;
}
