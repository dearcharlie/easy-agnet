#!/usr/bin/env bash
set -euo pipefail

# Easy-Agent Install Script
# One-click install of Hermes Agent + Easy-Agent + Novel Skills

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

HERMES_DEFAULT_VERSION="v2026.5.7"  # Hermes Agent v0.13.0
HERMES_VERSION=""
UPGRADE=false

print_usage() {
  echo "Usage: bash install.sh [OPTIONS]"
  echo ""
  echo "Options:"
  echo "  --upgrade                  Upgrade existing installation"
  echo "  --hermes-version VERSION   Pin Hermes Agent to a specific version/tag"
  echo "  --help                     Show this help"
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --upgrade) UPGRADE=true; shift ;;
    --hermes-version) HERMES_VERSION="$2"; shift 2 ;;
    --help) print_usage ;;
    *) echo "Unknown option: $1"; print_usage ;;
  esac
done

echo "=== Easy-Agent Install ==="

# ---------- Hermes Agent ----------
# Hermes uses its own official install script (not on PyPI)
echo "[*] Installing Hermes Agent..."

HERMES_INSTALL_URL="https://raw.githubusercontent.com/NousResearch/hermes-agent/${HERMES_VERSION:-$HERMES_DEFAULT_VERSION}/scripts/install.sh"

if command -v hermes &>/dev/null && ! $UPGRADE; then
  echo "[✓] Hermes Agent already installed: $(hermes --version 2>/dev/null || echo 'ok')"
elif command -v hermes &>/dev/null && $UPGRADE; then
  echo "[*] Upgrading Hermes Agent..."
  bash <(curl -fsSL "$HERMES_INSTALL_URL") 2>&1 | tail -5
  echo "[✓] Hermes Agent upgraded"
else
  bash <(curl -fsSL "$HERMES_INSTALL_URL") 2>&1 | tail -5
  if command -v hermes &>/dev/null; then
    echo "[✓] Hermes Agent installed"
  else
    echo "[!] Hermes install encountered issues. Try manually:"
    echo "    curl -fsSL $HERMES_INSTALL_URL | bash"
  fi
fi

# ---------- Easy-Agent ----------
echo "[*] Installing Easy-Agent..."
PYTHON=$(command -v python3 || command -v python)
$PYTHON -m pip install -e "$PROJECT_ROOT/packages/easy-agent/" 2>/dev/null || $PYTHON -m pip install -e "$PROJECT_ROOT/packages/easy-agent/" --break-system-packages

if command -v easy-agent &>/dev/null; then
  echo "[✓] Easy-Agent installed: $(easy-agent --version 2>/dev/null || echo 'ok')"
fi

# Copy skills to Hermes skill directory
mkdir -p ~/.hermes/skills/novel
if [ -d "$PROJECT_ROOT/skills/novel" ]; then
  cp -r "$PROJECT_ROOT/skills/novel/"* ~/.hermes/skills/novel/
  echo "[✓] Novel skills installed to ~/.hermes/skills/novel/"
fi

# Create projects directory
mkdir -p ~/easy-agent-projects
echo "[✓] Projects directory: ~/easy-agent-projects"

# Install Desktop npm dependencies
if [ -d "$PROJECT_ROOT/apps/desktop/node_modules" ] || $UPGRADE; then
  if [ -f "$PROJECT_ROOT/apps/desktop/package.json" ]; then
    echo "[*] Installing Desktop npm dependencies..."
    cd "$PROJECT_ROOT/apps/desktop" && npm install 2>/dev/null && cd "$PROJECT_ROOT"
  fi
fi

# Create default config
if [ ! -f ~/.hermes/config.yaml ]; then
  mkdir -p ~/.hermes
  cat > ~/.hermes/config.yaml << 'CONFIG'
novel:
  projects_dir: ~/easy-agent-projects
  default_language: zh
  max_concurrency: 3
  chapter_word_count: 2500
CONFIG
  echo "[✓] Default config created at ~/.hermes/config.yaml"
fi

echo ""
echo "=== Install complete! ==="
echo "Run 'easy-agent init <project-name>' to start a new novel project."
