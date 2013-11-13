# coding=utf8

# Copyright (C) 2012, Arthur Del Esposte, Leonardo Leite
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

class FiltroProposicao():

    def recupera_proposicoes(self, casa_legislativa):
        return models.Proposicao.objects.filter(casa_legislativa_id = casa_legislativa.id)

    def recupera_votacoes_da_proposicao(self,proposicao, votacoes):
        votacoes_da_proposicao = []
        for votacao in votacoes:
            if votacao.proposicao_id == proposicao.id:
                votacoes_da_proposicao.append(votacao)
        return votacoes_da_proposicao        

    def filtra_proposicoes_com_votacoes(self, proposicoes, votacoes):
        proposicoes_com_votacoes = []
        for proposicao in proposicoes:
            if len(self.recupera_votacoes_da_proposicao(proposicao, votacoes)) > 0:
                proposicoes_com_votacoes.append(proposicao)
        return proposicoes_com_votacoes 

    def filtra_proposicoes(self, casa_legislativa, periodo_casa_legislativa, palavras_chave):
        proposicoes = self.recupera_proposicoes(casa_legislativa)
        votacoes = models.Votacao.por_casa_legislativa(casa_legislativa, periodo_casa_legislativa.ini, periodo_casa_legislativa.fim)

        proposicoes_com_votacoes = filtra_proposicoes_com_votacoes(proposicoes, votacoes)

        return None

    '''def valida_proposicoes(self, lista_proposicoes):
        proposicoes_validas = []
        for proposicao in lista_proposicoes:
            if proposicao != None:
                proposicoes_validas.append(proposicao)
        return proposicoes_validas

    def palavra_existe_em_proposicao(self, proposicao, lista_palavras_chave):
        for palavra_chave in lista_palavras_chave:
            #procura uma substring dentro de uma string
            if(re.search(palavra_chave.upper(), proposicao.descricao.upper())!= None):
                return True		                    
        return False

    def verifica_proposicoes_no_banco(self, lista_proposicoes):
        proposicoes_validas = self.valida_proposicoes(lista_proposicoes)
        resultado = []
        proposicoes_persistidas = models.Proposicao.objects.all()
        for proposicao in proposicoes_validas:
            if proposicao in proposicoes_persistidas:
                resultado.append(proposicao)
        return resultado

    def filtra_proposicao(self, lista_proposicoes, lista_palavras):
        resultado = []
        proposicoes_validas = verifica_proposicoes_no_banco(lista_proposicoes)
        for proposicao in proposicoes_validas:
            if(palavra_existe_em_proposicao(proposicao, lista_palavras)):
                resultado.append(proposicao)
        imprimeDadosDeProposicoes(resultado)			
        return resultado

        proposicao = models.Proposicao.objects.filter(descricao = ).filter()
        lista_proposicoes_validas = valida_proposicao(lista_proposicoes)
        resultado = []
        for proposicao in lista_proposicoes_validas:
            if(busca_palavras(proposicao, lista_palavras))
                resultado.append(proposicao)
        if resultado == None:
            print 'Não foi encontrado resultado!' 
        else:
            imprimeDadosProposicao(resultado)'''
