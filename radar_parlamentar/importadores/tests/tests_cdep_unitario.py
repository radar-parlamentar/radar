#!/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Diego Rabatone
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
from importadores import camara
from importadores.tests.mocks_cdep import mock_obter_proposicao,mock_listar_proposicoes, mock_obter_votacoes
import Queue
from mock import Mock
import os

# constantes relativas ao código florestal
ID = '17338'
SIGLA = 'PL'
NUM = '1876'
ANO = '1999'
NOME = 'PL 1876/1999'

VOTADAS_FILE_PATH = camara.RESOURCES_FOLDER + 'votadas_test.txt'

class ProposicoesParserTest(TestCase):

    def test_parse(self):
        VOTADAS_FILE_PATH = camara.RESOURCES_FOLDER + 'votadas_test.txt'
        votadasParser = camara.ProposicoesParser(VOTADAS_FILE_PATH)
        votadas = votadasParser.parse()        
        codigo_florestal =  {'ano': ANO, 'id': ID, 'num': NUM, 'sigla': SIGLA}
        self.assertTrue(codigo_florestal in votadas)

class SeparadorDeListaTest(TestCase):
    
    def test_separa_lista(self):

        lista = [1, 2, 3, 4, 5, 6]
        
        separador = camara.SeparadorDeLista(1)
        listas = separador.separa_lista_em_varias_listas(lista)
        self.assertEquals(len(listas), 1)
        self.assertEquals(listas[0], lista)

        separador = camara.SeparadorDeLista(2)
        listas = separador.separa_lista_em_varias_listas(lista)
        self.assertEquals(len(listas), 2)
        self.assertEquals(listas[0], [1, 2, 3])
        self.assertEquals(listas[1], [4, 5, 6])

        separador = camara.SeparadorDeLista(3)
        listas = separador.separa_lista_em_varias_listas(lista)
        self.assertEquals(len(listas), 3)
        self.assertEquals(listas[0], [1, 2])
        self.assertEquals(listas[1], [3, 4])
        self.assertEquals(listas[2], [5, 6])

    def test_separa_lista_quando_nao_eh_multiplo(self):

        lista = [1, 2, 3, 4, 5, 6, 7]
        
        separador = camara.SeparadorDeLista(3)
        listas = separador.separa_lista_em_varias_listas(lista)
        self.assertEquals(len(listas), 3)
        self.assertEquals(listas[0], [1, 2, 3])
        self.assertEquals(listas[1], [4, 5, 6])
        self.assertEquals(listas[2], [7])

class ProposicoesFinderTest(TestCase):
    
    def setUp(self):
        #dublando a camaraws
        self.camaraws = camara.Camaraws()
        self.camaraws.listar_proposicoes = Mock(side_effect=mock_listar_proposicoes)
        self.camaraws.obter_proposicao = Mock(side_effect=mock_obter_proposicao)
        self.camaraws.obter_votacoes = Mock(side_effect=mock_obter_votacoes)

    def test_find_props_existem(self):

        ANO_MIN = 2012
        ANO_MAX = 2012
        IDS_QUE_EXISTEM = ['564446', '564313', '564126'] # proposições de 2012
        IDS_QUE_NAO_EXISTEM = ['382651', '382650'] # proposições de 2007
        FILE_NAME = 'ids_que_existem_test.txt'

        finder = camara.ProposicoesFinder(False) # False to verbose
        ids = finder.find_props_que_existem(ANO_MIN, ANO_MAX, FILE_NAME,camaraws=self.camaraws)

        for idp in IDS_QUE_EXISTEM:
            self.assertTrue(idp in ids)

        for idp in IDS_QUE_NAO_EXISTEM:
            self.assertFalse(idp in ids)

        os.system('rm %s' % FILE_NAME)


class VerificadorDeProposicoesTest(TestCase):
    def setUp(self):
        #dublando a camaraws
        self.camaraws = camara.Camaraws()
        self.camaraws.obter_votacoes = Mock(side_effect=mock_obter_votacoes)

    def test_verifica_se_tem_votacoes(self):
        
        prop_com_votacao = {'id': '17338', 'sigla': 'PL', 'num': '1876', 'ano': '1999'}
        prop_sem_votacao = {'id': '192074', 'sigla': 'PL', 'num': '1433', 'ano': '1988'}

        props_queue = Queue.Queue()
        props_queue.put(prop_com_votacao)
        props_queue.put(prop_sem_votacao)
        
        votadas_queue = Queue.Queue()    
        verificador = camara.VerificadorDeProposicoes( props_queue, votadas_queue, False, camaraws = self.camaraws)
        verificador.verifica_se_tem_votacoes()

        props_queue.join() # aguarda até que a fila seja toda processada
        votadas = []        
        while not votadas_queue.empty():
            prop = votadas_queue.get()            
            votadas.append(prop)
            
        self.assertEquals(len(votadas), 1)
        self.assertEquals(votadas[0], prop_com_votacao)

