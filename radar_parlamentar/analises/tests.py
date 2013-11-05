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
from analises import analise
from analises import grafico
from modelagem import models
from models import AnalisePeriodo, AnaliseTemporal
from importadores import convencao
from random import random
import numpy
import json

# tests AnalisePeriodo

# tests AnaliseTemporal

# Tests JsonAnaliseGenerator

class JsonAnaliseGeneratorTest(TestCase):
    # TODO some complicated calculus performed in JsonAnaliseGeneratorTest
    # should be done by a new class, possibly in grafico module.
    # This test is not complete, it could test more json elements.

    @classmethod
    def setUpClass(cls):
        cls.importer = convencao.ImportadorConvencao()
        cls.importer.importar()
            
    def setUp(self):
        
        self.casa = models.CasaLegislativa.objects.get(nome_curto='conv')
        
        self.analiseTemporal = AnaliseTemporal()
        self.analiseTemporal.casa_legislativa = self.casa
        self.analiseTemporal.periodicidade = models.BIENIO
        self.analiseTemporal.area_total = 1
        self.analiseTemporal.analises_periodo = []
        
        ap1 = AnalisePeriodo()
        periodos = models.CasaLegislativa.periodos(self.casa, models.BIENIO, 0)
        ap1.casa_legislativa = None
        ap1.periodo = periodos[0]
        ap1.partidos = [ p for p in JsonAnaliseGeneratorTest.importer.partidos ]
        ap1.votacoes = []
        ap1.num_votacoes = 0
        ap1.tamanhos_partidos = {convencao.JACOBINOS : 3, convencao.GIRONDINOS : 3, convencao.MONARQUISTAS : 3} 
        ap1.soma_dos_tamanhos_dos_partidos = 3*3
        ap1.pca = PCAStub()
        ap1.coordenadas_partidos = {}
        ap1.coordenadas_partidos[convencao.JACOBINOS] = [-0.4,0.3]
        ap1.coordenadas_partidos[convencao.GIRONDINOS] = [0.9,-0.3]
        ap1.coordenadas_partidos[convencao.MONARQUISTAS] = [0.2,0.1]
        ap1.legislaturas_por_partido = JsonAnaliseGeneratorTest.importer.legs
        ap1.coordenadas_legislaturas = {} # legislatura.id => [x,y]
        for p, legs in ap1.legislaturas_por_partido.items():
            for leg in legs:
                ap1.coordenadas_legislaturas[leg.id] = [random(), random()] 
        self.analiseTemporal.analises_periodo.append(ap1)

    def test_json(self):
        gen = grafico.JsonAnaliseGenerator(self.analiseTemporal)
        generated_json = gen.get_json()
        dict_analise = json.loads(generated_json)
        dict_casa = dict_analise['geral']['CasaLegislativa']
        self.assertEquals(dict_casa['nome_curto'], self.casa.nome_curto)  
        list_periodos = dict_analise['periodos']
        self.assertEquals(len(list_periodos), 1)
        dict_periodo = list_periodos[0]
        self.assertTrue('1989' in dict_periodo['nome'])
        list_partidos = dict_analise['partidos']
        self.assertEquals(len(list_partidos), 3)
        dict_partido = list_partidos[0]
        toutes_les_parties = [convencao.JACOBINOS, convencao.GIRONDINOS, convencao.MONARQUISTAS]
        self.assertTrue(dict_partido['nome'] in toutes_les_parties)
        list_tamanhos = dict_partido['t']
        self.assertEquals(list_tamanhos[0], 3)
        list_parlamentares = dict_partido['parlamentares']
        self.assertEquals(len(list_parlamentares), 3)
        dict_parlamentar = list_parlamentares[0] 
        list_xs = dict_parlamentar['x']
        x = list_xs[0]
        self.assertTrue(x >= 0 and x <= 100)
        
class PCAStub:
    # TODO self.Vt should be properly stubbed
    
    def __init__(self):
        self.eigen = numpy.zeros(4)
        self.eigen[0] = 0.6
        self.eigen[1] = 0.3
        self.eigen[2] = 0.05
        self.eigen[3] = 0.05
        self.Vt = None


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


        