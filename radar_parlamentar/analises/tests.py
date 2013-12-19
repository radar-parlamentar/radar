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

from django.utils.dateparse import parse_datetime

from analises import filtro
from analises import analise
from analises import grafico
from modelagem import models
from modelagem import utils
from models import AnalisePeriodo, AnaliseTemporal
from importadores import convencao
from random import random
import numpy
import json
from datetime import date

class AnalisadorPeriodoTest(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.importer = convencao.ImportadorConvencao()
        cls.importer.importar()

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)
        
    def setUp(self):
        self.casa_legislativa = models.CasaLegislativa.objects.get(nome_curto='conv')
        self.partidos = AnalisadorPeriodoTest.importer.partidos
        self.votacoes = models.Votacao.objects.filter(proposicao__casa_legislativa__nome_curto='conv')
        self.legislaturas = models.Legislatura.objects.filter(casa_legislativa__nome_curto='conv').distinct()
        for partido in self.partidos:
            if partido.nome == convencao.GIRONDINOS:
                self.girondinos = partido
            if partido.nome == convencao.JACOBINOS:
                self.jacobinos = partido
            if partido.nome == convencao.MONARQUISTAS:
                self.monarquistas = partido
        
    def test_coordenadas_partidos(self):
        periodo = models.PeriodoCasaLegislativa(date(1989,02,02), date(1989,10,10))
        analisador = analise.AnalisadorPeriodo(self.casa_legislativa, periodo)
        analise_periodo = analisador.analisa()
        coordenadas = analise_periodo.coordenadas_partidos
        self.assertAlmostEqual(coordenadas[self.girondinos][0], -0.152, 2)
        self.assertAlmostEqual(coordenadas[self.girondinos][1], -0.261, 2)
        self.assertAlmostEqual(coordenadas[self.jacobinos][0], -0.287, 2)
        self.assertAlmostEqual(coordenadas[self.jacobinos][1], 0.181, 2)
        self.assertAlmostEqual(coordenadas[self.monarquistas][0], 0.440, 2)
        self.assertAlmostEqual(coordenadas[self.monarquistas][1], 0.079, 2)
        
        
# tests AnalisadorTemporal
# ......

class AnalisadorTemporalTest(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.importer = convencao.ImportadorConvencao()
        cls.importer.importar()

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)
        
    def setUp(self):
        self.casa_legislativa = models.CasaLegislativa.objects.get(nome_curto='conv')
        self.partidos = AnalisadorTemporalTest.importer.partidos
        self.votacoes = models.Votacao.objects.filter(proposicao__casa_legislativa__nome_curto='conv')
        self.legislaturas = models.Legislatura.objects.filter(casa_legislativa__nome_curto='conv').distinct()
        for partido in self.partidos:
            if partido.nome == convencao.GIRONDINOS:
                self.girondinos = partido
            if partido.nome == convencao.JACOBINOS:
                self.jacobinos = partido
            if partido.nome == convencao.MONARQUISTAS:
                self.monarquistas = partido        
        
    def test_analisador_temporal(self):
        analisador_temporal = analise.AnalisadorTemporal(self.casa_legislativa, models.SEMESTRE)
        analise_temporal = analisador_temporal.get_analise_temporal()
        analises = analise_temporal.analises_periodo
        self.assertEqual(len(analises), 2)
        # primeiro semestre
        coordenadas = analises[0].coordenadas_partidos
        self.assertAlmostEqual(coordenadas[self.girondinos][0], -0.11788123, 4)
        self.assertAlmostEqual(coordenadas[self.girondinos][1], -0.29647299, 4)
        self.assertAlmostEqual(coordenadas[self.jacobinos][0], -0.30596818, 4)
        self.assertAlmostEqual(coordenadas[self.jacobinos][1], 0.19860293, 4)
        self.assertAlmostEqual(coordenadas[self.monarquistas][0], 0.42384941, 4)
        self.assertAlmostEqual(coordenadas[self.monarquistas][1], 0.09787006, 4)
        # segundo semestre
        coordenadas = analises[0].coordenadas_partidos
        self.assertAlmostEqual(coordenadas[self.girondinos][0], -0.11788123, 4)
        self.assertAlmostEqual(coordenadas[self.girondinos][1], -0.29647299, 4)
        self.assertAlmostEqual(coordenadas[self.jacobinos][0], -0.30596818, 4)
        self.assertAlmostEqual(coordenadas[self.jacobinos][1], 0.19860293, 4)
        self.assertAlmostEqual(coordenadas[self.monarquistas][0],  0.42384941, 4)
        self.assertAlmostEqual(coordenadas[self.monarquistas][1], 0.09787006, 4)                

class FiltroVotacaoTest(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.importer = convencao.ImportadorConvencao()
        cls.importer.importar()

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)

    def test_recupera_proposicoes(self):
        casa_legislativa = models.CasaLegislativa()
        casa_legislativa.id = 1

        filtro_votacao = filtro.FiltroVotacao()
        proposicoes = filtro_votacao._recupera_proposicoes(casa_legislativa)
        self.assertEquals(9, len(proposicoes))

    def test_recupera_votacoes_da_proposicao(self):
        proposicao = models.Proposicao()
        proposicao.id = 1;
        votacoes = models.Votacao.objects.all()
        filtro_votacao = filtro.FiltroVotacao()
        votacoes_da_proposicao = filtro_votacao._recupera_votacoes_da_proposicao(proposicao, votacoes)        
        self.assertEquals(1, len(votacoes_da_proposicao))

    def test_filtra_proposicoes_com_votacoes(self):
        proposicoes = models.Proposicao.objects.filter(casa_legislativa_id = 1)
        votacoes = models.Votacao.objects.all()
        filtro_votacao = filtro.FiltroVotacao()
        proposicoes_com_votacoes = filtro_votacao._filtra_proposicoes_com_votacoes(proposicoes, votacoes)
        self.assertEquals(8, len(proposicoes_com_votacoes))

    def test_filtra_proposicoes_sem_votacoes(self):
        proposicoes = models.Proposicao.objects.filter(casa_legislativa_id = 1)
        votacoes = models.Votacao.objects.all()
        filtro_votacao = filtro.FiltroVotacao()
        proposicoes_com_votacoes = filtro_votacao._filtra_proposicoes_com_votacoes(proposicoes, votacoes)
        self.assertEquals(8, len(proposicoes_com_votacoes))

    def test_palavra_existe_em_descricao_proposicao(self):
        proposicao = models.Proposicao.objects.get(id = 1)
        votacoes = models.Votacao.objects.filter(proposicao_id = 1)
        palavra_chave = 'reforma'
        filtro_votacao = filtro.FiltroVotacao()
        palavra_existe_em_proposicao = filtro_votacao._palavra_existe_em_proposicao(proposicao, votacoes, palavra_chave)
        self.assertTrue(palavra_existe_em_proposicao)
        
    def test_palavra_nao_existe_em_proposicao(self):
        proposicao = models.Proposicao.objects.get(id = 1)
        votacoes = models.Votacao.objects.filter(proposicao_id = 1)
        palavra_chave = 'corrupcao'
        filtro_votacao = filtro.FiltroVotacao()
        palavra_existe_em_proposicao = filtro_votacao._palavra_existe_em_proposicao(proposicao, votacoes, palavra_chave)
        self.assertFalse(palavra_existe_em_proposicao)

    def test_palavra_existe_em_ementa_proposicao(self):
        proposicao = models.Proposicao.objects.get(id = 8)
        votacoes = models.Votacao.objects.filter(proposicao_id = 8)
        palavra_chave = 'armas'
        filtro_votacao = filtro.FiltroVotacao()
        palavra_existe_em_proposicao = filtro_votacao._palavra_existe_em_proposicao(proposicao, votacoes, palavra_chave)
        self.assertTrue(palavra_existe_em_proposicao)

    def test_palavra_existe_em_indexacao_proposicao(self):
        proposicao = models.Proposicao.objects.get(id = 8)
        votacoes = models.Votacao.objects.filter(proposicao_id = 8)
        palavra_chave = 'bombas'
        filtro_votacao = filtro.FiltroVotacao()
        palavra_existe_em_proposicao = filtro_votacao._palavra_existe_em_proposicao(proposicao, votacoes, palavra_chave)
        self.assertTrue(palavra_existe_em_proposicao)

    def test_palavra_existe_em_descricao_votacao(self):
        proposicao = models.Proposicao.objects.get(id = 8)
        votacoes = models.Votacao.objects.filter(proposicao_id = 8)
        palavra_chave = 'inglaterra'
        filtro_votacao = filtro.FiltroVotacao()
        palavra_existe_em_proposicao = filtro_votacao._palavra_existe_em_proposicao(proposicao, votacoes, palavra_chave)
        self.assertTrue(palavra_existe_em_proposicao)

    def test_verifica_palavras_chave_em_proposicao(self):
        proposicao = models.Proposicao.objects.get(id = 8)
        votacoes = models.Votacao.objects.filter(proposicao_id = 8)
        lista_palavras_chave = ['cotas', 'guerra', 'violência']
        filtro_votacao = filtro.FiltroVotacao()
        filtra_proposicoes_por_palavras_chave = filtro_votacao._verifica_palavras_chave_em_proposicao(proposicao, votacoes, lista_palavras_chave)
        self.assertTrue(filtra_proposicoes_por_palavras_chave)
          
    def test_verifica_palavras_chave_nao_relacionadas_em_proposicao(self):
        proposicao = models.Proposicao.objects.get(id = 8)
        votacoes = models.Votacao.objects.filter(proposicao_id = 8)
        lista_palavras_chave = ['cotas', 'educação', 'violência']
        filtro_votacao = filtro.FiltroVotacao()
        filtra_proposicoes_por_palavras_chave = filtro_votacao._verifica_palavras_chave_em_proposicao(proposicao, votacoes, lista_palavras_chave)
        self.assertFalse(filtra_proposicoes_por_palavras_chave)

    def test_filtra_votacoes(self):
        casa_legislativa = models.CasaLegislativa.objects.get(id = 1)
        periodo_casa_legislativa = models.PeriodoCasaLegislativa(date(1989,02,02), date(1989,10,10))
        lista_palavras_chave = ['cotas', 'guerra', 'violência']
        filtro_votacao = filtro.FiltroVotacao()
        votacoes_filtradas = filtro_votacao.filtra_votacoes(casa_legislativa, periodo_casa_legislativa, lista_palavras_chave)
        self.assertEquals(1, len(votacoes_filtradas)) 
     
         
    def test_filtra_votacoes_com_periodo_invalido(self):
        casa_legislativa = models.CasaLegislativa.objects.get(id = 1)
        periodo_casa_legislativa = models.PeriodoCasaLegislativa(date(1990,10,10), date(1990,10,10))
        lista_palavras_chave = ['cotas', 'guerra', 'violência']
        filtro_votacao = filtro.FiltroVotacao()
        votacoes_filtradas = filtro_votacao.filtra_votacoes(casa_legislativa, periodo_casa_legislativa, lista_palavras_chave)
        self.assertEquals(0, len(votacoes_filtradas)) 

    def test_filtra_votacoes_com_periodo_(self):
        casa_legislativa = models.CasaLegislativa.objects.get(id = 1)
        periodo_casa_legislativa = models.PeriodoCasaLegislativa(date(1989,8,8), date(1992,11,11))
        lista_palavras_chave = ['cotas', 'guerra', 'violência']
        filtro_votacao = filtro.FiltroVotacao()
        votacoes_filtradas = filtro_votacao.filtra_votacoes(casa_legislativa, periodo_casa_legislativa, lista_palavras_chave)
        self.assertEquals(1, len(votacoes_filtradas)) 
     
    def test_filtra_votacoes_sem_palavras_chave_relacionadas(self):
        casa_legislativa = models.CasaLegislativa.objects.get(id = 1)
        periodo_casa_legislativa = models.PeriodoCasaLegislativa(date(1989,02,02), date(1989,10,10))
        lista_palavras_chave = ['cotas', 'educacao', 'violência']
        filtro_votacao = filtro.FiltroVotacao()
        votacoes_filtradas = filtro_votacao.filtra_votacoes(casa_legislativa, periodo_casa_legislativa, lista_palavras_chave)
        self.assertEquals(0, len(votacoes_filtradas))

    def test_filtra_votacoes_com_varias_palavras_chave(self):
        casa_legislativa = models.CasaLegislativa.objects.get(id = 1)
        periodo_casa_legislativa = models.PeriodoCasaLegislativa(date(1989,02,02), date(1989,10,10))
        lista_palavras_chave = ['militar', 'guerra', 'escolas', 'pensão']
        filtro_votacao = filtro.FiltroVotacao()
        votacoes_filtradas = filtro_votacao.filtra_votacoes(casa_legislativa, periodo_casa_legislativa, lista_palavras_chave)
        self.assertEquals(4, len(votacoes_filtradas))


    def test_filtra_votacoes_por_palavras_chave(self):
        proposicoes = models.Proposicao.objects.filter(casa_legislativa_id = 1)
        votacoes = models.Votacao.objects.all()
        lista_palavras_chave = ['militar', 'guerra', 'escolas', 'pensão']
        filtro_votacao = filtro.FiltroVotacao()
        votacoes_com_palavras_chave = filtro_votacao._filtra_votacoes_por_palavras_chave(proposicoes, votacoes, lista_palavras_chave)
        self.assertEquals(4, len(votacoes_com_palavras_chave))

# grafico tests

class JsonAnaliseGeneratorTest(TestCase):
    # TODO some complicated calculus performed in JsonAnaliseGeneratorTest
    # should be done by a new class, possibly in grafico module.
    # This test is not complete, it could test more json elements.

    @classmethod
    def setUpClass(cls):
        cls.importer = convencao.ImportadorConvencao()
        cls.importer.importar()
    
    @classmethod    
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)        
            
    def setUp(self):
        
        self.casa = models.CasaLegislativa.objects.get(nome_curto='conv')
        for partido in JsonAnaliseGeneratorTest.importer.partidos:
            if partido.nome == convencao.GIRONDINOS:
                self.girondinos = partido
            if partido.nome == convencao.JACOBINOS:
                self.jacobinos = partido
            if partido.nome == convencao.MONARQUISTAS:
                self.monarquistas = partido
                        
        self.analiseTemporal = AnaliseTemporal()
        self.analiseTemporal.casa_legislativa = self.casa
        self.analiseTemporal.periodicidade = models.BIENIO
        self.analiseTemporal.area_total = 1
        self.analiseTemporal.analises_periodo = []
        
        ap1 = AnalisePeriodo()
        periodos_retriever = utils.PeriodosRetriever(self.casa, models.BIENIO)
        periodos = periodos_retriever.get_periodos()
        ap1.casa_legislativa = None
        ap1.periodo = periodos[0]
        ap1.partidos = [ self.girondinos, self.jacobinos, self.monarquistas ]
        ap1.votacoes = []
        ap1.num_votacoes = 0
        ap1.tamanhos_partidos = {self.girondinos : 3, self.jacobinos : 3, self.monarquistas : 3} 
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


class MaxRadiusCalculatorTest(TestCase):
    
    def test_max_radius_calculator(self):
        calc = grafico.MaxRadiusCalculator()
        self.assertEquals(calc.max_r(), 0)
        calc.add_point(4, 3)
        self.assertEquals(calc.max_r(), 5)
        calc.add_point(1, 2)
        self.assertEquals(calc.max_r(), 5)
        calc.add_point(1, None)
        self.assertEquals(calc.max_r(), 5)
        calc.add_point(10, 3)
        self.assertAlmostEquals(calc.max_r(), 10.44, 1)

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
