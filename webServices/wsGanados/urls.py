from django.conf.urls import patterns, url


urlpatterns = patterns('webServices.wsGanados.views',
	url(r'^ws/ganados_hembras/$', 'wsGanadosHembras_view', name='wsGanadosHembras_view'),
	url(r'^ajax/cattle_male_rp/$', 'ajaxCattleMaleRp_view', name='ajaxCattleMaleRp_view'),
	url(r'^ajax/cattle_male/$', 'ajaxCattleMale_view', name='ajaxCattleMale_view'),
	url(r'^ajax/ganados_machos_inseminacion/$', 'ajaxGanadosMachosInseminacion_view', name='ajaxGanadosMachosInseminacion_view'),
	url(r'^ws/ganados/$', 'wsGanados_view', name='wsGanados_view'),
	url(r'^ws/ganados_produccion/$', 'wsGanadosProduccion_view', name='wsGanadosProduccion_view'),

	url(r'^ws/wormer/$', 'wsWormer_view', name='wsWormer_view'),
	url(r'^ajax/vaccine/$', 'ajaxVaccine_view', name='ajaxVaccine_view'),
	url(r'^ajax/food/$', 'ajaxFood_view', name='ajaxFood_view'),
	url(r'^ajax/insemination/$', 'ajaxInsemination_view', name='ajaxInsemination_view'),
	url(r'^ajax/assign_cattle_vaccine/$', 'ajaxAssignCattleVaccine_view', name='ajaxAssignCattleVaccine_view'),
	url(r'^ajax/assign_cattle_vaccine_final/$', 'ajaxAssignCattleVaccineFinal', name='ajaxAssignCattleVaccineFinal'),
	url(r'^ajax/assign_cattle_wormer/$', 'ajaxAssignCattleWormer_view', name='ajaxAssignCattleWormer_view'),
	url(r'^ajax/assign_cattle_wormer_final/$', 'ajaxAssignCattleWormerFinal', name='ajaxAssignCattleWormerFinal'),
	url(r'^ajax/assign_cattle_food/$', 'ajaxAssignCattleFood_view', name='ajaxAssignCattleFood_view'),
	url(r'^ajax/assign_cattle_food_final/$', 'ajaxAssignCattleFoodFinal', name='ajaxAssignCattleFoodFinal'),
	
	# refresh
	url(r'^ajax/refresh/$', 'ajaxRefresh', name='ajaxRefresh'),
	
)