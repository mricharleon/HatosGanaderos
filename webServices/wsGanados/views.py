#-*- coding: utf-8 -*-
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from ganados.models import Ganado, Identificacion_Simple, Ganaderia, Etapa, Identificacion_Ecuador, Ciclo, Verification, Insemination, Ordenio, DeferEtapa, Celo, ProblemaGestacion
from medicament.models import Medicament
from alimentos.models import Food, ApplicationFood
from medicament.models import Medicament, ApplicationMedicament
from notifications.models import Notification
from profiles.models import Configuracion, Profile, Ganaderia
from ganados.views import calcula_edad_anios, calcula_edad_meses, calcula_edad_dias
from django.shortcuts import redirect, HttpResponseRedirect

from django.contrib.auth.models import User

from django.core import serializers
from django.utils import simplejson as json

from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
import datetime
from dateutil.relativedelta import relativedelta

from drealtime import iShoutClient
ishout_client = iShoutClient()
from django.contrib.auth.models import User

import pytz
from dateutil.tz import *

# var aux
user_name = 0


@login_required
def wsGanadosHembras_view(request):
	search = request.GET['search']
	user = request.user
	id_user = User.objects.filter(username=user.username)
	ganaderia = Ganaderia.objects.get(perfil=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)


	if configuracion.tipo_identificacion == 'simple':
		data = serializers.serialize('json', Identificacion_Simple.objects.filter(
					  (Q(identificaciones_simples__ganaderia=ganaderia)
					  ) &
					  (	Q(identificaciones_simples__nacimiento__icontains=search) |
					  	Q(rp__iexact=search) |
					  	Q(nombre__icontains=search)
					  ) &
					    Q(identificaciones_simples__etapas__is_active__exact=True,
					    identificaciones_simples__genero__exact=1 )
		))
	elif configuracion.tipo_identificacion == 'norma_ecuador':
		data = serializers.serialize('json', Identificacion_Ecuador.objects.filter(
					  (Q(identificaciones_ecuador__ganaderia=ganaderia)
					  ) &
					  (	Q(identificaciones_ecuador__nacimiento__icontains=search) |
					  	Q(rp__iexact=search) |
					  	Q(nombre__icontains=search)
					  ) &
					    Q(identificaciones_ecuador__etapas__is_active__exact=True,
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
											Q(ganaderia=ganaderia, genero=1, down_cattle=None) &
											(
												Q(nacimiento__icontains=search) |
												Q(identificacion_simple__nombre__icontains=search) |
												Q(identificacion_simple__rp__icontains=search)
											)
										).order_by('id')

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
						data += ', "etapa": "Vacona media"'
					elif e.nombre == 2:
						data += ', "etapa": "Vacona fierro"'
					elif e.nombre == 3:
						data += ', "etapa": "Vacona vientre"'
					elif e.nombre == 4:
						data += ', "etapa": "Vaca"'

			number_cycle = 0
			for ciclo in ciclos:
				if ciclo.ganado_id == g.id and ciclo.is_active:
					if ciclo.nombre == 0:
						data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
					elif ciclo.nombre == 1:
						data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
					elif ciclo.nombre == 2:
						data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
					elif ciclo.nombre == 3:
						data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
					number_cycle += 1

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
						data += ', "etapa": "Vacona media"'
					elif e.nombre == 2:
						data += ', "etapa": "Vacona fierro"'
					elif e.nombre == 3:
						data += ', "etapa": "Vacona vientre"'
					elif e.nombre == 4:
						data += ', "etapa": "Vaca"'

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
def ajaxDownCattle_view(request):
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
										).exclude(down_cattle=None).order_by('id')

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
						data += ', "etapa": "Vacona media"'
					elif e.nombre == 2:
						data += ', "etapa": "Vacona fierro"'
					elif e.nombre == 3:
						data += ', "etapa": "Vacona vientre"'
					elif e.nombre == 4:
						data += ', "etapa": "Vaca"'

			number_cycle = 0
			for ciclo in ciclos:
				if ciclo.ganado_id == g.id and ciclo.is_active:
					if ciclo.nombre == 0:
						data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
					elif ciclo.nombre == 1:
						data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
					elif ciclo.nombre == 2:
						data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
					elif ciclo.nombre == 3:
						data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
					number_cycle += 1

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
						data += ', "etapa": "Vacona media"'
					elif e.nombre == 2:
						data += ', "etapa": "Vacona fierro"'
					elif e.nombre == 3:
						data += ', "etapa": "Vacona vientre"'
					elif e.nombre == 4:
						data += ', "etapa": "Vaca"'

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
def wsGanadosTerneras_view(request):
	search = request.GET['search']
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)

	if ganaderia.configuracion.tipo_identificacion == 'simple':

		ganados = Ganado.objects.filter(
											Q(ganaderia=ganaderia, genero=1, down_cattle=None, etapas__nombre__iexact='0', etapas__is_active=True ) &
											(
												Q(nacimiento__icontains=search) |
												Q(identificacion_simple__nombre__icontains=search) |
												Q(identificacion_simple__rp__icontains=search)
											)
										).order_by('id')

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

			for e in etapas:
				if e.ganado_id == g.id:
					if e.nombre == 0:
						data += ', "etapa": "Ternera"'
					elif e.nombre == 1:
						data += ', "etapa": "Vacona media"'
					elif e.nombre == 2:
						data += ', "etapa": "Vacona fierro"'
					elif e.nombre == 3:
						data += ', "etapa": "Vacona vientre"'
					elif e.nombre == 4:
						data += ', "etapa": "Vaca"'

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
										Q(ganaderia=ganaderia, genero=1, etapas__nombre__iexact='0') &
										(
											Q(nacimiento__icontains=search) |
											Q(identificacion_ecuador__nombre__icontains=search) |
											Q(identificacion_ecuador__rp__icontains=search)
										)
									)

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


			for e in etapas:
				if e.ganado_id == g.id:
					if e.nombre == 0:
						data += ', "etapa": "Ternera"'
					elif e.nombre == 1:
						data += ', "etapa": "Vacona media"'
					elif e.nombre == 2:
						data += ', "etapa": "Vacona fierro"'
					elif e.nombre == 3:
						data += ', "etapa": "Vacona vientre"'
					elif e.nombre == 4:
						data += ', "etapa": "Vaca"'

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
def wsGanadosMedia_view(request):
	search = request.GET['search']
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)

	if ganaderia.configuracion.tipo_identificacion == 'simple':

		ganados = Ganado.objects.filter(
											Q(ganaderia=ganaderia, genero=1, down_cattle=None, etapas__nombre__iexact='1', etapas__is_active=True ) &
											(
												Q(nacimiento__icontains=search) |
												Q(identificacion_simple__nombre__icontains=search) |
												Q(identificacion_simple__rp__icontains=search)
											)
										).order_by('id')

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


			for e in etapas:
				if e.ganado_id == g.id:
					if e.nombre == 0:
						data += ', "etapa": "Ternera"'
					elif e.nombre == 1:
						data += ', "etapa": "Vacona media"'
					elif e.nombre == 2:
						data += ', "etapa": "Vacona fierro"'
					elif e.nombre == 3:
						data += ', "etapa": "Vacona vientre"'
					elif e.nombre == 4:
						data += ', "etapa": "Vaca"'

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
										Q(ganaderia=ganaderia, genero=1, etapas__nombre__iexact='1') &
										(
											Q(nacimiento__icontains=search) |
											Q(identificacion_ecuador__nombre__icontains=search) |
											Q(identificacion_ecuador__rp__icontains=search)
										)
									)

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


			for e in etapas:
				if e.ganado_id == g.id:
					if e.nombre == 0:
						data += ', "etapa": "Ternera"'
					elif e.nombre == 1:
						data += ', "etapa": "Vacona media"'
					elif e.nombre == 2:
						data += ', "etapa": "Vacona fierro"'
					elif e.nombre == 3:
						data += ', "etapa": "Vacona vientre"'
					elif e.nombre == 4:
						data += ', "etapa": "Vaca"'

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
def wsGanadosFierro_view(request):
	search = request.GET['search']
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)

	if ganaderia.configuracion.tipo_identificacion == 'simple':

		ganados = Ganado.objects.filter(
											Q(ganaderia=ganaderia, genero=1, down_cattle=None, etapas__nombre__iexact='2', etapas__is_active=True ) &
											(
												Q(nacimiento__icontains=search) |
												Q(identificacion_simple__nombre__icontains=search) |
												Q(identificacion_simple__rp__icontains=search)
											)
										).order_by('id')

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


			for e in etapas:
				if e.ganado_id == g.id:
					if e.nombre == 0:
						data += ', "etapa": "Ternera"'
					elif e.nombre == 1:
						data += ', "etapa": "Vacona media"'
					elif e.nombre == 2:
						data += ', "etapa": "Vacona fierro"'
					elif e.nombre == 3:
						data += ', "etapa": "Vacona vientre"'
					elif e.nombre == 4:
						data += ', "etapa": "Vaca"'

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
										Q(ganaderia=ganaderia, genero=1, etapas__nombre__iexact='2') &
										(
											Q(nacimiento__icontains=search) |
											Q(identificacion_ecuador__nombre__icontains=search) |
											Q(identificacion_ecuador__rp__icontains=search)
										)
									)

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


			for e in etapas:
				if e.ganado_id == g.id:
					if e.nombre == 0:
						data += ', "etapa": "Ternera"'
					elif e.nombre == 1:
						data += ', "etapa": "Vacona media"'
					elif e.nombre == 2:
						data += ', "etapa": "Vacona fierro"'
					elif e.nombre == 3:
						data += ', "etapa": "Vacona vientre"'
					elif e.nombre == 4:
						data += ', "etapa": "Vaca"'

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
def wsGanadosVientre_view(request):
	search = request.GET['search']
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)

	if ganaderia.configuracion.tipo_identificacion == 'simple':

		ganados = Ganado.objects.filter(
											Q(ganaderia=ganaderia, genero=1, down_cattle=None, etapas__nombre__iexact='3', etapas__is_active=True ) &
											(
												Q(nacimiento__icontains=search) |
												Q(identificacion_simple__nombre__icontains=search) |
												Q(identificacion_simple__rp__icontains=search)
											)
										).order_by('id')

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
						data += ', "etapa": "Vacona media"'
					elif e.nombre == 2:
						data += ', "etapa": "Vacona fierro"'
					elif e.nombre == 3:
						data += ', "etapa": "Vacona vientre"'
					elif e.nombre == 4:
						data += ', "etapa": "Vaca"'

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
										Q(ganaderia=ganaderia, genero=1, etapas__nombre__iexact='3') &
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
						data += ', "etapa": "Vacona media"'
					elif e.nombre == 2:
						data += ', "etapa": "Vacona fierro"'
					elif e.nombre == 3:
						data += ', "etapa": "Vacona vientre"'
					elif e.nombre == 4:
						data += ', "etapa": "Vaca"'

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
def wsGanadosVaca_view(request):
	search = request.GET['search']
	user = request.user
	ganaderia = Ganaderia.objects.get(perfil=user)

	if ganaderia.configuracion.tipo_identificacion == 'simple':

		ganados = Ganado.objects.filter(
											Q(ganaderia=ganaderia, genero=1, down_cattle=None, etapas__nombre__iexact='4', etapas__is_active=True ) &
											(
												Q(nacimiento__icontains=search) |
												Q(identificacion_simple__nombre__icontains=search) |
												Q(identificacion_simple__rp__icontains=search)
											)
										).order_by('id')

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
						data += ', "etapa": "Vacona media"'
					elif e.nombre == 2:
						data += ', "etapa": "Vacona fierro"'
					elif e.nombre == 3:
						data += ', "etapa": "Vacona vientre"'
					elif e.nombre == 4:
						data += ', "etapa": "Vaca"'

			number_cycle = 0
			for ciclo in ciclos:
				if ciclo.ganado_id == g.id and ciclo.is_active:
					if ciclo.nombre == 0:
						data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
					elif ciclo.nombre == 1:
						data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
					elif ciclo.nombre == 2:
						data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
					elif ciclo.nombre == 3:
						data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
					number_cycle += 1

			for verificacion in verificaciones:
				if verificacion.cattle_id == g.id and verificacion.is_active:
					data += ', "verificacion": "True"'
				else:
					data += ', "verificacion": "False"'


			data += '}}'
		data += ']'

	else:
		ganados = Ganado.objects.filter(
										Q(ganaderia=ganaderia, genero=1, etapas__nombre__iexact='4') &
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
						data += ', "etapa": "Vacona media"'
					elif e.nombre == 2:
						data += ', "etapa": "Vacona fierro"'
					elif e.nombre == 3:
						data += ', "etapa": "Vacona vientre"'
					elif e.nombre == 4:
						data += ', "etapa": "Vaca"'

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
											Q(ganaderia=ganaderia, genero=0, down_cattle=None) &
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
											Q(ganaderia=ganaderia, genero=1, ciclos__nombre=2, ciclos__is_active=True) &
											(
												Q(identificacion_simple__rp__icontains=search) |
												Q(nacimiento__icontains =search) |
												Q(identificacion_simple__nombre__icontains=search)
											) &
											(
												Q(etapas__nombre=3, etapas__is_active=True) |
												Q(etapas__nombre=4, etapas__is_active=True)
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
						data += ', "etapa": "Vacona Media"'
					elif e.nombre == 2:
						data += ', "etapa": "Vacona Fierro"'
					elif e.nombre == 3:
						data += ', "etapa": "Vacona Vientre"'
					elif e.nombre == 4:
						data += ', "etapa": "Vaca"'

			number_cycle = 0
			for ciclo in ciclos:
				if ciclo.ganado_id == g.id and ciclo.is_active:
					if ciclo.nombre == 0:
						data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
					elif ciclo.nombre == 1:
						data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
					elif ciclo.nombre == 2:
						data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
					elif ciclo.nombre == 3:
						data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
					number_cycle += 1

			for verificacion in verificaciones:
				if verificacion.cattle_id == g.id and verificacion.is_active:
					data += ', "verificacion": "True"'
				else:
					data += ', "verificacion": "False"'

			data += '}}'
		data += ']'

	else:
		ganados = Ganado.objects.filter(
										Q(ganaderia=ganaderia, genero=1, etapas__nombre=2, ciclos__nombre=2, ciclos__is_active=True) &
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
						data += ', "etapa": "Vacona Media"'
					elif e.nombre == 2:
						data += ', "etapa": "Vacona Fierro"'
					elif e.nombre == 3:
						data += ', "etapa": "Vacona Vientre"'
					elif e.nombre == 4:
						data += ', "etapa": "Vaca"'

			if ciclos.count() > 0:
				number_cycle = 0
				for ciclo in ciclos:
					if ciclo.ganado_id == g.id and ciclo.is_active:
						if ciclo.nombre == 0:
							data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
						elif ciclo.nombre == 1:
							data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
						elif ciclo.nombre == 2:
							data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
						elif ciclo.nombre == 3:
							data += ', "ciclo'+str(number_cycle)+'": '+ str(ciclo.nombre)
						number_cycle += 1

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
									).order_by('name')
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
	for m in foods:
		if data == '[':
			data += '{"pk": ' + str(m.id) + ', '
		else:
			data += ',{"pk": ' + str(m.id) + ', '
		data += '"fields": {'
		data += '"name": "'+ str(m.name) +'"'
		data += ', "expiration_date": "'+ str(m.expiration_date) +'"'
		data += ', "phase": "'+ str(m.phase) +'"'
		data += ', "amount": "'+ str(m.amount) +'"'
		data += ', "unit": "'+ str(m.unit) +'"'
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
											Q(ganaderia=ganaderia, down_cattle=None) &
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
											Q(ganaderia=ganaderia, down_cattle=None) &
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
											Q(ganaderia=ganaderia, down_cattle=None) &
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
				  (Q(farm=farm, down_insemination=None)) &
				  (	Q(registration_date__icontains=search) |
				  	Q(rp__iexact=search) |
				  	Q(name__icontains=search)
				  )
	).order_by('-rp'))

	return HttpResponse(data, mimetype='application/json')


@login_required
def ajaxAddListNotificationsProduccionRealizadas(request):
	number_search = request.GET['number_search']
	user = request.user
	farm = Ganaderia.objects.get(perfil=user)

	if farm.configuracion.tipo_identificacion == 'simple':
		notificaciones = Notification.objects.filter( state=1, module=3, farm=farm ).order_by('-end_date')
		if int(notificaciones.count()) <= (int(number_search) + 5):
			notificaciones = Notification.objects.filter( state=1, module=3, farm=farm ).order_by('-end_date')[int(number_search):int(notificaciones.count())]
			hide_button = '1'
		else:
			notificaciones = Notification.objects.filter( state=1, module=3, farm=farm ).order_by('-end_date')[int(number_search):(int(number_search)+5)]
			hide_button = '0'

		# serializando
		data = '['
		for n in notificaciones:
			if data == '[':
				data += '{"pk": ' + str(n.id) + ', '
			else:
				data += ',{"pk": ' + str(n.id) + ', '
			data += '"fields": {'
			data += '"name": "'+ n.get_name_display() +'"'
			data += ', "cattle": "'+ n.ident_cattle.identificacion_simple.nombre +'"'
			data += ', "cattle_rp": "'+ str(n.ident_cattle.identificacion_simple.rp) +'"'
			data += ', "inicio": "'+str(n.start_date)+'"'
			data += ', "fin": "'+str(n.end_date)+'"'
			data += ', "hide_button": "' + hide_button + '"'


			data += '}}'
		data += ']'

	else:
		notificaciones = Notification.objects.filter( state=1, module=3, farm=farm ).order_by('-end_date')
		# serializando
		data = '['
		for n in notificaciones:
			if data == '[':
				data += '{"pk": ' + str(n.id) + ', '
			else:
				data += ',{"pk": ' + str(n.id) + ', '
			data += '"fields": {'
			data += '"name": "'+ n.get_name_display() +'"'
			data += ', "cattle": "'+ n.ident_cattle.identificacion_ecuador.nombre +'"'
			data += ', "cattle_rp": "'+ str(n.ident_cattle.identificacion_ecuador.rp) +'"'
			data += ', "inicio": '+ str(n.start_date )
			data += ', "fin": '+ str(n.end_date )

			data += '}}'
		data += ']'

	return HttpResponse(data, mimetype='application/json; charset=utf-8')


@login_required
def ajaxAddListNotificationsProduccionNoRealizadas(request):
	number_search = request.GET['number_search']
	user = request.user
	farm = Ganaderia.objects.get(perfil=user)

	if farm.configuracion.tipo_identificacion == 'simple':
		notificaciones = Notification.objects.filter( state=0, module=3, farm=farm ).order_by('-end_date')
		if int(notificaciones.count()) <= (int(number_search) + 5):
			notificaciones = Notification.objects.filter( state=0, module=3, farm=farm ).order_by('-end_date')[int(number_search):int(notificaciones.count())]
			hide_button = '1'
		else:
			notificaciones = Notification.objects.filter( state=0, module=3, farm=farm ).order_by('-end_date')[int(number_search):(int(number_search)+5)]
			hide_button = '0'

		# serializando
		data = '['
		for n in notificaciones:
			if data == '[':
				data += '{"pk": ' + str(n.id) + ', '
			else:
				data += ',{"pk": ' + str(n.id) + ', '
			data += '"fields": {'
			data += '"name": "'+ n.get_name_display() +'"'
			data += ', "cattle": "'+ n.ident_cattle.identificacion_simple.nombre +'"'
			data += ', "cattle_rp": "'+ str(n.ident_cattle.identificacion_simple.rp) +'"'
			data += ', "inicio": "'+str(n.start_date)+'"'
			data += ', "fin": "'+str(n.end_date)+'"'
			data += ', "hide_button": "' + hide_button + '"'


			data += '}}'
		data += ']'

	else:
		notificaciones = Notification.objects.filter( state=0, module=3, farm=farm ).order_by('-end_date')
		# serializando
		data = '['
		for n in notificaciones:
			if data == '[':
				data += '{"pk": ' + str(n.id) + ', '
			else:
				data += ',{"pk": ' + str(n.id) + ', '
			data += '"fields": {'
			data += '"name": "'+ n.get_name_display() +'"'
			data += ', "cattle": "'+ n.ident_cattle.identificacion_ecuador.nombre +'"'
			data += ', "cattle_rp": "'+ str(n.ident_cattle.identificacion_ecuador.rp) +'"'
			data += ', "inicio": '+ str(n.start_date )
			data += ', "fin": '+ str(n.end_date )

			data += '}}'
		data += ']'

	return HttpResponse(data, mimetype='application/json; charset=utf-8')



@login_required
def ajaxAddListNotificationsReproduccionRealizadas(request):
	number_search = request.GET['number_search']
	user = request.user
	farm = Ganaderia.objects.get(perfil=user)

	if farm.configuracion.tipo_identificacion == 'simple':
		notificaciones = Notification.objects.filter( state=1, module=0, farm=farm ).order_by('-end_date')
		if int(notificaciones.count()) <= (int(number_search) + 5):
			notificaciones = Notification.objects.filter( state=1, module=0, farm=farm ).order_by('-end_date')[int(number_search):int(notificaciones.count())]
			hide_button = '1'
		else:
			notificaciones = Notification.objects.filter( state=1, module=0, farm=farm ).order_by('-end_date')[int(number_search):(int(number_search)+5)]
			hide_button = '0'

		# serializando
		data = '['
		for n in notificaciones:
			if data == '[':
				data += '{"pk": ' + str(n.id) + ', '
			else:
				data += ',{"pk": ' + str(n.id) + ', '
			data += '"fields": {'
			data += '"name": "'+ n.get_name_display() +'"'
			data += ', "cattle": "'+ n.ident_cattle.identificacion_simple.nombre +'"'
			data += ', "cattle_rp": "'+ str(n.ident_cattle.identificacion_simple.rp) +'"'
			data += ', "inicio": "'+str(n.start_date)+'"'
			data += ', "fin": "'+str(n.end_date)+'"'
			data += ', "hide_button": "' + hide_button + '"'


			data += '}}'
		data += ']'

	else:
		notificaciones = Notification.objects.filter( state=1, module=0, farm=farm ).order_by('-end_date')
		# serializando
		data = '['
		for n in notificaciones:
			if data == '[':
				data += '{"pk": ' + str(n.id) + ', '
			else:
				data += ',{"pk": ' + str(n.id) + ', '
			data += '"fields": {'
			data += '"name": "'+ n.get_name_display() +'"'
			data += ', "cattle": "'+ n.ident_cattle.identificacion_ecuador.nombre +'"'
			data += ', "cattle_rp": "'+ str(n.ident_cattle.identificacion_ecuador.rp) +'"'
			data += ', "inicio": '+ str(n.start_date )
			data += ', "fin": '+ str(n.end_date )

			data += '}}'
		data += ']'

	return HttpResponse(data, mimetype='application/json; charset=utf-8')


@login_required
def ajaxAddListNotificationsReproduccionNoRealizadas(request):
	number_search = request.GET['number_search']
	user = request.user
	farm = Ganaderia.objects.get(perfil=user)

	if farm.configuracion.tipo_identificacion == 'simple':
		notificaciones = Notification.objects.filter( state=0, module=0, farm=farm ).order_by('-end_date')
		if int(notificaciones.count()) <= (int(number_search) + 5):
			notificaciones = Notification.objects.filter( state=0, module=0, farm=farm ).order_by('-end_date')[int(number_search):int(notificaciones.count())]
			hide_button = '1'
		else:
			notificaciones = Notification.objects.filter( state=0, module=0, farm=farm ).order_by('-end_date')[int(number_search):(int(number_search)+5)]
			hide_button = '0'

		# serializando
		data = '['
		for n in notificaciones:
			if data == '[':
				data += '{"pk": ' + str(n.id) + ', '
			else:
				data += ',{"pk": ' + str(n.id) + ', '
			data += '"fields": {'
			data += '"name": "'+ n.get_name_display() +'"'
			data += ', "cattle": "'+ n.ident_cattle.identificacion_simple.nombre +'"'
			data += ', "cattle_rp": "'+ str(n.ident_cattle.identificacion_simple.rp) +'"'
			data += ', "inicio": "'+str(n.start_date)+'"'
			data += ', "fin": "'+str(n.end_date)+'"'
			data += ', "hide_button": "' + hide_button + '"'


			data += '}}'
		data += ']'

	else:
		notificaciones = Notification.objects.filter( state=1, module=0, farm=farm ).order_by('-end_date')
		# serializando
		data = '['
		for n in notificaciones:
			if data == '[':
				data += '{"pk": ' + str(n.id) + ', '
			else:
				data += ',{"pk": ' + str(n.id) + ', '
			data += '"fields": {'
			data += '"name": "'+ n.get_name_display() +'"'
			data += ', "cattle": "'+ n.ident_cattle.identificacion_ecuador.nombre +'"'
			data += ', "cattle_rp": "'+ str(n.ident_cattle.identificacion_ecuador.rp) +'"'
			data += ', "inicio": '+ str(n.start_date )
			data += ', "fin": '+ str(n.end_date )

			data += '}}'
		data += ']'

	return HttpResponse(data, mimetype='application/json; charset=utf-8')


@login_required
def ajaxAddListNotificationsSanidadNoRealizadas(request):
	number_search = request.GET['number_search']
	user = request.user
	farm = Ganaderia.objects.get(perfil=user)

	if farm.configuracion.tipo_identificacion == 'simple':
		notificaciones = Notification.objects.filter( state=0, module=2, farm=farm ).order_by('-end_date')
		if int(notificaciones.count()) <= (int(number_search) + 5):
			notificaciones = Notification.objects.filter( state=0, module=2, farm=farm ).order_by('-end_date')[int(number_search):int(notificaciones.count())]
			hide_button = '1'
		else:
			notificaciones = Notification.objects.filter( state=0, module=2, farm=farm ).order_by('-end_date')[int(number_search):(int(number_search)+5)]
			hide_button = '0'

		# serializando
		data = '['
		for n in notificaciones:
			if data == '[':
				data += '{"pk": ' + str(n.id) + ', '
			else:
				data += ',{"pk": ' + str(n.id) + ', '
			data += '"fields": {'
			data += '"name": "'+ n.get_name_display() +'"'
			data += ', "name_medicament": "'+ n.ident_medicament.name +'"'
			data += ', "expiration_date": "'+ str(n.ident_medicament.expiration_date) +'"'
			data += ', "unit": "'+ n.ident_medicament.get_unit_display() +'"'
			data += ', "amount": "'+ str(n.ident_medicament.amount) +'"'
			if ((n.name==10)|(n.name==11)):
				data += ', "cattle": "'+ n.ident_cattle.identificacion_simple.nombre +'"'
				data += ', "cattle_rp": "'+ str(n.ident_cattle.identificacion_simple.rp) +'"'
			else:
				data += ', "cattle": "'+'"'
				data += ', "cattle_rp": "'+'"'
			data += ', "inicio": "'+str(n.start_date)+'"'
			data += ', "fin": "'+str(n.end_date)+'"'
			data += ', "hide_button": "' + hide_button + '"'


			data += '}}'
		data += ']'

	else:
		notificaciones = Notification.objects.filter( state=0, module=0, farm=farm ).order_by('-end_date')
		# serializando
		data = '['
		for n in notificaciones:
			if data == '[':
				data += '{"pk": ' + str(n.id) + ', '
			else:
				data += ',{"pk": ' + str(n.id) + ', '
			data += '"fields": {'
			data += '"name": "'+ n.get_name_display() +'"'
			data += ', "name_medicament": "'+ n.ident_medicament.name +'"'
			data += ', "expiration_date": "'+ str(n.ident_medicament.expiration_date) +'"'
			data += ', "unit": "'+ n.ident_medicament.get_unit_display() +'"'
			data += ', "amount": "'+ str(n.ident_medicament.amount) +'"'
			if ((n.name==10)|(n.name==11)):
				data += ', "cattle": "'+ n.ident_cattle.identificacion_ecuador.nombre +'"'
				data += ', "cattle_rp": "'+ str(n.ident_cattle.identificacion_ecuador.rp) +'"'
			else:
				data += ', "cattle": "'+'"'
				data += ', "cattle_rp": "'+'"'
			data += ', "inicio": '+ str(n.start_date )
			data += ', "fin": '+ str(n.end_date )

			data += '}}'
		data += ']'

	return HttpResponse(data, mimetype='application/json; charset=utf-8')

@login_required
def ajaxAddListNotificationsSanidadRealizadas(request):
	number_search = request.GET['number_search']
	user = request.user
	farm = Ganaderia.objects.get(perfil=user)

	if farm.configuracion.tipo_identificacion == 'simple':
		notificaciones = Notification.objects.filter( state=1, module=2, farm=farm ).order_by('-end_date')
		if int(notificaciones.count()) <= (int(number_search) + 5):
			notificaciones = Notification.objects.filter( state=1, module=2, farm=farm ).order_by('-end_date')[int(number_search):int(notificaciones.count())]
			hide_button = '1'
		else:
			notificaciones = Notification.objects.filter( state=1, module=2, farm=farm ).order_by('-end_date')[int(number_search):(int(number_search)+5)]
			hide_button = '0'

		# serializando
		data = '['
		for n in notificaciones:
			if data == '[':
				data += '{"pk": ' + str(n.id) + ', '
			else:
				data += ',{"pk": ' + str(n.id) + ', '
			data += '"fields": {'
			data += '"name": "'+ n.get_name_display() +'"'
			data += ', "name_medicament": "'+ n.ident_medicament.name +'"'
			data += ', "expiration_date": "'+ str(n.ident_medicament.expiration_date) +'"'
			data += ', "unit": "'+ n.ident_medicament.get_unit_display() +'"'
			data += ', "amount": "'+ str(n.ident_medicament.amount) +'"'
			if ((n.name==10)|(n.name==11)):
				data += ', "cattle": "'+ n.ident_cattle.identificacion_simple.nombre +'"'
				data += ', "cattle_rp": "'+ str(n.ident_cattle.identificacion_simple.rp) +'"'
			else:
				data += ', "cattle": "'+'"'
				data += ', "cattle_rp": "'+'"'
			data += ', "inicio": "'+str(n.start_date)+'"'
			data += ', "fin": "'+str(n.end_date)+'"'
			data += ', "hide_button": "' + hide_button + '"'


			data += '}}'
		data += ']'

	else:
		notificaciones = Notification.objects.filter( state=1, module=2, farm=farm ).order_by('-end_date')
		# serializando
		data = '['
		for n in notificaciones:
			if data == '[':
				data += '{"pk": ' + str(n.id) + ', '
			else:
				data += ',{"pk": ' + str(n.id) + ', '
			data += '"fields": {'
			data += '"name": "'+ n.get_name_display() +'"'
			data += ', "name_medicament": "'+ n.ident_medicament.name +'"'
			data += ', "expiration_date": "'+ str(n.ident_medicament.expiration_date) +'"'
			data += ', "unit": "'+ n.ident_medicament.get_unit_display() +'"'
			data += ', "amount": "'+ str(n.ident_medicament.amount) +'"'
			if ((n.name==10)|(n.name==11)):
				data += ', "cattle": "'+ n.ident_cattle.identificacion_ecuador.nombre +'"'
				data += ', "cattle_rp": "'+ str(n.ident_cattle.identificacion_ecuador.rp) +'"'
			else:
				data += ', "cattle": "'+'"'
				data += ', "cattle_rp": "'+'"'
			data += ', "inicio": '+ str(n.start_date )
			data += ', "fin": '+ str(n.end_date )

			data += '}}'
		data += ']'

	return HttpResponse(data, mimetype='application/json; charset=utf-8')



@login_required
def ajaxAddListNotificationsAlimentacionNoRealizadas(request):
	number_search = request.GET['number_search']
	user = request.user
	farm = Ganaderia.objects.get(perfil=user)

	if farm.configuracion.tipo_identificacion == 'simple':
		notificaciones = Notification.objects.filter( state=0, module=1, farm=farm ).order_by('-end_date')
		if int(notificaciones.count()) <= (int(number_search) + 5):
			notificaciones = Notification.objects.filter( state=0, module=1, farm=farm ).order_by('-end_date')[int(number_search):int(notificaciones.count())]
			hide_button = '1'
		else:
			notificaciones = Notification.objects.filter( state=0, module=1, farm=farm ).order_by('-end_date')[int(number_search):(int(number_search)+5)]
			hide_button = '0'

		# serializando
		data = '['
		for n in notificaciones:
			if data == '[':
				data += '{"pk": ' + str(n.id) + ', '
			else:
				data += ',{"pk": ' + str(n.id) + ', '
			data += '"fields": {'
			data += '"name": "'+ n.get_name_display() +'"'
			data += ', "name_food": "'+ n.ident_food.name +'"'
			data += ', "expiration_date": "'+ str(n.ident_food.expiration_date) +'"'
			data += ', "unit": "'+ n.ident_food.get_unit_display() +'"'
			data += ', "amount": "'+ str(n.ident_food.amount) +'"'
			if (n.name==14):
				data += ', "cattle": "'+ n.ident_cattle.identificacion_simple.nombre +'"'
				data += ', "cattle_rp": "'+ str(n.ident_cattle.identificacion_simple.rp) +'"'
			else:
				data += ', "cattle": "'+'"'
				data += ', "cattle_rp": "'+'"'
			data += ', "inicio": "'+str(n.start_date)+'"'
			data += ', "fin": "'+str(n.end_date)+'"'
			data += ', "hide_button": "' + hide_button + '"'


			data += '}}'
		data += ']'

	else:
		notificaciones = Notification.objects.filter( state=0, module=1, farm=farm ).order_by('-end_date')
		# serializando
		data = '['
		for n in notificaciones:
			if data == '[':
				data += '{"pk": ' + str(n.id) + ', '
			else:
				data += ',{"pk": ' + str(n.id) + ', '
			data += '"fields": {'
			data += '"name": "'+ n.get_name_display() +'"'
			data += ', "name_food": "'+ n.ident_food.name +'"'
			data += ', "expiration_date": "'+ str(n.ident_food.expiration_date) +'"'
			data += ', "unit": "'+ n.ident_food.get_unit_display() +'"'
			data += ', "amount": "'+ str(n.ident_food.amount) +'"'
			if (n.name==14):
				data += ', "cattle": "'+ n.ident_cattle.identificacion_ecuador.nombre +'"'
				data += ', "cattle_rp": "'+ str(n.ident_cattle.identificacion_ecuador.rp) +'"'
			else:
				data += ', "cattle": "'+'"'
				data += ', "cattle_rp": "'+'"'
			data += ', "inicio": '+ str(n.start_date )
			data += ', "fin": '+ str(n.end_date )

			data += '}}'
		data += ']'

	return HttpResponse(data, mimetype='application/json; charset=utf-8')







###############################################
###############################################
###############################################
###############################################
# INTELLIGENT AGENTS WITH SPADE


import spade
import datetime
import time
import sys


################################################
# Agente Sanidad
################################################
class BeliefSanidad:
	def __init__(self):
		self.beliefs_amount_vaccine = []
		self.beliefs_amount_wormer = []
		self.beliefs_expiration_vaccine = []
		self.beliefs_expiration_wormer = []
		self.beliefs_application_vaccine = []
		self.beliefs_application_vaccine2 = []
		self.beliefs_application_wormer = []
		self.beliefs_application_wormer2 = []

		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		medicament_vaccine = Medicament.objects.filter(farm=farm, amount__lt=30, is_vaccine=True)
		medicament_wormer = Medicament.objects.filter(farm=farm, amount__lt=30, is_wormer=True)
		medicament_expiration_vaccine = Medicament.objects.filter(farm=farm, is_vaccine=True)
		medicament_expiration_wormer = Medicament.objects.filter(farm=farm, is_wormer=True)

		for m in medicament_vaccine:
			self.beliefs_amount_vaccine.append(m.id)
		for m in medicament_wormer:
			self.beliefs_amount_wormer.append(m.id)

		date_expiration = date.today() + relativedelta(months=3)
		for m in medicament_expiration_vaccine:
			if m.expiration_date < date_expiration:
				self.beliefs_expiration_vaccine.append(m.id)
		for m in medicament_expiration_wormer:
			if m.expiration_date < date_expiration:
				self.beliefs_expiration_wormer.append(m.id)

		three_days_after = date.today() + relativedelta(days=3)
		one_day_before = date.today() - relativedelta(days=1)
		vaccines = Medicament.objects.filter(farm=farm, is_vaccine=True, is_active=True)
		wormers = Medicament.objects.filter(farm=farm, is_wormer=True, is_active=True)
		cattles = Ganado.objects.filter(ganaderia=farm, down_cattle=None)

		for v in vaccines: # recorre las vacunas
			for c in cattles: # recorre los ganados
				if v.option_number_application==0: # veces exactas de aplicar vacuna
					if ApplicationMedicament.objects.filter(cattle=c, medicament=v).count() > 0: # no es la primera vacuna
						av = ApplicationMedicament.objects.filter(cattle=c, medicament=v)
						av_final = av.reverse()[:1]
						
						if av.count() < v.number_application: # controla que no se pase del maximo de aplicaciones
							if v.time_interval==0: # comprueba que la vacuna siguiente sea en dias
								for i in range(av.count(), v.number_application+1): # recorre el numero total de aplicaciones que se deben dar
									date_now = av_final.date + relativedelta(days=(v.interval*i))
									if (date_now == three_days_after) | (date_now==one_day_before): # comprueba que sea el dia de aplicar
										self.beliefs_application_vaccine.append(v.id)
										self.beliefs_application_vaccine2.append(c.id)
										break # termina el for

							if v.time_interval==1: # comprueba que la vacuna siguiente sea en meses
								for i in range(av.count(), v.number_application+1): # recorre el numero total de aplicaciones que se deben dar
									date_now = av_final.date + relativedelta(months=(v.interval*i))
									if (date_now == three_days_after) | (date_now==one_day_before): # comprueba que sea el dia de aplicar
										self.beliefs_application_vaccine.append(v.id)
										self.beliefs_application_vaccine2.append(c.id)
										break # termina el for

							if v.time_interval==2: # comprueba que la vacuna siguiente sea en years
								for i in range(av.count(), v.number_application+1): # recorre el numero total de aplicaciones que se deben dar
									date_now = av_final.date + relativedelta(years=(v.interval*i))
									if (date_now == three_days_after) | (date_now==one_day_before): # comprueba que sea el dia de aplicar
										self.beliefs_application_vaccine.append(v.id)
										self.beliefs_application_vaccine2.append(c.id)
										break # termina el for							
						
					else: # es la vacuna inicial
						if v.time_application_age==0: # comprueba que la vacuna inicial sea en dias
							date_now = c.nacimiento + relativedelta(days=v.application_age)
						elif v.time_application_age==1: # comprueba que la vacuna inicial sea en meses
							date_now = c.nacimiento + relativedelta(months=v.application_age)
						elif v.time_application_age==2: # comprueba que la vacuna inicial sea en años
							date_now = c.nacimiento + relativedelta(years=v.application_age)
						if (date_now == three_days_after) | (date_now==one_day_before): # si es el día de la primera vacuna
							self.beliefs_application_vaccine.append(v.id)
							self.beliefs_application_vaccine2.append(c.id)

				elif (v.option_number_application==1): # veces repetitivas de aplicar vacuna

					# para la primera vacuna
					if ApplicationMedicament.objects.filter(cattle=c, medicament=v).count() < 1:
						if v.time_application_age==0: # comprueba que la vacuna inicial sea en dias
							date_now = c.nacimiento + relativedelta(days=v.application_age)
						elif v.time_application_age==1: # comprueba que la vacuna inicial sea en meses
							date_now = c.nacimiento + relativedelta(months=v.application_age)
						elif v.time_application_age==2: # comprueba que la vacuna inicial sea en años
							date_now = c.nacimiento + relativedelta(years=v.application_age)
						if (date_now == three_days_after) | (date_now==one_day_before): # si es el día de la primera vacuna
							self.beliefs_application_vaccine.append(v.id)
							self.beliefs_application_vaccine2.append(c.id)


					control = True
					if v.time_interval==0: # comprueba que la vacuna siguiente sea en dias
						i = 1 # contador
						while control: # repite multiples veces
							date_now = c.nacimiento + relativedelta(days=(v.interval*i))
							if (date_now == three_days_after): # comprueba que sea el dia de aplicar
								self.beliefs_application_vaccine.append(v.id)
								self.beliefs_application_vaccine2.append(c.id)
								control = False # termina el while
							elif(date_now > date.today()):
								control = False
							i+=1

					elif v.time_interval==1: # comprueba que la vacuna siguiente sea en meses
						i = 1 # contador
						while control: # repite multiples veces
							date_now = (c.nacimiento + relativedelta(months=(v.interval*i)))
							if (date_now == three_days_after): # comprueba que sea el dia de aplicar
								self.beliefs_application_vaccine.append(v.id)
								self.beliefs_application_vaccine2.append(c.id)
								control = False # termina el while
							elif(date_now > date.today()):
								control = False
							i+=1

					elif v.time_interval==2: # comprueba que la vacuna siguiente sea en years
						i = 1 # contador
						while control: # repite multiples veces
							date_now = c.nacimiento + relativedelta(years=(v.interval*i))
							if (date_now == date.today()): # comprueba que sea el dia de aplicar
								self.beliefs_application_vaccine.append(v.id)
								self.beliefs_application_vaccine2.append(c.id)
								control = False # termina el while
							elif(date_now > date.today()):
								control = False
							i+=1

		# para los wormers
		for v in wormers: # recorre las wormers
			for c in cattles: # recorre los ganados
				if v.option_number_application==0: # veces exactas de aplicar vacuna
					if ApplicationMedicament.objects.filter(cattle=c, medicament=v).count() > 0: # no es la primera vacuna
						av = ApplicationMedicament.objects.filter(cattle=c, medicament=v)
						av_final = av.reverse()[:1]
						
						if av.count() < v.number_application: # controla que no se pase del maximo de aplicaciones
							if v.time_interval==0: # comprueba que la vacuna siguiente sea en dias
								for i in range(av.count(), v.number_application+1): # recorre el numero total de aplicaciones que se deben dar
									date_now = av_final.date + relativedelta(days=(v.interval*i))
									if (date_now == three_days_after) | (date_now==one_day_before): # comprueba que sea el dia de aplicar
										self.beliefs_application_vaccine.append(v.id)
										self.beliefs_application_vaccine2.append(c.id)
										break # termina el for

							if v.time_interval==1: # comprueba que la vacuna siguiente sea en meses
								for i in range(av.count(), v.number_application+1): # recorre el numero total de aplicaciones que se deben dar
									date_now = av_final.date + relativedelta(months=(v.interval*i))
									if (date_now == three_days_after) | (date_now==one_day_before): # comprueba que sea el dia de aplicar
										self.beliefs_application_vaccine.append(v.id)
										self.beliefs_application_vaccine2.append(c.id)
										break # termina el for

							if v.time_interval==2: # comprueba que la vacuna siguiente sea en years
								for i in range(av.count(), v.number_application+1): # recorre el numero total de aplicaciones que se deben dar
									date_now = av_final.date + relativedelta(years=(v.interval*i))
									if (date_now == three_days_after) | (date_now==one_day_before): # comprueba que sea el dia de aplicar
										self.beliefs_application_vaccine.append(v.id)
										self.beliefs_application_vaccine2.append(c.id)
										break # termina el for							
						
					else: # es la vacuna inicial
						if v.time_application_age==0: # comprueba que la vacuna inicial sea en dias
							date_now = c.nacimiento + relativedelta(days=v.application_age)
						elif v.time_application_age==1: # comprueba que la vacuna inicial sea en meses
							date_now = c.nacimiento + relativedelta(months=v.application_age)
						elif v.time_application_age==2: # comprueba que la vacuna inicial sea en años
							date_now = c.nacimiento + relativedelta(years=v.application_age)
						if (date_now == three_days_after) | (date_now==one_day_before): # si es el día de la primera wormer
							self.beliefs_application_wormer.append(v.id)
							self.beliefs_application_wormer2.append(c.id)

				elif (v.option_number_application==1): # veces repetitivas de aplicar vacuna

					# para la primera vacuna
					if ApplicationMedicament.objects.filter(cattle=c, medicament=v).count() < 1:
						if v.time_application_age==0: # comprueba que la vacuna inicial sea en dias
							date_now = c.nacimiento + relativedelta(days=v.application_age)
						elif v.time_application_age==1: # comprueba que la vacuna inicial sea en meses
							date_now = c.nacimiento + relativedelta(months=v.application_age)
						elif v.time_application_age==2: # comprueba que la vacuna inicial sea en años
							date_now = c.nacimiento + relativedelta(years=v.application_age)
						if (date_now == three_days_after) | (date_now==one_day_before): # si es el día de la primera wormer
							self.beliefs_application_wormer.append(v.id)
							self.beliefs_application_wormer2.append(c.id)


					control = True
					if v.time_interval==0: # comprueba que la vacuna siguiente sea en dias
						i = 1 # contador
						while control: # repite multiples veces
							date_now = c.nacimiento + relativedelta(days=(v.interval*i))
							if (date_now == three_days_after): # comprueba que sea el dia de aplicar
								self.beliefs_application_wormer.append(v.id)
								self.beliefs_application_wormer2.append(c.id)
								control = False # termina el while
							elif(date_now > date.today()):
								control = False
							i+=1

					elif v.time_interval==1: # comprueba que la vacuna siguiente sea en meses
						i = 1 # contador
						while control: # repite multiples veces
							date_now = (c.nacimiento + relativedelta(months=(v.interval*i)))
							if (date_now == three_days_after): # comprueba que sea el dia de aplicar
								self.beliefs_application_wormer.append(v.id)
								self.beliefs_application_wormer2.append(c.id)
								control = False # termina el while
							elif(date_now > date.today()):
								control = False
							i+=1

					elif v.time_interval==2: # comprueba que la vacuna siguiente sea en years
						i = 1 # contador
						while control: # repite multiples veces
							date_now = c.nacimiento + relativedelta(years=(v.interval*i))
							if (date_now == date.today()): # comprueba que sea el dia de aplicar
								self.beliefs_application_wormer.append(v.id)
								self.beliefs_application_wormer2.append(c.id)
								control = False # termina el while
							elif(date_now > date.today()):
								control = False
							i+=1



class DesireSanidad:
	def __init__(self):
		self.desires = []
		self.desires.append(6)
		self.desires.append(7)
		self.desires.append(8)
		self.desires.append(9)
		self.desires.append(10)
		self.desires.append(11)

class IntentionSanidad:
	def assignNotification(self, d, datee, name):
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		
		notification = Notification()
		notification.start_date = datetime.date.today()
		notification.end_date = datee
		notification.state = 2
		notification.module = 2
		medicament = Medicament.objects.get(id=d)
		notification.ident_medicament = medicament
		notification.name = name
		notification.farm = farm
		notification.save()

		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2, farm=farm).count()
		for u in users:
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)

	def assignNotification2(self, c, d, datee, name):
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		
		notification = Notification()
		notification.start_date = datetime.date.today()
		notification.end_date = datee
		notification.state = 2
		cattle = Ganado.objects.get(id=c)
		notification.ident_cattle = cattle
		notification.module = 2
		medicament = Medicament.objects.get(id=d)
		notification.ident_medicament = medicament
		notification.name = name
		notification.farm = farm
		notification.save()

		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2, farm=farm).count()
		for u in users:
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)


	def sendNotificationAmountVaccine(self, beliefs_amount_vaccine):
		datee = date.today() + timedelta(days=3)
		one_day_before = date.today() - relativedelta(days=1)

		for d in beliefs_amount_vaccine:
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


	def sendNotificationAmountWormer(self, beliefs_amount_wormer):
		datee = date.today() + timedelta(days=3)
		one_day_before = date.today() - relativedelta(days=1)

		for d in beliefs_amount_wormer:
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


	def sendNotificationExpirationVaccine(self, beliefs_expiration_vaccine):
		datee = date.today() + relativedelta(months=3)
		one_day_before = date.today() - relativedelta(days=1)

		for d in beliefs_expiration_vaccine:
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

	def sendNotificationExpirationWormer(self, beliefs_expiration_wormer):
		datee = date.today() + relativedelta(months=3)
		one_day_before = date.today() - relativedelta(days=1)

		for d in beliefs_expiration_wormer:
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


	def sendNotificationApplicationVaccine(self, beliefs_application_vaccine, beliefs_application_vaccine2):
		datee = date.today() + relativedelta(days=3)
		three_day_before = date.today() - relativedelta(days=3)
		one_day_before = date.today() - relativedelta(days=1)

		for d in beliefs_application_vaccine:
			a = beliefs_application_vaccine.index(d)
			b = beliefs_application_vaccine2[a]
			try:
				notifi = Notification.objects.get(ident_medicament_id=d, start_date=date.today(), end_date=datee, name=10, ident_cattle=b)
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_medicament_id=d, state=2, end_date=one_day_before, name=10, ident_cattle=b)
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_medicament_id=d, state=2, name=10, ident_cattle=b)
					except ObjectDoesNotExist:
						try:
							notifi = Notification.objects.get(ident_medicament_id=d, name=10, end_date=one_day_before, ident_cattle=b)
						except ObjectDoesNotExist:
							try:
								notifi = Notification.objects.get(ident_medicament_id=d, name=10, end_date__gt=three_day_before, ident_cattle=b)
							except ObjectDoesNotExist:
								self.assignNotification2(b, d, datee, 10)
		
		if (Notification.objects.filter(state=2, end_date=one_day_before, name=10).count() > 0):
			Notification.objects.filter(state=2, end_date=one_day_before, name=10).update(state=0)

	def sendNotificationApplicationWormer(self, beliefs_application_wormer, beliefs_application_wormer2):
		datee = date.today() + relativedelta(days=3)
		three_day_before = date.today() - relativedelta(days=3)
		one_day_before = date.today() - relativedelta(days=1)

		for d in beliefs_application_wormer:
			a = beliefs_application_wormer.index(d)
			b = beliefs_application_wormer2[a]
			try:
				notifi = Notification.objects.get(ident_medicament_id=d, start_date=date.today(), end_date=datee, name=11, ident_cattle=b)
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_medicament_id=d, state=2, end_date=one_day_before, name=11, ident_cattle=b)
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_medicament_id=d, state=2, name=11, ident_cattle=b)
					except ObjectDoesNotExist:
						try:
							notifi = Notification.objects.get(ident_medicament_id=d, name=11, end_date=one_day_before, ident_cattle=b)
						except ObjectDoesNotExist:
							try:
								notifi = Notification.objects.get(ident_medicament_id=d, name=11, end_date__gt=three_day_before, ident_cattle=b)
							except ObjectDoesNotExist:
								self.assignNotification2(b, d, datee, 11)
		
		if (Notification.objects.filter(state=2, end_date=one_day_before, name=11).count() > 0):
			Notification.objects.filter(state=2, end_date=one_day_before, name=11).update(state=0)
		


class AgentSanidad(spade.Agent.Agent):
	class BehaviourSanidad(spade.Behaviour.OneShotBehaviour):
		def onStart(self):
			print "inicio del BehaviourSanidad . . ."

		def _process(self):
			user = User.objects.get(id=user_name)
			farm = Ganaderia.objects.get(perfil=user)
			beliefs = BeliefSanidad()
			desires = DesireSanidad()
			intention = IntentionSanidad()
						
			msg2 = self._receive(block=True,timeout=1)
			list_beliefs_ordenio_celo = msg2.getContent().split(',') 
			agent2 = list_beliefs_ordenio_celo[0]
			del(list_beliefs_ordenio_celo[0])

			# compruebo de que haya medicamentos
			list_medicaments_cattle = []
			character = ','
			msg_to_reproduccion = spade.ACLMessage.ACLMessage()
			msg_to_reproduccion.setPerformative("inform")
			if Ganado.objects.filter(ganaderia=farm, genero=1).count() > 0:
				cattles = Ganado.objects.filter(ganaderia=farm, genero=1, ciclos__nombre=2)

				for cattle in cattles:
					if cattle.application_medicament_medicament.all():
						for application_medicament in cattle.application_medicament_medicament.all():
							if application_medicament.cattle.all():
								for cattle_app in application_medicament.cattle.all():
									if str(cattle_app.id) not in list_medicaments_cattle:
										list_medicaments_cattle.append(str(cattle_app.id))

				msg_to_reproduccion.addReceiver(spade.AID.aid(agent2+"@127.0.0.1",["xmpp://"+agent2+"@127.0.0.1"]))
				
				if list_beliefs_ordenio_celo == []:
					list_beliefs_ordenio_celo = [n for n in list_beliefs_ordenio_celo if n not in list_medicaments_cattle]
					msg_to_reproduccion.setContent( character.join(list_beliefs_ordenio_celo) )
				else:	
					list_beliefs_ordenio_celo = [n for n in list_medicaments_cattle if n not in list_beliefs_ordenio_celo]
					msg_to_reproduccion.setContent( character.join(list_medicaments_cattle) )

				self.myAgent.send(msg_to_reproduccion)
			else:
				msg_to_reproduccion.addReceiver(spade.AID.aid(agent2+"@127.0.0.1",["xmpp://"+agent2+"@127.0.0.1"]))
				msg_to_reproduccion.setContent( '' )
				self.myAgent.send(msg_to_reproduccion)
			
			if 6 in desires.desires:
				intention.sendNotificationAmountVaccine(beliefs.beliefs_amount_vaccine)
			if 7 in desires.desires:
				intention.sendNotificationAmountWormer(beliefs.beliefs_amount_wormer)
			if 8 in desires.desires:
				intention.sendNotificationExpirationVaccine(beliefs.beliefs_expiration_vaccine)
			if 9 in desires.desires:
				intention.sendNotificationExpirationWormer(beliefs.beliefs_expiration_wormer)
			if 10 in desires.desires:
				intention.sendNotificationApplicationVaccine(beliefs.beliefs_application_vaccine, beliefs.beliefs_application_vaccine2)
			if 11 in desires.desires:
				intention.sendNotificationApplicationWormer(beliefs.beliefs_application_wormer, beliefs.beliefs_application_wormer2)

		def onEnd(self):
			sys.exit(0)

	def _setup(self):
		
		template = spade.Behaviour.ACLTemplate()
		template.setSender(spade.AID.aid("agent_reproduccion@127.0.0.1",["xmpp://agent_reproduccion@127.0.0.1"]))
		t = spade.Behaviour.MessageTemplate(template)
		self.addBehaviour(self.BehaviourSanidad(),t)
		
		template2 = spade.Behaviour.ACLTemplate()
		template2.setSender(spade.AID.aid("agent_produccion@127.0.0.1",["xmpp://agent_produccion@127.0.0.1"]))
		t2 = spade.Behaviour.MessageTemplate(template2)
		self.addBehaviour(self.BehaviourSanidad(),t2)
		
		b = self.BehaviourSanidad()
		self.addBehaviour(b, None)

################################################
# Agente Produccion
################################################
class BeliefProduccion:
	def __init__(self):
		self.beliefs_ordenio = ['agent_produccion']
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)

		cattle = Ganado.objects.filter( 
			Q(ganaderia=farm, genero=1, etapas__is_active=True, down_cattle=None) &
			(
				Q(ciclos__nombre='2', ciclos__is_active=True)
			) &
			(
				Q(etapas__nombre='3') |
				Q(etapas__nombre='4')
			)
		)
		
		for c in cattle:
			self.beliefs_ordenio.append(str(c.id))

class DesireProduccion:
	def __init__(self):
		self.desires = []
		self.desires.append(5)

class IntentionProduction:
	def assignNotification(self, d):
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)

		notification = Notification()
		notification.start_date = datetime.date.today()
		notification.end_date = date.today() + timedelta(days=0)
		notification.state = 2
		notification.module = 3
		cattle = Ganado.objects.get(id=d)
		notification.ident_cattle = cattle
		notification.name = 5
		notification.farm = farm
		notification.save()

	def sendNotificationOrdenio(self, beliefs_ordenio):
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)

		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		for d in beliefs_ordenio:
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
		n = Notification.objects.filter(state=2, farm=farm).count()
		for u in users:

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
			beliefs = BeliefProduccion()
			desires = DesireProduccion()
			intention = IntentionProduction()
			
			character = ','
			msg = spade.ACLMessage.ACLMessage()
			msg.setPerformative("request")
			msg.setLanguage('español')
			msg.addReceiver(spade.AID.aid("agent_sanidad@127.0.0.1",["xmpp://agent_sanidad@127.0.0.1"]))
			msg.setContent(character.join( beliefs.beliefs_ordenio ) )
			self.myAgent.send(msg)

			msg2 = self._receive(block=True,timeout=1)
			if msg2.getContent() != '':
				if 5 in desires.desires:
					intention.sendNotificationOrdenio( list(msg2.getContent().split(',')) )

		def onEnd(self):
			sys.exit(0)

	def _setup(self):
		template = spade.Behaviour.ACLTemplate()
		template.setSender(spade.AID.aid("agent_sanidad@127.0.0.1",["xmpp://agent_sanidad@127.0.0.1"]))
		t = spade.Behaviour.MessageTemplate(template)
		self.addBehaviour(self.BehaviourProduccion(), t)
		
		b = self.BehaviourProduccion()
		self.addBehaviour(b, None)

################################################
# Agente Alimentacion
################################################
class BeliefAlimentacion:
	def __init__(self):
		self.beliefs_amount_food = []
		self.beliefs_expiration_food = []
		self.beliefs_application_food = []
		self.beliefs_application_food2 = []

		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		food_amount = Food.objects.filter(farm=farm, amount__lt=30)
		food_expiration = Food.objects.filter(farm=farm)

		for m in food_amount:
			self.beliefs_amount_food.append(m.id)

		date_expiration = date.today() + relativedelta(months=3)
		for m in food_expiration:
			if m.expiration_date < date_expiration:
				self.beliefs_expiration_food.append(m.id)


		one_day_before = date.today() - relativedelta(days=1)
		foods = Food.objects.filter(farm=farm, is_active=True)
		cattles = Ganado.objects.filter(ganaderia=farm, down_cattle=None)


		for f in foods: # recorre las foods
			for c in cattles: # recorre los ganados

				control = True
				if f.phase==0: # si es para terneras
					i = 1 # contador
					if f.time_interval==0: # comprueba que el alimento inicial sea en dias
						if c.etapas.filter(is_active=True, nombre=0).count() > 0:
							for e in c.etapas.filter(is_active=True, nombre=0):
								while control:
									date_now = e.fecha_inicio + relativedelta(days=(f.interval*i))	
									if (date_now == date.today()) | (date_now==one_day_before): # si es el día de la primera alimentacion
										self.beliefs_application_food.append(f.id)
										self.beliefs_application_food2.append(c.id)
										control = False # termina el while
									elif(date_now > date.today()):
										control = False
									i+=1				
					elif f.time_interval==1: # comprueba que el alimento inicial sea en meses
						if c.etapas.filter(is_active=True, nombre=0).count() > 0:
							for e in c.etapas.filter(is_active=True, nombre=0):
								while control:
									date_now = e.fecha_inicio + relativedelta(months=(f.interval*i))	
									if (date_now == date.today()) | (date_now==one_day_before): # si es el día de la primera alimentacion
										self.beliefs_application_food.append(f.id)
										self.beliefs_application_food2.append(c.id)
										control = False # termina el while
									elif(date_now > date.today()):
										control = False
									i+=1
					elif f.time_interval==2: # comprueba que el alimento inicial sea en años
						if c.etapas.filter(is_active=True, nombre=0).count() > 0:
							for e in c.etapas.filter(is_active=True, nombre=0):
								while control:
									date_now = e.fecha_inicio + relativedelta(years=(f.interval*i))	
									if (date_now == date.today()) | (date_now==one_day_before): # si es el día de la primera alimentacion
										self.beliefs_application_food.append(f.id)
										self.beliefs_application_food2.append(c.id)
										control = False # termina el while
									elif(date_now > date.today()):
										control = False
									i+=1
					
				elif f.phase==1: # si es para adultos
					i = 1 # contador
					if f.time_interval==0: # comprueba que el alimento inicial sea en dias
						if c.etapas.filter(is_active=True).exclude(nombre=0).count() > 0:
							for e in c.etapas.filter(is_active=True).exclude(nombre=0):
								while control:
									date_now = e.fecha_inicio + relativedelta(days=(f.interval*i))	
									if (date_now == date.today()) | (date_now==one_day_before): # si es el día de la primera alimentacion
										self.beliefs_application_food.append(f.id)
										self.beliefs_application_food2.append(c.id)
										control = False # termina el while
									elif(date_now > date.today()):
										control = False
									i+=1	
					elif f.time_interval==1: # comprueba que el alimento inicial sea en meses
						if c.etapas.filter(is_active=True).exclude(nombre=0).count() > 0:
							for e in c.etapas.filter(is_active=True).exclude(nombre=0):
								while control:
									date_now = e.fecha_inicio + relativedelta(months=(f.interval*i))	
									if (date_now == date.today()) | (date_now==one_day_before): # si es el día de la primera alimentacion
										self.beliefs_application_food.append(f.id)
										self.beliefs_application_food2.append(c.id)
										control = False # termina el while
									elif(date_now > date.today()):
										control = False
									i+=1
					elif f.time_interval==2: # comprueba que el alimento inicial sea en años
						if c.etapas.filter(is_active=True).exclude(nombre=0).count() > 0:
							for e in c.etapas.filter(is_active=True).exclude(nombre=0):
								while control:
									date_now = e.fecha_inicio + relativedelta(years=(f.interval*i))	
									if (date_now == date.today()) | (date_now==one_day_before): # si es el día de la primera alimentacion
										self.beliefs_application_food.append(f.id)
										self.beliefs_application_food2.append(c.id)
										control = False # termina el while
									elif(date_now > date.today()):
										control = False
									i+=1
				elif f.phase==2: # si es para todos
					i = 1 # contador
					if f.time_interval==0: # comprueba que el alimento inicial sea en dias
						if c.etapas.all() > 0:
							for e in c.etapas.all():
								while control:
									date_now = e.fecha_inicio + relativedelta(days=(f.interval*i))	
									if (date_now == date.today()) | (date_now==one_day_before): # si es el día de la primera alimentacion
										self.beliefs_application_food.append(f.id)
										self.beliefs_application_food2.append(c.id)
										control = False # termina el while
									elif(date_now > date.today()):
										control = False
									i+=1	
					elif f.time_interval==1: # comprueba que el alimento inicial sea en meses
						if c.etapas.all() > 0:
							for e in c.etapas.all():
								while control:
									date_now = e.fecha_inicio + relativedelta(months=(f.interval*i))	
									if (date_now == date.today()) | (date_now==one_day_before): # si es el día de la primera alimentacion
										self.beliefs_application_food.append(f.id)
										self.beliefs_application_food2.append(c.id)
										control = False # termina el while
									elif(date_now > date.today()):
										control = False
									i+=1
					elif f.time_interval==2: # comprueba que el alimento inicial sea en años
						if c.etapas.all() > 0:
							for e in c.etapas.all():
								while control:
									date_now = e.fecha_inicio + relativedelta(years=(f.interval*i))	
									if (date_now == date.today()) | (date_now==one_day_before): # si es el día de la primera alimentacion
										self.beliefs_application_food.append(f.id)
										self.beliefs_application_food2.append(c.id)
										control = False # termina el while
									elif(date_now > date.today()):
										control = False
									i+=1


class DesireAlimentacion:
	def __init__(self):
		self.desires = []
		self.desires.append(12)
		self.desires.append(13)
		self.desires.append(14)

class IntentionAlimentacion:
	def assignNotification(self, d, datee, name):
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)

		notification = Notification()
		notification.start_date = datetime.date.today()
		notification.end_date = datee
		notification.state = 2
		notification.module = 1
		food = Food.objects.get(id=d)
		notification.ident_food = food
		notification.name = name
		notification.farm = farm
		notification.save()

		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2, farm=farm).count()
		for u in users:
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)

	def assignNotification2(self, c, d, datee, name):
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		
		notification = Notification()
		notification.start_date = datetime.date.today()
		notification.end_date = datee
		notification.state = 2
		cattle = Ganado.objects.get(id=c)
		notification.ident_cattle = cattle
		notification.module = 1
		food = Food.objects.get(id=d)
		notification.ident_food = food
		notification.name = name
		notification.farm = farm
		notification.save()

		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2, farm=farm).count()
		for u in users:
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)

	def sendNotificationAmountFood(self, beliefs_amount_food):
		datee = date.today() + timedelta(days=3)
		one_day_before = date.today() - relativedelta(days=1)

		for d in beliefs_amount_food:
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

	def sendNotificationExpirationFood(self, beliefs_expiration_food):
		datee = date.today() + relativedelta(months=3)
		one_day_before = date.today() - relativedelta(days=1)

		for d in beliefs_expiration_food:
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


	def sendNotificationApplicationFood(self, beliefs_application_food, beliefs_application_food2):
		one_day_before = date.today() - relativedelta(days=1)

		l = len(beliefs_application_food)
		for i in range(0,l):
			d = beliefs_application_food[i]
			b = beliefs_application_food2[i]
		
			try:
				notifi = Notification.objects.get(ident_food_id=d, start_date=date.today(), end_date=date.today(), name=14, ident_cattle=b)
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_food_id=d, state=2, end_date=one_day_before, name=14, ident_cattle=b)
					notifi.state=0
					notifi.save()
				except ObjectDoesNotExist:
					self.assignNotification2(b, d, date.today(), 14)


class AgentAlimentacion(spade.Agent.Agent):
	class BehaviourAlimentacion(spade.Behaviour.OneShotBehaviour):
		def onStart(self):
			print "inicio del BehaviourAlimentacion . . ."

		def _process(self):
			beliefs = BeliefAlimentacion()
			desires = DesireAlimentacion()
			intention = IntentionAlimentacion()
			if 12 in desires.desires:
				intention.sendNotificationAmountFood(beliefs.beliefs_amount_food)
			if 13 in desires.desires:
				intention.sendNotificationExpirationFood(beliefs.beliefs_expiration_food)
			if 14 in desires.desires:
				intention.sendNotificationApplicationFood(beliefs.beliefs_application_food, beliefs.beliefs_application_food2)

		def onEnd(self):
			sys.exit(0)

	def _setup(self):
		b = self.BehaviourAlimentacion()
		self.addBehaviour(b, None)



################################################
# Agente Reproduccion
################################################
class BeliefReproduccion:
	def __init__(self):
		self.beliefs_celo = ['agent_reproduccion']
		self.beliefs_service = []
		self.beliefs_verification = []
		self.beliefs_parto = []
		self.beliefs_pajuelas = []
		self.beliefs_terneras = []
		self.beliefs_media = []
		self.beliefs_fierro = []
		self.beliefs_vientre = []
		self.beliefs_cattles = []
		self.beliefs_seco = []

		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		configuration = Configuracion.objects.get(id=farm.configuracion_id)

		try:
			cattle_celo = Ganado.objects.filter( Q(ganaderia=farm, down_cattle=None) & (Q(etapas__nombre='3') | Q(etapas__nombre='4')) )
			for c in cattle_celo:
				self.beliefs_celo.append(str(c.id))
		except ObjectDoesNotExist:
			pass

		try:
			cattle_service = Ganado.objects.filter( ganaderia=farm, genero=1, celos__estado=0, celos__is_active=True, down_cattle=None )
			for c in cattle_service:
				if Verification.objects.filter(cattle=c, is_active=True).count() < 1:
					self.beliefs_service.append(c.id)
		except ObjectDoesNotExist:
			pass
		
		one_day_after = date.today() + relativedelta(days=1)
		two_day_before = date.today() - relativedelta(days=2)

		try:
			cattle_verification = Ganado.objects.filter( Q(ganaderia=farm, genero=1, verification_cattle__is_active=True, down_cattle=None) &
				(Q(verification_cattle__attempt_verification__attempt_date=one_day_after) | Q(verification_cattle__attempt_verification__attempt_date=two_day_before) ) )
			for c in cattle_verification:
				self.beliefs_verification.append(c.id)
		except ObjectDoesNotExist:
			pass

		one_day_before = date.today() - relativedelta(days=1)
		twelve_days_parto = date.today() + relativedelta(days=12)
		try:
			cattle_parto = Ganado.objects.filter( Q(ganaderia=farm, genero=1, gestaciones__is_active=True, down_cattle=None) &
				(Q(gestaciones__fecha_parto=twelve_days_parto) | Q(gestaciones__fecha_parto=one_day_before)) )
			for c in cattle_parto:
				self.beliefs_parto.append(c.id)
		except ObjectDoesNotExist:
			pass

		try:
			pajuelas = Insemination.objects.filter( farm=farm, amount_pajuelas__lt=5, down_insemination=None)
			for p in pajuelas:
				self.beliefs_pajuelas.append(p.id)
		except ObjectDoesNotExist:
			passrelative

		try:
			terneras = Ganado.objects.filter(ganaderia=farm, genero=1, etapas__nombre='0', etapas__is_active=True, down_cattle=None)
			for t in terneras:
				for e in t.etapas.all():
					if e.is_active:
						if ( ( t.nacimiento + relativedelta(months=configuration.etapa_ternera) ) - relativedelta(days=10) == date.today() ) or ( ( t.nacimiento + relativedelta(months=configuration.etapa_ternera) ) + relativedelta(days=1) == date.today() ):
							self.beliefs_terneras.append(t.id)
						if (DeferEtapa.objects.filter(cattle_id=t, is_active=True).count() > 0):
							defer = DeferEtapa.objects.get(cattle_id=t, is_active=True)
							if ((t.nacimiento + relativedelta(months=configuration.etapa_ternera)) + relativedelta(days=defer.number_days+1) == date.today()):
								self.beliefs_terneras.append(t.id)
		except ObjectDoesNotExist:
			pass

		try:
			media = Ganado.objects.filter(ganaderia=farm, genero=1, etapas__nombre='1', etapas__is_active=True, down_cattle=None)

			for m in media:
				for e in m.etapas.all():
					if e.is_active:
						if (DeferEtapa.objects.filter(cattle_id=m, is_active=True).count() > 0):
							defer = DeferEtapa.objects.get(cattle_id=m, is_active=True)
							if ((m.nacimiento + relativedelta(months=configuration.etapa_vacona_media)) + relativedelta(days=defer.number_days+1) == date.today()):
								self.beliefs_media.append(m.id)
						elif ( ( m.nacimiento + relativedelta(months=configuration.etapa_vacona_media) ) - relativedelta(days=10) == date.today() ) or ( ( m.nacimiento + relativedelta(months=configuration.etapa_vacona_media) ) + relativedelta(days=1) == date.today() ):
							self.beliefs_media.append(m.id)
						
		except ObjectDoesNotExist:
			pass

		try:
			fierro = Ganado.objects.filter(ganaderia=farm, genero=1, etapas__nombre='2', etapas__is_active=True, down_cattle=None)

			for f in fierro:
				for e in f.etapas.all():
					if e.is_active:
						if (DeferEtapa.objects.filter(cattle_id=f, is_active=True).count() > 0):
							defer = DeferEtapa.objects.get(cattle_id=f, is_active=True)
							if ((f.nacimiento + relativedelta(months=configuration.etapa_vacona_fierro)) + relativedelta(days=defer.number_days+1) == date.today()):
								self.beliefs_fierro.append(f.id)
						elif ( ( f.nacimiento + relativedelta(months=configuration.etapa_vacona_fierro) ) - relativedelta(days=10) == date.today() ) or ( ( f.nacimiento + relativedelta(months=configuration.etapa_vacona_fierro) ) + relativedelta(days=1) == date.today() ):
							self.beliefs_fierro.append(f.id)
						
		except ObjectDoesNotExist:
			pass

		try:
			vientre = Ganado.objects.filter(ganaderia=farm, genero=1, etapas__nombre='3', etapas__is_active=True, down_cattle=None)
			for v in vientre:
				for e in v.etapas.all():
					if e.is_active:
						if ( ( v.nacimiento + relativedelta(months=configuration.etapa_vacona_vientre) ) - relativedelta(days=10) == date.today() ) or ( ( v.nacimiento + relativedelta(months=configuration.etapa_vacona_vientre) ) + relativedelta(days=1) == date.today() ):
							self.beliefs_vientre.append(v.id)
						if (DeferEtapa.objects.filter(cattle_id=v, is_active=True).count() > 0):
							defer = DeferEtapa.objects.get(cattle_id=v, is_active=True)
							if ((v.nacimiento + relativedelta(months=configuration.etapa_vacona_vientre)) + relativedelta(days=defer.number_days+1) == date.today()):
								self.beliefs_vientre.append(v.id)
						
		except ObjectDoesNotExist:
			pass

		try:
			cattles = Ganado.objects.filter(ganaderia=farm, genero=1, ciclos__nombre=2, down_cattle=None) 
			for c in cattles:
				for i in c.ciclos.all():
					if ((i.nombre==2) & (i.is_active==True)):
						if ( ((i.fecha_fin) == (date.today() + relativedelta(days=3))) ):
							self.beliefs_seco.append(c.id)

						elif (DeferEtapa.objects.filter(cattle_id=c, is_active=True).count() > 0):
							defer = DeferEtapa.objects.get(cattle_id=c, is_active=True)
							if ((i.fecha_fin) + relativedelta(days=defer.number_days+1) == date.today()):
								self.beliefs_seco.append(c.id)
						elif ((i.fecha_fin) == (date.today() - relativedelta(days=1))):
							self.beliefs_seco.append(c.id)
		except ObjectDoesNotExist:
			pass

		try:
			cattles = Ganado.objects.filter(ganaderia=farm, genero=1, down_cattle=None)
			for c in cattles:
				self.beliefs_cattles.append(c.id)
		except ObjectDoesNotExist:
			pass



class DesireReproduccion:
	def __init__(self):
		self.desires = []
		self.desires.append(0)
		self.desires.append(1)
		self.desires.append(2)
		self.desires.append(3)
		self.desires.append(4)
		self.desires.append(15)
		self.desires.append(16)
		self.desires.append(17)
		self.desires.append(18)
		self.desires.append(19)
		self.desires.append(20)

class IntentionReproduccion:
	def assignNotification(self, d, datee, name):
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)

		notification = Notification()
		notification.start_date = datetime.date.today()
		notification.end_date = datee
		notification.state = 2
		notification.module = 0
		cattle = Ganado.objects.get(id=d)
		notification.ident_cattle = cattle
		notification.name = name
		notification.farm = farm
		notification.save()

		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2, farm=farm).count()
		for u in users:
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)

	def sendNotificationCelo(self, beliefs_celo):
		datee = date.today() + timedelta(days=3)
		one_day_before = date.today() - relativedelta(days=1)
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		configuration = Configuracion.objects.get(id=farm.configuracion_id)
		try:
			cattles = Ganado.objects.filter( Q(ganaderia=farm, ciclos__nombre=0, ciclos__is_active=True) & (Q(etapas__nombre='3') | Q(etapas__nombre='4')) )
			for c in cattles:

				if c.verification_cattle.all():
					for c_verification in c.verification_cattle.all():
						if c_verification.is_active == True:
							date_parto = 'verificacion'
							break
						else:
							if c.gestaciones.all():
								for c_parto in c.gestaciones.all(): # itera las gestaciones que haya tenido
									if (c_parto.problema!=None):
										problema = ProblemaGestacion.objects.get(id=c_parto.problema.id)
										if (problema.fecha_problema <= c_parto.fecha_parto):
											date_parto = 'p'+str(problema.fecha_problema)
										elif c_parto.is_active==False:
											date_parto = c_parto.fecha_parto
									elif c_parto.is_active==False:
										date_parto = c_parto.fecha_parto
							else:
								date_parto = None
				else:
					date_parto = None


				# pasar a false el celo si ha vencido
				try:
					celo = Celo.objects.get(ganado=c, is_active=True)
					if (celo.fecha_fin.date() < date.today()):
						celo.is_active=False
						celo.save()
						# pasar a false el deferetapa si ha vencido
						try:
							d = DeferEtapa.objects.get(cattle_id=c, is_active=True)
							d.is_active=False
							d.save()
						except ObjectDoesNotExist:
							pass
				except ObjectDoesNotExist:
					pass

				aux = str(date_parto)

				if (aux[:1]=='p'):
					fecha = date_parto.replace("p", "")
					fecha = fecha.replace('-', '')

					fecha = datetime.datetime.strptime(fecha, "%Y%m%d").date()

					date_celo = fecha + relativedelta( days=(configuration.celo_frecuencia - configuration.celo_frecuencia_error) )
					end_date_celo = fecha + relativedelta( days=(configuration.celo_frecuencia + configuration.celo_frecuencia_error) )

					try:
						notifi = Notification.objects.get(ident_cattle_id=c, state=2, end_date=one_day_before, module=0, name=0)
						notifi.state = 1
						notifi.save()
					except ObjectDoesNotExist:
						try:
							notifi = Notification.objects.get(ident_cattle_id=c, state=1, end_date=one_day_before, module=0, name=0)
							notifi.state = 1
							notifi.save()
						except ObjectDoesNotExist:
							pass

					if ( date.today() == date_celo ): # si hoy == a la fecha de celo 
						try:
							notifi = Notification.objects.get(ident_cattle_id=c, state=2, start_date=date.today(), module=0, name=0)
						except ObjectDoesNotExist:
							try:
								notifi = Notification.objects.get(ident_cattle_id=c, state=1, start_date=date.today(), module=0, name=0)
							except ObjectDoesNotExist:
								start_date = datetime.datetime.now(pytz.timezone('America/Guayaquil'))
								duration_celo = datetime.timedelta(days=configuration.celo_frecuencia_error*2)
								end_date = start_date + duration_celo

								celo = Celo()
								celo.fecha_inicio = start_date
								celo.fecha_fin = end_date
								celo.estado = 0
								celo.observaciones = 'Creado por HatosGanaderos'
								celo.ganado = c
								celo.is_active = True
								celo.save()
								self.assignNotification(c.id, end_date.date(), 0)
				elif ((date_parto != 'verificacion') & (date_parto != None)):  # si existe una previa gestacion (!=)
					days_after_parto = configuration.celo_despues_parto
					days_after_parto_error = configuration.celo_despues_parto_error
					
					date_celo = date_parto + relativedelta( days=(days_after_parto - days_after_parto_error) )
					end_date_celo = date_parto + relativedelta( days=(days_after_parto + days_after_parto_error) )

					try:
						notifi = Notification.objects.get(ident_cattle_id=c, state=2, end_date=one_day_before, module=0, name=0)
						notifi.state = 1
						notifi.save()
					except ObjectDoesNotExist:
						pass

					if (date.today() >= date_celo) & (date.today() <= end_date_celo): # si hoy == a la fecha de celo luego del parto
						
						notifi = Notification.objects.filter(Q(ident_cattle_id=c, module=0, name=0) & (Q(state=2) | Q(state=1))).order_by('end_date')[:1]
						for i in notifi:
							if (date.today() > i.end_date):
								try:
									notifi = Notification.objects.get(ident_cattle_id=c, state=2, start_date=date.today(), module=0, name=0)
								except ObjectDoesNotExist:
									try:
										notifi = Notification.objects.get(ident_cattle_id=c, state=1, start_date=date.today(), module=0, name=0)
									except ObjectDoesNotExist:
										start_date = datetime.datetime.now(pytz.timezone('America/Guayaquil'))
										duration_celo = datetime.timedelta(hours=configuration.celo_duracion + configuration.celo_duracion_error)
										end_date = start_date + duration_celo

										celo = Celo()
										celo.fecha_inicio = start_date
										celo.fecha_fin = end_date
										celo.estado = 0
										celo.observaciones = 'Creado por HatosGanaderos'
										celo.ganado = c
										celo.is_active = True
										celo.save()
										self.assignNotification(c.id, end_date.date(), 0)
				elif (date_parto=='verificacion'):
					pass
				else: # auscencia de previa gestacion
					if c.ciclos.all():
						for ci in c.ciclos.all():
							if ci.nombre == 0 and ci.is_active==True:
								start_date_ciclo = ci.fecha_inicio

					days_frequency_celo = configuration.celo_frecuencia
					days_frequency_celo_error = configuration.celo_frecuencia_error
					end_days = days_frequency_celo - days_frequency_celo_error

					date_now_ciclo = start_date_ciclo + relativedelta(days=end_days)

					date_now_celo = False
					
					if c.celos.all():
						for ce in c.celos.all():
							celo = Celo.objects.filter(ganado=c).reverse()[:1]
							for celito in celo:
								start_date_celo = celito.fecha_fin.date()
								date_now_celo = (start_date_celo - relativedelta(days=days_frequency_celo_error) ) + relativedelta(days=end_days)

					# para pasar notificación a realizada
					try:
						notifi = Notification.objects.get(ident_cattle_id=c, state=2, end_date=one_day_before, module=0, name=0)
						notifi.state = 1
						notifi.save()
					except ObjectDoesNotExist:
						pass


					if (date.today() == date_now_ciclo) | (date.today() == date_now_celo):
						start_date = datetime.datetime.now(pytz.timezone('America/Guayaquil'))
						if days_frequency_celo_error == 0:
							duration_celo = datetime.timedelta(hours=configuration.celo_duracion + configuration.celo_duracion_error)
							end_date = start_date + duration_celo
						else:
							duration_celo = start_date + relativedelta(days=days_frequency_celo_error*2)
							end_date = duration_celo 

						try:
							notifi = Notification.objects.get(ident_cattle_id=c, start_date=date.today(), end_date=end_date, module=0, name=0)
						except ObjectDoesNotExist:
							try:
								notifi = Notification.objects.get(ident_cattle_id=c, state=2, end_date=one_day_before, module=0, name=0)
								notifi.state = 1
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
									celo.observaciones = str(c.id)
									celo.ganado = c
									celo.is_active = True
									celo.save()
									self.assignNotification(c.id, end_date.date(), 0)
					else: # desactiva el celo pasada la fecha
						if c.celos.all():
							for c_celo in c.celos.all(): # itera los celos que haya tenido
								f = c_celo.fecha_fin - datetime.timedelta(hours=5)
								if (c_celo.is_active==True) & (c_celo.fecha_fin<=datetime.datetime.now(pytz.timezone('America/Guayaquil')) ):
									c_celo.is_active = False
									c_celo.save()


			users = User.objects.filter(profile_user__ganaderia_perfil=farm)

			msg = 'Notificación, REALIZADA con ÉXITO'
			n = Notification.objects.filter(state=2, farm=farm).count()
			for u in users:
				ishout_client.emit(
						u.id,
						'notifications',
						data = {'msg': msg,
								'number_notifications': n,}
					)

		except ObjectDoesNotExist:
			pass

	def sendNotificationService(self, beliefs_service):
		one_day_before = date.today() - relativedelta(days=1)
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		configuration = Configuracion.objects.get(id=farm.configuracion_id)
		if configuration.celo_frecuencia_error == 0:
			datee = date.today() + timedelta(days=1)
		else:
			datee = date.today() + timedelta(days=configuration.celo_frecuencia_error*2)

		for d in beliefs_service:
			try:
				notifi = Notification.objects.get(ident_cattle_id=d, start_date=date.today(), end_date=datee, module=0, name=1)
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_cattle_id=d, state=2, end_date=date.today(), module=0, name=1)
					notifi.state = 0
					notifi.save()
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_cattle_id=d, state=2, module=0, name=1)
					except ObjectDoesNotExist:
						try:
							notifi = Notification.objects.get(ident_cattle_id=d, state=0, module=0, name=1, end_date=date.today())
						except ObjectDoesNotExist:
							try:
								notifi = Notification.objects.get(ident_cattle_id=d, state=0, module=0, name=1, end_date__gt=date.today())# mayor que
								self.assignNotification(d, datee, 1)
							except ObjectDoesNotExist:
								try:
									notifi = Notification.objects.get(ident_cattle_id=d, state=0, module=0, name=1, end_date__lt=date.today())# mayor que
								except ObjectDoesNotExist:
									try:
										notifi = Notification.objects.filter(ident_cattle_id=d, state=1, module=0, name=1).reverse()[:1]
										if notifi.count() > 0:
											for t in notifi:
												if ( (date.today() <= t.end_date) | (date.today()-relativedelta(days=1) <= t.end_date) ):
													pass
												else:
													self.assignNotification(d, datee, 1)
										else:
											self.assignNotification(d, datee, 1)
									except ObjectDoesNotExist:
										self.assignNotification(d, datee, 1)

		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2, farm=farm).count()
		for u in users:
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)

	def sendNotificationVerification(self, beliefs_verification):
		datee = date.today() + timedelta(days=2)
		one_day_before = date.today() - relativedelta(days=1)
		two_day_before = date.today() - relativedelta(days=2)
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		configuration = Configuracion.objects.get(id=farm.configuracion_id)

		for d in beliefs_verification:
			try:
				notifi = Notification.objects.get(ident_cattle_id=d, start_date=date.today(), end_date=datee, module=0, name=2)
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_cattle_id=d, state=2, end_date=one_day_before, module=0, name=2)
					notifi.state = 0
					notifi.save()
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_cattle_id=d, state=2, module=0, name=2)
					except ObjectDoesNotExist:
						try:
							notifi = Notification.objects.get(ident_cattle_id=d, module=0, name=2, end_date=one_day_before)
						except ObjectDoesNotExist:
							try:
								notifi = Notification.objects.get(ident_cattle_id=d, module=0, name=2, end_date=two_day_before)
							except ObjectDoesNotExist:
								try:
									notifi = Notification.objects.get(ident_cattle_id=d, module=0, name=2, state=1, end_date__gte=date.today())
								except ObjectDoesNotExist:
									self.assignNotification(d, datee, 2)

		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2, farm=farm).count()
		for u in users:
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)

	def sendNotificationParto(self, beliefs_parto):
		datee = date.today() + timedelta(days=12)
		one_day_before = date.today() - relativedelta(days=1)
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		configuration = Configuracion.objects.get(id=farm.configuracion_id)

		for d in beliefs_parto:
			try:
				notifi = Notification.objects.get(ident_cattle_id=d, start_date=date.today(), end_date=datee, module=0, name=3 )
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_cattle_id=d, state=2, end_date=one_day_before, module=0, name=3)
					notifi.state = 0
					notifi.save()
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_cattle_id=d, state=2, module=0, name=3)
					except ObjectDoesNotExist:
						try:
							notifi = Notification.objects.get(ident_cattle_id=d, module=0, name=3, end_date=one_day_before)
						except ObjectDoesNotExist:
							self.assignNotification(d, datee, 3)

		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2, farm=farm).count()
		for u in users:
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)

	def assignNotification2(self, d, datee, name):
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)

		notification = Notification()
		notification.start_date = datetime.date.today()
		notification.end_date = datee
		notification.state = 2
		notification.module = 0
		sperm = Insemination.objects.get(id=d)
		notification.ident_sperm = sperm
		notification.name = name
		notification.farm = farm
		notification.save()

		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2, farm=farm).count()
		for u in users:
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)


	def sendNotificationPajuela(self, beliefs_pajuelas):
		datee = date.today() + timedelta(days=3)
		one_day_before = date.today() - relativedelta(days=1)
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		configuration = Configuracion.objects.get(id=farm.configuracion_id)

		for d in beliefs_pajuelas:
			try:
				notifi = Notification.objects.get(ident_sperm_id=d, start_date=date.today(), end_date=datee, module=0, name=4 )
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_sperm_id=d, state=2, end_date=one_day_before, module=0, name=4)
					notifi.state = 0
					notifi.save()
					self.assignNotification2(d, datee, 4)
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_sperm_id=d, state=2, module=0, name=4)
					except ObjectDoesNotExist:
						self.assignNotification2(d, datee, 4)

		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2, farm=farm).count()
		for u in users:
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)


	def sendNotificationTerneras(self, beliefs_terneras):
		datee = date.today() + relativedelta(days=10)
		one_day_before = date.today() - relativedelta(days=1)
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		configuration = Configuracion.objects.get(id=farm.configuracion_id)

		for d in beliefs_terneras:
			try:
				notifi = Notification.objects.get(ident_cattle_id=d, start_date=date.today(), end_date=datee, module=0, name=15 )
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.filter( Q(ident_cattle_id=d, state=2, end_date=one_day_before, module=0, name=15) | Q(ident_cattle_id=d, state=1, end_date=one_day_before, module=0, name=15) )
					if notifi.count() > 0:
						# desactiva etapa anterior
						etapa_last = Etapa.objects.get(ganado_id=d, is_active=True)
						etapa_last.is_active = False
						etapa_last.save()
						# desactiva la deferEtapa
						cattle = Ganado.objects.get(id=d)
						if DeferEtapa.objects.filter(cattle_id=cattle, is_active=True).count() > 0:
							deferEtap = DeferEtapa.objects.get(cattle_id_id=d, is_active=True)
							deferEtap.is_active = False
							deferEtap.save()
						
						# crea la nueva etapa
						etapa = Etapa()
						etapa.fecha_inicio = date.today()
						etapa.nombre = 1
						etapa.observaciones = 'Cambio realizado por el sistema'
						etapa.ganado = Ganado.objects.get(id=d)
						etapa.is_active = True
						etapa.save()
						for n in notifi:
							n.state = 1
							n.save()
					else:
						try:
							notifi = Notification.objects.get(ident_cattle_id=d, state=2, module=0, name=15)
						except ObjectDoesNotExist:
							try:
								notifi = Notification.objects.get(ident_cattle_id=d, state=1, module=0, name=15)
								if (date.today() + relativedelta(days=1) ) <= notifi.end_date:
									break
							except ObjectDoesNotExist:
								self.assignNotification(d, datee, 15)	
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_cattle_id=d, state=2, module=0, name=15)
					except ObjectDoesNotExist:
						try:
							notifi = Notification.objects.get(ident_cattle_id=d, state=1, module=0, name=15)
							if (date.today() + relativedelta(days=1) ) <= notifi.end_date:
								break
						except ObjectDoesNotExist:
							try:
								notifi = Notification.objects.get(ident_cattle_id=d, state=1, start_date=date.today(), module=0, name=15)
							except ObjectDoesNotExist:
								self.assignNotification(d, datee, 15)

		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2, farm=farm).count()
		for u in users:
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)

	def sendNotificationFierro(self, beliefs_media):
		datee = date.today() + relativedelta(days=10)
		one_day_before = date.today() - relativedelta(days=1)
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		configuration = Configuracion.objects.get(id=farm.configuracion_id)

		for d in beliefs_media:
			try:
				notifi = Notification.objects.get(ident_cattle_id=d, start_date=date.today(), end_date=datee, module=0, name=16 )
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.filter( Q(ident_cattle_id=d, state=2, end_date=one_day_before, module=0, name=16) | Q(ident_cattle_id=d, state=1, end_date=one_day_before, module=0, name=16) )
					if notifi.count() > 0:
						# desactiva etapa anterior
						etapa_last = Etapa.objects.get(ganado_id=d, is_active=True)
						etapa_last.is_active = False
						etapa_last.save()
						# desactiva la deferEtapa
						cattle = Ganado.objects.get(id=d)
						if DeferEtapa.objects.filter(cattle_id=cattle, is_active=True).count() > 0:
							deferEtap = DeferEtapa.objects.get(cattle_id_id=d, is_active=True)
							deferEtap.is_active = False
							deferEtap.save()
						# crea la nueva etapa
						etapa = Etapa()
						etapa.fecha_inicio = date.today()
						etapa.nombre = 2
						etapa.observaciones = 'Cambio realizado por el sistema'
						etapa.ganado = Ganado.objects.get(id=d)
						etapa.is_active = True
						etapa.save()
						for n in notifi:
							n.state = 1
							n.save()
					else:
						try:
							notifi = Notification.objects.get(ident_cattle_id=d, state=2, module=0, name=16)
						except ObjectDoesNotExist:
							self.assignNotification(d, datee, 16)	
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_cattle_id=d, state=2, module=0, name=16)
					except ObjectDoesNotExist:
						self.assignNotification(d, datee, 16)

		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2, farm=farm).count()
		for u in users:
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)

	def sendNotificationVientre(self, beliefs_fierro):
		datee = date.today() + relativedelta(days=10)
		one_day_before = date.today() - relativedelta(days=1)
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		configuration = Configuracion.objects.get(id=farm.configuracion_id)

		for d in beliefs_fierro:
			try:
				notifi = Notification.objects.get(ident_cattle_id=d, start_date=date.today(), end_date=datee, module=0, name=17 )
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.filter( Q(ident_cattle_id=d, state=2, end_date=one_day_before, module=0, name=17) | Q(ident_cattle_id=d, state=1, end_date=one_day_before, module=0, name=17) )
					if notifi.count() > 0:
						etapa_last = Etapa.objects.get(ganado_id=d, is_active=True)
						etapa_last.is_active = False
						etapa_last.save()
						# desactiva la deferEtapa
						cattle = Ganado.objects.get(id=d)
						if DeferEtapa.objects.filter(cattle_id=cattle, is_active=True).count() > 0:
							deferEtap = DeferEtapa.objects.get(cattle_id_id=d, is_active=True)
							deferEtap.is_active = False
							deferEtap.save()
						# crea la nueva etapa
						etapa = Etapa()
						etapa.fecha_inicio = date.today()
						etapa.nombre = 3
						etapa.observaciones = 'Cambio realizado por el sistema'
						etapa.ganado = Ganado.objects.get(id=d)
						etapa.is_active = True
						etapa.save()

						# crea el nuevo ciclo
						ciclo = Ciclo()
						ciclo.fecha_inicio = date.today()
						ciclo.nombre = 0
						ciclo.fecha_fin = (date.today() + relativedelta(days=configuration.periodo_vacio))
						ciclo.ganado = Ganado.objects.get(id=d)
						ciclo.is_active = True
						ciclo.save()

						# cambia la notificación a 'REALIZADA'
						for n in notifi:
							n.state = 1
							n.save()
					else:
						try:
							notifi = Notification.objects.get(ident_cattle_id=d, state=2, module=0, name=17)
						except ObjectDoesNotExist:
							try:
								notifi = Notification.objects.get(ident_cattle_id=d, state=1, start_date=date.today(), module=0, name=17)
							except ObjectDoesNotExist:
								self.assignNotification(d, datee, 17)
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_cattle_id=d, state=2, module=0, name=17)
					except ObjectDoesNotExist:
						try:
							notifi = Notification.objects.get(ident_cattle_id=d, state=1, start_date=date.today(), module=0, name=17)
						except ObjectDoesNotExist:
							self.assignNotification(d, datee, 17)

		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2, farm=farm).count()
		for u in users:
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)

	def sendNotificationVaca(self, beliefs_vientre):
		datee = date.today() + relativedelta(days=10)
		one_day_before = date.today() - relativedelta(days=1)
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		configuration = Configuracion.objects.get(id=farm.configuracion_id)

		for d in beliefs_vientre:
			try:
				notifi = Notification.objects.get(ident_cattle_id=d, start_date=date.today(), end_date=datee, module=0, name=18 )
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.filter( Q(ident_cattle_id=d, state=2, end_date=one_day_before, module=0, name=18) | Q(ident_cattle_id=d, state=1, end_date=one_day_before, module=0, name=18) )
					if notifi.count() > 0:
						# desactiva etapa anterior
						etapa_last = Etapa.objects.get(ganado_id=d, is_active=True)
						etapa_last.is_active = False
						etapa_last.save()
						# desactiva la deferEtapa
						cattle = Ganado.objects.get(id=d)
						if DeferEtapa.objects.filter(cattle_id=cattle, is_active=True).count() > 0:
							deferEtap = DeferEtapa.objects.get(cattle_id_id=d, is_active=True)
							deferEtap.is_active = False
							deferEtap.save()
						# crea la nueva etapa
						etapa = Etapa()
						etapa.fecha_inicio = date.today()
						etapa.nombre = 4
						etapa.observaciones = 'Cambio realizado por el sistema'
						etapa.ganado = Ganado.objects.get(id=d)
						etapa.is_active = True
						etapa.save()
						for n in notifi:
							n.state = 1
							n.save()
					else:
						try:
							notifi = Notification.objects.get(ident_cattle_id=d, state=2, module=0, name=18)
						except ObjectDoesNotExist:
							self.assignNotification(d, datee, 18)	
				except ObjectDoesNotExist:
					try:
						notifi = Notification.objects.get(ident_cattle_id=d, state=2, module=0, name=18)
					except ObjectDoesNotExist:
						self.assignNotification(d, datee, 18)

		users = User.objects.filter(profile_user__ganaderia_perfil=farm)

		msg = 'Notificación, REALIZADA con ÉXITO'
		n = Notification.objects.filter(state=2, farm=farm).count()
		for u in users:
			ishout_client.emit(
					u.id,
					'notifications',
					data = {'msg': msg,
							'number_notifications': n,}
				)


	def changeAge(self, beliefs_cattles):
		for c in beliefs_cattles:
			cc = Ganado.objects.get(id=c)
			edad_anios = calcula_edad_anios(self, cc.nacimiento)
			edad_meses = calcula_edad_meses(self, cc.nacimiento)
			edad_dias = calcula_edad_dias(self, cc.nacimiento)
			if ((cc.edad_anios != edad_anios) | (cc.edad_meses != edad_meses) | (cc.edad_dias != edad_dias)):
				cc.edad_anios = edad_anios
				cc.edad_meses = edad_meses
				cc.edad_dias = edad_dias
				cc.save()

	def sendNotificationChangeCicloSeco(self, beliefs_seco):
		datee = date.today() + relativedelta(days=3)
		one_day_before = date.today() - relativedelta(days=1)
		user = User.objects.get(id=user_name)
		farm = Ganaderia.objects.get(perfil=user)
		configuration = Configuracion.objects.get(id=farm.configuracion_id)

		for d in beliefs_seco:
			# suma los dias de ordeño a la fecha inicial de lactancia
			cattle = Ganado.objects.get(ganaderia=farm, id=d)
			try:
				notifi = Notification.objects.get(ident_cattle_id=d, start_date=date.today(), module=0, name=20 )
			except ObjectDoesNotExist:
				try:
					notifi = Notification.objects.get(ident_cattle_id=d, end_date=one_day_before, module=0, name=20 )
					# hay que hacer el cambio de ciclo lactancia a seco
					for c in cattle.ciclos.all():
						if ((c.nombre==2) & (c.is_active==True)):
							c.is_active=False
							c.save()
							# crea el nuevo ciclo seco
							seco = Ciclo()
							seco.fecha_inicio = date.today()
							seco.nombre = 1
							seco.fecha_fin = date.today() + relativedelta(days=configuration.periodo_seco)
							seco.ganado = cattle
							seco.is_active=True
							seco.save()
					# desactiva la notificacion pero la coloca como realizada automaticamente
					notifi.state=1
					notifi.save()

					# pasar a false el deferetapa si ha vencido
					try:
						d = DeferEtapa.objects.get(cattle_id=d, is_active=True)
						d.is_active=False
						d.save()
					except ObjectDoesNotExist:
						pass

				except ObjectDoesNotExist:
					self.assignNotification(d, datee, 20)
			
			


import time

class AgentReproduccion(spade.Agent.Agent):
	class BehaviourReproduccion(spade.Behaviour.OneShotBehaviour):
		def onStart(self):
			print "inicio del BehaviourReproduccion . . ."

		def _process(self):
			beliefs = BeliefReproduccion()
			desires = DesireReproduccion()
			intention = IntentionReproduccion()

			msg = spade.ACLMessage.ACLMessage()
			msg.setPerformative("request")
			msg.setLanguage('español')
			msg.addReceiver(spade.AID.aid("agent_sanidad@127.0.0.1",["xmpp://agent_sanidad@127.0.0.1"]))
			character = ','
			msg.setContent(character.join( beliefs.beliefs_celo ) )
			self.myAgent.send(msg)

			msg3 = self._receive(block=True,timeout=1)
			if msg3.getContent() != '':
				if 0 in desires.desires:
					intention.sendNotificationCelo( list(msg3.getContent().split(',')) )
			if 1 in desires.desires:
				intention.sendNotificationService(beliefs.beliefs_service)
			if 2 in desires.desires:
				intention.sendNotificationVerification(beliefs.beliefs_verification)
			if 3 in desires.desires:
				intention.sendNotificationParto(beliefs.beliefs_parto)
			if 4 in desires.desires:
				intention.sendNotificationPajuela(beliefs.beliefs_pajuelas)
			if 15 in desires.desires:
				intention.sendNotificationTerneras(beliefs.beliefs_terneras)
			if 16 in desires.desires:
				intention.sendNotificationFierro(beliefs.beliefs_media)
			if 17 in desires.desires:
				intention.sendNotificationVientre(beliefs.beliefs_fierro)
			if 18 in desires.desires:
				intention.sendNotificationVaca(beliefs.beliefs_vientre)
			if 19 in desires.desires:
				intention.changeAge(beliefs.beliefs_cattles)
			if 20 in desires.desires:
				intention.sendNotificationChangeCicloSeco(beliefs.beliefs_seco)

		def onEnd(self):
			sys.exit(0)

	def _setup(self):

		template2 = spade.Behaviour.ACLTemplate()
		template2.setSender(spade.AID.aid("agent_sanidad@127.0.0.1",["xmpp://agent_sanidad@127.0.0.1"]))
		t2 = spade.Behaviour.MessageTemplate(template2)

		self.addBehaviour(self.BehaviourReproduccion(),t2)

		b = self.BehaviourReproduccion()
		self.addBehaviour(b, None)


@login_required
def ajaxRefresh(request):
	user = request.user
	global user_name
	user_name = user.id

	p = AgentProduccion("agent_produccion@127.0.0.1", "secret")
	p.start()

	r = AgentReproduccion("agent_reproduccion@127.0.0.1", "secret")
	r.start()

	s = AgentSanidad("agent_sanidad@127.0.0.1", "secret")
	s.start()

	a = AgentAlimentacion("agent_alimentacion@127.0.0.1", "secret")
	a.start()

	

	data = serializers.serialize('json', '')

	return HttpResponse(data, mimetype='application/json')
