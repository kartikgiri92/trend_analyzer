from ..base import *

deployment_type = os.environ.get("deployment_type", 'development')
print("***** {} *****".format(deployment_type))

if deployment_type == "production":
    from .production import *

    STATIC_URL = '/static/'
    STATIC_ROOT = 'static'

else:
    from .local import *

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
