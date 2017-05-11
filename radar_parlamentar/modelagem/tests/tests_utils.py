# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Eduardo Hideo, Diego Rabatone
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
from importadores import conv
import datetime
import modelagem.models 
import modelagem.utils 
from util_test import flush_db
from django.utils.dateparse import parse_datetime
from modelagem.models import MUNICIPAL, FEDERAL, ESTADUAL, BIENIO
import logging

logger = logging.getLogger("radar")


class MandatoListsTest(TestCase):

    def test_get_mandatos_municipais(self):
        ini_date = datetime.date(2008, 10, 10)
        fim_date = datetime.date(2013, 10, 10)
        mandato_lists = modelagem.utils.MandatoLists()
        mandatos = mandato_lists.get_mandatos(MUNICIPAL, ini_date, fim_date)
        self.assertEquals(len(mandatos), 3)
        self.assertEquals(mandatos[0].year, 2005)
        self.assertEquals(mandatos[1].year, 2009)
        self.assertEquals(mandatos[2].year, 2013)
        for mandato in mandatos:
            self.assertEquals(mandato.day, 1)
            self.assertEquals(mandato.month, 1)

    def test_get_mandatos_municipais_soh_um(self):
        ini_date = parse_datetime('2009-10-10 0:0:0')
        fim_date = parse_datetime('2012-10-10 0:0:0')
        mandato_lists = modelagem.utils.MandatoLists()
        mandatos = mandato_lists.get_mandatos(MUNICIPAL, ini_date, fim_date)
        self.assertEquals(len(mandatos), 1)
        self.assertEquals(mandatos[0].year, 2009)

    def test_get_mandatos_federais(self):
        self._test_get_mandatos_federais_ou_estaduais(FEDERAL)

    def test_get_mandatos_estaduais(self):
        self._test_get_mandatos_federais_ou_estaduais(ESTADUAL)

    def _test_get_mandatos_federais_ou_estaduais(self, esfera):
        ini_date = datetime.date(2008, 10, 10)
        fim_date = datetime.date(2015, 10, 10)
        mandato_lists = modelagem.utils.MandatoLists()
        mandatos = mandato_lists.get_mandatos(esfera, ini_date, fim_date)
        self.assertEquals(len(mandatos), 3)
        self.assertEquals(mandatos[0].year, 2007)
        self.assertEquals(mandatos[1].year, 2011)
        self.assertEquals(mandatos[2].year, 2015)
        for mandato in mandatos:
            self.assertEquals(mandato.day, 1)
            self.assertEquals(mandato.month, 1)


class PeriodosRetrieverTest(TestCase):

    @classmethod
    def setUpClass(cls):
        importer = conv.ImportadorConvencao()
        importer.importar()

    @classmethod
    def tearDownClass(cls):
        flush_db(cls)

    def setUp(self):
        self.conv = modelagem.models.CasaLegislativa.objects.get(nome_curto='conv')

    def test_casa_legislativa_periodos_anuais(self):
        retriever = modelagem.utils.PeriodosRetriever(self.conv, modelagem.models.ANO)
        periodos = retriever.get_periodos()
        self.assertEquals(len(periodos), 2)
        self.assertEqual(periodos[0].string, '1989')
        self.assertEqual(periodos[1].string, '1990')
        self.assertEqual(periodos[0].quantidade_votacoes, 8)
        self.assertEqual(periodos[1].quantidade_votacoes, 1)

    def test_casa_legislativa_periodos_mensais(self):
        retriever = modelagem.utils.PeriodosRetriever(self.conv, modelagem.models.MES)
        periodos = retriever.get_periodos()
        self.assertEquals(len(periodos), 3)
        self.assertEqual(periodos[0].string, '1989 Fev')
        self.assertEqual(periodos[0].quantidade_votacoes, 4)
        self.assertEqual(periodos[1].string, '1989 Out')
        self.assertEqual(periodos[1].quantidade_votacoes, 4)
        self.assertEqual(periodos[2].string, '1990 Jan')
        self.assertEqual(periodos[2].quantidade_votacoes, 1)

    def test_casa_legislativa_periodos_semestrais(self):
        retriever = modelagem.utils.PeriodosRetriever(self.conv, modelagem.models.SEMESTRE)
        periodos = retriever.get_periodos()
        self.assertEquals(len(periodos), 3)
        d = periodos[0].ini
        self.assertEqual(1989, d.year)
        self.assertEqual(1, d.month)
        d = periodos[0].fim
        self.assertEqual(1989, d.year)
        self.assertEqual(6, d.month)
        d = periodos[1].ini
        self.assertEqual(1989, d.year)
        self.assertEqual(7, d.month)
        d = periodos[1].fim
        self.assertEqual(1989, d.year)
        self.assertEqual(12, d.month)
        d = periodos[2].ini
        self.assertEqual(1990, d.year)
        self.assertEqual(1, d.month)
        d = periodos[2].fim
        self.assertEqual(1990, d.year)
        self.assertEqual(6, d.month)
        self.assertEqual(periodos[0].string, '1989 1o Semestre')
        self.assertEqual(periodos[1].string, '1989 2o Semestre')
        self.assertEqual(periodos[2].string, '1990 1o Semestre')

    def test_periodo_municipal_nao_deve_conter_votacoes_de_dois_mandatos(self):
        self._test_periodos_em_duas_datas(2008, 2009, MUNICIPAL, BIENIO, 2)

    def test_periodo_municipal_deve_estar_em_um_mandato(self):
        self._test_periodos_em_duas_datas(2009, 2010, MUNICIPAL, BIENIO, 1)

    def test_inicio_de_periodo_municipal_deve_coincidir_com_inicio_mandato(
            self):
        self._test_periodos_em_duas_datas(2010, 2011, MUNICIPAL, BIENIO, 2)

    def test_periodo_federal_nao_deve_conter_votacoes_de_dois_mandatos(self):
        self._test_periodos_em_duas_datas(2010, 2011, FEDERAL, BIENIO, 2)

    def test_periodo_estadual_nao_deve_conter_votacoes_de_dois_mandatos(self):
        self._test_periodos_em_duas_datas(2010, 2011, ESTADUAL, BIENIO, 2)

    def test_periodo_federal_deve_estar_em_um_mandato(self):
        self._test_periodos_em_duas_datas(2011, 2012, FEDERAL, BIENIO, 1)

    def test_inicio_de_periodo_federal_deve_coincidir_com_inicio_mandato(self):
        self._test_periodos_em_duas_datas(2012, 2013, FEDERAL, BIENIO, 2)

    def _test_periodos_em_duas_datas(self, ano_ini, ano_fim, esfera,
                                     periodicidade, expected_periodos_len):
        UMA_DATA = datetime.date(ano_ini, 02, 02)
        OUTRA_DATA = datetime.date(ano_fim, 10, 02)
        votacoes = modelagem.models.Votacao.objects.all()
        half = len(votacoes) / 2
        datas_originais = {}  # votacao.id => data
        esfera_original = self.conv.esfera
        self.conv.esfera = esfera
        for i in range(0, half):
            v = votacoes[i]
            datas_originais[v.id] = v.data
            v.data = UMA_DATA
            v.save()
        for i in range(half, len(votacoes)):
            v = votacoes[i]
            datas_originais[v.id] = v.data
            v.data = OUTRA_DATA
            v.save()
        retriever = modelagem.utils.PeriodosRetriever(self.conv, periodicidade)
        periodos = retriever.get_periodos()
        self.assertEquals(len(periodos), expected_periodos_len)
        self._restore(esfera_original, votacoes, datas_originais)

    def _restore(self, esfera_original, votacoes, datas_originais):
        self.conv.esfera = esfera_original
        self.conv.save()
        for v in votacoes:
            v.data = datas_originais[v.id]
            v.save()

    def test_casa_legislativa_periodos_sem_lista_votacoes(self):
        casa_nova = modelagem.models.CasaLegislativa(nome="Casa Nova")
        retriever = modelagem.utils.PeriodosRetriever(casa_nova, modelagem.models.ANO)
        periodos = retriever.get_periodos()
        self.assertEquals(len(periodos), 0)

    def test_data_inicio_prox_periodo_mes_menor_12(self):
        retriever = modelagem.utils.PeriodosRetriever(self.conv, modelagem.models.MES)
        data_inicio_periodo = datetime.date(1989, 2, 1)
        resultado = retriever._data_inicio_prox_periodo(data_inicio_periodo)
        self.assertEquals(resultado, datetime.date(1989, 3, 1))

    def test_data_inicio_prox_periodo_mes_igual_a_12(self):
        retriever = modelagem.utils.PeriodosRetriever(self.conv, modelagem.models.MES)
        data_inicio_periodo = datetime.date(1989, 12, 1)
        resultado = retriever._data_inicio_prox_periodo(data_inicio_periodo)
        self.assertEquals(resultado, datetime.date(1990, 1, 1))

    def test_data_inicio_prox_periodo_semestre_com_inicio_mes_menor_7(self):
        retriever = modelagem.utils.PeriodosRetriever(self.conv, modelagem.models.SEMESTRE)
        data_inicio_periodo = datetime.date(1989, 1, 1)
        resultado = retriever._data_inicio_prox_periodo(data_inicio_periodo)
        self.assertEquals(resultado, datetime.date(1989, 7, 1))

    def test_data_inicio_prox_periodo_semestre_com_inicio_mes_maior_igual_7(self):
        retriever = modelagem.utils.PeriodosRetriever(self.conv, modelagem.models.SEMESTRE)
        data_inicio_periodo = datetime.date(1989, 7, 1)
        resultado = retriever._data_inicio_prox_periodo(data_inicio_periodo)
        self.assertEquals(resultado, datetime.date(1990, 1, 1))

    def test_data_inicio_prox_periodo_ano(self):
        retriever = modelagem.utils.PeriodosRetriever(self.conv, modelagem.models.ANO)
        data_inicio_periodo = datetime.date(1989, 2, 1)
        resultado = retriever._data_inicio_prox_periodo(data_inicio_periodo)
        self.assertEquals(resultado, datetime.date(1990, 1, 1))
        
    def test_data_inicio_prox_periodo_bienio(self):
        retriever = modelagem.utils.PeriodosRetriever(self.conv, modelagem.models.BIENIO)
        data_inicio_periodo = datetime.date(1989, 7, 1)
        resultado = retriever._data_inicio_prox_periodo(data_inicio_periodo)
        self.assertEquals(resultado, datetime.date(1991, 1, 1))

    def test_data_inicio_prox_periodo_quadrienio(self):
        retriever = modelagem.utils.PeriodosRetriever(self.conv, modelagem.models.QUADRIENIO)
        data_inicio_periodo = datetime.date(1989, 7, 1)
        resultado = retriever._data_inicio_prox_periodo(data_inicio_periodo)
        self.assertEquals(resultado, datetime.date(1993, 1, 1))
        

class StringUtilsTest(TestCase):

    def test_transforma_texto_em_lista_de_string_texto_vazio(self):
        lista_string = modelagem.utils.StringUtils.transforma_texto_em_lista_de_string(
            "")
        self.assertEquals(0, len(lista_string))

    def test_transforma_texto_em_lista_de_string_texto_nulo(self):
        lista_string = modelagem.utils.StringUtils.transforma_texto_em_lista_de_string(
            None)
        self.assertEquals(0, len(lista_string))

    def test_transforma_texto_em_lista_de_string(self):
        lista_string = modelagem.utils.StringUtils.transforma_texto_em_lista_de_string(
            "educação, saúde, desmatamento")
        self.assertEquals(3, len(lista_string))
        self.assertEquals("educação", lista_string[0])
        self.assertEquals("saúde", lista_string[1])
        self.assertEquals("desmatamento", lista_string[2])
