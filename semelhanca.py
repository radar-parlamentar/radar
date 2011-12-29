#!/usr/bin/python3.2
# -*- coding: utf-8 -*-
#
# Verifica a diferença entre dois partidos baseado nas proposições votadas em 2011

import proposicoes
import camaraws
import partidos
import sys

partido1 = sys.argv[1]
partido2 = sys.argv[2]

votadas = proposicoes.parse() # identificação das proposições votadas em 2011
proposicoes = [] # listagem das proposições com suas respectivas votações
n_vot = 0 # total de votações analisadas
for prop in votadas:
  print('Analisando proposição ' + prop['id'])
  prop_vot = camaraws.obter_votacao(prop['id'], prop['tipo'], prop['num'], prop['ano']) # obtêm votação do web service
#  for v in prop_vot.votacoes:
#    for d in v.deputados:
#      if (d.partido == partido1 or d.partido == partido2):
#        print(d)
  n_vot += len(prop_vot.votacoes)
  proposicoes.append(prop_vot)

sem = partidos.semelhanca(partido1, partido2, proposicoes)

print('Semelhança entre %s e %s = %.2f%s, baseado em %s votações' % (partido1, partido2, sem*100, '%', n_vot))

