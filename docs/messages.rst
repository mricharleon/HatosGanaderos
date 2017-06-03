messages package
================

El módulo de messages es el que se encarga de:
    
    - Listar mensajes
    - Listar mensajes leídos y no leídos
    - Detallar cada mensaje
    - Crear mensajes

Con la finalidad de obtener mayor comunicación entre los técnicos de la entidad ganadera. Consta de algunos archivos como: admin.py, forms.py, models.py y views.py.


admin.py
--------

El archivo admin.py es el encargado del registro de las clases que están en el modelo paraque funcionen en el admin de Django. En este caso se agregó el módelo **Message** ya que es la que deseamos se encuentre en el admin de django.

    .. py:function:: Código de admin.py:
    
        | from django.contrib import admin
        | from messages.models import Message
        | admin.site.register(Message)



forms.py
--------

Este archivo es el encargado de crear los parámetros correctos que serán utilizados en el formulario del **Mensaje** se realizan las debidas importaciones además de la configuración de los parámetros que deben o no ir con sus respectivos atributos como clases, id, etc.

Formulario de nuevo mensaje:
    El módulo HatosGanaderos presenta la funcionalidad de tener un módulo de mensajería entre técnicos, para lo cuál se inicia creando en modelo del formulario en este caso se hace uso de la clase **Message** con sus respectivos atributos, además se agregan widgets a cada uno de estos atributos que serán utiles para poder realizar un html más vistoso, amigable y funcional.

    .. note:: Código de MessageForm:
    
    .. py:function:: class MessageForm(forms.ModelForm):
        
        class Meta:

            | model = Message
            | exclude = ['sender',
                       'sent_at',
                       'read_at',
                       'front']
            | widgets ={
                        'content': forms.Textarea(attrs={
                                      'rows': '5',
                                      'placeholder': 'Tu mensaje aquí'
                          }),
            }


Formulario de respuesta al mensaje:
    El módulo HatosGanaderos presenta la funcionalidad de tener un módulo de mensajería entre técnicos en este caso se crea el formulario para dar respuesta al mensaje recibido, para lo cuál se inicia creando en modelo del formulario en este caso se hace uso de la clase **Message** con sus respectivos atributos, además se agregan widgets a cada uno de estos atributos que serán utiles para poder realizar un html más vistoso, amigable y funcional.

    .. note:: Código de MessageResponseForm:
    
    .. py:function:: class MessageResponseForm(forms.ModelForm):

        class Meta:

            | model = Message
            | exclude = ['sender',
                       'sent_at',
                       'read_at',
                       'front',
                       'receiver']
            | widgets ={
                        'content': forms.Textarea(attrs={
                       'rows': '3'
                          }),
            }



models.py
---------

En este archivo se detalla cada una de las clases que se van a utilizar en el sistema HatosGanaderos. Se describen con cada uno de sus atributos respetando las normas de Django.

Clase Message:
    Iniciamos con la clase **Message** que es la encargada de registrar el mensaje en el sistema HatosGanaderos. A continuación se lo describe con cada uno de sus atributos.

    .. note:: Código de la clase Message:
    
    .. py:function:: class Message(models.Model):
        
        sender = models.ForeignKey(Profile, related_name='sender_')
        receiver = models.ForeignKey(Profile, related_name='receiver_', verbose_name=u'Receptor')
        content = models.TextField('Tu mensaje', max_length=280)
        sent_at = models.DateTimeField('Enviado a')
        read_at = models.BooleanField('Leído')
        front = models.BooleanField('Frontal')

        def __str__(self):

            return 'De: %s, Para: %s, Msj: %s - Estado: %s' % (self.sender.user.username, 
                self.receiver.user.username, 
                self.content,
                self.read_at)



views.py
--------

El archivo views.py es aquel que se encarga de contener la lógica del sistema. Para ello se cuenta con las siguientes funciones:

    - messages_list
    - messages_list_read
    - messages_list_no_read
    - messages_details
    - new_message


messages_list
    Esta función es la encargada de calcular todos los mensajes que ha realizado el usuario que este logueado en el sistema y se le enviará a través de un template para que sea totalmente visible para el técnico.

    .. note:: Código de messages_list():
    
    .. py:function::def messages_list(request):
        
        user_receiver = request.user
        try:
            ganaderia = Ganaderia.objects.get(perfil=user_receiver)
        except ObjectDoesNotExist:
            return redirect(reverse('agrega_ganaderia_config'))
        
        number_message = number_messages(request, user_receiver.username)

        messages = []
        mc = Message.objects.all().order_by('-sent_at')
        for i in mc:
            if (i.sender_id == user_receiver.id) | (i.receiver_id == user_receiver.id) and (i.front == True):
                messages.append(i)
        
        return render_to_response('messages_list.html',
                                    {'messages': messages,
                                     'user_receiver': user_receiver,
                                     'number_messages': number_message,
                                    },
                                    context_instance=RequestContext(request))


messages_list_read
    Esta función es la encargada de calcular todos los mensajes leídos que ha realizado el usuario que este logueado en el sistema y se le enviará a través de un template para que sea totalmente visible para el técnico.

    .. note:: Código de messages_list_read():
    
    .. py:function:: def messages_list_read(request):
        
        user_receiver = request.user
        number_message = number_messages(request, user_receiver.username)
        messages = []
        mc = Message.objects.all().order_by('-sent_at')
        for i in mc:
            if (i.sender_id == user_receiver.id) | (i.receiver_id == user_receiver.id) and (i.front == True) and (i.read_at == True):
                messages.append(i)
        
        return render_to_response('messages_list_read.html',
                                    {'messages': messages,
                                     'user_receiver': user_receiver,
                                     'number_messages': number_message,
                                    },
                                    context_instance=RequestContext(request))

messages_list_no_read
    Esta función es la encargada de calcular todos los mensajes no leídos que ha realizado el usuario que este logueado en el sistema y se le enviará a través de un template para que sea totalmente visible para el técnico.

    .. note:: Código de messages_list_no_read():
    
    .. py:function:: def messages_list_no_read(request):
        
        user_receiver = request.user
        number_message = number_messages(request, user_receiver.username)
        messages = []
        mc = Message.objects.all().order_by('-sent_at')
        
        for i in mc:
            if (i.sender_id == user_receiver.id) | (i.receiver_id == user_receiver.id) and (i.front == True) and (i.read_at == False):
                messages.append(i)
        
        return render_to_response('messages_list_no_read.html',
                                    {'messages': messages,
                                     'user_receiver': user_receiver,
                                     'number_messages': number_message,
                                    },
                                    context_instance=RequestContext(request))


messages_details
    Esta función es la encargada de permitir al técnico visualizar una comunicación con detalle entre el emisor y receptor.

    .. note:: Código de messages_details():
    
    .. py:function:: def messages_details(request, user_id, user_send_id, user_receiver_id):

        user = User.objects.get(id=user_id)
        user_send = User.objects.get(id=user_send_id)
        user_receiver = User.objects.get(id=user_receiver_id)

        profile = Profile.objects.get(user=user)
        profile_sender = Profile.objects.get(user=user_send)
        profile_receiver = Profile.objects.get(user=user_receiver)


        messages = []
        msgs = Message.objects.all().order_by('-sent_at')
        if request.method == 'POST':
            form_message = MessageResponseForm(request.POST)
            date_now = datetime.datetime.today()
            if form_message.is_valid():
                form_message = form_message.save(commit=False)
                form_message.sender = profile
                if user_id == user_send_id:
                    form_message.receiver = profile_receiver
                    form_message.read_at = False
                elif user_id == user_receiver_id:
                    form_message.receiver = profile_sender
                    form_message.read_at = False
                form_message.sent_at = date_now
                for i in msgs:
                    if ((i.receiver_id == user_receiver.id) & (i.sender_id == user_send.id)) | ((i.sender_id == user_receiver.id) & (i.receiver_id == user_send.id)):
                        i.front=False
                        i.save()
                form_message.front = True
                form_message.save()

                number_message = number_messages(request, str(form_message.receiver_id))
                data = serializers.serialize("json", User.objects.all())
                
                ishout_client.emit(
                        form_message.receiver_id,
                        'alertchannel',
                        data = {'msg': data,
                                'number_messages': number_message,}
                    )
                
                return HttpResponseRedirect(reverse('messages_list'))
                #return redirect(reverse('messages_list', kwargs={'username': user.username}))
        elif request.method == 'GET':
            for i in msgs:
                if ((i.receiver_id == user_receiver.id) & (i.sender_id == user_send.id)) | ((i.sender_id == user_receiver.id) & (i.receiver_id == user_send.id)):
                    if user_id != user_send_id:
                        i.read_at=True
                        i.save()
                    messages.append(i)
            form_message = MessageResponseForm()

            number_message = number_messages(request, str(user.id))
            data = serializers.serialize("json", User.objects.all())
            
            ishout_client.emit(
                    user_send.id,
                    'alertchannel',
                    data = {'msg': data,
                            'number_messages': number_message}
                )

        return render_to_response('messages_details.html',
                                    {'messages': messages,
                                     'user_receiver': user_receiver,
                                     'user_sender': user_send,
                                     'form':form_message,
                                    },
                                    context_instance=RequestContext(request))


new_message
    Esta función es la encargada de permitir al técnico crear un nuevo mensaje y poderlo enviar a algún técnico registrado en la entidad ganadera.

    .. note:: Código de new_message():
    
    .. py:function:: def new_message(request):
        
        user = request.user
        profile = Profile.objects.get(user=user)
        try:
            ganaderia = Ganaderia.objects.get(perfil=user)
        except ObjectDoesNotExist:
            return redirect(reverse('agrega_ganaderia_config'))
        
        number_message = Message.objects.filter(Q(receiver_id=user.id), Q(front=True), Q(read_at=False)).count()
        msg_complete = Message.objects.all().order_by('sent_at')

        date_now = datetime.datetime.today()
        if request.method == 'POST':
            form_message = MessageForm(request.POST)
            if form_message.is_valid():
                form_message = form_message.save(commit=False)
                form_message.sender = profile
                form_message.sent_at = date_now
                form_message.read_at = False
                for i in msg_complete:
                    if ((i.receiver_id == form_message.receiver_id) & (i.sender_id == form_message.sender_id)) | ((i.sender_id == form_message.receiver_id) & (i.receiver_id == form_message.sender_id)):
                        i.front=False
                        i.save()
                form_message.front = True
                form_message.save()

                number_message = number_messages(request, str(form_message.receiver_id))
                data = serializers.serialize("json", User.objects.all())
                
                ishout_client.emit(
                        form_message.receiver_id,
                        'alertchannel',
                        data = {'msg': data,
                                'number_messages': number_message,}
                    )
                
                return HttpResponseRedirect(reverse('messages_list'))
                #return redirect(reverse('messages_list'))

        else:
            form_message = MessageForm()
            profile_model = get_profile_model()
            ganaderia = Ganaderia.objects.get(perfil=user)
            receivers = profile_model.objects.get_visible_profiles(user).select_related().exclude(id=user.id).filter(ganaderia_perfil=ganaderia)
        return render_to_response('new_message.html',
                                    {'form': form_message,
                                    'number_messages': number_message,
                                    'receivers': receivers,
                                    },
                                    context_instance=RequestContext(request))