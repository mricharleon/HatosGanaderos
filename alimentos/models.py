# -*- coding: utf-8 -*-
from django.db import models
from profiles.models import Ganaderia
from ganados.models import Ganado

class Alimento(models.Model):
    nombre = models.CharField('Nombre del alimento', max_length=100)
    caduca = models.DateField(u'Fecha de Expiración')
    ETAPA_CHOICES = (
        (0, 'Ternera'),
        (1, 'Vacona'),
        (2, 'Vaca')
        )
    etapa = models.PositiveSmallIntegerField('Etapa', 
                                            choices=ETAPA_CHOICES)
    cantidad = models.IntegerField()
    ganaderia = models.ForeignKey(Ganaderia, related_name='alimentos')
    ganado = models.ForeignKey(Ganado, blank=True, null=True, related_name='alimentos_ganado')
    