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

ULTIMA_ATUALIZACAO = parse_datetime('2012-06-01 0:0:0')

# Eu queria deixar as datas no século de 1700, mas o datetime só lida com
# datas a partir de 1900
INICIO_PERIODO = parse_datetime('1989-01-01 0:0:0')
FIM_PERIODO = parse_datetime('1989-12-30 0:0:0')

DATA_NO_PRIMEIRO_SEMESTRE = parse_datetime('1989-02-02 0:0:0')
DATA_NO_SEGUNDO_SEMESTRE = parse_datetime('1989-10-10 0:0:0')

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
        conv.atualizacao = ULTIMA_ATUALIZACAO
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
        self.partidos = {girondinos, jacobinos, monarquistas}

    def _gera_legislaturas(self):
        self.legs = {}  # nome partido => lista de legislaturas do partido
        for p in self.partidos:
            self.legs[p.nome] = []
            for i in range(0, PARLAMENTARES_POR_PARTIDO):

                parlamentar = models.Parlamentar()
                parlamentar.id_parlamentar = '%s%s' % (p.nome[0], str(i))
                parlamentar.nome = 'Pierre'
                parlamentar.save()

                leg = models.Legislatura()
                leg.casa_legislativa = self.casa
                leg.inicio = INICIO_PERIODO
                leg.fim = FIM_PERIODO
                leg.partido = p
                leg.parlamentar = parlamentar
                leg.save()
                self.legs[p.nome].append(leg)

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
            voto.legislatura = self.legs[nome_partido][i]
            voto.opcao = opcoes[i]
            voto.votacao = votacao
            voto.save()

    def _gera_votacao1(self):

        NUM = '1'
        DESCRICAO = 'Reforma agrária'
        prop = self._gera_proposicao(NUM, DESCRICAO)
        votacao = self._gera_votacao(
            NUM, DESCRICAO, DATA_NO_PRIMEIRO_SEMESTRE, prop)

        votos_girondinos = [models.SIM, models.ABSTENCAO, models.NAO]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.NAO, models.NAO, models.NAO]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    def _gera_votacao2(self):

        NUM = '2'
        DESCRICAO = 'Aumento da pensão dos nobres'
        prop = self._gera_proposicao(NUM, DESCRICAO)
        votacao = self._gera_votacao(
            NUM, DESCRICAO, DATA_NO_PRIMEIRO_SEMESTRE, prop)

        votos_girondinos = [models.NAO, models.NAO, models.NAO]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.NAO, models.NAO, models.NAO]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    def _gera_votacao3(self):

        NUM = '3'
        DESCRICAO = 'Institui o Dia de Carlos Magno'
        prop = self._gera_proposicao(NUM, DESCRICAO)
        votacao = self._gera_votacao(
            NUM, DESCRICAO, DATA_NO_PRIMEIRO_SEMESTRE, prop)

        votos_girondinos = [models.NAO, models.NAO, models.SIM]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.NAO, models.NAO, models.NAO]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    def _gera_votacao4(self):

        NUM = '4'
        DESCRICAO = 'Diminuição de impostos sobre a indústria'
        prop = self._gera_proposicao(NUM, DESCRICAO)
        votacao = self._gera_votacao(
            NUM, DESCRICAO, DATA_NO_PRIMEIRO_SEMESTRE, prop)

        votos_girondinos = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.SIM, models.ABSTENCAO, models.NAO]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.SIM, models.NAO, models.AUSENTE]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    def _gera_votacao5(self):

        NUM = '5'
        DESCRICAO = 'Guilhotinar o Conde Pierre'
        prop = self._gera_proposicao(NUM, DESCRICAO)
        votacao = self._gera_votacao(
            NUM, DESCRICAO, DATA_NO_SEGUNDO_SEMESTRE, prop)

        votos_girondinos = [models.SIM, models.SIM, models.ABSTENCAO]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.NAO, models.NAO, models.NAO]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    def _gera_votacao6(self):

        NUM = '6'
        DESCRICAO = 'Criação de novas escolas'
        prop = self._gera_proposicao(NUM, DESCRICAO)
        votacao = self._gera_votacao(
            NUM, DESCRICAO, DATA_NO_SEGUNDO_SEMESTRE, prop)

        votos_girondinos = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.AUSENTE, models.SIM, models.SIM]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    def _gera_votacao7(self):

        NUM = '7'
        DESCRICAO = 'Aumento do efetivo militar'
        prop = self._gera_proposicao(NUM, DESCRICAO)
        votacao = self._gera_votacao(
            NUM, DESCRICAO, DATA_NO_SEGUNDO_SEMESTRE, prop)

        votos_girondinos = [models.SIM, models.SIM, models.ABSTENCAO]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.SIM, models.SIM, models.SIM]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.SIM, models.AUSENTE, models.SIM]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    # votação com atributos diferentes para teste
    def _gera_votacao8(self):

        NUM = '8'
        DESCRICAO = 'Guerra contra a Inglaterra'
        prop = models.Proposicao()
        prop.id_prop = NUM
        prop.sigla = 'PL'
        prop.numero = NUM
        prop.ementa = 'o uso proibido de armas químicas'
        prop.descricao = 'descricao da guerra'
        prop.casa_legislativa = self.casa
        prop.indexacao = 'bombas, efeitos, destruições'
        prop.save()
        votacao = self._gera_votacao(
            NUM, DESCRICAO, DATA_NO_SEGUNDO_SEMESTRE, prop)

        votos_girondinos = [models.NAO, models.NAO, models.NAO]
        self._gera_votos(votacao, GIRONDINOS, votos_girondinos)

        votos_jacobinos = [models.ABSTENCAO, models.NAO, models.NAO]
        self._gera_votos(votacao, JACOBINOS, votos_jacobinos)

        votos_monarquistas = [models.SIM, models.AUSENTE, models.SIM]
        self._gera_votos(votacao, MONARQUISTAS, votos_monarquistas)

    def importar(self):
        self.casa = self._gera_casa_legislativa()
        self._gera_partidos()
        self._gera_legislaturas()
        self._gera_votacao1()
        self._gera_votacao2()
        self._gera_votacao3()
        self._gera_votacao4()
        self._gera_votacao5()
        self._gera_votacao6()
        self._gera_votacao7()
        self._gera_votacao8()
        self._gera_proposicao('9', 'Legalizacao da maconha')


def main():

    print 'IMPORTANDO DADOS DA CONVENÇÃO NACIONAL FRANCESA'
    importer = ImportadorConvencao()
    importer.importar()
