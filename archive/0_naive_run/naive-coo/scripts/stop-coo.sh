#!/bin/bash
set -euo pipefail

if ! podman ps --format '{{.Names}}' | grep -q '^timekeeper-coo$'; then
    echo "COO is not running."
    exit 0
fi

podman stop timekeeper-coo
echo "COO stopped. RAM released."
echo "To restart: scripts/launch-coo.sh"
