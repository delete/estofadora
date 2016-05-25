# -*- coding: utf-8 -*-
from .base import *

STATIC_ROOT = BASE_DIR.parent.child('static')
DEBUG = False
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')]
)

# OPBEAT
# Uncomment if you want to use

# OPBEAT = {
#     'ORGANIZATION_ID': config('ORGANIZATION_ID'),
#     'APP_ID': config('APP_ID'),
#     'SECRET_TOKEN': config('SECRET_TOKEN'),
# }

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('NAME'),
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
        'HOST': config('HOST'),
        'PORT': config('PORT'),
    }
}
