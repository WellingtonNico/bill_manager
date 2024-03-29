"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from dj_database_url import parse as dburl
from pathlib import Path
from decouple import config
from kombu import Queue,Exchange

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

CSRF_TRUSTED_ORIGINS = list(map(lambda host:f'http://{host}',ALLOWED_HOSTS)) + list(map(lambda host:f'https://{host}',ALLOWED_HOSTS))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'users',
    'bills',
    'bill_chargers',
    'bill_categories',
    'crispy_forms',
    'crispy_bootstrap5',
    'relatories',
    'django_cleanup.apps.CleanupConfig', # deve ficar sempre por último
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'coretags':'core.coretags'
            }
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

IS_LOCAL_TEST = config('IS_LOCAL_TEST',default=False,cast=bool)
default_db_url = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': config('DATABASE_URL',default=default_db_url,cast=dburl)
} 

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = './static'
STATICFILES_DIRS = ['./staticfiles']

MEDIA_ROOT = config('MEDIA_ROOT')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'bill_list'
LOGOUT_REDIRECT_URL = 'login'




###############################
####### CELERY SETTINGS #######
###############################
CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIME_ZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_ENABLE_UTC = True
# aks_late não pode ser usado como false
CELERY_MESSAGE_COMPRESSION = 'gzip'
CELERY_ACKS_LATE = True
CELERY_TASK_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_PREFETCH_MULTIPLIER = 1
CELERYD_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_TRACK_STARTED= True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_RESULT_PERSISTENT = True
CELERY_RESULT_EXTENDED = True
CELERY_REJECT_ON_WORKER_LOST = True
CELERY_TASK_CREATE_MISSING_QUEUES=True
CELERY_RESULT_EXPIRES = 60 * 60 * 24 * 4
QUEUES = ('celery',)
CELERY_X_MAX_PRIORITY = 5
CELERY_TASK_QUEUES = [
    Queue(
        queue,Exchange(queue),routing_key=queue,queue_arguments={'x-max-priority': CELERY_X_MAX_PRIORITY}
    ) for queue in QUEUES
]


# configurações dos comprovantes de pagamento
PAYMENT_PROOFS_MAX_LENGTH_KB = float(config('PAYMENT_PROOFS_MAX_LENGTH_KB'))


###############################
####### E-MAIL SETTINGS #######
###############################
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = f'Contas Fácil <{EMAIL_HOST_USER}>'
OWNER_EMAIL_RECEIVER = config('OWNER_EMAIL_RECEIVER')