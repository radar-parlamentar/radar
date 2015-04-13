from django.core.management.base import NoArgsCommand
from datetime import datetime
from django.http import HttpRequest  


import unittest
from analises import views
import sys
import os
import logging

ESSE_DIRETORIO = os.path.dirname(os.path.realpath(__file__))
TESTES_SISTEMA_PATH = os.path.join(ESSE_DIRETORIO, os.pardir, os.pardir)

#logger = logging.getLogger('radar')
#logger.setLevel(logging.ERROR)

class Command(NoArgsCommand):
    help = """
    Comando destinado a execucao de Testes de Sistema (carga, stress, performance, etc).
    Estes testes devem ser colocados dentro do pacote testes_sistema, em qualquer
    submodulo ou subpacote.
    """

    def handle_noargs(self, **options):
        print 'EXECUTANDO TESTES DE SISTEMA:'
        
        suite = unittest.TestLoader().discover(TESTES_SISTEMA_PATH, '*.py')
        unittest.TextTestRunner(verbosity=3).run(suite)