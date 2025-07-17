#!/usr/bin/env bash
set -euo pipefail

# VARIABLES
DEPOT_DIR="${HOME}/depot_tools"
RC_FILE=""

# Determine shell RC file
if [[ -n "${ZSH_VERSION-}" ]]; then
  RC_FILE="${HOME}/.zshrc"
elif [[ -n "${BASH_VERSION-}" ]]; then
  RC_FILE="${HOME}/.bashrc"
else
  echo "Unsupported shell. Please add depot_tools to your PATH manually."
  exit 1
fi

# 1. Install system dependencies
echo "Installing system dependencies..."
if [[ "$(uname)" == "Linux" ]]; then
  sudo apt-get update
  sudo apt-get install -y git curl python3 unzip build-essential
elif [[ "$(uname)" == "Darwin" ]]; then
  if ! command -v brew &> /dev/null; then
    echo "Homebrew not found; installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi
 
  # brew install git curl python3 unzip
else
  echo "Unsupported OS: $(uname)"
  exit 1
fi

# 2. Clone depot_tools if not already present
if [[ -d "${DEPOT_DIR}" ]]; then
  echo "depot_tools already cloned at ${DEPOT_DIR}, updating..."
  cd "${DEPOT_DIR}"
  # Check if we're on a branch or in detached HEAD state
  if git symbolic-ref HEAD &> /dev/null; then
    # We're on a branch, safe to pull
    git pull
  else
    # We're in detached HEAD state, fetch and reset to origin/main
    git fetch origin
    git reset --hard origin/main
  fi
  cd - > /dev/null
else
  echo "Cloning depot_tools into ${DEPOT_DIR}..."
  git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git "${DEPOT_DIR}"
fi

# 3. Add depot_tools to PATH persistently
if grep -Fxq "export PATH=\"${DEPOT_DIR}:\$PATH\"" "${RC_FILE}"; then
  echo "depot_tools PATH entry already exists in ${RC_FILE}"
else
  echo "Adding depot_tools to PATH in ${RC_FILE}"...
  {
    echo ""
    echo "# Added by depot_tools installer on $(date '+%Y-%m-%d')"
    echo "export PATH=\"${DEPOT_DIR}:\$PATH\""
  } >> "${RC_FILE}"
  echo "Please reload your shell or run: source ${RC_FILE}"
fi

# 4. Install vibe commands to $HOME/.local/bin
LOCAL_BIN="$HOME/.local/bin"
mkdir -p "$LOCAL_BIN"

install_script() {
  src="$1"
  dest="$2"
  cp "$src" "$dest"
  chmod +x "$dest"
}

install_script "$(dirname "$0")/2-fetch-code.py" "$LOCAL_BIN/vibe-fetch-code"
install_script "$(dirname "$0")/3-configure-debug.sh" "$LOCAL_BIN/vibe-configure-debug"
install_script "$(dirname "$0")/4-build-debug.sh" "$LOCAL_BIN/vibe-build-debug"

# 5. Add $HOME/.local/bin to PATH in shell RC file if not present
if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$RC_FILE"; then
  echo "Adding $HOME/.local/bin to PATH in $RC_FILE"...
  {
    echo ""
    echo "# Added by vibe installer on $(date '+%Y-%m-%d')"
    echo 'export PATH="$HOME/.local/bin:$PATH"'
  } >> "$RC_FILE"
  echo "Please reload your shell or run: source $RC_FILE"
else
  echo "$HOME/.local/bin already in PATH in $RC_FILE"
fi

# 4. Verify installation
echo "Verifying depot_tools installation..."
export PATH="${DEPOT_DIR}:$PATH"
if command -v gclient &> /dev/null; then
  echo "✅ depot_tools installed successfully!"
  gclient --version
else
  echo "❌ depot_tools installation failed; ensure PATH is set correctly."
  exit 1
fi
