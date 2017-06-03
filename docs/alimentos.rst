alimentos package
=================

El módulo de alimentación es el que se encarga de:
    
    - Registro de alimentos
    - Edición del alimento y
    - Asignar alimento a uno o varios ganados

Con la finalidad de obtener mayor cuidado en el ganado en cuanto a alimentación se refiere. Consta de algunos archivos como: admin.py, forms.py, models.py y views.py.


admin.py
--------

El archivo admin.py es el encargado del registro de las clases que están en el modelo paraque funcionen en el admin de Django. En este caso se agregó **Food** ya que es la única que queremos que se encuentre en el admin de django.

.. py:function:: Código:

    | from django.contrib import admin
    | from alimentos.models import Food
    | admin.site.register(Food)    




forms.py
--------

Este archivo es el encargado de crear los parámetros correctos que serán utilizados en el formulario del **Alimento** se realizan las debidas importaciones además de la configuración de los parámetros que deben o no ir con sus respectivos atributos como clases, id, etc.

.. py:function:: Código:

    | # -*- encoding: utf-8 -*-
    | from django import forms
    | from django.utils.translation import ugettext_lazy as _
    | from alimentos.models import Food
    .. py:class:: class alimentoForm(forms.ModelForm):
        
        .. py:class:: class Meta:
            
            | model = Food
            | exclude = ['farm', 'cattle', 'status', 'is_active']
            | widgets = {
                    'name': forms.TextInput(attrs={
                                    'placeholder': 'Nombre del alimento'
                    }),
                    'expiration_date':forms.DateInput(attrs={
                                    'class': 'datetimepicker2',
                                    'placeholder': 'Fecha de expiración'}),
                    'amount': forms.TextInput(attrs={
                                    'placeholder': 'Cantidad de alimento'
                    }),
                    'consumer_amount': forms.TextInput(attrs={
                                    'placeholder': 'Cantidad de consumo'
                    }),
                    'interval': forms.TextInput(attrs={
                                    'placeholder': 'Intervalo '
                    }),
                    'observations': forms.Textarea(attrs={
                                    'placeholder': 'Observaciones'
                    }),
            | }

models.py
---------

En este archivo se detalla cada una de las clases que se van a utilizar en el sistema HatosGanaderos. Se describen con cada uno de sus atributos respetando las normas de Django.

Clase Food:
    Iniciamos con la clase **Food** que es la que va registrar cada uno de los alimentos que se registren en el sistema HatosGanaderos. A continuación se la describe con cada uno de sus atributos.

    .. py:function:: Código de la clase Food:
    
        | # -*- encoding: utf-8 -*-
        | from django.db import models
        | from profiles.models import Ganaderia
        | from ganados.models import Ganado

        .. py:class:: class Food(models.Model):
            
            | name = models.CharField('Nombre del alimento', max_length=100)
            | expiration_date = models.DateField(u'Fecha de Expiración')
            | UNIT_CHOICES = (
                (0, 'ml'),
                (1, 'gr'),
                (2, 'lbs'),
                (3, 'Kg'),
                (4, 'Paquetes'),
                )
            | unit = models.PositiveSmallIntegerField('Unidad',
                                                    choices=UNIT_CHOICES,
                                                    default=0)
            | amount = models.FloatField('Cantidad de alimento')
            | SEX_CHOICES = (
                (0, 'Hembra'),
                (1, 'Macho'),  
                (2, 'Hembra y Macho')      
                )
            | sex = models.PositiveSmallIntegerField('Sexo a aplicar', 
                                                    choices=SEX_CHOICES,
                                                    default=0)
            | farm = models.ForeignKey(Ganaderia, related_name='farm_foods')
            | PHASE_CHOICES = (
                (0, 'Ternera(o)'),
                (1, 'Vacona'),  
                (2, 'Vientre')  ,
                (3, 'Ternera(o) y Vacona'),
                (4, 'Ternera(o) y Vientre'),
                (5, 'Vacona y Vientre'),
                (6, 'Todas')
                )
            | phase = models.PositiveSmallIntegerField('Etapa', 
                                                    choices=PHASE_CHOICES,
                                                    default=0)
            | consumer_amount = models.FloatField(u'cantidad de consumo')
            | interval = models.IntegerField('Intervalo de tiempo')
            | TIME_INTERVAL_CHOICES = (
                (0, u'Intervalo en días'),
                (1, 'Intervalo en meses'),  
                (2, u'Intervalo en años')      
                )
            | time_interval = models.PositiveSmallIntegerField('Unidad de tiempo',
                                    choices=TIME_INTERVAL_CHOICES,
                                    default=0)
            | ADMINISTRATION_ROUTE_CHOICES = (
                (0, 'Oral'),
                (1, 'Granulada')
                )
            | administration_route = models.PositiveSmallIntegerField(u'Vía de administración',
                                    choices=ADMINISTRATION_ROUTE_CHOICES,
                                    default=0)
            | observations = models.TextField('Observaciones')
            | is_active = models.BooleanField('Activo')

Clase ApplicationFood:
    Ahora necesitamos registrar cuando se asigne un alimento a un ganado para ello se hace uso de una nueva clase denominada **ApplicationFood** la cúal registra cada una de las asignaciones.

    .. note:: Código de la clase ApplicationFood:
    
    .. py:class:: class ApplicationFood(models.Model):
        
        | date = models.DateField('Fecha de aplicación')
        | cattle = models.ManyToManyField(Ganado, blank=True, null=True, related_name='application_food_food', verbose_name=u'Ganados')
        | food = models.ForeignKey(Food, related_name='application_food_cattle')
        | STATUS_CHOICES = (
            (0, 'Realizado'),
            (1, 'Cancelado')
            )
        | status = models.PositiveSmallIntegerField('Estado',
                                choices=STATUS_CHOICES,
                                )


views.py
--------

El archivo views.py es aquel que se encarga de contener la lógica del sistema. Para ello se cuenta con las siguientes funciones:

    - add_food
    - list_food
    - edit_food
    - asigna_alimento


add_food
    Esta función recibe el usuario que esta logueado, consulta si pertenece a una ganaderia dicho usuario.

    Se comprueba también a través de la función **number_messages** si existen mensajes para dicho usuario.

    Finalmente se valida si la información que viene del formulario es la correcta si lo és procede a guardarla.

    .. note:: Código de number_messages():

    .. py:function:: def number_messages(request, username): 

        if username.isdigit():
            
            user = User.objects.get(id=username)
        else:
            
            user = User.objects.get(username=username)
        | number_messages = Message.objects.filter(Q(receiver_id=user.id), Q(front=True), Q(read_at=False)).count()
        | return number_messages

    .. note:: Código de add_food():

    .. py:function:: def add_food(request):
        
        | user = request.user
        | number_message = number_messages(request, user.username)
        try:
            
            ganaderia = Ganaderia.objects.get(perfil=user)
        except ObjectDoesNotExist:
            
            return redirect(reverse('agrega_ganaderia_config'))

        if request.method == 'POST':
            
            | formAlimento = alimentoForm(request.POST)
            if formAlimento.is_valid():
                
                | formAliment = formAlimento.save(commit=False)
                | formAliment.farm = ganaderia
                | formAliment.is_active = True
                | formAliment.save()
                | return redirect(reverse('list_food'))
        elif request.method == 'GET':

            formAlimento = alimentoForm()
        | return render_to_response('add_food.html',
            {'formAlimento': formAlimento,
             'number_messages': number_message},
            context_instance=RequestContext(request))


list_food
    Esta función recibe el usuario que esta logueado, consulta a que ganadería pertenece y extrae todos los alimentos que pertenecen a dicha ganadería.

    .. note:: Código de list_food():

    .. py:function:: def list_food(request):
        
        | username = request.user.username
        | number_message = number_messages(request, username)
        | id_user = User.objects.filter(username=username)
        | ganaderia = Ganaderia.objects.get(perfil=id_user)
        if request.method == 'GET':
            
            alimentos = Food.objects.all().filter(farm=ganaderia)
        | return render_to_response('list_food.html',
            {'alimentos': alimentos,
             'number_messages': number_message},
            context_instance=RequestContext(request))


edit_food
    Esta función recibe el usuario que esta logueado, consulta si pertenece a una ganaderia dicho usuario y valida si la información que viene del formulario es la correcta si lo és procede a guardarla.

    .. note:: Código de edit_food():

    .. py:function:: def edit_food(request, alimento_id):
        
        | user = request.user
        | number_message = number_messages(request, user.username)
        | ganaderia = Ganaderia.objects.get(perfil=user)
        | alimento = Food.objects.get(id=alimento_id)
        if request.method == 'POST':

            | formAlimento = alimentoForm(request.POST, instance=alimento)
            if formAlimento.is_valid():
                
                | formAlimento = formAlimento.save(commit=False)
                | formAlimento.ganaderia = ganaderia
                | formAlimento.farm = ganaderia
                | formAlimento.is_active = True
                | formAlimento.save()
                | return redirect(reverse('list_food'))
        else:

            formAlimento = alimentoForm(instance=alimento)
        | return render_to_response('edit_food.html',
            {'formAlimento': formAlimento,
             'alimento_id': alimento_id,
              'number_messages': number_message},
            context_instance=RequestContext(request))   


asigna_alimento
    Esta función recibe el usuario que esta logueado y el id del alimento a asignar, comprueba la existencia de mensajes para el usuario y redirecciona a un template denominado **asigna_alimento.html**.

    .. note:: Código de asigna_alimento()

    .. py:function:: def asigna_alimento(request, alimento_id):

        | user = request.user
        | number_message = number_messages(request, user.username)
        | return render_to_response('asigna_alimento.html',
            {'id_food': alimento_id,
             'number_messages': number_message},
            context_instance=RequestContext(request))

    Luego que llega a este template se verifica que en el mismo se tiene una llamada por **ajax** para poder buscar y seleccionar los ganados. Esta función se encuentra en la app denominada **webServices** en el archivo views.py

    .. note:: Código de ajaxAssignCattleFood:

    .. py:function:: def ajaxAssignCattleFood_view(request):
        
        | search = request.GET['search']
        | listCattle = str(request.GET['listCattle'])
        | user = request.user
        | ganaderia = Ganaderia.objects.get(perfil=user)
        if ganaderia.configuracion.tipo_identificacion == 'simple':

            ganados = Ganado.objects.filter(
                    Q(ganaderia=ganaderia, down_cattle=None) &
                    (
                        Q(nacimiento__icontains=search) |
                        Q(identificacion_simple__nombre__icontains=search) |
                        Q(identificacion_simple__rp__icontains=search)
                    )
                                            )
            | #serializando
            | data = '['
            for g in ganados:
                
                if data == '[':
                    
                    data += '{"pk": ' + str(g.id) + ', '
                else:
                    
                    data += ',{"pk": ' + str(g.id) + ', '
                data += '"fields": {'
                data += '"rp": "'+ str(g.identificacion_simple.rp) +'"'
                data += ', "imagen": "'+ str(g.imagen) +'"'
                data += ', "nombre": "'+ g.identificacion_simple.nombre +'"'
                data += ', "edad_anios": '+ str(g.edad_anios )
                data += ', "edad_meses": '+ str(g.edad_meses )
                data += ', "edad_dias": '+ str(g.edad_dias )

                data += '}}'
            data += ']'

        else:
            ganados = Ganado.objects.filter(
                    Q(ganaderia=ganaderia) &
                    (
                        Q(nacimiento__icontains= search) |
                        Q(identificacion_ecuador__nombre__icontains =search) |
                        Q(identificacion_ecuador__rp__icontains =search)
                    )
                                            )
            | #serializando
            | data = '['
            for g in ganados:
                if data == '[':

                    data += '{"pk": ' + str(g.id) + ', '
                else:
                    
                    data += ',{"pk": ' + str(g.id) + ', '
                data += '"fields": {'
                data += '"rp": "'+ str(g.identificacion_ecuador.rp) +'"'
                data += ', "imagen": "'+ str(g.imagen) +'"'
                data += ', "nombre": "'+ g.identificacion_ecuador.nombre +'"'
                data += ', "edad_anios": '+ str(g.edad_anios )
                data += ', "edad_meses": '+ str(g.edad_meses )
                data += ', "edad_dias": '+ str(g.edad_dias )

                data += '}}'
            data += ']'

        return HttpResponse(data, mimetype='application/json')

    Luego que se hayan seleccionado todos los ganados próximos a la asignación del alimento se procede a guardarlo en la base de datos para ello se hace uso de otra función denominada **ajaxAssignCattleFoodFinal**.

    .. note:: Código de ajaxAssignCattleFoodFinal:

    .. py:function:: def ajaxAssignCattleFoodFinal(request):

        | id_food = request.GET['id_food']
        | listCattle = str(request.GET['listCattle'])
        | user = request.user
        | ganaderia = Ganaderia.objects.get(perfil=user)
        | food = Food.objects.get(id=id_food)
        | listCattle = listCattle.replace('[','')
        | listCattle = listCattle.replace(']','')
        | listCattle = listCattle.replace(',','')
        | listCattle = list(listCattle)
        | date_now = datetime.date.today()
        if len(listCattle) > 0:

            if (len(listCattle) * food.consumer_amount) <= food.amount:

                | application_food = ApplicationFood()
                | application_food.date = date_now
                | application_food.status = 0
                | application_food.food = food
                | application_food.save()
                for c in range(len(listCattle)):

                    application_food.cattle.add(listCattle[c])
                | food.amount=food.amount - (len(listCattle)*food.consumer_amount)
                | food.save()
                | data = '[ { "state": 0} ]'
            else:
                if food.unit == 0:

                    unit_display = 'ml'
                elif food.unit == 1:

                    unit_display='gr'
                elif food.unit==2:

                    unit_display='lbs'
                elif food.unit==3:

                    unit_display='kg'
                elif food.unit==4:

                    unit_display='paquetes'
                | data = '[ {"state": 1, "amount":'+str(food.amount)+', "amount_now": '+str(len(listCattle)*food.consumer_amount)+', "unit": "'+unit_display+'" , "consumer_amount": "'+str(food.consumer_amount)+'"}]'
        else:
            data = '[ { "state": 2} ]'

        return HttpResponse(data, mimetype='application/json')