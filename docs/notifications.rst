notifications package
=====================

El módulo de notifications es el que se encarga de:
    
    - Listar notificaciones
    - Listar notificaciones de reproducción
    - Listar notificaciones de reproducción realizadas
    - Listar notificaciones de reproducción no realizadas
    - Listar notificaciones de producción
    - Listar notificaciones de producción realizadas
    - Listar notificaciones de producción no realizadas
    - Listar notificaciones de sanidad
    - Listar notificaciones de sanidad realizadas
    - Listar notificaciones de sanidad no realizadas
    - Listar notificaciones de alimentación
    - Listar notificaciones de alimentación realizadas
    - Listar notificaciones de alimentación no realizadas
    - Notificación realizada


Con la finalidad de obtener mayor información a los técnicos de la entidad ganadera. Consta de algunos archivos como: admin.py, models.py y views.py.


admin.py
--------

El archivo admin.py es el encargado del registro de las clases que están en el modelo paraque funcionen en el admin de Django. En este caso se agregó el módelo **Notification** ya que es la que deseamos se encuentre en el admin de django.

    .. py:function:: Código:

        | from django.contrib import admin
        | from notifications.models import Notification
        | admin.site.register(Notification)



models.py
---------

En este archivo se detalla cada una de las clases que se van a utilizar en el sistema HatosGanaderos. Se describen con cada uno de sus atributos respetando las normas de Django.

Clase Notification:
    Iniciamos con la clase **Notification** que es la encargada de registrar la notificación en el sistema HatosGanaderos. A continuación se lo describe con cada uno de sus atributos.

    .. note:: Código de la clase Notification:
    
    .. py:function:: class Notification(models.Model):
        
        | start_date = models.DateField('Fecha inicial')
        | end_date = models.DateField('Fecha final')
        | STATE_CHOICES = (
            (0, 'No realizado'),
            (1, 'Realizado'),
            (2, 'Pendiente'),
            )
        | state = models.PositiveSmallIntegerField('Estado',
                                                choices=STATE_CHOICES
                                                )
        | MODULE_CHOICES = (
            (0, u'Reproducción'),
            (1, u'Alimentación'),
            (2, 'Sanidad'),
            (3, u'Producción'),
            )
        | module = models.PositiveSmallIntegerField(u'Módulo',
                                                choices=MODULE_CHOICES
                                                )
        NAME_CHOICES = (
            (0, 'Ganado en celo'),
            (1, 'Registro del servicio'),
            (2, u'Verificación del celo'),
            (3, 'Fecha de posible parto'),
            (4, 'Cantidad reducida de pajuelas'),
            (5, u'Registro de ordeño'),
            (6, 'Cantidad reducida de la vacuna'),
            (7, 'Cantidad reducida del desparacitador'),
            (8, u'Fecha próxima de vencimiento de la vacuna'),
            (9, u'Fecha próxima de vencimiento del desparacitador'),
            #(10, u'Fecha próxima de aplicación de la vacuna'),
            #(11, u'Fecha próxima de aplicación del desparacitador'),
            (12, 'Cantidad reducida del alimento'),
            (13, u'Fecha próxima de vencimiento del alimento'),
            #(14, u'Fecha próxima de aplicación del alimento')
            )

        ident_cattle = models.ForeignKey(Ganado, related_name='notification_cattle', blank=True, null=True)
        ident_sperm = models.ForeignKey(Insemination, related_name='notification_insemination', blank=True, null=True)
        ident_medicament = models.ForeignKey(Medicament, related_name='notification_medicament', blank=True, null=True)
        ident_food = models.ForeignKey(Food, related_name='notification_food', blank=True, null=True)
        name = models.PositiveSmallIntegerField('Nombre', choices=NAME_CHOICES)
        farm = models.ForeignKey(Ganaderia, related_name='notification_farm')


views.py
--------

El archivo views.py es aquel que se encarga de contener la lógica del sistema. Para ello se cuenta con las siguientes funciones:

    - list_notifications
    - list_notifications_reproduccion
    - list_notifications_reproduccion_realizadas
    - list_notifications_reproduccion_norealizadas
    - list_notifications_produccion
    - list_notifications_produccion_realizadas
    - list_notifications_produccion_norealizadas
    - list_notifications_sanidad
    - list_notifications_sanidad_realizadas
    - list_notifications_sanidad_norealizadas
    - list_notifications_alimentacion
    - list_notifications_alimentacion_realizadas
    - list_notifications_alimentacion_norealizadas
    - realizedNotification


list_notifications
    Esta función es la encargada de calcular todas las notificaciones que han registrado.

    .. note:: Código de list_notifications():
    
    .. py:function:: def list_notifications(request):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        notifications = Notification.objects.filter( Q(state=2) & (Q(ident_cattle__ganaderia=farm) | Q(ident_medicament__farm=farm) | Q(ident_food__farm=farm) | Q(ident_sperm__farm=farm)) ).order_by('end_date')
        number_todas = Notification.objects.filter( Q(state=2) & (Q(ident_cattle__ganaderia=farm) | Q(ident_medicament__farm=farm) | Q(ident_food__farm=farm) | Q(ident_sperm__farm=farm)) ).count()
        number_reproduccion = Notification.objects.filter( state=2, module=0, farm=farm ).count()
        number_produccion = Notification.objects.filter( state=2, module=3, farm=farm ).count()
        number_sanidad = Notification.objects.filter( state=2, module=2, farm=farm ).count()
        number_alimentacion = Notification.objects.filter( state=2, module=1, farm=farm ).count()

        return render_to_response('list_notifications.html',
                    {'notifications': notifications,
                     'number_messages': number_message,
                     'number_todas': number_todas,
                     'number_reproduccion': number_reproduccion,
                     'number_produccion': number_produccion,
                     'number_sanidad': number_sanidad,
                     'number_alimentacion': number_alimentacion},
                    context_instance=RequestContext(request))

list_notifications_reproduccion
    Esta función es la encargada de listar todas las notificaciones pertenecientes al módulo de reproducción con el fin de mantener mayor organización en cada una de las notificaciones de la entidad ganadera.

    .. note:: Código de list_notifications_reproduccion():
    
    .. py:function:: def list_notifications_reproduccion(request):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        notifications = Notification.objects.filter( state=2, module=0, farm=farm ).order_by('end_date')
        number_reproduccion = Notification.objects.filter( state=2, module=0, farm=farm ).count()
        
        number_reproduccion_realizadas = Notification.objects.filter( state=1, module=0, farm=farm ).count()
        number_reproduccion_norealizadas = Notification.objects.filter( state=0, module=0, farm=farm ).count()
        
        return render_to_response('list_notifications_reproduccion.html',
                    {'notifications': notifications,
                     'number_messages': number_message,
                     'number_reproduccion': number_reproduccion,
                     'number_reproduccion_realizadas': number_reproduccion_realizadas,
                     'number_reproduccion_norealizadas': number_reproduccion_norealizadas},
                    context_instance=RequestContext(request))


list_notifications_reproduccion_realizadas
    Esta función es la encargada de listar todas las notificaciones pertenecientes al módulo de reproducción que han sido realizadas con el fin de mantener mayor organización en cada una de las notificaciones de la entidad ganadera.

    .. note:: Código de list_notifications_reproduccion_realizadas():
    
    .. py:function:: def list_notifications_reproduccion_realizadas(request):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        notifications = Notification.objects.filter( state=1, module=0, farm=farm ).order_by('end_date')
        number_reproduccion = Notification.objects.filter( state=2, module=0, farm=farm ).count()
        
        number_reproduccion_realizadas = Notification.objects.filter( state=1, module=0, farm=farm ).count()
        number_reproduccion_norealizadas = Notification.objects.filter( state=0, module=0, farm=farm ).count()
        
        return render_to_response('list_notifications_reproduccion_realizadas.html',
                    {'notifications': notifications,
                     'number_messages': number_message,
                     'number_reproduccion': number_reproduccion,
                     'number_reproduccion_realizadas': number_reproduccion_realizadas,
                     'number_reproduccion_norealizadas': number_reproduccion_norealizadas},
                    context_instance=RequestContext(request))


list_notifications_reproduccion_norealizadas
    Esta función es la encargada de listar todas las notificaciones pertenecientes al módulo de reproducción que no han sido realizadas con el fin de mantener mayor organización en cada una de las notificaciones de la entidad ganadera.

    .. note:: Código de list_notifications_reproduccion_norealizadas():
    
    .. py:function:: def list_notifications_reproduccion_norealizadas(request):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        notifications = Notification.objects.filter( state=0, module=0, farm=farm ).order_by('end_date')
        number_reproduccion = Notification.objects.filter( state=2, module=0, farm=farm ).count()
        
        number_reproduccion_realizadas = Notification.objects.filter( state=1, module=0, farm=farm ).count()
        number_reproduccion_norealizadas = Notification.objects.filter( state=0, module=0, farm=farm ).count()
        
        return render_to_response('list_notifications_reproduccion_norealizadas.html',
                    {'notifications': notifications,
                     'number_messages': number_message,
                     'number_reproduccion': number_reproduccion,
                     'number_reproduccion_realizadas': number_reproduccion_realizadas,
                     'number_reproduccion_norealizadas': number_reproduccion_norealizadas},
                    context_instance=RequestContext(request))



list_notifications_produccion
    Esta función es la encargada de listar todas las notificaciones pertenecientes al módulo de producción con el fin de mantener mayor organización en cada una de las notificaciones de la entidad ganadera.

    .. note:: Código de list_notifications_produccion():
    
    .. py:function:: def list_notifications_produccion(request):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        notifications = Notification.objects.filter( state=2, module=3, farm=farm ).order_by('end_date')
        number_produccion = Notification.objects.filter( state=2, module=3, farm=farm ).count()

        number_produccion_realizadas = Notification.objects.filter( state=1, module=3, farm=farm ).count()
        number_produccion_norealizadas = Notification.objects.filter( state=0, module=3, farm=farm ).count()
        
        return render_to_response('list_notifications_produccion.html',
                    {'notifications': notifications,
                     'number_messages': number_message,
                     'number_produccion': number_produccion,
                     'number_produccion_realizadas': number_produccion_realizadas,
                     'number_produccion_norealizadas': number_produccion_norealizadas},
                    context_instance=RequestContext(request))



list_notifications_produccion_realizadas
    Esta función es la encargada de listar todas las notificaciones pertenecientes al módulo de reproducción que han sido realizadas con el fin de mantener mayor organización en cada una de las notificaciones de la entidad ganadera.

    .. note:: Código de list_notifications_produccion_realizadas():
    
    .. py:function:: def list_notifications_produccion_realizadas(request):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        notifications = Notification.objects.filter( state=1, module=3, farm=farm ).order_by('end_date')
        number_produccion = Notification.objects.filter( state=2, module=3, farm=farm ).count()

        number_produccion_realizadas = Notification.objects.filter( state=1, module=3, farm=farm ).count()
        number_produccion_norealizadas = Notification.objects.filter( state=0, module=3, farm=farm ).count()
        
        return render_to_response('list_notifications_produccion_realizadas.html',
                    {'notifications': notifications,
                     'number_messages': number_message,
                     'number_produccion': number_produccion,
                     'number_produccion_realizadas': number_produccion_realizadas,
                     'number_produccion_norealizadas': number_produccion_norealizadas},
                    context_instance=RequestContext(request))


list_notifications_produccion_norealizadas
    Esta función es la encargada de listar todas las notificaciones pertenecientes al módulo de producción que no han sido realizadas con el fin de mantener mayor organización en cada una de las notificaciones de la entidad ganadera.

    .. note:: Código de list_notifications_produccion_norealizadas():
    
    .. py:function:: def list_notifications_produccion_norealizadas(request):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        notifications = Notification.objects.filter( state=0, module=3, farm=farm ).order_by('end_date')
        number_produccion = Notification.objects.filter( state=2, module=3, farm=farm ).count()

        number_produccion_realizadas = Notification.objects.filter( state=1, module=3, farm=farm ).count()
        number_produccion_norealizadas = Notification.objects.filter( state=0, module=3, farm=farm ).count()
        
        return render_to_response('list_notifications_produccion_norealizadas.html',
                    {'notifications': notifications,
                     'number_messages': number_message,
                     'number_produccion': number_produccion,
                     'number_produccion_realizadas': number_produccion_realizadas,
                     'number_produccion_norealizadas': number_produccion_norealizadas},
                    context_instance=RequestContext(request))



list_notifications_sanidad
    Esta función es la encargada de listar todas las notificaciones pertenecientes al módulo de sanidad con el fin de mantener mayor organización en cada una de las notificaciones de la entidad ganadera.

    .. note:: Código de list_notifications_sanidad():
    
    .. py:function:: def list_notifications_sanidad(request):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        notifications = Notification.objects.filter( state=2, module=2, farm=farm ).order_by('end_date')
        number_sanidad = Notification.objects.filter( state=2, module=2, farm=farm ).count()

        number_sanidad_realizadas = Notification.objects.filter( state=1, module=2, farm=farm ).count()
        number_sanidad_norealizadas = Notification.objects.filter( state=0, module=2, farm=farm ).count()
        
        return render_to_response('list_notifications_sanidad.html',
                    {'notifications': notifications,
                     'number_messages': number_message,
                     'number_sanidad': number_sanidad,
                     'number_sanidad_realizadas': number_sanidad_realizadas,
                     'number_sanidad_norealizadas': number_sanidad_norealizadas},
                    context_instance=RequestContext(request))




list_notifications_sanidad_realizadas
    Esta función es la encargada de listar todas las notificaciones pertenecientes al módulo de sanidad que han sido realizadas con el fin de mantener mayor organización en cada una de las notificaciones de la entidad ganadera.

    .. note:: Código de list_notifications_sanidad_realizadas():
    
    .. py:function:: def list_notifications_sanidad_realizadas(request):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        notifications = Notification.objects.filter( state=1, module=2, farm=farm ).order_by('end_date')
        number_sanidad = Notification.objects.filter( state=2, module=2, farm=farm ).count()

        number_sanidad_realizadas = Notification.objects.filter( state=1, module=2, farm=farm ).count()
        number_sanidad_norealizadas = Notification.objects.filter( state=0, module=2, farm=farm ).count()
        
        return render_to_response('list_notifications_sanidad_realizadas.html',
                    {'notifications': notifications,
                     'number_messages': number_message,
                     'number_sanidad': number_sanidad,
                     'number_sanidad_realizadas': number_sanidad_realizadas,
                     'number_sanidad_norealizadas': number_sanidad_norealizadas},
                    context_instance=RequestContext(request))


list_notifications_sanidad_norealizadas
    Esta función es la encargada de listar todas las notificaciones pertenecientes al módulo de sanidad que no han sido realizadas con el fin de mantener mayor organización en cada una de las notificaciones de la entidad ganadera.

    .. note:: Código de list_notifications_sanidad_norealizadas():
    
    .. py:function:: def list_notifications_sanidad_norealizadas(request):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        notifications = Notification.objects.filter( state=0, module=2, farm=farm ).order_by('end_date')
        number_sanidad = Notification.objects.filter( state=2, module=2, farm=farm ).count()

        number_sanidad_realizadas = Notification.objects.filter( state=1, module=2, farm=farm ).count()
        number_sanidad_norealizadas = Notification.objects.filter( state=0, module=2, farm=farm ).count()
        
        return render_to_response('list_notifications_sanidad_norealizadas.html',
                    {'notifications': notifications,
                     'number_messages': number_message,
                     'number_sanidad': number_sanidad,
                     'number_sanidad_realizadas': number_sanidad_realizadas,
                     'number_sanidad_norealizadas': number_sanidad_norealizadas},
                    context_instance=RequestContext(request))



list_notifications_alimentacion
    Esta función es la encargada de listar todas las notificaciones pertenecientes al módulo de alimentación con el fin de mantener mayor organización en cada una de las notificaciones de la entidad ganadera.

    .. note:: Código de list_notifications_alimentacion():
    
    .. py:function:: def list_notifications_alimentacion(request):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        notifications = Notification.objects.filter( state=2, module=1, farm=farm ).order_by('end_date')
        number_alimentacion = Notification.objects.filter( state=2, module=1, farm=farm ).count()

        number_alimentacion_realizadas = Notification.objects.filter( state=1, module=1, farm=farm ).count()
        number_alimentacion_norealizadas = Notification.objects.filter( state=0, module=1, farm=farm ).count()
        
        return render_to_response('list_notifications_alimentacion.html',
                    {'notifications': notifications,
                     'number_messages': number_message,
                     'number_alimentacion': number_alimentacion,
                     'number_alimentacion_realizadas':number_alimentacion_realizadas,
                     'number_alimentacion_norealizadas': number_alimentacion_norealizadas},
                    context_instance=RequestContext(request))




list_notifications_alimentacion_realizadas
    Esta función es la encargada de listar todas las notificaciones pertenecientes al módulo de alimentación que han sido realizadas con el fin de mantener mayor organización en cada una de las notificaciones de la entidad ganadera.

    .. note:: Código de list_notifications_alimentacion_realizadas():
    
    .. py:function:: def list_notifications_alimentacion_realizadas(request):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        notifications = Notification.objects.filter( state=1, module=1, farm=farm ).order_by('end_date')
        number_alimentacion = Notification.objects.filter( state=2, module=1, farm=farm ).count()

        number_alimentacion_realizadas = Notification.objects.filter( state=1, module=1, farm=farm ).count()
        number_alimentacion_norealizadas = Notification.objects.filter( state=0, module=1, farm=farm ).count()
        
        return render_to_response('list_notifications_alimentacion_realizadas.html',
                    {'notifications': notifications,
                     'number_messages': number_message,
                     'number_alimentacion': number_alimentacion,
                     'number_alimentacion_realizadas':number_alimentacion_realizadas,
                     'number_alimentacion_norealizadas': number_alimentacion_norealizadas},
                    context_instance=RequestContext(request))


list_notifications_alimentacion_norealizadas
    Esta función es la encargada de listar todas las notificaciones pertenecientes al módulo de alimentación que no han sido realizadas con el fin de mantener mayor organización en cada una de las notificaciones de la entidad ganadera.

    .. note:: Código de list_notifications_alimentacion_norealizadas():
    
    .. py:function:: def list_notifications_alimentacion_norealizadas(request):
        
        user = request.user
        number_message = number_messages(request, user.username)
        farm = Ganaderia.objects.get(perfil=user)
        notifications = Notification.objects.filter( state=0, module=1, farm=farm ).order_by('end_date')
        number_alimentacion = Notification.objects.filter( state=2, module=1, farm=farm ).count()

        number_alimentacion_realizadas = Notification.objects.filter( state=1, module=1, farm=farm ).count()
        number_alimentacion_norealizadas = Notification.objects.filter( state=0, module=1, farm=farm ).count()
        
        return render_to_response('list_notifications_alimentacion_norealizadas.html',
                    {'notifications': notifications,
                     'number_messages': number_message,
                     'number_alimentacion': number_alimentacion,
                     'number_alimentacion_realizadas':number_alimentacion_realizadas,
                     'number_alimentacion_norealizadas': number_alimentacion_norealizadas},
                    context_instance=RequestContext(request))


realizedNotification
    Esta función es la encargada de dar por realizada una notificación dentro del sistema HatosGanaderos.

    .. note:: Código de realizedNotification():
    
    .. py:function:: def realizedNotification(request, notification_id):
        
        notification = Notification.objects.get(id=notification_id)
        notification.state = 1
        notification.save()

        msg = 'Notificación REALIZADA con EXITO'
        return render_to_response('list_notifications.html',
                    {'msg': msg,},
                    context_instance=RequestContext(request))