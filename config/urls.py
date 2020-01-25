from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

admin.site.site_header = 'Website Admin'

urlpatterns = [
    path('abcd/admin/', admin.site.urls),
    # path('api/profiles/', include('profiles.urls')),
    # path('api/messaging/', include('messaging.urls')),
]
