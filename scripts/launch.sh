#!/bin/bash
set -euo pipefail
EXPERIMENT="${1:?Usage: $0 <experiment-dir>  (e.g. qwen-think, qwen-think-noselfmod, qwen-hermes, qwen-hermes-noselfmod)}"
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

# Prefer experiment-local config (for isolated self-mod runs), fallback to shared root config.
CONFIG_SRC="$TK_DIR/config"
if [ ! -d "$CONFIG_SRC" ]; then
    CONFIG_SRC="$REPO_DIR/config"
fi

# Mount config writable only when SELF_MOD_ENABLED=true in the experiment .env.
SELF_MOD_ENABLED="$(grep -E '^SELF_MOD_ENABLED=' "$TK_DIR/.env" | tail -1 | cut -d= -f2- | tr -d '[:space:]' || true)"
CONFIG_MOUNT_MODE="ro"
if [ "${SELF_MOD_ENABLED,,}" = "true" ]; then
    CONFIG_MOUNT_MODE="rw"
fi

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
    -v "$CONFIG_SRC:/data/config:${CONFIG_MOUNT_MODE},Z" \
    -v "$TK_DIR/shared/workspace:/data/workspace:Z" \
    $EXTRA_VOLS \
    "$IMAGE_NAME"

echo "$CONTAINER_NAME launched."
echo "Logs:  podman logs -f $CONTAINER_NAME"
echo "State: $TK_DIR/shared/state/coo_state.json"
