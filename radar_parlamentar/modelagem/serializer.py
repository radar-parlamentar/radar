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

from analises.ordenacao import ordem_dos_parlamentares


class ProposicaoSerializer():

    def __init__(self):
        self.partidos_serial = {}

    def get_json_proposicao(self, proposicao):
        '''
        Recebe um objeto proposição e retorna o JSON da proposição.
        '''

        # Retorna lista ordenada de votações
        votacoes = ordem_dos_parlamentares(proposicao)

    #    fields = ['id_prop', 'sigla', 'numero', 'ano', 'ementa', 'descricao', 'indexacao', 'data_apresentacao', 'situacao']
        fields = ['id_prop', 'sigla', 'numero', 'ano', 'descricao', 'ementa']
        proposicao_serial = {}
        proposicao_serial['nome'] = proposicao.nome()
        for field in fields:
            proposicao_serial[field] = getattr(proposicao, field)
        proposicao_serial['votacoes'] = self.get_votacoes_serial(votacoes)
        proposicao_serial['partidos'] = self.partidos_serial
        return json.dumps(proposicao_serial)

    def get_votacoes_serial(self, votacoes):
        '''
        Recebe votações ordenadas e retorna JSON das votações.
        '''
        fields = ['id_vot', 'descricao', 'resultado']  # TODO
        votacoes_serial = []
        for votacao, parlamentares in votacoes:
            votacao_serial = {}
            votacao_serial['data'] = votacao.data.strftime('%d/%m/%Y')
            for field in fields:
                votacao_serial[field] = getattr(votacao, field)
            votacao_serial['parlamentares'] = self.get_parlamentares_serial(
                parlamentares,
                self.get_votos_parlamentares(votacao))
            votacoes_serial.append(votacao_serial)
        return votacoes_serial

    def get_parlamentares_serial(self, parlamentares, votos):
        '''
        Recebe a lista de parlamentares ordenados e um
        dicionário de votos e retorna o JSON dos parlamentares.
        '''
        parlamentares_serial = []
        for parlamentar in parlamentares:
            parlamentar_serial = {
                'voto': votos[parlamentar.id],
                'nome': parlamentar.nome,
                'id_partido': parlamentar.partido.id,
            }
            self.add_in_partidos_serial(parlamentar.partido)
            parlamentares_serial.append(parlamentar_serial)
        return parlamentares_serial

    def get_votos_parlamentares(self, votacao):
        '''
        Recebe uma votação e retarna um dicionário do voto
        para cada parlamentar.
        '''
        return {voto.parlamentar.id: voto.opcao for voto in votacao.votos()}

    def add_in_partidos_serial(self, partido):
        '''
        Adiciona um partido ao dicionário de partidos usados.
        '''
        self.partidos_serial[partido.id] = {
            'nome': partido.nome,
            'numero': partido.numero,
            'cor': partido.cor
        }


def main():
    p = models.Proposicao.objects.filter(casa_legislativa__nome_curto='cmsp')[0]
    json = get_json_proposicao(p)
    print json

