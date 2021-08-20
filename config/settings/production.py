# DEBUG = True
DEBUG = False
ALLOWED_HOSTS = [
    'trend-anaylzer-env.ksmsub4jne.ap-south-1.elasticbeanstalk.com',
    'www.thetrendanalysis.com',
    'thetrendanalysis.com'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "trend_analyzer",
        'USER': "root",
        'PASSWORD': "Oeidk23idfoi:@",
        'HOST': "localhost",
        'PORT': '3306',
    }
}
