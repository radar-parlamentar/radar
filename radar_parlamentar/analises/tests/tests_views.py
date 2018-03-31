"""Testing this module views."""
from django.test import Client, TestCase
from util_test import flush_db

from importadores.conv import ImportadorConvencao
from modelagem.models import BIENIO

class JsonAnaliseViewTest(TestCase):
    """Test analises.views methods."""

    @classmethod
    def setUpClass(cls):
        """Setup common for all test cases. Build the DB."""
        super().setUpClass()
        cls.importer = ImportadorConvencao()
        cls.importer.importar()
        cls.client = Client()

    @classmethod
    def tearDownClass(cls):
        """TearDown after all test cases. Flush the DB."""
        flush_db(cls)
        super().tearDownClass()

    def test_json_analise(self):
        """Test json_analise view."""
        # Test made without 'palavra-chave' since we need to rely on
        # elasticsearch for that
        response = self.client.get('/radar/json/conv/BIENIO/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
