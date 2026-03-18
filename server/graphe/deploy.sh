#!/bin/bash

echo "==============="
echo "Mise à jour automatique du git après export d'une carte"

git -C ./Cartes add .
git -C ./Cartes commit -m "Mise à jour autoumatique de la cartographie"
git -C ./Cartes push

echo "Mise à jour terminée : reprise du programme"
echo "==============="