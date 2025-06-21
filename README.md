# Uzdikland

A Django application for math problems.

## Docker Setup

This project uses a minimalistic Docker setup for easy deployment.

### Building the Docker Image

```bash
docker build -t uzdikland .
```

### Running the Container

```bash
# Using SQLite (default)
docker run -d --name uzdikland \
  -p 8000:8000 \
  -v uzdikland_data:/app/data \
  uzdikland

# Using PostgreSQL
docker run -d --name uzdikland \
  -p 8000:8000 \
  -e DATABASE_URL=postgres://username:password@host:port/dbname \
  uzdikland
```

### Environment Variables

The application uses the following environment variables:

- `DATABASE_URL`: Database connection string (default: SQLite in /app/data)
  - SQLite example: `sqlite:///data/db.sqlite3`
  - PostgreSQL example: `postgres://username:password@host:port/dbname`

- `DJANGO_SUPERUSER_USERNAME`: Username for the Django superuser (default: uzdikland_admin)
- `DJANGO_SUPERUSER_PASSWORD`: Password for the Django superuser (default: Uzd1kL@nd2025!)
- `DJANGO_SUPERUSER_EMAIL`: Email for the Django superuser (default: admin@uzdikland.kz)

- `CREATE_SAMPLE_DATA`: Whether to create sample data (default: "yes")

### Accessing the Application

Once the container is running, you can access the application at:

- Application: http://localhost:8000
- Admin interface: http://localhost:8000/admin
  - Default superuser credentials: 
    - Username: `uzdikland_admin`
    - Password: `Uzd1kL@nd2025!`

### Stopping the Container

```bash
docker stop uzdikland
docker rm uzdikland
```

## Development

For local development without Docker, set up a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Run migrations and start the development server:

```bash
python manage.py migrate
python manage.py runserver
```

## Database Configuration

The application uses `dj-database-url` to parse the `DATABASE_URL` environment variable. By default, it uses SQLite stored in the `/app/data` directory. You can switch to any supported database by setting the `DATABASE_URL` environment variable.

### SQLite (Default)
```
DATABASE_URL=sqlite:///data/db.sqlite3
```

### PostgreSQL
```
DATABASE_URL=postgres://username:password@host:port/dbname
```

### MySQL
```
DATABASE_URL=mysql://username:password@host:port/dbname
```

## Scripts

The application includes several utility scripts:

### create_superuser.py

Creates a superuser account using environment variables:
- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_PASSWORD`
- `DJANGO_SUPERUSER_EMAIL`

This script is automatically run during container startup.

### create_sample_data.py

Creates sample math problems in the database. This script is automatically run during container startup if `CREATE_SAMPLE_DATA` is set to "yes".