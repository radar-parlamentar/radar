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





class ExportadoresFileTest(TestCase):
    @classmethod
    def setUpClass(cls):
        '''Metodo responsavel por setar o que for necessario para rodar os testes. No nosso a criacao dos objetos no 
        banco de testes'''
        
        partidoTest1 = models.Partido(nome = 'PMDB',numero = '40')
        partidoTest2 = models.Partido(nome = 'PT',numero = '13')
        partidoTest3 = models.Partido(nome = 'PSDB',numero = '23')
        partidoTest1.save()
        partidoTest2.save()
        partidoTest3.save()
        
        parlamentarTest1 = models.Parlamentar(id_parlamentar = '',nome = 'Ivandro Cunha Lima',genero = '')
        parlamentarTest2 = models.Parlamentar(id_parlamentar = '',nome = 'Fernando Ferro',genero = '')
        parlamentarTest3 = models.Parlamentar(id_parlamentar = '',nome = 'Humberto Costa',genero = '')
        
        parlamentarTest1.save()
        parlamentarTest2.save()
        parlamentarTest3.save()


        casa_legislativaTest1 = models.CasaLegislativa(nome = 'Camara dos Deputados',nome_curto = 'cdep',esfera = 'FEDERAL',
                local = '', atualizacao = '2012-06-01')

        casa_legislativaTest2 = models.CasaLegislativa(nome = 'Camara Municipal de Sao Paulo',nome_curto = 'cmsp',
            esfera = 'MUNICIPAL' ,local = 'Sao Paulo - SP', atualizacao = '2012-12-31')

        casa_legislativaTest1.save()
        casa_legislativaTest2.save()


    def test_create_file_partido(self):
        
        exportar.serialize_partido()
    	filepath = os.path.join(MODULE_DIR, 'dados/partido.xml')
    	self.assertTrue(os.path.isfile(filepath))
	
    def test_verify_file_partido(self):
        partido = models.Partido.objects.get(nome = 'PMDB')
        filepath = os.path.join(MODULE_DIR, 'dados/partido.xml')
        file_xml = open(filepath,'r')
        file_read = file_xml.read()
        self.assertTrue(file_read.find(partido.nome) > 0)
        self.assertTrue(file_read.find(str(partido.numero)) > 0)




    def test_create_file_casa_legislativa(self):
		exportar.serialize_casa_legislativa()
		filepath = os.path.join(MODULE_DIR, 'dados/casa_legislativa.xml')
		self.assertTrue(os.path.isfile(filepath))
    
    
    def test_verify_file_casa_legislativa(self):
        casa_legislativa = models.CasaLegislativa.objects.get(atualizacao = '2012-12-31') 
        filepath = os.path.join(MODULE_DIR, 'dados/casa_legislativa.xml')
        file_xml = open(filepath,'r')
        file_read = file_xml.read() #Transforma o arquivo xml em uma string 
        self.assertTrue(file_read.find(casa_legislativa.nome.decode("utf-8")) > 0)
        self.assertTrue(file_read.find(casa_legislativa.nome_curto)> 0)
        self.assertTrue(file_read.find(casa_legislativa.esfera)>0)
        self.assertTrue(file_read.find('cdeb') < 0) #Caso for menor que zero a palavra nao existe na string



    def test_create_file_parlamentar(self):
    	exportar.serialize_parlamentar()
    	filepath = os.path.join(MODULE_DIR, 'dados/parlamentar.xml')
    	self.assertTrue(os.path.isfile(filepath))
    	
    def test_verify_file_parlamentar(self):
        parlamentar = models.Parlamentar.objects.get(nome ='Humberto Costa')
        filepath = os.path.join(MODULE_DIR, 'dados/parlamentar.xml')
        file_xml = open(filepath,'r')
        file_read = file_xml.read()
        self.assertTrue(file_read.find(parlamentar.nome) > 0)
        


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


#class DadosExportardosTest (TestCase):
	
	

        


