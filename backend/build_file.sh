#!/bin/bash

pip install --upgrade pip  # Ensure pip is updated
pip install --no-cache-dir -r requirements.txt  # Install dependencies without cache

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
