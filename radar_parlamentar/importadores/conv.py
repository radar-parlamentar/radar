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
import json
import os

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
ARQUIVO = os.path.dirname(__file__)


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

    def _gera_proposicao(self, num, descricao, indexacao_ementa_dict=None):
        prop = models.Proposicao()
        prop.id_prop = num
        prop.sigla = 'PL'
        prop.numero = num
        prop.descricao = descricao
        prop.casa_legislativa = self.casa
        prop.ementa = descricao
        if indexacao_ementa_dict is not None:
            prop.indexacao = indexacao_ementa_dict.get("indexacao")
            prop.ementa = indexacao_ementa_dict.get("ementa")
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

    def _obtem_dados_json(self):
        data = None
        with open(os.path.join(ARQUIVO, 'votacoes.json')) as arquivo:
            data = json.load(arquivo)
        if data is None:
            data = {"votacao_params": {}}
        return data

    def _gera_votacao_geral(self):
        data = self._obtem_dados_json()
        votacoes_params = data.get("votacoes_params")
        for index, valor in enumerate(votacoes_params):
            numero_prop = str(index+1)
            descricao_prop = valor["descricao"]
            prop = valor.get("prop")
            if prop is not None:
                valor_prop = valor.get("prop")
                descricao = valor_prop.get("descricao_extra")
                indexacao_ementa_dict = {
                   "indexacao": valor_prop.get("indexacao"),
                   "ementa":  valor_prop.get("ementa")}
                prop = self._gera_proposicao(
                    numero_prop,
                    descricao,
                    indexacao_ementa_dict)
            else:
                prop = self._gera_proposicao(numero_prop, descricao_prop)
            votacao = self._gera_votacao(
                numero_prop,
                descricao_prop,
                DATA_NO_PRIMEIRO_SEMESTRE, prop)
            partidos = valor["partidos"]
            for partido, votos in partidos.items():
                self._gera_votos(votacao, partido, votos)

    def importar(self):
        self.casa = self._gera_casa_legislativa()
        self._gera_partidos()
        self._gera_parlamentares()
        self._gera_votacao_geral()
        self._gera_proposicao('10', 'Legalizacao da maconha')


def main():

    logger.info('IMPORTANDO DADOS DA CONVENÇÃO NACIONAL FRANCESA')
    importer = ImportadorConvencao()
    importer.importar()
