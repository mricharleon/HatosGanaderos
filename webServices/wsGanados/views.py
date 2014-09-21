#-*- coding: utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse
from ganados.models import Ganado, Identificacion_Simple, Ganaderia, Etapa, Identificacion_Ecuador, Ciclo, Verification
from medicament.models import Medicament
from alimentos.models import Food, ApplicationFood
from profiles.models import Configuracion

from django.contrib.auth.models import User

from django.core import serializers
from django.utils import simplejson as json
from ganados.models import Celo, LoadTest

from django.contrib.auth.decorators import login_required

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
def wsGanadosMachos_view(request):
	search = request.GET['search']
	user = request.user
	id_user = User.objects.filter(username=user.username)
	ganaderia = Ganaderia.objects.get(perfil=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)
	
	gg = Ganado.objects.filter(ganaderia=ganaderia)
	#gg = Ganado.objects.filter(ganaderia_id=ganaderia.id).filter()

	if configuracion.tipo_identificacion == 'simple' and search != '':
		data = serializers.serialize('json', Identificacion_Simple.objects.filter(
					  (Q(identificaciones_simples__ganaderia=ganaderia)
					  ) &
					  (	Q(identificaciones_simples__nacimiento__icontains=search) |
					  	Q(rp__iexact=search) |
					  	Q(nombre__icontains=search)
					  ) &
					  	Q(identificaciones_simples__genero__exact=0)
		))
	else:
		data = serializers.serialize('json', Identificacion_Ecuador.objects.filter(
					  (Q(identificaciones_ecuador__ganaderia=ganaderia)
					  ) &
					  (	Q(identificaciones_ecuador__nacimiento__icontains=search) |
					  	Q(rp__iexact=search) |
					  	Q(nombre__icontains=search)
					  ) &
					  	Q(identificaciones_ecuador__genero__exact=0)
		))
	return HttpResponse(data, mimetype='application/json')

@login_required
def wsGanados_view(request):
	search = request.GET['search']
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)
	
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
		data += '"imagen": "'+ str(g.imagen) +'"'
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
	
	'''
	reigistros = LoadTest.objects.all()
	datas = serializers.serialize('json', reigistros, indent=2)
	'''
	
	return HttpResponse(data, mimetype='application/json')

@login_required
def wsGanadosProduccion_view(request):
	search = request.GET['search']
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)

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
		data += '"imagen": "'+ str(g.imagen) +'"'
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
def ajaxAssignCattleFood_view(request):
	search = request.GET['search']
	listCattle = str(request.GET['listCattle'])
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)
	
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
		data += '"imagen": "'+ str(g.imagen) +'"'
		data += ', "nombre": "'+ g.identificacion_simple.nombre +'"'
		data += ', "edad_anios": '+ str(g.edad_anios )
		data += ', "edad_meses": '+ str(g.edad_meses )
		data += ', "edad_dias": '+ str(g.edad_dias )

		data += '}}'
	data += ']'

	return HttpResponse(data, mimetype='application/json')


import datetime

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

