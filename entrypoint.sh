#!/usr/bin/env bash

set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
# Use a simple timeout approach instead of netcat
RETRIES=30
until PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for PostgreSQL server, $((RETRIES--)) remaining attempts..."
  sleep 1
done

if [ $RETRIES -eq 0 ]; then
  echo "PostgreSQL server failed to start. Exiting..."
  exit 1
fi

echo "PostgreSQL is up and running!"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if not exists
echo "Creating superuser if not exists..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser created.')
else:
    print('Superuser already exists.')
"

# Create sample data if needed
echo "Creating sample data if needed..."
python create_sample_data.py

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 mathproblems.wsgi:application