from __future__ import unicode_literals
from django.core import serializers
import xml.etree.ElementTree as etree
import urllib2
import os


MODULE_DIR = os.path.abspath(os.path.dirname(__file__))
RESOURCES_FOLDER = os.path.join(MODULE_DIR, '../exportadores/dados/EXEMPLO.xml')


class importador_interno:

	@staticmethod
	def carrega_xml():
		diretorio = RESOURCES_FOLDER
		try:	
			#xml = open(diretorio,'r')
			tree = etree.parse(diretorio)
			root = tree.getroot()
			print root.tag, root.attrib
			for child in root:
				print child.tag, child.attrib
		except IOError as e:
			print "I/O erro, nao ha nenhum arquivo de Partido para ser importado".format(e.errno, e.strerror)
			return


def main():
	importador_interno.carrega_xml()










