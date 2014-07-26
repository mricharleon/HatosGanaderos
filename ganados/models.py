# -*- coding: utf-8 -*-
from django.db import models
from profiles.models import Ganaderia

class Identificacion_Simple(models.Model):
    rp = models.PositiveIntegerField('RP')
    nombre = models.CharField('Nombre', max_length='13')
    rp_madre = models.PositiveIntegerField('RP-Madre')
    rp_padre = models.PositiveIntegerField('RP-Padre')

    def __unicode__(self):
        return self.nombre

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


class Ganado(models.Model):
    imagen = models.ImageField(upload_to='imagenGanado')
    ganaderia = models.ForeignKey(Ganaderia, related_name='ganados')
    nacimiento = models.DateField()
    GENDER_CHOICES = (
        (0, 'Macho'),
        (1, 'Hembra')
    )
    genero = models.PositiveSmallIntegerField('Genero',
                                              choices=GENDER_CHOICES
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
        (11,'Chianina')
    )
    raza = models.PositiveSmallIntegerField('Raza',
                                              choices=RAZAS_CHOICES
                                              )

    CONCEPCION_CHOICES = (
        (0, 'Inseminacion'),
        (1, 'Monta')
    )
    forma_concepcion = models.PositiveSmallIntegerField('Forma de Concepcion',
                                              choices=CONCEPCION_CHOICES
                                              )

    observaciones = models.TextField(max_length=125)
    
    edad_anios = models.IntegerField()
    edad_meses = models.IntegerField()
    edad_dias = models.IntegerField()
    #gestacion = models.ForeignKey(Gestacion, blank=True, null=True, related_name='gestaciones')
    #ciclo = models.ForeignKey(Ciclo, blank=True, null=True, related_name='ciclos')
    identificacion_simple = models.ForeignKey(Identificacion_Simple, blank=True, null=True, related_name='identificaciones_simples')
    identificacion_ecuador = models.ForeignKey(Identificacion_Ecuador, blank=True, null=True, related_name='identificaciones_ecuador')
    #etapa = models.ForeignKey(Etapa, null=True, related_name='etapas')
    #verificacion = models.ForeignKey(Verificacion, blank=True, null=True, related_name='verificaciones')
    #celo = models.ForeignKey(Celo, blank=True, null=True, related_name='celos')
    #ordenio = models.ForeignKey(Ordenio, blank=True, null=True, related_name='ordenios')

    def __unicode__(self):
        if self.identificacion_simple:
            ctx = self.identificacion_simple.rp
        else:
            ctx = self.identificacion_ecuador.rp
        return ctx

class Verificacion(models.Model):
    intento = models.IntegerField()
    fecha_inicio = models.DateField('Fecha de inicio')
    fecha_fin = models.DateField('Fecha final')
    ESTADO_CHOICES = (
        (0, 'Correcto'),
        (1, 'Incorrecto')
    )
    estado = models.PositiveSmallIntegerField('Estado',
                                            choices=ESTADO_CHOICES,
                                            blank=True,
                                            null=True)
    observaciones = models.TextField('Observaciones', max_length=150, blank=True, null=True)
    ganado = models.ForeignKey(Ganado, null=True, related_name='verificaciones')
    is_active = models.BooleanField()
    def __unicode__(self):
        return self.estado

class Ordenio(models.Model):
    fecha = models.DateField(u'Fecha de Ordeño')
    numero_ordenio = models.IntegerField(u'Número de Ordeños')
    cantidad = models.IntegerField('Cantidad de litros de leche')
    total = models.IntegerField('Total de leche')
    observaciones = models.TextField('Observaciones', max_length=150, blank=True, null=True)
    ganado = models.ForeignKey(Ganado, null=True, related_name='ordenios')
    
    def __unicode__(self):
        return self.fecha


class Celo(models.Model):
    fecha_inicio = models.DateTimeField('Fecha de inicio')
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
        (0, u'Período seco'),
        (1, u'Período lactancia'),
        (2, u'Período Vacío')
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
        (1, 'Fallecimiento'),
        (2, 'Perdida'))
    tipo_problema = models.PositiveSmallIntegerField('Tipo de problema',
                                                    choices=TIPO_PROBLEMA_CHOICES)
    observaciones = models.TextField('Observaciones', max_length=150)
    def __unicode__(self):
        return self.fecha_problema

class Gestacion(models.Model):
    fecha_servicio = models.DateField('Fecha de servicio')
    fecha_parto = models.DateField('Fecha de parto')
    TIPO_PARTO_CHOICES = (
        (0, 'Monta'),
        (1, u'Inseminación')
        )
    tipo_parto = models.PositiveSmallIntegerField('Tipo de parto',
                                                    choices=TIPO_PARTO_CHOICES
                                                    )
    observaciones = models.TextField('Observaciones', max_length=150)
    problema = models.OneToOneField(ProblemaGestacion)
    ganado = models.ForeignKey(Ganado, null=True, related_name='gestaciones')
    is_active = models.BooleanField()
    def __unicode__(self):
        return self.fecha_servicio


class Etapa(models.Model):
    fecha_inicio = models.DateField('Fecha de inicio')
    NOMBRE_CHOICES = (
        (0, 'Ternera'),
        (1, 'Vacona'),
        (2, 'Vientre')
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
