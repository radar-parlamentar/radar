# Classes do modelo de negócio, no caso o XML da proposição
import xml.etree.ElementTree as etree
import io

class Proposicao:
  sigla = ''
  numero = ''
  ano = ''
  votacoes = []
  
  def fromxml(xml):
    tree = etree.parse(io.StringIO(xml))
    prop = Proposicao()
    prop.sigla = tree.find('Sigla').text
    prop.numero = tree.find('Numero').text
    prop.ano = tree.find('Ano').text
    for child in tree.find('Votacoes'):
      vot = Votacao.fromtree(child)
      prop.votacoes.append(vot)
    return prop

  def __str__(self):
    return "%s %s/%s" % (self.sigla, self.numero, self.ano)

class Votacao:
  resumo = ''
  data = ''
  hora = ''
  deputados = []

  def fromtree(tree):
    vot = Votacao()
    vot.resumo = tree.attrib['Resumo']
    vot.data = tree.attrib['Data']
    vot.hora = tree.attrib['Hora']
    for child in tree:
      dep = Deputado.fromtree(child)
      vot.deputados.append(dep)
    return vot

  def __str__(self):
    return "[%s, %s] %s" % (self.data, self.hora, self.resumo)

class Deputado:
  nome = ''
  partido = ''
  uf = ''
  voto = ''

  def fromtree(tree):
    dep = Deputado()
    dep.nome = tree.attrib['Nome']
    dep.partido = tree.attrib['Partido']
    dep.uf = tree.attrib['UF']
    dep.voto = tree.attrib['Voto']
    return dep

  def __str__(self):
    return "%s (%s-%s) votou %s" % (self.nome, self.partido, self.uf, self.voto)

  

