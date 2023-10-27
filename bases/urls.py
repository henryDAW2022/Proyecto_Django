from django.urls import path

from bases.views import *

app_name = "config"

urlpatterns = [
    path('',Home.as_view(),name='home'),
]