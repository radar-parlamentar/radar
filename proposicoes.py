#!/usr/bin/python3.2
# -*- coding: utf-8 -*-
import re
import codecs
import camaraws

# PL - projeto de lei
# PLP - projeto de lei complementar
# PDC - projeto de decreto legislativo
# MPV - projeto de medida provisória
# PEC - proposta de emenda à constituição


# Parse do arquivo proposicoes.html
# Recupera uma lista com apenas a identificação das proposições (tipo número/ano, e id também)
def parse_html():
  file_name = 'recursos/proposicoes2011.htm'  # arquivo contem proposições votadas pela câmara em 2011
  prop_file = codecs.open(file_name, encoding='ISO-8859-15', mode='r')
  regexp = '<A HREF=http://.*?id=([0-9]*?)>([A-Z]*?) ([0-9]*?)/([0-9]{4}?)</A>'
  proposicoes = []
  for line in prop_file:
    res = re.search(regexp, line)
    if res:
      proposicoes.append({'id':res.group(1), 'tipo':res.group(2), 'num':res.group(3), 'ano':res.group(4)})
  return proposicoes


# Verifica qual das proposições retornam votações pelo web service da câmara
# Ou seja, sobre quais proposições poderemos fazer nossas análises de votação
def com_votacao(proposicoes): 
  votadas = []
  for prop in proposicoes:
    vot = camaraws.obter_votacao(prop['id'], prop['tipo'], prop['num'], prop['ano']) 
    if vot != None:
      votadas.append(prop)
  return votadas

#script
proposicoes = parse_html()
votadas = com_votacao(proposicoes)
print("# Documento entregue pela câmara continha %d proposições votadas em 2011" % len(proposicoes))
print("# %d proposições retornaram informações sobre suas votações pelo web service" % len(votadas))
print("# Proposições que retornaram a votação:")
for prop in votadas:
  print("%s: %s %s/%s" % (prop['id'],prop['tipo'],prop['num'],prop['ano']))



