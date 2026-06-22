#!/bin/bash

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

echo "====================="

echo -e "${BLUE}Préparation de l'espace de travail${NC}"

cd "$(dirname "$0")"

if [ ! -d "sens" ]; then
    echo -e "${YELLOW}Aie... Je vais devoir installer l'environnement...${NC}"
    python3 -m venv sens
    echo -e "${YELLOW}J'ai fini !${NC}"
fi

echo -e "${GREEN}Info : Je lance l'environnement...${NC}"
source sens/bin/activate
echo -e "${GREEN}J'ai fini !${NC}"

echo -e "${GREEN}J'installe les dépendances${NC}"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo -e "${GREEN}J'ai fini !${NC}"

echo "====================="

echo -e "${BLUE}Début du programme !${NC}"
python kalman.py