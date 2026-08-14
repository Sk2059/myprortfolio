"""
Django settings for backend project.
Production-ready for Render + Supabase/PostgreSQL
"""
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta
import dj_database_url
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# -----------------------
# SECURITY
# -----------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "local-dev-secret-change-in-production")

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "myprortfolio.onrender.com",
    "localhost",
    "127.0.0.1",
    "myportfolio-ejsba2man-sksingh4919-6927s-projects.vercel.app",
    "myportfolio-phi-ten-58.vercel.app",
]

# -----------------------
# APPS
# -----------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary',
    'cloudinary_storage',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',

    'projects',
    'contacts',
    'services',
]


# -----------------------
# MIDDLEWARE
# -----------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',        
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# -----------------------
# CORS
# -----------------------
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "https://myprortfolio.vercel.app",
    "https://myprortfolio.onrender.com",
    "http://localhost:5173",
]

CSRF_TRUSTED_ORIGINS = [
    "https://myprortfolio.vercel.app",
    "https://myprortfolio.onrender.com",
]


# -----------------------
# URLS
# -----------------------
ROOT_URLCONF = 'backend.urls'
APPEND_SLASH = False


# -----------------------
# TEMPLATES
# -----------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# -----------------------
# DATABASE
# Locally falls back to SQLite if DATABASE_URL not set
# -----------------------
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=not DEBUG,   # SSL only in production
        )
    }
else:
    # Local development fallback — uses SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# -----------------------
# PASSWORD VALIDATION
# -----------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# -----------------------
# INTERNATIONALIZATION
# -----------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# -----------------------
# CLOUDINARY
# -----------------------
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get("CLOUDINARY_CLOUD_NAME"),
    'API_KEY':    os.environ.get("CLOUDINARY_API_KEY"),
    'API_SECRET': os.environ.get("CLOUDINARY_API_SECRET"),
}


# -----------------------
# STATIC / MEDIA
# -----------------------


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"

# ✅ IMPORTANT: keep ONLY ONE static system (no duplication conflicts)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Prevent collectstatic crash if some DRF assets are missing
WHITENOISE_MANIFEST_STRICT = False

# -----------------------
# DEFAULT PK
# -----------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -----------------------
# DRF + JWT
# -----------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    # ✅ safe for production APIs (prevents DRF bootstrap/static issues)
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
}


# -----------------------
# PRODUCTION SECURITY HEADERS
# Only applied when DEBUG=False (i.e. on Render)
# -----------------------
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SECURE_CONTENT_TYPE_NOSNIFF = True
