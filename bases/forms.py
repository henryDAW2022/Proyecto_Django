from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.forms import fields

from .models import Usuario


## Formulario para crear un usuario sin que tenga privilegios y solamente dando email y password
class UsuarioCreationForm(UserCreationForm):
    def __init__(self, *args,**kwargs):
        super(UsuarioCreationForm,self).__init__(*args, **kwargs)

    class Meta:
        model = Usuario
        fields = ("email",)

## Formulario para editar el usuario
class UsuarioChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UsuarioChangeForm,self).__init__(*args, **kwargs)

    class Meta:
        model: Usuario
        fields = '__all__'