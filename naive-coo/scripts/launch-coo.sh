#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TK_DIR="$SCRIPT_DIR/.."

mkdir -p "$TK_DIR/shared/logs" "$TK_DIR/shared/state" "$TK_DIR/shared/memory" "$TK_DIR/shared/workspace"

podman stop timekeeper-coo 2>/dev/null || true
podman rm timekeeper-coo 2>/dev/null || true

podman run -d \
    --name timekeeper-coo \
    --network timekeeper-internal \
    --restart unless-stopped \
    --env-file "$TK_DIR/.env" \
    -v "$TK_DIR/shared/logs:/data/logs:Z" \
    -v "$TK_DIR/shared/state:/data/state:Z" \
    -v "$TK_DIR/shared/memory:/data/memory:Z" \
    -v "$TK_DIR/config:/data/config:Z" \
    -v "$TK_DIR/shared/workspace:/data/workspace:Z" \
    timekeeper-coo:latest

echo "COO launched."
echo "Logs:  podman logs -f timekeeper-coo"
echo "State: $TK_DIR/shared/state/coo_state.json"
