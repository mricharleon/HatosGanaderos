from django.conf.urls import patterns, url, include
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

import django_cron
#django_cron.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    # favicon

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
    url(r'^agrega_ganaderia_config/$', 'profiles.views.agrega_ganaderia_config', name='agrega_ganaderia_config'),

    # ganados
    url(r'^add_cattle/$', 'ganados.views.add_cattle', name='add_cattle'),
    url(r'^add_down_cattle/(?P<id_cattle>[\.\w-]+)/$', 'ganados.views.add_down_cattle', name='add_down_cattle'),
    url(r'^list_down_cattle/$', 'ganados.views.list_down_cattle', name='list_down_cattle'),
    url(r'^list_cattle/$', 'ganados.views.list_cattle', name='list_cattle'),
    url(r'^list_cattle_terneras/$', 'ganados.views.list_cattle_terneras', name='list_cattle_terneras'),
    url(r'^list_cattle_media/$', 'ganados.views.list_cattle_media', name='list_cattle_media'),
    url(r'^list_cattle_fierro/$', 'ganados.views.list_cattle_fierro', name='list_cattle_fierro'),
    url(r'^list_cattle_vientre/$', 'ganados.views.list_cattle_vientre', name='list_cattle_vientre'),
    url(r'^list_cattle_vaca/$', 'ganados.views.list_cattle_vaca', name='list_cattle_vaca'),
    url(r'^list_cattle_male/$', 'ganados.views.list_cattle_male', name='list_cattle_male'),
    url(r'^edita_ganado/(?P<ganado_id>[\.\w-]+)/$', 'ganados.views.edita_ganado', name='edita_ganado'),
    url(r'^edit_cattle_male/(?P<cattle_id>[\.\w-]+)/$', 'ganados.views.edit_cattle_male', name='edit_cattle_male'),
    url(r'^edita_ganado_celo/(?P<ganado_id>[\.\w-]+)/$', 'ganados.views.edita_ganado_celo', name='edita_ganado_celo'),

    url(r'^lista_ganado_produccion/$', 'ganados.views.lista_ganado_produccion', name='lista_ganado_produccion'),
    url(r'^agrega_ganado_ordenio/(?P<ganado_id>[\.\w-]+)/$', 'ganados.views.agrega_ganado_ordenio', name='agrega_ganado_ordenio'),
    url(r'^edita_ganado_ordenio/(?P<ganado_id>[\.\w-]+)/(?P<num_ordenio>[\.\w-]+)/$', 'ganados.views.edita_ganado_ordenio', name='edita_ganado_ordenio'),

    url(r'^deferEtapa/(?P<notification_id>[\.\w-]+)/$', 'ganados.views.deferEtapa', name='deferEtapa'),

    # inseminacion
    url(r'^add_insemination/$', 'ganados.views.add_insemination', name='add_insemination'),
    url(r'^add_down_insemination/(?P<id_sperm>[\.\w-]+)/$', 'ganados.views.add_down_insemination', name='add_down_insemination'),
    url(r'^list_insemination/$', 'ganados.views.list_insemination', name='list_insemination'),
    url(r'^edit_insemination/(?P<insemination_id>[\.\w-]+)/$', 'ganados.views.edit_insemination', name='edit_insemination'),

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
    url(r'^asign_wormer/(?P<wormer_id>[\.\w-]+)/$', 'medicament.views.asign_wormer', name='asign_wormer'),

    url(r'^add_vaccine/$', 'medicament.views.add_vaccine', name='add_vaccine'),
    url(r'^list_vaccine/$', 'medicament.views.list_vaccine', name='list_vaccine'),
    url(r'^edit_vaccine/(?P<id_medicament>[\.\w-]+)/$', 'medicament.views.edit_vaccine', name='edit_vaccine'),
    url(r'^asign_vaccine/(?P<vaccine_id>[\.\w-]+)/$', 'medicament.views.asign_vaccine', name='asign_vaccine'),

    # notificaciones
    url(r'^list_notifications/$', 'notifications.views.list_notifications', name='list_notifications'),
    url(r'^list_notifications_reproduccion/$', 'notifications.views.list_notifications_reproduccion', name='list_notifications_reproduccion'),
    url(r'^list_notifications_reproduccion_realizadas/$', 'notifications.views.list_notifications_reproduccion_realizadas', name='list_notifications_reproduccion_realizadas'),
    url(r'^list_notifications_reproduccion_norealizadas/$', 'notifications.views.list_notifications_reproduccion_norealizadas', name='list_notifications_reproduccion_norealizadas'),
    url(r'^list_notifications_produccion/$', 'notifications.views.list_notifications_produccion', name='list_notifications_produccion'),
    url(r'^list_notifications_produccion_realizadas/$', 'notifications.views.list_notifications_produccion_realizadas', name='list_notifications_produccion_realizadas'),
    url(r'^list_notifications_produccion_norealizadas/$', 'notifications.views.list_notifications_produccion_norealizadas', name='list_notifications_produccion_norealizadas'),
    url(r'^list_notifications_sanidad/$', 'notifications.views.list_notifications_sanidad', name='list_notifications_sanidad'),
    url(r'^list_notifications_sanidad_realizadas/$', 'notifications.views.list_notifications_sanidad_realizadas', name='list_notifications_sanidad_realizadas'),
    url(r'^list_notifications_sanidad_norealizadas/$', 'notifications.views.list_notifications_sanidad_norealizadas', name='list_notifications_sanidad_norealizadas'),
    url(r'^list_notifications_alimentacion/$', 'notifications.views.list_notifications_alimentacion', name='list_notifications_alimentacion'),
    url(r'^list_notifications_alimentacion_realizadas/$', 'notifications.views.list_notifications_alimentacion_realizadas', name='list_notifications_alimentacion_realizadas'),
    url(r'^list_notifications_alimentacion_norealizadas/$', 'notifications.views.list_notifications_alimentacion_norealizadas', name='list_notifications_alimentacion_norealizadas'),
    url(r'^realized_notification/(?P<notification_id>[\.\w-]+)/$', 'notifications.views.realizedNotification', name='realizedNotification'),
    url(r'^realized_notification_before/(?P<notification_id>[\.\w-]+)/(?P<cattle_id>[\.\w-]+)/$', 'notifications.views.realizedNotificationBefore', name='realizedNotificationBefore'),


    # reportes
    url(r'^list_reports/$', 'reports.views.list_reports', name='list_reports'),    
    url(r'^view_report_female/(?P<id_cattle>[\.\w-]+)/$', 'reports.views.view_report_female', name='view_report_female'),    
    url(r'^generate_pdf/(?P<cattle_id>[\.\w-]+)/$', 'reports.views.generatePdf', name='generate_pdf'),    
    #url(r'^list_report_reproduccion/$', 'reports.views.list_report_reproduccion', name='list_report_reproduccion'),    

    url(r'^docs/.*', 'reports.views.docs', name='docs'),  
    #url(r'^docs/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.DOCS_ROOT}),
    #url(r'^docs/', 'reports.views.docs', ),


    (r'^', include('webServices.wsGanados.urls')),
)

# Add media and static files
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


