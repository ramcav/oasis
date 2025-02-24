#!/bin/bash

# Ensure Vercel's Python environment is used
export PATH="/vercel/.python/bin:$PATH"

# Check if Python is available
which python3 || echo "Python3 not found"
which pip || echo "Pip not found"

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install --no-cache-dir -r requirements.txt

# Run Django commands
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
