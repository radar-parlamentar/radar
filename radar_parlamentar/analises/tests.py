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
from analises import analise
from grafico import GeradorGrafico
from importadores import convencao
from modelagem import models

class AnaliseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.importer = convencao.ImportadorConvencao()
        cls.importer.importar()

    def setUp(self):

        self.casa_legislativa = models.CasaLegislativa.objects.get(nome_curto='conv')
        self.partidos = AnaliseTest.importer.partidos

    def test_casa(self):
        """Testa se casa legislativa foi corretamente recuperada do banco"""

        self.assertAlmostEqual(self.casa_legislativa.nome, 'Convenção Nacional Francesa')
        
    def test_tamanho_partidos(self):
        """Testa tamanho dos partidos"""

        an = analise.AnalisadorPeriodo(self.casa_legislativa, partidos=self.partidos)
        an._inicializa_vetores()
        tamanhos = an.tamanhos_partidos
        tamanho_jacobinos = tamanhos[convencao.JACOBINOS]
        tamanho_girondinos = tamanhos[convencao.GIRONDINOS]
        tamanho_monarquistas = tamanhos[convencao.MONARQUISTAS]
        self.assertEqual(tamanho_jacobinos, convencao.PARLAMENTARES_POR_PARTIDO)
        self.assertEqual(tamanho_girondinos, convencao.PARLAMENTARES_POR_PARTIDO)
        self.assertEqual(tamanho_monarquistas, convencao.PARLAMENTARES_POR_PARTIDO)

    def test_partidos_2d(self):
        """Testa resultado do PCA"""

        an = analise.AnalisadorPeriodo(self.casa_legislativa, partidos=self.partidos)
        grafico = an.partidos_2d()

        self.assertAlmostEqual(grafico[convencao.JACOBINOS][0], -0.49321534, 4)
        self.assertAlmostEqual(grafico[convencao.JACOBINOS][1], -0.65069601, 4)
        self.assertAlmostEqual(grafico[convencao.MONARQUISTAS][0], 0.81012694, 4)
        self.assertAlmostEqual(grafico[convencao.MONARQUISTAS][1], -0.10178901, 4)
        self.assertAlmostEqual(grafico[convencao.GIRONDINOS][0], -0.31691161, 4)
        self.assertAlmostEqual(grafico[convencao.GIRONDINOS][1], 0.75248502, 4)
        
    def test_json(self):
        
        EXPECTED_JSON = '{"1989 1o Semestre":{"Monarquistas":{"numPartido":79, "tamanhoPartido":2309, "x":0.8, "y":0.18}, "Girondinos":{"numPartido":27, "tamanhoPartido":2309, "x":-0.24, "y":-0.78}, "Jacobinos":{"numPartido":42, "tamanhoPartido":2309, "x":-0.56, "y":0.6}},  "1989 2o Semestre":{"Monarquistas":{"numPartido":79, "tamanhoPartido":2309, "x":0.01, "y":0.82}, "Girondinos":{"numPartido":27, "tamanhoPartido":2309, "x":0.7, "y":-0.41}, "Jacobinos":{"numPartido":42, "tamanhoPartido":2309, "x":-0.71, "y":-0.4}}}'

# estrutura do novo json (verificar valores de x e y)        
#         EXPECTED_JSON = ( '{ "periodos":{ "1":"1989 1o Semestre", "2":"1989 2o Semestre" }, '
#                  '"partidos":[ { "nome":"Monarquistas", "numero":79, "cor":"#A81450", '
#                  '"tamanho":[ [1,3], [2,3] ],   '
#                  '"x":[ [1,89.77], [2,97.97] ], '
#                  '"y":[ [1,59.24], [2,-33.48] ] }, '
#                  '{ "nome":"Jacobinos", "numero":42, "cor":"#1421CC", '
#                  '"tamanho":[ [1,2], [2,3] ], '
#                  '"x":[ [1,22.12], [2,83.24] ], '
#                  '"y":[ [1,79.82], [2,35.68] ] }, '
#                  '{ "nome":"Girondinos", "numero":27, "cor":"#42A116", '
#                  '"tamanho":[ [1,3], [2,3] ], '
#                  '"x":[ [1,38.12], [2,30.71] ], '
#                  '"y":[ [1,10.94], [2,-11.66] ] } ] }' )
        
        gen = analise.JsonAnaliseGenerator()
        json = gen.get_json(self.casa_legislativa)
        self.assertEqual(json, EXPECTED_JSON)

############################
# Testes não automatizados #
############################

class GraficoTest():

    def importa_dados(self):
        if not models.CasaLegislativa.objects.filter(nome_curto='conv').exists():
            importer = convencao.ImportadorConvencao()
            importer.importar()
        self.casa_legislativa = models.CasaLegislativa.objects.get(nome_curto='conv')
        g = models.Partido.objects.get(nome=convencao.GIRONDINOS)
        j = models.Partido.objects.get(nome=convencao.JACOBINOS)
        m = models.Partido.objects.get(nome=convencao.MONARQUISTAS)
        self.partidos = [g, j, m]

    def testa_geracao_figura(self):
        self.importa_dados()
        an = analise.AnalisadorPeriodo(self.casa_legislativa, partidos=self.partidos)
        an.partidos_2d()
        gen = GeradorGrafico(an)
        gen.figura()

def main():
    test = GraficoTest()
    test.testa_geracao_figura()

