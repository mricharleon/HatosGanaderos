from django.conf.urls import patterns, url


urlpatterns = patterns('webServices.wsGanados.views',
	url(r'^ws/ganados/(?P<username>[\.\w-]+)/$', 'wsGanados_view', name='wsGanados_view'),
)