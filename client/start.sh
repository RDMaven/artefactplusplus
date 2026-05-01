#!/bin/sh
# Lançement automatique du client.
# - Activation du venv
# - Recherche de python
# - Exécution de 'client.py'

. .venv/bin/activate

if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
elif command -v py >/dev/null 2>&1; then
    PYTHON=py
else
    echo "Python not found"
    exit 1
fi

"$PYTHON" client.py