#-*- coding: utf-8 -*-
from django.db import models
from profiles.models import Ganaderia
from django.core import serializers

class Identificacion_Simple(models.Model):
    rp = models.PositiveIntegerField('RP')
    nombre = models.CharField('Agregue un nombre', max_length='13')
    rp_madre = models.PositiveIntegerField('RP de la Madre')
    rp_padre = models.PositiveIntegerField('RP del Padre')

    class Meta:
        ordering = ['rp']


class Identificacion_Ecuador(models.Model):
    siglas_pais = models.CharField('Siglas del pais',
                                    max_length='7'
                                    )
    codigo_pais = models.CharField('Codigo de pais',
                                    max_length='7'
                                    )
    codigo_provincia = models.CharField('Codigo de provincia',
                                    max_length='7'
                                    )
    numero_serie = models.CharField('Numero de serie',
                                    max_length='8'
                                    )
    codigo_barras = models.CharField('Codigo de barras',
                                    max_length='20'
                                    )
    rp = models.PositiveIntegerField('RP')
    nombre = models.CharField('Nombre',
                                max_length='13'
                                )
    rp_madre = models.PositiveIntegerField('RP-Madre')
    rp_padre = models.PositiveIntegerField('RP-Padre')

    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ['rp']


class DownCattle(models.Model):
    date = models.DateField('Fecha de Baja')
    CAUSE_DOWN_CHOICES = (
        (0, 'Muerte'),
        (1, 'Venta'),
        (2, u'Desaparición'),
        (2, u'Ingreso erróneo'))
    cause_down = models.PositiveSmallIntegerField('Causa de la Baja',
                                        choices=CAUSE_DOWN_CHOICES,
                                        )
    observations = models.TextField('Observaciones')
    
    def __unicode__(self):
        return self.date + " - " + self.cause_down

class Ganado(models.Model):
    imagen = models.ImageField('Agregue una imagen', upload_to='imagenGanado')
    ganaderia = models.ForeignKey(Ganaderia, related_name='ganados')
    nacimiento = models.DateField('Agregue el nacimiento')
    GENDER_CHOICES = (
        (0, 'Macho'),
        (1, 'Hembra'),
        (2, 'Sin Definir')
    )
    genero = models.PositiveSmallIntegerField('¿Cuál es el sexo?',
                                              choices=GENDER_CHOICES,
                                              default=0
                                              )
    RAZAS_CHOICES = (
        (0, 'Angus'),
        (1, 'Ankole'),
        (2, 'Asturiana de los Valles'),
        (3, 'Avilenia'),
        (4, 'Blonde D Aquitaine'),
        (5, 'Braford'),
        (6, 'Brahman'),
        (7, 'Braunvieh'),
        (8, 'Brava'),
        (9,'Cachena'),
        (10,'Charolais'),
        (11,'Chianina'),
        (12, 'Sin Definir')
    )
    raza = models.PositiveSmallIntegerField('¿Cuál es la Raza?',
                                              choices=RAZAS_CHOICES,
                                              default=0
                                              )

    CONCEPCION_CHOICES = (
        (0, u'Inseminación'),
        (1, 'Monta')
    )
    forma_concepcion = models.PositiveSmallIntegerField('¿Cómo se concibio?',
                                              choices=CONCEPCION_CHOICES,
                                              default=0
                                              )
    live_weight = models.FloatField('¿Cuál es el peso vivo?', blank=True, null=True)
    UNIT_LIVE_WEIGHT_CHOICES = (
        (0, 'Kg'),
        (1, 'lbs'),
        (2, 'Arrobas')
        )
    unit_live_weight = models.PositiveSmallIntegerField('Unidad de peso vivo',
                            choices=UNIT_LIVE_WEIGHT_CHOICES,
                            blank=True,
                            null=True,
                            default=0)
    observaciones = models.TextField(max_length=125)    
    edad_anios = models.IntegerField()
    edad_meses = models.IntegerField()
    edad_dias = models.IntegerField()
    identificacion_simple = models.ForeignKey(Identificacion_Simple, blank=True, null=True, related_name='identificaciones_simples')
    identificacion_ecuador = models.ForeignKey(Identificacion_Ecuador, blank=True, null=True, related_name='identificaciones_ecuador')
    down_cattle = models.OneToOneField(DownCattle, related_name='cattle_down_cattle', blank=True, null=True)

    def __unicode__(self):
        if self.identificacion_simple:
            ctx = self.identificacion_simple.rp
        else:
            ctx = self.identificacion_ecuador.rp
        return ctx


class Verification(models.Model):
    initial_date = models.DateField('Fecha inicial')
    is_active = models.BooleanField()
    cattle = models.ForeignKey(Ganado, related_name='verification_cattle')

class Attempt(models.Model):
    attempt = models.IntegerField('Intento')
    attempt_date = models.DateField('Fecha del intento')
    STATE_CHOICES = (
        (0, 'Correcto'),
        (1, 'Incorrecto')
    )
    state = models.PositiveSmallIntegerField('Estado', 
                        choices=STATE_CHOICES,
                        blank=True,
                        null=True)
    observations = models.TextField('Observaciones', blank=True, null=True)
    TYPE_CONCEPTION_CHOICES = (
        (0, u'Inseminación'),
        (1, 'Monta')
    )
    type_conception = models.PositiveSmallIntegerField(u'Tipo de concepción',
                        choices=TYPE_CONCEPTION_CHOICES,
                        default=0)
    rp_father = models.PositiveIntegerField('RP del Padre', null=True, blank=True)
    verification = models.ForeignKey(Verification, null=True, related_name='attempt_verification')


class Ordenio(models.Model):
    fecha = models.DateField(u'Fecha de Ordeño')
    numero_ordenio = models.IntegerField(u'Número de Ordeños')
    cantidad = models.IntegerField('¿Cantidad de leche hoy?')
    total = models.IntegerField('Total de leche')
    observaciones = models.TextField('Observaciones', max_length=150, blank=True, null=True)
    ganado = models.ForeignKey(Ganado, null=True, related_name='ordenios')
    unique_ordenio = models.BooleanField(u'Guardar único ordeño', blank=True)
    
    def __unicode__(self):
        return self.fecha


class Celo(models.Model):
    fecha_inicio = models.DateTimeField('¿Cuándo inicio el celo?')
    fecha_fin = models.DateTimeField('Fecha final')
    ESTADO_CHOICES = (
        (0, 'En celo'),
        (1, 'Sin celo')
        )
    estado = models.PositiveSmallIntegerField('Estado',
                                            choices=ESTADO_CHOICES
                                            )
    observaciones = models.TextField('Observaciones', max_length=150, blank=True, null=True)
    ganado = models.ForeignKey(Ganado, null=True, related_name='celos')
    is_active = models.BooleanField()

    def __unicode__(self):
        return self.fecha_inicio


class Ciclo(models.Model):
    fecha_inicio = models.DateField('Fecha de inicio')
    NOMBRE_CHOICES = (
        (0, u'Período Vacío'),
        (1, u'Período seco'),
        (2, u'Período lactancia'),
        (3, u'Período gestación')

    )
    nombre = models.PositiveSmallIntegerField(u'Período',
                                            choices=NOMBRE_CHOICES
                                            )
    fecha_fin = models.DateField('Fecha final')
    ganado = models.ForeignKey(Ganado, null=True, related_name='ciclos')
    is_active = models.BooleanField()
    def __unicode__(self):
        return self.nombre

class ProblemaGestacion(models.Model):
    fecha_problema = models.DateField()
    TIPO_PROBLEMA_CHOICES = (
        (0, 'Aborto'),
        (1, 'Nacido muerto'),
        (2, 'Madre muerta'),
        (3, 'Los dos muertos'))
    tipo_problema = models.PositiveSmallIntegerField('Tipo de problema',
                                                    choices=TIPO_PROBLEMA_CHOICES)
    observaciones = models.TextField('Observaciones', max_length=150)
    def __unicode__(self):
        return self.fecha_problema

class Gestacion(models.Model):
    fecha_servicio = models.DateField('Fecha de servicio')
    fecha_parto = models.DateField('Fecha del posible parto')
    TIPO_PARTO_CHOICES = (
        (0, 'Natural'),
        (1, u'Cesárea')
        )
    tipo_parto = models.PositiveSmallIntegerField('Tipo de parto',
                                                    choices=TIPO_PARTO_CHOICES,
                                                    blank=True,
                                                    null=True
                                                    )
    observaciones = models.TextField('Observaciones', max_length=150, blank=True, null=True)
    problema = models.OneToOneField(ProblemaGestacion, blank=True, null=True)
    ganado = models.ForeignKey(Ganado, null=True, related_name='gestaciones')
    is_active = models.BooleanField()
    def __unicode__(self):
        return self.fecha_servicio

class DeferEtapa(models.Model):
    number_days = models.PositiveIntegerField('Días de postergación')
    observations = models.TextField('Observaciones', max_length=250)
    is_active = models.BooleanField()
    cattle_id = models.ForeignKey(Ganado, related_name='cattle_id_ganado', blank=True, null=True)

class Etapa(models.Model):
    fecha_inicio = models.DateField('Fecha de inicio')
    NOMBRE_CHOICES = (
        (0, 'Ternera'),
        (1, 'Vacona media'),
        (2, 'Vacona fierro'),
        (3, 'Vacona vientre'),
        (4, 'Vaca'),
        )
    nombre = models.PositiveSmallIntegerField('Etapa',
                                            choices=NOMBRE_CHOICES
                                            )
    observaciones = models.TextField('Observaciones', max_length=150)
    ganado = models.ForeignKey(Ganado, null=True, related_name='etapas')
    is_active = models.BooleanField()

    def __str__(self):
        ctx = str(self.nombre) + ' - ' + str(self.fecha_inicio)
        return ctx

class DownInsemination(models.Model):
    date = models.DateField('Fecha de Baja')
    CAUSE_DOWN_CHOICES = (
        (0, 'Agotamiento'),
        (1, u'Muestra no adecuada')
        )
    cause_down = models.PositiveSmallIntegerField('Causa de la Baja',
                                        choices=CAUSE_DOWN_CHOICES,
                                        )
    observations = models.TextField('Observaciones')
    
    def __unicode__(self):
        return self.date + " - " + self.cause_down

class Insemination(models.Model):
    down_insemination = models.OneToOneField(DownInsemination, related_name='insemination_down', blank=True, null=True)
    farm = models.ForeignKey(Ganaderia, related_name='insemination_farm')
    rp = models.IntegerField('RP')
    name = models.TextField('Nombre', max_length=50)
    registration_date = models.DateField('Fecha de registro')
    amount_pajuelas = models.IntegerField('Número de pajuelas')
    BREED_CHOICES = (
        (0, 'Angus'),
        (1, 'Ankole'),
        (2, 'Asturiana de los Valles'),
        (3, 'Avilenia'),
        (4, 'Blonde D Aquitaine'),
        (5, 'Braford'),
        (6, 'Brahman'),
        (7, 'Braunvieh'),
        (8, 'Brava'),
        (9,'Cachena'),
        (10,'Charolais'),
        (11,'Chianina'),
        (12, 'Sin Definir')
    )
    breed = models.PositiveSmallIntegerField('Raza',
                        choices=BREED_CHOICES)
    observations = models.TextField('Observaciones')


