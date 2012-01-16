# -*- coding: utf-8 -*-
#suportado apenas em python 2
import partidos
import numpy
import pca
import algebra

def semelhanca_pca(partidos, vetores):

  # necessário normalizar?
  nvetores = [] # cada linha é um partido, e cada coluna uma votação
  for v in vetores:
    nvetores.append(algebra.normaliza(v))

  #PCA: linhas são amostras e colunas variáveis
  matriz =  numpy.array(nvetores)
  matriz = matriz.transpose() #Aqui nossas amostras são as votações e as variáveis são os partidos
  p = pca.PCA(matriz)
  return p.pc()
