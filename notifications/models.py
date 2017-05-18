# -*- encoding: utf-8 -*-
from django.db import models
from ganados.models import Ganado, Insemination
from medicament.models import Medicament
from alimentos.models import Food
from profiles.models import Ganaderia


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
        #reproduccion
		(0, 'Ganado en celo'), #ya
        (1, 'Registro del servicio'), #ya
        (2, u'Verificación del celo'), #ya
        (3, 'Fecha de posible parto'), #ya
        (4, 'Cantidad reducida de pajuelas'), #ya
        #produccion
        (5, u'Registro de ordeño'), #ya
        #sanidad
        (6, 'Cantidad reducida de la vacuna'), #ya
        (7, 'Cantidad reducida del desparasitador'), #ya
        (8, u'Fecha próxima de vencimiento de la vacuna'), #ya
        (9, u'Fecha próxima de vencimiento del desparasitador'), #ya
        (10, u'Fecha próxima de aplicación de la vacuna'), #ya
        (11, u'Fecha próxima de aplicación del desparasitador'), #ya
        #alimentacion
        (12, 'Cantidad reducida del alimento'), #ya
        (13, u'Fecha próxima de vencimiento del alimento'), #ya
        (14, u'Fecha próxima de aplicación del alimento'), #ya
        #reproduccion
        (15, 'Cambio de etapa a Vacona Media'), #ya
        (16, 'Cambio de etapa a Vacona Fierro'), #ya
        (17, 'Cambio de etapa a Vacona Vientre'), #ya
        (18, 'Cambio de etapa a Vaca'), #ya
        (19, 'Cambio de edad'), #ya
        (20, 'Cambio a ciclo seco'), #ya
        )

    ident_cattle = models.ForeignKey(Ganado, related_name='notification_cattle', blank=True, null=True)
    ident_sperm = models.ForeignKey(Insemination, related_name='notification_insemination', blank=True, null=True)
    ident_medicament = models.ForeignKey(Medicament, related_name='notification_medicament', blank=True, null=True)
    ident_food = models.ForeignKey(Food, related_name='notification_food', blank=True, null=True)
    name = models.PositiveSmallIntegerField('Nombre', choices=NAME_CHOICES)
    farm = models.ForeignKey(Ganaderia, related_name='notification_farm')

