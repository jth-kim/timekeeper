#!/bin/bash
set -euo pipefail
EXPERIMENT="${1:?Usage: $0 <experiment-dir>  (e.g. qwen-think)}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$SCRIPT_DIR/.."
COO_DIR="$REPO_DIR/$EXPERIMENT/coo"
IMAGE_NAME="timekeeper-${EXPERIMENT}:latest"

if [ ! -d "$COO_DIR" ]; then
    echo "Error: $COO_DIR does not exist"
    exit 1
fi

podman build -t "$IMAGE_NAME" -f "$COO_DIR/Containerfile" "$COO_DIR"
echo "Built $IMAGE_NAME"
