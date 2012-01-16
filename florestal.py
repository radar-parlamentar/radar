#!/usr/bin/python3.2
# -*- coding: utf-8 -*-
#
# Pequeno script que baixa a votação do código florestal
# Mostra votos agregados por partido
# Se tiver flag -uf, mostra votos por UF
import camaraws
import sys

# código florestal
# http://www.camara.gov.br/proposicoesWeb/fichadetramitacao?idProposicao=17338
prop_id = '17338'
tipo = 'pl'
num = '1876'
ano = '1999'
prop = camaraws.obter_votacao(prop_id, tipo, num, ano) 

print(prop)
for votacao in prop.votacoes:
  print('************')
  print(votacao)
  if (len(sys.argv)>1 and sys.argv[1] == '-uf'):
    dic = votacao.por_uf()
  else:
    dic = votacao.por_partido()
  for key, voto in dic.items():
    print("%s: \t Sim: %s \t Não: %s \t Abstenções: %s" % (key, voto.sim, voto.nao, voto.abstencao))

