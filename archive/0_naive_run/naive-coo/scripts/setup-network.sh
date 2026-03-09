#!/bin/bash
set -euo pipefail
NETWORK="timekeeper-internal"
if podman network exists "$NETWORK" 2>/dev/null; then
    echo "Network '$NETWORK' already exists."
else
    podman network create "$NETWORK"
    echo "Created network '$NETWORK'."
fi
