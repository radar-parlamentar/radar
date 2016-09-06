# !/usr/bin/python
# coding=utf8

from __future__ import unicode_literals
from django.test import TestCase
from importadores.chefes_executivos import *
from modelagem import models
from importadores.cmsp import GeradorCasaLegislativa
from importadores.sen import CasaLegislativaGerador
import os
import xml.etree.ElementTree as etree

XML_TEST = os.path.join(MODULE_DIR, 'dados/chefe_executivo/chefe_executivo_teste.xml')


class ImportadorChefesExecutivosTeste(TestCase):

    def setUp(self):
        partido = models.Partido(nome="PTest", numero="1")
        partido.save()

    def test_chefe_cmsp_importado(self):
        gerador = GeradorCasaLegislativa()
        casa = gerador.gerar_cmsp()
        importer_chefe = ImportadorChefesExecutivos(casa.nome_curto, 'PrefeitosSP', 'PrefeitoSP', XML_TEST)
        importer_chefe.importar_chefes()
        chefe = models.ChefeExecutivo.objects.get(nome="teste_chefe_cmsp")

        self.assertEquals(chefe.nome, "teste_chefe_cmsp")
        self.assertEquals(chefe.partido.nome, "PT")
        self.assertEquals(chefe.mandato_ano_inicio, 1989)
        self.assertEquals(chefe.mandato_ano_fim, 1992)
        self.assertEquals(chefe.genero, "F")


    def test_chefe_sen_importado(self):
        gerador = CasaLegislativaGerador()
        casa = gerador.gera_senado()
        importer_chefe = ImportadorChefesExecutivos(casa.nome_curto, 'Presidentes', 'Presidente', XML_TEST)
        importer_chefe.importar_chefes()
        chefe = models.ChefeExecutivo.objects.get(nome="teste_chefe_sen")

        self.assertEquals(chefe.nome, "teste_chefe_sen")
        self.assertEquals(chefe.partido.nome, "PT")
        self.assertEquals(chefe.mandato_ano_inicio, 1990)
        self.assertEquals(chefe.mandato_ano_fim, 1992)
        self.assertEquals(chefe.genero, "M")