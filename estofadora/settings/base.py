"""
Django settings for estofadora project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from decouple import config
from unipath import Path

# Get .../estofadora/estofadora
BASE_DIR = Path(__file__).ancestor(2)


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

    # 'opbeat.contrib.django',

    # My apps
    'estofadora.core',
    'estofadora.client',
    'estofadora.login',
    'estofadora.item',
    'estofadora.statement',
    'estofadora.bills',
)


MIDDLEWARE_CLASSES = (
    # 'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'estofadora.urls'

WSGI_APPLICATION = 'estofadora.wsgi.application'


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

MEDIA_ROOT = BASE_DIR.child('media')
MEDIA_URL = '/media/'

# Auth
LOGIN_URL = 'login:login'
LOGOUT_URL = 'login:logout'
LOGIN_REDIRECT_URL = 'core:home'
