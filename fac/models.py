from django.db import models


# importo el modelo abstracto que creamos en bases
from bases.models import ClaseModelo



class Cliente(ClaseModelo):
    AUT='Autónomo'
    EMP='Empresa'
    TIPO_CLIENTE = [
        (AUT,'Autónomo'),
        (EMP,'Empresa')
    ]
    nombres = models.CharField(
        max_length=100
    )
    apellidos = models.CharField(
        max_length=100
    )
    telefono = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    tipo=models.CharField(
        max_length=10,
        choices=TIPO_CLIENTE,
        default=AUT
    )

    def __str__(self):
        return '{} {}'.format(self.apellidos,self.nombres)  ## Para mostrarlo

    def save(self):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        super(Cliente, self).save()

    class Meta:
        verbose_name_plural = "Clientes"