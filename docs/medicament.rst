medicament package
==================

El módulo de medicaments es el que se encarga de:
    
    - Registrar desparasitador
    - Listar desparasitadores
    - Editar desparasitador
    - Asignar desparasitador al ganado
    - Registrar vacuna
    - Listar vacuna
    - Editar vacuna
    - Asignar vacuna al ganado

Con la finalidad de obtener mayor cuidado en el ganado en cuanto a sanidad se refiere. Consta de algunos archivos como: admin.py, forms.py, models.py y views.py.


admin.py
--------

El archivo admin.py es el encargado del registro de las clases que están en el modelo paraque funcionen en el admin de Django. En este caso se agregó el módelo **Medicament** ya que es la que deseamos se encuentre en el admin de django.

    .. py:function:: Código:
    
        | from django.contrib import admin
        | from medicament.models import Medicament
        | admin.site.register(Medicament)


forms.py
--------

Este archivo es el encargado de crear los parámetros correctos que serán utilizados en el formulario del **Desparasitador y Vacuna** se realizan las debidas importaciones además de la configuración de los parámetros que deben o no ir con sus respectivos atributos como clases, id, etc.

Formulario de desparasitador:
    El módulo HatosGanaderos presenta la funcionalidad de registar desparasitadores, para lo cuál se inicia creando en modelo del formulario en este caso se hace uso de la clase **Medicament** con sus respectivos atributos, además se agregan widgets a cada uno de estos atributos que serán utiles para poder realizar un html más vistoso, amigable y funcional.

    .. note:: Código:
    
    .. py:function:: class wormerForm(forms.ModelForm):
        
        class Meta:

            | model = Medicament
            | exclude = ['farm', 'is_vaccine', 'status', 'is_wormer', 'cattle']
            | widgets = {
                'name': forms.TextInput(attrs={
                                'placeholder': 'Nombre de la medicina',
                }),
                'expiration_date':forms.DateInput(attrs={
                                'class': 'datetimepicker2',
                                'placeholder': 'Fecha de expiración',
                }),
               'cattle': forms.TextInput(attrs={}),
               'amount': forms.TextInput(attrs={
                                'placeholder': 'Cantidad de medicina'
                }),
               'application_age': forms.TextInput(attrs={
                                'placeholder': 'Edad de aplicación'
                }),
               'amount_application': forms.TextInput(attrs={
                                'placeholder': 'Cantidad de aplicación'
                }),
               'number_application': forms.TextInput(attrs={
                                'placeholder': 'Número de aplicaciones'
                }),
               'interval': forms.TextInput(attrs={
                                'placeholder': 'Intervalo de tiempo'
                }),
               'live_weight': forms.TextInput(attrs={
                                'placeholder': '¿Cuál es el peso vivo?'
                }),
               'observations': forms.Textarea(attrs={
                                'placeholder': 'Observaciones'
                })
            }


Formulario de vacuna:
    El módulo HatosGanaderos presenta la funcionalidad de registar vacunas, para lo cuál se inicia creando en modelo del formulario en este caso se hace uso de la clase **Medicament** con sus respectivos atributos, además se agregan widgets a cada uno de estos atributos que serán utiles para poder realizar un html más vistoso, amigable y funcional.

    .. note:: Código:
    
    .. py:function:: class vaccineForm(forms.ModelForm):
        
        class Meta:

            | model = Medicament
            | exclude = ['farm', 'is_vaccine', 'status', 'is_wormer', 'cattle']
            | widgets = {
                        'name': forms.TextInput(attrs={
                                        'placeholder': 'Nombre de la medicina',
                        }),
                        'expiration_date':forms.DateInput(attrs={
                                        'class': 'datetimepicker2',
                                        'placeholder': 'Fecha de expiración',
                        }),
                       'cattle': forms.TextInput(attrs={}),
                       'amount': forms.TextInput(attrs={
                                        'placeholder': 'Cantidad de medicina'
                        }),
                       'application_age': forms.TextInput(attrs={
                                        'placeholder': 'Edad de aplicación'
                        }),
                       'amount_application': forms.TextInput(attrs={
                                        'placeholder': 'Cantidad de aplicación'
                        }),
                       'number_application': forms.TextInput(attrs={
                                        'placeholder': 'Número de aplicaciones'
                        }),
                       'interval': forms.TextInput(attrs={
                                        'placeholder': 'Intervalo de tiempo'
                        }),
                       'live_weight': forms.TextInput(attrs={
                                        'placeholder': '¿Cuál es el peso vivo?'
                        }),
                       'observations': forms.Textarea(attrs={
                                        'placeholder': 'Observaciones'
                        })
            }



models.py
---------

En este archivo se detalla cada una de las clases que se van a utilizar en el sistema HatosGanaderos. Se describen con cada uno de sus atributos respetando las normas de Django.

Clase Medicament:
    Iniciamos con la clase **Medicament** que es la encargada de registrar el desparasitador o vacuna que será aplicado a cada ganado que se registre en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. note:: Código de la clase Medicament:
    
    .. py:function:: class Medicament(models.Model):
        
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
        application_age = models.IntegerField( u'Edad de Aplicación')
        TIME_APPLICATION_AGE_CHOICES = (
            (0, u'Aplicación en días'),
            (1, 'Aplicación en meses'),  
            (2, u'Aplicación en años')      
            )
        time_application_age = models.PositiveSmallIntegerField( 'Unidad de tiempo',
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


Clase ApplicationMedicament:
    Continuamos con la clase **ApplicationMedicament** que es la encargada de asignar el desparasitador o vacuna al ganado que se registre en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. note:: Código de la clase ApplicationMedicament:
    
    .. py:function:: class ApplicationMedicament(models.Model):

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



views.py
--------

El archivo views.py es aquel que se encarga de contener la lógica del sistema. Para ello se cuenta con las siguientes funciones:

    - add_wormer
    - list_wormer
    - edit_wormer
    - asign_wormer
    - add_vaccine
    - list_vaccine
    - edit_vaccine
    - asign_vaccine


add_wormer
    Esta función es la encargada de emitir y recibir el formulario con los datos ingresados por el usuario luego son validados y si son sorrectos se persisten en el sistema.

    .. note:: Código de add_wormer():
    
    .. py:function:: def add_wormer(request):
        
        user = request.user
        try:
            ganaderia = Ganaderia.objects.get(perfil=user)
        except ObjectDoesNotExist:
            return redirect(reverse('agrega_ganaderia_config'))
        number_message = number_messages(request, user.username)
        
        if request.method == 'POST':

            form_worme = wormerForm(request.POST)
            if form_worme.is_valid():

                form_wormer = form_worme.save(commit=False)
                form_wormer.farm = ganaderia
                form_wormer.is_vaccine = False
                form_wormer.is_wormer = True
                form_wormer.status = 0
                form_wormer.save()

                return redirect(reverse('list_wormer'))

        elif request.method == 'GET':
            form_wormer = wormerForm()

        return render_to_response('add_wormer.html',
                                    {'form_wormer': form_wormer,
                                     'number_messages': number_message},
                                    context_instance=RequestContext(request)
            )


list_wormer
    Esta función es la encargada de devolver al usuario un listado completo de todos los desparasitadores registrados en la entidad ganadera.

    .. note:: Código de list_wormer():
    
    .. py:function:: def list_wormer(request):
        
        | user = request.user
        | number_message = number_messages(request, user.username)
        | medicaments = Medicament.objects.filter(is_wormer=True, farm_id=user)
        
        return render_to_response('list_wormer.html',
                                    {'medicaments': medicaments,
                                     'number_messages': number_message},
                                    context_instance=RequestContext(request)
                                )


edit_wormer
    Esta función es la encargada de cargar los datos de un desparasitador en un template para que el usuario tenga la opción a modificar cada uno de estos datos luego se valida para persistirlo de manetra correcta.
    
    .. note:: Código de edit_wormer():
    
    .. py:function:: def edit_wormer(request, id_medicament):
        
        | user = request.user
        | number_message = number_messages(request, user.username)
        | medicament = Medicament.objects.get(id=id_medicament)
        if request.method == 'GET':

            form_medicament = wormerForm(instance=medicament)
        elif request.method == 'POST':

            form_medicament = wormerForm(request.POST, instance=medicament)
            if form_medicament.is_valid():

                form_medicament = form_medicament.save(commit=False)
                form_medicament.farm = medicament.farm
                form_medicament.save()
                return redirect(reverse('list_wormer'))

        return render_to_response('edit_wormer.html',
                                    {'form_wormer': form_medicament,
                                     'number_messages': number_message},
                                    context_instance=RequestContext(request)
                                )


asign_wormer
    Esta función es la encargada de asignar un desparasitador a uno o varios ganados que el cliente elija. Finalmente guarda este registro en la base de datos.
    
    .. note :: Código de asign_wormer():
    
    .. py:function:: def asign_wormer(request, wormer_id):
        
        | user = request.user
        | number_message = number_messages(request, user.username)

        return render_to_response('asign_wormer.html',
                                    {'id_wormer': wormer_id,
                                     'number_messages': number_message},
                                    context_instance=RequestContext(request)
                                )



add_vaccine
    Esta función es la encargada de emitir y recibir el formulario con los datos ingresados por el usuario luego son validados y si son sorrectos se persisten en el sistema.

    .. note:: Código de add_vaccine():
    
    .. py:function:: def add_vaccine(request):
        
        | user = request.user
        | number_message = number_messages(request, user.username)
        | ganaderia = Ganaderia.objects.get(perfil=user)
        if request.method == 'POST':

            form_vaccine = vaccineForm(request.POST)
            if form_vaccine.is_valid():

                | form_vaccine = form_vaccine.save(commit=False)
                | form_vaccine.farm = ganaderia
                | form_vaccine.is_vaccine = True
                | form_vaccine.is_wormer = False
                | form_vaccine.status = 0
                | form_vaccine.save()
                
                return redirect(reverse('list_vaccine'))

        elif request.method == 'GET':

            form_vaccine = vaccineForm()

        return render_to_response('add_vaccine.html',
                                    {'form_vaccine': form_vaccine,
                                     'number_messages': number_message},
                                    context_instance=RequestContext(request)
            )


list_vaccine
    Esta función es la encargada de devolver al usuario un listado completo de todos las vacunas registradas en la entidad ganadera.

    .. note:: Código de list_vaccine():
    
    .. py:function:: def list_vaccine(request):
        
        | user = request.user
        | number_message = number_messages(request, user.username)
        | medicaments = Medicament.objects.filter(is_vaccine=True, farm_id=user)

        return render_to_response('list_vaccine.html',
                                    {'vaccines': medicaments,
                                     'number_messages': number_message},
                                    context_instance=RequestContext(request)
                                )


edit_vaccine
    Esta función es la encargada de cargar los datos de una vacuna en un template para que el usuario tenga la opción a modificar cada uno de estos datos luego se valida para persistirlo de manetra correcta.
    
    .. note:: Código de edit_vaccine():
    
    .. py:function:: def edit_vaccine(request, id_medicament):
        
        | user = request.user
        | number_message = number_messages(request, user.username)
        | medicament = Medicament.objects.get(id=id_medicament)
        if request.method == 'GET':

            form_medicament = vaccineForm(instance=medicament)
        elif request.method == 'POST':

            form_medicament = vaccineForm(request.POST, instance=medicament)
            if form_medicament.is_valid():

                form_medicament = form_medicament.save(commit=False)
                form_medicament.farm = medicament.farm
                form_medicament.save()
                return redirect(reverse('list_vaccine'))

        return render_to_response('edit_vaccine.html',
                                    {'form_vaccine': form_medicament,
                                     'number_messages': number_message},
                                    context_instance=RequestContext(request)
                                )


asign_vaccine
    Esta función es la encargada de asignar una vacuna a uno o varios ganados que el cliente elija. Finalmente guarda este registro en la base de datos.
    
    .. note:: Código de asign_vaccine():
    
    .. py:function:: def asign_vaccine(request, vaccine_id):
        
        | user = request.user
        | number_message = number_messages(request, user.username)

        return render_to_response('asign_vaccine.html',
                                    {'id_vaccine': vaccine_id,
                                     'number_messages': number_message},
                                    context_instance=RequestContext(request)
                                )