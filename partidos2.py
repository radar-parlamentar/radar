# -*- coding: utf-8 -*-
#suportado apenas em python 2
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
  return p.pc()


