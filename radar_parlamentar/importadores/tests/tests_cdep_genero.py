# -*- coding: utf-8 -*-


from django.test import TestCase
from importadores import cdep_genero
from modelagem.models import Parlamentar
from modelagem.models import Partido


class ImportadorGeneroTest(TestCase):

    @classmethod
    def setUpClass(cls):
        # Criando dados fictícios para parlamentares da Camara
        partido = Partido()
        partido.nome = 'Jacobinos'
        partido.numero = 42
        partido.save()
        cls.parlamentar_camara_test_1 = Parlamentar(
            id_parlamentar='1', nome='Abelardo Camarinha',
            genero='', partido=partido)
        cls.parlamentar_camara_test_2 = Parlamentar(
            id_parlamentar='2', nome='Fernando Rodrigues',
            genero='', partido=partido)
        cls.parlamentar_camara_test_3 = Parlamentar(
            id_parlamentar='3', nome='Flávia Morais',
            genero='', partido=partido)
        cls.parlamentar_camara_test_4 = Parlamentar(
            id_parlamentar='4', nome='Zulaiê Cobra',
            genero='', partido=partido)
        cls.parlamentar_camara_test_5 = Parlamentar(
            id_parlamentar='5', nome='Chiquinho da Silva',
            genero='', partido=partido)

        cls.parlamentar_camara_test_1.save()
        cls.parlamentar_camara_test_2.save()
        cls.parlamentar_camara_test_3.save()
        cls.parlamentar_camara_test_4.save()
        cls.parlamentar_camara_test_5.save()

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)

    def test_parlamentares_camara_com_generos_alterados(self):
        cdep_genero.insere_genero_parlamentares_camara()

        # Resgatando parlamentares no banco de dados.
        parlamentar_banco_test_1 = Parlamentar.objects.get(
            nome='Abelardo Camarinha')
        parlamentar_banco_test_2 = Parlamentar.objects.get(
            nome='Flávia Morais')
        parlamentar_banco_test_3 = Parlamentar.objects.get(
            nome='Zulaiê Cobra')

        # Verificando parlamentares com generos alterados
        self.assertEqual('M', parlamentar_banco_test_1.genero)
        self.assertEqual('F', parlamentar_banco_test_2.genero)
        self.assertEqual('F', parlamentar_banco_test_3.genero)

    def test_parlamentares_camara_sem_generos_alterados(self):
        cdep_genero.insere_genero_parlamentares_camara()

        # Resgatando parlamentares no banco de dados.
        parlamentar_banco_test_1 = Parlamentar.objects.get(
            nome='Fernando Rodrigues')
        parlamentar_banco_test_2 = Parlamentar.objects.get(
            nome='Chiquinho da Silva')

        # Verificando parlamentares sem generos alterados
        self.assertEqual('', parlamentar_banco_test_1.genero)
        self.assertEqual('', parlamentar_banco_test_2.genero)
