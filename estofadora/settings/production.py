# -*- coding: utf-8 -*-
from .base import *

DEBUG = False

OPBEAT = {
    'ORGANIZATION_ID': '6409f61f82ab4ee58bf78923b1645a29',
    'APP_ID': '8ee0dafc3e',
    'SECRET_TOKEN': 'bbedc0141783b774e7ba5061d7a8ed6328bc148e',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}
