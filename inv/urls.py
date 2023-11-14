from django.urls import path

from .views import CategoriaDel, CategoriaView, CategoriaNew, CategoriaEdit, MarcaEdit, MarcaNew, MarcaView, ProductoEdit, ProductoNew, ProductoView, SubCategoriaDel, \
SubCategoriaView,SubCategoriaEdit, SubCategoriaNew, UMEdit, UMNew, UMView, marca_desactivar, producto_desactivar, um_desactivar

# \ es un salto de linea para seguir con el misma linea de codigo

urlpatterns = [
    path('categorias/',CategoriaView.as_view(),name='categoria_list'),
    path('categorias/new',CategoriaNew.as_view(),name='categoria_new'),
    path('categorias/edit/<int:pk>',CategoriaEdit.as_view(),name='categoria_edit'),
    path('categorias/delete/<int:pk>',CategoriaDel.as_view(),name='categoria_del'),

    ## SubCategorias
    path('subcategorias/',SubCategoriaView.as_view(),name='subcategoria_list'),
    path('subcategorias/new',SubCategoriaNew.as_view(),name='subcategoria_new'),
    path('subcategorias/edit/<int:pk>',SubCategoriaEdit.as_view(),name='subcategoria_edit'),
    path('subcategorias/delete/<int:pk>',SubCategoriaDel.as_view(),name='subcategoria_del'),

    ## Marcas
    path('marcas/',MarcaView.as_view(),name='marca_list'),
    path('marcas/new',MarcaNew.as_view(),name='marca_new'),
    path('marcas/edit/<int:pk>',MarcaEdit.as_view(),name='marca_edit'),
    path('marcas/desactivar/<int:id>',marca_desactivar,name='marca_desactivar'),

    ## Unidad de Medida
    path('um/',UMView.as_view(), name="um_list"),
    path('um/new',UMNew.as_view(), name="um_new"),
    path('um/edit/<int:pk>',UMEdit.as_view(), name="um_edit"),
    path('um/desactivar/<int:id>',um_desactivar, name="um_desactivar"),

    ## Productos
    path('productos/',ProductoView.as_view(), name="producto_list"),
    path('productos/new',ProductoNew.as_view(), name="producto_new"),
    path('productos/edit/<int:pk>',ProductoEdit.as_view(), name="producto_edit"),
    path('productos/desactivar/<int:id>',producto_desactivar, name="producto_desactivar"),
]