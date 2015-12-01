"""
Django settings for estofadora project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sw=o-z2wh&!z40pmr8whsii++ud^1etdz&)f*@2)t@bgpzb2qg'

#For tests
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

PATH_TO_IMAGE_TEST = os.path.join(
    BASE_DIR, 'core', 'static', 'img') + '/test.jpg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #'opbeat.contrib.django',

    #My apps
    'estofadora.core',
    'estofadora.client',
    'estofadora.login',
    'estofadora.item',
    'estofadora.statement',
    'estofadora.bills',
)


MIDDLEWARE_CLASSES = (
    #'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

OPBEAT = {
    'ORGANIZATION_ID': '6409f61f82ab4ee58bf78923b1645a29',
    'APP_ID': '8ee0dafc3e',
    'SECRET_TOKEN': 'bbedc0141783b774e7ba5061d7a8ed6328bc148e',
}

ROOT_URLCONF = 'estofadora.urls'

WSGI_APPLICATION = 'estofadora.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'banco.db'),
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Auth
LOGIN_URL = 'login:login'
LOGOUT_URL = 'login:logout'
LOGIN_REDIRECT_URL = 'core:home'
