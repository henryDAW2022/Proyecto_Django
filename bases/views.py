from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission


from .models import Usuario


class Home(LoginRequiredMixin,TemplateView):
    template_name = 'bases/home.html'
    login_url = 'config:login'

class UserList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name ='bases/users_list.html'
    login_url = 'config:login'
    model = Usuario
    permission_required = 'bases:view_usuario'
    context_object_name = 'obj'
    