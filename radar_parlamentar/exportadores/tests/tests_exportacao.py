from django.test import TestCase
from exportadores import exportador_csv
from modelagem.models import CasaLegislativa
from modelagem.models import Votacao
import os.path
import csv

class ExportacaoClass(TestCase):

	@classmethod
	def setUpClass(cls):
		exportador_csv.main()

	#@classmethod
	#def tearDownClass(cls):
	#	from util_test import flush_db
	#	flush_db(cls)


	def test_exportar_cvs(self):
            CAMINHO = "./exportadores/saida/votacoes.csv"
            colunas_csv = []
            existe = False
	    existe = os.path.isfile(CAMINHO)
	    colunas = ["PROPOSICAO","VOTACAO","PARLAMENTAR_ID","PARLAMENTAR_NOME","PARTIDO","UF","REGIAO","VOTO"]
            with open(CAMINHO,'rb') as arquivo:
                readers = csv.reader(arquivo, delimiter=',')
                for row in readers:
                    colunas_csv = row
	    self.assertEquals(True, existe)
            self.assertEquals(colunas_csv, colunas)
