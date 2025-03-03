# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY ../backend /app/backend
COPY ../manage.py /app/manage.py
COPY ../requirements.txt /app/requirements.txt
COPY check_google_sheets.py /app/check_google_sheets.py

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Run the scheduled task script
CMD ["python", "/app/check_google_sheets.py"]