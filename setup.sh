#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

command -v uv >/dev/null 2>&1 || {
    echo "Error: uv is not installed or not on PATH." >&2
    exit 1
}

[[ -d "$VENV_DIR" ]] || uv venv "$VENV_DIR"

cd "$SCRIPT_DIR"

uv sync

cat > "$SCRIPT_DIR/start.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/.venv/bin/activate"
uv run "$SCRIPT_DIR/src/dice-game/main.py" "$@"
EOF

chmod u+x "$SCRIPT_DIR/start.sh"

echo "Created start.sh"
