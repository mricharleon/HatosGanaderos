# -*- encoding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from alimentos.models import Food

class alimentoForm(forms.ModelForm):
    class Meta:
        model = Food
        exclude = ['farm', 'cattle', 'status', 'is_active']
        widgets = {
              			'name': forms.TextInput(attrs={
              							'placeholder': 'Nombre del alimento'
              			}),
                  	'expiration_date':forms.DateInput(attrs={
                  					'class': 'datetimepicker2',
                  					'placeholder': 'Fecha de expiración'}),
                  	'amount': forms.TextInput(attrs={
                  					'placeholder': 'Cantidad de alimento'
                  	}),
                  	'consumer_amount': forms.TextInput(attrs={
                  					'placeholder': 'Cantidad de consumo'
                  	}),
                  	'interval': forms.TextInput(attrs={
                  					'placeholder': 'Intervalo '
                  	}),
                  	'observations': forms.Textarea(attrs={
                  					'placeholder': 'Observaciones'
                  	}),
        }