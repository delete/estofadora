# -*- coding: utf-8 -*-
from .base import *

DEBUG = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'banco.db'),
    }
}
