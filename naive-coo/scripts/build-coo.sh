#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COO_DIR="$SCRIPT_DIR/../coo"
podman build -t timekeeper-coo:latest -f "$COO_DIR/Containerfile" "$COO_DIR"
echo "Built timekeeper-coo:latest"
