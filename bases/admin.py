from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

## mostrar usuarios en portal adminDjango
from .models import Usuario
from .forms import UserChangeForm, UserCreationForm,UsuarioChangeForm,UsuarioCreationForm


## Agregamor y cambiar instancias de usuario
class UsuarioAdmin(UserAdmin):
    ## definimos el conjunto de campos que utilizaremos
    fieldsets = (
        (None, {'fields':('email','password')}),
        (_('Personal info'),{'fields':('first_name', 'last_name')}),
        (_('Permissions'),{'fields':('is_active','is_staff','is_superuser','groups','user_permissions')}),
        (_('Important dates'),{'fields':('last_login','date_joined')}),
    )

    ## Cuando se agrega un usuario, para confirmar la contraseña de registro
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields': ('email','password1','password2')
        }),
    )

    form = UsuarioChangeForm
    add_form = UsuarioCreationForm
    list_display = ('email','first_name','last_name','is_staff') ## Campos que se van a mostrar
    search_fields = ('email','first_name','last_name') ## campos de busqueda
    ordering = ('email',) ## lista ordenada por el campo email


## Agregamos usuario y usuario admin
admin.site.register(Usuario,UsuarioAdmin)