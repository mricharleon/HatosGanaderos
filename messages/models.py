# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from profiles.models import Profile

class Message(models.Model):
	sender = models.ForeignKey(Profile, related_name='sender_')
	receiver = models.ForeignKey(Profile, related_name='receiver_', verbose_name=u'Receptor')
	content = models.TextField('Tu mensaje', max_length=280)
	sent_at = models.DateTimeField('Enviado a')
	read_at = models.BooleanField('Leído')
	front = models.BooleanField('Frontal')

	def __str__(self):
		return 'De: %s, Para: %s, Msj: %s - Estado: %s' % (self.sender.user.username, 
													self.receiver.user.username, 
													self.content,
													self.read_at)
