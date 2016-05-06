# -*- coding: utf-8 -*-
from .base import *

DEBUG = True
SECRET_KEY = 'SECRET_TO_DEV'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.child('banco.db'),
    }
}

# For tests
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
