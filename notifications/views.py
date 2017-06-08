# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User

from ganados.models import Ganaderia
from profiles.views import number_messages
from notifications.models import Notification
from django.db.models import Q


@login_required
def list_notifications(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	notifications = Notification.objects.filter( Q(state=2) & (Q(ident_cattle__ganaderia=farm) | Q(ident_medicament__farm=farm) | Q(ident_food__farm=farm) | Q(ident_sperm__farm=farm)) ).order_by('-end_date')
	number_todas = Notification.objects.filter( Q(state=2) & (Q(ident_cattle__ganaderia=farm) | Q(ident_medicament__farm=farm) | Q(ident_food__farm=farm) | Q(ident_sperm__farm=farm)) ).count()
	number_reproduccion = Notification.objects.filter( state=2, module=0, farm=farm ).count()
	number_produccion = Notification.objects.filter( state=2, module=3, farm=farm ).count()
	number_sanidad = Notification.objects.filter( state=2, module=2, farm=farm ).count()
	number_alimentacion = Notification.objects.filter( state=2, module=1, farm=farm ).count()

	return render_to_response('list_notifications.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_todas': number_todas,
				 'number_reproduccion': number_reproduccion,
				 'number_produccion': number_produccion,
				 'number_sanidad': number_sanidad,
				 'number_alimentacion': number_alimentacion},
				context_instance=RequestContext(request))

@login_required
def list_notifications_reproduccion(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	notifications = Notification.objects.filter( state=2, module=0, farm=farm ).order_by('-end_date')
	number_reproduccion = Notification.objects.filter( state=2, module=0, farm=farm ).count()

	number_reproduccion_realizadas = Notification.objects.filter( state=1, module=0, farm=farm ).count()
	number_reproduccion_norealizadas = Notification.objects.filter( state=0, module=0, farm=farm ).count()

	return render_to_response('list_notifications_reproduccion.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_reproduccion': number_reproduccion,
				 'number_reproduccion_realizadas': number_reproduccion_realizadas,
				 'number_reproduccion_norealizadas': number_reproduccion_norealizadas},
				context_instance=RequestContext(request))

@login_required
def list_notifications_reproduccion_realizadas(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	notifications = Notification.objects.filter( state=1, module=0, farm=farm ).order_by('-end_date')[:5]
	number_reproduccion = Notification.objects.filter( state=2, module=0, farm=farm ).count()

	number_reproduccion_realizadas = Notification.objects.filter( state=1, module=0, farm=farm ).count()
	number_reproduccion_norealizadas = Notification.objects.filter( state=0, module=0, farm=farm ).count()

	return render_to_response('list_notifications_reproduccion_realizadas.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_reproduccion': number_reproduccion,
				 'number_reproduccion_realizadas': number_reproduccion_realizadas,
				 'number_reproduccion_norealizadas': number_reproduccion_norealizadas},
				context_instance=RequestContext(request))

@login_required
def list_notifications_reproduccion_norealizadas(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	notifications = Notification.objects.filter( state=0, module=0, farm=farm ).order_by('-end_date')
	number_reproduccion = Notification.objects.filter( state=2, module=0, farm=farm ).count()

	number_reproduccion_realizadas = Notification.objects.filter( state=1, module=0, farm=farm ).count()
	number_reproduccion_norealizadas = Notification.objects.filter( state=0, module=0, farm=farm ).count()

	return render_to_response('list_notifications_reproduccion_norealizadas.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_reproduccion': number_reproduccion,
				 'number_reproduccion_realizadas': number_reproduccion_realizadas,
				 'number_reproduccion_norealizadas': number_reproduccion_norealizadas},
				context_instance=RequestContext(request))


@login_required
def list_notifications_produccion(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	notifications = Notification.objects.filter( state=2, module=3, farm=farm ).order_by('-end_date')
	number_produccion = Notification.objects.filter( state=2, module=3, farm=farm ).count()

	number_produccion_realizadas = Notification.objects.filter( state=1, module=3, farm=farm ).count()
	number_produccion_norealizadas = Notification.objects.filter( state=0, module=3, farm=farm ).count()

	return render_to_response('list_notifications_produccion.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_produccion': number_produccion,
				 'number_produccion_realizadas': number_produccion_realizadas,
				 'number_produccion_norealizadas': number_produccion_norealizadas},
				context_instance=RequestContext(request))

@login_required
def list_notifications_produccion_realizadas(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	notifications = Notification.objects.filter( state=1, module=3, farm=farm ).order_by('-end_date')[:5]
	number_produccion = Notification.objects.filter( state=2, module=3, farm=farm ).count()

	number_produccion_realizadas = Notification.objects.filter( state=1, module=3, farm=farm ).count()
	number_produccion_norealizadas = Notification.objects.filter( state=0, module=3, farm=farm ).count()

	return render_to_response('list_notifications_produccion_realizadas.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_produccion': number_produccion,
				 'number_produccion_realizadas': number_produccion_realizadas,
				 'number_produccion_norealizadas': number_produccion_norealizadas},
				context_instance=RequestContext(request))

@login_required
def list_notifications_produccion_norealizadas(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	notifications = Notification.objects.filter( state=0, module=3, farm=farm ).order_by('-end_date')[:5]
	number_produccion = Notification.objects.filter( state=2, module=3, farm=farm ).count()

	number_produccion_realizadas = Notification.objects.filter( state=1, module=3, farm=farm ).count()
	number_produccion_norealizadas = Notification.objects.filter( state=0, module=3, farm=farm ).count()

	return render_to_response('list_notifications_produccion_norealizadas.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_produccion': number_produccion,
				 'number_produccion_realizadas': number_produccion_realizadas,
				 'number_produccion_norealizadas': number_produccion_norealizadas},
				context_instance=RequestContext(request))


@login_required
def list_notifications_sanidad(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	notifications = Notification.objects.filter( state=2, module=2, farm=farm ).order_by('-end_date')
	number_sanidad = Notification.objects.filter( state=2, module=2, farm=farm ).count()

	number_sanidad_realizadas = Notification.objects.filter( state=1, module=2, farm=farm ).count()
	number_sanidad_norealizadas = Notification.objects.filter( state=0, module=2, farm=farm ).count()

	return render_to_response('list_notifications_sanidad.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_sanidad': number_sanidad,
				 'number_sanidad_realizadas': number_sanidad_realizadas,
				 'number_sanidad_norealizadas': number_sanidad_norealizadas},
				context_instance=RequestContext(request))

@login_required
def list_notifications_sanidad_realizadas(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	notifications = Notification.objects.filter( state=1, module=2, farm=farm ).order_by('-end_date')[:5]
	number_sanidad = Notification.objects.filter( state=2, module=2, farm=farm ).count()

	number_sanidad_realizadas = Notification.objects.filter( state=1, module=2, farm=farm ).count()
	number_sanidad_norealizadas = Notification.objects.filter( state=0, module=2, farm=farm ).count()

	return render_to_response('list_notifications_sanidad_realizadas.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_sanidad': number_sanidad,
				 'number_sanidad_realizadas': number_sanidad_realizadas,
				 'number_sanidad_norealizadas': number_sanidad_norealizadas},
				context_instance=RequestContext(request))

@login_required
def list_notifications_sanidad_norealizadas(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	notifications = Notification.objects.filter( state=0, module=2, farm=farm ).order_by('-end_date')[:5]
	number_sanidad = Notification.objects.filter( state=2, module=2, farm=farm ).count()

	number_sanidad_realizadas = Notification.objects.filter( state=1, module=2, farm=farm ).count()
	number_sanidad_norealizadas = Notification.objects.filter( state=0, module=2, farm=farm ).count()

	return render_to_response('list_notifications_sanidad_norealizadas.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_sanidad': number_sanidad,
				 'number_sanidad_realizadas': number_sanidad_realizadas,
				 'number_sanidad_norealizadas': number_sanidad_norealizadas},
				context_instance=RequestContext(request))

@login_required
def list_notifications_alimentacion(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	notifications = Notification.objects.filter( state=2, module=1, farm=farm ).order_by('-end_date')
	number_alimentacion = Notification.objects.filter( state=2, module=1, farm=farm ).count()

	number_alimentacion_realizadas = Notification.objects.filter( state=1, module=1, farm=farm ).count()
	number_alimentacion_norealizadas = Notification.objects.filter( state=0, module=1, farm=farm ).count()

	return render_to_response('list_notifications_alimentacion.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_alimentacion': number_alimentacion,
				 'number_alimentacion_realizadas':number_alimentacion_realizadas,
				 'number_alimentacion_norealizadas': number_alimentacion_norealizadas},
				context_instance=RequestContext(request))

@login_required
def list_notifications_alimentacion_realizadas(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	notifications = Notification.objects.filter( state=1, module=1, farm=farm ).order_by('-end_date')[:5]
	number_alimentacion = Notification.objects.filter( state=2, module=1, farm=farm ).count()

	number_alimentacion_realizadas = Notification.objects.filter( state=1, module=1, farm=farm ).count()
	number_alimentacion_norealizadas = Notification.objects.filter( state=0, module=1, farm=farm ).count()

	return render_to_response('list_notifications_alimentacion_realizadas.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_alimentacion': number_alimentacion,
				 'number_alimentacion_realizadas':number_alimentacion_realizadas,
				 'number_alimentacion_norealizadas': number_alimentacion_norealizadas},
				context_instance=RequestContext(request))

@login_required
def list_notifications_alimentacion_norealizadas(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	notifications = Notification.objects.filter( state=0, module=1, farm=farm ).order_by('-end_date')[:5]
	number_alimentacion = Notification.objects.filter( state=2, module=1, farm=farm ).count()

	number_alimentacion_realizadas = Notification.objects.filter( state=1, module=1, farm=farm ).count()
	number_alimentacion_norealizadas = Notification.objects.filter( state=0, module=1, farm=farm ).count()

	return render_to_response('list_notifications_alimentacion_norealizadas.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_alimentacion': number_alimentacion,
				 'number_alimentacion_realizadas':number_alimentacion_realizadas,
				 'number_alimentacion_norealizadas': number_alimentacion_norealizadas},
				context_instance=RequestContext(request))

@login_required
def realizedNotification(request, notification_id):
	notification = Notification.objects.get(id=notification_id)
	notification.state = 1
	notification.save()

	msg = 'Notificación REALIZADA con EXITO'
	return redirect(reverse('list_notifications'))


@login_required
def realizedNotificationBefore(request, notification_id, cattle_id):
	notification = Notification.objects.get(id=notification_id)
	notification.state = 1
	notification.save()

	return redirect(reverse('add_service', kwargs={'id_cattle': cattle_id}))

