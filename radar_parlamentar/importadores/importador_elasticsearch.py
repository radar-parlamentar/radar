# !/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Guilherme Januário, Diego Rabatone
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


import modelagem.models as models
from elasticsearch import Elasticsearch
from django.conf import settings
from elasticsearch.client import IndicesClient

ELASTIC_SEARCH_ADDRESS_DEFAULT = {'host': 'localhost', 'port': '9200'}
ELASTIC_SEARCH_INDEX_DEFAULT = "radar_parlamentar"

"""
    Esse modulo e responsavel por transportar as informacoes que estao no banco
    de dados do radar parlamentar para uma instancia de Elasticsearch.
    E feita a coleta atraves dos modelos do django,
    conversao desse modelo para um objeto RadarParlamentarIndex e, por fim,
    o envio desse objeto para o Elasticsearch.
"""


class RadarParlamentarIndex():

    def __init__(self, votacao, proposicao, casa_legislativa):
        self.votacao_id = votacao.id
        self.votacao_id_vot = votacao.id_vot
        self.votacao_descricao = votacao.descricao
        self.votacao_data = votacao.data.strftime("%Y-%m-%d")
        self.votacao_resultado = votacao.resultado
        self.proposicao_id = proposicao.id
        self.proposicao_id_prop = proposicao.id_prop
        self.proposicao_sigla = proposicao.sigla
        self.proposicao_numero = proposicao.numero
        self.proposicao_ano = proposicao.ano
        self.proposicao_ementa = proposicao.ementa
        self.proposicao_descricao = proposicao.descricao
        self.proposicao_indexacao = proposicao.indexacao
        if proposicao.data_apresentacao is not None:
            self.proposicao_data_apresentacao = \
                proposicao.data_apresentacao.strftime("%Y-%m-%d")
        self.proposicao_situacao = proposicao.situacao
        self.casa_legislativa_id = casa_legislativa.id
        self.casa_legislativa_nome = casa_legislativa.nome
        self.casa_legislativa_nome_curto = casa_legislativa.nome_curto
        self.casa_legislativa_esfera = casa_legislativa.esfera
        self.casa_legilativa_local = casa_legislativa.local

"""
    construcao do modelo json baseado no modelo do banco de dados
"""


def gerar_json_radar():
    list_json = []
    votacoes = models.Votacao.objects.all()
    for votacao in votacoes:
        proposicao = votacao.proposicao
        casa_legislativa = proposicao.casa_legislativa
        radarParlamentarIndex = RadarParlamentarIndex(
            votacao, proposicao, casa_legislativa)
        list_json.append(radarParlamentarIndex.__dict__)
    return list_json


"""
    faz a abertura de uma conexao com o ElasticSearch
"""


def conectar_em_elastic_search():
    elastic_search_address = None
    try:
        elastic_search_address = settings.ELASTIC_SEARCH_ADDRESS
    except AttributeError:
        elastic_search_address = ELASTIC_SEARCH_ADDRESS_DEFAULT
    es = Elasticsearch([elastic_search_address])
    return es

"""
    remove o indice do Elasticsearch
    (o indice de elasticsearch e analogo a uma tabela em um SGBD)
"""


def remover_indice(nome_indice):
    es = conectar_em_elastic_search()
    client_indice = IndicesClient(es)
    if client_indice.exists(index=[nome_indice]):
        client_indice.delete(nome_indice)


def criar_indice(nome_indice):
    config_settings = """
{
"settings": {
    "analysis": {
        "analyzer": {
            "my_analyzer": {
                "tokenizer": "standard",
                "filter": ["standard", "pt_BR", "lowercase","portuguese_stop",
                           "asciifolding"]
        }
        },
        "filter": {
            "my_stemmer": {
                "type": "stemmer",
            "name": "brazilian"
            },
             "portuguese_stop": {
                 "type":       "stop",
                 "stopwords":  "_brazilian_"
            },
             "pt_BR": {
                 "type":       "hunspell",
                 "language":  "pt_BR"
            }
        }
    }
}
}
"""
    config_mapping = """
{
  "radar" : {
    "_all" : {"enabled" : true, "analyzer": "my_analyzer"},
    "properties" : {
      "casa_legilativa_local" : {
        "type" : "string"
      },
      "casa_legislativa_esfera" : {
        "type" : "string"
      },
      "casa_legislativa_id" : {
        "type" : "long"
      },
      "casa_legislativa_nome" : {
        "type" : "string"
      },
      "casa_legislativa_nome_curto" : {
        "type" : "string"
      },
      "proposicao_ano" : {
        "type" : "string"
      },
      "proposicao_data_apresentacao" : {
        "type" : "date",
        "format" : "dateOptionalTime"
      },
      "proposicao_descricao" : {
        "type" : "string"
      },
      "proposicao_ementa" : {
        "type" : "string",
        "analyzer": "my_analyzer"
      },
      "proposicao_id" : {
        "type" : "long"
      },
      "proposicao_id_prop" : {
        "type" : "string"
      },
      "proposicao_indexacao" : {
        "type" : "string",
        "analyzer": "my_analyzer"
      },
      "proposicao_numero" : {
        "type" : "string"
      },
      "proposicao_sigla" : {
        "type" : "string"
      },
      "proposicao_situacao" : {
        "type" : "string"
      },
      "votacao_data" : {
        "type" : "date",
        "format" : "dateOptionalTime"
      },
      "votacao_descricao" : {
        "type" : "string",
        "analyzer": "my_analyzer"
      },
      "votacao_id" : {
        "type" : "long"
      },
      "votacao_id_vot" : {
        "type" : "string"
      },
      "votacao_resultado" : {
        "type" : "string"
      }
}}}
"""
    es = conectar_em_elastic_search()
    client_indice = IndicesClient(es)
    client_indice.create(index=nome_indice, body=config_settings)
    client_indice.put_mapping(
        index=nome_indice, doc_type="radar", body=config_mapping)

"""
    envia o json do modelo do radar para o elasticSearch
"""


def enviar_para_elasticsearch(list_json, nome_indice):
    es = conectar_em_elastic_search()
    for item in list_json:
        for key in list(item.keys()):
            if item[key] == "":
                item.pop(key)
        es.index(index=nome_indice, doc_type="radar", body=item)


def obter_indice():
    try:
        indice = settings.ELASTIC_SEARCH_INDEX
    except AttributeError:
        indice = ELASTIC_SEARCH_INDEX_DEFAULT
    return indice


def main():
    indice = obter_indice()
    remover_indice(indice)
    criar_indice(indice)
    enviar_para_elasticsearch(gerar_json_radar(), indice)
