from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.views.generic import TemplateView

admin.site.site_header = 'Website Admin'

urlpatterns = [
    path('abcd/admin/', admin.site.urls),
    path('api/prime/', include('prime.urls')),
    path('', TemplateView.as_view(template_name="prime/homepage.html")),
]
