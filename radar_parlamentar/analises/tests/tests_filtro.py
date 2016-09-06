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
from datetime import date
from importadores import conv

def get_periodo_casa_legislativa():
    ini = date(2000,1,1)
    fim = date(2010,1,1)
    periodo = models.PeriodoCasaLegislativa(ini,fim) 
    return periodo



class FiltroVotacaoTest(TestCase):

    def test_build_query_to_elaslicSearch(self):
        nome_curto = "cmsp"
        periodo = get_periodo_casa_legislativa()
        palavras_chaves = ["Educação","Professor","Escola"]
        query_builder = filtro.LuceneQueryBuilder(nome_curto, periodo, palavras_chaves)
        query = query_builder.build()
        query_esperada = 'casa_legislativa_nome_curto:cmsp AND Educação AND Professor AND Escola AND votacao_data:[2000-01-01 TO 2010-01-01]'
        self.assertEquals(query, query_esperada)

class FiltroChefeExecutivoTest(TestCase):

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
        self.periodo = get_periodo_casa_legislativa()
        self.partido = models.Partido.objects.get(id=1)

        # Chefe no período testado
        self.chefe = models.ChefeExecutivo(nome="Luiz Inacio Pierre da Silva", genero="M", partido = self.partido,
                                    mandato_ano_inicio = 2006, mandato_ano_fim = 2010)
        self.chefe.save()
        self.chefe.casas_legislativas.add(self.casa)
        
        # Chefe no período testado
        self.chefe2 = models.ChefeExecutivo(nome="Ferdinand Henry Cardoso", genero="M", partido = self.partido,
                                    mandato_ano_inicio = 2002, mandato_ano_fim = 2006)
        self.chefe2.save()
        self.chefe2.casas_legislativas.add(self.casa)

        # Chefe fora do período testado
        self.chefe3 = models.ChefeExecutivo(nome="Dilmé Rousseffé", genero="F", partido = self.partido,
                                    mandato_ano_inicio = 2012, mandato_ano_fim = 2014)
        self.chefe3.save()
        self.chefe3.casas_legislativas.add(self.casa)
        

    def test_filtra_chefes_executivo(self):
        filtro_chefe = filtro.FiltroChefesExecutivo(self.casa, self.periodo)
        result = filtro_chefe.filtra_chefes_executivo()
        expected = "Presidente: " + self.chefe.nome + " - " + self.partido.nome
        self.assertEquals(unicode(result[0]), expected)

    def test_filtra_chefes_executivo_varios_chefes(self):
        filtro_chefe = filtro.FiltroChefesExecutivo(self.casa, self.periodo)
        result = filtro_chefe.filtra_chefes_executivo()
        expected_chefe_1 = "Presidente: " + self.chefe.nome + " - " + self.partido.nome
        self.assertEquals(unicode(result[0]), expected_chefe_1)
        expected_chefe_2 = "Presidente: " + self.chefe2.nome + " - " + self.partido.nome
        self.assertEquals(unicode(result[1]), expected_chefe_2)

    def test_filtra_chefes_executivo_com_chefes_de_outros_periodos(self):

        filtro_chefe = filtro.FiltroChefesExecutivo(self.casa, self.periodo)
        result = filtro_chefe.filtra_chefes_executivo()
    
        chefes_no_periodo = 2
        self.assertEquals(len(result), chefes_no_periodo)


