#!/usr/bin/python3.2
# -*- coding: utf-8 -*-
#
# Salva os vetores de votação em um arquivo
# Fiz isso porque o script pra baixar as votações só funciona com python3
# e a análise PCA só com python2, pq depende do numpy
# Uma solução alternativa seria fazer o download utilizar o python 2

import proposicoes
import camaraws
import partidos
import sys

PARTIDOS = ['PT', 'PSDB', 'PV', 'PSOL', 'PCdoB', 'PP', 'PR', 'DEM', 'PMDB', 'PSC', 'PTB', 'PDT', 'PSB', 'PSB', 'PPS', 'PRB']
length = len(PARTIDOS)

# recuperação das proposições
votadas = proposicoes.parse() # identificação das proposições votadas em 2011
proposicoes = [] # listagem das proposições com suas respectivas votações
n_vot = 0 # total de votações analisadas
for prop in votadas:
  print('Analisando proposição ' + prop['id'])
  prop_vot = camaraws.obter_votacao(prop['id'], prop['tipo'], prop['num'], prop['ano']) # obtêm votação do web service
  n_vot += len(prop_vot.votacoes)
  proposicoes.append(prop_vot)

for p in PARTIDOS:
  v = partidos.vetor_votacoes(p, proposicoes)
  print("%s\n%s" % (p, v))
