#!/bin/bash
set -euo pipefail
EXPERIMENT="${1:?Usage: $0 <experiment-dir>  (e.g. qwen-think, qwen-nothink, qwen-hermes)}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$SCRIPT_DIR/.."
TK_DIR="$REPO_DIR/$EXPERIMENT"
CONTAINER_NAME="timekeeper-${EXPERIMENT}"
IMAGE_NAME="timekeeper-${EXPERIMENT}:latest"

if [ ! -d "$TK_DIR" ]; then
    echo "Error: $TK_DIR does not exist"
    exit 1
fi

if [ ! -f "$TK_DIR/.env" ]; then
    echo "Error: $TK_DIR/.env not found. Copy from .env.example and fill in credentials."
    exit 1
fi

mkdir -p "$TK_DIR/shared/logs" "$TK_DIR/shared/state" "$TK_DIR/shared/memory" "$TK_DIR/shared/workspace"

# Extra volume mounts per experiment
EXTRA_VOLS=""
if [ -d "$TK_DIR/shared/hermes" ]; then
    mkdir -p "$TK_DIR/shared/hermes"
    EXTRA_VOLS="-v $TK_DIR/shared/hermes:/data/hermes:Z"
fi

podman stop "$CONTAINER_NAME" 2>/dev/null || true
podman rm "$CONTAINER_NAME" 2>/dev/null || true

podman run -d \
    --name "$CONTAINER_NAME" \
    --network timekeeper-internal \
    --restart unless-stopped \
    --env-file "$TK_DIR/.env" \
    -v "$TK_DIR/shared/logs:/data/logs:Z" \
    -v "$TK_DIR/shared/state:/data/state:Z" \
    -v "$TK_DIR/shared/memory:/data/memory:Z" \
    -v "$REPO_DIR/config:/data/config:ro,Z" \
    -v "$TK_DIR/shared/workspace:/data/workspace:Z" \
    $EXTRA_VOLS \
    "$IMAGE_NAME"

echo "$CONTAINER_NAME launched."
echo "Logs:  podman logs -f $CONTAINER_NAME"
echo "State: $TK_DIR/shared/state/coo_state.json"
