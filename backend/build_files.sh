#!/bin/bash

export PATH="/vercel/.python/bin:$PATH"  # Ensure Python is accessible

# Ensure the correct Python and pip version
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip  # Ensure pip is updated
pip install --no-cache-dir -r requirements.txt  # Install dependencies without cache

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
