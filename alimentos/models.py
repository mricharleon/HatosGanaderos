# -*- encoding: utf-8 -*-
from django.db import models
from profiles.models import Ganaderia
from ganados.models import Ganado

class Food(models.Model):
    name = models.CharField('Nombre del alimento', max_length=100)
    expiration_date = models.DateField(u'Fecha de Expiración')
    UNIT_CHOICES = (
        (0, 'ml'),
        (1, 'gr'),
        (2, 'lbs'),
        (3, 'Kg'),
        (4, 'Paquetes'),
        )
    unit = models.PositiveSmallIntegerField('Unidad',
                                            choices=UNIT_CHOICES,
                                            default=0)
    amount = models.FloatField('Cantidad de alimento')
    SEX_CHOICES = (
        (0, 'Hembra'),
        (1, 'Macho'),  
        (2, 'Hembra y Macho')      
        )
    sex = models.PositiveSmallIntegerField('Sexo a aplicar', 
                                            choices=SEX_CHOICES,
                                            default=0)
    farm = models.ForeignKey(Ganaderia, related_name='farm_foods')
    PHASE_CHOICES = (
        (0, 'Terneras(os)'),
        (1, 'Adultos'),
        (2, 'Todas')
        )
    phase = models.PositiveSmallIntegerField('Etapa', 
                                            choices=PHASE_CHOICES,
                                            default=0)
    consumer_amount = models.FloatField(u'cantidad de consumo')
    interval = models.IntegerField('Intervalo de tiempo')
    TIME_INTERVAL_CHOICES = (
        (0, u'Intervalo en días'),
        (1, 'Intervalo en meses'),  
        (2, u'Intervalo en años')      
        )
    time_interval = models.PositiveSmallIntegerField('Unidad de tiempo',
                            choices=TIME_INTERVAL_CHOICES,
                            default=0)
    ADMINISTRATION_ROUTE_CHOICES = (
        (0, 'Oral'),
        (1, 'Granulada')
        )
    administration_route = models.PositiveSmallIntegerField(u'Vía de administración',
                            choices=ADMINISTRATION_ROUTE_CHOICES,
                            default=0)
    observations = models.TextField('Observaciones')
    is_active = models.BooleanField('Activo')

class ApplicationFood(models.Model):
    date = models.DateField('Fecha de aplicación')
    cattle = models.ManyToManyField(Ganado, blank=True, null=True, related_name='application_food_food', verbose_name=u'Ganados')
    food = models.ForeignKey(Food, related_name='application_food_cattle')
    STATUS_CHOICES = (
        (0, 'Realizado'),
        (1, 'Cancelado')
        )
    status = models.PositiveSmallIntegerField('Estado',
                            choices=STATUS_CHOICES,
                            )