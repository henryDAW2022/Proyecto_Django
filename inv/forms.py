## Para crear un registro se debe renderizar a traves del modulo forms de django.

from django import forms

from .models import Categoria, SubCategoria  ## importo el modelo sobre el que voy a actuar



class CategoriaForm(forms.ModelForm): ## hacemos la herencia para poder utilizar los metodos definidos de django
    class Meta:
        model = Categoria
        fields = ['descripcion', 'estado'] ## solo seran estos dos campos los que queremos manipular.
        labels = {'descripcion':"Descripción de la Categoría",
               "estado":"Estado"}
        widget={'descripcion': forms.TextInput}  ## asi definimos que tipo de elemento html utilizado.

    ## Como estamos utilizando bootstrap vamos a sobreescribir el metodo init de este formulario.
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs) ## invocamos el init de la clase padre tambien.
        for field in iter(self.fields): ## vamos a ir iterando cada campo, para asignarle el widget, o el atributo que necesitamos modificar, para que bootstrap lo muestre como queremos.
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

class SubCategoriaForm(forms.ModelForm): ## hacemos la herencia para poder utilizar los metodos definidos de django
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(estado=True).order_by('descripcion') ## Con esto mostraremos solo las categorias que esten activas en la seleccion al crear una subcategoria.
    )
    class Meta:
        model = SubCategoria
        fields = ['categoria','descripcion', 'estado'] ## queremos estos campos nada mas
        labels = {'descripcion':"Descripción de la SubCategoría",
               "estado":"Estado"}
        widget={'descripcion': forms.TextInput}  

    ## Como estamos utilizando bootstrap vamos a sobreescribir el metodo init de este formulario.
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs) ## invocamos el init de la clase padre tambien.
        for field in iter(self.fields): ## vamos a ir iterando cada campo, para asignarle el widget, o el atributo que necesitamos modificar, para que bootstrap lo muestre como queremos.
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
                ## vamos a indicar por defecto el combo
        self.fields['categoria'].empty_label = "Selecciona Categoría"