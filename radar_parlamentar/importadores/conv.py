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

    def _gera_dados(self, dictionary):
        prop = self._gera_proposicao(dictionary['numero_proposicao'], dictionary['descricao_proposicao'])
        votacao = self._gera_votacao(dictionary['numero_proposicao'], dictionary['descricao_proposicao'],
                                     DATA_NO_PRIMEIRO_SEMESTRE, prop)
        self._gera_votos(votacao, GIRONDINOS, dictionary['votos_girondinos'])
        self._gera_votos(votacao, JACOBINOS, dictionary['votos_jacobinos'])
        self._gera_votos(votacao, MONARQUISTAS, dictionary['votos_monarquistas'])

    def _cria_dicionario_dados(self, numero_proposicao, descricao_proposicao,
        votos_girondinos, votos_jacobinos, votos_monarquistas):

        dictionary = {}
        dictionary['numero_proposicao']=numero_proposicao
        dictionary['descricao_proposicao']=descricao_proposicao
        dictionary['votos_girondinos']=votos_girondinos
        dictionary['votos_jacobinos']=votos_jacobinos
        dictionary['votos_monarquistas']=votos_monarquistas

        return dictionary

    def _gera_informacoes(self):

        votos_sim = [models.SIM, models.SIM, models.SIM]
        votos_nao = [models.NAO, models.NAO, models.NAO]
        votos_sim_abs_nao = [models.SIM, models.ABSTENCAO, models.NAO]
        votos_sim_sim_abs =[models.SIM, models.SIM, models.ABSTENCAO]
        votos_sim_ause_sim = [models.SIM, models.AUSENTE, models.SIM]

        self._gera_dados(self._cria_dicionario_dados('1', 'Reforma agrária',
            votos_sim_abs_nao,votos_sim, votos_nao))
        self._gera_dados(self._cria_dicionario_dados('2', 'Aumento da pensão dos nobres',
            votos_nao, votos_nao, votos_sim))
        self._gera_dados(self._cria_dicionario_dados('3', 'Institui o Dia de Carlos Magno',
            [models.NAO, models.NAO, models.SIM], votos_nao, votos_sim))
        self._gera_dados(self._cria_dicionario_dados('4', 'Diminuição de impostos sobre a indústria',
            votos_sim, votos_sim_abs_nao, [models.SIM, models.NAO, models.AUSENTE]))
        self._gera_dados(self._cria_dicionario_dados('5', 'Guilhotinar o Conde Pierre',
            votos_sim_sim_abs, votos_sim, votos_nao))
        self._gera_dados(self._cria_dicionario_dados('6', 'Criação de novas escolas', 
            votos_sim, votos_sim, [models.AUSENTE, models.SIM, models.SIM]))
        self._gera_dados(self._cria_dicionario_dados('7', 'Aumento do efetivo militar',
            votos_sim_sim_abs, votos_sim, votos_sim_ause_sim))
        self._gera_dados(self._cria_dicionario_dados('9', 'Contratar médicos para a capital',
            votos_sim_sim_abs, votos_sim, votos_sim_ause_sim))

    # votação com atributos diferentes para teste
    def _gera_dados_customizados(self):

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

    def importar(self):
        self.casa = self._gera_casa_legislativa()
        self._gera_partidos()
        self._gera_parlamentares()
        self._gera_informacoes()
        self._gera_dados_customizados()
        self._gera_proposicao('10', 'Legalizacao da maconha')


def main():

    logger.info('IMPORTANDO DADOS DA CONVENÇÃO NACIONAL FRANCESA')
    importer = ImportadorConvencao()
    importer.importar()
