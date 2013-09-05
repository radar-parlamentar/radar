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

class Temas():

    dicionario = {}   

    @staticmethod
    def get_temas_padrao():
        temas = Temas()

        temas.inserir_sinonimo("educação", 'escola')
        temas.inserir_sinonimo("educação", 'professor')
        temas.inserir_sinonimo("educação", 'aluno')

        temas.inserir_sinonimo("segurança", 'policial')
        temas.inserir_sinonimo("segurança", 'polícia')
        temas.inserir_sinonimo("segurança", 'bandido')

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
