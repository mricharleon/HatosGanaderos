from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase
from django.test.client import Client

from models import Configuracion
from views import home

class ProfileTestCase(TestCase):
    def setUp(self):
        Configuracion.objects.create(tipo_identificacion= 'Simple', celo_frecuencia=20, celo_frecuencia_error=2, celo_duracion=24, celo_duracion_error=2, celo_despues_parto=70, celo_despues_parto_error=2, intentos_verificacion_celo=4, etapa_ternera=10, etapa_vacona=20, etapa_vientre=20, periodo_gestacion=300, periodo_seco=3, periodo_lactancia=3, periodo_vacio=3, numero_ordenios=50)
        print "inicio el setup()"
        a = 10

    def login(self):
    	c = Client()
    	response = c.post('/accounts/signin/', {'username': 'richar', 'password': 'richar'})
    	print response.status_code

    def test_configuracion(self):
        c = Configuracion.objects.get(numero_ordenios__exact=50)
        self.assertEqual(c.numero_ordenios, 50)
        print "inicio del test"

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')  
        self.assertEqual(found.func, home) 

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()  
        response = home(request)  
        self.assertTrue(response.content.startswith(b'<html>'))  
        self.assertIn(b'<title>HatosGanaderos</title>', response.content)  
        self.assertTrue(response.content.endswith(b'</html>'))  