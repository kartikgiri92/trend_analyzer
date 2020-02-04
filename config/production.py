from .base import *

import mysite_config

DEBUG = True

SECRET_KEY = mysite_config.prod_keys['secret_key']

ALLOWED_HOSTS = ['trend-anaylzer-env.ksmsub4jne.ap-south-1.elasticbeanstalk.com']

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

STATIC_URL = '/static/'
STATIC_ROOT = 'static'