from .base import *

DEBUG = True
ALLOWED_HOSTS = []

if 'RDS_HOSTNAME' in os.environ:
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
            'NAME': "trend_analyzer",
            'USER': "trend_analyzer",
            'PASSWORD': "root1234",
            'HOST': "localhost",
            'PORT': '3306',
        }
    }

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
