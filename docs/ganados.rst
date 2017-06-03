ganados package
===============

El módulo de ganados es el que se encarga de:
    
    - Registrar ganados
    - Editar el celo de un ganado
    - Registrar el servicio de un ganado
    - Registrar intentos de verificación del servicio
    - Regitrar la gestación
    - Registrar problema de gestación
    - Registrar la baja del ganado
    - Registrar la baja del registro de esperma
    - Listar ganado en producción
    - Registrar el ordeño diario
    - Editar el ordeñi diario
    - Listar todos los ganados
    - Listar los ganados machos
    - Editar el ganado
    - Editar ganado machos
    - Registrar el esperma
    - Editar el registro de esperma
    - Listar registros de esperma

Con la finalidad de obtener mayor cuidado en el ganado en cuanto a alimentación se refiere. Consta de algunos archivos como: admin.py, forms.py, models.py y views.py.


admin.py
--------

El archivo admin.py es el encargado del registro de las clases que están en el modelo paraque funcionen en el admin de Django. En este caso se agregó todos los modelos de la app **ganados** **(*)** ya que son las que deseamos se encuentre en el admin de django.

    .. py:function:: Código de admin.py
        
        | from django.contrib import admin
        | from ganados.models import *
        | admin.site.register(Etapa)
        | admin.site.register(Ganado)
        | admin.site.register(Verification)
        | admin.site.register(Attempt)
        | admin.site.register(Ordenio)
        | admin.site.register(Celo)
        | admin.site.register(Ciclo)
        | admin.site.register(Gestacion)
        | admin.site.register(ProblemaGestacion)
        | admin.site.register(Identificacion_Simple)
        | admin.site.register(Identificacion_Ecuador)


forms.py
--------

Este archivo es el encargado de crear los parámetros correctos que serán utilizados en el formulario del **Ganado e Inseminación** se realizan las debidas importaciones además de la configuración de los parámetros que deben o no ir con sus respectivos atributos como clases, id, etc.

Formulario de inseminación:
    El módulo HatosGanaderos presenta la funcionalidad de registar esperma, para lo cuál se inicia creando en modelo del formulario en este caso se hace uso de la clase **Insemination** con sus respectivos atributos, además se agregan widgets a cada uno de estos atributos que serán utiles para poder realizar un html más vistoso, amigable y funcional.

    .. py:class:: class inseminationForm(forms.ModelForm):

        class Meta:
            
            | model = Insemination
            | exclude = ['down_insemination', 'farm', 'rp']
            | widgets = {
                      'name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
                      'registration_date': forms.DateInput(attrs={'class': 'datetimepicker2', 'placeholder': 'Fecha de registro'}),
                      'amount_pajuelas': forms.TextInput(attrs={'placeholder': 'Número de pajuelas'}),
                      'observations': forms.Textarea(attrs={'placeholder': 'Observaciones'})
            }


Formulario de identificación tipo simple:
    El módulo HatosGanaderos presenta la funcionalidad de registar ganados de dos maneras una de ellas es la denominada **simple**, para lo cuál se inicia creando en modelo del formulario en este caso se hace uso de la clase **tipoSimpleForm** con sus respectivos atributos, además se agregan widgets a cada uno de estos atributos que serán utiles para poder realizar un html más vistoso, amigable y funcional.

    .. py:class:: class tipoSimpleForm(forms.ModelForm):
        
        class Meta:
            
            | model = Identificacion_Simple
            | exclude = ['rp',]
            | widgets = {
                      'nombre':forms.TextInput(attrs={'placeholder': 'Nombre'}),
                      'rp_madre':forms.TextInput(attrs={
                                      'placeholder': 'RP de la madre',
                                      'data-reveal-id': 'myModal'}),
                      'rp_padre':forms.TextInput(attrs={
                                      'placeholder': 'RP del padre',
                                      'data-reveal-id': 'myModal2'}),
            }


Formulario de identificación tipo norma Ecuador:
    El módulo HatosGanaderos presenta la funcionalidad de registar ganados de dos maneras una de ellas es la denominada **normaEcuador**, para lo cuál se inicia creando en modelo del formulario en este caso se hace uso de la clase **tipoNormaEcuadorForm** con sus respectivos atributos, además se agregan widgets a cada uno de estos atributos que serán utiles para poder realizar un html más vistoso, amigable y funcional.

    .. py:class:: class tipoNormaEcuadorForm(forms.ModelForm):

        class Meta:

            | model = Identificacion_Ecuador
            | exclude = ['rp',]
            | widgets = {
                       'siglas_pais': forms.TextInput(attrs={'placeholder': 'Siglas del País'}),
                       'codigo_pais': forms.TextInput(attrs={'placeholder': 'Código del País'}),
                       'codigo_provincia': forms.TextInput(attrs={'placeholder': 'Código de Provincia'}),
                       'numero_serie': forms.TextInput(attrs={'placeholder': 'Número de Serie'}),
                       'codigo_barras': forms.TextInput(attrs={'placeholder': 'Código de Barras'}),
                       'nombre':forms.TextInput(attrs={'placeholder': 'Nombre'}),
                       'rp_madre':forms.TextInput(attrs={
                                      'placeholder': 'RP de la madre',
                                      'data-reveal-id': 'myModal'}),
                       'rp_padre':forms.TextInput(attrs={
                                      'placeholder': 'RP del padre',
                                      'data-reveal-id': 'myModal2'}),
            }

Formulario de Ordeño
    Para el registro diario de producción de leche de las vacas registradas en HatosGanaderos se ahce uso de un formulario, el cuál contiene la clase que va a usar en este caso **Ordenio** luego se registran los atributos con ciertas caracteristicas que serán indicadas en el template.

    .. py:class:: class ordenioForm(forms.ModelForm):
      
      class Meta:

        | model = Ordenio
        | exclude = ['total',
                   'numero_ordenio',
                   'ganado',
                   'fecha']
        | widgets = {
                    'cantidad': forms.TextInput(attrs={
                                'placeholder': 'Número de litros de leche'
                      }),
                    'observaciones': forms.Textarea(attrs={
                                'placeholder': 'Observaciones'
                      })
        }     


Formulario de Etapa
    Un ganado pertenece a una etapa segun su edad para ello se hace uso de un formulario que brinde esta funcionalidad.

    .. py:class:: class etapaForm(forms.ModelForm):
      
      class Meta:

        | model = Etapa
        | exclude =['is_active']    


Formulario del Ganado
    En el sistema se pueden registrar los ganados y es necesario crear un formulario para poder ingresar correctamente los datos. Con sus respectivas clases atributos y widgets para mejorar la funcionalidad y diseño en el template.

    .. py:class:: class ganadoForm(forms.ModelForm):
        
        class Meta:

            | model = Ganado
            | exclude = ['ganaderia', 
                       'identificacion_simple', 
                       'identificacion_ecuador',
                       'edad',
                       'etapa',
                       'verificacion',
                       'celo',
                       'ciclo',
                       'gestacion',
                       'ordenio',
                       'edad_anios',
                       'edad_meses',
                       'edad_dias',
                       ]
            | widgets ={
                        'nacimiento': forms.DateInput(attrs={
                                        'class': 'datetimepicker2',
                                        'placeholder': 'Fecha de nacimiento'
                          }),
                        'observaciones': forms.Textarea(attrs={
                                        'placeholder': 'Observaciones'
                          }),
                        'imagen': forms.FileInput(attrs={}),
                        'live_weight': forms.TextInput(attrs={
                                        'placeholder': '¿Cuál es el peso vivo?'
                        }),
            } 


Formulario de edición del registro del ganado:
    Los ganados registrados en HatosGanaderos deben brindar la posibilidad de que se realice algún cambio en sus datos. Para ello se crea el formulario de edición del ganado a través de **editaGanadoForm**.

    .. py:class:: class editaGanadoCeloForm(forms.ModelForm):
      
      class Meta:

        | model = Celo
        | exclude = ['ganado',
                   'is_active',
                   'fecha_fin',
                   'estado']
        | widgets = {
                    'fecha_inicio': forms.DateInput(attrs={
                                      'class': 'datetimepicker',
                                      'placeholder': u'¿Cuándo inicio el celo?'
                      }),
                    'observaciones': forms.Textarea(attrs={
                                      'placeholder': 'Observaciones'
                      })
        }


Formulario de intentos de verificación del servicio:
    El sistema HatosGanaderos provee una funcionalidad de verificar el correcto servicio a través de intentos y para ello se hace uso de varias clases con sus respectivos atributos y widgets.

    .. py:class:: class attemptForm(forms.ModelForm):
      
      class Meta:

        | model = Attempt
        | exclude = ['attempt', 'attempt_date', 'state', 'verification']
        | widgets = {
                    'rp_father': forms.TextInput(attrs={
                                      'placeholder': 'RP del padre',
                                      'data-reveal-id': 'myModal2'
                      }),
                    'observations': forms.Textarea(attrs={
                                      'placeholder': 'Observaciones'
                      })
        }

    .. py:class:: class verificationForm(forms.ModelForm):
     
      class Meta:

        | model = Verification


    .. py:class:: class attemptServiceForm(forms.ModelForm):
      
      class Meta:

        | model = Attempt
        | exclude = ['verification']

    .. py:class:: class verifyAttemptForm(forms.ModelForm):
      
      class Meta:

        | model = Attempt
        | exclude = ['attempt', 'attempt_date', 'verification']
        | widgets = {
                    'rp_father': forms.TextInput(attrs={
                                      'placeholder': 'RP del padre',
                                      'data-reveal-id': 'myModal2'
                      }),
                    'observations': forms.Textarea(attrs={
                                      'placeholder': 'Observaciones'
                      })
        }


Formulario de gestación del ganado:
    El sistema HatosGanaderos provee una funcionalidad de registrar la gestación de los ganados y además registrar un posible problema que se pueda presentar en el transcurso del mismo.

    .. py:class:: class gestacionForm(forms.ModelForm):
      
      class Meta:

        | model = Gestacion
        | exclude = ['problema', 'is_active', 'ganado']
        | widgets = {
                    'fecha_servicio': forms.TextInput(attrs={
                                      'placeholder': 'Fecha del Servicio',
                                      'class': 'datetimepicker2'
                      }),
                    'fecha_parto': forms.TextInput(attrs={
                                      'placeholder': 'Fecha Posible del Parto',
                                      'class': 'datetimepicker2'
                      }),
                    'observaciones': forms.Textarea(attrs={
                                      'placeholder': 'Observaciones'
                      })
        }

    .. py:class:: class problemGestacionForm(forms.ModelForm):

      class Meta: 

        | model = ProblemaGestacion
        | widgets = {
                    'fecha_problema': forms.TextInput(attrs={
                                      'placeholder': 'Fecha del Problema',
                                      'class': 'datetimepicker2'
                      }),
                    'observaciones': forms.Textarea(attrs={
                                      'placeholder': 'Observaciones'
                      })
        }


Formulario de baja de ganados y esperma:
    El sistema HatosGanaderos provee una funcionalidad de dar de baja ya sea el registro de ganado como de esperma, se creó un formulario con las clases, atributos y widgets necesarios.

    .. py:class:: class downCattleForm(forms.ModelForm):
      
      class Meta:

        | model = DownCattle
        | widgets = {
                    'date': forms.TextInput(attrs={
                        'placeholder': 'Fecha de la baja',
                        'class': 'datetimepicker2'
                      }),
                    'observations': forms.Textarea(attrs={
                        'placeholder': 'Observaciones'
                      })
        }

    .. py:class:: class downInseminationForm(forms.ModelForm):
      
      class Meta:

        | model = DownInsemination
        | widgets = {
                    'date': forms.TextInput(attrs={
                        'placeholder': 'Fecha de la baja',
                        'class': 'datetimepicker2'
                      }),
                    'observations': forms.Textarea(attrs={
                        'placeholder': 'Observaciones'
                      })
        }




models.py
---------

En este archivo se detalla cada una de las clases que se van a utilizar en el sistema HatosGanaderos. Se describen con cada uno de sus atributos respetando las normas de Django.

Clase Identificacion_Simple:
    Iniciamos con la clase **Identificacion_Simple** que es la encargada de registrar el identificativo de cada ganado que se registre en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. py:function:: Código de la clase Identificacion_Simple:

      | #-*- coding: utf-8 -*-
      | from django.db import models
      | from profiles.models import Ganaderia
      | from django.core import serializers
      
      .. py:class:: class Identificacion_Simple(models.Model):

          | rp = models.PositiveIntegerField('RP')
          | nombre = models.CharField('Agregue un nombre', max_length='13')
          | rp_madre = models.PositiveIntegerField('RP de la Madre')
          | rp_padre = models.PositiveIntegerField('RP del Padre')

          class Meta:

              ordering = ['rp']


Clase Identificacion_Ecuador:
    Iniciamos con la clase **Identificacion_Ecuador** que es la encargada de registrar el identificativo de cada ganado que se registre en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. note:: Código de la clase Identificacion_Ecuador:

    .. py:class:: class Identificacion_Ecuador(models.Model):

        | siglas_pais = models.CharField('Siglas del pais',
                                        max_length='7'
                                        )
        | codigo_pais = models.CharField('Codigo de pais',
                                        max_length='7'
                                        )
        | codigo_provincia = models.CharField('Codigo de provincia',
                                        max_length='7'
                                        )
        | numero_serie = models.CharField('Numero de serie',
                                        max_length='8'
                                        )
        | codigo_barras = models.CharField('Codigo de barras',
                                        max_length='20'
                                        )
        | rp = models.PositiveIntegerField('RP')
        | nombre = models.CharField('Nombre',
                                    max_length='13'
                                    )
        | rp_madre = models.PositiveIntegerField('RP-Madre')
        | rp_padre = models.PositiveIntegerField('RP-Padre')

        def __unicode__(self):

            return self.nombre

        class Meta:

            ordering = ['rp']


Clase Ganado:
    Iniciamos con la clase **Ganado** que es la encargada de persistir cada ganado que se registre en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. note:: Código de la clase Ganado:

    .. py:function:: class Ganado(models.Model):

        | imagen = models.ImageField('Agregue una imagen', upload_to='imagenGanado')
        | ganaderia = models.ForeignKey(Ganaderia, related_name='ganados')
        | nacimiento = models.DateField('Agregue el nacimiento')
        | GENDER_CHOICES = (
            (0, 'Macho'),
            (1, 'Hembra'),
            (2, 'Sin Definir')
        )
        | genero = models.PositiveSmallIntegerField('¿Cuál es el sexo?',
                                                  choices=GENDER_CHOICES,
                                                  default=0
                                                  )
        | RAZAS_CHOICES = (
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
        | raza = models.PositiveSmallIntegerField('¿Cuál es la Raza?',
                                                  choices=RAZAS_CHOICES,
                                                  default=0
                                                  )

        | CONCEPCION_CHOICES = (
            (0, u'Inseminación'),
            (1, 'Monta')
        )
        | forma_concepcion = models.PositiveSmallIntegerField('¿Cómo se concibio?',
                                                  choices=CONCEPCION_CHOICES,
                                                  default=0
                                                  )
        | live_weight = models.FloatField('¿Cuál es el peso vivo?', blank=True, null=True)
        | UNIT_LIVE_WEIGHT_CHOICES = (
            (0, 'Kg'),
            (1, 'lbs'),
            (2, 'Arrobas')
            )
        | unit_live_weight = models.PositiveSmallIntegerField('Unidad de peso vivo',
                                choices=UNIT_LIVE_WEIGHT_CHOICES,
                                blank=True,
                                null=True,
                                default=0)
        | observaciones = models.TextField(max_length=125)    
        | edad_anios = models.IntegerField()
        | edad_meses = models.IntegerField()
        | edad_dias = models.IntegerField()
        | identificacion_simple = models.ForeignKey(Identificacion_Simple, blank=True, null=True, related_name='identificaciones_simples')
        | identificacion_ecuador = models.ForeignKey(Identificacion_Ecuador, blank=True, null=True, related_name='identificaciones_ecuador')
        | down_cattle = models.OneToOneField(DownCattle, related_name='cattle_down_cattle', blank=True, null=True)

        def __unicode__(self):

            if self.identificacion_simple:

                ctx = self.identificacion_simple.rp
            else:

                ctx = self.identificacion_ecuador.rp
            return ctx

Clase DownCattle:
    Iniciamos con la clase **DownCattle** que es la encargada de dara de baja cada ganado que se registre en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. note:: Código de la clase DownCattle:

    .. py:function:: class DownCattle(models.Model):

        | date = models.DateField('Fecha de Baja')
        | CAUSE_DOWN_CHOICES = (
            (0, 'Muerte'),
            (1, 'Venta'),
            (2, 'Desaparición'))
        | cause_down = models.PositiveSmallIntegerField('Causa de la Baja',
                                            choices=CAUSE_DOWN_CHOICES,
                                            )
        | observations = models.TextField('Observaciones')
        
        def __unicode__(self):

            return self.date + " - " + self.cause_down


Clase Verification:
    Iniciamos con la clase **Verification** que es la encargada de registrar la verificación del servicio en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. note:: Código de la clase Verification:

    .. py:function:: class Verification(models.Model):
        
        | initial_date = models.DateField('Fecha inicial')
        | is_active = models.BooleanField()
        | cattle = models.ForeignKey(Ganado, related_name='verification_cattle')


Clase Attempt:
    Iniciamos con la clase **Attempt** que es la encargada de registrar los intentos previo a la verificación del servicio en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. note:: Código de la clase Attempt:

    .. py:function:: class Attempt(models.Model):
        
        | attempt = models.IntegerField('Intento')
        | attempt_date = models.DateField('Fecha del intento')
        | STATE_CHOICES = (
            (0, 'Correcto'),
            (1, 'Incorrecto')
        )
        | state = models.PositiveSmallIntegerField('Estado', 
                            choices=STATE_CHOICES,
                            blank=True,
                            null=True)
        | observations = models.TextField('Observaciones', blank=True, null=True)
        | TYPE_CONCEPTION_CHOICES = (
            (0, u'Inseminación'),
            (1, 'Monta')
        )
        | type_conception = models.PositiveSmallIntegerField(u'Tipo de concepción',
                            choices=TYPE_CONCEPTION_CHOICES,
                            default=0)
        | rp_father = models.PositiveIntegerField('RP del Padre', null=True, blank=True)
        | verification = models.ForeignKey(Verification, null=True, related_name='attempt_verification')


Clase Ordenio:
    Iniciamos con la clase **Ordenio** que es la encargada de registrar los ordeños diarios de cada ganado en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. note:: Código de la clase Ordenio:
    
    .. py:function:: class Ordenio(models.Model):
        
        | fecha = models.DateField(u'Fecha de Ordeño')
        | numero_ordenio = models.IntegerField(u'Número de Ordeños')
        | cantidad = models.IntegerField('¿Cantidad de leche hoy?')
        | total = models.IntegerField('Total de leche')
        | observaciones = models.TextField('Observaciones', max_length=150, blank=True, null=True)
        | ganado = models.ForeignKey(Ganado, null=True, related_name='ordenios')
        
        def __unicode__(self):

            return self.fecha

Clase Celo:
    Iniciamos con la clase **Celo** que es la encargada de agregar el celo a cada uno de los ganados en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. note:: Código de la clase Celo:
    
    .. py:function:: class Celo(models.Model):
        
        | fecha_inicio = models.DateTimeField('¿Cuándo inicio el celo?')
        | fecha_fin = models.DateTimeField('Fecha final')
        | ESTADO_CHOICES = (
            (0, 'En celo'),
            (1, 'Sin celo')
            )
        | estado = models.PositiveSmallIntegerField('Estado',
                                                choices=ESTADO_CHOICES
                                                )
        | observaciones = models.TextField('Observaciones', max_length=150, blank=True, null=True)
        | ganado = models.ForeignKey(Ganado, null=True, related_name='celos')
        | is_active = models.BooleanField()

        def __unicode__(self):

            return self.fecha_inicio


Clase Ciclo:
    Iniciamos con la clase **Ciclo** que es la encargada de agregar el ciclo a cada uno de los ganados en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. note:: Código de la clase Ciclo:
    
    .. py:function:: class Ciclo(models.Model):
        
        | fecha_inicio = models.DateField('Fecha de inicio')
        | NOMBRE_CHOICES = (
            (0, u'Período Vacío'),
            (1, u'Período seco'),
            (2, u'Período lactancia'),
            (3, u'Período gestación')
        )
        | nombre = models.PositiveSmallIntegerField(u'Período',
                                                choices=NOMBRE_CHOICES
                                                )
        | fecha_fin = models.DateField('Fecha final')
        | ganado = models.ForeignKey(Ganado, null=True, related_name='ciclos')
        | is_active = models.BooleanField()
        def __unicode__(self):

            return self.nombre

Clase Etapa:
    Iniciamos con la clase **Etapa** que es la encargada de agregar la etapa a cada uno de los ganados en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. note:: Código de la clase Etapa:
    
    .. py:function:: class Etapa(models.Model):
        
        | fecha_inicio = models.DateField('Fecha de inicio')
        | NOMBRE_CHOICES = (
            (0, 'Ternera'),
            (1, 'Vacona'),
            (2, 'Vientre'),
            )
        | nombre = models.PositiveSmallIntegerField('Etapa',
                                                choices=NOMBRE_CHOICES
                                                )
        | observaciones = models.TextField('Observaciones', max_length=150)
        | ganado = models.ForeignKey(Ganado, null=True, related_name='etapas')
        | is_active = models.BooleanField()

        def __str__(self):

            | ctx = str(self.nombre) + ' - ' + str(self.fecha_inicio)
            | return ctx

Clase Gestacion:
    Iniciamos con la clase **Gestacion** que es la encargada de agregar la gestación a cada uno de los ganados en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. note:: Código de la clase Gestacion:
    
    .. py:function:: class Gestacion(models.Model):
        
        | fecha_servicio = models.DateField('Fecha de servicio')
        | fecha_parto = models.DateField('Fecha del posible parto')
        | TIPO_PARTO_CHOICES = (
            (0, 'Natural'),
            (1, u'Cesárea')
            )
        | tipo_parto = models.PositiveSmallIntegerField('Tipo de parto',
                                                        choices=TIPO_PARTO_CHOICES,
                                                        blank=True,
                                                        null=True
                                                        )
        | observaciones = models.TextField('Observaciones', max_length=150, blank=True, null=True)
        | problema = models.OneToOneField(ProblemaGestacion, blank=True, null=True)
        ganado = models.ForeignKey(Ganado, null=True, related_name='gestaciones')
        | is_active = models.BooleanField()
        def __unicode__(self):

            return self.fecha_servicio


Clase ProblemaGestacion:
    Iniciamos con la clase **ProblemaGestacion** que es la encargada de agregar un problema de gestación a cada uno de los ganados que se encuentre en gestación en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. note:: Código de la clase ProblemaGestacion:
    
    .. py:function:: class ProblemaGestacion(models.Model):
        
        | fecha_problema = models.DateField()
        | TIPO_PROBLEMA_CHOICES = (
            (0, 'Aborto'),
            (1, 'Nacido muerto'),
            (2, 'Madre muerta'),
            (3, 'Los dos muertos'))
        | tipo_problema = models.PositiveSmallIntegerField('Tipo de problema',
                                                        choices=TIPO_PROBLEMA_CHOICES)
        | observaciones = models.TextField('Observaciones', max_length=150)
        def __unicode__(self):

            return self.fecha_problema

Clase Insemination:
    Iniciamos con la clase **Insemination** que es la encargada de persistir un registro de esperma en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. note:: Código de la clase Insemination:
    
    .. py:function:: class Insemination(models.Model):
        
        | down_insemination = models.OneToOneField(DownInsemination, related_name='insemination_down', blank=True, null=True)
        | farm = models.ForeignKey(Ganaderia, related_name='insemination_farm')
        | rp = models.IntegerField('RP')
        | name = models.TextField('Nombre', max_length=50)
        | registration_date = models.DateField('Fecha de registro')
        | amount_pajuelas = models.IntegerField('Número de pajuelas')
        | BREED_CHOICES = (
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
        | breed = models.PositiveSmallIntegerField('Raza',
                            choices=BREED_CHOICES)
        | observations = models.TextField('Observaciones')


Clase DownInsemination:
    Iniciamos con la clase **DownInsemination** que es la encargada de dar de baja a cada uno de los registros de esperma en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. note:: Código de la clase DownInsemination:
    
    .. py:function:: class DownInsemination(models.Model):
        
        | date = models.DateField('Fecha de Baja')
        | CAUSE_DOWN_CHOICES = (
            (0, 'Agotamiento'),
            (1, u'Muestra no adecuada')
            )
        | cause_down = models.PositiveSmallIntegerField('Causa de la Baja',
                                            choices=CAUSE_DOWN_CHOICES,
                                            )
        | observations = models.TextField('Observaciones')
        
        def __unicode__(self):

            return self.date + " - " + self.cause_down



views.py
--------

El archivo views.py es aquel que se encarga de contener la lógica del sistema. Para ello se cuenta con las siguientes funciones:

    - add_down_cattle
    - add_down_insemination
    - lista_ganado_produccion
    - agrega_ganado_ordenio
    - edita_ganado_ordenio
    - list_cattle
    - list_cattle_male
    - edita_ganado
    - edit_cattle_male
    - add_insemination
    - edit_insemination
    - list_insemination
    - add_cattle
    - edita_ganado_celo
    - add_service
    - add_attempt_service
    - verify_attempt
    - gestacion
    - problem_gestacion


add_down_cattle
    Esta función recibe el id del ganado, luego valida si la información que viene del formulario es la correcta si lo és procede a guardarla.

    .. note:: Código de add_down_cattle():
    
    .. py:function:: def add_down_cattle(request, id_cattle):
        
        | cattle = Ganado.objects.get(id=id_cattle)
        if request.method == 'POST':

            formDownCattleForm = downCattleForm(request.POST)
            if formDownCattleForm.is_valid():

                | cattle.down_cattle = formDownCattleForm.save()
                | cattle.save()
                | return redirect(reverse('add_cattle'))
        else:

            formDownCattleForm = downCattleForm()
        return render_to_response('add_down_cattle.html', 
            {'formDownCattleForm': formDownCattleForm,
             'cattle': cattle},
             context_instance=RequestContext(request))


add_down_insemination
    Esta función recibe el id del registro de esperma, luego valida si la información que viene del formulario es la correcta si lo és procede a guardarla.

    .. note:: Código de add_down_insemination():
    
    .. py:function:: def add_down_insemination(request, id_sperm):
        
        | sperm = Insemination.objects.get(id=id_sperm)
        if request.method == 'POST':

            | formDownInseminationForm = downInseminationForm(request.POST)
            if formDownInseminationForm.is_valid():

                | sperm.down_insemination = formDownInseminationForm.save()
                | sperm.save()
                | return redirect(reverse('add_cattle'))
        else:

            formDownInseminationForm = downInseminationForm()
        return render_to_response('add_down_insemination.html', 
            {'formDownInseminationForm': formDownInseminationForm,
             'sperm': sperm},
             context_instance=RequestContext(request))


lista_ganado_produccion
    Esta función recibe el usuario logueado en el sistema, verifica el número de mensajes que existán para la ganadería.

    Finalmente devuelve al usuario un listado de los ganados que se encuentren actualmente en producción dentro de la ganadería.

    .. note:: Código de lista_ganado_produccion():
    
    .. py:function:: def lista_ganado_produccion(request, username):
        
        | user = request.user
        | id_user = User.objects.filter(username=username)
        number_message = number_messages(request, user.username)
        try:

            ganaderia = Ganaderia.objects.get(perfil=id_user)
        except ObjectDoesNotExist:

            | return redirect(reverse('agrega_ganaderia_config'))
        | configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)

        if configuracion.tipo_identificacion == 'simple':

            gg = Ganado.objects.filter(ganaderia_id=ganaderia.id, down_cattle=None, genero=1, etapas__nombre=2, ciclos__nombre=2)

        else:

            gg = Ganado.objects.filter(ganaderia_id=ganaderia.id, genero=1)
        
        return render_to_response('lista_ganado_produccion.html',
            {'ganado':gg,
             'number_messages': number_message},
            context_instance=RequestContext(request))


agrega_ganado_ordenio
    Esta función recibe el usuario logueado en el sistema y el id del ganado, verifica el número de mensajes que existán para la ganadería.

    Finalmente verifica la información recibida en el formulario y si es correcta la persiste.

    .. note:: Código de agrega_ganado_ordenio():
    
    .. py:function:: def agrega_ganado_ordenio(request, username, ganado_id):

        | user = request.user
        | id_user = User.objects.filter(username=username)
        | number_message = number_messages(request, user.username)
        | ganaderia = Ganaderia.objects.get(perfil=id_user)
        | configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)
        | ganado = Ganado.objects.get(id=ganado_id)
        | fecha_hoy = datetime.date.today()
        | ordenios = ganado.ordenios.all()
        | num_ordenios = 1
        
        for ordenio in ordenios:

            if fecha_hoy == ordenio.fecha:

                num_ordenios = ordenio.numero_ordenio + 1
                cantidad = ordenio.total
        | total_ordenios = configuracion.numero_ordenios
        msj = 'False'

        if request.method == 'POST':

            formOrdenio = ordenioForm(request.POST)
            if formOrdenio.is_valid():

                formOrdenio = formOrdenio.save(commit=False)
                if num_ordenios == 1:

                    formOrdenio.numero_ordenio = num_ordenios
                    formOrdenio.total = formOrdenio.cantidad 
                else:

                    formOrdenio.numero_ordenio = num_ordenios
                    formOrdenio.total = formOrdenio.cantidad + cantidad
                formOrdenio.ganado = ganado
                formOrdenio.fecha = fecha_hoy
                formOrdenio.save()
                return redirect(reverse('agrega_ganado_ordenio', kwargs={'username': username,
                    'ganado_id': ganado_id}))

        else:
            formOrdenio = ordenioForm()

            if num_ordenios > total_ordenios:
                msj = "Ya has llenado tus registros hoy."

        return render_to_response('agrega_ganado_ordenio.html',
            {'ganado_id': ganado_id,
             'formOrdenio': formOrdenio,
             'fecha': fecha_hoy,
             'num_ordenios': num_ordenios,
             'total_ordenios': total_ordenios,
             'msj': msj,
             'range': range(num_ordenios), 
             'number_messages': number_message},
            context_instance=RequestContext(request))


edita_ganado_ordenio
    Esta función recibe el usuario logueado en el sistema y el id del ganado, verifica el número de mensajes que existán para la ganadería.

    Finalmente verifica la información recibida en el formulario y si es correcta la persiste.

    .. note:: Código de edita_ganado_ordenio():
    
    .. py:function:: def edita_ganado_ordenio(request, username, ganado_id, num_ordenio):
        
        | user = request.user
        | id_user = User.objects.filter(username=username)
        | number_message = number_messages(request, user.username)
        | ganaderia = Ganaderia.objects.get(perfil=id_user)
        | configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)
        | ganado = Ganado.objects.get(id=ganado_id)
        | fecha_hoy = datetime.date.today()
        | ordenios = ganado.ordenios.all()
        | cont_ordenios = 0

        for ordenio in ordenios:

            if fecha_hoy == ordenio.fecha:

                | cont_ordenios += 1
                | id = ordenio.id
                | cantidad = ordenio.total
        
        if request.method == 'POST':

            | ordenio = ganado.ordenios.get(numero_ordenio=num_ordenio, fecha=fecha_hoy)
            | formOrdenio = ordenioForm(request.POST, instance=ordenio)
            | formOrdenio = formOrdenio.save(commit=False)
            formOrdenio.numero_ordenio = ordenio.numero_ordenio
            if num_ordenio == '1':

                formOrdenio.total = formOrdenio.cantidad
            else:

                formOrdenio.total = formOrdenio.cantidad  + cantidad
            formOrdenio.ganado = ganado
            formOrdenio.fecha = ordenio.fecha
            formOrdenio.save()
            return redirect(reverse('edita_ganado_ordenio', kwargs={'username': username,
                    'ganado_id': ganado_id, 'num_ordenio':num_ordenio
                    }))
        else:
            ordenio = ganado.ordenios.get(numero_ordenio=num_ordenio, fecha=fecha_hoy)
            formOrdenio = ordenioForm(instance=ordenio)

        return render_to_response('edita_ganado_ordenio.html',
            {'ganado_id': ganado_id,
             'formOrdenio': formOrdenio,
             'range': range(cont_ordenios+1),
             'number_messages': number_message},
            context_instance=RequestContext(request))


list_cattle
    Esta función verifica el número de mensajes que existán para la ganadería.

    Finalmente envia el listado de todos los animales registrados en la entidad ganadera.

    .. note:: Código de list_cattle():
    
    .. py:function:: def list_cattle(request):
        
        | user = request.user
        | number_message = number_messages(request, user.username)
        | return render_to_response('list_cattle.html',
            {'number_messages': number_message},
            context_instance=RequestContext(request))


list_cattle_male
    Esta función verifica el número de mensajes que existán para la ganadería.

    Finalmente envia el listado de todos los animales machos registrados en la entidad ganadera.

    .. note:: Código de list_cattle_male():
    
    .. py:function:: def list_cattle_male(request):
        
        | user = request.user
        | number_message = number_messages(request, user.username)    
        | return render_to_response('list_cattles_male.html',
            {'number_messages': number_message},
            context_instance=RequestContext(request))


Calcular edad en días, meses y años
    Estas funciones reciben la fehca de nacimiento y calculan el número de días, meses y años del ganado.

    .. note:: Código de Calcular edad en días, meses y años:
    
    .. py:function:: def calcula_edad_anios(request, date):
        
        | #Get the current date
        | now = datetime.datetime.utcnow()
        | now = now.date()
        | #Get the difference between the current date and the birthday
        | age = dateutil.relativedelta.relativedelta(now, date)
        | age = age.years

        return age

    def calcula_edad_meses(request, date):
        
        | now = datetime.datetime.utcnow()
        | now = now.date()
        | age = dateutil.relativedelta.relativedelta(now, date)
        | age = age.months

        return age

    def calcula_edad_dias(request, date):
        
        | now = datetime.datetime.utcnow()
        | now = now.date()
        | age = dateutil.relativedelta.relativedelta(now, date)
        | age = age.days

        return age


Calcular calcula_etapa
    Esta función recibe la edad en días, meses y años,el número de meses maximo de la etapa de ternera reistrada en la configuración y la edad máxima de la etapa de vacona registrada en la configuración de la ganadería.

    .. note:: Código de calcula_etapa():
    
    .. py:function:: def calcula_etapa(request, anios, meses, etapa_ternera, etapa_vacona):
        
        | multiplicador = 12
        if( (multiplicador * anios) + meses ) < etapa_ternera:

            valor_etapa=0
        elif ( (multiplicador * anios) + meses ) < etapa_vacona:

            valor_etapa=1
        else:

            valor_etapa=2
        return valor_etapa


Calcular edita_ganado
    Esta función recibe el id del ganado a editar los datos, verifica que pertenezca a la entidad gandera si es correcta recalcula lo que es la etapa y la asigna nuevamente.

    Finalmente persiste los nuevos datos en el registro del ganado.

    .. note:: Código de edita_ganado():
    
    .. py:function:: def edita_ganado(request, ganado_id):
        
        id_user = request.user
        number_message = number_messages(request, id_user.username)
        ganaderia = Ganaderia.objects.get(perfil=id_user)
        configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)
        ganado = Ganado.objects.get(id=ganado_id)
        et = ganado.etapas.all()

        if configuracion.tipo_identificacion== 'simple':
            identificacion_s = Identificacion_Simple.objects.get(id= ganado.identificacion_simple.id)
        else:
            identificacion_e = Identificacion_Ecuador.objects.get(id= ganado.identificacion_ecuador.id)
        
        ganado = Ganado.objects.get(id=ganado.id)

        if request.method == 'POST':
            form2 = ganadoForm(request.POST, request.FILES, instance=ganado)

            if configuracion.tipo_identificacion == 'simple':
                form = tipoSimpleForm(request.POST, instance=identificacion_s)
                if form.is_valid() and form2.is_valid():
                    # pauso guardar ganado para agregar atributos
                    form2 = form2.save(commit=False)
                    form2.ganaderia = ganaderia
                    
                    form2.identificacion_simple = form.save()
                    anios = calcula_edad_anios(request, form2.nacimiento)
                    meses = calcula_edad_meses(request, form2.nacimiento)
                    form2.edad_anios = anios
                    form2.edad_meses = meses
                    form2.edad_dias = calcula_edad_dias(request, form2.nacimiento)

                    # saber cual es la ultima etapa de este ganado
                    et_actual = calcula_etapa(request, anios, meses, configuracion.etapa_ternera, configuracion.etapa_vacona)
                    
                    for etapa in et:
                        if etapa.nombre == 0:
                            id = etapa.nombre
                        elif etapa.nombre == 1:
                            id = etapa.nombre
                        else:
                            id = etapa.nombre
                        #etapa.is_active=False
                        etapa.save()
                    
                    if id != et_actual:
                        etapa_antigua = ganado.etapas.get(nombre=id, is_active=True)
                        etapa_antigua.is_active = False
                        etapa_antigua.save()
                        fecha = datetime.date.today()
                        et = etapaForm()
                        et = et.save(commit=False)
                        et.fecha_inicio=fecha
                        et.nombre = et_actual
                        et.observaciones='ninguna observacion'
                        form2.save()
                        et.ganado = Ganado.objects.get(id=form2.id)
                        et.is_active = True
                        et.save()
                    else:
                        form2.save()
            else:
                form = tipoNormaEcuadorForm(request.POST, instance=identificacion_e)
                if form.is_valid() and form2.is_valid():
                    # pauso guardar ganado para agregar atributos
                    form2 = form2.save(commit=False)
                    form2.ganaderia = ganaderia
                    
                    form2.identificacion_ecuador = form.save()
                    anios = calcula_edad_anios(request, form2.nacimiento)
                    meses = calcula_edad_meses(request, form2.nacimiento)
                    form2.edad_anios = anios
                    form2.edad_meses = meses
                    form2.edad_dias = calcula_edad_dias(request, form2.nacimiento)

                    # saber cual es la ultima etapa de este ganado
                    et_actual = calcula_etapa(request, anios, meses, configuracion.etapa_ternera, configuracion.etapa_vacona)
                    
                    for etapa in et:
                        if etapa.nombre == 0:
                            id = etapa.nombre
                        elif etapa.nombre == 1:
                            id = etapa.nombre
                        else:
                            id = etapa.nombre
                        #etapa.is_active=False
                        etapa.save()
                    
                    if id != et_actual:
                        etapa_antigua = ganado.etapas.get(nombre=id, is_active=True)
                        etapa_antigua.is_active = False
                        etapa_antigua.save()
                        fecha = datetime.date.today()
                        et = etapaForm()
                        et = et.save(commit=False)
                        et.fecha_inicio=fecha
                        et.nombre = et_actual
                        et.observaciones='ninguna observacion'
                        form2.save()
                        et.ganado = Ganado.objects.get(id=form2.id)
                        et.is_active = True
                        et.save()
                    else:
                        form2.save()

            return redirect(reverse('list_cattle'))

        elif configuracion.tipo_identificacion == 'simple':
            form = tipoSimpleForm(instance=identificacion_s)
            form2 = ganadoForm(instance=ganado)
        else:
            form = tipoNormaEcuadorForm(instance=identificacion_e)
            form2 = ganadoForm(instance=ganado)

        return render_to_response('edita_ganado.html',
            {'formIdentificacion': form,
             'formGanado': form2,
             'id_cattle': ganado_id,
             'ganado': ganado,
             'number_messages': number_message},
            context_instance=RequestContext(request))


Calcular edit_cattle_male
    Esta función recibe el id del ganado macho a editar los datos, verifica que pertenezca a la entidad gandera si es correcta recalcula lo que es la etapa y la asigna nuevamente.

    Finalmente persiste los nuevos datos en el registro del ganado.

    .. note:: Código de edit_cattle_male():
    
    .. py:function:: def edit_cattle_male(request, cattle_id):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        configuration = Configuracion.objects.get(id=farm.configuracion_id)
        cattle = Ganado.objects.get(id=cattle_id)

        if configuration.tipo_identificacion== 'simple':
            identification_simple = Identificacion_Simple.objects.get(id= cattle.identificacion_simple.id)
        else:
            identification_ecuador = Identificacion_Ecuador.objects.get(id= cattle.identificacion_ecuador.id)

        if request.method == 'POST':
            form2 = ganadoForm(request.POST, request.FILES, instance=cattle)

            if configuration.tipo_identificacion == 'simple':
                form = tipoSimpleForm(request.POST, instance= identification_simple)
                if form.is_valid() and form2.is_valid():
                    # pauso guardar ganado para agregar atributos
                    form2 = form2.save(commit=False)
                    form2.ganaderia = farm
                    
                    form2.identificacion_simple = form.save()
                    anios = calcula_edad_anios(request, form2.nacimiento)
                    meses = calcula_edad_meses(request, form2.nacimiento)
                    form2.edad_anios = anios
                    form2.edad_meses = meses
                    form2.edad_dias = calcula_edad_dias(request, form2.nacimiento)
                    form2.save()
            else:
                form = tipoNormaEcuadorForm(request.POST, instance= identification_ecuador)
                if form.is_valid() and form2.is_valid():
                    # pauso guardar ganado para agregar atributos
                    form2 = form2.save(commit=False)
                    form2.ganaderia = farm
                    
                    form2.identificacion_ecuador = form.save()
                    anios = calcula_edad_anios(request, form2.nacimiento)
                    meses = calcula_edad_meses(request, form2.nacimiento)
                    form2.edad_anios = anios
                    form2.edad_meses = meses
                    form2.edad_dias = calcula_edad_dias(request, form2.nacimiento)
                    form2.save()

            return redirect(reverse('list_cattle_male'))

        elif configuration.tipo_identificacion == 'simple':
            form = tipoSimpleForm(instance=identification_simple)
            form2 = ganadoForm(instance=cattle)
        else:
            form = tipoNormaEcuadorForm(instance=identification_ecuador)
            form2 = ganadoForm(instance=cattle)

        return render_to_response('edita_ganado.html',
            {'formIdentificacion': form,
             'formGanado': form2,
             'id_cattle': cattle_id,
             'ganado': cattle,
             'number_messages': number_message},
            context_instance=RequestContext(request))


Calcular add_insemination
    Esta función verifica el número de mensajes que pueda tener la entidad ganadera ademas de enviar un formulario al usuario luego que el lo llena el usuario es verficado para que sea correcto y es perisistido finalmente.

    .. note:: Código de add_insemination():
    
    .. py:function:: def add_insemination(request):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)

        if request.method == 'POST':
            formInsemination = inseminationForm(request.POST)
            if formInsemination.is_valid():
                formInsemination = formInsemination.save(commit=False)
                if Insemination.objects.filter(farm=farm).count() > 0:
                    insemination = Insemination.objects.filter(farm=farm).order_by('rp').reverse()[:1]
                    for i in insemination:
                        formInsemination.rp = i.rp+1
                else:
                    formInsemination.rp = 1

                formInsemination.farm = farm
                formInsemination.save()

                return redirect(reverse('list_insemination'))

        elif request.method == 'GET':
            formInsemination = inseminationForm()
        return render_to_response('add_insemination.html',
                {'formInsemination': formInsemination,
                 'number_messages': number_message},
                context_instance=RequestContext(request))


Calcular edit_insemination
    Esta función recibe el id del registro de la inseminación registrada en el sistema web HatosGanaderos. 

    Finalmente verifica los nuevos datos ingresados por el usuario y si son correctos los érsiste.

    .. note:: Código de edit_insemination():
    
    .. py:function:: def edit_insemination(request, insemination_id):

        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        insemination = Insemination.objects.get(id=insemination_id)

        if request.method == 'POST':
            formInsemination = inseminationForm(request.POST, instance=insemination)
            if formInsemination.is_valid():
                formInsemination = formInsemination.save(commit=False)
                formInsemination.farm = farm
                formInsemination.rp = insemination.rp
                formInsemination.save()

                return redirect(reverse('list_insemination'))
                
        else:
            formInsemination = inseminationForm(instance=insemination)

        return render_to_response('edit_insemination.html',
            {'formInsemination': formInsemination,
             'insemination_id': insemination_id,
             'number_messages': number_message},
            context_instance=RequestContext(request))


Calcular list_insemination
    Esta función redirecciona al usuario a un template para que pueda listar todos los registros de esperma registrados en HatosGanaderos.

    .. note:: Código de list_insemination():
    
    .. py:function:: def list_insemination(request): 
        
        user = request.user
        number_message = number_messages(request, user.username)
        return render_to_response('list_insemination.html',
            {'number_messages': number_message},
            context_instance=RequestContext(request))


Calcular add_cattle
    Esta función envia al usuario un formulario para que ingrese datos del ganado luego que el finaliza y envía los datos, el sistema verifica esa información y calcula los días, meses y años del ganado con lo cuál ya puede caluclar la etapa y el período en el que se encuentra y persistirlo de manera correcta.

    .. note:: Código de add_cattle():
    
    .. py:function:: def add_cattle(request):
        
        user = request.user
        number_message = number_messages(request, user.username)
        try:
            farm = Ganaderia.objects.get(perfil=user)
        except ObjectDoesNotExist:
            return redirect(reverse('agrega_ganaderia_config'))
        configuration = Configuracion.objects.get(id=farm.configuracion_id)
        
        if request.method == 'POST':

            formGanado = ganadoForm(request.POST, request.FILES)
            
            if configuration.tipo_identificacion == 'simple':
                formIdentificacion = tipoSimpleForm(request.POST)
                if formIdentificacion.is_valid() and formGanado.is_valid():
                    # pauso guardar ganado para agregar atributos
                    formGanado = formGanado.save(commit=False)
                    formIdentificacion = formIdentificacion.save(commit=False)

                    if Ganado.objects.filter(ganaderia=farm).count() > 0:
                        cattle = Ganado.objects.filter(ganaderia=farm).reverse()[:1]
                        for g in cattle:
                            rp_old = Identificacion_Simple.objects.filter(id=g.identificacion_simple.id).order_by('rp').reverse()[:1]
                            for r in rp_old:
                                formIdentificacion.rp = r.rp+1
                    else:
                        formIdentificacion.rp = 1


                    # disminuir las pajuelas
                    if formGanado.forma_concepcion == 0: # inseminacion
                        try:
                            insemination = Insemination.objects.get(rp=formIdentificacion.rp_padre)
                            insemination.amount_pajuelas = insemination.amount_pajuelas - 1
                            insemination.save()
                        except ObjectDoesNotExist:
                            pass
                        

                    # crea objeto etapa
                    date = datetime.date.today()
                    if formGanado.genero == 1:
                        et = etapaForm()
                        et = et.save(commit=False)
                        et.fecha_inicio=date
                        anios = calcula_edad_anios(request, formGanado.nacimiento)
                        meses = calcula_edad_meses(request, formGanado.nacimiento)
                        et.nombre = calcula_etapa(request, anios, meses, configuration.etapa_ternera, configuration.etapa_vacona)
                        et.observaciones='ninguna observacion'
                                    
                    formGanado.ganaderia = farm
                    
                    
                    formIdentificacion.save()
                    formGanado.identificacion_simple = formIdentificacion
                    formGanado.edad_anios = calcula_edad_anios(request, formGanado.nacimiento)
                    formGanado.edad_meses = calcula_edad_meses(request, formGanado.nacimiento)
                    formGanado.edad_dias = calcula_edad_dias(request, formGanado.nacimiento)
                    formGanado.save()
                    if formGanado.genero == 1:
                        et.ganado = Ganado.objects.get(id=formGanado.id)
                        et.is_active = True
                        et.save()
                        if et.nombre == 2:
                            periodo = Ciclo()
                            periodo.nombre = 0
                            periodo.fecha_inicio = date.today()
                            periodo.fecha_fin = date.today()+timedelta(days=configuration.periodo_vacio)
                            periodo.ganado = formGanado
                            periodo.is_active = True
                            periodo.save()

                    return redirect(reverse('list_cattle'))
            else:
                formIdentificacion = tipoNormaEcuadorForm(request.POST)
                if formIdentificacion.is_valid() and formGanado.is_valid():
                    # pauso guardar ganado para agregar atributos
                    formGanado = formGanado.save(commit=False)
                    # crea objeto etapa
                    date = datetime.date.today()
                    if formGanado.genero == 1:
                        et = etapaForm()
                        et = et.save(commit=False)
                        et.fecha_inicio=date
                        anios = calcula_edad_anios(request, formGanado.nacimiento)
                        meses = calcula_edad_meses(request, formGanado.nacimiento)
                        et.nombre = calcula_etapa(request, anios, meses, configuration.etapa_ternera, configuration.etapa_vacona)
                        et.observaciones='ninguna observacion'
                                    
                    formGanado.ganaderia = farm
                    
                    formIdentificacion = formIdentificacion.save(commit=False)
                    if Ganado.objects.filter(ganaderia=farm).count() > 0:
                        cattle = Ganado.objects.filter(ganaderia=farm).reverse()[:1]
                        for g in cattle:
                            rp_old = Identificacion_Ecuador.objects.filter(id=g.identificacion_ecuador.id).order_by('rp').reverse()[:1]
                            for r in rp_old:
                                formIdentificacion.rp = r.rp+1
                    else:
                        formIdentificacion.rp = 1
                    formIdentificacion.save()
                    formGanado.identificacion_ecuador = formIdentificacion
                    formGanado.edad_anios = calcula_edad_anios(request, formGanado.nacimiento)
                    formGanado.edad_meses = calcula_edad_meses(request, formGanado.nacimiento)
                    formGanado.edad_dias = calcula_edad_dias(request, formGanado.nacimiento)
                    formGanado.save()
                    if formGanado.genero == 1:
                        et.ganado = Ganado.objects.get(id=formGanado.id)
                        et.is_active = True
                        et.save()
                        if et.nombre == 2:
                            periodo = Ciclo()
                            periodo.nombre = 0
                            periodo.fecha_inicio = date.today()
                            periodo.fecha_fin = date.today()+timedelta(days=configuration.periodo_vacio)
                            periodo.ganado = formGanado
                            periodo.is_active = True
                            periodo.save()

                    return redirect(reverse('list_cattle'))

        elif configuration.tipo_identificacion == 'simple':
            formIdentificacion = tipoSimpleForm()
            formGanado = ganadoForm()
        else:
            formIdentificacion = tipoNormaEcuadorForm()
            formGanado = ganadoForm()

        return render_to_response('add_cattle.html',
            {'formIdentificacion': formIdentificacion,
             'formGanado': formGanado,
             'number_messages': number_message},
            context_instance=RequestContext(request))   


Calcular edita_ganado_celo
    Esta función recibe como parámetro el id del ganado, verifica el número de mensajes que pueda tener esa entidad gandera.

    Finalmente calcula los datos del nuevo celo y persiste la información.

    .. note:: Código de edita_ganado_celo():
    
    .. py:function:: def edita_ganado_celo(request, ganado_id):

        id_user = request.user
        number_message = number_messages(request, id_user.username)
        ganaderia = Ganaderia.objects.get(perfil=id_user)
        configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)
        ganado = Ganado.objects.get(id=ganado_id)
        ce = ganado.celos.all()

        if ganado.celos.filter(is_active= True).count() > 0:

            if ganado.celos.get(ganado_id=ganado_id, is_active=True):
                celo_ganado = ganado.celos.get(ganado_id=ganado_id, is_active=True)
                if request.method == 'POST':
                    form = editaGanadoCeloForm(request.POST)
                    if form.is_valid():
                        form = form.save(commit=False)
                        # saber cual es la ultima etapa de este ganado
                        for celo in ce:
                            fecha_inicio = celo.fecha_inicio
                            id = celo.id

                        if fecha_inicio != form.fecha_inicio:
                            for celo in ce:
                                celo.is_active = False
                                celo.save()
                            d2=datetime.timedelta(hours=configuracion.celo_duracion)
                            age=form.fecha_inicio + d2
                            form.estado = 0
                            form.fecha_fin = age
                            form.ganado = ganado
                            form.is_active = True
                            form.save()
                            return redirect(reverse('list_cattle'))
                        else:
                            c = Celo.objects.get(id=id)
                            c.observaciones=form.observaciones
                            c.save()

                            return redirect(reverse('list_cattle'))
                    
                else:
                    form = editaGanadoCeloForm(instance=celo_ganado)
            
        else:
            form = editaGanadoCeloForm()
            if request.method == 'POST':
                form = editaGanadoCeloForm(request.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    d2=datetime.timedelta(hours =configuracion.celo_duracion)
                    age=form.fecha_inicio + d2
                    form.estado = 0
                    form.fecha_fin = age
                    form.ganado = ganado
                    form.is_active = True
                    form.save()
                    return redirect(reverse('list_cattle'))

        if ganado.celos.all():
            return render_to_response('edita_ganado_celo.html',
                {'form': form,
                 'ganado_id': ganado_id,
                 'number_messages': number_message},
                context_instance=RequestContext(request))
        else:
            return render_to_response('edita_ganado_celo.html',
                {'form': form,
                 'ganado_id': ganado_id,
                 'number_messages': number_message},
                context_instance=RequestContext(request))


Calcular add_service
    Esta función recibe como parámetro el id del ganado, verifica el número de mensajes que pueda tener esa entidad gandera.

    Finalmente calcula los datos del servicio y persiste la información.

    .. note:: Código de add_service():
    
    .. py:function:: def add_service(request, id_cattle):
        
        user = request.user
        number_message = number_messages(request, user.username)
        cattle = Ganado.objects.get(id=id_cattle)
        
        if request.method == 'POST':
            farm = Ganaderia.objects.get(perfil=user)
            formAttempt = attemptForm(request.POST)

            if formAttempt.is_valid():
                formAttempt = formAttempt.save(commit=False)

                verification = Verification()
                verification.initial_date = date.today()
                verification.is_active = True
                verification.cattle = cattle
                verification.save()
                
                formAttempt.attempt = 1
                date_actual = date.today()+timedelta(days=21)
                formAttempt.attempt_date = date_actual
                formAttempt.verification = verification
                formAttempt.save()

                for i in range(2, farm.configuracion.intentos_verificacion_celo+1):
                    date_actual = date_actual+timedelta(days=21)
                    attempt = Attempt()
                    attempt.attempt = i
                    attempt.attempt_date = date_actual
                    attempt.verification = verification
                    attempt.type_conception = formAttempt.type_conception
                    attempt.rp_father = formAttempt.rp_father
                    attempt.save()

                return redirect(reverse('list_cattle'))
                
        elif request.method == 'GET':
            v = Verification.objects.filter(is_active=True, cattle=id_cattle).count()
            if v > 0:
                return redirect(reverse('add_attempt_service', kwargs={'id_cattle': id_cattle}))
            else:
                formAttempt = attemptForm()

        return render_to_response('add_service.html',
            {'id_cattle': id_cattle,
             'formAttempt': formAttempt,
             'number_messages': number_message},
            context_instance=RequestContext(request))



Calcular intento y verificación del servicio
    Esta función recibe como parámetro el id del ganado, verifica el número de mensajes que pueda tener esa entidad gandera.

    Finalmente calcula los datos del intento y verificación del servicio y persiste la información necesaria.

    .. note:: Código de intento del servicio:
    
    .. py:function:: def add_attempt_service(request, id_cattle):

        user = request.user
        number_message = number_messages(request, user.username)
        cattle = Ganado.objects.get(id=id_cattle)
        attempts = Attempt.objects.filter(verification__cattle=cattle, verification__is_active=True).order_by('id')

        return render_to_response('add_attempt_service.html',
            {'attempts': attempts,
             'number_messages': number_message},
            context_instance=RequestContext(request))

    .. note:: Código de verificación del servicio:
    
    .. py:function:: def verify_attempt(request, id_attempt):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        configuration = Configuracion.objects.get(id=farm.configuracion_id)
        attempt = Attempt.objects.get(id=id_attempt)

        if request.method == 'POST':
            formAttempt = verifyAttemptForm(request.POST, instance=attempt) 
            if formAttempt.is_valid():
                
                formAttempt = formAttempt.save(commit= False)
                formAttempt.save()
                # si fue correcto
                if formAttempt.state == 0:

                    attempt.verification.is_active=False
                    attempt.verification.save()
                    # cambio el is_active de etapa y celo anterior
                    ganado = Ganado.objects.get(id= attempt.verification.cattle.id)
                    #etapa = Etapa.objects.get(ganado_id=ganado.id, is_active=True)
                    #etapa.is_active = False
                    #etapa.save()
                    celo = Celo.objects.get(ganado_id= ganado.id, is_active=True)
                    celo.is_active=False
                    celo.estado = 1
                    celo.save()
                    
                    # agrego el nuevo ciclo
                    ciclo = Ciclo.objects.get(ganado_id=ganado.id, is_active=True, nombre=0)
                    ciclo.is_active = False
                    ciclo.save()
                    ciclo = Ciclo()
                    ciclo.nombre = 3
                    ciclo.fecha_inicio = date.today()
                    ciclo.fecha_fin = date.today()+timedelta(days= configuration.periodo_gestacion)
                    ciclo.ganado = ganado
                    ciclo.is_active = True
                    ciclo.save()

                    # agrego la gestacion
                    gestacion = Gestacion()
                    gestacion.fecha_servicio = date.today()
                    gestacion.fecha_parto = date.today() + timedelta(days=configuration.periodo_gestacion)
                    gestacion.is_active = True
                    gestacion.ganado = ganado
                    gestacion.save()
                    
                    return redirect(reverse('list_cattle'))

                id_cattle = attempt.verification.cattle_id 
                return redirect(reverse('add_attempt_service', kwargs={'id_cattle': id_cattle}))
        else:
            formVerifyAttempt = verifyAttemptForm(instance=attempt)

        return render_to_response('verify_attempt.html',
            {'formVerifyAttempt': formVerifyAttempt,
             'number_messages': number_message},
            context_instance=RequestContext(request))


Calcular registro de gestacion
    Esta función recibe como parámetro el id del ganado, verifica el número de mensajes que pueda tener esa entidad gandera.

    Finalmente calcula los datos del nuevo registro de gestación y persiste la información necesaria.

    .. note:: Código de gestacion():
    
    .. py:function:: def gestacion(request, id_cattle):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        configuration = Configuracion.objects.get(id=farm.configuracion_id)
        ganado = Ganado.objects.get(id=id_cattle)
        gestacion = Gestacion.objects.get(ganado=ganado, is_active=True)

        if request.method == 'POST':

            formGestacion = gestacionForm(request.POST, instance =gestacion)
            if formGestacion.is_valid():
                formGestacion = formGestacion.save(commit=False)
                # gestacion en false
                gestacion.is_active = False
                gestacion.save()
                # desactivar el anterior ciclo
                ciclo = Ciclo.objects.get(ganado= ganado, is_active=True)
                ciclo.is_active = False
                ciclo.save()
                # nuevo ciclo de lactancia
                ciclo = Ciclo()
                ciclo.nombre = 2
                ciclo.fecha_inicio = date.today()
                ciclo.fecha_fin = date.today() + timedelta(days =configuration.periodo_lactancia)
                ciclo.is_active = True
                ciclo.ganado = ganado
                ciclo.save()
                # nuevo ciclo vacio
                ciclo = Ciclo()
                ciclo.nombre = 0
                ciclo.fecha_inicio = date.today()
                ciclo.fecha_fin = date.today() + timedelta(days=configuration.periodo_vacio)
                ciclo.is_active = True
                ciclo.ganado = ganado
                ciclo.save()

                formGestacion.save()
                return redirect(reverse('list_cattle'))
        else:
            formGestacion = gestacionForm(instance =gestacion)
        return render_to_response('gestacion.html',
            {'formGestacion': formGestacion,
             'id_cattle': id_cattle,
             'number_messages': number_message},
            context_instance=RequestContext(request))


Calcular problem_gestacion
    Esta función recibe como parámetro el id del ganado, verifica el número de mensajes que pueda tener esa entidad gandera.

    Finalmente valida los datos del nuevo registro de un problema de gestación y la persiste.

    .. note:: Código de problem_gestacion():
    
    .. py:function:: def problem_gestacion(request, id_cattle):
    
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        configuration = Configuracion.objects.get(id=farm.configuracion_id)
        ganado = Ganado.objects.get(id=id_cattle)
        gestacion = Gestacion.objects.get(ganado=ganado, is_active=True)

        if request.method == 'POST':
            formProblemGestacion = problemGestacionForm(request.POST)
            if formProblemGestacion.is_valid():
                formProblemGestacion = formProblemGestacion.save(commit=False)
                # en el caso de aborto
                if formProblemGestacion.tipo_problema == 0:
                    # desactivar el anterior ciclo
                    ciclo = Ciclo.objects.get(ganado=ganado, is_active=True)
                    ciclo.is_active = False
                    ciclo.save()
                    # nuevo ciclo vacio
                    ciclo = Ciclo()
                    ciclo.nombre = 0
                    ciclo.fecha_inicio = date.today()
                    ciclo.fecha_fin = date.today() + timedelta(days=configuration.periodo_vacio)
                    ciclo.is_active = True
                    ciclo.ganado = ganado
                    ciclo.save()
                    # gestacion en false
                    gestacion.is_active = False
                    gestacion.save()
                # en el caso de nacido muerto
                elif formProblemGestacion.tipo_problema == 1:
                    # desactivar el anterior ciclo
                    ciclo = Ciclo.objects.get(ganado=ganado, is_active=True)
                    ciclo.is_active = False
                    ciclo.save()
                    # nuevo ciclo vacio
                    ciclo = Ciclo()
                    ciclo.nombre = 1
                    ciclo.fecha_inicio = date.today()
                    ciclo.fecha_fin = date.today() + timedelta(days=configuration.periodo_vacio)
                    ciclo.is_active = True
                    ciclo.ganado = ganado
                    ciclo.save()
                    # gestacion en false
                    gestacion.is_active = False
                    gestacion.save()
                # en el caso de madre muerta
                elif formProblemGestacion.tipo_problema == 2:
                    # ciclo en false
                    ciclo = Ciclo.objects.get(ganado=ganado, is_active=True)
                    ciclo.is_active = False
                    ciclo.save()
                    # se llena el DownCattle
                    down_cattle = DownCattle()
                    down_cattle.date = date.today()
                    down_cattle.cause_down = 0
                    down_cattle.observations = 'Desceso del animal'
                    down_cattle.save()
                    # se asigna el down_cattle al ganado
                    ganado.down_cattle = down_cattle
                    ganado.save()
                    # gestacion en false
                    gestacion.is_active = False
                    gestacion.save()
                    # se registra la cria
                    attempt = Attempt.objects.get(verification_id=ganado.id, state=0)
                    cria = Ganado()
                    cria.ganaderia = farm
                    cria.nacimiento = date.today()
                    cria.genero = 2
                    cria.raza = 12
                    cria.forma_concepcion = attempt.type_conception
                    cria.observaciones = 'Nacido pero sin madre'
                    cria.edad_anios = calcula_edad_anios(request, formProblemGestacion.fecha_problema)
                    cria.edad_meses = calcula_edad_meses(request, formProblemGestacion.fecha_problema)
                    cria.edad_dias = calcula_edad_dias(request, formProblemGestacion.fecha_problema)
                    # se crea la identificacion dependiendo (simple o ecuador)
                    if configuration.tipo_identificacion == 'simple':
                        id_simple = Identificacion_Simple()
                        if Ganado.objects.filter(ganaderia=farm).count() > 0:
                            ganad = Ganado.objects.filter(ganaderia=farm).reverse()[:1]
                            for g in ganad:
                                rp_old = Identificacion_Simple.objects.filter(id=g.id).order_by('rp').reverse()[:1]
                                for r in rp_old:
                                    id_simple.rp = r.rp+1
                        id_simple.nombre = 'Temporal'
                        id_simple.rp_madre = ganado.identificacion_simple.rp
                        id_simple.rp_padre = attempt.rp_father
                        id_simple.save()
                        cria.identificacion_simple = id_simple
                        cria.save()
                    else:
                        id_ecuador = Identificacion_Ecuador()
                        if Ganado.objects.filter(ganaderia=farm).count() > 0:
                            ganad = Ganado.objects.filter(ganaderia=farm).reverse()[:1]
                            for g in ganad:
                                rp_old = Identificacion_Ecuador.objects.filter(id=g.id).order_by('rp').reverse()[:1]
                                for r in rp_old:
                                    id_ecuador.rp = r.rp+1
                        id_ecuador.siglas_pais = 'EC'
                        id_ecuador.codigo_pais = '593'
                        id_ecuador.codigo_provincia = '7'
                        id_ecuador.numero_serie = '12345'
                        id_ecuador.codigo_barras = '6789'
                        id_ecuador.nombre = 'Temporal'
                        id_ecuador.rp_madre = ganado.identificacion_ecuador.rp
                        id_ecuador.rp_padre = attempt.rp_father
                        id_ecuador.save()
                        cria.identificacion_ecuador = id_ecuador
                        cria.save()
                # en el caso de los dos muertos
                elif formProblemGestacion.tipo_problema == 3:
                    # ciclo en false
                    ciclo = Ciclo.objects.get(ganado=ganado, is_active=True)
                    ciclo.is_active = False
                    ciclo.save()
                    # se llena el DownCattle
                    down_cattle = DownCattle()
                    down_cattle.date = date.today()
                    down_cattle.cause_down = 0
                    down_cattle.observations = 'Desceso del animal'
                    down_cattle.save()
                    # se asigna el down_cattle al ganado
                    ganado.down_cattle = down_cattle
                    ganado.save()
                    # gestacion en false
                    gestacion.is_active = False
                    gestacion.save()

                formProblemGestacion.save()
                gestacion.problema = formProblemGestacion
                gestacion.save()

                return redirect(reverse('list_cattle'))
        elif request.method == 'GET':
            formProblemGestacion = problemGestacionForm()

        return render_to_response('problem_gestacion.html',
                {'formProblemGestacion': formProblemGestacion,
                 'id_cattle': id_cattle,
                 'number_messages': number_message},
                context_instance=RequestContext(request))