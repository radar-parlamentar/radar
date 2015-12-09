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

class FiltroVotacaoTest(TestCase):

    def test_build_query_to_elaslicSearch(self):
        nome_curto = "cmsp"
        ini = date(2000,1,1)
        fim = date(2010,1,1)
        periodo = models.PeriodoCasaLegislativa(ini,fim)
        palavras_chaves = ["Educação","Professor","Escola"]
        query_builder = filtro.LuceneQueryBuilder(nome_curto, periodo, palavras_chaves)
        query = query_builder.build()
        query_esperada = 'casa_legislativa_nome_curto:cmsp AND Educação AND Professor AND Escola AND votacao_data:[2000-01-01 TO 2010-01-01]'
        self.assertEquals(query, query_esperada)









