#!/usr/bin/python3.2
# -*- coding: utf-8 -*-
#
# Pequeno script que baixa a votação do código florestal
# Mostra votos agregados por partido
import camaraws

# prorroga a vigência da DRU até 31 de dezembro de 2015
# http://www.camara.gov.br/proposicoesWeb/fichadetramitacao?idProposicao=513496
prop_id = '513496'
tipo = 'pec'
num = '61'
ano = '2011'
# código florestal
# http://www.camara.gov.br/proposicoesWeb/fichadetramitacao?idProposicao=17338
prop_id = '17338'
tipo = 'pl'
num = '1876'
ano = '1999'
prop = camaraws.obter_votacao(prop_id, tipo, num, ano) 

print(prop)
for votacao in prop.votacoes:
  print(votacao)
  dic = votacao.por_partido()
  for partido, voto in dic.items():
    print("%s: \t Sim: %s \t Não: %s \t Abstenções: %s" % (partido, voto.sim, voto.nao, voto.abstencao))
  print('************')
