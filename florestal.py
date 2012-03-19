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

"""Script florestal 
Baixa a votação do código florestal
Mostra votos agregados por partido
Se tiver flag -uf, mostra votos por UF
"""

from __future__ import unicode_literals
import camaraws
import sys

# código florestal
# http://www.camara.gov.br/proposicoesWeb/fichadetramitacao?idProposicao=17338
tipo = 'pl'
num = '1876'
ano = '1999'
prop = camaraws.obter_votacao(tipo, num, ano) 

txt = str(prop)
print type(txt)
#print prop
for votacao in prop.votacoes:
  print('************')
  print(votacao)
  if (len(sys.argv)>1 and sys.argv[1] == '-uf'):
    dic = votacao.por_uf()
  else:
    dic = votacao.por_partido()
  for key, voto in dic.items():
    sim = voto.sim
    nao = voto.nao
    abst = voto.abstencao
    print("%s: \t Sim: %s \t Não: %s \t Abstenções: %s" % (key, sim, nao, abst))

