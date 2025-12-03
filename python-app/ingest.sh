#!/usr/bin/env bash
set -euo pipefail  #Exits on unset vars, pipe failures

# Script to run file ingestion pipeline.
cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1

# Setup virtualenv if missing
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtualenv..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found. Assuming deps are installed."
fi

echo "Starting ingestion..."
python3 -m app.ingest

# Deactivate venv
deactivate

echo "Ingestion complete."
