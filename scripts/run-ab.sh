#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Setting up network ==="
"$SCRIPT_DIR/setup-network.sh"

echo ""
echo "=== Building qwen-think ==="
"$SCRIPT_DIR/build.sh" qwen-think

echo ""
echo "=== Building qwen-nothink ==="
"$SCRIPT_DIR/build.sh" qwen-nothink

echo ""
echo "=== Building qwen-hermes ==="
"$SCRIPT_DIR/build.sh" qwen-hermes

echo ""
echo "=== Launching qwen-think ==="
"$SCRIPT_DIR/launch.sh" qwen-think

echo ""
echo "=== Launching qwen-nothink ==="
"$SCRIPT_DIR/launch.sh" qwen-nothink

echo ""
echo "=== Launching qwen-hermes ==="
"$SCRIPT_DIR/launch.sh" qwen-hermes

echo ""
echo "=== All three experiments running ==="
echo "Think logs:    podman logs -f timekeeper-qwen-think"
echo "No-think logs: podman logs -f timekeeper-qwen-nothink"
echo "Hermes logs:   podman logs -f timekeeper-qwen-hermes"
