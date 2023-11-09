from django.db import models

# importo el modelo abastracto que creamos en bases
from bases.models import ClaseModelo

class Categoria(ClaseModelo): ## no hace falta que herede de clase models de django, porque claseModelo ya hereda de esa clase.
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripción de la Categoría',
        unique=True
    )

    def __str__(self): ## Sobreescribimos este metodo, para que django muestre la descripcion en lugar de lo que django determine automaticamente.
        return '{}'.format(self.descripcion)

    def save(self):  ## sobreescribimos el metodo save(), para que guarde en mayusculas la descripcion.
        self.descripcion = self.descripcion.upper()
        super(Categoria, self).save()

    class Meta:  ## Aqui sobreescribimos la forma en que Django muestre el plural del modelo.
        verbose_name_plural= "Categorias"