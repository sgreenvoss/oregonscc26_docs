#!/usr/bin/env bash
set -euo pipefail

# ---- Configuration ----
CUDA_HOME="${CUDA_HOME:-/usr/local/cuda}"
NCCL_DIR="${NCCL_DIR:-$(pwd)/nccl}"
TESTS_DIR="${TESTS_DIR:-$(pwd)/nccl-tests}"

# Pinned versions (match the report)
NCCL_TAG="${NCCL_TAG:-v2.32.3-1}"   #
TESTS_REV="${TESTS_REV:-afd59ab}"   #

# H100 = compute capability 9.0
GENCODE="-gencode=arch=compute_90,code=sm_90"


if [ ! -d "$NCCL_DIR" ] || [ ! -d "$TESTS_DIR" ]; then
  echo "Clone the repositories first:"
  echo "  git clone https://github.com/NVIDIA/nccl.git"
  echo "  git clone https://github.com/NVIDIA/nccl-tests.git"
  exit 1
fi
[ -x "$CUDA_HOME/bin/nvcc" ] || { echo "nvcc not found in $CUDA_HOME/bin"; exit 1; }

# ---- Step 0: pin versions ----
echo "--- Step 0: Pinning versions ---"
git -C "$NCCL_DIR"  checkout "$NCCL_TAG"
git -C "$TESTS_DIR" checkout "$TESTS_REV"
echo "NCCL:       $(git -C "$NCCL_DIR" describe --tags --always)"
echo "nccl-tests: $(git -C "$TESTS_DIR" log -1 --format=%h)"


echo "--- Step 1: Building NCCL ---"
cd "$NCCL_DIR"
make clean
make -j 4 src.build CUDA_HOME="$CUDA_HOME" NVCC_GENCODE="$GENCODE"


echo "--- Step 2: Building nccl-tests ---"
cd "$TESTS_DIR"
make clean
make -j 4 CUDA_HOME="$CUDA_HOME" NCCL_HOME="$NCCL_DIR/build" NVCC_GENCODE="$GENCODE"


export LD_LIBRARY_PATH="$NCCL_DIR/build/lib:${LD_LIBRARY_PATH:-}"

echo "--- Step 3: Verification ---"
ldd "$TESTS_DIR/build/broadcast_perf" | grep -i nccl
"$TESTS_DIR/build/broadcast_perf" -b 8 -e 8 -g 2 2>&1 | grep -i "nccl-headers" || true

echo
echo "Build complete. Binaries are in $TESTS_DIR/build/"
echo "In every new shell, before running benchmarks:"
echo "  export LD_LIBRARY_PATH=$NCCL_DIR/build/lib:\$LD_LIBRARY_PATH"