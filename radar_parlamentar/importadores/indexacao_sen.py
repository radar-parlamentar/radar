# coding:utf-8
from __future__ import unicode_literals
from modelagem.models import Proposicao, CasaLegislativa
import urllib2
import xml.etree.ElementTree as etree
import logging

logger = logging.getLogger("radar")


def get_materia_xml(proposicao):
    url = "http://legis.senado.gov.br/dadosabertos/materia/%s/%s/%s" % (proposicao.sigla,proposicao.numero,proposicao.ano)
    logger.info(url)
    try:
        request = urllib2.Request(url)
        xml = urllib2.urlopen(request).read()
    except urllib2.URLError, error:
        logger.error("urllib2.URLError: %s" % error)
        raise ValueError('Legislatura %s não encontrada' % id_leg)
    try:
        tree = etree.fromstring(xml)
    except etree.ParseError, error:
        logger.error("etree.ParseError: %s" % error)
        raise ValueError('Legislatura %s não encontrada' % id_leg)
    return tree


def inserirIndex(proposicao):
    materia_xml = get_materia_xml(proposicao)
    ementa =  materia_xml.find("Materia").find("DadosBasicosMateria").find("EmentaMateria")
    if ementa is not None:
        proposicao.descricao = ementa.text
    index = materia_xml.find("Materia").find("DadosBasicosMateria").find("IndexacaoMateria")
    if index is not None:
        proposicao.indexacao=index.text
    proposicao.save()

def indexar_proposicoes():
    lista_senado = CasaLegislativa.objects.filter(nome_curto="sen")
    if len(lista_senado) == 0:
        raise NameError("Casa Legislativa do senado nao encontrada")
    lista_proposicao = Proposicao.objects.all().filter(casa_legislativa_id=lista_senado[0].id)
    for proposicao in lista_proposicao:
      inserirIndex(proposicao)

def main():
    indexar_proposicoes()
