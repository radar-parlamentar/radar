#!/usr/bin/python
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

"""Módulo gráfico

Responsável por cuidar das coisas relacionadas à apresentação do PCA para o usuário final,
dado que os cálculos do PCA já foram realizados
"""

from __future__ import unicode_literals
from matplotlib.pyplot import figure, show, scatter, text
import matplotlib.colors
import numpy

class GeradorGrafico:
    """Gera imagem com o gráfico estático da análise utilizando matplotlib"""

    def __init__(self, analise):
        self.analise = analise

    def figura(self, escala=10, print_nome=False):
        """Apresenta o gráfico da análise na tela.

		O gráfico é gerado utilizando o matplotlib. 
		O primeiro componente principal no eixo x e o segundo no eixo y.
        
        Argumentos:
            escala: afeta tamanho das circunferências
            print_nome: se False imprime números dos partidos, se True imprime nomes dos partidos
        """

        dados = self.analise.coordenadas 

        if not self.analise.coordenadas:
            dados = self.analisep.artidos_2d()

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
        for partido in self.analise.partidos:
            if partido.nome in cores_partidos:
                lista_cores_partidos.append(cores_partidos[partido.nome])
            else:
                lista_cores_partidos.append((1,1,1))

        colormap_partidos = matplotlib.colors.ListedColormap(lista_cores_partidos,name='partidos')

        fig.add_subplot(111, autoscale_on=True) #, xlim=(-1,5), ylim=(-5,3))
        x = []
        y = []
        tamanhos = []
        for partido in self.analise.partidos:
            x.append(dados[partido.nome][0])
            y.append(dados[partido.nome][1])
            tamanhos.append(self.analise.tamanhos_partidos[partido.nome])
        size = numpy.array(tamanhos) * escala * 3
        scatter(x, y, size, range(len(x)), marker='o', cmap=colormap_partidos) #, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, faceted=True, verts=None, hold=None, **kwargs)

        for partido in self.analise.partidos:
            legenda = partido.nome if print_nome else partido.numero
            text(dados[partido.nome][0]+.005,dados[partido.nome][1],legenda,fontsize=12,stretch=100,alpha=1)

        show()

