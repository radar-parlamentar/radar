# coding=utf8

# Copyright (C) 2012, Arthur Del Esposte, Leonardo Leite, Aline Santos, Gabriel Augusto, Thallys Martins, Thatiany Lima, Winstein Martins.
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

    dicionario = {}   
           
  
    @staticmethod
    def get_temas_padrao():
	temas = Temas()
        sinonimos = {}
        sinonimos['educação'] = ['escola', 'professor', 'aluno', 'EAD', 'universidade', 'cotas']
        sinonimos['segurança'] = ['policial', 'polícia', 'bandido', 'PM','violência', 'presídios']
        sinonimos['economia'] = ['impostos', 'dívida', 'tributos']
        sinonimos['saúde'] = ['medicina', 'médicos', 'SUS', 'hospital', 'enfermeiro', 'remédios', 'receita']
        sinonimos['transporte'] = ['trânsito', 'pedágio', 'congestionamento', 'ônibus', 'metrô', 'avião'] 
        sinonimos['violência'] = ['desarmamento', 'bullying']
        sinonimos['esporte'] = ['futebol', 'inclusão', 'torcida', 'estádio', 'copa', 'jogo']
        sinonimos['drogas'] = ['álcool', 'entorpecentes', 'maconha', 'cigarro']
        sinonimos['turismo'] = ['hotel', 'turista']
        sinonimos['meio ambiente'] = ['poluição', 'mineração', 'desmatamento', 'energia', 'usina']
        sinonimos['assistência social'] = ['bolsa', 'família', 'cidadania']
        sinonimos['tecnologia'] = ['inovação', 'internet', 'rede', 'dados', 'hacker']
        sinonimos['política'] = ['eleição', 'partido', 'mandato', 'sistema eleitoral', 'voto', 'reforma', 'prefeito', 'deputado', 'vereador', 'senador', 'presidente', 'eleitor']
        for i in sinonimos:
            for j in sinonimos[i]:
                temas.inserir_sinonimo(i,j)
	return temas
	
	

    def inserir_sinonimo(self, tema, sinonimo):
        if tema == None or sinonimo == None:
            raise ValueError('Impossivel adicionar sinonimo\n')
        if self.dicionario.has_key(tema.encode('utf-8')):
		 self.dicionario[tema.encode('utf-8')].add(sinonimo.encode('utf-8'))
        else:
            self.dicionario[tema.encode('utf-8')] = set()
            self.dicionario[tema.encode('utf-8')].add(sinonimo.encode('utf-8'))

    def recuperar_palavras_por_sinonimo(self, sinonimo):
        if sinonimo == None:
            raise ValueError('Impossivel encontrar palavra\n')

        palavras = []
        for e in self.dicionario:
            
            if sinonimo in self.dicionario[e]:
                palavras.append(e)

        return palavras

class FiltroVotacao():

    def filtra_votacoes(self, casa_legislativa, periodo_casa_legislativa, palavras_chave):
        """Argumentos:
            casa_legislativa -- objeto do tipo CasaLegislativa; somente votações desta casa serão filtradas.
            periodo_casa_legislativa -- objeto do tipo PeriodoCasaLegislativa; somente votações deste período serão filtradas.
            palavras_chave -- lista de strings para serem usadas na filtragem das votações.
        """
        proposicoes = self._recupera_proposicoes(casa_legislativa)

        votacoes = models.Votacao.por_casa_legislativa(casa_legislativa, periodo_casa_legislativa.ini, periodo_casa_legislativa.fim)
        if palavras_chave==[]:
            votacoes_com_palavras_chave = votacoes   
        else:
            proposicoes_com_votacoes = self._filtra_proposicoes_com_votacoes(proposicoes, votacoes)

            votacoes_com_palavras_chave = self._filtra_votacoes_por_palavras_chave(proposicoes_com_votacoes, votacoes, palavras_chave)

        return votacoes_com_palavras_chave

    def _recupera_proposicoes(self, casa_legislativa):
        return models.Proposicao.objects.filter(casa_legislativa_id = casa_legislativa.id)

    def _recupera_votacoes_da_proposicao(self,proposicao, votacoes):
        votacoes_da_proposicao = []
        for votacao in votacoes:
            if votacao.proposicao_id == proposicao.id:
                votacoes_da_proposicao.append(votacao)
        return votacoes_da_proposicao        

    def _filtra_proposicoes_com_votacoes(self, proposicoes, votacoes):
        proposicoes_com_votacoes = []
        for proposicao in proposicoes:
            if len(self._recupera_votacoes_da_proposicao(proposicao, votacoes)) > 0:
                proposicoes_com_votacoes.append(proposicao)
        return proposicoes_com_votacoes 
    
    def _palavra_existe_em_proposicao(self, proposicao, votacoes, palavra_chave):
        #procura uma substring dentro de uma string
        if((re.search(palavra_chave.upper(), proposicao.descricao.upper())!= None) or (re.search(palavra_chave.upper(), proposicao.ementa.upper())!= None) or (re.search(palavra_chave.upper(),       proposicao.indexacao.upper())!= None)):
            return True

        for votacao in votacoes:
            if(re.search(palavra_chave.upper(), votacao.descricao.upper())!= None):
                return True
        return False	 

    def _verifica_palavras_chave_em_proposicao(self, proposicao, votacoes, lista_palavras_chave):
        votacoes_da_proposicao = self._recupera_votacoes_da_proposicao(proposicao, votacoes)
        for palavra_chave in lista_palavras_chave:
            if(self._palavra_existe_em_proposicao(proposicao, votacoes_da_proposicao, palavra_chave)):
                return True
        return False

    def _filtra_votacoes_por_palavras_chave(self, proposicoes, votacoes, palavras_chave):
        votacoes_com_palavras_chave = []

        for proposicao in proposicoes:
            if self._verifica_palavras_chave_em_proposicao(proposicao, votacoes, palavras_chave):
                votacoes_com_palavras_chave.extend(self._recupera_votacoes_da_proposicao(proposicao, votacoes))
        return votacoes_com_palavras_chave
