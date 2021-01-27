DEBUG = True
ALLOWED_HOSTS = []

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
