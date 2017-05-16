# !/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Diego Rabatone
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


from django.test import TestCase
from importadores import conv
from modelagem import models

NUMERO_VOTACOES = 9
NUMERO_PARTIDOS = 3
NUMERO_PARLAMENTARES_POR_PARTIDO = 3
NUMERO_VOTOS_TOTAIS = \
    NUMERO_VOTACOES * NUMERO_PARTIDOS * NUMERO_PARLAMENTARES_POR_PARTIDO
NUMERO_VOTOS_POR_VOTACAO = NUMERO_PARTIDOS * NUMERO_PARLAMENTARES_POR_PARTIDO


class ConvencaoTest(TestCase):

    @classmethod
    def setUpClass(cls):
        importer = conv.ImportadorConvencao()
        importer.importar()

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)

    def setUp(self):
        self.conv = models.CasaLegislativa.objects.get(nome_curto='conv')

    def test_check_len_votacoes(self):
        num_votacoes = len(models.Votacao.objects.filter(
            proposicao__casa_legislativa=self.conv))
        self.assertEqual(num_votacoes, NUMERO_VOTACOES)

    def test_check_len_votos(self):
        num_votos = len(models.Voto.objects.filter(
            votacao__proposicao__casa_legislativa=self.conv))
        self.assertEqual(num_votos, NUMERO_VOTOS_TOTAIS)

    def test_check_len_votos_por_votacao(self):
        votacoes = models.Votacao.objects.filter(
            proposicao__casa_legislativa=self.conv)
        for votacao in votacoes:
            num_votos = len(models.Voto.objects.filter(votacao=votacao))
            self.assertEqual(num_votos, NUMERO_VOTOS_POR_VOTACAO)

    def test_check_partidos(self):
        partidos = models.Partido.objects.all()
        nomes_partidos = [p.nome for p in partidos]
        self.assertTrue(conv.GIRONDINOS in nomes_partidos)
        self.assertTrue(conv.JACOBINOS in nomes_partidos)
        self.assertTrue(conv.MONARQUISTAS in nomes_partidos)

    def test_check_parlamentares(self):
        parlamentares = models.Parlamentar.objects.filter(
            casa_legislativa=self.conv)
        self.assertEqual(len(parlamentares),
                         NUMERO_PARTIDOS * NUMERO_PARLAMENTARES_POR_PARTIDO)
        nomes_parlamentares = [p.nome for p in parlamentares]
        self.assertEqual(nomes_parlamentares.count('Pierre'),
                          NUMERO_PARTIDOS * NUMERO_PARLAMENTARES_POR_PARTIDO)
