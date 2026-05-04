#!/bin/bash
echo "====================="



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

"$PYTHON" -m pip install -r ./requirements.txt

echo "====================="
"$PYTHON" MPU_9250_6500.py