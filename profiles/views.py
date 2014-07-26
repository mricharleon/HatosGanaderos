from django.http import Http404
#raise Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from profiles.forms import GanaderiaForm, ConfiguracionForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from profiles.models import Profile, Ganaderia, Configuracion

def home(request):
	return render_to_response('home.html',
		context_instance=RequestContext(request))



def agrega_ganaderia_config(request, username):
	id_user = User.objects.filter(username=username)
	if Ganaderia.objects.filter(perfil_id=id_user):
		ganaderia_perfil = Ganaderia.objects.get(perfil_id=id_user)
		configuracion_perfil = Configuracion.objects.get(id=ganaderia_perfil.configuracion_id)
		# verfica si la ganaderia existe
		if ganaderia_perfil:
			form = ConfiguracionForm(instance=configuracion_perfil)
			form2 = GanaderiaForm(instance=ganaderia_perfil)

			if request.method == 'POST' and ganaderia_perfil:
				form = ConfiguracionForm(request.POST, instance=configuracion_perfil)
				form2 = GanaderiaForm(request.POST, instance=ganaderia_perfil)
				if form.is_valid() and form2.is_valid():
					form = form.save(commit=False)
					form.etapa_vientre = form.etapa_vacona
					form.save()
					form2.save()
					return redirect(reverse('userena_profile_detail', kwargs={'username': username}))

	elif request.method == 'POST':
		form = ConfiguracionForm(request.POST)
		form2 = GanaderiaForm(request.POST)#, instance=request.user

		if form.is_valid() and form2.is_valid():
			perf = Profile.objects.get(id=id_user)
			
			form2 = form2.save(commit=False)
			form2.perfil = perf
			form = form.save(commit=False)
			form.etapa_vientre = form.etapa_vacona
			form.save()
			c = Configuracion.objects.get(id=form.id)
			form2.configuracion = c
			form2.save()
			return redirect(reverse('userena_profile_detail', kwargs={'username': username}))
	else:
		form = ConfiguracionForm()
		form2 = GanaderiaForm()
	return render_to_response('agrega_ganaderia_configuracion.html',
								{'form': form, 'form2': form2},
								context_instance=RequestContext(request))
