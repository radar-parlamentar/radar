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

class CamaraTest(TestCase):
    """Testes do módulo camara"""

    def test_parse_votadas(self):

        importer = camara.ImportadorCamara()
        props_votadas = importer._parse_votadas()
        codigo_florestal =  {'ano': '1999', 'id': '17338', 'num': '1876', 'tipo': 'PL'}
        self.assertTrue(codigo_florestal in props_votadas)

    def test_obter_proposicao(self):

        camaraws = camara.Camaraws()
        codigo_florestal_xml = camaraws.obter_proposicao('17338')
        nome = codigo_florestal_xml.find('nomeProposicao').text
        self.assertEquals(nome, 'PL 1876/1999')
        
    def test_obter_votacoes(self):

        camaraws = camara.Camaraws()
        codigo_florestal_xml = camaraws.obter_votacoes('pl', '1876', '1999')
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


    

