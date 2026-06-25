#!/bin/sh
# Lançement automatique du client.
# - Activation du venv
# - Recherche de python
# - Exécution de 'client.py'

MAGENTA="\033[38;5;127m"
ROYALBLUE="\033[38;5;63m"
NC="\033[0m" # No Color

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

# echo -e "${MAGENTA} VOUS ALLEZ RIRE : MAX LANCE UN ENVIRONNEMENT MAIS N'INSTALLE PAS LES REQUIREMENTS DE MODULE PYTHON... ${NC}"
# echo -e "${ROYALBLUE} DÉSOLÉ SI VOUS DEVEZ TOUT INSTALLER ${NC}"

# pip install -r requirements.txt

# echo -e "${ROYALBLUE} C EST BON, PROFITEZ DU PROGRAMME ! ${NC}"

"$PYTHON" client.py