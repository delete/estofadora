# -*- coding: utf-8 -*-
from .base import *

DEBUG = False

# OPBEAT
ORGANIZATION_ID = config('ORGANIZATION_ID')
APP_ID = config('APP_ID')
SECRET_TOKEN = config('SECRET_TOKEN')

OPBEAT = {
    'ORGANIZATION_ID': ORGANIZATION_ID,
    'APP_ID': APP_ID,
    'SECRET_TOKEN': SECRET_TOKEN,
}

# DATABASE
NAME = config('NAME')
USER = config('USER')
PASSWORD = config('PASSWORD')
HOST = config('HOST')
PORT = config('PORT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': NAME,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': PORT,
    }
}
