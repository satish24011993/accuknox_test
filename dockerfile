# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variable
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8000

# Run the application
CMD ['python', 'manage.py', 'runserver', '0.0.0.0:8000']

# Collect static files
RUN python manage.py collectstatic --noinput

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ['/entrypoint.sh']