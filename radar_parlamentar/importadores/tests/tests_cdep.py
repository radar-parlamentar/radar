#!/usr/bin/python
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
from importadores import camara
from importadores.tests.mocks_cdep import mock_obter_proposicao,mock_listar_proposicoes, mock_obter_votacoes
import Queue
from mock import Mock
from modelagem import models
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
        verificador = camara.VerificadorDeProposicoesVotadas(props_queue, votadas_queue, False, camaraws = self.camaraws)
        verificador.verifica_se_tem_votacoes()

        props_queue.join() # aguarda até que a fila seja toda processada
        votadas = []        
        while not votadas_queue.empty():
            prop = votadas_queue.get()            
            votadas.append(prop)
            
        self.assertEquals(len(votadas), 1)
        self.assertEquals(votadas[0], prop_com_votacao)
        

class CamaraTest(TestCase):

    @classmethod
    def setUpClass(cls):
        # vamos importar apenas as votações das proposições em votadas_test.txt
        votadasParser = camara.ProposicoesParser(VOTADAS_FILE_PATH)
        votadas = votadasParser.parse()        
        importer = camara.ImportadorCamara(votadas)
        #dublando a camara
        camaraWS = camara.Camaraws()
        camaraWS.listar_proposicoes = Mock(side_effect=mock_listar_proposicoes)
        camaraWS.obter_proposicao_por_id = Mock(side_effect=mock_obter_proposicao)
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
        votadasParser = camara.ProposicoesParser(VOTADAS_FILE_PATH)
        votadas = votadasParser.parse()        
        importer = camara.ImportadorCamara(votadas)
        data = importer._converte_data('19/10/1999')

        prop_cod_flor = models.Proposicao.objects.get(id_prop=ID)
        self.assertEquals(prop_cod_flor.nome(), NOME)
        self.assertEquals(prop_cod_flor.situacao, 'Tranformada no(a) Lei Ordinária 12651/2012')
        self.assertEquals(prop_cod_flor.data_apresentacao.day, data.day)
        self.assertEquals(prop_cod_flor.data_apresentacao.month, data.month)
        self.assertEquals(prop_cod_flor.data_apresentacao.year, data.year)

    def test_votacoes_cod_florestal(self):
        votacoes = models.Votacao.objects.filter(proposicao__id_prop=ID)
        self.assertEquals(len(votacoes), 5)

        vot = votacoes[0]
        self.assertTrue('REQUERIMENTO DE RETIRADA DE PAUTA' in vot.descricao)

        importer = camara.ImportadorCamara(votacoes)
        data = importer._converte_data('24/5/2011', '20:52')
        vot = votacoes[1]
        self.assertEquals(vot.data.day, data.day)
        self.assertEquals(vot.data.month, data.month)
        self.assertEquals(vot.data.year, data.year)
        # vot.data está sem hora e minuto
#         self.assertEquals(vot.data.hour, data.hour)
#         self.assertEquals(vot.data.minute, data.minute)

    def test_votos_cod_florestal(self):
        votacao = models.Votacao.objects.filter(proposicao__id_prop=ID)[0]
        voto1 = [ v for v in votacao.votos() if v.legislatura.parlamentar.nome == 'Mara Gabrilli' ][0]
        voto2 = [ v for v in votacao.votos() if v.legislatura.parlamentar.nome == 'Carlos Roberto' ][0]
        self.assertEquals(voto1.opcao, models.SIM)
        self.assertEquals(voto2.opcao, models.NAO)
        self.assertEquals(voto1.legislatura.partido.nome, 'PSDB')
        self.assertEquals(voto2.legislatura.localidade, 'SP')





