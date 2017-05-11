# coding=utf8

# Copyright (C) 2012, Arthur Del Esposte, Leonardo Leite, Aline Santos,
# Gabriel Augusto, Thallys Martins, Thatiany Lima, Winstein Martins,
# Eduardo Kuroda.
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
from modelagem import models
from elasticsearch import Elasticsearch
from django.conf import settings
import logging

logger = logging.getLogger("radar")

# TODO: AND no elasticsearch
# es.search(index=settings.ELASTIC_SEARCH_INDEX,
#     q="casa_legislativa_nome_curto:cmsp AND Educação)
# não retorna a votação 204
# Mas
# res = es.search(index=settings.ELASTIC_SEARCH_INDEX,
#      q="casa_legislativa_nome_curto:cmsp AND Educação AND
#      votacao_data:[2013-01-01 TO 2014-01-01]")
# retorna a votação 204!
# Como pode um "AND" a mais retornar mais coisas?

# TODO: Que fazer quando o ElasticSearch não retorna resultados?


class LuceneQueryBuilder():

    def __init__(self, nome_curto_casa_legislativa, periodo_casa_legislativa,
                 palavras_chave):
        self.nome_curto_casa_legislativa = nome_curto_casa_legislativa
        self.periodo_casa_legislativa = periodo_casa_legislativa
        self.palavras_chaves = palavras_chave

    def build(self):
        return "%s AND %s AND %s" % (self._build_nome_curto(),
                                     self._build_palavras_chaves(),
                                     self._build_range_data())

    def _build_nome_curto(self):
        return "casa_legislativa_nome_curto:%s" % \
            self.nome_curto_casa_legislativa

    def _build_palavras_chaves(self):
        return " AND ".join(self.palavras_chaves)

    def _build_range_data(self):
        return "votacao_data:[%s TO %s]" % (
            self.periodo_casa_legislativa.ini.isoformat(),
            self.periodo_casa_legislativa.fim.isoformat())

class FiltroVotacao(TestCase):

    """Filtra votações pelos campos:
        * votacao.descricao
        * proposicao.ementa
        * proposicao.descricao
        * proposicao.indexacao
    """

    def __init__(self, casa_legislativa, periodo_casa_legislativa,
                 palavras_chave):
        """Argumentos:
            casa_legislativa -- objeto do tipo CasaLegislativa;
            somente votações desta casa serão filtradas.
            periodo_casa_legislativa -- objeto do tipo PeriodoCasaLegislativa;
            somente votações deste período serão filtradas.
            palavras_chave -- lista de strings para serem usadas na filtragem
            das votações.
        """
        self.casa_legislativa = casa_legislativa
        self.periodo_casa_legislativa = periodo_casa_legislativa
        self.palavras_chaves = palavras_chave
        self.votacoes = []

    def filtra_votacoes(self):
        if not self.palavras_chaves:
            self.votacoes = models.Votacao.por_casa_legislativa(
                self.casa_legislativa,
                self.periodo_casa_legislativa.ini,
                self.periodo_casa_legislativa.fim)
            return self.votacoes

        es = Elasticsearch([settings.ELASTIC_SEARCH_ADDRESS])
        query_builder = LuceneQueryBuilder(self.casa_legislativa.nome_curto,
                                           self.periodo_casa_legislativa,
                                           self.palavras_chaves)
        query = query_builder.build()
        res = es.search(
            index=settings.ELASTIC_SEARCH_INDEX, q=query, fields="votacao_id")
        logger.info(res)
        votacoes_ids = [
            e["fields"]["votacao_id"][0] for e in res["hits"]["hits"]]
        self.votacoes = models.Votacao.objects.filter(id__in=votacoes_ids)
        return self.votacoes


class FiltroChefesExecutivo(TestCase):

    """Filtra chefes executivos pelo período do mandato e pela casa """

    def __init__(self, casa_legislativa, periodo_casa_legislativa):
        """Argumentos:
            casa_legislativa -- objeto do tipo CasaLegislativa;
            somente chefes executivos desta casa serão filtrados.
            periodo_casa_legislativa -- objeto do tipo PeriodoCasaLegislativa;
            somente chefes executivos deste período serão filtrados.
        """
        self.casa_legislativa = casa_legislativa
        self.periodo_casa_legislativa = periodo_casa_legislativa
        self.chefes_executivos = []

    def filtra_chefes_executivo(self):
        self.chefes_executivo = models.ChefeExecutivo.por_casa_legislativa_e_periodo(
            self.casa_legislativa,
            self.periodo_casa_legislativa.ini,
            self.periodo_casa_legislativa.fim)
        return self.chefes_executivo

