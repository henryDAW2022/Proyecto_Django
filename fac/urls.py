from django.urls import path, include


## modulo reporte pdf
# from .reportes import imprimir_factura_recibo, imprimir_factura_list

from .views import ClienteView, ClienteNew, ClienteEdit,clienteDesactivar

urlpatterns = [
    path('clientes/',ClienteView.as_view(), name="cliente_list"),
    path('clientes/new',ClienteNew.as_view(), name="cliente_new"),
    path('clientes/<int:pk>',ClienteEdit.as_view(), name="cliente_edit"),
    path('clientes/estado/<int:id>',clienteDesactivar, name="cliente_desactivar"),
]