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

    @staticmethod
    def definir_palavras(genero, id_casa_legislativa):
        temas = []
        for parlamentar in Parlamentar.objects.filter(genero=genero, casa_legislativa_id=id_casa_legislativa):
            for proposicao in Proposicao.objects.filter(
                    autor_principal=parlamentar.nome):
                for tema in proposicao.indexacao.split(','):
                    if len(tema) != 0:
                        temas.append(tema.strip().lower())

        temas_dicionario = {}

        for tema in temas:
            if temas_dicionario.has_key(tema):
                temas_dicionario[tema] = temas_dicionario[tema] + 1
            else:
                temas_dicionario[tema] = 1

        temas_frequencia = sorted(
            temas_dicionario.items(), reverse=True, key=lambda i: i[1])
        temas_frequencia = temas_frequencia[:51]

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

