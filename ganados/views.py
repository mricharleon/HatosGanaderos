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
from django.contrib.auth.models import User

from datetime import date
import datetime, dateutil
import calendar

from dateutil.relativedelta import *

@login_required
def lista_ganado_produccion(request, username):
	id_user = User.objects.filter(username=username)
	ganaderia = Ganaderia.objects.get(perfil_id=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)

	if configuracion.tipo_identificacion == 'simple':

		gg = Ganado.objects.filter(ganaderia_id=ganaderia.id)

	else:

		gg = Ganado.objects.filter(ganaderia_id=ganaderia.id)
	
	return render_to_response('lista_ganado_produccion.html',
		{'ganado':gg},
		context_instance=RequestContext(request))

def agrega_ganado_ordenio(request, username, ganado_id):
	id_user = User.objects.filter(username=username)
	ganaderia = Ganaderia.objects.get(perfil_id=id_user)
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
	ganaderia = Ganaderia.objects.get(perfil_id=id_user)
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
def lista_ganado(request, username):
	id_user = User.objects.filter(username=username)
	ganaderia = Ganaderia.objects.get(perfil_id=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)

	if configuracion.tipo_identificacion == 'simple':

		gg = Ganado.objects.filter(ganaderia_id=ganaderia.id)

	else:

		gg = Ganado.objects.filter(ganaderia_id=ganaderia.id)
	
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
	ganaderia = Ganaderia.objects.get(perfil_id=id_user)
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

		return redirect(reverse('lista_ganado', kwargs={'username': username}))

	elif configuracion.tipo_identificacion == 'simple':
		form = tipoSimpleForm(instance=identificacion_s)
		form2 = ganadoForm(instance=ganado)
	else:
		form = tipoNormaEcuadorForm(instance=identificacion_e)
		form2 = ganadoForm(instance=ganado)

	return render_to_response('edita_ganado.html',
		{'form': form,
		 'form2': form2,
		 'ganado_id': ganado_id
		},
		context_instance=RequestContext(request))

@login_required
def agrega_ganado(request, username):
	id_user = User.objects.filter(username=username)
	ganaderia = Ganaderia.objects.get(perfil_id=id_user)
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
				et = etapaForm()
				et = et.save(commit=False)
				et.fecha_inicio=fecha
				anios = calcula_edad_anios(request, formGanado.nacimiento)
				meses = calcula_edad_meses(request, formGanado.nacimiento)
				et.nombre = calcula_etapa(request, anios, meses, configuracion.etapa_ternera, configuracion.etapa_vacona)
				et.observaciones='ninguna observacion'
								
				formGanado.ganaderia = ganaderia
				
				formGanado.identificacion_simple = formIdentificacion.save()
				formGanado.edad_anios = calcula_edad_anios(request, formGanado.nacimiento)
				formGanado.edad_meses = calcula_edad_meses(request, formGanado.nacimiento)
				formGanado.edad_dias = calcula_edad_dias(request, formGanado.nacimiento)
				formGanado.save()
				et.ganado = Ganado.objects.get(id=formGanado.id)
				et.is_active = True
				et.save()

				return redirect(reverse('lista_ganado', kwargs={'username': username}))
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

				return redirect(reverse('lista_ganado', kwargs={'username': username}))

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
	ganaderia = Ganaderia.objects.get(perfil_id=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)
	ganado = Ganado.objects.get(id=ganado_id)
	ce = ganado.celos.all()

	if ganado.celos.all():

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
						return redirect(reverse('lista_ganado', kwargs={'username': username}))
					else:
						c = Celo.objects.get(id=id)
						c.observaciones=form.observaciones
						c.save()

						return redirect(reverse('lista_ganado', kwargs={'username': username}))
				
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
				return redirect(reverse('lista_ganado', kwargs={'username': username}))

	if ganado.celos.all():
		return render_to_response('edita_ganado_celo.html',
			{'form': form,
			 'ganado_id': ganado_id,
			 'fecha_inicio': celo_ganado.fecha_inicio
			},
			context_instance=RequestContext(request))
	else:
		return render_to_response('edita_ganado_celo.html',
			{'form': form,
			 'ganado_id': ganado_id,
			},
			context_instance=RequestContext(request))
