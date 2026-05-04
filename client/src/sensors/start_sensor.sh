#!/bin/bash

echo "====================="

cd "$(dirname "$0")"

if [ ! -d "sens" ]; then
    python3 -m venv sens
fi

source sens/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "====================="
python MPU_9250_6500.py