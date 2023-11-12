from django.db import models

# importo el modelo abstracto que creamos en bases
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

## Creacion Modelo Subcategoria
class SubCategoria(ClaseModelo):
    ## como tiene relacion con categoria, añado primero el fk. categoria
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripción de la Categoría'
    )

    ## Mostramos la categoria y la subcategoria
    def __str__(self):
        return '{}:{}'.format(self.categoria.descripcion,self.descripcion)
    
    ## Sobreescribo el metodo save(), para que se guarde en mayusculas.
    def save(self):
        self.descripcion = self.descripcion.upper()
        super(SubCategoria, self).save()

    ## Hacemos el plural del modelo, y que no se repitan si existe la subcategoria.
    class Meta:
        verbose_name_plural= "Sub Categorias"
        unique_together = ('categoria','descripcion')