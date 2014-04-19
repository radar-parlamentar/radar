# coding=utf8

# Copyright (C) 2014, Leonardo Leite
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

from analises import filtro
from modelagem import models
from importadores import convencao
from datetime import date


class FiltroVotacaoTest(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.importer = convencao.ImportadorConvencao()
        cls.importer.importar()

    @classmethod
    def tearDownClass(cls):
        from util_test import flush_db
        flush_db(cls)

    def test_recupera_proposicoes(self):
        casa_legislativa = models.CasaLegislativa()
        casa_legislativa.id = 1

        filtro_votacao = filtro.FiltroVotacao()
        proposicoes = filtro_votacao._recupera_proposicoes(casa_legislativa)
        self.assertEquals(9, len(proposicoes))

    def test_recupera_votacoes_da_proposicao(self):
        proposicao = models.Proposicao()
        proposicao.id = 1;
        votacoes = models.Votacao.objects.all()
        filtro_votacao = filtro.FiltroVotacao()
        votacoes_da_proposicao = filtro_votacao._recupera_votacoes_da_proposicao(proposicao, votacoes)        
        self.assertEquals(1, len(votacoes_da_proposicao))

    def test_filtra_proposicoes_com_votacoes(self):
        proposicoes = models.Proposicao.objects.filter(casa_legislativa_id = 1)
        votacoes = models.Votacao.objects.all()
        filtro_votacao = filtro.FiltroVotacao()
        proposicoes_com_votacoes = filtro_votacao._filtra_proposicoes_com_votacoes(proposicoes, votacoes)
        self.assertEquals(8, len(proposicoes_com_votacoes))

    def test_filtra_proposicoes_sem_votacoes(self):
        proposicoes = models.Proposicao.objects.filter(casa_legislativa_id = 1)
        votacoes = models.Votacao.objects.all()
        filtro_votacao = filtro.FiltroVotacao()
        proposicoes_com_votacoes = filtro_votacao._filtra_proposicoes_com_votacoes(proposicoes, votacoes)
        self.assertEquals(8, len(proposicoes_com_votacoes))

    def test_palavra_existe_em_descricao_proposicao(self):
        proposicao = models.Proposicao.objects.get(id = 1)
        votacoes = models.Votacao.objects.filter(proposicao_id = 1)
        palavra_chave = 'reforma'
        filtro_votacao = filtro.FiltroVotacao()
        palavra_existe_em_proposicao = filtro_votacao._palavra_existe_em_proposicao(proposicao, votacoes, palavra_chave)
        self.assertTrue(palavra_existe_em_proposicao)
        
    def test_palavra_nao_existe_em_proposicao(self):
        proposicao = models.Proposicao.objects.get(id = 1)
        votacoes = models.Votacao.objects.filter(proposicao_id = 1)
        palavra_chave = 'corrupcao'
        filtro_votacao = filtro.FiltroVotacao()
        palavra_existe_em_proposicao = filtro_votacao._palavra_existe_em_proposicao(proposicao, votacoes, palavra_chave)
        self.assertFalse(palavra_existe_em_proposicao)

    def test_palavra_existe_em_ementa_proposicao(self):
        proposicao = models.Proposicao.objects.get(id = 8)
        votacoes = models.Votacao.objects.filter(proposicao_id = 8)
        palavra_chave = 'armas'
        filtro_votacao = filtro.FiltroVotacao()
        palavra_existe_em_proposicao = filtro_votacao._palavra_existe_em_proposicao(proposicao, votacoes, palavra_chave)
        self.assertTrue(palavra_existe_em_proposicao)

    def test_palavra_existe_em_indexacao_proposicao(self):
        proposicao = models.Proposicao.objects.get(id = 8)
        votacoes = models.Votacao.objects.filter(proposicao_id = 8)
        palavra_chave = 'bombas'
        filtro_votacao = filtro.FiltroVotacao()
        palavra_existe_em_proposicao = filtro_votacao._palavra_existe_em_proposicao(proposicao, votacoes, palavra_chave)
        self.assertTrue(palavra_existe_em_proposicao)

    def test_palavra_existe_em_descricao_votacao(self):
        proposicao = models.Proposicao.objects.get(id = 8)
        votacoes = models.Votacao.objects.filter(proposicao_id = 8)
        palavra_chave = 'inglaterra'
        filtro_votacao = filtro.FiltroVotacao()
        palavra_existe_em_proposicao = filtro_votacao._palavra_existe_em_proposicao(proposicao, votacoes, palavra_chave)
        self.assertTrue(palavra_existe_em_proposicao)

    def test_verifica_palavras_chave_em_proposicao(self):
        proposicao = models.Proposicao.objects.get(id = 8)
        votacoes = models.Votacao.objects.filter(proposicao_id = 8)
        lista_palavras_chave = ['cotas', 'guerra', 'violência']
        filtro_votacao = filtro.FiltroVotacao()
        filtra_proposicoes_por_palavras_chave = filtro_votacao._verifica_palavras_chave_em_proposicao(proposicao, votacoes, lista_palavras_chave)
        self.assertTrue(filtra_proposicoes_por_palavras_chave)
          
    def test_verifica_palavras_chave_nao_relacionadas_em_proposicao(self):
        proposicao = models.Proposicao.objects.get(id = 8)
        votacoes = models.Votacao.objects.filter(proposicao_id = 8)
        lista_palavras_chave = ['cotas', 'educação', 'violência']
        filtro_votacao = filtro.FiltroVotacao()
        filtra_proposicoes_por_palavras_chave = filtro_votacao._verifica_palavras_chave_em_proposicao(proposicao, votacoes, lista_palavras_chave)
        self.assertFalse(filtra_proposicoes_por_palavras_chave)

    def test_filtra_votacoes(self):
        casa_legislativa = models.CasaLegislativa.objects.get(id = 1)
        periodo_casa_legislativa = models.PeriodoCasaLegislativa(date(1989,02,02), date(1989,10,10))
        lista_palavras_chave = ['cotas', 'guerra', 'violência']
        filtro_votacao = filtro.FiltroVotacao()
        votacoes_filtradas = filtro_votacao.filtra_votacoes(casa_legislativa, periodo_casa_legislativa, lista_palavras_chave)
        self.assertEquals(1, len(votacoes_filtradas)) 
     
         
    def test_filtra_votacoes_com_periodo_invalido(self):
        casa_legislativa = models.CasaLegislativa.objects.get(id = 1)
        periodo_casa_legislativa = models.PeriodoCasaLegislativa(date(1990,10,10), date(1990,10,10))
        lista_palavras_chave = ['cotas', 'guerra', 'violência']
        filtro_votacao = filtro.FiltroVotacao()
        votacoes_filtradas = filtro_votacao.filtra_votacoes(casa_legislativa, periodo_casa_legislativa, lista_palavras_chave)
        self.assertEquals(0, len(votacoes_filtradas)) 

    def test_filtra_votacoes_com_periodo_(self):
        casa_legislativa = models.CasaLegislativa.objects.get(id = 1)
        periodo_casa_legislativa = models.PeriodoCasaLegislativa(date(1989,8,8), date(1992,11,11))
        lista_palavras_chave = ['cotas', 'guerra', 'violência']
        filtro_votacao = filtro.FiltroVotacao()
        votacoes_filtradas = filtro_votacao.filtra_votacoes(casa_legislativa, periodo_casa_legislativa, lista_palavras_chave)
        self.assertEquals(1, len(votacoes_filtradas)) 
     
    def test_filtra_votacoes_sem_palavras_chave_relacionadas(self):
        casa_legislativa = models.CasaLegislativa.objects.get(id = 1)
        periodo_casa_legislativa = models.PeriodoCasaLegislativa(date(1989,02,02), date(1989,10,10))
        lista_palavras_chave = ['cotas', 'educacao', 'violência']
        filtro_votacao = filtro.FiltroVotacao()
        votacoes_filtradas = filtro_votacao.filtra_votacoes(casa_legislativa, periodo_casa_legislativa, lista_palavras_chave)
        self.assertEquals(0, len(votacoes_filtradas))

    def test_filtra_votacoes_com_varias_palavras_chave(self):
        casa_legislativa = models.CasaLegislativa.objects.get(id = 1)
        periodo_casa_legislativa = models.PeriodoCasaLegislativa(date(1989,02,02), date(1989,10,10))
        lista_palavras_chave = ['militar', 'guerra', 'escolas', 'pensão']
        filtro_votacao = filtro.FiltroVotacao()
        votacoes_filtradas = filtro_votacao.filtra_votacoes(casa_legislativa, periodo_casa_legislativa, lista_palavras_chave)
        self.assertEquals(4, len(votacoes_filtradas))


    def test_filtra_votacoes_por_palavras_chave(self):
        proposicoes = models.Proposicao.objects.filter(casa_legislativa_id = 1)
        votacoes = models.Votacao.objects.all()
        lista_palavras_chave = ['militar', 'guerra', 'escolas', 'pensão']
        filtro_votacao = filtro.FiltroVotacao()
        votacoes_com_palavras_chave = filtro_votacao._filtra_votacoes_por_palavras_chave(proposicoes, votacoes, lista_palavras_chave)
        self.assertEquals(4, len(votacoes_com_palavras_chave))



class TemasTest(TestCase):

    dici = None

    def setUp(self):
        self.dici = filtro.Temas.get_temas_padrao()
        self.dici.inserir_sinonimo("testing","test")

    def test_criacao_dicionario(self):
        self.assertTrue(len(self.dici.dicionario.items()) > 0)
    
    def test_insercao_palavra_nova(self):
        self.dici.inserir_sinonimo("teste", "test")
        self.assertTrue(self.dici.dicionario.has_key("teste"))

    def test_insercao_sinonimo_novo(self):
        self.dici.inserir_sinonimo("testing", "teste")
        self.assertEquals(2, len(self.dici.dicionario["testing"]))

    def test_insercao_erro(self):
        with self.assertRaises(ValueError):
            self.dici.inserir_sinonimo("testing", None)
            
        with self.assertRaises(ValueError):
            self.dici.inserir_sinonimo(None, "dinossauro")

    def test_recuperacao_com_uma_chave(self):
        self.dici.inserir_sinonimo("testing","assert")
        palavras = self.dici.recuperar_palavras_por_sinonimo("assert")
        self.assertEquals(1, len(palavras))

        self.dici.inserir_sinonimo("another","assert")
        palavras = self.dici.recuperar_palavras_por_sinonimo("assert")
        self.assertEquals(2, len(palavras))

        palavras = self.dici.recuperar_palavras_por_sinonimo("sandslash")
        self.assertEquals(0, len(palavras))

    def test_recuperacao_erro(self):
        with self.assertRaises(ValueError):
            self.dici.recuperar_palavras_por_sinonimo(None)
