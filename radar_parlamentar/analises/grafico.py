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
import json
import logging
from math import sqrt

logger = logging.getLogger("radar")

class JsonAnaliseGenerator:
    """Classe que gera o Json da Analise"""
    
    def __init__(self, analise_temporal):
        self.CONSTANTE_ESCALA_TAMANHO = 120
        self.analise_temporal = analise_temporal
        self.escala_periodo = None
        self.json = None
        self.max_r2 = 0
        
    def get_json(self):
        if not self.json:
            self._cria_json()
        return self.json
    
    def _cria_json(self):
        
        logger.info('Gerando json')
        casa_legislativa = self.analise_temporal.casa_legislativa

        self.json = '{"geral":{"CasaLegislativa":{'
        self.json += '"nome":"' + casa_legislativa.nome + '",'
        self.json += '"nome_curto":"' + casa_legislativa.nome_curto + '",'
        self.json += '"esfera":"' + casa_legislativa.esfera + '",'
        self.json += '"local":"' + casa_legislativa.local + '",'
        self.json += '"atualizacao":"' + unicode(casa_legislativa.atualizacao) + '"'
        self.json += "}," # fecha casa legislativa
        self.escala_periodo = self.CONSTANTE_ESCALA_TAMANHO**2. / max(1,self.analise_temporal.area_total)
        escala_20px = 20**2. * (1./max(1,self.escala_periodo)) # numero de parlamentares representado
                                                # por um circulo de raio 20 pixels.
        self.json += '"escala_tamanho":' + str(round(escala_20px,5)) + ','
        self.json += '"filtro_partidos":null,'
        self.json += '"filtro_votacoes":null},' # fecha bloco "geral"
        self.json += '"periodos":['
        
        for ap in self.analise_temporal.analises_periodo:
            self.json += '{' # abre periodo
            self.json += '"nvotacoes":' + str(ap.num_votacoes) + ','
            self.json += '"nome":"' + ap.periodo.string + '",'
            var_explicada = round((ap.pca.eigen[0] + ap.pca.eigen[1])/ap.pca.eigen.sum() * 100,1)
            self.json += '"var_explicada":' + str(var_explicada) + ","
            try:
                self.json += '"cp1":{"theta":' + str(round(ap.theta,0)%180) + ','
            except AttributeError:
                self.json += '"cp1":{"theta":0,'           
            var_explicada = round(ap.pca.eigen[0]/ap.pca.eigen.sum() * 100,1)
            self.json += '"var_explicada":' + str(var_explicada) + ","
            self.json += '"composicao":' + str([round(el,2) for el in 100*ap.pca.Vt[0,:]**2]) + "}," # fecha cp1
            try:
                self.json += '"cp2":{"theta":' + str(round(ap.theta,0)%180 + 90) + ','
            except AttributeError:
                self.json += '"cp2":{"theta":0,'
            var_explicada = str(round(ap.pca.eigen[1]/ap.pca.eigen.sum() * 100,1))
            self.json += '"var_explicada":' + str(var_explicada) + ","
            self.json += '"composicao":' + str([round(el,2) for el in 100*ap.pca.Vt[1,:]**2]) + "}," # fecha cp2
            self.json += '"votacoes":' # deve trazer a lista de votacoes do periodo
                                        # na mesma ordem apresentada nos vetores
                                        # composicao das componentes principais.
            lista_votacoes = []
            for votacao in ap.votacoes:
                lista_votacoes.append({"id":unicode(votacao).replace('"',"'")})
            self.json += json.dumps(lista_votacoes)
            self.json += ' },' # fecha lista de votações e fecha período
            
        self.json = self.json[0:-1] # apaga última vírgula
        self.json += '],' # fecha lista de períodos
        self.json += '"partidos":' + self._list_partidos()
        self.json += ', "max_raio":' + str(round(sqrt(self.max_r2), 1))
        self.json += ' }' 

    def _list_partidos(self):
        list_partidos = []
        partidos = self.analise_temporal.casa_legislativa.partidos().select_related('nome','numero','cor')
        for partido in partidos: #  self.analise_temporal.analises_periodo[0].partidos:
            list_partidos.append(self._dict_partido(partido))
        return json.dumps(list_partidos)

    def _sem_ultima_virgula(self, json):
        return json[0:-1]
        
    def _dict_partido(self, partido):
        dict_partido = {"nome":partido.nome ,"numero":partido.numero,"cor":partido.cor}
        dict_partido["t"] =  []
        dict_partido["r"] =  []
        dict_partido["x"] =  []
        dict_partido["y"] =  []
        for ap in self.analise_temporal.analises_periodo:
            scaler = GraphScaler()
            coordenadas = scaler.scale(ap.coordenadas_partidos)
            try:
                dict_partido["x"].append(round(coordenadas[partido][0],2))
                dict_partido["y"].append(round(coordenadas[partido][1],2))
            except KeyError:
                dict_partido["x"].append(0.)
                dict_partido["y"].append(0.)
            t = ap.tamanhos_partidos[partido]
            dict_partido["t"].append(t)
            r = sqrt(t*self.escala_periodo)
            dict_partido["r"].append(round(r,1))
        dict_partido["parlamentares"] = []
        legislaturas = self.analise_temporal.analises_periodo[0].legislaturas_por_partido[partido.nome]
        #legislaturas = self.analise_temporal.casa_legislativa.legislaturas().filter(partido=partido).select_related('id', 'partido__nome')
        for leg in legislaturas:
            dict_partido["parlamentares"].append(self._dict_parlamentar(leg))
        return dict_partido
    
    def _dict_parlamentar(self, legislatura):
        leg_id = legislatura.id
        nome = legislatura.parlamentar.nome
        dict_parlamentar = {"nome":nome, "id":leg_id}
        dict_parlamentar["x"] =  []
        dict_parlamentar["y"] =  []     
        for ap in self.analise_temporal.analises_periodo:
            scaler = GraphScaler()
            coordenadas = scaler.scale(ap.coordenadas_legislaturas)
            if coordenadas.has_key(leg_id):
                x = coordenadas[leg_id][0]
                y = coordenadas[leg_id][1]
                dict_parlamentar["x"].append(round(x,2))
                dict_parlamentar["y"].append(round(y,2))
                r2 = x**2 + y**2
                self.max_r2 = max(self.max_r2, r2)
            else:
                dict_parlamentar["x"].append(None)
                dict_parlamentar["y"].append(None)
        return dict_parlamentar

    

class GraphScaler:

    def scale(self, partidos2d):
        """Recebe mapa de coordenadas de partidos (saída de analise.partidos_2d()
        e altera a escala dos valores de [-1,1] para [-100,100]
        """
        scaled = {}
        for partido, coord in partidos2d.items():
            x, y = coord[0], coord[1]
            if x < -1 or x > 1 or y < -1 or y > 1:
                raise ValueError("Value should be in [-1,1]")
            scaled[partido] = [x*100, y*100]
        return scaled



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

        lista_cores_partidos = []
        for partido in self.analise.partidos:
            if partido.cor:
                lista_cores_partidos.append(partido.cor)
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

