from django.urls import path, include


## modulo reporte pdf
# from .reportes import imprimir_factura_recibo, imprimir_factura_list

from .views import ClienteView, ClienteNew, ClienteEdit, clienteDesactivar, FacturaView, facturas, ProductoView

urlpatterns = [
    ## Clientes
    path('clientes/',ClienteView.as_view(), name="cliente_list"),
    path('clientes/new',ClienteNew.as_view(), name="cliente_new"),
    path('clientes/<int:pk>',ClienteEdit.as_view(), name="cliente_edit"),
    path('clientes/estado/<int:id>',clienteDesactivar, name="cliente_desactivar"),

    ## Facturas
    path('facturas/',FacturaView.as_view(), name="factura_list"),
    path('facturas/new',facturas, name="factura_new"),
    path('facturas/buscar-producto',ProductoView.as_view(), name='factura_producto'),
]