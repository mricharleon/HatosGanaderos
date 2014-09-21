# -*- encoding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from messages.models import Message

from userena.forms import SignupForm

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['sender',
        		   'sent_at',
        		   'read_at',
        		   'front']
        widgets ={
                    'content': forms.Textarea(attrs={
                                  'rows': '5',
                                  'placeholder': 'Tu mensaje aquí'
                      }),
        }

class MessageResponseForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['sender',
                   'sent_at',
                   'read_at',
                   'front',
                   'receiver']
        widgets ={
                    'content': forms.Textarea(attrs={
                                                          'rows': '3'
                      }),
        }
