#!/bin/bash
# Arranque en Linux (para pruebas; el destino previsto es macOS).
cd "$(dirname "$0")" || exit 1
if [ ! -d ".venv" ]; then
    python3 -m venv .venv && ./.venv/bin/pip install -q -r requirements.txt
fi
source .venv/bin/activate
python main.py
