from django.shortcuts import render
from django.urls import reverse_lazy

## importamos el paquete de vista generica
from django.views import generic

# para ver las categorias sera necesario estar logeado..
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse
import json  ## esto para trabajar con ajax.


from .models import Proveedor
from cmp.forms import ProveedorForm

class ProveedorView(LoginRequiredMixin, generic.ListView):
    model = Proveedor
    template_name = "cmp/proveedor_list.html"
    context_object_name = "obj"

class ProveedorNew(LoginRequiredMixin,\
                   generic.CreateView):
    model=Proveedor
    template_name="cmp/proveedor_form.html"
    context_object_name = 'obj'
    form_class=ProveedorForm
    success_url= reverse_lazy("cmp:proveedor_list")
    success_message="Proveedor Nuevo"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        print(self.request.user.id)   
        return super().form_valid(form)


class ProveedorEdit(LoginRequiredMixin,\
                   generic.UpdateView):
    model=Proveedor
    template_name="cmp/proveedor_form.html"
    context_object_name = 'obj'
    form_class=ProveedorForm
    success_url= reverse_lazy("cmp:proveedor_list")
    success_message="Proveedor Editado"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        print(self.request.user.id)
        return super().form_valid(form)


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