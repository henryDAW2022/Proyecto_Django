from django.urls import path
from django.contrib.auth import views as auth_views


from bases.views import *

app_name = "config"  ## Esto lo utilizaremos para referirnos a la ruta bases...para la parte de views.

urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='bases/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='bases/login.html'),name='logout'),
]