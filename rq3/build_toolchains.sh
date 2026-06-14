#!/usr/bin/env bash
# build_toolchains.sh — build the 4 RQ3 fuzzer toolchain images from OUR vendored
# Dockerfiles (rq3/toolchain/Dockerfile.<fuzzer>), not FuzzBench's directly.
#
# Why we vendor: the stock FuzzBench builders pin a fuzzer commit + Rust nightly
# that drift against crates.io (libafl: latest crates need a newer Rust than the
# pinned nightly). Owning the recipe lets us pin the base-builder digest, purge a
# preinstalled Rust, and build LibAFL `--locked`. afl/hong/libfuzzer are FuzzBench's
# recipe verbatim + the pinned base; libafl carries the bitrot fixes.
#
# Usage:  ./rq3/build_toolchains.sh [fuzzer ...]   (default: all 4)
set -euo pipefail
DIR="$(cd "$(dirname "$0")/toolchain" && pwd)"
FUZZERS=("${@:-aflplusplus honggfuzz libfuzzer libafl}")
for f in ${FUZZERS[@]}; do
  img="rq3-toolchain-$f"
  if docker image inspect "$img" >/dev/null 2>&1; then echo "skip $img (cached)"; continue; fi
  echo "=== build $img ==="
  docker build -t "$img" -f "$DIR/Dockerfile.$f" "$DIR"
done
echo "toolchains:"; for f in ${FUZZERS[@]}; do
  docker image inspect rq3-toolchain-$f >/dev/null 2>&1 && echo "  $f OK" || echo "  $f MISSING"
done
