import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "6Le1y-IqAAAAAP9K6_Gr8v7Yp_XShGY0a--JWgrv"
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    # Custom admin interface (must come before django.contrib.admin)
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Additional packages
    "django_recaptcha",  # django-recaptcha for CAPTCHA functionality
    "django_ckeditor_5",  # CKEditor 5 for rich text editing
    # Our apps
    "forum.apps.ForumConfig",  # Specify the AppConfig class
]

# Fixture directories for loaddata command
FIXTURE_DIRS = [
    os.path.join(BASE_DIR),
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Custom middleware to load demo data
    "forum.middleware.LoadDemoDataMiddleware",
]

ROOT_URLCONF = "cybershield_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],  # Global templates folder
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

WSGI_APPLICATION = "cybershield_project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "CyberShieldDB",
        "USER": "root",
        "PASSWORD": "wut8402hb",
        "HOST": "localhost",
        "PORT": "3306",
    }
}

AUTH_USER_MODEL = "forum.CustomUser"

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

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# django-recaptcha settings (replace with your actual keys)
RECAPTCHA_PUBLIC_KEY = "6LecF-YqAAAAAMFhyCJZgi7o-jxcO4sH8oCVG9su"
RECAPTCHA_PRIVATE_KEY = "6LecF-YqAAAAAG_kRwtekfS1NgfnHJ8tAuQP6cPp"
NOCAPTCHA = True

# Set the media root and URL
MEDIA_ROOT = os.path.join(
    BASE_DIR,
    "media",
)
MEDIA_URL = "/media/"

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

# CKEditor 5 configuration
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "bold",
            "italic",
            "|",
            "Subscript",
            "Superscript",
            "|",
            "link",
            "RemoveFormat",
        ],
    },
}

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "forum": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}
