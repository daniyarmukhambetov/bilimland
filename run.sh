#!/usr/bin/env bash

# Stop and remove existing containers
echo "Stopping and removing existing containers..."
docker-compose down

# Build and start containers
echo "Building and starting containers..."
docker-compose up -d --build

# Wait for containers to start
echo "Waiting for containers to start..."
sleep 5

# Check container status
echo "Container status:"
docker-compose ps

echo ""
echo "Application is running at http://localhost"
echo "Admin interface is available at http://localhost/admin"
echo "Default admin credentials: username: admin, password: admin"
echo ""
echo "To view logs, run: docker-compose logs -f"
echo "To stop containers, run: docker-compose down"