"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from __future__ import unicode_literals
from django.test import TestCase
from django.core import serializers
from exportadores import exportar
import os
from modelagem import models


MODULE_DIR = os.path.abspath(os.path.dirname(__file__))


class ExportadoresFileTest (TestCase):
    
    def test_create_file_partido(self):
    	exportar.serialize_partido()
    	filepath = os.path.join(MODULE_DIR, 'dados/partido.xml')
    	self.assertTrue(os.path.isfile(filepath))
	
	def test_create_file_casa_legislativa(self):
		exportar.serialize_casa_legislativa()
		filepath = os.path.join(MODULE_DIR, 'dados/casa_legislativa.xml')
		self.assertTrue(os.path.isfile(filepath))
    
    def test_create_file_parlamentar(self):
    	exportar.serialize_parlamentar()
    	filepath = os.path.join(MODULE_DIR, 'dados/parlamentar.xml')
    	self.assertTrue(os.path.isfile(filepath))
    	
    def test_create_file_legislatura(self):
    	exportar.serialize_legislatura()
    	filepath = os.path.join(MODULE_DIR, 'dados/legislatura.xml')
    	self.assertTrue(os.path.isfile(filepath))
    	
    def test_create_file_proposicao(self):
    	exportar.serialize_proposicao()
    	filepath = os.path.join(MODULE_DIR, 'dados/proposicao.xml')
    	self.assertTrue(os.path.isfile(filepath))
    	
    def test_create_file_votacao(self):
    	exportar.serialize_votacao()
    	filepath = os.path.join(MODULE_DIR, 'dados/votacao.xml')
    	self.assertTrue(os.path.isfile(filepath))
    	
    def test_create_file_voto(self):
    	exportar.serialize_voto()
    	filepath = os.path.join(MODULE_DIR, 'dados/voto.xml')
    	self.assertTrue(os.path.isfile(filepath))


class DadosExportardosTest (TestCase):
	
	

        


