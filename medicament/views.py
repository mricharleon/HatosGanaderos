# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from userena.utils import get_user_model
from django.shortcuts import render_to_response
from django.template import RequestContext
from profiles.models import Ganaderia
from ganados.models import *
from ganados.forms import *
from medicament.forms import *
from medicament.models import *
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def add_wormer(request):
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)
	
	if request.method == 'POST':
		form_worme = wormerForm(request.POST)
		if form_worme.is_valid():
			form_wormer = form_worme.save(commit=False)
			form_wormer.farm = ganaderia
			form_wormer.is_vaccine = False
			form_wormer.is_wormer = True
			form_wormer.status = 0
			form_wormer.save()
			#a = (1,2)
			#form_wormer.cattle.add(1)
			#form_wormer.cattle.add(2)
			#form_worme.save_m2m()
			return redirect(reverse('list_wormer'))

	elif request.method == 'GET':
		form_wormer = wormerForm()

	return render_to_response('add_wormer.html',
								{'form_wormer': form_wormer,},
								context_instance=RequestContext(request)
		)

@login_required
def list_wormer(request):
	user = request.user

	medicaments = Medicament.objects.filter(is_wormer=True, farm_id=user)
	
	return render_to_response('list_wormer.html',
								{'medicaments': medicaments},
								context_instance=RequestContext(request)
							)

@login_required
def edit_wormer(request, id_medicament):
	medicament = Medicament.objects.get(id=id_medicament)
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
								{'form_wormer': form_medicament},
								context_instance=RequestContext(request)
							)

# vaccine
@login_required
def add_vaccine(request):
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)
	if request.method == 'POST':
		form_vaccine = vaccineForm(request.POST)
		if form_vaccine.is_valid():
			form_vaccine = form_vaccine.save(commit=False)
			form_vaccine.farm = ganaderia
			form_vaccine.is_vaccine = True
			form_vaccine.is_wormer = False
			form_vaccine.status = 0
			form_vaccine.save()
			
			return redirect(reverse('list_vaccine'))

	elif request.method == 'GET':
		form_vaccine = vaccineForm()
	return render_to_response('add_vaccine.html',
								{'form_vaccine': form_vaccine},
								context_instance=RequestContext(request)
		)

@login_required
def list_vaccine(request):
	user = request.user
	medicaments = Medicament.objects.filter(is_vaccine=True, farm_id=user)

	return render_to_response('list_vaccine.html',
								{'vaccines': medicaments},
								context_instance=RequestContext(request)
							)

@login_required
def edit_vaccine(request, id_medicament):
	medicament = Medicament.objects.get(id=id_medicament)
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
								{'form_vaccine': form_medicament},
								context_instance=RequestContext(request)
							)