#!/bin/bash

echo "==============="
echo "Lancement de l'environnement server"
. ../.venv/bin/activate

echo "==============="
echo "Conversion du TypeScript pour exécution :"
tsc ./www_graphe/assets/script/script_index.ts
tsc ./www_graphe/assets/script/script_map.ts
echo "Conversion effectuée sans problèmes !"

echo "==============="
echo "Git pull pour être à jour sur les cartes créées"
git -C ./Cartes pull

echo "==============="
echo "Lancement de l'application sur le port 4242 :"

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
