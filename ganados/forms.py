from django import forms
from django.utils.translation import ugettext_lazy as _
from ganados.models import Identificacion_Simple, Identificacion_Ecuador, Ganado, Etapa, Celo, Ordenio

from userena.forms import SignupForm

class tipoSimpleForm(forms.ModelForm):
    class Meta:
        model = Identificacion_Simple
        '''widgets = {
                  'rp':forms.TextInput(attrs={'disabled': ''})
        }'''

class tipoNormaEcuadorForm(forms.ModelForm):
    class Meta:
        model = Identificacion_Ecuador
        '''widgets = {
                   'rp':forms.TextInput(attrs={'placeholder': 'Name'}),
        }'''

class ordenioForm(forms.ModelForm):
  class Meta:
    model = Ordenio
    exclude = ['total',
               'numero_ordenio',
               'ganado',
               'fecha']
    '''widgets = {
                'fecha':forms.DateInput(attrs={'class': 'datetimepicker2'})
    }'''

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
                   'edad_dias'
                   ]
        widgets ={
                    'nacimiento': forms.DateInput(attrs={
                                                          'class': 'datetimepicker2'
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
                                                        'class': 'datetimepicker'
                  }),
    }
    