from django.contrib import messages
from django.shortcuts import render,redirect
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password  ## para no ver la password
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import request
from django.http.response import HttpResponse,Http404

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

        ## Añado permisos (Grupos) a usuarios
        grupos_usuarios = None
        grupos = None
        if obj:
            grupos_usuarios = obj.groups.all() ## obtengo todos los grupos que estan asignados al usuario
            grupos = Group.objects.filter(~Q(id__in=obj.groups.values('id'))) ## devuelve todos los grupos menos los que ya estan asignados al usuario

        context["grupos_usuario"] = grupos_usuarios
        context["grupos"] = grupos

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


## Vista de grupos de usuarios
class UserGroupList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name ='bases/users_group_list.html'
    login_url = 'config:login'
    model = Group
    permission_required = 'bases:view_usuario'
    context_object_name = 'obj'


@login_required(login_url='config:login')
@permission_required('bases.change_usuario',login_url='bases:login')
def user_groups_admin(request,pk=None):
    template_name = 'bases/users_group_add.html'
    context = {}

    obj = Group.objects.filter(id=pk).first()
    context["obj"] = obj
    permisos = {}
    permisos_grupo = {}
    context["permisos"] = permisos
    context["permisos_grupo"] = permisos_grupo

    if obj:
        permisos_grupo = obj.permissions.all()
        context["permisos_grupo"] = permisos_grupo

        permisos = Permission.objects.filter(~Q(group=obj))  ## devuelve todos los permisos donde no este asignado obj
        context["permisos"] = permisos
    
    # print(permisos)
    # print(permisos_grupo)  ## ver que es lo que esta sucediendo
    
    ## Comprobamos si existe el grupo.
    if request.method == 'POST':
        name = request.POST.get("name")
        grp = Group.objects.filter(name=name).first()

        if grp and grp.id != pk:
            print("El grupo ya existe, elija otro nombre para crearlo")
            messages.error(request,"El grupo ya existe, elija otro nombre para crearlo")
            return redirect("config:user_groups_new")

        if not grp and pk != None: ## El grupo existe, se esta cambiando el nombre
            grp = Group.objects.filter(id=pk).first()
            grp.name = name
            grp.save()
        elif not grp and pk == None:
            grp = Group(name=name)
        else:
            ...
        
        grp.save()
        messages.success(request,"Grupo Creado Satisfactoriamente")
        return redirect("config:user_groups_modify", grp.id)

    return render(request,template_name,context)


## Vista eliminar grupos de usuarios
@login_required(login_url='config:login')
@permission_required('bases.change_usuario',login_url='bases:login')
def user_group_delete(request,pk):
    if request.method == "POST":
        grp = Group.objects.filter(id=pk).first()

        if not grp:
            print("Groupo no Existe")
        else:
            grp.delete()
        messages.success(request,"Grupo Eliminado Satisfactoriamente")
        return HttpResponse("OK")


## Vista permisos grupos
@login_required(login_url='config:login')
@permission_required('bases.change_usuario',login_url='bases:login')
def user_group_permission(request,id_grp,id_perm):
    if(request.method == "POST"):
        grp = Group.objects.filter(id=id_grp).first()

        if not grp:
            messages.error(request,"Grupo No Existe")
            return HttpResponse("Grupo No Existe")
        
        accion = request.POST.get("accion")
        perm = Permission.objects.filter(id=id_perm).first()
        if not perm:
            messages.error(request,"Permiso no existe")
            return HttpResponse("Permiso No Existe")

        if accion == "ADD":
            grp.permissions.add(perm)
            messages.success(request,"Permiso Agregado")
        elif accion == "DEL":
            grp.permissions.remove(perm)
            messages.success(request,"Permiso Eliminado")
        else:
            messages.error(request,"Accion no Reconocida")
            return HttpResponse("Accion No Reconocida")
        return HttpResponse("OK")    

    return Http404("Método no Reconocido")