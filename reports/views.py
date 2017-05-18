#-*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


from profiles.views import number_messages
from ganados.models import Ganaderia, Ganado, Gestacion, ProblemaGestacion, Ordenio, Insemination, Etapa
from profiles.models import Configuracion
from alimentos.models import ApplicationFood
from medicament.models import ApplicationMedicament, Medicament

from django.http import HttpResponse

from z3c.rml import rml2pdf
import datetime
import preppy

def generatePdf(request, cattle_id):
	# Load the rml template into the preprocessor, ...
    template = preppy.getModule('testDoc.prep')
    user = request.user
    farm = Ganaderia.objects.get(perfil=user)
    cattle = Ganado.objects.get(id=cattle_id)
    configuration = Configuracion.objects.get(id=farm.configuracion.id)
    if configuration.tipo_identificacion=='simple':
    	nombre = cattle.identificacion_simple.nombre
    	rp = cattle.identificacion_simple.rp
    	raza = cattle.get_raza_display()
    	nacimiento = str(cattle.nacimiento)
    	concepcion = cattle.get_forma_concepcion_display()
    	edad = str(cattle.edad_anios)+' años, '+str(cattle.edad_meses)+' meses y '+str(cattle.edad_dias)+' dias'
    	try:
    		cattle_mother = Ganado.objects.get(identificacion_simple__rp=cattle.identificacion_simple.rp_madre)
    		cattle_mother = cattle_mother.identificacion_simple.nombre
    	except ObjectDoesNotExist:
    		cattle_mother = 'Madre Desconocida'
    	try:
    		cattle_father = Ganado.objects.get(identificacion_simple__rp=cattle.identificacion_simple.rp_padre)
    		cattle_father = cattle_father.identificacion_simple.nombre
    	except ObjectDoesNotExist:
    		try:
    			cattle_father = Insemination.objects.get(rp=cattle.identificacion_simple.rp_padre)
    			cattle_father= cattle_father.name
    		except ObjectDoesNotExist:
    			cattle_father='Padre Desconocido'
    	celos = cattle.celos.count()
    	problem_gestacion=ProblemaGestacion.objects.filter(id=cattle.id)
    	total_births = Gestacion.objects.filter(
    		Q(ganado=cattle, is_active=False) &
    		~Q(problema=problem_gestacion)
    		).count()
    	total_problems_births=ProblemaGestacion.objects.filter(id=cattle.id).count()
    	ordenio = Ordenio.objects.filter(ganado=cattle)
    	count_milk=0
    	count=0
    	for o in ordenio:
    		if o.numero_ordenio == configuration.numero_ordenios:
    			count_milk+=o.total
    			count+=1
    	if count_milk > 0:
    		count_milk=count_milk/count

    	application_food=ApplicationFood.objects.filter(cattle=cattle)
    	food=[]
    	i=1
    	for f in application_food:
    		aux = str(f.food.name+' - '+str(f.food.consumer_amount)+' '+f.food.get_unit_display()+'. (X'+str(i)+')')
    		if aux not in food:
    			food.append(aux)
    		else:
    			index=food.index(aux)
    			i+=1
    			food[index]=str(f.food.name+' - '+str(f.food.consumer_amount)+' '+f.food.get_unit_display()+'.')+' (X'+str(i)+')'
    	medicament_wormer=Medicament.objects.filter(farm=farm, is_wormer=True)
    	application_medicament_wormer=ApplicationMedicament.objects.filter(medicament=medicament_wormer, cattle=cattle).order_by('medicament')
    	wormer=[]
    	i=1
    	for w in application_medicament_wormer:
    		aux=str(w.medicament.name+' - '+str(w.medicament.amount_application)+' '+w.medicament.get_unit_display()+'. (X'+str(i)+')')
    		if aux not in wormer:
    			wormer.append(aux)
    		else:
    			index=wormer.index(aux)
    			i+=1
    			wormer[index]=str(w.medicament.name+' - '+str(w.medicament.amount_application)+' '+w.medicament.get_unit_display()+'.')+' (X'+str(i)+')'
    	medicament_vaccine=Medicament.objects.filter(farm=farm, is_vaccine=True)
    	application_medicament_vaccine=ApplicationMedicament.objects.filter(medicament=medicament_vaccine, cattle=cattle).order_by('medicament')
    	vaccine=[]
    	i=1
    	for v in application_medicament_vaccine:
    		aux=str(v.medicament.name+' - '+str(v.medicament.amount_application)+' '+v.medicament.get_unit_display()+'. (X'+str(i)+')')
    		if aux not in vaccine:
    			vaccine.append(aux)
    		else:
    			index=vaccine.index(aux)
    			i+=1
    			vaccine[index]=str(v.medicament.name+' - '+str(v.medicament.amount_application)+' '+v.medicament.get_unit_display()+'.')+' (X'+str(i)+')'

    else:
    	nombre = cattle.identificacion_ecuador.nombre
    	rp = cattle.identificacion_ecuador.rp
    	raza = cattle.get_raza_display()
    	nacimiento = str(cattle.nacimiento)
    	concepcion = cattle.get_forma_concepcion_display()
    	edad = str(cattle.edad_anios)+' años, '+str(cattle.edad_meses)+' meses y '+str(cattle.edad_dias)+' dias'
    	try:
    		cattle_mother = Ganado.objects.get(identificacion_ecuador__rp=cattle.identificacion_ecuador.rp_madre)
    		cattle_mother = cattle_mother.identificacion_ecuador.nombre
    	except ObjectDoesNotExist:
    		cattle_mother = 'Madre Desconocida'
    	try:
    		cattle_father = Ganado.objects.get(identificacion_ecuador__rp=cattle.identificacion_ecuador.rp_padre)
    		cattle_father = cattle_father.identificacion_ecuador.nombre
    	except ObjectDoesNotExist:
    		try:
    			cattle_father = Insemination.objects.get(rp=cattle.identificacion_ecuador.rp_padre)
    			cattle_father= cattle_father.name
    		except ObjectDoesNotExist:
    			cattle_father='Padre Desconocido'
    	celos = cattle.celos.count()
    	problem_gestacion=ProblemaGestacion.objects.filter(id=cattle.id)
    	total_births = Gestacion.objects.filter(
    		Q(ganado=cattle, is_active=False) &
    		~Q(problema=problem_gestacion)
    		).count()
    	total_problems_births=ProblemaGestacion.objects.filter(id=cattle.id).count()
    	ordenio = Ordenio.objects.filter(ganado=cattle)
    	count_milk=0
    	count=0
    	for o in ordenio:
    		if o.numero_ordenio == configuration.numero_ordenios:
    			count_milk+=o.total
    			count+=1
    	if count_milk > 0:
    		count_milk=count_milk/count
    	application_food=ApplicationFood.objects.filter(cattle=cattle)
    	food=[]
    	i=1
    	for f in application_food:
    		aux = str(f.food.name+' - '+str(f.food.consumer_amount)+' '+f.food.get_unit_display()+'. (X'+str(i)+')')
    		if aux not in food:
    			food.append(aux)
    		else:
    			index=food.index(aux)
    			i+=1
    			food[index]=str(f.food.name+' - '+str(f.food.consumer_amount)+' '+f.food.get_unit_display()+'.')+' (X'+str(i)+')'
    	medicament_wormer=Medicament.objects.filter(farm=farm, is_wormer=True)
    	application_medicament_wormer=ApplicationMedicament.objects.filter(medicament=medicament_wormer, cattle=cattle).order_by('medicament')
    	wormer=[]
    	i=1
    	for w in application_medicament_wormer:
    		aux=str(w.medicament.name+' - '+str(w.medicament.amount_application)+' '+w.medicament.get_unit_display()+'. (X'+str(i)+')')
    		if aux not in wormer:
    			wormer.append(aux)
    		else:
    			index=wormer.index(aux)
    			i+=1
    			wormer[index]=str(w.medicament.name+' - '+str(w.medicament.amount_application)+' '+w.medicament.get_unit_display()+'.')+' (X'+str(i)+')'
    	

    # ... and do the preprocessing.
    table=[]
    # date, name, website, email, description, farm, adress, table
    rmlText = template.get(
        table,
        datetime.datetime.now().strftime("%Y-%m-%d"),
        'Reporte Individual de Ganado',
        'www.hatosganaderos.com',
        'info@hatosganaderos.com',
        'HatosGanaderos te ayuda con el control y organización de reproducción, alimentación, sanidad y producción de toda tu entidad ganadera.',
        'Ganadería Lojana',
        'Ciudadela universitaria',
        nombre,
        rp,
        raza,
        nacimiento,
        concepcion,
        edad,
        cattle_mother,
        cattle_father,
        celos,
        total_births,
        total_problems_births,
        count_milk,
        food,
        wormer,
        vaccine)
    
    # Finally generate the *.pdf output ...
    pdf = rml2pdf.parseString(rmlText)
    
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="somefilename.pdf"'

    return response


def docs(request):
	return render_to_response('_build/html/index.html',
		context_instance=RequestContext(request))

def list_reports(request):
	user = request.user
	number_message = number_messages(request, user.username)
	return render_to_response('list_reports.html',
		{'number_messages': number_message},
		context_instance=RequestContext(request))

def view_report_female(request, id_cattle):
	user = request.user
	number_message = number_messages(request, user.username)
	farm = Ganaderia.objects.get(perfil=user)
	configuration = Configuracion.objects.get(id=farm.configuracion.id)

	cattle = Ganado.objects.get(Q(ganaderia=farm) & ( Q(identificacion_simple_id__rp=id_cattle) | Q(identificacion_ecuador_id__rp=id_cattle) ) )
	problem_gestacion = ProblemaGestacion.objects.filter(id=cattle.id)

	total_births = Gestacion.objects.filter(
			Q(ganado=cattle, is_active=False) &
			~Q(problema=problem_gestacion)
		).count()
	total_problems_births =ProblemaGestacion.objects.filter(id=cattle.id).count()
	
	if configuration.tipo_identificacion=='simple':
		try:
			cattle_mother = Ganado.objects.get(identificacion_simple__rp=cattle.identificacion_simple.rp_madre)
		except ObjectDoesNotExist:
			cattle_mother = 'Desconocida'

		try:
			cattle_father = Ganado.objects.get(identificacion_simple__rp=cattle.identificacion_simple.rp_padre)
		except ObjectDoesNotExist:
			try:
				cattle_father = Insemination.objects.get(rp=cattle.identificacion_simple.rp_padre)
			except ObjectDoesNotExist:
				cattle_father = 'Desconocido'

	else:
		try:
			cattle_mother = Ganado.objects.get(identificacion_ecuador__rp=cattle.identificacion_ecuador.rp_madre)
		except ObjectDoesNotExist:
			cattle_mother = 'Desconocida'

		try:
			cattle_father = Ganado.objects.get(identificacion_ecuador__rp=cattle.identificacion_ecuador.rp_padre)
		except ObjectDoesNotExist:
			try:
				cattle_father = Insemination.objects.get(rp=cattle.identificacion_ecuador.rp_padre)
			except ObjectDoesNotExist:
				cattle_father = 'Desconocido'


	if cattle.etapas.all():
		etapa = Etapa.objects.get(ganado=cattle, is_active=True)


	ordenio = Ordenio.objects.filter(ganado=cattle)
	count_milk = 0
	count = 0
	for o in ordenio:
		if o.numero_ordenio == configuration.numero_ordenios:
			count_milk += o.total
			count += 1
	if count_milk > 0:
		count_milk = count_milk / count

	application_food = ApplicationFood.objects.filter(cattle=cattle)
	food = []
	i = 1
	for f in application_food:
		aux = str(f.food.name+' - '+str(f.food.consumer_amount)+' '+f.food.get_unit_display()+'. (X'+str(i)+')')
		if aux not in food:
			food.append(aux)
		else:
			index = food.index(aux)
			i += 1
			food[index] = str(f.food.name+' - '+str(f.food.consumer_amount)+' '+f.food.get_unit_display()+'.')+' (X'+str(i)+')'

	medicament_wormer = Medicament.objects.filter(farm=farm, is_wormer=True)
	application_medicament_wormer = ApplicationMedicament.objects.filter(medicament=medicament_wormer, cattle=cattle).order_by('medicament')
	wormer = []
	i = 1
	for w in application_medicament_wormer:
		aux = str(w.medicament.name+' - '+str(w.medicament.amount_application)+' '+w.medicament.get_unit_display()+'. (X'+str(i)+')')
		if aux not in wormer:
			wormer.append(aux)
		else:
			index = wormer.index(aux)
			i += 1
			wormer[index] = str(w.medicament.name+' - '+str(w.medicament.amount_application)+' '+w.medicament.get_unit_display()+'.')+' (X'+str(i)+')'

	medicament_vaccine = Medicament.objects.filter(farm=farm, is_vaccine=True)
	application_medicament_vaccine = ApplicationMedicament.objects.filter(medicament=medicament_vaccine, cattle=cattle).order_by('medicament')
	vaccine = []
	i = 1
	for v in application_medicament_vaccine:
		aux = str(v.medicament.name+' - '+str(v.medicament.amount_application)+' '+v.medicament.get_unit_display()+'. (X'+str(i)+')')
		if aux not in vaccine:
			vaccine.append(aux)
		else:
			index = vaccine.index(aux)
			i += 1
			vaccine[index] = str(v.medicament.name+' - '+str(v.medicament.amount_application)+' '+v.medicament.get_unit_display()+'.')+' (X'+str(i)+')'
		
	

	return render_to_response('view_report_female.html',
		{'cattle': cattle,
		 'total_births': total_births,
		 'total_problems_births': total_problems_births,
		 'cattle_mother': cattle_mother,
		 'cattle_father': cattle_father,
		 'count_milk': count_milk,
		 'food': food,
		 'wormer': wormer,
		 'vaccine': vaccine,
		 'number_messages': number_message,
		 'etapa': etapa},
		context_instance=RequestContext(request))	


 