# !/usr/bin/python
# coding=utf8

# Copyright (C) 2012, 2013, Leonardo Leite, Diego Rabatone, Eduardo Hideo
#
# This file is part of Radar Parlamentar.
#
# Radar Parlamentar is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Radar Parlamentar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Radar Parlamentar.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from django.test import TestCase
from importadores import cdep
from importadores.tests.mocks_cdep import mock_obter_proposicao
from importadores.tests.mocks_cdep import mock_listar_proposicoes
from importadores.tests.mocks_cdep import mock_obter_votacoes
from importadores.tests.mocks_cdep import mock_obter_proposicoes_votadas_plenario
from mock import Mock
from modelagem import models

# constantes relativas ao código florestal
# Alterar teste para que o mesmo utilize alguma proposicao retornada pela
# funcionalidade do Plenário.
# constantes relativas a emenda à consituição

ID = '17338'
ANO = '1999'
SIGLA = 'PL'
NUM = '1876'
NOME = 'PL 1876/1999'


ID_PLENARIO = '584279'
ANO_PLENARIO = '2013'
SIGLA_PLENARIO = 'REQ'
NUM_PLENARIO = '8196'

test_votadas = [[('17338', 'PL 1876/1999')]]


class ProposicoesParserTest(TestCase):

    def test_parse(self):
        votadasParser = cdep.ProposicoesParser(test_votadas)
        votadas = votadasParser.parse()
        codigo_florestal = {'id': ID, 'sigla': SIGLA, 'num': NUM, 'ano': ANO}
        self.assertTrue(codigo_florestal in votadas)


class SeparadorDeListaTest(TestCase):

    def test_separa_lista(self):

        lista = [1, 2, 3, 4, 5, 6]

        separador = cdep.SeparadorDeLista(1)
        listas = separador.separa_lista_em_varias_listas(lista)
        self.assertEquals(len(listas), 1)
        self.assertEquals(listas[0], lista)

        separador = cdep.SeparadorDeLista(2)
        listas = separador.separa_lista_em_varias_listas(lista)
        self.assertEquals(len(listas), 2)
        self.assertEquals(listas[0], [1, 2, 3])
        self.assertEquals(listas[1], [4, 5, 6])

        separador = cdep.SeparadorDeLista(3)
        listas = separador.separa_lista_em_varias_listas(lista)
        self.assertEquals(len(listas), 3)
        self.assertEquals(listas[0], [1, 2])
        self.assertEquals(listas[1], [3, 4])
        self.assertEquals(listas[2], [5, 6])

    def test_separa_lista_quando_nao_eh_multiplo(self):

        lista = [1, 2, 3, 4, 5, 6, 7]

        separador = cdep.SeparadorDeLista(3)
        listas = separador.separa_lista_em_varias_listas(lista)
        self.assertEquals(len(listas), 3)
        self.assertEquals(listas[0], [1, 2, 3])
        self.assertEquals(listas[1], [4, 5, 6])
        self.assertEquals(listas[2], [7])


class CamaraTest(TestCase):

    @classmethod
    def setUpClass(cls):
        # vamos importar apenas as votações das proposições em votadas_test.txt
        votadasParser = cdep.ProposicoesParser(test_votadas)
        votadas = votadasParser.parse()
        importer = cdep.ImportadorCamara(votadas)
        # dublando a camara
        camaraWS = cdep.Camaraws()
        camaraWS.listar_proposicoes = Mock(side_effect=mock_listar_proposicoes)
        camaraWS.obter_proposicao_por_id = Mock(
            side_effect=mock_obter_proposicao)
        camaraWS.obter_votacoes = Mock(side_effect=mock_obter_votacoes)
        importer.importar(camaraWS)

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)

    def test_casa_legislativa(self):
        camara = models.CasaLegislativa.objects.get(nome_curto='cdep')
        self.assertEquals(camara.nome, 'Câmara dos Deputados')

    def test_prop_cod_florestal(self):
        votadasParser = cdep.ProposicoesParser(test_votadas)
        votadas = votadasParser.parse()
        importer = cdep.ImportadorCamara(votadas)
        data = importer._converte_data('19/10/1999')
        prop_cod_flor = models.Proposicao.objects.get(id_prop=ID)
        self.assertEquals(prop_cod_flor.nome(), NOME)
        self.assertEquals(
            prop_cod_flor.situacao,
            'Tranformada no(a) Lei Ordinária 12651/2012')
        self.assertEquals(prop_cod_flor.data_apresentacao.day, data.day)
        self.assertEquals(prop_cod_flor.data_apresentacao.month, data.month)
        self.assertEquals(prop_cod_flor.data_apresentacao.year, data.year)

    def test_votacoes_cod_florestal(self):
        votacoes = models.Votacao.objects.filter(proposicao__id_prop=ID)
        self.assertEquals(len(votacoes), 5)

        vot = votacoes[0]
        self.assertTrue('REQUERIMENTO DE RETIRADA DE PAUTA' in vot.descricao)

        importer = cdep.ImportadorCamara(votacoes)
        data = importer._converte_data('24/5/2011')
        vot = votacoes[1]
        self.assertEquals(vot.data.day, data.day)
        self.assertEquals(vot.data.month, data.month)
        self.assertEquals(vot.data.year, data.year)

    def test_votos_cod_florestal(self):
        votacao = models.Votacao.objects.filter(proposicao__id_prop=ID)[0]
        voto1 = [
            v for v in votacao.votos() if v.legislatura.parlamentar.nome == 'Mara Gabrilli'][0]
        voto2 = [
            v for v in votacao.votos() if v.legislatura.parlamentar.nome == 'Carlos Roberto'][0]
        self.assertEquals(voto1.opcao, models.SIM)
        self.assertEquals(voto2.opcao, models.NAO)
        self.assertEquals(voto1.legislatura.partido.nome, 'PSDB')
        self.assertEquals(voto2.legislatura.localidade, 'SP')


class WsPlenarioTest(TestCase):

    def test_prop_in_xml(self):
        ano_min = 2013
        ano_max = 2013
        camaraWS = cdep.Camaraws()
        camaraWS.obter_proposicoes_votadas_plenario = Mock(
            side_effect=mock_obter_proposicoes_votadas_plenario)
        propFinder = cdep.ProposicoesFinder()
        zip_votadas = propFinder.find_props_disponiveis(
            ano_min, ano_max, camaraWS)
        prop_test = ('14245', 'PEC 3/1999')
        for x in range(0, len(zip_votadas)):
            self.assertTrue(prop_test in zip_votadas[x])

    def test_prop_in_dict(self):
        ano_min = 2013
        ano_max = 2013
        camaraWS = cdep.Camaraws()
        camaraWS.obter_proposicoes_votadas_plenario = Mock(
            side_effect=mock_obter_proposicoes_votadas_plenario)
        propFinder = cdep.ProposicoesFinder()
        zip_votadas = propFinder.find_props_disponiveis(
            ano_min, ano_max, camaraWS)
        propParser = cdep.ProposicoesParser(zip_votadas)
        dict_votadas = propParser.parse()
        prop_in_dict = {'id': ID_PLENARIO, 'sigla':
                        SIGLA_PLENARIO, 'num': NUM_PLENARIO, 'ano': ANO_PLENARIO}
        self.assertTrue(prop_in_dict in dict_votadas)
