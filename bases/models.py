from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

## Importamos el manager
from .manager import UsuarioManager

# Create your models here.
## Extencion del modelo User de DJANGO, para autenticacion de usuarios.
## **Tenemos que crear un manager segun la documentacion de django, por la cual se administran las querys a la bd**.

class Usuario(AbstractBaseUser,PermissionsMixin): ## Estoy creando usuario que extiende de AbstractUser, y Permission asi que no necesitamos declarar campo password. porque existe ya.
    email = models.EmailField(_('direccion email'), max_length=254, unique=True)
    first_name = models.CharField(_('nombre'), max_length=30, blank=True)
    last_name = models.CharField(_('apellidos'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('es staff'), default=False, help_text=_('Indica si el usuario puede iniciar sesion en Admin '))
    is_active = models.BooleanField(_('activo'), default=True, help_text=_('Indica si este ususario debe ser tratado como activo ' ' Deselecciona en lugar de eliminar cuentas.'))
    date_joined = models.DateTimeField(_('fecha registro'), default=timezone.now)

    USERNAME_FIELD = 'email'  ##Especificamos que el nombre de usuario sea email, en la autenticacion.
    REQUIRED_FIELDS = []

    ## El manager que trae cualquier modelo es object, asi que sobreescribiremos con nuestro manager.
    objects = UsuarioManager()

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')

        
    ## Sobreescribimos los metodos que ya existen

    def get_absolute_url(self):
        return "/users/%s" % urlquote(self.email)

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.stript()
    
    def get_short_name(self):
        return self.first_name

    