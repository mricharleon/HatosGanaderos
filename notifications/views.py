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
	notifications = Notification.objects.filter( Q(state=2) & (Q(ident_cattle__ganaderia=farm) | Q(ident_medicament__farm=farm) | Q(ident_food__farm=farm)) ).order_by('end_date')
	number_todas = Notification.objects.filter( Q(state=2) & (Q(ident_cattle__ganaderia=farm) | Q(ident_medicament__farm=farm) | Q(ident_food__farm=farm)) ).count()
	number_reproduccion = Notification.objects.filter( state=2, module=0 ).count()
	number_produccion = Notification.objects.filter( state=2, module=3 ).count()
	number_sanidad = Notification.objects.filter( state=2, module=2 ).count()
	number_alimentacion = Notification.objects.filter( state=2, module=1 ).count()

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
	notifications = Notification.objects.filter( state=2, module=0 ).order_by('end_date')
	number_todas = Notification.objects.filter( Q(state=2) & (Q(ident_cattle__ganaderia=farm) | Q(ident_medicament__farm=farm) | Q(ident_food__farm=farm)) ).count()
	number_reproduccion = Notification.objects.filter( state=2, module=0 ).count()
	number_produccion = Notification.objects.filter( state=2, module=3 ).count()
	number_sanidad = Notification.objects.filter( state=2, module=2 ).count()
	number_alimentacion = Notification.objects.filter( state=2, module=1 ).count()
	
	return render_to_response('list_notifications_reproduccion.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_todas': number_todas,
				 'number_reproduccion': number_reproduccion,
				 'number_produccion': number_produccion,
				 'number_sanidad': number_sanidad,
				 'number_alimentacion': number_alimentacion},
				context_instance=RequestContext(request))

@login_required
def list_notifications_produccion(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	notifications = Notification.objects.filter( state=2, module=3 ).order_by('end_date')
	number_todas = Notification.objects.filter( Q(state=2) & (Q(ident_cattle__ganaderia=farm) | Q(ident_medicament__farm=farm) | Q(ident_food__farm=farm)) ).count()
	number_reproduccion = Notification.objects.filter( state=2, module=0 ).count()
	number_produccion = Notification.objects.filter( state=2, module=3 ).count()
	number_sanidad = Notification.objects.filter( state=2, module=2 ).count()
	number_alimentacion = Notification.objects.filter( state=2, module=1 ).count()
	
	return render_to_response('list_notifications_produccion.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_todas': number_todas,
				 'number_reproduccion': number_reproduccion,
				 'number_produccion': number_produccion,
				 'number_sanidad': number_sanidad,
				 'number_alimentacion': number_alimentacion},
				context_instance=RequestContext(request))

@login_required
def list_notifications_sanidad(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	notifications = Notification.objects.filter( state=2, module=2 ).order_by('end_date')
	number_todas = Notification.objects.filter( Q(state=2) & (Q(ident_cattle__ganaderia=farm) | Q(ident_medicament__farm=farm) | Q(ident_food__farm=farm)) ).count()
	number_reproduccion = Notification.objects.filter( state=2, module=0 ).count()
	number_produccion = Notification.objects.filter( state=2, module=3 ).count()
	number_sanidad = Notification.objects.filter( state=2, module=2 ).count()
	number_alimentacion = Notification.objects.filter( state=2, module=1 ).count()
	
	return render_to_response('list_notifications_sanidad.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_todas': number_todas,
				 'number_reproduccion': number_reproduccion,
				 'number_produccion': number_produccion,
				 'number_sanidad': number_sanidad,
				 'number_alimentacion': number_alimentacion},
				context_instance=RequestContext(request))

@login_required
def list_notifications_alimentacion(request):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	notifications = Notification.objects.filter( state=2, module=1 ).order_by('end_date')
	number_todas = Notification.objects.filter( Q(state=2) & (Q(ident_cattle__ganaderia=farm) | Q(ident_medicament__farm=farm) | Q(ident_food__farm=farm)) ).count()
	number_reproduccion = Notification.objects.filter( state=2, module=0 ).count()
	number_produccion = Notification.objects.filter( state=2, module=3 ).count()
	number_sanidad = Notification.objects.filter( state=2, module=2 ).count()
	number_alimentacion = Notification.objects.filter( state=2, module=1 ).count()
	
	return render_to_response('list_notifications_alimentacion.html',
				{'notifications': notifications,
				 'number_messages': number_message,
				 'number_todas': number_todas,
				 'number_reproduccion': number_reproduccion,
				 'number_produccion': number_produccion,
				 'number_sanidad': number_sanidad,
				 'number_alimentacion': number_alimentacion},
				context_instance=RequestContext(request))

@login_required
def realizedNotification(request, notification_id):
	notification = Notification.objects.get(id=notification_id)
	notification.state = 1
	notification.save()

	msg = 'Notificación REALIZADA con EXITO'
	return render_to_response('list_notifications.html',
				{'msg': msg,},
				context_instance=RequestContext(request))
