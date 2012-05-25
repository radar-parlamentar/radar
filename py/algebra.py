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

"""Módulo algebra -- possui funcões de álgebra vetorial

Funcões: 
norma -- calcula a norma de um vetor
normaliza -- calcula um vetor normalizado no mesmo sentido e direcão do vetor fornecido
prod_escalar -- calcula o produto escalar entre dois vetores         
"""

import math

def norma(vetor):
  """Calcula a norma de um vetor (também chamada de módulo ou tamanho)
  Argumentos:
  vetor -- uma lista contendo valores reais

  Retorna:
  A norma do vetor, que é a raiz quadrada da soma dos quadrados de cada elemento do vetor
  """
  sum = 0
  for v_i in vetor:
    sum += v_i*v_i
  return math.sqrt(sum)

def normaliza(vetor):
  """Calcula um vetor normalizado no mesmo sentido e direcão do vetor fornecido
  Argumentos:
  vetor -- uma lista contendo valores reais

  Retorna:
  Uma lista representando um vetor normalizado (vn), calculado como vn_i = vetor_i / norma(vetor)  
  """
  normalizado = []
  n = norma(vetor)
  for v_i in vetor:
    normalizado.append(v_i / n)
  return normalizado

def prod_escalar(vetor1, vetor2):
  """Calcula o produto escalar entre dois vetores
  Argumentos:
  vetor1, vetor2 -- listas contendo valores reais

  Retorna:
  O produto escalar vetor1.vetor2, dado pela soma dos produtos dos elementos dos vetores
  Exemplo: v1=[a,b,c], v2=[x,y,z] => v1.v2 = a*x + b*y +c*z
  """
  sum = 0
  for v1, v2 in zip(vetor1, vetor2):
    sum += v1*v2
  return sum
