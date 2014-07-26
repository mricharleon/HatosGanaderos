from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from userena.utils import get_user_model
from django.shortcuts import render_to_response
from django.template import RequestContext
from profiles.models import Ganaderia, Configuracion
from ganados.models import *
from ganados.forms import *
from alimentos.forms import *
from alimentos.models import *
from django.contrib.auth.models import User

from datetime import date
import datetime, dateutil
import calendar

from dateutil.relativedelta import *


@login_required
def agrega_alimento(request, username):
	id_user = User.objects.filter(username=username)
	ganaderia = Ganaderia.objects.get(perfil_id=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)

	if request.method == 'POST':
		formAlimento = alimentoForm(request.POST)
		if formAlimento.is_valid():
			formAlimento = formAlimento.save(commit=False)
			formAlimento.ganaderia = ganaderia
			formAlimento.save()
			return redirect(reverse('lista_alimento', kwargs={'username': username}))
		
	else:
		formAlimento = alimentoForm()
	return render_to_response('agrega_alimento.html',
		{'formAlimento': formAlimento
		},
		context_instance=RequestContext(request))

@login_required
def lista_alimento(request, username):
	id_user = User.objects.filter(username=username)
	ganaderia = Ganaderia.objects.get(perfil_id=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)

	if request.method == 'GET':
		alimentos = ganaderia.alimentos.all()

	return render_to_response('lista_alimento.html',
		{'alimentos': alimentos},
		context_instance=RequestContext(request))

@login_required
def edita_alimento(request, username, alimento_id):
	id_user = User.objects.filter(username=username)
	ganaderia = Ganaderia.objects.get(perfil_id=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)

	alimento = ganaderia.alimentos.get(id=alimento_id)

	if request.method == 'POST':
		formAlimento = alimentoForm(request.POST, instance=alimento)
		if formAlimento.is_valid():
			formAlimento = formAlimento.save(commit=False)
			formAlimento.ganaderia = ganaderia
			formAlimento.save()
			return redirect(reverse('lista_alimento', kwargs={'username': username}))
	else:
		formAlimento = alimentoForm(instance=alimento)

	return render_to_response('edita_alimento.html',
		{'formAlimento': formAlimento,
		 'alimento_id': alimento_id},
		context_instance=RequestContext(request))	

@login_required
def asigna_alimento(request, username, alimento_id, ganado_id):
	id_user = User.objects.filter(username=username)
	ganaderia = Ganaderia.objects.get(perfil_id=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)

	ganados = ganaderia.ganados.all()

	if ganado_id != '0':
		ganado = ganaderia.ganados.get(id=ganado_id)
		alimento = ganaderia.alimentos.get(id=alimento_id)
		
	else:
		alimento = ''
		ganado = '0'

	
	return render_to_response('asigna_alimento.html',
		{'ganados': ganados,
		 'alimento_id': alimento_id,
		 'ganado': ganado,
		 'alimento': alimento},
		context_instance=RequestContext(request))
