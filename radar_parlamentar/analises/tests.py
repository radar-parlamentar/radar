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

        self.assertAlmostEqual(grafico[convencao.JACOBINOS][0], 25.339, 2)
        self.assertAlmostEqual(grafico[convencao.JACOBINOS][1], 17.465, 2)
        self.assertAlmostEqual(grafico[convencao.MONARQUISTAS][0], 90.506, 2)
        self.assertAlmostEqual(grafico[convencao.MONARQUISTAS][1], 44.911, 2)
        self.assertAlmostEqual(grafico[convencao.GIRONDINOS][0], 34.154, 2)
        self.assertAlmostEqual(grafico[convencao.GIRONDINOS][1], 87.624, 2)
        
    def test_json(self):
        
        EXPECTED_JSON = ( '{"1989 1o Semestre":{"Monarquistas":{"numPartido":79, "tamanhoPartido":2309, "x":89.77, "y":59.24}, '
                          '"Girondinos":{"numPartido":27, "tamanhoPartido":2309, "x":38.12, "y":10.94}, '
                          '"Jacobinos":{"numPartido":42, "tamanhoPartido":2309, "x":22.12, "y":79.82}},  '
                          '"1989 2o Semestre":{"Monarquistas":{"numPartido":79, "tamanhoPartido":2309, "x":97.97, "y":-33.48}, '
                          '"Girondinos":{"numPartido":27, "tamanhoPartido":2309, "x":30.71, "y":-11.66}, '
                          '"Jacobinos":{"numPartido":42, "tamanhoPartido":2309, "x":83.24, "y":35.68}}}' )
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

