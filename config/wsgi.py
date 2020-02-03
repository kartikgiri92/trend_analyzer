import os

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.production'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.local')

application = get_wsgi_application()
