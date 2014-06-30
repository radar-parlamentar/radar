# !/usr/bin/python
# coding=utf8

# Copyright (C) 2013, Arthur Del Esposte, Gustavo Corrêia
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
from importadorInterno import importador_interno
from exportadores import exportar
from modelagem import models


class ImportadorInternoTest(TestCase):

    @classmethod
    def setUpClass(cls):
        # Criando dados ficticios no mock
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

        # Exportando dados do mock para os xml
        exportar.serialize_partido()
        exportar.serialize_parlamentar()
        exportar.serialize_casa_legislativa()
        exportar.serialize_legislatura()
        exportar.serialize_proposicao()
        exportar.serialize_votacao()
        exportar.serialize_voto()

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

        proposicaoTest1.delete()

        votacaoTest1.delete()

        votoTest1.delete()

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)

    def test_deserialize_partido(self):

        importador_interno.deserialize_partido()
        PMDB = models.Partido.objects.filter(nome='PMDB')
        self.assertEquals(PMDB[0].numero, 40)

    def test_deserialize_parlamentar(self):

        importador_interno.deserialize_parlamentar()
        parlamentar = models.Parlamentar.objects.filter(
            nome='Ivandro Cunha Lima')
        self.assertEquals(parlamentar[0].nome, 'Ivandro Cunha Lima')

    def test_deserialize_casa_legislativa(self):

        importador_interno.deserialize_casa_legislativa()
        casa_legislativa = models.CasaLegislativa.objects.filter(
            nome_curto='cdep')
        self.assertEquals(casa_legislativa[0].nome, 'Camara dos Deputados')

    def test_deserialize_legislatura(self):

        importador_interno.main()
        parlamentar = models.Parlamentar.objects.filter(
            nome='Ivandro Cunha Lima')
        legislatura = models.Legislatura.objects.filter(
            parlamentar=parlamentar[0])
        self.assertEquals(
            legislatura[0].parlamentar.nome, 'Ivandro Cunha Lima')

    def test_deserialize_proposicao(self):

        importador_interno.main()
        proposicao = models.Proposicao.objects.filter(numero='4520')
        self.assertEquals(proposicao[0].sigla, 'PL')

    def test_deserialize_votacao(self):

        importador_interno.main()
        votacao = models.Votacao.objects.filter(id_vot='12345')
        self.assertEquals(str(votacao[0].data), '1900-12-05')

    def test_deserialize_voto(self):

        importador_interno.main()
        voto = models.Voto.objects.filter(opcao='TESTE')
        self.assertEquals(voto[0].opcao, 'TESTE')

    def test_importa_casa_legislativa(self):

        models.CasaLegislativa.deleta_casa('cmsp')
        models.CasaLegislativa.deleta_casa('cdep')

        importador_interno.importa_casa_legislativa('cdep')
        casa_legislativa = models.CasaLegislativa.objects.filter(
            nome_curto='cdep')
        self.assertEquals(casa_legislativa[0].nome, 'Camara dos Deputados')

        casa_cmsp = models.CasaLegislativa.objects.filter(nome_curto='cmsp')
        self.assertEquals(casa_cmsp[0].nome, 'Camara Municipal de Sao Paulo')
