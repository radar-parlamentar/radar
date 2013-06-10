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
from sets import Set
from modelagem import models
from numpy import sqrt
import json
from json import encoder
import logging
import analise

logger = logging.getLogger("radar")

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
    """
    Classe que gera o Json da Analise
    """

    @staticmethod
    def _get_analises(casa_legislativa):
        """
        importa os dados da analise
        """
        analisador_temporal = analise.AnalisadorTemporal(casa_legislativa)
        analisador_temporal.get_analises()
        return analisador_temporal
    
    @staticmethod
    def inicia_dicionario(key,lista):
        if key not in lista:
            lista[key] = []

    def _json_partidos_config(self,partidos2d,partidos, tamanhos,escala_tamanhos,analises_len,periodo,analisador,xs,ys):
            """
            preenche a lista de tamanhos, xs e ys para serem utilizadas no json dos partidos
            """
            for p in partidos:
                JsonAnaliseGenerator.inicia_dicionario(p,tamanhos)
                JsonAnaliseGenerator.inicia_dicionario(p,xs)
                JsonAnaliseGenerator.inicia_dicionario(p,ys)
            for partido in partidos2d.keys():
                tamanhos[partido].append([periodo, round(analisador.tamanhos_partidos[partido]/escala_tamanhos,1)])
                xs[partido].append([periodo, round(partidos2d[partido][0],2)])
                ys[partido].append([periodo, round(partidos2d[partido][1],2)])

   
    def _json_partidos(self,analise,analises_len):
        """
        constroi o json dos partidos
        """
        tamanhos = {}
        xs = {}
        ys = {}
        partidos = Set()
        scaler = GraphScaler()
        periodo = 0
        analises = analise.analisadores_periodo
        constante_escala_tamanho = 26 # quanto maior, maior serão as bolhas.
        escala_tamanhos = sqrt(analise.area_total) / constante_escala_tamanho
        if escala_tamanhos < 0.0001: # quero evitar divisões por zero
            logger.info("Atenção: Fator de escala fixado em 1, pois %f seria muito baixo." %escala_tamanhos)
            escala_tamanhos = 1
        for analisador in analises:
            periodo +=1
            partidos2d = scaler.scale(analisador.partidos_2d())
            partidos.update(set(partidos2d.keys()))
            self._json_partidos_config(partidos2d,partidos, tamanhos,escala_tamanhos,analises_len,periodo,analisador,xs,ys)
        json_partidos = []
        for nome_partido in partidos:
            partido = models.Partido.objects.get(nome=nome_partido)
            json_partido = {"nome": nome_partido,"numero":partido.numero,"cor":"#000000","tamanho":tamanhos[nome_partido],"x":xs[nome_partido]\
            ,"y":ys[nome_partido]}
            json_partidos.append(json_partido)
        return json_partidos

    def _json_periodos(self,analises,analises_len):
        """
        constroi o json dos periodos
        """
        periodo = 0
        json_periodos = {}
        for analisador in analises:
            periodo += 1
            json_periodos[str(periodo)] = {"nome":unicode(analisador.periodo),"quantidade_votacoes":analisador.num_votacoes}
        return json_periodos

    def get_json(self, casa_legislativa):
        """Retorna JSON para ser usado no gráfico"""
        encoder.FLOAT_REPR = lambda o:format(o,'.2f')
        return json.dumps(self.get_json_dic(casa_legislativa),separators=(",",":"))
    
    def get_json_dic(self,casa_legislativa):
        """Retorna o dicionario usado para gerar o JSON"""
        analise = JsonAnaliseGenerator._get_analises(casa_legislativa)
        analises = analise.analisadores_periodo
        analises_len = len(analises)
        json_periodos = self._json_periodos(analises,analises_len)
        json_partidos = self._json_partidos(analise,analises_len)
        return {"periodos":json_periodos,"partidos":json_partidos} 


class CorPartido:
    """Associa uma cor a um partido"""
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
    @staticmethod
    def cor(partido):
        """Recebe um objeto tipo partido e retorna uma cor. Retorna #000000 (preto) se não estiver na lista."""
        try:
            return CorPartido.cores_partidos[partido.nome]
        except KeyError:
            return "#000000"

class GeradorGrafico:
    """Gera imagem com o gráfico estático da análise utilizando matplotlib"""

    def __init__(self, analise):
        self.analise = analise

    def figura(self, escala=10, print_nome=False):
        from matplotlib.pyplot import figure, show, scatter, text
        import matplotlib.colors
        import numpy
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

