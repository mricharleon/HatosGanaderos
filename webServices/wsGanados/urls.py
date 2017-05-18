from django.conf.urls import patterns, url


urlpatterns = patterns('webServices.wsGanados.views',
	url(r'^ws/ganados_hembras/$', 'wsGanadosHembras_view', name='wsGanadosHembras_view'),
	url(r'^ajax/cattle_male_rp/$', 'ajaxCattleMaleRp_view', name='ajaxCattleMaleRp_view'),
	url(r'^ajax/cattle_male/$', 'ajaxCattleMale_view', name='ajaxCattleMale_view'),
	url(r'^ajax/ganados_machos_inseminacion/$', 'ajaxGanadosMachosInseminacion_view', name='ajaxGanadosMachosInseminacion_view'),
	url(r'^ws/ganados/$', 'wsGanados_view', name='wsGanados_view'),
	url(r'^ws/ganados/terneras$', 'wsGanadosTerneras_view', name='wsGanadosTerneras_view'),
	url(r'^ws/ganados/media$', 'wsGanadosMedia_view', name='wsGanadosMedia_view'),
	url(r'^ws/ganados/fierro$', 'wsGanadosFierro_view', name='wsGanadosFierro_view'),
	url(r'^ws/ganados/vientre$', 'wsGanadosVientre_view', name='wsGanadosVientre_view'),
	url(r'^ws/ganados/vaca$', 'wsGanadosVaca_view', name='wsGanadosVaca_view'),
	url(r'^ws/ganados_produccion/$', 'wsGanadosProduccion_view', name='wsGanadosProduccion_view'),
	url(r'^ajax/downCattle/$', 'ajaxDownCattle_view', name='ajaxDownCattle_view'),

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

	# carga notificaciones por partes
	url(r'^ajax/add_list_notifications_produccion_realizadas/$', 'ajaxAddListNotificationsProduccionRealizadas', name='ajaxAddListNotificationsProduccionRealizadas'),
	url(r'^ajax/add_list_notifications_produccion_no_realizadas/$', 'ajaxAddListNotificationsProduccionNoRealizadas', name='ajaxAddListNotificationsProduccionNoRealizadas'),
	url(r'^ajax/add_list_notifications_reproduccion_realizadas/$', 'ajaxAddListNotificationsReproduccionRealizadas', name='ajaxAddListNotificationsReproduccionRealizadas'),
	url(r'^ajax/add_list_notifications_reproduccion_no_realizadas/$', 'ajaxAddListNotificationsReproduccionNoRealizadas', name='ajaxAddListNotificationsReproduccionNoRealizadas'),
	url(r'^ajax/add_list_notifications_sanidad_no_realizadas/$', 'ajaxAddListNotificationsSanidadNoRealizadas', name='ajaxAddListNotificationsSanidadNoRealizadas'),
	url(r'^ajax/add_list_notifications_sanidad_realizadas/$', 'ajaxAddListNotificationsSanidadRealizadas', name='ajaxAddListNotificationsSanidadRealizadas'),
	url(r'^ajax/add_list_notifications_alimentacion_no_realizadas/$', 'ajaxAddListNotificationsAlimentacionNoRealizadas', name='ajaxAddListNotificationsAlimentacionNoRealizadas'),
	
	# refresh
	url(r'^ajax/refresh/$', 'ajaxRefresh', name='ajaxRefresh'),
	
)