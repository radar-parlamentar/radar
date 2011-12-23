# Requisições para os Web Services da câmara
from model import Proposicao
import urllib.request
import xml.etree.ElementTree as etree
import io

OBTER_VOTACAO_PROPOSICAO = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterVotacaoProposicao?tipo=%s&numero=%s&ano=%s'
OBTER_VOTACAO_POR_ID = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterProposicaoPorID?idProp=%s'

def obter_votacao(prop_id, tipo, num, ano):
  url = OBTER_VOTACAO_PROPOSICAO % (tipo, num, ano)
  try:
    xml = urllib.request.urlopen(url).read()
  except urllib.error.HTTPError:
    return None
  xml = str(xml, "utf-8")
  prop = Proposicao.fromxml(xml)
  prop.id = prop_id
  prop.explicacao = obter_explicacao_ementa(prop_id)
  return prop

def obter_proposicao(prop_id):
  url = OBTER_VOTACAO_POR_ID % prop_id
  xml = urllib.request.urlopen(url).read()
  return xml

def obter_explicacao_ementa(prop_id):
  xml = obter_proposicao(prop_id)
  xml = str(xml, "utf-8")
  tree = etree.parse(io.StringIO(xml))
  return tree.find('ExplicacaoEmenta').text
