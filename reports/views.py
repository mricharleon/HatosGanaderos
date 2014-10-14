# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


from profiles.views import number_messages
from ganados.models import Ganaderia, Ganado, Gestacion, ProblemaGestacion, Ordenio
from profiles.models import Configuracion
from alimentos.models import ApplicationFood
from medicament.models import ApplicationMedicament, Medicament

def docs(request):
	return render_to_response('_build/html/index.html',
		context_instance=RequestContext(request))

def list_reports(request):
	user = request.user
	number_message = number_messages(request, user.username)
	return render_to_response('list_reports.html',
		{'number_messages': number_message},
		context_instance=RequestContext(request))

def view_report_female(request, id_cattle):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	configuration = Configuracion.objects.get(id=farm.configuracion.id)

	cattle = Ganado.objects.get(id=id_cattle, ganaderia=farm)
	problem_gestacion = ProblemaGestacion.objects.filter(id=cattle.id)

	total_births = Gestacion.objects.filter(
			Q(ganado=cattle) &
			~Q(problema=problem_gestacion)
		).count()
	total_problems_births =ProblemaGestacion.objects.filter(id=cattle.id).count()
	if configuration.tipo_identificacion=='simple':
		try:
			cattle_mother = Ganado.objects.get(identificacion_simple__rp=cattle.identificacion_simple.rp_madre)
		except ObjectDoesNotExist:
			cattle_mother = 'Desconocida'

		try:
			cattle_father = Ganado.objects.get(identificacion_simple__rp=cattle.identificacion_simple.rp_padre)
		except ObjectDoesNotExist:
			cattle_father = 'Desconocido'
		
	else:
		try:
			cattle_mother = Ganado.objects.get(identificacion_ecuador__rp=cattle.identificacion_ecuador.rp_madre)
		except ObjectDoesNotExist:
			cattle_mother = 'Desconocida'

		try:
			cattle_father = Ganado.objects.get(identificacion_ecuador__rp=cattle.identificacion_ecuador.rp_padre)
		except ObjectDoesNotExist:
			cattle_father = 'Desconocido'

	ordenio = Ordenio.objects.filter(ganado=cattle)
	count_milk = 0
	count = 0
	for o in ordenio:
		if o.numero_ordenio == configuration.numero_ordenios:
			count_milk += o.total
			count += 1
	if count_milk > 0:
		count_milk = count_milk / count

	application_food = ApplicationFood.objects.filter(cattle=cattle)
	food = []
	for f in application_food:
		if f.food.name not in food:
			food.append(f.food.name)
			food.append('('+str(f.food.consumer_amount)+' '+f.food.get_unit_display()+') ')
		else:
			index = food.index(f.food.name)+1
			food[index] = '('+str(f.food.consumer_amount)+' '+f.food.get_unit_display()+') '

	medicament_wormer = Medicament.objects.filter(farm=farm, is_wormer=True)
	application_medicament_wormer = ApplicationMedicament.objects.filter(medicament=medicament_wormer)
	wormer = []
	for w in application_medicament_wormer:
		if w.medicament.name not in wormer:
			wormer.append(w.medicament.name)
			wormer.append('('+str(w.medicament.amount_application)+' '+w.medicament.get_unit_display()+') ')
		else:
			index = wormer.index(w.medicament.name)+1
			wormer[index] = '('+str(w.medicament.amount_application)+' '+w.medicament.get_unit_display()+') '

	
	medicament_vaccine = Medicament.objects.filter(farm=farm, is_vaccine=True)
	application_medicament_vaccine = ApplicationMedicament.objects.filter(medicament=medicament_vaccine)
	vaccine = []
	for v in application_medicament_vaccine:
		if v.medicament.name not in vaccine:
			vaccine.append(v.medicament.name)
			vaccine.append('('+str(v.medicament.amount_application)+' '+v.medicament.get_unit_display()+') ')
		else:
			index = vaccine.index(v.medicament.name)+1
			vaccine[index] = '('+str(v.medicament.amount_application)+' '+v.medicament.get_unit_display()+') '
	

	return render_to_response('view_report_female.html',
		{'cattle': cattle,
		 'total_births': total_births,
		 'total_problems_births': total_problems_births,
		 'cattle_mother': cattle_mother,
		 'cattle_father': cattle_father,
		 'count_milk': count_milk,
		 'food': food,
		 'wormer': wormer,
		 'vaccine': vaccine,
		 'number_messages': number_message},
		context_instance=RequestContext(request))	


