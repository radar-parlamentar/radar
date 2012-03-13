# -*- coding: utf-8 -*-
#suportado apenas em python 2

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

import numpy
import pca
import algebra

def semelhanca_pca(vetores):

  #PCA: linhas são amostras e colunas variáveis
  # vamos fazer linhas = partidos e colunas = votações
  # devemos também centralizar os valores
  # como todos os valores \in [0,1], não precisamos ajustar a escala
  matriz =  numpy.array(vetores)
  matriz -= matriz.mean(axis=0) # centralização 
  p = pca.PCA(matriz)
  return p


