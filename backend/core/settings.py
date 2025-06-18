import os
import sys
from django.core.management.utils import get_random_secret_key
from pathlib import Path
from decouple import config
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY', default=get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Administration interface
    # 'jazzmin', # Temporarily commented out

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Back-end: Django Rest
    'rest_framework',

    # Authentication with SimpleJWT
    'rest_framework_simplejwt',

    # Documentation
    'drf_spectacular',

    # Registring the App


    # Core app for custom fields, etc.
    'core',

    # New apps from script
    'pacientes.apps.PacientesConfig',
    'agendamentos.apps.AgendamentosConfig',
    'consultas.apps.ConsultasConfig',
    'usuarios.apps.UsuariosConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Default to PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# Use SQLite in-memory for tests
# if 'test' in sys.argv or 'test_coverage' in sys.argv:
#     DATABASES['default'] = {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': ':memory:',
#     }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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

# This will tell Django to use the custom user model for authentication.
AUTH_USER_MODEL = 'usuarios.CustomUser'


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Tempo de vida do token
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),  # Token de acesso: 7 dias
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),  # Token de refresh: opcional, pode manter 30 dias
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Basic DRF settings from script
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}


# Fernet key for encrypting consultation data
# IMPORTANT: DJANGO_FERNET_KEY environment variable MUST be set in production.
DEFAULT_FERNET_KEY_BYTES = 'DoDOnwOMoURGhGUfE87fgBEtXgLo6ObG84l_us9fGT4=' # generate_key() output is str
FERNET_KEY = config('DJANGO_FERNET_KEY', default='DoDOnwOMoURGhGUfE87fgBEtXgLo6ObG84l_us9fGT4=').encode('utf-8')
if isinstance(FERNET_KEY, str): FERNET_KEY = FERNET_KEY.encode('utf-8') # This ensures it becomes bytes