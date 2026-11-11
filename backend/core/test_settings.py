"""Isolated SQLite settings for fast API regression tests; never for deployment."""
import os
os.environ.setdefault('DJANGO_SECRET_KEY', 'test-only-not-for-deployment')
for name in ('DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT'):
    os.environ.setdefault(name, 'unused')
from .settings import *
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
