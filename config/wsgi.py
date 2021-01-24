import os

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.production'
os.environ['ENV_TYPE'] = 'production'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.local')
os.environ.setdefault('ENV_TYPE', 'development')

application = get_wsgi_application()
