#-*- coding: utf-8 -*-
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from ganados.models import Ganado, Identificacion_Simple, Ganaderia, Etapa, Identificacion_Ecuador, Ciclo, Verification, Insemination, Ordenio
from medicament.models import Medicament
from alimentos.models import Food, ApplicationFood
from medicament.models import Medicament, ApplicationMedicament
from notifications.models import Notification
from profiles.models import Configuracion, Profile
from django.shortcuts import redirect, HttpResponseRedirect

from django.contrib.auth.models import User

from django.core import serializers
from django.utils import simplejson as json
from ganados.models import Celo

from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
import datetime
from dateutil.relativedelta import relativedelta

from drealtime import iShoutClient
ishout_client = iShoutClient()
from django.contrib.auth.models import User

import pytz

# var aux
user_name = 0


@login_required
def wsGanadosHembras_view(request):
	search = request.GET['search']
	user = request.user
	id_user = User.objects.filter(username=user.username)
	ganaderia = Ganaderia.objects.get(perfil=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)
	

	if configuracion.tipo_identificacion == 'simple' and search != '':
		data = serializers.serialize('json', Identificacion_Simple.objects.filter(
					  (Q(identificaciones_simples__ganaderia=ganaderia)
					  ) &
					  (	Q(identificaciones_simples__nacimiento__icontains=search) |
					  	Q(rp__iexact=search) |
					  	Q(nombre__icontains=search)
					  ) &
					    Q(identificaciones_simples__etapas__nombre__exact=2,
					    identificaciones_simples__etapas__is_active__exact=True,
					    identificaciones_simples__genero__exact=1 )
		))
	else:
		data = serializers.serialize('json', Identificacion_Ecuador.objects.filter(
					  (Q(identificaciones_ecuador__ganaderia=ganaderia)
					  ) &
					  (	Q(identificaciones_ecuador__nacimiento__icontains=search) |
					  	Q(rp__iexact=search) |
					  	Q(nombre__icontains=search)
					  ) &
					    Q(identificaciones_ecuador__etapas__nombre__exact=2,
					    identificaciones_ecuador__etapas__is_active__exact=True,
					    identificaciones_ecuador__genero__exact=1 )
		))
	return HttpResponse(data, mimetype='application/json')

@login_required
def ajaxCattleMaleRp_view(request):
	search = request.GET['search']
	user = request.user
	farm = Ganaderia.objects.get(perfil=user)
	configuration = Configuracion.objects.get(id=farm.configuracion_id)
	
	gg = Ganado.objects.filter(ganaderia=farm)

	if configuration.tipo_identificacion == 'simple' and search != '':
		data = serializers.serialize('json', Identificacion_Simple.objects.filter(
					  (Q(identificaciones_simples__ganaderia=farm)
					  ) &
					  (	Q(identificaciones_simples__nacimiento__icontains=search) |
					  	Q(rp__iexact=search) |
					  	Q(nombre__icontains=search)
					  ) &
					  	Q(identificaciones_simples__genero__exact=0)
		))
	else:
		data = serializers.serialize('json', Identificacion_Ecuador.objects.filter(
					  (Q(identificaciones_ecuador__ganaderia=farm)
					  ) &
					  (	Q(identificaciones_ecuador__nacimiento__icontains=search) |
					  	Q(rp__iexact=search) |
					  	Q(nombre__icontains=search)
					  ) &
					  	Q(identificaciones_ecuador__genero__exact=0)
		))
	return HttpResponse(data, mimetype='application/json')

@login_required
def ajaxGanadosMachosInseminacion_view(request):
	search = request.GET['search']
	user = request.user
	farm = Ganaderia.objects.get(perfil=user)
	
	data = serializers.serialize('json', Insemination.objects.filter(
				  (Q(farm=farm)
				  ) &
				  (	Q(registration_date__icontains=search) |
				  	Q(rp__iexact=search) |
				  	Q(name__icontains=search)
				  ) 
		))
	
	return HttpResponse(data, mimetype='application/json')

@login_required
def wsGanados_view(request):
	search = request.GET['search']
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)

	if ganaderia.configuracion.tipo_identificacion == 'simple':
	
		ganados = Ganado.objects.filter(
											Q(ganaderia=ganaderia, genero=1) &
											(
												Q(nacimiento__icontains=search) |
												Q(identificacion_simple__nombre__icontains=search) |
												Q(identificacion_simple__rp__icontains=search)
											)
										)
		
		celos = Celo.objects.filter(is_active=True, estado=0, ganado_id=ganados)
		etapas = Etapa.objects.filter(is_active=True, ganado_id=ganados)
		ciclos = Ciclo.objects.filter(is_active=True, ganado_id=ganados)
		verificaciones = Verification.objects.filter(is_active=True, cattle_id=ganados)

		# serializando
		data = '['
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

			if celos.count() > 0:
				for c in celos:
					if c.ganado_id == g.id:
						data += ', "celo": "En Celo"'
					else:
						data += ', "celo": "Sin Celo"'
			else:
				data += ', "celo": "Sin celo"'
				
			for e in etapas:
				if e.ganado_id == g.id:
					if e.nombre == 0:
						data += ', "etapa": "Ternera"'
					elif e.nombre == 1:
						data += ', "etapa": "Vacona"'
					elif e.nombre == 2:
						data += ', "etapa": "Vientre"'

			for ciclo in ciclos:
				if ciclo.ganado_id == g.id and ciclo.is_active:
					if ciclo.nombre == 0:
						data += ', "ciclo": '+ str(ciclo.nombre) 
					elif ciclo.nombre == 1:
						data += ', "ciclo": '+ str(ciclo.nombre) 
					elif ciclo.nombre == 2:
						data += ', "ciclo": '+ str(ciclo.nombre) 
					elif ciclo.nombre == 3:
						data += ', "ciclo": '+ str(ciclo.nombre) 

			for verificacion in verificaciones:
				if verificacion.cattle_id == g.id and verificacion.is_active:
					data += ', "verificacion": "True"'
				else:
					data += ', "verificacion": "False"'
					

			data += '}}'
		data += ']'

	else:
		ganados = Ganado.objects.filter(
										Q(ganaderia=ganaderia, genero=1) &
										(
											Q(nacimiento__icontains=search) |
											Q(identificacion_ecuador__nombre__icontains=search) |
											Q(identificacion_ecuador__rp__icontains=search)
										)
									)
		
		celos = Celo.objects.filter(is_active=True, estado=0, ganado_id=ganados)
		etapas = Etapa.objects.filter(is_active=True, ganado_id=ganados)
		ciclos = Ciclo.objects.filter(is_active=True, ganado_id=ganados)
		verificaciones = Verification.objects.filter(is_active=True, cattle_id=ganados)

		# serializando
		data = '['
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

			if celos.count() > 0:
				for c in celos:
					if c.ganado_id == g.id:
						data += ', "celo": "En Celo"'
					else:
						data += ', "celo": "Sin Celo"'
			else:
				data += ', "celo": "Sin celo"'
				
			for e in etapas:
				if e.ganado_id == g.id:
					if e.nombre == 0:
						data += ', "etapa": "Ternera"'
					elif e.nombre == 1:
						data += ', "etapa": "Vacona"'
					elif e.nombre == 2:
						data += ', "etapa": "Vientre"'

			if ciclos.count() > 0:
				for ciclo in ciclos:
					if ciclo.ganado_id == g.id and ciclo.is_active:
						if ciclo.nombre == 0:
							data += ', "ciclo": '+ str(ciclo.nombre) 
						elif ciclo.nombre == 1:
							data += ', "ciclo": '+ str(ciclo.nombre) 
						elif ciclo.nombre == 2:
							data += ', "ciclo": '+ str(ciclo.nombre) 
						elif ciclo.nombre == 3:
							data += ', "ciclo": '+ str(ciclo.nombre) 

			if verificaciones.count() > 0:
				for verificacion in verificaciones:
					if verificacion.cattle_id == g.id and verificacion.is_active:
						data += ', "verificacion": "True"'
					else:
						data += ', "verificacion": "False"'
					

			data += '}}'
		data += ']'
		
		'''
		reigistros = LoadTest.objects.all()
		datas = serializers.serialize('json', reigistros, indent=2)
		'''
	
	return HttpResponse(data, mimetype='application/json')

@login_required
def ajaxCattleMale_view(request):
	search = request.GET['search']
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)

	if ganaderia.configuracion.tipo_identificacion == 'simple':
	
		ganados = Ganado.objects.filter(
											Q(ganaderia=ganaderia, genero=0) &
											(
												Q(nacimiento__icontains=search) |
												Q(identificacion_simple__nombre__icontains=search) |
												Q(identificacion_simple__rp__icontains=search)
											)
										)

		# serializando
		data = '['
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
										Q(ganaderia=ganaderia, genero=0) &
										(
											Q(nacimiento__icontains=search) |
											Q(identificacion_ecuador__nombre__icontains=search) |
											Q(identificacion_ecuador__rp__icontains=search)
										)
									)
		
		# serializando
		data = '['
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

@login_required
def wsGanadosProduccion_view(request):
	search = request.GET['search']
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)

	if ganaderia.configuracion.tipo_identificacion == 'simple':

		ganados = Ganado.objects.filter(
											Q(ganaderia=ganaderia, genero=1, etapas__nombre=2, ciclos__nombre=2) &
											(
												Q(identificacion_simple__rp__icontains=search) |
												Q(nacimiento__icontains=search) |
												Q(identificacion_simple__nombre__icontains=search) 
											)
										)
		celos = Celo.objects.filter(is_active=True, ganado_id=ganados)
		etapas = Etapa.objects.filter(is_active=True, ganado_id=ganados)
		ciclos = Ciclo.objects.filter(is_active=True, ganado_id=ganados)
		verificaciones = Verification.objects.filter(is_active=True, cattle_id=ganados)
		# serializando
		data = '['
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

			if celos.count() > 0:
				for c in celos:
					if c.ganado_id == g.id:
						data += ', "celo": "En celo"'
					else:
						data += ', "celo": "Sin celo"'
			else:
				data += ', "celo": "Sin celo"'
				
			for e in etapas:
				if e.ganado_id == g.id:
					if e.nombre == 0:
						data += ', "etapa": "Ternera"'
					elif e.nombre == 1:
						data += ', "etapa": "Vacona"'
					elif e.nombre == 2:
						data += ', "etapa": "Vientre"'

			for ciclo in ciclos:
				if ciclo.ganado_id == g.id and ciclo.is_active:
					if ciclo.nombre == 0:
						data += ', "ciclo": '+ str(ciclo.nombre) 
					elif ciclo.nombre == 1:
						data += ', "ciclo": '+ str(ciclo.nombre) 
					elif ciclo.nombre == 2:
						data += ', "ciclo": '+ str(ciclo.nombre) 
					elif ciclo.nombre == 3:
						data += ', "ciclo": '+ str(ciclo.nombre) 

			for verificacion in verificaciones:
				if verificacion.cattle_id == g.id and verificacion.is_active:
					data += ', "verificacion": "True"'
				else:
					data += ', "verificacion": "False"'

			data += '}}'
		data += ']'

	else:
		ganados = Ganado.objects.filter(
										Q(ganaderia=ganaderia, genero=1, etapas__nombre=2, ciclos__nombre=2) &
										(
											Q(identificacion_ecuador__rp__icontains=search) |
											Q(nacimiento__icontains=search) |
											Q(identificacion_ecuador__nombre__icontains=search) 
										)
									)
		celos = Celo.objects.filter(is_active=True, ganado_id=ganados)
		etapas = Etapa.objects.filter(is_active=True, ganado_id=ganados)
		ciclos = Ciclo.objects.filter(is_active=True, ganado_id=ganados)
		verificaciones = Verification.objects.filter(is_active=True, cattle_id=ganados)
		# serializando
		data = '['
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

			if celos.count() > 0:
				for c in celos:
					if c.ganado_id == g.id:
						data += ', "celo": "En celo"'
					else:
						data += ', "celo": "Sin celo"'
			else:
				data += ', "celo": "Sin celo"'
				
			for e in etapas:
				if e.ganado_id == g.id:
					if e.nombre == 0:
						data += ', "etapa": "Ternera"'
					elif e.nombre == 1:
						data += ', "etapa": "Vacona"'
					elif e.nombre == 2:
						data += ', "etapa": "Vientre"'

			if ciclos.count() > 0:
				for ciclo in ciclos:
					if ciclo.ganado_id == g.id and ciclo.is_active:
						if ciclo.nombre == 0:
							data += ', "ciclo": '+ str(ciclo.nombre) 
						elif ciclo.nombre == 1:
							data += ', "ciclo": '+ str(ciclo.nombre) 
						elif ciclo.nombre == 2:
							data += ', "ciclo": '+ str(ciclo.nombre) 
						elif ciclo.nombre == 3:
							data += ', "ciclo": '+ str(ciclo.nombre) 

			if verificaciones.count() > 0:
				for verificacion in verificaciones:
					if verificacion.cattle_id == g.id and verificacion.is_active:
						data += ', "verificacion": "True"'
					else:
						data += ', "verificacion": "False"'

			data += '}}'
		data += ']'

	'''
	reigistros = LoadTest.objects.all()
	datas = serializers.serialize('json', reigistros, indent=2)
	'''
	return HttpResponse(data, mimetype='application/json')

# ------------------------------------------------------------
# WORMER
# ------------------------------------------------------------
@login_required
def wsWormer_view(request):
	search = request.GET['search']
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)
	'''
	datas = serializers.serialize('json', Medicament.objects.filter(
				  (	Q(farm=ganaderia, is_wormer=True) &
				  	Q(name__icontains=search)
				  ) 
	))
	'''
	datas = Medicament.objects.filter(
										(
											Q(is_wormer=True, farm=ganaderia)
										) & 
										(Q(expiration_date__icontains=search) |
										Q(name__icontains=search))
									)
	data = '['
	for g in datas:
		if data == '[':
			data += '{"pk": ' + str(g.id) + ', '
		else:
			data += ',{"pk": ' + str(g.id) + ', '
		data += '"fields": {'
		data += '"name": "'+ str(g.name) +'"'
		data += ', "expiration_date": "'+ str(g.expiration_date) +'"'
		data += ', "sex": "'+ str(g.sex) +'"'
		data += ', "amount": "'+ str(g.amount) +'"'
		data += ', "unit": "'+ str(g.unit) +'"'
		

		data += '}}'
	data += ']'

	return HttpResponse(data, mimetype='application/json')

@login_required
def ajaxVaccine_view(request):
	search = request.GET['search']
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)
	
	medicaments = Medicament.objects.filter(
										(
											Q(is_vaccine=True, farm=ganaderia)
										) & 
										(Q(expiration_date__icontains=search) |
										Q(name__icontains=search))
									)
	data = '['
	for m in medicaments:
		if data == '[':
			data += '{"pk": ' + str(m.id) + ', '
		else:
			data += ',{"pk": ' + str(m.id) + ', '
		data += '"fields": {'
		data += '"name": "'+ str(m.name) +'"'
		data += ', "expiration_date": "'+ str(m.expiration_date) +'"'
		data += ', "sex": "'+ str(m.sex) +'"'
		data += ', "amount": "'+ str(m.amount) +'"'
		data += ', "unit": "'+ str(m.unit) +'"'
		data += '}}'
	data += ']'
	
	return HttpResponse(data, mimetype='application/json')

@login_required
def ajaxFood_view(request):
	search = request.GET['search']
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)
	
	foods = Food.objects.filter(
										(
											Q(farm=ganaderia)
										) & 
										(Q(expiration_date__icontains=search) |
										Q(name__icontains=search))
									)
	
	data = '['
	for f in foods:
		if data == '[':
			data += '{"pk": ' + str(f.id) + ', '
		else:
			data += ',{"pk": ' + str(f.id) + ', '
		data += '"fields": {'
		data += '"name": "'+ str(f.name) +'"'
		data += ', "expiration_date": "'+ str(f.expiration_date) +'"'
		data += ', "phase": "'+ str(f.phase) +'"'
		data += ', "amount": "'+ str(f.amount) +'"'
		data += ', "unit": "'+ str(f.unit) +'"'
		data += '}}'
	data += ']'
	
	return HttpResponse(data, mimetype='application/json')


@login_required
def ajaxAssignCattleVaccine_view(request):
	search = request.GET['search']
	listCattle = str(request.GET['listCattle'])
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)
	
	if ganaderia.configuracion.tipo_identificacion == 'simple':
		ganados = Ganado.objects.filter(
											Q(ganaderia=ganaderia) &
											(
												Q(nacimiento__icontains=search) |
												Q(identificacion_simple__nombre__icontains=search) |
												Q(identificacion_simple__rp__icontains=search)
											)
										)
		# serializando
		data = '['
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
												Q(nacimiento__icontains=search) |
												Q(identificacion_ecuador__nombre__icontains=search) |
												Q(identificacion_ecuador__rp__icontains=search)
											)
										)
		# serializando
		data = '['
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


@login_required
def ajaxAssignCattleVaccineFinal(request):
	id_wormer = request.GET['id_vaccine']
	listCattle = str(request.GET['listCattle'])
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)
	wormer = Medicament.objects.get(id=id_wormer)
	listCattle = listCattle.replace('[','')
	listCattle = listCattle.replace(']','')
	listCattle = listCattle.replace(',','')
	listCattle = list(listCattle)

	date_now = datetime.date.today()
	if len(listCattle) > 0:
		if (len(listCattle) * wormer.amount_application) <= wormer.amount:
			application_wormer = ApplicationMedicament()
			application_wormer.date = date_now
			application_wormer.status = 0
			application_wormer.medicament = wormer
			application_wormer.save()
			for c in range(len(listCattle)):
				application_wormer.cattle.add(listCattle[c])
			wormer.amount=wormer.amount - (len(listCattle)*wormer.amount_application)
			wormer.save()
			data = '[ { "state": 0} ]'
		else:
			if wormer.unit == 0:
				unit_display = 'ml'
			elif wormer.unit == 1: 
				unit_display='gr'
			elif wormer.unit==2: 
				unit_display='lbs' 
			elif wormer.unit==3: 
				unit_display='kg' 
			elif wormer.unit==4: 
				unit_display='paquetes'
			data = '[ {"state": 1, "amount":'+str(wormer.amount)+', "amount_now": '+str(len(listCattle)*wormer.amount_application)+', "unit": "'+unit_display+'" , "consumer_amount": "'+str(wormer.amount_application)+'"}]'
	else:
		data = '[ { "state": 2} ]'

	return HttpResponse(data, mimetype='application/json')



@login_required
def ajaxAssignCattleWormer_view(request):
	search = request.GET['search']
	listCattle = str(request.GET['listCattle'])
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)
	
	if ganaderia.configuracion.tipo_identificacion == 'simple':
		ganados = Ganado.objects.filter(
											Q(ganaderia=ganaderia) &
											(
												Q(nacimiento__icontains=search) |
												Q(identificacion_simple__nombre__icontains=search) |
												Q(identificacion_simple__rp__icontains=search)
											)
										)
		# serializando
		data = '['
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
												Q(nacimiento__icontains=search) |
												Q(identificacion_ecuador__nombre__icontains=search) |
												Q(identificacion_ecuador__rp__icontains=search)
											)
										)
		# serializando
		data = '['
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

@login_required
def ajaxAssignCattleWormerFinal(request):
	id_wormer = request.GET['id_wormer']
	listCattle = str(request.GET['listCattle'])
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)
	wormer = Medicament.objects.get(id=id_wormer)
	listCattle = listCattle.replace('[','')
	listCattle = listCattle.replace(']','')
	listCattle = listCattle.replace(',','')
	listCattle = list(listCattle)

	date_now = datetime.date.today()
	if len(listCattle) > 0:
		if (len(listCattle) * wormer.amount_application) <= wormer.amount:
			application_wormer = ApplicationMedicament()
			application_wormer.date = date_now
			application_wormer.status = 0
			application_wormer.medicament = wormer
			application_wormer.save()
			for c in range(len(listCattle)):
				application_wormer.cattle.add(listCattle[c])
			wormer.amount=wormer.amount - (len(listCattle)*wormer.amount_application)
			wormer.save()
			data = '[ { "state": 0} ]'
		else:
			if wormer.unit == 0:
				unit_display = 'ml'
			elif wormer.unit == 1: 
				unit_display='gr'
			elif wormer.unit==2: 
				unit_display='lbs' 
			elif wormer.unit==3: 
				unit_display='kg' 
			elif wormer.unit==4: 
				unit_display='paquetes'
			data = '[ {"state": 1, "amount":'+str(wormer.amount)+', "amount_now": '+str(len(listCattle)*wormer.amount_application)+', "unit": "'+unit_display+'" , "consumer_amount": "'+str(wormer.amount_application)+'"}]'
	else:
		data = '[ { "state": 2} ]'

	return HttpResponse(data, mimetype='application/json')



@login_required
def ajaxAssignCattleFood_view(request):
	search = request.GET['search']
	listCattle = str(request.GET['listCattle'])
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)
	
	if ganaderia.configuracion.tipo_identificacion == 'simple':
		ganados = Ganado.objects.filter(
											Q(ganaderia=ganaderia) &
											(
												Q(nacimiento__icontains=search) |
												Q(identificacion_simple__nombre__icontains=search) |
												Q(identificacion_simple__rp__icontains=search)
											)
										)
		# serializando
		data = '['
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
												Q(nacimiento__icontains=search) |
												Q(identificacion_ecuador__nombre__icontains=search) |
												Q(identificacion_ecuador__rp__icontains=search)
											)
										)
		# serializando
		data = '['
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



@login_required
def ajaxAssignCattleFoodFinal(request):
	id_food = request.GET['id_food']
	listCattle = str(request.GET['listCattle'])
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)
	food = Food.objects.get(id=id_food)
	listCattle = listCattle.replace('[','')
	listCattle = listCattle.replace(']','')
	listCattle = listCattle.replace(',','')
	listCattle = list(listCattle)

	date_now = datetime.date.today()
	if len(listCattle) > 0:
		if (len(listCattle) * food.consumer_amount) <= food.amount:
			application_food = ApplicationFood()
			application_food.date = date_now
			application_food.status = 0
			application_food.food = food
			application_food.save()
			for c in range(len(listCattle)):
				application_food.cattle.add(listCattle[c])
			food.amount=food.amount - (len(listCattle)*food.consumer_amount)
			food.save()
			data = '[ { "state": 0} ]'
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
			data = '[ {"state": 1, "amount":'+str(food.amount)+', "amount_now": '+str(len(listCattle)*food.consumer_amount)+', "unit": "'+unit_display+'" , "consumer_amount": "'+str(food.consumer_amount)+'"}]'
	else:
		data = '[ { "state": 2} ]'

	return HttpResponse(data, mimetype='application/json')


@login_required
def ajaxInsemination_view(request):
	search = request.GET['search']
	user = request.user
	farm = Ganaderia.objects.get(perfil=user)

	data = serializers.serialize('json', Insemination.objects.filter(
				  (Q(farm=farm)) &
				  (	Q(registration_date__icontains=search) |
				  	Q(rp__iexact=search) |
				  	Q(name__icontains=search)
				  ) 
	).order_by('-rp'))
	
	return HttpResponse(data, mimetype='application/json')


import spade
import datetime
import time
import sys

################################################
# Agente Produccion
################################################
class DesireProduccion:
	def __init__(self):
		self.desire_ordenio = []
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		date = datetime.date.today()
		cattle = Ganado.objects.filter(ganaderia=farm, genero=1, etapas__nombre=2, ciclos__nombre=2)
		for c in cattle:
			self.desire_ordenio.append(c.id)

class BeliefProduccion:
	def __init__(self):
		self.belief1 = []
		self.belief1.append(5)

class IntentionProduction:
	def assignNotification(self, d):
		notification = Notification()
		notification.start_date = datetime.date.today()
		notification.end_date = date.today() + timedelta(days=0)
		notification.state = 2
		notification.module = 3
		cattle = Ganado.objects.get(id=d)
		notification.ident_cattle = cattle
		notification.name = 5
		notification.save()

	def sendNotificationOrdenio(self, desire_ordenio):
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		
		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		for d in desire_ordenio:
			one_day_before = date.today() - relativedelta(days=1)
			try:
				notifi = Notification.objects.get(ident_cattle_id=d, start_date=date.today())
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_cattle_id=d, start_date=one_day_before, state=2, name=5)
					notifi.state = 0
					notifi.save()
					self.assignNotification(d)
				except ObjectDoesNotExist:
					self.assignNotification(d)
					

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2).count()
		for u in users:
			print "enviando a: ", u.username
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)


class AgentProduccion(spade.Agent.Agent):
	class BehaviourProduccion(spade.Behaviour.OneShotBehaviour):
		def onStart(self):
			print "inicio del BehaviourProduccion . . ."

		def _process(self):
			print "Inicio del proceso del BehaviourProduccion"
			desire = DesireProduccion()		
			belief = BeliefProduccion()
			intention = IntentionProduction()
			if 5 in belief.belief1:
				intention.sendNotificationOrdenio(desire.desire_ordenio)
				print "Notificación enviada"

		def onEnd(self):
			print "fin del BehaviourProduccion . . ."
			sys.exit(0)

	def _setup(self):
		print "Inicio del AgentProduccion . . ."
		b = self.BehaviourProduccion()
		self.addBehaviour(b, None)

################################################
# Agente Sanidad
################################################
class DesireSanidad:
	def __init__(self):
		self.desire_amount_vaccine = []
		self.desire_amount_wormer = []
		self.desire_expiration_vaccine = []
		self.desire_expiration_wormer = []

		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		medicament_vaccine = Medicament.objects.filter(farm=farm, amount__lt=30, is_vaccine=True)
		medicament_wormer = Medicament.objects.filter(farm=farm, amount__lt=30, is_wormer=True)
		medicament_expiration_vaccine = Medicament.objects.filter(farm=farm, is_vaccine=True)
		medicament_expiration_wormer = Medicament.objects.filter(farm=farm, is_wormer=True)

		for m in medicament_vaccine:
			self.desire_amount_vaccine.append(m.id)
		for m in medicament_wormer:
			self.desire_amount_wormer.append(m.id)
		
		date_expiration = date.today() + relativedelta(months=3)
		for m in medicament_expiration_vaccine:
			if m.expiration_date < date_expiration:
				self.desire_expiration_vaccine.append(m.id)
		for m in medicament_expiration_wormer:
			if m.expiration_date < date_expiration:
				self.desire_expiration_wormer.append(m.id)


class BeliefSanidad:
	def __init__(self):
		self.beliefs = []
		self.beliefs.append(6)
		self.beliefs.append(7)
		self.beliefs.append(8)
		self.beliefs.append(9)
		self.beliefs.append(10)
		self.beliefs.append(11)

class IntentionSanidad:
	def assignNotification(self, d, datee, name):
		notification = Notification()
		notification.start_date = datetime.date.today()
		notification.end_date = datee
		notification.state = 2
		notification.module = 2
		medicament = Medicament.objects.get(id=d)
		notification.ident_medicament = medicament
		notification.name = name
		notification.save()

		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2).count()
		for u in users:
			print "enviando a: ", u.username
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)

	def sendNotificationAmountVaccine(self, desire_amount_vaccine):
		datee = date.today() + timedelta(days=3)
		one_day_before = date.today() - relativedelta(days=1)
			
		for d in desire_amount_vaccine:
			try:
				notifi = Notification.objects.get(ident_medicament_id=d, start_date=date.today(), end_date=datee)
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_medicament_id=d, state=2, end_date=one_day_before, name=6)
					notifi.state = 0
					notifi.save()
					self.assignNotification(d, datee, 6)
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_medicament_id=d, state=2, name=6)
					except ObjectDoesNotExist:
						self.assignNotification(d, datee, 6)


	def sendNotificationAmountWormer(self, desire_amount_wormer):
		datee = date.today() + timedelta(days=3)
		one_day_before = date.today() - relativedelta(days=1)

		for d in desire_amount_wormer:
			try:
				notifi = Notification.objects.get(ident_medicament_id=d, start_date=date.today(), end_date=datee)
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_medicament_id=d, state=2, end_date=one_day_before, name=7)
					notifi.state = 0
					notifi.save()
					self.assignNotification(d, datee, 7)
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_medicament_id=d, state=2, name=7)
					except ObjectDoesNotExist:
						self.assignNotification(d, datee, 7)


	def sendNotificationExpirationVaccine(self, desire_expiration_vaccine):
		datee = date.today() + relativedelta(months=3)
		one_day_before = date.today() - relativedelta(days=1)
		
		for d in desire_expiration_vaccine:
			try:
				notifi = Notification.objects.get(ident_medicament_id=d, start_date=date.today(), end_date=datee)
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_medicament_id=d, state=2, end_date=one_day_before, name=8)
					notifi.state = 0
					notifi.save()
					self.assignNotification(d, datee, 8)
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_medicament_id=d, state=2, name=8)
					except ObjectDoesNotExist:
						self.assignNotification(d, datee, 8)

	def sendNotificationExpirationWormer(self, desire_expiration_wormer):
		datee = date.today() + relativedelta(months=3)
		one_day_before = date.today() - relativedelta(days=1)
		
		for d in desire_expiration_wormer:
			try:
				notifi = Notification.objects.get(ident_medicament_id=d, start_date=date.today(), end_date=datee)
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_medicament_id=d, state=2, end_date=one_day_before, name=9)
					notifi.state = 0
					notifi.save()
					self.assignNotification(d, datee, 9)
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_medicament_id=d, state=2, name=9)
					except ObjectDoesNotExist:
						self.assignNotification(d, datee, 9)


class AgentSanidad(spade.Agent.Agent):
	class BehaviourSanidad(spade.Behaviour.OneShotBehaviour):
		def onStart(self):
			print "inicio del BehaviourSanidad . . ."

		def _process(self):
			print "Inicio del proceso del BehaviourSanidad"
			desire = DesireSanidad()		
			belief = BeliefSanidad()
			intention = IntentionSanidad()
			if 6 in belief.beliefs:
				intention.sendNotificationAmountVaccine(desire.desire_amount_vaccine)
				print "Notificación: desire_amount_vaccine, Enviada"
			if 7 in belief.beliefs:
				intention.sendNotificationAmountWormer(desire.desire_amount_wormer)
				print "Notificación: desire_amount_wormer, Enviada"
			if 8 in belief.beliefs:
				intention.sendNotificationExpirationVaccine(desire.desire_expiration_vaccine)
				print "Notificación: desire_expiration_vaccine, Enviada"
			if 9 in belief.beliefs:
				intention.sendNotificationExpirationWormer(desire.desire_expiration_wormer)
				print "Notificación: desire_expiration_wormer, Enviada"

		def onEnd(self):
			print "fin del BehaviourSanidad . . ."
			sys.exit(0)

	def _setup(self):
		print "Inicio del AgentSanidad . . ."
		b = self.BehaviourSanidad()
		self.addBehaviour(b, None)


################################################
# Agente Alimentacion
################################################
class DesireAlimentacion:
	def __init__(self):
		self.desire_amount_food = []
		self.desire_expiration_food = []
		

		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		food_amount = Food.objects.filter(farm=farm, amount__lt=30)
		food_expiration = Food.objects.filter(farm=farm)

		for f in food_amount:
			self.desire_amount_food.append(f.id)

		date_expiration = date.today() + relativedelta(months=3)
		for f in food_expiration:
			if f.expiration_date < date_expiration:
				self.desire_expiration_food.append(f.id)

class BeliefAlimentacion:
	def __init__(self):
		self.beliefs = []
		self.beliefs.append(12)
		self.beliefs.append(13)
		self.beliefs.append(14)

class IntentionAlimentacion:
	def assignNotification(self, d, datee, name):
		notification = Notification()
		notification.start_date = datetime.date.today()
		notification.end_date = datee
		notification.state = 2
		notification.module = 1
		food = Food.objects.get(id=d)
		notification.ident_food = food
		notification.name = name
		notification.save()

		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2).count()
		for u in users:
			print "enviando a: ", u.username
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)

	def sendNotificationAmountFood(self, desire_amount_food):
		datee = date.today() + timedelta(days=3)
		one_day_before = date.today() - relativedelta(days=1)
		
		for d in desire_amount_food:
			try:
				notifi = Notification.objects.get(ident_food_id=d, start_date=date.today(), end_date=datee)
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_food_id=d, state=2, end_date=one_day_before, name=12)
					notifi.state = 0
					notifi.save()
					self.assignNotification(d, datee, 12)
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_food_id=d, state=2, name=12)
					except ObjectDoesNotExist:
						self.assignNotification(d, datee, 12)

	def sendNotificationExpirationFood(self, desire_expiration_food):
		datee = date.today() + relativedelta(months=3)
		one_day_before = date.today() - relativedelta(days=1)
		
		for d in desire_expiration_food:
			try:
				notifi = Notification.objects.get(ident_food_id=d, start_date=date.today(), end_date=datee)
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_food_id=d, state=2, end_date=one_day_before, name=13)
					notifi.state = 0
					notifi.save()
					self.assignNotification(d, datee, 13)
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_food_id=d, state=2, name=13)
					except ObjectDoesNotExist:
						self.assignNotification(d, datee, 13)
				


class AgentAlimentacion(spade.Agent.Agent):
	class BehaviourAlimentacion(spade.Behaviour.OneShotBehaviour):
		def onStart(self):
			print "inicio del BehaviourAlimentacion . . ."

		def _process(self):
			print "Inicio del proceso del BehaviourAlimentacion"
			desire = DesireAlimentacion()		
			belief = BeliefAlimentacion()
			intention = IntentionAlimentacion()
			if 12 in belief.beliefs:
				intention.sendNotificationAmountFood(desire.desire_amount_food)
				print "Notificación: desire_amount_food, Enviada"
			if 13 in belief.beliefs:
				intention.sendNotificationExpirationFood(desire.desire_expiration_food)
				print "Notificación: desire_expiration_food, Enviada"

		def onEnd(self):
			print "fin del BehaviourAlimentacion . . ."
			sys.exit(0)

	def _setup(self):
		print "Inicio del AgentAlimentacion . . ."
		b = self.BehaviourAlimentacion()
		self.addBehaviour(b, None)



################################################
# Agente Reproduccion
################################################
class DesireReproduccion:
	def __init__(self):
		self.desire_celo = []
		self.desire_service = []
		self.desire_verification = []
		self.desire_parto = []
		self.desire_pajuelas = []

		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)

		try:
			cattle_celo = Ganado.objects.filter( etapas__nombre=2, ganaderia=farm )
			for c in cattle_celo:
				self.desire_celo.append(c.id)
		except ObjectDoesNotExist:
			pass

		try:
			cattle_service = Ganado.objects.filter( ganaderia=farm, genero=1, celos__estado=0, celos__is_active=True )
			for c in cattle_service:
				self.desire_service.append(c.id)
		except ObjectDoesNotExist:
			pass

		try:
			cattle_verification = Ganado.objects.filter( ganaderia=farm, genero=1, verification_cattle__is_active=True, verification_cattle__attempt_verification__attempt_date=date.today() )
			for c in cattle_verification:
				self.desire_verification.append(c.id)
		except ObjectDoesNotExist:
			pass

		ten_days_parto = date.today() + relativedelta(days=10)
		try:
			cattle_parto = Ganado.objects.filter( ganaderia=farm, genero=1, gestaciones__fecha_parto=ten_days_parto, gestaciones__is_active=True )
			for c in cattle_parto:
				self.desire_parto.append(c.id)
		except ObjectDoesNotExist:
			pass

		try:
			pajuelas = Insemination.objects.filter( farm=farm, amount_pajuelas__lt=5 )
			for p in pajuelas:
				self.desire_pajuelas.append(p.id)
		except ObjectDoesNotExist:
			pass



class BeliefReproduccion:
	def __init__(self):
		self.beliefs = []
		self.beliefs.append(0)
		self.beliefs.append(1)
		self.beliefs.append(2)
		self.beliefs.append(3)
		self.beliefs.append(4)

class IntentionReproduccion:
	def assignNotification(self, d, datee, name):
		notification = Notification()
		notification.start_date = datetime.date.today()
		notification.end_date = datee
		notification.state = 2
		notification.module = 0
		cattle = Ganado.objects.get(id=d)
		notification.ident_cattle = cattle
		notification.name = name
		notification.save()

		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2).count()
		for u in users:
			print "enviando a: ", u.username
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)

	def sendNotificationCelo(self, desire_celo):
		datee = date.today() + timedelta(days=3)
		one_day_before = date.today() - relativedelta(days=1)
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		configuration = Configuracion.objects.get(id=farm.configuracion_id)
		try:
			cattles = Ganado.objects.filter(ganaderia=farm, etapas__nombre=2, ciclos__nombre=0, ciclos__is_active=True)

			for c in cattles:

				if c.gestaciones.all():
					for c_parto in c.gestaciones.all(): # itera las gestaciones que haya tenido
						if c_parto.is_active==False:
							date_parto = c_parto.fecha_parto
				else:
					date_parto = ''
				
				if date_parto != '':  # si existe una previa gestacion (!=)
					days_after_parto = configuration.celo_despues_parto
					days_after_parto_error = configuration.celo_despues_parto_error
					date_celo = date_parto + relativedelta( days=(days_after_parto + days_after_parto_error) )
					
					if date.today() >= date_celo: # si >= a la fecha de celo luego del parto
						celo = Celo()
						start_date = datetime.datetime.now(pytz.timezone('America/Guayaquil'))
						duration_celo = datetime.timedelta(hours=configuration.celo_duracion + configuration.celo_duracion_error)
						end_date = start_date + duration_celo
						celo.fecha_inicio = start_date
						celo.fecha_fin = end_date
						celo.estado = 0
						celo.observaciones = ''
						celo.ganado = c
						celo.is_active = True
						celo.save()
						self.assignNotification(c.id, end_date.date(), 0)
				else: # auscencia de previa gestacion
					if c.ciclos.all():
						for ci in c.ciclos.all():
							if ci.nombre == 0 and ci.is_active==True:
								start_date_ciclo = ci.fecha_inicio
								
					days_frequency_celo = configuration.celo_frecuencia
					days_frequency_celo_error = configuration.celo_frecuencia_error
					end_days = days_frequency_celo - days_frequency_celo_error
					date_now = start_date_ciclo + relativedelta(days=end_days)
					
					print date.today(), " >= ", date_now
					if date.today() >= date_now:
						start_date = datetime.datetime.now(pytz.timezone('America/Guayaquil'))
						duration_celo = datetime.timedelta(hours=configuration.celo_duracion + configuration.celo_duracion_error)
						end_date = start_date + duration_celo

						try:
							notifi = Notification.objects.get(ident_cattle_id=c, start_date=date.today(), end_date=end_date, module=0, name=0)
						except ObjectDoesNotExist:
							try:
								notifi = Notification.objects.get(ident_cattle_id=c, state=2, end_date=one_day_before, module=0, name=0)
								notifi.state = 0
								notifi.save()
								self.assignNotification(c, end_date, 0)
							except ObjectDoesNotExist:
								try:
									notifi = Notification.objects.get(ident_cattle_id=c, state=2, module=0, name=0)
								except ObjectDoesNotExist:
									celo = Celo()
									celo.fecha_inicio = start_date
									celo.fecha_fin = end_date
									celo.estado = 0
									celo.observaciones = ''
									celo.ganado = c
									celo.is_active = True
									celo.save()
									self.assignNotification(c.id, end_date.date(), 0)

			users = User.objects.filter(profile_user__ganaderia_perfil=farm)

			msg = 'Notificación, REALIZADA con ÉXITO'
			n = Notification.objects.filter(state=2).count()
			for u in users:
				print "enviando a: ", u.username
				ishout_client.emit(
						u.id,
						'notifications',
						data = {'msg': msg,
								'number_notifications': n,}
					)
					
		except ObjectDoesNotExist:
			pass

	def sendNotificationService(self, desire_service):
		datee = date.today() + timedelta(days=1)
		one_day_before = date.today() - relativedelta(days=1)
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		
		for d in desire_service:
			try:
				notifi = Notification.objects.get(ident_cattle_id=d, start_date=date.today(), end_date=datee, module=0, name=1)
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_cattle_id=d, state=2, end_date=one_day_before, module=0, name=1)
					notifi.state = 0
					notifi.save()
					self.assignNotification(d, datee, 1)
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_cattle_id=d, state=2, module=0, name=1)
					except ObjectDoesNotExist:
						self.assignNotification(d, datee, 1)
						
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2).count()
		for u in users:
			print "enviando a: ", u.username
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)

	def sendNotificationVerification(self, desire_verification):
		datee = date.today() + timedelta(days=1)
		one_day_before = date.today() - relativedelta(days=1)
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		configuration = Configuracion.objects.get(id=farm.configuracion_id)

		for d in desire_verification:
			try:
				notifi = Notification.objects.get(ident_cattle_id=d, start_date=date.today(), end_date=datee, module=0, name=2 )
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_cattle_id=d, state=2, end_date=one_day_before, module=0, name=2)
					notifi.state = 0
					notifi.save()
					self.assignNotification(d, datee, 2)
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_cattle_id=d, state=2, module=0, name=2)
					except ObjectDoesNotExist:
						self.assignNotification(d, datee, 2)
						
		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2).count()
		for u in users:
			print "enviando a: ", u.username
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)

	def sendNotificationParto(self, desire_parto):
		datee = date.today() + timedelta(days=12)
		one_day_before = date.today() - relativedelta(days=1)
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		configuration = Configuracion.objects.get(id=farm.configuracion_id)

		for d in desire_parto:
			try:
				notifi = Notification.objects.get(ident_cattle_id=d, start_date=date.today(), end_date=datee, module=0, name=3 )
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_cattle_id=d, state=2, end_date=one_day_before, module=0, name=3)
					notifi.state = 0
					notifi.save()
					self.assignNotification(d, datee, 3)
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_cattle_id=d, state=2, module=0, name=3)
					except ObjectDoesNotExist:
						self.assignNotification(d, datee, 3)
						
		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2).count()
		for u in users:
			print "enviando a: ", u.username
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)


	def sendNotificationPajuela(self, desire_pajuelas):
		datee = date.today() + timedelta(days=3)
		one_day_before = date.today() - relativedelta(days=1)
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		configuration = Configuracion.objects.get(id=farm.configuracion_id)

		for d in desire_pajuelas:
			try:
				notifi = Notification.objects.get(ident_cattle_id=d, start_date=date.today(), end_date=datee, module=0, name=4 )
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_cattle_id=d, state=2, end_date=one_day_before, module=0, name=4)
					notifi.state = 0
					notifi.save()
					self.assignNotification(d, datee, 4)
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_cattle_id=d, state=2, module=0, name=4)
					except ObjectDoesNotExist:
						self.assignNotification(d, datee, 4)
						
		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2).count()
		for u in users:
			print "enviando a: ", u.username
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)				



class AgentReproduccion(spade.Agent.Agent):
	class BehaviourReproduccion(spade.Behaviour.OneShotBehaviour):
		def onStart(self):
			print "inicio del BehaviourReproduccion . . ."

		def _process(self):
			print "Inicio del proceso del BehaviourReproduccion"
			desire = DesireReproduccion()		
			belief = BeliefReproduccion()
			intention = IntentionReproduccion()
			
			if 0 in belief.beliefs:
				intention.sendNotificationCelo(desire.desire_celo)
				print "Notificación: desire_celo, Enviada"
			if 1 in belief.beliefs:
				intention.sendNotificationService(desire.desire_service)
				print "Notificación: desire_service, Enviada"
			if 2 in belief.beliefs:
				intention.sendNotificationVerification(desire.desire_verification)
				print "Notificación: desire_verification, Enviada"
			if 3 in belief.beliefs:
				intention.sendNotificationParto(desire.desire_parto)
				print "Notificación: desire_parto, Enviada"
			if 4 in belief.beliefs:
				intention.sendNotificationPajuela(desire.desire_pajuelas)
				print "Notificación: desire_pajuelas, Enviada"
			
		def onEnd(self):
			print "fin del BehaviourReproduccion . . ."
			sys.exit(0)

	def _setup(self):
		print "Inicio del AgentReproduccion . . ."
		b = self.BehaviourReproduccion()
		self.addBehaviour(b, None)


@login_required
def ajaxRefresh(request):
	user = request.user
	global user_name
	user_name = user.id

	p = AgentProduccion("agent_produccion@127.0.0.1", "secret")
	p.start()

	s = AgentSanidad("agent_sanidad@127.0.0.1", "secret")
	s.start()

	a = AgentAlimentacion("agent_alimentacion@127.0.0.1", "secret")
	a.start()

	r = AgentReproduccion("agent_reproduccion@127.0.0.1", "secret")
	r.start()

	data = serializers.serialize('json', '')

	return HttpResponse(data, mimetype='application/json')