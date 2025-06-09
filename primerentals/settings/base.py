import os
from pathlib import Path
from typing import Any, cast
import importlib
try:
    import environ
except ImportError:  # pragma: no cover - allow running without django-environ installed
    environ = None

try:
    importlib.import_module('django_cleanup')
    CLEANUP_APP = 'django_cleanup.apps.CleanupConfig'
except ImportError:  # pragma: no cover - django-cleanup optional
    CLEANUP_APP = None

BASE_DIR = Path(__file__).resolve().parent.parent.parent

if environ:
    env = environ.Env(DEBUG=(bool, False))
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
    SECRET_KEY = env('SECRET_KEY', default=cast(Any, 'insecure'))
    DEBUG = env.bool('DEBUG', default=cast(Any, False))
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=cast(Any, ['*']))
    DATABASES = {
        'default': env.db('DATABASE_URL', default=cast(Any, f'sqlite:///{BASE_DIR / "db.sqlite3"}'))
    }
else:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'insecure')
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'django_filters',
    'rentals',
]

if CLEANUP_APP:
    INSTALLED_APPS.append(CLEANUP_APP)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'primerentals.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'primerentals.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
