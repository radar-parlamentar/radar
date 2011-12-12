# Classes do modelo de negócio, no caso o XML da proposição
import xml.etree.ElementTree as etree
import io

SIM = 'Sim'
NAO = 'Não'
ABSTENCAO = 'Abstenção'

class Proposicao:
  id = ''
  sigla = ''
  numero = ''
  ano = ''
  explicacao = ''
  votacoes = []

  def __init__(self):
    id = ''
    sigla = ''
    numero = ''
    ano = ''
    explicacao = ''
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
    return "[%s %s/%s]: %s" % (self.sigla, self.numero, self.ano, self.explicacao)

class Votacao:
  resumo = ''
  data = ''
  hora = ''
  deputados = []

  def __init__(self): # não deveria ser necessário
    self.resumo = ''
    self.data = ''
    self.hora = ''
    self.deputados = []

  def fromtree(tree):
    vot = Votacao() # se não fosse pelo init, faria coisa errada (utilizar os valores do objeto anteriormente criados!!!)
    vot.resumo = tree.attrib['Resumo']
    vot.data = tree.attrib['Data']
    vot.hora = tree.attrib['Hora']
    for child in tree:
      dep = Deputado.fromtree(child)
      vot.deputados.append(dep)
    return vot

  def por_partido(self):
    # partido => VotoPartido
    dic = {}
    for dep in self.deputados:
      part = dep.partido
      if not part in dic:
        dic[part] = VotoPartido(part)
      voto = dic[part]
      voto.add(dep.voto)
    return dic  
  

  def __str__(self):
    return "[%s, %s] %s" % (self.data, self.hora, self.resumo)

class Deputado:
  nome = ''
  partido = ''
  uf = ''
  voto = ''

  def __init__(self):
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

  
class VotoPartido:
  partido = ''
  sim = 0
  nao = 0
  abstencao = 0

  def add(self, voto):
    if (voto == SIM):
      self.sim += 1
    if (voto == NAO):
      self.nao += 1
    if (voto == ABSTENCAO):
      self.abstencao += 1

  def __init__(self, partido):
    self.partido = partido



