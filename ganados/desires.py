# -*- coding: utf-8 -*-
from ganados.models import Ganado
import datetime
"""
class Desires(self):
	def __init__(self):
		self.date = datetime.date.today()
		#cattles = Ganado.objects.filter(ganaderia=farm, ordenios__fecha=self.date, ordenios__numero_ordenio=0)
		dic_ordenio = []
		#for c in cattles:
		#	dic_ordenio["ganado"] = "sa" 
		#self.num_ordenios = 
"""
def cattleProduccion(self):
	print "inicio el cattleProduccion(): "
	date = datetime.date.today()
	print date
	cattles = Ganado.objects.get(id=1)
	print " cattle_id"
	print cattles.id