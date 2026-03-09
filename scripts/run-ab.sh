#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Setting up network ==="
"$SCRIPT_DIR/setup-network.sh"

echo ""
echo "=== Building qwen-think ==="
"$SCRIPT_DIR/build.sh" qwen-think

echo ""
echo "=== Building qwen-think-noselfmod ==="
"$SCRIPT_DIR/build.sh" qwen-think-noselfmod

echo ""
echo "=== Building qwen-hermes ==="
"$SCRIPT_DIR/build.sh" qwen-hermes

echo ""
echo "=== Building qwen-hermes-noselfmod ==="
"$SCRIPT_DIR/build.sh" qwen-hermes-noselfmod

echo ""
echo "=== Launching qwen-think ==="
"$SCRIPT_DIR/launch.sh" qwen-think

echo ""
echo "=== Launching qwen-think-noselfmod ==="
"$SCRIPT_DIR/launch.sh" qwen-think-noselfmod

echo ""
echo "=== Launching qwen-hermes ==="
"$SCRIPT_DIR/launch.sh" qwen-hermes

echo ""
echo "=== Launching qwen-hermes-noselfmod ==="
"$SCRIPT_DIR/launch.sh" qwen-hermes-noselfmod

echo ""
echo "=== All four experiments running ==="
echo "Think logs:    podman logs -f timekeeper-qwen-think"
echo "Think no-self-mod logs: podman logs -f timekeeper-qwen-think-noselfmod"
echo "Hermes logs:   podman logs -f timekeeper-qwen-hermes"
echo "Hermes no-self-mod logs: podman logs -f timekeeper-qwen-hermes-noselfmod"
