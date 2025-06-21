#!/bin/bash

set -e

# Check database type from DATABASE_URL
if [[ -n "$DATABASE_URL" && ("$DATABASE_URL" == postgres://* || "$DATABASE_URL" == postgresql://*) ]]; then
  echo "PostgreSQL database detected in DATABASE_URL"
else
  echo "Using SQLite or other database as configured in DATABASE_URL"
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser
echo "Creating superuser..."
python create_superuser.py

# Create sample data if needed
if [ "${CREATE_SAMPLE_DATA:-yes}" = "yes" ]; then
  echo "Creating sample data if needed..."
  python create_sample_data.py
fi

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 uzdikland.wsgi:application