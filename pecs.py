#!/usr/bin/python3.2
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

"""Script pecs
Baixa as PECs de 2011
Mostra votos agregados por partido
"""

import camaraws

pecs = []

# PEC da música (isenção fiscal para músicas e artistas brasileiros)
# http://www.camara.gov.br/proposicoesWeb/fichadetramitacao?idProposicao=357094
# (a primeira vista me parece absurdo que algo assim deva estar na constituição)
prop_id = '357094'
tipo = 'pec'
num = '98'
ano = '2007'
pecs.append(camaraws.obter_votacao(prop_id, tipo, num, ano))
# prorroga a vigência da DRU até 31 de dezembro de 2015
# http://www.camara.gov.br/proposicoesWeb/fichadetramitacao?idProposicao=513496
prop_id = '513496'
tipo = 'pec'
num = '61'
ano = '2011'
pecs.append(camaraws.obter_votacao(prop_id, tipo, num, ano))

for prop in pecs:
  print(prop)
  for votacao in prop.votacoes:
    print('************')
    print(votacao)
    dic = votacao.por_partido()
    for partido, voto in dic.items():
      print("%s: \t Sim: %s \t Não: %s \t Abstenções: %s" % (partido, voto.sim, voto.nao, voto.abstencao))
  print('=================================================================================')
