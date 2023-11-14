from django.shortcuts import render
from django.urls import reverse_lazy
## importamos el paquete de vista generica
from django.views import generic

# para ver las categorias sera necesario estar logeado..
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Categoria, Marca, SubCategoria  ## importamos el modelo en el cual vamos a actuar.
from .forms import CategoriaForm, MarcaForm, SubCategoriaForm ## importamos el formulario sobre el cual daremos de alta,eliminaremos o editaremos las categorias

class CategoriaView(LoginRequiredMixin, generic.ListView):
    model = Categoria
    template_name = "inv/categoria_list.html"
    context_object_name = "obj"
    login_url = 'config:login'

 ## Vista para crear nueva Categoria en el modelo.
class CategoriaNew(LoginRequiredMixin, generic.CreateView):
    model = Categoria
    template_name = "inv/categoria_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    success_url = reverse_lazy('inv:categoria_list')  ## ruta al tener exito en el evento.
    login_url = "config:login"

    ## Necesitamos obtener el id del usuario que crea la categoria, por eso sobreescribimos la funcion
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

 ## Vista para editar una Categoria existente en el modelo.
class CategoriaEdit(LoginRequiredMixin, generic.UpdateView):
    model = Categoria
    template_name = "inv/categoria_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    success_url = reverse_lazy('inv:categoria_list')  ## ruta al tener exito en el evento.
    login_url = "config:login"

    ## Necesitamos obtener el id del usuario que modifica la categoria, por eso sobreescribimos la funcion y obtenemos el id.
    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)
 
## Vista para eliminar una Categoria existente en el modelo.
class CategoriaDel(LoginRequiredMixin, generic.DeleteView):
    model=Categoria
    template_name='inv/catalogos_del.html' ## a este template le ponemos un nombre mas generico, para utilizarlo con los demas modelos que se vayan implementando.
    context_object_name='obj'
    success_url=reverse_lazy("inv:categoria_list")  ## utilizamos categoria_list, porque mostraremos un mensaje para asegurarnos de que se quiere eliminar el registro.
    success_message="Categoría Eliminada Satisfactoriamente"

####################
#    SubCategoria  #
####################
 ## Vista para crear nueva SubCategoria en el modelo.
class SubCategoriaView(LoginRequiredMixin, generic.ListView):
    model = SubCategoria
    template_name = "inv/subcategoria_list.html"
    context_object_name = "obj"
    login_url = "config:login"

 ## Vista para crear nueva SubCategoria en el modelo.
class SubCategoriaNew(LoginRequiredMixin, generic.CreateView):
    model = SubCategoria
    template_name = "inv/subcategoria_form.html"
    context_object_name = "obj"
    form_class = SubCategoriaForm
    success_url = reverse_lazy('inv:subcategoria_list')  ## ruta al tener exito en el evento.
    login_url = "config:login"

    ## Necesitamos obtener el id del usuario que crea la categoria, por eso sobreescribimos la funcion
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

 ## Vista para editar una SubCategoria existente en el modelo.
class SubCategoriaEdit(LoginRequiredMixin, generic.UpdateView):
    model = SubCategoria
    template_name = "inv/subcategoria_form.html"
    context_object_name = "obj"
    form_class = SubCategoriaForm
    success_url = reverse_lazy('inv:subcategoria_list')  ## ruta al tener exito en el evento.
    login_url = "config:login"

    ## Necesitamos obtener el id del usuario que modifica la categoria, por eso sobreescribimos la funcion y obtenemos el id.
    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

## Vista para eliminar una SubCategoria existente en el modelo.
class SubCategoriaDel(LoginRequiredMixin, generic.DeleteView):
    model=SubCategoria
    template_name='inv/catalogos_del.html' ## a este template le ponemos un nombre mas generico, para utilizarlo con los demas modelos que se vayan implementando.
    context_object_name='obj'
    success_url=reverse_lazy("inv:subcategoria_list")  ## utilizamos categoria_list, porque mostraremos un mensaje para asegurarnos de que se quiere eliminar el registro.
    success_message="Categoría Eliminada Satisfactoriamente"

## Seguimos el mismo patron para los demas modelos creados Marca, UnidadMedida, etc.

## Vistas para Marca
class MarcaView(LoginRequiredMixin,\
     generic.ListView):
    permission_required = "inv.view_marca"
    model = Marca
    template_name = "inv/marca_list.html"
    context_object_name = "obj"


class MarcaNew(LoginRequiredMixin,
                   generic.CreateView):
    model=Marca
    template_name="inv/marca_form.html"
    context_object_name = 'obj'
    form_class=MarcaForm
    success_url= reverse_lazy("inv:marca_list")
    success_message="Marca Creada"
    permission_required="inv.add_marca"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class MarcaEdit(LoginRequiredMixin,
                   generic.UpdateView):
    model=Marca
    template_name="inv/marca_form.html"
    context_object_name = 'obj'
    form_class=MarcaForm
    success_url= reverse_lazy("inv:marca_list")
    success_message="Marca Editada"
    permission_required="inv.change_marca"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)
