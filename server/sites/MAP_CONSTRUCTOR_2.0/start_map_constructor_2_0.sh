#!/bin/bash

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

PROJECT_NAME="map_constructor_2.0"
TEMPLATE="react-ts"

echo -e "${BLUE}========### LANCEMENT DU PROJET ###========${NC}"

echo "Vérification que le projet vite existe"

if [ ! -d "$PROJECT_NAME" ]; then
    echo -e "${YELLOW} Le projet vite n'existe pas ! Création en cours...${NC}"
    yes | npm create vite@latest "$PROJECT_NAME" -- --template "$TEMPLATE"
    echo -e "${YELLOW} Projet créé !${NC}"
fi

echo "Le projet vite est bien créé !"
cd "$PROJECT_NAME" || exit

echo -e "${BLUE}========### INSTALATION DES DÉPENDANCES DE NPM ###========${NC}"
npm install
npm install react-toastify express cors
npm install concurrently --save-dev
echo -e "${BLUE}========### LANCEMENT DU SERVEUR ET DU REACT ###========${NC}"

npm run dev 

