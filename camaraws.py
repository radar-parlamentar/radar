# Requisições para os Web Services da câmara
import urllib.request
from model import Proposicao

OBTER_VOTACAO_PROPOSICAO = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterVotacaoProposicao?tipo=%s&numero=%s&ano=%s'

def obter_votacao(tipo, num, ano):
  url = OBTER_VOTACAO_PROPOSICAO % (tipo, num, ano)
  xml = urllib.request.urlopen(url).read()
  xml = str(xml, "utf-8")
  prop = Proposicao.fromxml(xml)
  return prop


