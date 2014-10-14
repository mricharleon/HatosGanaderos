from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.db.models import Q

from profiles.models import Profile
from messages.models import Message

from messages.forms import MessageForm, MessageResponseForm
from django.core.exceptions import ObjectDoesNotExist

import datetime

from drealtime import iShoutClient
ishout_client = iShoutClient()
from django.core import serializers
from django.db.models import Q

from profiles.views import number_messages, Ganaderia

def alert_messages(request):
	pass


def messages_list(request):
	user_receiver = request.user
	try:
		ganaderia = Ganaderia.objects.get(perfil=user_receiver)
	except ObjectDoesNotExist:
		return redirect(reverse('agrega_ganaderia_config'))
	
	number_message = number_messages(request, user_receiver.username)

	messages = []
	mc = Message.objects.all().order_by('-sent_at')
	for i in mc:
		if (i.sender_id == user_receiver.id) | (i.receiver_id == user_receiver.id) and (i.front == True):
			messages.append(i)
	
	return render_to_response('messages_list.html',
								{'messages': messages,
								 'user_receiver': user_receiver,
								 'number_messages': number_message,
								},
								context_instance=RequestContext(request))

def messages_list_read(request):
	user_receiver = request.user
	number_message = number_messages(request, user_receiver.username)
	messages = []
	mc = Message.objects.all().order_by('-sent_at')
	for i in mc:
		if (i.sender_id == user_receiver.id) | (i.receiver_id == user_receiver.id) and (i.front == True) and (i.read_at == True):
			messages.append(i)
	
	return render_to_response('messages_list_read.html',
								{'messages': messages,
								 'user_receiver': user_receiver,
								 'number_messages': number_message,
								},
								context_instance=RequestContext(request))

def messages_list_no_read(request):
	user_receiver = request.user
	number_message = number_messages(request, user_receiver.username)
	messages = []
	mc = Message.objects.all().order_by('-sent_at')
	for i in mc:
		if (i.sender_id == user_receiver.id) | (i.receiver_id == user_receiver.id) and (i.front == True) and (i.read_at == False):
			messages.append(i)
	
	return render_to_response('messages_list_no_read.html',
								{'messages': messages,
								 'user_receiver': user_receiver,
								 'number_messages': number_message,
								},
								context_instance=RequestContext(request))

def messages_details(request, user_id, user_send_id, user_receiver_id):
	user = User.objects.get(id=user_id)
	user_send = User.objects.get(id=user_send_id)
	user_receiver = User.objects.get(id=user_receiver_id)

	profile = Profile.objects.get(user=user)
	profile_sender = Profile.objects.get(user=user_send)
	profile_receiver = Profile.objects.get(user=user_receiver)


	messages = []
	msgs = Message.objects.all().order_by('-sent_at')
	if request.method == 'POST':
		form_message = MessageResponseForm(request.POST)
		date_now = datetime.datetime.today()
		if form_message.is_valid():
			form_message = form_message.save(commit=False)
			form_message.sender = profile
			if user_id == user_send_id:
				form_message.receiver = profile_receiver
				form_message.read_at = False
			elif user_id == user_receiver_id:
				form_message.receiver = profile_sender
				form_message.read_at = False
			form_message.sent_at = date_now
			for i in msgs:
				if ((i.receiver_id == user_receiver.id) & (i.sender_id == user_send.id)) | ((i.sender_id == user_receiver.id) & (i.receiver_id == user_send.id)):
					i.front=False
					i.save()
			form_message.front = True
			form_message.save()

			number_message = number_messages(request, str(form_message.receiver_id))
			data = serializers.serialize("json", User.objects.all())
			
			ishout_client.emit(
					form_message.receiver_id,
					'alertchannel',
					data = {'msg': data,
							'number_messages': number_message,}
				)
			
			return HttpResponseRedirect(reverse('messages_list'))
			#return redirect(reverse('messages_list', kwargs={'username': user.username}))
	elif request.method == 'GET':
		for i in msgs:
			if ((i.receiver_id == user_receiver.id) & (i.sender_id == user_send.id)) | ((i.sender_id == user_receiver.id) & (i.receiver_id == user_send.id)):
				if user_id != user_send_id:
					i.read_at=True
					i.save()
				messages.append(i)
		form_message = MessageResponseForm()

		number_message = number_messages(request, str(user.id))
		data = serializers.serialize("json", User.objects.all())
		
		ishout_client.emit(
				user_send.id,
				'alertchannel',
				data = {'msg': data,
						'number_messages': number_message}
			)

	return render_to_response('messages_details.html',
								{'messages': messages,
								 'user_receiver': user_receiver,
								 'user_sender': user_send,
								 'form':form_message,
								},
								context_instance=RequestContext(request))

from userena.utils import *

def new_message(request):
	user = request.user
	profile = Profile.objects.get(user=user)
	try:
		ganaderia = Ganaderia.objects.get(perfil=user)
	except ObjectDoesNotExist:
		return redirect(reverse('agrega_ganaderia_config'))
	
	number_message = Message.objects.filter(Q(receiver_id=user.id), Q(front=True), Q(read_at=False)).count()
	msg_complete = Message.objects.all().order_by('sent_at')

	date_now = datetime.datetime.today()
	if request.method == 'POST':
		form_message = MessageForm(request.POST)
		if form_message.is_valid():
			form_message = form_message.save(commit=False)
			form_message.sender = profile
			form_message.sent_at = date_now
			form_message.read_at = False
			for i in msg_complete:
				if ((i.receiver_id == form_message.receiver_id) & (i.sender_id == form_message.sender_id)) | ((i.sender_id == form_message.receiver_id) & (i.receiver_id == form_message.sender_id)):
					i.front=False
					i.save()
			form_message.front = True
			form_message.save()

			number_message = number_messages(request, str(form_message.receiver_id))
			data = serializers.serialize("json", User.objects.all())
			
			ishout_client.emit(
					form_message.receiver_id,
					'alertchannel',
					data = {'msg': data,
							'number_messages': number_message,}
				)
			
			return HttpResponseRedirect(reverse('messages_list'))
			#return redirect(reverse('messages_list'))

	else:
		form_message = MessageForm()
		profile_model = get_profile_model()
		ganaderia = Ganaderia.objects.get(perfil=user)
		receivers = profile_model.objects.get_visible_profiles(user).select_related().exclude(id=user.id).filter(ganaderia_perfil=ganaderia)
	return render_to_response('new_message.html',
								{'form': form_message,
								'number_messages': number_message,
								'receivers': receivers,
								},
								context_instance=RequestContext(request))