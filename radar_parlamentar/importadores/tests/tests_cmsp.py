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
XML_TEST = os.path.join(cmsp.MODULE_DIR,'dados/cmsp/cmsp_test.xml')

class GeradorCasaLegislativaCase(TestCase):
    def test_gera_casa_correta(self):
        casa = GeradorCasaLegislativa().gerar_cmsp()
        self.assertEquals(casa.nome_curto,'cmsp')

class ImportadorCase(TestCase):
    def setUp(self):
        casa = GeradorCasaLegislativa().gerar_cmsp()
        importer = ImportadorCMSP(casa,True)
        self.votacao = importer.importar_de(XML_TEST)[0]

    def test_votacao_importada(self):
        self.assertEquals(self.votacao.id_vot,'1')
         
    def test_parlamentar_importado(self):
        parlamentar = models.Parlamentar.objects.get(id_parlamentar='1')
        self.assertTrue(parlamentar)
