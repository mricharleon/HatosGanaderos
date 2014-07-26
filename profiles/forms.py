# -*- encoding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from profiles.models import Configuracion, Ganaderia

from userena.forms import SignupForm

class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = Configuracion
        exclude = ['etapa_vientre']
        '''widgets = {
                  'celo_frecuencia':forms.NumberInput(attrs={'placeholder': 'Frecuencia de celo'}),
                  'celo_frecuencia_error':forms.NumberInput(attrs={'placeholder': 'Error de frecuencia'}),
                  'celo_duracion':forms.NumberInput(attrs={'placeholder': 'Duracion del celo'}),
                  'celo_duracion_error':forms.NumberInput(attrs={'placeholder': 'Error de duracion'}),
                  'celo_despues_parto':forms.NumberInput(attrs={'placeholder': 'Celo despues del parto'}),
                  'celo_despues_parto_error':forms.NumberInput(attrs={'placeholder': 'Error despues del parto'}),
                  'intentos_verificacion_celo':forms.NumberInput(attrs={'placeholder': 'Intentos verifica celo'}),
                  'etapa_ternera':forms.NumberInput(attrs={'placeholder': 'Edad max. de ternera'}),
                  'etapa_vacona':forms.NumberInput(attrs={'placeholder': 'Edad max. de vacona'}),
                  'etapa_vientre':forms.NumberInput(attrs={'placeholder': 'Edad max. de vientre'}),
                  'periodo_gestacion':forms.NumberInput(attrs={'placeholder': 'Periodo de gestacion'}),
                  'periodo_seco':forms.NumberInput(attrs={'placeholder': 'Periodo dseco'}),
                  'periodo_lactancia':forms.NumberInput(attrs={'placeholder': 'Periodo de lactancia'}),
                  'periodo_vacio':forms.NumberInput(attrs={'placeholder': 'Periodo vacio'}),
                  'numero_ordenios':forms.NumberInput(attrs={'placeholder': 'Numero de ordenios diarios'}),
                  
        }'''

class GanaderiaForm(forms.ModelForm):
    class Meta:
        model = Ganaderia
        fields = ('nombreEntidad', 'direccion')
        '''widgets = {
                  'nombreEntidad':forms.TextInput(attrs={'placeholder': 'Nombre de la Entidad'}),
                  'direccion':forms.TextInput(attrs={'placeholder': 'Direccion'}),
        }'''

class SignupFormExtra(SignupForm):
    """ 
    A form to SIDGVnstrate how to add extra fields to the signup form, in this
    case adding the first and last name.
    

    """
    first_name = forms.CharField(label=_(u'First name'),
                                 max_length=30,
                                 required=False)

    last_name = forms.CharField(label=_(u'Last name'),
                                max_length=30,
                                required=False)

    def __init__(self, *args, **kw):
        """
        
        A bit of hackery to get the first name and last name at the top of the
        form instead at the end.
        
        """
        super(SignupFormExtra, self).__init__(*args, **kw)
        # Put the first and last name at the top
        new_order = self.fields.keyOrder[:-2]
        new_order.insert(0, 'first_name')
        new_order.insert(1, 'last_name')
        self.fields.keyOrder = new_order

    def save(self):
        """ 
        Override the save method to save the first and last name to the user
        field.

        """
        # First save the parent form and get the user.
        new_user = super(SignupFormExtra, self).save()

        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user
