# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Saulo Trento, Diego Rabatone
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Módulo analise"""

import re
import numpy
import pca
import sys
from django.utils.dateparse import parse_datetime
from modelagem import models


class Analise:

    def __init__(self):

        # pega votações do banco de dados
        self.votacoes = models.Votacao.objects.all() 
        self.partidos = models.Partido.objects.all()
        self.num_votacoes = len(self.votacoes)

    def _inicializa_vetores(self):
        """ Cria os 'vetores de votação' para cada partido. 
            O 'vetor' usa um número entre -1 (não) e 1 (sim) para representar a "posição média" do partido em cada votação, 
            tendo N dimensões correspondentes às N votações.
            Aproveita para calcular o tamanho dos partidos, presença dos parlamentares, etc.

            Retorna a 'matriz de votações', em que cada linha é um vetor de votações de um partido 
            A ordenação das linhas segue a ordem de self.partidos
        """

        # numpy.zeros((n,m)) gera matriz
        self.vetores_votacao = numpy.zeros((len(self.partidos), self.num_votacoes))
        self.debug = numpy.zeros(self.num_votacoes)

        iv =-1
        for v in self.votacoes:
            iv += 1
            self.debug[iv] = v.id_vot
            mapa_votos = v.por_partido() # mapa: chave é nome do partido, e valor é VotoPartido
            ip =-1
            for p in self.partidos:
                ip += 1
                if mapa_votos.has_key(p.nome):
                    votoPartido = mapa_votos[p.nome] # models.VotoPartido
                    self.vetores_votacao[ip][iv] = (float(votoPartido.sim) - float(votoPartido.nao)) / float(votoPartido.total())
                else:
                    self.vetores_votacao[ip][iv] = 0

        return self.vetores_votacao


#    def _pca_partido(self):

#    def partidos_2d(self):
#        """Retorna matriz com as coordenadas dos partidos no plano 2d formado pelas duas primeiras componentes principais."""



