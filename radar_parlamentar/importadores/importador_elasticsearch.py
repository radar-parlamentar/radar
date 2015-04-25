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

from __future__ import unicode_literals
import modelagem.models as models
import json
from elasticsearch import Elasticsearch

class RadarParlamentarIndex():
    def __init__(self,votacao, proposicao,casa_legislativa):
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
        if proposicao.data_apresentacao != None:
            self.proposicao_data_apresentacao = proposicao.data_apresentacao.strftime("%Y-%m-%d")
        self.proposicao_situacao = proposicao.situacao
        self.casa_legislativa_id = casa_legislativa.id
        self.casa_legislativa_nome = casa_legislativa.nome
        self.casa_legislativa_nome_curto = casa_legislativa.nome_curto
        self.casa_legislativa_esfera = casa_legislativa.esfera
        self.casa_legilativa_local = casa_legislativa.local
        self.casa_legislativa_atualizacao = casa_legislativa.atualizacao.strftime("%Y-%m-%d") 

def gerar_json_radar():
    list_json = []
    votacoes = models.Votacao.objects.all()
    for votacao in votacoes:
        proposicao = votacao.proposicao
        casa_legislativa = proposicao.casa_legislativa
        radarParlamentarIndex = RadarParlamentarIndex(votacao,proposicao,casa_legislativa)
        list_json.append(radarParlamentarIndex.__dict__)
    return list_json

def enviar_para_elasticsearch(list_json):
    host = "ec2-52-10-251-45.us-west-2.compute.amazonaws.com"
    port = "9200"
    es = Elasticsearch([{"host":host,"port":port}])
    for item in list_json:
        for key in item.keys():
            if item[key] == "":
                item.pop(key)
    	list_es = json.dumps(item)
    	es.index(index="radar_parlamentar",doc_type="radar",body=item)

def main():
   enviar_para_elasticsearch(gerar_json_radar())
