from django.core.management.base import NoArgsCommand
from datetime import datetime
from django.http import HttpRequest  

import unittest
from analises import views
import sys
import os
import logging

class TestesDesempenho(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print 'Executando testes de desempenho:'
        
    @classmethod
    def tearDownClass(cls):
        print 'Finalizando testes de desempenho...'

    def test_desempenho_analise_camara_federal(self):
        """
        Testa o desempenho da geracao da nalise PCA para a Camara Federal (deve estar sem cache)
        """
        
        request = HttpRequest()
        nome_curto_casa = 'cdep'
        periodicidade = 'BIENIO'
        palavras_chave=''
        
        start = datetime.now()
        views.json_analise(request, nome_curto_casa, periodicidade, palavras_chave)
        end = datetime.now()
        
        print 'Tempo decorrido = %s' % str(end - start)