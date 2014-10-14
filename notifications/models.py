# -*- encoding: utf-8 -*-
from django.db import models
from ganados.models import Ganado
from medicament.models import Medicament
from alimentos.models import Food


class Notification(models.Model):
    start_date = models.DateField('Fecha inicial')
    end_date = models.DateField('Fecha final')
    STATE_CHOICES = (
        (0, 'No realizado'),
        (1, 'Realizado'),
        (2, 'Pendiente'),
        )
    state = models.PositiveSmallIntegerField('Estado',
                                            choices=STATE_CHOICES
                                            )
    MODULE_CHOICES = (
        (0, u'Reproducción'),
        (1, u'Alimentación'),
        (2, 'Sanidad'),
        (3, u'Producción'),
        )
    module = models.PositiveSmallIntegerField(u'Módulo',
    										choices=MODULE_CHOICES
    										)
    NAME_CHOICES = (
		(0, 'Ganado en celo'),
        (1, 'Registro del servicio'),
        (2, u'Verificación del celo'),
        (3, 'Fecha de posible parto'),
        (4, 'Cantidad reducida de pajuelas'),
        (5, u'Registro de ordeño'),
        (6, 'Cantidad reducida de la vacuna'),
        (7, 'Cantidad reducida del desparacitador'),
        (8, u'Fecha próxima de vencimiento de la vacuna'),
        (9, u'Fecha próxima de vencimiento del desparacitador'),
        (10, u'Fecha próxima de aplicación de la vacuna'),
        (11, u'Fecha próxima de aplicación del desparacitador'),
        (12, 'Cantidad reducida del alimento'),
        (13, u'Fecha próxima de vencimiento del alimento'),
        (14, u'Fecha próxima de aplicación del alimento')
        )

    ident_cattle = models.ForeignKey(Ganado, related_name='notification_cattle', blank=True, null=True)
    ident_medicament = models.ForeignKey(Medicament, related_name='notification_medicament', blank=True, null=True)
    ident_food = models.ForeignKey(Food, related_name='notification_food', blank=True, null=True)
    name = models.PositiveSmallIntegerField('Nombre', choices=NAME_CHOICES)

