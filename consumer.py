#!/usr/bin/python3.2
# -*- coding: utf-8 -*-
#
# Pequeno script que baixa a votação do código florestal
import camaraws

tipo = 'pl'
num = '1876'
ano = '1999'
prop = camaraws.obter_votacao(tipo, num, ano)

print(prop)
for vot in prop.votacoes:
  print(vot)
  for dep in vot.deputados:
    print(dep)

