# coding=utf8

# Copyright (C) 2015, Vanessa Soares e Thaiane Braga
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

from modelagem.models import Proposicao
from modelagem.models import Parlamentar
from analises.genero import Genero


class GeneroTest(TestCase):

    def setUp(self):
        self.parlamentar = Parlamentar(nome='Ana')
        self.proposicao = Proposicao(autor_principal='Ana', indexacao='mulher')
        self.id_casa_legislativa = 1
        self.genero = Genero()

    def test_definir_palavra(self):
        # temas_frequencia_mulher = self.genero.definir_palavras('F')
        self.assertEquals('Ana', self.parlamentar.nome)
        self.assertEquals('Ana', self.proposicao.autor_principal)
        self.assertEquals((u'mulher'), self.proposicao.indexacao)

    def test_organiza_lista_palavras(self):
        self.dicionario_palavras = {"Saude":2, "Educacao":1, "Transporte":26}
        self.assertEquals(self.genero.organiza_lista_palavras(self.dicionario_palavras), [(u'Transporte', 26), (u'Saude', 2), (u'Educacao', 1)] )

    def test_define_chaves_dicionario(self):
        self.dicionario_ordenado = ["Saude", "Saude", "Educacao"]
        self.assertEquals(self.genero.define_chaves_dicionario(self.dicionario_ordenado), [("Saude",2), ("Educacao",1)])

    def test_agrupa_palavras(self):
        self.assertEquals(self.genero.agrupa_palavras(self.genero, self.id_casa_legislativa), [])

    def test_get_casas_legislativas_com_genero(self):
        self.assertEquals(self.genero.get_casas_legislativas_com_genero(), [])
