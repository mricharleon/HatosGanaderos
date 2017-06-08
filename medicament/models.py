# -*- encoding: utf-8 -*-
from django.db import models
from profiles.models import Ganaderia
from ganados.models import Ganado

class Medicament(models.Model):
    name = models.CharField('Nombre de la medicina', max_length=100)
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
    amount = models.FloatField('Cantidad de medicina')
    SEX_CHOICES = (
        (0, 'Hembra'),
        (1, 'Macho'),
        (2, 'Hembra y Macho')
        )
    sex = models.PositiveSmallIntegerField('Sexo a aplicar',
                                            choices=SEX_CHOICES,
                                            default=0)
    farm = models.ForeignKey(Ganaderia, related_name='medicaments')
    application_age = models.IntegerField(u'Edad de Aplicación')
    TIME_APPLICATION_AGE_CHOICES = (
        (0, u'Aplicación en días'),
        (1, 'Aplicación en meses'),
        (2, u'Aplicación en años')
        )
    time_application_age = models.PositiveSmallIntegerField('Unidad de tiempo',
                            choices=TIME_APPLICATION_AGE_CHOICES,
                            default=0)
    amount_application = models.FloatField(u'cantidad de aplicación')
    OPTION_NUMBER_APPLICATION = (
        (0, 'Veces exactas'),
        (1, 'Repetitivo')
        )
    option_number_application = models.PositiveSmallIntegerField('Ciclo de la medicina',
                            choices = OPTION_NUMBER_APPLICATION
                            )
    number_application = models.IntegerField(u'Número de aplicaciones')
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
        (0, 'Intravenosa'),
        (1, 'Intramuscular'),
        (2, u'Subcutánea'),
        (3, 'Intraperitoneal'),
        (4, 'Oral'),
        (5, 'Rectal'),
        (6, 'Intrauterina'),
        (7, 'Intramamaria'),
        (8, u'Tópica')
        )
    administration_route = models.PositiveSmallIntegerField(u'Vía de administración',
                            choices=ADMINISTRATION_ROUTE_CHOICES,
                            default=0)
    observations = models.TextField('Observaciones')
    is_vaccine = models.BooleanField()
    is_wormer = models.BooleanField()
    is_active = models.BooleanField('Activo')

class ApplicationMedicament(models.Model):
    date = models.DateField('Fecha de aplicación')
    cattle = models.ManyToManyField(Ganado, blank=True, null=True, related_name='application_medicament_medicament', verbose_name=u'Ganados')
    medicament = models.ForeignKey(Medicament, related_name='application_medicament_cattle')
    STATUS_CHOICES = (
        (0, 'Realizado'),
        (1, 'Cancelado')
        )
    status = models.PositiveSmallIntegerField('Estado',
                            choices=STATUS_CHOICES,
                            )
