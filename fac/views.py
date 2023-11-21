
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import generic
from bases.views import SinPrivilegios
from django.contrib import messages


from .models import Cliente, FacturaEnc,FacturaDet
from .forms import ClienteForm
import inv.views as inv
from inv.models import Producto

class ClienteView(SinPrivilegios, generic.ListView):
    model = Cliente
    template_name = "fac/cliente_list.html"
    context_object_name = "obj"
    permission_required="fac.view_cliente"


## Herencia basada en classes sobreescribiendo algunas propiedades genericas en las clases.
class VistaBaseCreate(SuccessMessageMixin,SinPrivilegios, \
    generic.CreateView):
    context_object_name = 'obj'
    success_message="Registro Agregado Satisfactoriamente" ##ejemplo: mensaje mas generico al agregar un registro

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class VistaBaseEdit(SuccessMessageMixin,SinPrivilegios, \
    generic.UpdateView):
    context_object_name = 'obj'
    success_message="Registro Actualizado Satisfactoriamente"  ##ejemplo: mensaje mas generico al agregar un registro

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

## aplico la herencia en esta clase, de la vistaBasecreate
class ClienteNew(VistaBaseCreate):
    model=Cliente
    template_name="fac/cliente_form.html"
    form_class=ClienteForm
    success_url= reverse_lazy("fac:cliente_list")
    permission_required="fac.add_cliente"
'''
    def get(self, request, *args, **kwargs):
        print("sobre escribir get")
        
        try:
            t = request.GET["t"]
        except:
            t = None

        print(t)
        
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 't':t})
'''
## aplico la herencia en esta clase, de la vistaBaseCreate
class ClienteEdit(VistaBaseEdit):
    model=Cliente
    template_name="fac/cliente_form.html"
    form_class=ClienteForm
    success_url= reverse_lazy("fac:cliente_list")
    permission_required="fac.change_cliente"
'''
    def get(self, request, *args, **kwargs):
        print("sobre escribir get en editar")

        print(request)
        
        try:
            t = request.GET["t"]
        except:
            t = None

        print(t)
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form,t=t)
        print(form_class,form,context)
        return self.render_to_response(context)
'''

@login_required(login_url="/login/")
@permission_required("fac.change_cliente",login_url="/login/")
def clienteDesactivar(request,id):
    cliente = Cliente.objects.filter(pk=id).first()

    if request.method=="POST":
        if cliente:
            cliente.estado = not cliente.estado
            cliente.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")

class FacturaView(SinPrivilegios, generic.ListView):
    model = FacturaEnc
    template_name = "fac/factura_list.html"
    context_object_name = "obj"
    permission_required="fac.view_facturaenc"



@login_required(login_url='/login/')
@permission_required('fac.change_facturaenc', login_url='bases:sin_privilegios')
def facturas(request,id=None):
    template_name='fac/facturas.html'

    # encabezado = {
    #     'fecha':datetime.today()
    # }
    detalle = {}
    clientes = Cliente.objects.filter(estado=True)

    ## Compruebo que el metodo sea GET
    if request.method == "GET":
        enc = FacturaEnc.objects.filter(pk=id).first() ## filtro el modelo por id.

        ## Compruebo si no existe, y lo inicializo el encabezado con los atributos
        if not enc:
            encabezado = {
                'id':0,
                'fecha':datetime.today(),
                'cliente':0,
                'sub_total':0,
                'descuento':0,
                'total': 0
            }
            detalle=None
        else:
            encabezado = {
                'id':enc.id,
                'fecha':enc.fecha,
                'cliente':enc.cliente,
                'sub_total':enc.sub_total,
                'descuento':enc.descuento,
                'total':enc.total
            }

        detalle=FacturaDet.objects.filter(factura=enc)
        contexto = {"enc":encabezado,"det":detalle,"clientes":clientes}

    ## si es de tipo post, capturamos los parametros, 
    if request.method == "POST":
        cliente = request.POST.get("enc_cliente")
        fecha  = request.POST.get("fecha")
        cli=Cliente.objects.get(pk=cliente)  ## verifico si existe el cliente por medio de capturar id.

        if not id: ## si no existe id la factura es nueva.
            enc = FacturaEnc(
                cliente = cli,
                fecha = fecha
            )
            if enc:
                enc.save()
                id = enc.id
        else:
            enc = FacturaEnc.objects.filter(pk=id).first() ## si si existe filtramos
            if enc:
                enc.cliente = cli ## lo unico que se puede modificar en este caso.
                enc.save()

        if not id:
            messages.error(request,'No existe No. de Factura')
            return redirect("fac:factura_list")
        
        codigo = request.POST.get("codigo")
        cantidad = request.POST.get("cantidad")
        precio = request.POST.get("precio")
        s_total = request.POST.get("sub_total_detalle")
        descuento = request.POST.get("descuento_detalle")
        total = request.POST.get("total_detalle")

        prod = Producto.objects.get(codigo=codigo) ## capturamos los parametros del producto
        det = FacturaDet(
            factura = enc,
            producto = prod,
            cantidad = cantidad,
            precio = precio,
            sub_total = s_total,
            descuento = descuento,
            total = total
        )
        
        if det:
            det.save()
        
        return redirect("fac:factura_edit",id=id)

    return render(request,template_name,contexto)


## Reutilizacion de vistas, simplemente estamos redirigiendo a otra plantilla.
class ProductoView(inv.ProductoView):
    template_name="fac/buscar_producto.html"