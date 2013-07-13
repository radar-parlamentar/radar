#!/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Eduardo Hideo
#
# This file is part of Radar Parlamentar.
#
# Radar Parlamentar is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Radar Parlamentar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Radar Parlamentar.  If not, see <http://www.gnu.org/licenses/>.



from __future__ import unicode_literals
from django.test import TestCase
from importadores.cmsp import *
from importadores import cmsp
from modelagem import models
import os
import xml.etree.ElementTree as etree

XML_TEST = os.path.join(cmsp.MODULE_DIR,'dados/cmsp/cmsp_test.xml')

class AprendizadoEtreeCase(TestCase):

    def setUp(self):
        xml =   """<CMSP>
                    <Votacao VotacaoID="1">
                        <Vereador NomeParlamentar="Teste_vereador"/>
                    </Votacao>
                </CMSP>
                """
        self.no_xml = etree.fromstring(xml)

    def test_ler_no(self):
        self.assertEquals(self.no_xml.tag,"CMSP")
    
    def test_percorre_no(self):
        for no_filho in self.no_xml.getchildren():
            self.assertEquals(no_filho.tag,"Votacao")
            for no_neto in no_filho:
                self.assertEquals(no_neto.tag,"Vereador")

    def test_ler_atributo(self):
        for no_filho in self.no_xml.getchildren():
            self.assertEquals(no_filho.get("VotacaoID"),"1")


class GeradorCMSPCase(TestCase):
    
    def test_gera_a_casa(self):
        casa = GeradorCasaLegislativa().gerar_cmsp()
        self.assertEquals(casa.nome_curto,'cmsp')

    def test_recupera_a_casa_existente(self):
        casa1 = GeradorCasaLegislativa().gerar_cmsp()
        casa2 = GeradorCasaLegislativa().gerar_cmsp()
        self.assertEquals(casa1.pk,casa2.pk)


class ImportadorCMSPCase(TestCase):
    def setUp(self):
        casa = GeradorCasaLegislativa().gerar_cmsp()
        importer = ImportadorCMSP(casa,True)
        self.votacao = importer.importar_de(XML_TEST)[0]

    def test_votacao_importada(self):
        self.assertEquals(self.votacao.id_vot,'1')
         
    def test_parlamentar_importado(self):
        parlamentar = models.Parlamentar.objects.get(id_parlamentar='1')
        self.assertTrue(parlamentar)

