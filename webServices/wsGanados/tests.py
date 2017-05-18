from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase
from django.test.client import Client

from views import *

class ProfileTestCase(TestCase):
    def setUp(self):
        pass

    def test_root_url_resolves_to_insemination_page_view(self):
        found = resolve('/ajax/insemination/')  
        self.assertEqual(found.func, insemination) 

    def test_insemination_page_returns_correct_html(self):
        request = HttpRequest()  
        response = insemination(request)  
        self.assertTrue(response.content.startswith(b'<html>'))  
        self.assertIn(b'<title>HatosGanaderos</title>', response.content)  
        self.assertTrue(response.content.endswith(b'</html>')) 