# !/usr/bin/python
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

XML_TEST = os.path.join(cmsp.MODULE_DIR, 'dados/cmsp/cmsp_test.xml')


class AprendizadoEtreeCase(TestCase):

    """Testes para entender o funcionamento da lib etree"""

    def setUp(self):
        xml = """<CMSP>
                    <Votacao VotacaoID="1">
                        <Vereador NomeParlamentar="Teste_vereador"/>
                    </Votacao>
                </CMSP>
                """
        self.no_xml = etree.fromstring(xml)

    def test_ler_no(self):
        self.assertEquals(self.no_xml.tag, "CMSP")

    def test_percorre_no(self):
        for no_filho in self.no_xml.getchildren():
            self.assertEquals(no_filho.tag, "Votacao")
            for no_neto in no_filho:
                self.assertEquals(no_neto.tag, "Vereador")

    def test_ler_atributo(self):
        for no_filho in self.no_xml.getchildren():
            self.assertEquals(no_filho.get("VotacaoID"), "1")


class GeradorCMSPCase(TestCase):

    def test_gera_a_casa(self):
        casa = GeradorCasaLegislativa().gerar_cmsp()
        self.assertEquals(casa.nome_curto, 'cmsp')

    def test_recupera_a_casa_existente(self):
        casa1 = GeradorCasaLegislativa().gerar_cmsp()
        casa2 = GeradorCasaLegislativa().gerar_cmsp()
        self.assertEquals(casa1.pk, casa2.pk)


class ImportadorCMSPCase(TestCase):

    def setUp(self):
        casa = GeradorCasaLegislativa().gerar_cmsp()
        importer = ImportadorCMSP(casa, True)
        self.votacao = importer.importar_de(XML_TEST)[0]

    def test_votacao_importada(self):
        self.assertEquals(self.votacao.id_vot, '1')

    def test_parlamentar_importado(self):
        parlamentar = models.Parlamentar.objects.get(id_parlamentar='1')
        self.assertTrue(parlamentar)


class EstaticosCMSPCase(TestCase):

    """Caso de teste de métodos Estáticos do XmlCMSP"""

    def setUp(self):
        casa = GeradorCasaLegislativa().gerar_cmsp()
        self.xmlCMSP = XmlCMSP(casa, True)

    def test_converte_data_valida(self):
        from django.utils.dateparse import parse_datetime
        data = self.xmlCMSP.converte_data("1/1/1000")
        self.assertEquals(data, parse_datetime("1000-1-1 0:0:0"))

    def test_converte_data_invalida(self):
        data = self.xmlCMSP.converte_data("1000")
        self.assertEquals(data, None)

    def test_prop_nome_valido(self):
        texto = "encontra Proposicoes como PL 1 /1000 no texto"
        pl = self.xmlCMSP.prop_nome(texto)
        self.assertEquals(pl, "PL 1 /1000")

    def test_prop_nome_invalido(self):
        texto = "n encontra proposicoes no texto"
        pl = self.xmlCMSP.prop_nome(texto)
        self.assertEquals(pl, None)

    def test_tipo_num_ano_de_prop_nome_valido(self):
        prop_nome = "PL 1 /1000"
        num_ano = self.xmlCMSP.tipo_num_anoDePropNome(prop_nome)
        self.assertEquals(num_ano, ("PL", "1", "1000"))

    def test_tipo_num_ano_de_prop_nome_invalido(self):
        prop_nome = "nao e proposicao valida"
        num_ano = self.xmlCMSP.tipo_num_anoDePropNome(prop_nome)
        self.assertEquals(num_ano, (None, None, None))

    def test_voto_cmsp_mapeado(self):
        voto = "Sim"
        modelo_voto = self.xmlCMSP.voto_cmsp_to_model(voto)
        self.assertEquals(modelo_voto, models.SIM)

    def test_voto_cmsp_nao_mapeado(self):
        voto = "voto nao mapeado"
        modelo_voto = self.xmlCMSP.voto_cmsp_to_model(voto)
        self.assertEquals(modelo_voto, models.ABSTENCAO)


class ModelCMSPCase(TestCase):

    """Caso de teste de métodos que usam objetos model no XmlCMSP"""

    def setUp(self):
        casa = GeradorCasaLegislativa().gerar_cmsp()
        self.xmlCMSP = XmlCMSP(casa, True)
        type(self).preencher_banco(casa)

    @staticmethod
    def preencher_banco(casa):
        partido = models.Partido(nome="PTest", numero="1")
        partido.save()
        parlamentar = models.Parlamentar(
            id_parlamentar="1", nome="Teste_vereador")
        parlamentar.save()
        legislatura = models.Legislatura(
            parlamentar=parlamentar, partido=partido, casa_legislativa=casa)
        legislatura.save()

    def test_vereador_sem_partido(self):
        xml_vereador = etree.fromstring(
            "<Vereador Partido=\"nao tem partido\"/>")
        partido = self.xmlCMSP.partido(xml_vereador)
        self.assertEquals(
            partido, models.Partido.objects.get(nome=models.SEM_PARTIDO))

    def test_vereador_com_partido(self):
        xml_vereador = etree.fromstring("<Vereador Partido=\"PTest\"/>")
        partido = self.xmlCMSP.partido(xml_vereador)
        self.assertEquals(partido, models.Partido.objects.get(nome="PTest"))

    # def test_retorna_vereador_existente(self):
        # TODO: 2 parlamentares identicos podem ser cadastrados se 1
        # ja existir no banco
        # xml_vereador = etree.fromstring("<Vereador IDParlamentar=\"1\"
        # NomeParlamentar=\"Teste_vereador\"/>")
        # parlamentar = self.xmlCMSP.votante(xml_vereador)
        # self.assertEquals(parlamentar,models.Parlamentar.objects.get(
        #    nome = "Teste_vereador"))

    def test_salva_vereador_inexistente(self):
        xml_vereador = etree.fromstring(
            "<Vereador IDParlamentar=\"999\" NomeParlamentar=\"Nao_consta\"/>")
        parlamentar = self.xmlCMSP.votante(xml_vereador)
        self.assertEquals(
            parlamentar, models.Parlamentar.objects.get(id_parlamentar=999))

    def test_salva_legislatura_inexistente(self):
        xml_vereador = etree.fromstring(
            "<Vereador IDParlamentar=\"999\" NomeParlamentar=\"Nao_consta\" Partido=\"PTest\"/>")
        legislatura = self.xmlCMSP.legislatura(xml_vereador)
        self.assertEquals(legislatura, models.Legislatura.objects.get(
            parlamentar__id_parlamentar="999", partido__nome="PTest"))

    # def test_retorna_legislatura_existente(self):
        # TODO: problema com parlamentares duplicados
        # xml_vereador = etree.fromstring("<Vereador IDParlamentar=\"1\"
        # NomeParlamentar=\"Teste_vereador\" Partido=\"PTest\"/>")
        # legislatura = self.xmlCMSP.legislatura(xml_vereador)
        # self.assertEquals(legislatura,models.Legislatura.objects.get(
        #    parlamentar__id_parlamentar="1",partido__nome="PTest"))


class IdempotenciaCMSPCase(TestCase):

#    def setUp(self):

    def test_idempotencia_cmsp(self):

        casa = GeradorCasaLegislativa().gerar_cmsp()
        importer = ImportadorCMSP(casa, False)

        # importa a primeira vez
        votacoes = importer.importar_de(XML_TEST)
        self.votacao = votacoes[0]

        num_casas_antes = models.CasaLegislativa.objects.filter(
            nome_curto='cmsp').count()
        num_votacoes_antes = models.Votacao.objects.filter(
            proposicao__casa_legislativa=casa).count()
        num_legs_antes = models.Legislatura.objects.filter(
            casa_legislativa=casa).count()
        num_parlamentares_antes = models.Parlamentar.objects.all().count()

        # importa de novo
        self.votacao = importer.importar_de(XML_TEST)[0]

        num_casas_depois = models.CasaLegislativa.objects.filter(
            nome_curto='cmsp').count()
        num_votacoes_depois = models.Votacao.objects.filter(
            proposicao__casa_legislativa=casa).count()
        num_legs_depois = models.Legislatura.objects.filter(
            casa_legislativa=casa).count()
        num_parlamentares_depois = models.Parlamentar.objects.all().count()

        self.assertEqual(num_casas_antes, 1)
        self.assertEqual(num_casas_depois, 1)
        self.assertEquals(num_votacoes_depois, num_votacoes_antes)
        self.assertEquals(num_legs_depois, num_legs_antes)
        self.assertEquals(num_parlamentares_depois, num_parlamentares_antes)
