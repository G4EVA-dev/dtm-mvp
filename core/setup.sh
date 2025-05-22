#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Make sure the virtual environment is using the correct Python version
python -c "import sys; print(f'Using Python {sys.version}')"

echo "Environment setup complete!" 