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

class Filtro_Proposicao():

    def imprimeDadosProposicao(proposicao):
        

    def valida_proposicao(lista_proposicoes):
        proposicoes_validas = []
        for proposicao in lista_proposicoes:
            if isOK(proposicao):
                proposicoes_validas.append(proposicao)
        return proposicoes_validas

    def busca_proposicao(lista_proposicoes, lista_palavras_chave):
        lista_resultado_proposicoes = []
        for proposicao in lista_proposicoes:
            for palavra_chave in lista_palavras_chave:
                #procura uma substring dentro de uma string
                if(re.search(palavra_chave, proposicao.descricao)!= None):
                    lista_resultado_proposicoes.append(proposicao)
                    break
        return lista_resultado_proposicoes

    def filtra_proposicao(lista_proposicoes, lista_palavras):
    	proposicao = models.Proposicao.objects.all()
        lista_proposicoes_validas = valida_proposicao(lista_proposicoes)
        resultado = busca_proposicao(lista_proposicoes_validas, lista_palavras)
        if resultado == None:
            print 'Não foi encontrado resultado!' 
        else:
            print 'Descricao:' + resultado[].descricao + '\n'
	for r in lista_siglas:
		sigla = r
		for p in proposicao:
			if(sigla == p.sigla):
				for e in lista_palavras:
					
					palavra = e
					if(busca_proposicao()):
						print 'Descricao:' + p.descricao + '\n'
    						print 'Ementa:' + p.ementa + '\n'
						print 'Indexacao' + p.indexao
						lista_proposicao.append(p.descricao)
						lista_proposicao.append(p.ementa)

					else:
						print 'palavra: ' + palavra + ' nao encontrada na descricao: ' + p.descricao + '\n' 

	
	return lista_proposicao
