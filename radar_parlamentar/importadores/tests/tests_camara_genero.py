from django.test import TestCase
from importadores.camara_genero import _null_to_none
from importadores.camara_genero import multiple_null_remove, proposicoes_indexadas, parseia_indexacoes

class CamaraTest(TestCase):

    def test__null_to_none_com_null(self):
        proposicao = {"Casa":"NULL"}
        self.assertEquals(_null_to_none(proposicao), {"Casa":None})

    def test__null_to_none_sem_null(self):
        proposicao = {"Casa":1}
        self.assertEquals(_null_to_none(proposicao), {"Casa":1})

    def test_multiple_null_remove(self):
        lista_proposicoes_null = [{"Casa":1}, {"Educacao":"NULL"}, {"Transporte":"NULL"}]
        lista_proposicoes = [{"Casa:":1, "Lar":2}]
        self.assertEquals(multiple_null_remove(lista_proposicoes_null), [{"Casa":1}, {"Educacao":None}, {"Transporte":None}])
        self.assertEquals(multiple_null_remove(lista_proposicoes), [{"Casa:":1, "Lar":2}])

    def test_proposicoes_indexadas_partido_lista(self):
    	indexados_partido = [{'txtIndexacao':1, 'txtSiglaPartido': "AL"}]
    	lista_proposicoes_partido = [{'txtIndexacao':1, 'txtSiglaPartido': "AL"}]
    	self.assertEquals(proposicoes_indexadas(lista_proposicoes_partido), indexados_partido)

    def test_proposicoes_indexadas_partido_errado(self):
        indexados = []
        lista_proposicoes = [{'txtIndexacao':1, 'txtSiglaPartido': "ALLL"}]
        self.assertEquals(proposicoes_indexadas(lista_proposicoes), indexados)

    def test_parseia_indexacoes(self):
        indexacao = "Teste\nRadar.Parlamentar, _radar_parlamentar_"
        self.assertEquals(parseia_indexacoes(indexacao), [u'testeradarparlamentar', u'radarparlamentar'])
