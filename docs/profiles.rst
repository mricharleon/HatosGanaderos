profiles package
================

El módulo de messages es el que se encarga de:
    
    - Número de mensajes al técnico
    - Agregar la configuración de la ganadería

Con la finalidad de obtener mayor comunicación entre los técnicos de la entidad ganadera. Consta de algunos archivos como: admin.py, forms.py, models.py y views.py.

admin.py
--------

El archivo admin.py es el encargado del registro de las clases que están en el modelo paraque funcionen en el admin de Django. En este caso se agregó el módelo **Configuracion y Ganaderia** ya que es la que deseamos se encuentre en el admin de django.

    .. py:function:: Código:
    
        | from django.contrib import admin
        | from profiles.models import Configuracion, Ganaderia
        | admin.site.register(Configuracion)
        | admin.site.register(Ganaderia)


forms.py
--------

Este archivo es el encargado de crear los parámetros correctos que serán utilizados en el formulario de la **configuración, gandería y el registro de cuentas** se realizan las debidas importaciones además de la configuración de los parámetros que deben o no ir con sus respectivos atributos como clases, id, etc.

Formulario de configuración de la ganadería:
    El módulo HatosGanaderos presenta la funcionalidad de configurar parámetros de la entidad gandera brindando la opción a que se registren multiples entidades ganderas, para lo cuál se inicia creando en modelo del formulario en este caso se hace uso de la clase **Configuracion** con sus respectivos atributos, además se agregan widgets a cada uno de estos atributos que serán utiles para poder realizar un html más vistoso, amigable y funcional.

    .. note:: Código de ConfiguracionForm:
    
    .. py:function:: class ConfiguracionForm(forms.ModelForm):

        class Meta:

            | model = Configuracion
            | exclude = ['etapa_vientre']
            | widgets = {
                      'celo_frecuencia':forms.TextInput(attrs={}),
                      'celo_frecuencia_error':forms.TextInput(attrs={}),
                      'celo_duracion':forms.TextInput(attrs={}),
                      'celo_duracion_error':forms.TextInput(attrs={}),
                      'celo_despues_parto':forms.TextInput(attrs={}),
                      'celo_despues_parto_error':forms.TextInput(attrs={}),
                      'intentos_verificacion_celo':forms.TextInput(attrs={}),
                      'etapa_ternera':forms.TextInput(attrs={}),
                      'etapa_vacona':forms.TextInput(attrs={}),
                      'etapa_vientre':forms.TextInput(attrs={}),
                      'periodo_gestacion':forms.TextInput(attrs={}),
                      'periodo_seco':forms.TextInput(attrs={}),
                      'periodo_lactancia':forms.TextInput(attrs={}),
                      'periodo_vacio':forms.TextInput(attrs={}),
                      'numero_ordenios':forms.TextInput(attrs={}),
            }


Formulario de la ganadería:
    El módulo HatosGanaderos presenta la funcionalidad de crear la ganadería, para lo cuál se inicia creando en modelo del formulario en este caso se hace uso de la clase **Ganderia** con sus respectivos atributos, además se agregan widgets a cada uno de estos atributos que serán utiles para poder realizar un html más vistoso, amigable y funcional.

    .. note:: Código de GanaderiaForm:
    
    .. py:function:: class GanaderiaForm(forms.ModelForm):
        
        class Meta:

            | model = Ganaderia
            | fields = ('nombreEntidad', 'direccion')
            | widgets = {
                      'nombreEntidad':forms.TextInput(attrs={'placeholder': 'Nombre de la ganadería'}),
                      'direccion':forms.TextInput(attrs={'placeholder': 'Direccion de la ganadería'}),
            }


Formulario de cuentas en HatosGanaderos:
    El módulo HatosGanaderos presenta la funcionalidad de crear cuentas pero con ciertos valores personalizados, para lo cuál se inicia creando en modelo del formulario en este caso se hace uso de la clase **Ganderia** con sus respectivos atributos, además se agregan widgets a cada uno de estos atributos que serán utiles para poder realizar un html más vistoso, amigable y funcional.

    .. note:: Código de SignupFormExtra:
    
    .. py:function:: class SignupFormExtra(SignupForm):
        
        """ 
        A form to SIDGVnstrate how to add extra fields to the signup form, in this
        case adding the first and last name.
        

        """
        first_name = forms.CharField(label=_(u'First name'),
                                     max_length=30,
                                     required=False)

        last_name = forms.CharField(label=_(u'Last name'),
                                    max_length=30,
                                    required=False)

        def __init__(self, *args, **kw):
            """
            
            A bit of hackery to get the first name and last name at the top of the
            form instead at the end.
            
            """
            
            super(SignupFormExtra, self).__init__(*args, **kw)
            # Put the first and last name at the top
            new_order = self.fields.keyOrder[:-2]
            new_order.insert(0, 'first_name')
            new_order.insert(1, 'last_name')
            self.fields.keyOrder = new_order

        def save(self):
            """ 
            Override the save method to save the first and last name to the user
            field.

            """
            # First save the parent form and get the user.
            new_user = super(SignupFormExtra, self).save()

            new_user.first_name = self.cleaned_data['first_name']
            new_user.last_name = self.cleaned_data['last_name']
            new_user.save()

            # Userena expects to get the new user from this form, so return the new
    # user.
    return new_user



models.py
---------

En este archivo se detalla cada una de las clases que se van a utilizar en el sistema HatosGanaderos. Se describen con cada uno de sus atributos respetando las normas de Django.

Clase Configuracion:
    Iniciamos con la clase **Configuracion** que es la encargada de registrar la configuración de la entidad gandera en el sistema HatosGanaderos. A continuación se lo describe con cada uno de sus atributos.

    .. note:: Código de la clase Configuracion:
    
    .. py:function:: class Configuracion(models.Model):
        
        | IDENTIFICACION_CHOICES = (
            ('simple', 'Simple'),
            ('norma_ecuador', 'Norma Ecuador')
            )
        | tipo_identificacion = models.CharField("Tipo de identificacion", 
                                                max_length=15, 
                                                choices = IDENTIFICACION_CHOICES,
                                                default=0
                                                )
        | celo_frecuencia = models.IntegerField("Frecuencia de celo", 
                                                max_length=2
                                                )
        | celo_frecuencia_error = models.IntegerField("Error frecuencia en celo", 
                                                max_length=2
                                                )
        | celo_duracion = models.IntegerField("Duración de celo", 
                                                max_length=2
                                                )
        | celo_duracion_error = models.IntegerField("Error (+/-)", 
                                                max_length=2
                                                )
        | celo_despues_parto = models.IntegerField(u"Celo despues de parto", 
                                                max_length=2
                                                )
        | celo_despues_parto_error = models.IntegerField("Error (+/-)", 
                                                max_length=2
                                                )
        | intentos_verificacion_celo = models.IntegerField("Intentos de Verificación Celo", 
                                                max_length=1
                                                )
        | etapa_ternera = models.IntegerField("Edad máxima de una ternera", 
                                                max_length=2
                                                )
        | etapa_vacona = models.IntegerField("Edad máxima de una vacona", 
                                                max_length=2
                                                )
        | etapa_vientre = models.IntegerField("Edad minima de una vientre", 
                                                max_length=2
                                                )
        | periodo_gestacion = models.IntegerField("Dias de periodo de gestacion", 
                                                max_length=3
                                                )
        | periodo_seco = models.IntegerField("Dias de periodo seco", 
                                                max_length=3
                                                )
        | periodo_lactancia = models.IntegerField("Dias de periodo de lactancia", 
                                                max_length=3
                                                )
        | periodo_vacio = models.IntegerField("Dias de periodo vacio", 
                                                max_length=3
                                                )
        | numero_ordenios = models.IntegerField("Numero de ordeños", 
                                                max_length=1
                                                )

        def __unicode__(self):
            return 'Configuración'


Clase Profile:
    Iniciamos con la clase **Profile** que es la encargada de registrar parámetros adicionales en la cuenta del sistema HatosGanaderos. A continuación se lo describe con cada uno de sus atributos.

    .. note:: Código de la clase Profile:
    
    .. py:function:: class Profile(UserenaLanguageBaseProfile):
        
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

        def __unicode__(self):
            return self.user



Clase Ganaderia:
    Iniciamos con la clase **Ganaderia** que es la encargada de registrar la ganadería en el sistema HatosGanaderos. A continuación se lo describe con cada uno de sus atributos.

    .. note:: Código de la clase Ganaderia:
    
    .. py:function:: class Ganaderia(models.Model):
        
        | nombreEntidad = models.CharField(_(u'Nombre de Ganadería'), max_length=75)
        | direccion = models.CharField(_(u'Direccion de Ganadería'), max_length=50)
        | perfil = models.ManyToManyField(Profile, 
                                            verbose_name=_('perfil'), 
                                            related_name='ganaderia_perfil'
                                            )    
        | configuracion = models.OneToOneField(Configuracion, 
                                            verbose_name=_('configuracion'), 
                                            related_name='ganaderia'
                                            )
        def __unicode__(self):
            return self.nombreEntidad



views.py
--------

El archivo views.py es aquel que se encarga de contener la lógica del sistema. Para ello se cuenta con las siguientes funciones:

    - number_messages
    - home
    - agrega_ganaderia_config


number_messages
    Esta función es la encargada de calcular todos los mensajes que ha realizado el usuario que este logueado en el sistema y se le enviará a través de un template para que sea totalmente visible para el técnico.

    .. note:: Código de number_messages():
    
    .. py:function:: def number_messages(request, username): 

        if username.isdigit():

            user = User.objects.get(id=username)
        else:

            user = User.objects.get(username=username)
        number_messages = Message.objects.filter(Q(receiver_id=user.id), Q(front=True), Q(read_at=False)).count()
        return number_messages

home
    Esta función es la encargada de dirigir al usuario al home de HatosGanaderos.

    .. note:: Código de home():
    
    .. py:function:: def home(request):
        
        user = request.user
        number_message = number_messages(request, user.username )

        return render_to_response('home.html',
                                    {'number_messages': number_message,},
                                    context_instance=RequestContext(request))


agrega_ganaderia_config
    Esta función es la encargada de crear la configuración de la entidad ganadera registrada en HatosGanaderos.

    .. note:: Código de agrega_ganaderia_config():
    
    .. py:function:: def agrega_ganaderia_config(request):
        
        | id_user = request.user
        | number_message = number_messages(request, id_user.username )
        if id_user.is_staff:

            if Ganaderia.objects.filter(perfil=id_user):

                | ganaderia_perfil = Ganaderia.objects.get(perfil =id_user)
                | configuracion_perfil = Configuracion.objects.get(id =ganaderia_perfil.configuracion_id)
                | #verifica si la ganaderia existe
                if ganaderia_perfil:

                    | form = ConfiguracionForm(instance = configuracion_perfil)
                    | form2 = GanaderiaForm(instance = ganaderia_perfil)

                    if request.method == 'POST' and ganaderia_perfil:

                        | form = ConfiguracionForm(request.POST, instance=configuracion_perfil)
                        | form2 = GanaderiaForm(request.POST, instance =ganaderia_perfil)
                        if form.is_valid() and form2.is_valid():

                            | form = form.save(commit=False)
                            | form.etapa_vientre = form.etapa_vacona
                            | form.save()
                            | form2.save()
                            | data = serializers.serialize("json", User.objects.all())
                            ishout_client.emit(
                                    id_user.id,
                                    'alertchannel',
                                    data = {'msg': data,
                                            'number_messages': number_message,}
                                )
                            return redirect(reverse('userena_profile_detail', kwargs={'username': id_user.username}))

            elif request.method == 'POST':

                form = ConfiguracionForm(request.POST)
                form2 = GanaderiaForm(request.POST)#, instance=request.user

                if form.is_valid() and form2.is_valid():
                
                    perf = Profile.objects.get(user_id=id_user.id)
                    
                    form_ganaderia = form2.save(commit=False)
                    form = form.save(commit=False)
                    form.etapa_vientre = form.etapa_vacona
                    form.save()
                    c = Configuracion.objects.get(id=form.id)
                    form_ganaderia.configuracion = c
                    form_ganaderia.save()
                    form_ganaderia.perfil.add(perf.id)

                    data = serializers.serialize("json", User.objects.all())
                    ishout_client.emit(
                            id_user.id,
                            'alertchannel',
                            data = {'msg': data,
                                    'number_messages': number_message,}
                        )
                    return redirect(reverse('userena_profile_detail', kwargs={'username': id_user.username}))
            else:
                form = ConfiguracionForm()
                form2 = GanaderiaForm()
        else:
            return redirect(reverse('userena_profile_detail', kwargs={'username': id_user.username}))
        return render_to_response('agrega_ganaderia_configuracion.html',
                                    {'form': form,
                                     'form2': form2,
                                     'number_messages': number_message},
                                    context_instance=RequestContext(request))