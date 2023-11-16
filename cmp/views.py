from django.shortcuts import render
from django.urls import reverse_lazy

## importamos el paquete de vista generica
from django.views import generic

# para ver las categorias sera necesario estar logeado..
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.http import HttpResponse
import json  ## esto para trabajar con ajax.

## importamos la vista sin permisos creada en el modulo bases
from bases.views import SinPrivilegios
from inv.models import Producto


from .models import Proveedor, ComprasDet, ComprasEnc
from cmp.forms import ProveedorForm

class ProveedorView(SinPrivilegios, generic.ListView):
    permission_required = "inv.view_proveedor" 
    model = Proveedor
    template_name = "cmp/proveedor_list.html"
    context_object_name = "obj"

class ProveedorNew(SuccessMessageMixin, SinPrivilegios,generic.CreateView):
    permission_required="cmp.add_proveedor"
    model=Proveedor
    template_name="cmp/proveedor_form.html"
    context_object_name = 'obj'
    form_class=ProveedorForm
    success_url= reverse_lazy("cmp:proveedor_list")
    success_message="Proveedor Nuevo Crado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        print(self.request.user.id)   
        return super().form_valid(form)


class ProveedorEdit(SuccessMessageMixin, SinPrivilegios,generic.UpdateView):
    permission_required="cmp.change_proveedor"
    model=Proveedor
    template_name="cmp/proveedor_form.html"
    context_object_name = 'obj'
    form_class=ProveedorForm
    success_url= reverse_lazy("cmp:proveedor_list")
    success_message="Proveedor Actualizado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        print(self.request.user.id)
        return super().form_valid(form)

##uso de decoradores django para permisos basados en funciones
@login_required(login_url='/login/')
@permission_required('cmp.change_proveedor', login_url='bases:sin_privilegios')
def proveedorDesactivar(request,id):
    template_name = 'cmp/desactivar_prv.html'
    contexto = {}
    prv = Proveedor.objects.filter(pk=id).first()

    if not prv:
        return HttpResponse('Proveedor no existe ' + str(id))

    if request.method=='GET':
        contexto = {'obj':prv}

    if request.method=='POST':
        prv.estado=False
        prv.save()
        contexto = {'obj':'OK'}
        return HttpResponse('Proveedor Desactivado')

    return render(request,template_name,contexto)

###############################################

## Vistas Compras

class ComprasView(SinPrivilegios, generic.ListView):
    model = ComprasEnc
    template_name = "cmp/compras_list.html"
    context_object_name = "obj"
    permission_required="cmp.view_comprasenc"


