# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from StringIO import StringIO
from modelagem import models
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist

import xml.etree.ElementTree as etree
import os
import zipfile
import urllib2
import logging

logger = logging.getLogger("radar")

def ler_url(url):
    text = ''
    try:
        request = urllib2.Request(url)
        text = urllib2.urlopen(request).read()
    except urllib2.URLError, error:
        logger.error("urllib2.URLError: %s" % error)
    except urllib2.HTTPError:
        logger.error("urllib2.HTTPError: %s" % error)
    return text

def abrir_xml(url):
    try:
        xml = ler_url(url)
        tree = etree.fromstring(xml)
    except etree.ParseError, error:
        logger.error("etree.ParseError: %s" % error)
        return None
    return tree

def abrir_xml_zipado(url=None):
	xml = None
	try:
		xml_zip_text = _faz_download_arquivo_zipado(url)
		
		xml_zip_file = StringIO()
		xml_zip_file.write(xml_zip_text)
		
		xml_zip = zipfile.ZipFile(xml_zip_file)
		xml_file_name = xml_zip.namelist()[0] # pega só o primeiro arquivo
		xml_text = xml_zip.read(xml_file_name)
		
		xml = etree.fromstring(xml_text)
	except (etree.ParseError, zipfile.BadZipfile) as e:
		print '%s: %s' % (e.__class__.__name__, e)
	
	return xml

def _faz_download_arquivo_zipado(url):
	text = ''
	try:
		text = urllib2.urlopen(url).read()
	except (urllib2.URLError, urllib2.HTTPError) as e:
		print '%s: %s' % (e.__class__.__name__, e)
		
	return text

def insere_genero_parlamentares_senado():
    URL_DADOS_SENADO = 'http://legis.senado.leg.br/dadosabertos/senador/lista/legislatura/52/54'
    xml = abrir_xml(URL_DADOS_SENADO)
    
    lista_parlamentares_xml = xml[1][0]
    
    for parlamentar_xml in lista_parlamentares_xml:
        # Buscando conteúdos das tags NomeParlamentar e SexoParlamentar. 
        nome_parlamentar_xml = parlamentar_xml.find('NomeParlamentar').text.encode('utf-8')
        sexo_parlamentar_xml = parlamentar_xml.find('SexoParlamentar').text.encode('utf-8')
        
        if(sexo_parlamentar_xml == 'Masculino'):
            sexo_parlamentar_xml = 'M'
        else:
            sexo_parlamentar_xml = 'F'
        
        lista_parlamentar_banco = models.Parlamentar.objects.filter(nome=nome_parlamentar_xml)
        
        for parlamentar_banco in lista_parlamentar_banco:
            if((parlamentar_banco.genero == '') or (parlamentar_banco.genero is None)):
                parlamentar_banco.genero = sexo_parlamentar_xml
                parlamentar_banco.save()
                
                string_log = 'Genero de {0} alterado com sucesso!'.decode().encode('utf-8')
                string_log = string_log.format(nome_parlamentar_xml)
                logger.debug(string_log)
                
def insere_genero_parlamentares_camara():
    URL_DADOS_CDEP = 'http://www.camara.leg.br/internet/Deputado/DeputadosXML.zip'
    xml = abrir_xml_zipado(url=URL_DADOS_CDEP)
    
    lista_parlamentares_xml = xml[0]

    for parlamentar_xml in lista_parlamentares_xml:
        # Buscando conteúdos das tags nomeParlamentar e SEXO.
        nome_parlamentar_xml = parlamentar_xml.find('nomeParlamentar').text
        sexo_parlamentar_xml = parlamentar_xml.find('SEXO').text
        
        # Transformando nome do parlamentar no formato title do Python.
        nome_parlamentar_xml = unicode(nome_parlamentar_xml).title().encode('utf-8')
        
        lista_parlamentar_banco = models.Parlamentar.objects.filter(nome=nome_parlamentar_xml)
        
        for parlamentar_banco in lista_parlamentar_banco:
            if((parlamentar_banco.genero == '') or (parlamentar_banco.genero is None)):
                parlamentar_banco.genero = sexo_parlamentar_xml
                parlamentar_banco.save()
                
                string_log = 'Genero de {0} alterado com sucesso!'.decode().encode('utf-8')
                string_log = string_log.format(nome_parlamentar_xml)
                logger.debug(string_log)
            
def main():
    insere_genero_parlamentares_senado()
    logger.info('Generos dos parlamentares do Senado alterados com sucesso!')
    
    insere_genero_parlamentares_camara()
    logger.info('Generos dos parlamentares da Camara alterados com sucesso!')
    
if __name__ == '__main__':
    main()