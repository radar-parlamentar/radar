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

from analises import filtro
from modelagem import models
from importadores import conv
from datetime import date


class FiltroVotacaoTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.importer = conv.ImportadorConvencao()
        cls.importer.importar()

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)

    def test_filtra_votacoes(self):
        casa_legislativa = models.CasaLegislativa.objects.get(id=1)
        periodo_casa_legislativa = models.PeriodoCasaLegislativa(
            date(1989, 8, 8), date(1992, 11, 11))
        lista_palavras_chave = ['cotas', 'guerra', 'violência']
        filtro_votacao = filtro.FiltroVotacao(
            casa_legislativa, periodo_casa_legislativa, lista_palavras_chave)
        votacoes_filtradas = filtro_votacao.filtra_votacoes()
        self.assertEquals(2, len(votacoes_filtradas))

    def test_filtra_votacoes_com_periodo_invalido(self):
        casa_legislativa = models.CasaLegislativa.objects.get(id=1)
        periodo_casa_legislativa = models.PeriodoCasaLegislativa(
            date(1990, 10, 10), date(1990, 10, 10))
        lista_palavras_chave = ['cotas', 'guerra', 'violência']
        filtro_votacao = filtro.FiltroVotacao(
            casa_legislativa, periodo_casa_legislativa, lista_palavras_chave)
        votacoes_filtradas = filtro_votacao.filtra_votacoes()
        self.assertEquals(0, len(votacoes_filtradas))

    def test_filtra_votacoes_sem_palavras_chave_relacionadas(self):
        casa_legislativa = models.CasaLegislativa.objects.get(id=1)
        periodo_casa_legislativa = models.PeriodoCasaLegislativa(date(1989, 02, 02), date(1989, 10, 10))
        lista_palavras_chave = ['educacao', 'violência']
        filtro_votacao = filtro.FiltroVotacao(
            casa_legislativa, periodo_casa_legislativa, lista_palavras_chave)
        votacoes_filtradas = filtro_votacao.filtra_votacoes()
        self.assertEquals(0, len(votacoes_filtradas))

    def test_filtra_votacoes_com_varias_palavras_chave(self):
        casa_legislativa = models.CasaLegislativa.objects.get(id=1)
        periodo_casa_legislativa = models.PeriodoCasaLegislativa(date(1989, 02, 02), date(1989, 10, 10))
        lista_palavras_chave = ['militar', 'guerra', 'escolas', 'nobres']
        filtro_votacao = filtro.FiltroVotacao(
            casa_legislativa, periodo_casa_legislativa, lista_palavras_chave)
        votacoes_filtradas = filtro_votacao.filtra_votacoes()
        self.assertEquals(4, len(votacoes_filtradas))


class TemasTest(TestCase):

    # TODO teste com acentos
    # TODO teste com palavra pertencente a mais de um tema

    def setUp(self):
        self.temas = filtro.Temas()
        self.temas.inserir_sinonimo("tecnologia", "software")
        self.temas.inserir_sinonimo("tecnologia", "internet")
        self.temas.inserir_sinonimo("tecnologia", "hacker")
        self.temas.inserir_sinonimo("paleontologia", "sítio")
        self.temas.inserir_sinonimo("paleontologia", "dinossauro")
        self.temas.inserir_sinonimo("economia", "bolsa")
        self.temas.inserir_sinonimo("economia", "mercado")

    def test_insercao_erro(self):
        with self.assertRaises(ValueError):
            self.temas.inserir_sinonimo("tecnologia", None)

        with self.assertRaises(ValueError):
            self.temas.inserir_sinonimo(None, "software")

    def test_recuperacao_por_sinonimo(self):
        palavras = self.temas.recuperar_sinonimos("software")
        self.assertEquals(4, len(palavras))
        self.assertTrue("tecnologia" in palavras)
        self.assertTrue("software" in palavras)
        self.assertTrue("internet" in palavras)
        self.assertTrue("hacker" in palavras)

    def test_recuperacao_por_tema(self):
        palavras = self.temas.recuperar_sinonimos("tecnologia")
        self.assertEquals(4, len(palavras))
        self.assertTrue("tecnologia" in palavras)
        self.assertTrue("software" in palavras)
        self.assertTrue("internet" in palavras)
        self.assertTrue("hacker" in palavras)

    def test_recuperacao_por_tema_abreviado(self):
        palavras = self.temas.recuperar_sinonimos("tec")
        self.assertEquals(4, len(palavras))
        self.assertTrue("tecnologia" in palavras)
        self.assertTrue("software" in palavras)
        self.assertTrue("internet" in palavras)
        self.assertTrue("hacker" in palavras)

    def test_recuperacao_por_sinonimo_abreviado(self):
        palavras = self.temas.recuperar_sinonimos("hack")
        self.assertEquals(4, len(palavras))
        self.assertTrue("tecnologia" in palavras)
        self.assertTrue("software" in palavras)
        self.assertTrue("internet" in palavras)
        self.assertTrue("hacker" in palavras)

    def test_expandir_palavras_chaves(self):
        palavras_chaves = ["soft", "eco"]
        palavras = self.temas.expandir_palavras_chaves(palavras_chaves)
        self.assertEquals(7, len(palavras))
        self.assertTrue("tecnologia" in palavras)
        self.assertTrue("software" in palavras)
        self.assertTrue("internet" in palavras)
        self.assertTrue("hacker" in palavras)
        self.assertTrue("economia" in palavras)
        self.assertTrue("bolsa" in palavras)
        self.assertTrue("mercado" in palavras)

    def test_palavra_nao_cadastrada(self):
        palavras_chaves = ["guerra"]
        palavras = self.temas.expandir_palavras_chaves(palavras_chaves)
        self.assertEquals(1, len(palavras))
        self.assertTrue("guerra" in palavras)
