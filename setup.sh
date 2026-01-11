#!/usr/bin/env bash
set -euo pipefail

VENV_DIR=".venv"

command -v uv >/dev/null 2>&1 || {
    echo "Error: uv is not installed or not on PATH." >&2
    exit 1
}

[[ -d "$VENV_DIR" ]] || uv venv "$VENV_DIR"

source "$VENV_DIR/bin/activate"

uv sync

cat > start.sh <<'EOF'
#!/usr/bin/env bash
source .venv/bin/activate
uv run src/dice-game/main.py "$@"
EOF

chmod u+x start.sh

echo "Created start.sh"
