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
from analises import analise
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

        an = analise.AnalisePeriodo(self.casa_legislativa, partidos=self.partidos)
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

        an = analise.AnalisePeriodo(self.casa_legislativa, partidos=self.partidos)
        grafico = an.partidos_2d()

        self.assertAlmostEqual(grafico[convencao.JACOBINOS][0], -0.49321534, 4)
        self.assertAlmostEqual(grafico[convencao.JACOBINOS][1], -0.65069601, 4)
        self.assertAlmostEqual(grafico[convencao.MONARQUISTAS][0], 0.81012694, 4)
        self.assertAlmostEqual(grafico[convencao.MONARQUISTAS][1], -0.10178901, 4)
        self.assertAlmostEqual(grafico[convencao.GIRONDINOS][0], -0.31691161, 4)
        self.assertAlmostEqual(grafico[convencao.GIRONDINOS][1], 0.75248502, 4)
        
    def test_json(self):
        
        EXPECTED_JSON = '{1000:{"Monarquistas":{"numPartido":79, "tamanhoPartido":2309, "x":0.8, "y":0.18}, "Girondinos":{"numPartido":27, "tamanhoPartido":2309, "x":-0.24, "y":-0.78}, "Jacobinos":{"numPartido":42, "tamanhoPartido":2309, "x":-0.56, "y":0.6}},  1001:{"Monarquistas":{"numPartido":79, "tamanhoPartido":2309, "x":0.01, "y":0.82}, "Girondinos":{"numPartido":27, "tamanhoPartido":2309, "x":0.7, "y":-0.41}, "Jacobinos":{"numPartido":42, "tamanhoPartido":2309, "x":-0.71, "y":-0.4}}}'
        
        gen = analise.JsonAnaliseGenerator()
        ini = '1989-01-01'
        fim = '1989-12-30'
        json = gen.get_json(self.casa_legislativa, ini, fim, self.partidos)
        self.assertEqual(json, EXPECTED_JSON)

