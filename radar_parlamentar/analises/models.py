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

"""Com este módulo podemos salvar os resultados das análises no banco de dados.
Assim não precisamos refazer todas as contas a cada requisição
"""

from django.db import models
from modelagem.models import Partido
from modelagem.models import CasaLegislativa
from modelagem.models import Votacao

#deprecated (serve para o json antigo funcionar)
class PosicaoPartido(models.Model):

    partido = models.ForeignKey(Partido)
    x = models.FloatField()
    y = models.FloatField()
    tamanho = models.IntegerField()
    presenca = models.IntegerField()

#deprecated (serve para o json antigo funcionar)
class AnaliseTemporal(models.Model):

    hash_id = models.CharField(max_length=32,primary_key=True)
    casa_legislativa = models.ForeignKey(CasaLegislativa, null=True)
    periodicidade = models.CharField(max_length=15)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    votacoes = models.ManyToManyField(Votacao)
    partidos = models.ManyToManyField(Partido)
    area_total = models.FloatField()

#deprecated (serve para o json antigo funcionar)
class AnalisePeriodo(models.Model):

    casa_legislativa = models.ForeignKey(CasaLegislativa, null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    #periodo = models.CharField(max_length=100)
    #votacoes = models.ManyToManyField(Votacao)
    #partidos = models.ManyToManyField(Partido)
    posicoes = models.ManyToManyField(PosicaoPartido)
    analiseTemporal = models.ForeignKey(AnaliseTemporal)

class JsonAnaliseTemporal(models.Model):

    hash_id = models.CharField(max_length=32,primary_key=True)
    casa_legislativa = models.ForeignKey(CasaLegislativa, null=True)
    periodicidade = models.CharField(max_length=15)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    votacoes = models.ManyToManyField(Votacao)
    partidos = models.ManyToManyField(Partido)
    json = models.TextField()
