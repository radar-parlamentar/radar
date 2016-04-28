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
from modelagem import models
import os
import xml.etree.ElementTree as etree
from mock import Mock
from importadores.tests.mocks_cdep \
    import mock_obter_proposicoes_votadas_plenario


MOCK_PATH = os.path.join(cdep.RESOURCES_FOLDER, 'mocks')
PROPOSICAO_XML_COD_FLORESTAL = os.path.join(MOCK_PATH, 'proposicao_17338.xml')
VOTACOES_XML_COD_FLORESTAL = os.path.join(MOCK_PATH, 'votacoes_PL18761999.xml')

ID_FLORESTAL = '17338'
NOME_FLORESTAL = 'PL 1876/1999'


class ProposicoesFinderTest(TestCase):

    def test_prop_in_xml(self):
        ano_min = 2013
        ano_max = 2013
        camaraws = cdep.Camaraws()
        camaraws.obter_proposicoes_votadas_plenario = Mock(
            side_effect=mock_obter_proposicoes_votadas_plenario)
        proposicoesFinder = cdep.ProposicoesFinder()
        dic_votadas = proposicoesFinder.find_props_disponiveis(
            ano_min, ano_max, camaraws)
        proposicao = {'id': '14245', 'sigla': 'PEC', 'num': '3', 'ano': '1999'}
        self.assertTrue(proposicao in dic_votadas)


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


class ImportadorCamaraTest(TestCase):

    @classmethod
    def setUpClass(cls):
        # vamos importar apenas o código florestal
        with open(PROPOSICAO_XML_COD_FLORESTAL, "r") as f:
            prop_xml_str = f.read()
        with open(VOTACOES_XML_COD_FLORESTAL, "r") as f:
            vots_xml_str = f.read()
        prop_xml = etree.fromstring(prop_xml_str)
        vots_xml = etree.fromstring(vots_xml_str)
        importer = cdep.ImportadorCamara()
        importer.importar({prop_xml: vots_xml})

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)

    def test_casa_legislativa(self):
        camara = models.CasaLegislativa.objects.get(nome_curto='cdep')
        self.assertEquals(camara.nome, 'Câmara dos Deputados')

    def test_prop_cod_florestal(self):
        data = cdep._converte_data('19/10/1999')
        prop_cod_flor = models.Proposicao.objects.get(id_prop=ID_FLORESTAL)
        self.assertEquals(prop_cod_flor.nome(), NOME_FLORESTAL)
        self.assertEquals(prop_cod_flor.situacao,
                          'Tranformada no(a) Lei Ordinária 12651/2012')
        self.assertEquals(prop_cod_flor.data_apresentacao.day, data.day)
        self.assertEquals(prop_cod_flor.data_apresentacao.month, data.month)
        self.assertEquals(prop_cod_flor.data_apresentacao.year, data.year)

    def test_votacoes_cod_florestal(self):
        votacoes = models.Votacao.objects.filter(
            proposicao__id_prop=ID_FLORESTAL)
        self.assertEquals(len(votacoes), 5)

        vot = votacoes[0]
        self.assertTrue('REQUERIMENTO DE RETIRADA DE PAUTA' in vot.descricao)

        data = cdep._converte_data('24/5/2011')
        vot = votacoes[1]
        self.assertEquals(vot.data.day, data.day)
        self.assertEquals(vot.data.month, data.month)
        self.assertEquals(vot.data.year, data.year)

    def test_votos_cod_florestal(self):
        votacao = models.Votacao.objects.filter(
            proposicao__id_prop=ID_FLORESTAL)[0]
        voto1 = [
            v for v in votacao.votos()
            if v.parlamentar.nome == 'Mara Gabrilli'][0]
        voto2 = [
            v for v in votacao.votos()
            if v.parlamentar.nome == 'Carlos Roberto'][0]
        self.assertEquals(voto1.opcao, models.SIM)
        self.assertEquals(voto2.opcao, models.NAO)
        self.assertEquals(voto1.parlamentar.partido.nome, 'PSDB')
        self.assertEquals(voto2.parlamentar.localidade, 'SP')

    def test_nao_tem_parlamentares_repetidos(self):
        todos = models.Parlamentar.objects.filter(
            casa_legislativa__nome_curto='cdep')
        self.assertTrue(todos.count() > 100)
        repetidos = []
        for p in todos:
            count_p = models.Parlamentar.objects.filter(
                casa_legislativa__nome_curto='cdep', nome=p.nome,
                partido__numero=p.partido.numero,
                localidade=p.localidade).count()
            if count_p > 1:
                repetidos.append(p)
        self.assertTrue(len(repetidos) == 0)
