import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)  # Force .env to override system variables


# Simple logging control
# Add ENABLE_FILE_LOGGING=True to .env file to enable file logging
# Default: Console logging only

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-default-key-for-development")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")


# Authentication backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework",
    "at_identity",
]

# Using custom User model
AUTH_USER_MODEL = "at_identity.User"
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database - FORCED POSTGRESQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "at_identity"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    },
}

# Database router for CRM
# DATABASE_ROUTERS = ["artisan_crm.database_router.CRMDatabaseRouter"]


# Auto-create PostgreSQL database if it doesn't exist
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_database_if_not_exists():
    db_config = DATABASES["default"]
    try:
        conn = psycopg2.connect(
            host=db_config["HOST"],
            port=db_config["PORT"],
            user=db_config["USER"],
            password=db_config["PASSWORD"],
            database=db_config["NAME"],
        )
        conn.close()
    except psycopg2.OperationalError as e:
        if "does not exist" in str(e):
            conn = psycopg2.connect(
                host=db_config["HOST"],
                port=db_config["PORT"],
                user=db_config["USER"],
                password=db_config["PASSWORD"],
                database="postgres",
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            cursor.execute(f'CREATE DATABASE "{db_config["NAME"]}"')
            cursor.close()
            conn.close()
            print(f"Created database: {db_config['NAME']}")


# Only create database during migrations or runserver
import sys

if "migrate" in sys.argv or "runserver" in sys.argv:
    try:
        create_database_if_not_exists()
    except Exception as e:
        print(f"Warning: Could not auto-create database: {e}")



# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Language support
LANGUAGES = [
    ("en", "English"),
    ("hi", "हिंदी"),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# Database encoding for Unicode support
DATABASE_OPTIONS = {
    "charset": "utf8mb4",
    "use_unicode": True,
}

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "staticcss"),
]

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'UNAUTHENTICATED_USER': None,
    'UNAUTHENTICATED_TOKEN': None,
}

# Using Django's default User model for independence

AT_IDENTITY_URL = "http://localhost:8001/api/"
APP_NAME = "at_identity"

# Allauth settings
SITE_ID = 1
ACCOUNT_LOGIN_METHODS = {'username'}
ACCOUNT_SIGNUP_FIELDS = ['username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGIN_REDIRECT_URL = "/api/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/api/"
ACCOUNT_SIGNUP_REDIRECT_URL = "/api/"
LOGIN_URL = "/accounts/login/"
LOGOUT_URL = "/accounts/logout/"
LOGIN_REDIRECT_URL = "/api/"

# Tailwind configuration
TAILWIND_APP_NAME = "theme"
INTERNAL_IPS = [
    "127.0.0.1",
]

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@at-identity.com"

# Razorpay settings
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "")
RAZORPAY_TEST_MODE = True

# Login redirect
LOGIN_REDIRECT_URL = "/api/"
LOGIN_URL = "/accounts/login/"

# Additional settings for Indian locale
USE_L10N = True
USE_THOUSAND_SEPARATOR = True

# Ensure proper Unicode handling
DEFAULT_CHARSET = "utf-8"

# Session settings
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = True

# Simple logging toggle via environment variable
# Set ENABLE_FILE_LOGGING=True in .env to enable file logging
if os.environ.get("ENABLE_FILE_LOGGING", "False").lower() == "true":
    # Create logs directory
    LOGS_DIR = BASE_DIR / "logs"
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "file": {
                "level": "ERROR",
                "class": "logging.FileHandler",
                "filename": LOGS_DIR / "django.log",
            },
        },
        "root": {
            "handlers": ["file"],
            "level": "ERROR",
        },
    }
else:
    # Console logging only (default)
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
    }
