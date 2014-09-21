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
def add_food(request):
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)

	if request.method == 'POST':
		formAlimento = alimentoForm(request.POST)
		if formAlimento.is_valid():
			formAliment = formAlimento.save(commit=False)
			formAliment.farm = ganaderia
			formAliment.is_active = True
			formAliment.save()
			return redirect(reverse('list_food'))
		
	elif request.method == 'GET':
		formAlimento = alimentoForm()

	return render_to_response('add_food.html',
		{'formAlimento': formAlimento},
		context_instance=RequestContext(request))

@login_required
def list_food(request):
	username = request.user.username
	id_user = User.objects.filter(username=username)
	ganaderia = Ganaderia.objects.get(perfil=id_user)

	if request.method == 'GET':
		alimentos = Food.objects.all().filter(farm=ganaderia)

	return render_to_response('list_food.html',
		{'alimentos': alimentos},
		context_instance=RequestContext(request))

@login_required
def edit_food(request, alimento_id):
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)

	alimento = Food.objects.get(id=alimento_id)

	if request.method == 'POST':
		formAlimento = alimentoForm(request.POST, instance=alimento)
		if formAlimento.is_valid():
			formAlimento = formAlimento.save(commit=False)
			formAlimento.ganaderia = ganaderia
			formAlimento.farm = ganaderia
			formAlimento.is_active = True
			formAlimento.save()
			return redirect(reverse('list_food'))
	else:
		formAlimento = alimentoForm(instance=alimento)

	return render_to_response('edit_food.html',
		{'formAlimento': formAlimento,
		 'alimento_id': alimento_id},
		context_instance=RequestContext(request))	

@login_required
def asigna_alimento(request, alimento_id):
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)
	
	return render_to_response('asigna_alimento.html',
		{'id_food': alimento_id,
		},
		context_instance=RequestContext(request))


	