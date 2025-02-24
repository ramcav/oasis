#!/bin/bash

# Ensure Python is available
which python3 || echo "Python3 not found"
python3 -m venv venv  # Create a virtual environment
source venv/bin/activate  # Activate the virtual environment

# Ensure pip is installed inside the venv
python3 -m ensurepip --default-pip
pip install --upgrade pip  # Upgrade pip inside the venv

# Debugging: Check if pip is available now
which pip || echo "Pip still not found"

# Install dependencies
pip install --no-cache-dir -r requirements.txt

# Debugging: Check installed packages
pip list

# Run Django commands
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
