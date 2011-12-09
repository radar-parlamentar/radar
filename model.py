#!/usr/bin/python3.2
# -*- coding: utf-8 -*-
#
# Classes do modelo de negócio, no caso o XML da proposição
import xml.etree.ElementTree as etree
import io

class Proposicao:
  sigla = ''
  numero = ''
  ano = ''
  votacoes = []
  
  def fromxml(self, xml):
    tree = etree.parse(io.StringIO(xml))
    self.sigla = tree.find('Sigla').text
    self.numero = tree.find('Numero').text
    self.ano = tree.find('Ano').text

  def __str__(self):
    return "%s %s/%s" % (self.sigla, self.numero, self.ano)

#class Votacao:
#  resumo
#  data
#  hora
#  deputados

#class Deputado:
#  nome
#  partifo
#  uf
#  voto
  

