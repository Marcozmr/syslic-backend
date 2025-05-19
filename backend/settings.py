import os
from re import LOCALE

import environ
from pathlib import Path

env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

try:
    SECRET_KEY = env.str("BACKEND_SECRET_KEY")
except KeyError as e:
    raise RuntimeError("Could not find a BACKEND_SECRET_KEY in environment") from e

DEBUG = False
if (env.bool("BACKEND_DEBUG_MODE") == True):
    DEBUG = True

ALLOWED_HOSTS = ['*']

DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'djoser',
    'drf_yasg',
    'django_cpf_cnpj',
    'django_extensions',
    'import_export',
    'django_filters',
    'django_cleanup.apps.CleanupConfig',
    'treebeard',
    'simple_history',
    'silk',
]

LOCAL_APPS = [
    'apps.accounts',
    'apps.address',
    'apps.permission',
    'apps.company',
    'apps.client',
    'apps.bidding',
    'apps.supplier',
    'apps.product',
    'apps.transport',
    'apps.contact',
    'apps.order',
    'apps.messager',
    'apps.contract',
    'apps.pncp',
    'apps.commission',
    'apps.metadata',
    'apps.report',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'silk.middleware.SilkyMiddleware',
    'apps.accounts.middleware.AccountMiddleware',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

SILKY_INTERCEPT_PERCENT = 100

if (env.bool("BACKEND_DEBUG_MODE") == False):
    SILKY_INTERCEPT_PERCENT = 0

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": env.str("BACKEND_DB_ENGINE"),
        "NAME": env.str("BACKEND_DB_NAME"),
        "USER": env.str("BACKEND_DB_USER"),
        "PASSWORD": env.str("BACKEND_DB_PASSWORD"),
        "HOST": env.str("BACKEND_DB_HOST"),
        "PORT": env.int("BACKEND_DB_PORT"),
    }
}

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

USE_I18N = False

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
    env.str("BACKEND_DOMAIN"),
]

CORS_ALLOW_ALL_ORIGINS = True

MEDIA_ROOT = os.path.join(env.str("BACKEND_DATA_STORAGE"), 'media')

CACHE_ADDRESS = 'redis://' + env.str("BACKEND_REDIS_HOST") + ':' + env.str("BACKEND_REDIS_PORT") + '/1'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': CACHE_ADDRESS,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.DjangoModelPermissions',
    ],
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
}

AUTH_USER_MODEL = 'accounts.User'

DECIMAL_SEPARATOR = ','

SILKY_PYTHON_PROFILER = True
