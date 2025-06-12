# Math Problems Platform

A Django-based platform for solving math problems, similar to LeetCode but for mathematics.

## Features

- User authentication (login, registration)
- Problem listing with filters and pagination
- Different problem types (MCQ, SCQ, open-ended)
- LaTeX support for mathematical expressions
- User profiles with statistics
- Admin interface for problem and user management

## Project Structure

- `mathproblems/` - Main project settings
- `problems/` - App for managing math problems
- `accounts/` - App for user accounts and profiles
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)
- `nginx/` - Nginx configuration for production
- `docker-compose.yml` - Docker Compose configuration

## Running with Docker (Recommended)

1. Make sure you have Docker and Docker Compose installed on your system.

2. Clone the repository:
   ```
   git clone <repository-url>
   cd mathproblems
   ```

3. Build and start the containers:
   ```
   docker-compose up -d --build
   ```

4. Access the application at http://localhost

5. Access the admin interface at http://localhost/admin
   - Default admin credentials: username: `admin`, password: `admin`

6. To stop the containers:
   ```
   docker-compose down
   ```

## Local Development Setup

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```
   python manage.py migrate
   ```

4. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

5. Create sample data:
   ```
   python create_sample_data.py
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the site at http://127.0.0.1:8000/

## Production Deployment

The application is configured to run with:

- **Gunicorn**: WSGI HTTP server with 3 worker processes
- **Nginx**: Web server for static files and reverse proxy
- **PostgreSQL**: Database server
- **Docker**: Containerization for easy deployment

### Environment Variables

The following environment variables can be configured in the `.env` file:

- `DEBUG`: Set to "True" for development, "False" for production
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `POSTGRES_DB`: PostgreSQL database name
- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_HOST`: PostgreSQL host
- `POSTGRES_PORT`: PostgreSQL port
- `STATIC_URL`: URL for static files
- `STATIC_ROOT`: Directory for collected static files

## Usage

1. Log in as an admin and create problems through the admin interface
2. Create different types of problems (MCQ, SCQ, open-ended)
3. For MCQ/SCQ problems, add choices and mark the correct ones
4. Users can register, browse problems, and submit solutions
5. The system tracks user progress and statistics

## LaTeX Support

The platform supports LaTeX for mathematical expressions:

- Inline math: `$x^2 + y^2 = z^2$`
- Display math: `$$\int_{a}^{b} f(x) dx$$`

## Problem Types

1. **Multiple Choice Questions (MCQ)**: Users can select multiple correct answers
2. **Single Choice Questions (SCQ)**: Users must select exactly one correct answer
3. **Open-ended Questions**: Users can provide a text answer that will be reviewed manually

## Admin Features

Administrators can:
- Create and manage problems
- Review user submissions for open-ended questions
- Manage user accounts
- View statistics and reports