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
from . import models
import json

def get_json_proposicao(proposicao):
#    fields = ['id_prop', 'sigla', 'numero', 'ano', 'ementa', 'descricao', 'indexacao', 'data_apresentacao', 'situacao']
    fields = ['id_prop', 'sigla', 'numero', 'ano']
    proposicao_serial = {}
    proposicao_serial['nome'] = proposicao.nome()
    for field in fields:
        proposicao_serial[field] = getattr(proposicao, field)
    votacoes = models.Votacao.objects.filter(proposicao=proposicao)
    proposicao_serial['votacoes'] = get_votacoes_serial(votacoes)
    return json.dumps(proposicao_serial)


def get_votacoes_serial(votacoes):
    votacoes_serial = []
    # TODO...
    return votacoes_serial

def main():
    p = models.Proposicao.objects.filter(casa_legislativa__nome_curto='cdep')[147]
    json = get_json_proposicao(p)
    print json
 


