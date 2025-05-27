#!/bin/bash

if [ ! -d "venv" ]; then
    echo "-> Creating virtual environment..."
    python -m venv venv
    echo "-> Virtual environment created!"
fi

# Attiva il venv
source venv/bin/activate

# Installa i pacchetti da requirements.txt se esiste
if [ -f "requirements.txt" ]; then
    echo "-> Installing dependencies inside virtual environment..."
    pip install -r requirements.txt
    echo "-> Dependencies installed inside virtual environment!"
fi

python main.py
