from django.test import TestCase
from exportadores import exportador_csv
from modelagem.models import CasaLegislativa
from modelagem.models import Votacao

class ExportacaoClass(TestCase):	


	# # @classmethod
	# # def setUpClass(cls):
	# # 	cls.importer = conv.ImportadorConvencao()
	# # 	cls.importer.importar()

	# @classmethod
	# def tearDownClass(cls):
	# 	from util_test import flush_db
	# 	flush_db(cls)


	def test_exportar_cvs(self):
		exportador_csv.main()
