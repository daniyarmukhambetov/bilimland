#!/usr/bin/env bash

# Exit on error
set -e

# Check if .env file exists
if [ ! -f .env ]; then
  echo "Error: .env file not found."
  echo "Please create a .env file with the following variables:"
  echo "DATABASE_URL=sqlite:///db.sqlite3 (or your database connection string)"
  exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Build the Docker image
echo "Building Docker image..."
docker build -t uzdikland .

# Stop and remove existing container if it exists
if docker ps -a | grep -q uzdikland; then
  echo "Stopping and removing existing container..."
  docker stop uzdikland || true
  docker rm uzdikland || true
fi

# Create a volume for SQLite database if using SQLite
if [[ -z "$DATABASE_URL" || "$DATABASE_URL" == sqlite://* ]]; then
  echo "Using SQLite database, creating volume for persistence..."
  docker volume create uzdikland_data || true
  DB_VOLUME_MOUNT="-v uzdikland_data:/app/data"
else
  echo "Using external database as configured in DATABASE_URL"
  DB_VOLUME_MOUNT=""
fi

# Run the container
echo "Starting container..."
docker run -d --name uzdikland \
  -p 8000:8000 \
  --env-file .env \
  $DB_VOLUME_MOUNT \
  uzdikland

# Wait for container to start
echo "Waiting for container to start..."
sleep 3

# Check container status
echo "Container status:"
docker ps | grep uzdikland

echo ""
echo "Application is running at http://localhost:8000"
echo "Admin interface is available at http://localhost:8000/admin"
echo "Default admin credentials: username: admin, password: admin"
echo ""
echo "To view logs, run: docker logs -f uzdikland"
echo "To stop container, run: docker stop uzdikland"