from django.utils import timezone
from django.contrib.auth.models import BaseUserManager


class UsuarioManager(BaseUserManager):

    ## declaramos esta funcion para definir el super usuario o admin, y los usuarios comunes.
    ## almacenaremos la fecha de creacion de usuario
    ## verificaremos si el usuario esta registrado o no.

    def _create_user(self, email, password,is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('Debes introducir un email válido')

        email = self.normalize_email(email) ## normalizamos el email a lowerCase
        user = self.model(email=email, is_staff=is_staff, is_active = True, is_superuser=is_superuser, last_login=now, **extra_fields)      ## aqui crearemos al usuario

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields): ## Aqui estamos sobreescribiendo
        return self._create_user(email,password,False,False,**extra_fields) ## Se creara siempre usuarios sin permisos superusers

    def create_superuser(self, email, password, **extra_fields): ##para superuser si requerimos password
        return self._create_user(email,password,True,True,**extra_fields)