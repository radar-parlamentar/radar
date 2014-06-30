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

# constantes relativas ao código florestal
ID = '17338'
SIGLA = 'PL'
NUM = '1876'
ANO = '1999'
NOME = 'PL 1876/1999'


class CamarawsTest(TestCase):

    """Realiza testes envolvendo os web services da câmara"""

    def setUp(self):
        self.camaraws = cdep.Camaraws()

    def test_obter_proposicao(self):
        codigo_florestal_xml = self.camaraws.obter_proposicao_por_id(ID)
        nome = codigo_florestal_xml.find('nomeProposicao').text
        self.assertEquals(nome, NOME)

    def test_obter_votacoes(self):
        codigo_florestal_xml = self.camaraws.obter_votacoes(SIGLA, NUM, ANO)
        data_vot_encontrada = codigo_florestal_xml.find(
            'Votacoes').find('Votacao').get('Data')
        self.assertEquals(data_vot_encontrada, '11/5/2011')

    def test_listar_proposicoes(self):
        pecs_2011_xml = self.camaraws.listar_proposicoes('PEC', '2011')
        pecs_elements = pecs_2011_xml.findall('proposicao')
        self.assertEquals(len(pecs_elements), 135)
        # 135 obtido por conferência manual com:
        # http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoes?sigla=PEC&numero=&ano=2011&datApresentacaoIni=&datApresentacaoFim=&autor=&parteNomeAutor=&siglaPartidoAutor=&siglaUFAutor=&generoAutor=&codEstado=&codOrgaoEstado=&emTramitacao=

    def test_prop_nao_existe(self):
        id_que_nao_existe = 'id_que_nao_existe'
        caught = False
        try:
            self.camaraws.obter_proposicao_por_id(id_que_nao_existe)
        except ValueError as e:
            self.assertEquals(
                e.message, 'Proposicao %s nao encontrada' % id_que_nao_existe)
            caught = True
        self.assertTrue(caught)

    def test_votacoes_nao_existe(self):
        sigla = 'PCC'
        num = '1500'
        ano = '1876'
        caught = False
        try:
            self.camaraws.obter_votacoes(sigla, num, ano)
        except ValueError as e:
            self.assertEquals(
                e.message, 'Votacoes da proposicao %s %s/%s nao encontrada'
                % (sigla, num, ano))
            caught = True
        self.assertTrue(caught)

    def test_listar_proposicoes_que_nao_existem(self):
        sigla = 'PEC'
        ano = '3013'
        try:
            self.camaraws.listar_proposicoes(sigla, ano)
        except ValueError as e:
            self.assertEquals(
                e.message, 'Proposicoes nao encontradas para sigla=%s&ano=%s'
                % (sigla, ano))
            caught = True
        self.assertTrue(caught)

    def test_listar_siglas(self):
        siglas = self.camaraws.listar_siglas()
        self.assertTrue('PL' in siglas)
        self.assertTrue('PEC' in siglas)
        self.assertTrue('MPV' in siglas)

    def test_votacao_presente_plenario(self):
        ANO_PLENARIO = 2013
        NOME_PLENARIO = 'REQ 8196/2013'
        NOT_NOME_PLENARIO = 'DAVID 1309/1992'
        etree_plenario = self.camaraws.obter_proposicoes_votadas_plenario(
            ANO_PLENARIO)
        nome_prop_list = []
        for nomeProp in etree_plenario:
            nome_prop_list.append(nomeProp.find('nomeProposicao').text)
        self.assertTrue(NOME_PLENARIO in nome_prop_list)
        self.assertFalse(NOT_NOME_PLENARIO in nome_prop_list)
