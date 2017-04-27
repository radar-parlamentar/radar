from django.test import TestCase
from importadores.camara_genero import _null_to_none

class CamaraTest(TestCase):

    def test__null_to_none(self):
        proposicao = {"CASA":"NULL"}
        self.assertEquals(_null_to_none(proposicao), {"CASA": None})
