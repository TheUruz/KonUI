#!/bin/bash

if [ ! -d "venv" ]; then
    echo "-> Creating virtual environment..."
    python -m venv venv
    echo "-> Virtual environment created!"
fi

source venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo "-> Installing dependencies inside virtual environment..."
    pip install -r requirements.txt
    echo "-> Dependencies installed inside virtual environment!"
fi

python main.py
