#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from userena.utils import get_user_model
from django.shortcuts import render_to_response
from django.template import RequestContext
from profiles.models import Ganaderia, Configuracion
from ganados.models import *
from ganados.forms import *
from django.contrib.auth.models import User

from datetime import date, timedelta
import datetime, dateutil
import calendar

from dateutil.relativedelta import *

@login_required
def lista_ganado_produccion(request, username):
	id_user = User.objects.filter(username=username)
	ganaderia = Ganaderia.objects.get(perfil=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)

	if configuracion.tipo_identificacion == 'simple':

		gg = Ganado.objects.filter(ganaderia_id=ganaderia.id, genero=1, etapas__nombre=2, ciclos__nombre=2)

	else:

		gg = Ganado.objects.filter(ganaderia_id=ganaderia.id, genero=1)
	
	return render_to_response('lista_ganado_produccion.html',
		{'ganado':gg},
		context_instance=RequestContext(request))

def agrega_ganado_ordenio(request, username, ganado_id):
	id_user = User.objects.filter(username=username)
	ganaderia = Ganaderia.objects.get(perfil=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)
	ganado = Ganado.objects.get(id=ganado_id)

	fecha_hoy = datetime.date.today()
	ordenios = ganado.ordenios.all()
	num_ordenios = 1
	for ordenio in ordenios:
		if fecha_hoy == ordenio.fecha:
			num_ordenios = ordenio.numero_ordenio + 1
			cantidad = ordenio.total
	total_ordenios = configuracion.numero_ordenios
	msj = 'False'

	if request.method == 'POST':
		formOrdenio = ordenioForm(request.POST)
		if formOrdenio.is_valid():
			formOrdenio = formOrdenio.save(commit=False)
			if num_ordenios == 1:
				formOrdenio.numero_ordenio = num_ordenios
				formOrdenio.total = formOrdenio.cantidad 
			else:
				formOrdenio.numero_ordenio = num_ordenios
				formOrdenio.total = formOrdenio.cantidad + cantidad
			formOrdenio.ganado = ganado
			formOrdenio.fecha = fecha_hoy
			formOrdenio.save()
			return redirect(reverse('agrega_ganado_ordenio', kwargs={'username': username,
				'ganado_id': ganado_id}))

	else:
		formOrdenio = ordenioForm()

		if num_ordenios > total_ordenios:
			msj = "Ya has llenado tus registros hoy."

	return render_to_response('agrega_ganado_ordenio.html',
		{'ganado_id': ganado_id,
		 'formOrdenio': formOrdenio,
		 'fecha': fecha_hoy,
		 'num_ordenios': num_ordenios,
		 'total_ordenios': total_ordenios,
		 'msj': msj,
		 'range': range(num_ordenios), 
		 },
		context_instance=RequestContext(request))

def edita_ganado_ordenio(request, username, ganado_id, num_ordenio):
	id_user = User.objects.filter(username=username)
	ganaderia = Ganaderia.objects.get(perfil=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)
	ganado = Ganado.objects.get(id=ganado_id)

	fecha_hoy = datetime.date.today()
	ordenios = ganado.ordenios.all()
	cont_ordenios = 0
	for ordenio in ordenios:
		if fecha_hoy == ordenio.fecha:
			cont_ordenios += 1
			id = ordenio.id
			cantidad = ordenio.total
	

	if request.method == 'POST':
		ordenio = ganado.ordenios.get(numero_ordenio=num_ordenio, fecha=fecha_hoy)
		formOrdenio = ordenioForm(request.POST, instance=ordenio)
		formOrdenio = formOrdenio.save(commit=False)
		formOrdenio.numero_ordenio = ordenio.numero_ordenio
		if num_ordenio == '1':
			formOrdenio.total = formOrdenio.cantidad
		else:
			formOrdenio.total = formOrdenio.cantidad  + cantidad
		formOrdenio.ganado = ganado
		formOrdenio.fecha = ordenio.fecha
		formOrdenio.save()
		return redirect(reverse('edita_ganado_ordenio', kwargs={'username': username,
				'ganado_id': ganado_id, 'num_ordenio':num_ordenio
				}))
	else:
		ordenio = ganado.ordenios.get(numero_ordenio=num_ordenio, fecha=fecha_hoy)
		formOrdenio = ordenioForm(instance=ordenio)

	return render_to_response('edita_ganado_ordenio.html',
		{'ganado_id': ganado_id,
		 'formOrdenio': formOrdenio,
		 'range': range(cont_ordenios+1)},
		context_instance=RequestContext(request))


@login_required
def lista_ganado(request):
	id_user = request.user.id
	ganaderia = Ganaderia.objects.get(perfil=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)
	
	gg = Ganado.objects.filter(ganaderia_id=ganaderia.id, genero=1)
	
	return render_to_response('lista_ganado.html',
		{'ganado':gg},
		context_instance=RequestContext(request))


def calcula_edad_anios(request, date):
	# Get the current date
    now = datetime.datetime.utcnow()
    now = now.date()

    # Get the difference between the current date and the birthday
    age = dateutil.relativedelta.relativedelta(now, date)
    age = age.years

    return age

def calcula_edad_meses(request, date):
    now = datetime.datetime.utcnow()
    now = now.date()
    age = dateutil.relativedelta.relativedelta(now, date)
    age = age.months

    return age

def calcula_edad_dias(request, date):
    now = datetime.datetime.utcnow()
    now = now.date()
    age = dateutil.relativedelta.relativedelta(now, date)
    age = age.days

    return age

def calcula_etapa(request, anios, meses, etapa_ternera, etapa_vacona):
	multiplicador = 12
	if( (multiplicador * anios) + meses ) < etapa_ternera:
		valor_etapa=0
	elif ( (multiplicador * anios) + meses ) < etapa_vacona:
		valor_etapa=1
	else:
		valor_etapa=2
	return valor_etapa

@login_required
def edita_ganado(request, username, ganado_id):
	id_user = User.objects.filter(username=username)
	ganaderia = Ganaderia.objects.get(perfil=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)
	ganado = Ganado.objects.get(id=ganado_id)
	et = ganado.etapas.all()

	if configuracion.tipo_identificacion== 'simple':
		identificacion_s = Identificacion_Simple.objects.get(id=ganado.identificacion_simple.id)
	else:
		identificacion_e = Identificacion_Ecuador.objects.get(id=ganado.identificacion_ecuador.id)
	
	ganado = Ganado.objects.get(id=ganado.id)

	if request.method == 'POST':
		form2 = ganadoForm(request.POST, request.FILES, instance=ganado)

		if configuracion.tipo_identificacion == 'simple':
			form = tipoSimpleForm(request.POST, instance=identificacion_s)
			if form.is_valid() and form2.is_valid():
				# pauso guardar ganado para agregar atributos
				form2 = form2.save(commit=False)
				form2.ganaderia = ganaderia
				
				form2.identificacion_simple = form.save()
				anios = calcula_edad_anios(request, form2.nacimiento)
				meses = calcula_edad_meses(request, form2.nacimiento)
				form2.edad_anios = anios
				form2.edad_meses = meses
				form2.edad_dias = calcula_edad_dias(request, form2.nacimiento)

				# saber cual es la ultima etapa de este ganado
				et_actual = calcula_etapa(request, anios, meses, configuracion.etapa_ternera, configuracion.etapa_vacona)
				
				for etapa in et:
					if etapa.nombre == 0:
						id = etapa.nombre
					elif etapa.nombre == 1:
						id = etapa.nombre
					else:
						id = etapa.nombre
					#etapa.is_active=False
					etapa.save()
				
				if id != et_actual:
					etapa_antigua = ganado.etapas.get(nombre=id, is_active=True)
					etapa_antigua.is_active = False
					etapa_antigua.save()
					fecha = datetime.date.today()
					et = etapaForm()
					et = et.save(commit=False)
					et.fecha_inicio=fecha
					et.nombre = et_actual
					et.observaciones='ninguna observacion'
					form2.save()
					et.ganado = Ganado.objects.get(id=form2.id)
					et.is_active = True
					et.save()
				else:
					form2.save()
		else:
			form = tipoNormaEcuadorForm(request.POST, instance=identificacion_e)
			if form.is_valid() and form2.is_valid():
				# pauso guardar ganado para agregar atributos
				form2 = form2.save(commit=False)
				form2.ganaderia = ganaderia

				form2.identificacion_ecuador = form.save()
				anios = calcula_edad_anios(request, form2.nacimiento)
				meses = calcula_edad_meses(request, form2.nacimiento)
				form2.edad_anios = anios
				form2.edad_meses = meses
				form2.edad_dias = calcula_edad_dias(request, form2.nacimiento)

				# saber cual es la ultima etapa de este ganado
				
				for etapa in et:
					if etapa.nombre == 0:
						id = etapa.nombre
					elif etapa.nombre == 1:
						id = etapa.nombre
					else:
						id = etapa.nombre
					etapa.is_active=False
					etapa.save()
				
				et_actual = calcula_etapa(request, anios, meses, configuracion.etapa_ternera, configuracion.etapa_vacona)
				if id != et_actual:
					fecha = datetime.date.today()
					et = etapaForm()
					et = et.save(commit=False)
					et.fecha_inicio=fecha
					et.nombre = et_actual
					et.observaciones='ninguna observacion'
					form2.save()
					et.ganado = Ganado.objects.get(id=form2.id)
					et.is_active = True
					et.save()
				else:
					form2.save()

		return redirect(reverse('lista_ganado'))

	elif configuracion.tipo_identificacion == 'simple':
		form = tipoSimpleForm(instance=identificacion_s)
		form2 = ganadoForm(instance=ganado)
	else:
		form = tipoNormaEcuadorForm(instance=identificacion_e)
		form2 = ganadoForm(instance=ganado)

	return render_to_response('edita_ganado.html',
		{'formIdentificacion': form,
		 'formGanado': form2,
		 'id_cattle': ganado_id,
		 'ganado': ganado,
		},
		context_instance=RequestContext(request))

@login_required
def agrega_ganado(request, username):
	id_user = User.objects.filter(username=username)
	ganaderia = Ganaderia.objects.get(perfil=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)
	
	if request.method == 'POST':

		formGanado = ganadoForm(request.POST, request.FILES)
		
		if configuracion.tipo_identificacion == 'simple':
			formIdentificacion = tipoSimpleForm(request.POST)
			if formIdentificacion.is_valid() and formGanado.is_valid():
				# pauso guardar ganado para agregar atributos
				formGanado = formGanado.save(commit=False)
				# crea objeto etapa
				fecha = datetime.date.today()
				if formGanado.genero == 1:
					et = etapaForm()
					et = et.save(commit=False)
					et.fecha_inicio=fecha
					anios = calcula_edad_anios(request, formGanado.nacimiento)
					meses = calcula_edad_meses(request, formGanado.nacimiento)
					et.nombre = calcula_etapa(request, anios, meses, configuracion.etapa_ternera, configuracion.etapa_vacona)
					et.observaciones='ninguna observacion'
								
				formGanado.ganaderia = ganaderia
				
				formIdentificacion = formIdentificacion.save(commit=False)
				if Ganado.objects.filter(ganaderia=ganaderia).count() > 0:
					ganado = Ganado.objects.filter(ganaderia=ganaderia).reverse()[:1]
					for g in ganado:
						rp_old = Identificacion_Simple.objects.filter(id=g.id).order_by('rp').reverse()[:1]
						for r in rp_old:
							formIdentificacion.rp = r.rp+1
				else:
					formIdentificacion.rp = 1
				formIdentificacion.save()
				formGanado.identificacion_simple = formIdentificacion
				formGanado.edad_anios = calcula_edad_anios(request, formGanado.nacimiento)
				formGanado.edad_meses = calcula_edad_meses(request, formGanado.nacimiento)
				formGanado.edad_dias = calcula_edad_dias(request, formGanado.nacimiento)
				formGanado.save()
				if formGanado.genero == 1:
					et.ganado = Ganado.objects.get(id=formGanado.id)
					et.is_active = True
					et.save()
					if et.nombre == 2:
						periodo = Ciclo()
						periodo.nombre = 0
						periodo.fecha_inicio = date.today()
						periodo.fecha_fin = date.today()+timedelta(days=configuracion.periodo_vacio)
						periodo.ganado = formGanado
						periodo.is_active = True
						periodo.save()

				return redirect(reverse('lista_ganado'))
		else:
			formIdentificacion = tipoNormaEcuadorForm(request.POST)
			if formIdentificacion.is_valid() and formGanado.is_valid():
				# pauso guardar ganado para agregar atributos
				formGanado = formGanado.save(commit=False)
				# crea objeto etapa
				fecha = datetime.date.today()
				et = etapaForm()
				et = et.save(commit=False)
				et.fecha_inicio=fecha
				fecha_nacimiento = formGanado.nacimiento
				anios = calcula_edad_anios(request, fecha_nacimiento)
				meses = calcula_edad_meses(request, fecha_nacimiento)
				et.nombre = calcula_etapa(request, anios, meses, configuracion.etapa_ternera, configuracion.etapa_vacona)
				et.observaciones='ninguna observacion'
								
				formGanado.ganaderia = ganaderia
				
				formGanado.identificacion_ecuador = formIdentificacion.save()
				formGanado.edad_anios = calcula_edad_anios(request, formGanado.nacimiento)
				formGanado.edad_meses = calcula_edad_meses(request, formGanado.nacimiento)
				formGanado.edad_dias = calcula_edad_dias(request, formGanado.nacimiento)
				formGanado.save()
				et.ganado = Ganado.objects.get(id=formGanado.id)
				et.is_active = True
				et.save()

				return redirect(reverse('lista_ganado'))

	elif configuracion.tipo_identificacion == 'simple':
		formIdentificacion = tipoSimpleForm()
		formGanado = ganadoForm()
	else:
		formIdentificacion = tipoNormaEcuadorForm()
		formGanado = ganadoForm()

	return render_to_response('agrega_ganado.html',
		{'formIdentificacion': formIdentificacion,
		 'formGanado': formGanado
		 },
		context_instance=RequestContext(request))	

@login_required
def edita_ganado_celo(request, username, ganado_id):
	id_user = User.objects.filter(username=username)
	ganaderia = Ganaderia.objects.get(perfil=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)
	ganado = Ganado.objects.get(id=ganado_id)
	ce = ganado.celos.all()

	if ganado.celos.filter(is_active=True).count() > 0:

		if ganado.celos.get(ganado_id=ganado_id, is_active=True):
			celo_ganado = ganado.celos.get(ganado_id=ganado_id, is_active=True)
			if request.method == 'POST':
				form = editaGanadoCeloForm(request.POST)
				if form.is_valid():
					form = form.save(commit=False)
					# saber cual es la ultima etapa de este ganado
					for celo in ce:
						fecha_inicio = celo.fecha_inicio
						id = celo.id

					if fecha_inicio != form.fecha_inicio:
						for celo in ce:
							celo.is_active = False
							celo.save()
						d2=datetime.timedelta(hours=configuracion.celo_duracion)
						age=form.fecha_inicio + d2
						form.estado = 0
						form.fecha_fin = age
						form.ganado = ganado
						form.is_active = True
						form.save()
						return redirect(reverse('lista_ganado'))
					else:
						c = Celo.objects.get(id=id)
						c.observaciones=form.observaciones
						c.save()

						return redirect(reverse('lista_ganado'))
				
			else:
				form = editaGanadoCeloForm(instance=celo_ganado)
		
	else:
		form = editaGanadoCeloForm()
		if request.method == 'POST':
			form = editaGanadoCeloForm(request.POST)
			if form.is_valid():
				form = form.save(commit=False)
				d2=datetime.timedelta(hours=configuracion.celo_duracion)
				age=form.fecha_inicio + d2
				form.estado = 0
				form.fecha_fin = age
				form.ganado = ganado
				form.is_active = True
				form.save()
				return redirect(reverse('lista_ganado'))

	if ganado.celos.all():
		return render_to_response('edita_ganado_celo.html',
			{'form': form,
			 'ganado_id': ganado_id
			},
			context_instance=RequestContext(request))
	else:
		return render_to_response('edita_ganado_celo.html',
			{'form': form,
			 'ganado_id': ganado_id,
			},
			context_instance=RequestContext(request))

@login_required
def add_service(request, id_cattle):
	user = request.user
	cattle = Ganado.objects.get(id=id_cattle)
	
	if request.method == 'POST':
		farm = Ganaderia.objects.get(perfil=user)
		formAttempt = attemptForm(request.POST)

		if formAttempt.is_valid():
			formAttempt = formAttempt.save(commit=False)

			verification = Verification()
			verification.initial_date = date.today()
			verification.is_active = True
			verification.cattle = cattle
			verification.save()
			
			formAttempt.attempt = 1
			date_actual = date.today()+timedelta(days=21)
			formAttempt.attempt_date = date_actual
			formAttempt.verification = verification
			formAttempt.save()

			for i in range(2, farm.configuracion.intentos_verificacion_celo+1):
				date_actual = date_actual+timedelta(days=21)
				attempt = Attempt()
				attempt.attempt = i
				attempt.attempt_date = date_actual
				attempt.verification = verification
				attempt.type_conception = formAttempt.type_conception
				attempt.rp_father = formAttempt.rp_father
				attempt.save()

			return redirect(reverse('lista_ganado'))
			
	elif request.method == 'GET':
		v = Verification.objects.filter(is_active=True, cattle=id_cattle).count()
		if v > 0:
			return redirect(reverse('add_attempt_service', kwargs={'id_cattle': id_cattle}))
		else:
			formAttempt = attemptForm()

	return render_to_response('add_service.html',
		{'id_cattle': id_cattle,
		 'formAttempt': formAttempt},
		context_instance=RequestContext(request))

@login_required
def add_attempt_service(request, id_cattle):
	cattle = Ganado.objects.get(id=id_cattle)
	attempts = Attempt.objects.filter(verification__cattle=cattle, verification__is_active=True).order_by('id')

	return render_to_response('add_attempt_service.html',
		{'attempts': attempts},
		context_instance=RequestContext(request))

@login_required
def verify_attempt(request, id_attempt):
	user = request.user
	farm = Ganaderia.objects.get(perfil=user)
	configuration = Configuracion.objects.get(id=farm.configuracion_id)
	attempt = Attempt.objects.get(id=id_attempt)

	if request.method == 'POST':
		formAttempt = verifyAttemptForm(request.POST, instance=attempt) 
		if formAttempt.is_valid():
			
			formAttempt = formAttempt.save(commit=False)
			formAttempt.save()
			# si fue correcto
			if formAttempt.state == 0:
				attempt.verification.is_active=False
				attempt.verification.save()
				# cambio el is_active de etapa y celo anterior
				ganado = Ganado.objects.get(id=attempt.verification.cattle.id)
				#etapa = Etapa.objects.get(ganado_id=ganado.id, is_active=True)
				#etapa.is_active = False
				#etapa.save()
				celo = Celo.objects.get(ganado_id=ganado.id, is_active=True)
				celo.is_active=False
				celo.estado = 1
				celo.save()
				
				# agrego el nuevo ciclo
				ciclo = Ciclo.objects.get(ganado_id=ganado.id, is_active=True)
				ciclo.is_active = False
				ciclo.save()
				ciclo = Ciclo()
				ciclo.nombre = 3
				ciclo.fecha_inicio = date.today()
				ciclo.fecha_fin = date.today()+timedelta(days=configuration.periodo_gestacion)
				ciclo.ganado = ganado
				ciclo.is_active = True
				ciclo.save()

				# agrego la gestacion
				gestacion = Gestacion()
				gestacion.fecha_servicio = date.today()
				gestacion.fecha_parto = date.today() + timedelta(days=configuration.periodo_gestacion)
				gestacion.is_active = True
				gestacion.ganado = ganado
				gestacion.save()
				
				return redirect(reverse('lista_ganado'))

			id_cattle = attempt.verification.cattle_id 
			return redirect(reverse('add_attempt_service', kwargs={'id_cattle': id_cattle}))
	else:
		formVerifyAttempt = verifyAttemptForm(instance=attempt)

	return render_to_response('verify_attempt.html',
		{'formVerifyAttempt': formVerifyAttempt},
		context_instance=RequestContext(request))

@login_required
def gestacion(request, id_cattle):
	user = request.user
	farm = Ganaderia.objects.get(perfil=user)
	configuration = Configuracion.objects.get(id=farm.configuracion_id)
	ganado = Ganado.objects.get(id=id_cattle)
	gestacion = Gestacion.objects.get(ganado=ganado, is_active=True)

	if request.method == 'POST':
		formGestacion = gestacionForm(request.POST, instance=gestacion)
		if formGestacion.is_valid():
			formGestacion = formGestacion.save(commit=False)
			# gestacion en false
			gestacion.is_active = False
			gestacion.save()
			# desactivar el anterior ciclo
			ciclo = Ciclo.objects.get(ganado=ganado, is_active=True)
			ciclo.is_active = False
			ciclo.save()
			# nuevo ciclo de lactancia
			ciclo = Ciclo()
			ciclo.nombre = 2
			ciclo.fecha_inicio = date.today()
			ciclo.fecha_fin = date.today() + timedelta(days=configuration.periodo_lactancia)
			ciclo.is_active = True
			ciclo.ganado = ganado
			ciclo.save()
			# nuevo ciclo vacio
			ciclo = Ciclo()
			ciclo.nombre = 0
			ciclo.fecha_inicio = date.today()
			ciclo.fecha_fin = date.today() + timedelta(days=configuration.periodo_vacio)
			ciclo.is_active = True
			ciclo.ganado = ganado
			ciclo.save()

			formGestacion.save()
			return redirect(reverse('lista_ganado'))
	else:
		formGestacion = gestacionForm(instance=gestacion)
	return render_to_response('gestacion.html',
		{'formGestacion': formGestacion,
		 'id_cattle': id_cattle},
		context_instance=RequestContext(request))
	

@login_required
def problem_gestacion(request, id_cattle):
	user = request.user
	farm = Ganaderia.objects.get(perfil=user)
	configuration = Configuracion.objects.get(id=farm.configuracion_id)
	ganado = Ganado.objects.get(id=id_cattle)
	gestacion = Gestacion.objects.get(ganado=ganado, is_active=True)

	if request.method == 'POST':
		formProblemGestacion = problemGestacionForm(request.POST)
		if formProblemGestacion.is_valid():
			formProblemGestacion = formProblemGestacion.save(commit=False)
			# en el caso de aborto
			if formProblemGestacion.tipo_problema == 0:
				# desactivar el anterior ciclo
				ciclo = Ciclo.objects.get(ganado=ganado, is_active=True)
				ciclo.is_active = False
				ciclo.save()
				# nuevo ciclo vacio
				ciclo = Ciclo()
				ciclo.nombre = 0
				ciclo.fecha_inicio = date.today()
				ciclo.fecha_fin = date.today() + timedelta(days=configuration.periodo_vacio)
				ciclo.is_active = True
				ciclo.ganado = ganado
				ciclo.save()
				# gestacion en false
				gestacion.is_active = False
				gestacion.save()
			# en el caso de nacido muerto
			elif formProblemGestacion.tipo_problema == 1:
				# desactivar el anterior ciclo
				ciclo = Ciclo.objects.get(ganado=ganado, is_active=True)
				ciclo.is_active = False
				ciclo.save()
				# nuevo ciclo vacio
				ciclo = Ciclo()
				ciclo.nombre = 1
				ciclo.fecha_inicio = date.today()
				ciclo.fecha_fin = date.today() + timedelta(days=configuration.periodo_vacio)
				ciclo.is_active = True
				ciclo.ganado = ganado
				ciclo.save()
				# gestacion en false
				gestacion.is_active = False
				gestacion.save()
			# en el caso de madre muerta
			elif formProblemGestacion.tipo_problema == 2:
				# ciclo en false
				ciclo = Ciclo.objects.get(ganado=ganado, is_active=True)
				ciclo.is_active = False
				ciclo.save()
				# se llena el DownCattle
				down_cattle = DownCattle()
				down_cattle.date = date.today()
				down_cattle.cause_down = 0
				down_cattle.observations = 'Desceso del animal'
				down_cattle.save()
				# se asigna el down_cattle al ganado
				ganado.down_cattle = down_cattle
				ganado.save()
				# gestacion en false
				gestacion.is_active = False
				gestacion.save()
				# se registra la cria
				attempt = Attempt.objects.get(verification_id=ganado.id, state=0)
				cria = Ganado()
				cria.ganaderia = farm
				cria.nacimiento = date.today()
				cria.genero = 2
				cria.raza = 12
				cria.forma_concepcion = attempt.type_conception
				cria.observaciones = 'Nacido pero sin madre'
				cria.edad_anios = calcula_edad_anios(request, formProblemGestacion.fecha_problema)
				cria.edad_meses = calcula_edad_meses(request, formProblemGestacion.fecha_problema)
				cria.edad_dias = calcula_edad_dias(request, formProblemGestacion.fecha_problema)
				# se crea la identificacion dependiendo (simple o ecuador)
				if configuration.tipo_identificacion == 'simple':
					id_simple = Identificacion_Simple()
					if Ganado.objects.filter(ganaderia=farm).count() > 0:
						ganad = Ganado.objects.filter(ganaderia=farm).reverse()[:1]
						for g in ganad:
							rp_old = Identificacion_Simple.objects.filter(id=g.id).order_by('rp').reverse()[:1]
							for r in rp_old:
								id_simple.rp = r.rp+1
					id_simple.nombre = 'Temporal'
					id_simple.rp_madre = ganado.identificacion_simple.rp
					id_simple.rp_padre = attempt.rp_father
					id_simple.save()
					cria.identificacion_simple = id_simple
					cria.save()
				else:
					id_ecuador = Identificacion_Ecuador()
					if Ganado.objects.filter(ganaderia=farm).count() > 0:
						ganad = Ganado.objects.filter(ganaderia=farm).reverse()[:1]
						for g in ganad:
							rp_old = Identificacion_Ecuador.objects.filter(id=g.id).order_by('rp').reverse()[:1]
							for r in rp_old:
								id_ecuador.rp = r.rp+1
					id_ecuador.siglas_pais = 'EC'
					id_ecuador.codigo_pais = '593'
					id_ecuador.codigo_provincia = '7'
					id_ecuador.numero_serie = '12345'
					id_ecuador.codigo_barras = '6789'
					id_ecuador.nombre = 'Temporal'
					id_ecuador.rp_madre = ganado.identificacion_ecuador.rp
					id_ecuador.rp_padre = attempt.rp_father
					id_ecuador.save()
					cria.identificacion_ecuador = id_ecuador
					cria.save()
			# en el caso de los dos muertos
			elif formProblemGestacion.tipo_problema == 3:
				# ciclo en false
				ciclo = Ciclo.objects.get(ganado=ganado, is_active=True)
				ciclo.is_active = False
				ciclo.save()
				# se llena el DownCattle
				down_cattle = DownCattle()
				down_cattle.date = date.today()
				down_cattle.cause_down = 0
				down_cattle.observations = 'Desceso del animal'
				down_cattle.save()
				# se asigna el down_cattle al ganado
				ganado.down_cattle = down_cattle
				ganado.save()
				# gestacion en false
				gestacion.is_active = False
				gestacion.save()

			formProblemGestacion.save()
			gestacion.problema = formProblemGestacion
			gestacion.save()

			return redirect(reverse('lista_ganado'))
	elif request.method == 'GET':
		formProblemGestacion = problemGestacionForm()

	return render_to_response('problem_gestacion.html',
			{'formProblemGestacion': formProblemGestacion,
			 'id_cattle': id_cattle},
			context_instance=RequestContext(request))
