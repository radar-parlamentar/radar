#!/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Leonardo Leite
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from django.test import TestCase
from importadores import camara
from modelagem import models

# constantes relativas ao código florestal
ID = '17338'
SIGLA = 'PL'
NUM = '1876'
ANO = '1999'
NOME = 'PL 1876/1999'


class CamaraTest(TestCase):
    """Testes do módulo camara"""

    @classmethod
    def setUpClass(cls):
        # vamos importar apenas as votações das proposições em votadas_test.txt
        camara.VOTADAS_FILE_PATH = camara.RESOURCES_FOLDER + 'votadas_test.txt'
        importer = camara.ImportadorCamara()
        importer.importar()

    def test_parse_votadas(self):

        importer = camara.ImportadorCamara()
        codigo_florestal =  {'ano': ANO, 'id': ID, 'num': NUM, 'sigla': SIGLA}
        self.assertTrue(codigo_florestal in importer.votadas_ids)

    def test_obter_proposicao(self):

        camaraws = camara.Camaraws()
        codigo_florestal_xml = camaraws.obter_proposicao(ID)
        nome = codigo_florestal_xml.find('nomeProposicao').text
        self.assertEquals(nome, NOME)
        
    def test_obter_votacoes(self):

        camaraws = camara.Camaraws()
        codigo_florestal_xml = camaraws.obter_votacoes(SIGLA, NUM, ANO)
        data_vot_encontrada = codigo_florestal_xml.find('Votacoes').find('Votacao').get('Data')
        self.assertEquals(data_vot_encontrada, '11/5/2011')

    def test_prop_nao_existe(self):

        id_que_nao_existe = 'id_que_nao_existe'
        camaraws = camara.Camaraws()
        caught = False
        try:        
            camaraws.obter_proposicao(id_que_nao_existe)
        except ValueError as e:
            self.assertEquals(e.message, 'Proposição %s não encontrada' % id_que_nao_existe)
            caught = True
        self.assertTrue(caught)

    def test_votacoes_nao_existe(self):

        sigla = 'PCC'
        num = '1500'
        ano = '1876'
        camaraws = camara.Camaraws()
        caught = False
        try:        
            camaraws.obter_votacoes(sigla, num, ano)
        except ValueError as e:
            self.assertEquals(e.message, 'Votações da proposição %s %s/%s não encontrada' % (sigla, num, ano))
            caught = True
        self.assertTrue(caught)

    def test_casa_legislativa(self):

        camara = models.CasaLegislativa.objects.get(nome_curto='camara')
        self.assertEquals(camara.nome, 'Câmara dos Deputados')

    def test_prop_cod_florestal(self):

        importer = camara.ImportadorCamara()
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

        importer = camara.ImportadorCamara()
        data = importer._converte_data('24/5/2011', '20:52')
        vot = votacoes[1]
        self.assertEquals(vot.data.day, data.day)
        self.assertEquals(vot.data.month, data.month)
        self.assertEquals(vot.data.year, data.year)
        # vot.data está sem hora e minuto
#        self.assertEquals(vot.data.hour, data.hour)
#        self.assertEquals(vot.data.minute, data.minute)

    def test_votos_cod_florestal(self):

        votacao = models.Votacao.objects.filter(proposicao__id_prop=ID)[0]
        voto1 = [ v for v in votacao.votos.all() if v.legislatura.parlamentar.nome == 'Mara Gabrilli' ][0]
        voto2 = [ v for v in votacao.votos.all() if v.legislatura.parlamentar.nome == 'Carlos Roberto' ][0]
        self.assertEquals(voto1.opcao, models.SIM)
        self.assertEquals(voto2.opcao, models.NAO)
        self.assertEquals(voto1.legislatura.partido.nome, 'PSDB')
        self.assertEquals(voto2.legislatura.localidade, 'SP')

        


    

