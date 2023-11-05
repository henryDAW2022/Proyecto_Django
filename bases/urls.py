from django.urls import path
from django.contrib.auth import views as auth_views


from bases.views import *

app_name = "config"  ## Esto lo utilizaremos para referirnos a la ruta bases...para la parte de views.

urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='bases/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='bases/login.html'),name='logout'),

    ## rutas lista usuarios
    path('users/lists',UserList.as_view(),name='users_list'),

    ## ruta lista usuarios GRUPOS
    path('users/groups/list', UserGroupList.as_view(),name='user_groups_list'),
    path('users/groups/add',user_groups_admin,name='user_groups_new'),
    path('users/groups/modify/<int:pk>',user_groups_admin,name='user_groups_modify'),
    path('users/groups/delete/<int:pk>',user_group_delete,name='user_groups_delete'),

    ## Permisos grupos
    path('users/groups/permission/<int:id_grp>/<int:id_perm>', user_group_permission, name='user_groups_permission'),

    ## rutas crear/modificar usuarios
    path('users/add',user_admin,name='user_add'),
    path('users/modify/<int:pk>',user_admin,name='user_modify'),

    ## rutas menu derecha oculto
    path('catalogo/categorias',Home.as_view(),name='categorias'),
    path('catalogo/subcategorias',Home.as_view(),name='subcategorias'),
    path('movimientos/compras',Home.as_view(),name='compras'),
]