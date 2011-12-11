#!/usr/bin/python3.2
# -*- coding: utf-8 -*-
#
# Pequeno script que baixa a votação do código florestal
# Mostra votos agregados por partido
import camaraws

tipo = 'pl'
num = '1876'
ano = '1999'
prop = camaraws.obter_votacao(tipo, num, ano)

print(prop)
print(prop.votacoes[1])
dic = prop.votacoes[1].por_partido()
for partido, voto in dic.items():
  print("%s: \t Sim: %s \t Não: %s \t Abstenções: %s" % (partido, voto.sim, voto.nao, voto.abstencao))
