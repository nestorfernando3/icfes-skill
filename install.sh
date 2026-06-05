#!/usr/bin/env bash
# One-command installer for ICFES Skill.
set -euo pipefail

DEFAULT_REPO_URL="https://github.com/nestorfernando3/icfes-skill.git"
REPO_URL="${ICFES_SKILL_REPO:-$DEFAULT_REPO_URL}"
INSTALL_DIR="${ICFES_SKILL_HOME:-$HOME/.icfes-skill/repo}"
USE_HOMEBREW=0
REPO_EXPLICIT=0
SETUP_ARGS=()

usage() {
  cat <<'EOF'
Uso:
  install.sh [--repo URL] [--install-dir DIR] [--homebrew] [setup args...]

Ejemplos:
  install.sh --target codex --scope user
  install.sh --repo https://github.com/nestorfernando3/icfes-skill.git
  install.sh --repo https://github.com/nestorfernando3/icfes-skill.git --target "codex,claude" --scope project --project .
  install.sh --homebrew
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --repo) REPO_URL="${2:-}"; REPO_EXPLICIT=1; shift 2 ;;
    --repo=*) REPO_URL="${1#--repo=}"; REPO_EXPLICIT=1; shift ;;
    --install-dir) INSTALL_DIR="${2:-}"; shift 2 ;;
    --install-dir=*) INSTALL_DIR="${1#--install-dir=}"; shift ;;
    --homebrew) USE_HOMEBREW=1; shift ;;
    -h|--help) usage; exit 0 ;;
    --) shift; SETUP_ARGS+=("$@"); break ;;
    *) SETUP_ARGS+=("$1"); shift ;;
  esac
done

find_brew() {
  if [ -n "${BREW_BIN:-}" ]; then
    echo "$BREW_BIN"
  elif command -v brew >/dev/null 2>&1; then
    command -v brew
  elif [ -x /opt/homebrew/bin/brew ]; then
    echo "/opt/homebrew/bin/brew"
  elif [ -x /usr/local/bin/brew ]; then
    echo "/usr/local/bin/brew"
  fi
}

run_homebrew_install() {
  local brew_bin icfes_bin
  brew_bin="$(find_brew)"
  if [ -z "$brew_bin" ]; then
    echo "Homebrew no esta instalado o no esta en PATH." >&2
    echo "Usa modo repo directo o instala Homebrew: https://brew.sh" >&2
    exit 1
  fi

  echo "Instalando ICFES Skill con Homebrew..."
  "$brew_bin" tap nestorfernando3/icfes-skill >/dev/null
  if "$brew_bin" list icfes-skill >/dev/null 2>&1; then
    "$brew_bin" upgrade icfes-skill || "$brew_bin" reinstall icfes-skill
  else
    "$brew_bin" install icfes-skill
  fi

  echo
  echo "Abriendo instalador interactivo..."
  icfes_bin="$(dirname "$brew_bin")/icfes-skill"
  exec "$icfes_bin" install "${SETUP_ARGS[@]}"
}

script_root() {
  local source dir
  source="${BASH_SOURCE[0]}"
  while [ -L "$source" ]; do
    dir="$(cd -P "$(dirname "$source")" && pwd)"
    source="$(readlink "$source")"
    case "$source" in
      /*) ;;
      *) source="$dir/$source" ;;
    esac
  done
  cd "$(dirname "$source")" && pwd -P
}

run_repo_install() {
  local root
  root="$(script_root)"

  if [ "$REPO_EXPLICIT" -eq 0 ] && [ -f "$root/setup" ] && [ -d "$root/skills/icfes-item-workflow" ]; then
    echo "Usando repo local: $root"
    exec "$root/setup" "${SETUP_ARGS[@]}"
  fi

  if ! command -v git >/dev/null 2>&1; then
    echo "Git requerido para instalar desde repo: $REPO_URL" >&2
    exit 1
  fi

  echo "Instalando ICFES Skill desde repo:"
  echo "  repo: $REPO_URL"
  echo "  dir:  $INSTALL_DIR"

  if [ -d "$INSTALL_DIR/.git" ]; then
    git -C "$INSTALL_DIR" fetch --quiet origin
    git -C "$INSTALL_DIR" checkout --quiet main || true
    git -C "$INSTALL_DIR" pull --ff-only --quiet origin main || true
  else
    rm -rf "$INSTALL_DIR"
    mkdir -p "$(dirname "$INSTALL_DIR")"
    git clone --quiet "$REPO_URL" "$INSTALL_DIR"
  fi

  echo
  echo "Abriendo instalador interactivo..."
  exec "$INSTALL_DIR/setup" "${SETUP_ARGS[@]}"
}

if [ "$USE_HOMEBREW" -eq 1 ]; then
  run_homebrew_install
else
  run_repo_install
fi
