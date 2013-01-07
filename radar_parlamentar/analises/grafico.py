#!/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Saulo Trento, Diego Rabatone
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

"""Módulo gráfico

Responsável por cuidar das coisas relacionadas à apresentação do PCA para o usuário final,
dado que os cálculos do PCA já foram realizados
"""

from __future__ import unicode_literals
from matplotlib.pyplot import figure, show, scatter, text
import matplotlib.colors
import numpy
from sets import Set
from analises import analise
from modelagem import models

class GraphScaler:
    
    def scale(self, partidos2d):
        """Recebe mapa de coordenadas de partidos (saída de analise.partidos_2d()
        e altera a escala dos valores de [-1,1] para [0,100] 
        """
        scaled = {}
        for partido, coord in partidos2d.items():
            x, y = coord[0], coord[1]
            if x < -1 or x > 1 or y < -1 or y > 1:
                raise ValueError("Value should be in [-1,1]")
            scaled[partido] = [x*50+50, y*50+50]
        return scaled
    
class JsonAnaliseGenerator:
    
    def _pair_to_json_list(self, a, b, periodo, size):
        if (periodo < size):
            end = ', '
        else:
            end = ''
        return '[%s,%s]%s' % (a, b, end)       

    def get_json(self, casa_legislativa):
        """Retorna JSON para ser usado no gráfico"""

        analisador_temporal = analise.AnalisadorTemporal(casa_legislativa)
        analisador_temporal._faz_analises()

        scaler = GraphScaler()
        tamanhos = {}
        xs = {}
        ys = {}
        partidos = Set()
        periodo = 0
        json_periodos = '"periodos":{ '
        analises = analisador_temporal.analisadores_periodo
        for analisador in analises:
            periodo += 1
            json_periodos += '"%s":"%s"' % (periodo, analisador.periodo)
            if periodo != len(analises):
                json_periodos += ', ' 
            partidos2d = scaler.scale(analisador.partidos_2d())
            for partido in partidos2d.keys():
                partidos.add(partido)
                if not tamanhos.has_key(partido):
                    tamanhos[partido] = self._pair_to_json_list(periodo, analisador.tamanhos_partidos[partido], periodo, len(analises)) 
                else:
                    tamanhos[partido] = tamanhos[partido] +  self._pair_to_json_list(periodo, analisador.tamanhos_partidos[partido], periodo, len(analises))  
                if not xs.has_key(partido):
                    xs[partido] = self._pair_to_json_list(periodo, '%.2f' % partidos2d[partido][0], periodo, len(analises)) 
                else:
                    xs[partido] = xs[partido] +  self._pair_to_json_list(periodo, '%.2f' % partidos2d[partido][0], periodo, len(analises))  
                if not ys.has_key(partido):
                    ys[partido] =  self._pair_to_json_list(periodo, '%.2f' % partidos2d[partido][1], periodo, len(analises))  
                else:
                    ys[partido] = ys[partido] +  self._pair_to_json_list(periodo, '%.2f' % partidos2d[partido][1], periodo, len(analises)) 
        
        json_periodos += ' }'    
        
        json_partidos = '"partidos":[ '
        count = 1;
        for nome_partido in partidos:
            partido = models.Partido.objects.get(nome=nome_partido)
            json_partidos += '{ "nome":"%s", "numero":%d, "cor":"#000000", ' % (nome_partido, partido.numero)
            json_partidos += '"tamanho":[ %s ], ' % tamanhos[nome_partido]             
            json_partidos += '"x":[ %s ], ' % xs[nome_partido] 
            json_partidos += '"y":[ %s ] ' % ys[nome_partido] 
            json_partidos += '}'
            if count < len(partidos):
                json_partidos += ', '
            count += 1
        json_partidos += ' ]'

        return '{ %s, %s }'% (json_periodos, json_partidos)
        

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

