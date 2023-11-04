from django.shortcuts import render,redirect
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password  ## para no ver la password
from django.contrib.auth.decorators import login_required, permission_required

from .models import Usuario
from .forms import Userform

## vista pagina principal Home
class Home(LoginRequiredMixin,TemplateView):
    template_name = 'bases/home.html'
    login_url = 'config:login'

## Vista lista de usuarios
class UserList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name ='bases/users_list.html'
    login_url = 'config:login'
    model = Usuario
    permission_required = 'bases:view_usuario'
    context_object_name = 'obj'
    
@login_required(login_url='config:login')   ## Incluimos estas lineas, 
@permission_required('bases.change_usuario',login_url='config:home') ## para asegurar los permisos de edicion y modificacion de datos si el usuario no dispone de permisos
## Vista para crear o modificar un usuario
def user_admin(request, pk=None):
    template_name = "bases/users_add.html"
    context = {}
    form = None
    obj = None

    ## Identificamos el metodo de envio del formulario y realizamos las acciones oportunas.
    if request.method == 'GET':
        if not pk:
            form = Userform(instance= None)
        else:
            obj = Usuario.objects.filter(id=pk).first()
            form = Userform(instance = obj)
        context["form"] = form
        context["obj"] = obj
    if request.method == 'POST':
        data = request.POST       ## capturamos los datos del formulario
        e = data.get("email")
        fn = data.get("first_name")
        ln = data.get("last_name")
        p = data.get("password")

        if pk:   ## validamos si existe el pk.
             obj = Usuario.objects.filter(id=pk).first()
             if not obj:
                print("Error, el usuario no existe")
             else:
                obj.email = e
                obj.first_name = fn
                obj.last_name = ln
                obj.password = make_password(p)
                obj.save()
        
        else:  ## opcion en el caso de que no exista ese pk, usuario nuevo.
            obj = Usuario.objects.create_user(
                email = e,
                password = p,
                first_name = fn,
                last_name = ln
            )
            print(obj.email,obj.password) ##simplemente es para ver si se esta grabando bien

        return redirect('config:users_list')

    return render(request,template_name,context)