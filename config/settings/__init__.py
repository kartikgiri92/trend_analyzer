from ..base import *

deployment_type = os.environ.get("deployment_type", 'staging')
print("***** {} *****".format(deployment_type))

if deployment_type == "production":
    from .production import *

    STATIC_URL = '/var/www/project/static/'
    STATIC_ROOT = 'static'

else:
    from .local import *

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
