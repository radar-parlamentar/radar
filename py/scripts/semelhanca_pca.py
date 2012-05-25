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

"""Script semelhanca_pca
Verifica a diferença entre os partidos 
baseado nas proposições votadas em 2011
utilizando PCA (análise de componentes primários)
"""

import partidos
import sys

partidos_list = []
vetores = []

# recuperação dos vetores de votações
name = 'resultados/vetores.txt'
vfile = open(name, 'r')
flag = 1
for line in vfile:
  if flag % 2 == 1:
    partidos_list.append(line.rstrip())
  else:
    vetores.append(eval(line))
  flag += 1

# análise das semelhanças
print('Análise PCA')
p = partidos.semelhanca_pca(vetores)
pc = p.pc()

# impressão
print "Fração da variância explicada pelas dimensões:"
for i in range(0, 4):
  print "%f " % ( p.eigen[i] / p.eigen.sum() )

print "\nCoordenadas:"
for i in range(0,len(partidos_list)):
  print "%s: [%f, %f]" % (partidos_list[i], pc[i][0], pc[i][1])
