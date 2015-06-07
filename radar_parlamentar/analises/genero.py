# coding=utf8

# Copyright (C) 2015, Vanessa Soares, Thaiane Braga
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

from modelagem.models import Proposicao
from modelagem.models import Parlamentar

class Genero:

	@staticmethod
	def definir_palavras_mulher():
	    temas = []
	    for parlamentar_mulher in Parlamentar.objects.filter(genero = 'F'): 
	      for proposicao in Proposicao.objects.filter(autor_principal = parlamentar_mulher.nome):    
	        for tema in proposicao.indexacao.split(','):
	            if len(tema) != 0:
	                temas.append(tema.strip().lower())

	    temas_dicionario = {}

	    for tema in temas:
	        if temas_dicionario.has_key(tema):
	            temas_dicionario[tema] = temas_dicionario[tema] + 1
	        else:
	            temas_dicionario[tema] = 1

	    temas_frequencia = sorted(temas_dicionario.items(), reverse=True, key=lambda i: i[1])
	    temas_frequencia = temas_frequencia[:51]

	    return temas_frequencia

	@staticmethod
	def definir_palavras_homem():
	    temas = []
	    for parlamentar_homem in Parlamentar.objects.filter(genero = 'M'): 
	      for proposicao in Proposicao.objects.filter(autor_principal = parlamentar_homem.nome):    
	        for tema in proposicao.indexacao.split(','):
	            if len(tema) != 0:
	                temas.append(tema.strip().lower())

	    temas_dicionario = {}

	    for tema in temas:
	        if temas_dicionario.has_key(tema):
	            temas_dicionario[tema] = temas_dicionario[tema] + 1
	        else:
	            temas_dicionario[tema] = 1

	    temas_frequencia = sorted(temas_dicionario.items(), reverse=True, key=lambda i: i[1])
	    temas_frequencia = temas_frequencia[:51]

	    return temas_frequencia
