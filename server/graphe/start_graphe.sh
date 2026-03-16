#!/bin/sh

echo "==============="
echo "Lancement de l'environnement server"
source ../.venv/bin/activate

echo "==============="
echo "Conversion suivie du TypeScript pour exécution :"
tsc ./www_graphe/assets/script/script.ts

echo "==============="
echo "Lancement de l'application sur le port 4242"

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

"$PYTHON" run.py
