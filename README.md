# Genesis Backend

A Django REST backend for a task management / to-do list application.

## Overview

This project provides a JWT-secured REST API for user registration, authentication, profile management, and to-do item management. It is built with Django, Django REST Framework, JWT authentication, CORS support, and PostgreSQL database configuration.

## Features

- User registration with email-based login
- JWT authentication with access and refresh tokens
- Protected endpoints for authenticated users
- Create, list, update, and delete to-do items
- Mark tasks as completed or important
- User profile read/update
- Task statistics (completed, in progress, overdue)

## Tech Stack

- Python / Django
- Django REST Framework
- djangorestframework-simplejwt
- PostgreSQL
- django-cors-headers
- whitenoise

## Prerequisites

- Python 3.11+ (or compatible)
- PostgreSQL
- Git

## Getting Started

1. Clone the repository

```bash
git clone <repo-url>
cd genesis-backend
```

2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and configure your environment variables

Example `.env`:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_HOST=localhost
DB_PORT=5432
DB_NAME=genesis_db
DB_USER=postgres
DB_PASSWORD=your-db-password
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

5. Apply database migrations

```bash
env\Scripts\activate
python manage.py migrate
```

6. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

Base API path: `/api/`

- `POST /api/register/` - Register a new user
- `POST /api/token/` - Login and obtain JWT tokens
- `POST /api/token/refresh/` - Refresh access token
- `GET /api/dashboard/` - Verify current user session
- `GET, POST /api/todo/` - List or create to-do items
- `GET, PATCH, DELETE /api/todo-detail/<id>/` - Retrieve, update, or delete a specific task
- `PATCH /api/todo-completed/<id>/` - Toggle completed status for a task
- `PATCH /api/todo-important/<id>/` - Toggle important status for a task
- `GET, PUT /api/profile/` - Get or update current user profile
- `PUT /api/change-username/` - Change current user username
- `PUT /api/change-password/` - Change current user password
- `GET /api/tasks/stats/` - Get task statistics for current user

## Authentication

This API uses JWT authentication. Add the access token to request headers:

```http
Authorization: Bearer <access_token>
```

## Models

- `User` - Custom user model using email as the login field
- `Todo` - Task model with title, due date, status, completion, and importance

## Notes

- The project loads environment variables from `.env` using `python-dotenv`
- `STATIC_ROOT` is configured for static file collection via `whitenoise`
- `DEBUG` is enabled by default when `DEBUG=True`

## License

This repository does not include a specific license file. Add one if needed.
 

