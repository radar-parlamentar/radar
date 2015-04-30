# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree
import os
import zipfile
import urllib2
import logging
from StringIO import StringIO

logger = logging.getLogger("radar")
	
def abrir_xml_zipado(url=None):
	xml = None
	try:
		xml_zip_text = _faz_download(url)
		
		xml_zip_file = StringIO()
		xml_zip_file.write(xml_zip_text)
		
		xml_zip = zipfile.ZipFile(xml_zip_file)
		xml_file_name = xml_zip.namelist()[0] # pega só o primeiro arquivo
		xml_text = xml_zip.read(xml_file_name)
		
		xml = etree.fromstring(xml_text)
	except (etree.ParseError, zipfile.BadZipfile) as e:
		print '%s: %s' % (e.__class__.__name__, e)
	
	return xml

def _faz_download(url):
	text = ''
	try:
		text = urllib2.urlopen(url).read()
	except (urllib2.URLError, urllib2.HTTPError) as e:
		print '%s: %s' % (e.__class__.__name__, e)
		
	return text
	
def main():
	URL_DADOS_CDEP = 'http://www.camara.leg.br/internet/Deputado/DeputadosXML.zip'

	xml = abrir_xml_zipado(url=URL_DADOS_CDEP)
	nome_parlamentar = unicode('ROMÁRIO', 'utf-8')
	parlamentar_tag = xml.find('Deputados/Deputado[nomeParlamentar="%s"]' % nome_parlamentar)

	if parlamentar_tag is not None:
		sexo_tag = parlamentar_tag.find('SEXO')
		if sexo_tag is not None:
			sexo = sexo_tag.text
			print sexo
		else:
			print 'Parlamentar "%s" sem tag SEXO' % nome_parlamentar
	else:
		print 'Parlamentar "%s" nao foi encontrado' % nome_parlamentar

	
if __name__ == '__main__':
	main()