#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required. Install Python 3.10+ first." >&2
  exit 1
fi

if ! command -v pipx >/dev/null 2>&1; then
  echo "pipx was not found. Installing pipx for the current user..."
  python3 -m pip install --user pipx
  python3 -m pipx ensurepath || true
  PIPX_BIN="$(python3 -m site --user-base)/bin/pipx"
else
  PIPX_BIN="$(command -v pipx)"
fi

"$PIPX_BIN" install --force "$ROOT_DIR"
pbi-cli skills install --agent codex --force --yes

echo
echo "pbi-cli is installed for Codex."
echo "Installed skills: $HOME/.agents/skills/power-bi-*"
echo "Codex guidance:   ${CODEX_HOME:-$HOME/.codex}/AGENTS.md"
echo
echo "Report/PBIR commands can run on macOS."
echo "Semantic model commands require Power BI Desktop, which is Windows-only."
