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

from modelagem.models import CasaLegislativa, Parlamentar, Proposicao

class Genero:

    def __init__(self):
        self.palavras = []
        self.dicionario_palavras = {}

    def agrupa_palavras(self, genero, id_casa_legislativa):
        for parlamentar in Parlamentar.objects.filter(genero=genero, casa_legislativa_id=id_casa_legislativa):
            for proposicao in Proposicao.objects.filter(autor_principal=parlamentar.nome):
                for palavra in proposicao.indexacao.split(','):
                    if len(palavra) != 0:
                        self.palavras.append(palavra.strip().lower())
        return self.define_chaves_dicionario(self.palavras)


    def define_chaves_dicionario(self, palavras):
        for palavra in palavras:
            if palavra in self.dicionario_palavras:
                self.dicionario_palavras[palavra] = self.dicionario_palavras[palavra] + 1
            else:
                self.dicionario_palavras[palavra] = 1
        return self.organiza_lista_palavras(self.dicionario_palavras)

    def organiza_lista_palavras(self, dicionario_palavras):
        numero_maximo_de_palavras = 51
        temas_frequencia = sorted(
            list(dicionario_palavras.items()), reverse=True, key=lambda i: i[1])
        temas_frequencia = temas_frequencia[:numero_maximo_de_palavras]
        return temas_frequencia


    '''
    Retorna as casas legislativas que tenham parlamentares com a informacao de genero
    '''
    @staticmethod
    def get_casas_legislativas_com_genero():

        casas_legislativas = []

        for casa in CasaLegislativa.objects.all():
            for parlamentar in Parlamentar.objects.filter(casa_legislativa_id=casa.id):
                if parlamentar.genero != "":
                    casas_legislativas.append(casa)
                    break

        return casas_legislativas
