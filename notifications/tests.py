from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase
from django.test.client import Client

from models import Notification


class NotificationTestCase(TestCase):
    def setUp(self):
        Notification.objects.create(star_date='2014-10-01',
                end_date='2014-10-10',
                state=2,
                module=0,
                ident_cattle=1,
                ident_sperm=1,
                ident_medicament=1,
                ident_food=1,
                name=0,
                farm=1)
        print "inicio el setup()"

    def listaNotificacionesReproduccion(self):
        nr = Notification.objects.get(module=0)
        self.assertEqual(c.farm, 1)
        print "inicio del test"

    def list_notification(self):
        c = Client()
        response = c.get('/list_notifications/')
        print response.status_code
