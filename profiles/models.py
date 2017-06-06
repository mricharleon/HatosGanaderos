# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from userena.models import UserenaLanguageBaseProfile
from userena.utils import user_model_label
from django.contrib.auth.models import User

import datetime


class Configuracion(models.Model):
    IDENTIFICACION_CHOICES = (
            ('simple', 'Simple'),
            ('norma_ecuador', 'Norma Ecuador')
            )
    tipo_identificacion = models.CharField("Tipo de identificacion",
            max_length=15,
            choices = IDENTIFICACION_CHOICES,
            default=0
            )
    celo_frecuencia = models.IntegerField("Frecuencia de celo",
            max_length=2
            )
    celo_frecuencia_error = models.IntegerField("Error frecuencia en celo",
            max_length=2
            )
    celo_duracion = models.IntegerField("Duración de celo",
            max_length=2
            )
    celo_duracion_error = models.IntegerField("Error (+/-)",
            max_length=2
            )
    celo_despues_parto = models.IntegerField(u"Celo despues de parto",
            max_length=2
            )
    celo_despues_parto_error = models.IntegerField("Error (+/-)",
            max_length=2
            )
    intentos_verificacion_celo = models.IntegerField(
            "Intentos de Verificación Celo",
            max_length=1
            )
    etapa_ternera = models.IntegerField("Edad máxima de una ternera",
            max_length=2
            )
    etapa_vacona_media = models.IntegerField("Edad máxima de una vacona media",
            max_length=2
            )
    etapa_vacona_fierro = models.IntegerField(
            "Edad máxima de una vacona fierro",
            max_length=2
            )
    etapa_vacona_vientre = models.IntegerField(
            "Edad máxima de una vacona vientre",
            max_length=2
            )
    etapa_vaca = models.IntegerField("Edad máxima de una vaca",
            max_length=2
            )
    periodo_gestacion = models.IntegerField("Dias de periodo de gestacion",
            max_length=3
            )
    periodo_seco = models.IntegerField("Dias de periodo seco",
            max_length=3
            )
    periodo_lactancia = models.IntegerField("Dias de periodo de lactancia",
            max_length=3
            )
    periodo_vacio = models.IntegerField("Dias de periodo vacio",
            max_length=3
            )
    numero_ordenios = models.IntegerField("Numero de ordeños",
            max_length=1
            )
    initial_rp = models.IntegerField("Número RP inicial",
            max_length=6)

    def __unicode__(self):
        return 'Configuración'


class Profile(UserenaLanguageBaseProfile):
    """ Default profile """
    GENDER_CHOICES = (
            (1, _('Male')),
            (2, _('Female')),
            )

    user = models.OneToOneField(user_model_label,
            unique=True,
            verbose_name=_('user'),
            related_name='profile_user')
    gender = models.PositiveSmallIntegerField(_('gender'),
            choices=GENDER_CHOICES,
            blank=True,
            null=True)

    direccion = models.CharField(_('Direccion'), blank=True, max_length=50)
    telefono = models.CharField(_('Telefono'), blank=True, max_length=10)
    # location =  models.CharField(_('location'), max_length=255, blank=True)
    # birth_date = models.DateField(_('birth date'), blank=True, null=True)
    # about_me = models.TextField(_('about me'), blank=True)

    def __unicode__(self):
        return self.user


class Ganaderia(models.Model):
    nombreEntidad = models.CharField(_(u'Nombre de Ganadería'), max_length=75)
    direccion = models.CharField(_(u'Direccion de Ganadería'), max_length=50)
    perfil = models.ManyToManyField(Profile,
            verbose_name=_('perfil'),
            related_name='ganaderia_perfil'
            )
    configuracion = models.OneToOneField(Configuracion,
            verbose_name=_('configuracion'),
            related_name='ganaderia'
            )

    def __unicode__(self):
        return self.nombreEntidad


'''
    @property
    def age(self, User):
        if not User.date_joined: return False
        else:
            today = datetime.date.today()
            # Raised when birth date is February 29 and the current year is not
            # a leap year.
            try:
                birthday = User.date_joined.replace(year=today.year)
            except ValueError:
                day = today.day - 1 if today.day != 1 else today.day + 2
                birthday = User.date_joined.replace(year=today.year, day=day)
            if birthday > today: return today.year - User.date_joined.year - 1
            else: return today.year - User.date_joined.year
'''
