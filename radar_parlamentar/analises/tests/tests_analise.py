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

from analises import analise
from modelagem import models
from importadores import convencao
from datetime import date
import numpy

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



class MatrizesDeDadosBuilderTest(TestCase):        

    @classmethod
    def setUpClass(cls):
        cls.importer = convencao.ImportadorConvencao()
        cls.importer.importar()

    def setUp(self):
        self.casa_legislativa = models.CasaLegislativa.objects.get(nome_curto='conv')
        self.partidos = MatrizesDeDadosBuilderTest.importer.partidos
        self.votacoes = models.Votacao.objects.filter(proposicao__casa_legislativa__nome_curto='conv')
        self.legislaturas = models.Legislatura.objects.filter(casa_legislativa__nome_curto='conv').distinct()
                        
    # TODO creio que esta matriz não é mais utilizada...                     
    def test_matriz_votacoes_por_partido(self):
        vetor_girondinos =   [mean([1, 0, -1]), mean([-1, -1, -1]), mean([-1, -1, 1]), mean([1, 1, 1]), mean([1, 1, 0]), mean([1, 1, 1]), mean([1, 1, 0]), mean([-1, -1, -1])]
        vetor_jacobinos =    [mean([1, 1, 1]), mean([-1, -1, -1]), mean([-1, -1, -1]), mean([1, 0 -1]), mean([1, 1, 1]), mean([1, 1, 1]), mean([1, 1, 1]), mean([0, -1, -1])]
        vetor_monarquistas = [mean([-1, -1, -1]), mean([1, 1, 1]), mean([1, 1, 1]), mean([1, -1]), mean([-1, -1, -1]), mean([1, 1]), mean([1,  1]), mean([1, 1])]
        MATRIZ_VOTACAO_ESPERADA = numpy.matrix([vetor_girondinos, vetor_jacobinos, vetor_monarquistas])
        builder = analise.MatrizesDeDadosBuilder(self.votacoes, self.partidos, self.legislaturas)
        builder.gera_matrizes()
        matriz_votacao_por_partido = builder.matriz_votacoes_por_partido
        self.assertTrue((matriz_votacao_por_partido == MATRIZ_VOTACAO_ESPERADA).all())         

def mean(v):
    return 1.0 * sum(v) / len(v)

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





