#!/usr/bin/python3.2
# -*- coding: utf-8 -*-
#
# Verifica a diferença entre dois partidos baseado nas proposições votadas em 2011

import proposicoes
import camaraws
import partidos
import sys

PARTIDOS = ['PT', 'PSDB', 'PV', 'PSOL', 'PCdoB', 'PP', 'PR', 'DEM', 'PMDB', 'PSC', 'PTB', 'PDT', 'PSB', 'PSB', 'PPS', 'PRB']
# PRTB, PRP, PMN, PSL, PHS deram problema, pois não aparecem em algumas votações
# TODO: o que fazer nesses casos?
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

# análise das semelhanças
print('Análise baseada em %d votações de %d proposições, votadas na camâra em 2011' % (n_vot, len(votadas)))
for i in range(0,length):
  for j in range(i+1,length):
    sem = partidos.semelhanca(PARTIDOS[i], PARTIDOS[j], proposicoes)
    print('Semelhança entre %s e %s = %.2f%s' % (PARTIDOS[i], PARTIDOS[j], sem*100, '%'))

