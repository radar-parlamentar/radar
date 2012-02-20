# Requisições para os Web Services da câmara
from model import Proposicao
import urllib.request
import xml.etree.ElementTree as etree
import io

OBTER_VOTACOES_PROPOSICAO = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterVotacaoProposicao?tipo=%s&numero=%s&ano=%s'
OBTER_INFOS_PROPOSICAO_POR_DADOS = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterProposicao?tipo=%s&numero=%s&ano=%s'
OBTER_INFOS_PROPOSICAO_POR_ID = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterProposicaoPorID?idProp=%s'

# obtém as votações utilizando o ID da proposição
def obter_votacao(prop_id, tipo, num, ano):
    url = OBTER_VOTACOES_PROPOSICAO % (tipo, num, ano)
    try:
        xml = urllib.request.urlopen(url).read()
    except urllib.error.HTTPError:
        return None
    xml = str(xml, "utf-8") # aqui é o xml da votação
    prop = Proposicao.fromxml(xml)
    prop.id = prop_id

    xml = obter_proposicao(prop_id) # aqui é o xml com mais detalhes sobre a proposição
    xml = str(xml, "utf-8")
    tree = etree.parse(io.StringIO(xml))
    prop.ementa = tree.find('Ementa').text
    prop.explicacao = tree.find('ExplicacaoEmenta').text
    prop.situacao = tree.find('Situacao').text
    return prop

# obtém as votações sem utilizar o ID da proposição
def obert_votacao(tipo, num, ano):
    url  = OBTER_VOTACOES_PROPOSICAO % (tipo, num, ano)
    try:
        xml = urllib.request.urlopen(url).read()
    except urllib.error.HTTPError:
        return None
    xml = str(xml, "utf-8") # aqui é o xml da votação
    proposicao = Proposicao.fromxml(xml)

    xml = obter_proposicao(tipo, num, ano) #aqui é o xml com mais detalhes sobre a proposição
    xml = str(xml, "utf-8")
    tree = etree.parse(io.StringIO(xml))
    prop.ementa = tree.find('Ementa').text
    prop.explicacao = tree.find('ExplicacaoEmenta').text
    prop.situacao = tree.find('Situacao').text
    return prop

# obtém dados da proposição por tipo, número e ano
def obter_proposicao(tipo, num, ano):
    url = OBTER_INFOS_PROPOSICAO_POR_DADOS % (tipo, num, ano)
    xml = urllib.request.urlopen(url).read()
    return xml

# obtém dados da proposição por ID
def obter_proposicao(prop_id):
    url = OBTER_INFOS_PROPOSICAO_POR_ID % prop_id
    xml = urllib.request.urlopen(url).read()
    return xml
