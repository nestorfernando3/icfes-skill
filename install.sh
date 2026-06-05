#!/usr/bin/env bash
# One-command installer for ICFES Skill.
set -euo pipefail

BREW_BIN="${BREW_BIN:-}"
if [ -z "$BREW_BIN" ]; then
  if command -v brew >/dev/null 2>&1; then
    BREW_BIN="$(command -v brew)"
  elif [ -x /opt/homebrew/bin/brew ]; then
    BREW_BIN="/opt/homebrew/bin/brew"
  elif [ -x /usr/local/bin/brew ]; then
    BREW_BIN="/usr/local/bin/brew"
  fi
fi

if [ -z "$BREW_BIN" ]; then
  echo "Homebrew no esta instalado o no esta en PATH." >&2
  echo "Instala Homebrew primero: https://brew.sh" >&2
  exit 1
fi

echo "Instalando ICFES Skill con Homebrew..."
"$BREW_BIN" tap nestorfernando3/icfes-skill >/dev/null
if "$BREW_BIN" list icfes-skill >/dev/null 2>&1; then
  "$BREW_BIN" upgrade icfes-skill || "$BREW_BIN" reinstall icfes-skill
else
  "$BREW_BIN" install icfes-skill
fi

echo
echo "Abriendo instalador interactivo..."
ICFES_BIN="$(dirname "$BREW_BIN")/icfes-skill"
exec "$ICFES_BIN" install "$@"
