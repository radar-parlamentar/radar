from __future__ import unicode_literals
from django.test import TestCase
import os
import xml.etree.ElementTree as etree
import mock

from importadores import sen, sen_indexacao
from modelagem import models

XML_TEST = os.path.join(sen.MODULE_DIR, 'dados/senado/ListaVotacoesTest.xml')


class GeradorSenadoTest(TestCase):

    def test_geracao_da_casa(self):
        casa = sen.CasaLegislativaGerador().gera_senado()
        self.assertEquals(casa.nome_curto, 'sen')

    def test_recupera_a_casa_existente(self):
        casa1 = sen.CasaLegislativaGerador().gera_senado()
        casa2 = sen.CasaLegislativaGerador().gera_senado()
        self.assertEquals(casa1.pk, casa2.pk)

class ImportadorSenadoTest(TestCase):

    def setUp(self):
        casa = sen.CasaLegislativaGerador().gera_senado()
        self.importer = sen.ImportadorVotacoesSenado()
        self.importer._xml_file_names = mock.Mock(return_value=[XML_TEST])
        self.importer.importar_votacoes()

    def test_votacao_importada(self):
        votacao = models.Votacao.objects.get(pk=1)
        self.assertEquals(votacao.resultado, "R")

    def test_parlamentar_importado(self):
        parlamentar = models.Parlamentar.objects.get(nome='Jader Barbalho')
        self.assertTrue(parlamentar)
        self.assertEquals(parlamentar.genero, 'M')
        self.assertEquals(parlamentar.localidade, 'PA')
        partido = models.Partido.objects.get(nome='PMDB')
        self.assertTrue(partido)
        self.assertEquals(parlamentar.partido.nome, 'PMDB')

class IndexacaoSenadoTest(TestCase):

    def setUp(self):
        casa = sen.CasaLegislativaGerador().gera_senado()
        self.importer = sen.ImportadorVotacoesSenado()
        self.importer._xml_file_names = mock.Mock(return_value=[XML_TEST])
        self.importer.importar_votacoes()
        sen_indexacao.indexar_proposicoes()

    def test_proposicoes_importadas(self):
        proposicao = models.Proposicao.objects.get(pk=1)
        self.assertTrue(proposicao)
        self.assertEquals(proposicao.ano, '2015')
        self.assertEquals(proposicao.sigla, 'PLS')
        self.assertEquals(proposicao.numero, '00131')

