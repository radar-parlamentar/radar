from django.test import TestCase
from django_cron import Schedule, CronJobBase
import datetime
import os
from  importadores import cdep
from modelagem.models import TesteCron
from importadores import importador
from mock import Mock
from modelagem import models
from importadores.tests.mocks_cdep import mock_obter_proposicao,mock_listar_proposicoes, mock_obter_votacoes, mock_obter_proposicoes_votadas_plenario


test_votadas = [[('17338', 'PL 1876/1999')]]

ID = '17338' 
ANO = '2012'
SIGLA = 'PL'
NUM = '1876'
NOME = 'PL 1876/1999'

# Create your tests here.


class CronTest(TestCase):

    def _import(self):
        votadasParser = cdep.ProposicoesParser(test_votadas)
        votadas = votadasParser.parse()        
        importer = cdep.ImportadorCamara(votadas)
        #dublando a camara
        camaraWS = cdep.Camaraws()
        camaraWS.listar_proposicoes = Mock(side_effect=mock_listar_proposicoes)
        camaraWS.obter_proposicao_por_id = Mock(side_effect=mock_obter_proposicao)
        camaraWS.obter_votacoes = Mock(side_effect=mock_obter_votacoes)
        importer.importar(camaraWS)

    def setup(self):
        #Chama o importador no momento que o teste for executado
        RUN_AT_TIMES = [str(str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute))]
        schedule = Schedule(run_at_times = RUN_AT_TIMES) 
        code = "cron.ImportadorAnaliseCron"      
        teste_cron = TesteCron()
        teste_cron.save()
        self._import()
    
    def test_check_duplicate_values(self):
        #Segunda chamada ao cron
        teste_cron = TesteCron()
        teste_cron.save()
        self._import()
        query = models.Proposicao.objects.filter(id_prop=ID)
        self.assertEquals(1,len(query))
