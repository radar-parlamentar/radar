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

import numpy
import pca
from django.utils.dateparse import parse_datetime
from django.db import connection
from modelagem import models
from matplotlib.pyplot import figure, show, scatter,text
from matplotlib.patches import Ellipse
import matplotlib.colors


class Analise:

    def __init__(self):

        # pega votações do banco de dados
        self.votacoes = models.Votacao.objects.all() 
        self.partidos = models.Partido.objects.all()
        self.num_votacoes = len(self.votacoes)
        self.vetores_votacao = []
        self.pca_partido = []
        self.tamanhos_partidos = {}

    def _inicializa_tamanhos_partidos(self):
        """Retorna um dicionário cuja chave é o nome do partido, e o valor é a quantidade de parlamentares do partido no banco.

        Este dicionário é também salvo no atributo self.mapa_tamanho_partidos
        """
        self.tamanho_partidos = {}
        cursor = connection.cursor()
        for partido in self.partidos:
            # a linha comentada é mais django e mais portável, mas acho que a usada deve ser bem mais eficiente, 
            # pois não precisamos carregar os objetos
            # parlamentares = models.Parlamentar.objects.filter(partido=partido)
            # tamanho = len(parlamentares)
            cursor.execute("SELECT count(id) FROM modelagem_parlamentar WHERE partido_id = %s", [partido.id])
            tamanho = cursor.fetchone()[0]
            self.tamanhos_partidos[partido.nome] = tamanho
        return self.tamanhos_partidos

    def _inicializa_vetores(self):
        """Cria os 'vetores de votação' para cada partido. 

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


    def _pca_partido(self):
        """Roda a análise de componentes principais por partidos.

        Guarda o resultado em self.pca
        Retorna um dicionário no qual as chaves são as siglas dos partidos
        e o valor de cada chave é um vetor com as n dimensões da análise pca
        """
        if not self.pca_partido:
            if not self.vetores_votacao:
                self._inicializa_vetores()
            matriz = self.vetores_votacao - self.vetores_votacao.mean(axis=0)
            self.pca_partido = pca.PCA(matriz)

        dicionario = {}
        for partido, vetor in zip(self.partidos, self.pca_partido.U):
            dicionario[partido.nome] = vetor
        return dicionario


    def partidos_2d(self):
        """Retorna mapa com as coordenadas dos partidos no plano 2D formado pelas duas primeiras componentes principais.

        A chave do mapa é o nome do partido (string) e o valor é uma lista de duas posições [x,y].
        """

        coordenadas = self._pca_partido()
        for partido in coordenadas.keys():
            coordenadas[partido] = (coordenadas[partido])[0:2]
        return coordenadas


    def figura(self, escala=10):
        """Apresenta um plot de bolhas (usando matplotlib) com os partidos de tamanho maior ou igual a tamanho_min com o primeiro componente principal no eixo x e o segundo no eixo y.
        """

        if not self.tamanhos_partidos:
            self._inicializa_tamanhos_partidos()
        dados = self.partidos_2d()

        fig = figure(1)
        fig.clf()

        cores_partidos = {'PT'   :'#FF0000',
                      'PSOL' :'#FFFF00',
                      'PV'   :'#00CC00',
                      'DEM'  :'#002664',
                      'PSDB' :'#0059AB',
                      'PSD'  :'#80c341',
                      'PMDB' :'#CC0000',
                      'PR'   :'#110274',
                      'PSC'  :'#25b84a',
                      'PSB'  :'#ff8d00',
                      'PP'   :'#203487',
                      'PCdoB':'#da251c',
                      'PTB'  :'#1f1a17',
                      'PPS'  :'#fea801',
                      'PDT'  :'#6c85b1',
                      'PRB'  :'#67a91e'}

        lista_cores_partidos = []
        for partido in self.partidos:
            if partido.nome in cores_partidos:
                lista_cores_partidos.append(cores_partidos[partido.nome])
            else:
                lista_cores_partidos.append((1,1,1))

        colormap_partidos = matplotlib.colors.ListedColormap(lista_cores_partidos,name='partidos')

        ax = fig.add_subplot(111, autoscale_on=True) #, xlim=(-1,5), ylim=(-5,3))
        x = []
        y = []
        tamanhos = []
        for partido in self.partidos:
            x.append(dados[partido.nome][0])
            y.append(dados[partido.nome][1])
            tamanhos.append(self.tamanhos_partidos[partido.nome])
        size = numpy.array(tamanhos) * escala * 3
        scatter(x, y, size, range(len(x)), marker='o', cmap=colormap_partidos) #, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, faceted=True, verts=None, hold=None, **kwargs)

        for partido in self.partidos:
            text(dados[partido.nome][0]+.005,dados[partido.nome][1],partido.numero,fontsize=12,stretch=100,alpha=1)

        show()

