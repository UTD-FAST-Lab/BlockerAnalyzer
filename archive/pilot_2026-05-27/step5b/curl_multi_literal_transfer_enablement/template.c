/*
 * Synthetic harness for feature cluster: curl_multi_literal_transfer_enablement
 * (mechanism_family: I2S_pro; mechanism_label: chained_protocol_literal_transfer_state)
 *
 * Cluster mechanism (from brief): in curl's URL/HTTP parsers, I2S satisfies one
 * or more SEQUENTIAL opaque multi-byte literal CMPs (scheme 'pop3+-', host
 * '127.0.0.1', 'HTTP/', header tokens). Only after every literal gate clears
 * does a DOWNSTREAM derived-state condition (byte counters, header-line
 * counters, linked-list head pointer, socket revents flag) become
 * nonzero/non-null and the blocked branch flips. The blocker is that derived
 * state, not the literal compare itself.
 *
 * This harness isolates exactly that shape: a CHAIN of N sequential opaque
 * 4-byte literal gates that the input must clear in order. Each cleared gate
 * advances a "transfer-state" counter; only when ALL N gates are cleared (state
 * fully advanced) does the downstream condition fire __builtin_trap(). The
 * literal of gate i is reached only if gate i-1 already matched, so the gates
 * are genuinely sequential (the i-th literal is "downstream" of the prior).
 *
 * The single program-feature axis is the CHAIN LENGTH: the number of sequential
 * opaque multi-byte literal gates the input must clear before the trap. I2S
 * (cmplog / value_profile_cmplog) substitutes each logged literal operand into
 * the input one gate at a time, so its time-to-clear scales ~linearly in the
 * chain length; blind search (naive / value_profile) must land all 4*N literal
 * bytes by chance, a ~1/256^(4*N) collapse. The I2S-vs-blind-search advantage
 * therefore grows with chain length -> the sole knob is LITERAL_CHAIN_LEN.
 *
 * No partial-match coverage ladder is exposed across the WHOLE chain: the trap
 * is the only objective and fires only on full-chain success. (The per-gate
 * sequencing is the mechanism being modeled, not a coverage gradient handed to
 * naive -- each gate is a single exact 4-byte equality, which CMP_MAP cannot
 * climb into without the I2S substitution.)
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

/* ---- ONE compile-time knob: number of sequential literal gates ---- */
#ifndef LITERAL_CHAIN_LEN
#define LITERAL_CHAIN_LEN 1
#endif

/* Each gate is one opaque 4-byte literal the input must match at its slot. */
#define GATE_WIDTH 4

/* A pool of distinct opaque 4-byte literals, one consumed per chain step.
 * Mirrors the cluster's real tokens: scheme/host/HTTP-prefix/header fragments. */
static const uint8_t GATE_LITERALS[8][GATE_WIDTH] = {
    { 'p', 'o', 'p', '3' },   /* scheme            */
    { '1', '2', '7', '.' },   /* host prefix       */
    { 'H', 'T', 'T', 'P' },   /* response framing  */
    { 'R', 'e', 't', 'r' },   /* header token      */
    { 'T', 'r', 'a', 'n' },   /* header token      */
    { 'L', 'o', 'c', 'a' },   /* header token      */
    { 'C', 'o', 'n', 't' },   /* header token      */
    { 'A', 'c', 'c', 'e' },   /* header token      */
};

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  /* Each gate owns its own GATE_WIDTH-byte slot in the input. */
  if (size < (size_t)(LITERAL_CHAIN_LEN * GATE_WIDTH))
    return 0;

  uint8_t buf[8 * GATE_WIDTH];
  memcpy(buf, data, (size_t)(LITERAL_CHAIN_LEN * GATE_WIDTH));

  /* Downstream transfer-state, advanced one step per cleared literal gate.
   * This is the derived state the real blocker keys on (counter/head/flag). */
  int transfer_state = 0;

  /* Sequential chain: gate i is only evaluated once gate i-1 has matched,
   * so the i-th literal is genuinely downstream of the prior CMP. */
  for (int i = 0; i < LITERAL_CHAIN_LEN; i++) {
    if (memcmp(buf + i * GATE_WIDTH, GATE_LITERALS[i], GATE_WIDTH) != 0)
      break;                 /* first failed gate stops the chain */
    transfer_state++;        /* this literal cleared -> advance state */
  }

  /* Downstream derived-state condition: fires only when the FULL chain
   * cleared (transfer fully enabled). Sole objective. */
  if (transfer_state == LITERAL_CHAIN_LEN)
    __builtin_trap();

  return 0;
}
