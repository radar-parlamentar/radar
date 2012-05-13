#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, Leonardo Leite, Diego Rabatone
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

import svgwrite
import re, math
import analise

class Grafico:
    """Desenha o gráfico SVG baseado nas coordenadas fornecidas"""

    # or parâmetros são os valores extremos obtidos no PCA
    def __init__(self, top, bottom, left, right):
        self.radius = 6
        self.factor = 400 # ajusta distância entre circunferências
        #self.pagefactor = 600
        self.offset = (-left*self.factor + 2*self.radius, -bottom*self.factor + 2*self.radius) # ajusta posição (obs, se valores são positivos, offset deveria ser ZERO)
        self.width = (right - left)*self.factor + 4*self.radius
        self.height = (top - bottom)*self.factor + 4*self.radius
        self.svg = svgwrite.Drawing(filename="resultados/grafico.svg", size = ("%fpx" % self.width, "%fpx" % self.height))

    def add_partido(self, nome, center):

        # preparação das coordenadas para uma melhor distribuição visual
        x = center[0]*self.factor + self.offset[0]
        y = center[1]*self.factor + self.offset[1]
        center = (x, y)
        # a ideia é que a intensidade seja um valor entre 0 e 255, em hexadecimal
        intensidade = hex(int(abs(y) % 255))[2:]
        cor='#'
        #deve-se encontrar qual a linha divisória entre "direita e esquerda", é o valor do '620'.
        if y < 620:
            cor += intensidade
            cor += "0000"
        else:
            cor += "0000"
            cor += intensidade
        self.svg.add(self.svg.circle(center=center, r=self.radius, fill_opacity='0.5', stroke='black', stroke_width='1'))
        text = self.svg.text(nome, insert=center, text_anchor='middle', font_family='LMMono10', font_size='6', alignment_baseline='middle')
        self.svg.add(text)
        self.svg.save()
    


# parseia o arquivo resultados/pca.txt pra gerar o mapa partido => coordenadas do gráfico
def parse_from_file():

    mapa = {}
    name = 'resultados/pca.txt'
    vfile = open(name, 'r')
    regexp = '^([a-zA-Z]*?): (.*)'
    for line in vfile:
        res = re.search(regexp, line)
        if res:
            mapa[res.group(1)] = eval(res.group(2))
    return mapa

# preparacão semântica das coordenadas
# inverte os eixos do gráfico oriundo do PCA
# o que faz com que esquerda/direita fique no eixo orizontal
# e situacão/oposicão no eixo vertical
def muda_eixos(partidos):
    for part, coord in partidos.items():
        partidos[part] = (coord[1], coord[0])

# encontra extremos do gráfico
def extremos(dados):
    top = bottom = left = right = 0
    for partido in dados.keys():
        coord=dados[partido]
        if coord[0] > right:
            right = coord[0] 
        if coord[0] < left:
            left = coord[0] 
        if coord[1] > top:
            top = coord[1] 
        if coord[1] < bottom:
            bottom = coord[1]

    return top, bottom, left, right 

def numero_part(analise, nomePartido):
    # meio feio =/
    for part in analise.partidos:
        if nomePartido == part.nome:
            return part.numero

if __name__ == "__main__":

    analise = analise.Analise()
    dados = analise.partidos_2d()
    #invertendo eixo y das coordenadas
    for partido in dados:
        dados[partido][1]=-dados[partido][1]
    top, bottom, left, right = extremos(dados)

    # desenha a página do gráfico
    grafico = Grafico(top, bottom, left, right)
    # desenha as bolinhas dos partidos no gráfico
    for part, coord in dados.items():
        grafico.add_partido(numero_part(analise,part), (coord[0], coord[1]))

