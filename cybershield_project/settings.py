import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Secrets come from environment variables; the fallback is for local development only.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-insecure-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = ["127.0.0.1", "35.182.152.63", "d2r6sxfy47w9d0.cloudfront.net"]
# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000", "https://d2r6sxfy47w9d0.cloudfront.net"]

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
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
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

# reCAPTCHA keys come from the environment; without them django-recaptcha uses Google's test keys.
if os.environ.get("RECAPTCHA_PUBLIC_KEY"):
    RECAPTCHA_PUBLIC_KEY = os.environ["RECAPTCHA_PUBLIC_KEY"]
    RECAPTCHA_PRIVATE_KEY = os.environ["RECAPTCHA_PRIVATE_KEY"]
NOCAPTCHA = True
SILENCED_SYSTEM_CHECKS = ["django_recaptcha.recaptcha_test_key_error"]

# Set the media root and URL
MEDIA_ROOT = os.path.join(
    BASE_DIR,
    "media",
)
MEDIA_URL = "/media/"


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
