from __future__ import unicode_literals
from django.core import serializers
import xml.etree.ElementTree as etree
import urllib2
import os
from modelagem import models

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))
RESOURCES_FOLDER = os.path.join(MODULE_DIR, '../exportadores/dados/EXEMPLO.xml')



class importador_interno:


	@staticmethod
	def carrega_xml():
		diretorio = RESOURCES_FOLDER	
		tree = etree.parse(diretorio)
		root = tree.getroot()
		for child in root:
			print root.tag,root.attrib
			print child.tag	
		#dicionario = dict(root)
		casaLegislativa = models.CasaLegislativa()
		casaLegislativa.nome_curto = root.attrib.get("nome_curto")
		casaLegislativa.nome = root.attrib.get("nome")
		casaLegislativa.esfera = root.attrib.get("esfera")
		casaLegislativa.local = root.attrib.get("local")
		casaLegislativa.atualizacao = root.attrib.get("atualizacao")
		casaLegislativa.save()	

def main():
	importador_interno.carrega_xml()










