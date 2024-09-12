# Django Project with OTP Authentication and File Management API

This project is built with Django and includes OTP (One-Time Password) authentication for users and admins, allowing them to log in via email or phone number. The project also provides an API for managing files, including uploading, updating, deleting, and viewing files. JWT-based authentication is used for accessing the API after OTP login.

## Features

- **OTP Authentication**: Users and admins can log in using OTP sent via email or phone number.
- **File Management**: Users can upload, update, delete, and view files.
- **Public and Private Files**: Files can be marked as public or private. Public files are listed for anyone to view or download, while private files require a unique encrypted link.
- **Hashtags and Descriptions**: Files can be tagged with hashtags and descriptions. Clicking a hashtag filters files associated with that hashtag.
- **File Expiration**: Files can be assigned an expiration date, and the system automatically deletes expired files using Celery tasks.
- **Click Statistics**: Click statistics for each file are cached and displayed on the file detail page.
- **JWT Authentication**: After OTP login, a JWT token is generated for secure access to the API.

## Prerequisites

- **Python 3.8+**
- **Django 3.2+**
- **PostgreSQL**
- **Redis** (for caching and Celery tasks)
- **Celery** (for background tasks like deleting expired files)
- **Docker** (for containerizing the services)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/your-project.git
cd your-project
```
### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the project root with the following:

```makefile
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/your_db
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST=smtp.your_email_provider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
```

### 5. Create a Superuser
Create an admin user to access the Django admin interface:
```sh
python manage.py migrate
```

### 6. Set Up Celery
Make sure Redis is running for Celery to use as the message broker.

Start the Celery worker and Beat scheduler:

```sh
celery -A config worker --loglevel=info
celery -A config beat --loglevel=info
```

### 7. Run the Development Server
```sh
python manage.py runserver
```

### 8. Access the Application
Admin Panel: Go to http://127.0.0.1:8000/admin to manage files, users, and hashtags.
OTP Login: Go to http://127.0.0.1:8000/otp-login/ to log in using OTP.
File Management API: API endpoints are available for managing files after OTP authentication.
API Endpoints

1. Authentication
* Request OTP: POST /otp-login/
* Request an OTP by providing an email or phone number.
* Verify OTP: POST /verify-otp/
* Verify the OTP to log in and receive a JWT token.
2. File Management
* List Files: GET /files/ (JWT required)
* List all files uploaded by the authenticated user.
* Retrieve a File: GET /files/<id>/ (JWT required)
* Retrieve details of a specific file.
* Create a File: POST /files/ (JWT required)
* Upload a new file.
* Update a File: PUT /files/<id>/ (JWT required)
* Update an existing file.
* Delete a File: DELETE /files/<id>/ (JWT required)
* Delete a file.

### Celery Tasks

Delete Expired Files: Automatically deletes files that have reached their expiration date. This task runs every minute using Celery Beat.
To manually trigger this task, use:

```sh
celery -A config call dashboard.tasks.delete_expired_files
```

### Docker Support

You can optionally use Docker to containerize the application. Ensure docker-compose.yml is configured with services for PostgreSQL, Redis, Celery, and the Django app.

To start the services:

```sh
docker-compose up --build
```
