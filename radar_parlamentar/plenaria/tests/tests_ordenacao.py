# -*- coding: utf-8 -*- 

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
	
	def test_ordem_dos_parlamentares(self):
		proposicao = models.Proposicao.objects.get(id=1)
		resultado = ordenacao.ordem_dos_parlamentares(proposicao)
		self.assertEqual(resultado[0][0].descricao, 'Reforma agrária')
		self.assertEqual(resultado[0][1][0].nome, 'Pierre')


	def test_ordenar_partidos(self):
		periodo = models.PeriodoCasaLegislativa(date(1989, 0o2, 0o2),
		date(1989, 10, 10))
		casa_legislativa = models.CasaLegislativa.objects.get(
		nome_curto='conv')
		ordem = []
		ordem = ordenacao.ordenar_partidos(casa_legislativa, periodo)
		self.assertEqual(ordem[0].nome, 'Jacobinos')
		self.assertEqual(ordem[1].nome, 'Girondinos')
		self.assertEqual(ordem[2].nome, 'Monarquistas')

	def test_def_ordenar_votantes(self):
		proposicao = models.Proposicao.objects.get(id=1)
		resultado = ordenacao.ordenar_votantes(proposicao)
		parla = Parlamentar.objects.filter(nome='Pierre')[0]
		primeiro = (parla.partido,1)
		self.assertEqual(resultado[parla],primeiro)

	

		#AttributeError: 'QuerySet' object has no attribute 'voto_set', QuerySet não está reconhecendo o _set
	"""def test_ordem_dos_parl_por_votacao(self):
		proposicao = models.Proposicao.objects.get(id=1)
		votacao = Votacao.objects.filter(proposicao=proposicao).order_by('data')
		casa_legislativa = proposicao.casa_legislativa
		datas_votacoes = [votac.data for votac in votacao]
		pr = utils.PeriodosRetriever(casa_legislativa = casa_legislativa,
			periodicidade = QUADRIENIO,
			data_da_primeira_votacao = min(datas_votacoes),
			data_da_ultima_votacao = max(datas_votacoes),
			numero_minimo_de_votacoes = 1 )
		periodo = pr.get_periodos()[-1]
		lista_ordenada_partidos = ordenacao.ordenar_partidos(casa_legislativa, periodo)
		dicionario_votantes = ordenacao.ordenar_votantes(proposicao) 
		partidos = ordenacao.ordenar_partidos(casa_legislativa, periodo)
		teste = ordenacao.ordem_dos_parl_por_votacao(votacao,dicionario_votantes,partidos)
		print teste"""
