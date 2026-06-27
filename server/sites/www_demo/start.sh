#!/bin/bash

# Commande spécifique pour un mac qui n'est pas à la dernière mise à jour.
export DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib

set -e

VENV=".venv"

# Trouver un interpréteur python
if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "Error: Python n'est pas installé."
    exit 1
fi

# Créer un venv s'il n'existe pas
if [ ! -d "$VENV" ]; then
    echo "Création d'un venv..."
    "$PYTHON" -m venv "$VENV"
fi

source "$VENV/bin/activate"

# Install requirements only if they're missing/outdated
pip install -q -r requirements.txt >/dev/null

# Run the application
"$PYTHON" run.py
