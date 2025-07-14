# AT Identity - Centralized User Management Service

A Django-based identity management service that provides centralized authentication and authorization for multiple applications without requiring local user storage.

## Features

- **Centralized User Management** - Single service manages users for multiple apps
- **Django Allauth Integration** - Professional authentication with login/signup/password reset
- **REST API** - Complete API for user management and permissions
- **Multi-App Support** - Users can have different roles across applications
- **No Local User Storage** - Client apps don't need User models
- **Bootstrap UI** - Styled authentication pages
- **PostgreSQL Backend** - Robust database storage

## Quick Start

### 1. Installation

```bash
git clone <repository-url>
cd at-identity
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Update .env with your PostgreSQL credentials
cp .env.example .env

# Run migrations
python manage.py migrate

# Create site object
python manage.py shell
>>> from django.contrib.sites.models import Site
>>> Site.objects.get_or_create(id=1, defaults={'domain': 'localhost:8001', 'name': 'AT Identity'})
>>> exit()
```

### 3. Run Server

```bash
python manage.py runserver 8001
```

## Available Endpoints

### Authentication (Web UI)

- `/accounts/login/` - User login page
- `/accounts/signup/` - User registration
- `/accounts/logout/` - Logout
- `/accounts/password/reset/` - Password reset

### API Endpoints

- `/api/users/` - User management
- `/api/organizations/` - Organization management
- `/api/sync/user/` - Sync users from external apps
- `/api/permissions/` - Get user permissions
- `/api/verify-permission/` - Check user permissions

### Admin

- `/admin/` - Django admin interface

## Environment Variables

Create a `.env` file with:

```bash
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,*

# Database
DB_NAME=artisan_crm
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Application
APP_NAME=at_identity
```

## Integration with Other Django Apps

See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for detailed instructions on how to integrate this service with other Django applications.

### Quick Integration Example

1. **Add middleware to your Django app:**

```python
# your_app/middleware.py
import requests
from django.contrib.auth.models import AnonymousUser

class ATIdentityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.identity_url = 'http://localhost:8001/api/'

    def __call__(self, request):
        user_id = request.session.get('at_identity_user_id')
        if user_id:
            try:
                response = requests.get(f'{self.identity_url}users/{user_id}/')
                if response.status_code == 200:
                    request.user = ATIdentityUser(response.json())
                else:
                    request.user = AnonymousUser()
            except:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()

        return self.get_response(request)
```

2. **Add to your settings:**

```python
MIDDLEWARE = [
    # ... other middleware
    'your_app.middleware.ATIdentityMiddleware',
]
```

3. **Redirect users for authentication:**

```python
# Redirect to AT Identity for login
return redirect('http://localhost:8001/accounts/login/')
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Django App 1  │    │   Django App 2  │    │   Django App 3  │
│                 │    │                 │    │                 │
│ AT Identity     │    │ AT Identity     │    │ AT Identity     │
│ Middleware      │    │ Middleware      │    │ Middleware      │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │     AT Identity Service   │
                    │                           │
                    │ • User Management         │
                    │ • Authentication          │
                    │ • Authorization           │
                    │ • Role Management         │
                    │ • Multi-App Support       │
                    └───────────────────────────┘
```

## Technology Stack

- **Django 4.2.7** - Web framework
- **Django REST Framework** - API development
- **Django Allauth** - Authentication system
- **PostgreSQL** - Database
- **Bootstrap 5** - UI styling
- **Celery + Redis** - Background tasks (optional)

## Development

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run Tests

```bash
python manage.py test
```

### Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Configure proper `SECRET_KEY`
3. Set up PostgreSQL database
4. Configure static files serving
5. Use gunicorn for WSGI server

```bash
gunicorn core.wsgi:application --bind 0.0.0.0:8001
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license here]

## Support

For integration help, see [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) or create an issue in the repository.
