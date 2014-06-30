# coding=utf8

# Copyright (C) 2012, Arthur Del Esposte, Leonardo Leite, Aline Santos,
# Gabriel Augusto, Thallys Martins, Thatiany Lima, Winstein Martins.
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
from modelagem import models
import re


class Temas():

    def __init__(self):
        self.dicionario = {}

    @staticmethod
    def get_temas_padrao():
        temas = Temas()
        sinonimos = {}
        sinonimos['educação'] = [
            'escola', 'professor', 'aluno', 'EAD', 'universidade', 'cotas']
        sinonimos['segurança'] = [
            'policial', 'polícia', 'bandido', 'PM', 'violência', 'presídios']
        sinonimos['economia'] = [
            'impostos', 'dívida', 'tributos', 'financeira']
        sinonimos['saúde'] = [
            'medicina', 'médicos', 'SUS', 'hospital', 'enfermeiro',
            'remédios', 'receita']
        sinonimos['transporte'] = ['trânsito', 'pedágio',
                                   'congestionamento', 'ônibus',
                                   'metrô', 'avião']
        sinonimos['violência'] = ['desarmamento', 'bullying']
        sinonimos['esporte'] = [
            'futebol', 'inclusão', 'torcida', 'estádio', 'copa', 'jogo']
        sinonimos['drogas'] = ['álcool', 'entorpecentes', 'maconha', 'cigarro']
        sinonimos['turismo'] = ['hotel', 'turista']
        sinonimos['meio ambiente'] = [
            'poluição', 'mineração', 'desmatamento', 'energia', 'usina']
        sinonimos['assistência social'] = ['bolsa', 'família', 'cidadania']
        sinonimos['tecnologia'] = [
            'inovação', 'internet', 'rede', 'dados', 'hacker']
        sinonimos['política'] = [
            'eleição', 'partido', 'mandato', 'eleitor', 'voto', 'reforma',
            'prefeito', 'deputado', 'vereador', 'senador', 'presidente',
            'sistema eleitoral']
        sinonimos['família'] = [
            'maternidade', 'mãe', 'pai', 'paternidade', 'adoção']
        sinonimos['constituição'] = ['PEC', 'constituinte']
        sinonimos['burocrática'] = [
            'pauta', 'quorum', 'urgência', 'adiamento', 'sessão']
        for i in sinonimos:
            for j in sinonimos[i]:
                temas.inserir_sinonimo(i, j)
        return temas

    def inserir_sinonimo(self, tema, sinonimo):
        if tema is None or sinonimo is None:
            raise ValueError('Impossivel adicionar sinonimo\n')
        if tema.encode('utf-8') in self.dicionario:
        # if self.dicionario.has_key(tema.encode('utf-8')):
            self.dicionario[tema.encode('utf-8')].add(sinonimo.encode('utf-8'))
        else:
            self.dicionario[tema.encode('utf-8')] = set()
            self.dicionario[tema.encode('utf-8')].add(sinonimo.encode('utf-8'))

    def expandir_palavras_chaves(self, palavras_chaves):
        expandido = []
        for palavra in palavras_chaves:
            expandido.extend(self.recuperar_sinonimos(palavra))
        return expandido

    def recuperar_sinonimos(self, palavra):
        palavra = palavra.encode('utf-8')
        palavras = []
        for tema, sinonimos in self.dicionario.items():
            if palavra in tema or self._palavra_in_sinonimos(palavra, sinonimos):
                palavras.append(tema)
                palavras.extend(sinonimos)
        if not palavras:
            palavras.append(palavra)
        return palavras

    def _palavra_in_sinonimos(self, palavra, sinonimos):
        for sinonimo in sinonimos:
            if palavra in sinonimo:
                return True
        return False


class FiltroVotacao():

    """Filtra votações pelos campos:
        * votacao.descricao
        * proposicao.ementa
        * proposicao.descricao
        * proposicao.indexacao
    """

    def __init__(self, casa_legislativa, periodo_casa_legislativa,
                 palavras_chave):
        """Argumentos:
            casa_legislativa -- objeto do tipo CasaLegislativa;
            somente votações desta casa serão filtradas.
            periodo_casa_legislativa -- objeto do tipo PeriodoCasaLegislativa;
            somente votações deste período serão filtradas.
            palavras_chave -- lista de strings para serem usadas na filtragem
            das votações.
        """
        self.casa_legislativa = casa_legislativa
        self.periodo_casa_legislativa = periodo_casa_legislativa
        self.palavras_chaves = palavras_chave
        self.temas = Temas.get_temas_padrao()
        self.votacoes = []

    def filtra_votacoes(self):
        self.votacoes = models.Votacao.por_casa_legislativa(
            self.casa_legislativa,
            self.periodo_casa_legislativa.ini,
            self.periodo_casa_legislativa.fim)
        if self.palavras_chaves:
            self.palavras_chaves = self.temas.expandir_palavras_chaves(
                self.palavras_chaves)
            self.votacoes = self._filtra_votacoes_por_palavras_chave()
        return self.votacoes

    def _filtra_votacoes_por_palavras_chave(self):
        votacoes_com_palavras_chave = []
        for votacao in self.votacoes:
            if self._verifica_palavras_chave_em_votacao(votacao):
                votacoes_com_palavras_chave.append(votacao)
        return votacoes_com_palavras_chave

    def _verifica_palavras_chave_em_votacao(self, votacao):
        for palavra_chave in self.palavras_chaves:
            if(self._palavra_existe_em_votacao(votacao, palavra_chave)):
                return True
        return False

    def _palavra_existe_em_votacao(self, votacao, palavra_chave):
        # procura uma substring dentro de uma string
        proposicao = votacao.proposicao
        if((re.search(palavra_chave.upper(),
            proposicao.descricao.upper()) is not None) or
           (re.search(palavra_chave.upper(),
            proposicao.ementa.upper()) is not None) or
           (re.search(palavra_chave.upper(),
            proposicao.indexacao.upper()) is not None) or
           (re.search(palavra_chave.upper(),
                      votacao.descricao.upper()) is not None)):
            return True
        else:
            return False
