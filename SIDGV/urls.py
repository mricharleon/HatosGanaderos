from django.conf.urls import patterns, url, include
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    # SIDGV Override the signup form with our own, which includes a
    # first and last name.
    # (r'^accounts/signup/$',
    #  'userena.views.signup',
    #  {'signup_form': SignupFormExtra}),
    
    (r'^accounts/', include('userena.urls')),
    (r'^messages/', include('userena.contrib.umessages.urls')),
    url(r'^$', 'profiles.views.home', name='home'),
    (r'^i18n/', include('django.conf.urls.i18n')),

    # ganaderia
    url(r'^agrega_ganaderia_config/(?P<username>[\.\w-]+)/$', 'profiles.views.agrega_ganaderia_config', name='agrega_ganaderia_config'),

    # ganados
    url(r'^agrega_ganado/(?P<username>[\.\w-]+)/$', 'ganados.views.agrega_ganado', name='agrega_ganado'),
    url(r'^lista_ganado/(?P<username>[\.\w-]+)/$', 'ganados.views.lista_ganado', name='lista_ganado'),
    url(r'^edita_ganado/(?P<username>[\.\w-]+)/(?P<ganado_id>[\.\w-]+)/$', 'ganados.views.edita_ganado', name='edita_ganado'),
    url(r'^edita_ganado_celo/(?P<username>[\.\w-]+)/(?P<ganado_id>[\.\w-]+)/$', 'ganados.views.edita_ganado_celo', name='edita_ganado_celo'),

    url(r'^lista_ganado_produccion/(?P<username>[\.\w-]+)/$', 'ganados.views.lista_ganado_produccion', name='lista_ganado_produccion'),
    url(r'^agrega_ganado_ordenio/(?P<username>[\.\w-]+)/(?P<ganado_id>[\.\w-]+)/$', 'ganados.views.agrega_ganado_ordenio', name='agrega_ganado_ordenio'),
    url(r'^edita_ganado_ordenio/(?P<username>[\.\w-]+)/(?P<ganado_id>[\.\w-]+)/(?P<num_ordenio>[\.\w-]+)/$', 'ganados.views.edita_ganado_ordenio', name='edita_ganado_ordenio'),

    url(r'^agrega_alimento/(?P<username>[\.\w-]+)/$', 'alimentos.views.agrega_alimento', name='agrega_alimento'),
    url(r'^lista_alimento/(?P<username>[\.\w-]+)/$', 'alimentos.views.lista_alimento', name='lista_alimento'),
    url(r'^edita_alimento/(?P<username>[\.\w-]+)/(?P<alimento_id>[\.\w-]+)/$', 'alimentos.views.edita_alimento', name='edita_alimento'),
    url(r'^asigna_alimento/(?P<username>[\.\w-]+)/(?P<alimento_id>[\.\w-]+)/(?P<ganado_id>[\.\w-]+)/$', 'alimentos.views.asigna_alimento', name='asigna_alimento'),

    (r'^', include('webServices.wsGanados.urls')),
)

# Add media and static files
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


