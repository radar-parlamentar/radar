from django.test import TestCase
from importadores.camara_genero import _null_to_none
from importadores.camara_genero import multiple_null_remove

class CamaraTest(TestCase):

    def test__null_to_none(self):
        proposicao = {"Casa":"NULL"}
        self.assertEquals(_null_to_none(proposicao), {"Casa":None})

    def test__multiple_null_remove(self):
        lista_proposicoes = [{"Casa":1}, {"Educacao":2}, {"Transporte":"NULL"}]
        self.assertEquals(multiple_null_remove(lista_proposicoes), [{"Casa":1}, {"Educacao":2}, {"Transporte":None}])
