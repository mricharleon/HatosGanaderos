from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase
from django.test.client import Client

from models import Ganado
from views import list_cattle

class ProfileTestCase(TestCase):
    def setUp(self):
        Ganado.objects.create(ganaderia=1, nacimiento='2012-10-2', genero=1, raza=2, forma_concepcion=0, live_weight=10, unit_live_weight=2, observaciones='ninguna', edad_anios=2, edad_meses=2, edad_dias=12, identificacion_simple=1)

    def test_root_url_resolves_to_cattle_page_view(self):
        found = resolve('/list_cattle/')  
        self.assertEqual(found.func, home) 