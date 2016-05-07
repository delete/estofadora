# -*- coding: utf-8 -*-
from .base import *

DEBUG = True
SECRET_KEY = 'SECRET_TO_DEV'

# Global variables
PATH_TO_IMAGE_TEST = BASE_DIR.child('core', 'static', 'img', 'test.jpg')

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
