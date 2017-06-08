# -*- encoding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from profiles.models import Configuracion, Ganaderia

from userena.forms import SignupForm

class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = Configuracion
        exclude = ['etapa_vaca']
        widgets = {
                  'celo_frecuencia':forms.TextInput(attrs={}),
                  'celo_frecuencia_error':forms.TextInput(attrs={}),
                  'celo_duracion':forms.TextInput(attrs={}),
                  'celo_duracion_error':forms.TextInput(attrs={}),
                  'celo_despues_parto':forms.TextInput(attrs={}),
                  'celo_despues_parto_error':forms.TextInput(attrs={}),
                  'intentos_verificacion_celo':forms.TextInput(attrs={}),
                  'etapa_ternera':forms.TextInput(attrs={}),
                  'etapa_vacona_media':forms.TextInput(attrs={}),
                  'etapa_vacona_fierro':forms.TextInput(attrs={}),
                  'etapa_vacona_vientre':forms.TextInput(attrs={}),
                  'etapa_vaca':forms.TextInput(attrs={}),
                  'periodo_gestacion':forms.TextInput(attrs={}),
                  'periodo_seco':forms.TextInput(attrs={}),
                  'periodo_lactancia':forms.TextInput(attrs={}),
                  'periodo_vacio':forms.TextInput(attrs={}),
                  'numero_ordenios':forms.TextInput(attrs={}),
                  'initial_rp':forms.TextInput(attrs={}),

        }

class GanaderiaForm(forms.ModelForm):
    class Meta:
        model = Ganaderia
        fields = ('nombreEntidad', 'direccion')
        widgets = {
                  'nombreEntidad':forms.TextInput(attrs={'placeholder': 'Nombre de la ganadería'}),
                  'direccion':forms.TextInput(attrs={'placeholder': 'Direccion de la ganadería'}),
        }

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

