#!/usr/bin/python
# -*- coding: utf-8 -*-

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

"""Script vetores -- imprime os vetores de votações"""

import proposicoes
import camaraws
import partidos
import sys
from partidos import PARTIDOS

length = len(PARTIDOS)

# recuperação das proposições
votadas = proposicoes.parse() # identificação das proposições votadas em 2011
proposicoes = [] # listagem das proposições com suas respectivas votações
n_vot = 0 # total de votações analisadas
for prop in votadas:
    print('Analisando proposição ' + prop['id'])
    prop_vot = camaraws.obter_votacao(prop['tipo'], prop['num'], prop['ano']) # obtêm votação do web service
    n_vot += len(prop_vot.votacoes)
    proposicoes.append(prop_vot)

for p in PARTIDOS:
    v = partidos.vetor_votacoes(p, proposicoes)
    print("%s\n%s" % (p, v))
