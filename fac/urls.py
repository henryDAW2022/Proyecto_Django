from django.urls import path, include


# modulo reporte pdf
from .reportes import reporte_facturas, imprimir_factura

from .views import ClienteView, ClienteNew, ClienteEdit, clienteDesactivar, FacturaView, facturas, ProductoView, borrar_detalle_factura

urlpatterns = [
    ## Clientes
    path('clientes/',ClienteView.as_view(), name="cliente_list"),
    path('clientes/new',ClienteNew.as_view(), name="cliente_new"),
    path('clientes/<int:pk>',ClienteEdit.as_view(), name="cliente_edit"),
    path('clientes/estado/<int:id>',clienteDesactivar, name="cliente_desactivar"),

    ## Facturas
    path('facturas/',FacturaView.as_view(), name="factura_list"),
    path('facturas/new',facturas, name="factura_new"),
    path('facturas/edit/<int:id>',facturas, name='factura_edit'),
    
    path('facturas/buscar-producto',ProductoView.as_view(), name='factura_producto'),

    path('facturas/borrar-detalle/<int:id>',borrar_detalle_factura, name="factura_borrar_detalle"),

    ## PDFs
    path('facturas/listado', reporte_facturas, name= 'facturas_print_all'),
    path('facturas/<int:factura_id>/imprimir', imprimir_factura, name= 'facturas_print_one'),
]