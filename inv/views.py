from django.shortcuts import render, redirect 
from django.urls import reverse_lazy
## importamos el paquete de vista generica
from django.views import generic

# para ver las categorias sera necesario estar logeado..... y para evitar que se vean vistas sin permiso utilizamos permissionrequiredmixin.
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin 

## permisos requeridos en funciones
from django.contrib.auth.decorators import login_required, permission_required

# para trabajar con mensajes cuando realizamos alguna accion en las plantillas
from django.contrib.messages.views import SuccessMessageMixin

from .models import Categoria, Marca, Producto, SubCategoria, UnidadMedida  ## importamos el modelo en el cual vamos a actuar.
from .forms import CategoriaForm, MarcaForm, ProductoForm, SubCategoriaForm, UMForm ## importamos el formulario sobre el cual daremos de alta,eliminaremos o editaremos las categorias

## importamos la vista sin permisos creada en el modulo bases
from bases.views import SinPrivilegios

class CategoriaView(SinPrivilegios, generic.ListView):
    permission_required = "inv.view_categoria" ## se le indica cual es el permiso que se necesita para poder entrar a esta vista.
    model = Categoria
    template_name = "inv/categoria_list.html"
    context_object_name = "obj"

 ## Vista para crear nueva Categoria en el modelo.
class CategoriaNew(SuccessMessageMixin,SinPrivilegios, generic.CreateView):
    permission_required="inv.add_categoria"
    model = Categoria
    template_name = "inv/categoria_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    success_url = reverse_lazy('inv:categoria_list')  ## ruta al tener exito en el evento.
    success_message = "Categoría Creada Satisfactoriamente"

    ## Necesitamos obtener el id del usuario que crea la categoria, por eso sobreescribimos la funcion
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

 ## Vista para editar una Categoria existente en el modelo.
class CategoriaEdit(SuccessMessageMixin,SinPrivilegios, generic.UpdateView):
    permission_required="inv.change_categoria"
    model = Categoria
    template_name = "inv/categoria_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    success_url = reverse_lazy('inv:categoria_list')  ## ruta al tener exito en el evento.
    success_message = "Categoría Actualizada Satisfactoriamente"

    ## Necesitamos obtener el id del usuario que modifica la categoria, por eso sobreescribimos la funcion y obtenemos el id.
    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)
 
## Vista para eliminar una Categoria existente en el modelo.
class CategoriaDel(SuccessMessageMixin,SinPrivilegios, generic.DeleteView):
    permission_required="inv.delete_categoria"
    model=Categoria
    template_name='inv/modal_del.html' ## a este template le ponemos un nombre mas generico, para utilizarlo con los demas modelos que se vayan implementando.
    context_object_name='obj'
    success_url=reverse_lazy("inv:categoria_list")  ## utilizamos categoria_list, porque mostraremos un mensaje para asegurarnos de que se quiere eliminar el registro.
    success_message="Categoría Eliminada Satisfactoriamente"

####################
#    SubCategoria  #
####################
 ## Vista para crear nueva SubCategoria en el modelo.
class SubCategoriaView(SinPrivilegios, generic.ListView):
    permission_required = "inv.view_subcategoria"
    model = SubCategoria
    template_name = "inv/subcategoria_list.html"
    context_object_name = "obj"

 ## Vista para crear nueva SubCategoria en el modelo.
class SubCategoriaNew(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required="inv.add_subcategoria"
    model = SubCategoria
    template_name = "inv/subcategoria_form.html"
    context_object_name = "obj"
    form_class = SubCategoriaForm
    success_url = reverse_lazy('inv:subcategoria_list')  ## ruta al tener exito en el evento.
    success_message="SubCategoría Creada Satisfactoriamente"

    ## Necesitamos obtener el id del usuario que crea la categoria, por eso sobreescribimos la funcion
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

 ## Vista para editar una SubCategoria existente en el modelo.
class SubCategoriaEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    permission_required="inv.change_subcatetoria"
    model = SubCategoria
    template_name = "inv/subcategoria_form.html"
    context_object_name = "obj"
    form_class = SubCategoriaForm
    success_url = reverse_lazy('inv:subcategoria_list')  ## ruta al tener exito en el evento.
    success_message="SubCategoría Actualizada Satisfactoriamente"

    ## Necesitamos obtener el id del usuario que modifica la categoria, por eso sobreescribimos la funcion y obtenemos el id.
    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

## Vista para eliminar una SubCategoria existente en el modelo.
class SubCategoriaDel(SuccessMessageMixin, SinPrivilegios, generic.DeleteView):
    permission_required="inv.delete_subcategoria"
    model=SubCategoria
    template_name='inv/modal_del.html' ## a este template le ponemos un nombre mas generico, para utilizarlo con los demas modelos que se vayan implementando.
    context_object_name='obj'
    success_url=reverse_lazy("inv:subcategoria_list")  ## utilizamos categoria_list, porque mostraremos un mensaje para asegurarnos de que se quiere eliminar el registro.
    success_message="SubCategoría Eliminada Satisfactoriamente"

## Seguimos el mismo patron para los demas modelos creados Marca, UnidadMedida, etc.

## Vistas para Marca
class MarcaView(SinPrivilegios,\
     generic.ListView):
    permission_required = "inv.view_marca"
    model = Marca
    template_name = "inv/marca_list.html"
    context_object_name = "obj"


class MarcaNew(SuccessMessageMixin,SinPrivilegios,
                   generic.CreateView):
    model=Marca
    template_name="inv/marca_form.html"
    context_object_name = 'obj'
    form_class=MarcaForm
    success_url= reverse_lazy("inv:marca_list")
    success_message="Marca Creada Satisfactoriamente"
    permission_required="inv.add_marca"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class MarcaEdit(SuccessMessageMixin,SinPrivilegios,
                   generic.UpdateView):
    model=Marca
    template_name="inv/marca_form.html"
    context_object_name = 'obj'
    form_class=MarcaForm
    success_url= reverse_lazy("inv:marca_list")
    success_message="Marca Actualizada Satisfactoriamente"
    permission_required="inv.change_marca"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


##### Implemento la vista basada en funciones, para no eliminar los registros, si no simplemente desactivar el registro. 
## ejemplo con Marca

##uso de decoradores django para permisos basados en funciones
@login_required(login_url='/login/')
@permission_required('inv.change_marca', login_url='bases:sin_privilegios')
def marca_desactivar(request, id):
    marca = Marca.objects.filter(pk=id).first()
    contexto = {}
    template_name = "inv/modal_del.html"

    if not marca:
        return redirect("inv:marca_list")

    if request.method == 'GET':
        contexto={'obj':marca}

    if request.method == 'POST':
        marca.estado=False
        marca.save()
        return redirect("inv:marca_list")

    return render(request,template_name,contexto)

## Vistas para Unidad de Medida
class UMView( SinPrivilegios, generic.ListView):
    permission_required = "inv.view_unidad_medida"
    model = UnidadMedida
    template_name = "inv/um_list.html"
    context_object_name = "obj"
    

class UMNew(SuccessMessageMixin,SinPrivilegios,generic.CreateView):
    permission_required="inv.add_unidadmedida"
    model=UnidadMedida
    template_name="inv/um_form.html"
    context_object_name = 'obj'
    form_class=UMForm
    success_url= reverse_lazy("inv:um_list")
    success_message="Unidad Medida Creada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        print(self.request.user.id)
        return super().form_valid(form)


class UMEdit(SuccessMessageMixin,SinPrivilegios,generic.UpdateView):
    permission_required="inv.change_unidadmedida"
    model=UnidadMedida
    template_name="inv/um_form.html"
    context_object_name = 'obj'
    form_class=UMForm
    success_url= reverse_lazy("inv:um_list")
    success_message="Unidad Medida Actualizada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        print(self.request.user.id)
        return super().form_valid(form)

##uso de decoradores django para permisos basados en funciones
@login_required(login_url='/login/')
@permission_required('inv.change_unidadmedida', login_url='bases:sin_privilegios')
def um_desactivar(request, id):
    um = UnidadMedida.objects.filter(pk=id).first()
    contexto={}
    template_name="inv/modal_del.html"

    if not um:
        return redirect("inv:um_list")
    
    if request.method=='GET':
        contexto={'obj':um}
    
    if request.method=='POST':
        um.estado=False
        um.save()
        return redirect("inv:um_list")

    return render(request,template_name,contexto)


## Vistas Producto(s)
class ProductoView( SinPrivilegios, generic.ListView):
    permission_required = "inv.view_producto"
    model = Producto
    template_name = "inv/producto_list.html"
    context_object_name = "obj"


class ProductoNew(SuccessMessageMixin,SinPrivilegios,generic.CreateView):
    permission_required="inv.add_producto"
    model=Producto
    template_name="inv/producto_form.html"
    context_object_name = 'obj'
    form_class=ProductoForm
    success_url= reverse_lazy("inv:producto_list")
    success_message="Producto Creado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class ProductoEdit(SuccessMessageMixin,SinPrivilegios,generic.UpdateView):
    permission_required="inv.change_producto"
    model=Producto
    template_name="inv/producto_form.html"
    context_object_name = 'obj'
    form_class=ProductoForm
    success_url= reverse_lazy("inv:producto_list")
    success_message="Producto Actualizado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

##uso de decoradores django para permisos basados en funciones
@login_required(login_url='/login/')
@permission_required('inv.change_producto', login_url='bases:sin_privilegios')
def producto_desactivar(request, id):
    prod = Producto.objects.filter(pk=id).first()
    contexto={}
    template_name="inv/modal_del.html"

    if not prod:
        return redirect("inv:producto_list")
    
    if request.method=='GET':
        contexto={'obj':prod}
    
    if request.method=='POST':
        prod.estado=False
        prod.save()
        return redirect("inv:producto_list")

    return render(request,template_name,contexto)