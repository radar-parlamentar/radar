# coding=utf8

# Copyright (C) 2014, Leonardo Leite
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

from analises import grafico
from modelagem import models
from modelagem import utils
from analises.models import AnalisePeriodo, AnaliseTemporal
from importadores import conv
from random import random
import numpy
import json


class JsonAnaliseGeneratorTest(TestCase):
    # TODO some complicated calculus performed in JsonAnaliseGeneratorTest
    # should be done by a new class, possibly in grafico module.
    # This test is not complete, it could test more json elements.

    @classmethod
    def setUpClass(cls):
        cls.importer = conv.ImportadorConvencao()
        cls.importer.importar()

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)

    def setUp(self):

        self.casa = models.CasaLegislativa.objects.get(nome_curto='conv')
        for partido in JsonAnaliseGeneratorTest.importer.partidos:
            if partido.nome == conv.GIRONDINOS:
                self.girondinos = partido
            if partido.nome == conv.JACOBINOS:
                self.jacobinos = partido
            if partido.nome == conv.MONARQUISTAS:
                self.monarquistas = partido

        self.analiseTemporal = AnaliseTemporal()
        self.analiseTemporal.casa_legislativa = self.casa
        self.analiseTemporal.periodicidade = models.BIENIO
        self.analiseTemporal.analises_periodo = []
        self.analiseTemporal.total_votacoes = 8

        ap1 = AnalisePeriodo()
        periodos_retriever = utils.PeriodosRetriever(self.casa, models.BIENIO)
        periodos = periodos_retriever.get_periodos()
        ap1.casa_legislativa = None
        ap1.periodo = periodos[0]
        ap1.partidos = [self.girondinos, self.jacobinos, self.monarquistas]
        ap1.votacoes = []
        ap1.num_votacoes = 0
        ap1.tamanhos_partidos = {
            self.girondinos: 3, self.jacobinos: 3, self.monarquistas: 3}
        ap1.soma_dos_tamanhos_dos_partidos = 3 * 3
        ap1.pca = PCAStub()
        ap1.coordenadas_partidos = {}
        ap1.coordenadas_partidos[conv.JACOBINOS] = [-0.4, 0.3]
        ap1.coordenadas_partidos[conv.GIRONDINOS] = [0.9, -0.3]
        ap1.coordenadas_partidos[conv.MONARQUISTAS] = [0.2, 0.1]
        ap1.legislaturas_por_partido = JsonAnaliseGeneratorTest.importer.legs
        ap1.coordenadas_legislaturas = {}  # legislatura.id => [x,y]
        for p, legs in ap1.legislaturas_por_partido.items():
            for leg in legs:
                ap1.coordenadas_legislaturas[leg.id] = [random(), random()]
        self.analiseTemporal.analises_periodo.append(ap1)

    def test_json(self):
        gen = grafico.JsonAnaliseGenerator(self.analiseTemporal)
        generated_json = gen.get_json()
        dict_analise = json.loads(generated_json)
        self.assertEquals(dict_analise['geral']['total_votacoes'], 8)
        dict_casa = dict_analise['geral']['CasaLegislativa']
        self.assertEquals(dict_casa['nome_curto'], self.casa.nome_curto)
        list_periodos = dict_analise['periodos']
        self.assertEquals(len(list_periodos), 1)
        dict_periodo = list_periodos[0]
        self.assertTrue('1989' in dict_periodo['nome'])
        list_partidos = dict_analise['partidos']
        self.assertEquals(len(list_partidos), 3)
        dict_partido = list_partidos[0]
        toutes_les_parties = [
            conv.JACOBINOS, conv.GIRONDINOS, conv.MONARQUISTAS]
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


class GraphScalerTest(TestCase):

    def test_graph_scale(self):
        partidos = {}
        partidos['Jacobinos'] = [0.1, -0.2]
        partidos['Girondinos'] = [0.5, 1]
        scaler = grafico.GraphScaler()
        scaled = scaler.scale(partidos, "cach_key")
        self.assertEqual(10, scaled['Jacobinos'][0])
        self.assertEqual(-20, scaled['Jacobinos'][1])
        self.assertEqual(50, scaled['Girondinos'][0])
        self.assertEqual(100, scaled['Girondinos'][1])


class RaioPartidoCalculatorTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.importer = conv.ImportadorConvencao()
        cls.importer.importar()

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)

    def setUp(self):
        self.partidos = RaioPartidoCalculatorTest.importer.partidos

    def test_raio_partidos(self):
        periodo_str = '1o Semestre'
        tamanhos = {}
        tamanho_por_partido = conv.PARLAMENTARES_POR_PARTIDO
        for partido in self.partidos:
            tamanhos[partido] = tamanho_por_partido
        tamanhos_dos_partidos_por_periodo = {periodo_str: tamanhos}
        raio_calculator = grafico.RaioPartidoCalculator(
            tamanhos_dos_partidos_por_periodo)
        raio_esperado = 69.3
        for partido in self.partidos:
            raio = raio_calculator.get_raio(partido, periodo_str)
            self.assertAlmostEqual(raio, raio_esperado, 1)
