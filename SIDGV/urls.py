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
    
    # perfiles de tecnicos tambien
    (r'^accounts/', include('userena.urls')),
    #(r'^messages/', include('userena.contrib.umessages.urls')),
    url(r'^$', 'profiles.views.home', name='home'),
   
    (r'^i18n/', include('django.conf.urls.i18n')),


    # messages
    url(r'^messages/$', 'messages.views.messages_list', name='messages_list'),
    url(r'^messages_read/$', 'messages.views.messages_list_read', name='messages_list_read'),
    url(r'^messages_no_read/$', 'messages.views.messages_list_no_read', name='messages_list_no_read'),
    url(r'^messages_details/(?P<user_id>[\.\w-]+)/(?P<user_send_id>[\.\w-]+)/(?P<user_receiver_id>[\.\w-]+)/$', 'messages.views.messages_details', name='messages_details'),
    url(r'^new_message/$', 'messages.views.new_message', name='new_message'),

    # real time of the messages
    url(r'^alert_messages/$', 'messages.views.alert_messages', name='alert_messages'),

    # farm
    url(r'^agrega_ganaderia_config/$', 'profiles.views.agrega_ganaderia_config', name='agrega_ganaderia_config'),

    # ganados
    url(r'^agrega_ganado/(?P<username>[\.\w-]+)/$', 'ganados.views.agrega_ganado', name='agrega_ganado'),
    url(r'^lista_ganado/$', 'ganados.views.lista_ganado', name='lista_ganado'),
    url(r'^edita_ganado/(?P<username>[\.\w-]+)/(?P<ganado_id>[\.\w-]+)/$', 'ganados.views.edita_ganado', name='edita_ganado'),
    url(r'^edita_ganado_celo/(?P<username>[\.\w-]+)/(?P<ganado_id>[\.\w-]+)/$', 'ganados.views.edita_ganado_celo', name='edita_ganado_celo'),

    url(r'^lista_ganado_produccion/(?P<username>[\.\w-]+)/$', 'ganados.views.lista_ganado_produccion', name='lista_ganado_produccion'),
    url(r'^agrega_ganado_ordenio/(?P<username>[\.\w-]+)/(?P<ganado_id>[\.\w-]+)/$', 'ganados.views.agrega_ganado_ordenio', name='agrega_ganado_ordenio'),
    url(r'^edita_ganado_ordenio/(?P<username>[\.\w-]+)/(?P<ganado_id>[\.\w-]+)/(?P<num_ordenio>[\.\w-]+)/$', 'ganados.views.edita_ganado_ordenio', name='edita_ganado_ordenio'),

    # servicio
    url(r'^add_service/(?P<id_cattle>[\.\w-]+)/$', 'ganados.views.add_service', name='add_service'),
    url(r'^add_attempt_service/(?P<id_cattle>[\.\w-]+)/$', 'ganados.views.add_attempt_service', name='add_attempt_service'),
    url(r'^verify_attempt/(?P<id_attempt>[\.\w-]+)/$', 'ganados.views.verify_attempt', name='verify_attempt'),

    # gestacion
    url(r'^gestacion/(?P<id_cattle>[\.\w-]+)/$', 'ganados.views.gestacion', name='gestacion'),
    url(r'^problem_gestacion/(?P<id_cattle>[\.\w-]+)/$', 'ganados.views.problem_gestacion', name='problem_gestacion'),

    # food
    url(r'^add_food/$', 'alimentos.views.add_food', name='add_food'),
    url(r'^list_food/$', 'alimentos.views.list_food', name='list_food'),
    url(r'^edit_food/(?P<alimento_id>[\.\w-]+)/$', 'alimentos.views.edit_food', name='edit_food'),
    url(r'^asigna_alimento/(?P<alimento_id>[\.\w-]+)/$', 'alimentos.views.asigna_alimento', name='asigna_alimento'),

    # medicaments and vaccine
    url(r'^add_wormer/$', 'medicament.views.add_wormer', name='add_wormer'),
    url(r'^list_wormer/$', 'medicament.views.list_wormer', name='list_wormer'),
    url(r'^edit_wormer/(?P<id_medicament>[\.\w-]+)/$', 'medicament.views.edit_wormer', name='edit_wormer'),

    url(r'^add_vaccine/$', 'medicament.views.add_vaccine', name='add_vaccine'),
    url(r'^list_vaccine/$', 'medicament.views.list_vaccine', name='list_vaccine'),
    url(r'^edit_vaccine/(?P<id_medicament>[\.\w-]+)/$', 'medicament.views.edit_vaccine', name='edit_vaccine'),


    (r'^', include('webServices.wsGanados.urls')),
)

# Add media and static files
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


