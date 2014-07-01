# !/usr/bin/python
# coding=utf8

# Copyright (C) 2013, Leonardo Leite
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

"""Exportação para CSV para nossas análises no R.
   Para ler o arquivo csv no R: read.csv('votes.csv', sep=',', as.is=T)
   O último argumento impede que as strings sejam importadas como "factors".
"""

import os
import csv
from modelagem import models
from django.utils.dateparse import parse_datetime
import logging
logger = logging.getLogger("radar")

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))

COALITION_PARTIES = ['PT', 'PCdoB', 'PSB', 'PP', 'PMDB', 'PTB']
# PR, PDT não são coalition?

ROLLCALL = 'rollcall'
VOTER_ID = 'voter_id'
NAME = 'name'
PARTY = 'party'
COALITION = 'coalition'
VOTE = 'vote'

LABELS = [ROLLCALL, VOTER_ID, NAME, PARTY, COALITION, VOTE]

CSV_FILE = 'votes.csv'


class ExportadorCSV:

    def __init__(self, nome_curto_casa_legislativa, data_ini, data_fim):
        self.nome_curto = nome_curto_casa_legislativa
        self.ini = data_ini
        self.fim = data_fim
        self.votacoes = None
        self.csv_rows = []

    def exportar_csv(self):
        self.retrieve_votacoes()
        self.transform_data()
        self.write_csv()

    def retrieve_votacoes(self):
        casa = models.CasaLegislativa.objects.get(nome_curto=self.nome_curto)
        if self.ini is None and self.fim is None:
            self.votacoes = models.Votacao.objects.filter(
                proposicao__casa_legislativa=casa).order_by('data')
        if self.ini is None and self.fim is not None:
            self.votacoes = models.Votacao.objects.filter(
                proposicao__casa_legislativa=casa
            ).filter(data__lte=self.fim).order_by('data')
        if self.ini is not None and self.fim is None:
            self.votacoes = models.Votacao.objects.filter(
                proposicao__casa_legislativa=casa
            ).filter(data__gte=self.ini).order_by('data')
        if self.ini is not None and self.fim is not None:
            self.votacoes = models.Votacao.objects.filter(
                proposicao__casa_legislativa=casa
            ).filter(data__gte=self.ini, data__lte=self.fim).order_by('data')

    def transform_data(self):
        self.csv_rows.append(LABELS)
        for votacao in self.votacoes:
            votos = votacao.votos()
            for voto in votos:
                legislatura = voto.legislatura
                parlamentar = legislatura.parlamentar
                partido = legislatura.partido
                csv_row = []
                csv_row.append(votacao.id_vot)
                csv_row.append(legislatura.id)
                csv_row.append(parlamentar.nome.encode('UTF-8'))
                csv_row.append(partido.nome)
                csv_row.append(self.coalition(partido.nome))
                try:
                    csv_row.append(self.voto(voto.opcao))
                    self.csv_rows.append(csv_row)
                except:
                    print 'Ignorando voto ', voto.opcao
                    logger.info("Ignorando voto: %s" % voto.opcao)

    def coalition(self, nome_partido):
        return '1' if nome_partido in COALITION_PARTIES else '0'

    def voto(self, opcao):
        if opcao == models.SIM:
            return 1
        elif opcao == models.NAO:
            return -1
        elif opcao == models.ABSTENCAO:
            return 0
        elif opcao == models.OBSTRUCAO:
            return 0
        elif opcao == models.AUSENTE:
            return 0
        else:
            raise ValueError()

    def write_csv(self):
        filepath = os.path.join(MODULE_DIR, 'dados', CSV_FILE)
        with open(filepath, 'wb') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(self.csv_rows)


def main():
    data_ini = parse_datetime('2010-06-09 0:0:0')
    data_fim = parse_datetime('2010-06-09 23:59:0')
    exportador = ExportadorCSV('sen', data_ini, data_fim)
    exportador.exportar_csv()
