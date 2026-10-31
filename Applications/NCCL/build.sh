#!/usr/bin/env bash
set -euo pipefail

CUDA_HOME="${CUDA_HOME:-/usr/local/cuda}"
NCCL_DIR="$(pwd)/nccl"
TESTS_DIR="$(pwd)/nccl-tests"

echo "--- Step 1: Building NCCL ---"
cd "$NCCL_DIR"
make -j 4 src.build CUDA_HOME="$CUDA_HOME"

echo "--- Step 2: Building nccl-tests ---"
cd "$TESTS_DIR"
make clean
make -j 4 CUDA_HOME="$CUDA_HOME" NCCL_HOME="$NCCL_DIR/build"

echo "Build complete! Test binaries are ready in ./nccl-tests/build/"
