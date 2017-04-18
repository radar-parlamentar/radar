# !/usr/bin/python
# coding=utf8

# Copyright (C) 2016, Leonardo Leite
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

"""Exportação para CSV com o objetivo de criar uma base de dados com schema simplificado para análises ad-hoc."""

import os
import csv
from modelagem import models
from django.utils.dateparse import parse_datetime
import logging
logger = logging.getLogger("radar")

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))

NORTE = 'Norte'
NORDESTE = 'Nordeste'
CENTRO_OESTE = 'CentroOeste'
SUDESTE = 'Sudeste'
SUL =  'Sul'

REGIAO_POR_UF = {
  'AC' : NORTE,
  'AL' : NORDESTE,
  'AP' : NORTE,
  'AM' : NORTE,
  'BA' : NORDESTE,
  'CE' : NORDESTE,
  'DF' : CENTRO_OESTE,
  'ES' : SUDESTE,
  'GO' : CENTRO_OESTE,
  'MA' : NORTE,
  'MT' : CENTRO_OESTE,
  'MS' : CENTRO_OESTE,
  'MG' : SUDESTE,
  'PA' : NORTE,
  'PB' : NORDESTE,
  'PR' : SUL,
  'PE' : NORDESTE,
  'PI' : NORDESTE,
  'RJ' : SUDESTE,
  'RN' : NORTE,
  'RS' : SUL,
  'RO' : NORTE,
  'RR' : NORTE,
  'SC' : NORTE,
  'SP' : SUDESTE,
  'SE' : NORDESTE,
  'TO' : NORTE 
}

PROPOSICAO = 'PROPOSICAO'
VOTACAO = 'VOTACAO'
PARLAMENTAR_ID = 'PARLAMENTAR_ID'
PARLAMENTAR_NOME = 'PARLAMENTAR_NOME'
PARTIDO = 'PARTIDO'
UF = 'UF'
REGIAO = 'REGIAO'
VOTO = 'VOTO'

LABELS = [PROPOSICAO, VOTACAO, PARLAMENTAR_ID, PARLAMENTAR_NOME, PARTIDO, UF, REGIAO, VOTO]

CSV_FILE = 'votacoes.csv'


class ExportadorCSV:

    def __init__(self, votacoes):
        self.votacoes = votacoes
        self.csv_rows = []

    def exportar_csv(self):
        self.transform_data()
        self.write_csv()

    def transform_data(self):
        self.csv_rows.append(LABELS)
        for votacao in self.votacoes:
            votos = votacao.votos()
            for voto in votos:
                parlamentar = voto.parlamentar
                partido = parlamentar.partido
                csv_row = []
                csv_row.append(votacao.proposicao.nome())
                csv_row.append(votacao.id)
                csv_row.append(parlamentar.id)
                csv_row.append(parlamentar.nome.encode('UTF-8'))
                csv_row.append(partido.nome)
                csv_row.append(parlamentar.localidade)
                csv_row.append(REGIAO_POR_UF[parlamentar.localidade])
                csv_row.append(voto.opcao)
                self.csv_rows.append(csv_row)

    def write_csv(self):
        filepath = os.path.join(MODULE_DIR, 'saida', CSV_FILE)
        with open(filepath, 'wb') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(self.csv_rows)


def main():
    print((models.CasaLegislativa))
    try:
      cdep = models.CasaLegislativa.objects.get(nome_curto='cdep')
    except models.CasaLegislativa.DoesNotExist:
      cdep = None
    try:
      sen = models.CasaLegislativa.objects.get(nome_curto='sen')
    except models.CasaLegislativa.DoesNotExist:
      sen = None
    vs1 = models.Votacao.objects.filter(proposicao__casa_legislativa=cdep, proposicao__sigla='PL', proposicao__numero='1876', proposicao__ano='1999')
    vs2 = models.Votacao.objects.filter(proposicao__casa_legislativa=sen, proposicao__sigla='PLC', proposicao__numero='00007', proposicao__ano='2010')
    vs3 = models.Votacao.objects.filter(proposicao__casa_legislativa=sen, proposicao__sigla='PEC', proposicao__numero='00007', proposicao__ano='2015')
    votacoes = vs1 | vs2 | vs3
    exportador = ExportadorCSV(votacoes)
    exportador.exportar_csv()




