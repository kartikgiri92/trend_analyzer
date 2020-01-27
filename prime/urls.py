from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers

import prime.views as prime_views

app_name = 'prime'
urlpatterns = [

    path('foung/', prime_views.foung.as_view()),

    path('get-trend/', prime_views.GetTrend.as_view()),
    path('get-trend/<int:id>/', prime_views.GetTrend.as_view()),

    path('get-active-trend/', prime_views.GetActiveTrend.as_view()),
    
]