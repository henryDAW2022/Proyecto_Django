from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.forms import fields
from django.db import models
from django import forms
from django.forms.widgets import PasswordInput

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

## definimos nuestro formulario utilizando forms de django, para tratar los usuarios.
class Userform(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput) ## no se vera la constraseña

    class Meta: ## definimos los campos
        model = Usuario
        fields = ['email','first_name', 'last_name', 'password']
        widget = {'email':forms.EmailInput, 'password':forms.PasswordInput}

    def __init__(self, *args, **kwargs):  ## nuestro constructor hereda de la clase forms, por eso utilizamods super()
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })