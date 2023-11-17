from django.urls import path, include

from .views import CompraDetDelete, ComprasView, ProveedorView, ProveedorNew, ProveedorEdit, compras, proveedorDesactivar

urlpatterns = [
    path('proveedores/', ProveedorView.as_view(), name= 'proveedor_list'),
    path('proveedores/new', ProveedorNew.as_view(), name= 'proveedor_new'),
    path('proveedores/edit/<int:pk>', ProveedorEdit.as_view(), name= 'proveedor_edit'),
    path('proveedores/desactivar/<int:id>', proveedorDesactivar, name= 'proveedor_desactivar'),

    ## Compras
    path('compras/', ComprasView.as_view(), name= 'compras_list'),
    path('compras/new', compras, name= 'compras_new'),
    path('compras/edit/<int:compra_id>', compras, name= 'compras_edit'),
    path('compras/<int:compra_id>/delete/<int:pk>', CompraDetDelete.as_view(), name= 'compras_del'),
]