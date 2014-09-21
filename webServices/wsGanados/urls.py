from django.conf.urls import patterns, url


urlpatterns = patterns('webServices.wsGanados.views',
	url(r'^ws/ganados_hembras/$', 'wsGanadosHembras_view', name='wsGanadosHembras_view'),
	url(r'^ws/ganados_machos/$', 'wsGanadosMachos_view', name='wsGanadosMachos_view'),
	url(r'^ws/ganados/$', 'wsGanados_view', name='wsGanados_view'),
	url(r'^ws/ganados_produccion/$', 'wsGanadosProduccion_view', name='wsGanadosProduccion_view'),

	url(r'^ws/wormer/$', 'wsWormer_view', name='wsWormer_view'),
	url(r'^ajax/vaccine/$', 'ajaxVaccine_view', name='ajaxVaccine_view'),
	url(r'^ajax/food/$', 'ajaxFood_view', name='ajaxFood_view'),
	url(r'^ajax/assign_cattle_food/$', 'ajaxAssignCattleFood_view', name='ajaxAssignCattleFood_view'),
	url(r'^ajax/assign_cattle_food_final/$', 'ajaxAssignCattleFoodFinal', name='ajaxAssignCattleFoodFinal'),
)