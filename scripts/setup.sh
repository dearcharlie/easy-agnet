#!/usr/bin/env bash
set -euo pipefail

# Easy-Agent Setup Script
# Delegates to install.sh with defaults

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Easy-Agent Setup ==="
echo "[*] Running one-click install..."
exec bash "$SCRIPT_DIR/install.sh" "$@"
