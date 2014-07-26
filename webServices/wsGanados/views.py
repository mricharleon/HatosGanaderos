from django.db.models import Q
from django.http import HttpResponse
from ganados.models import Ganado, Identificacion_Simple, Ganaderia
from profiles.models import Configuracion

from django.contrib.auth.models import User

from django.core import serializers
from django.utils import simplejson

def wsGanados_view(request, username):
	#p = Identificacion_Simple.objects.filter(ganado__identificacion_simple__isnull=False)
	id_user = User.objects.filter(username=username)
	ganaderia = Ganaderia.objects.get(perfil_id=id_user)
	
	gg = Ganado.objects.filter(ganaderia_id=ganaderia.id).filter(identificacion_simple__nombre__isnull=False)

	data = serializers.serialize('json', gg)
	#data = serializers.serialize('json', Ganado.objects.all())
	return HttpResponse(data, mimetype='application/json')




'''
from django.core.exceptions import ObjectDoesNotExist
try:
    e = Entry.objects.get(id=3)
    b = Blog.objects.get(id=1)
except ObjectDoesNotExist:
    print("Either the entry or blog doesn't exist.")
'''