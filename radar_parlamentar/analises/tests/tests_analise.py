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
from modelagem import models
from modelagem.utils import PeriodosRetriever
from importadores import conv
from datetime import date
import numpy
import logging

logger = logging.getLogger("radar")


class AnalisadorPeriodoTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.importer = conv.ImportadorConvencao()
        cls.importer.importar()

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)

    def setUp(self):
        self.casa_legislativa = models.CasaLegislativa.objects.get(
            nome_curto='conv')
        self.partidos = AnalisadorPeriodoTest.importer.partidos
        self.votacoes = models.Votacao.objects.filter(
            proposicao__casa_legislativa__nome_curto='conv')
        self.parlamentares = models.Parlamentar.objects.filter(
            casa_legislativa__nome_curto='conv').distinct()
        for partido in self.partidos:
            if partido.nome == conv.GIRONDINOS:
                self.girondinos = partido
            if partido.nome == conv.JACOBINOS:
                self.jacobinos = partido
            if partido.nome == conv.MONARQUISTAS:
                self.monarquistas = partido
        
        self.chefe = models.ChefeExecutivo(nome="Luiz Inacio Pierre da Silva", genero="M", partido = self.girondinos,
                                    mandato_ano_inicio = 1988, mandato_ano_fim = 1992)
        self.chefe.save()
        self.chefe.casas_legislativas.add(self.casa_legislativa)
        

    # TODO test_coordenadas_parlamentares

    # TODO mover test_coordenadas_partidos para AnalisadorPartidosTest
    def test_coordenadas_partidos(self):
        periodo = models.PeriodoCasaLegislativa(date(1989, 02, 02),
                                                date(1989, 10, 10))
        analisador = analise.AnalisadorPeriodo(self.casa_legislativa, periodo)
        analise_periodo = analisador.analisa()
        coordenadas = analise_periodo.coordenadas_partidos
        self.assertAlmostEqual(coordenadas[self.girondinos][0], -0.152, 2)
        self.assertAlmostEqual(coordenadas[self.girondinos][1], -0.261, 2)
        self.assertAlmostEqual(coordenadas[self.jacobinos][0], -0.287, 2)
        self.assertAlmostEqual(coordenadas[self.jacobinos][1], 0.181, 2)
        self.assertAlmostEqual(coordenadas[self.monarquistas][0], 0.440, 2)
        self.assertAlmostEqual(coordenadas[self.monarquistas][1], 0.079, 2)

    # TODO mover test_tamanho_partidos para AnalisadorPartidosTest
    def test_tamanho_partidos(self):
        periodo = models.PeriodoCasaLegislativa(date(1989, 02, 02),
                                                date(1989, 10, 10))
        analisador = analise.AnalisadorPeriodo(self.casa_legislativa, periodo)
        analise_periodo = analisador.analisa()
        tamanhos = analise_periodo.tamanhos_partidos
        tamanho_esperado = conv.PARLAMENTARES_POR_PARTIDO
        partidos = AnalisadorPeriodoTest.importer.partidos
        self.assertEquals(3, len(partidos))
        for p in partidos:
            self.assertEqual(tamanhos[p], tamanho_esperado)
    
    def test_chefes_executivos(self):
        periodo = models.PeriodoCasaLegislativa(date(1989, 02, 02), date(1989, 10, 10))
        analisador = analise.AnalisadorPeriodo(self.casa_legislativa, periodo)
        analise_periodo = analisador.analisa()
        chefes_executivos = analise_periodo.chefes_executivos
        chefe_esperado = self.chefe
        
        self.assertEquals(unicode(chefes_executivos[0]), unicode(chefe_esperado))

class MatrizesDeDadosBuilderTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.importer = conv.ImportadorConvencao()
        cls.importer.importar()

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)

    def setUp(self):
        self.casa_legislativa = models.CasaLegislativa.objects.get(
            nome_curto='conv')
        self.partidos = MatrizesDeDadosBuilderTest.importer.partidos
        self.votacoes = models.Votacao.objects.filter(
            proposicao__casa_legislativa__nome_curto='conv')
        self.parlamentares = models.Parlamentar.objects.filter(
            casa_legislativa__nome_curto='conv').distinct()

    def test_matriz_votacoes(self):
        # linhas são parlamentares e colunas são votações
        MATRIZ_VOTACAO_ESPERADA = numpy.matrix(
            [[1., -1., -1., 1., 1., 1., 1., -1., 1],
             [0., -1., -1., 1., 1., 1., 1., -1., 1],
             [-1., -1., 1., 1., 0., 1., 0., -1., 0],
             [1., -1., -1., 1., 1., 1., 1., 0., 1],
             [1., -1., -1., 0., 1., 1., 1., -1., 1],
             [1., -1., -1., -1., 1., 1., 1., -1., 1],
             [-1., 1., 1., 1., -1., 0., 1., 1., 1],
             [-1., 1., 1., -1., -1., 1., 0., 0., 0],
             [-1., 1., 1., 0., -1., 1., 1., 1., 1]])
        builder = analise.MatrizesDeDadosBuilder(
            self.votacoes, self.partidos, self.parlamentares)
        builder.gera_matrizes()
        self.assertTrue(
            (builder.matriz_votacoes == MATRIZ_VOTACAO_ESPERADA).all())

    def test_matriz_presencas(self):
        MATRIZ_PRESENCAS_ESPERADA = numpy.matrix(
            [[1., 1., 1., 1., 1., 1., 1., 1., 1],
             [1., 1., 1., 1., 1., 1., 1., 1., 1],
             [1., 1., 1., 1., 1., 1., 1., 1., 1],
             [1., 1., 1., 1., 1., 1., 1., 1., 1],
             [1., 1., 1., 1., 1., 1., 1., 1., 1],
             [1., 1., 1., 1., 1., 1., 1., 1., 1],
             [1., 1., 1., 1., 1., 0., 1., 1., 1],
             [1., 1., 1., 1., 1., 1., 0., 0., 0],
             [1., 1., 1., 0., 1., 1., 1., 1., 1]])

        builder = analise.MatrizesDeDadosBuilder(
            self.votacoes, self.partidos, self.parlamentares)
        builder.gera_matrizes()
        self.assertTrue(
            (builder.matriz_presencas == MATRIZ_PRESENCAS_ESPERADA).all())


class AnalisadorTemporalTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.importer = conv.ImportadorConvencao()
        cls.importer.importar()

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)

    def setUp(self):
        self.casa_legislativa = models.CasaLegislativa.objects.get(
            nome_curto='conv')
        self.partidos = AnalisadorTemporalTest.importer.partidos
        self.votacoes = models.Votacao.objects.filter(
            proposicao__casa_legislativa__nome_curto='conv')
        self.parlamentares = models.Parlamentar.objects.filter(
            casa_legislativa__nome_curto='conv').distinct()
        for partido in self.partidos:
            if partido.nome == conv.GIRONDINOS:
                self.girondinos = partido
            if partido.nome == conv.JACOBINOS:
                self.jacobinos = partido
            if partido.nome == conv.MONARQUISTAS:
                self.monarquistas = partido

    def test_analisador_temporal(self):
        analisador_temporal = analise.AnalisadorTemporal(
            self.casa_legislativa, models.SEMESTRE)
        analise_temporal = analisador_temporal.get_analise_temporal()
        self.assertEqual(analise_temporal.total_votacoes, 9)
        analises = analise_temporal.analises_periodo
        self.assertEqual(len(analises), 3)

        self.assertEqual(analise_temporal.chefes_executivos, [])

        # primeiro semestre de 1989
        coordenadas = analises[0].coordenadas_partidos
        self.assertAlmostEqual(
            coordenadas[self.girondinos][0], -0.11788123, 4)
        self.assertAlmostEqual(
            coordenadas[self.girondinos][1], -0.29647299, 4)
        self.assertAlmostEqual(
            coordenadas[self.jacobinos][0], -0.30596818, 4)
        self.assertAlmostEqual(
            coordenadas[self.jacobinos][1], 0.19860293, 4)
        self.assertAlmostEqual(
            coordenadas[self.monarquistas][0], 0.42384941, 4)
        self.assertAlmostEqual(
            coordenadas[self.monarquistas][1], 0.09787006, 4)

        # segundo semestre de 1989
        coordenadas = analises[1].coordenadas_partidos
        self.assertAlmostEqual(
            coordenadas[self.girondinos][0], -0.217213339209, 4)
        self.assertAlmostEqual(
            coordenadas[self.girondinos][1], 0.162195036556, 4)
        self.assertAlmostEqual(
            coordenadas[self.jacobinos][0], -0.234612288891, 4)
        self.assertAlmostEqual(
            coordenadas[self.jacobinos][1], -0.173823604055, 4)
        self.assertAlmostEqual(
            coordenadas[self.monarquistas][0], 0.45182562815, 4)
        self.assertAlmostEqual(
            coordenadas[self.monarquistas][1], 0.011628567499, 4)

        # primeiro semestre de 1990 (nesse período teve só uma votação)
        coordenadas = analises[2].coordenadas_partidos
        self.assertAlmostEqual(
            coordenadas[self.girondinos][0], -0.222717701594, 4)
        self.assertAlmostEqual(
            coordenadas[self.girondinos][1], 0.0, 4)
        self.assertAlmostEqual(
            coordenadas[self.jacobinos][0], 0.133630620956, 4)
        self.assertAlmostEqual(
            coordenadas[self.jacobinos][1], 0.0, 4)
        self.assertAlmostEqual(
            coordenadas[self.monarquistas][0], 0.133630620956, 4)
        self.assertAlmostEqual(
            coordenadas[self.monarquistas][1], 0.0, 4)


class RotacionadorTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.importer = conv.ImportadorConvencao()
        cls.importer.importar()

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)

    def setUp(self):
        self.casa_legislativa = models.CasaLegislativa.objects.get(
            nome_curto='conv')

    def test_rotacao(self):
        periodosRetriever = PeriodosRetriever(
            self.casa_legislativa, models.SEMESTRE)
        periodos = periodosRetriever.get_periodos()
        analisador1 = analise.AnalisadorPeriodo(
            self.casa_legislativa, periodo=periodos[0])
        analise_do_periodo1 = analisador1.analisa()
        analisador2 = analise.AnalisadorPeriodo(
            self.casa_legislativa, periodo=periodos[1])
        analise_do_periodo2 = analisador2.analisa()
        rotacionador = analise.Rotacionador(
            analise_do_periodo2, analise_do_periodo1)
        analise_rotacionada = rotacionador.espelha_ou_roda()
        grafico = analise_rotacionada.coordenadas_parlamentares
        # parlamentar 1
        self.assertAlmostEqual(grafico[1][0], -0.29498659, 4)
        self.assertAlmostEqual(grafico[1][1], -0.06674737, 4)
        # parlamentar 4
        self.assertAlmostEqual(grafico[4][0], -0.11386368, 4)
        self.assertAlmostEqual(grafico[4][1], -0.38797608, 4)
        # parlamentar 9
        self.assertAlmostEqual(grafico[9][0], 0.49080368, 4)
        self.assertAlmostEqual(grafico[9][1], -0.20057948, 4)
