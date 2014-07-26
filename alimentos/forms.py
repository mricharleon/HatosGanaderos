from django import forms
from django.utils.translation import ugettext_lazy as _
from alimentos.models import Alimento


class alimentoForm(forms.ModelForm):
    class Meta:
        model = Alimento
        exclude = ['ganaderia', 'ganado']
        widgets = {
                  'caduca':forms.DateInput(attrs={'class': 'datetimepicker2'})
        }