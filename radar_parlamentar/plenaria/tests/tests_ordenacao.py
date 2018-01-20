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
        proposicao = models.Proposicao.objects.all()[2]
        resultado = ordenacao.ordem_dos_parlamentares(proposicao)
        self.assertEqual(resultado[0][0].descricao,
                         'Institui o Dia de Carlos Magno')
        self.assertEqual(resultado[0][1][0].nome, 'Pierre')

    def test_ordenar_partidos(self):
        periodo = models.PeriodoCasaLegislativa(date(1989, 2, 2),
                                                date(1989, 10, 10))
        casa_legislativa = \
            models.CasaLegislativa.objects.get(nome_curto='conv')
        ordem = []
        ordem = ordenacao.ordenar_partidos(casa_legislativa, periodo)
        self.assertEqual(ordem[0].nome, 'Jacobinos')
        self.assertEqual(ordem[1].nome, 'Girondinos')
        self.assertEqual(ordem[2].nome, 'Monarquistas')

    def test_def_ordenar_votantes(self):
        proposicao = models.Proposicao.objects.first()
        resultado = ordenacao.ordenar_votantes(proposicao)
        parlamentar = Parlamentar.objects.filter(nome='Pierre')[0]
        primeiro = (parlamentar.partido, 1)
        self.assertEqual(resultado[parlamentar], primeiro)
