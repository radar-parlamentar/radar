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

def main():
    
    tree = toXml('http://legis.senado.leg.br/dadosabertos/senador/lista/legislatura/52/54')
    lista_parlamentares = tree[1][0]
    
    total_parlamentares = len(lista_parlamentares)
    
    for contador in range(0, total_parlamentares):
        parlamentar = lista_parlamentares[contador]
    
        nome_parlamentar = parlamentar.find('NomeParlamentar').text
        sexo_parlamentar = parlamentar.find('SexoParlamentar').text
        
        if(sexo_parlamentar == 'Masculino'):
            sexo_parlamentar = 'Masc'
        else:
            sexo_parlamentar = 'Fem'
        
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
        '''
        
if __name__ == '__main__':
    main()