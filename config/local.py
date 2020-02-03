from .base import *

import mysite_config

DEBUG = True

SECRET_KEY = mysite_config.dev_keys['secret_key']

ALLOWED_HOSTS = []

if('RDS_HOSTNAME' in os.environ):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': mysite_config.dev_keys['db_name'],
            'USER': mysite_config.dev_keys['db_user'],
            'PASSWORD': mysite_config.dev_keys['db_pass'],
            'HOST': mysite_config.dev_keys['host'],
            'PORT': '3306',
        }
    }

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')