# -*- coding: utf-8 -*-
from django_cron import CronJobBase, Schedule

import spade
import sys
import datetime
import time

import desires

from django.contrib.auth.models import User

def userActive(request):
	return request.user

class AgentProduccion(spade.Agent.Agent):
    class BehaviourProduccion(spade.Behaviour.Behaviour):
        def onStart(self):
            print "Inicio de BehaviourProduccion . . ."
            self.counter = 0

        def _process(self):
            print "Contador:", self.counter
            user = userActive()
            self.counter += 1
            time.sleep(1)
            desires.cattleProduccion(self)
            if self.counter > 10:
            	self.stop()
            	sys.exit(0)

    def _setup(self):
        print "AgentProduccion iniciado . . ."
        b = self.BehaviourProduccion()
        self.addBehaviour(b, None)


class CronJobProduccion(CronJobBase):
	#ALLOW_PARALLEL_RUNS = True
	RUN_EVERY_MINS = 0
	MIN_NUM_FAILURES = 3
	
	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'ganados.cron_job'    # a unique code

	def do(self):
		a = AgentProduccion("agent_produccion@127.0.0.1", "secret")
		a.start()