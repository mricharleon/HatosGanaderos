from django.contrib.auth.decorators import login_required
from django.http import Http404
#raise Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from profiles.forms import GanaderiaForm, ConfiguracionForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Q

from profiles.models import Profile, Ganaderia, Configuracion
from messages.models import Message
from notifications.models import Notification
from django.core.exceptions import ObjectDoesNotExist

from drealtime import iShoutClient
ishout_client = iShoutClient()
from django.core import serializers

# recibe '1' o admin
@login_required
def number_messages(request, username):
    if username.isdigit():
        user = User.objects.get(id=username)
    else:
        user = User.objects.get(username=username)
    number_messages = Message.objects.filter(Q(receiver_id=user.id), Q(front=True), Q(read_at=False)).count()
    return number_messages

def home(request):
    user = request.user
    number_message = number_messages(request, user.username )

    return render_to_response('home.html',
            {'number_messages': number_message,},
            context_instance=RequestContext(request))

def agrega_ganaderia_config(request):
    id_user = request.user
    number_message = number_messages(request, id_user.username )
    if id_user.is_staff:
        if Ganaderia.objects.filter(perfil=id_user):
            ganaderia_perfil = Ganaderia.objects.get(perfil=id_user)
            configuracion_perfil = Configuracion.objects.get(id=ganaderia_perfil.configuracion_id)
            # verfica si la ganaderia existe
            if ganaderia_perfil:
                form = ConfiguracionForm(instance=configuracion_perfil)
                form2 = GanaderiaForm(instance=ganaderia_perfil)

                if request.method == 'POST' and ganaderia_perfil:
                    form = ConfiguracionForm(request.POST, instance=configuracion_perfil)
                    form2 = GanaderiaForm(request.POST, instance=ganaderia_perfil)
                    if form.is_valid() and form2.is_valid():
                        form = form.save(commit=False)
                        form.etapa_vaca = form.etapa_vacona_vientre
                        form.save()
                        form2.save()

                        data = serializers.serialize("json", User.objects.all())
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
                form.etapa_vaca = form.etapa_vacona_vientre
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
