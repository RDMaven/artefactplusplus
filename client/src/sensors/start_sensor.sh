#!/bin/bash

echo "====================="
echo "Lancement de l'environnement des capteurs"
source ./sens/bin/activate



echo "====================="

python3 -m pip install -r ./requirements.txt

echo "====================="
python3 MPU_9250_6500.py