#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from userena.utils import get_user_model
from django.shortcuts import render_to_response
from django.template import RequestContext
from notifications.models import Notification
from profiles.models import Ganaderia, Configuracion
from ganados.models import *
from ganados.forms import *
from django.contrib.auth.models import User
from profiles.views import number_messages

from datetime import date, timedelta
import datetime, dateutil
import calendar
import pytz

from dateutil.relativedelta import *

def add_down_cattle(request, id_cattle):
	cattle = Ganado.objects.get(id=id_cattle)
	if request.method == 'POST':
		formDownCattleForm = downCattleForm(request.POST)
		if formDownCattleForm.is_valid():
			cattle.down_cattle = formDownCattleForm.save()
			cattle.save()
			return redirect(reverse('add_cattle'))
	else:
		formDownCattleForm = downCattleForm()
	return render_to_response('add_down_cattle.html',
		{'formDownCattleForm': formDownCattleForm,
		 'cattle': cattle},
		 context_instance=RequestContext(request))

def list_down_cattle(request):
	user = request.user
	farm = Ganaderia.objects.get(perfil=user)
	cattles = Ganado.objects.filter(ganaderia=farm).exclude(down_cattle=None)
	formDownCattleForm = downCattleForm()
	return render_to_response('list_down_cattle.html',
		{'cattles': cattles},
		 context_instance=RequestContext(request))

def add_down_insemination(request, id_sperm):
	sperm = Insemination.objects.get(id=id_sperm)
	if request.method == 'POST':
		formDownInseminationForm = downInseminationForm(request.POST)
		if formDownInseminationForm.is_valid():
			sperm.down_insemination = formDownInseminationForm.save()
			sperm.save()
			return redirect(reverse('add_cattle'))
	else:
		formDownInseminationForm = downInseminationForm()
	return render_to_response('add_down_insemination.html',
		{'formDownInseminationForm': formDownInseminationForm,
		 'sperm': sperm},
		 context_instance=RequestContext(request))


"""
metodo lista_ganado_produccion
"""
@login_required
def lista_ganado_produccion(request):
	user = request.user
	number_message = number_messages(request, user.username)

	return render_to_response('lista_ganado_produccion.html',
		{'number_messages': number_message},
		context_instance=RequestContext(request))


"""
metodo agrega_ganado_ordenio
"""
def agrega_ganado_ordenio(request, ganado_id):
	user = request.user
	id_user = User.objects.filter(username=user.username)
	number_message = number_messages(request, user.username)
	ganaderia = Ganaderia.objects.get(perfil=id_user)
	configuracion = Configuracion.objects.get(id=ganaderia.configuracion_id)
	ganado = Ganado.objects.get(id=ganado_id)

	fecha_hoy = datetime.date.today()
	ordenios = ganado.ordenios.all()
	num_ordenios = 1
	cantidad = 0
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
			# verifico que es ordenio unico
			if (formOrdenio.unique_ordenio) & (num_ordenios==1):
				formOrdenio.numero_ordenio = num_ordenios
				formOrdenio.total = formOrdenio.cantidad
				formOrdenio.ganado = ganado
				formOrdenio.fecha = fecha_hoy
				formOrdenio.save()
				rangee = range(1)
				for i in range(2, total_ordenios+1):
					last_ordenio = Ordenio.objects.get(fecha=date.today(), numero_ordenio=1, ganado=ganado)
					ordenio = Ordenio()
					ordenio.fecha = date.today()
					ordenio.numero_ordenio = i
					ordenio.cantidad = 0
					ordenio.total = last_ordenio.total
					ordenio.observaciones = 'Ninguna (Agregada por el sistema)'
					ordenio.ganado = ganado
					ordenio.unique_ordenio = False
					ordenio.save()

			else:
				formOrdenio.numero_ordenio = num_ordenios
				formOrdenio.total = formOrdenio.cantidad + cantidad
				formOrdenio.ganado = ganado
				formOrdenio.fecha = fecha_hoy
				formOrdenio.save()
				rangee = range(num_ordenios)
			return redirect(reverse('agrega_ganado_ordenio', kwargs={'ganado_id': ganado_id}))

	else:
		formOrdenio = ordenioForm()
		rangee = range(num_ordenios)
		try:
			ordenio = Ordenio.objects.get(fecha=date.today(), numero_ordenio=1)
			if ( ((num_ordenios==total_ordenios) & (ordenio.unique_ordenio)) | (num_ordenios > total_ordenios) ):
				msj = "Ya has llenado tus registros hoy."
				if (total_ordenios == 2) & (ordenio.unique_ordenio):
					rangee = range(2)
		except ObjectDoesNotExist:
			pass

	return render_to_response('agrega_ganado_ordenio.html',
		{'ganado_id': ganado_id,
		 'formOrdenio': formOrdenio,
		 'fecha': fecha_hoy,
		 'num_ordenios': num_ordenios,
		 'total_ordenios': total_ordenios,
		 'msj': msj,
		 'range': rangee,
		 'number_messages': number_message},
		context_instance=RequestContext(request))

def edita_ganado_ordenio(request, ganado_id, num_ordenio):
	user = request.user
	id_user = User.objects.filter(username=user.username)
	number_message = number_messages(request, user.username)
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
		# verifico si esta activo unique_ordenio
		initial_ordenio = ganado.ordenios.get(numero_ordenio=1, fecha=fecha_hoy)
		# obtengo el registro del ordeño a editar
		ordenio = ganado.ordenios.get(numero_ordenio=num_ordenio, fecha=fecha_hoy)
		formOrdenio = ordenioForm(request.POST, instance=ordenio)
		formOrdenio = formOrdenio.save(commit=False)
		formOrdenio.numero_ordenio = ordenio.numero_ordenio
		if (num_ordenio == '1') & (initial_ordenio.unique_ordenio):
			formOrdenio.total = formOrdenio.cantidad

			for i in range(2, (configuracion.numero_ordenios+1)):
				ordenio2 = Ordenio.objects.get(numero_ordenio=i, fecha=date.today())
				ordenio2.total = formOrdenio.cantidad
				ordenio2.save()
		else:
			if num_ordenio == '1':
				n = (int(num_ordenio)+1)
			else:
				n = num_ordenio
			for i in range(int(n), (configuracion.numero_ordenios+1)):
				try:
					ordenio2 = Ordenio.objects.get(numero_ordenio=i, fecha=date.today())
					if num_ordenio == '1':
						sumar = ordenio2.cantidad
						formOrdenio.total = (formOrdenio.cantidad)
					else:
						ordenio3 = Ordenio.objects.get(fecha=date.today(), numero_ordenio=(int(n)-1))
						sumar = ordenio3.cantidad
						formOrdenio.total = (formOrdenio.cantidad + sumar)
					# sumo total
					ordenio2.total = (formOrdenio.cantidad + sumar)
					ordenio2.save()
				except ObjectDoesNotExist:
					formOrdenio.total = formOrdenio.cantidad

		formOrdenio.ganado = ganado
		formOrdenio.fecha = ordenio.fecha
		formOrdenio.save()
		return redirect(reverse('edita_ganado_ordenio', kwargs={'ganado_id': ganado_id, 'num_ordenio':num_ordenio
				}))
	else:
		ordenio = ganado.ordenios.get(numero_ordenio=num_ordenio, fecha=fecha_hoy)
		formOrdenio = ordenioForm(instance=ordenio)

		ordenio = Ordenio.objects.get(fecha=date.today(), numero_ordenio=1)
		if cont_ordenios > cantidad:
			if (cantidad == 2) & (ordenio.unique_ordenio):
				rangee = range(2)

		if (ordenio.unique_ordenio):
			num_ordenios = 1
			rangee = range(2)
		else:
			rangee = range(cont_ordenios+1)
			num_ordenios = cont_ordenios

	return render_to_response('edita_ganado_ordenio.html',
		{'ganado_id': ganado_id,
		 'formOrdenio': formOrdenio,
		 'range': rangee,
		 'number_messages': number_message,
		 'num_ordenios': num_ordenios},
		context_instance=RequestContext(request))


@login_required
def list_cattle(request):
	user = request.user
	number_message = number_messages(request, user.username)
	return render_to_response('list_cattle.html',
		{'number_messages': number_message},
		context_instance=RequestContext(request))

@login_required
def list_cattle_terneras(request):
	user = request.user
	number_message = number_messages(request, user.username)
	return render_to_response('list_cattle_ternera.html',
		{'number_messages': number_message},
		context_instance=RequestContext(request))

@login_required
def list_cattle_media(request):
	user = request.user
	number_message = number_messages(request, user.username)
	return render_to_response('list_cattle_media.html',
		{'number_messages': number_message},
		context_instance=RequestContext(request))

@login_required
def list_cattle_fierro(request):
	user = request.user
	number_message = number_messages(request, user.username)
	return render_to_response('list_cattle_fierro.html',
		{'number_messages': number_message},
		context_instance=RequestContext(request))

@login_required
def list_cattle_vientre(request):
	user = request.user
	number_message = number_messages(request, user.username)
	return render_to_response('list_cattle_vientre.html',
		{'number_messages': number_message},
		context_instance=RequestContext(request))

@login_required
def list_cattle_vaca(request):
	user = request.user
	number_message = number_messages(request, user.username)
	return render_to_response('list_cattle_vaca.html',
		{'number_messages': number_message},
		context_instance=RequestContext(request))


@login_required
def list_cattle_male(request):
	user = request.user
	number_message = number_messages(request, user.username)
	return render_to_response('list_cattles_male.html',
		{'number_messages': number_message},
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

def calcula_etapa(request, anios, meses, etapa_ternera, etapa_vacona_media, etapa_vacona_fierro, etapa_vacona_vientre, etapa_vaca):
	multiplicador = 12
	if( (multiplicador * anios) + meses ) < etapa_ternera:
		valor_etapa=0
	elif ( (multiplicador * anios) + meses ) < etapa_vacona_media:
		valor_etapa=1
	elif ( (multiplicador * anios) + meses ) < etapa_vacona_fierro:
		valor_etapa=2
	elif ( (multiplicador * anios) + meses ) < etapa_vacona_vientre:
		valor_etapa=3
	else:
		valor_etapa=4
	return valor_etapa



@login_required
def edita_ganado(request, ganado_id):
	id_user = request.user
	number_message = number_messages(request, id_user.username)
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
				et_actual = calcula_etapa(request, anios, meses, configuracion.etapa_ternera, configuracion.etapa_vacona_media, configuracion.etapa_vacona_fierro, configuracion.etapa_vacona_vientre, configuracion.etapa_vaca)

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
				et_actual = calcula_etapa(request, anios, meses, configuracion.etapa_ternera, configuracion.etapa_vacona_media, configuracion.etapa_vacona_fierro, configuracion.etapa_vacona_vientre, configuracion.etapa_vaca)

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

		return redirect(reverse('list_cattle'))

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
		 'number_messages': number_message},
		context_instance=RequestContext(request))

@login_required
def edit_cattle_male(request, cattle_id):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	configuration = Configuracion.objects.get(id=farm.configuracion_id)
	cattle = Ganado.objects.get(id=cattle_id)

	if configuration.tipo_identificacion== 'simple':
		identification_simple = Identificacion_Simple.objects.get(id=cattle.identificacion_simple.id)
	else:
		identification_ecuador = Identificacion_Ecuador.objects.get(id=cattle.identificacion_ecuador.id)

	if request.method == 'POST':
		form2 = ganadoForm(request.POST, request.FILES, instance=cattle)

		if configuration.tipo_identificacion == 'simple':
			form = tipoSimpleForm(request.POST, instance=identification_simple)
			if form.is_valid() and form2.is_valid():
				# pauso guardar ganado para agregar atributos
				form2 = form2.save(commit=False)
				form2.ganaderia = farm

				form2.identificacion_simple = form.save()
				anios = calcula_edad_anios(request, form2.nacimiento)
				meses = calcula_edad_meses(request, form2.nacimiento)
				form2.edad_anios = anios
				form2.edad_meses = meses
				form2.edad_dias = calcula_edad_dias(request, form2.nacimiento)
				form2.save()
		else:
			form = tipoNormaEcuadorForm(request.POST, instance=identification_ecuador)
			if form.is_valid() and form2.is_valid():
				# pauso guardar ganado para agregar atributos
				form2 = form2.save(commit=False)
				form2.ganaderia = farm

				form2.identificacion_ecuador = form.save()
				anios = calcula_edad_anios(request, form2.nacimiento)
				meses = calcula_edad_meses(request, form2.nacimiento)
				form2.edad_anios = anios
				form2.edad_meses = meses
				form2.edad_dias = calcula_edad_dias(request, form2.nacimiento)
				form2.save()

		return redirect(reverse('list_cattle_male'))

	elif configuration.tipo_identificacion == 'simple':
		form = tipoSimpleForm(instance=identification_simple)
		form2 = ganadoForm(instance=cattle)
	else:
		form = tipoNormaEcuadorForm(instance=identification_ecuador)
		form2 = ganadoForm(instance=cattle)

	return render_to_response('edita_ganado.html',
		{'formIdentificacion': form,
		 'formGanado': form2,
		 'id_cattle': cattle_id,
		 'ganado': cattle,
		 'number_messages': number_message},
		context_instance=RequestContext(request))

@login_required
def add_insemination(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)

	if request.method == 'POST':
		formInsemination = inseminationForm(request.POST)
		if formInsemination.is_valid():
			formInsemination = formInsemination.save(commit=False)
			if Insemination.objects.filter(farm=farm).count() > 0:
				insemination = Insemination.objects.filter(farm=farm).order_by('rp').reverse()[:1]
				for i in insemination:
					formInsemination.rp = i.rp+1
			else:
				formInsemination.rp = 1

			formInsemination.farm = farm
			formInsemination.save()

			return redirect(reverse('list_insemination'))

	elif request.method == 'GET':
		formInsemination = inseminationForm()
	return render_to_response('add_insemination.html',
			{'formInsemination': formInsemination,
			 'number_messages': number_message},
			context_instance=RequestContext(request))

@login_required
def edit_insemination(request, insemination_id):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	insemination = Insemination.objects.get(id=insemination_id)

	if request.method == 'POST':
		formInsemination = inseminationForm(request.POST, instance=insemination)
		if formInsemination.is_valid():
			formInsemination = formInsemination.save(commit=False)
			formInsemination.farm = farm
			formInsemination.rp = insemination.rp
			formInsemination.save()

			return redirect(reverse('list_insemination'))

	else:
		formInsemination = inseminationForm(instance=insemination)

	return render_to_response('edit_insemination.html',
		{'formInsemination': formInsemination,
		 'insemination_id': insemination_id,
		 'number_messages': number_message},
		context_instance=RequestContext(request))

@login_required
def list_insemination(request):
	user = request.user
	number_message = number_messages(request, user.username)
	return render_to_response('list_insemination.html',
		{'number_messages': number_message},
		context_instance=RequestContext(request))


@login_required
def add_cattle(request):
	user = request.user
	number_message = number_messages(request, user.username)
	try:
		farm = Ganaderia.objects.get(perfil=user)
	except ObjectDoesNotExist:
		return redirect(reverse('agrega_ganaderia_config'))
	configuration = Configuracion.objects.get(id=farm.configuracion_id)

	if request.method == 'POST':

		formGanado = ganadoForm(request.POST, request.FILES)

		if configuration.tipo_identificacion == 'simple':
			formIdentificacion = tipoSimpleForm(request.POST)
			if formIdentificacion.is_valid() and formGanado.is_valid():
				# pauso guardar ganado para agregar atributos
				formGanado = formGanado.save(commit=False)
				formIdentificacion = formIdentificacion.save(commit=False)

				if Ganado.objects.filter(ganaderia=farm).count() > 0:
					cattle = Ganado.objects.filter(ganaderia=farm).order_by('id').reverse()[:1]
					for g in cattle:
						rp_old = Identificacion_Simple.objects.filter(id=g.identificacion_simple.id).order_by('rp').reverse()[:1]
						for r in rp_old:
							formIdentificacion.rp = r.rp+1
				else:
					formIdentificacion.rp = configuration.initial_rp


				# disminuir las pajuelas
				if formGanado.forma_concepcion == 0: # inseminacion
					try:
						insemination = Insemination.objects.get(rp=formIdentificacion.rp_padre)
						insemination.amount_pajuelas = insemination.amount_pajuelas - 1
						insemination.save()
					except ObjectDoesNotExist:
						pass


				# crea objeto etapa
				date = datetime.date.today()
				if formGanado.genero == 1:
					et = etapaForm()
					et = et.save(commit=False)
					et.fecha_inicio=date
					anios = calcula_edad_anios(request, formGanado.nacimiento)
					meses = calcula_edad_meses(request, formGanado.nacimiento)
					et.nombre = calcula_etapa(request, anios, meses, configuration.etapa_ternera, configuration.etapa_vacona_media, configuration.etapa_vacona_fierro, configuration.etapa_vacona_vientre, configuration.etapa_vaca)
					et.observaciones='ninguna observacion'

				formGanado.ganaderia = farm


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
					if (et.nombre == 3) | (et.nombre == 4):
						periodo = Ciclo()
						periodo.nombre = 0
						periodo.fecha_inicio = date.today()
						periodo.fecha_fin = date.today()+timedelta(days=configuration.periodo_vacio)
						periodo.ganado = formGanado
						periodo.is_active = True
						periodo.save()

				return redirect(reverse('list_cattle'))
		else:
			formIdentificacion = tipoNormaEcuadorForm(request.POST)
			if formIdentificacion.is_valid() and formGanado.is_valid():
				# pauso guardar ganado para agregar atributos
				formGanado = formGanado.save(commit=False)
				# crea objeto etapa
				date = datetime.date.today()
				if formGanado.genero == 1:
					et = etapaForm()
					et = et.save(commit=False)
					et.fecha_inicio=date
					anios = calcula_edad_anios(request, formGanado.nacimiento)
					meses = calcula_edad_meses(request, formGanado.nacimiento)
					et.nombre = calcula_etapa(request, anios, meses, configuration.etapa_ternera, configuration.etapa_vacona_media, configuration.etapa_vacona_fierro, configuration.etapa_vacona_vientre, configuration.etapa_vaca)
					et.observaciones='ninguna observacion'

				formGanado.ganaderia = farm

				formIdentificacion = formIdentificacion.save(commit=False)
				if Ganado.objects.filter(ganaderia=farm).count() > 0:
					cattle = Ganado.objects.filter(ganaderia=farm).order_by('id').reverse()[:1]
					for g in cattle:
						rp_old = Identificacion_Ecuador.objects.filter(id=g.identificacion_ecuador.id).order_by('rp').reverse()[:1]
						for r in rp_old:
							formIdentificacion.rp = r.rp+1
				else:
					formIdentificacion.rp = configuration.initial_rp
				formIdentificacion.save()
				formGanado.identificacion_ecuador = formIdentificacion
				formGanado.edad_anios = calcula_edad_anios(request, formGanado.nacimiento)
				formGanado.edad_meses = calcula_edad_meses(request, formGanado.nacimiento)
				formGanado.edad_dias = calcula_edad_dias(request, formGanado.nacimiento)
				formGanado.save()
				if formGanado.genero == 1:
					et.ganado = Ganado.objects.get(id=formGanado.id)
					et.is_active = True
					et.save()
					if (et.nombre == 3) | (et.nombre == 4):
						periodo = Ciclo()
						periodo.nombre = 0
						periodo.fecha_inicio = date.today()
						periodo.fecha_fin = date.today()+timedelta(days=configuration.periodo_vacio)
						periodo.ganado = formGanado
						periodo.is_active = True
						periodo.save()

				return redirect(reverse('list_cattle'))

	elif configuration.tipo_identificacion == 'simple':
		formIdentificacion = tipoSimpleForm()
		formGanado = ganadoForm()
	else:
		formIdentificacion = tipoNormaEcuadorForm()
		formGanado = ganadoForm()

	return render_to_response('add_cattle.html',
		{'formIdentificacion': formIdentificacion,
		 'formGanado': formGanado,
		 'number_messages': number_message},
		context_instance=RequestContext(request))

@login_required
def edita_ganado_celo(request, ganado_id):
	id_user = request.user
	number_message = number_messages(request, id_user.username)
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
						return redirect(reverse('list_cattle'))
					else:
						c = Celo.objects.get(id=id)
						c.observaciones=form.observaciones
						c.save()

						return redirect(reverse('list_cattle'))

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
				return redirect(reverse('list_cattle'))

	if ganado.celos.all():
		return render_to_response('edita_ganado_celo.html',
			{'form': form,
			 'ganado_id': ganado_id,
			 'number_messages': number_message},
			context_instance=RequestContext(request))
	else:
		return render_to_response('edita_ganado_celo.html',
			{'form': form,
			 'ganado_id': ganado_id,
			 'number_messages': number_message},
			context_instance=RequestContext(request))


@login_required
def add_service(request, id_cattle):
	user = request.user
	number_message = number_messages(request, user.username)
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

			# restar pajuela
			if formAttempt.type_conception == 0:
				insemina = Insemination.objects.get(rp=formAttempt.rp_father)
				insemina.amount_pajuelas = insemina.amount_pajuelas - 1
				insemina.save()


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

			return redirect(reverse('list_cattle'))

	elif request.method == 'GET':
		v = Verification.objects.filter(is_active=True, cattle=id_cattle).count()
		if v > 0:
			return redirect(reverse('add_attempt_service', kwargs={'id_cattle': id_cattle}))
		else:
			formAttempt = attemptForm()

	return render_to_response('add_service.html',
		{'id_cattle': id_cattle,
		 'formAttempt': formAttempt,
		 'number_messages': number_message},
		context_instance=RequestContext(request))

@login_required
def add_attempt_service(request, id_cattle):
	user = request.user
	number_message = number_messages(request, user.username)
	cattle = Ganado.objects.get(id=id_cattle)
	attempts = Attempt.objects.filter(verification__cattle=cattle, verification__is_active=True).order_by('id')

	return render_to_response('add_attempt_service.html',
		{'attempts': attempts,
		 'number_messages': number_message},
		context_instance=RequestContext(request))

@login_required
def verify_attempt(request, id_attempt):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	configuration = Configuracion.objects.get(id=farm.configuracion_id)
	attempt = Attempt.objects.get(id=id_attempt)

	if request.method == 'POST':
		formAttempt = verifyAttemptForm(request.POST, instance=attempt)
		if formAttempt.is_valid():

			formAttempt = formAttempt.save(commit=False)
			formAttempt.save()

			ganado = Ganado.objects.get(id=attempt.verification.cattle.id)
			# si fue correcto
			if formAttempt.state == 0:
				attempt.verification.is_active=False
				attempt.verification.save()


				# agrego el nuevo ciclo
				ciclo = Ciclo.objects.get(ganado_id=ganado.id, is_active=True, nombre=0)
				ciclo.is_active = False
				ciclo.save()
				ciclo = Ciclo()
				ciclo.nombre = 3
				ciclo.fecha_inicio = date.today()
				ciclo.fecha_fin = date.today()+timedelta(days=configuration.periodo_gestacion)
				ciclo.ganado = ganado
				ciclo.is_active = True
				ciclo.save()

				# restar pajuela
				if formAttempt.type_conception == 0:
					insemina = Insemination.objects.get(rp=formAttempt.rp_father)
					insemina.amount_pajuelas = insemina.amount_pajuelas - 1
					insemina.save()

				# agrego la gestacion
				gestacion = Gestacion()
				gestacion.fecha_servicio = date.today()
				gestacion.fecha_parto = date.today() + timedelta(days=configuration.periodo_gestacion)
				gestacion.is_active = True
				gestacion.ganado = ganado
				gestacion.save()

				return redirect(reverse('list_cattle'))

			# compruebo si es el ultimo intento
			if (configuration.intentos_verificacion_celo==formAttempt.attempt):
				# desactiva la verificacion
				v = Verification.objects.get(cattle=ganado, is_active=True)
				v.is_active=False
				v.save()

				# crea el celo
				celo = Celo()
				celo.fecha_inicio = datetime.datetime.now(pytz.timezone('America/Guayaquil'))
				celo.fecha_fin = celo.fecha_inicio + relativedelta(days=configuration.celo_frecuencia_error)
				celo.estado = 0
				celo.observaciones = 'Celo creado por HatosGanaderos'
				celo.ganado = ganado
				celo.is_active = True
				celo.save()


			id_cattle = attempt.verification.cattle_id
			return redirect(reverse('add_attempt_service', kwargs={'id_cattle': id_cattle}))
	else:
		formVerifyAttempt = verifyAttemptForm(instance=attempt)

	return render_to_response('verify_attempt.html',
		{'formVerifyAttempt': formVerifyAttempt,
		 'number_messages': number_message},
		context_instance=RequestContext(request))

@login_required
def gestacion(request, id_cattle):
	user = request.user
	number_message = number_messages(request, user.username)
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
			# desactivar los anteriores ciclos
			for c in ganado.ciclos.all():
				if c.is_active:
					c.is_active = False
					c.save()
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
			return redirect(reverse('list_cattle'))
	else:
		formGestacion = gestacionForm(instance=gestacion)
		if configuration.tipo_identificacion == 'simple':
			rp_cattle = ganado.identificacion_simple.rp
		else:
			rp_cattle = ganado.identificacion_ecuador.rp
	return render_to_response('gestacion.html',
		{'formGestacion': formGestacion,
		 'id_cattle': id_cattle,
		 'rp_cattle': rp_cattle,
		 'number_messages': number_message},
		context_instance=RequestContext(request))


@login_required
def problem_gestacion(request, id_cattle):
	user = request.user
	number_message = number_messages(request, user.username)
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
				# desactivar el anterior o anteriores ciclos
				if ganado.ciclos.all():
					for cicl in ganado.ciclos.all():
						if cicl.nombre != 2:
							cicl.is_active = False
							cicl.save()

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
				if ganado.ciclos.all():
					for cicl in ganado.ciclos.all():
						if cicl.nombre != 2:
							cicl.is_active = False
							cicl.save()

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
				if ganado.ciclos.all():
					for cicl in ganado.ciclos.all():
						ciclo.is_active = False
						ciclo.save()
				# se llena el DownCattle
				down_cattle = DownCattle()
				down_cattle.date = date.today()
				down_cattle.cause_down = 0
				down_cattle.observations = 'Desceso del animal, HatosGanaderos.'
				down_cattle.save()
				# se asigna el down_cattle al ganado
				ganado.down_cattle = down_cattle
				ganado.save()
				# gestacion en false
				gestacion.is_active = False
				gestacion.save()
				# se cancela la etapa
				if ganado.etapas.all():
					for et in ganado.etapas.all():
						et.is_active = False
						et.save()
				# se registra la cria
				'''attempt = Attempt.objects.get(verification_id=ganado.id, state=0)
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
					cria.save()'''
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
				# se cancela la etapa
				if ganado.etapas.all():
					for et in ganado.etapas.all():
						et.is_active = False
						et.save()

			formProblemGestacion.save()
			gestacion.problema = formProblemGestacion
			gestacion.save()

			return redirect(reverse('list_cattle'))
	elif request.method == 'GET':
		formProblemGestacion = problemGestacionForm()

	return render_to_response('problem_gestacion.html',
			{'formProblemGestacion': formProblemGestacion,
			 'id_cattle': id_cattle,
			 'number_messages': number_message},
			context_instance=RequestContext(request))

# aplazar notificaciones
@login_required
def deferEtapa(request, notification_id):
	if request.method == 'POST':
		formDeferEtapa = deferEtapaForm(request.POST)
		if formDeferEtapa.is_valid():
			notification = Notification.objects.get(id=notification_id)
			formDeferEtapa = formDeferEtapa.save(commit=False)
			# cambia la notificacion de registro de servicio
			if (notification.name==0):
				try:
					Notification.objects.get(ident_cattle=notification.ident_cattle, name=1, state=2)
					n = Notification.objects.get(ident_cattle=notification.ident_cattle, name=1, state=2)
					n.end_date = notification.end_date + relativedelta(days=formDeferEtapa.number_days)
					n.save()
				except ObjectDoesNotExist:
					pass
			# cambia la notificacion de celo
			elif (notification.name==1):
				try:
					Notification.objects.get(ident_cattle=notification.ident_cattle, name=0, state=2)
					n = Notification.objects.get(ident_cattle=notification.ident_cattle, name=0, state=2)
					n.end_date = notification.end_date + relativedelta(days=formDeferEtapa.number_days)
					n.save()
				except ObjectDoesNotExist:
					pass
			# modifico el fin del celo
			try:
				c = Celo.objects.get(ganado=notification.ident_cattle, is_active=True)
				c.fecha_fin = c.fecha_fin + relativedelta(days=formDeferEtapa.number_days)
				c.save()
			except ObjectDoesNotExist:
				pass
			# actualizo la deferetapa en caso de existir
			try:
				d = DeferEtapa.objects.get(cattle_id=notification.ident_cattle, is_active=True)
				d.number_days = d.number_days + formDeferEtapa.number_days
				d.observations = d.observations + '. ' + formDeferEtapa.observations
				d.save()
			except ObjectDoesNotExist:
				formDeferEtapa.is_active = True
				formDeferEtapa.cattle_id = notification.ident_cattle
				formDeferEtapa.save()


			notification.end_date = notification.end_date + relativedelta(days=formDeferEtapa.number_days)
			notification.save()

			return redirect(reverse('list_notifications'))

	else:
		notification = Notification.objects.get(id=notification_id)
		formDeferEtapa = deferEtapaForm()
	return render_to_response('deferEtapa.html',
				{'formDeferEtapa': formDeferEtapa,
				 'notification': notification},
				context_instance=RequestContext(request))
