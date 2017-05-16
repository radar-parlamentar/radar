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



from django.test import TestCase
from importadores.cmsp import GeradorCasaLegislativa, XmlCMSP, ImportadorCMSP
from importadores import cmsp
from modelagem import models
import os
import xml.etree.ElementTree as etree
import datetime
# from modelagem.models import Parlamentar

XML_TEST = os.path.join(cmsp.MODULE_DIR, 'dados/cmsp/testes/cmsp_teste.xml')


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
        self.assertEqual(self.no_xml.tag, "CMSP")

    def test_percorre_no(self):
        for no_filho in self.no_xml.getchildren():
            self.assertEqual(no_filho.tag, "Votacao")
            for no_neto in no_filho:
                self.assertEqual(no_neto.tag, "Vereador")

    def test_ler_atributo(self):
        for no_filho in self.no_xml.getchildren():
            self.assertEqual(no_filho.get("VotacaoID"), "1")


class GeradorCMSPCase(TestCase):

    def test_gera_a_casa(self):
        casa = GeradorCasaLegislativa().gerar_cmsp()
        self.assertEqual(casa.nome_curto, 'cmsp')

    def test_recupera_a_casa_existente(self):
        casa1 = GeradorCasaLegislativa().gerar_cmsp()
        casa2 = GeradorCasaLegislativa().gerar_cmsp()
        self.assertEqual(casa1.pk, casa2.pk)


class ImportadorCMSPCase(TestCase):

    def setUp(self):
        casa = GeradorCasaLegislativa().gerar_cmsp()
        importer = ImportadorCMSP(casa)
        importer.importar_de(XML_TEST)

    def test_proposicoes_importadas(self):
        """PL 673/2015 e PL 140 /2015"""
        self.assertEqual(2, models.Proposicao.objects.count())
        pl140 = models.Proposicao.objects.get(sigla='PL', numero='140', ano='2015')
        self.assertTrue('REFORMA E REGULARIZAÇÃO DE EQUIPAMENTOS PÚBLICOS DE EDUCAÇÃO, SAÚDE E ASSISTÊNCIA SOCIAL' in pl140.ementa)

    def test_votacoes_importadas(self):
        """PL 673/2015 : 2 votações
        PL 140 /2015: 1 votação
        """
        self.assertEqual(3, models.Votacao.objects.count())
        pl673 = models.Proposicao.objects.get(sigla='PL', numero='673', ano='2015')
        self.assertEqual(2, models.Votacao.objects.filter(proposicao=pl673).count())
        pl140 = models.Proposicao.objects.get(sigla='PL', numero='140', ano='2015')
        self.assertEqual(1, models.Votacao.objects.filter(proposicao=pl140).count())
        votPl140 = models.Votacao.objects.get(proposicao=pl140)
        self.assertEqual(votPl140.id_vot, '2015')
        self.assertEqual(votPl140.resultado, 'Aprovado')
        self.assertEqual(votPl140.data, datetime.date(2015, 12, 16))
        self.assertTrue('APROVADO EM PRIMEIRA DISCUSSÃO' in votPl140.descricao)

    def test_parlamentares_importados(self):
        self.assertTrue(models.Parlamentar.objects.count() < 60)
        toninho = models.Parlamentar.objects.get(nome='TONINHO PAIVA')
        self.assertEqual(toninho.id_parlamentar, '220') 
        self.assertEqual(toninho.partido.nome, 'PR')
        pl140 = models.Proposicao.objects.get(sigla='PL', numero='140', ano='2015')
        votPl140 = models.Votacao.objects.get(proposicao=pl140)
        voto = models.Voto.objects.get(votacao=votPl140, parlamentar=toninho)
        self.assertEqual(voto.opcao, models.SIM)

    def test_parlamentares_nao_se_repetem(self):
        parlamentares = models.Parlamentar.objects.all()
        tuplas_vereadores_list = [ (p.nome, p.partido.nome, p.partido.numero) for p in parlamentares ]
        tuplas_vereadores_set = set(tuplas_vereadores_list)
        self.assertEqual(len(tuplas_vereadores_list), len(tuplas_vereadores_set))

    def test_tratamento_votos_repetidos_mesma_votacao(self):
        """VALDECIR CABRABOM deu dois votos (um sim e um não) na votação do PL 140/2015
        WADIH MUTRAN deu dois votos iguais (sim)  na votação do PL 140/2015
        """
        pl140 = models.Proposicao.objects.get(sigla='PL', numero='140', ano='2015')
        votPl140 = models.Votacao.objects.get(proposicao=pl140)
        valdecir = models.Parlamentar.objects.get(nome='VALDECIR CABRABOM')
        votos_count = models.Voto.objects.filter(votacao=votPl140, parlamentar=valdecir).count()
        self.assertEqual(votos_count, 1) # polêmico, estmoas
        wadih = models.Parlamentar.objects.get(nome='WADIH MUTRAN')
        votos_count = models.Voto.objects.filter(votacao=votPl140, parlamentar=wadih).count()
        self.assertEqual(votos_count, 1)

# TODO testar que proposições não se repetem issue #388



class EstaticosCMSPCase(TestCase):

    """Caso de teste de métodos Estáticos do XmlCMSP"""

    def setUp(self):
        casa = GeradorCasaLegislativa().gerar_cmsp()
        self.xmlCMSP = XmlCMSP(casa, True)

    def test_converte_data_valida(self):
        from django.utils.dateparse import parse_datetime
        data = self.xmlCMSP.converte_data("1/1/1000")
        self.assertEqual(data, parse_datetime("1000-1-1 0:0:0"))

    def test_converte_data_invalida(self):
        data = self.xmlCMSP.converte_data("1000")
        self.assertEqual(data, None)

    def test_prop_nome_valido(self):
        texto = "encontra Proposicoes como PL 1 /1000 no texto"
        pl = self.xmlCMSP.prop_nome(texto)
        self.assertEqual(pl, "PL 1/1000")

    def test_prop_nome_invalido(self):
        texto = "n encontra proposicoes no texto"
        pl = self.xmlCMSP.prop_nome(texto)
        self.assertEqual(pl, None)

    def test_tipo_num_ano_de_prop_nome_valido(self):
        prop_nome = "PL 1 /1000"
        num_ano = self.xmlCMSP.tipo_num_anoDePropNome(prop_nome)
        self.assertEqual(num_ano, ("PL", "1", "1000"))

    def test_tipo_num_ano_de_prop_nome_invalido(self):
        prop_nome = "nao e proposicao valida"
        num_ano = self.xmlCMSP.tipo_num_anoDePropNome(prop_nome)
        self.assertEqual(num_ano, (None, None, None))

    def test_voto_cmsp_mapeado(self):
        voto = "Sim"
        modelo_voto = self.xmlCMSP.voto_cmsp_to_model(voto)
        self.assertEqual(modelo_voto, models.SIM)

    def test_voto_cmsp_nao_mapeado(self):
        voto = "voto nao mapeado"
        modelo_voto = self.xmlCMSP.voto_cmsp_to_model(voto)
        self.assertEqual(modelo_voto, models.ABSTENCAO)


class ModelCMSPCase(TestCase):
    """Caso de teste de métodos que usam objetos model no XmlCMSP"""

    def setUp(self):
        casa = GeradorCasaLegislativa().gerar_cmsp()
        self.xmlCMSP = XmlCMSP(casa)
        type(self).preencher_banco(casa)

    @staticmethod
    def preencher_banco(casa):
        partido = models.Partido(nome="PTest", numero="1")
        partido.save()
        parlamentar = models.Parlamentar(
            id_parlamentar="1", nome="Teste_vereador",
            partido=partido, casa_legislativa=casa)
        parlamentar.save()

    def test_vereador_sem_partido(self):
        xml_vereador = etree.fromstring(
            "<Vereador Partido=\"nao tem partido\"/>")
        partido = self.xmlCMSP.partido(xml_vereador)
        self.assertEqual(
            partido, models.Partido.objects.get(nome=models.SEM_PARTIDO))

    def test_vereador_com_partido(self):
        xml_vereador = etree.fromstring("<Vereador Partido=\"PTest\"/>")
        partido = self.xmlCMSP.partido(xml_vereador)
        self.assertEqual(partido, models.Partido.objects.get(nome="PTest"))

    def test_retorna_vereador_existente(self):
        xml_vereador = etree.fromstring("<Vereador IDParlamentar=\"2\" Nome=\"Seu Vereador\" Partido=\"PTest\"/>")
        parlamentar = self.xmlCMSP.vereador(xml_vereador)
        self.assertEqual(parlamentar.nome, 'Seu Vereador')
        self.assertEqual(parlamentar.partido.nome, 'PTest')
        self.assertEqual(parlamentar.id_parlamentar, '2')

    def test_salva_vereador_inexistente(self):
        xml_vereador = etree.fromstring("<Vereador IDParlamentar=\"999\" \
            Nome=\"Nao_consta\" Partido=\"PN\"/>")
        parlamentar = self.xmlCMSP.vereador(xml_vereador)
        self.assertEqual(
            parlamentar, models.Parlamentar.objects.get(id_parlamentar=999))


class IdempotenciaCMSPCase(TestCase):

    def test_idempotencia_cmsp(self):

        casa = GeradorCasaLegislativa().gerar_cmsp()
        importer = ImportadorCMSP(casa)

        # importa a primeira vez
        votacoes = importer.importar_de(XML_TEST)
        self.votacao = votacoes[0]

        num_casas_antes = models.CasaLegislativa.objects.filter(
            nome_curto='cmsp').count()
        num_votacoes_antes = models.Votacao.objects.filter(
            proposicao__casa_legislativa=casa).count()
        num_parlamentares_antes = models.Parlamentar.objects.all().count()

        # importa de novo
        # TODO usar um XML com votações novas
        self.votacao = importer.importar_de(XML_TEST)[0]

        num_casas_depois = models.CasaLegislativa.objects.filter(
            nome_curto='cmsp').count()
        num_votacoes_depois = models.Votacao.objects.filter(
            proposicao__casa_legislativa=casa).count()
        num_parlamentares_antes_depois = models.Parlamentar.objects.filter(
            casa_legislativa=casa).count()
        num_parlamentares_depois = models.Parlamentar.objects.all().count()

        self.assertEqual(num_casas_antes, 1)
        self.assertEqual(num_casas_depois, 1)
        self.assertEqual(num_votacoes_depois, num_votacoes_antes)
        self.assertEqual(num_parlamentares_antes_depois,
                          num_parlamentares_antes)
        self.assertEqual(num_parlamentares_depois, num_parlamentares_antes)

