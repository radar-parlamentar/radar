# coding=utf8

# Copyright (C) 2016, Leonardo Leite
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
from django.utils.dateparse import parse_datetime
from . import models
import json


class ProposicaoSerializer():

    def __init__(self):
        self.partidos_serial = {}

    def get_json_proposicao(self, proposicao):
    #    fields = ['id_prop', 'sigla', 'numero', 'ano', 'ementa', 'descricao', 'indexacao', 'data_apresentacao', 'situacao']
        fields = ['id_prop', 'sigla', 'numero', 'ano', 'descricao', 'ementa']
        proposicao_serial = {}
        proposicao_serial['nome'] = proposicao.nome()
        for field in fields:
            proposicao_serial[field] = getattr(proposicao, field)
        votacoes = models.Votacao.objects.filter(proposicao=proposicao)
        proposicao_serial['votacoes'] = self.get_votacoes_serial(votacoes)
        proposicao_serial['partidos'] = self.partidos_serial
        return json.dumps(proposicao_serial)

    def get_votacoes_serial(self, votacoes):
        fields = ['id_vot', 'descricao', 'resultado']  # TODO
        votacoes_serial = []
        for votacao in votacoes:
            votacao_serial = {}
            votacao_serial['data'] = votacao.data.strftime('%d/%m/%Y')
            for field in fields:
                votacao_serial[field] = getattr(votacao, field)
            votos = votacao.votos()
            votacao_serial['parlamentares'] = \
                self.get_parlamentares_serial(votos)
            votacoes_serial.append(votacao_serial)
        return votacoes_serial

    def get_parlamentares_serial(self, votos):
        parlamentares_serial = []
        for voto in votos:
            parlamentar_serial = {
               'voto': voto.opcao,
               'nome': voto.parlamentar.nome,
               'id_partido': voto.parlamentar.partido.id,
            }
            self.add_in_partidos_serial(voto.parlamentar.partido)
            parlamentares_serial.append(parlamentar_serial)
        return parlamentares_serial

    def add_in_partidos_serial(self, partido):
        self.partidos_serial[partido.id] = {
            'nome': partido.nome,
            'numero': partido.numero,
            'cor': partido.cor
        }


def main():
    p = models.Proposicao.objects.filter(casa_legislativa__nome_curto='cmsp')[0]
    json = get_json_proposicao(p)
    print json

