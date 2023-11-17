from django.shortcuts import render,redirect
from django.urls import reverse_lazy
import datetime

## importamos el paquete de vista generica
from django.views import generic

# para ver las categorias sera necesario estar logeado..
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.http import HttpResponse
import json  ## esto para trabajar con ajax.
from django.db.models import Sum

## importamos la vista sin permisos creada en el modulo bases
from bases.views import SinPrivilegios
from inv.models import Producto


from .models import Proveedor, ComprasDet, ComprasEnc
from cmp.forms import ComprasEncForm, ProveedorForm

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


@login_required(login_url='/login/')
@permission_required('cmp.view_comprasenc', login_url='bases:sin_privilegios')
def compras(request,compra_id=None):
    template_name="cmp/compras.html"
    prod=Producto.objects.filter(estado=True) ## obtenemos todos los productos activos.
    form_compras={} ## declaro estas variables de contexto vacias.
    contexto={}  ## para poder popularlas mas adelante.

    if request.method=='GET':
        form_compras=ComprasEncForm() ## almacenamos el formulariode compras.
        enc = ComprasEnc.objects.filter(pk=compra_id).first()  ## filtramos para ver si existe ese encabezado
        
        if enc: ## si existe tomamos los valores
            det = ComprasDet.objects.filter(compra=enc)
            fecha_compra = datetime.date.isoformat(enc.fecha_compra)
            fecha_factura = datetime.date.isoformat(enc.fecha_factura)
            e = {
                'fecha_compra':fecha_compra,  ## estos seran los valores del formulario
                'proveedor': enc.proveedor,
                'observacion': enc.observacion,
                'no_factura': enc.no_factura,
                'fecha_factura': fecha_factura,
                'sub_total': enc.sub_total,
                'descuento': enc.descuento,
                'total':enc.total
            }
            form_compras = ComprasEncForm(e)  ## populamos el formulario
        else:
            det=None ## si no existe lo dejamos vacio.
    
        contexto={'productos':prod,'encabezado':enc,'detalle':det,'form_enc':form_compras} ## estas son las variables para la plantilla.

    if request.method=='POST':
        fecha_compra = request.POST.get("fecha_compra")
        observacion = request.POST.get("observacion")
        no_factura = request.POST.get("no_factura")
        fecha_factura = request.POST.get("fecha_factura")
        proveedor = request.POST.get("proveedor")
        sub_total = 0
        descuento = 0
        total = 0

        if not compra_id:
            prov=Proveedor.objects.get(pk=proveedor)

            enc = ComprasEnc(
                fecha_compra=fecha_compra,
                observacion=observacion,
                no_factura=no_factura,
                fecha_factura=fecha_factura,
                proveedor=prov,
                uc = request.user 
            )
            if enc:
                enc.save()
                compra_id=enc.id
        else:
            enc=ComprasEnc.objects.filter(pk=compra_id).first()
            if enc:
                enc.fecha_compra = fecha_compra
                enc.observacion = observacion
                enc.no_factura=no_factura
                enc.fecha_factura=fecha_factura
                enc.um=request.user.id
                enc.save()

        if not compra_id:
            return redirect("cmp:compras_list")
        
        ## Aqui recogemos los campos para la parte de lineas de compra
        producto = request.POST.get("id_id_producto")
        cantidad = request.POST.get("id_cantidad_detalle")
        precio = request.POST.get("id_precio_detalle")
        sub_total_detalle = request.POST.get("id_sub_total_detalle")
        descuento_detalle  = request.POST.get("id_descuento_detalle")
        total_detalle  = request.POST.get("id_total_detalle")

        prod = Producto.objects.get(pk=producto)

        det = ComprasDet(
            compra=enc,
            producto=prod,
            cantidad=cantidad,
            precio_prv=precio,
            descuento=descuento_detalle,
            costo=0,
            uc = request.user
        )

        if det:
            det.save()

            sub_total=ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('sub_total'))  ## hacemos que filtre por el id de compra.
            descuento=ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('descuento'))
            enc.sub_total = sub_total["sub_total__sum"]
            enc.descuento=descuento["descuento__sum"]
            enc.save()

        return redirect("cmp:compras_edit",compra_id=compra_id)   
    
    return render(request, template_name, contexto)

## Vista para eliminar detalles de compras
class CompraDetDelete(SinPrivilegios, generic.DeleteView):
    permission_required = "cmp.delete_comprasdet"
    model = ComprasDet
    template_name = "cmp/compras_det_del.html"
    context_object_name = 'obj'
    
    def get_success_url(self):
          compra_id=self.kwargs['compra_id']
          return reverse_lazy('cmp:compras_edit', kwargs={'compra_id': compra_id})