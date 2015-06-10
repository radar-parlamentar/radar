# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from __future__ import unicode_literals
from django.test import TestCase
from importadores import importador_genero
from modelagem.models import Parlamentar

class ImportadorGeneroTest(TestCase):

    @classmethod
    def setUpClass(cls):
        # Criando dados fictícios para parlamentares da Camara
        cls.parlamentar_camara_test_1 = Parlamentar(
            id_parlamentar='', nome='Abelardo Camarinha', genero='')
        cls.parlamentar_camara_test_2= Parlamentar(
            id_parlamentar='', nome='Fernando Rodrigues', genero='')
        cls.parlamentar_camara_test_3 = Parlamentar(
            id_parlamentar='', nome='Flávia Morais', genero='')
        cls.parlamentar_camara_test_4 = Parlamentar(
            id_parlamentar='', nome='Zulaiê Cobra', genero='')
        cls.parlamentar_camara_test_5 = Parlamentar(
            id_parlamentar='', nome='Chiquinho da Silva', genero='')

        cls.parlamentar_camara_test_1.save()
        cls.parlamentar_camara_test_2.save()
        cls.parlamentar_camara_test_3.save()
        cls.parlamentar_camara_test_4.save()
        cls.parlamentar_camara_test_5.save()

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)
    
    def test_parlamentares_camara_com_generos_alterados(self):
        importador_genero.insere_genero_parlamentares_camara()
        
        # Resgatando parlamentares no banco de dados.
        parlamentar_banco_test_1 = Parlamentar.objects.get(nome='Abelardo Camarinha')
        parlamentar_banco_test_2 = Parlamentar.objects.get(nome='Flávia Morais')
        parlamentar_banco_test_3 = Parlamentar.objects.get(nome='Zulaiê Cobra')
        
        # Verificando parlamentares com generos alterados
        self.assertEquals('M', parlamentar_banco_test_1.genero)
        self.assertEquals('F', parlamentar_banco_test_2.genero)
        self.assertEquals('F', parlamentar_banco_test_3.genero)
    
    def test_parlamentares_camara_sem_generos_alterados(self):
        importador_genero.insere_genero_parlamentares_camara()

        # Resgatando parlamentares no banco de dados.
        parlamentar_banco_test_1 = Parlamentar.objects.get(nome='Fernando Rodrigues')
        parlamentar_banco_test_2 = Parlamentar.objects.get(nome='Chiquinho da Silva')
        
        # Verificando parlamentares sem generos alterados
        self.assertEquals('', parlamentar_banco_test_1.genero)
        self.assertEquals('', parlamentar_banco_test_2.genero)
    