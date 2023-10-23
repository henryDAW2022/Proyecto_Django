from django.contrib import admin

## mostrar usuarios en portal adminDjango
from .models import Usuario

# Register your models here.
admin.site.register(Usuario)