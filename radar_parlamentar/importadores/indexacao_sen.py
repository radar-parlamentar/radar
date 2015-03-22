# coding:utf-8
from __future__ import unicode_literals
from modelagem.models import Proposicao
import urllib2
import xml.etree.ElementTree as etree


def get_materia_xml(proposicao):
	url = "http://legis.senado.gov.br/dadosabertos/materia/%s/%s/%s" % (proposicao.sigla,proposicao.numero,proposicao.ano)
	print url
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

def main():
	lista_proposicao = Proposicao.objects.all().filter(casa_legislativa_id=1)
	for proposicao in lista_proposicao:
		materia_xml = get_materia_xml(proposicao)
		ementa =  materia_xml.find("Materia").find("DadosBasicosMateria").find("EmentaMateria")
		if ementa is not None:
			proposicao.descricao = ementa.text
			
		index = materia_xml.find("Materia").find("DadosBasicosMateria").find("IndexacaoMateria")
		if index is not None:
			proposicao.indexacao=index.text
		proposicao.save()
