# caveman_cms/base.py  (revised)

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# ─────── Build paths ───────
PROJECT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = PROJECT_DIR.parent
ENV = os.getenv('ENV', 'dev') 
dotenv_path = BASE_DIR / f'.env.{ENV}'
load_dotenv(dotenv_path)

# ─────── Security & Debug ───────
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# If you want to override Wagtail’s admin login URL, you can also set:
# LOGIN_URL = "/admin/login/"

# ─────── Applications ───────
INSTALLED_APPS = [
    # Your “feature” apps
    "users",
    "home",
    "search",
    "helpdocs",

    # Core Wagtail apps
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",

    # Misc
    "modelcluster",
    "taggit",
    "django_filters",

    # Django “built-in” apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Wagtail’s headless REST API
    "wagtail.api.v2",

    # Add the same DRF/JWT/CORS apps as your backend
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",

    # If you want GraphQL preview or headless preview features:
    # "wagtail_headless_preview",
]

# ─────── Middleware ───────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    # Session + CORS
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",          # ← same as backend
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # Wagtail Redirects
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "caveman_cms.urls"

# ─────── Templates ───────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_DIR / "templates"],
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

WSGI_APPLICATION = "caveman_cms.wsgi.application"

# ─────── Database ───────
# (Keep the same SQLite/MSSQL switch if you want, or lock to SQLite for Wagtail dev.)
CMS_DB_ENGINE = os.getenv('DB_ENGINE', 'sqlite')
if CMS_DB_ENGINE == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / os.getenv('CMS_DB_NAME', 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': CMS_DB_ENGINE,
            'NAME':     os.getenv('CMS_DB_NAME'),
            'USER':     os.getenv('CMS_DB_USER'),
            'PASSWORD': os.getenv('CMS_DB_PASSWORD'),
            'HOST':     os.getenv('CMS_DB_HOST'),
            'PORT':     os.getenv('CMS_DB_PORT'),
            'OPTIONS': {
                'driver': os.getenv('CMS_DB_DRIVER', 'ODBC Driver 17 for SQL Server'),
                'unicode_results': True,
                'extra_params': 'TrustServerCertificate=yes;Encrypt=no;charset=utf8',
            } if CMS_DB_ENGINE == 'mssql' else {},
        }
    }

# ─────── Auth & JWT ───────
#AUTH_USER_MODEL = "users.RemoteUser"  # match backend

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # Reuse your custom fetch‐and‐create logic if you have it, e.g.:
        "common.authentication.JWTAuthenticationFetchUser",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

SIMPLE_JWT = {
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,  # same key as backend
    "USER_ID_CLAIM": "user_id",
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=10),
    "LEEWAY": 10,
}

# ─────── Password Validation ───────
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

# ─────── Internationalization ───────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Australia/Brisbane"   # match backend
USE_I18N = True
USE_TZ = True

# ─────── Static & Media ───────
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [PROJECT_DIR / "static"]
STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000

# ─────── CORS ───────
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL_ORIGINS", "False") == "True"
CORS_ALLOWED_ORIGIN_REGEXES = os.getenv(
    "CORS_ALLOWED_ORIGIN_REGEXES", r"^http://10\.\d+\.\d+\.\d+"
).split(",")
CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000"
).split(",")
CORS_ORIGIN_WHITELIST = os.getenv(
    "CORS_ORIGIN_WHITELIST", "http://localhost:3000,http://127.0.0.1"
).split(",")
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "True") == "True"

# ─────── Wagtail Settings ───────
WAGTAIL_SITE_NAME = "caveman_cms"
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}
# Base URL in emails/redirects. Use your actual dev or prod host.
WAGTAILADMIN_BASE_URL = os.getenv("WAGTAILADMIN_BASE_URL", "http://localhost:8002")

WAGTAILDOCS_EXTENSIONS = [
    "csv",
    "docx",
    "key",
    "odt",
    "pdf",
    "pptx",
    "rtf",
    "txt",
    "xlsx",
    "zip",
]

# If you want to override default login redirect:
# LOGIN_URL = "/admin/login/"
