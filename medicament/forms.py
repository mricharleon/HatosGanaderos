# -*- encoding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from medicament.models import Medicament


class wormerForm(forms.ModelForm):
    class Meta:
        model = Medicament
        exclude = ['farm', 'is_vaccine', 'status', 'is_wormer', 'cattle']
        widgets = {
                'name': forms.TextInput(attrs={
                    'placeholder': 'Nombre de la medicina',
                    }),
                'expiration_date': forms.DateInput(attrs={
                    'class': 'datetimepicker2',
                    'placeholder': 'Fecha de expiración',
                    }),
                'cattle': forms.TextInput(attrs={}),
                'amount': forms.TextInput(attrs={
                    'placeholder': 'Cantidad de medicina'
                    }),
                'application_age': forms.TextInput(attrs={
                    'placeholder': 'Edad de aplicación'
                    }),
                'amount_application': forms.TextInput(attrs={
                    'placeholder': 'Cantidad de aplicación'
                    }),
                'number_application': forms.TextInput(attrs={
                    'placeholder': 'Número de aplicaciones'
                    }),
                'interval': forms.TextInput(attrs={
                    'placeholder': 'Intervalo de tiempo'
                    }),
                'live_weight': forms.TextInput(attrs={
                    'placeholder': '¿Cuál es el peso vivo?'
                    }),
                'observations': forms.Textarea(attrs={
                    'placeholder': 'Observaciones'
                    })
                }


class vaccineForm(forms.ModelForm):
    class Meta:
        model = Medicament
        exclude = ['farm', 'is_vaccine', 'status', 'is_wormer', 'cattle']
        widgets = {
                'name': forms.TextInput(attrs={
                    'placeholder': 'Nombre de la medicina',
                    }),
                'expiration_date': forms.DateInput(attrs={
                    'class': 'datetimepicker2',
                    'placeholder': 'Fecha de expiración',
                    }),
                'cattle': forms.TextInput(attrs={}),
                'amount': forms.TextInput(attrs={
                    'placeholder': 'Cantidad de medicina'
                    }),
                'application_age': forms.TextInput(attrs={
                    'placeholder': 'Edad de aplicación'
                    }),
                'amount_application': forms.TextInput(attrs={
                    'placeholder': 'Cantidad de aplicación'
                    }),
                'number_application': forms.TextInput(attrs={
                    'placeholder': 'Número de aplicaciones'
                    }),
                'interval': forms.TextInput(attrs={
                    'placeholder': 'Intervalo de tiempo'
                    }),
                'live_weight': forms.TextInput(attrs={
                    'placeholder': '¿Cuál es el peso vivo?'
                    }),
                'observations': forms.Textarea(attrs={
                    'placeholder': 'Observaciones'
                    })
                }
