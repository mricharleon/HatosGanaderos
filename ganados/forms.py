# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from ganados.models import Identificacion_Simple, Identificacion_Ecuador, Ganado, Etapa, Celo, Ordenio, Verification, Attempt, Gestacion, ProblemaGestacion, Insemination, DownCattle, DownInsemination, DeferEtapa

from userena.forms import SignupForm

class inseminationForm(forms.ModelForm):
    class Meta:
        model = Insemination
        exclude = ['down_insemination', 'farm', 'rp']
        widgets = {
                  'name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
                  'registration_date': forms.DateInput(attrs={'class': 'datetimepicker2', 'placeholder': 'Fecha de registro'}),
                  'amount_pajuelas': forms.TextInput(attrs={'placeholder': 'Número de pajuelas'}),
                  'observations': forms.Textarea(attrs={'placeholder': 'Observaciones'})
        }

class tipoSimpleForm(forms.ModelForm):
    class Meta:
        model = Identificacion_Simple
        exclude = ['rp',]
        widgets = {
                  'nombre':forms.TextInput(attrs={'placeholder': 'Nombre'}),
                  'rp_madre':forms.TextInput(attrs={
                                  'placeholder': 'RP de la madre',
                                  'data-reveal-id': 'myModal'}),
                  'rp_padre':forms.TextInput(attrs={
                                  'placeholder': 'RP del padre',
                                  'data-reveal-id': 'myModal2'}),
        }

class tipoNormaEcuadorForm(forms.ModelForm):
    class Meta:
        model = Identificacion_Ecuador
        exclude = ['rp',]
        widgets = {
                   'siglas_pais': forms.TextInput(attrs={'placeholder': 'Siglas del País'}),
                   'codigo_pais': forms.TextInput(attrs={'placeholder': 'Código del País'}),
                   'codigo_provincia': forms.TextInput(attrs={'placeholder': 'Código de Provincia'}),
                   'numero_serie': forms.TextInput(attrs={'placeholder': 'Número de Serie'}),
                   'codigo_barras': forms.TextInput(attrs={'placeholder': 'Código de Barras'}),
                   'nombre':forms.TextInput(attrs={'placeholder': 'Nombre'}),
                   'rp_madre':forms.TextInput(attrs={
                                  'placeholder': 'RP de la madre',
                                  'data-reveal-id': 'myModal'}),
                   'rp_padre':forms.TextInput(attrs={
                                  'placeholder': 'RP del padre',
                                  'data-reveal-id': 'myModal2'}),
        }

class ordenioForm(forms.ModelForm):
  class Meta:
    model = Ordenio
    exclude = ['total',
               'numero_ordenio',
               'ganado',
               'fecha']
    widgets = {
                'cantidad': forms.TextInput(attrs={
                            'placeholder': 'Número de litros de leche'
                  }),
                'observaciones': forms.Textarea(attrs={
                            'placeholder': 'Observaciones'
                  })
    }

class etapaForm(forms.ModelForm):
  class Meta:
    model = Etapa
    exclude =['is_active']

class ganadoForm(forms.ModelForm):
    class Meta:
        model = Ganado
        exclude = ['ganaderia', 
                   'identificacion_simple', 
                   'identificacion_ecuador',
                   'edad',
                   'etapa',
                   'verificacion',
                   'celo',
                   'ciclo',
                   'gestacion',
                   'ordenio',
                   'edad_anios',
                   'edad_meses',
                   'edad_dias',
                   ]
        widgets ={
                    'nacimiento': forms.DateInput(attrs={
                                    'class': 'datetimepicker2',
                                    'placeholder': 'Fecha de nacimiento'
                      }),
                    'observaciones': forms.Textarea(attrs={
                                    'placeholder': 'Observaciones'
                      }),
                    'imagen': forms.FileInput(attrs={}),
                    'live_weight': forms.TextInput(attrs={
                                    'placeholder': '¿Cuál es el peso vivo?'
                    }),
        }      

class editaGanadoCeloForm(forms.ModelForm):
  class Meta:
    model = Celo
    exclude = ['ganado',
               'is_active',
               'fecha_fin',
               'estado']
    widgets = {
                'fecha_inicio': forms.DateInput(attrs={
                                  'class': 'datetimepicker',
                                  'placeholder': u'¿Cuándo inicio el celo?'
                  }),
                'observaciones': forms.Textarea(attrs={
                                  'placeholder': 'Observaciones'
                  })
    }

class attemptForm(forms.ModelForm):
  class Meta:
    model = Attempt
    exclude = ['attempt', 'attempt_date', 'state', 'verification']
    widgets = {
                'rp_father': forms.TextInput(attrs={
                                  'placeholder': 'RP del padre',
                                  'data-reveal-id': 'myModal2'
                  }),
                'observations': forms.Textarea(attrs={
                                  'placeholder': 'Observaciones'
                  })
    }

class verificationForm(forms.ModelForm):
  class Meta:
    model = Verification


class attemptServiceForm(forms.ModelForm):
  class Meta:
    model = Attempt
    exclude = ['verification']

class verifyAttemptForm(forms.ModelForm):
  class Meta:
    model = Attempt
    exclude = ['attempt', 'attempt_date', 'verification']
    widgets = {
                'rp_father': forms.TextInput(attrs={
                                  'placeholder': 'RP del padre',
                                  'data-reveal-id': 'myModal2'
                  }),
                'observations': forms.Textarea(attrs={
                                  'placeholder': 'Observaciones'
                  })
    }

class gestacionForm(forms.ModelForm):
  class Meta:
    model = Gestacion
    exclude = ['problema', 'is_active', 'ganado']
    widgets = {
                'fecha_servicio': forms.TextInput(attrs={
                                  'placeholder': 'Fecha del Servicio',
                                  'class': 'datetimepicker2'
                  }),
                'fecha_parto': forms.TextInput(attrs={
                                  'placeholder': 'Fecha Posible del Parto',
                                  'class': 'datetimepicker2'
                  }),
                'observaciones': forms.Textarea(attrs={
                                  'placeholder': 'Observaciones'
                  })
    }

class problemGestacionForm(forms.ModelForm):
  class Meta: 
    model = ProblemaGestacion
    widgets = {
                'fecha_problema': forms.TextInput(attrs={
                                  'placeholder': 'Fecha del Problema',
                                  'class': 'datetimepicker2'
                  }),
                'observaciones': forms.Textarea(attrs={
                                  'placeholder': 'Observaciones'
                  })
    }

class downCattleForm(forms.ModelForm):
  class Meta:
    model = DownCattle
    widgets = {
                'date': forms.TextInput(attrs={
                    'placeholder': 'Fecha de la baja',
                    'class': 'datetimepicker2'
                  }),
                'observations': forms.Textarea(attrs={
                    'placeholder': 'Observaciones'
                  })
    }

class downInseminationForm(forms.ModelForm):
  class Meta:
    model = DownInsemination
    widgets = {
                'date': forms.TextInput(attrs={
                    'placeholder': 'Fecha de la baja',
                    'class': 'datetimepicker2'
                  }),
                'observations': forms.Textarea(attrs={
                    'placeholder': 'Observaciones'
                  })
    }

class deferEtapaForm(forms.ModelForm):
  class Meta:
    model = DeferEtapa
    exclude = ['is_active', 'cattle_id']
    widgets = {
                'observations': forms.Textarea(attrs={
                    'placeholder': 'Observaciones'
                  })
    }