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

def read(url):
    text = ''
    try:
        request = urllib2.Request(url)
        text = urllib2.urlopen(request).read()
    except urllib2.URLError, error:
        logger.error("urllib2.URLError: %s" % error)
    except urllib2.HTTPError:
        logger.error("urllib2.HTTPError: %s" % error)
    return text

def toXml(url):
    try:
        xml = read(url)
        tree = etree.fromstring(xml)
    except etree.ParseError, error:
        logger.error("etree.ParseError: %s" % error)
        return None
    return tree

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
    '''
    tree = toXml('http://legis.senado.leg.br/dadosabertos/senador/lista/legislatura/52/54')
    lista_parlamentares = tree[1][0]
    
    total_parlamentares = len(lista_parlamentares)
    
    for contador in range(0, total_parlamentares):
        
        parlamentar = lista_parlamentares[contador]
    
        nome_parlamentar = parlamentar.find('NomeParlamentar').text.encode('utf-8')
        sexo_parlamentar = parlamentar.find('SexoParlamentar').text.encode('utf-8')
        
        if(sexo_parlamentar == 'Masculino'):
            sexo_parlamentar = 'M'
        else:
            sexo_parlamentar = 'F'
        
        try:
            parlamentar_salvo_banco = models.Parlamentar.objects.get(nome=nome_parlamentar)
        except MultipleObjectsReturned:
            parlamentar_salvo_banco = models.Parlamentar.objects.filter(nome=nome_parlamentar)[0]
        except ObjectDoesNotExist:
            logger.info("Parlamentar %s nao existente!" % nome_parlamentar)
        
        if(parlamentar_salvo_banco is not None):
            parlamentar_salvo_banco.genero = sexo_parlamentar
            parlamentar_salvo_banco.save()
        '''
        
    URL_DADOS_CDEP = 'http://www.camara.leg.br/internet/Deputado/DeputadosXML.zip'
    xml = abrir_xml_zipado(url=URL_DADOS_CDEP)
    
    lista_parlamentares_xml = xml[0]

    for parlamentar_xml in lista_parlamentares_xml:
        nome_parlamentar_lista = parlamentar_xml.find('nomeParlamentar').text
        nome_parlamentar_lista = unicode(nome_parlamentar_lista).title().encode('utf-8')
        
        sexo_parlamentar_lista = parlamentar_xml.find('SEXO').text
    
        lista_parlamentar_banco = models.Parlamentar.objects.filter(nome=nome_parlamentar_lista)
        
        for parlamentar_banco in lista_parlamentar_banco:
            if((parlamentar_banco.genero == '') or (parlamentar_banco.genero is None)):
                parlamentar_banco.genero = sexo_parlamentar_lista
                parlamentar_banco.save()
                
                string_log = 'Genero de {0} adicionado com sucesso!'.decode().encode('utf-8')
                string_log = string_log.format(nome_parlamentar_lista)
                logger.info(string_log)
            
if __name__ == '__main__':
    main()