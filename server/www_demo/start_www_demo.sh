#!/bin/bash

if [ ! -dir venv_demo]; then
    echo "Je vais créer l'environnement"
    python3 -m venv .venv_demo
fi

. .venv_demo/bin/activate

pip install -r requirements.txt

python3 ./www_demo.py