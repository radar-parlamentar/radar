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


from django.test import TestCase
from importadores import cdep
from modelagem import models
import os
import xml.etree.ElementTree as etree
from mock import Mock
from importadores.tests.mocks_cdep \
    import mock_obter_proposicoes_votadas_plenario, mock_obter_proposicao, \
    mock_obter_votacoes

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


class ImportadorCamaraTest(TestCase):

    @classmethod
    def setUpClass(cls):
        # vamos importar apenas o código florestal
        dic_votadas = [{'id': '17338', 'sigla': 'PL', 'num': '1876', 'ano': '1999'}]
        camaraws = cdep.Camaraws()
        camaraws.obter_proposicao_por_id = Mock(
            side_effect=mock_obter_proposicao)
        camaraws.obter_votacoes = Mock(
            side_effect=mock_obter_votacoes)

        importer = cdep.ImportadorCamara(camaraws)
        importer.importar(dic_votadas)
        importer.importar(dic_votadas) # chamando duas vezes pra testar idempotência

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)

    def test_casa_legislativa(self):
        camara = models.CasaLegislativa.objects.get(nome_curto='cdep')
        self.assertEqual(camara.nome, 'Câmara dos Deputados')

    def test_prop_cod_florestal(self):
        data = cdep._converte_data('19/10/1999')
        prop_cod_flor = models.Proposicao.objects.get(id_prop=ID_FLORESTAL)
        self.assertEqual(prop_cod_flor.nome(), NOME_FLORESTAL)
        self.assertEqual(prop_cod_flor.situacao,
                          'Tranformada no(a) Lei Ordinária 12651/2012')
        self.assertEqual(prop_cod_flor.data_apresentacao.day, data.day)
        self.assertEqual(prop_cod_flor.data_apresentacao.month, data.month)
        self.assertEqual(prop_cod_flor.data_apresentacao.year, data.year)

    def test_votacoes_cod_florestal(self):
        votacoes = models.Votacao.objects.filter(
            proposicao__id_prop=ID_FLORESTAL)
        self.assertEqual(len(votacoes), 5)

        vot = votacoes[0]
        self.assertTrue('REQUERIMENTO DE RETIRADA DE PAUTA' in vot.descricao)

        data = cdep._converte_data('24/5/2011')
        vot = votacoes[1]
        self.assertEqual(vot.data.day, data.day)
        self.assertEqual(vot.data.month, data.month)
        self.assertEqual(vot.data.year, data.year)

    def test_votos_cod_florestal(self):
        votacao = models.Votacao.objects.filter(
            proposicao__id_prop=ID_FLORESTAL)[0]
        voto1 = [
            v for v in votacao.votos()
            if v.parlamentar.nome == 'Mara Gabrilli'][0]
        voto2 = [
            v for v in votacao.votos()
            if v.parlamentar.nome == 'Carlos Roberto'][0]
        self.assertEqual(voto1.opcao, models.SIM)
        self.assertEqual(voto2.opcao, models.NAO)
        self.assertEqual(voto1.parlamentar.partido.nome, 'PSDB')
        self.assertEqual(voto2.parlamentar.localidade, 'SP')

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

