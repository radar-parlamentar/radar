
from __future__ import unicode_literals
from django.test import TestCase
from modelagem.models import Parlamentar, Proposicao, Votacao, \
        PeriodoCasaLegislativa, Voto
from modelagem import utils
from modelagem.models import ANO, BIENIO, QUADRIENIO
from analises.analise import AnalisadorPeriodo
from plenaria import ordenacao
from modelagem import models
from datetime import date
from importadores import conv
from operator import itemgetter

class OrdenacaoTest(TestCase):	

	@classmethod
	def setUpClass(cls):
		cls.importer = conv.ImportadorConvencao()
		cls.importer.importar()

	@classmethod
	def tearDownClass(cls):
		from util_test import flush_db
		flush_db(cls)

	def test_ordenar_partidos(self):
		periodo = models.PeriodoCasaLegislativa(date(1989, 02, 02),
		date(1989, 10, 10))
		casa_legislativa = models.CasaLegislativa.objects.get(
		nome_curto='conv')
		ordem = []
		ordem = ordenacao.ordenar_partidos(casa_legislativa, periodo)
		self.assertEquals(ordem[0].nome, 'Jacobinos')
