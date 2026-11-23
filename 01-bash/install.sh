#!/usr/bin/env bash
#
# install.sh - configure a Python development environment from scratch.
#
# Works on Debian/Ubuntu (apt). Safe to run several times (idempotent).
# Usage:  chmod +x install.sh && ./install.sh
#
set -euo pipefail   # stop on error, on unset variable, and on pipe failure

PACKAGES=(git curl wget vim build-essential python3 python3-pip python3-venv)
VENV_DIR="${HOME}/.venvs/aidams"

log() { printf '\n[install] %s\n' "$*"; }

# Use sudo only when we are not already root.
if [[ "${EUID}" -eq 0 ]]; then SUDO=""; else SUDO="sudo"; fi

if ! command -v apt-get >/dev/null 2>&1; then
    echo "This script only supports apt-based systems (Debian/Ubuntu)." >&2
    exit 1
fi

echo "Starting installation..."

log "Updating package lists"
${SUDO} apt-get update -y

log "Installing packages: ${PACKAGES[*]}"
${SUDO} apt-get install -y "${PACKAGES[@]}"

log "Creating Python virtual environment in ${VENV_DIR}"
mkdir -p "$(dirname "${VENV_DIR}")"
python3 -m venv "${VENV_DIR}"
"${VENV_DIR}/bin/pip" install --quiet --upgrade pip

log "Installing Python tooling (pytest, fastapi, uvicorn)"
"${VENV_DIR}/bin/pip" install --quiet pytest fastapi uvicorn

log "Verifying installation"
for cmd in git python3 pip3 curl vim; do
    if command -v "${cmd}" >/dev/null 2>&1; then
        printf '  OK       %-8s %s\n' "${cmd}" "$(command -v "${cmd}")"
    else
        printf '  MISSING  %s\n' "${cmd}"
    fi
done
git --version
python3 --version
"${VENV_DIR}/bin/pytest" --version

echo
echo "Installation complete!"
echo "Activate the environment with:  source ${VENV_DIR}/bin/activate"
