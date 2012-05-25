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

"""Com este módulo podemos salvar os resultados das análises no banco de dados.
Assim não precisamos refazer todas as contas a cada requisição
"""

from django.db import models
from modelagem.models import Partido


class PosicaoPartido(models.Model):

    partido = models.ForeignKey(Partido)
    x = models.FloatField()
    y = models.FloatField()


class PeriodoAnalise(models.Model):

    periodo = models.CharField(max_length=100)
    posicoes = models.ManyToManyField(PosicaoPartido)


class AnaliseJSON(models.Model):

    inicio = models.DateField()
    fim = models.DateField()
    periodos = models.ManyToManyField(PeriodoAnalise)


class TamanhoPartido(models.Model):

    partido = models.ForeignKey(Partido)
    tamanho = models.IntegerField()

    
