# coding=utf8

# Copyright (C) 2012, Leonardo Leite
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
from analises import filtro
from modelagem import models


# tests AnalisePeriodo

# tests AnaliseTemporal

# Tests JsonAnaliseGenerator

# Testes filtro

class Filtro_ProposicaoTest(TestCase):
    
    def test_filtro_proposicao(self):
        obj_filtro = filtro.Filtro_Proposicao() 
        obj_filtro1 = filtro.Filtro_Proposicao()
        palavra_proposicao = models.Proposicao()
        palavra_proposicao1 = models.Proposicao()
        palavra_proposicao.sigla = 'PTB'
        sigla = 'PTB'
        palavra_proposicao.descricao = 'Discussao da legalizacao do aborto'
        palavra_proposicao1.descricao = 'Estudo de caso para viabilidade do VLP'
        palavra_proposicao1.sigla = 'PM'
        sigla1 = 'PM'
        palavra_proposicao.save()
        palavra_proposicao1.save()
        
        self.assertTrue(palavra_proposicao.descricao in obj_filtro.filtra_proposicao([sigla],['aborto']))
        self.assertTrue(palavra_proposicao1.descricao in obj_filtro1.filtra_proposicao([sigla1],['viabilidade']))
            
    
    def test_filtro_proposicao1(self):
        palavra_proposicao = models.Proposicao()
        obj_filtro = filtro.Filtro_Proposicao() 
        obj_filtro1 = filtro.Filtro_Proposicao()
        palavra_proposicao1 = models.Proposicao()
        palavra_proposicao.sigla = 'PTB'
        sigla = 'PTB'
        palavra_proposicao.descricao = 'Discussao da legalizacao do aborto'
        palavra_proposicao1.descricao = 'Estudo de caso para viabilidade do VLP'
        palavra_proposicao1.sigla = 'PM'
        sigla1 = 'PM'
        palavra_proposicao.save()
        palavra_proposicao1.save()
        
        self.assertFalse(palavra_proposicao.descricao in obj_filtro.filtra_proposicao([sigla],['musica']))
        self.assertFalse(palavra_proposicao1.descricao in obj_filtro1.filtra_proposicao([sigla1],['futebol']))


class TemasTest(TestCase):

    dici = None

    def setUp(self):
        self.dici = filtro.Temas.get_temas_padrao()
        self.dici.inserir_sinonimo("testing","test")

    def test_criacao_dicionario(self):
        self.assertTrue(len(self.dici.dicionario.items()) > 0)
    
    def test_insercao_palavra_nova(self):
        self.dici.inserir_sinonimo("teste", "test")
        self.assertTrue(self.dici.dicionario.has_key("teste"))

    def test_insercao_sinonimo_novo(self):
        self.dici.inserir_sinonimo("testing", "teste")
        self.assertEquals(2, len(self.dici.dicionario["testing"]))

    def test_insercao_erro(self):
        with self.assertRaises(ValueError):
            self.dici.inserir_sinonimo("testing", None)
            
        with self.assertRaises(ValueError):
            self.dici.inserir_sinonimo(None, "dinossauro")

    def test_recuperacao_com_uma_chave(self):
        self.dici.inserir_sinonimo("testing","assert")
        palavras = self.dici.recuperar_palavras_por_sinonimo("assert")
        self.assertEquals(1, len(palavras))

        self.dici.inserir_sinonimo("another","assert")
        palavras = self.dici.recuperar_palavras_por_sinonimo("assert")
        self.assertEquals(2, len(palavras))

        palavras = self.dici.recuperar_palavras_por_sinonimo("sandslash")
        self.assertEquals(0, len(palavras))

    def test_recuperacao_erro(self):
        with self.assertRaises(ValueError):
            self.dici.recuperar_palavras_por_sinonimo(None)


        