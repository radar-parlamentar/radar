"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from __future__ import unicode_literals
from django.test import TestCase
from importadores import importador_interno
from modelagem import models


class ImportadorInternoTest(TestCase):

    @classmethod
    def setUpClass(cls):

        # Criando dados fictícios no mock
        partidoTest1 = models.Partido(nome='PMDB', numero='40')
        partidoTest2 = models.Partido(nome='PT', numero='13')
        partidoTest3 = models.Partido(nome='PSDB', numero='23')
        partidoTest1.save()
        partidoTest2.save()
        partidoTest3.save()

        parlamentarTest1 = models.Parlamentar(
            id_parlamentar='', nome='Ivandro Cunha Lima', genero='')
        parlamentarTest2 = models.Parlamentar(
            id_parlamentar='', nome='Fernando Ferro', genero='')
        parlamentarTest3 = models.Parlamentar(
            id_parlamentar='', nome='Humberto Costa', genero='')

        parlamentarTest1.save()
        parlamentarTest2.save()
        parlamentarTest3.save()

        casa_legislativaTest1 = models.CasaLegislativa(
            nome='Camara dos Deputados', nome_curto='cdep', esfera='FEDERAL',
            local='', atualizacao='2012-06-01')

        casa_legislativaTest2 = models.CasaLegislativa(
            nome='Camara Municipal de Sao Paulo', nome_curto='cmsp',
            esfera='MUNICIPAL', local='Sao Paulo - SP',
            atualizacao='2012-12-31')

        casa_legislativaTest1.save()
        casa_legislativaTest2.save()

        legislaturaTest1 = models.Legislatura(
            parlamentar=parlamentarTest1,
            casa_legislativa=casa_legislativaTest1,
            inicio='2004-01-01', fim='2012-07-01',
            partido=partidoTest1, localidade='PB')
        legislaturaTest1.save()

        # Exportando dados do mock para os xml
        # exportar.serialize_partido()
        # exportar.serialize_parlamentar()
        # exportar.serialize_casa_legislativa()
        # exportar.serialize_legislatura()

        # Deletando os registros do mock
        partidoTest1.delete()
        partidoTest2.delete()
        partidoTest3.delete()

        parlamentarTest1.delete()
        parlamentarTest2.delete()
        parlamentarTest3.delete()

        casa_legislativaTest1.delete()
        casa_legislativaTest2.delete()

        legislaturaTest1.delete()

    def test_importar_partido(self):
        importador_interno.deserialize_partido()
        PMDB = Partido.objects.filter(nome='PMDB')
        self.assertEquals(PMDB.numero, 40)

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)
