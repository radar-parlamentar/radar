# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django.test import TestCase
from modelagem.models import Parlamentar, Proposicao, Votacao, \
        PeriodoCasaLegislativa, Voto
from modelagem import utils
from modelagem.models import ANO, BIENIO, QUADRIENIO
from analises.analise import AnalisadorPeriodo
from modelagem import models
from datetime import date
from importadores import conv
from operator import itemgetter
from plenaria import views

class ViewsTest(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.importer = conv.ImportadorConvencao()
		cls.importer.importar()

	@classmethod
	def tearDownClass(cls):
		from util_test import flush_db
		flush_db(cls)

	def test_identificador(self):
		proposicao = models.Proposicao.objects.get(id=3)
		#proposicao.ano = "1990"
		resultado = views.identificador(proposicao)
		self.assertEquals(resultado, "PL-1-")