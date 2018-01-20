# !/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Leonardo Leite
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

"""módulo convencao (Convenção Nacional Francesa)

Classes:
    ImportadorConvencao gera dados para casa legislativa fictícia chamada
    Convenção Nacional Francesa
"""

from __future__ import unicode_literals
from django.utils.dateparse import parse_datetime
from modelagem import models
import logging

logger = logging.getLogger("radar")

# Eu queria deixar as datas no século de 1700, mas o datetime só lida com
# datas a partir de 1900
INICIO_PERIODO = parse_datetime('1989-01-01 0:0:0')
FIM_PERIODO = parse_datetime('1989-12-30 0:0:0')

DATA_NO_PRIMEIRO_SEMESTRE = parse_datetime('1989-02-02 0:0:0')
DATA_NO_SEGUNDO_SEMESTRE = parse_datetime('1989-10-10 0:0:0')
DATA_VOTACAO_9 = parse_datetime('1990-01-01 0:0:0')

PARLAMENTARES_POR_PARTIDO = 3

GIRONDINOS = 'Girondinos'
JACOBINOS = 'Jacobinos'
MONARQUISTAS = 'Monarquistas'


class ImportadorConvencao:

    def _gera_casa_legislativa(self):
        conv = models.CasaLegislativa()
        conv.nome = 'Convenção Nacional Francesa'
        conv.nome_curto = 'conv'
        conv.esfera = models.FEDERAL
        conv.local = 'Paris (FR)'
        conv.save()
        return conv

    def _gera_partidos(self):
        girondinos = models.Partido()
        girondinos.nome = GIRONDINOS
        girondinos.numero = 27
        girondinos.cor = '#008000'
        girondinos.save()
        jacobinos = models.Partido()
        jacobinos.nome = JACOBINOS
        jacobinos.numero = 42
        jacobinos.cor = '#FF0000'
        jacobinos.save()
        monarquistas = models.Partido()
        monarquistas.nome = MONARQUISTAS
        monarquistas.numero = 79
        monarquistas.cor = '#800080'
        monarquistas.save()
        "self.partidos = {girondinos, jacobinos, monarquistas}"
        self.partidos = [girondinos, jacobinos, monarquistas]

    def _gera_parlamentares(self):
        # nome partido => lista de parlamentares do partido
        self.parlamentares = {}
        for partido in self.partidos:
            self.parlamentares[partido.nome] = []
            for i in range(0, PARLAMENTARES_POR_PARTIDO):
                parlamentar = models.Parlamentar()
                parlamentar.id_parlamentar = '%s%s' % (partido.nome[0], str(i))
                parlamentar.nome = 'Pierre'
                parlamentar.casa_legislativa = self.casa
                parlamentar.partido = partido
                parlamentar.save()
                self.parlamentares[partido.nome].append(parlamentar)

    def _gera_proposicao(self, num, descricao):
        prop = models.Proposicao()
        prop.id_prop = num
        prop.sigla = 'PL'
        prop.numero = num
        prop.ementa = descricao
        prop.descricao = descricao
        prop.casa_legislativa = self.casa
        prop.save()
        return prop

    def _gera_votacao(self, num, descricao, data, prop):
        votacao = models.Votacao()
        votacao.id_vot = num
        votacao.descricao = descricao
        votacao.data = data
        votacao.proposicao = prop
        votacao.save()
        return votacao

    def _gera_votos(self, votacao, nome_partido, opcoes):
        # opcoes é uma lista de opções (SIM, NÃO ...)
        for i in range(0, PARLAMENTARES_POR_PARTIDO):
            voto = models.Voto()
            voto.parlamentar = self.parlamentares[nome_partido][i]
            voto.opcao = opcoes[i]
            voto.votacao = votacao
            voto.save()

    def _gera_votacao1(self):

        numero_proposicao = '1'
        descricao_proposicao = 'Reforma agrária'
        prop = self._gera_proposicao(numero_proposicao, descricao_proposicao)
        votacao = self._gera_votacao(numero_proposicao, descricao_proposicao,
                                     DATA_NO_PRIMEIRO_SEMESTRE, prop)

        votos_girondinos = [models.SIM, models.ABSTENCAO, models.NAO]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.NAO, models.NAO, models.NAO]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    def _gera_votacao2(self):

        numero_proposicao = '2'
        descricao_proposicao = 'Aumento da pensão dos nobres'
        prop = self._gera_proposicao(numero_proposicao, descricao_proposicao)
        votacao = self._gera_votacao(numero_proposicao, descricao_proposicao,
                                     DATA_NO_PRIMEIRO_SEMESTRE, prop)

        votos_girondinos = [models.NAO, models.NAO, models.NAO]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.NAO, models.NAO, models.NAO]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    def _gera_votacao3(self):

        numero_proposicao = '3'
        descricao_proposicao = 'Institui o Dia de Carlos Magno'
        prop = self._gera_proposicao(numero_proposicao, descricao_proposicao)
        votacao = self._gera_votacao(numero_proposicao, descricao_proposicao,
                                     DATA_NO_PRIMEIRO_SEMESTRE, prop)

        votos_girondinos = [models.NAO, models.NAO, models.SIM]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.NAO, models.NAO, models.NAO]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    def _gera_votacao4(self):

        numero_proposicao = '4'
        descricao_proposicao = 'Diminuição de impostos sobre a indústria'
        prop = self._gera_proposicao(numero_proposicao, descricao_proposicao)
        votacao = self._gera_votacao(numero_proposicao, descricao_proposicao,
                                     DATA_NO_PRIMEIRO_SEMESTRE, prop)

        votos_girondinos = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.SIM, models.ABSTENCAO, models.NAO]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.SIM, models.NAO, models.AUSENTE]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    def _gera_votacao5(self):

        numero_proposicao = '5'
        descricao_proposicao = 'Guilhotinar o Conde Pierre'
        prop = self._gera_proposicao(numero_proposicao, descricao_proposicao)
        votacao = self._gera_votacao(numero_proposicao, descricao_proposicao,
                                     DATA_NO_SEGUNDO_SEMESTRE, prop)

        votos_girondinos = [models.SIM, models.SIM, models.ABSTENCAO]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.NAO, models.NAO, models.NAO]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    def _gera_votacao6(self):

        numero_proposicao = '6'
        descricao_proposicao = 'Criação de novas escolas'
        prop = self._gera_proposicao(numero_proposicao, descricao_proposicao)
        votacao = self._gera_votacao(numero_proposicao, descricao_proposicao,
                                     DATA_NO_SEGUNDO_SEMESTRE, prop)

        votos_girondinos = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.AUSENTE, models.SIM, models.SIM]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    def _gera_votacao7(self):

        numero_proposicao = '7'
        descricao_proposicao = 'Aumento do efetivo militar'
        prop = self._gera_proposicao(numero_proposicao, descricao_proposicao)
        votacao = self._gera_votacao(numero_proposicao, descricao_proposicao,
                                     DATA_NO_SEGUNDO_SEMESTRE, prop)

        votos_girondinos = [models.SIM, models.SIM, models.ABSTENCAO]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.SIM, models.AUSENTE, models.SIM]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    # votação com atributos diferentes para teste
    def _gera_votacao8(self):

        numero_proposicao = '8'
        descricao_proposicao = 'Guerra contra a Inglaterra'
        prop = models.Proposicao()
        prop.id_prop = numero_proposicao
        prop.sigla = 'PL'
        prop.numero = numero_proposicao
        prop.ementa = 'o uso proibido de armas químicas'
        prop.descricao = 'descricao da guerra'
        prop.casa_legislativa = self.casa
        prop.indexacao = 'bombas, efeitos, destruições'
        prop.save()
        votacao = self._gera_votacao(numero_proposicao, descricao_proposicao,
                                     DATA_NO_SEGUNDO_SEMESTRE, prop)

        votos_girondinos = [models.NAO, models.NAO, models.NAO]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.ABSTENCAO, models.NAO, models.NAO]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.SIM, models.AUSENTE, models.SIM]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    def _gera_votacao9(self):
        numero_proposicao = '9'
        descricao_proposicao = 'Contratar médicos para a capital'
        prop = self._gera_proposicao(numero_proposicao, descricao_proposicao)
        votacao = self._gera_votacao(numero_proposicao, descricao_proposicao,
                                     DATA_VOTACAO_9, prop)

        votos_girondinos = [models.SIM, models.SIM, models.ABSTENCAO]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.SIM, models.AUSENTE, models.SIM]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    def importar(self):
        self.casa = self._gera_casa_legislativa()
        self._gera_partidos()
        self._gera_parlamentares()
        self._gera_votacao1()
        self._gera_votacao2()
        self._gera_votacao3()
        self._gera_votacao4()
        self._gera_votacao5()
        self._gera_votacao6()
        self._gera_votacao7()
        self._gera_votacao8()
        self._gera_votacao9()
        self._gera_proposicao('10', 'Legalizacao da maconha')


def main():

    logger.info('IMPORTANDO DADOS DA CONVENÇÃO NACIONAL FRANCESA')
    importer = ImportadorConvencao()
    importer.importar()
