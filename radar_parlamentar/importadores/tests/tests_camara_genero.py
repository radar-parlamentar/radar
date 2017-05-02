from django.test import TestCase
from importadores.camara_genero import _null_to_none
from importadores.camara_genero import multiple_null_remove, proposicoes_indexadas, parseia_indexacoes

class CamaraTest(TestCase):

    def test__null_to_none(self):
        proposicao = {"Casa":"NULL"}
        self.assertEquals(_null_to_none(proposicao), {"Casa":None})

    def test_multiple_null_remove(self):
        lista_proposicoes = [{"Casa":1}, {"Educacao":2}, {"Transporte":"NULL"}]
        self.assertEquals(multiple_null_remove(lista_proposicoes), [{"Casa":1}, {"Educacao":2}, {"Transporte":None}])

    def test_proposicoes_indexadas(self):
    	indexados = [{'txtIndexacao':1, 'txtSiglaPartido': "AL"}]
    	lista_proposicoes = [{'txtIndexacao':1, 'txtSiglaPartido': "AL"}]
    	self.assertEquals(proposicoes_indexadas(lista_proposicoes), indexados)

    def test_parseia_indexacoes(self):
        indexacao = "Teste\nRadar.Parlamentar, _radar_parlamentar_"
        self.assertEquals(parseia_indexacoes(indexacao), [u'testeradarparlamentar', u'radarparlamentar'])
