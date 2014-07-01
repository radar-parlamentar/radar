# !/usr/bin/python
# coding=utf8

# Copyright (C) 2013, Arthur Del Esposte,  David Carlos de Araujo Silva
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
from exportadores import exportar
import os
from modelagem import models


MODULE_DIR = os.path.abspath(os.path.dirname(__file__))


class ExportadoresFileTest(TestCase):

    @classmethod
    def setUpClass(cls):
        '''Metodo responsavel por setar o que for necessario para rodar os
        testes. No nosso a criacao dos objetos no banco de testes'''

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
            casa_legislativa=casa_legislativaTest1, inicio='2004-01-01',
            fim='2012-07-01', partido=partidoTest1, localidade='PB')
        legislaturaTest1.save()

        proposicaoTest1 = models.Proposicao()
        proposicaoTest1.id_prop = '5555'
        proposicaoTest1.sigla = 'PL'
        proposicaoTest1.numero = '4520'
        proposicaoTest1.casa_legislativa = casa_legislativaTest1
        proposicaoTest1.save()

        votacaoTest1 = models.Votacao(
            id_vot=' 12345', descricao='Teste da votacao',
            data='1900-12-05', resultado='Teste', proposicao=proposicaoTest1)
        votacaoTest1.save()

        votoTest1 = models.Voto(
            votacao=votacaoTest1, legislatura=legislaturaTest1, opcao='TESTE')
        votoTest1.save()

        exportar.main()

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)

    def test_create_file_partido(self):
        filepath = os.path.join(MODULE_DIR, 'dados/partido.xml')
        self.assertTrue(os.path.isfile(filepath))

    def test_verify_file_partido(self):
        partido = models.Partido.objects.get(nome='PMDB')
        filepath = os.path.join(MODULE_DIR, 'dados/partido.xml')
        file_xml = open(filepath, 'r')
        file_read = file_xml.read()
        self.assertTrue(file_read.find(partido.nome) > 0)
        self.assertTrue(file_read.find(str(partido.numero)) > 0)

    def test_create_file_casa_legislativa(self):
        filepath = os.path.join(MODULE_DIR, 'dados/casa_legislativa.xml')
        self.assertTrue(os.path.isfile(filepath))

    def test_verify_file_casa_legislativa(self):
        casa_legislativa = models.CasaLegislativa.objects.get(
            atualizacao='2012-12-31')
        filepath = os.path.join(MODULE_DIR, 'dados/casa_legislativa.xml')
        file_xml = open(filepath, 'r')
        file_read = file_xml.read()  # Transforma o arquivo xml em uma string
        self.assertTrue(
            file_read.find(casa_legislativa.nome.decode("utf-8")) > 0)
        self.assertTrue(file_read.find(casa_legislativa.nome_curto) > 0)
        self.assertTrue(file_read.find(casa_legislativa.esfera) > 0)
        # Caso for menor que zero a palavra nao existe na string
        self.assertTrue(file_read.find('cdeb') < 0)

    def test_create_file_parlamentar(self):
        filepath = os.path.join(MODULE_DIR, 'dados/parlamentar.xml')
        self.assertTrue(os.path.isfile(filepath))

    def test_verify_file_parlamentar(self):
        parlamentar = models.Parlamentar.objects.get(nome='Humberto Costa')
        filepath = os.path.join(MODULE_DIR, 'dados/parlamentar.xml')
        file_xml = open(filepath, 'r')
        file_read = file_xml.read()
        self.assertTrue(file_read.find(parlamentar.nome) > 0)

    def test_create_file_legislatura(self):
        filepath = os.path.join(MODULE_DIR, 'dados/legislatura.xml')
        self.assertTrue(os.path.isfile(filepath))

    def test_verify_file_legislatura(self):
        legislatura = models.Legislatura.objects.get(inicio='2004-01-01')
        filepath = os.path.join(MODULE_DIR, 'dados/legislatura.xml')
        file_xml = open(filepath, 'r')
        file_read = file_xml.read()
        self.assertTrue(file_read.find(legislatura.localidade) > 0)
        self.assertTrue(file_read.find(str(legislatura.inicio)) > 0)
        self.assertTrue(file_read.find(str(legislatura.fim)) > 0)

    def test_create_file_proposicao(self):
        filepath = os.path.join(MODULE_DIR, 'dados/proposicao.xml')
        self.assertTrue(os.path.isfile(filepath))

    def teste_verify_file_proposicao(self):
        proposicao = models.Proposicao.objects.get(sigla='PL')
        filepath = os.path.join(MODULE_DIR, 'dados/proposicao.xml')
        file_xml = open(filepath, 'r')
        file_read = file_xml.read()
        self.assertTrue(file_read.find(proposicao.numero) > 0)
        self.assertTrue(file_read.find(proposicao.id_prop) > 0)

    def test_create_file_votacao(self):
        filepath = os.path.join(MODULE_DIR, 'dados/votacao.xml')
        self.assertTrue(os.path.isfile(filepath))

    def test_verify_file_votacao(self):
        votacao = models.Votacao.objects.get(resultado='Teste')
        filepath = os.path.join(MODULE_DIR, 'dados/votacao.xml')
        file_xml = open(filepath, 'r')
        file_read = file_xml.read()
        self.assertTrue(file_read.find(votacao.descricao) > 0)
        self.assertTrue(file_read.find(str(votacao.data)) > 0)

    def test_verify_file_voto(self):
        voto = models.Voto.objects.get(opcao='TESTE')
        filepath = os.path.join(MODULE_DIR, 'dados/voto.xml')
        file_xml = open(filepath, 'r')
        file_read = file_xml.read()
        self.assertTrue(file_read.find(voto.opcao) > 0)

    def test_create_file_voto(self):
        filepath = os.path.join(MODULE_DIR, 'dados/voto.xml')
        self.assertTrue(os.path.isfile(filepath))
