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
    for child in tree.find('Votacoes'):
      vot = Votacao()
      vot.fromtree(child)
      self.votacoes.append(vot)

  def __str__(self):
    return "%s %s/%s" % (self.sigla, self.numero, self.ano)

class Votacao:
  resumo = ''
  data = ''
  hora = ''
  deputados = []

  def fromtree(self, tree):
    self.resumo = tree.attrib['Resumo']
    self.data = tree.attrib['Data']
    self.hora = tree.attrib['Hora']
    for child in tree:
      dep = Deputado()
      dep.fromtree(child)
      self.deputados.append(dep)

  def __str__(self):
    return "[%s, %s] %s" % (self.data, self.hora, self.resumo)

class Deputado:
  nome = ''
  partido = ''
  uf = ''
  voto = ''

  def fromtree(self, tree):
    self.nome = tree.attrib['Nome']
    self.partido = tree.attrib['Partido']
    self.uf = tree.attrib['UF']
    self.voto = tree.attrib['Voto']

  def __str__(self):
    return "%s (%s-%s) votou %s" % (self.nome, self.partido, self.uf, self.voto)

  

